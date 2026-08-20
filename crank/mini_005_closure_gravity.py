#!/usr/bin/env python3
"""OpenCore Mini 005: post-closure reopenability and contract non-appropriation.

mini.py is imported unchanged.

Two independent harness attacks:

1) Closure Gravity
   First obtain a closure that is *authorized under the Mini 004 external
   contract*.  Then deliver one of three post-closure events:

     - IN_SCOPE_COUNTEREXAMPLE: valid evidence inside the closed scope.
     - OUT_OF_SCOPE_COUNTEREXAMPLE: valid evidence, but outside that scope.
     - NUISANCE: surprising but not target-relevant evidence.

   Controllers:
     reopenable      uses typed evidence: reopen only for the in-scope case.
     closure_gravity logs the in-scope counterexample but preserves CLOSED.
     panic           reopens on every surprise.

   This separates reopenability from overreaction.

2) Contract Non-Appropriation
   The declared external contract fixes p_min, delta, and therefore q_required.
   An "optimistic" controller is offered a cheaper self-authored closure rule
   q_self < q_required.  Nothing external authorizes the revision.

   fixed_contract    may close only at q_required.
   self_rewriter     silently substitutes q_self and closes earlier.

   The assay measures cost benefit, unauthorized promotion, and false closure.

This is a crank-science harness, not an OpenCore kernel/conformance claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from mini import MOD
from mini_004_budgeted_closure import (
    MINI_EXPECTED_SHA256,
    PopulationCase,
    Triad,
    conservative_miss_bound,
    make_triad,
    required_challenges,
)


@dataclass(frozen=True)
class ClosureReceipt:
    scope: str
    p_min: float
    delta: float
    q_clean: int
    basis: str
    authorized: bool


@dataclass(frozen=True)
class PostClosureEvent:
    kind: str
    scope: str
    x: int
    expected_y: int
    observed_y: int
    target_relevant: bool


@dataclass(frozen=True)
class EventOutcome:
    controller: str
    action: str
    original_closure_retained: bool
    challenge_path_open: bool
    policy_changed: bool
    repeated_same_error: bool


def mini_sha256() -> str:
    return hashlib.sha256(Path(__file__).with_name("mini.py").read_bytes()).hexdigest()


def clean_prefix(case: PopulationCase, order: tuple[int, ...], q: int) -> bool:
    for slot in order[:q]:
        obs = case.observe_slot(slot)
        if obs.y != case.rule(obs.x):
            return False
    return True


def authorized_receipt(triad: Triad, p_min: float, delta: float, scope: str = "A") -> ClosureReceipt:
    q = required_challenges(p_min, delta)
    if conservative_miss_bound(p_min, q) > delta:
        raise AssertionError("q does not satisfy declared closure contract")
    return ClosureReceipt(
        scope=scope,
        p_min=p_min,
        delta=delta,
        q_clean=q,
        basis="EXTERNAL_CONTRACT_PLUS_NO_HIT_EVIDENCE",
        authorized=True,
    )


def first_postclosure_defect(case: PopulationCase, order: tuple[int, ...], q: int) -> int | None:
    for slot in order[q:]:
        obs = case.observe_slot(slot)
        if obs.y != case.rule(obs.x):
            return slot
    return None


def make_in_scope_event(case: PopulationCase, order: tuple[int, ...], q: int, scope: str = "A") -> PostClosureEvent | None:
    slot = first_postclosure_defect(case, order, q)
    if slot is None:
        return None
    obs = case.observe_slot(slot)
    return PostClosureEvent(
        kind="IN_SCOPE_COUNTEREXAMPLE",
        scope=scope,
        x=obs.x,
        expected_y=case.rule(obs.x),
        observed_y=obs.y,
        target_relevant=True,
    )


def make_out_of_scope_event(case: PopulationCase, order: tuple[int, ...], q: int) -> PostClosureEvent | None:
    base = make_in_scope_event(case, order, q, scope="B")
    if base is None:
        # Any valid mismatch in a different scope is sufficient for the type assay.
        x = 0
        expected = case.rule(x)
        return PostClosureEvent("OUT_OF_SCOPE_COUNTEREXAMPLE", "B", x, expected, (expected + 1) % MOD, True)
    return PostClosureEvent(
        kind="OUT_OF_SCOPE_COUNTEREXAMPLE",
        scope="B",
        x=base.x,
        expected_y=base.expected_y,
        observed_y=base.observed_y,
        target_relevant=True,
    )


def make_nuisance_event(case: PopulationCase) -> PostClosureEvent:
    x = 0
    y = case.rule(x)
    # Surprise is intentionally non-target-relevant; payload differs but is typed nuisance.
    return PostClosureEvent("NUISANCE", "A", x, y, (y + 1) % MOD, False)


def handle_event(controller: str, receipt: ClosureReceipt, event: PostClosureEvent) -> EventOutcome:
    if not receipt.authorized:
        raise ValueError("closure-gravity assay requires an initially authorized closure")

    in_scope_valid = (
        event.kind == "IN_SCOPE_COUNTEREXAMPLE"
        and event.scope == receipt.scope
        and event.target_relevant
        and event.observed_y != event.expected_y
    )

    if controller == "reopenable":
        if in_scope_valid:
            return EventOutcome(controller, "REOPEN", False, True, False, False)
        if event.kind == "OUT_OF_SCOPE_COUNTEREXAMPLE" and event.target_relevant:
            return EventOutcome(controller, "FORK_SCOPE", True, True, False, False)
        return EventOutcome(controller, "KEEP_CLOSED", True, False, False, False)

    if controller == "closure_gravity":
        # Logs evidence but CLOSED retains authority.
        if in_scope_valid:
            return EventOutcome(controller, "LOG_ONLY_KEEP_CLOSED", True, False, False, True)
        if event.kind == "OUT_OF_SCOPE_COUNTEREXAMPLE" and event.target_relevant:
            return EventOutcome(controller, "LOG_OUT_OF_SCOPE", True, False, False, False)
        return EventOutcome(controller, "KEEP_CLOSED", True, False, False, False)

    if controller == "panic":
        # Treats every surprise as revocation-worthy.
        return EventOutcome(controller, "REOPEN", False, True, False, False)

    raise ValueError(controller)


def closure_gravity_demo(seed: int, p_min: float, delta: float) -> dict:
    # Find the first dense triad where an authorized closure occurs before a later
    # real counterexample.  This is residual risk materializing after legitimate closure.
    q = required_challenges(p_min, delta)
    chosen: tuple[Triad, PopulationCase, PostClosureEvent] | None = None
    s = seed
    while chosen is None:
        triad = make_triad(s, p_min)
        case = triad.dense
        if clean_prefix(case, triad.challenge_order, q):
            event = make_in_scope_event(case, triad.challenge_order, q)
            if event is not None:
                chosen = (triad, case, event)
                break
        s += 1
        if s - seed > 200000:
            raise RuntimeError("failed to locate post-closure residual-risk witness")

    triad, case, event = chosen
    receipt = authorized_receipt(triad, p_min, delta)
    controls = {
        name: handle_event(name, receipt, event).__dict__
        for name in ["reopenable", "closure_gravity", "panic"]
    }
    out_scope = make_out_of_scope_event(case, triad.challenge_order, q)
    nuisance = make_nuisance_event(case)
    typed_controls = {
        "out_of_scope": {
            name: handle_event(name, receipt, out_scope).__dict__
            for name in ["reopenable", "closure_gravity", "panic"]
        },
        "nuisance": {
            name: handle_event(name, receipt, nuisance).__dict__
            for name in ["reopenable", "closure_gravity", "panic"]
        },
    }
    return {
        "seed_requested": seed,
        "seed_used": triad.seed,
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "receipt": receipt.__dict__,
        "latent_defect_prevalence_harness_only": case.prevalence,
        "postclosure_event": event.__dict__,
        "controllers": controls,
        "typed_negative_controls": typed_controls,
    }


def closure_gravity_sweep(n_events: int, p_min: float, delta: float, start_seed: int = 0) -> dict:
    q = required_challenges(p_min, delta)
    controllers = ["reopenable", "closure_gravity", "panic"]
    agg = {
        c: {
            "in_scope_total": 0,
            "in_scope_reopened": 0,
            "in_scope_retained": 0,
            "repeated_same_error": 0,
            "out_scope_total": 0,
            "out_scope_false_reopen": 0,
            "nuisance_total": 0,
            "nuisance_false_reopen": 0,
        }
        for c in controllers
    }

    found = 0
    seed = start_seed
    searched = 0
    while found < n_events:
        triad = make_triad(seed, p_min)
        case = triad.dense
        searched += 1
        seed += 1
        if not clean_prefix(case, triad.challenge_order, q):
            continue
        event = make_in_scope_event(case, triad.challenge_order, q)
        if event is None:
            continue
        receipt = authorized_receipt(triad, p_min, delta)
        out_scope = make_out_of_scope_event(case, triad.challenge_order, q)
        nuisance = make_nuisance_event(case)

        for c in controllers:
            a = agg[c]
            o = handle_event(c, receipt, event)
            a["in_scope_total"] += 1
            a["in_scope_reopened"] += int(o.action == "REOPEN")
            a["in_scope_retained"] += int(o.original_closure_retained)
            a["repeated_same_error"] += int(o.repeated_same_error)

            oo = handle_event(c, receipt, out_scope)
            a["out_scope_total"] += 1
            a["out_scope_false_reopen"] += int(oo.action == "REOPEN")

            on = handle_event(c, receipt, nuisance)
            a["nuisance_total"] += 1
            a["nuisance_false_reopen"] += int(on.action == "REOPEN")
        found += 1

    summary = {}
    for c, a in agg.items():
        summary[c] = {
            "closure_gravity_index": a["in_scope_retained"] / a["in_scope_total"],
            "reopen_rate_on_valid_in_scope_counterexample": a["in_scope_reopened"] / a["in_scope_total"],
            "repeated_same_error_rate": a["repeated_same_error"] / a["in_scope_total"],
            "false_reopen_rate_out_of_scope": a["out_scope_false_reopen"] / a["out_scope_total"],
            "false_reopen_rate_nuisance": a["nuisance_false_reopen"] / a["nuisance_total"],
        }
    return {
        "n_postclosure_residual_risk_events": n_events,
        "triads_searched": searched,
        "contract": {"p_min": p_min, "delta": delta, "q_required": q},
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "summary": summary,
    }


def self_authored_q(q_required: int) -> int:
    # Deliberately tempting but unauthorized: halves challenge burden.
    return max(2, q_required // 2)


def contract_action(case: PopulationCase, order: tuple[int, ...], q: int) -> tuple[str, int, bool]:
    """Return action, challenges used, whether a counterexample was hit first."""
    for i, slot in enumerate(order[:q], start=1):
        obs = case.observe_slot(slot)
        if obs.y != case.rule(obs.x):
            return "CHALLENGE_HIT", i, True
    return "STOP", q, False


def contract_nonappropriation_sweep(n: int, p_min: float, delta: float, start_seed: int = 0) -> dict:
    q_external = required_challenges(p_min, delta)
    q_self = self_authored_q(q_external)
    agg = {
        "fixed_contract": {"stops": 0, "false_closures": 0, "unauthorized_stops": 0, "challenges": 0},
        "self_rewriter": {"stops": 0, "false_closures": 0, "unauthorized_stops": 0, "challenges": 0},
    }
    sufficient_stops = {"fixed_contract": 0, "self_rewriter": 0}

    for seed in range(start_seed, start_seed + n):
        triad = make_triad(seed, p_min)
        for name, q, authority_q in [
            ("fixed_contract", q_external, q_external),
            ("self_rewriter", q_self, q_external),
        ]:
            # Sufficient case: cost/availability benefit only.
            action_s, used_s, _ = contract_action(triad.sufficient, triad.challenge_order, q)
            if action_s == "STOP":
                sufficient_stops[name] += 1

            # Dense in-contract defect: false closure if no witness before STOP.
            action, used, hit = contract_action(triad.dense, triad.challenge_order, q)
            a = agg[name]
            a["challenges"] += used
            if action == "STOP":
                a["stops"] += 1
                a["false_closures"] += 1
                # A STOP is authorized only if the declared external q was met.
                authorized = used >= authority_q
                a["unauthorized_stops"] += int(not authorized)

    out = {}
    for name, a in agg.items():
        out[name] = {
            "q_used": q_external if name == "fixed_contract" else q_self,
            "sufficient_stop_rate": sufficient_stops[name] / n,
            "dense_in_contract_false_closure_rate": a["false_closures"] / n,
            "unauthorized_stop_rate_all_dense_trials": a["unauthorized_stops"] / n,
            "unauthorized_fraction_of_stops": a["unauthorized_stops"] / a["stops"] if a["stops"] else 0.0,
            "mean_challenges_dense": a["challenges"] / n,
        }
    return {
        "n_triads": n,
        "external_contract": {
            "p_min": p_min,
            "delta": delta,
            "q_required": q_external,
            "self_authored_q_has_authority": False,
        },
        "tempting_self_revision": {
            "q_self": q_self,
            "mechanism": "controller silently substitutes a cheaper closure threshold without external authority",
        },
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "summary": out,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=53)
    p.add_argument("--p-min", type=float, default=0.25)
    p.add_argument("--delta", type=float, default=0.10)
    p.add_argument("--gravity-sweep", type=int, default=0)
    p.add_argument("--contract-sweep", type=int, default=0)
    args = p.parse_args()

    if mini_sha256() != MINI_EXPECTED_SHA256:
        raise SystemExit("mini.py changed; Mini 005 requires the organism byte-identical")

    if args.gravity_sweep:
        print(json.dumps(closure_gravity_sweep(args.gravity_sweep, args.p_min, args.delta), indent=2, sort_keys=True))
    elif args.contract_sweep:
        print(json.dumps(contract_nonappropriation_sweep(args.contract_sweep, args.p_min, args.delta), indent=2, sort_keys=True))
    else:
        print(json.dumps(closure_gravity_demo(args.seed, args.p_min, args.delta), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
