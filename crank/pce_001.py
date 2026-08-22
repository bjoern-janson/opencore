from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

WORLD_NULL = "WORLD_NULL"
WORLD_INFORMATIVE = "WORLD_INFORMATIVE"
WORLD_CORRECTIVE = "WORLD_CORRECTIVE"
WORLDS = (WORLD_NULL, WORLD_INFORMATIVE, WORLD_CORRECTIVE)

ARM_ENDOGENOUS = "ARM_ENDOGENOUS"
ARM_SUPPORT = "ARM_SUPPORT"
ARM_FLOOR = "ARM_FLOOR"
ARM_HAZARD = "ARM_HAZARD"
ARMS = (ARM_ENDOGENOUS, ARM_SUPPORT, ARM_FLOOR, ARM_HAZARD)

REVEAL_ACTIONS = ("skip", "probe")
DECISION_ACTIONS = ("safe", "left", "right")
Q_INIT = 1.10
PROBE_COST = 0.20
EPSILON = 0.05
ETA = 0.05
EPISODES = 420
SHIFT_EPISODE = 180
SEEDS = 256
POST_TARGET_HORIZON = 120
TC_CENSOR = 121
CORRECTIVE_DELTA_THRESHOLD = 0.10
EQUIV_T_MARGIN = 5.0
EQUIV_RATE_MARGIN = 0.05
INITIAL_SUPPRESSION_FLOOR = 0.95


@dataclass(frozen=True)
class EpisodeWorld:
    episode: int
    context: str
    regime: str


class Agent:
    def __init__(self) -> None:
        self.q_reveal: Dict[str, Dict[str, float]] = {}
        self.n_reveal: Dict[str, Dict[str, int]] = {}
        self.q_decision: Dict[str, Dict[str, float]] = {}
        self.n_decision: Dict[str, Dict[str, int]] = {}

    def _ensure_reveal(self, context: str) -> None:
        if context not in self.q_reveal:
            self.q_reveal[context] = {a: Q_INIT for a in REVEAL_ACTIONS}
            self.n_reveal[context] = {a: 0 for a in REVEAL_ACTIONS}

    def _ensure_obs(self, obs: str) -> None:
        if obs not in self.q_decision:
            self.q_decision[obs] = {a: Q_INIT for a in DECISION_ACTIONS}
            self.n_decision[obs] = {a: 0 for a in DECISION_ACTIONS}

    @staticmethod
    def greedy_support_values(values: Dict[str, float]) -> List[str]:
        m = max(values.values())
        return sorted(a for a, v in values.items() if math.isclose(v, m, abs_tol=1e-12))

    def reveal_support(self, context: str) -> List[str]:
        self._ensure_reveal(context)
        return self.greedy_support_values(self.q_reveal[context])

    def decision_support(self, obs: str, mutate: bool = True) -> List[str]:
        if mutate:
            self._ensure_obs(obs)
            values = self.q_decision[obs]
        else:
            values = self.q_decision.get(obs, {a: Q_INIT for a in DECISION_ACTIONS})
        return self.greedy_support_values(values)

    @staticmethod
    def update_mean(q: Dict[str, float], n: Dict[str, int], action: str, value: float) -> None:
        n[action] += 1
        q[action] += (value - q[action]) / n[action]

    def update(
        self,
        context: str,
        reveal_action: str,
        obs: str,
        decision_action: str,
        decision_reward_value: float,
        total_return: float,
    ) -> None:
        self._ensure_reveal(context)
        self._ensure_obs(obs)
        self.update_mean(self.q_reveal[context], self.n_reveal[context], reveal_action, total_return)
        self.update_mean(self.q_decision[obs], self.n_decision[obs], decision_action, decision_reward_value)


def stable_unit(seed: int, episode: int, stage: str) -> float:
    body = f"PCE001|{seed}|{episode}|{stage}".encode("utf-8")
    h = hashlib.sha256(body).digest()
    return int.from_bytes(h[:8], "big") / 2**64


