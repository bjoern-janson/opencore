#!/usr/bin/env python3
"""OpenCore Mini 006: recursive correction of closure policy.

mini.py is imported unchanged.

The harness separates two surprise types:

OBJECT_LEVEL_SURPRISE
  A valid, externally contracted closure encounters a later counterexample.
  Because the closure contract explicitly permits residual risk, the current
  claim must reopen, but this event alone does not authorize rewriting the
  closure contract or policy.

POLICY_LEVEL_SURPRISE
  The closure mechanism inherited an existing contract into a new scope that
  never had that authority.  A later counterexample exposes the policy defect:
  the mechanism allowed CLOSED without an explicit scope contract.

Controllers:

  grounded
    object surprise  -> reopen claim; closure mechanism unchanged.
    policy surprise  -> reopen claim AND revise K_closure so new scopes require
                        explicit contract authority before closure.
    recursive optimizer later proposes removing this guard for throughput;
    an independent grounding probe can veto that self-modification.

  proxy
    reopens individual claims but never changes the closure mechanism.
    It accepts the throughput-improving removal/inheritance policy.

The key assay is causal:

  E* -> Delta K_closure -> different future closure behavior

rather than merely "counterexample was seen".

This is a crank-science harness, not an OpenCore kernel/conformance claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, replace
from pathlib import Path

from mini_004_budgeted_closure import MINI_EXPECTED_SHA256, make_triad, required_challenges
from mini_005_closure_gravity import clean_prefix, first_postclosure_defect


@dataclass(frozen=True)
class ClosurePolicy:
    require_explicit_contract: bool
    revision_count: int = 0


@dataclass(frozen=True)
class ScopeContext:
    name: str
    has_explicit_contract: bool
    p_min: float | None
    delta: float | None


@dataclass(frozen=True)
class PolicyEvent:
    kind: str
    scope: ScopeContext
    counterexample: bool
    closure_was_authorized: bool
    evidence_basis: str


@dataclass(frozen=True)
class PolicyResponse:
    controller: str
    claim_action: str
    policy_before: ClosurePolicy
    policy_after: ClosurePolicy
    policy_changed_due_to_event: bool
    future_behavior_changed: bool
    basis: str


def mini_sha256() -> str:
    return hashlib.sha256(Path(__file__).with_name("mini.py").read_bytes()).hexdigest()


def closure_threshold(scope: ScopeContext, inherited_p_min: float, inherited_delta: float) -> int:
    p_min = scope.p_min if scope.has_explicit_contract else inherited_p_min
    delta = scope.delta if scope.has_explicit_contract else inherited_delta
    assert p_min is not None and delta is not None
    return required_challenges(p_min, delta)


def initial_closure_decision(policy: ClosurePolicy, scope: ScopeContext, *, inherited_p_min: float, inherited_delta: float) -> tuple[str, str, int]:
    if policy.require_explicit_contract and not scope.has_explicit_contract:
        return "DEFER", "NO_EXPLICIT_SCOPE_CONTRACT", 0
    q = closure_threshold(scope, inherited_p_min, inherited_delta)
    authority = scope.has_explicit_contract
    basis = "EXPLICIT_SCOPE_CONTRACT" if authority else "INHERITED_CONTRACT_WITHOUT_AUTHORITY"
    return "CHALLENGE_THEN_STOP", basis, q


def respond(controller: str, policy: ClosurePolicy, event: PolicyEvent) -> PolicyResponse:
    if not event.counterexample:
        return PolicyResponse(controller, "KEEP", policy, policy, False, False, "NO_COUNTEREXAMPLE")

    if event.kind == "OBJECT_LEVEL_SURPRISE":
        # The event is inside a declared residual-risk contract.  Reopen this claim,
        # but do not silently rewrite the policy from one allowed miss.
        return PolicyResponse(
            controller, "REOPEN_CLAIM", policy, policy, False, False,
            "IN_SCOPE_RESIDUAL_RISK_MATERIALIZED",
        )

    if event.kind != "POLICY_LEVEL_SURPRISE":
        raise ValueError(event.kind)

    if controller == "grounded":
        updated = replace(policy, require_explicit_contract=True, revision_count=policy.revision_count + 1)
        return PolicyResponse(
            controller, "REOPEN_CLAIM", policy, updated, updated != policy, updated != policy,
            "UNAUTHORIZED_SCOPE_INHERITANCE_EXPOSED_BY_CONSEQUENCE",
        )

    if controller == "proxy":
        return PolicyResponse(
            controller, "REOPEN_CLAIM", policy, policy, False, False,
            "COUNTEREXAMPLE_LOCALIZED_TO_CURRENT_CLAIM_ONLY",
        )

    raise ValueError(controller)


def find_object_level_event(start_seed: int, p_min: float, delta: float) -> tuple[int, float]:
    q = required_challenges(p_min, delta)
    seed = start_seed
    while True:
        triad = make_triad(seed, p_min)
        case = triad.dense
        if clean_prefix(case, triad.challenge_order, q) and first_postclosure_defect(case, triad.challenge_order, q) is not None:
            return seed, case.prevalence
        seed += 1
        if seed - start_seed > 200000:
            raise RuntimeError("no object-level residual-risk witness found")


def find_policy_level_event(start_seed: int, inherited_p_min: float, inherited_delta: float) -> tuple[int, float]:
    # Sparse case: the inherited contract is not authorized for this new scope.
    q = required_challenges(inherited_p_min, inherited_delta)
    seed = start_seed
    while True:
        triad = make_triad(seed, inherited_p_min)
        case = triad.sparse
        if clean_prefix(case, triad.challenge_order, q) and first_postclosure_defect(case, triad.challenge_order, q) is not None:
            return seed, case.prevalence
        seed += 1
        if seed - start_seed > 200000:
            raise RuntimeError("no policy-level witness found")


def future_sparse_trial(policy: ClosurePolicy, seed: int, inherited_p_min: float, inherited_delta: float) -> dict:
    scope = ScopeContext(f"novel/{seed}", False, None, None)
    action, basis, q = initial_closure_decision(
        policy, scope, inherited_p_min=inherited_p_min, inherited_delta=inherited_delta
    )
    triad = make_triad(seed, inherited_p_min)
    case = triad.sparse

    if action == "DEFER":
        return {
            "action": "DEFER",
            "basis": basis,
            "challenges": 0,
            "false_closure": False,
            "authorized": False,
            "latent_prevalence_harness_only": case.prevalence,
        }

    for i, slot in enumerate(triad.challenge_order[:q], start=1):
        obs = case.observe_slot(slot)
        if obs.y != case.rule(obs.x):
            return {
                "action": "CHALLENGE_HIT",
                "basis": "COUNTEREVIDENCE_BEFORE_STOP",
                "challenges": i,
                "false_closure": False,
                "authorized": False,
                "latent_prevalence_harness_only": case.prevalence,
            }
    return {
        "action": "STOP",
        "basis": basis,
        "challenges": q,
        "false_closure": True,
        "authorized": False,
        "latent_prevalence_harness_only": case.prevalence,
    }


def optimizer_proposal(policy: ClosurePolicy) -> ClosurePolicy:
    """Short-run throughput optimizer tries to remove explicit-contract guard."""
    if not policy.require_explicit_contract:
        return policy
    return replace(policy, require_explicit_contract=False, revision_count=policy.revision_count + 1)


def grounding_probe_veto(controller: str, incumbent: ClosurePolicy, proposal: ClosurePolicy) -> tuple[ClosurePolicy, dict]:
    # The independent probe asks only whether the proposed mechanism would grant
    # closure in an uncontracted scope.  This is an authority test, not a hidden
    # prevalence estimate.
    probe_scope = ScopeContext("grounding/probe-uncontracted", False, None, None)
    action, basis, q = initial_closure_decision(proposal, probe_scope, inherited_p_min=0.25, inherited_delta=0.10)
    violates_authority = action != "DEFER"

    if controller == "grounded" and violates_authority:
        return incumbent, {
            "proposal": proposal.__dict__,
            "grounding_probe_action": action,
            "grounding_probe_basis": basis,
            "would_close_without_scope_authority": True,
            "veto_applied": True,
            "accepted_policy": incumbent.__dict__,
        }

    return proposal, {
        "proposal": proposal.__dict__,
        "grounding_probe_action": action,
        "grounding_probe_basis": basis,
        "would_close_without_scope_authority": violates_authority,
        "veto_applied": False,
        "accepted_policy": proposal.__dict__,
    }


def demo(start_seed: int, p_min: float, delta: float, recursion_depth: int) -> dict:
    base = ClosurePolicy(require_explicit_contract=False, revision_count=0)
    contracted_scope = ScopeContext("core/A", True, p_min, delta)
    novel_scope = ScopeContext("novel/X", False, None, None)

    obj_seed, obj_prev = find_object_level_event(start_seed, p_min, delta)
    policy_seed, policy_prev = find_policy_level_event(obj_seed + 1, p_min, delta)

    object_event = PolicyEvent(
        "OBJECT_LEVEL_SURPRISE", contracted_scope, True, True,
        "authorized closure; residual risk later materialized",
    )
    policy_event = PolicyEvent(
        "POLICY_LEVEL_SURPRISE", novel_scope, True, False,
        "closure mechanism inherited a contract into a scope with no closure authority",
    )

    responses = {}
    final_policies = {}
    recursion = {}
    for controller in ["grounded", "proxy"]:
        r_obj = respond(controller, base, object_event)
        r_pol = respond(controller, r_obj.policy_after, policy_event)
        responses[controller] = {
            "object_level": {
                **r_obj.__dict__,
                "policy_before": r_obj.policy_before.__dict__,
                "policy_after": r_obj.policy_after.__dict__,
            },
            "policy_level": {
                **r_pol.__dict__,
                "policy_before": r_pol.policy_before.__dict__,
                "policy_after": r_pol.policy_after.__dict__,
            },
        }
        policy = r_pol.policy_after
        steps = []
        for n in range(recursion_depth):
            proposal = optimizer_proposal(policy)
            policy, probe = grounding_probe_veto(controller, policy, proposal)
            steps.append({"depth": n + 1, **probe})
        final_policies[controller] = policy
        recursion[controller] = steps

    return {
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "initial_buggy_policy": base.__dict__,
        "object_level_witness": {
            "seed": obj_seed,
            "scope_has_contract": True,
            "latent_prevalence_harness_only": obj_prev,
        },
        "policy_level_witness": {
            "seed": policy_seed,
            "scope_has_contract": False,
            "latent_prevalence_harness_only": policy_prev,
        },
        "responses": responses,
        "recursive_optimizer_pressure": recursion,
        "final_policies": {k: v.__dict__ for k, v in final_policies.items()},
        "future_same_class_example": {
            c: future_sparse_trial(final_policies[c], policy_seed + 1000, p_min, delta)
            for c in final_policies
        },
    }


def sweep(n: int, p_min: float, delta: float, recursion_depth: int, start_seed: int = 100000) -> dict:
    # First establish the two policy states using one policy-level event.
    base = ClosurePolicy(False, 0)
    policy_scope = ScopeContext("novel/X", False, None, None)
    event = PolicyEvent(
        "POLICY_LEVEL_SURPRISE", policy_scope, True, False,
        "uncontracted scope inherited closure authority",
    )

    policies = {}
    causal_update = {}
    object_precision = {}
    contracted_scope = ScopeContext("core/A", True, p_min, delta)
    object_event = PolicyEvent(
        "OBJECT_LEVEL_SURPRISE", contracted_scope, True, True,
        "authorized residual-risk miss",
    )

    for c in ["grounded", "proxy"]:
        obj = respond(c, base, object_event)
        pol = respond(c, obj.policy_after, event)
        object_precision[c] = int(not obj.policy_changed_due_to_event)
        causal_update[c] = int(pol.policy_changed_due_to_event)
        policy = pol.policy_after
        vetoes = 0
        for _ in range(recursion_depth):
            proposal = optimizer_proposal(policy)
            new_policy, probe = grounding_probe_veto(c, policy, proposal)
            vetoes += int(probe["veto_applied"])
            policy = new_policy
        policies[c] = (policy, vetoes)

    stats = {
        c: {
            "future_trials": 0,
            "stops": 0,
            "defers": 0,
            "hits": 0,
            "false_closures": 0,
            "unauthorized_stops": 0,
            "challenges": 0,
        }
        for c in policies
    }

    for seed in range(start_seed, start_seed + n):
        for c, (policy, _) in policies.items():
            r = future_sparse_trial(policy, seed, p_min, delta)
            a = stats[c]
            a["future_trials"] += 1
            a["stops"] += int(r["action"] == "STOP")
            a["defers"] += int(r["action"] == "DEFER")
            a["hits"] += int(r["action"] == "CHALLENGE_HIT")
            a["false_closures"] += int(r["false_closure"])
            a["unauthorized_stops"] += int(r["action"] == "STOP" and not r["authorized"])
            a["challenges"] += r["challenges"]

    summary = {}
    for c, a in stats.items():
        total = a["future_trials"]
        policy, vetoes = policies[c]
        # Short-run proxy favors closure throughput and low challenge cost; it does
        # not inspect latent truth.  Higher is "better" under the pathological proxy.
        proxy_throughput_score = (a["stops"] / total) - 0.01 * (a["challenges"] / total)
        summary[c] = {
            "policy_level_causal_update_rate": causal_update[c],
            "object_level_policy_stability": object_precision[c],
            "recursive_grounding_veto_rate": vetoes / recursion_depth if recursion_depth else 0.0,
            "final_policy": policy.__dict__,
            "future_stop_rate_uncontracted_sparse_scopes": a["stops"] / total,
            "future_defer_rate_uncontracted_sparse_scopes": a["defers"] / total,
            "future_challenge_hit_rate": a["hits"] / total,
            "future_false_closure_rate": a["false_closures"] / total,
            "future_unauthorized_stop_rate": a["unauthorized_stops"] / total,
            "mean_future_challenges": a["challenges"] / total,
            "short_run_proxy_throughput_score": proxy_throughput_score,
        }

    return {
        "n_future_uncontracted_sparse_scopes": n,
        "recursion_depth": recursion_depth,
        "inherited_contract": {"p_min": p_min, "delta": delta, "q": required_challenges(p_min, delta)},
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "summary": summary,
        "interpretation_boundary": "grounded policy narrows authority after policy-level surprise; it does not self-author a new contract",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=53)
    p.add_argument("--p-min", type=float, default=0.25)
    p.add_argument("--delta", type=float, default=0.10)
    p.add_argument("--recursion-depth", type=int, default=8)
    p.add_argument("--sweep", type=int, default=0)
    args = p.parse_args()

    if mini_sha256() != MINI_EXPECTED_SHA256:
        raise SystemExit("mini.py changed; Mini 006 requires the organism byte-identical")

    if args.sweep:
        out = sweep(args.sweep, args.p_min, args.delta, args.recursion_depth)
    else:
        out = demo(args.seed, args.p_min, args.delta, args.recursion_depth)
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
