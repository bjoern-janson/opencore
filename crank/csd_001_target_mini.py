#!/usr/bin/env python3
"""CSD-001 frozen Mini target runner.

Mechanical implementation of CSD_001_TARGET_SPEC.md only.

Pipeline:
    unchanged CSD visible event
    -> exact frozen transport
    -> unchanged Mini Organism.observe(...)
    -> exact stateless needs_probe adapter
    -> frozen scorer

No L2 cognition, adequacy evaluator, challenge generator, or repair mechanism is
implemented here.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from csd_001 import (
    FAILURE_CLASSES,
    SEEDS,
    apparatus_checks,
    make_world,
    run_world,
)
from mini import Organism

ASSAY = "CSD-001"
TARGET = "OPENCORE_MINI_CORE"

MINI_EXPECTED_SHA256 = "fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55"
CSD_HARNESS_EXPECTED_SHA256 = "1899da7f1675d9b0fb691d973351ebe86aca3819e01182f108e7ee515f93a7c9"
CSD_SPEC_EXPECTED_SHA256 = "ee2b14de9e0ab8ee332d3198b676115ed58714c0f69a6af0b1c1ffd0999d3271"
CSD_MANIFEST_EXPECTED_SHA256 = "cdbba807bd5587dfa21f892801661a97fb0be7103a3e7a748d2dbda087242f06"
CSD_ANALYSIS_EXPECTED_SHA256 = "c7426bea36074a96a1567abf2cf1784f31ed265e2d59e1a95dc99e87f823da4d"
TARGET_SPEC_EXPECTED_GIT_BLOB = "fd55b90e4068f7b75f01f2fbcea900c45dd8e153"

SCOPE_MAP = {
    "c0": "CSD001::c0",
    "c1": "CSD001::c1",
    "c2": "CSD001::c2",
}
Y_MAP = {
    "AMBIGUOUS": 0,
    "SIG_A": 1,
    "SIG_B": 2,
}
SCOPES = tuple(SCOPE_MAP[a] for a in ("c0", "c1", "c2"))

MIN_F3_VALID_DIAGNOSES = 205
MAX_FALSE_PER_CONTROL = 12
MAX_F3_PREMATURE = 12

_A4_HARNESS_CONTEXT: dict = {}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    body = path.read_bytes()
    header = f"blob {len(body)}\0".encode("ascii")
    return hashlib.sha1(header + body).hexdigest()


def csd001_mini_adapter(org: Organism) -> Dict[str, bool]:
    """Exact frozen stateless projection from native Mini state."""
    return {
        "CSD001::c0": org.needs_probe("CSD001::c0"),
        "CSD001::c1": org.needs_probe("CSD001::c1"),
        "CSD001::c2": org.needs_probe("CSD001::c2"),
    }


def _a4_negative_control(org: Organism) -> Tuple[bool, str]:
    """Deliberately contaminated adapter used only to prove A4 has power."""
    raw = org.needs_probe("CSD001::c2")
    return raw, str(_A4_HARNESS_CONTEXT.get("F_i"))


def adapter_admissibility_checks() -> Tuple[List[dict], dict]:
    """Run A1-A4 before any target evaluation world is generated."""
    checks: List[dict] = []

    def add(name: str, ok: bool, detail=None) -> None:
        checks.append({"name": name, "pass": bool(ok), "detail": detail})

    sig = inspect.signature(csd001_mini_adapter)
    params = list(sig.parameters.values())
    one_org_input = (
        len(params) == 1
        and params[0].name == "org"
        and params[0].kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    )
    add("A1_single_organism_input", one_org_input, str(sig))

    allowed_names = {"needs_probe"}
    code_names = set(csd001_mini_adapter.__code__.co_names)
    add(
        "A1_direct_native_projection_only",
        code_names <= allowed_names,
        {"code_names": sorted(code_names), "allowed": sorted(allowed_names)},
    )

    forbidden_tokens = (
        "failure",
        "gamma",
        "coverage",
        "warrant",
        "oracle",
        "c_star",
        "t_w",
        "hidden",
        "adequ",
        "count",
        "history",
        "trace",
        "lineage",
        "observation",
    )
    source = inspect.getsource(csd001_mini_adapter).lower()
    forbidden_hits = sorted(token for token in forbidden_tokens if token in source)
    add("A2_failure_class_blind", "failure" not in source and "hidden" not in source, forbidden_hits)
    add(
        "A3_Gamma_and_coverage_blind",
        all(token not in source for token in ("gamma", "coverage", "warrant", "count")),
        forbidden_hits,
    )

    org = Organism()
    scope = "CSD001::c2"
    org.observe(scope, 0, 0, "A4_SELF_TEST")
    org.observe(scope, 1, 1, "A4_SELF_TEST")
    org.observe(scope, 2, 0, "A4_SELF_TEST")
    native_pending = org.needs_probe(scope)
    add("A1_native_state_fixture_has_pending_request", native_pending)

    global _A4_HARNESS_CONTEXT
    omega_1 = {
        "F_i": "F2",
        "Gamma": {"B": 8},
        "D_oracle": ["different-a"],
        "T_W": None,
        "c_star": "hidden-one",
    }
    omega_2 = {
        "F_i": "F3",
        "Gamma": {"B": 999},
        "D_oracle": ["different-b"],
        "T_W": 24,
        "c_star": "hidden-two",
    }

    _A4_HARNESS_CONTEXT = omega_1
    out_1 = csd001_mini_adapter(org)
    _A4_HARNESS_CONTEXT = omega_2
    out_2 = csd001_mini_adapter(org)
    add(
        "A4_counterfactual_invariance",
        out_1 == out_2,
        {"omega_1_output": out_1, "omega_2_output": out_2},
    )

    _A4_HARNESS_CONTEXT = omega_1
    neg_1 = _a4_negative_control(org)
    _A4_HARNESS_CONTEXT = omega_2
    neg_2 = _a4_negative_control(org)
    add(
        "A4_negative_control_detects_hidden_oracle_dependency",
        neg_1 != neg_2,
        {"omega_1_output": neg_1, "omega_2_output": neg_2},
    )
    _A4_HARNESS_CONTEXT = {}

    summary = {
        "checks_passed": sum(int(c["pass"]) for c in checks),
        "checks_total": len(checks),
        "all_pass": all(c["pass"] for c in checks),
    }
    return checks, summary


def transport_event(org: Organism, event: dict) -> dict:
    """Exact frozen CSD-visible-event -> Mini.observe transport."""
    phase = event["phase"]
    action = event["action"]
    execution_valid = event["execution_valid"]
    observation = event["observation"]
    valid_use_count = event["valid_use_counts"][action]

    if execution_valid is not True:
        raise ValueError("INVALID_TARGET_TRANSPORT: execution_valid is not True")
    if action not in SCOPE_MAP:
        raise ValueError(f"INVALID_TARGET_TRANSPORT: unsupported action {action!r}")
    if observation not in Y_MAP:
        raise ValueError(f"INVALID_TARGET_TRANSPORT: unsupported observation {observation!r}")
    if phase not in ("PRE", "PRE_AUDIT", "AUDIT"):
        raise ValueError(f"INVALID_TARGET_TRANSPORT: unsupported phase {phase!r}")
    if not isinstance(valid_use_count, int):
        raise ValueError("INVALID_TARGET_TRANSPORT: valid-use count is not int")

    scope = SCOPE_MAP[action]
    x = valid_use_count % 11
    y = Y_MAP[observation]

    before_n = len(org.observations)
    org.observe(scope, x, y, phase)
    after_n = len(org.observations)
    if after_n != before_n + 1:
        raise AssertionError("INVALID_TARGET_TRANSPORT: one event != one Mini observation")

    return {"scope": scope, "x": x, "y": y, "phase": phase}


def audit_step_by_event(visible_trace: List[dict]) -> List[Optional[int]]:
    out: List[Optional[int]] = []
    step = 0
    for event in visible_trace:
        if event["phase"] == "AUDIT":
            step += 1
            out.append(step)
        else:
            out.append(None)
    return out


def bool_intervals(samples: List[dict], scope: str) -> List[dict]:
    """Contiguous True intervals in event order, with audit-step coordinates."""
    intervals: List[dict] = []
    start: Optional[int] = None
    for i, sample in enumerate(samples):
        val = bool(sample["Y_t"][scope])
        if val and start is None:
            start = i
        if start is not None and (not val or i == len(samples) - 1):
            end = i if val and i == len(samples) - 1 else i - 1
            chunk = samples[start : end + 1]
            audit_steps = [x["audit_step"] for x in chunk if x["audit_step"] is not None]
            intervals.append(
                {
                    "event_start": start,
                    "event_end": end,
                    "phase_start": chunk[0]["phase"],
                    "phase_end": chunk[-1]["phase"],
                    "audit_step_start": min(audit_steps) if audit_steps else None,
                    "audit_step_end": max(audit_steps) if audit_steps else None,
                    "reaches_scored_endpoint": end == len(samples) - 1,
                }
            )
            start = None
    return intervals


def persistent_suffix_candidate(samples: List[dict]) -> dict:
    """Frozen persistent-c2-request suffix and T_D_candidate extraction."""
    scope = "CSD001::c2"
    if not samples or not samples[-1]["Y_t"][scope]:
        return {
            "persistent_c2_request": False,
            "suffix_event_start": None,
            "T_D_candidate": None,
            "already_active_before_audit": False,
        }

    start = len(samples) - 1
    while start > 0 and samples[start - 1]["Y_t"][scope]:
        start -= 1

    begins_pre_audit = samples[start]["phase"] != "AUDIT"
    if begins_pre_audit:
        t_d_candidate = 1
    else:
        t_d_candidate = samples[start]["audit_step"]
        if t_d_candidate is None:
            raise AssertionError("AUDIT suffix start lacks audit step")

    return {
        "persistent_c2_request": True,
        "suffix_event_start": start,
        "T_D_candidate": t_d_candidate,
        "already_active_before_audit": begins_pre_audit,
    }


def run_target_world(csd_run: dict) -> dict:
    """Run one fresh continuous-lifetime Mini instance on one frozen CSD world."""
    org = Organism()
    visible = csd_run["visible_trace"]
    steps = audit_step_by_event(visible)
    samples: List[dict] = []
    transported: List[dict] = []

    for event, audit_step in zip(visible, steps):
        call = transport_event(org, event)
        y_t = csd001_mini_adapter(org)
        transported.append(call)
        samples.append(
            {
                "phase": event["phase"],
                "action": event["action"],
                "observation": event["observation"],
                "audit_step": audit_step,
                "Y_t": y_t,
                "shadow_request_c2": (
                    "REQUEST_MORE_EVIDENCE_ON_CSD001::c2"
                    if y_t["CSD001::c2"]
                    else "NO_REQUEST_ON_CSD001::c2"
                ),
            }
        )

    suffix = persistent_suffix_candidate(samples)
    intervals = {scope: bool_intervals(samples, scope) for scope in SCOPES}

    summary = csd_run["summary"]
    t_w = summary["T_W"]
    t_star = summary["T_star"]
    t_d = suffix["T_D_candidate"]

    timing_valid = (
        bool(suffix["persistent_c2_request"])
        and t_w is not None
        and t_d is not None
        and summary["T_U"] is not None
        and summary["T_U"] <= t_w <= t_d < t_star
    )
    premature = (
        bool(suffix["persistent_c2_request"])
        and t_w is not None
        and t_d is not None
        and t_d < t_w
    )

    return {
        "seed": csd_run["seed"],
        "failure_class": csd_run["failure_class"],
        "samples": samples,
        "transported": transported,
        "pending_intervals": intervals,
        "candidate": {
            **suffix,
            "T_U": summary["T_U"],
            "T_W": t_w,
            "T_star": t_star,
            "timing_valid": timing_valid,
            "premature": premature,
            "T_D_minus_T_W": (
                t_d - t_w if timing_valid and t_d is not None and t_w is not None else None
            ),
        },
    }


def summarize_target(rows: List[dict]) -> dict:
    by_class = {c: [r for r in rows if r["failure_class"] == c] for c in FAILURE_CLASSES}

    def persistent_count(c: str) -> int:
        return sum(int(r["candidate"]["persistent_c2_request"]) for r in by_class[c])

    f3_valid = sum(int(r["candidate"]["timing_valid"]) for r in by_class["F3"])
    f3_premature = sum(int(r["candidate"]["premature"]) for r in by_class["F3"])

    counts = {
        "F1_persistent": persistent_count("F1"),
        "F2_persistent": persistent_count("F2"),
        "F3_persistent": persistent_count("F3"),
        "F3u_persistent": persistent_count("F3u"),
        "F3_valid_timing": f3_valid,
        "F3_premature": f3_premature,
    }
    rates = {k: v / SEEDS for k, v in counts.items()}

    control_breach = (
        counts["F1_persistent"] > MAX_FALSE_PER_CONTROL
        or counts["F2_persistent"] > MAX_FALSE_PER_CONTROL
        or counts["F3u_persistent"] > MAX_FALSE_PER_CONTROL
        or counts["F3_premature"] > MAX_F3_PREMATURE
    )

    positive = (
        counts["F3_persistent"] >= MIN_F3_VALID_DIAGNOSES
        and counts["F3_valid_timing"] >= MIN_F3_VALID_DIAGNOSES
        and counts["F3_premature"] <= MAX_F3_PREMATURE
        and counts["F1_persistent"] <= MAX_FALSE_PER_CONTROL
        and counts["F2_persistent"] <= MAX_FALSE_PER_CONTROL
        and counts["F3u_persistent"] <= MAX_FALSE_PER_CONTROL
    )

    if positive:
        scientific_classification = "CHALLENGE_SET_INSUFFICIENCY_DIAGNOSIS_ESTABLISHED"
    elif control_breach:
        scientific_classification = "FAILURE_CAUSE_CONFLATION"
    else:
        scientific_classification = "FAILURE_TO_DIAGNOSE"

    paired_f2_f3 = []
    f2_by_seed = {r["seed"]: r for r in by_class["F2"]}
    f3_by_seed = {r["seed"]: r for r in by_class["F3"]}
    for seed in range(SEEDS):
        r2 = f2_by_seed[seed]["candidate"]
        r3 = f3_by_seed[seed]["candidate"]
        paired_f2_f3.append(
            {
                "seed": seed,
                "F2_persistent": r2["persistent_c2_request"],
                "F2_T_D_candidate": r2["T_D_candidate"],
                "F3_persistent": r3["persistent_c2_request"],
                "F3_T_D_candidate": r3["T_D_candidate"],
                "F3_timing_valid": r3["timing_valid"],
                "F3_premature": r3["premature"],
            }
        )

    td_values = [
        r["candidate"]["T_D_candidate"]
        for r in by_class["F3"]
        if r["candidate"]["T_D_candidate"] is not None
    ]

    return {
        "counts": counts,
        "rates": rates,
        "thresholds": {
            "MIN_F3_VALID_DIAGNOSES": MIN_F3_VALID_DIAGNOSES,
            "MAX_FALSE_PER_CONTROL": MAX_FALSE_PER_CONTROL,
            "MAX_F3_PREMATURE": MAX_F3_PREMATURE,
        },
        "F3_T_D_candidate_distribution": {
            str(v): td_values.count(v) for v in sorted(set(td_values))
        },
        "paired_F2_F3": paired_f2_f3,
        "scientific_classification": scientific_classification,
    }


def source_identity_checks(root: Path) -> Tuple[List[dict], dict]:
    checks = []

    def add(name: str, actual: str, expected: str) -> None:
        checks.append({"name": name, "pass": actual == expected, "actual": actual, "expected": expected})

    add("mini_sha256", sha256_file(root / "mini.py"), MINI_EXPECTED_SHA256)
    add("csd_harness_sha256", sha256_file(root / "csd_001.py"), CSD_HARNESS_EXPECTED_SHA256)
    add("csd_spec_sha256", sha256_file(root / "CSD_001_SPEC.md"), CSD_SPEC_EXPECTED_SHA256)
    add("csd_manifest_sha256", sha256_file(root / "CSD_001_MANIFEST.json"), CSD_MANIFEST_EXPECTED_SHA256)
    add("csd_analysis_sha256", sha256_file(root / "CSD_001_ANALYSIS.md"), CSD_ANALYSIS_EXPECTED_SHA256)
    add(
        "target_spec_git_blob",
        git_blob_sha1(root / "CSD_001_TARGET_SPEC.md"),
        TARGET_SPEC_EXPECTED_GIT_BLOB,
    )

    summary = {
        "checks_passed": sum(int(c["pass"]) for c in checks),
        "checks_total": len(checks),
        "all_pass": all(c["pass"] for c in checks),
    }
    return checks, summary


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "results")
    parser.add_argument("--emit-traces", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    args.out.mkdir(parents=True, exist_ok=True)

    source_checks, source_summary = source_identity_checks(root)
    adapter_checks, adapter_summary = adapter_admissibility_checks()

    if not source_summary["all_pass"]:
        result = {
            "assay": ASSAY,
            "target": TARGET,
            "status": "INVALID_TARGET_IDENTITY",
            "source_checks": source_checks,
            "source_check_summary": source_summary,
            "adapter_checks": adapter_checks,
            "adapter_check_summary": adapter_summary,
            "scientific_classification": "INVALID",
        }
        write_json(args.out / "csd_001_mini_target_result.json", result)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2

    if not adapter_summary["all_pass"]:
        result = {
            "assay": ASSAY,
            "target": TARGET,
            "status": "INVALID_MEASUREMENT_INTERFACE",
            "source_checks": source_checks,
            "source_check_summary": source_summary,
            "adapter_checks": adapter_checks,
            "adapter_check_summary": adapter_summary,
            "scientific_classification": "INVALID",
        }
        write_json(args.out / "csd_001_mini_target_result.json", result)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 3

    csd_runs = [
        run_world(make_world(seed, failure_class))
        for seed in range(SEEDS)
        for failure_class in FAILURE_CLASSES
    ]
    app_checks, app_summary = apparatus_checks(csd_runs)
    if not app_summary["all_pass"]:
        result = {
            "assay": ASSAY,
            "target": TARGET,
            "status": "INVALID_APPARATUS",
            "source_checks": source_checks,
            "source_check_summary": source_summary,
            "adapter_checks": adapter_checks,
            "adapter_check_summary": adapter_summary,
            "apparatus_checks": app_checks,
            "apparatus_check_summary": app_summary,
            "scientific_classification": "INVALID",
        }
        write_json(args.out / "csd_001_mini_target_result.json", result)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 4

    target_rows = [run_target_world(r) for r in csd_runs]
    target_summary = summarize_target(target_rows)

    result = {
        "assay": ASSAY,
        "target": TARGET,
        "status": "TARGET_EVALUATED",
        "scientific_classification": target_summary["scientific_classification"],
        "target_spec_git_blob": TARGET_SPEC_EXPECTED_GIT_BLOB,
        "mini_sha256": MINI_EXPECTED_SHA256,
        "source_checks": source_checks,
        "source_check_summary": source_summary,
        "adapter_checks": adapter_checks,
        "adapter_check_summary": adapter_summary,
        "apparatus_check_summary": app_summary,
        "apparatus_checks": app_checks,
        "target_summary": target_summary,
        "claim_boundary": (
            "This result classifies unchanged Mini under the frozen CSD-001 target transport and thresholds. "
            "needs_probe retains its native pre-CSD meaning unless and only insofar as the complete frozen "
            "cross-condition result earns the bounded L2 interpretation."
        ),
    }
    result_path = args.out / "csd_001_mini_target_result.json"
    write_json(result_path, result)

    if args.emit_traces:
        write_jsonl(args.out / "csd_001_mini_target_traces.jsonl", target_rows)

    print(
        json.dumps(
            {
                "status": result["status"],
                "scientific_classification": result["scientific_classification"],
                "adapter": adapter_summary,
                "apparatus": app_summary,
                "target_counts": target_summary["counts"],
                "target_rates": target_summary["rates"],
                "F3_T_D_candidate_distribution": target_summary["F3_T_D_candidate_distribution"],
                "result": str(result_path),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
