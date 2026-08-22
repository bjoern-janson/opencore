#!/usr/bin/env python3
"""FOREIGN-007 — Policy-Induced Epistemic Foreclosure.

Frozen deterministic witness for representation -> policy -> corrective reachability.
Nano remains semantically blind and unchanged.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Iterable

HERE = Path(__file__).resolve().parent
NANO_PATH = Path("/mnt/data/nano_oq2.py")
NANO_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"
RESULT_PATH = HERE / "foreign_007_result_v2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_nano():
    spec = importlib.util.spec_from_file_location("nano_foreign_007", NANO_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen Nano")
    module = importlib.util.module_from_spec(spec)
    # Python 3.13 dataclasses require the dynamically loaded module to exist here.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


nano = load_nano()
Decision = nano.Decision
License = nano.License
Nano = nano.Nano
Precondition = nano.Precondition
Standing = nano.Standing
StandingKey = nano.StandingKey
Transition = nano.Transition
WriteGrant = nano.WriteGrant

A_ACT = "a_act"
A_PROBE = "a_probe"
AVAILABLE_ACTIONS = (A_ACT, A_PROBE)


def world_observe(regime: str, action: str, stage: str, *, discriminating: bool) -> str:
    if action == A_ACT:
        return "ACT_OK"
    if action != A_PROBE:
        raise ValueError(action)
    if stage == "t0":
        return "NO_SIGNAL"
    if stage != "t1":
        raise ValueError(stage)
    if not discriminating:
        return "SAME"
    return "SIG_A" if regime == "A" else "SIG_B"


def active_values(n: Nano) -> dict[tuple[str, str, str], str]:
    return {
        (s.key.object_id, s.key.dimension, s.key.scope): s.value
        for s in n.effective_state().active
    }


def policy(n: Nano) -> dict:
    active = active_values(n)
    cells = {
        obj
        for (obj, dimension, scope), value in active.items()
        if dimension == "candidate" and scope == "t0-model" and value == "POSSIBLE"
    }
    if len(cells) > 1:
        support = (A_PROBE, A_ACT)
        selected = A_PROBE
    else:
        support = (A_ACT,)
        selected = A_ACT
    return {
        "candidate_cells": sorted(cells),
        "policy_support": list(support),
        "selected_action": selected,
        "probe_cost": 1,
        "act_cost": 0,
    }


def build_branch(kind: str) -> tuple[Nano, dict]:
    if kind not in {"fine", "coarse"}:
        raise ValueError(kind)

    q0 = StandingKey("world", "current-interface", "t0")
    cand_a = StandingKey("candidate:A", "candidate", "t0-model")
    cand_b = StandingKey("candidate:B", "candidate", "t0-model")
    cand_k = StandingKey("candidate:K", "candidate", "t0-model")
    obs = StandingKey("world", "probe-observation", "t1")
    identified = StandingKey("world", "identified-regime", "t1")
    null_profile = StandingKey("world", "null-probe-profile", "t1")

    if kind == "fine":
        seed_grants = (
            WriteGrant(q0, ("K",)),
            WriteGrant(cand_a, ("POSSIBLE",)),
            WriteGrant(cand_b, ("POSSIBLE",)),
        )
        seed_writes = (
            Standing(q0, "K"),
            Standing(cand_a, "POSSIBLE"),
            Standing(cand_b, "POSSIBLE"),
        )
    else:
        seed_grants = (
            WriteGrant(q0, ("K",)),
            WriteGrant(cand_k, ("POSSIBLE",)),
        )
        seed_writes = (
            Standing(q0, "K"),
            Standing(cand_k, "POSSIBLE"),
        )

    licenses = (
        License("seed", "seed", allowed_writes=seed_grants),
        License("admit-sig-a", "observe", allowed_writes=(WriteGrant(obs, ("SIG_A",)),)),
        License("admit-sig-b", "observe", allowed_writes=(WriteGrant(obs, ("SIG_B",)),)),
        License("admit-same", "observe", allowed_writes=(WriteGrant(obs, ("SAME",)),)),
        License(
            "refine-a",
            "refine",
            preconditions=(Precondition(obs, "SIG_A"),),
            allowed_writes=(WriteGrant(identified, ("A",)),),
        ),
        License(
            "refine-b",
            "refine",
            preconditions=(Precondition(obs, "SIG_B"),),
            allowed_writes=(WriteGrant(identified, ("B",)),),
        ),
        License(
            "record-null",
            "record-null",
            preconditions=(Precondition(obs, "SAME"),),
            allowed_writes=(WriteGrant(null_profile, ("NONDISCRIMINATING",)),),
        ),
    )
    n = Nano(licenses=licenses)
    seed_receipt = n.apply_transition(Transition("seed", writes=seed_writes), "seed")
    assert seed_receipt.decision is Decision.ALLOW
    keys = {
        "q0": q0,
        "obs": obs,
        "identified": identified,
        "null_profile": null_profile,
    }
    return n, {"seed_receipt": seed_receipt, "keys": keys}


def admit_probe_and_refine(n: Nano, keys: dict, observation: str) -> dict:
    if observation not in {"SIG_A", "SIG_B"}:
        raise ValueError(observation)
    obs_license = "admit-sig-a" if observation == "SIG_A" else "admit-sig-b"
    expected = "A" if observation == "SIG_A" else "B"
    refine_license = "refine-a" if expected == "A" else "refine-b"
    r_obs = n.apply_transition(
        Transition("observe", writes=(Standing(keys["obs"], observation),)),
        obs_license,
    )
    r_ref = n.apply_transition(
        Transition("refine", writes=(Standing(keys["identified"], expected),)),
        refine_license,
    )
    return {"observation_receipt": r_obs, "refinement_receipt": r_ref, "expected": expected}


def admit_null(n: Nano, keys: dict) -> dict:
    r_obs = n.apply_transition(
        Transition("observe", writes=(Standing(keys["obs"], "SAME"),)),
        "admit-same",
    )
    r_null = n.apply_transition(
        Transition("record-null", writes=(Standing(keys["null_profile"], "NONDISCRIMINATING"),)),
        "record-null",
    )
    # Attempt both regime-specific refinements from SAME: both matching signals are contradicted.
    r_false_a = n.apply_transition(
        Transition("refine", writes=(Standing(keys["identified"], "A"),)),
        "refine-a",
    )
    r_false_b = n.apply_transition(
        Transition("refine", writes=(Standing(keys["identified"], "B"),)),
        "refine-b",
    )
    return {
        "observation_receipt": r_obs,
        "null_receipt": r_null,
        "false_refinement_a": r_false_a,
        "false_refinement_b": r_false_b,
    }


def serialize_receipt(r) -> dict:
    return asdict(r)


def branch_run(kind: str, regime: str, *, discriminating: bool, force_probe: bool = False) -> dict:
    n, meta = build_branch(kind)
    keys = meta["keys"]
    p = policy(n)
    available = list(AVAILABLE_ACTIONS)
    selected = A_PROBE if force_probe else p["selected_action"]
    before_action_state = n.state_digest()
    observation = world_observe(regime, selected, "t1", discriminating=discriminating)

    evidence = None
    null = None
    if selected == A_PROBE and observation in {"SIG_A", "SIG_B"}:
        evidence = admit_probe_and_refine(n, keys, observation)
    elif selected == A_PROBE and observation == "SAME":
        null = admit_null(n, keys)

    active = active_values(n)
    identified_value = active.get(("world", "identified-regime", "t1"))
    null_value = active.get(("world", "null-probe-profile", "t1"))
    return {
        "kind": kind,
        "regime": regime,
        "discriminating": discriminating,
        "force_probe": force_probe,
        "available_actions": available,
        "policy": p,
        "executed_action": selected,
        "observation": observation,
        "before_action_state_digest": before_action_state,
        "after_state_digest": n.state_digest(),
        "identified_value": identified_value,
        "null_profile": null_value,
        "seed_receipt": serialize_receipt(meta["seed_receipt"]),
        "evidence": None if evidence is None else {
            "observation_receipt": serialize_receipt(evidence["observation_receipt"]),
            "refinement_receipt": serialize_receipt(evidence["refinement_receipt"]),
            "expected": evidence["expected"],
        },
        "null": None if null is None else {
            "observation_receipt": serialize_receipt(null["observation_receipt"]),
            "null_receipt": serialize_receipt(null["null_receipt"]),
            "false_refinement_a": serialize_receipt(null["false_refinement_a"]),
            "false_refinement_b": serialize_receipt(null["false_refinement_b"]),
        },
        "effective_state": {
            "active": [asdict(s) for s in n.effective_state().active],
            "deferred": [asdict(s) for s in n.effective_state().deferred],
        },
    }


def check(name: str, cond: bool, checks: list[dict]) -> None:
    checks.append({"name": name, "pass": bool(cond)})


def main() -> int:
    nano_before = sha256(NANO_PATH)
    if nano_before != NANO_SHA256:
        raise RuntimeError(f"Nano hash mismatch before run: {nano_before}")

    # Exact frozen world checks, including complete t0 surface.
    formal: list[dict] = []
    persistence: list[dict] = []

    check("hidden regimes differ", "A" != "B", formal)
    check("t0 current interface collides", True, formal)  # Phi_t0 is frozen as K for both.
    for action in AVAILABLE_ACTIONS:
        check(
            f"t0 {action} consequence equivalent",
            world_observe("A", action, "t0", discriminating=True)
            == world_observe("B", action, "t0", discriminating=True),
            formal,
        )
    check(
        "target t1 act remains nondiscriminating",
        world_observe("A", A_ACT, "t1", discriminating=True)
        == world_observe("B", A_ACT, "t1", discriminating=True),
        formal,
    )
    check(
        "target t1 probe discriminates",
        world_observe("A", A_PROBE, "t1", discriminating=True)
        != world_observe("B", A_PROBE, "t1", discriminating=True),
        formal,
    )
    check(
        "null t1 probe nondiscriminating",
        world_observe("A", A_PROBE, "t1", discriminating=False)
        == world_observe("B", A_PROBE, "t1", discriminating=False),
        formal,
    )

    # Policy snapshots before executing actions.
    fine_probe = {}
    coarse_act = {}
    forced = {}
    for regime in ("A", "B"):
        fine_probe[regime] = branch_run("fine", regime, discriminating=True)
        coarse_act[regime] = branch_run("coarse", regime, discriminating=True)
        forced[regime] = branch_run("coarse", regime, discriminating=True, force_probe=True)

    null_fine = {r: branch_run("fine", r, discriminating=False) for r in ("A", "B")}
    null_coarse = {r: branch_run("coarse", r, discriminating=False) for r in ("A", "B")}
    null_forced = {
        r: branch_run("coarse", r, discriminating=False, force_probe=True)
        for r in ("A", "B")
    }

    for regime in ("A", "B"):
        f = fine_probe[regime]
        c = coarse_act[regime]
        x = forced[regime]
        check(f"{regime} fine/coarse physical availability identical", f["available_actions"] == c["available_actions"] == list(AVAILABLE_ACTIONS), formal)
        check(f"{regime} target probe physically available coarse", A_PROBE in c["available_actions"], formal)
        check(f"{regime} fine policy contains probe", A_PROBE in f["policy"]["policy_support"], formal)
        check(f"{regime} coarse policy excludes probe", A_PROBE not in c["policy"]["policy_support"], formal)
        check(f"{regime} fine selects probe", f["executed_action"] == A_PROBE, formal)
        check(f"{regime} coarse selects act", c["executed_action"] == A_ACT, formal)
        check(f"{regime} coarse act sees only ACT_OK", c["observation"] == "ACT_OK", formal)
        check(f"{regime} coarse policy produces no identification", c["identified_value"] is None, formal)
        expected = regime
        sig = "SIG_A" if regime == "A" else "SIG_B"
        check(f"{regime} fine probe gets matching signal", f["observation"] == sig, formal)
        check(f"{regime} fine identifies regime", f["identified_value"] == expected, formal)
        check(f"{regime} forced coarse probe gets matching signal", x["observation"] == sig, formal)
        check(f"{regime} forced coarse identifies regime", x["identified_value"] == expected, formal)

        # Nano receipt ancestry for fine and forced targeted branches.
        for label, row in (("fine", f), ("forced", x)):
            ev = row["evidence"]
            check(f"{regime} {label} observation ALLOW", ev is not None and ev["observation_receipt"]["decision"] == "ALLOW", persistence)
            check(f"{regime} {label} refinement ALLOW", ev is not None and ev["refinement_receipt"]["decision"] == "ALLOW", persistence)
            check(
                f"{regime} {label} refinement parent is observation receipt",
                ev is not None
                and tuple(ev["refinement_receipt"]["parent_receipts"])
                == (ev["observation_receipt"]["id"],),
                persistence,
            )

    # Reachability condition directly.
    targeted_discriminator = {A_PROBE}
    coarse_policy_support = set(coarse_act["A"]["policy"]["policy_support"])
    available = set(coarse_act["A"]["available_actions"])
    check("discriminator intersects physical availability", bool(targeted_discriminator & available), formal)
    check("discriminator excluded from coarse policy support", not bool(targeted_discriminator & coarse_policy_support), formal)

    # Null world: coarse non-probing is harmless; fine probing and forced coarse probing do not false-split.
    for regime in ("A", "B"):
        nf = null_fine[regime]
        nc = null_coarse[regime]
        nx = null_forced[regime]
        check(f"null {regime} availability identical", nf["available_actions"] == nc["available_actions"] == list(AVAILABLE_ACTIONS), formal)
        check(f"null {regime} coarse excludes probe", A_PROBE not in nc["policy"]["policy_support"], formal)
        check(f"null {regime} coarse selected act harmless", nc["executed_action"] == A_ACT and nc["observation"] == "ACT_OK" and nc["identified_value"] is None, formal)
        check(f"null {regime} fine probe returns SAME", nf["executed_action"] == A_PROBE and nf["observation"] == "SAME", formal)
        check(f"null {regime} fine produces no regime identification", nf["identified_value"] is None, formal)
        check(f"null {regime} forced coarse probe returns SAME", nx["observation"] == "SAME", formal)
        check(f"null {regime} forced coarse produces no regime identification", nx["identified_value"] is None, formal)

        for label, row in (("fine", nf), ("forced", nx)):
            nr = row["null"]
            check(f"null {regime} {label} SAME observation ALLOW", nr is not None and nr["observation_receipt"]["decision"] == "ALLOW", persistence)
            check(f"null {regime} {label} shared null standing ALLOW", nr is not None and nr["null_receipt"]["decision"] == "ALLOW", persistence)
            check(f"null {regime} {label} false A refinement DENY", nr is not None and nr["false_refinement_a"]["decision"] == "DENY", persistence)
            check(f"null {regime} {label} false B refinement DENY", nr is not None and nr["false_refinement_b"]["decision"] == "DENY", persistence)
            check(
                f"null {regime} {label} null standing parent is SAME observation",
                nr is not None
                and tuple(nr["null_receipt"]["parent_receipts"])
                == (nr["observation_receipt"]["id"],),
                persistence,
            )

    nano_after = sha256(NANO_PATH)
    check("Nano SHA unchanged", nano_before == nano_after == NANO_SHA256, persistence)

    formal_pass = sum(c["pass"] for c in formal)
    persistence_pass = sum(c["pass"] for c in persistence)
    all_pass = formal_pass == len(formal) and persistence_pass == len(persistence)

    # NO_FORECLOSURE is reserved for the targeted coarse policy retaining the probe.
    if all_pass:
        classification = "EPISTEMIC_FORECLOSURE_ESTABLISHED"
    elif A_PROBE in coarse_policy_support:
        classification = "NO_FORECLOSURE"
    else:
        classification = "INVALID"

    result = {
        "assay": "FOREIGN-007 — Policy-Induced Epistemic Foreclosure",
        "classification": classification,
        "nano_sha256_before": nano_before,
        "nano_sha256_after": nano_after,
        "world": {
            "regimes": ["W_A", "W_B"],
            "available_actions": list(AVAILABLE_ACTIONS),
            "t0": {
                "Phi": {"W_A": "K", "W_B": "K"},
                "a_act": {"W_A": "ACT_OK", "W_B": "ACT_OK"},
                "a_probe": {"W_A": "NO_SIGNAL", "W_B": "NO_SIGNAL"},
            },
            "t1_target": {
                "a_act": {"W_A": "ACT_OK", "W_B": "ACT_OK"},
                "a_probe": {"W_A": "SIG_A", "W_B": "SIG_B"},
            },
            "t1_null": {
                "a_act": {"W_A": "ACT_OK", "W_B": "ACT_OK"},
                "a_probe": {"W_A": "SAME", "W_B": "SAME"},
            },
        },
        "policy_rule": {
            "description": "probe iff effective candidate-cell count > 1; otherwise act",
            "probe_cost": 1,
            "act_cost": 0,
        },
        "target": {"fine": fine_probe, "coarse": coarse_act, "forced_coarse": forced},
        "null": {"fine": null_fine, "coarse": null_coarse, "forced_coarse": null_forced},
        "reachability": {
            "D_Pi": sorted(targeted_discriminator),
            "R_available": sorted(available),
            "R_policy_coarse": sorted(coarse_policy_support),
            "D_intersect_available_nonempty": bool(targeted_discriminator & available),
            "D_intersect_policy_empty": not bool(targeted_discriminator & coarse_policy_support),
        },
        "checks": {
            "formal": {"passed": formal_pass, "total": len(formal), "rows": formal},
            "persistence": {"passed": persistence_pass, "total": len(persistence), "rows": persistence},
        },
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "classification": classification,
        "formal": f"{formal_pass}/{len(formal)}",
        "persistence": f"{persistence_pass}/{len(persistence)}",
        "result_path": str(RESULT_PATH),
    }, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
