#!/usr/bin/env python3
"""OQ-001: Outcome-equivalent instrument divergence.

Foreign-pressure assay only. No Nano, Base, quantum schema, or persistence repair.
The assay asks whether a coarse classical event carrier aliases two quantum
instrument histories that are distinguishable by a later measurement.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

SEED = 20260821
SHOTS = 100_000
TOL = 1e-12
RESULT_POSITIVE = "APPARATUS_EXPRESSIVE_WOUND_ESTABLISHED"
RESULT_SURVIVES = "COARSE_REPRESENTATION_SURVIVES"
RESULT_INVALID = "ASSAY_INVALID_OR_UNDERCONSTITUTED"


def ketbra(v: np.ndarray) -> np.ndarray:
    return v @ v.conj().T


def effect(k: np.ndarray) -> np.ndarray:
    return k.conj().T @ k


def branch(k: np.ndarray, rho: np.ndarray) -> tuple[float, np.ndarray]:
    unnormalized = k @ rho @ k.conj().T
    probability = float(np.real(np.trace(unnormalized)))
    if probability <= 0:
        raise ValueError("zero-probability branch")
    return probability, unnormalized / probability


def probabilities(rho: np.ndarray, projectors: tuple[np.ndarray, np.ndarray]) -> tuple[float, float]:
    return tuple(float(np.real(np.trace(p @ rho))) for p in projectors)  # type: ignore[return-value]


def total_variation(p: tuple[float, float], q: tuple[float, float]) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def simulate(
    rng: np.random.Generator,
    rho0: np.ndarray,
    instrument: tuple[np.ndarray, np.ndarray],
    second_projectors: tuple[np.ndarray, np.ndarray],
) -> dict[str, object]:
    counts = {"x0_y+": 0, "x0_y-": 0, "x1_y+": 0, "x1_y-": 0}
    first_probs = [branch(k, rho0)[0] for k in instrument]
    for _ in range(SHOTS):
        x = 0 if rng.random() < first_probs[0] else 1
        _, post = branch(instrument[x], rho0)
        second_probs = probabilities(post, second_projectors)
        y_plus = rng.random() < second_probs[0]
        counts[f"x{x}_y{'+' if y_plus else '-'}"] += 1
    x0 = counts["x0_y+"] + counts["x0_y-"]
    return {
        "shots": SHOTS,
        "x0_trials": x0,
        "p_y_plus_given_x0": counts["x0_y+"] / x0,
        "counts": counts,
    }


def run() -> dict[str, object]:
    zero = np.array([[1.0], [0.0]], dtype=complex)
    one = np.array([[0.0], [1.0]], dtype=complex)
    plus = (zero + one) / math.sqrt(2)
    minus = (zero - one) / math.sqrt(2)
    y_plus = (zero + 1j * one) / math.sqrt(2)
    y_minus = (zero - 1j * one) / math.sqrt(2)
    identity = np.eye(2, dtype=complex)
    rho0 = ketbra(plus)

    # Instrument A: ordinary Z measurement.
    a0 = zero @ zero.conj().T
    a1 = one @ one.conj().T
    instrument_a = (a0, a1)

    # Instrument B: identical Z-outcome POVM, then prepare |+> for either outcome.
    b0 = plus @ zero.conj().T
    b1 = plus @ one.conj().T
    instrument_b = (b0, b1)

    complete_a = sum((effect(k) for k in instrument_a), np.zeros((2, 2), dtype=complex))
    complete_b = sum((effect(k) for k in instrument_b), np.zeros((2, 2), dtype=complex))
    cptp_a = np.allclose(complete_a, identity, atol=TOL)
    cptp_b = np.allclose(complete_b, identity, atol=TOL)

    effects_equal = all(
        np.allclose(effect(ka), effect(kb), atol=TOL)
        for ka, kb in zip(instrument_a, instrument_b)
    )

    pa0, rho_a0 = branch(a0, rho0)
    pb0, rho_b0 = branch(b0, rho0)
    first_outcome_equal = abs(pa0 - pb0) <= TOL

    x_projectors = (ketbra(plus), ketbra(minus))
    y_projectors = (ketbra(y_plus), ketbra(y_minus))

    x_a = probabilities(rho_a0, x_projectors)
    x_b = probabilities(rho_b0, x_projectors)
    y_a = probabilities(rho_a0, y_projectors)
    y_b = probabilities(rho_b0, y_projectors)

    tv_x = total_variation(x_a, x_b)
    tv_y = total_variation(y_a, y_b)

    coarse_a = ("Z", 0)
    coarse_b = ("Z", 0)
    coarse_aliases = coarse_a == coarse_b

    # Any predictor keyed only by the coarse carrier must issue one Bernoulli
    # probability q for X+. The two true targets are 1/2 and 1. The minimax
    # choice is q=3/4, leaving TV error 1/4 in either history.
    coarse_minimax_q_x_plus = 0.75
    coarse_minimax_tv_error_x = max(
        abs(coarse_minimax_q_x_plus - x_a[0]),
        abs(coarse_minimax_q_x_plus - x_b[0]),
    )
    coarse_minimax_tv_error_y = 0.0 if abs(y_a[0] - y_b[0]) <= TOL else abs(y_a[0] - y_b[0]) / 2

    discriminator_pass = tv_x > TOL
    negative_control_pass = tv_y <= TOL

    valid = cptp_a and cptp_b and effects_equal and first_outcome_equal
    if not valid:
        result_class = RESULT_INVALID
    elif coarse_aliases and discriminator_pass and negative_control_pass and coarse_minimax_tv_error_x > TOL:
        result_class = RESULT_POSITIVE
    else:
        result_class = RESULT_SURVIVES

    rng = np.random.default_rng(SEED)
    sampling = {
        "X": {
            "A": simulate(rng, rho0, instrument_a, x_projectors),
            "B": simulate(rng, rho0, instrument_b, x_projectors),
        },
        "Y_control": {
            "A": simulate(rng, rho0, instrument_a, y_projectors),
            "B": simulate(rng, rho0, instrument_b, y_projectors),
        },
    }

    result = {
        "experiment": "OQ-001",
        "title": "Outcome-equivalent instrument divergence",
        "execution": {
            "mode": "exact statevector/Kraus simulation plus seeded Monte Carlo",
            "hardware": False,
            "qiskit_used": False,
            "numpy_version": np.__version__,
            "seed": SEED,
            "shots_per_instrument_probe": SHOTS,
        },
        "prospective_result_class": result_class,
        "instrument_validation": {
            "A_complete": cptp_a,
            "B_complete": cptp_b,
            "POVM_effects_equal_for_both_outcomes": effects_equal,
            "implication": "first-outcome distributions agree for every input density operator",
        },
        "first_event": {
            "initial_state": "|+><+|",
            "conditioned_outcome": 0,
            "P_A_x0": pa0,
            "P_B_x0": pb0,
            "coarse_carrier_A": list(coarse_a),
            "coarse_carrier_B": list(coarse_b),
            "coarse_carriers_equal": coarse_aliases,
            "post_state_A": "|0><0|",
            "post_state_B": "|+><+|",
        },
        "downstream": {
            "X_discriminator": {
                "P_A_plus_given_x0": x_a[0],
                "P_B_plus_given_x0": x_b[0],
                "total_variation": tv_x,
                "pass": discriminator_pass,
            },
            "Y_negative_control": {
                "P_A_plus_given_x0": y_a[0],
                "P_B_plus_given_x0": y_b[0],
                "total_variation": tv_y,
                "pass": negative_control_pass,
            },
        },
        "coarse_carrier_attack": {
            "same_key_has_two_X_plus_targets": [x_a[0], x_b[0]],
            "best_minimax_coarse_prediction_X_plus": coarse_minimax_q_x_plus,
            "irreducible_worst_case_TV_error_X": coarse_minimax_tv_error_x,
            "irreducible_worst_case_TV_error_Y_control": coarse_minimax_tv_error_y,
        },
        "sampling_check": sampling,
        "claim_ceiling": (
            "The tested coarse event representation erased a distinction required "
            "to predict a later discriminating consequence. No quantum-specific "
            "OpenCore schema or persistence primitive is thereby earned."
        ),
        "not_claimed": [
            "quantum hardware result",
            "OpenCore improves quantum computation",
            "Nano requires a post_state field",
            "quantum-state provenance is a universal OpenCore primitive",
            "persistence consequence has been tested",
        ],
    }
    result["result_sha256"] = canonical_sha256(result)
    return result


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
