#!/usr/bin/env python3
"""ARO-001d v0.1 frozen executable.

Fixed-continuation VOI assay. Do not edit after observing v0.1 results.
"""

from __future__ import annotations

import json
from itertools import product

import numpy as np

CONTEXTS = ("W1_G", "W1_I", "W2_XOR", "W3_VALUE")
FIRST_ACTIONS = ("SELECT_G", "SELECT_I", "COMPOSE_GI", "COMPOSE_GIS", "PROBE_S")
Q_GRID = (0.60, 0.70, 0.75, 0.80, 0.85, 0.90)

COST = {
    "SELECT_G": 1.0,
    "SELECT_I": 1.0,
    "COMPOSE_GI": 1.6,
    "COMPOSE_GIS": 2.3,
    "PROBE_S": 1.0,
}

LAMBDA = 0.15
N_SEEDS = 256
TRAIN_EPISODES = 4000
ALPHA_Q = 0.10
GAMMA = 1.0
EPS_START = 0.20
EPS_END = 0.01
FORCED_PROBE_RATE = 0.25

EXPECTED_TRUE_DV = {
    "0.60": -0.100,
    "0.70": -0.050,
    "0.75": -0.025,
    "0.80": 0.000,
    "0.85": 0.025,
    "0.90": 0.045,
}


def target(context: str, g: int, i: int, s: int, b: int) -> int:
    if context == "W1_G":
        return g
    if context == "W1_I":
        return i
    if context == "W2_XOR":
        return g ^ i
    if context == "W3_VALUE":
        if b == 0:
            return g
        return g if s == 0 else i
    raise ValueError(context)


def latent_weight(context: str, q: float, b: int) -> float:
    if context != "W3_VALUE":
        return 1.0 if b == 0 else 0.0
    return (1.0 - q) if b == 0 else q


def posterior_y_prob(context: str, q: float, observed: dict[str, int]) -> float:
    num = 0.0
    den = 0.0
    for g, i, s in product((0, 1), repeat=3):
        latent = {"G": g, "I": i, "S": s}
        if not all(latent[k] == v for k, v in observed.items()):
            continue
        for b in (0, 1):
            w = latent_weight(context, q, b)
            if w == 0.0:
                continue
            num += w * target(context, g, i, s, b)
            den += w
    if den <= 0.0:
        raise RuntimeError("No latent state consistent with observations")
    return num / den


def bayes_predict(context: str, q: float, observed: dict[str, int]) -> int:
    p = posterior_y_prob(context, q, observed)
    return 1 if p > 0.5 else 0


def observe_first(action: str, g: int, i: int, s: int) -> tuple[dict[str, int], bool]:
    if action == "SELECT_G":
        return {"G": g}, True
    if action == "SELECT_I":
        return {"I": i}, True
    if action == "COMPOSE_GI":
        return {"G": g, "I": i}, True
    if action == "COMPOSE_GIS":
        return {"G": g, "I": i, "S": s}, True
    if action == "PROBE_S":
        return {"S": s}, False
    raise ValueError(action)


def fixed_continuation(context: str, s: int) -> str:
    # Evaluator-fixed optimal continuation. W3_VALUE is the scientific target;
    # the other entries make PROBE_S total under unchanged first-stage exploration.
    if context == "W1_G":
        return "SELECT_G"
    if context == "W1_I":
        return "SELECT_I"
    if context == "W2_XOR":
        return "COMPOSE_GI"
    if context == "W3_VALUE":
        return "SELECT_G" if s == 0 else "SELECT_I"
    raise ValueError(context)


def observe_continuation(action: str, observed: dict[str, int], g: int, i: int) -> dict[str, int]:
    out = dict(observed)
    if action == "SELECT_G":
        out["G"] = g
    elif action == "SELECT_I":
        out["I"] = i
    elif action == "COMPOSE_GI":
        out["G"] = g
        out["I"] = i
    else:
        raise ValueError(action)
    return out


def choose_eps_greedy(values: np.ndarray, eps: float, rng: np.random.Generator) -> int:
    if rng.random() < eps:
        return int(rng.integers(len(values)))
    max_v = np.max(values)
    ties = np.flatnonzero(np.isclose(values, max_v))
    return int(rng.choice(ties))


def greedy_index(values: np.ndarray) -> int:
    return int(np.argmax(values))


