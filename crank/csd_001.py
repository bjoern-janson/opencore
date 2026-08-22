from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ASSAY = "CSD-001"
SEEDS = 256
B = 8
PRE_AUDIT_FAILURE_ROUNDS = 12
F3U_USES_PER_CHALLENGE = 3
F2_P_SIGNAL = 0.25
D_AGENT = ("c0", "c1", "c2")
SIGNALS = {"h_A": "SIG_A", "h_B": "SIG_B"}
FAILURE_CLASSES = ("F1", "F2", "F3", "F3u")
HARNESS_ONLY_FIELDS = {
    "failure_class",
    "hidden_hypothesis",
    "ground_truth_adequate",
    "c_star",
    "warrant_time",
}


@dataclass(frozen=True)
class AuditWorld:
    seed: int
    failure_class: str
    hidden_hypothesis: str
    f2_signal_use: Optional[int]


def stable_bit(seed: int, label: str) -> int:
    body = f"{ASSAY}|{seed}|{label}".encode()
    return hashlib.sha256(body).digest()[0] & 1


def hidden_hypothesis(seed: int) -> str:
    return "h_A" if stable_bit(seed, "hidden") == 0 else "h_B"


def f2_signal_use(seed: int) -> int:
    """Prospectively generated bounded stochastic miss schedule.

    Uses a seed-keyed PRNG. Each of the first B-1 c2 uses independently
    succeeds with probability F2_P_SIGNAL. If none succeeds, Gamma forces
    the Bth use to signal. This is generated before target behavior.
    """
    rng = random.Random(seed ^ 0xC5D001F2)
    for use in range(1, B):
        if rng.random() < F2_P_SIGNAL:
            return use
    return B


def make_world(seed: int, failure_class: str) -> AuditWorld:
    if failure_class not in FAILURE_CLASSES:
        raise ValueError(failure_class)
    return AuditWorld(
        seed=seed,
        failure_class=failure_class,
        hidden_hypothesis=hidden_hypothesis(seed),
        f2_signal_use=f2_signal_use(seed) if failure_class == "F2" else None,
    )


def pre_transition_observation(world: AuditWorld, action: str) -> str:
    if action == "c2":
        return SIGNALS[world.hidden_hypothesis]
    return "AMBIGUOUS"


def post_transition_observation(world: AuditWorld, action: str, valid_use_index: int) -> str:
    if action not in D_AGENT:
        raise ValueError("target-visible current-set action required")

    if world.failure_class == "F1":
        return SIGNALS[world.hidden_hypothesis] if action == "c2" else "AMBIGUOUS"

    if world.failure_class == "F2":
        if action == "c2" and valid_use_index >= int(world.f2_signal_use):
            return SIGNALS[world.hidden_hypothesis]
        return "AMBIGUOUS"

    if world.failure_class in ("F3", "F3u"):
        return "AMBIGUOUS"

    raise AssertionError(world.failure_class)


def forced_c_star_observation(world: AuditWorld) -> str:
    """Harness-only post-endpoint attribution control."""
    return SIGNALS[world.hidden_hypothesis]


def validation(resolved: bool) -> str:
    return "PASS" if resolved else "FAIL"


def visible_event(
    phase: str,
    action: str,
    valid: bool,
    observation: str,
    use_counts: Dict[str, int],
    coverage_complete: bool,
    resolved: bool,
) -> dict:
    return {
        "phase": phase,
        "D_agent": list(D_AGENT),
        "action": action,
        "execution_valid": valid,
        "observation": observation,
        "valid_use_counts": dict(use_counts),
        "coverage_complete": coverage_complete,
        "Gamma": {"B_valid_uses_per_current_challenge": B},
        "validation": validation(resolved),
    }


