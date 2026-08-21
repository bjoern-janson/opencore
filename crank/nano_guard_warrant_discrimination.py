"""GW-001: discriminate candidate repairs for Base-002B's guard/warrant wound.

This harness does NOT modify Nano V0. It instantiates Nano V0 and three small
harness-only parent-selection variants to ask what the Base-002B failure actually
requires.

Question:
    Is the missing mechanism merely a special case around same-key replacement
    or same-transition revocation, or does the tested family require independent
    control over execution preconditions and continuing warrant parents?

Candidate parent policies:
    NANO_V0             every precondition source becomes a warrant parent
    SAME_KEY_EXEMPT     preconditions on keys written by T are not parents
    REVOKED_SRC_EXEMPT  precondition sources revoked by T are not parents
    SELF_INVALIDATING_EXEMPT
                        exclude only when the checked source is both overwritten
                        by T and its producing license is revoked by T
    EXPLICIT_SELECTIVE  all preconditions are checked, but harness-declared guard
                        keys are excluded from continuing warrant ancestry
    DROP_ALL_PARENTS    permissive control: check preconditions, retain no parents

The EXPLICIT_SELECTIVE arm is an experimental comparator, not a Nano repair.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable

from nano import (
    Decision,
    License,
    Nano,
    Precondition,
    Standing,
    StandingKey,
    Transition,
    WriteGrant,
)


POLICIES = (
    "NANO_V0",
    "SAME_KEY_EXEMPT",
    "REVOKED_SRC_EXEMPT",
    "SELF_INVALIDATING_EXEMPT",
    "EXPLICIT_SELECTIVE",
    "DROP_ALL_PARENTS",
)


def opaque(seed: int, label: str) -> str:
    return hashlib.sha256(f"GW001|{seed}|{label}".encode()).hexdigest()[:24]


def key(seed: int, label: str, dimension: str = "status", scope: str = "world") -> StandingKey:
    return StandingKey(opaque(seed, label), dimension, scope)


def active_map(nano: Nano) -> dict[StandingKey, str]:
    return {s.key: s.value for s in nano.effective_state().active}


def deferred_map(nano: Nano) -> dict[StandingKey, str]:
    return {s.key: s.value for s in nano.effective_state().deferred}


class PolicyNano(Nano):
    """Harness-only Nano variant changing only warrant-parent selection.

    check_transition() is inherited unchanged from frozen Nano V0, so every
    license precondition remains an execution-time condition in every arm.
    """

    def __init__(
        self,
        *,
        policy: str,
        guard_keys_by_license: dict[str, frozenset[StandingKey]] | None = None,
        licenses: Iterable[License] = (),
    ) -> None:
        if policy not in POLICIES:
            raise ValueError(policy)
        self.parent_policy = policy
        self.guard_keys_by_license = guard_keys_by_license or {}
        super().__init__(licenses=licenses)

    def _parents_for(self, transition: Transition, license_: License | None) -> tuple[str, ...]:
        if license_ is None:
            return ()

        write_keys = {s.key for s in transition.writes}
        guard_keys = self.guard_keys_by_license.get(license_.id, frozenset())
        parent_ids: set[str] = set()

        for pre in license_.preconditions:
            current = self._current.get(pre.key)
            if current is None or current.receipt_id is None:
                continue

            include = True
            if self.parent_policy == "NANO_V0":
                include = True
            elif self.parent_policy == "SAME_KEY_EXEMPT":
                include = pre.key not in write_keys
            elif self.parent_policy == "REVOKED_SRC_EXEMPT":
                include = current.license_id not in set(transition.revoke_licenses)
            elif self.parent_policy == "SELF_INVALIDATING_EXEMPT":
                include = not (
                    pre.key in write_keys
                    and current.license_id in set(transition.revoke_licenses)
                )
            elif self.parent_policy == "EXPLICIT_SELECTIVE":
                include = pre.key not in guard_keys
            elif self.parent_policy == "DROP_ALL_PARENTS":
                include = False

            if include:
                parent_ids.add(current.receipt_id)

        return tuple(sorted(parent_ids))


def add_revoker(licenses: list[License], seed: int, label: str, target_license_id: str) -> License:
    revoker = License(
        opaque(seed, f"license:{label}:revoker"),
        f"{label}:revoke",
        allowed_revocations=(target_license_id,),
    )
    licenses.append(revoker)
    return revoker


def strict_reopen_case(seed: int, policy: str) -> dict:
    """Base-002B geometry: old G is guard; counterexample is continuing warrant."""
    g = key(seed, "reopen:G")
    e = key(seed, "reopen:E")

    l_g = License(
        opaque(seed, "reopen:license:G"),
        "reopen:admit-G",
        allowed_writes=(WriteGrant(g, ("EFFECTIVE",)),),
    )
    l_e = License(
        opaque(seed, "reopen:license:E"),
        "reopen:admit-E",
        allowed_writes=(WriteGrant(e, ("REFUTES_G",)),),
    )
    l_reopen = License(
        opaque(seed, "reopen:license:reopen"),
        "reopen:apply",
        preconditions=(Precondition(g, "EFFECTIVE"), Precondition(e, "REFUTES_G")),
        allowed_writes=(WriteGrant(g, ("REOPENED",)),),
        allowed_revocations=(l_g.id,),
    )
    guards = {l_reopen.id: frozenset((g,))}
    nano = PolicyNano(policy=policy, guard_keys_by_license=guards, licenses=(l_g, l_e, l_reopen))

    g_r = nano.apply_transition(Transition("reopen:admit-G", writes=(Standing(g, "EFFECTIVE"),)), l_g.id)
    e_r = nano.apply_transition(Transition("reopen:admit-E", writes=(Standing(e, "REFUTES_G"),)), l_e.id)
    r = nano.apply_transition(
        Transition("reopen:apply", writes=(Standing(g, "REOPENED"),), revoke_licenses=(l_g.id,)),
        l_reopen.id,
    )

    active = active_map(nano)
    deferred = deferred_map(nano)
    parents = set(r.parent_receipts)
    return {
        "transition_allow": r.decision is Decision.ALLOW,
        "reopened_active": active.get(g) == "REOPENED",
        "reopened_deferred": deferred.get(g) == "REOPENED",
        "parent_old_g": g_r.id in parents,
        "parent_counterexample": e_r.id in parents,
        "expected_pass": (
            r.decision is Decision.ALLOW
            and active.get(g) == "REOPENED"
            and g_r.id not in parents
            and e_r.id in parents
        ),
    }


def same_key_warrant_case(seed: int, policy: str) -> dict:
    """Same-key rewrite where the old standing is a genuine continuing warrant.

    PROVISIONAL -> CERTIFIED is allowed only because PROVISIONAL is effective,
    and the constructed contract says CERTIFIED must lose authority if the
    PROVISIONAL warrant is later revoked.
    """
    stage = key(seed, "samekey:stage")
    l_old = License(
        opaque(seed, "samekey:license:old"),
        "samekey:admit",
        allowed_writes=(WriteGrant(stage, ("PROVISIONAL",)),),
    )
    l_upgrade = License(
        opaque(seed, "samekey:license:upgrade"),
        "samekey:upgrade",
        preconditions=(Precondition(stage, "PROVISIONAL"),),
        allowed_writes=(WriteGrant(stage, ("CERTIFIED",)),),
    )
    licenses = [l_old, l_upgrade]
    revoker = add_revoker(licenses, seed, "samekey", l_old.id)
    nano = PolicyNano(policy=policy, licenses=licenses)

    old_r = nano.apply_transition(Transition("samekey:admit", writes=(Standing(stage, "PROVISIONAL"),)), l_old.id)
    upgrade_r = nano.apply_transition(Transition("samekey:upgrade", writes=(Standing(stage, "CERTIFIED"),)), l_upgrade.id)
    before_revoke_active = active_map(nano).get(stage) == "CERTIFIED"
    nano.apply_transition(Transition("samekey:revoke", revoke_licenses=(l_old.id,)), revoker.id)
    after = nano.effective_state()
    active = {s.key: s.value for s in after.active}
    deferred = {s.key: s.value for s in after.deferred}
    parents = set(upgrade_r.parent_receipts)

    return {
        "upgrade_allow": upgrade_r.decision is Decision.ALLOW,
        "before_revoke_active": before_revoke_active,
        "parent_old_stage": old_r.id in parents,
        "after_old_warrant_revoke_deferred": deferred.get(stage) == "CERTIFIED",
        "after_old_warrant_revoke_active": active.get(stage) == "CERTIFIED",
        "expected_pass": (
            upgrade_r.decision is Decision.ALLOW
            and before_revoke_active
            and old_r.id in parents
            and deferred.get(stage) == "CERTIFIED"
        ),
    }


def revoked_source_warrant_case(seed: int, policy: str) -> dict:
    """A different-key source is a genuine warrant even though T retires it.

    The result is deliberately allowed to be written, but its current authority
    must be absent immediately after the transition because the source warrant
    is retired in the same transition.
    """
    src = key(seed, "revokedw:source")
    out = key(seed, "revokedw:result")
    l_src = License(
        opaque(seed, "revokedw:license:source"),
        "revokedw:admit-source",
        allowed_writes=(WriteGrant(src, ("VALID",)),),
    )
    l_derive = License(
        opaque(seed, "revokedw:license:derive"),
        "revokedw:derive-and-retire",
        preconditions=(Precondition(src, "VALID"),),
        allowed_writes=(WriteGrant(out, ("DERIVED",)),),
        allowed_revocations=(l_src.id,),
    )
    nano = PolicyNano(policy=policy, licenses=(l_src, l_derive))

    src_r = nano.apply_transition(Transition("revokedw:admit-source", writes=(Standing(src, "VALID"),)), l_src.id)
    out_r = nano.apply_transition(
        Transition(
            "revokedw:derive-and-retire",
            writes=(Standing(out, "DERIVED"),),
            revoke_licenses=(l_src.id,),
        ),
        l_derive.id,
    )
    active = active_map(nano)
    deferred = deferred_map(nano)
    parents = set(out_r.parent_receipts)

    return {
        "transition_allow": out_r.decision is Decision.ALLOW,
        "parent_source": src_r.id in parents,
        "result_deferred": deferred.get(out) == "DERIVED",
        "result_active": active.get(out) == "DERIVED",
        "expected_pass": (
            out_r.decision is Decision.ALLOW
            and src_r.id in parents
            and deferred.get(out) == "DERIVED"
        ),
    }


def mixed_guard_warrant_case(seed: int, policy: str) -> dict:
    """Different-key guard and warrant coexist in one transition.

    MODE=OPEN is execution-only. E=SUPPORTS_RESULT is a continuing warrant.
    After MODE authority is revoked, RESULT should remain active. After E is
    revoked, RESULT should become deferred.

    This forces selective ancestry within a single precondition list.
    """
    mode = key(seed, "mixed:mode")
    evidence = key(seed, "mixed:evidence")
    out = key(seed, "mixed:result")

    l_mode = License(
        opaque(seed, "mixed:license:mode"),
        "mixed:admit-mode",
        allowed_writes=(WriteGrant(mode, ("OPEN",)),),
    )
    l_e = License(
        opaque(seed, "mixed:license:evidence"),
        "mixed:admit-evidence",
        allowed_writes=(WriteGrant(evidence, ("SUPPORTS_RESULT",)),),
    )
    l_result = License(
        opaque(seed, "mixed:license:result"),
        "mixed:write-result",
        preconditions=(
            Precondition(mode, "OPEN"),
            Precondition(evidence, "SUPPORTS_RESULT"),
        ),
        allowed_writes=(WriteGrant(out, ("ACTIVE",)),),
    )
    licenses = [l_mode, l_e, l_result]
    mode_revoker = add_revoker(licenses, seed, "mixed:mode", l_mode.id)
    evidence_revoker = add_revoker(licenses, seed, "mixed:evidence", l_e.id)
    guards = {l_result.id: frozenset((mode,))}
    nano = PolicyNano(policy=policy, guard_keys_by_license=guards, licenses=licenses)

    mode_r = nano.apply_transition(Transition("mixed:admit-mode", writes=(Standing(mode, "OPEN"),)), l_mode.id)
    e_r = nano.apply_transition(
        Transition("mixed:admit-evidence", writes=(Standing(evidence, "SUPPORTS_RESULT"),)),
        l_e.id,
    )
    out_r = nano.apply_transition(Transition("mixed:write-result", writes=(Standing(out, "ACTIVE"),)), l_result.id)
    initial_active = active_map(nano).get(out) == "ACTIVE"
    parents = set(out_r.parent_receipts)

    nano.apply_transition(Transition("mixed:mode:revoke", revoke_licenses=(l_mode.id,)), mode_revoker.id)
    after_mode_active = active_map(nano).get(out) == "ACTIVE"
    after_mode_deferred = deferred_map(nano).get(out) == "ACTIVE"

    nano.apply_transition(Transition("mixed:evidence:revoke", revoke_licenses=(l_e.id,)), evidence_revoker.id)
    after_e_active = active_map(nano).get(out) == "ACTIVE"
    after_e_deferred = deferred_map(nano).get(out) == "ACTIVE"

    return {
        "transition_allow": out_r.decision is Decision.ALLOW,
        "initial_active": initial_active,
        "parent_mode": mode_r.id in parents,
        "parent_evidence": e_r.id in parents,
        "after_mode_revoke_active": after_mode_active,
        "after_mode_revoke_deferred": after_mode_deferred,
        "after_evidence_revoke_active": after_e_active,
        "after_evidence_revoke_deferred": after_e_deferred,
        "expected_pass": (
            out_r.decision is Decision.ALLOW
            and initial_active
            and mode_r.id not in parents
            and e_r.id in parents
            and after_mode_active
            and after_e_deferred
        ),
    }


def trial(seed: int) -> dict:
    return {
        policy: {
            "strict_reopen": strict_reopen_case(seed, policy),
            "same_key_warrant": same_key_warrant_case(seed, policy),
            "revoked_source_warrant": revoked_source_warrant_case(seed, policy),
            "mixed_guard_warrant": mixed_guard_warrant_case(seed, policy),
        }
        for policy in POLICIES
    }


def sweep(n: int, start_seed: int = 0) -> dict:
    counts = {
        p: {
            "strict_reopen_pass": 0,
            "same_key_warrant_pass": 0,
            "revoked_source_warrant_pass": 0,
            "mixed_guard_warrant_pass": 0,
            "all_four_pass": 0,
        }
        for p in POLICIES
    }
    first_failure = {p: None for p in POLICIES}

    for seed in range(start_seed, start_seed + n):
        result = trial(seed)
        for policy in POLICIES:
            cases = result[policy]
            verdicts = {
                "strict_reopen_pass": cases["strict_reopen"]["expected_pass"],
                "same_key_warrant_pass": cases["same_key_warrant"]["expected_pass"],
                "revoked_source_warrant_pass": cases["revoked_source_warrant"]["expected_pass"],
                "mixed_guard_warrant_pass": cases["mixed_guard_warrant"]["expected_pass"],
            }
            for metric, ok in verdicts.items():
                counts[policy][metric] += int(ok)
            all_ok = all(verdicts.values())
            counts[policy]["all_four_pass"] += int(all_ok)
            if not all_ok and first_failure[policy] is None:
                first_failure[policy] = {"seed": seed, "cases": cases}

    return {
        "experiment": "OPENCORE_GW_001_GUARD_WARRANT_DISCRIMINATION",
        "worlds": n,
        "start_seed": start_seed,
        "policies": list(POLICIES),
        "counts": counts,
        "rates": {
            p: {k: v / n for k, v in metrics.items()}
            for p, metrics in counts.items()
        },
        "first_failure": first_failure,
        "claim_ceiling": (
            "On the constructed four-family assay, only the harness-selective parent policy "
            "matched all externally declared execution-vs-continuing-authority relationships. "
            "This identifies a functional need for selective authority ancestry beyond the tested "
            "same-key and same-transition-revocation heuristics; it does not establish a Nano schema."
        ),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--worlds", type=int, default=100)
    parser.add_argument("--start-seed", type=int, default=0)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    result = sweep(args.worlds, args.start_seed)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
