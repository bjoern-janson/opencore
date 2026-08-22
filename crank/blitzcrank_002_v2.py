from __future__ import annotations

import copy
import hashlib
import json
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

EPISODES = 900
SHIFT_EPISODE = 180
SEEDS = 256
PROBE_COST = 0.20
POST_SHIFT_TARGET_SKIP_COST = 0.35
Q_INIT = 1.10
BASE_CONTEXTS = ("train", "target", "null")
REVEAL_ACTIONS = ("skip", "probe")
DECISION_ACTIONS = ("safe", "left", "right")
CONDITIONS = ("persistent_ordinary", "persistent_signaled", "reset")


@dataclass(frozen=True)
class EpisodeWorld:
    episode: int
    base_context: str
    regime: str


@dataclass
class Snapshot:
    q_reveal: Dict[str, Dict[str, float]]
    n_reveal: Dict[str, Dict[str, int]]
    q_decision: Dict[str, Dict[str, float]]
    n_decision: Dict[str, Dict[str, int]]


class Agent:
    def __init__(self):
        self.reset_memory()

    def reset_memory(self):
        self.q_reveal: Dict[str, Dict[str, float]] = {}
        self.n_reveal: Dict[str, Dict[str, int]] = {}
        self.q_decision: Dict[str, Dict[str, float]] = {}
        self.n_decision: Dict[str, Dict[str, int]] = {}

    def _ensure_reveal_context(self, context_key: str):
        if context_key not in self.q_reveal:
            self.q_reveal[context_key] = {a: Q_INIT for a in REVEAL_ACTIONS}
            self.n_reveal[context_key] = {a: 0 for a in REVEAL_ACTIONS}

    def _ensure_obs(self, obs: str):
        if obs not in self.q_decision:
            self.q_decision[obs] = {a: Q_INIT for a in DECISION_ACTIONS}
            self.n_decision[obs] = {a: 0 for a in DECISION_ACTIONS}

    @staticmethod
    def greedy_support(values: Dict[str, float]) -> List[str]:
        m = max(values.values())
        return [a for a, v in values.items() if math.isclose(v, m, abs_tol=1e-12)]

    def reveal_support(self, context_key: str) -> List[str]:
        self._ensure_reveal_context(context_key)
        return self.greedy_support(self.q_reveal[context_key])

    def decision_support(self, obs: str) -> List[str]:
        self._ensure_obs(obs)
        return self.greedy_support(self.q_decision[obs])

    @staticmethod
    def update_mean(q: Dict[str, float], n: Dict[str, int], action: str, value: float):
        n[action] += 1
        q[action] += (value - q[action]) / n[action]

    def update(self, context_key: str, reveal_action: str, obs: str,
               decision_action: str, decision_reward_value: float, total_return: float):
        self._ensure_reveal_context(context_key)
        self._ensure_obs(obs)
        self.update_mean(self.q_reveal[context_key], self.n_reveal[context_key], reveal_action, total_return)
        self.update_mean(self.q_decision[obs], self.n_decision[obs], decision_action, decision_reward_value)

    def snapshot(self) -> Snapshot:
        return Snapshot(
            q_reveal=copy.deepcopy(self.q_reveal),
            n_reveal=copy.deepcopy(self.n_reveal),
            q_decision=copy.deepcopy(self.q_decision),
            n_decision=copy.deepcopy(self.n_decision),
        )

    def restore(self, s: Snapshot):
        self.q_reveal = copy.deepcopy(s.q_reveal)
        self.n_reveal = copy.deepcopy(s.n_reveal)
        self.q_decision = copy.deepcopy(s.q_decision)
        self.n_decision = copy.deepcopy(s.n_decision)


def stable_choice(seed: int, episode: int, stage: str, support: List[str]) -> str:
    if len(support) == 1:
        return support[0]
    body = f"{seed}|{episode}|{stage}|{'|'.join(sorted(support))}".encode()
    h = hashlib.sha256(body).digest()
    return sorted(support)[int.from_bytes(h[:8], "big") % len(support)]


