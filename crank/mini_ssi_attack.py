#!/usr/bin/env python3
"""SSI-derived hostile role-transport attacks on the frozen OpenCore Mini stack.

This harness does NOT modify mini.py and does NOT add a kernel primitive.

Attack A -- evidence-type laundering
-----------------------------------
Mini's Observation carrier has fields (id, scope, x, y, phase), but phase has no
operational effect on admission.  We therefore compare:

  external observation -> Observation
  internal prediction  -> Observation

with identical carrier shape.  A typed ingress control admits only externally
constituted observations.  The native Mini path admits both.

Two variants are measured:
  * correct self-prediction: Mini commits after only one external data point;
  * wrong self-prediction: an internally generated affine candidate shares one
    crossing with reality, then supplies the second point and causes Mini to
    commit the wrong rule.

We also apply the same laundering to the Mini-004 closure count: internally
predicted challenge values are syntactically clean but are not independent
reality-contact.  Counting them as observation evidence manufactures closure.

Attack B -- validity/authority role crossing
--------------------------------------------
A closure authorization earned in a declared applicability regime is carried
across an explicit regime transition where the model's validity envelope no
longer applies.  The current output is chosen at a crossing where old and new
laws agree, so contradiction is not yet visible.  A naive composition that
checks model support + closure authority but omits applicability continues;
a role-separated comparator returns INAPPLICABLE.  The next non-crossing state
makes the consequence observable.

The result is a constructed stress test, not a universal theorem.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

from mini import MOD, Organism, Rule
from mini_004_budgeted_closure import make_triad, required_challenges

HERE = Path(__file__).resolve().parent
MINI_PATH = HERE / "mini.py"
MINI_EXPECTED_SHA256 = "fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55"


def mini_sha256() -> str:
    return hashlib.sha256(MINI_PATH.read_bytes()).hexdigest()


def crossing(r0: Rule, r1: Rule) -> int:
    """Unique crossing for affine rules with different slopes over prime Z_11."""
    d = (r0.a - r1.a) % MOD
    if d == 0:
        raise ValueError("rules require different slopes")
    return ((r1.c - r0.c) * pow(d, -1, MOD)) % MOD


def choose_distinct_slope_rules(rng: random.Random) -> tuple[Rule, Rule]:
    a0, a1 = rng.sample(range(1, MOD), 2)
    return Rule(a0, rng.randrange(MOD)), Rule(a1, rng.randrange(MOD))


@dataclass(frozen=True)
class CarrierEvent:
    scope: str
    x: int
    y: int
    evidence_type: str  # OBSERVATION | PREDICTION
    provenance: str
    phase: str


def deliver_native(org: Organism, ev: CarrierEvent) -> None:
    """Native Mini sees the carrier fields but has no evidence-type admission gate."""
    org.observe(ev.scope, ev.x, ev.y, ev.phase)


def deliver_typed(org: Organism, ev: CarrierEvent) -> bool:
    """SSI-style comparator: only world observations may enter Observation evidence."""
    if ev.evidence_type != "OBSERVATION":
        return False
    org.observe(ev.scope, ev.x, ev.y, ev.phase)
    return True


def evidence_role_trial(seed: int) -> dict:
    rng = random.Random(seed)
    truth, fake = choose_distinct_slope_rules(rng)
    x0 = crossing(truth, fake)
    choices = [x for x in range(MOD) if x != x0]
    x1 = rng.choice(choices)

    real0 = CarrierEvent("A", x0, truth(x0), "OBSERVATION", "world", "external-observation")
    real1 = CarrierEvent("A", x1, truth(x1), "OBSERVATION", "world", "external-observation")
    pred_true = CarrierEvent("A", x1, truth(x1), "PREDICTION", "internal:true-predictor", "internal-prediction")
    pred_fake = CarrierEvent("A", x1, fake(x1), "PREDICTION", "internal:fake-predictor", "internal-prediction")

    # External-evidence control.
    external = Organism()
    deliver_native(external, real0)
    deliver_native(external, real1)

    # Same semantic value as a real observation, but wrong evidence role.
    native_true = Organism()
    deliver_native(native_true, real0)
    deliver_native(native_true, pred_true)

    typed_true = Organism()
    deliver_typed(typed_true, real0)
    admitted_true_prediction = deliver_typed(typed_true, pred_true)

    # Wrong internally generated candidate: one world crossing + one self-produced point.
    native_fake = Organism()
    deliver_native(native_fake, real0)
    deliver_native(native_fake, pred_fake)

    typed_fake = Organism()
    deliver_typed(typed_fake, real0)
    admitted_fake_prediction = deliver_typed(typed_fake, pred_fake)

    external_rule = external.active.get("A").rule if "A" in external.active else None
    native_true_rule = native_true.active.get("A").rule if "A" in native_true.active else None
    native_fake_rule = native_fake.active.get("A").rule if "A" in native_fake.active else None

    fake_errors = sum(int(fake(x) != truth(x)) for x in range(MOD))

    return {
        "seed": seed,
        "truth": asdict(truth),
        "fake": asdict(fake),
        "crossing_x": x0,
        "second_x": x1,
        "external_control_committed_truth": external_rule == truth,
        "native_correct_self_prediction_committed": native_true_rule is not None,
        "native_correct_self_prediction_rule_is_truth": native_true_rule == truth,
        "typed_correct_self_prediction_admitted": admitted_true_prediction,
        "typed_correct_self_prediction_committed": "A" in typed_true.active,
        "native_wrong_self_prediction_committed_fake": native_fake_rule == fake,
        "native_wrong_self_prediction_committed_truth": native_fake_rule == truth,
        "typed_wrong_self_prediction_admitted": admitted_fake_prediction,
        "typed_wrong_self_prediction_committed": "A" in typed_fake.active,
        "wrong_candidate_global_errors": fake_errors,
        "external_observation_count_native_true": 1,
    }


def closure_role_trial(seed: int, p_min: float, delta: float) -> dict:
    """Count internally generated predictions as if they were closure challenges."""
    triad = make_triad(seed, p_min)
    case = triad.dense
    q = required_challenges(p_min, delta)
    rule = case.rule

    # Licensed control: actual environment challenge values.
    real_hit = False
    real_challenges = 0
    for slot in triad.challenge_order[:q]:
        real_challenges += 1
        obs = case.observe_slot(slot)
        if obs.y != rule(obs.x):
            real_hit = True
            break
    real_false_closure = not real_hit

    # Laundered carrier: same challenge x/context, but y is generated by incumbent.
    # It is semantically a prediction, not an observation of the environment.
    pseudo_clean = 0
    for slot in triad.challenge_order[:q]:
        x = case.x_by_slot[slot]
        y = rule(x)  # self-generated
        if y == rule(x):
            pseudo_clean += 1
    native_pseudo_stop = pseudo_clean >= q
    pseudo_false_closure = native_pseudo_stop and bool(case.defect_slots)

    # Typed comparator admits zero pseudo observations, so no closure certificate is earned.
    typed_admissible_challenges = 0
    typed_stop = typed_admissible_challenges >= q

    return {
        "seed": seed,
        "q_required": q,
        "latent_prevalence_harness_only": case.prevalence,
        "licensed_real_challenges_until_hit_or_q": real_challenges,
        "licensed_real_hit": real_hit,
        "licensed_real_false_closure": real_false_closure,
        "native_pseudo_clean_count": pseudo_clean,
        "native_pseudo_stop": native_pseudo_stop,
        "native_pseudo_false_closure": pseudo_false_closure,
        "typed_admissible_challenges": typed_admissible_challenges,
        "typed_stop": typed_stop,
    }


@dataclass(frozen=True)
class TransitionReceipt:
    scope: str
    model_rule: Rule
    closure_authorized: bool
    validity_regime: str


def validity_authority_trial(seed: int) -> dict:
    """Authority survives syntactically while applicability has changed."""
    rng = random.Random(seed ^ 0x5A17)
    old_rule, new_rule = choose_distinct_slope_rules(rng)
    x_same = crossing(old_rule, new_rule)
    x_diff = rng.choice([x for x in range(MOD) if x != x_same])

    receipt = TransitionReceipt(
        scope="A",
        model_rule=old_rule,
        closure_authorized=True,
        validity_regime="regime-0",
    )

    current_regime = "regime-1"  # independently known to be outside V(receipt)
    current_y = new_rule(x_same)
    current_prediction = old_rule(x_same)
    no_current_contradiction = current_y == current_prediction

    # Naive role collapse: support + closure authority -> continue/closed.
    native_status = "CLOSED_USE" if receipt.closure_authorized and no_current_contradiction else "REOPEN"

    # SSI-separated comparator checks V and Lambda independently.
    applicable = current_regime == receipt.validity_regime
    if not applicable:
        typed_status = "INAPPLICABLE"
    elif not receipt.closure_authorized:
        typed_status = "UNAUTHORIZED"
    else:
        typed_status = "CLOSED_USE"

    later_truth = new_rule(x_diff)
    later_prediction = old_rule(x_diff)
    later_failure = later_truth != later_prediction

    return {
        "seed": seed,
        "old_rule": asdict(old_rule),
        "new_rule": asdict(new_rule),
        "receipt": {**asdict(receipt), "model_rule": asdict(receipt.model_rule)},
        "current_regime": current_regime,
        "crossing_x": x_same,
        "current_output_matches": no_current_contradiction,
        "native_status": native_status,
        "typed_status": typed_status,
        "later_x": x_diff,
        "later_prediction": later_prediction,
        "later_truth": later_truth,
        "later_failure": later_failure,
    }


def sweep(n: int, p_min: float, delta: float, start_seed: int = 0) -> dict:
    evidence = {
        "n": n,
        "external_control_truth_commits": 0,
        "correct_self_prediction_native_commits": 0,
        "correct_self_prediction_typed_commits": 0,
        "wrong_self_prediction_native_fake_commits": 0,
        "wrong_self_prediction_typed_commits": 0,
        "wrong_candidate_error_sum": 0,
    }
    closure = {
        "n": n,
        "licensed_real_false_closures": 0,
        "native_pseudo_stops": 0,
        "native_pseudo_false_closures": 0,
        "typed_pseudo_stops": 0,
    }
    validity = {
        "n": n,
        "native_closed_use_after_validity_boundary": 0,
        "typed_inapplicable": 0,
        "later_failures": 0,
    }

    demos = {}
    for i, seed in enumerate(range(start_seed, start_seed + n)):
        a = evidence_role_trial(seed)
        evidence["external_control_truth_commits"] += int(a["external_control_committed_truth"])
        evidence["correct_self_prediction_native_commits"] += int(a["native_correct_self_prediction_committed"])
        evidence["correct_self_prediction_typed_commits"] += int(a["typed_correct_self_prediction_committed"])
        evidence["wrong_self_prediction_native_fake_commits"] += int(a["native_wrong_self_prediction_committed_fake"])
        evidence["wrong_self_prediction_typed_commits"] += int(a["typed_wrong_self_prediction_committed"])
        evidence["wrong_candidate_error_sum"] += a["wrong_candidate_global_errors"]

        c = closure_role_trial(seed, p_min, delta)
        closure["licensed_real_false_closures"] += int(c["licensed_real_false_closure"])
        closure["native_pseudo_stops"] += int(c["native_pseudo_stop"])
        closure["native_pseudo_false_closures"] += int(c["native_pseudo_false_closure"])
        closure["typed_pseudo_stops"] += int(c["typed_stop"])

        v = validity_authority_trial(seed)
        validity["native_closed_use_after_validity_boundary"] += int(v["native_status"] == "CLOSED_USE")
        validity["typed_inapplicable"] += int(v["typed_status"] == "INAPPLICABLE")
        validity["later_failures"] += int(v["later_failure"])

        if i == 0:
            demos = {"evidence_role": a, "closure_role": c, "validity_authority": v}

    evidence["mean_global_errors_of_wrong_self_candidate"] = evidence["wrong_candidate_error_sum"] / n
    closure["licensed_real_false_closure_rate"] = closure["licensed_real_false_closures"] / n
    closure["native_pseudo_false_closure_rate"] = closure["native_pseudo_false_closures"] / n
    validity["native_boundary_crossing_rate"] = validity["native_closed_use_after_validity_boundary"] / n

    return {
        "experiment": "OpenCore Mini x SSI hostile role-transport audit",
        "claim_ceiling": "constructed harness result only; no M7, no kernel primitive, no autonomous evidence-role discovery",
        "mini_sha256": mini_sha256(),
        "mini_unchanged": mini_sha256() == MINI_EXPECTED_SHA256,
        "parameters": {"n": n, "start_seed": start_seed, "p_min": p_min, "delta": delta},
        "attack_a_evidence_type_laundering": evidence,
        "attack_a2_closure_evidence_type_laundering": closure,
        "attack_b_validity_authority_role_crossing": validity,
        "demo_seed": demos,
    }


def render_report(payload: dict) -> str:
    e = payload["attack_a_evidence_type_laundering"]
    c = payload["attack_a2_closure_evidence_type_laundering"]
    v = payload["attack_b_validity_authority_role_crossing"]
    n = e["n"]
    return f"""# OpenCore Mini × SSI hostile role-transport audit

