#!/usr/bin/env python3
"""OpenCore Base 002: global reopening without global replacement.

Question
--------
Can one globally available counterexample withdraw the current authority of a
shared invariant and propagate uncertainty through heterogeneous local views,
while lacking authority to install a successor invariant until separately
licensed later evidence exists?

This experiment reuses the 12-unit geometry from Base-001 and Nano V0 unchanged.
It deliberately separates three world transitions:

    ADMIT(G) != REOPEN(G) != REPLACE(G, G')

Constructed sequence per world
------------------------------
1. Admit shared invariant G and status G_STATUS=EFFECTIVE.
2. All 12 units can read the shared world; 8 relevant units materialize H_i
   standings whose licenses require G_STATUS=EFFECTIVE.
3. All 12 units learn unrelated L_i standings *after* G with no G precondition.
4. Admit a counterexample E* whose externally supplied role is REFUTES_G.
5. E* licenses REOPEN(G): write G_STATUS=REOPENED and revoke G's producing
   license.  No H_i/L_i cleanup writes or deletes occur.
6. Using that same reopen capability, attempt to install G'.  Nano must DENY
   because replacement is outside E*'s effect envelope; naive persistence
   accepts the same write.
7. Also preview a genuine successor-install transition under its authentic
   replacement license *before* later evidence E' exists. Nano must DEFER.
8. Verify the REOPENED world is a real in-process persistent intermediate state:
   G-derived H_i are ineffective, relevant local projections report uncertainty,
   unrelated L_i remain effective, and G' is absent.  An unrelated checkpoint
   transition is executed and REOPENED must remain effective afterward.
9. Admit later evidence E' under a separate license.
10. The authentic replacement transition may now install G' and mark the world
    status REPLACED.
11. Relevant units may materialize successor-derived K_i standings requiring G'.
    Irrelevant units remain unchanged; unrelated L_i survive.

Claim ceiling
-------------
Constructed Base-level mechanics only. Counterexample constitution, later-evidence
constitution, unit relevance, projection functions, licenses, and dependency
semantics are externally supplied. This does not establish autonomous refutation,
autonomous successor discovery, general distributed learning, or a general Base
architecture. Nano V0 remains unchanged and its journal remains in-process only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from base_001_shared_world import (
    N_RELEVANT,
    N_UNITS,
    NaiveStore,
    active_map,
    deferred_map,
    make_units,
    receipt_writing,
)
from nano import Decision, License, Nano, Precondition, Standing, StandingKey, Transition, WriteGrant

HERE = Path(__file__).resolve().parent
NANO_PATH = HERE / "nano.py"
BASE001_PATH = HERE / "base_001_shared_world.py"
NANO_EXPECTED_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"
BASE001_EXPECTED_SHA256 = "e8b435da6b3e18a7d718d5add22d2c7575e23bae787bf92f3dc99827f9bc1463"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def opaque(seed: int, label: str) -> str:
    return hashlib.sha256(f"base-002:{seed}:{label}".encode()).hexdigest()[:16]


def key(seed: int, label: str, dimension: str, scope: str) -> StandingKey:
    return StandingKey(opaque(seed, label), dimension, scope)


def successor_projection(mode: str, private_token: str, relevant: bool, successor_effective: bool) -> str:
    if not relevant or not successor_effective:
        return f"BASE:{private_token}"
    return f"GPRIME:{mode}:{private_token}"


def reopened_projection(private_token: str, relevant: bool, status: str | None) -> str:
    if relevant and status == "REOPENED":
        return f"UNCERTAIN:{private_token}"
    return f"BASE:{private_token}"


def clone_naive(store: NaiveStore) -> NaiveStore:
    clone = NaiveStore(Standing(k, v) for k, v in store.current.items())
    clone.revoked_licenses = set(store.revoked_licenses)
    return clone


def strict_reopen_control(seed: int) -> dict:
    """Natural strict contract: current G is a guard, but Nano makes it a parent.

    This deliberately exposes a Nano V0 limitation. A reopening transition should
    plausibly require that G is currently EFFECTIVE, yet the resulting REOPENED
    standing should not derive its authority from the very G warrant it revokes.
    Nano V0 has only one precondition class, and `_parents_for()` treats every
    precondition source receipt as a warrant parent.
    """
    g_status = key(seed, "strict:G-status", "global-status", "world")
    counterexample = key(seed, "strict:E-star", "counterexample", "world")
    l_g = License(
        opaque(seed, "strict:license:G"),
        "strict-admit-G",
        allowed_writes=(WriteGrant(g_status, ("EFFECTIVE",)),),
    )
    l_e = License(
        opaque(seed, "strict:license:E"),
        "strict-admit-counterexample",
        allowed_writes=(WriteGrant(counterexample, ("REFUTES_G",)),),
    )
    l_reopen = License(
        opaque(seed, "strict:license:reopen"),
        "strict-reopen-G",
        preconditions=(
            Precondition(g_status, "EFFECTIVE"),
            Precondition(counterexample, "REFUTES_G"),
        ),
        allowed_writes=(WriteGrant(g_status, ("REOPENED",)),),
        allowed_revocations=(l_g.id,),
    )
    nano = Nano(licenses=(l_g, l_e, l_reopen))
    g_receipt = nano.apply_transition(
        Transition("strict-admit-G", writes=(Standing(g_status, "EFFECTIVE"),)),
        l_g.id,
    )
    e_receipt = nano.apply_transition(
        Transition("strict-admit-counterexample", writes=(Standing(counterexample, "REFUTES_G"),)),
        l_e.id,
    )
    reopen_receipt = nano.apply_transition(
        Transition(
            "strict-reopen-G",
            writes=(Standing(g_status, "REOPENED"),),
            revoke_licenses=(l_g.id,),
        ),
        l_reopen.id,
    )
    active = active_map(nano)
    deferred = deferred_map(nano)
    return {
        "transition_decision": reopen_receipt.decision.value,
        "reopened_active": active.get(g_status) == "REOPENED",
        "reopened_deferred": deferred.get(g_status) == "REOPENED",
        "parent_count": len(reopen_receipt.parent_receipts),
        "parent_includes_old_G": g_receipt.id in reopen_receipt.parent_receipts,
        "parent_includes_counterexample": e_receipt.id in reopen_receipt.parent_receipts,
        "failure": "PRECONDITION_COLLAPSED_INTO_WARRANT_PARENT",
    }


@dataclass(frozen=True)
class WorldKeys:
    g_content: StandingKey
    g_status: StandingKey
    counterexample: StandingKey
    later_evidence: StandingKey
    gprime: StandingKey
    checkpoint: StandingKey


def trial(seed: int) -> dict:
    units = make_units(seed)
    relevant_units = tuple(u for u in units if u.relevant)
    irrelevant_units = tuple(u for u in units if not u.relevant)
    assert len(relevant_units) == N_RELEVANT
    assert len(irrelevant_units) == N_UNITS - N_RELEVANT
    strict_reopen = strict_reopen_control(seed)

    wk = WorldKeys(
        g_content=key(seed, "G-content", "global-invariant", "world"),
        g_status=key(seed, "G-status", "global-status", "world"),
        counterexample=key(seed, "E-star", "counterexample", "world"),
        later_evidence=key(seed, "E-prime", "successor-evidence", "world"),
        gprime=key(seed, "G-prime", "global-invariant", "world"),
        checkpoint=key(seed, "checkpoint", "control", "world"),
    )
    h_keys = {u.index: key(seed, f"H:{u.index}", "local-g-derived", f"unit:{u.index}") for u in units}
    l_keys = {u.index: key(seed, f"L:{u.index}", "local-independent", f"unit:{u.index}") for u in units}
    k_keys = {u.index: key(seed, f"K:{u.index}", "local-gprime-derived", f"unit:{u.index}") for u in units}

    # ADMIT(G): one receipt supplies both the invariant content and its EFFECTIVE status.
    l_admit_g = License(
        opaque(seed, "license:admit-G"),
        "admit-shared-invariant",
        allowed_writes=(
            WriteGrant(wk.g_content, ("G",)),
            WriteGrant(wk.g_status, ("EFFECTIVE",)),
        ),
    )

    # External apparatus constitutes E* only as a counterexample to G.
    l_admit_counterexample = License(
        opaque(seed, "license:admit-counterexample"),
        "admit-counterexample",
        allowed_writes=(WriteGrant(wk.counterexample, ("REFUTES_G",)),),
    )

    # E* can reopen G, but cannot create G'.  Reopening both records a persistent
    # REOPENED status and revokes the receipt-producing license for G.
    l_reopen = License(
        opaque(seed, "license:reopen-G"),
        "reopen-global-invariant",
        preconditions=(Precondition(wk.counterexample, "REFUTES_G"),),
        allowed_writes=(WriteGrant(wk.g_status, ("REOPENED",)),),
        allowed_revocations=(l_admit_g.id,),
    )

    l_checkpoint = License(
        opaque(seed, "license:checkpoint"),
        "record-reopened-checkpoint",
        preconditions=(Precondition(wk.g_status, "REOPENED"),),
        allowed_writes=(WriteGrant(wk.checkpoint, ("AFTER_REOPEN",)),),
    )

    # Later evidence is independently admitted.
    l_admit_later = License(
        opaque(seed, "license:admit-later-evidence"),
        "admit-successor-evidence",
        allowed_writes=(WriteGrant(wk.later_evidence, ("SUPPORTS_GPRIME",)),),
    )

    # Authentic successor-install authority exists from the beginning, but cannot
    # execute until both the reopened world status and later evidence are effective.
    l_replace = License(
        opaque(seed, "license:replace-G"),
        "install-successor-invariant",
        preconditions=(
            Precondition(wk.g_status, "REOPENED"),
            Precondition(wk.later_evidence, "SUPPORTS_GPRIME"),
        ),
        allowed_writes=(
            WriteGrant(wk.gprime, ("GPRIME",)),
            WriteGrant(wk.g_status, ("REPLACED",)),
        ),
    )

    h_licenses: dict[int, License] = {}
    l_licenses: dict[int, License] = {}
    k_licenses: dict[int, License] = {}
    for u in units:
        if u.relevant:
            h_licenses[u.index] = License(
                opaque(seed, f"license:H:{u.index}"),
                f"derive-from-G:{u.index}",
                preconditions=(Precondition(wk.g_status, "EFFECTIVE"),),
                allowed_writes=(WriteGrant(h_keys[u.index], (u.project(True),)),),
            )
            k_licenses[u.index] = License(
                opaque(seed, f"license:K:{u.index}"),
                f"derive-from-Gprime:{u.index}",
                preconditions=(Precondition(wk.gprime, "GPRIME"),),
                allowed_writes=(
                    WriteGrant(
                        k_keys[u.index],
                        (successor_projection(u.mode, u.private_token, True, True),),
                    ),
                ),
            )
        l_licenses[u.index] = License(
            opaque(seed, f"license:L:{u.index}"),
            f"independent-local-learn:{u.index}",
            allowed_writes=(WriteGrant(l_keys[u.index], (f"LOCAL:{u.private_token}",)),),
        )

    licenses = (
        l_admit_g,
        l_admit_counterexample,
        l_reopen,
        l_checkpoint,
        l_admit_later,
        l_replace,
        *h_licenses.values(),
        *l_licenses.values(),
        *k_licenses.values(),
    )
    nano = Nano(licenses=licenses)
    naive_clean = NaiveStore()

    # --- ADMIT(G) -----------------------------------------------------------
    admit_g = Transition(
        "admit-shared-invariant",
        writes=(Standing(wk.g_content, "G"), Standing(wk.g_status, "EFFECTIVE")),
    )
    assert nano.apply_transition(admit_g, l_admit_g.id).decision is Decision.ALLOW
    naive_clean.apply(admit_g)

    # Relevant units materialize G-derived state. All units then learn unrelated
    # local state after G to make temporal ancestry a hostile control.
    for u in relevant_units:
        t = Transition(f"derive-from-G:{u.index}", writes=(Standing(h_keys[u.index], u.project(True)),))
        assert nano.apply_transition(t, h_licenses[u.index].id).decision is Decision.ALLOW
        naive_clean.apply(t)

    for u in units:
        t = Transition(
            f"independent-local-learn:{u.index}",
            writes=(Standing(l_keys[u.index], f"LOCAL:{u.private_token}"),),
        )
        assert nano.apply_transition(t, l_licenses[u.index].id).decision is Decision.ALLOW
        naive_clean.apply(t)

    # --- COUNTEREXAMPLE -----------------------------------------------------
    admit_counterexample = Transition(
        "admit-counterexample",
        writes=(Standing(wk.counterexample, "REFUTES_G"),),
    )
    assert nano.apply_transition(admit_counterexample, l_admit_counterexample.id).decision is Decision.ALLOW
    naive_clean.apply(admit_counterexample)

    # The proper replacement license exists but later evidence does not. This is
    # an authentic capability that is not currently authorized to execute.
    install_successor = Transition(
        "install-successor-invariant",
        writes=(Standing(wk.gprime, "GPRIME"), Standing(wk.g_status, "REPLACED")),
    )
    replace_preview_before_reopen = nano.check_transition(install_successor, l_replace.id)
    # At this point status is still EFFECTIVE and later evidence is absent, so DENY
    # dominates DEFER. The decisive missing-evidence check is repeated after reopen.
    assert replace_preview_before_reopen.decision is Decision.DENY

    # --- REOPEN(G) ----------------------------------------------------------
    reopen = Transition(
        "reopen-global-invariant",
        writes=(Standing(wk.g_status, "REOPENED"),),
        revoke_licenses=(l_admit_g.id,),
    )
    reopen_receipt = nano.apply_transition(reopen, l_reopen.id)
    assert reopen_receipt.decision is Decision.ALLOW
    naive_clean.apply(reopen)
    assert not reopen.deletes

    # Same E* / same reopen capability now tries to manufacture G'.  Preconditions
    # are satisfied. Only the effect ceiling should stop the replacement laundering.
    bad_replace = Transition(
        "reopen-global-invariant",
        writes=(Standing(wk.gprime, "GPRIME"),),
    )
    naive_attack = clone_naive(naive_clean)
    naive_bad_replace = naive_attack.apply(bad_replace)
    nano_bad_replace = nano.apply_transition(bad_replace, l_reopen.id)

    # Genuine replacement license after reopen but before E' must DEFER rather than
    # inherit replacement authority from the counterexample.
    naive_missing_evidence = clone_naive(naive_clean)
    naive_replace_without_later = naive_missing_evidence.apply(install_successor)
    replace_check_without_later = nano.check_transition(install_successor, l_replace.id)
    nano_replace_without_later = nano.apply_transition(install_successor, l_replace.id)

    # --- PERSISTENT INTERMEDIATE REOPENED WORLD ----------------------------
    active_reopened = active_map(nano)
    deferred_reopened = deferred_map(nano)
    reopened_status_persistent = active_reopened.get(wk.g_status) == "REOPENED"
    g_content_withdrawn = wk.g_content not in active_reopened and wk.g_content in deferred_reopened
    h_withdrawn = sum(h_keys[u.index] not in active_reopened and h_keys[u.index] in deferred_reopened for u in relevant_units)
    l_survive_reopen = sum(active_reopened.get(l_keys[u.index]) == f"LOCAL:{u.private_token}" for u in units)
    no_successor_before_evidence = wk.gprime not in active_reopened

    reopened_views = {
        u.index: reopened_projection(u.private_token, u.relevant, active_reopened.get(wk.g_status))
        for u in units
    }
    uncertainty_propagation = sum(
        reopened_views[u.index] == f"UNCERTAIN:{u.private_token}" for u in relevant_units
    )
    irrelevant_reopen_disturbance = sum(
        reopened_views[u.index] != f"BASE:{u.private_token}" for u in irrelevant_units
    )

    # Execute an unrelated transaction while the world is reopened. The status must
    # remain REOPENED afterward: it is state, not a transient return code.
    checkpoint = Transition(
        "record-reopened-checkpoint",
        writes=(Standing(wk.checkpoint, "AFTER_REOPEN"),),
    )
    checkpoint_receipt = nano.apply_transition(checkpoint, l_checkpoint.id)
    assert checkpoint_receipt.decision is Decision.ALLOW
    naive_clean.apply(checkpoint)
    active_after_checkpoint = active_map(nano)
    reopened_survives_checkpoint = (
        active_after_checkpoint.get(wk.g_status) == "REOPENED"
        and active_after_checkpoint.get(wk.checkpoint) == "AFTER_REOPEN"
    )

    # --- LATER EVIDENCE -> REPLACE(G,G') -----------------------------------
    admit_later = Transition(
        "admit-successor-evidence",
        writes=(Standing(wk.later_evidence, "SUPPORTS_GPRIME"),),
    )
    assert nano.apply_transition(admit_later, l_admit_later.id).decision is Decision.ALLOW
    naive_clean.apply(admit_later)

    replace_after_later = nano.apply_transition(install_successor, l_replace.id)
    naive_replace_after_later = naive_clean.apply(install_successor)
    assert replace_after_later.decision is Decision.ALLOW

    active_replaced = active_map(nano)
    assert active_replaced.get(wk.gprime) == "GPRIME"
    assert active_replaced.get(wk.g_status) == "REPLACED"

    # Relevant units may now materialize successor-specific consequences.
    for u in relevant_units:
        kval = successor_projection(u.mode, u.private_token, True, True)
        t = Transition(f"derive-from-Gprime:{u.index}", writes=(Standing(k_keys[u.index], kval),))
        assert nano.apply_transition(t, k_licenses[u.index].id).decision is Decision.ALLOW
        naive_clean.apply(t)

    active_final = active_map(nano)
    deferred_final = deferred_map(nano)
    successor_response = sum(
        active_final.get(k_keys[u.index]) == successor_projection(u.mode, u.private_token, True, True)
        for u in relevant_units
    )
    successor_irrelevant_disturbance = sum(k_keys[u.index] in active_final for u in irrelevant_units)
    l_survive_replacement = sum(active_final.get(l_keys[u.index]) == f"LOCAL:{u.private_token}" for u in units)
    old_h_still_withdrawn = sum(
        h_keys[u.index] not in active_final and h_keys[u.index] in deferred_final for u in relevant_units
    )

    # Provenance/authority checks from Nano's public journal.
    g_receipt = receipt_writing(nano, wk.g_content)
    counter_receipt = receipt_writing(nano, wk.counterexample)
    reopened_status_receipt = next(
        r for r in nano.journal
        if r.decision is Decision.ALLOW
        and any(s.key == wk.g_status and s.value == "REOPENED" for s in r.writes)
    )
    later_receipt = receipt_writing(nano, wk.later_evidence)
    gprime_receipt = receipt_writing(nano, wk.gprime)

    reopen_warranted_by_counterexample = counter_receipt.id in reopened_status_receipt.parent_receipts
    reopen_not_warranted_by_invalidated_g = g_receipt.id not in reopened_status_receipt.parent_receipts
    replacement_has_later_evidence_parent = later_receipt.id in gprime_receipt.parent_receipts
    replacement_has_reopened_parent = reopened_status_receipt.id in gprime_receipt.parent_receipts

    independent_parentless = all(len(receipt_writing(nano, l_keys[u.index]).parent_receipts) == 0 for u in units)

    return {
        "seed": seed,
        "units": N_UNITS,
        "relevant_units": N_RELEVANT,
        "admit_reopen_replace_distinct": True,
        "strict_reopen_control": strict_reopen,
        "reopen": {
            "nano": reopen_receipt.decision.value,
            "writes": len(reopen.writes),
            "deletes": len(reopen.deletes),
            "revocations": len(reopen.revoke_licenses),
            "status_persistent": reopened_status_persistent,
            "status_survives_unrelated_checkpoint": reopened_survives_checkpoint,
            "g_content_withdrawn": g_content_withdrawn,
            "g_derived_withdrawn": h_withdrawn,
            "unrelated_local_survive": l_survive_reopen,
            "uncertainty_propagation": uncertainty_propagation,
            "irrelevant_disturbance": irrelevant_reopen_disturbance,
            "no_successor_before_later_evidence": no_successor_before_evidence,
            "warranted_by_counterexample": reopen_warranted_by_counterexample,
            "not_warranted_by_invalidated_g": reopen_not_warranted_by_invalidated_g,
        },
        "replacement_laundering": {
            "naive_same_counterexample": naive_bad_replace.value,
            "nano_same_counterexample": nano_bad_replace.decision.value,
            "nano_reasons": nano_bad_replace.reasons,
        },
        "authentic_replace_before_later_evidence": {
            "naive": naive_replace_without_later.value,
            "nano_check": replace_check_without_later.decision.value,
            "nano_apply": nano_replace_without_later.decision.value,
            "nano_reasons": nano_replace_without_later.reasons,
        },
        "replacement_after_later_evidence": {
            "naive": naive_replace_after_later.value,
            "nano": replace_after_later.decision.value,
            "has_later_evidence_parent": replacement_has_later_evidence_parent,
            "has_reopened_parent": replacement_has_reopened_parent,
        },
        "final": {
            "successor_relevant_response": successor_response,
            "successor_irrelevant_disturbance": successor_irrelevant_disturbance,
            "unrelated_local_survive": l_survive_replacement,
            "old_g_derived_still_withdrawn": old_h_still_withdrawn,
            "independent_post_g_parentless": independent_parentless,
        },
    }


def sweep(n: int, start_seed: int = 0) -> dict:
    totals = {
        "worlds": n,
        "reopen_allow": 0,
        "reopen_status_persistent": 0,
        "reopen_survives_checkpoint": 0,
        "g_content_withdrawn": 0,
        "g_derived_withdrawn": 0,
        "unrelated_survive_reopen": 0,
        "uncertainty_propagation": 0,
        "irrelevant_reopen_disturbance": 0,
        "no_successor_before_later": 0,
        "reopen_warranted_by_counterexample": 0,
        "reopen_not_warranted_by_invalidated_g": 0,
        "laundering_naive_allow": 0,
        "laundering_nano_allow": 0,
        "laundering_nano_deny": 0,
        "replace_before_later_naive_allow": 0,
        "replace_before_later_nano_defer": 0,
        "replace_after_later_nano_allow": 0,
        "replace_has_later_parent": 0,
        "replace_has_reopened_parent": 0,
        "successor_relevant_response": 0,
        "successor_irrelevant_disturbance": 0,
        "unrelated_survive_final": 0,
        "old_g_derived_still_withdrawn": 0,
        "independent_post_g_parentless": 0,
        "strict_transition_allow": 0,
        "strict_reopened_active": 0,
        "strict_reopened_deferred": 0,
        "strict_parent_includes_old_g": 0,
        "strict_parent_includes_counterexample": 0,
    }
    first = None
    failures: list[dict] = []

    for seed in range(start_seed, start_seed + n):
        r = trial(seed)
        if first is None:
            first = r
        rr = r["reopen"]
        rl = r["replacement_laundering"]
        rb = r["authentic_replace_before_later_evidence"]
        ra = r["replacement_after_later_evidence"]
        rf = r["final"]
        sr = r["strict_reopen_control"]

        totals["reopen_allow"] += int(rr["nano"] == "ALLOW")
        totals["reopen_status_persistent"] += int(rr["status_persistent"])
        totals["reopen_survives_checkpoint"] += int(rr["status_survives_unrelated_checkpoint"])
        totals["g_content_withdrawn"] += int(rr["g_content_withdrawn"])
        totals["g_derived_withdrawn"] += rr["g_derived_withdrawn"]
        totals["unrelated_survive_reopen"] += rr["unrelated_local_survive"]
        totals["uncertainty_propagation"] += rr["uncertainty_propagation"]
        totals["irrelevant_reopen_disturbance"] += rr["irrelevant_disturbance"]
        totals["no_successor_before_later"] += int(rr["no_successor_before_later_evidence"])
        totals["reopen_warranted_by_counterexample"] += int(rr["warranted_by_counterexample"])
        totals["reopen_not_warranted_by_invalidated_g"] += int(rr["not_warranted_by_invalidated_g"])
        totals["laundering_naive_allow"] += int(rl["naive_same_counterexample"] == "ALLOW")
        totals["laundering_nano_allow"] += int(rl["nano_same_counterexample"] == "ALLOW")
        totals["laundering_nano_deny"] += int(rl["nano_same_counterexample"] == "DENY")
        totals["replace_before_later_naive_allow"] += int(rb["naive"] == "ALLOW")
        totals["replace_before_later_nano_defer"] += int(rb["nano_apply"] == "DEFER")
        totals["replace_after_later_nano_allow"] += int(ra["nano"] == "ALLOW")
        totals["replace_has_later_parent"] += int(ra["has_later_evidence_parent"])
        totals["replace_has_reopened_parent"] += int(ra["has_reopened_parent"])
        totals["successor_relevant_response"] += rf["successor_relevant_response"]
        totals["successor_irrelevant_disturbance"] += rf["successor_irrelevant_disturbance"]
        totals["unrelated_survive_final"] += rf["unrelated_local_survive"]
        totals["old_g_derived_still_withdrawn"] += rf["old_g_derived_still_withdrawn"]
        totals["independent_post_g_parentless"] += int(rf["independent_post_g_parentless"])
        totals["strict_transition_allow"] += int(sr["transition_decision"] == "ALLOW")
        totals["strict_reopened_active"] += int(sr["reopened_active"])
        totals["strict_reopened_deferred"] += int(sr["reopened_deferred"])
        totals["strict_parent_includes_old_g"] += int(sr["parent_includes_old_G"])
        totals["strict_parent_includes_counterexample"] += int(sr["parent_includes_counterexample"])

        ok = (
            rr["nano"] == "ALLOW"
            and sr["transition_decision"] == "ALLOW"
            and not sr["reopened_active"]
            and sr["reopened_deferred"]
            and sr["parent_includes_old_G"]
            and sr["parent_includes_counterexample"]
            and rr["status_persistent"]
            and rr["status_survives_unrelated_checkpoint"]
            and rr["g_content_withdrawn"]
            and rr["g_derived_withdrawn"] == N_RELEVANT
            and rr["unrelated_local_survive"] == N_UNITS
            and rr["uncertainty_propagation"] == N_RELEVANT
            and rr["irrelevant_disturbance"] == 0
            and rr["no_successor_before_later_evidence"]
            and rr["warranted_by_counterexample"]
            and rr["not_warranted_by_invalidated_g"]
            and rl["naive_same_counterexample"] == "ALLOW"
            and rl["nano_same_counterexample"] == "DENY"
            and any(reason.startswith("effect:write_not_licensed") for reason in rl["nano_reasons"])
            and rb["naive"] == "ALLOW"
            and rb["nano_apply"] == "DEFER"
            and any(reason.startswith("precondition:unestablished") for reason in rb["nano_reasons"])
            and ra["nano"] == "ALLOW"
            and ra["has_later_evidence_parent"]
            and ra["has_reopened_parent"]
            and rf["successor_relevant_response"] == N_RELEVANT
            and rf["successor_irrelevant_disturbance"] == 0
            and rf["unrelated_local_survive"] == N_UNITS
            and rf["old_g_derived_still_withdrawn"] == N_RELEVANT
            and rf["independent_post_g_parentless"]
        )
        if not ok and len(failures) < 10:
            failures.append(r)

    relevant_opportunities = n * N_RELEVANT
    unit_opportunities = n * N_UNITS
    irrelevant_opportunities = n * (N_UNITS - N_RELEVANT)
    return {
        "experiment": "OPENCORE_BASE_002_GLOBAL_REOPENING",
        "status": "CONSTRUCTED_BASE_LEVEL_ASSAY",
        "n_worlds": n,
        "units_per_world": N_UNITS,
        "relevant_units_per_world": N_RELEVANT,
        "nano_sha256": file_sha(NANO_PATH),
        "nano_v0_unchanged": file_sha(NANO_PATH) == NANO_EXPECTED_SHA256,
        "base001_sha256": file_sha(BASE001_PATH),
        "base001_unchanged": file_sha(BASE001_PATH) == BASE001_EXPECTED_SHA256,
        "metrics": {
            "ReopenAllow": totals["reopen_allow"] / n,
            "ReopenedStatusPersistent": totals["reopen_status_persistent"] / n,
            "ReopenedStatusSurvivesCheckpoint": totals["reopen_survives_checkpoint"] / n,
            "GContentWithdrawn": totals["g_content_withdrawn"] / n,
            "GDerivedAuthorityWithdrawal": totals["g_derived_withdrawn"] / relevant_opportunities,
            "DistributedUncertainty": totals["uncertainty_propagation"] / relevant_opportunities,
            "IrrelevantReopenDisturbance": totals["irrelevant_reopen_disturbance"] / irrelevant_opportunities,
            "UnrelatedLocalRetentionAfterReopen": totals["unrelated_survive_reopen"] / unit_opportunities,
            "NoSuccessorBeforeLaterEvidence": totals["no_successor_before_later"] / n,
            "ReopenCounterexampleAncestry": totals["reopen_warranted_by_counterexample"] / n,
            "ReopenAvoidsInvalidatedGParent": totals["reopen_not_warranted_by_invalidated_g"] / n,
            "ReplacementLaunderingNaiveOverreach": totals["laundering_naive_allow"] / n,
            "ReplacementLaunderingNanoOverreach": totals["laundering_nano_allow"] / n,
            "ReplacementBeforeLaterEvidenceNaiveOverreach": totals["replace_before_later_naive_allow"] / n,
            "ReplacementBeforeLaterEvidenceNanoDefer": totals["replace_before_later_nano_defer"] / n,
            "ReplacementAfterLaterEvidenceAllow": totals["replace_after_later_nano_allow"] / n,
            "ReplacementLaterEvidenceAncestry": totals["replace_has_later_parent"] / n,
            "ReplacementReopenedStateAncestry": totals["replace_has_reopened_parent"] / n,
            "SuccessorRelevantResponse": totals["successor_relevant_response"] / relevant_opportunities,
            "SuccessorIrrelevantDisturbance": totals["successor_irrelevant_disturbance"] / irrelevant_opportunities,
            "UnrelatedLocalRetentionAfterReplacement": totals["unrelated_survive_final"] / unit_opportunities,
            "OldGDerivedRemainWithdrawn": totals["old_g_derived_still_withdrawn"] / relevant_opportunities,
            "IndependentPostGTemporalOnlyParentless": totals["independent_post_g_parentless"] / n,
            "StrictReopenTransitionAllow": totals["strict_transition_allow"] / n,
            "StrictReopenedStatusEffective": totals["strict_reopened_active"] / n,
            "StrictReopenedStatusSelfInvalidation": totals["strict_reopened_deferred"] / n,
            "StrictReopenOldGParentRate": totals["strict_parent_includes_old_g"] / n,
            "StrictReopenCounterexampleParentRate": totals["strict_parent_includes_counterexample"] / n,
        },
        "counts": totals,
        "first_world": first,
        "first_failures": failures,
        "claim_ceiling": (
            "constructed 12-unit Base-level global-reopening assay only; counterexample/later-evidence constitution, "
            "unit relevance, projection functions, licenses, and dependency semantics are externally supplied; "
            "no autonomous refutation, successor discovery, distributed learning, or general Base architecture claim; "
            "strict current-G reopening exposes Nano V0 precondition/warrant-parent collapse and is not repaired here"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", type=int, default=1000)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    if file_sha(NANO_PATH) != NANO_EXPECTED_SHA256:
        raise SystemExit(f"nano.py changed: {file_sha(NANO_PATH)}")
    if file_sha(BASE001_PATH) != BASE001_EXPECTED_SHA256:
        raise SystemExit(f"base_001_shared_world.py changed: {file_sha(BASE001_PATH)}")

    out = sweep(args.sweep, args.start_seed)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")

    m = out["metrics"]
    ok = (
        m["ReopenAllow"] == 1.0
        and m["ReopenedStatusPersistent"] == 1.0
        and m["GDerivedAuthorityWithdrawal"] == 1.0
        and m["DistributedUncertainty"] == 1.0
        and m["IrrelevantReopenDisturbance"] == 0.0
        and m["UnrelatedLocalRetentionAfterReopen"] == 1.0
        and m["ReplacementLaunderingNanoOverreach"] == 0.0
        and m["ReplacementBeforeLaterEvidenceNanoDefer"] == 1.0
        and m["ReplacementAfterLaterEvidenceAllow"] == 1.0
        and m["SuccessorRelevantResponse"] == 1.0
        and m["SuccessorIrrelevantDisturbance"] == 0.0
        and m["UnrelatedLocalRetentionAfterReplacement"] == 1.0
        and m["StrictReopenTransitionAllow"] == 1.0
        and m["StrictReopenedStatusEffective"] == 0.0
        and m["StrictReopenedStatusSelfInvalidation"] == 1.0
        and not out["first_failures"]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