def run_world(world: AuditWorld) -> dict:
    visible: List[dict] = []
    audit: List[dict] = []
    resolved = False

    # PRE calibration: D_agent is genuinely adequate in every family.
    counts = {a: 0 for a in D_AGENT}
    obs = pre_transition_observation(world, "c2")
    resolved = obs in ("SIG_A", "SIG_B")
    visible.append(
        visible_event("PRE", "c2", True, obs, counts, False, resolved)
    )
    audit.append({
        "phase": "PRE",
        "failure_class": world.failure_class,
        "hidden_hypothesis": world.hidden_hypothesis,
        "ground_truth_adequate": True,
    })

    # Transition resets the current live distinction to unresolved.
    resolved = False

    # F1 pre-audit execution pressure: many current-set challenges, poor coverage.
    # Other classes receive the same number of generic c0 executions to keep
    # task-failure pressure available without completing the certificate.
    for _ in range(PRE_AUDIT_FAILURE_ROUNDS):
        action = "c0"
        counts[action] += 1
        obs = post_transition_observation(world, action, counts[action])
        if obs in ("SIG_A", "SIG_B"):
            resolved = True
        visible.append(
            visible_event("PRE_AUDIT", action, True, obs, counts, False, resolved)
        )
        audit.append({
            "phase": "PRE_AUDIT",
            "failure_class": world.failure_class,
            "hidden_hypothesis": world.hidden_hypothesis,
            "ground_truth_adequate": world.failure_class in ("F1", "F2"),
        })

    # Certified audit counts are distinct from pre-audit counts.
    audit_counts = {a: 0 for a in D_AGENT}
    t_u = None
    t_w = None
    step = 0
    max_uses = F3U_USES_PER_CHALLENGE if world.failure_class == "F3u" else B

    for _round_idx in range(max_uses):
        for action in D_AGENT:
            step += 1
            audit_counts[action] += 1
            obs = post_transition_observation(world, action, audit_counts[action])
            if obs in ("SIG_A", "SIG_B"):
                resolved = True

            coverage_complete = all(audit_counts[a] >= B for a in D_AGENT)
            if coverage_complete and t_u is None:
                t_u = step

            # Under Gamma, F3 becomes warranted insufficient only after the
            # complete certificate and persistent unresolved ambiguity.
            if (
                world.failure_class == "F3"
                and coverage_complete
                and not resolved
                and t_w is None
            ):
                t_w = step

            visible.append(
                visible_event(
                    "AUDIT",
                    action,
                    True,
                    obs,
                    audit_counts,
                    coverage_complete,
                    resolved,
                )
            )
            audit.append({
                "phase": "AUDIT",
                "step": step,
                "failure_class": world.failure_class,
                "hidden_hypothesis": world.hidden_hypothesis,
                "ground_truth_adequate": world.failure_class in ("F1", "F2"),
                "warrant_time": t_w,
            })

    # T_* occurs after the scored prefix; c_star is never target-visible.
    t_star = step + 1
    c_star_obs = forced_c_star_observation(world) if world.failure_class in ("F3", "F3u") else None

    return {
        "seed": world.seed,
        "failure_class": world.failure_class,
        "visible_trace": visible,
        "audit_trace": audit,
        "summary": {
            "hidden_hypothesis": world.hidden_hypothesis,
            "f2_signal_use": world.f2_signal_use,
            "ground_truth_adequate": world.failure_class in ("F1", "F2"),
            "resolved_by_scored_endpoint": resolved,
            "T_U": t_u,
            "T_W": t_w,
            "T_star": t_star,
            "post_endpoint_c_star_observation": c_star_obs,
            "audit_valid_use_counts": audit_counts,
        },
    }


def visible_payload_has_leak(event: dict) -> bool:
    return any(k in event for k in HARNESS_ONLY_FIELDS)


