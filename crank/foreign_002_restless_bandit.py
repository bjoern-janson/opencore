#!/usr/bin/env python3
"""FOREIGN-002: frozen OpenCore stack under restless-bandit pressure.

Foreign task
------------
A finite deterministic instance of a restless multi-armed bandit (RMAB): eight
arms evolve independently even when they are not selected, but only one arm can
be played/observed per round.  The finite horizon is 80 rounds.

Each arm's latent state is deliberately chosen from frozen Mini's *existing*
affine Z_11 hypothesis family.  This controls the expressive wound found by
FOREIGN-001 without changing Mini: every current arm state is exactly
representable by Mini if the relevant observations are acquired.

Pressure question
-----------------
With representation controlled and Nano authority available, where does scarce
attention go?  Does Mini's existing contradiction-triggered `needs_probe` signal
behave like a general challenge-allocation policy, or only as local repair after
corrective evidence has already arrived?

Policies (harness controls, not architectural additions)
---------------------------------------------------------
  greedy         -- highest Base-predicted immediate reward
  mini_reactive  -- honor Mini `needs_probe` first; otherwise greedy
  epsilon        -- 10% random exploration; otherwise greedy
  round_robin    -- uniform coverage control
  oracle         -- true best arm each round (reward ceiling only)

No Mini, Nano, or Base repair is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from mini import HYPOTHESES, MOD, Organism, Rule
from nano import Decision, License, Nano, Precondition, Standing, StandingKey, Transition, WriteGrant

HERE = Path(__file__).resolve().parent
MINI_PATH = HERE / "mini.py"
NANO_PATH = HERE / "nano.py"
MINI_EXPECTED_SHA256 = "fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55"
NANO_EXPECTED_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"

N_ARMS = 8
HORIZON = 80
SHIFT_HAZARD = 0.05
EPSILON = 0.10
SEVERE_BEST_ROUNDS = N_ARMS  # at least one full round-robin cycle as oracle-best

RULES = tuple(Rule(a, c) for a, c in HYPOTHESES)
RULE_TO_INDEX = {r: i for i, r in enumerate(RULES)}
RULE_VALUES = tuple(r.short() for r in RULES)
POLICIES = ("greedy", "mini_reactive", "epsilon", "round_robin")
POLICY_SEED_XOR = {
    "greedy": 0xA11CE001,
    "mini_reactive": 0xA11CE002,
    "epsilon": 0xA11CE003,
    "round_robin": 0xA11CE004,
}


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_rule(value: str) -> Rule:
    left = value.split(" mod ", 1)[0]
    a_s, c_s = left.split("x+", 1)
    return Rule(int(a_s), int(c_s))


def choose_other_rule(rng: random.Random, old: Rule) -> Rule:
    old_i = RULE_TO_INDEX[old]
    j = rng.randrange(len(RULES) - 1)
    if j >= old_i:
        j += 1
    return RULES[j]


@dataclass(frozen=True)
class ShiftEvent:
    idx: int
    t: int
    arm: int
    old: Rule
    new: Rule
    end: int
    best_rounds: int

    @property
    def severe(self) -> bool:
        return self.best_rounds >= SEVERE_BEST_ROUNDS


@dataclass(frozen=True)
class Environment:
    initial_rules: tuple[Rule, ...]
    states: tuple[tuple[Rule, ...], ...]
    shifts: tuple[ShiftEvent, ...]
    oracle_reward: int


def build_environment(seed: int) -> Environment:
    rng = random.Random(seed ^ 0xF002BADD)
    initial = tuple(rng.sample(RULES, N_ARMS))
    current = list(initial)
    raw_shifts: list[tuple[int, int, Rule, Rule]] = []
    states: list[tuple[Rule, ...]] = []

    for t in range(HORIZON):
        for arm in range(N_ARMS):
            if rng.random() < SHIFT_HAZARD:
                old = current[arm]
                new = choose_other_rule(rng, old)
                current[arm] = new
                raw_shifts.append((t, arm, old, new))
        states.append(tuple(current))

    # Score how consequential each exogenous shift is without reference to any policy:
    # number of rounds before that arm's next shift on which it is oracle-best.
    by_arm: dict[int, list[int]] = {i: [] for i in range(N_ARMS)}
    for idx, (_, arm, _, _) in enumerate(raw_shifts):
        by_arm[arm].append(idx)

    events: list[ShiftEvent | None] = [None] * len(raw_shifts)
    for arm, idxs in by_arm.items():
        for j, idx in enumerate(idxs):
            t, _, old, new = raw_shifts[idx]
            end = raw_shifts[idxs[j + 1]][0] if j + 1 < len(idxs) else HORIZON
            best_rounds = 0
            for s in range(t, end):
                x = s % MOD
                vals = [states[s][k](x) for k in range(N_ARMS)]
                if states[s][arm](x) == max(vals):
                    best_rounds += 1
            events[idx] = ShiftEvent(idx, t, arm, old, new, end, best_rounds)

    oracle_reward = 0
    for t, rules in enumerate(states):
        x = t % MOD
        oracle_reward += max(rule(x) for rule in rules)

    return Environment(initial, tuple(states), tuple(e for e in events if e is not None), oracle_reward)


@dataclass
class PolicyStats:
    worlds: int = 0
    reward: int = 0
    oracle_reward: int = 0
    regret: int = 0
    true_best_pulls: int = 0
    total_pulls: int = 0
    shifts: int = 0
    severe_shifts: int = 0
    detected_shifts: int = 0
    detected_severe_shifts: int = 0
    repaired_shifts: int = 0
    repaired_severe_shifts: int = 0
    detection_delay_sum: int = 0
    detection_delay_count: int = 0
    reactive_probe_pulls: int = 0
    reactive_probe_predicted_sacrifice_pulls: int = 0
    reactive_probe_predicted_opportunity_cost: int = 0
    reactive_probe_actual_opportunity_cost: int = 0
    contradictions: int = 0
    reopens: int = 0
    stale_arm_rounds: int = 0
    stale_oracle_best_arm_rounds: int = 0
    final_fresh_arms: int = 0
    nano_model_attempts: int = 0
    nano_allows: int = 0
    nano_denies: int = 0
    nano_defers: int = 0

    def add(self, row: dict) -> None:
        self.worlds += 1
        for k in (
            "reward", "oracle_reward", "regret", "true_best_pulls", "total_pulls",
            "shifts", "severe_shifts", "detected_shifts", "detected_severe_shifts",
            "repaired_shifts", "repaired_severe_shifts", "detection_delay_sum",
            "detection_delay_count", "reactive_probe_pulls",
            "reactive_probe_predicted_sacrifice_pulls",
            "reactive_probe_predicted_opportunity_cost",
            "reactive_probe_actual_opportunity_cost", "contradictions", "reopens",
            "stale_arm_rounds", "stale_oracle_best_arm_rounds", "final_fresh_arms",
            "nano_model_attempts", "nano_allows", "nano_denies", "nano_defers",
        ):
            setattr(self, k, getattr(self, k) + row[k])

    def summary(self) -> dict:
        w = max(1, self.worlds)
        pulls = max(1, self.total_pulls)
        det = max(1, self.detected_shifts)
        sev = max(1, self.severe_shifts)
        rp = max(1, self.reactive_probe_pulls)
        attempts = max(1, self.nano_model_attempts)
        return {
            **asdict(self),
            "mean_reward_per_world": self.reward / w,
            "mean_oracle_reward_per_world": self.oracle_reward / w,
            "mean_regret_per_world": self.regret / w,
            "true_best_pull_rate": self.true_best_pulls / pulls,
            "shift_detection_rate": self.detected_shifts / max(1, self.shifts),
            "severe_shift_detection_rate": self.detected_severe_shifts / sev,
            "detected_to_repaired_rate": self.repaired_shifts / det,
            "severe_shift_repair_rate": self.repaired_severe_shifts / sev,
            "mean_detection_delay": self.detection_delay_sum / max(1, self.detection_delay_count),
            "mean_reactive_probe_pulls_per_world": self.reactive_probe_pulls / w,
            "reactive_probe_predicted_sacrifice_rate": self.reactive_probe_predicted_sacrifice_pulls / rp,
            "mean_predicted_probe_opportunity_cost": self.reactive_probe_predicted_opportunity_cost / rp,
            "mean_actual_probe_opportunity_cost": self.reactive_probe_actual_opportunity_cost / rp,
            "mean_stale_arm_rounds_per_world": self.stale_arm_rounds / w,
            "mean_stale_oracle_best_arm_rounds_per_world": self.stale_oracle_best_arm_rounds / w,
            "mean_final_fresh_arms": self.final_fresh_arms / w,
            "nano_allow_rate": self.nano_allows / attempts,
        }


class FrozenStack:
    def __init__(self, initial_rules: tuple[Rule, ...], seed: int, policy: str):
        self.org = Organism()
        source_key = StandingKey(f"foreign-002-{seed}-{policy}", "source-role", "global")
        standings = [Standing(source_key, "RESTLESS_BANDIT_REWARD")]
        self.model_keys: list[StandingKey] = []
        self.licenses: list[License] = []
        for arm in range(N_ARMS):
            key = StandingKey(f"foreign-002-arm-{arm}", "mini-model", policy)
            self.model_keys.append(key)
            self.licenses.append(
                License(
                    id=f"foreign-002-{policy}-{seed}-{arm}",
                    operation="persist-foreign-002-model",
                    preconditions=(Precondition(source_key, "RESTLESS_BANDIT_REWARD"),),
                    allowed_writes=(WriteGrant(key, RULE_VALUES),),
                )
            )
        self.nano = Nano(standings=standings, licenses=self.licenses)
        self.base_rules: list[Rule | None] = [None] * N_ARMS
        self.nano_counts = {Decision.ALLOW.value: 0, Decision.DENY.value: 0, Decision.DEFER.value: 0}

        # Unscored common bootstrap: two distinct observations per arm establish the
        # initial representable state before scarce-attention pressure begins.
        for arm, rule in enumerate(initial_rules):
            scope = f"A{arm}"
            self.org.observe(scope, 9, rule(9), "foreign-002-bootstrap")
            self.org.observe(scope, 10, rule(10), "foreign-002-bootstrap")
            assert self.org.active[scope].rule == rule
            self._persist(arm, rule)

    def _persist(self, arm: int, rule: Rule) -> None:
        receipt = self.nano.apply_transition(
            Transition(
                "persist-foreign-002-model",
                writes=(Standing(self.model_keys[arm], rule.short()),),
            ),
            self.licenses[arm].id,
        )
        self.nano_counts[receipt.decision.value] += 1
        if receipt.decision is Decision.ALLOW:
            # No revocation path exists in this assay; the cache is exactly the current
            # effective Base-facing model after each successful Nano write.
            self.base_rules[arm] = rule

    def observe(self, arm: int, x: int, y: int) -> str | None:
        scope = f"A{arm}"
        before = len(self.org.lineage.get(scope, []))
        self.org.observe(scope, x, y, "foreign-002-restless-pull")
        after = len(self.org.lineage.get(scope, []))
        if after > before:
            commit = self.org.lineage[scope][-1]
            self._persist(arm, commit.rule)
            return commit.reason
        return None


def choose_arm(policy: str, stack: FrozenStack, t: int, rng: random.Random) -> tuple[int, str, list[int]]:
    x = t % MOD
    preds = [rule(x) for rule in stack.base_rules if rule is not None]
    assert len(preds) == N_ARMS

    if policy == "round_robin":
        return t % N_ARMS, "coverage", preds

    if policy == "epsilon" and rng.random() < EPSILON:
        return rng.randrange(N_ARMS), "explore", preds

    if policy == "mini_reactive":
        pending = [arm for arm in range(N_ARMS) if stack.org.needs_probe(f"A{arm}")]
        if pending:
            # Mini exposes only a binary per-scope request, not a consequence ranking.
            # Oldest request is a deterministic transport tie-break, not cognition.
            def first_obs_id(arm: int) -> int:
                return stack.org.challenge_buffers[f"A{arm}"][0]
            return min(pending, key=lambda arm: (first_obs_id(arm), arm)), "reactive_probe", preds

    arm = max(range(N_ARMS), key=lambda i: (preds[i], -i))
    return arm, "greedy", preds


def run_policy(seed: int, env: Environment, policy: str) -> dict:
    stack = FrozenStack(env.initial_rules, seed, policy)
    rng = random.Random(seed ^ POLICY_SEED_XOR[policy])

    events_by_t: dict[int, list[ShiftEvent]] = {}
    for event in env.shifts:
        events_by_t.setdefault(event.t, []).append(event)
    active_event: list[int | None] = [None] * N_ARMS
    event_by_idx = {e.idx: e for e in env.shifts}
    detected_at: dict[int, int] = {}
    repaired_at: dict[int, int] = {}

    reward = regret = true_best = 0
    contradictions = reopens = 0
    reactive_probe_pulls = 0
    probe_sacrifice = 0
    probe_pred_cost = 0
    probe_actual_cost = 0
    stale_arm_rounds = 0
    stale_best_rounds = 0

    for t, true_rules in enumerate(env.states):
        for event in events_by_t.get(t, ()):
            active_event[event.arm] = event.idx

        x = t % MOD
        actual = [true_rules[i](x) for i in range(N_ARMS)]
        actual_best = max(actual)
        stale = [stack.org.active[f"A{i}"].rule != true_rules[i] for i in range(N_ARMS)]
        stale_arm_rounds += sum(stale)
        stale_best_rounds += sum(1 for i in range(N_ARMS) if stale[i] and actual[i] == actual_best)

        arm, kind, preds = choose_arm(policy, stack, t, rng)
        reward += actual[arm]
        regret += actual_best - actual[arm]
        true_best += int(actual[arm] == actual_best)

        if kind == "reactive_probe":
            reactive_probe_pulls += 1
            pred_best = max(preds)
            if preds[arm] < pred_best:
                probe_sacrifice += 1
            probe_pred_cost += pred_best - preds[arm]
            probe_actual_cost += actual_best - actual[arm]

        predicted = stack.org.answer(f"A{arm}", x)
        assert predicted is not None
        if predicted != actual[arm]:
            contradictions += 1
            ev = active_event[arm]
            if ev is not None and ev not in detected_at:
                detected_at[ev] = t

        reason = stack.observe(arm, x, actual[arm])
        if reason == "counterevidence":
            reopens += 1
            ev = active_event[arm]
            if ev is not None and ev not in repaired_at:
                # Count only if the resulting Mini rule actually matches the current
                # latent arm state; a coincidental reopen is not a repair witness.
                if stack.org.active[f"A{arm}"].rule == true_rules[arm]:
                    repaired_at[ev] = t

    detected = 0
    detected_severe = 0
    repaired = 0
    repaired_severe = 0
    delay_sum = delay_count = 0
    for event in env.shifts:
        dt = detected_at.get(event.idx)
        if dt is not None and dt < event.end:
            detected += 1
            delay_sum += dt - event.t
            delay_count += 1
            if event.severe:
                detected_severe += 1
        rt = repaired_at.get(event.idx)
        if rt is not None and rt < event.end:
            repaired += 1
            if event.severe:
                repaired_severe += 1

    final_rules = env.states[-1]
    final_fresh = sum(stack.org.active[f"A{i}"].rule == final_rules[i] for i in range(N_ARMS))
    severe = sum(e.severe for e in env.shifts)
    attempts = sum(stack.nano_counts.values())

    return {
        "reward": reward,
        "oracle_reward": env.oracle_reward,
        "regret": regret,
        "true_best_pulls": true_best,
        "total_pulls": HORIZON,
        "shifts": len(env.shifts),
        "severe_shifts": severe,
        "detected_shifts": detected,
        "detected_severe_shifts": detected_severe,
        "repaired_shifts": repaired,
        "repaired_severe_shifts": repaired_severe,
        "detection_delay_sum": delay_sum,
        "detection_delay_count": delay_count,
        "reactive_probe_pulls": reactive_probe_pulls,
        "reactive_probe_predicted_sacrifice_pulls": probe_sacrifice,
        "reactive_probe_predicted_opportunity_cost": probe_pred_cost,
        "reactive_probe_actual_opportunity_cost": probe_actual_cost,
        "contradictions": contradictions,
        "reopens": reopens,
        "stale_arm_rounds": stale_arm_rounds,
        "stale_oracle_best_arm_rounds": stale_best_rounds,
        "final_fresh_arms": final_fresh,
        "nano_model_attempts": attempts,
        "nano_allows": stack.nano_counts[Decision.ALLOW.value],
        "nano_denies": stack.nano_counts[Decision.DENY.value],
        "nano_defers": stack.nano_counts[Decision.DEFER.value],
    }


def run_world(seed: int) -> dict:
    if file_sha(MINI_PATH) != MINI_EXPECTED_SHA256:
        raise RuntimeError("frozen mini.py hash mismatch")
    if file_sha(NANO_PATH) != NANO_EXPECTED_SHA256:
        raise RuntimeError("frozen nano.py hash mismatch")

    env = build_environment(seed)
    rows = {p: run_policy(seed, env, p) for p in POLICIES}
    return {
        "seed": seed,
        "environment": {
            "shifts": len(env.shifts),
            "severe_shifts": sum(e.severe for e in env.shifts),
            "oracle_reward": env.oracle_reward,
        },
        "policies": rows,
    }


def aggregate_worlds(rows: Iterable[dict]) -> dict:
    stats = {p: PolicyStats() for p in POLICIES}
    env_worlds = env_shifts = env_severe = 0
    first = None
    for row in rows:
        if first is None:
            first = row
        env_worlds += 1
        env_shifts += row["environment"]["shifts"]
        env_severe += row["environment"]["severe_shifts"]
        for p in POLICIES:
            stats[p].add(row["policies"][p])
    return {
        "worlds": env_worlds,
        "environment": {
            "total_shifts": env_shifts,
            "total_severe_shifts": env_severe,
            "mean_shifts_per_world": env_shifts / max(1, env_worlds),
            "severe_shift_rate": env_severe / max(1, env_shifts),
        },
        "policies": {p: stats[p].summary() for p in POLICIES},
        "first_world": first,
    }


def merge_aggregates(payloads: Iterable[dict]) -> dict:
    # Merge raw additive PolicyStats fields from chunk payloads.
    payloads = list(payloads)
    merged_stats = {p: PolicyStats() for p in POLICIES}
    worlds = shifts = severe = 0
    first = None
    field_names = tuple(PolicyStats.__dataclass_fields__)
    for payload in payloads:
        a = payload["aggregate"]
        worlds += a["worlds"]
        shifts += a["environment"]["total_shifts"]
        severe += a["environment"]["total_severe_shifts"]
        if first is None:
            first = a.get("first_world")
        for p in POLICIES:
            src = a["policies"][p]
            dst = merged_stats[p]
            for k in field_names:
                setattr(dst, k, getattr(dst, k) + int(src[k]))
    return {
        "worlds": worlds,
        "environment": {
            "total_shifts": shifts,
            "total_severe_shifts": severe,
            "mean_shifts_per_world": shifts / max(1, worlds),
            "severe_shift_rate": severe / max(1, shifts),
        },
        "policies": {p: merged_stats[p].summary() for p in POLICIES},
        "first_world": first,
    }


def payload_for(start_seed: int, n: int) -> dict:
    rows = [run_world(seed) for seed in range(start_seed, start_seed + n)]
    agg = aggregate_worlds(rows)
    return {
        "object": "OPENCORE_FOREIGN_002_RESTLESS_BANDIT",
        "status": "FOREIGN_PRESSURE_ASSAY",
        "construction": {
            "task_family": "restless multi-armed bandit",
            "n_arms": N_ARMS,
            "horizon": HORIZON,
            "one_observable_pull_per_round": True,
            "shift_hazard_per_arm_per_round": SHIFT_HAZARD,
            "epsilon_control": EPSILON,
            "severe_shift_definition": f"shifted arm is oracle-best for >= {SEVERE_BEST_ROUNDS} rounds before its next shift/end",
            "all_latent_arm_states_in_frozen_mini_hypothesis_class": True,
            "mini_modified": False,
            "nano_modified": False,
            "base_role": "Nano-effective per-arm Mini models are the shared prediction surface",
        },
        "component_hashes": {
            "mini.py": file_sha(MINI_PATH),
            "nano.py": file_sha(NANO_PATH),
        },
        "seed_range": [start_seed, start_seed + n - 1],
        "aggregate": agg,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sweep", type=int, default=0)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--merge", type=Path, nargs="*")
    ap.add_argument("--output-json", type=Path)
    args = ap.parse_args()

    if args.merge is not None and len(args.merge) > 0:
        payloads = [json.loads(p.read_text(encoding="utf-8")) for p in args.merge]
        out = {
            "object": "OPENCORE_FOREIGN_002_RESTLESS_BANDIT",
            "status": "FOREIGN_PRESSURE_ASSAY",
            "construction": payloads[0]["construction"],
            "component_hashes": payloads[0]["component_hashes"],
            "seed_range": [min(p["seed_range"][0] for p in payloads), max(p["seed_range"][1] for p in payloads)],
            "aggregate": merge_aggregates(payloads),
        }
    elif args.sweep:
        out = payload_for(args.start_seed, args.sweep)
    else:
        out = run_world(args.seed)

    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        args.output_json.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