def make_schedule(seed: int) -> List[EpisodeWorld]:
    rng = random.Random(seed ^ 0xB1172C02)
    out = []
    for ep in range(EPISODES):
        base_context = BASE_CONTEXTS[ep % len(BASE_CONTEXTS)]
        if base_context == "train":
            regime = rng.choice(("A", "B"))
        elif base_context == "target":
            regime = "N" if ep < SHIFT_EPISODE else rng.choice(("A", "B"))
        else:
            regime = "N"
        out.append(EpisodeWorld(ep, base_context, regime))
    return out


def reveal_context_key(world: EpisodeWorld, condition: str) -> str:
    if condition == "persistent_signaled" and world.base_context == "target" and world.episode >= SHIFT_EPISODE:
        return "target_shifted"
    return world.base_context


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


def reveal_cost(world: EpisodeWorld, action: str) -> float:
    if action == "probe":
        return PROBE_COST
    if world.base_context == "target" and world.episode >= SHIFT_EPISODE:
        return POST_SHIFT_TARGET_SKIP_COST
    return 0.0


def pi_label(q_probe: float, q_skip: float) -> str:
    if math.isclose(q_probe, q_skip, abs_tol=1e-12):
        return "TIED"
    return "PROBE_PREFERRED" if q_probe > q_skip else "SKIP_PREFERRED"


