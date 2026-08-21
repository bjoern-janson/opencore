from __future__ import annotations

from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
NANO_PATH = Path('/mnt/data/nano_oq2.py')
NANO_SHA256 = '8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329'
SEED = 3003
TRIALS = 100_000


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(payload).hexdigest()


def load_nano():
    actual = sha256_file(NANO_PATH)
    if actual != NANO_SHA256:
        raise RuntimeError(f'Nano hash mismatch: expected {NANO_SHA256}, got {actual}')
    spec = importlib.util.spec_from_file_location('foreign003_frozen_nano', NANO_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load Nano')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------- classical foreign world ----------
# Both interventions emit x~Bernoulli(1/2). They differ only in the hidden
# classical state left behind: h=0 versus h=1.

def first_outcome_probability(history: str, x: int) -> float:
    if history not in {'A', 'B'} or x not in {0, 1}:
        raise ValueError((history, x))
    return 0.5


def post_state(history: str, x: int) -> dict[str, int]:
    if history == 'A':
        return {'x': x, 'hidden': 0}
    if history == 'B':
        return {'x': x, 'hidden': 1}
    raise ValueError(history)


def targeted_distribution(state: dict[str, int]) -> dict[str, float]:
    # M_X reads the hidden bit exactly.
    if state['hidden'] == 0:
        return {'ZERO': 1.0, 'ONE': 0.0}
    return {'ZERO': 0.0, 'ONE': 1.0}


def control_distribution(state: dict[str, int]) -> dict[str, float]:
    # M_Y intentionally ignores the history-sensitive hidden bit.
    return {'ZERO': 0.5, 'ONE': 0.5}


def profile(dist: dict[str, float]) -> str:
    if dist == {'ZERO': 1.0, 'ONE': 0.0}:
        return 'ZERO'
    if dist == {'ZERO': 0.0, 'ONE': 1.0}:
        return 'ONE'
    if dist == {'ZERO': 0.5, 'ONE': 0.5}:
        return 'HALF'
    raise ValueError(f'unconstituted profile: {dist}')


def monte_carlo_sanity() -> dict[str, object]:
    rng = random.Random(SEED)
    out: dict[str, object] = {}
    for history in ('A', 'B'):
        x0 = 0
        targeted_one = 0
        control_one = 0
        for _ in range(TRIALS):
            x = rng.getrandbits(1)
            if x == 0:
                x0 += 1
                state = post_state(history, x)
                targeted_one += state['hidden']
                control_one += rng.getrandbits(1)
        out[history] = {
            'x0_count': x0,
            'P_x0_empirical': x0 / TRIALS,
            'P_target_ONE_given_x0_empirical': targeted_one / x0,
            'P_control_ONE_given_x0_empirical': control_one / x0,
        }
    return out


# ---------- persistence pressure, unchanged Nano ----------

def carrier(mode: str, history: str) -> str:
    if mode == 'coarse':
        return 'event:x:0'
    if mode == 'complete':
        return f'event:{history}:x:0'
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


def active_value(kernel, key) -> str | None:
    for standing in kernel.effective_state().active:
        if standing.key == key:
            return standing.value
    return None


def run_branch(nano, *, mode: str, probe: str, truth_A: str, truth_B: str) -> dict[str, object]:
    event_A = carrier(mode, 'A')
    event_B = carrier(mode, 'B')
    key_A = profile_key(nano, event_A, probe)
    key_B = profile_key(nano, event_B, probe)
    out_key = output_key(nano, probe)

    # Deduplicate opaque objects when the coarse carrier aliases A and B.
    object_ids = [event_A, event_B, out_key.object_id]
    objects = tuple(
        nano.ObjectRecord(obj_id, hashlib.sha256(obj_id.encode()).hexdigest(), 'OPAQUE_CLASSICAL_EVENT' if obj_id.startswith('event:') else 'OPAQUE_PERSISTENT_RESULT')
        for obj_id in dict.fromkeys(object_ids)
    )

    admit_A = nano.License(
        id=f'admit-A-{probe}',
        operation='admit-profile',
        allowed_writes=(nano.WriteGrant(key_A, (truth_A,)),),
    )
    use_A_profile_for_B = nano.License(
        id=f'use-A-profile-for-B-{probe}',
        operation='persist-downstream-profile',
        preconditions=(nano.Precondition(key_B, truth_A),),
        allowed_writes=(nano.WriteGrant(out_key, (truth_A,)),),
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

    kernel = nano.Nano(objects=objects, licenses=(admit_A, use_A_profile_for_B, admit_B, use_truth_B))

    r_A = kernel.apply_transition(
        nano.Transition('admit-profile', writes=(nano.Standing(key_A, truth_A),)),
        admit_A.id,
    )

    # This downstream transition object is held identical across coarse/complete.
    old_profile_proposal = nano.Transition(
        'persist-downstream-profile',
        writes=(nano.Standing(out_key, truth_A),),
    )
    r_use_before_B = kernel.apply_transition(old_profile_proposal, use_A_profile_for_B.id)
    persisted_before_B = active_value(kernel, out_key)
    oracle_correct_before_B = persisted_before_B == truth_B if persisted_before_B is not None else None

    r_B = None
    r_old_after_B = None
    r_correct_after_B = None
    persisted_after_B = None
    if mode == 'complete':
        r_B = kernel.apply_transition(
            nano.Transition('admit-profile', writes=(nano.Standing(key_B, truth_B),)),
            admit_B.id,
        )
        r_old_after_B = kernel.apply_transition(old_profile_proposal, use_A_profile_for_B.id)
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
        'contract_template': contract_template(probe, truth_A, truth_A),
        'contract_template_digest': digest_json(contract_template(probe, truth_A, truth_A)),
        'A_profile_receipt': asdict(r_A),
        'use_before_B': {
            'receipt': asdict(r_use_before_B),
            'persisted_value': persisted_before_B,
            'oracle_correct': oracle_correct_before_B,
        },
        'B_profile_receipt': asdict(r_B) if r_B else None,
        'old_use_after_B': asdict(r_old_after_B) if r_old_after_B else None,
        'correct_use_after_B': asdict(r_correct_after_B) if r_correct_after_B else None,
        'persisted_after_B': persisted_after_B,
        'final_effective_state': asdict(kernel.effective_state()),
    }


def main() -> int:
    # Formal classical witness, prospectively frozen.
    witness = {
        'initial_state': 's0',
        'first_outcome': 0,
        'P_A_x0': first_outcome_probability('A', 0),
        'P_B_x0': first_outcome_probability('B', 0),
        'post_A_x0': post_state('A', 0),
        'post_B_x0': post_state('B', 0),
        'target_A': targeted_distribution(post_state('A', 0)),
        'target_B': targeted_distribution(post_state('B', 0)),
        'control_A': control_distribution(post_state('A', 0)),
        'control_B': control_distribution(post_state('B', 0)),
    }
    truth = {
        'X': {'A': profile(witness['target_A']), 'B': profile(witness['target_B'])},
        'Y': {'A': profile(witness['control_A']), 'B': profile(witness['control_B'])},
    }

    formal_checks = {
        'same_first_outcome_distribution': witness['P_A_x0'] == witness['P_B_x0'] == 0.5,
        'different_post_intervention_state': witness['post_A_x0'] != witness['post_B_x0'],
        'targeted_probe_diverges': witness['target_A'] != witness['target_B'],
        'null_probe_agrees': witness['control_A'] == witness['control_B'],
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

    persistence_checks = {
        'nano_unchanged': nano_pre == nano_post == NANO_SHA256,
        'coarse_X_aliases_histories': coarse_x['carriers_equal'],
        'complete_X_distinguishes_histories': not complete_x['carriers_equal'],
        'same_X_downstream_transition_object': coarse_x['use_before_B']['receipt']['transition_digest'] == complete_x['use_before_B']['receipt']['transition_digest'],
        'same_Y_downstream_transition_object': coarse_y['use_before_B']['receipt']['transition_digest'] == complete_y['use_before_B']['receipt']['transition_digest'],
        'coarse_X_cross_history_use_ALLOW': coarse_x['use_before_B']['receipt']['decision'] == 'ALLOW',
        'coarse_X_wrong_value_persisted': coarse_x['use_before_B']['persisted_value'] == truth['X']['A'],
        'coarse_X_oracle_marks_wrong': coarse_x['use_before_B']['oracle_correct'] is False,
        'coarse_X_parent_is_A_profile': coarse_x['use_before_B']['receipt']['parent_receipts'] == (coarse_x['A_profile_receipt']['id'],),
        'complete_X_before_B_DEFER': complete_x['use_before_B']['receipt']['decision'] == 'DEFER',
        'complete_X_old_after_B_DENY': complete_x['old_use_after_B']['decision'] == 'DENY',
        'complete_X_correct_after_B_ALLOW': complete_x['correct_use_after_B']['decision'] == 'ALLOW',
        'complete_X_correct_value_persisted': complete_x['persisted_after_B'] == truth['X']['B'],
        'coarse_Y_use_ALLOW': coarse_y['use_before_B']['receipt']['decision'] == 'ALLOW',
        'coarse_Y_oracle_marks_correct': coarse_y['use_before_B']['oracle_correct'] is True,
        'complete_Y_before_B_DEFER': complete_y['use_before_B']['receipt']['decision'] == 'DEFER',
        'complete_Y_after_B_old_use_ALLOW': complete_y['old_use_after_B']['decision'] == 'ALLOW',
        'complete_Y_correct_value_persisted': complete_y['persisted_after_B'] == 'HALF',
    }

    if all(formal_checks.values()) and all(persistence_checks.values()):
        result_class = 'CLASSICAL_REPRODUCTION_ESTABLISHED'
    elif all(formal_checks.values()):
        result_class = 'NO_CLASSICAL_REPRODUCTION'
    else:
        result_class = 'ASSAY_INVALID_OR_UNDERCONSTITUTED'

    result = {
        'experiment': 'FOREIGN-003',
        'title': 'History-Dependent Outcome Equivalence',
        'prospective_result_class': result_class,
        'world': {
            'type': 'classical stateful intervention process',
            'quantum_dependencies': False,
            'witness': witness,
            'truth_profiles': truth,
            'formal_checks': formal_checks,
            'monte_carlo_sanity': monte_carlo_sanity(),
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
        'persistence_checks': persistence_checks,
        'earned_claim': (
            'The OQ-002 causal topology reproduced in a purely classical stateful world: '
            'outcome-equivalent acquisition histories with different future consequence structure, '
            'when collapsed to one persistence identity, caused an A-derived standing to authorize '
            'a wrong durable B-history targeted-probe profile. Preserving opaque history identity '
            'blocked the transfer; the null probe remained harmless under the same aliasing.'
        ),
        'diagnosis': 'cross-domain persistence wound caused by premature apparatus identity quotienting upstream of unchanged Nano',
        'not_claimed': [
            'the pattern is universal across all domains',
            'quantum mechanics is irrelevant to all future OpenCore Quantum assays',
            'Nano is defective',
            'Nano requires new semantics',
            'history identity is a universal OpenCore primitive',
            'a schema repair is earned',
        ],
    }

    result_path = HERE / 'foreign_003_result.json'
    result_path.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    result_sha = sha256_file(result_path)

    print(result_class)
    print('formal_checks=', sum(formal_checks.values()), '/', len(formal_checks))
    print('persistence_checks=', sum(persistence_checks.values()), '/', len(persistence_checks))
    print('nano_sha256=', nano_pre)
    print('coarse_X=', coarse_x['use_before_B']['receipt']['decision'], coarse_x['use_before_B']['persisted_value'], 'oracle_correct=', coarse_x['use_before_B']['oracle_correct'])
    print('coarse_X_parent=', coarse_x['use_before_B']['receipt']['parent_receipts'])
    print('A_profile_receipt=', coarse_x['A_profile_receipt']['id'])
    print('complete_X_before=', complete_x['use_before_B']['receipt']['decision'])
    print('complete_X_after_old=', complete_x['old_use_after_B']['decision'])
    print('complete_X_after_correct=', complete_x['correct_use_after_B']['decision'], complete_x['persisted_after_B'])
    print('coarse_Y=', coarse_y['use_before_B']['receipt']['decision'], coarse_y['use_before_B']['persisted_value'], 'oracle_correct=', coarse_y['use_before_B']['oracle_correct'])
    print('same_X_transition=', persistence_checks['same_X_downstream_transition_object'])
    print('result_sha256=', result_sha)
    return 0 if result_class == 'CLASSICAL_REPRODUCTION_ESTABLISHED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
