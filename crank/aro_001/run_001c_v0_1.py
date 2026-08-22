#!/usr/bin/env python3
"""ARO-001c v0.1 frozen executable.

Do not edit after observing v0.1 results. Any change creates a new version.
"""

from __future__ import annotations

import json
from itertools import product

import numpy as np

CONTEXTS = ("W1_G", "W1_I", "W2_XOR", "W3_VALUE")
FIRST_ACTIONS = ("SELECT_G", "SELECT_I", "COMPOSE_GI", "COMPOSE_GIS", "PROBE_S")
SECOND_ACTIONS = ("SELECT_G", "SELECT_I", "COMPOSE_GI")
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


def observe_second(action: str, observed: dict[str, int], g: int, i: int) -> dict[str, int]:
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


def choose_eps_greedy(q_values: np.ndarray, eps: float, rng: np.random.Generator) -> int:
    if rng.random() < eps:
        return int(rng.integers(len(q_values)))
    max_q = np.max(q_values)
    ties = np.flatnonzero(np.isclose(q_values, max_q))
    return int(rng.choice(ties))


def greedy_index(q_values: np.ndarray) -> int:
    return int(np.argmax(q_values))


def run_training_episode(
    q_world: float,
    context_idx: int,
    q1: np.ndarray,
    q2: np.ndarray,
    eps: float,
    rng: np.random.Generator,
) -> tuple[str, str | None, bool]:
    context = CONTEXTS[context_idx]
    g, i, s = [int(x) for x in rng.integers(0, 2, size=3)]
    b = int(rng.random() < q_world) if context == "W3_VALUE" else 0

    proposed_idx = choose_eps_greedy(q1[context_idx], eps, rng)
    proposed = FIRST_ACTIONS[proposed_idx]

    forced = False
    if context == "W3_VALUE" and rng.random() < FORCED_PROBE_RATE:
        a1 = "PROBE_S"
        a1_idx = FIRST_ACTIONS.index(a1)
        forced = True
    else:
        a1 = proposed
        a1_idx = proposed_idx

    observed, terminal = observe_first(a1, g, i, s)
    total_cost = COST[a1]
    a2 = None
    a2_idx = None

    if not terminal:
        a2_idx = choose_eps_greedy(q2[context_idx, s], eps, rng)
        a2 = SECOND_ACTIONS[a2_idx]
        observed = observe_second(a2, observed, g, i)
        total_cost += COST[a2]

    y = target(context, g, i, s, b)
    pred = bayes_predict(context, q_world, observed)
    loss = float(pred != y)
    reward = -(loss + LAMBDA * total_cost)

    if a2_idx is not None:
        q2[context_idx, s, a2_idx] += ALPHA_Q * (reward - q2[context_idx, s, a2_idx])
    q1[context_idx, a1_idx] += ALPHA_Q * (reward - q1[context_idx, a1_idx])

    return a1, a2, forced


def train_condition(q_world: float, seed: int) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    rng = np.random.default_rng(seed)
    q1 = np.zeros((len(CONTEXTS), len(FIRST_ACTIONS)), dtype=float)
    q2 = np.zeros((len(CONTEXTS), 2, len(SECOND_ACTIONS)), dtype=float)
    counts = {"w3_training_count": 0, "forced_probe_count": 0, "executed_probe_count": 0}

    for ep in range(TRAIN_EPISODES):
        frac = ep / max(1, TRAIN_EPISODES - 1)
        eps = EPS_START + frac * (EPS_END - EPS_START)
        context_idx = int(rng.integers(len(CONTEXTS)))
        a1, _, forced = run_training_episode(q_world, context_idx, q1, q2, eps, rng)
        if CONTEXTS[context_idx] == "W3_VALUE":
            counts["w3_training_count"] += 1
            if forced:
                counts["forced_probe_count"] += 1
            if a1 == "PROBE_S":
                counts["executed_probe_count"] += 1

    return q1, q2, counts


