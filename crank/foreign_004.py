from __future__ import annotations

from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
SPEC_PATH = HERE / 'FOREIGN_004_SPEC.md'
NANO_PATH = Path('/mnt/data/nano_oq2.py')
NANO_SHA256 = '8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329'
SEED = 4004
TRIALS = 100_000
Q = ('X', 'Y', 'Z')


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    ).hexdigest()


def load_nano():
    actual = sha256_file(NANO_PATH)
    if actual != NANO_SHA256:
        raise RuntimeError(f'Nano hash mismatch: expected {NANO_SHA256}, got {actual}')
    spec = importlib.util.spec_from_file_location('foreign004_frozen_nano', NANO_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load Nano')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------- independently motivated classical convergent-history world ----------

HISTORIES = {
    'A': (('inc', 1), ('inc', 1)),
    'B': (('inc', 3), ('dec', 1)),
}


def execute_history(history: str) -> dict[str, object]:
    if history not in HISTORIES:
        raise ValueError(history)
    counter = 0
    trace = [counter]
    for op, amount in HISTORIES[history]:
        if op == 'inc':
            counter += amount
        elif op == 'dec':
            counter -= amount
        else:
            raise ValueError(op)
        trace.append(counter)
    return {
        'history': history,
        'operations': HISTORIES[history],
        'trace': tuple(trace),
        'final_state': {'counter': counter},
    }


def first_outcome_probability(history: str, x: int) -> float:
    if history not in HISTORIES or x not in {0, 1}:
        raise ValueError((history, x))
    return 0.5


def future_distribution(state: dict[str, int], probe: str) -> dict[str, float]:
    counter = state['counter']
    if probe == 'X':
        return {'EVEN': 1.0, 'ODD': 0.0} if counter % 2 == 0 else {'EVEN': 0.0, 'ODD': 1.0}
    if probe == 'Y':
        return {'LOW': 0.0, 'HIGH': 1.0} if counter >= 2 else {'LOW': 1.0, 'HIGH': 0.0}
    if probe == 'Z':
        return {'ZERO': 0.5, 'ONE': 0.5}
    raise ValueError(probe)


def profile(dist: dict[str, float]) -> str:
    if dist == {'EVEN': 1.0, 'ODD': 0.0}:
        return 'EVEN'
    if dist == {'LOW': 0.0, 'HIGH': 1.0}:
        return 'HIGH'
    if dist == {'ZERO': 0.5, 'ONE': 0.5}:
        return 'HALF'
    raise ValueError(f'unconstituted profile: {dist}')


def monte_carlo_sanity() -> dict[str, object]:
    rng = random.Random(SEED)
    out: dict[str, object] = {}
    for history in ('A', 'B'):
        x0 = 0
        z_one = 0
        for _ in range(TRIALS):
            x = rng.getrandbits(1)
            if x == 0:
                x0 += 1
                z_one += rng.getrandbits(1)
        out[history] = {
            'x0_count': x0,
            'P_x0_empirical': x0 / TRIALS,
            'P_Z_ONE_given_x0_empirical': z_one / x0,
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


def contract_template(probe: str, expected: str) -> dict[str, object]:
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
            'value': expected,
        },
    }


def active_value(kernel, key) -> str | None:
    for standing in kernel.effective_state().active:
        if standing.key == key:
            return standing.value
    return None