`mini.py` remained byte-identical: `{payload['mini_sha256']}`.

## Attack A — prediction → observation evidence-type laundering

Across {n} seeds:

- two external world observations committed the true rule: **{e['external_control_truth_commits']}/{n}**
- one external point + one *correct internal prediction* caused native Mini to commit: **{e['correct_self_prediction_native_commits']}/{n}**
- typed ingress admitted that prediction as observation: **0/{n}**; typed Mini committed: **{e['correct_self_prediction_typed_commits']}/{n}**
- one external crossing + one *wrong internal prediction* caused native Mini to commit the internally generated wrong rule: **{e['wrong_self_prediction_native_fake_commits']}/{n}**
- typed Mini committed in the same wrong-prediction condition: **{e['wrong_self_prediction_typed_commits']}/{n}**
- the wrong internally generated affine rule disagreed with reality on mean **{e['mean_global_errors_of_wrong_self_candidate']:.2f}/11** states.

Interpretation: native Mini operationally treats carrier-compatible predictions as observations; the `phase` string is historical text, not an evidence-admission type.

## Attack A2 — self-prediction → closure evidence

With the M4 contract (`p_min=0.25`, `delta=0.10`):

- licensed world-contact challenges false-closed: **{c['licensed_real_false_closures']}/{n} = {100*c['licensed_real_false_closure_rate']:.2f}%**
- replacing those challenge values with incumbent-generated predictions produced native STOPs: **{c['native_pseudo_stops']}/{n}**
- resulting false closures: **{c['native_pseudo_false_closures']}/{n} = {100*c['native_pseudo_false_closure_rate']:.2f}%**
- typed comparator STOPs from prediction-only challenge evidence: **{c['typed_pseudo_stops']}/{n}**

