#!/usr/bin/env python3
"""FOREIGN-001: frozen OpenCore stack under Mastermind pressure.

Foreign task
------------
A reduced but semantics-preserving Mastermind game with 2 positions, 3 colours,
repetition allowed, and standard (black, white) feedback.  The task is foreign to
OpenCore; no Mastermind solver is added to Mini.

Two arms:
  STATIC   - one hidden code is fixed for the whole game.
  DYNAMIC  - an adaptive codemaker may change the hidden code after each guess,
             but every answer must preserve a non-empty set of codes consistent
             with the complete public history.

Frozen stack usage
------------------
Mini: receives a lossless scalar encoding of (guess -> feedback) and proposes its
      existing affine Z_11 commitments without modification.
Nano: persists Mini's current model under an externally supplied, narrow license.
Base: the Nano effective MODEL standing is the shared computational world read by
      the task-facing predictor.  No Base-001 12-unit scaffold is imported.

Question
--------
Where does corrective flow stop in a genuinely foreign task, classified as:
  evidence insufficiency | authority insufficiency | expressive insufficiency ?

This harness is diagnostic.  It does not repair Mini or Nano and does not claim
that Mastermind is a benchmark for general intelligence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from itertools import product
from pathlib import Path

from mini import HYPOTHESES, MOD, Organism, Rule
from nano import Decision, License, Nano, Precondition, Standing, StandingKey, Transition, WriteGrant

HERE = Path(__file__).resolve().parent
MINI_PATH = HERE / "mini.py"
NANO_PATH = HERE / "nano.py"
MINI_EXPECTED_SHA256 = "fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55"
NANO_EXPECTED_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"

COLORS = 3
POSITIONS = 2
CODES = tuple(product(range(COLORS), repeat=POSITIONS))
GUESSES = CODES
# All feedback values possible in 2x3 Mastermind, sorted for a fixed injective encoding.
FEEDBACKS = ((0, 0), (0, 1), (0, 2), (1, 0), (2, 0))
FEEDBACK_TO_Y = {fb: i for i, fb in enumerate(FEEDBACKS)}
Y_TO_FEEDBACK = {i: fb for fb, i in FEEDBACK_TO_Y.items()}
RULE_VALUES = tuple(Rule(a, c).short() for a, c in HYPOTHESES)


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def score(code: tuple[int, ...], guess: tuple[int, ...]) -> tuple[int, int]:
    black = sum(a == b for a, b in zip(code, guess))
    cc: Counter[int] = Counter()
    gc: Counter[int] = Counter()
    for a, b in zip(code, guess):
        if a != b:
            cc[a] += 1
            gc[b] += 1
    white = sum(min(cc[k], gc[k]) for k in cc)
    return black, white


def guess_x(guess: tuple[int, int]) -> int:
    # Base-3 enumeration is injective and uses x=0..8, all inside Mini's Z_11 input domain.
    return guess[0] * COLORS + guess[1]


def feedback_y(fb: tuple[int, int]) -> int:
    return FEEDBACK_TO_Y[fb]


def candidate_filter(
    candidates: set[tuple[int, int]], guess: tuple[int, int], fb: tuple[int, int]
) -> set[tuple[int, int]]:
    return {code for code in candidates if score(code, guess) == fb}


def parse_rule(value: str) -> Rule:
    # Values are generated only by Rule.short(), e.g. "7x+3 mod 11".
    left = value.split(" mod ", 1)[0]
    a_s, c_s = left.split("x+", 1)
    return Rule(int(a_s), int(c_s))


def effective_value(nano: Nano, key: StandingKey) -> str | None:
    for standing in nano.effective_state().active:
        if standing.key == key:
            return standing.value
    return None


def master_function(secret: tuple[int, int]) -> tuple[int, ...]:
    return tuple(feedback_y(score(secret, guess)) for guess in GUESSES)


def representability_proof() -> dict:
    """Exhaustively prove the reduced foreign mapping is outside Mini's hypothesis class.

    Every Mini Rule uses non-zero slope modulo 11 and is therefore injective on distinct
    x. Every 2x3 Mastermind secret maps at least two different guesses to the same
    feedback class. Thus no injective feedback-class encoding can make the full
    guess->feedback relation equal a Mini Rule. We also exhaustively verify against the
    fixed encoding used by this harness.
    """
    repeated_feedback = {}
    matching_rules = {}
    for secret in CODES:
        ys = master_function(secret)
        repeated_feedback[str(secret)] = len(set(ys)) < len(ys)
        matches = []
        for a, c in HYPOTHESES:
            r = Rule(a, c)
            if all(r(guess_x(g)) == y for g, y in zip(GUESSES, ys)):
                matches.append(r.short())
        matching_rules[str(secret)] = matches
    return {
        "codes": len(CODES),
        "feedback_classes": len(FEEDBACKS),
        "mini_hypotheses": len(HYPOTHESES),
        "all_foreign_functions_have_feedback_collisions": all(repeated_feedback.values()),
        "all_mini_rules_injective_on_x_0_to_8": all(
            len({Rule(a, c)(x) for x in range(len(GUESSES))}) == len(GUESSES)
            for a, c in HYPOTHESES
        ),
        "codes_representable_by_mini": sum(bool(v) for v in matching_rules.values()),
        "matching_rules": matching_rules,
    }


@dataclass
class ArmStats:
    worlds: int = 0
    oracle_unique_worlds: int = 0
    oracle_unique_step_sum: int = 0
    mini_ever_committed: int = 0
    mini_final_has_model: int = 0
    mini_final_needs_probe: int = 0
    mini_final_global_model_consistent: int = 0
    mini_reopen_events: int = 0
    mini_commit_events: int = 0
    nano_model_attempts: int = 0
    nano_model_allows: int = 0
    nano_model_denies: int = 0
    nano_model_defers: int = 0
    base_predictions: int = 0
    base_correct: int = 0
    base_wrong: int = 0
    base_abstain: int = 0
    expressive_block_after_sufficient_evidence: int = 0
    authority_check_allows: int = 0
    hidden_secret_changes: int = 0
    worlds_with_hidden_secret_change: int = 0
    dynamic_trace_has_static_explanation: int = 0

    def summary(self) -> dict:
        d = asdict(self)
        d.update(
            {
                "oracle_unique_rate": self.oracle_unique_worlds / max(1, self.worlds),
                "mean_oracle_unique_step": self.oracle_unique_step_sum / max(1, self.oracle_unique_worlds),
                "mini_ever_commit_rate": self.mini_ever_committed / max(1, self.worlds),
                "mini_final_needs_probe_rate": self.mini_final_needs_probe / max(1, self.worlds),
                "mini_final_global_model_consistency_rate": self.mini_final_global_model_consistent / max(1, self.worlds),
                "nano_model_allow_rate": self.nano_model_allows / max(1, self.nano_model_attempts),
                "base_prediction_accuracy": self.base_correct / max(1, self.base_predictions),
                "expressive_block_after_sufficient_evidence_rate": self.expressive_block_after_sufficient_evidence / max(1, self.worlds),
                "authority_check_allow_rate": self.authority_check_allows / max(1, self.worlds),
                "mean_hidden_secret_changes": self.hidden_secret_changes / max(1, self.worlds),
                "worlds_with_hidden_secret_change_rate": self.worlds_with_hidden_secret_change / max(1, self.worlds),
            }
        )
        return d


class StaticMaker:
    def __init__(self, secret: tuple[int, int]):
        self.secret = secret
        self.candidates = set(CODES)
        self.secret_changes = 0

    def respond(self, guess: tuple[int, int]) -> tuple[int, int]:
        fb = score(self.secret, guess)
        self.candidates = candidate_filter(self.candidates, guess, fb)
        return fb

    def hidden_now(self) -> tuple[int, int]:
        return self.secret


class DynamicMaker:
    """Adaptive/dynamic codemaker with a max-survivor response policy.

    The public answers always remain jointly consistent with at least one static code.
    Internally, the representative hidden code is changed whenever possible after a
    response, making the hidden mechanism nonstationary without exposing that change
    through the standard Mastermind feedback interface.
    """

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.candidates = set(CODES)
        self.secret = rng.choice(CODES)
        self.secret_changes = 0

    def respond(self, guess: tuple[int, int]) -> tuple[int, int]:
        parts: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
        for code in self.candidates:
            parts[score(code, guess)].add(code)
        # Maximize surviving ambiguity. Tie-break by feedback tuple for determinism.
        fb, new_candidates = max(parts.items(), key=lambda kv: (len(kv[1]), -kv[0][0], -kv[0][1]))
        old = self.secret
        alternatives = sorted(c for c in new_candidates if c != old)
        if alternatives:
            self.secret = self.rng.choice(alternatives)
        else:
            self.secret = sorted(new_candidates)[0]
        if self.secret != old:
            self.secret_changes += 1
        self.candidates = set(new_candidates)
        return fb

    def hidden_now(self) -> tuple[int, int]:
        return self.secret


def run_world(seed: int, arm: str, verbose: bool = False) -> dict:
    if file_sha(MINI_PATH) != MINI_EXPECTED_SHA256:
        raise RuntimeError("frozen mini.py hash mismatch")
    if file_sha(NANO_PATH) != NANO_EXPECTED_SHA256:
        raise RuntimeError("frozen nano.py hash mismatch")

    rng = random.Random(seed ^ (0x51A71C if arm == "static" else 0xD1A0C0))
    order = list(GUESSES)
    rng.shuffle(order)
    maker = StaticMaker(rng.choice(CODES)) if arm == "static" else DynamicMaker(rng)

    org = Organism()
    source_key = StandingKey("foreign-mastermind", "source-role", "global")
    model_key = StandingKey("foreign-mastermind", "mini-model", "global")
    license_ = License(
        id=f"foreign-model-{arm}-{seed}",
        operation="persist-foreign-mini-model",
        preconditions=(Precondition(source_key, "EXTERNAL_MASTERMIND_FEEDBACK"),),
        allowed_writes=(WriteGrant(model_key, RULE_VALUES),),
    )
    nano = Nano(
        standings=(Standing(source_key, "EXTERNAL_MASTERMIND_FEEDBACK"),),
        licenses=(license_,),
    )

    oracle = set(CODES)
    history: list[tuple[tuple[int, int], tuple[int, int]]] = []
    unique_step: int | None = None
    commitment_versions_seen = 0
    persist_decisions: list[str] = []
    base_predictions = 0
    base_correct = 0
    base_wrong = 0
    base_abstain = 0
    commit_events = 0
    reopen_events = 0

    for step, guess in enumerate(order, start=1):
        x = guess_x(guess)
        # Base-facing prediction reads only the current effective shared MODEL standing.
        model_value = effective_value(nano, model_key)
        if model_value is None:
            base_abstain += 1
            predicted_y = None
        else:
            base_predictions += 1
            predicted_y = parse_rule(model_value)(x)

        fb = maker.respond(guess)
        y = feedback_y(fb)
        if predicted_y is not None:
            if predicted_y == y:
                base_correct += 1
            else:
                base_wrong += 1

        history.append((guess, fb))
        oracle = candidate_filter(oracle, guess, fb)
        if unique_step is None and len(oracle) == 1:
            unique_step = step

        before_versions = len(org.lineage.get("MM", []))
        org.observe("MM", x, y, f"foreign-{arm}-feedback")
        after_versions = len(org.lineage.get("MM", []))
        if after_versions > before_versions:
            new_commit = org.lineage["MM"][-1]
            commit_events += 1
            if new_commit.reason == "counterevidence":
                reopen_events += 1
            transition = Transition(
                "persist-foreign-mini-model",
                writes=(Standing(model_key, new_commit.rule.short()),),
            )
            receipt = nano.apply_transition(transition, license_.id)
            persist_decisions.append(receipt.decision.value)
            commitment_versions_seen = after_versions

    # Explicit authority control: irrespective of whether Mini happened to emit a
    # commitment, the existing foreign-model contract remains executable now.
    authority_control = Transition(
        "persist-foreign-mini-model",
        writes=(Standing(model_key, RULE_VALUES[0]),),
    )
    authority_check = nano.check_transition(authority_control, license_.id).decision

    # The public history is tested against all static codes, independently of arm internals.
    static_explanations = {
        code for code in CODES if all(score(code, guess) == fb for guess, fb in history)
    }
    assert static_explanations == oracle

    final = org.active.get("MM")
    if final is None:
        global_consistent = False
    else:
        global_consistent = all(
            final.rule(guess_x(guess)) == feedback_y(fb) for guess, fb in history
        )

    # Expressive blockage requires all three conditions:
    # (1) evidence identifies one foreign-task secret under the task semantics;
    # (2) the persistence path accepted every actual Mini model proposal;
    # (3) Mini still lacks a model consistent with the observed foreign relation.
    authority_live = (
        all(d == Decision.ALLOW.value for d in persist_decisions)
        and authority_check is Decision.ALLOW
    )
    expressive_block = len(oracle) == 1 and authority_live and not global_consistent

    result = {
        "seed": seed,
        "arm": arm,
        "probe_order": [list(g) for g in order],
        "history": [{"guess": list(g), "feedback": list(fb)} for g, fb in history],
        "oracle_final_candidates": [list(c) for c in sorted(oracle)],
        "oracle_unique_step": unique_step,
        "mini_commit_events": commit_events,
        "mini_reopen_events": reopen_events,
        "mini_final_has_model": final is not None,
        "mini_final_needs_probe": org.needs_probe("MM"),
        "mini_final_rule": None if final is None else final.rule.short(),
        "mini_final_global_model_consistent": global_consistent,
        "nano_model_persist_decisions": persist_decisions,
        "base_predictions": base_predictions,
        "base_correct": base_correct,
        "base_wrong": base_wrong,
        "base_abstain": base_abstain,
        "authority_check": authority_check.value,
        "hidden_secret_changes": maker.secret_changes,
        "dynamic_trace_has_static_explanation": len(static_explanations) > 0,
        "static_explanations": [list(c) for c in sorted(static_explanations)],
        "expressive_block_after_sufficient_evidence": expressive_block,
        "trace": org.trace,
    }
    if verbose:
        print(json.dumps(result, indent=2, sort_keys=True))
    return result


def sweep(n: int, start_seed: int = 0) -> dict:
    proof = representability_proof()
    arms = {"static": ArmStats(), "dynamic": ArmStats()}
    first: dict[str, dict] = {}
    for arm in arms:
        stats = arms[arm]
        for seed in range(start_seed, start_seed + n):
            r = run_world(seed, arm)
            if arm not in first:
                first[arm] = r
            stats.worlds += 1
            if r["oracle_unique_step"] is not None:
                stats.oracle_unique_worlds += 1
                stats.oracle_unique_step_sum += r["oracle_unique_step"]
            stats.mini_ever_committed += int(r["mini_commit_events"] > 0)
            stats.mini_final_has_model += int(r["mini_final_has_model"])
            stats.mini_final_needs_probe += int(r["mini_final_needs_probe"])
            stats.mini_final_global_model_consistent += int(r["mini_final_global_model_consistent"])
            stats.mini_reopen_events += r["mini_reopen_events"]
            stats.mini_commit_events += r["mini_commit_events"]
            decisions = r["nano_model_persist_decisions"]
            stats.nano_model_attempts += len(decisions)
            stats.nano_model_allows += sum(d == Decision.ALLOW.value for d in decisions)
            stats.nano_model_denies += sum(d == Decision.DENY.value for d in decisions)
            stats.nano_model_defers += sum(d == Decision.DEFER.value for d in decisions)
            stats.base_predictions += r["base_predictions"]
            stats.base_correct += r["base_correct"]
            stats.base_wrong += r["base_wrong"]
            stats.base_abstain += r["base_abstain"]
            stats.expressive_block_after_sufficient_evidence += int(r["expressive_block_after_sufficient_evidence"])
            stats.authority_check_allows += int(r["authority_check"] == Decision.ALLOW.value)
            stats.hidden_secret_changes += r["hidden_secret_changes"]
            stats.worlds_with_hidden_secret_change += int(r["hidden_secret_changes"] > 0)
            stats.dynamic_trace_has_static_explanation += int(r["dynamic_trace_has_static_explanation"])

    out = {
        "experiment": "FOREIGN-001 Mastermind pressure",
        "worlds_per_arm": n,
        "start_seed": start_seed,
        "foreign_task": {
            "positions": POSITIONS,
            "colors": COLORS,
            "codes": len(CODES),
            "guesses": len(GUESSES),
            "feedback_classes": [list(x) for x in FEEDBACKS],
            "adapter": "lossless guess index x=0..8; injective feedback class y=0..4",
        },
        "frozen": {
            "mini_sha256": file_sha(MINI_PATH),
            "nano_sha256": file_sha(NANO_PATH),
        },
        "representability": proof,
        "arms": {arm: stats.summary() for arm, stats in arms.items()},
        "classification": {
            "static": "EXPRESSIVE_BLOCK if oracle uniquely identifies foreign secret and Nano authority path is live while Mini has no globally consistent affine model",
            "dynamic": "same expressive block plus hidden mechanism non-identifiability: adaptive history remains exactly explainable by at least one static code",
        },
        "first_worlds": first,
    }
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--arm", choices=("static", "dynamic"), default="static")
    p.add_argument("--sweep", type=int, default=0)
    p.add_argument("--json-out", type=Path)
    args = p.parse_args()
    if args.sweep:
        result = sweep(args.sweep, args.seed)
    else:
        result = run_world(args.seed, args.arm, verbose=False)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
