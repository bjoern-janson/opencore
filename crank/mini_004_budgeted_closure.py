#!/usr/bin/env python3
"""OpenCore Mini 004: budgeted epistemic closure under an unknown finite horizon.

mini.py is imported unchanged.

The harness creates paired latent-context populations with identical initial
visible evidence and the same supported affine model:

  A sufficient: no hidden context changes the consequence.
  B sparse_defect: a genuine interface collision exists in one rare context.
  C dense_defect: genuine interface collisions occupy at least p_min of the
    hidden challenge population.

The population is finite but its effective size is hidden from the controller.
A challenge reveals one previously unseen context.  The controller never sees
true defect prevalence.

Controllers:
  zero_error_stop       STOP immediately when empirical error is zero.
  budget_exhaustion_stop
                        challenge until the budget is gone, then STOP.
  no_contract           challenge until the budget is gone, then DEFER.
  contract_aware        STOP only when an external adversary contract plus
                        no-hit challenge evidence licenses closure; otherwise
                        MORE_COVERAGE or DEFER when resources run out.

The external closure contract is:
  "Any in-scope material hidden defect affects at least p_min of challenge
   opportunities.  Closure may be promoted after q no-hit challenges when the
   conservative miss bound (1-p_min)^q <= delta."

Sparse defects deliberately violate that contract.  They measure global
residual risk outside the licensed scope rather than in-scope contract failure.

This is a crank-science harness, not an OpenCore kernel/conformance claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from dataclasses import dataclass
from typing import Iterable

from mini import MOD, Organism, Rule, choose_rules

MINI_EXPECTED_SHA256 = "fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55"


@dataclass(frozen=True)
class InitialObs:
    x: int
    y: int


@dataclass(frozen=True)
class PopulationCase:
    kind: str
    rule: Rule
    x_by_slot: tuple[int, ...]
    defect_slots: frozenset[int]
    shift_by_slot: tuple[int, ...]

    @property
    def n(self) -> int:
        return len(self.x_by_slot)

    @property
    def defect_count(self) -> int:
        return len(self.defect_slots)

    @property
    def prevalence(self) -> float:
        return self.defect_count / self.n

    def observe_slot(self, slot: int) -> InitialObs:
        x = self.x_by_slot[slot]
        y = self.rule(x)
        if slot in self.defect_slots:
            y = (y + self.shift_by_slot[slot]) % MOD
        return InitialObs(x, y)

    def has_interface_collision(self) -> bool:
        """Every defect must conflict with at least one normal context at same x."""
        normals_by_x = {x: False for x in range(MOD)}
        defects_by_x = {x: False for x in range(MOD)}
        for slot, x in enumerate(self.x_by_slot):
            if slot in self.defect_slots:
                defects_by_x[x] = True
            else:
                normals_by_x[x] = True
        return any(normals_by_x[x] and defects_by_x[x] for x in range(MOD))


@dataclass(frozen=True)
class Triad:
    seed: int
    rule: Rule
    initial: tuple[InitialObs, ...]
    challenge_order: tuple[int, ...]
    sufficient: PopulationCase
    sparse: PopulationCase
    dense: PopulationCase


@dataclass(frozen=True)
class PolicyOutcome:
    controller: str
    action: str
    closure_basis: str
    challenges_used: int
    challenge_hit: bool
    stop_authorized_under_declared_contract: bool
    model_usable_provisionally: bool
    residual_hidden_prevalence: float
    rho_remaining_budget: float


def mini_sha256() -> str:
    from pathlib import Path
    return hashlib.sha256(Path(__file__).with_name("mini.py").read_bytes()).hexdigest()


def unique_supported_model(initial: Iterable[InitialObs]) -> Rule:
    organism = Organism()
    for row in initial:
        organism.observe("A", row.x, row.y, phase="mini004-initial")
    active = organism.active.get("A")
    if active is None:
        raise RuntimeError("initial evidence did not produce a Mini commitment")
    for row in initial:
        if active.rule(row.x) != row.y:
            raise AssertionError("Mini active model does not support initial evidence")
    return active.rule


def _balanced_slots(rng: random.Random, repeats: int) -> tuple[int, ...]:
    xs = [x for _ in range(repeats) for x in range(MOD)]
    rng.shuffle(xs)
    return tuple(xs)


def _choose_defects(
    rng: random.Random,
    x_by_slot: tuple[int, ...],
    count: int,
) -> frozenset[int]:
    """Choose defects while preserving at least one normal twin for each visible x."""
    capacity = {x: x_by_slot.count(x) - 1 for x in range(MOD)}
    slots = list(range(len(x_by_slot)))
    rng.shuffle(slots)
    chosen: list[int] = []
    used = {x: 0 for x in range(MOD)}
    for slot in slots:
        x = x_by_slot[slot]
        if used[x] >= capacity[x]:
            continue
        chosen.append(slot)
        used[x] += 1
        if len(chosen) == count:
            break
    if len(chosen) != count:
        raise RuntimeError("unable to place requested defects without destroying normal twins")
    return frozenset(chosen)


def make_triad(seed: int, p_min: float, initial_k: int = 3) -> Triad:
    if not (0.0 < p_min < 0.5):
        raise ValueError("p_min must be in (0, 0.5)")
    if initial_k < 2:
        raise ValueError("initial_k must be >=2")

    rng = random.Random(seed ^ 0x4004)
    rule = choose_rules(rng)[0]

    initial_xs = list(range(MOD))
    rng.shuffle(initial_xs)
    initial = tuple(InitialObs(x, rule(x)) for x in initial_xs[:initial_k])
    fitted = unique_supported_model(initial)
    if fitted != rule:
        raise AssertionError("Mini fitted a different rule to canonical initial evidence")

    # Hidden finite effective horizon: 8..18 repeats of each visible x => 88..198
    # latent contexts.  N is never passed to a controller.
    repeats = rng.randint(8, 18)
    x_by_slot = _balanced_slots(rng, repeats)
    n = len(x_by_slot)

    challenge_order = list(range(n))
    rng.shuffle(challenge_order)
    challenge_order = tuple(challenge_order)

    shifts = [0] * n
    for slot in range(n):
        shifts[slot] = rng.randint(1, MOD - 1)
    shift_by_slot = tuple(shifts)

    sufficient = PopulationCase("sufficient", rule, x_by_slot, frozenset(), shift_by_slot)

    # One rare target-relevant collision: deliberately outside any p_min>=~1% contract.
    sparse_slots = _choose_defects(rng, x_by_slot, 1)
    sparse = PopulationCase("sparse_defect", rule, x_by_slot, sparse_slots, shift_by_slot)

    # Dense in-scope defect family.  Prevalence is randomized but guaranteed >= p_min.
    dense_p = p_min + rng.random() * min(0.20, 0.48 - p_min)
    dense_count = max(1, math.ceil(dense_p * n))
    dense_slots = _choose_defects(rng, x_by_slot, dense_count)
    dense = PopulationCase("dense_defect", rule, x_by_slot, dense_slots, shift_by_slot)

    if dense.prevalence < p_min:
        raise AssertionError("dense defect violates p_min construction")
    if sparse.prevalence >= p_min:
        raise AssertionError("sparse defect unexpectedly falls inside p_min contract")
    if not sparse.has_interface_collision() or not dense.has_interface_collision():
        raise AssertionError("defect construction failed to create a genuine interface collision")

    return Triad(seed, rule, initial, challenge_order, sufficient, sparse, dense)


def conservative_miss_bound(p_min: float, q_no_hit: int) -> float:
    return (1.0 - p_min) ** q_no_hit


def required_challenges(p_min: float, delta: float) -> int:
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must be in (0,1)")
    return math.ceil(math.log(delta) / math.log(1.0 - p_min))


def _rho_remaining_budget(case: PopulationCase, remaining_slots: list[int], budget_left: int) -> float:
    """Harness-only chance remaining random no-replacement budget hits >=1 defect."""
    if budget_left <= 0 or not remaining_slots:
        return 0.0
    b = min(budget_left, len(remaining_slots))
    m = sum(slot in case.defect_slots for slot in remaining_slots)
    if m <= 0:
        return 0.0
    if b > len(remaining_slots) - m:
        return 1.0
    misses = math.comb(len(remaining_slots) - m, b)
    total = math.comb(len(remaining_slots), b)
    return 1.0 - misses / total


def _residual_hidden_prevalence(case: PopulationCase, seen_slots: set[int]) -> float:
    remaining = [s for s in range(case.n) if s not in seen_slots]
    if not remaining:
        return 0.0
    hidden = sum(s in case.defect_slots for s in remaining)
    return hidden / len(remaining)


def simulate(
    case: PopulationCase,
    order: tuple[int, ...],
    budget: int,
    controller: str,
    p_min: float,
    delta: float,
) -> PolicyOutcome:
    budget = max(0, min(budget, len(order)))
    seen: set[int] = set()
    q_no_hit = 0

    if controller == "zero_error_stop":
        remaining = list(order)
        return PolicyOutcome(
            controller, "STOP", "ZERO_EMPIRICAL_ERROR", 0, False, False, True,
            _residual_hidden_prevalence(case, seen),
            _rho_remaining_budget(case, remaining, budget),
        )

    q_required = required_challenges(p_min, delta)

    for i in range(budget):
        if controller == "contract_aware" and conservative_miss_bound(p_min, q_no_hit) <= delta:
            remaining = [s for s in order if s not in seen]
            return PolicyOutcome(
                controller, "STOP", "EXTERNAL_CONTRACT_PLUS_NO_HIT_EVIDENCE",
                len(seen), False, True, True,
                _residual_hidden_prevalence(case, seen),
                _rho_remaining_budget(case, remaining, budget - len(seen)),
            )

        slot = order[i]
        seen.add(slot)
        obs = case.observe_slot(slot)
        if obs.y != case.rule(obs.x):
            remaining = [s for s in order if s not in seen]
            return PolicyOutcome(
                controller, "CHALLENGE_HIT", "COUNTEREVIDENCE",
                len(seen), True, False, False,
                _residual_hidden_prevalence(case, seen),
                _rho_remaining_budget(case, remaining, budget - len(seen)),
            )
        q_no_hit += 1

    # Budget is exhausted.  Contract-aware may have crossed its threshold exactly
    # on the final no-hit sample, so evaluate the license once more.
    if controller == "contract_aware" and conservative_miss_bound(p_min, q_no_hit) <= delta:
        action = "STOP"
        basis = "EXTERNAL_CONTRACT_PLUS_NO_HIT_EVIDENCE"
        authorized = True
    elif controller == "budget_exhaustion_stop":
        action = "STOP"
        basis = "BUDGET_EXHAUSTED"
        authorized = False
    elif controller in {"contract_aware", "no_contract"}:
        action = "DEFER"
        basis = "BUDGET_EXHAUSTED_WITHOUT_CLOSURE_LICENSE"
        authorized = False
    else:
        raise ValueError(f"unknown controller {controller}")

    remaining = [s for s in order if s not in seen]
    return PolicyOutcome(
        controller, action, basis, len(seen), False, authorized, True,
        _residual_hidden_prevalence(case, seen),
        _rho_remaining_budget(case, remaining, 0),
    )


def case_record(triad: Triad, case: PopulationCase, budget: int, p_min: float, delta: float) -> dict:
    controllers = [
        "zero_error_stop",
        "budget_exhaustion_stop",
        "no_contract",
        "contract_aware",
    ]
    rows = {}
    for name in controllers:
        out = simulate(case, triad.challenge_order, budget, name, p_min, delta)
        rows[name] = {
            "action": out.action,
            "closure_basis": out.closure_basis,
            "challenges_used": out.challenges_used,
            "challenge_hit": out.challenge_hit,
            "stop_authorized_under_declared_contract": out.stop_authorized_under_declared_contract,
            "model_usable_provisionally": out.model_usable_provisionally,
            "residual_hidden_prevalence_harness_only": out.residual_hidden_prevalence,
            "rho_remaining_budget_harness_only": out.rho_remaining_budget,
        }
    return {
        "kind_posthoc": case.kind,
        "hidden_population_size_harness_only": case.n,
        "latent_defect_count_harness_only": case.defect_count,
        "latent_defect_prevalence_harness_only": case.prevalence,
        "inside_declared_contract": case.kind != "sparse_defect",
        "controllers": rows,
    }


def run_seed(seed: int, budget: int, p_min: float, delta: float) -> dict:
    triad = make_triad(seed, p_min)
    return {
        "seed": seed,
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "supported_model": triad.rule.short(),
        "initial_history_identical": [(o.x, o.y) for o in triad.initial],
        "paired_no_hit_challenge_prefix_identical": True,
        "budget": budget,
        "contract": {
            "p_min": p_min,
            "delta": delta,
            "q_required": required_challenges(p_min, delta),
            "meaning": "in-scope material defect prevalence >= p_min",
        },
        "controller_observability": {
            "hidden_population_size": False,
            "true_defect_prevalence": False,
            "posthoc_world_kind": False,
            "p_min_delta_contract": True,
            "challenge_no_hit_or_counterexample": True,
        },
        "cases": [
            case_record(triad, triad.sufficient, budget, p_min, delta),
            case_record(triad, triad.sparse, budget, p_min, delta),
            case_record(triad, triad.dense, budget, p_min, delta),
        ],
    }


def _empty_agg() -> dict:
    return {
        "stops": 0,
        "authorized_stops": 0,
        "defers": 0,
        "hits": 0,
        "false_closures_global": 0,
        "false_closures_in_scope": 0,
        "total_challenges": 0,
        "count": 0,
    }


def sweep(n: int, budgets: list[int], p_min: float, delta: float, start_seed: int = 0) -> dict:
    controllers = ["zero_error_stop", "budget_exhaustion_stop", "no_contract", "contract_aware"]
    kinds = ["sufficient", "sparse_defect", "dense_defect"]
    agg = {
        str(b): {c: {k: _empty_agg() for k in kinds} for c in controllers}
        for b in budgets
    }
    population_sizes = []
    sparse_prevalences = []
    dense_prevalences = []

    for seed in range(start_seed, start_seed + n):
        triad = make_triad(seed, p_min)
        population_sizes.append(triad.sufficient.n)
        sparse_prevalences.append(triad.sparse.prevalence)
        dense_prevalences.append(triad.dense.prevalence)
        cases = [triad.sufficient, triad.sparse, triad.dense]

        for b in budgets:
            for case in cases:
                for controller in controllers:
                    out = simulate(case, triad.challenge_order, b, controller, p_min, delta)
                    a = agg[str(b)][controller][case.kind]
                    a["count"] += 1
                    a["stops"] += int(out.action == "STOP")
                    a["authorized_stops"] += int(out.stop_authorized_under_declared_contract)
                    a["defers"] += int(out.action == "DEFER")
                    a["hits"] += int(out.action == "CHALLENGE_HIT")
                    latent_defect = case.kind != "sufficient"
                    a["false_closures_global"] += int(out.action == "STOP" and latent_defect)
                    in_scope_defect = case.kind == "dense_defect"
                    a["false_closures_in_scope"] += int(out.action == "STOP" and in_scope_defect)
                    a["total_challenges"] += out.challenges_used

    summary = {}
    for b in budgets:
        bkey = str(b)
        summary[bkey] = {}
        for controller in controllers:
            summary[bkey][controller] = {}
            for kind in kinds:
                a = agg[bkey][controller][kind]
                count = a["count"]
                summary[bkey][controller][kind] = {
                    "stop_rate": a["stops"] / count,
                    "authorized_stop_rate": a["authorized_stops"] / count,
                    "defer_rate": a["defers"] / count,
                    "challenge_hit_rate": a["hits"] / count,
                    "global_false_closure_rate": a["false_closures_global"] / count,
                    "in_scope_false_closure_rate": a["false_closures_in_scope"] / count,
                    "mean_challenges": a["total_challenges"] / count,
                }

    return {
        "n_triads": n,
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "contract": {
            "p_min": p_min,
            "delta": delta,
            "q_required": required_challenges(p_min, delta),
            "miss_bound_at_q_required": conservative_miss_bound(p_min, required_challenges(p_min, delta)),
        },
        "population_horizon_harness_only": {
            "min": min(population_sizes),
            "mean": sum(population_sizes) / len(population_sizes),
            "max": max(population_sizes),
            "revealed_to_controller": False,
        },
        "latent_prevalence_harness_only": {
            "sparse_mean": sum(sparse_prevalences) / len(sparse_prevalences),
            "dense_mean": sum(dense_prevalences) / len(dense_prevalences),
            "revealed_to_controller": False,
        },
        "budgets": summary,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=2556)
    p.add_argument("--budget", type=int, default=8)
    p.add_argument("--p-min", type=float, default=0.25)
    p.add_argument("--delta", type=float, default=0.10)
    p.add_argument("--sweep", type=int, default=0)
    p.add_argument("--budgets", default="0,2,4,6,8,9,12,16")
    args = p.parse_args()

    if mini_sha256() != MINI_EXPECTED_SHA256:
        raise SystemExit("mini.py changed; Mini 004 requires the prior organism byte-identical")

    if args.sweep:
        budgets = [int(x) for x in args.budgets.split(",") if x.strip()]
        print(json.dumps(sweep(args.sweep, budgets, args.p_min, args.delta), indent=2, sort_keys=True))
    else:
        print(json.dumps(run_seed(args.seed, args.budget, args.p_min, args.delta), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