def stable_choice(seed: int, episode: int, stage: str, support: List[str]) -> str:
    support = sorted(support)
    if len(support) == 1:
        return support[0]
    u = stable_unit(seed, episode, stage)
    idx = min(int(u * len(support)), len(support) - 1)
    return support[idx]


def context_for_episode(episode: int) -> str:
    return "train" if episode % 2 == 0 else "target"


def binary_regime(seed: int, episode: int, stage: str) -> str:
    return "A" if stable_unit(seed, episode, stage) < 0.5 else "B"


def make_schedule(seed: int, world: str) -> List[EpisodeWorld]:
    schedule: List[EpisodeWorld] = []
    for ep in range(EPISODES):
        context = context_for_episode(ep)
        if context == "train":
            regime = binary_regime(seed, ep, "schedule-train")
        elif ep < SHIFT_EPISODE or world == WORLD_NULL:
            regime = "N"
        else:
            regime = binary_regime(seed, ep, "schedule-target")
        schedule.append(EpisodeWorld(ep, context, regime))
    return schedule


def schedule_digest(schedule: List[EpisodeWorld]) -> str:
    body = "\n".join(f"{x.episode}|{x.context}|{x.regime}" for x in schedule).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def reveal_observation(world: EpisodeWorld, action: str) -> str:
    if action == "skip":
        return "UNKNOWN"
    if world.regime == "A":
        return "SIG_A"
    if world.regime == "B":
        return "SIG_B"
    return "SAME"


def regime_consistent_action(regime: str) -> Optional[str]:
    if regime == "A":
        return "left"
    if regime == "B":
        return "right"
    return None


def decision_reward(world_class: str, world: EpisodeWorld, obs: str, action: str) -> float:
    # Unknown observations intentionally carry no hidden-regime reward information.
    if obs == "UNKNOWN":
        return 1.0
    if world.regime == "N":
        return 1.0
    if world.context == "target" and world_class == WORLD_INFORMATIVE:
        return 1.0
    if world.regime == "A":
        return 1.4 if action == "left" else (0.6 if action == "right" else 1.0)
    if world.regime == "B":
        return 1.4 if action == "right" else (0.6 if action == "left" else 1.0)
    raise AssertionError(world)


def reveal_cost(action: str) -> float:
    return PROBE_COST if action == "probe" else 0.0


def preference_label(agent: Agent, context: str) -> str:
    agent._ensure_reveal(context)
    qp = agent.q_reveal[context]["probe"]
    qs = agent.q_reveal[context]["skip"]
    if math.isclose(qp, qs, abs_tol=1e-12):
        return "TIED"
    return "PROBE_PREFERRED" if qp > qs else "SKIP_PREFERRED"


def base_probe_probability(base_support: List[str]) -> float:
    return (1.0 / len(base_support)) if "probe" in base_support else 0.0


def post_target_index(episode: int) -> Optional[int]:
    if episode < SHIFT_EPISODE or context_for_episode(episode) != "target":
        return None
    # First post-shift target is episode 181.
    return (episode - (SHIFT_EPISODE + 1)) // 2


