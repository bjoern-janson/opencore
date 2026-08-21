#!/usr/bin/env python3
"""OpenCore Nano subtraction study over the frozen Mini x Nano composition suite.

The existing Mini x Nano trial constructors are reused unchanged by temporarily
substituting only the persistence-boundary class they instantiate.  mini.py,
nano.py, and mini_nano_composition.py remain byte-identical.

Ablations:
  naive                         existing comparison store inside frozen harness
  effect_ceiling_only           license/effect containment only
  live_preconditions_only       exact execution-time preconditions over raw current state
  lineage_liveness_only         warrant-parent receipt liveness only; ignores values
  preconditions_plus_lineage    exact preconditions over liveness-filtered state
  full_nano                     frozen Nano V0

The derived preconditions_plus_lineage arm is included only after the single-
feature ablations: it removes effect-ceiling and preservation checks together
and tests whether the two selectively useful mechanisms suffice on this exact
frozen suite.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Type

import mini_nano_composition as comp
from nano import CheckResult, Decision, License, Nano, Transition, _digest, _key_id

HERE = Path(__file__).resolve().parent
MINI_PATH = HERE / "mini.py"
NANO_PATH = HERE / "nano.py"
COMPOSITION_PATH = HERE / "mini_nano_composition.py"

EXPECTED = {
    "mini.py": comp.MINI_EXPECTED_SHA256,
    "nano.py": comp.NANO_EXPECTED_SHA256,
    "mini_nano_composition.py": "116d6e285855081126608a962ad5bb3990f634c63bf76a40c19f7ad18027e7a2",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AblatedNano(Nano):
    """Harness-only feature subtraction; not a Nano revision."""

    CHECK_EFFECTS = False
    CHECK_PRECONDITIONS = False
    CHECK_PRESERVATION = False
    CHECK_LINEAGE_LIVENESS = False
    CHECK_LINEAGE_INPUT_LIVENESS = False

    def _receipt_effective(self, receipt_id: str, seen: set[str] | None = None) -> bool:
        if self.CHECK_LINEAGE_LIVENESS:
            return super()._receipt_effective(receipt_id, seen)
        receipt = self._receipts_by_id.get(receipt_id)
        return receipt is not None and receipt.decision is Decision.ALLOW

    def _precondition_current(self, key):
        if self.CHECK_LINEAGE_LIVENESS:
            return super()._effective_current(key)
        return self._current.get(key)

    def check_transition(self, transition: Transition, license_id: str) -> CheckResult:
        before = self.state_digest()
        tdigest = _digest(asdict(transition))
        deny: list[str] = []
        defer: list[str] = []

        license_ = self.licenses.get(license_id)
        if license_ is None:
            return CheckResult(Decision.DEFER, ("license:not_present",), before, tdigest, license_id)
        if license_id in self.revoked_licenses:
            deny.append("license:revoked")
        if transition.operation != license_.operation:
            deny.append("operation:not_licensed")

        if self.CHECK_PRECONDITIONS:
            for pre in license_.preconditions:
                current = self._precondition_current(pre.key)
                if current is None:
                    defer.append(f"precondition:unestablished:{_key_id(pre.key)}")
                elif current.standing.value != pre.expected:
                    deny.append(f"precondition:contradicted:{_key_id(pre.key)}")
        elif self.CHECK_LINEAGE_INPUT_LIVENESS:
            # Deliberately *not* a value/presence precondition check.  This arm
            # only asks whether an already-present declared warrant input has a
            # still-effective receipt path. Missing inputs and wrong values are
            # invisible to this ablation.
            for pre in license_.preconditions:
                raw = self._current.get(pre.key)
                if raw is not None and raw.receipt_id is not None and not super()._receipt_effective(raw.receipt_id):
                    defer.append(f"lineage:inactive:{_key_id(pre.key)}")

        if self.CHECK_EFFECTS:
            grants = {grant.key: set(grant.allowed_values) for grant in license_.allowed_writes}
            for write in transition.writes:
                allowed = grants.get(write.key)
                if allowed is None or write.value not in allowed:
                    deny.append(f"effect:write_not_licensed:{_key_id(write.key)}")
            allowed_deletes = set(license_.allowed_deletes)
            for key in transition.deletes:
                if key not in allowed_deletes:
                    deny.append(f"effect:delete_not_licensed:{_key_id(key)}")
            allowed_revocations = set(license_.allowed_revocations)
            for target in transition.revoke_licenses:
                if target not in allowed_revocations:
                    deny.append(f"effect:revocation_not_licensed:{target}")

        if self.CHECK_PRESERVATION:
            writes = {standing.key: standing.value for standing in transition.writes}
            deletes = set(transition.deletes)
            for key in license_.required_preservation:
                current = self._current.get(key)
                if current is None:
                    defer.append(f"preservation:unestablished:{_key_id(key)}")
                elif key in deletes or (key in writes and writes[key] != current.standing.value):
                    deny.append(f"preservation:violated:{_key_id(key)}")

        if deny:
            return CheckResult(Decision.DENY, tuple(sorted(set(deny + defer))), before, tdigest, license_id)
        if defer:
            return CheckResult(Decision.DEFER, tuple(sorted(set(defer))), before, tdigest, license_id)
        return CheckResult(Decision.ALLOW, (), before, tdigest, license_id)


class EffectCeilingOnly(AblatedNano):
    CHECK_EFFECTS = True


class LivePreconditionsOnly(AblatedNano):
    CHECK_PRECONDITIONS = True


class LineageLivenessOnly(AblatedNano):
    CHECK_LINEAGE_LIVENESS = True
    CHECK_LINEAGE_INPUT_LIVENESS = True


class PreconditionsPlusLineage(AblatedNano):
    CHECK_PRECONDITIONS = True
    CHECK_LINEAGE_LIVENESS = True


VARIANTS: tuple[tuple[str, Type[Nano]], ...] = (
    ("effect_ceiling_only", EffectCeilingOnly),
    ("live_preconditions_only", LivePreconditionsOnly),
    ("lineage_liveness_only", LineageLivenessOnly),
    ("preconditions_plus_lineage", PreconditionsPlusLineage),
    ("full_nano", Nano),
)


def run_variant(name: str, cls: Type[Nano], n: int, start_seed: int) -> dict:
    original = comp.Nano
    try:
        comp.Nano = cls
        out = comp.sweep(n, start_seed)
    finally:
        comp.Nano = original

    families = {}
    for family, row in out["families"].items():
        families[family] = {
            "attack_attempts": row["attack_attempts"],
            "attack_allows": row["nano_attack_allows"],
            "attack_denies": row["nano_attack_denies"],
            "attack_defers": row["nano_attack_defers"],
            "legitimate_attempts": row["legitimate_attempts"],
            "legitimate_allows": row["nano_legitimate_allows"],
            "false_refusals": row["nano_legitimate_denies"] + row["nano_legitimate_defers"],
        }

    return {
        "variant": name,
        "families": families,
        "aggregate": {
            "attack_attempts": out["aggregate"]["attack_attempts"],
            "attack_allows": out["aggregate"]["nano_attack_overreach"],
            "attack_overreach_rate": out["aggregate"]["nano_attack_overreach_rate"],
            "legitimate_attempts": out["aggregate"]["legitimate_attempts"],
            "legitimate_allows": out["aggregate"]["nano_legitimate_allows"],
            "legitimate_retention_rate": out["aggregate"]["nano_legitimate_retention_rate"],
            "native_mini_lifecycle_pass": out["aggregate"]["native_mini_lifecycle_pass"],
            "native_mini_lifecycle_rate": out["aggregate"]["native_mini_lifecycle_rate"],
        },
    }


def sweep(n: int, start_seed: int) -> dict:
    hashes = {
        "mini.py": sha256(MINI_PATH),
        "nano.py": sha256(NANO_PATH),
        "mini_nano_composition.py": sha256(COMPOSITION_PATH),
    }
    if hashes != EXPECTED:
        raise RuntimeError({"frozen_component_hash_mismatch": hashes, "expected": EXPECTED})

    variants = {name: run_variant(name, cls, n, start_seed) for name, cls in VARIANTS}

    attack_families = [
        "role_laundering",
        "dependency_laundering",
        "acquisition_closure_composition",
        "authority_applicability",
        "stale_descendant",
    ]
    matrix = {}
    for family in attack_families:
        matrix[family] = {
            name: variants[name]["families"][family]["attack_allows"]
            for name, _ in VARIANTS
        }

    preservation = {
        name: {
            "legitimate_allows": variants[name]["families"]["preservation_not_warrant_regression"]["legitimate_allows"],
            "false_refusals": variants[name]["families"]["preservation_not_warrant_regression"]["false_refusals"],
        }
        for name, _ in VARIANTS
    }

    # Naive is fixed by the frozen harness and identical in every arm.
    naive_attack_attempts = n * len(attack_families)
    naive = {
        "attack_attempts": naive_attack_attempts,
        "attack_allows": naive_attack_attempts,
        "attack_overreach_rate": 1.0,
    }

    return {
        "experiment": "OPENCORE_NANO_MINI_SUBTRACTION_V0",
        "n": n,
        "start_seed": start_seed,
        "frozen_component_hashes": hashes,
        "frozen_case_source": "mini_nano_composition.py trial functions reused unchanged via persistence-boundary substitution",
        "naive": naive,
        "variants": variants,
        "attack_allow_matrix_counts": matrix,
        "preservation_not_warrant_regression": preservation,
        "claim_boundary": (
            "ablation over the frozen constructed Mini x Nano composition suite only; "
            "a mechanism absent from the load-bearing set here may still be required by Nano's isolated matrix or other domains"
        ),
    }


def render_markdown(out: dict) -> str:
    n = out["n"]
    names = [name for name, _ in VARIANTS]
    short = {
        "effect_ceiling_only": "effect only",
        "live_preconditions_only": "preconditions",
        "lineage_liveness_only": "lineage/liveness",
        "preconditions_plus_lineage": "preconditions+lineage",
        "full_nano": "full Nano",
    }
    lines = [
        "# OpenCore Nano × Mini — Subtraction / Ablation V0",
        "",
        "**Status:** local constructed ablation; not published; no component modification.",
        "",
        "The exact frozen Mini × Nano trial functions were reused unchanged. Only the persistence-boundary class was substituted.",
        "",
        "## Attack overreach matrix",
        "",
        "Each cell is `ALLOW / attempts` for an already-discovered illegal persistence transition. Lower is better.",
        "",
        "| Family | naive | " + " | ".join(short[x] for x in names) + " |",
        "|---|---:|" + "---:|" * len(names),
    ]
    for fam, row in out["attack_allow_matrix_counts"].items():
        lines.append(
            f"| {fam} | {n}/{n} | " + " | ".join(f"{row[x]}/{n}" for x in names) + " |"
        )
    lines += ["", "## Aggregate", "", "| Boundary | attack ALLOW | legitimate ALLOW | Mini lifecycle |", "|---|---:|---:|---:|"]
    lines.append(f"| naive | {out['naive']['attack_allows']}/{out['naive']['attack_attempts']} | n/a | n/a |")
    for name in names:
        a = out["variants"][name]["aggregate"]
        lines.append(
            f"| {short[name]} | {a['attack_allows']}/{a['attack_attempts']} | "
            f"{a['legitimate_allows']}/{a['legitimate_attempts']} | "
            f"{a['native_mini_lifecycle_pass']}/{n} |"
        )
    lines += [
        "",
        "## Claim boundary",
        "",
        out["claim_boundary"],
        "",
        "This assay identifies what is load-bearing for these five frozen Mini authority attacks. It does not show that omitted mechanisms are globally redundant.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", type=int, default=1000)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--output-json", type=Path)
    ap.add_argument("--output-md", type=Path)
    args = ap.parse_args()

    out = sweep(args.sweep, args.start_seed)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        args.output_json.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.output_md:
        args.output_md.write_text(render_markdown(out), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