def expected_loss_for_policy(
    context: str,
    q_world: float,
    first_action: str,
    second_policy: dict[int, str] | None = None,
) -> float:
    total = 0.0
    for g, i, s in product((0, 1), repeat=3):
        observed, terminal = observe_first(first_action, g, i, s)
        if not terminal:
            if second_policy is None:
                raise RuntimeError("Second policy required after PROBE_S")
            a2 = second_policy[s]
            observed = observe_second(a2, observed, g, i)

        pred = bayes_predict(context, q_world, observed)

        if context == "W3_VALUE":
            for b in (0, 1):
                wb = latent_weight(context, q_world, b)
                y = target(context, g, i, s, b)
                total += (1.0 / 8.0) * wb * float(pred != y)
        else:
            y = target(context, g, i, s, 0)
            total += (1.0 / 8.0) * float(pred != y)
    return float(total)


def expected_cost_for_policy(first_action: str, second_policy: dict[int, str] | None = None) -> float:
    if first_action != "PROBE_S":
        return COST[first_action]
    if second_policy is None:
        raise RuntimeError("Second policy required")
    return COST["PROBE_S"] + 0.5 * COST[second_policy[0]] + 0.5 * COST[second_policy[1]]


def exact_true_voi(q_world: float) -> dict[str, object]:
    no_probe = []
    for a1 in FIRST_ACTIONS:
        if a1 == "PROBE_S":
            continue
        loss = expected_loss_for_policy("W3_VALUE", q_world, a1)
        cost = expected_cost_for_policy(a1)
        J = loss + LAMBDA * cost
        no_probe.append((J, a1, loss, cost))
    best_no = min(no_probe, key=lambda x: (x[0], FIRST_ACTIONS.index(x[1])))

    probe_candidates = []
    for a0 in SECOND_ACTIONS:
        for a1 in SECOND_ACTIONS:
            pol = {0: a0, 1: a1}
            loss = expected_loss_for_policy("W3_VALUE", q_world, "PROBE_S", pol)
            cost = expected_cost_for_policy("PROBE_S", pol)
            J = loss + LAMBDA * cost
            probe_candidates.append((J, (a0, a1), loss, cost))
    best_probe = min(
        probe_candidates,
        key=lambda x: (
            x[0],
            SECOND_ACTIONS.index(x[1][0]),
            SECOND_ACTIONS.index(x[1][1]),
        ),
    )

    return {
        "q": q_world,
        "best_no_probe": {
            "action": best_no[1],
            "loss": best_no[2],
            "cost": best_no[3],
            "J": best_no[0],
        },
        "best_probe": {
            "branches": {"S0": best_probe[1][0], "S1": best_probe[1][1]},
            "loss": best_probe[2],
            "cost": best_probe[3],
            "J": best_probe[0],
        },
        "DeltaV_true": best_no[0] - best_probe[0],
    }


def learned_w3_readout(q1: np.ndarray, q2: np.ndarray) -> dict[str, object]:
    c = CONTEXTS.index("W3_VALUE")
    probe_idx = FIRST_ACTIONS.index("PROBE_S")
    nonprobe_idx = [j for j, a in enumerate(FIRST_ACTIONS) if a != "PROBE_S"]
    best_nonprobe_q = float(np.max(q1[c, nonprobe_idx]))
    probe_q = float(q1[c, probe_idx])
    dv_hat = probe_q - best_nonprobe_q

    first = FIRST_ACTIONS[greedy_index(q1[c])]
    branches = {
        "S0": SECOND_ACTIONS[greedy_index(q2[c, 0])],
        "S1": SECOND_ACTIONS[greedy_index(q2[c, 1])],
    }
    branch_full = branches["S0"] == "SELECT_G" and branches["S1"] == "SELECT_I"
    return {
        "DeltaV_hat": dv_hat,
        "probe_q": probe_q,
        "best_nonprobe_q": best_nonprobe_q,
        "greedy_first": first,
        "probe_preferred": first == "PROBE_S",
        "branches": branches,
        "branch_full": branch_full,
    }