def compact_L(agent: Agent, context_key: str) -> dict:
    agent._ensure_reveal_context(context_key)
    return {
        "reveal_context_key": context_key,
        "reveal_q": {k: round(v, 8) for k, v in agent.q_reveal[context_key].items()},
        "reveal_n": dict(agent.n_reveal[context_key]),
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


def forced_episode(seed: int, condition: str, world: EpisodeWorld, snapshot: Snapshot,
                   endogenous: dict) -> dict:
    agent = Agent()
    agent.restore(snapshot)
    context_key = reveal_context_key(world, condition)
    r_support = agent.reveal_support(context_key)
    obs = reveal_observation(world, "probe")
    d_support = agent.decision_support(obs)
    d_selected = stable_choice(seed, world.episode, f"decision:{obs}", d_support)
    d_reward = decision_reward(world.regime, d_selected)
    total = d_reward - reveal_cost(world, "probe")
    return {
        "episode": world.episode,
        "base_context": world.base_context,
        "regime": world.regime,
        "endogenous_observation": endogenous["E_t1"],
        "forced_observation": obs,
        "endogenous_decision": endogenous["decision_action"],
        "forced_decision": d_selected,
        "endogenous_return": endogenous["return"],
        "forced_return": total,
        "forced_return_delta": total - endogenous["return"],
        "observation_changed": obs != endogenous["E_t1"],
        "decision_changed": d_selected != endogenous["decision_action"],
        "forced_reveal_support_before_override": list(r_support),
    }


def run_condition(seed: int, condition: str, schedule: List[EpisodeWorld], capture_trace: bool = False) -> dict:
    agent = Agent()
    total = pre = post = 0.0
    target_post_n = 0
    target_probe_support_n = 0
    target_probe_selected_n = 0
    tau_support = None
    tau_selected = None
    initial_probe_in_support = None
    target_forced = []
    null_forced = []
    trace = [] if capture_trace else None

    for world in schedule:
        if condition == "reset":
            agent.reset_memory()

        context_key = reveal_context_key(world, condition)
        agent._ensure_reveal_context(context_key)
        r_support = agent.reveal_support(context_key)
        selected = stable_choice(seed, world.episode, "reveal", r_support)

        eligible_forced = (
            condition == "persistent_ordinary"
            and world.episode >= SHIFT_EPISODE
            and world.base_context in ("target", "null")
            and "probe" not in r_support
        )
        snap = agent.snapshot() if eligible_forced else None

        obs = reveal_observation(world, selected)
        d_support = agent.decision_support(obs)
        d_selected = stable_choice(seed, world.episode, f"decision:{obs}", d_support)
        d_reward = decision_reward(world.regime, d_selected)
        cost = reveal_cost(world, selected)
        ret = d_reward - cost

        record = {
            "episode": world.episode,
            "base_context": world.base_context,
            "audit_regime": world.regime,
            "L_t": compact_L(agent, context_key),
            "Pi_t": pi_label(agent.q_reveal[context_key]["probe"], agent.q_reveal[context_key]["skip"]),
            "pi_t": {"support": list(r_support), "selected": selected},
            "R_available": list(REVEAL_ACTIONS),
            "a_t": selected,
            "E_t1": obs,
            "decision_support": list(d_support),
            "decision_action": d_selected,
            "decision_reward": d_reward,
            "reveal_cost": cost,
            "return": ret,
        }

        if eligible_forced and snap is not None:
            fc = forced_episode(seed, condition, world, snap, record)
            (target_forced if world.base_context == "target" else null_forced).append(fc)

        agent.update(context_key, selected, obs, d_selected, d_reward, ret)

        total += ret
        if world.episode < SHIFT_EPISODE:
            pre += ret
        else:
            post += ret

        if world.episode >= SHIFT_EPISODE and world.base_context == "target":
            idx = target_post_n
            in_support = "probe" in r_support
            is_selected = selected == "probe"
            if initial_probe_in_support is None:
                initial_probe_in_support = in_support
            if in_support:
                target_probe_support_n += 1
                if tau_support is None:
                    tau_support = idx
            if is_selected:
                target_probe_selected_n += 1
                if tau_selected is None:
                    tau_selected = idx
            target_post_n += 1

        if capture_trace:
            trace.append(record)

    recovery = {
        "n_target_post": target_post_n,
        "initial_probe_in_support": initial_probe_in_support,
        "tau_reopen_support_target_encounters": tau_support,
        "tau_reopen_selected_target_encounters": tau_selected,
        "tau_reopen_support_global_episodes": (3 * tau_support + 1) if tau_support is not None else None,
        "tau_reopen_selected_global_episodes": (3 * tau_selected + 1) if tau_selected is not None else None,
        "probe_support_fraction": target_probe_support_n / target_post_n,
        "probe_selected_fraction": target_probe_selected_n / target_post_n,
        "reopened_within_horizon": tau_support is not None,
    }
    return {
        "returns": {"total": total, "pre": pre, "post": post},
        "recovery": recovery,
        "target_forced": target_forced,
        "null_forced": null_forced,
        "trace": trace,
    }


def classify(recovery: dict) -> str:
    if recovery["initial_probe_in_support"]:
        return "NO_INITIAL_SUPPRESSION"
    if recovery["reopened_within_horizon"]:
        return "POLICY_SUPPORT_REOPENING_OBSERVED"
    return "PERSISTENT_SUPPRESSION_WITHIN_HORIZON"


def metric_summary(values: List[float]) -> dict:
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
    }


def nullable_summary(values: List[int | None]) -> dict:
    finite = [v for v in values if v is not None]
    return {
        "n": len(values),
        "finite_n": len(finite),
        "finite_fraction": len(finite) / len(values),
        "mean_if_finite": statistics.mean(finite) if finite else None,
        "median_if_finite": statistics.median(finite) if finite else None,
        "min_if_finite": min(finite) if finite else None,
        "max_if_finite": max(finite) if finite else None,
    }