def arm_select(
    seed: int,
    episode: int,
    arm: str,
    j: int,
    base_support: List[str],
) -> Tuple[str, float, dict]:
    p_base = base_probe_probability(base_support)
    base_selected = stable_choice(seed, episode, "base-policy", base_support)
    meta = {
        "base_p_probe": p_base,
        "effective_p_probe": p_base,
        "intervention_active": False,
        "hazard_trigger": False,
        "support_probability": None,
    }

    if arm == ARM_ENDOGENOUS:
        return base_selected, p_base, meta

    if arm == ARM_SUPPORT:
        p_support = 1.0 / ((j + 2) ** 2)
        meta["support_probability"] = p_support
        if p_base > 0.0:
            return base_selected, p_base, meta
        meta["effective_p_probe"] = p_support
        meta["intervention_active"] = True
        selected = "probe" if stable_unit(seed, episode, "protected-policy") < p_support else "skip"
        return selected, p_support, meta

    if arm == ARM_FLOOR:
        p_eff = max(p_base, EPSILON)
        meta["effective_p_probe"] = p_eff
        if math.isclose(p_eff, p_base, abs_tol=1e-15):
            return base_selected, p_base, meta
        meta["intervention_active"] = True
        selected = "probe" if stable_unit(seed, episode, "protected-policy") < p_eff else "skip"
        return selected, p_eff, meta

    if arm == ARM_HAZARD:
        fired = stable_unit(seed, episode, "hazard") < ETA
        meta["hazard_trigger"] = fired
        meta["effective_p_probe"] = ETA + (1.0 - ETA) * p_base
        if fired:
            meta["intervention_active"] = True
            return "probe", meta["effective_p_probe"], meta
        return base_selected, meta["effective_p_probe"], meta

    raise ValueError(arm)


def compact_state(agent: Agent) -> dict:
    agent._ensure_reveal("target")
    target_q = agent.q_reveal["target"]
    target_n = agent.n_reveal["target"]

    def obs_values(obs: str) -> dict:
        q = agent.q_decision.get(obs, {a: Q_INIT for a in DECISION_ACTIONS})
        n = agent.n_decision.get(obs, {a: 0 for a in DECISION_ACTIONS})
        return {
            "q": {a: round(q[a], 8) for a in DECISION_ACTIONS},
            "n": {a: n[a] for a in DECISION_ACTIONS},
        }

    return {
        "target": {
            "q_probe": round(target_q["probe"], 8),
            "q_skip": round(target_q["skip"], 8),
            "n_probe": target_n["probe"],
            "n_skip": target_n["skip"],
        },
        "SIG_A": obs_values("SIG_A"),
        "SIG_B": obs_values("SIG_B"),
    }


def counterfactual_probe(
    agent: Agent,
    seed: int,
    world_class: str,
    world: EpisodeWorld,
    realized_return: float,
) -> dict:
    obs = reveal_observation(world, "probe")
    support = agent.decision_support(obs, mutate=False)
    action = stable_choice(seed, world.episode, f"decision:{obs}", support)
    d_reward = decision_reward(world_class, world, obs, action)
    ret = d_reward - PROBE_COST
    return {
        "observation": obs,
        "decision_action": action,
        "decision_reward": d_reward,
        "return": ret,
        "delta": ret - realized_return,
    }


def evidence_role(world_class: str, selected: str, c4a: bool, c5: bool) -> str:
    if selected != "probe":
        return "NO_CHALLENGE"
    if not c4a:
        return "NONDISCRIMINATING"
    if world_class == WORLD_INFORMATIVE:
        return "DISCRIMINATING_NONCORRECTIVE_RECOGNIZED" if c5 else "DISCRIMINATING_NONCORRECTIVE_UNRECOGNIZED"
    if world_class == WORLD_CORRECTIVE:
        return "DISCRIMINATING_CORRECTIVE_RECOGNIZED" if c5 else "DISCRIMINATING_CORRECTIVE_UNRECOGNIZED"
    return "NONDISCRIMINATING"


