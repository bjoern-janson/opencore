#!/usr/bin/env python3
"""ARO-001b v0.1 frozen executable.

Single intervention relative to ARO-001 v0.1:
force PROBE_S on 25% of W3_GATE training episodes.
Second-stage choice remains learned; evaluation is unforced.

Do not edit after observing v0.1b results. Any change creates a new version.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_v0_1 as base

FORCED_PROBE_RATE_W3 = 0.25
FORCE_SEED_OFFSET = 10_000_019
PROBE_IDX = base.FIRST_ACTIONS.index("PROBE_S")
W3_IDX = base.CONTEXTS.index("W3_GATE")


def run_episode_controlled(
    context_idx: int,
    q1: np.ndarray,
    q2: np.ndarray,
    eps: float,
    rng: np.random.Generator,
    force_rng: np.random.Generator,
) -> tuple[float, float, str, str | None, bool]:
    context = base.CONTEXTS[context_idx]
    g, i, s = [int(x) for x in rng.integers(0, 2, size=3)]

    # Preserve the ordinary v0.1 proposal, then apply the single exposure intervention.
    proposed_idx = base.choose_eps_greedy(q1[context_idx], eps, rng)
    forced = bool(context_idx == W3_IDX and force_rng.random() < FORCED_PROBE_RATE_W3)
    a1_idx = PROBE_IDX if forced else proposed_idx
    a1 = base.FIRST_ACTIONS[a1_idx]

    observed, terminal = base.observe_first(a1, g, i, s)
    total_cost = base.COST[a1]
    a2 = None
    a2_idx = None

    if not terminal:
        a2_idx = base.choose_eps_greedy(q2[context_idx, s], eps, rng)
        a2 = base.SECOND_ACTIONS[a2_idx]
        observed = base.observe_second(a2, observed, g, i)
        total_cost += base.COST[a2]

    y = base.target(context, g, i, s)
    pred = base.bayes_predict(context, observed)
    loss = float(pred != y)
    reward = -(loss + base.LAMBDA * total_cost)

    if a2_idx is not None:
        q2[context_idx, s, a2_idx] += base.ALPHA * (reward - q2[context_idx, s, a2_idx])
    q1[context_idx, a1_idx] += base.ALPHA * (reward - q1[context_idx, a1_idx])

    return loss, total_cost, a1, a2, forced


def train_controlled(seed: int) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    rng = np.random.default_rng(seed)
    force_rng = np.random.default_rng(seed + FORCE_SEED_OFFSET)
    q1 = np.zeros((len(base.CONTEXTS), len(base.FIRST_ACTIONS)), dtype=float)
    q2 = np.zeros((len(base.CONTEXTS), 2, len(base.SECOND_ACTIONS)), dtype=float)

    forced_probe_count = 0
    executed_probe_count = 0
    w3_count = 0

    for ep in range(base.TRAIN_EPISODES):
        frac = ep / max(1, base.TRAIN_EPISODES - 1)
        eps = base.EPS_START + frac * (base.EPS_END - base.EPS_START)
        context_idx = int(rng.integers(len(base.CONTEXTS)))
        if context_idx == W3_IDX:
            w3_count += 1
        _, _, a1, _, forced = run_episode_controlled(
            context_idx, q1, q2, eps, rng, force_rng
        )
        forced_probe_count += int(forced)
        executed_probe_count += int(a1 == "PROBE_S")

    return q1, q2, {
        "w3_training_count": w3_count,
        "forced_probe_count": forced_probe_count,
        "executed_probe_count": executed_probe_count,
    }


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


def main() -> None:
    oracle = base.exact_fixed_policy(base.ORACLE_FIRST, route_oracle=True)
    one_shot = base.exact_fixed_policy(base.ONE_SHOT_FIRST, route_oracle=False)
    empty_losses = {c: base.empty_information_loss(c) for c in base.CONTEXTS}

    rows: list[dict[str, object]] = []
    sample_shapes: dict[str, object] = {}

    for seed in range(base.N_SEEDS):
        q1, q2, exposure = train_controlled(seed)
        d = base.seed_diagnostics(q1, q2, oracle["J"])
        shape = base.policy_shape(q1, q2)
        first = shape["first"]
        branches = shape["branches"]
        branch_full = bool(
            branches["W3_GATE_S0"] == "SELECT_G"
            and branches["W3_GATE_S1"] == "SELECT_I"
        )
        probe_preferred = bool(first["W3_GATE"] == "PROBE_S")
        d.update(exposure)
        d["W3_branch_full"] = branch_full
        d["W3_probe_preferred"] = probe_preferred
        rows.append(d)
        if seed < 8:
            sample_shapes[str(seed)] = shape

    branch_rate = float(np.mean([bool(r["W3_branch_full"]) for r in rows]))
    probe_rate = float(np.mean([bool(r["W3_probe_preferred"]) for r in rows]))
    full_rate = float(np.mean([bool(r["oracle_equivalent_full_policy"]) for r in rows]))

    learned = {
        "W3_branch_full_seed_rate": branch_rate,
        "W3_probe_preferred_seed_rate": probe_rate,
        "oracle_equivalent_full_policy_seed_rate": full_rate,
        "loss": summarize([float(r["loss"]) for r in rows]),
        "cost": summarize([float(r["cost"]) for r in rows]),
        "J": summarize([float(r["J"]) for r in rows]),
        "regret_J": summarize([float(r["regret_J"]) for r in rows]),
        "first_operation_accuracy": summarize([float(r["first_operation_accuracy"]) for r in rows]),
        "W3_branch_accuracy": summarize([float(r["W3_branch_accuracy"]) for r in rows]),
        "P_Trecover_le_1": summarize([float(r["P_Trecover_le_1"]) for r in rows]),
        "w3_training_count": summarize([float(r["w3_training_count"]) for r in rows]),
        "forced_probe_count": summarize([float(r["forced_probe_count"]) for r in rows]),
        "executed_probe_count": summarize([float(r["executed_probe_count"]) for r in rows]),
    }

    criteria = {
        "E1_W3_branch_full_seed_rate_ge_0_95": branch_rate >= 0.95,
        "E2_W3_probe_preferred_seed_rate_ge_0_95": probe_rate >= 0.95,
        "E3_full_oracle_equivalent_seed_rate_ge_0_95": full_rate >= 0.95,
        "E4_mean_predictive_loss_le_0_01": learned["loss"]["mean"] <= 0.01,
        "E5_mean_cost_le_1_425": learned["cost"]["mean"] <= 1.425,
        "E6_mean_regret_J_le_0_02": learned["regret_J"]["mean"] <= 0.02,
        "E7_P_Trecover_le_1_ge_0_95": learned["P_Trecover_le_1"]["mean"] >= 0.95,
        "E8_matched_nuisance_gate": all(np.isclose(v, 0.5) for v in empty_losses.values()),
    }

    if branch_rate >= 0.95 and probe_rate >= 0.95 and full_rate >= 0.95:
        diagnostic = "D1_EXPOSURE_SUFFICIENT_IN_FROZEN_ASSAY"
    elif branch_rate >= 0.95 and probe_rate < 0.95:
        diagnostic = "D2_BRANCH_LEARNED_PROBE_NOT_VALUED"
    elif branch_rate < 0.95:
        diagnostic = "D3_BRANCH_NOT_LEARNED_UNDER_CONTROLLED_EXPOSURE"
    else:
        diagnostic = "D4_PARTIAL_OR_HETEROGENEOUS"

    summary = {
        "status": "RUN_COMPLETE",
        "protocol": "ARO_001B_EXPOSURE_CONTROLLED_FREEZE_V0_1",
        "variant": "ARO-A",
        "single_intervention": {
            "forced_probe_rate_conditional_W3": FORCED_PROBE_RATE_W3,
            "second_stage_teacher_forced": False,
            "evaluation_forced": False,
        },
        "inherited_constants": {
            "seeds": base.N_SEEDS,
            "training_episodes_per_seed": base.TRAIN_EPISODES,
            "lambda": base.LAMBDA,
            "alpha_Q": base.ALPHA,
            "gamma": base.GAMMA,
            "epsilon_start": base.EPS_START,
            "epsilon_end": base.EPS_END,
            "H_recover": base.H_RECOVER,
        },
        "matched_nuisance_gate": {
            "empty_information_loss_by_world": empty_losses,
            "passes_exact_half": all(np.isclose(v, 0.5) for v in empty_losses.values()),
        },
        "baselines": {
            "ORACLE_FULL": oracle,
            "ORACLE_ONESHOT": one_shot,
        },
        "learned": learned,
        "diagnostic_classification": diagnostic,
        "criteria": criteria,
        "ALL_FROZEN_CRITERIA_PASS": bool(all(criteria.values())),
        "sample_greedy_policy_shapes_first_8_seeds": sample_shapes,
    }

    out = Path("crank/results/ARO_001B_V0_1_RESULT.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
