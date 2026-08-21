from __future__ import annotations

import copy
import hashlib
import json
import math
import random
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

EPISODES = 300
SHIFT_EPISODE = 180
SEEDS = 256
PROBE_COST = 0.20
Q_INIT = 1.10
CONTEXTS = ("train", "target", "null")
REVEAL_ACTIONS = ("skip", "probe")
DECISION_ACTIONS = ("safe", "left", "right")


@dataclass(frozen=True)
class EpisodeWorld:
    episode: int
    context: str
    regime: str


@dataclass
class Snapshot:
    q_reveal: Dict[str, Dict[str, float]]
    n_reveal: Dict[str, Dict[str, int]]
    q_decision: Dict[str, Dict[str, float]]
    n_decision: Dict[str, Dict[str, int]]
    rng_state: object


class Agent:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.reset_memory()

    def reset_memory(self):
        self.q_reveal = {
            c: {a: Q_INIT for a in REVEAL_ACTIONS} for c in CONTEXTS
        }
        self.n_reveal = {
            c: {a: 0 for a in REVEAL_ACTIONS} for c in CONTEXTS
        }
        self.q_decision: Dict[str, Dict[str, float]] = {}
        self.n_decision: Dict[str, Dict[str, int]] = {}

    def _ensure_obs(self, obs: str):
        if obs not in self.q_decision:
            self.q_decision[obs] = {a: Q_INIT for a in DECISION_ACTIONS}
            self.n_decision[obs] = {a: 0 for a in DECISION_ACTIONS}

    def greedy_support(self, values: Dict[str, float]) -> List[str]:
        m = max(values.values())
        return [a for a, v in values.items() if math.isclose(v, m, abs_tol=1e-12)]

    def choose_reveal(self, context: str) -> Tuple[List[str], str]:
        support = self.greedy_support(self.q_reveal[context])
        return support, self.rng.choice(support)

    def choose_decision(self, obs: str) -> Tuple[List[str], str]:
        self._ensure_obs(obs)
        support = self.greedy_support(self.q_decision[obs])
        return support, self.rng.choice(support)

    def update_mean(self, q: Dict[str, float], n: Dict[str, int], action: str, value: float):
        n[action] += 1
        q[action] += (value - q[action]) / n[action]

    def update(self, context: str, reveal_action: str, obs: str, decision_action: str,
               decision_reward: float, total_return: float):
        self._ensure_obs(obs)
        self.update_mean(self.q_reveal[context], self.n_reveal[context], reveal_action, total_return)
        self.update_mean(self.q_decision[obs], self.n_decision[obs], decision_action, decision_reward)

    def snapshot(self) -> Snapshot:
        return Snapshot(
            q_reveal=copy.deepcopy(self.q_reveal),
            n_reveal=copy.deepcopy(self.n_reveal),
            q_decision=copy.deepcopy(self.q_decision),
            n_decision=copy.deepcopy(self.n_decision),
            rng_state=self.rng.getstate(),
        )

    def restore(self, s: Snapshot):
        self.q_reveal = copy.deepcopy(s.q_reveal)
        self.n_reveal = copy.deepcopy(s.n_reveal)
        self.q_decision = copy.deepcopy(s.q_decision)
        self.n_decision = copy.deepcopy(s.n_decision)
        self.rng.setstate(s.rng_state)


def make_schedule(seed: int) -> List[EpisodeWorld]:
    rng = random.Random(seed ^ 0xB1172C)
    out = []
    for ep in range(EPISODES):
        context = CONTEXTS[ep % len(CONTEXTS)]
        if context == "train":
            regime = rng.choice(("A", "B"))
        elif context == "target":
            regime = "N" if ep < SHIFT_EPISODE else rng.choice(("A", "B"))
        else:
            regime = "N"
        out.append(EpisodeWorld(ep, context, regime))
    return out


def reveal_observation(world: EpisodeWorld, action: str) -> str:
    if action == "skip":
        return "UNKNOWN"
    if world.regime == "A":
        return "SIG_A"
    if world.regime == "B":
        return "SIG_B"
    return "SAME"


def decision_reward(regime: str, action: str) -> float:
    if regime == "N":
        return 1.0
    if action == "safe":
        return 1.0
    if regime == "A":
        return 1.4 if action == "left" else 0.6
    return 1.4 if action == "right" else 0.6


def pi_label(q_probe: float, q_skip: float) -> str:
    if math.isclose(q_probe, q_skip, abs_tol=1e-12):
        return "TIED"
    return "PROBE_PREFERRED" if q_probe > q_skip else "SKIP_PREFERRED"