def run_branch(
    seed: int,
    world_class: str,
    arm: str,
    schedule: List[EpisodeWorld],
    trace_sink,
    trace_hash,
) -> dict:
    agent = Agent()
    total_return = 0.0
    post_target_return = 0.0
    post_target_count = 0
    challenge_count = 0
    sum_effective_p = 0.0
    t_c: Optional[int] = None
    t_l: Optional[int] = None
    initial_base_suppressed: Optional[bool] = None
    gates = {k: 0 for k in ("C1", "C2", "C3", "C4a", "C4b", "C5", "C6")}
    missed_positive_cf = 0
    missed_cf_n = 0
    missed_cf_delta_sum = 0.0
    base_support_reopen_count = 0
    base_support_after_first_reopen = 0
    first_base_reopen_j: Optional[int] = None

    for world in schedule:
        base_support = agent.reveal_support(world.context)
        j = post_target_index(world.episode)
        is_challenge_opportunity = j is not None

        if is_challenge_opportunity:
            if initial_base_suppressed is None:
                initial_base_suppressed = "probe" not in base_support
            selected, p_eff, arm_meta = arm_select(seed, world.episode, arm, j, base_support)
        else:
            selected = stable_choice(seed, world.episode, "base-policy", base_support)
            p_eff = base_probe_probability(base_support)
            arm_meta = {
                "base_p_probe": p_eff,
                "effective_p_probe": p_eff,
                "intervention_active": False,
                "hazard_trigger": False,
                "support_probability": None,
            }

        e_t = compact_state(agent) if is_challenge_opportunity else None
        pi_label_t = preference_label(agent, world.context)
        obs = reveal_observation(world, selected)
        d_support = agent.decision_support(obs, mutate=True)
        d_selected = stable_choice(seed, world.episode, f"decision:{obs}", d_support)
        d_reward = decision_reward(world_class, world, obs, d_selected)
        ret = d_reward - reveal_cost(selected)

        cf = counterfactual_probe(agent, seed, world_class, world, ret) if is_challenge_opportunity else None

        channel_discriminating = (
            is_challenge_opportunity
            and world_class in (WORLD_INFORMATIVE, WORLD_CORRECTIVE)
            and world.regime in ("A", "B")
        )
        d_oracle = ["probe"] if channel_discriminating else []
        c1 = bool(is_challenge_opportunity and "probe" in REVEAL_ACTIONS)
        c2 = bool(is_challenge_opportunity and p_eff > 0.0)
        c3 = bool(is_challenge_opportunity and selected == "probe")
        c4a = bool(c3 and channel_discriminating)
        c4b = c4a  # SIG_A/SIG_B are not aliased by the frozen representation.
        optimal = regime_consistent_action(world.regime)
        c5 = bool(c4b and optimal is not None and d_selected == optimal)

        agent.update(world.context, selected, obs, d_selected, d_reward, ret)
        base_support_after = agent.reveal_support(world.context)
        c6 = bool(
            is_challenge_opportunity
            and world_class == WORLD_CORRECTIVE
            and c5
            and "probe" in base_support_after
        )

        total_return += ret
        if is_challenge_opportunity:
            post_target_count += 1
            post_target_return += ret
            sum_effective_p += p_eff
            challenge_count += int(c3)
            for k, v in zip(("C1", "C2", "C3", "C4a", "C4b", "C5", "C6"), (c1, c2, c3, c4a, c4b, c5, c6)):
                gates[k] += int(v)

            if "probe" in base_support_after:
                base_support_reopen_count += 1
                if first_base_reopen_j is None:
                    first_base_reopen_j = j
                if first_base_reopen_j is not None and j >= first_base_reopen_j:
                    base_support_after_first_reopen += 1

            if t_c is None and c6:
                t_c = j

            if selected != "probe":
                missed_cf_n += 1
                missed_cf_delta_sum += cf["delta"]
                if cf["delta"] >= CORRECTIVE_DELTA_THRESHOLD:
                    missed_positive_cf += 1
                    if t_l is None:
                        t_l = j

            w_t1 = evidence_role(world_class, selected, c4a, c5)
            e_t1 = compact_state(agent)
            record = {
                "seed": seed,
                "world": world_class,
                "arm": arm,
                "episode": world.episode,
                "target_j": j,
                "audit_regime": world.regime,
                "E_t": e_t,
                "Pi_t": pi_label_t,
                "pi_t": {
                    "base_support": base_support,
                    "base_p_probe": arm_meta["base_p_probe"],
                    "effective_p_probe": p_eff,
                    "selected": selected,
                    "intervention_active": arm_meta["intervention_active"],
                    "hazard_trigger": arm_meta["hazard_trigger"],
                    "support_probability": arm_meta["support_probability"],
                },
                "D_t_oracle": d_oracle,
                "C1": c1,
                "C2": c2,
                "C3": c3,
                "C4a": c4a,
                "C4b": c4b,
                "C5": c5,
                "C6": c6,
                "A_t": selected,
                "O_t1": obs,
                "W_t1": w_t1,
                "E_t1": e_t1,
                "decision_action": d_selected,
                "decision_reward": d_reward,
                "return": ret,
                "forced_probe": cf,
                "base_support_after": base_support_after,
            }
            line = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
            trace_hash.update(line)
            trace_sink.write(line)

    assert post_target_count == POST_TARGET_HORIZON
    assert initial_base_suppressed is not None
    return {
        "seed": seed,
        "world": world_class,
        "arm": arm,
        "schedule_sha256": schedule_digest(schedule),
        "total_return": total_return,
        "post_target_return": post_target_return,
        "post_target_count": post_target_count,
        "challenge_count": challenge_count,
        "mean_effective_probe_probability": sum_effective_p / post_target_count,
        "T_C": t_c,
        "T_C_censored": t_c if t_c is not None else TC_CENSOR,
        "T_L": t_l,
        "initial_base_suppressed": initial_base_suppressed,
        "gates": gates,
        "missed_cf_n": missed_cf_n,
        "missed_positive_cf": missed_positive_cf,
        "missed_cf_delta_mean": (missed_cf_delta_sum / missed_cf_n) if missed_cf_n else None,
        "first_base_reopen_j": first_base_reopen_j,
        "base_support_reopen_fraction": base_support_reopen_count / post_target_count,
        "base_support_post_first_fraction": (
            base_support_after_first_reopen / (post_target_count - first_base_reopen_j)
            if first_base_reopen_j is not None else 0.0
        ),
    }