def run_branch(nano, *, mode: str, probe: str, truth: str) -> dict[str, object]:
    event_A = carrier(mode, 'A')
    event_B = carrier(mode, 'B')
    key_A = profile_key(nano, event_A, probe)
    key_B = profile_key(nano, event_B, probe)
    out_key = output_key(nano, probe)

    object_ids = [event_A, event_B, out_key.object_id]
    objects = tuple(
        nano.ObjectRecord(
            obj_id,
            hashlib.sha256(obj_id.encode()).hexdigest(),
            'OPAQUE_CLASSICAL_EVENT' if obj_id.startswith('event:') else 'OPAQUE_PERSISTENT_RESULT',
        )
        for obj_id in dict.fromkeys(object_ids)
    )

    admit_A = nano.License(
        id=f'admit-A-{probe}',
        operation='admit-profile',
        allowed_writes=(nano.WriteGrant(key_A, (truth,)),),
    )
    use_profile_for_B = nano.License(
        id=f'use-profile-for-B-{probe}',
        operation='persist-downstream-profile',
        preconditions=(nano.Precondition(key_B, truth),),
        allowed_writes=(nano.WriteGrant(out_key, (truth,)),),
    )
    admit_B = nano.License(
        id=f'admit-B-{probe}',
        operation='admit-profile',
        allowed_writes=(nano.WriteGrant(key_B, (truth,)),),
    )

    kernel = nano.Nano(objects=objects, licenses=(admit_A, use_profile_for_B, admit_B))

    r_A = kernel.apply_transition(
        nano.Transition('admit-profile', writes=(nano.Standing(key_A, truth),)),
        admit_A.id,
    )

    # Literally the same downstream transition object is used in coarse and complete modes.
    proposal = nano.Transition(
        'persist-downstream-profile',
        writes=(nano.Standing(out_key, truth),),
    )
    r_before_B = kernel.apply_transition(proposal, use_profile_for_B.id)
    persisted_before_B = active_value(kernel, out_key)
    oracle_correct_before_B = persisted_before_B == truth if persisted_before_B is not None else None

    r_B = None
    r_after_B = None
    persisted_after_B = None
    oracle_correct_after_B = None
    if mode == 'complete':
        r_B = kernel.apply_transition(
            nano.Transition('admit-profile', writes=(nano.Standing(key_B, truth),)),
            admit_B.id,
        )
        r_after_B = kernel.apply_transition(proposal, use_profile_for_B.id)
        persisted_after_B = active_value(kernel, out_key)
        oracle_correct_after_B = persisted_after_B == truth if persisted_after_B is not None else None

    return {
        'mode': mode,
        'probe': probe,
        'carrier_A': event_A,
        'carrier_B': event_B,
        'carriers_equal': event_A == event_B,
        'truth_A': truth,
        'truth_B': truth,
        'contract_template': contract_template(probe, truth),
        'contract_template_digest': digest_json(contract_template(probe, truth)),
        'A_profile_receipt': asdict(r_A),
        'use_before_B': {
            'receipt': asdict(r_before_B),
            'persisted_value': persisted_before_B,
            'oracle_correct': oracle_correct_before_B,
        },
        'B_profile_receipt': asdict(r_B) if r_B else None,
        'use_after_B': {
            'receipt': asdict(r_after_B) if r_after_B else None,
            'persisted_value': persisted_after_B,
            'oracle_correct': oracle_correct_after_B,
        },
        'final_effective_state': asdict(kernel.effective_state()),
    }