def expected_greedy_metrics(q_world: float, q1: np.ndarray, q2: np.ndarray) -> dict[str, float]:
    losses = []
    costs = []
    weights = []
    for context_idx, context in enumerate(CONTEXTS):
        a1 = FIRST_ACTIONS[greedy_index(q1[context_idx])]
        second_policy = None
        if a1 == "PROBE_S":
            second_policy = {
                0: SECOND_ACTIONS[greedy_index(q2[context_idx, 0])],
                1: SECOND_ACTIONS[greedy_index(q2[context_idx, 1])],
            }
        loss = expected_loss_for_policy(context, q_world, a1, second_policy)
        cost = expected_cost_for_policy(a1, second_policy)
        losses.append(loss)
        costs.append(cost)
        weights.append(0.25)
    mean_loss = float(np.dot(weights, losses))
    mean_cost = float(np.dot(weights, costs))
    return {
        "loss": mean_loss,
        "cost": mean_cost,
        "J": mean_loss + LAMBDA * mean_cost,
    }


def exact_full_oracle_metrics(q_world: float) -> dict[str, float]:
    w1g = (0.0, 1.0)
    w1i = (0.0, 1.0)
    w2 = (0.0, 1.6)
    voi = exact_true_voi(q_world)
    if voi["best_probe"]["J"] < voi["best_no_probe"]["J"] - 1e-15:
        w3_loss = float(voi["best_probe"]["loss"])
        w3_cost = float(voi["best_probe"]["cost"])
    else:
        w3_loss = float(voi["best_no_probe"]["loss"])
        w3_cost = float(voi["best_no_probe"]["cost"])
    loss = 0.25 * (w1g[0] + w1i[0] + w2[0] + w3_loss)
    cost = 0.25 * (w1g[1] + w1i[1] + w2[1] + w3_cost)
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
    sx = float(np.std(rx))
    sy = float(np.std(ry))
    if sx == 0.0 or sy == 0.0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def main() -> None:
    condition_results: dict[str, object] = {}
    true_values = []
    learned_means = []
    probe_rates = []
    branch_rates = []

    for q_world in Q_GRID:
        key = f"{q_world:.2f}"
        truth = exact_true_voi(q_world)
        true_values.append(float(truth["DeltaV_true"]))

        rows = []
        for seed in range(N_SEEDS):
            q1, q2, counts = train_condition(q_world, seed)
            readout = learned_w3_readout(q1, q2)
            learned_metrics = expected_greedy_metrics(q_world, q1, q2)
            oracle_metrics = exact_full_oracle_metrics(q_world)
            rows.append({
                "DeltaV_hat": float(readout["DeltaV_hat"]),
                "probe_preferred": bool(readout["probe_preferred"]),
                "branch_full": bool(readout["branch_full"]),
                "loss": learned_metrics["loss"],
                "cost": learned_metrics["cost"],
                "J": learned_metrics["J"],
                "regret_J": learned_metrics["J"] - oracle_metrics["J"],
                "forced_probe_count": float(counts["forced_probe_count"]),
                "executed_probe_count": float(counts["executed_probe_count"]),
                "w3_training_count": float(counts["w3_training_count"]),
            })

        dvhat_summary = summarize([r["DeltaV_hat"] for r in rows])
        probe_rate = float(np.mean([r["probe_preferred"] for r in rows]))
        branch_rate = float(np.mean([r["branch_full"] for r in rows]))
        learned_means.append(dvhat_summary["mean"])
        probe_rates.append(probe_rate)
        branch_rates.append(branch_rate)

        condition_results[key] = {
            "truth": truth,
            "matched_nuisance_empty_loss": empty_information_loss(q_world),
            "learned": {
                "DeltaV_hat": dvhat_summary,
                "probe_preference_seed_rate": probe_rate,
                "branch_full_seed_rate": branch_rate,
                "loss": summarize([r["loss"] for r in rows]),
                "cost": summarize([r["cost"] for r in rows]),
                "J": summarize([r["J"] for r in rows]),
                "regret_J": summarize([r["regret_J"] for r in rows]),
                "forced_probe_count": summarize([r["forced_probe_count"] for r in rows]),
                "executed_probe_count": summarize([r["executed_probe_count"] for r in rows]),
                "w3_training_count": summarize([r["w3_training_count"] for r in rows]),
            },
        }

    rho_q = spearman(true_values, learned_means)
    rho_probe = spearman(true_values, probe_rates)

    truth_gate = all(
        np.isclose(
            condition_results[key]["truth"]["DeltaV_true"],
            EXPECTED_TRUE_DV[key],
            atol=1e-12,
            rtol=0.0,
        )
        for key in EXPECTED_TRUE_DV
    )
    nuisance_gate = all(
        np.isclose(condition_results[f"{q:.2f}"]["matched_nuisance_empty_loss"], 0.5, atol=1e-12, rtol=0.0)
        for q in Q_GRID
    )
    continuation_gate = all(rate >= 0.95 for rate in branch_rates)

    primary = {
        "R0_continuation_branch_rate_ge_0_95_every_q": continuation_gate,
        "R1_true_DeltaV_vector_matches_freeze": truth_gate,
        "R2_rho_Q_ge_0_90": rho_q >= 0.90,
        "R3_rho_probe_ge_0_90": rho_probe >= 0.90,
    }
    primary["PRIMARY_RANK_ORDERING_PASS"] = all(primary.values())

    neg_keys = ("0.60", "0.70", "0.75")
    pos_keys = ("0.85", "0.90")
    mean_hat = {k: condition_results[k]["learned"]["DeltaV_hat"]["mean"] for k in condition_results}
    p_probe = {k: condition_results[k]["learned"]["probe_preference_seed_rate"] for k in condition_results}

    calibration = {
        "C1_negative_mean_DeltaV_hat_below_zero": all(mean_hat[k] < 0.0 for k in neg_keys),
        "C2_zero_mean_DeltaV_hat_abs_le_0_02": abs(mean_hat["0.80"]) <= 0.02,
        "C3_positive_mean_DeltaV_hat_above_zero": all(mean_hat[k] > 0.0 for k in pos_keys),
        "C4_negative_probe_rates_below_0_50": all(p_probe[k] < 0.50 for k in neg_keys),
        "C5_positive_probe_rates_above_0_50": all(p_probe[k] > 0.50 for k in pos_keys),
        "C6_zero_probe_rate_between_0_20_and_0_80": 0.20 <= p_probe["0.80"] <= 0.80,
    }
    calibration["SECONDARY_CALIBRATION_PASS"] = all(calibration.values())

    summary = {
        "status": "RUN_COMPLETE",
        "protocol": "ARO_001C_PROBE_VALUE_CALIBRATION_V0_1",
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
        },
        "expected_true_DeltaV": EXPECTED_TRUE_DV,
        "condition_results": condition_results,
        "curve_metrics": {
            "rho_Q": rho_q,
            "rho_probe": rho_probe,
            "true_DeltaV": true_values,
            "mean_DeltaV_hat": learned_means,
            "probe_preference_seed_rate": probe_rates,
            "branch_full_seed_rate": branch_rates,
        },
        "gates": {
            "matched_nuisance_empty_loss_exact_half_every_q": nuisance_gate,
            "primary": primary,
            "secondary_calibration": calibration,
        },
        "identification_note": (
            "Final evaluation is greedy. Probe behavior is therefore a thresholded readout "
            "of learned first-stage Q values, not an independently identified policy-conversion layer."
        ),
    }

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
