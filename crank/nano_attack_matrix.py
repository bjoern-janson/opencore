"""Isolated OpenCore Nano attack matrix.

Paired illegal/legal cases for role, dependency, applicability, revocation,
preservation, and composition. The identifiers are seed-opaque; Nano receives no
domain semantics beyond exact transition contracts.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from nano import (
    Decision,
    License,
    Nano,
    ObjectRecord,
    Precondition,
    Standing,
    StandingKey,
    Transition,
    WriteGrant,
)


def opaque(seed: int, label: str) -> str:
    return hashlib.sha256(f"nano-v0|{seed}|{label}".encode()).hexdigest()[:16]


def obj(seed: int, label: str) -> ObjectRecord:
    oid = opaque(seed, f"obj:{label}")
    return ObjectRecord(
        id=oid,
        payload_digest=hashlib.sha256(f"payload:{seed}:{label}".encode()).hexdigest(),
        type_tag=opaque(seed, f"type:{label}"),
    )


def k(o: ObjectRecord, seed: int, dimension: str, scope: str = "global") -> StandingKey:
    return StandingKey(o.id, opaque(seed, f"dim:{dimension}"), opaque(seed, f"scope:{scope}"))


def v(seed: int, value: str) -> str:
    return opaque(seed, f"value:{value}")


def lic(seed: int, label: str, **kwargs) -> License:
    return License(id=opaque(seed, f"lic:{label}"), **kwargs)


def role_case(seed: int) -> dict:
    signal = obj(seed, "role.signal")
    support = obj(seed, "role.support")
    role_key = k(signal, seed, "role")
    support_key = k(support, seed, "support")
    pred, obs, empirical = v(seed, "prediction"), v(seed, "observation"), v(seed, "empirical")
    L = lic(
        seed,
        "role.support",
        operation=opaque(seed, "op:grant-support"),
        preconditions=(Precondition(role_key, obs),),
        allowed_writes=(WriteGrant(support_key, (empirical,)),),
    )
    T = Transition(L.operation, writes=(Standing(support_key, empirical),))

    illegal = Nano(objects=(signal, support), standings=(Standing(role_key, pred),), licenses=(L,))
    legal = Nano(objects=(signal, support), standings=(Standing(role_key, obs),), licenses=(L,))
    return {
        "illegal": illegal.apply_transition(T, L.id).decision,
        "legal": legal.apply_transition(T, L.id).decision,
        "checks": {"illegal_reason": illegal.journal[-1].reasons},
    }


def dependency_case(seed: int) -> dict:
    report = obj(seed, "dep.report")
    counter = obj(seed, "dep.counter")
    attest_key = k(report, seed, "path-attestation")
    count_key = k(counter, seed, "independent-count")
    independent, one = v(seed, "independent"), v(seed, "one")
    L = lic(
        seed,
        "dep.increment",
        operation=opaque(seed, "op:increment-independent"),
        preconditions=(Precondition(attest_key, independent),),
        allowed_writes=(WriteGrant(count_key, (one,)),),
    )
    T = Transition(L.operation, writes=(Standing(count_key, one),))

    illegal = Nano(objects=(report, counter), standings=(), licenses=(L,))
    legal = Nano(objects=(report, counter), standings=(Standing(attest_key, independent),), licenses=(L,))
    return {
        "illegal": illegal.apply_transition(T, L.id).decision,
        "legal": legal.apply_transition(T, L.id).decision,
        "checks": {"illegal_reason": illegal.journal[-1].reasons},
    }


def applicability_case(seed: int) -> dict:
    ctx = obj(seed, "app.ctx")
    closure = obj(seed, "app.closure")
    use = obj(seed, "app.use")
    regime_key = k(ctx, seed, "regime")
    closure_key = k(closure, seed, "closure-authority")
    use_key = k(use, seed, "use")
    old, new = v(seed, "old-regime"), v(seed, "new-regime")
    authorized, closed_use = v(seed, "closure-authorized"), v(seed, "closed-use")
    L = lic(
        seed,
        "app.use-old",
        operation=opaque(seed, "op:use-closure"),
        preconditions=(
            Precondition(regime_key, old),
            Precondition(closure_key, authorized),
        ),
        allowed_writes=(WriteGrant(use_key, (closed_use,)),),
    )
    T = Transition(L.operation, writes=(Standing(use_key, closed_use),))
    illegal = Nano(
        objects=(ctx, closure, use),
        standings=(Standing(regime_key, new), Standing(closure_key, authorized)),
        licenses=(L,),
    )
    legal = Nano(
        objects=(ctx, closure, use),
        standings=(Standing(regime_key, old), Standing(closure_key, authorized)),
        licenses=(L,),
    )
    return {
        "illegal": illegal.apply_transition(T, L.id).decision,
        "legal": legal.apply_transition(T, L.id).decision,
        "checks": {"illegal_reason": illegal.journal[-1].reasons},
    }


def preservation_case(seed: int) -> dict:
    claim = obj(seed, "pres.claim")
    lineage_key = k(claim, seed, "lineage")
    status_key = k(claim, seed, "status")
    lineage_v1, active, revised = v(seed, "lineage-v1"), v(seed, "active"), v(seed, "revised")
    L = lic(
        seed,
        "pres.revise",
        operation=opaque(seed, "op:revise"),
        allowed_writes=(WriteGrant(status_key, (revised,)),),
        allowed_deletes=(lineage_key,),
        required_preservation=(lineage_key,),
    )
    illegal_T = Transition(
        L.operation,
        writes=(Standing(status_key, revised),),
        deletes=(lineage_key,),
    )
    legal_T = Transition(L.operation, writes=(Standing(status_key, revised),))
    initial = (Standing(lineage_key, lineage_v1), Standing(status_key, active))
    illegal = Nano(objects=(claim,), standings=initial, licenses=(L,))
    legal = Nano(objects=(claim,), standings=initial, licenses=(L,))
    return {
        "illegal": illegal.apply_transition(illegal_T, L.id).decision,
        "legal": legal.apply_transition(legal_T, L.id).decision,
        "checks": {
            "illegal_reason": illegal.journal[-1].reasons,
            "legal_lineage_preserved": Standing(lineage_key, lineage_v1) in legal.effective_state().active,
        },
    }


def composition_case(seed: int) -> dict:
    ctx = obj(seed, "comp.ctx")
    challenge = obj(seed, "comp.challenge")
    closure = obj(seed, "comp.closure")
    mode = obj(seed, "comp.mode")
    protocol_key = k(ctx, seed, "protocol")
    challenge_key = k(challenge, seed, "challenge-state")
    closure_key = k(closure, seed, "closure")
    mode_key = k(mode, seed, "mode")
    uniform, active = v(seed, "uniform"), v(seed, "active-selector")
    clean9, stopped = v(seed, "clean9"), v(seed, "stopped")
    idle, changed = v(seed, "idle"), v(seed, "changed")

    L_close = lic(
        seed,
        "comp.close",
        operation=opaque(seed, "op:close"),
        preconditions=(Precondition(protocol_key, uniform), Precondition(challenge_key, clean9)),
        allowed_writes=(WriteGrant(closure_key, (stopped,)),),
    )
    T_close = Transition(L_close.operation, writes=(Standing(closure_key, stopped),))

    L_change_protocol = lic(
        seed,
        "comp.change-protocol",
        operation=opaque(seed, "op:change-protocol"),
        allowed_writes=(WriteGrant(protocol_key, (active,)),),
    )
    T_change_protocol = Transition(
        L_change_protocol.operation,
        writes=(Standing(protocol_key, active),),
    )

    L_change_unrelated = lic(
        seed,
        "comp.change-unrelated",
        operation=opaque(seed, "op:change-unrelated"),
        allowed_writes=(WriteGrant(mode_key, (changed,)),),
    )
    T_change_unrelated = Transition(
        L_change_unrelated.operation,
        writes=(Standing(mode_key, changed),),
    )

    standings = (
        Standing(protocol_key, uniform),
        Standing(challenge_key, clean9),
        Standing(mode_key, idle),
    )
    licenses = (L_close, L_change_protocol, L_change_unrelated)

    illegal = Nano(objects=(ctx, challenge, closure, mode), standings=standings, licenses=licenses)
    preview_illegal = illegal.check_transition(T_close, L_close.id).decision
    first_illegal = illegal.apply_transition(T_change_protocol, L_change_protocol.id).decision
    final_illegal = illegal.apply_transition(T_close, L_close.id).decision

    legal = Nano(objects=(ctx, challenge, closure, mode), standings=standings, licenses=licenses)
    preview_legal = legal.check_transition(T_close, L_close.id).decision
    first_legal = legal.apply_transition(T_change_unrelated, L_change_unrelated.id).decision
    final_legal = legal.apply_transition(T_close, L_close.id).decision

    return {
        "illegal": final_illegal,
        "legal": final_legal,
        "checks": {
            "illegal_preview": preview_illegal.value,
            "illegal_t1": first_illegal.value,
            "legal_preview": preview_legal.value,
            "legal_t1": first_legal.value,
            "illegal_reason": illegal.journal[-1].reasons,
        },
    }


def revocation_case(seed: int) -> dict:
    root = obj(seed, "rev.root")
    parent = obj(seed, "rev.parent")
    child = obj(seed, "rev.child")
    use = obj(seed, "rev.use")
    review = obj(seed, "rev.review")
    root_key = k(root, seed, "root")
    parent_key = k(parent, seed, "standing")
    child_key = k(child, seed, "standing")
    use_key = k(use, seed, "use")
    review_key = k(review, seed, "review")
    yes, current, used, passed = v(seed, "yes"), v(seed, "current"), v(seed, "used"), v(seed, "passed")

    # L0 creates an upstream standing. L1 derives a child from it. Revoking L0
    # must make the L1 child ineffective even though L1 itself remains active.
    L0 = lic(
        seed,
        "rev.upstream",
        operation=opaque(seed, "op:authorize-parent"),
        preconditions=(Precondition(root_key, yes),),
        allowed_writes=(WriteGrant(parent_key, (current,)),),
    )
    L1 = lic(
        seed,
        "rev.derive-child",
        operation=opaque(seed, "op:derive-child"),
        preconditions=(Precondition(parent_key, current),),
        allowed_writes=(WriteGrant(child_key, (current,)),),
    )
    L_revoke = lic(
        seed,
        "rev.revoke",
        operation=opaque(seed, "op:revoke-upstream"),
        allowed_revocations=(L0.id,),
    )
    L_use = lic(
        seed,
        "rev.use",
        operation=opaque(seed, "op:use-child"),
        preconditions=(Precondition(child_key, current),),
        allowed_writes=(WriteGrant(use_key, (used,)),),
    )
    L_reauth = lic(
        seed,
        "rev.reauth",
        operation=opaque(seed, "op:reauthorize-child"),
        preconditions=(Precondition(review_key, passed),),
        allowed_writes=(WriteGrant(child_key, (current,)),),
    )
    licenses = (L0, L1, L_revoke, L_use, L_reauth)
    initial = (Standing(root_key, yes), Standing(review_key, passed))

    T_parent = Transition(L0.operation, writes=(Standing(parent_key, current),))
    T_child = Transition(L1.operation, writes=(Standing(child_key, current),))
    T_revoke = Transition(L_revoke.operation, revoke_licenses=(L0.id,))
    T_use = Transition(L_use.operation, writes=(Standing(use_key, used),))
    T_reauth = Transition(L_reauth.operation, writes=(Standing(child_key, current),))

    illegal = Nano(objects=(root, parent, child, use, review), standings=initial, licenses=licenses)
    assert illegal.apply_transition(T_parent, L0.id).decision is Decision.ALLOW
    parent_receipt = illegal.journal[-1].id
    assert illegal.apply_transition(T_child, L1.id).decision is Decision.ALLOW
    child_receipt = illegal.journal[-1]
    assert parent_receipt in child_receipt.parent_receipts
    assert illegal.apply_transition(T_revoke, L_revoke.id).decision is Decision.ALLOW
    after_revoke = illegal.effective_state()
    final_illegal = illegal.apply_transition(T_use, L_use.id).decision

    legal = Nano(objects=(root, parent, child, use, review), standings=initial, licenses=licenses)
    assert legal.apply_transition(T_parent, L0.id).decision is Decision.ALLOW
    assert legal.apply_transition(T_child, L1.id).decision is Decision.ALLOW
    assert legal.apply_transition(T_revoke, L_revoke.id).decision is Decision.ALLOW
    assert legal.apply_transition(T_reauth, L_reauth.id).decision is Decision.ALLOW
    final_legal = legal.apply_transition(T_use, L_use.id).decision

    return {
        "illegal": final_illegal,
        "legal": final_legal,
        "checks": {
            "illegal_reason": illegal.journal[-1].reasons,
            "child_deferred_after_upstream_revoke": any(s.key == child_key for s in after_revoke.deferred),
            "upstream_receipt_preserved": any(r.id == parent_receipt for r in illegal.lineage(parent.id)),
            "child_receipt_preserved": any(r.id == child_receipt.id for r in illegal.lineage(child.id)),
            "legal_child_active_after_reauth": any(s.key == child_key for s in legal.effective_state().active),
        },
    }


CASES = {
    "role": role_case,
    "dependency": dependency_case,
    "applicability": applicability_case,
    "revocation": revocation_case,
    "preservation": preservation_case,
    "composition": composition_case,
}


def run(seeds: int) -> dict:
    counts = {
        family: {"illegal": Counter(), "legal": Counter()}
        for family in CASES
    }
    reason_counts = {family: Counter() for family in CASES}
    invariant_failures: list[dict] = []

    for seed in range(seeds):
        for family, fn in CASES.items():
            result = fn(seed)
            counts[family]["illegal"][result["illegal"].value] += 1
            counts[family]["legal"][result["legal"].value] += 1
            for reason in result["checks"].get("illegal_reason", ()):
                reason_counts[family][reason.split(":", 1)[0]] += 1

            checks = result["checks"]
            if family == "composition":
                ok = (
                    checks["illegal_preview"] == "ALLOW"
                    and checks["illegal_t1"] == "ALLOW"
                    and checks["legal_preview"] == "ALLOW"
                    and checks["legal_t1"] == "ALLOW"
                )
                if not ok:
                    invariant_failures.append({"seed": seed, "family": family, "checks": checks})
            elif family == "revocation":
                ok = (
                    checks["child_deferred_after_upstream_revoke"]
                    and checks["upstream_receipt_preserved"]
                    and checks["child_receipt_preserved"]
                    and checks["legal_child_active_after_reauth"]
                )
                if not ok:
                    invariant_failures.append({"seed": seed, "family": family, "checks": checks})
            elif family == "preservation" and not checks["legal_lineage_preserved"]:
                invariant_failures.append({"seed": seed, "family": family, "checks": checks})

    illegal_total = seeds * len(CASES)
    legal_total = seeds * len(CASES)
    illegal_allows = sum(counts[f]["illegal"]["ALLOW"] for f in CASES)
    legal_refusals = sum(
        counts[f]["legal"]["DENY"] + counts[f]["legal"]["DEFER"] for f in CASES
    )

    summary = {
        "experiment": "OPENCORE_NANO_ISOLATED_ATTACK_MATRIX_V0",
        "seeds": seeds,
        "families": list(CASES),
        "nano": {
            "illegal_total": illegal_total,
            "legal_total": legal_total,
            "overreach_count": illegal_allows,
            "overreach_rate": illegal_allows / illegal_total,
            "false_refusal_count": legal_refusals,
            "false_refusal_rate": legal_refusals / legal_total,
            "family_counts": {
                family: {
                    side: dict(counts[family][side])
                    for side in ("illegal", "legal")
                }
                for family in CASES
            },
            "illegal_reason_classes": {family: dict(reason_counts[family]) for family in CASES},
            "invariant_failure_count": len(invariant_failures),
            "first_invariant_failures": invariant_failures[:10],
        },
        "naive_persistence": {
            "policy": "ALLOW_EVERY_PROPOSED_PERSISTENT_EFFECT",
            "overreach_count": illegal_total,
            "overreach_rate": 1.0,
            "false_refusal_count": 0,
            "false_refusal_rate": 0.0,
        },
        "claim_ceiling": (
            "Given externally constituted kernel-visible transition contracts on this "
            "constructed matrix, Nano may be assessed only for contract enforcement; "
            "contract correctness, truth, reliable generalization, and autonomous "
            "epistemology are out of scope."
        ),
    }
    return summary


def render_report(result: dict) -> str:
    lines = [
        "# OpenCore Nano — isolated attack matrix V0",
        "",
        "## Frozen question",
        "",
        "> Given externally constituted transition contracts, can a small semantically agnostic persistence kernel reject effects that exceed those contracts while admitting matched licensed transitions?",
        "",
        f"Seeds: **{result['seeds']}**  ",
        f"Paired decisions: **{result['nano']['illegal_total']} illegal + {result['nano']['legal_total']} legal**",
        "",
        "## Primary result",
        "",
        f"- Nano overreach: **{result['nano']['overreach_count']}/{result['nano']['illegal_total']} = {result['nano']['overreach_rate']:.6%}**",
        f"- Nano false refusal: **{result['nano']['false_refusal_count']}/{result['nano']['legal_total']} = {result['nano']['false_refusal_rate']:.6%}**",
        f"- Naive-persistence overreach: **{result['naive_persistence']['overreach_rate']:.6%}**",
        f"- Invariant failures: **{result['nano']['invariant_failure_count']}**",
        "",
        "## Family matrix",
        "",
        "| family | illegal ALLOW | illegal DENY | illegal DEFER | legal ALLOW | legal DENY/DEFER |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for family in result["families"]:
        fc = result["nano"]["family_counts"][family]
        illegal = fc["illegal"]
        legal = fc["legal"]
        lines.append(
            f"| {family} | {illegal.get('ALLOW',0)} | {illegal.get('DENY',0)} | "
            f"{illegal.get('DEFER',0)} | {legal.get('ALLOW',0)} | "
            f"{legal.get('DENY',0)+legal.get('DEFER',0)} |"
        )
    lines += [
        "",
        "## Composition centerpiece",
        "",
        "The illegal composition case first previews `T2` as `ALLOW`, then executes a separately licensed `T1` that changes a `T2` precondition. `T2` is checked again at execution and must no longer be authorized.",
        "",
        "```text",
        "valid L2 at t0",
        "-> preview(T2) = ALLOW",
        "-> apply(T1) = ALLOW",
        "-> Post(T1) no longer satisfies Pre(L2)",
        "-> apply(T2) = DENY",
        "```",
        "",
        "The matched legal case changes an orthogonal standing and then admits `T2`.",
        "",
        "## Revocation / history check",
        "",
        "A standing produced under a license becomes ineffective after that license is revoked, but the producing receipt remains in append-only lineage. A separately licensed reauthorization can make the same standing effective again without rewriting the old receipt.",
        "",
        "## Claim ceiling",
        "",
        result["claim_ceiling"],
        "",
        "No claim is made that Nano can determine whether the external contracts are epistemically correct.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=10_000)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = run(args.seeds)
    if args.json:
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.report:
        args.report.write_text(render_report(result))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
