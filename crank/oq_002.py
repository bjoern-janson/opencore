from __future__ import annotations

from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
NANO_PATH = Path('/mnt/data/nano_oq2.py')
OQ1_RESULT = Path('/mnt/data/opencore_quantum_oq001/oq_001_result.json')
NANO_SHA256 = '8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329'


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(payload).hexdigest()


def load_nano():
    actual = sha256_file(NANO_PATH)
    if actual != NANO_SHA256:
        raise RuntimeError(f'Nano hash mismatch: {actual}')
    spec = importlib.util.spec_from_file_location('oq002_frozen_nano', NANO_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load Nano')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def profile(p_plus: float) -> str:
    if abs(p_plus - 0.5) < 1e-12:
        return 'HALF'
    if abs(p_plus - 1.0) < 1e-12:
        return 'CERTAIN_PLUS'
    raise ValueError(f'unconstituted profile probability: {p_plus}')


def carrier(mode: str, history: str) -> str:
    if mode == 'coarse':
        return 'event:Z:0'
    if mode == 'complete':
        return f'event:{history}:Z:0'
    raise ValueError(mode)


def profile_key(nano, event_id: str, probe: str):
    return nano.StandingKey(event_id, 'probe-profile', probe)


def output_key(nano, probe: str):
    return nano.StandingKey('history:B:downstream', 'persistent-profile', probe)


def contract_template(probe: str, expected: str, output_value: str) -> dict[str, object]:
    return {
        'operation': 'persist-downstream-profile',
        'precondition': {
            'key_binding': 'CURRENT_EVENT_ID',
            'dimension': 'probe-profile',
            'scope': probe,
            'expected': expected,
        },
        'effect': {
            'object_id': 'history:B:downstream',
            'dimension': 'persistent-profile',
            'scope': probe,
            'value': output_value,
        },
    }


def active_value(nano_kernel, key) -> str | None:
    for standing in nano_kernel.effective_state().active:
        if standing.key == key:
            return standing.value
    return None


def run_branch(nano, *, mode: str, probe: str, truth_A: str, truth_B: str) -> dict[str, object]:
    event_A = carrier(mode, 'A')
    event_B = carrier(mode, 'B')
    key_A = profile_key(nano, event_A, probe)
    key_B = profile_key(nano, event_B, probe)
    out_key = output_key(nano, probe)

    objects = (
        nano.ObjectRecord(event_A, hashlib.sha256(event_A.encode()).hexdigest(), 'OPAQUE_APPARATUS_EVENT'),
        nano.ObjectRecord(event_B, hashlib.sha256(event_B.encode()).hexdigest(), 'OPAQUE_APPARATUS_EVENT'),
        nano.ObjectRecord(out_key.object_id, hashlib.sha256(out_key.object_id.encode()).hexdigest(), 'OPAQUE_PERSISTENT_RESULT'),
    )

    admit_A = nano.License(
        id=f'admit-A-{probe}',
        operation='admit-profile',
        allowed_writes=(nano.WriteGrant(key_A, (truth_A,)),),
    )
    use_half = nano.License(
        id=f'use-half-{probe}',
        operation='persist-downstream-profile',
        preconditions=(nano.Precondition(key_B, 'HALF'),),
        allowed_writes=(nano.WriteGrant(out_key, ('HALF',)),),
    )
    admit_B = nano.License(
        id=f'admit-B-{probe}',
        operation='admit-profile',
        allowed_writes=(nano.WriteGrant(key_B, (truth_B,)),),
    )
    use_truth_B = nano.License(
        id=f'use-truth-B-{probe}',
        operation='persist-downstream-profile',
        preconditions=(nano.Precondition(key_B, truth_B),),
        allowed_writes=(nano.WriteGrant(out_key, (truth_B,)),),
    )

    kernel = nano.Nano(objects=objects, licenses=(admit_A, use_half, admit_B, use_truth_B))

    r_A = kernel.apply_transition(
        nano.Transition('admit-profile', writes=(nano.Standing(key_A, truth_A),)),
        admit_A.id,
    )

    wrong_proposal = nano.Transition(
        'persist-downstream-profile',
        writes=(nano.Standing(out_key, 'HALF'),),
    )
    r_use_before_B = kernel.apply_transition(wrong_proposal, use_half.id)
    persisted_before_B = active_value(kernel, out_key)
    oracle_correct_before_B = persisted_before_B == truth_B if persisted_before_B is not None else None

    # Complete-carrier positive control: constitute the B-specific profile after the
    # first attempt. In the coarse carrier this would overwrite the same aliased key,
    # so we only perform this stage for the complete representation.
    r_B = None
    r_wrong_after_B = None
    r_correct_after_B = None
    persisted_after_B = None
    if mode == 'complete':
        r_B = kernel.apply_transition(
            nano.Transition('admit-profile', writes=(nano.Standing(key_B, truth_B),)),
            admit_B.id,
        )
        r_wrong_after_B = kernel.apply_transition(wrong_proposal, use_half.id)
        correct_proposal = nano.Transition(
            'persist-downstream-profile',
            writes=(nano.Standing(out_key, truth_B),),
        )
        r_correct_after_B = kernel.apply_transition(correct_proposal, use_truth_B.id)
        persisted_after_B = active_value(kernel, out_key)

    return {
        'mode': mode,
        'probe': probe,
        'carrier_A': event_A,
        'carrier_B': event_B,
        'carriers_equal': event_A == event_B,
        'truth_A': truth_A,
        'truth_B': truth_B,
        'contract_template': contract_template(probe, 'HALF', 'HALF'),
        'contract_template_digest': digest_json(contract_template(probe, 'HALF', 'HALF')),
        'A_profile_receipt': asdict(r_A),
        'use_before_B': {
            'receipt': asdict(r_use_before_B),
            'persisted_value': persisted_before_B,
            'oracle_correct': oracle_correct_before_B,
        },
        'B_profile_receipt': asdict(r_B) if r_B else None,
        'wrong_use_after_B': asdict(r_wrong_after_B) if r_wrong_after_B else None,
        'correct_use_after_B': asdict(r_correct_after_B) if r_correct_after_B else None,
        'persisted_after_B': persisted_after_B,
        'final_effective_state': asdict(kernel.effective_state()),
    }


def main() -> int:
    oq1 = json.loads(OQ1_RESULT.read_text())
    if oq1['prospective_result_class'] != 'APPARATUS_EXPRESSIVE_WOUND_ESTABLISHED':
        raise RuntimeError('OQ-001 prerequisite not established')

    x = oq1['downstream']['X_discriminator']
    y = oq1['downstream']['Y_negative_control']
    truth = {
        'X': {'A': profile(x['P_A_plus_given_x0']), 'B': profile(x['P_B_plus_given_x0'])},
        'Y': {'A': profile(y['P_A_plus_given_x0']), 'B': profile(y['P_B_plus_given_x0'])},
    }

    nano_pre = sha256_file(NANO_PATH)
    nano = load_nano()

    branches = {
        f'{mode}_{probe}': run_branch(
            nano,
            mode=mode,
            probe=probe,
            truth_A=truth[probe]['A'],
            truth_B=truth[probe]['B'],
        )
        for mode in ('coarse', 'complete')
        for probe in ('X', 'Y')
    }

    nano_post = sha256_file(NANO_PATH)

    coarse_x = branches['coarse_X']
    complete_x = branches['complete_X']
    coarse_y = branches['coarse_Y']
    complete_y = branches['complete_Y']

    same_x_transition = (
        coarse_x['use_before_B']['receipt']['transition_digest']
        == complete_x['use_before_B']['receipt']['transition_digest']
    )
    same_y_transition = (
        coarse_y['use_before_B']['receipt']['transition_digest']
        == complete_y['use_before_B']['receipt']['transition_digest']
    )

    checks = {
        'nano_unchanged': nano_pre == nano_post == NANO_SHA256,
        'coarse_X_aliases_histories': coarse_x['carriers_equal'],
        'complete_X_distinguishes_histories': not complete_x['carriers_equal'],
        'same_X_downstream_transition_object': same_x_transition,
        'same_Y_downstream_transition_object': same_y_transition,
        'coarse_X_wrong_use_ALLOWED': coarse_x['use_before_B']['receipt']['decision'] == 'ALLOW',
        'coarse_X_wrong_value_persisted': coarse_x['use_before_B']['persisted_value'] == 'HALF',
        'coarse_X_oracle_marks_wrong': coarse_x['use_before_B']['oracle_correct'] is False,
        'coarse_X_authority_parent_is_A_profile': coarse_x['use_before_B']['receipt']['parent_receipts'] == (coarse_x['A_profile_receipt']['id'],),
        'complete_X_before_B_DEFER': complete_x['use_before_B']['receipt']['decision'] == 'DEFER',
        'complete_X_wrong_after_B_DENY': complete_x['wrong_use_after_B']['decision'] == 'DENY',
        'complete_X_correct_after_B_ALLOW': complete_x['correct_use_after_B']['decision'] == 'ALLOW',
        'complete_X_correct_value_persisted': complete_x['persisted_after_B'] == 'CERTAIN_PLUS',
        'coarse_Y_use_ALLOWED': coarse_y['use_before_B']['receipt']['decision'] == 'ALLOW',
        'coarse_Y_oracle_marks_correct': coarse_y['use_before_B']['oracle_correct'] is True,
        'complete_Y_before_B_DEFER': complete_y['use_before_B']['receipt']['decision'] == 'DEFER',
        'complete_Y_after_B_same_use_ALLOW': complete_y['wrong_use_after_B']['decision'] == 'ALLOW',
        'complete_Y_correct_value_persisted': complete_y['persisted_after_B'] == 'HALF',
    }

    if all(checks.values()):
        result_class = 'PERSISTENCE_WOUND_ESTABLISHED'
    else:
        result_class = 'ASSAY_INVALID_OR_UNDERCONSTITUTED'

    result = {
        'experiment': 'OQ-002',
        'title': 'Coarse-carrier persistence pressure',
        'prospective_result_class': result_class,
        'oq001_prerequisite': {
            'result_class': oq1['prospective_result_class'],
            'result_file_sha256': sha256_file(OQ1_RESULT),
            'X_truth': truth['X'],
            'Y_truth': truth['Y'],
        },
        'nano': {
            'sha256_expected': NANO_SHA256,
            'sha256_pre': nano_pre,
            'sha256_post': nano_post,
            'modified': False,
            'source': 'bjoern-janson/opencore:opencore/crank-mini-001/crank/nano.py',
        },
        'manipulated_variable': 'apparatus event identity resolution only',
        'carrier_regimes': {
            'coarse': {'A0': carrier('coarse', 'A'), 'B0': carrier('coarse', 'B')},
            'complete': {'A0': carrier('complete', 'A'), 'B0': carrier('complete', 'B')},
        },
        'branches': branches,
        'checks': checks,
        'earned_claim': (
            'A quantum-mechanically consequence-relevant apparatus distinction, when erased before the persistence boundary, '
            'caused an A-derived standing to satisfy a B-history precondition and authorize a wrong durable X-profile. '
            'Preserving opaque apparatus identity prevented that transfer; the Y control remained harmless under the same aliasing.'
        ),
        'diagnosis': 'persistent-authority wound caused by premature apparatus quotienting upstream of unchanged Nano',
        'not_claimed': [
            'Nano is defective',
            'Nano requires quantum semantics',
            'OpenCore requires a post_state field',
            'instrument identity is a universal OpenCore primitive',
            'quantum hardware result',
            'QuantumNano or QuantumBase is earned',
        ],
    }

    payload = json.dumps(result, sort_keys=True, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x)) + '\n'
    result_path = HERE / 'oq_002_result.json'
    result_path.write_text(payload)
    result_sha = sha256_file(result_path)
    print(result_class)
    print('nano_sha256=', nano_pre)
    print('coarse_X=', coarse_x['use_before_B']['receipt']['decision'], coarse_x['use_before_B']['persisted_value'], 'oracle_correct=', coarse_x['use_before_B']['oracle_correct'])
    print('complete_X_before=', complete_x['use_before_B']['receipt']['decision'])
    print('complete_X_after_wrong=', complete_x['wrong_use_after_B']['decision'])
    print('complete_X_after_correct=', complete_x['correct_use_after_B']['decision'], complete_x['persisted_after_B'])
    print('coarse_Y=', coarse_y['use_before_B']['receipt']['decision'], coarse_y['use_before_B']['persisted_value'], 'oracle_correct=', coarse_y['use_before_B']['oracle_correct'])
    print('coarse_X_parent=', coarse_x['use_before_B']['receipt']['parent_receipts'])
    print('A_profile_receipt=', coarse_x['A_profile_receipt']['id'])
    print('same_X_transition=', same_x_transition)
    print('result_sha256=', result_sha)
    return 0 if result_class == 'PERSISTENCE_WOUND_ESTABLISHED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