def main():
    root = Path(__file__).resolve().parent
    spec_sha = hashlib.sha256((root / "BLITZCRANK_002_SPEC.md").read_bytes()).hexdigest()
    harness_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    paired = []
    all_target_forced = []
    all_null_forced = []
    exemplar = None

    for seed in range(SEEDS):
        schedule = make_schedule(seed)
        ordinary = run_condition(seed, "persistent_ordinary", schedule, capture_trace=(exemplar is None))
        signaled = run_condition(seed, "persistent_signaled", schedule)
        reset = run_condition(seed, "reset", schedule)

        branches = {
            "persistent_ordinary": ordinary,
            "persistent_signaled": signaled,
            "reset": reset,
        }
        returns = {k: v["returns"] for k, v in branches.items()}
        recovery = {k: v["recovery"] for k, v in branches.items()}

        all_target_forced.extend({"seed": seed, **x} for x in ordinary["target_forced"])
        all_null_forced.extend({"seed": seed, **x} for x in ordinary["null_forced"])

        row = {
            "seed": seed,
            "returns": returns,
            "recovery": recovery,
            "ordinary_class": classify(recovery["persistent_ordinary"]),
            "delta_total_ordinary_vs_reset": returns["persistent_ordinary"]["total"] - returns["reset"]["total"],
            "delta_post_ordinary_vs_reset": returns["persistent_ordinary"]["post"] - returns["reset"]["post"],
            "delta_total_signaled_vs_reset": returns["persistent_signaled"]["total"] - returns["reset"]["total"],
            "delta_post_signaled_vs_reset": returns["persistent_signaled"]["post"] - returns["reset"]["post"],
            "delta_post_signaled_vs_ordinary": returns["persistent_signaled"]["post"] - returns["persistent_ordinary"]["post"],
            "ordinary_target_forced_n": len(ordinary["target_forced"]),
            "ordinary_target_forced_positive": sum(x["forced_return_delta"] > 0 for x in ordinary["target_forced"]),
            "ordinary_null_forced_n": len(ordinary["null_forced"]),
        }
        paired.append(row)

        if exemplar is None and recovery["persistent_ordinary"]["tau_reopen_support_target_encounters"] is not None:
            tau_global = recovery["persistent_ordinary"]["tau_reopen_support_global_episodes"]
            center_ep = SHIFT_EPISODE + tau_global
            tr = ordinary["trace"] or []
            exemplar = {
                "seed": seed,
                "ordinary_recovery": recovery["persistent_ordinary"],
                "signaled_recovery": recovery["persistent_signaled"],
                "reset_recovery": recovery["reset"],
                "ordinary_window": [r for r in tr if abs(r["episode"] - center_ep) <= 9],
            }

    ordinary_delta_total = [x["delta_total_ordinary_vs_reset"] for x in paired]
    ordinary_delta_post = [x["delta_post_ordinary_vs_reset"] for x in paired]
    signaled_delta_total = [x["delta_total_signaled_vs_reset"] for x in paired]
    signaled_delta_post = [x["delta_post_signaled_vs_reset"] for x in paired]
    signaled_vs_ordinary_post = [x["delta_post_signaled_vs_ordinary"] for x in paired]

    tau_ord = [x["recovery"]["persistent_ordinary"]["tau_reopen_support_target_encounters"] for x in paired]
    tau_sig = [x["recovery"]["persistent_signaled"]["tau_reopen_support_target_encounters"] for x in paired]
    tau_reset = [x["recovery"]["reset"]["tau_reopen_support_target_encounters"] for x in paired]

    class_counts = {k: 0 for k in ("POLICY_SUPPORT_REOPENING_OBSERVED", "PERSISTENT_SUPPRESSION_WITHIN_HORIZON", "NO_INITIAL_SUPPRESSION")}
    for x in paired:
        class_counts[x["ordinary_class"]] += 1

    target_deltas = [x["forced_return_delta"] for x in all_target_forced]
    null_deltas = [x["forced_return_delta"] for x in all_null_forced]

    result = {
        "assay": "BLITZCRANK-002",
        "spec_sha256": spec_sha,
        "harness_sha256": harness_sha,
        "parameters": {
            "episodes": EPISODES,
            "shift_episode": SHIFT_EPISODE,
            "seeds": SEEDS,
            "probe_cost": PROBE_COST,
            "post_shift_target_skip_cost": POST_SHIFT_TARGET_SKIP_COST,
            "q_init": Q_INIT,
        },
        "validity": {
            "paired_hidden_world_schedule": True,
            "identical_physical_actions": True,
            "identical_reward_function": True,
            "exogenous_target_shift": True,
            "hidden_regime_not_exposed": True,
            "ordinary_receives_no_shift_marker": True,
            "signaled_receives_only_context_key_change": True,
            "reset_retains_no_cross_episode_values": True,
            "forced_controls_exact_snapshot_clone": True,
            "forced_controls_do_not_modify_endogenous_trajectory": True,
            "null_stationary_and_nondiscriminating": True,
            "nano_present": False,
        },
        "ordinary_outcome_class_counts": class_counts,
        "performance": {
            "ordinary_vs_reset_total": metric_summary(ordinary_delta_total),
            "ordinary_vs_reset_post": metric_summary(ordinary_delta_post),
            "ordinary_memory_win_rate_total": sum(x > 0 for x in ordinary_delta_total) / SEEDS,
            "ordinary_memory_win_rate_post": sum(x > 0 for x in ordinary_delta_post) / SEEDS,
            "signaled_vs_reset_total": metric_summary(signaled_delta_total),
            "signaled_vs_reset_post": metric_summary(signaled_delta_post),
            "signaled_memory_win_rate_total": sum(x > 0 for x in signaled_delta_total) / SEEDS,
            "signaled_vs_ordinary_post": metric_summary(signaled_vs_ordinary_post),
        },
        "reopening": {
            "persistent_ordinary_tau_support": nullable_summary(tau_ord),
            "persistent_signaled_tau_support": nullable_summary(tau_sig),
            "reset_tau_support": nullable_summary(tau_reset),
            "ordinary_mean_probe_support_fraction": statistics.mean(x["recovery"]["persistent_ordinary"]["probe_support_fraction"] for x in paired),
            "ordinary_mean_probe_selected_fraction": statistics.mean(x["recovery"]["persistent_ordinary"]["probe_selected_fraction"] for x in paired),
            "signaled_mean_probe_support_fraction": statistics.mean(x["recovery"]["persistent_signaled"]["probe_support_fraction"] for x in paired),
            "reset_mean_probe_support_fraction": statistics.mean(x["recovery"]["reset"]["probe_support_fraction"] for x in paired),
        },
        "forced_controls": {
            "ordinary_target_excluded_states_n": len(all_target_forced),
            "ordinary_target_observation_change_rate": sum(x["observation_changed"] for x in all_target_forced) / len(all_target_forced) if all_target_forced else None,
            "ordinary_target_positive_one_step_rate": sum(x > 0 for x in target_deltas) / len(target_deltas) if target_deltas else None,
            "ordinary_target_mean_one_step_delta": statistics.mean(target_deltas) if target_deltas else None,
            "ordinary_target_delta_summary": metric_summary(target_deltas) if target_deltas else None,
            "ordinary_null_excluded_states_n": len(all_null_forced),
            "ordinary_null_observation_change_rate": sum(x["observation_changed"] for x in all_null_forced) / len(all_null_forced) if all_null_forced else None,
            "ordinary_null_positive_one_step_rate": sum(x > 0 for x in null_deltas) / len(null_deltas) if null_deltas else None,
            "ordinary_null_mean_one_step_delta": statistics.mean(null_deltas) if null_deltas else None,
            "ordinary_null_delta_summary": metric_summary(null_deltas) if null_deltas else None,
        },
        "exemplar": exemplar,
        "paired_seed_results": paired,
    }

    out = root / "blitzcrank_002_result_v2.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("paired_seed_results", "exemplar")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