The semantic `(x,y)` shape is not enough to constitute a challenge observation.

## Attack B — closure authority → validity laundering

Each trial carried a legitimate old-regime closure receipt across an explicit applicability boundary. The old and new response laws were forced to agree at the first post-boundary state, so there was no current contradiction.

- naive support+closure composition remained `CLOSED_USE`: **{v['native_closed_use_after_validity_boundary']}/{n}**
- role-separated comparator returned `INAPPLICABLE`: **{v['typed_inapplicable']}/{n}**
- at the next non-crossing state the carried model failed: **{v['later_failures']}/{n}**

This is the SSI distinction `APPLICABLE != AUTHORIZED`: closure authority cannot manufacture validity transport.

## Frozen local conclusion

The Mini stack does not presently preserve epistemic role across all carrier/transition boundaries. In these constructed attacks, semantic content that is acceptable in one role can acquire unauthorized force when transported as another role.

Candidate compression:

`semantic preservation != epistemic-role preservation`

No new OpenCore primitive is implied. A shallow ingress/type gate or external protocol receipt may be sufficient; representation choice remains open.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--p-min", type=float, default=0.25)
    ap.add_argument("--delta", type=float, default=0.10)
    ap.add_argument("--output-json", type=Path)
    ap.add_argument("--output-md", type=Path)
    args = ap.parse_args()

    payload = sweep(args.n, args.p_min, args.delta, args.start_seed)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        args.output_json.write_text(text, encoding="utf-8")
    else:
        print(text)
    if args.output_md:
        args.output_md.write_text(render_report(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