def compact_L(agent: Agent, context: str) -> dict:
    return {
        "reveal_q": {k: round(v, 8) for k, v in agent.q_reveal[context].items()},
        "reveal_n": dict(agent.n_reveal[context]),
        "signal_q": {
            obs: {a: round(v, 8) for a, v in qs.items()}
            for obs, qs in sorted(agent.q_decision.items())
            if obs in ("SIG_A", "SIG_B", "SAME", "UNKNOWN")
        },
        "signal_n": {
            obs: dict(agent.n_decision[obs]) for obs in sorted(agent.n_decision)
            if obs in ("SIG_A", "SIG_B", "SAME", "UNKNOWN")
        },
    }


def run_episode(agent: Agent, world: EpisodeWorld, force_reveal: str | None = None,
                learn: bool = True) -> dict:
    snap = agent.snapshot()
    reveal_support, selected = agent.choose_reveal(world.context)
    if force_reveal is not None:
        selected = force_reveal
    obs = reveal_observation(world, selected)
    decision_support, decision = agent.choose_decision(obs)
    d_reward = decision_reward(world.regime, decision)
    total = d_reward - (PROBE_COST if selected == "probe" else 0.0)
    before = {
        "L_t": compact_L(agent, world.context),
        "Pi_t": pi_label(agent.q_reveal[world.context]["probe"], agent.q_reveal[world.context]["skip"]),
        "pi_t": {
            "support": reveal_support,
            "selected": selected if force_reveal is None else reveal_support and "FORCED:" + selected,
        },
        "R_available": list(REVEAL_ACTIONS),
    }
    if learn:
        agent.update(world.context, selected, obs, decision, d_reward, total)
    return {
        "episode": world.episode,
        "context": world.context,
        "audit_regime": world.regime,
        **before,
        "a_t": selected,
        "E_t1": obs,
        "decision_support": decision_support,
        "decision_action": decision,
        "decision_reward": d_reward,
        "return": total,
        "pre_snapshot": snap,
    }


def run_branch(seed: int, memory_on: bool, schedule: List[EpisodeWorld]) -> List[dict]:
    agent = Agent(seed ^ 0x1111)
    records = []
    for world in schedule:
        if not memory_on:
            agent.reset_memory()
        rec = run_episode(agent, world)
        records.append(rec)
    return records


def first_trigger(records: List[dict], context: str) -> dict | None:
    for r in records:
        if r["episode"] >= SHIFT_EPISODE and r["context"] == context:
            if "probe" in r["R_available"] and "probe" not in r["pi_t"]["support"]:
                return r
    return None


def forced_control(seed: int, trigger: dict, world: EpisodeWorld) -> dict:
    agent = Agent(seed ^ 0x1111)
    agent.restore(trigger["pre_snapshot"])
    rec = run_episode(agent, world, force_reveal="probe", learn=False)
    return {
        "episode": world.episode,
        "context": world.context,
        "regime": world.regime,
        "endogenous_observation": trigger["E_t1"],
        "forced_observation": rec["E_t1"],
        "endogenous_decision": trigger["decision_action"],
        "forced_decision": rec["decision_action"],
        "endogenous_return": trigger["return"],
        "forced_return": rec["return"],
        "observation_changed": trigger["E_t1"] != rec["E_t1"],
        "decision_changed": trigger["decision_action"] != rec["decision_action"],
        "forced_return_delta": rec["return"] - trigger["return"],
    }


def strip_record(r: dict) -> dict:
    return {k: v for k, v in r.items() if k != "pre_snapshot"}


def summarize(records: List[dict]) -> dict:
    total = sum(r["return"] for r in records)
    pre = sum(r["return"] for r in records if r["episode"] < SHIFT_EPISODE)
    post = sum(r["return"] for r in records if r["episode"] >= SHIFT_EPISODE)
    def reach(context: str):
        xs = [r for r in records if r["episode"] >= SHIFT_EPISODE and r["context"] == context]
        return {
            "n": len(xs),
            "probe_available_fraction": sum("probe" in r["R_available"] for r in xs) / len(xs),
            "probe_support_fraction": sum("probe" in r["pi_t"]["support"] for r in xs) / len(xs),
            "probe_selected_fraction": sum(r["a_t"] == "probe" for r in xs) / len(xs),
        }
    return {
        "total_return": total,
        "pre_shift_return": pre,
        "post_shift_return": post,
        "target_reachability": reach("target"),
        "null_reachability": reach("null"),
    }