def main() -> int:
    spec_sha = sha256_file(SPEC_PATH)
    world_A = execute_history('A')
    world_B = execute_history('B')
    state_A = world_A['final_state']
    state_B = world_B['final_state']

    surface = {
        probe: {
            'A': future_distribution(state_A, probe),
            'B': future_distribution(state_B, probe),
        }
        for probe in Q
    }
    truths = {
        probe: {'A': profile(surface[probe]['A']), 'B': profile(surface[probe]['B'])}
        for probe in Q
    }

    formal_checks = {
        'histories_genuinely_different': world_A['operations'] != world_B['operations'] and world_A['trace'] != world_B['trace'],
        'intermediate_states_differ': world_A['trace'][1] != world_B['trace'][1],
        'final_operational_state_equal': state_A == state_B == {'counter': 2},
        'same_first_outcome_distribution': first_outcome_probability('A', 0) == first_outcome_probability('B', 0) == 0.5,
        'future_surface_frozen_nonempty': Q == ('X', 'Y', 'Z'),
        'all_future_probe_distributions_equal': all(surface[p]['A'] == surface[p]['B'] for p in Q),
        'all_future_profiles_equal': all(truths[p]['A'] == truths[p]['B'] for p in Q),
    }

    nano_pre = sha256_file(NANO_PATH)
    nano = load_nano()
    branches = {
        f'{mode}_{probe}': run_branch(nano, mode=mode, probe=probe, truth=truths[probe]['A'])
        for mode in ('coarse', 'complete')
        for probe in Q
    }
    nano_post = sha256_file(NANO_PATH)

    persistence_checks: dict[str, bool] = {
        'nano_unchanged': nano_pre == nano_post == NANO_SHA256,
    }

    for probe in Q:
        coarse = branches[f'coarse_{probe}']
        complete = branches[f'complete_{probe}']
        persistence_checks.update({
            f'{probe}_coarse_aliases_histories': coarse['carriers_equal'],
            f'{probe}_complete_distinguishes_histories': not complete['carriers_equal'],
            f'{probe}_same_downstream_transition_object': (
                coarse['use_before_B']['receipt']['transition_digest']
                == complete['use_before_B']['receipt']['transition_digest']
            ),
            f'{probe}_same_contract_template': coarse['contract_template_digest'] == complete['contract_template_digest'],
            f'{probe}_coarse_cross_history_use_ALLOW': coarse['use_before_B']['receipt']['decision'] == 'ALLOW',
            f'{probe}_coarse_oracle_correct': coarse['use_before_B']['oracle_correct'] is True,
            f'{probe}_coarse_parent_is_A_profile': (
                coarse['use_before_B']['receipt']['parent_receipts']
                == (coarse['A_profile_receipt']['id'],)
            ),
            f'{probe}_complete_before_B_DEFER': complete['use_before_B']['receipt']['decision'] == 'DEFER',
            f'{probe}_complete_B_admission_ALLOW': complete['B_profile_receipt']['decision'] == 'ALLOW',
            f'{probe}_complete_after_B_ALLOW': complete['use_after_B']['receipt']['decision'] == 'ALLOW',
            f'{probe}_complete_after_B_oracle_correct': complete['use_after_B']['oracle_correct'] is True,
            f'{probe}_complete_parent_is_B_profile': (
                complete['use_after_B']['receipt']['parent_receipts']
                == (complete['B_profile_receipt']['id'],)
            ),
            f'{probe}_coarse_complete_same_persisted_value': (
                coarse['use_before_B']['persisted_value']
                == complete['use_after_B']['persisted_value']
                == truths[probe]['B']
            ),
        })

    formal_valid = all(formal_checks.values())
    safe = formal_valid and all(persistence_checks.values())

    aliasing_wound = False
    if formal_valid and not safe:
        for probe in Q:
            coarse = branches[f'coarse_{probe}']
            complete = branches[f'complete_{probe}']
            if (
                coarse['use_before_B']['persisted_value'] is not None
                and (
                    coarse['use_before_B']['oracle_correct'] is False
                    or (
                        complete['use_after_B']['persisted_value'] is not None
                        and coarse['use_before_B']['persisted_value'] != complete['use_after_B']['persisted_value']
                    )
                )
            ):
                aliasing_wound = True
                break

    if safe:
        result_class = 'SAFE_QUOTIENT_ESTABLISHED'
    elif aliasing_wound:
        result_class = 'HISTORY_ALIASING_WOUND_ESTABLISHED'
    else:
        result_class = 'ASSAY_INVALID_OR_UNDERCONSTITUTED'

    result = {
        'experiment': 'FOREIGN-004',
        'title': 'Safe quotient under future-consequence equivalence',
        'prospective_result_class': result_class,
        'spec_sha256': spec_sha,
        'world': {
            'type': 'classical convergent-history Markov/control process',
            'history_A': world_A,
            'history_B': world_B,
            'first_outcome': {
                'conditioned_value': 0,
                'P_A_x0': first_outcome_probability('A', 0),
                'P_B_x0': first_outcome_probability('B', 0),
            },
            'future_surface_Q': Q,
            'future_distributions': surface,
            'truth_profiles': truths,
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
            'In this classical convergent-history specimen, two genuinely different histories '
            'that converge to the same operational state and are equivalent across the frozen '
            'future-consequence surface can safely share a coarse persistence identity: A-derived '
            'standing reuse under B remains externally correct and converges to the same durable '
            'values as independently constituted complete-history identity.'
        ),
        'candidate_strengthened_not_proven': (
            'History distinctions appear persistence-relevant when, and only to the tested extent that, '
            'they preserve distinctions required by the constituted future consequence surface.'
        ),
        'not_claimed': [
            'history is generally irrelevant',
            'future-consequence equivalence is universally sufficient for quotienting',
            'all safe compression can be recognized automatically',
            'provenance should be erased',
            'a new OpenCore primitive is earned',
            'Nano should be modified',
        ],
    }

    result_path = HERE / 'foreign_004_result.json'
    result_path.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    result_sha = sha256_file(result_path)

    print(result_class)
    print('formal_checks=', sum(formal_checks.values()), '/', len(formal_checks))
    print('persistence_checks=', sum(persistence_checks.values()), '/', len(persistence_checks))
    print('spec_sha256=', spec_sha)
    print('nano_sha256=', nano_pre)
    for probe in Q:
        coarse = branches[f'coarse_{probe}']
        complete = branches[f'complete_{probe}']
        print(
            probe,
            'coarse=', coarse['use_before_B']['receipt']['decision'], coarse['use_before_B']['persisted_value'], coarse['use_before_B']['oracle_correct'],
            'parent=', coarse['use_before_B']['receipt']['parent_receipts'],
            'complete_before=', complete['use_before_B']['receipt']['decision'],
            'complete_after=', complete['use_after_B']['receipt']['decision'], complete['use_after_B']['persisted_value'], complete['use_after_B']['oracle_correct'],
            'parent=', complete['use_after_B']['receipt']['parent_receipts'],
        )
    print('result_sha256=', result_sha)
    return 0 if result_class == 'SAFE_QUOTIENT_ESTABLISHED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