def execute_action(
    context: str,
    q_world: float,
    action: str,
    g: int,
    i: int,
    s: int,
    b: int,
) -> tuple[float, float]:
    observed, terminal = observe_first(action, g, i, s)
    cost = COST[action]
    if not terminal:
        a2 = fixed_continuation(context, s)
        observed = observe_continuation(a2, observed, g, i)
        cost += COST[a2]
    y = target(context, g, i, s, b)
    pred = bayes_predict(context, q_world, observed)
    return float(pred != y), float(cost)


def run_training_episode(
    q_world: float,
    context_idx: int,
    q1: np.ndarray,
    eps: float,
    rng: np.random.Generator,
) -> tuple[str, bool]:
    context = CONTEXTS[context_idx]
    g, i, s = [int(x) for x in rng.integers(0, 2, size=3)]
    b = int(rng.random() < q_world) if context == "W3_VALUE" else 0

    proposed_idx = choose_eps_greedy(q1[context_idx], eps, rng)
    proposed = FIRST_ACTIONS[proposed_idx]
    forced = False
    if context == "W3_VALUE" and rng.random() < FORCED_PROBE_RATE:
        action = "PROBE_S"
        action_idx = FIRST_ACTIONS.index(action)
        forced = True
    else:
        action = proposed
        action_idx = proposed_idx

    loss, cost = execute_action(context, q_world, action, g, i, s, b)
    reward = -(loss + LAMBDA * cost)
    q1[context_idx, action_idx] += ALPHA_Q * (reward - q1[context_idx, action_idx])
    return action, forced


def train_condition(q_world: float, seed: int) -> tuple[np.ndarray, dict[str, int]]:
    rng = np.random.default_rng(seed)
    q1 = np.zeros((len(CONTEXTS), len(FIRST_ACTIONS)), dtype=float)
    counts = {"w3_training_count": 0, "forced_probe_count": 0, "executed_probe_count": 0}

    for ep in range(TRAIN_EPISODES):
        frac = ep / max(1, TRAIN_EPISODES - 1)
        eps = EPS_START + frac * (EPS_END - EPS_START)
        context_idx = int(rng.integers(len(CONTEXTS)))
        action, forced = run_training_episode(q_world, context_idx, q1, eps, rng)
        if CONTEXTS[context_idx] == "W3_VALUE":
            counts["w3_training_count"] += 1
            if forced:
                counts["forced_probe_count"] += 1
            if action == "PROBE_S":
                counts["executed_probe_count"] += 1
    return q1, counts


def expected_action_loss_cost(context: str, q_world: float, action: str) -> tuple[float, float]:
    loss_total = 0.0
    cost_total = 0.0
    for g, i, s in product((0, 1), repeat=3):
        if context == "W3_VALUE":
            for b in (0, 1):
                wb = latent_weight(context, q_world, b)
                loss, cost = execute_action(context, q_world, action, g, i, s, b)
                loss_total += (1.0 / 8.0) * wb * loss
                cost_total += (1.0 / 8.0) * wb * cost
        else:
            loss, cost = execute_action(context, q_world, action, g, i, s, 0)
            loss_total += (1.0 / 8.0) * loss
            cost_total += (1.0 / 8.0) * cost
    return float(loss_total), float(cost_total)


def exact_true_voi(q_world: float) -> dict[str, object]:
    candidates = []
    for action in FIRST_ACTIONS:
        loss, cost = expected_action_loss_cost("W3_VALUE", q_world, action)
        J = loss + LAMBDA * cost
        candidates.append((J, action, loss, cost))
    probe = next(x for x in candidates if x[1] == "PROBE_S")
    nonprobe = min(
        (x for x in candidates if x[1] != "PROBE_S"),
        key=lambda x: (x[0], FIRST_ACTIONS.index(x[1])),
    )
    return {
        "q": q_world,
        "best_nonprobe": {"action": nonprobe[1], "loss": nonprobe[2], "cost": nonprobe[3], "J": nonprobe[0]},
        "fixed_probe": {
            "branches": {"S0": "SELECT_G", "S1": "SELECT_I"},
            "loss": probe[2],
            "cost": probe[3],
            "J": probe[0],
        },
        "DeltaV_true": nonprobe[0] - probe[0],
    }


def learned_w3_readout(q1: np.ndarray) -> dict[str, object]:
    c = CONTEXTS.index("W3_VALUE")
    probe_idx = FIRST_ACTIONS.index("PROBE_S")
    nonprobe_idx = [j for j, a in enumerate(FIRST_ACTIONS) if a != "PROBE_S"]
    best_nonprobe_q = float(np.max(q1[c, nonprobe_idx]))
    probe_q = float(q1[c, probe_idx])
    return {
        "DeltaV_hat": probe_q - best_nonprobe_q,
        "probe_q": probe_q,
        "best_nonprobe_q": best_nonprobe_q,
        "greedy_first": FIRST_ACTIONS[greedy_index(q1[c])],
        "probe_preferred": FIRST_ACTIONS[greedy_index(q1[c])] == "PROBE_S",
    }