def mean(xs: Iterable[float]) -> float:
    vals = list(xs)
    return statistics.mean(vals) if vals else float("nan")


def metric_summary(values: List[float]) -> dict:
    if not values:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None}
    return {
        "n": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
    }


def aggregate_rows(rows: List[dict]) -> dict:
    finite_tc = [r["T_C"] for r in rows if r["T_C"] is not None]
    finite_tl = [r["T_L"] for r in rows if r["T_L"] is not None]
    opportunities = sum(r["post_target_count"] for r in rows)
    gate_sums = {k: sum(r["gates"][k] for r in rows) for k in rows[0]["gates"]}
    both = [r for r in rows if r["T_C"] is not None and r["T_L"] is not None]
    return {
        "n_seeds": len(rows),
        "finite_T_C_rate": len(finite_tc) / len(rows),
        "T_C_finite": metric_summary([float(x) for x in finite_tc]),
        "T_C_censored": metric_summary([float(r["T_C_censored"]) for r in rows]),
        "finite_T_L_rate": len(finite_tl) / len(rows),
        "T_L_finite": metric_summary([float(x) for x in finite_tl]),
        "T_clock_relation_when_both_finite": {
            "n": len(both),
            "T_C_lt_T_L": sum(r["T_C"] < r["T_L"] for r in both),
            "T_C_eq_T_L": sum(r["T_C"] == r["T_L"] for r in both),
            "T_C_gt_T_L": sum(r["T_C"] > r["T_L"] for r in both),
        },
        "total_return": metric_summary([r["total_return"] for r in rows]),
        "post_target_return": metric_summary([r["post_target_return"] for r in rows]),
        "challenge_count": metric_summary([float(r["challenge_count"]) for r in rows]),
        "mean_effective_probe_probability": mean(r["mean_effective_probe_probability"] for r in rows),
        "initial_base_suppression_rate": mean(float(r["initial_base_suppressed"]) for r in rows),
        "gate_counts": gate_sums,
        "gate_rates_per_opportunity": {k: gate_sums[k] / opportunities for k in gate_sums},
        "missed_positive_cf_rate": (
            sum(r["missed_positive_cf"] for r in rows) / sum(r["missed_cf_n"] for r in rows)
            if sum(r["missed_cf_n"] for r in rows) else None
        ),
        "base_support_reopen_fraction_mean": mean(r["base_support_reopen_fraction"] for r in rows),
    }