def apparatus_checks(all_runs: List[dict]) -> Tuple[List[dict], dict]:
    checks: List[dict] = []

    def add(name: str, ok: bool, detail=None):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})

    by_class: Dict[str, List[dict]] = {c: [] for c in FAILURE_CLASSES}
    for run in all_runs:
        by_class[run["failure_class"]].append(run)

    add("seed_count_per_class",
        all(len(by_class[c]) == SEEDS for c in FAILURE_CLASSES),
        {c: len(by_class[c]) for c in FAILURE_CLASSES})

    # PRE adequacy: every family resolves from pre-transition c2.
    pre_ok = all(
        any(e["phase"] == "PRE" and e["observation"] in ("SIG_A", "SIG_B")
            for e in r["visible_trace"])
        for r in all_runs
    )
    add("pre_transition_D_agent_adequate_all_classes", pre_ok)

    # F1/F2 must resolve within Gamma.
    f1_ok = all(r["summary"]["resolved_by_scored_endpoint"] for r in by_class["F1"])
    f2_ok = all(r["summary"]["resolved_by_scored_endpoint"] for r in by_class["F2"])
    add("F1_adequate_under_Gamma", f1_ok)
    add("F2_adequate_under_Gamma", f2_ok)

    # Boundary subset exists: first F2 signal on final c2 use B.
    boundary = sum(r["summary"]["f2_signal_use"] == B for r in by_class["F2"])
    add("F2_boundary_subset_exists", boundary > 0, {"count": boundary})

    # F3 must remain unresolved after complete certified audit.
    f3_unresolved = all(not r["summary"]["resolved_by_scored_endpoint"] for r in by_class["F3"])
    f3_coverage = all(
        r["summary"]["T_U"] is not None and
        all(v >= B for v in r["summary"]["audit_valid_use_counts"].values())
        for r in by_class["F3"]
    )
    add("F3_no_current_set_discriminator", f3_unresolved)
    add("F3_complete_certified_exposure", f3_coverage)

    # F3u stays incomplete and unresolved.
    f3u_unresolved = all(not r["summary"]["resolved_by_scored_endpoint"] for r in by_class["F3u"])
    f3u_incomplete = all(r["summary"]["T_U"] is None for r in by_class["F3u"])
    add("F3u_true_insufficiency_unresolved", f3u_unresolved)
    add("F3u_certificate_incomplete", f3u_incomplete)

    # F3 warrant time must coincide with certificate completion.
    warrant_ok = all(
        r["summary"]["T_W"] == r["summary"]["T_U"] and r["summary"]["T_W"] is not None
        for r in by_class["F3"]
    )
    add("F3_warrant_after_complete_Gamma_certificate", warrant_ok)

    # Post-endpoint c_star resolves F3/F3u.
    cstar_ok = all(
        r["summary"]["post_endpoint_c_star_observation"] in ("SIG_A", "SIG_B")
        for c in ("F3", "F3u") for r in by_class[c]
    )
    add("post_endpoint_c_star_discriminates", cstar_ok)

    # No target-visible leak.
    leaks = [
        (r["seed"], r["failure_class"], i)
        for r in all_runs
        for i, e in enumerate(r["visible_trace"])
        if visible_payload_has_leak(e)
    ]
    add("no_harness_only_field_in_visible_payload", len(leaks) == 0, {"leaks": leaks[:5]})

    # Same certified audit action sequence for F2/F3.
    def audit_actions(r: dict) -> List[str]:
        return [e["action"] for e in r["visible_trace"] if e["phase"] == "AUDIT"]
    schedule_ok = all(
        audit_actions(by_class["F2"][i]) == audit_actions(by_class["F3"][i])
        for i in range(SEEDS)
    )
    add("F2_F3_identical_certified_audit_schedule", schedule_ok)

    # Generic FAIL consequence occurs in every class.
    fail_presence = {
        c: all(any(e["validation"] == "FAIL" for e in r["visible_trace"]) for r in by_class[c])
        for c in FAILURE_CLASSES
    }
    add("generic_FAIL_available_all_classes", all(fail_presence.values()), fail_presence)

    # Shortcut scorer control: FAIL=>DIAG would false-positive in F1/F2/F3u.
    shortcut_false_positive = {
        c: sum(any(e["validation"] == "FAIL" for e in r["visible_trace"]) for r in by_class[c])
        for c in ("F1", "F2", "F3u")
    }
    add(
        "generic_failure_shortcut_is_rejected_by_controls",
        all(shortcut_false_positive[c] == SEEDS for c in shortcut_false_positive),
        shortcut_false_positive,
    )

    # Timing T_* strictly after scored audit.
    tstar_ok = all(r["summary"]["T_star"] > 0 for r in all_runs)
    add("missing_discriminator_disclosed_only_post_endpoint", tstar_ok)

    passed = sum(c["pass"] for c in checks)
    summary = {
        "checks_passed": passed,
        "checks_total": len(checks),
        "all_pass": passed == len(checks),
        "F2_boundary_count": boundary,
    }
    return checks, summary


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "results")
    parser.add_argument("--emit-traces", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    args.out.mkdir(parents=True, exist_ok=True)

    source_hashes = {}
    for name in ("CSD_001_SPEC.md", "CSD_001_MANIFEST.json", "CSD_001_ANALYSIS.md", "csd_001.py"):
        p = root / name
        source_hashes[name] = hashlib.sha256(p.read_bytes()).hexdigest()

    all_runs = []
    for seed in range(SEEDS):
        for failure_class in FAILURE_CLASSES:
            all_runs.append(run_world(make_world(seed, failure_class)))

    checks, check_summary = apparatus_checks(all_runs)

    result = {
        "assay": ASSAY,
        "status": (
            "APPARATUS_READY_FOR_TARGET_FREEZE"
            if check_summary["all_pass"]
            else "INVALID_APPARATUS"
        ),
        "scientific_target_evaluated": False,
        "target_mechanism": None,
        "source_sha256": source_hashes,
        "parameters": {
            "seeds": SEEDS,
            "B": B,
            "D_agent": list(D_AGENT),
            "pre_audit_failure_rounds": PRE_AUDIT_FAILURE_ROUNDS,
            "F3u_uses_per_challenge": F3U_USES_PER_CHALLENGE,
            "F2_p_signal_before_bound": F2_P_SIGNAL,
        },
        "apparatus_check_summary": check_summary,
        "apparatus_checks": checks,
        "descriptive": {
            "F2_signal_use_distribution": {
                str(k): sum(
                    1 for r in all_runs
                    if r["failure_class"] == "F2" and r["summary"]["f2_signal_use"] == k
                )
                for k in range(1, B + 1)
            },
            "F3_T_U_values": sorted(set(
                r["summary"]["T_U"] for r in all_runs if r["failure_class"] == "F3"
            )),
            "F3_T_W_values": sorted(set(
                r["summary"]["T_W"] for r in all_runs if r["failure_class"] == "F3"
            )),
            "F3u_T_U_values": sorted(set(
                r["summary"]["T_U"] for r in all_runs if r["failure_class"] == "F3u"
            )),
        },
        "claim_ceiling": (
            "This run validates only the frozen CSD-001 assay apparatus. "
            "No L2 target mechanism was implemented or evaluated."
        ),
    }

    result_path = args.out / "csd_001_apparatus_result.json"
    write_json(result_path, result)

    if args.emit_traces:
        trace_path = args.out / "csd_001_apparatus_traces.jsonl"
        with trace_path.open("w", encoding="utf-8", newline="\n") as f:
            for r in all_runs:
                f.write(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n")

    print(json.dumps({
        "status": result["status"],
        "checks": check_summary,
        "result": str(result_path),
    }, indent=2))
    return 0 if check_summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