def expected_greedy_metrics(q_world: float, q1: np.ndarray) -> dict[str, float]:
    losses = []
    costs = []
    for context_idx, context in enumerate(CONTEXTS):
        action = FIRST_ACTIONS[greedy_index(q1[context_idx])]
        loss, cost = expected_action_loss_cost(context, q_world, action)
        losses.append(loss)
        costs.append(cost)
    mean_loss = float(np.mean(losses))
    mean_cost = float(np.mean(costs))
    return {"loss": mean_loss, "cost": mean_cost, "J": mean_loss + LAMBDA * mean_cost}


def exact_full_oracle_metrics(q_world: float) -> dict[str, float]:
    choices = []
    for context in CONTEXTS:
        rows = []
        for action in FIRST_ACTIONS:
            loss, cost = expected_action_loss_cost(context, q_world, action)
            rows.append((loss + LAMBDA * cost, loss, cost, action))
        choices.append(min(rows, key=lambda x: (x[0], FIRST_ACTIONS.index(x[3]))))
    loss = float(np.mean([x[1] for x in choices]))
    cost = float(np.mean([x[2] for x in choices]))
    return {"loss": loss, "cost": cost, "J": loss + LAMBDA * cost}


def empty_information_loss(q_world: float) -> float:
    p = posterior_y_prob("W3_VALUE", q_world, {})
    return float(min(p, 1.0 - p))


def summarize(values: list[float]) -> dict[str, float]:
    a = np.asarray(values, dtype=float)
    return {
        "mean": float(np.mean(a)),
        "sd": float(np.std(a)),
        "min": float(np.min(a)),
        "p05": float(np.quantile(a, 0.05)),
        "median": float(np.median(a)),
        "p95": float(np.quantile(a, 0.95)),
        "max": float(np.max(a)),
    }