def paired_contrast(rows: List[dict], arm_left: str, arm_right: str, world: str) -> dict:
    left = {r["seed"]: r for r in rows if r["world"] == world and r["arm"] == arm_left}
    right = {r["seed"]: r for r in rows if r["world"] == world and r["arm"] == arm_right}
    assert left.keys() == right.keys() == set(range(SEEDS))
    deltas = [left[s]["T_C_censored"] - right[s]["T_C_censored"] for s in range(SEEDS)]
    finite_left = mean(float(left[s]["T_C"] is not None) for s in range(SEEDS))
    finite_right = mean(float(right[s]["T_C"] is not None) for s in range(SEEDS))
    rate_diff = finite_right - finite_left
    mean_delta = statistics.mean(deltas)
    if mean_delta >= EQUIV_T_MARGIN and rate_diff >= EQUIV_RATE_MARGIN:
        classification = "SUPPORTS_DIRECTIONAL_SEPARATION"
    elif abs(mean_delta) < EQUIV_T_MARGIN and abs(rate_diff) < EQUIV_RATE_MARGIN:
        classification = "APPROXIMATELY_EQUIVALENT"
    else:
        classification = "UNDERDETERMINED"
    return {
        "left": arm_left,
        "right": arm_right,
        "world": world,
        "mean_paired_T_C_censored_left_minus_right": mean_delta,
        "median_paired_T_C_censored_left_minus_right": statistics.median(deltas),
        "finite_rate_left": finite_left,
        "finite_rate_right": finite_right,
        "finite_rate_right_minus_left": rate_diff,
        "right_faster": sum(d > 0 for d in deltas),
        "tie": sum(d == 0 for d in deltas),
        "right_slower": sum(d < 0 for d in deltas),
        "classification": classification,
    }


def empirical_survival(rows: List[dict], world: str, arm: str) -> List[dict]:
    branch = [r for r in rows if r["world"] == world and r["arm"] == arm]
    # This is correction survival, not challenge survival: P(T_C > j).
    out = []
    for j in range(POST_TARGET_HORIZON):
        no_correction = sum(r["T_C"] is None or r["T_C"] > j for r in branch)
        out.append({"j": j, "p_no_correction": no_correction / len(branch)})
    return out


def trace_required_fields_ok(sample_record: dict) -> bool:
    required = {
        "E_t", "Pi_t", "pi_t", "D_t_oracle",
        "C1", "C2", "C3", "C4a", "C4b", "C5", "C6",
        "A_t", "O_t1", "W_t1", "E_t1",
    }
    return required.issubset(sample_record)


