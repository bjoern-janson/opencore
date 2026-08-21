#!/usr/bin/env python3
"""OpenCore Base 001: shared authority-filtered world with local projections.

Question
--------
Can one warranted shared-world change influence heterogeneous local units,
become ineffective through one upstream warrant revocation, and remove only its
authority-dependent consequences while preserving unrelated local learning?

The experiment deliberately uses Nano V0 unchanged.  Local units are tiny
harness-level projectors/proposers; they do not mutate shared state directly.

Constructed sequence per world:
  1. Admit one global standing G through an explicit license.
  2. All 12 units can read G through the effective shared world.
  3. Eight relevant units derive heterogeneous local H_i standings whose
     licenses require G.  Four irrelevant units make no G-derived persistent
     change.
  4. All 12 units acquire an unrelated local L_i standing *after* G with no G
     precondition (temporal ancestry control).
  5. One relevant unit uses H_i for a licensed local descendant D_i.
  6. The same unit tries to write J_global using that local-use license.  This
     is the authority-escalation attack; naive persistence accepts it, Nano must
     deny the out-of-envelope write.
  7. A matched explicit global-export license permits H_i -> J_global_licensed.
  8. Revoke only G's producing license.  No H_i/L_i/D_i/J cleanup transitions
     are issued.
  9. Inspect Nano effective state.  G-dependent H_i, D_i, and licensed J must
     become deferred by warrant ancestry; unrelated L_i must remain active.

Claim ceiling
-------------
Constructed 12-unit shared-world mechanics only.  The harness supplies unit
relevance, projection functions, licenses, and dependency semantics.  This is
not autonomous relevance discovery, distributed learning, or a general Base
architecture result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from nano import Decision, License, Nano, Precondition, Standing, StandingKey, Transition, WriteGrant

HERE = Path(__file__).resolve().parent
NANO_PATH = HERE / "nano.py"
NANO_EXPECTED_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"
N_UNITS = 12
N_RELEVANT = 8
PROJECTION_MODES = ("AMPLIFY", "INVERT", "GATE", "ROUTE")


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def opaque(seed: int, label: str) -> str:
    return hashlib.sha256(f"base-001:{seed}:{label}".encode()).hexdigest()[:16]


def key(seed: int, label: str, dimension: str, scope: str) -> StandingKey:
    return StandingKey(opaque(seed, label), dimension, scope)


@dataclass(frozen=True)
class Unit:
    index: int
    relevant: bool
    mode: str
    private_token: str

    def project(self, global_effective: bool) -> str:
        """Tiny heterogeneous local projection over the shared world."""
        if not self.relevant or not global_effective:
            return f"BASE:{self.private_token}"
        return f"G:{self.mode}:{self.private_token}"


class NaiveStore:
    """Control persistence: every proposed transition mutates raw current state."""

    def __init__(self, standings: Iterable[Standing] = ()) -> None:
        self.current = {s.key: s.value for s in standings}
        self.revoked_licenses: set[str] = set()

    def apply(self, transition: Transition) -> Decision:
        for k in transition.deletes:
            self.current.pop(k, None)
        for s in transition.writes:
            self.current[s.key] = s.value
        self.revoked_licenses.update(transition.revoke_licenses)
        return Decision.ALLOW

    def value(self, k: StandingKey) -> str | None:
        return self.current.get(k)


def make_units(seed: int) -> tuple[Unit, ...]:
    rng = random.Random(seed ^ 0xBA5E001)
    indices = list(range(N_UNITS))
    rng.shuffle(indices)
    relevant = set(indices[:N_RELEVANT])
    units: list[Unit] = []
    for i in range(N_UNITS):
        mode = PROJECTION_MODES[(i + seed) % len(PROJECTION_MODES)]
        units.append(Unit(i, i in relevant, mode, opaque(seed, f"private:{i}")))
    return tuple(units)


def active_map(nano: Nano) -> dict[StandingKey, str]:
    return {s.key: s.value for s in nano.effective_state().active}


def deferred_map(nano: Nano) -> dict[StandingKey, str]:
    return {s.key: s.value for s in nano.effective_state().deferred}


def receipt_writing(nano: Nano, target: StandingKey):
    for receipt in nano.journal:
        if receipt.decision is Decision.ALLOW and any(s.key == target for s in receipt.writes):
            return receipt
    raise AssertionError(f"no receipt writes {target}")


def trial(seed: int) -> dict:
    units = make_units(seed)
    relevant_units = tuple(u for u in units if u.relevant)
    irrelevant_units = tuple(u for u in units if not u.relevant)
    assert len(relevant_units) == N_RELEVANT
    assert len(irrelevant_units) == N_UNITS - N_RELEVANT

    g_key = key(seed, "G", "global-standing", "world")
    bad_j_key = key(seed, "J-bad", "global-standing", "world")
    good_j_key = key(seed, "J-good", "global-standing", "world")

    h_keys = {u.index: key(seed, f"H:{u.index}", "local-g-derived", f"unit:{u.index}") for u in units}
    l_keys = {u.index: key(seed, f"L:{u.index}", "local-independent", f"unit:{u.index}") for u in units}
    d_keys = {u.index: key(seed, f"D:{u.index}", "local-descendant", f"unit:{u.index}") for u in units}

    # Global warrant edge.
    l_g = License(
        opaque(seed, "license:G"),
        "admit-global-experience",
        allowed_writes=(WriteGrant(g_key, ("EFFECTIVE",)),),
    )
    l_revoke_g = License(
        opaque(seed, "license:revoke-G"),
        "revoke-global-warrant",
        allowed_revocations=(l_g.id,),
    )

    # Local G-derived edges and independent post-G learning edges.
    h_licenses: dict[int, License] = {}
    local_licenses: dict[int, License] = {}
    use_licenses: dict[int, License] = {}
    for u in units:
        projected = u.project(True)
        if u.relevant:
            h_licenses[u.index] = License(
                opaque(seed, f"license:H:{u.index}"),
                f"derive-from-global:{u.index}",
                preconditions=(Precondition(g_key, "EFFECTIVE"),),
                allowed_writes=(WriteGrant(h_keys[u.index], (projected,)),),
            )
            use_licenses[u.index] = License(
                opaque(seed, f"license:use-H:{u.index}"),
                f"local-use:{u.index}",
                preconditions=(Precondition(h_keys[u.index], projected),),
                allowed_writes=(WriteGrant(d_keys[u.index], (f"USED:{u.private_token}",)),),
            )
        local_licenses[u.index] = License(
            opaque(seed, f"license:L:{u.index}"),
            f"independent-local-learn:{u.index}",
            allowed_writes=(WriteGrant(l_keys[u.index], (f"LOCAL:{u.private_token}",)),),
        )

    # Choose one relevant unit for the local->global escalation assay.
    exporter = relevant_units[seed % len(relevant_units)]
    exporter_h = h_keys[exporter.index]
    exporter_h_value = exporter.project(True)
    l_export = License(
        opaque(seed, "license:global-export"),
        "licensed-global-export",
        preconditions=(Precondition(exporter_h, exporter_h_value),),
        allowed_writes=(WriteGrant(good_j_key, ("GLOBALIZED",)),),
    )

    all_licenses = (l_g, l_revoke_g, l_export, *h_licenses.values(), *local_licenses.values(), *use_licenses.values())
    nano = Nano(licenses=all_licenses)
    naive = NaiveStore()

    # Pre-experience projections.
    pre_projection = {u.index: u.project(False) for u in units}

    admit_g = Transition("admit-global-experience", writes=(Standing(g_key, "EFFECTIVE"),))
    assert nano.apply_transition(admit_g, l_g.id).decision is Decision.ALLOW
    naive.apply(admit_g)

    active_after_g = active_map(nano)
    reach = {u.index: active_after_g.get(g_key) == "EFFECTIVE" for u in units}
    post_projection = {u.index: u.project(reach[u.index]) for u in units}

    # Relevant local units materialize their G-derived consequences. Irrelevant
    # units still see G but their projection is unchanged and they make no
    # G-derived persistence proposal.
    for u in relevant_units:
        t = Transition(
            f"derive-from-global:{u.index}",
            writes=(Standing(h_keys[u.index], post_projection[u.index]),),
        )
        assert nano.apply_transition(t, h_licenses[u.index].id).decision is Decision.ALLOW
        naive.apply(t)

    active_after_h = active_map(nano)

    # Every unit learns an unrelated local state AFTER G.  These transitions
    # have no G/H precondition and therefore must not acquire G warrant ancestry.
    for u in units:
        t = Transition(
            f"independent-local-learn:{u.index}",
            writes=(Standing(l_keys[u.index], f"LOCAL:{u.private_token}"),),
        )
        assert nano.apply_transition(t, local_licenses[u.index].id).decision is Decision.ALLOW
        naive.apply(t)

    # Legitimate local descendant from H_i.
    local_use = Transition(
        f"local-use:{exporter.index}",
        writes=(Standing(d_keys[exporter.index], f"USED:{exporter.private_token}"),),
    )
    assert nano.apply_transition(local_use, use_licenses[exporter.index].id).decision is Decision.ALLOW
    naive.apply(local_use)

    # Attack: use the *local-use* license to create a global standing.  Same H_i
    # is available, but there is no licensed local->global effect edge.
    illegal_export = Transition(
        f"local-use:{exporter.index}",
        writes=(Standing(bad_j_key, "GLOBALIZED"),),
    )
    naive_illegal_export = naive.apply(illegal_export)
    nano_illegal_receipt = nano.apply_transition(illegal_export, use_licenses[exporter.index].id)

    # Matched legal: a separately constituted global-export edge exists.
    legal_export = Transition(
        "licensed-global-export",
        writes=(Standing(good_j_key, "GLOBALIZED"),),
    )
    naive_legal_export = naive.apply(legal_export)
    nano_legal_receipt = nano.apply_transition(legal_export, l_export.id)

    # Capture ancestry before revocation using only Nano's public receipt journal.
    g_receipt = receipt_writing(nano, g_key)
    h_receipt = receipt_writing(nano, exporter_h)
    j_receipt = receipt_writing(nano, good_j_key)
    ancestry_chain_ok = (
        g_receipt.id in h_receipt.parent_receipts
        and h_receipt.id in j_receipt.parent_receipts
    )

    # Single upstream action. No local rewrite/delete sweep is performed.
    revoke = Transition("revoke-global-warrant", revoke_licenses=(l_g.id,))
    naive_revoke = naive.apply(revoke)
    nano_revoke = nano.apply_transition(revoke, l_revoke_g.id)
    assert nano_revoke.decision is Decision.ALLOW
    assert not revoke.writes and not revoke.deletes

    active_after_revoke = active_map(nano)
    deferred_after_revoke = deferred_map(nano)
    post_revoke_projection = {u.index: u.project(g_key in active_after_revoke) for u in units}

    relevant_response = sum(
        active_after_h.get(h_keys[u.index]) == post_projection[u.index]
        and post_projection[u.index] != pre_projection[u.index]
        for u in relevant_units
    )
    irrelevant_disturbance = sum(
        post_projection[u.index] != pre_projection[u.index]
        or h_keys[u.index] in active_after_h
        for u in irrelevant_units
    )
    revocation_recovery = sum(
        h_keys[u.index] not in active_after_revoke
        and h_keys[u.index] in deferred_after_revoke
        and post_revoke_projection[u.index] == pre_projection[u.index]
        for u in relevant_units
    )
    collateral_loss = sum(l_keys[u.index] not in active_after_revoke for u in units)

    # Naive persistence records revocation metadata but does not reinterpret raw
    # current state through warrant ancestry.
    naive_recovery = sum(naive.value(h_keys[u.index]) is None for u in relevant_units)

    independent_parent_counts = {
        u.index: len(receipt_writing(nano, l_keys[u.index]).parent_receipts)
        for u in units
    }

    history_preserved = all(h_keys[u.index] in deferred_after_revoke for u in relevant_units)
    transitive_global_revocation = good_j_key not in active_after_revoke and good_j_key in deferred_after_revoke
    local_descendant_revocation = d_keys[exporter.index] not in active_after_revoke and d_keys[exporter.index] in deferred_after_revoke

    return {
        "seed": seed,
        "units": N_UNITS,
        "relevant_units": N_RELEVANT,
        "projection_modes_relevant": sorted({u.mode for u in relevant_units}),
        "projection_diversity": len({post_projection[u.index] for u in relevant_units}),
        "reach_count": sum(reach.values()),
        "relevant_response_count": relevant_response,
        "irrelevant_disturbance_count": irrelevant_disturbance,
        "revocation_recovery_count": revocation_recovery,
        "naive_revocation_recovery_count": naive_recovery,
        "collateral_loss_count": collateral_loss,
        "independent_local_parent_counts": independent_parent_counts,
        "history_preserved_without_cleanup": history_preserved,
        "revocation_transition_local_writes": len(revoke.writes),
        "revocation_transition_local_deletes": len(revoke.deletes),
        "illegal_global_export": {
            "naive": naive_illegal_export.value,
            "nano": nano_illegal_receipt.decision.value,
            "nano_reasons": nano_illegal_receipt.reasons,
        },
        "legal_global_export": {
            "naive": naive_legal_export.value,
            "nano": nano_legal_receipt.decision.value,
        },
        "legal_export_ancestry_G_to_H_to_J": ancestry_chain_ok,
        "legal_global_export_revoked_transitively": transitive_global_revocation,
        "local_H_descendant_revoked_transitively": local_descendant_revocation,
        "naive_revoke": naive_revoke.value,
        "nano_revoke": nano_revoke.decision.value,
        "active_after_revoke": len(active_after_revoke),
        "deferred_after_revoke": len(deferred_after_revoke),
    }


def sweep(n: int, start_seed: int = 0) -> dict:
    totals = {
        "unit_opportunities": 0,
        "relevant_opportunities": 0,
        "irrelevant_opportunities": 0,
        "reach": 0,
        "relevant_response": 0,
        "irrelevant_disturbance": 0,
        "revocation_recovery": 0,
        "naive_revocation_recovery": 0,
        "collateral_loss": 0,
        "illegal_export_naive_allow": 0,
        "illegal_export_nano_allow": 0,
        "illegal_export_nano_deny": 0,
        "legal_export_nano_allow": 0,
        "legal_export_ancestry_ok": 0,
        "legal_export_transitive_revocation": 0,
        "local_descendant_transitive_revocation": 0,
        "history_preserved_without_cleanup": 0,
        "all_independent_local_parentless": 0,
        "zero_local_cleanup": 0,
        "projection_diversity_sum": 0,
    }
    first: dict | None = None
    failures: list[dict] = []

    for seed in range(start_seed, start_seed + n):
        r = trial(seed)
        if first is None:
            first = r
        totals["unit_opportunities"] += N_UNITS
        totals["relevant_opportunities"] += N_RELEVANT
        totals["irrelevant_opportunities"] += N_UNITS - N_RELEVANT
        totals["reach"] += r["reach_count"]
        totals["relevant_response"] += r["relevant_response_count"]
        totals["irrelevant_disturbance"] += r["irrelevant_disturbance_count"]
        totals["revocation_recovery"] += r["revocation_recovery_count"]
        totals["naive_revocation_recovery"] += r["naive_revocation_recovery_count"]
        totals["collateral_loss"] += r["collateral_loss_count"]
        totals["illegal_export_naive_allow"] += int(r["illegal_global_export"]["naive"] == "ALLOW")
        totals["illegal_export_nano_allow"] += int(r["illegal_global_export"]["nano"] == "ALLOW")
        totals["illegal_export_nano_deny"] += int(r["illegal_global_export"]["nano"] == "DENY")
        totals["legal_export_nano_allow"] += int(r["legal_global_export"]["nano"] == "ALLOW")
        totals["legal_export_ancestry_ok"] += int(r["legal_export_ancestry_G_to_H_to_J"])
        totals["legal_export_transitive_revocation"] += int(r["legal_global_export_revoked_transitively"])
        totals["local_descendant_transitive_revocation"] += int(r["local_H_descendant_revoked_transitively"])
        totals["history_preserved_without_cleanup"] += int(r["history_preserved_without_cleanup"])
        totals["all_independent_local_parentless"] += int(all(v == 0 for v in r["independent_local_parent_counts"].values()))
        totals["zero_local_cleanup"] += int(
            r["revocation_transition_local_writes"] == 0 and r["revocation_transition_local_deletes"] == 0
        )
        totals["projection_diversity_sum"] += r["projection_diversity"]

        ok = (
            r["reach_count"] == N_UNITS
            and r["relevant_response_count"] == N_RELEVANT
            and r["irrelevant_disturbance_count"] == 0
            and r["revocation_recovery_count"] == N_RELEVANT
            and r["collateral_loss_count"] == 0
            and r["illegal_global_export"]["naive"] == "ALLOW"
            and r["illegal_global_export"]["nano"] == "DENY"
            and r["legal_global_export"]["nano"] == "ALLOW"
            and r["legal_export_ancestry_G_to_H_to_J"]
            and r["legal_global_export_revoked_transitively"]
            and r["local_H_descendant_revoked_transitively"]
            and r["history_preserved_without_cleanup"]
            and all(v == 0 for v in r["independent_local_parent_counts"].values())
            and r["revocation_transition_local_writes"] == 0
            and r["revocation_transition_local_deletes"] == 0
        )
        if not ok and len(failures) < 10:
            failures.append(r)

    return {
        "experiment": "OPENCORE_BASE_001_SHARED_AUTHORITY_FILTERED_WORLD",
        "status": "CONSTRUCTED_BASE_LEVEL_ASSAY",
        "n_worlds": n,
        "units_per_world": N_UNITS,
        "relevant_units_per_world": N_RELEVANT,
        "nano_sha256": file_sha(NANO_PATH),
        "nano_v0_unchanged": file_sha(NANO_PATH) == NANO_EXPECTED_SHA256,
        "metrics": {
            "Reach": totals["reach"] / totals["unit_opportunities"],
            "RelevantResponse": totals["relevant_response"] / totals["relevant_opportunities"],
            "IrrelevantDisturbance": totals["irrelevant_disturbance"] / totals["irrelevant_opportunities"],
            "RevocationRecovery": totals["revocation_recovery"] / totals["relevant_opportunities"],
            "NaiveRevocationRecovery": totals["naive_revocation_recovery"] / totals["relevant_opportunities"],
            "CollateralLoss": totals["collateral_loss"] / totals["unit_opportunities"],
            "IllegalGlobalExportNanoOverreach": totals["illegal_export_nano_allow"] / n,
            "IllegalGlobalExportNaiveOverreach": totals["illegal_export_naive_allow"] / n,
            "LegalGlobalExportRetention": totals["legal_export_nano_allow"] / n,
            "LicensedReexportAncestryIntegrity": totals["legal_export_ancestry_ok"] / n,
            "LicensedReexportRevocationRecovery": totals["legal_export_transitive_revocation"] / n,
            "LocalDescendantRevocationRecovery": totals["local_descendant_transitive_revocation"] / n,
            "HistoryPreservedWithoutLocalCleanup": totals["history_preserved_without_cleanup"] / n,
            "IndependentPostGLocalLearningParentless": totals["all_independent_local_parentless"] / n,
            "ZeroLocalCleanupTransitionsOnRevoke": totals["zero_local_cleanup"] / n,
            "MeanRelevantProjectionDiversity": totals["projection_diversity_sum"] / n,
        },
        "counts": totals,
        "first_world": first,
        "first_failures": failures,
        "claim_ceiling": (
            "constructed 12-unit Base-level assay only; unit relevance, local projection functions, licenses, "
            "and dependency semantics are externally supplied; no autonomous relevance discovery, distributed learning, "
            "general Base architecture, or universal warrant propagation claim"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", type=int, default=1000)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    digest = file_sha(NANO_PATH)
    if digest != NANO_EXPECTED_SHA256:
        raise SystemExit(f"nano.py changed: {digest}")

    out = sweep(args.sweep, args.start_seed)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")

    m = out["metrics"]
    ok = (
        m["Reach"] == 1.0
        and m["RelevantResponse"] == 1.0
        and m["IrrelevantDisturbance"] == 0.0
        and m["RevocationRecovery"] == 1.0
        and m["CollateralLoss"] == 0.0
        and m["IllegalGlobalExportNanoOverreach"] == 0.0
        and m["LegalGlobalExportRetention"] == 1.0
        and m["LicensedReexportRevocationRecovery"] == 1.0
        and not out["first_failures"]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