def average_ranks(values: list[float]) -> np.ndarray:
    a = np.asarray(values, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    pos = 0
    while pos < len(a):
        end = pos + 1
        while end < len(a) and np.isclose(a[order[end]], a[order[pos]], atol=1e-15, rtol=0.0):
            end += 1
        avg = 0.5 * ((pos + 1) + end)
        ranks[order[pos:end]] = avg
        pos = end
    return ranks


def spearman(x: list[float], y: list[float]) -> float:
    rx = average_ranks(x)
    ry = average_ranks(y)
    if np.std(rx) == 0.0 or np.std(ry) == 0.0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def ols(x: list[float], y: list[float]) -> dict[str, float]:
    xa = np.asarray(x, dtype=float)
    ya = np.asarray(y, dtype=float)
    X = np.column_stack([xa, np.ones_like(xa)])
    slope, intercept = np.linalg.lstsq(X, ya, rcond=None)[0]
    pred = slope * xa + intercept
    ss_res = float(np.sum((ya - pred) ** 2))
    ss_tot = float(np.sum((ya - np.mean(ya)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0.0 else float("nan")
    zero = float(-intercept / slope) if not np.isclose(slope, 0.0) else float("nan")
    return {"slope": float(slope), "intercept": float(intercept), "r2": r2, "zero_crossing": zero}


def main() -> None:
    condition_results: dict[str, object] = {}
    true_values: list[float] = []
    learned_means: list[float] = []
    probe_rates: list[float] = []

    for q_world in Q_GRID:
        key = f"{q_world:.2f}"
        truth = exact_true_voi(q_world)
        true_values.append(float(truth["DeltaV_true"]))
        oracle = exact_full_oracle_metrics(q_world)
        rows = []

        for seed in range(N_SEEDS):
            q1, counts = train_condition(q_world, seed)
            readout = learned_w3_readout(q1)
            metrics = expected_greedy_metrics(q_world, q1)
            rows.append({
                **readout,
                **counts,
                "loss": metrics["loss"],
                "cost": metrics["cost"],
                "J": metrics["J"],
                "regret_J": metrics["J"] - oracle["J"],
            })

        dv_summary = summarize([float(r["DeltaV_hat"]) for r in rows])
        probe_rate = float(np.mean([bool(r["probe_preferred"]) for r in rows]))
        learned_means.append(dv_summary["mean"])
        probe_rates.append(probe_rate)

        condition_results[key] = {
            "truth": truth,
            "matched_nuisance_empty_loss": empty_information_loss(q_world),
            "learned": {
                "DeltaV_hat": dv_summary,
                "probe_preference_seed_rate": probe_rate,
                "loss": summarize([float(r["loss"]) for r in rows]),
                "cost": summarize([float(r["cost"]) for r in rows]),
                "J": summarize([float(r["J"]) for r in rows]),
                "regret_J": summarize([float(r["regret_J"]) for r in rows]),
                "forced_probe_count": summarize([float(r["forced_probe_count"]) for r in rows]),
                "executed_probe_count": summarize([float(r["executed_probe_count"]) for r in rows]),
                "w3_training_count": summarize([float(r["w3_training_count"]) for r in rows]),
            },
        }

    rho_q = spearman(true_values, learned_means)
    regression = ols(true_values, learned_means)

    truth_gate = all(
        np.isclose(condition_results[key]["truth"]["DeltaV_true"], EXPECTED_TRUE_DV[key], atol=1e-12, rtol=0.0)
        for key in EXPECTED_TRUE_DV
    )
    nuisance_gate = all(
        np.isclose(condition_results[f"{q:.2f}"]["matched_nuisance_empty_loss"], 0.5, atol=1e-12, rtol=0.0)
        for q in Q_GRID
    )
    fixed_continuation_gate = True

    mean_hat = {k: float(condition_results[k]["learned"]["DeltaV_hat"]["mean"]) for k in condition_results}
    p_probe = {k: float(condition_results[k]["learned"]["probe_preference_seed_rate"]) for k in condition_results}
    neg_keys = ("0.60", "0.70", "0.75")
    pos_keys = ("0.85", "0.90")

    primary = {
        "G0_fixed_continuation_probability_one": fixed_continuation_gate,
        "G1_true_DeltaV_vector_matches_freeze": truth_gate,
        "G2_empty_information_loss_exact_half_every_q": nuisance_gate,
        "V1_rho_Q_ge_0_90": rho_q >= 0.90,
        "V2_slope_in_0_75_1_25": 0.75 <= regression["slope"] <= 1.25,
        "V3_abs_intercept_le_0_020": abs(regression["intercept"]) <= 0.020,
        "V4_abs_zero_crossing_le_0_020": abs(regression["zero_crossing"]) <= 0.020,
        "V5_negative_mean_DeltaV_hat_below_zero": all(mean_hat[k] < 0.0 for k in neg_keys),
        "V6_positive_mean_DeltaV_hat_above_zero": all(mean_hat[k] > 0.0 for k in pos_keys),
    }
    primary["PRIMARY_VOI_CALIBRATION_PASS"] = all(primary.values())

    behavior = {
        "B1_negative_probe_rates_below_0_50": all(p_probe[k] < 0.50 for k in neg_keys),
        "B2_positive_probe_rates_above_0_50": all(p_probe[k] > 0.50 for k in pos_keys),
        "B3_zero_probe_rate_between_0_20_and_0_80": 0.20 <= p_probe["0.80"] <= 0.80,
    }
    behavior["SECONDARY_BEHAVIORAL_CALIBRATION_PASS"] = all(behavior.values())

    summary = {
        "status": "RUN_COMPLETE",
        "protocol": "ARO_001D_FIXED_CONTINUATION_VOI_V0_1",
        "variant": "ARO-A",
        "constants": {
            "q_grid": list(Q_GRID),
            "seeds_per_q": N_SEEDS,
            "training_episodes_per_seed": TRAIN_EPISODES,
            "lambda": LAMBDA,
            "alpha_Q": ALPHA_Q,
            "gamma": GAMMA,
            "epsilon_start": EPS_START,
            "epsilon_end": EPS_END,
            "forced_probe_rate_conditional_W3": FORCED_PROBE_RATE,
            "fixed_continuation": {"W3_VALUE_S0": "SELECT_G", "W3_VALUE_S1": "SELECT_I"},
        },
        "expected_true_DeltaV": EXPECTED_TRUE_DV,
        "condition_results": condition_results,
        "curve_metrics": {
            "rho_Q": rho_q,
            "true_DeltaV": true_values,
            "mean_DeltaV_hat": learned_means,
            "probe_preference_seed_rate": probe_rates,
            "ols": regression,
        },
        "gates": {
            "primary": primary,
            "secondary_behavioral_calibration": behavior,
        },
        "identification_note": (
            "Continuation after PROBE_S is evaluator-fixed. Final behavior is greedy and is therefore a "
            "thresholded readout of learned first-stage Q values, not an independently identified policy layer."
        ),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