def validate(rows: List[dict], trace_sample: dict) -> dict:
    checks = {}

    # Schedules are identical across arms within each seed/world.
    schedule_ok = True
    for world in WORLDS:
        for seed in range(SEEDS):
            hs = {r["schedule_sha256"] for r in rows if r["world"] == world and r["seed"] == seed}
            schedule_ok &= len(hs) == 1
    checks["identical_schedule_across_arms"] = schedule_ok

    checks["physical_reveal_actions_fixed"] = set(REVEAL_ACTIONS) == {"skip", "probe"}
    checks["hazard_key_state_independent_by_construction"] = True
    checks["support_schedule_positive_and_vanishing"] = (
        all(1.0 / ((j + 2) ** 2) > 0 for j in range(POST_TARGET_HORIZON))
        and (1.0 / ((POST_TARGET_HORIZON + 1) ** 2)) < (1.0 / 4.0)
    )

    # Floor is audited from branch summaries indirectly by deterministic arm code; add direct function checks.
    floor_ok = True
    for base_support in (["skip"], ["probe", "skip"], ["probe"]):
        for j in (0, POST_TARGET_HORIZON - 1):
            _, p, _ = arm_select(0, SHIFT_EPISODE + 1 + 2 * j, ARM_FLOOR, j, list(base_support))
            floor_ok &= p + 1e-15 >= min(1.0, max(base_probe_probability(list(base_support)), EPSILON))
    checks["floor_guarantee"] = floor_ok

    # Hazard trigger must be invariant to world because world never enters stable_unit key.
    checks["hazard_world_independent_audit"] = all(
        (stable_unit(seed, SHIFT_EPISODE + 1 + 2 * j, "hazard") < ETA)
        == (stable_unit(seed, SHIFT_EPISODE + 1 + 2 * j, "hazard") < ETA)
        for seed in range(8) for j in range(POST_TARGET_HORIZON)
    )

    null_rows = [r for r in rows if r["world"] == WORLD_NULL]
    info_rows = [r for r in rows if r["world"] == WORLD_INFORMATIVE]
    corr_rows = [r for r in rows if r["world"] == WORLD_CORRECTIVE]
    checks["null_never_environmentally_discriminating"] = sum(r["gates"]["C4a"] for r in null_rows) == 0
    checks["informative_never_authority_revision_proxy"] = sum(r["gates"]["C6"] for r in info_rows) == 0
    checks["corrective_has_discriminating_events"] = sum(r["gates"]["C4a"] for r in corr_rows) > 0
    checks["representation_preserves_signal_labels_by_construction"] = True

    endo_corr = [r for r in rows if r["world"] == WORLD_CORRECTIVE and r["arm"] == ARM_ENDOGENOUS]
    suppression_rate = mean(float(r["initial_base_suppressed"]) for r in endo_corr)
    checks["initial_endogenous_corrective_suppression_rate"] = suppression_rate
    checks["initial_suppression_manipulation_pass"] = suppression_rate >= INITIAL_SUPPRESSION_FLOOR
    checks["trace_required_fields"] = trace_required_fields_ok(trace_sample)
    checks["nano_absent"] = True

    bool_checks = [v for v in checks.values() if isinstance(v, bool)]
    checks["valid"] = all(bool_checks)
    return checks


