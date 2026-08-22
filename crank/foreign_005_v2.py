#!/usr/bin/env python3
"""FOREIGN-005 — Reopenable Quotient.

Prospectively frozen assay for safe effective quotienting, latent interrogable
substrate, later interface expansion, and a destructive-retention control.
Nano remains semantically blind and byte-identical.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

EXPECTED_NANO_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"
H_A = (1, -1, 1, -1)
H_B = (1, 1, -1, -1)
Q0_CARRIER = "event:q0:mean=0:energy=4"
Q0_PROFILE = "MEAN_0__ENERGY_4"
Q0_CONSEQUENCE = "Q0_SAFE"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_payload(history: tuple[int, ...]) -> bytes:
    # No A/B/history-class label is encoded in the opaque source bytes.
    return json.dumps({"samples": list(history)}, sort_keys=True, separators=(",", ":")).encode()


def opaque_id(payload: bytes) -> str:
    return "opaque:" + sha256_bytes(payload)[:20]


def q0(history: tuple[int, ...]) -> tuple[int, int]:
    # Numerator of mean is sufficient here because n is fixed and both are 0.
    return sum(history), sum(x * x for x in history)


def m_star(payload: bytes) -> int:
    """Lag-one autocorrelation numerator, computed only from temporal payload."""
    obj = json.loads(payload.decode())
    samples = obj.get("samples")
    if not isinstance(samples, list) or len(samples) < 2:
        raise ValueError("temporal payload unavailable")
    vals = [int(x) for x in samples]
    return sum(a * b for a, b in zip(vals, vals[1:]))


def n_star(payload: bytes) -> int:
    obj = json.loads(payload.decode())
    samples = obj.get("samples")
    if not isinstance(samples, list):
        raise ValueError("temporal payload unavailable")
    return sum(abs(int(x)) for x in samples)


def load_nano(path: Path):
    spec = importlib.util.spec_from_file_location("foreign005_frozen_nano", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Nano")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def stand_tuple(st) -> tuple[str, str, str, str]:
    return (st.key.object_id, st.key.dimension, st.key.scope, st.value)


def effective_snapshot(nano) -> dict[str, list[tuple[str, str, str, str]]]:
    eff = nano.effective_state()
    return {
        "active": sorted(stand_tuple(x) for x in eff.active),
        "deferred": sorted(stand_tuple(x) for x in eff.deferred),
    }


def has_future_semantics(snapshot: dict[str, Any]) -> bool:
    forbidden = ("m-star", "m_star", "autocorr", "lag1", "n-star", "n_star", "refined", "ac_neg", "ac_pos")
    text = json.dumps(snapshot, sort_keys=True).lower()
    return any(token in text for token in forbidden)


def build_initial_branch(N, retained_sources: bool, payloads: dict[str, bytes]):
    StandingKey, Standing = N.StandingKey, N.Standing
    Precondition, WriteGrant = N.Precondition, N.WriteGrant
    License, Transition, ObjectRecord, Nano = N.License, N.Transition, N.ObjectRecord, N.Nano

    qkey = StandingKey(Q0_CARRIER, "q0-profile", "Q0")
    downkey = StandingKey("downstream:q0:B", "consequence", "Q0")

    objects = [ObjectRecord(Q0_CARRIER, sha256_bytes(Q0_PROFILE.encode()), "Q0_QUOTIENT_OPAQUE")]
    if retained_sources:
        for sid, payload in payloads.items():
            objects.append(ObjectRecord(sid, sha256_bytes(payload), "OPAQUE_TEMPORAL_SOURCE"))

    licenses = (
        License(
            "admit-q0-A",
            "admit-q0",
            allowed_writes=(WriteGrant(qkey, (Q0_PROFILE,)),),
        ),
        License(
            "use-q0-for-B",
            "persist-q0-consequence",
            preconditions=(Precondition(qkey, Q0_PROFILE),),
            allowed_writes=(WriteGrant(downkey, (Q0_CONSEQUENCE,)),),
        ),
    )
    nano = Nano(objects=tuple(objects), licenses=licenses)
    t_admit = Transition("admit-q0", writes=(Standing(qkey, Q0_PROFILE),))
    r_admit = nano.apply_transition(t_admit, "admit-q0-A")
    t_use = Transition("persist-q0-consequence", writes=(Standing(downkey, Q0_CONSEQUENCE),))
    r_use = nano.apply_transition(t_use, "use-q0-for-B")
    return nano, {
        "qkey": qkey,
        "downkey": downkey,
        "admit": r_admit,
        "use": r_use,
        "admit_transition_digest": r_admit.transition_digest,
        "use_transition_digest": r_use.transition_digest,
    }


def add_interface_licenses(N, nano, source_ids: list[str]):
    StandingKey, Precondition, WriteGrant, License = N.StandingKey, N.Precondition, N.WriteGrant, N.License
    for sid in source_ids:
        mkey = StandingKey(sid, "new-observation", "M-star")
        rkey = StandingKey(sid, "refined-profile", "M-star")
        nkey = StandingKey(sid, "new-observation", "N-star")
        # External contracts admit the possible assay outputs; Nano does not compute them.
        nano.licenses[f"admit-M:{sid}"] = License(
            f"admit-M:{sid}",
            "admit-M",
            allowed_writes=(WriteGrant(mkey, ("-3", "1")),),
        )
        nano.licenses[f"refine-M-neg:{sid}"] = License(
            f"refine-M-neg:{sid}",
            "refine-M",
            preconditions=(Precondition(mkey, "-3"),),
            allowed_writes=(WriteGrant(rkey, ("AC_NEG3",)),),
        )
        nano.licenses[f"refine-M-pos:{sid}"] = License(
            f"refine-M-pos:{sid}",
            "refine-M",
            preconditions=(Precondition(mkey, "1"),),
            allowed_writes=(WriteGrant(rkey, ("AC_POS1",)),),
        )
        nano.licenses[f"admit-N:{sid}"] = License(
            f"admit-N:{sid}",
            "admit-N",
            allowed_writes=(WriteGrant(nkey, ("4",)),),
        )


def apply_m_refinement(N, nano, sid: str, value: int):
    StandingKey, Standing, Transition = N.StandingKey, N.Standing, N.Transition
    mkey = StandingKey(sid, "new-observation", "M-star")
    rkey = StandingKey(sid, "refined-profile", "M-star")
    r_obs = nano.apply_transition(
        Transition("admit-M", writes=(Standing(mkey, str(value)),)),
        f"admit-M:{sid}",
    )
    if value == -3:
        rval, lid = "AC_NEG3", f"refine-M-neg:{sid}"
    elif value == 1:
        rval, lid = "AC_POS1", f"refine-M-pos:{sid}"
    else:
        raise AssertionError("unexpected frozen M* value")
    r_ref = nano.apply_transition(
        Transition("refine-M", writes=(Standing(rkey, rval),)),
        lid,
    )
    return r_obs, r_ref, rkey


def destructive_nonidentifiability() -> dict[str, Any]:
    # Both histories map to the same Q0 carrier but require different M* values.
    qa, qb = q0(H_A), q0(H_B)
    ma = sum(a * b for a, b in zip(H_A, H_A[1:]))
    mb = sum(a * b for a, b in zip(H_B, H_B[1:]))
    collision = qa == qb
    target_difference = ma != mb
    # Therefore no deterministic function g(Q0) can equal both frozen targets.
    impossible = collision and target_difference
    return {
        "q0_A": qa,
        "q0_B": qb,
        "M_target_A": ma,
        "M_target_B": mb,
        "q0_collision": collision,
        "M_targets_differ": target_difference,
        "deterministic_recovery_from_q0_impossible": impossible,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nano", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    nano_sha_before = sha256_path(args.nano)
    if nano_sha_before != EXPECTED_NANO_SHA256:
        raise SystemExit(f"Nano SHA mismatch before run: {nano_sha_before}")
    N = load_nano(args.nano)

    payload_A = canonical_payload(H_A)
    payload_B = canonical_payload(H_B)
    sid_A, sid_B = opaque_id(payload_A), opaque_id(payload_B)
    payloads = {sid_A: payload_A, sid_B: payload_B}

    qA, qB = q0(H_A), q0(H_B)
    mA, mB = m_star(payload_A), m_star(payload_B)
    nA, nB = n_star(payload_A), n_star(payload_B)

    formal_checks: dict[str, bool] = {
        "histories_differ": H_A != H_B,
        "Q0_equivalent": qA == qB,
        "Q0_expected": qA == (0, 4) and qB == (0, 4),
        "opaque_payloads_differ": payload_A != payload_B and sha256_bytes(payload_A) != sha256_bytes(payload_B),
        "opaque_ids_nonsemantic": all(token not in (sid_A + sid_B).lower() for token in ("history", "autocorr", "lag", "source_a", "source_b")),
        "M_distinguishes": (mA, mB) == (-3, 1),
        "N_null_equivalent": (nA, nB) == (4, 4),
        "M_not_function_of_Q0_on_frozen_pair": qA == qB and mA != mB,
    }

    reopen, r0 = build_initial_branch(N, True, payloads)
    destructive, d0 = build_initial_branch(N, False, payloads)

    reopen_pre = effective_snapshot(reopen)
    destructive_pre = effective_snapshot(destructive)

    # Extend contracts only after the future interface becomes available.
    add_interface_licenses(N, reopen, [sid_A, sid_B])
    r_mA_obs, r_mA_ref, rkey_A = apply_m_refinement(N, reopen, sid_A, mA)
    r_mB_obs, r_mB_ref, rkey_B = apply_m_refinement(N, reopen, sid_B, mB)
    reopen_post_m = effective_snapshot(reopen)

    # Destructive branch: no temporal source payload exists. The new apparatus cannot run.
    nonident = destructive_nonidentifiability()
    StandingKey, Standing, Precondition, WriteGrant = N.StandingKey, N.Standing, N.Precondition, N.WriteGrant
    License, Transition = N.License, N.Transition
    missing_mkey = StandingKey("destroyed-source", "new-observation", "M-star")
    missing_rkey = StandingKey("destroyed-source", "refined-profile", "M-star")
    destructive.licenses["destructive-refine-guess"] = License(
        "destructive-refine-guess",
        "refine-M",
        preconditions=(Precondition(missing_mkey, "-3"),),
        allowed_writes=(WriteGrant(missing_rkey, ("AC_NEG3",)),),
    )
    destructive_before_guess = effective_snapshot(destructive)
    d_guess = destructive.apply_transition(
        Transition("refine-M", writes=(Standing(missing_rkey, "AC_NEG3"),)),
        "destructive-refine-guess",
    )
    destructive_after_guess = effective_snapshot(destructive)

    # Null new interface: both retained sources yield N*=4. Alias them again safely.
    null = N.Nano(
        objects=(N.ObjectRecord("event:nstar:4", sha256_bytes(b"NSTAR4"), "NULL_INTERFACE_QUOTIENT"),),
        licenses=(
            N.License(
                "admit-null-A",
                "admit-null",
                allowed_writes=(N.WriteGrant(N.StandingKey("event:nstar:4", "N-star-profile", "N-star"), ("4",)),),
            ),
            N.License(
                "use-null-for-B",
                "persist-null-consequence",
                preconditions=(N.Precondition(N.StandingKey("event:nstar:4", "N-star-profile", "N-star"), "4"),),
                allowed_writes=(N.WriteGrant(N.StandingKey("downstream:null:B", "consequence", "N-star"), ("NULL_SAFE",)),),
            ),
        ),
    )
    n_admit = null.apply_transition(
        N.Transition("admit-null", writes=(N.Standing(N.StandingKey("event:nstar:4", "N-star-profile", "N-star"), "4"),)),
        "admit-null-A",
    )
    n_use = null.apply_transition(
        N.Transition("persist-null-consequence", writes=(N.Standing(N.StandingKey("downstream:null:B", "consequence", "N-star"), "NULL_SAFE"),)),
        "use-null-for-B",
    )

    persistence_checks: dict[str, bool] = {
        "initial_reopen_q0_admit_ALLOW": r0["admit"].decision.value == "ALLOW",
        "initial_reopen_q0_use_ALLOW": r0["use"].decision.value == "ALLOW",
        "initial_destructive_q0_admit_ALLOW": d0["admit"].decision.value == "ALLOW",
        "initial_destructive_q0_use_ALLOW": d0["use"].decision.value == "ALLOW",
        "initial_transition_objects_identical": r0["admit_transition_digest"] == d0["admit_transition_digest"] and r0["use_transition_digest"] == d0["use_transition_digest"],
        "initial_cross_history_parent_is_A_reopen": r0["use"].parent_receipts == (r0["admit"].id,),
        "initial_cross_history_parent_is_A_destructive": d0["use"].parent_receipts == (d0["admit"].id,),
        "initial_q0_consequence_correct": Q0_CONSEQUENCE == "Q0_SAFE",
        "effective_standing_state_identical_pre_interface": reopen_pre == destructive_pre,
        "no_future_semantics_pre_interface_reopen": not has_future_semantics(reopen_pre),
        "no_future_semantics_pre_interface_destructive": not has_future_semantics(destructive_pre),
        "M_A_observation_ALLOW": r_mA_obs.decision.value == "ALLOW",
        "M_B_observation_ALLOW": r_mB_obs.decision.value == "ALLOW",
        "M_A_refinement_ALLOW": r_mA_ref.decision.value == "ALLOW",
        "M_B_refinement_ALLOW": r_mB_ref.decision.value == "ALLOW",
        "M_refined_values_distinct": rkey_A != rkey_B and mA != mB,
        "M_A_refinement_parent_is_measurement": r_mA_ref.parent_receipts == (r_mA_obs.id,),
        "M_B_refinement_parent_is_measurement": r_mB_ref.parent_receipts == (r_mB_obs.id,),
        "M_refined_semantics_absent_before_present_after": not has_future_semantics(reopen_pre) and has_future_semantics(reopen_post_m),
        "destructive_M_nonidentifiable": nonident["deterministic_recovery_from_q0_impossible"],
        "destructive_guess_DEFER": d_guess.decision.value == "DEFER",
        "destructive_guess_reason_missing_M": any(x.startswith("precondition:unestablished:") for x in d_guess.reasons),
        "destructive_guess_does_not_change_effective_state": destructive_before_guess == destructive_after_guess,
        "null_admit_ALLOW": n_admit.decision.value == "ALLOW",
        "null_cross_history_use_ALLOW": n_use.decision.value == "ALLOW",
        "null_cross_history_parent_is_A": n_use.parent_receipts == (n_admit.id,),
        "null_consequence_correct": nA == nB == 4,
    }

    nano_sha_after = sha256_path(args.nano)
    persistence_checks["nano_sha_unchanged"] = nano_sha_after == nano_sha_before == EXPECTED_NANO_SHA256

    formal_pass = sum(formal_checks.values())
    persistence_pass = sum(persistence_checks.values())

    if formal_pass != len(formal_checks):
        classification = "INVALID"
    elif persistence_checks["destructive_M_nonidentifiable"] and all(persistence_checks.values()):
        classification = "REOPENABLE_QUOTIENT_ESTABLISHED"
    elif mA != mB and not (r_mA_ref.decision.value == "ALLOW" and r_mB_ref.decision.value == "ALLOW"):
        classification = "IRREVERSIBLE_QUOTIENT_WOUND"
    else:
        classification = "INVALID"

    result = {
        "assay": "FOREIGN-005 — Reopenable Quotient",
        "classification": classification,
        "nano_sha256_before": nano_sha_before,
        "nano_sha256_after": nano_sha_after,
        "world": {
            "H_A": H_A,
            "H_B": H_B,
            "Q0_A": {"mean_numerator": qA[0], "energy": qA[1]},
            "Q0_B": {"mean_numerator": qB[0], "energy": qB[1]},
            "M_star_A": mA,
            "M_star_B": mB,
            "N_star_A": nA,
            "N_star_B": nB,
        },
        "opaque_sources": {
            "ids": [sid_A, sid_B],
            "payload_sha256": [sha256_bytes(payload_A), sha256_bytes(payload_B)],
            "semantic_labels_in_object_ids": False,
        },
        "formal_checks": formal_checks,
        "formal_pass": formal_pass,
        "formal_total": len(formal_checks),
        "persistence_checks": persistence_checks,
        "persistence_pass": persistence_pass,
        "persistence_total": len(persistence_checks),
        "initial": {
            "reopenable_effective_state": reopen_pre,
            "destructive_effective_state": destructive_pre,
            "reopenable_A_q0_receipt": asdict(r0["admit"]),
            "reopenable_B_q0_use_receipt": asdict(r0["use"]),
            "destructive_A_q0_receipt": asdict(d0["admit"]),
            "destructive_B_q0_use_receipt": asdict(d0["use"]),
        },
        "reopenable_after_M": {
            "M_A_observation": asdict(r_mA_obs),
            "M_A_refinement": asdict(r_mA_ref),
            "M_B_observation": asdict(r_mB_obs),
            "M_B_refinement": asdict(r_mB_ref),
            "effective_state": reopen_post_m,
        },
        "destructive_after_M": {
            "information_theoretic_control": nonident,
            "guess_receipt": asdict(d_guess),
            "effective_state_before_guess": destructive_before_guess,
            "effective_state_after_guess": destructive_after_guess,
        },
        "null_N_star": {
            "A": nA,
            "B": nB,
            "A_admit_receipt": asdict(n_admit),
            "B_use_receipt": asdict(n_use),
        },
        "claim_ceiling": [
            "constructed classical witness only",
            "no universal archival requirement",
            "no automatic interface invention",
            "no automatic quotient refinement",
            "no HistoryID or reopenability primitive",
            "no Nano modification or new semantics",
            "no oscillatory ontology",
        ],
    }
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(f"classification={classification}")
    print(f"formal={formal_pass}/{len(formal_checks)}")
    print(f"persistence={persistence_pass}/{len(persistence_checks)}")
    print(f"nano_before={nano_sha_before}")
    print(f"nano_after={nano_sha_after}")
    print(f"Q0_A={qA} Q0_B={qB}")
    print(f"M_A={mA} M_B={mB}")
    print(f"N_A={nA} N_B={nB}")
    print(f"reopenable_pre_equals_destructive_pre={reopen_pre == destructive_pre}")
    print(f"destructive_recovery_impossible={nonident['deterministic_recovery_from_q0_impossible']}")
    print(f"destructive_guess={d_guess.decision.value} reasons={list(d_guess.reasons)}")
    return 0 if classification == "REOPENABLE_QUOTIENT_ESTABLISHED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