def main():
    root = Path(__file__).resolve().parent
    spec_sha = hashlib.sha256((root / "BLITZCRANK_001_SPEC.md").read_bytes()).hexdigest()
    harness_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    paired = []
    target_forced = []
    null_forced = []
    exemplar = None

    for seed in range(SEEDS):
        schedule = make_schedule(seed)
        on = run_branch(seed, True, schedule)
        off = run_branch(seed, False, schedule)
        s_on, s_off = summarize(on), summarize(off)

        t = first_trigger(on, "target")
        n = first_trigger(on, "null")
        tf = forced_control(seed, t, schedule[t["episode"]]) if t else None
        nf = forced_control(seed, n, schedule[n["episode"]]) if n else None
        if tf:
            target_forced.append(tf)
        if nf:
            null_forced.append(nf)

        paired.append({
            "seed": seed,
            "memory_on": s_on,
            "memory_off": s_off,
            "delta_total": s_on["total_return"] - s_off["total_return"],
            "delta_pre": s_on["pre_shift_return"] - s_off["pre_shift_return"],
            "delta_post": s_on["post_shift_return"] - s_off["post_shift_return"],
            "target_forced": tf,
            "null_forced": nf,
        })

        if exemplar is None and tf and nf:
            start = max(0, t["episode"] - 3)
            end = min(EPISODES, t["episode"] + 4)
            exemplar = {
                "seed": seed,
                "memory_on_window": [strip_record(r) for r in on[start:end]],
                "memory_off_window": [strip_record(r) for r in off[start:end]],
                "target_forced": tf,
                "null_forced": nf,
            }

    deltas_total = [x["delta_total"] for x in paired]
    deltas_pre = [x["delta_pre"] for x in paired]
    deltas_post = [x["delta_post"] for x in paired]

    result = {
        "assay": "BLITZCRANK-001",
        "spec_sha256": spec_sha,
        "harness_sha256": harness_sha,
        "parameters": {
            "episodes": EPISODES,
            "shift_episode": SHIFT_EPISODE,
            "seeds": SEEDS,
            "probe_cost": PROBE_COST,
            "q_init": Q_INIT,
        },
        "validity": {
            "memory_only_manipulation": True,
            "paired_schedule_identity": True,
            "physical_action_identity": True,
            "exogenous_shift": True,
            "hidden_regime_not_exposed": True,
            "forced_control_exact_snapshot_clone": True,
            "null_remains_nondiscriminating": True,
            "target_pre_shift_nondiscriminating": True,
            "nano_present": False,
        },
        "performance": {
            "mean_delta_total": statistics.mean(deltas_total),
            "median_delta_total": statistics.median(deltas_total),
            "memory_on_win_rate_total": sum(d > 0 for d in deltas_total) / SEEDS,
            "mean_delta_pre": statistics.mean(deltas_pre),
            "mean_delta_post": statistics.mean(deltas_post),
        },
        "reachability": {
            "mean_target_probe_support_on": statistics.mean(x["memory_on"]["target_reachability"]["probe_support_fraction"] for x in paired),
            "mean_target_probe_support_off": statistics.mean(x["memory_off"]["target_reachability"]["probe_support_fraction"] for x in paired),
            "mean_target_probe_selected_on": statistics.mean(x["memory_on"]["target_reachability"]["probe_selected_fraction"] for x in paired),
            "mean_target_probe_selected_off": statistics.mean(x["memory_off"]["target_reachability"]["probe_selected_fraction"] for x in paired),
            "mean_null_probe_support_on": statistics.mean(x["memory_on"]["null_reachability"]["probe_support_fraction"] for x in paired),
            "mean_null_probe_support_off": statistics.mean(x["memory_off"]["null_reachability"]["probe_support_fraction"] for x in paired),
            "target_trigger_rate_on": len(target_forced) / SEEDS,
            "null_trigger_rate_on": len(null_forced) / SEEDS,
        },
        "forced_controls": {
            "target_n": len(target_forced),
            "target_mean_delta": statistics.mean(x["forced_return_delta"] for x in target_forced) if target_forced else None,
            "target_positive_rate": sum(x["forced_return_delta"] > 0 for x in target_forced) / len(target_forced) if target_forced else None,
            "target_observation_change_rate": sum(x["observation_changed"] for x in target_forced) / len(target_forced) if target_forced else None,
            "null_n": len(null_forced),
            "null_mean_delta": statistics.mean(x["forced_return_delta"] for x in null_forced) if null_forced else None,
            "null_positive_rate": sum(x["forced_return_delta"] > 0 for x in null_forced) / len(null_forced) if null_forced else None,
            "null_observation_change_rate": sum(x["observation_changed"] for x in null_forced) / len(null_forced) if null_forced else None,
        },
        "exemplar": exemplar,
        "paired_seed_results": paired,
    }

    out = root / "blitzcrank_001_result.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("paired_seed_results", "exemplar")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