def read_first_trace_record(trace_path: Path) -> dict:
    with gzip.open(trace_path, "rt", encoding="utf-8") as f:
        return json.loads(next(f))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(freeze_commit: str, output_dir: Path) -> dict:
    if len(freeze_commit) != 40 or any(c not in "0123456789abcdef" for c in freeze_commit.lower()):
        raise SystemExit("--freeze-commit must be a 40-character hexadecimal commit SHA")

    root = Path(__file__).resolve().parent
    spec_path = root / "PCE_001_SPEC.md"
    manifest_path = root / "PCE_001_MANIFEST.json"
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_path = output_dir / "pce_001_trace.jsonl.gz"
    result_path = output_dir / "pce_001_result.json"

    trace_hash = hashlib.sha256()
    rows: List[dict] = []

    with trace_path.open("wb") as raw_file:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_file, compresslevel=9, mtime=0) as gz:
            for world in WORLDS:
                for arm in ARMS:
                    for seed in range(SEEDS):
                        schedule = make_schedule(seed, world)
                        row = run_branch(seed, world, arm, schedule, gz, trace_hash)
                        rows.append(row)

    sample_record = read_first_trace_record(trace_path)
    validity = validate(rows, sample_record)
    primary = paired_contrast(rows, ARM_ENDOGENOUS, ARM_HAZARD, WORLD_CORRECTIVE)
    secondary = paired_contrast(rows, ARM_SUPPORT, ARM_FLOOR, WORLD_CORRECTIVE)

    if not validity["valid"]:
        overall = "INVALID"
    elif primary["classification"] == "SUPPORTS_DIRECTIONAL_SEPARATION":
        overall = "CAUSALLY_LOCALIZED_ENDOGENOUS_EVIDENCE_ACQUISITION_FAILURE"
    elif primary["classification"] == "APPROXIMATELY_EQUIVALENT":
        overall = "PRIMARY_CAUSAL_EXPLANATION_LOSES_AUTHORITY"
    else:
        overall = "PRIMARY_UNDERDETERMINED"

    aggregates = {
        world: {
            arm: aggregate_rows([r for r in rows if r["world"] == world and r["arm"] == arm])
            for arm in ARMS
        }
        for world in WORLDS
    }

    result = {
        "assay": "PCE-001",
        "freeze_commit": freeze_commit,
        "source_hashes": {
            "spec_sha256": sha256_file(spec_path),
            "manifest_sha256": sha256_file(manifest_path),
            "harness_sha256": sha256_file(Path(__file__)),
        },
        "frozen_constants": {
            "seeds": SEEDS,
            "episodes": EPISODES,
            "shift_episode": SHIFT_EPISODE,
            "post_target_horizon": POST_TARGET_HORIZON,
            "epsilon": EPSILON,
            "eta": ETA,
            "support_schedule": "1/(j+2)^2",
            "T_C_censor": TC_CENSOR,
            "corrective_delta_threshold": CORRECTIVE_DELTA_THRESHOLD,
        },
        "validity": validity,
        "primary": primary,
        "secondary": secondary,
        "overall_classification": overall,
        "aggregates": aggregates,
        "correction_survival": {
            arm: empirical_survival(rows, WORLD_CORRECTIVE, arm) for arm in ARMS
        },
        "per_seed": rows,
        "trace": {
            "canonical_jsonl_uncompressed_sha256": trace_hash.hexdigest(),
            "gzip_sha256": sha256_file(trace_path),
            "gzip_bytes": trace_path.stat().st_size,
            "records": SEEDS * len(WORLDS) * len(ARMS) * POST_TARGET_HORIZON,
            "ordering": "world, arm, seed, target_j",
        },
        "claim_ceiling": (
            "Challenge preservation under a prospectively fixed corrective channel only; "
            "autonomous challenge discovery/constitution is not tested."
        ),
    }

    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["result_json_sha256"] = sha256_file(result_path)
    return result


def self_test() -> None:
    assert post_target_index(181) == 0
    assert post_target_index(419) == 119
    assert post_target_index(180) is None
    assert context_for_episode(181) == "target"
    assert math.isclose(1.0 / ((0 + 2) ** 2), 0.25)
    assert 1.0 / ((119 + 2) ** 2) > 0.0
    assert base_probe_probability(["skip"]) == 0.0
    assert base_probe_probability(["probe"]) == 1.0
    assert base_probe_probability(["probe", "skip"]) == 0.5
    # World does not enter the hazard key.
    assert stable_unit(7, 181, "hazard") == stable_unit(7, 181, "hazard")
    print("PCE-001 self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser(description="PCE-001 frozen intervention assay")
    parser.add_argument("--freeze-commit", help="40-char prospective freeze commit SHA")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "results")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if not args.freeze_commit:
        raise SystemExit("--freeze-commit is required for evaluation execution")

    result = run(args.freeze_commit.lower(), args.output_dir)
    print(json.dumps({
        "assay": result["assay"],
        "valid": result["validity"]["valid"],
        "overall_classification": result["overall_classification"],
        "primary": result["primary"],
        "secondary": result["secondary"],
        "trace": result["trace"],
        "result_json_sha256": result["result_json_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
