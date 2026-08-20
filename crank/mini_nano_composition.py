#!/usr/bin/env python3
"""OpenCore Nano x wounded Mini composition assay.

Scientific question
-------------------
Does the frozen Nano V0 persistence boundary change outcomes of already-discovered
Mini-stack authority failures without modifying Mini and without suppressing matched
legitimate transitions?

The assay intentionally does NOT add semantics to Nano.  A harness adapter turns
externally constituted control facts into Nano's existing Standing / License /
Transition surface.  The same proposed transitions are sent to a naive persistence
store and to Nano.  Only the persistence boundary differs.

Frozen attack families reused here:
  1. prediction -> observation/support role laundering (SSI)
  2. correlated reports -> independent-path promotion (Correctable Lineage)
  3. active acquisition protocol -> stale closure authorization (Cerebro / M2 x M4)
  4. closure authority -> applicability/use (SSI)
  5. stale warrant parent -> effective descendant (Cerebro / Nano wound)
  6. preservation relation != warrant dependency regression (Nano V0 wound)

No claim about contract correctness, autonomous typing, dependency discovery, or
truth follows from this harness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from mini import MOD, Organism, Rule, choose_rules, distinct_inputs
from mini_004_budgeted_closure import make_triad, required_challenges
from mini_cerebro_attack import make_aperture_world
from mini_ssi_attack import choose_distinct_slope_rules, crossing
from nano import (
    Decision,
    License,
    Nano,
    Precondition,
    Standing,
    StandingKey,
    Transition,
    WriteGrant,
)

HERE = Path(__file__).resolve().parent
MINI_PATH = HERE / "mini.py"
NANO_PATH = HERE / "nano.py"
MINI_EXPECTED_SHA256 = "fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55"
NANO_EXPECTED_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def opaque(seed: int, label: str) -> str:
    return hashlib.sha256(f"mini-nano:{seed}:{label}".encode()).hexdigest()[:16]


def sk(seed: int, label: str, dimension: str = "state", scope: str = "global") -> StandingKey:
    return StandingKey(opaque(seed, label), dimension, scope)


class NaivePersistence:
    """Persistence that applies every proposed effect and never rechecks authority."""

    def __init__(self, standings: Iterable[Standing] = ()) -> None:
        self.current = {s.key: s.value for s in standings}
        self.revoked_licenses: set[str] = set()

    def apply(self, transition: Transition) -> Decision:
        for key in transition.deletes:
            self.current.pop(key, None)
        for standing in transition.writes:
            self.current[standing.key] = standing.value
        self.revoked_licenses.update(transition.revoke_licenses)
        return Decision.ALLOW

    def value(self, key: StandingKey) -> str | None:
        return self.current.get(key)


@dataclass
class PairStats:
    attack_attempts: int = 0
    naive_attack_allows: int = 0
    nano_attack_allows: int = 0
    nano_attack_denies: int = 0
    nano_attack_defers: int = 0
    legitimate_attempts: int = 0
    naive_legitimate_allows: int = 0
    nano_legitimate_allows: int = 0
    nano_legitimate_denies: int = 0
    nano_legitimate_defers: int = 0

    def attack(self, naive: Decision, nano: Decision) -> None:
        self.attack_attempts += 1
        self.naive_attack_allows += int(naive is Decision.ALLOW)
        self.nano_attack_allows += int(nano is Decision.ALLOW)
        self.nano_attack_denies += int(nano is Decision.DENY)
        self.nano_attack_defers += int(nano is Decision.DEFER)

    def legitimate(self, naive: Decision, nano: Decision) -> None:
        self.legitimate_attempts += 1
        self.naive_legitimate_allows += int(naive is Decision.ALLOW)
        self.nano_legitimate_allows += int(nano is Decision.ALLOW)
        self.nano_legitimate_denies += int(nano is Decision.DENY)
        self.nano_legitimate_defers += int(nano is Decision.DEFER)

    def summary(self) -> dict:
        attack_n = max(1, self.attack_attempts)
        legit_n = max(1, self.legitimate_attempts)
        return {
            **asdict(self),
            "naive_attack_overreach_rate": self.naive_attack_allows / attack_n,
            "nano_attack_overreach_rate": self.nano_attack_allows / attack_n,
            "nano_legitimate_retention_rate": self.nano_legitimate_allows / legit_n,
            "nano_false_refusal_rate": (self.nano_legitimate_denies + self.nano_legitimate_defers) / legit_n,
        }


def effective_value(nano: Nano, key: StandingKey) -> str | None:
    for s in nano.effective_state().active:
        if s.key == key:
            return s.value
    return None


def role_laundering_trial(seed: int, stats: PairStats) -> dict:
    """Same Mini commitment proposal; last source role differs externally."""
    rng = random.Random(seed ^ 0x551)
    truth, _fake = choose_distinct_slope_rules(rng)
    x0, x1 = rng.sample(range(MOD), 2)

    # Wounded Mini: a correct self-prediction is accepted by native Observation.
    illegal_org = Organism()
    illegal_org.observe("A", x0, truth(x0), "external-observation")
    illegal_org.observe("A", x1, truth(x1), "internal-prediction")
    assert "A" in illegal_org.active

    legal_org = Organism()
    legal_org.observe("A", x0, truth(x0), "external-observation")
    legal_org.observe("A", x1, truth(x1), "external-observation")
    assert "A" in legal_org.active

    source_key = sk(seed, "role-source", "source-role")
    commit_key = sk(seed, "role-commit", "commitment", "A")
    rule_value = illegal_org.active["A"].rule.short()
    assert rule_value == legal_org.active["A"].rule.short()

    lic = License(
        id=opaque(seed, "role-license"),
        operation="persist-mini-commitment",
        preconditions=(Precondition(source_key, "OBSERVATION"),),
        allowed_writes=(WriteGrant(commit_key, (rule_value,)),),
    )
    proposal = Transition("persist-mini-commitment", writes=(Standing(commit_key, rule_value),))

    # Attack: same proposed commitment, but the second datum is a prediction.
    attack_initial = (Standing(source_key, "PREDICTION"),)
    naive_a = NaivePersistence(attack_initial)
    nano_a = Nano(standings=attack_initial, licenses=(lic,))
    nd_a = naive_a.apply(proposal)
    nn_a = nano_a.apply_transition(proposal, lic.id).decision
    stats.attack(nd_a, nn_a)

    # Matched legal: same rule/value and transition shape, genuine observation role.
    legal_initial = (Standing(source_key, "OBSERVATION"),)
    naive_l = NaivePersistence(legal_initial)
    nano_l = Nano(standings=legal_initial, licenses=(lic,))
    nd_l = naive_l.apply(proposal)
    nn_l = nano_l.apply_transition(proposal, lic.id).decision
    stats.legitimate(nd_l, nn_l)

    return {
        "mini_illegal_committed": True,
        "same_semantic_rule": True,
        "nano_attack": nn_a.value,
        "nano_legal": nn_l.value,
    }


def dependency_laundering_trial(seed: int, stats: PairStats, p_min: float = 0.25, delta: float = 0.10) -> dict:
    """q reports share one upstream slot; promotion to q independent paths needs attestation."""
    q = required_challenges(p_min, delta)
    triad = make_triad(seed ^ 0xC1A0, p_min)
    case = triad.dense
    slot = triad.challenge_order[0]
    obs = case.observe_slot(slot)
    repeated_clean = obs.y == case.rule(obs.x)

    independence_key = sk(seed, "dep-attestation", "independence")
    count_key = sk(seed, "dep-count", "independent-path-count")
    count_value = str(q)
    lic = License(
        id=opaque(seed, "dep-license"),
        operation="promote-independent-path-count",
        preconditions=(Precondition(independence_key, "ATTESTED"),),
        allowed_writes=(WriteGrant(count_key, (count_value,)),),
    )
    proposal = Transition("promote-independent-path-count", writes=(Standing(count_key, count_value),))

    # Attack: q nominal reports are repeated views of one source path.
    # No independent-path attestation exists.  Absence is unresolved, not a
    # contradictory semantic fact, so Nano should DEFER rather than invent it.
    attack_initial: tuple[Standing, ...] = ()
    naive_a = NaivePersistence(attack_initial)
    nano_a = Nano(standings=attack_initial, licenses=(lic,))
    nd_a = naive_a.apply(proposal)
    nn_a = nano_a.apply_transition(proposal, lic.id).decision
    stats.attack(nd_a, nn_a)

    # Matched legal: external protocol actually constitutes independent-path attestation.
    legal_initial = (Standing(independence_key, "ATTESTED"),)
    naive_l = NaivePersistence(legal_initial)
    nano_l = Nano(standings=legal_initial, licenses=(lic,))
    nd_l = naive_l.apply(proposal)
    nn_l = nano_l.apply_transition(proposal, lic.id).decision
    stats.legitimate(nd_l, nn_l)

    return {"q": q, "repeated_source_clean": repeated_clean, "nano_attack": nn_a.value, "nano_legal": nn_l.value}


def acquisition_closure_trial(seed: int, stats: PairStats, p_min: float = 0.25, delta: float = 0.10) -> dict:
    """Authentic closure license becomes stale after acquisition protocol transition."""
    q = required_challenges(p_min, delta)
    world = make_aperture_world(seed ^ 0xCEB0, p_min=p_min)
    protocol_key = sk(seed, "acq-protocol", "protocol")
    count_key = sk(seed, "acq-count", "challenge-count")
    closure_key = sk(seed, "acq-closure", "closure")

    l_change = License(
        id=opaque(seed, "acq-change-license"),
        operation="set-acquisition-protocol",
        allowed_writes=(WriteGrant(protocol_key, ("ACTIVE", "UNIFORM")),),
    )
    l_close = License(
        id=opaque(seed, "acq-close-license"),
        operation="close-under-contract",
        preconditions=(Precondition(protocol_key, "UNIFORM"), Precondition(count_key, str(q))),
        allowed_writes=(WriteGrant(closure_key, ("CLOSED",)),),
    )
    close = Transition("close-under-contract", writes=(Standing(closure_key, "CLOSED"),))

    # Attack branch starts at a state where L_close is authentic and applicable.
    initial = (Standing(protocol_key, "UNIFORM"), Standing(count_key, str(q)))
    nano_a = Nano(standings=initial, licenses=(l_change, l_close))
    naive_a = NaivePersistence(initial)
    preview_before = nano_a.check_transition(close, l_close.id).decision
    assert preview_before is Decision.ALLOW

    # M2-like active selector changes the protocol; selected stream is clean by construction.
    selected_slots = [i for i, x in enumerate(world.x_by_slot) if x in world.selected_xs][:q]
    selected_clean = all(not world.observe(slot)[2] for slot in selected_slots)
    change_active = Transition("set-acquisition-protocol", writes=(Standing(protocol_key, "ACTIVE"),))
    assert nano_a.apply_transition(change_active, l_change.id).decision is Decision.ALLOW
    naive_a.apply(change_active)
    nd_a = naive_a.apply(close)
    nn_a = nano_a.apply_transition(close, l_close.id).decision
    stats.attack(nd_a, nn_a)

    # Matched legal: same authentic closure license, protocol remains the one it requires.
    nano_l = Nano(standings=initial, licenses=(l_change, l_close))
    naive_l = NaivePersistence(initial)
    refresh_uniform = Transition("set-acquisition-protocol", writes=(Standing(protocol_key, "UNIFORM"),))
    assert nano_l.apply_transition(refresh_uniform, l_change.id).decision is Decision.ALLOW
    naive_l.apply(refresh_uniform)
    nd_l = naive_l.apply(close)
    nn_l = nano_l.apply_transition(close, l_close.id).decision
    stats.legitimate(nd_l, nn_l)

    return {
        "q": q,
        "preview_before_protocol_change": preview_before.value,
        "selected_stream_clean": selected_clean,
        "nano_attack_after_protocol_change": nn_a.value,
        "nano_legal": nn_l.value,
    }


def authority_applicability_trial(seed: int, stats: PairStats) -> dict:
    """Closure authority is present, but applicability has crossed to a new regime."""
    rng = random.Random(seed ^ 0x551A)
    old, new = choose_distinct_slope_rules(rng)
    xc = crossing(old, new)
    x_next = next(x for x in range(MOD) if x != xc and old(x) != new(x))
    assert old(xc) == new(xc)
    assert old(x_next) != new(x_next)

    # Wounded Mini has an incumbent old rule and sees no contradiction at the crossing.
    org = Organism()
    x0 = next(x for x in range(MOD) if x != xc)
    x1 = next(x for x in range(MOD) if x not in {xc, x0})
    org.observe("A", x0, old(x0), "old-regime")
    org.observe("A", x1, old(x1), "old-regime")
    assert org.answer("A", xc) == new(xc)

    auth_key = sk(seed, "valid-auth", "closure-authority")
    validity_key = sk(seed, "valid-envelope", "applicability")
    use_key = sk(seed, "valid-use", "use")
    lic = License(
        id=opaque(seed, "valid-use-license"),
        operation="activate-model-use",
        preconditions=(Precondition(auth_key, "AUTHORIZED"), Precondition(validity_key, "CURRENT")),
        allowed_writes=(WriteGrant(use_key, ("ACTIVE",)),),
    )
    proposal = Transition("activate-model-use", writes=(Standing(use_key, "ACTIVE"),))

    attack_initial = (Standing(auth_key, "AUTHORIZED"), Standing(validity_key, "OLD"))
    naive_a = NaivePersistence(attack_initial)
    nano_a = Nano(standings=attack_initial, licenses=(lic,))
    nd_a = naive_a.apply(proposal)
    nn_a = nano_a.apply_transition(proposal, lic.id).decision
    stats.attack(nd_a, nn_a)

    legal_initial = (Standing(auth_key, "AUTHORIZED"), Standing(validity_key, "CURRENT"))
    naive_l = NaivePersistence(legal_initial)
    nano_l = Nano(standings=legal_initial, licenses=(lic,))
    nd_l = naive_l.apply(proposal)
    nn_l = nano_l.apply_transition(proposal, lic.id).decision
    stats.legitimate(nd_l, nn_l)

    return {
        "crossing_output_matches": old(xc) == new(xc),
        "next_state_failure_guaranteed": old(x_next) != new(x_next),
        "nano_attack": nn_a.value,
        "nano_legal": nn_l.value,
    }


def _make_revised_mini(seed: int) -> tuple[Organism, Rule, Rule, Rule]:
    rng = random.Random(seed ^ 0xD35C)
    old, new, b = choose_rules(rng)
    org = Organism()
    x0, x1 = distinct_inputs(rng)
    org.observe("A", x0, old(x0), "acquire")
    org.observe("A", x1, old(x1), "acquire")
    bx0, bx1 = distinct_inputs(rng)
    org.observe("B", bx0, b(bx0), "acquire")
    org.observe("B", bx1, b(bx1), "acquire")
    # Force a clean two/three-point revision to new.
    used: set[int] = set()
    for x in range(MOD):
        if old(x) != new(x):
            org.observe("A", x, new(x), "counterevidence")
            used.add(x)
            if len(org.lineage.get("A", [])) == 2:
                break
    if org.needs_probe("A"):
        for x in range(MOD):
            if x not in used:
                org.observe("A", x, new(x), "active-probe")
                if not org.needs_probe("A"):
                    break
    assert len(org.lineage.get("A", [])) == 2
    return org, old, new, b


def stale_descendant_trial(seed: int, stats: PairStats) -> dict:
    """A child standing depends on a Mini commitment whose producing license is revoked."""
    org, old, new, _b = _make_revised_mini(seed)
    model_key = sk(seed, "desc-model", "commitment", "A")
    child_key = sk(seed, "desc-child", "closure", "A")
    use_key = sk(seed, "desc-use", "use", "A")
    old_value, new_value = old.short(), new.short()

    l_old = License(opaque(seed, "desc-old-license"), "persist-model", allowed_writes=(WriteGrant(model_key, (old_value,)),))
    l_child = License(
        opaque(seed, "desc-child-license"),
        "persist-child",
        preconditions=(Precondition(model_key, old_value),),
        allowed_writes=(WriteGrant(child_key, ("AUTHORIZED",)),),
    )
    l_revoke = License(
        opaque(seed, "desc-revoke-license"),
        "revoke-old-model-license",
        allowed_revocations=(l_old.id,),
    )
    l_use = License(
        opaque(seed, "desc-use-license"),
        "use-child",
        preconditions=(Precondition(child_key, "AUTHORIZED"),),
        allowed_writes=(WriteGrant(use_key, ("USED",)),),
    )
    old_commit = Transition("persist-model", writes=(Standing(model_key, old_value),))
    child = Transition("persist-child", writes=(Standing(child_key, "AUTHORIZED"),))
    revoke = Transition("revoke-old-model-license", revoke_licenses=(l_old.id,))
    use = Transition("use-child", writes=(Standing(use_key, "USED"),))

    nano_a = Nano(licenses=(l_old, l_child, l_revoke, l_use))
    naive_a = NaivePersistence()
    for t, lid in ((old_commit, l_old.id), (child, l_child.id), (revoke, l_revoke.id)):
        assert nano_a.apply_transition(t, lid).decision is Decision.ALLOW
        naive_a.apply(t)
    nd_a = naive_a.apply(use)
    nn_a = nano_a.apply_transition(use, l_use.id).decision
    stats.attack(nd_a, nn_a)

    # Matched legal: reauthorize child from the revised Mini commitment under a fresh license.
    l_new = License(opaque(seed, "desc-new-license"), "persist-new-model", allowed_writes=(WriteGrant(model_key, (new_value,)),))
    l_child2 = License(
        opaque(seed, "desc-child2-license"),
        "reauthorize-child",
        preconditions=(Precondition(model_key, new_value),),
        allowed_writes=(WriteGrant(child_key, ("AUTHORIZED",)),),
    )
    nano_l = Nano(licenses=(l_old, l_child, l_revoke, l_use, l_new, l_child2))
    naive_l = NaivePersistence()
    for t, lid in ((old_commit, l_old.id), (child, l_child.id), (revoke, l_revoke.id)):
        assert nano_l.apply_transition(t, lid).decision is Decision.ALLOW
        naive_l.apply(t)
    new_commit = Transition("persist-new-model", writes=(Standing(model_key, new_value),))
    reauth = Transition("reauthorize-child", writes=(Standing(child_key, "AUTHORIZED"),))
    assert nano_l.apply_transition(new_commit, l_new.id).decision is Decision.ALLOW
    assert nano_l.apply_transition(reauth, l_child2.id).decision is Decision.ALLOW
    naive_l.apply(new_commit); naive_l.apply(reauth)
    nd_l = naive_l.apply(use)
    nn_l = nano_l.apply_transition(use, l_use.id).decision
    stats.legitimate(nd_l, nn_l)

    return {
        "mini_revised": org.active["A"].rule == new,
        "nano_attack": nn_a.value,
        "nano_legal_reauthorized": nn_l.value,
    }


def preservation_regression_trial(seed: int, stats: PairStats) -> dict:
    """Revoking an unrelated preserved B warrant must not demote revised A."""
    org, old, new, b = _make_revised_mini(seed ^ 0xA11)
    a_key = sk(seed, "pres-A", "commitment", "A")
    b_key = sk(seed, "pres-B", "commitment", "B")
    a_out = sk(seed, "pres-out", "derived", "A")

    l_a = License(opaque(seed, "pres-la"), "persist-A", allowed_writes=(WriteGrant(a_key, (old.short(),)),))
    l_b = License(opaque(seed, "pres-lb"), "persist-B", allowed_writes=(WriteGrant(b_key, (b.short(),)),))
    l_rev = License(
        opaque(seed, "pres-revise"),
        "revise-A",
        preconditions=(Precondition(a_key, old.short()),),
        allowed_writes=(WriteGrant(a_out, (new.short(),)),),
        required_preservation=(b_key,),
    )
    l_revoke_b = License(opaque(seed, "pres-revoke-b"), "revoke-B", allowed_revocations=(l_b.id,))
    use_key = sk(seed, "pres-use", "use", "A")
    l_use = License(
        opaque(seed, "pres-use-license"),
        "use-revised-A",
        preconditions=(Precondition(a_out, new.short()),),
        allowed_writes=(WriteGrant(use_key, ("USED",)),),
    )

    nano = Nano(licenses=(l_a, l_b, l_rev, l_revoke_b, l_use))
    naive = NaivePersistence()
    ta = Transition("persist-A", writes=(Standing(a_key, old.short()),))
    tb = Transition("persist-B", writes=(Standing(b_key, b.short()),))
    tr = Transition("revise-A", writes=(Standing(a_out, new.short()),))
    rv = Transition("revoke-B", revoke_licenses=(l_b.id,))
    for t, lid in ((ta, l_a.id), (tb, l_b.id), (tr, l_rev.id), (rv, l_revoke_b.id)):
        assert nano.apply_transition(t, lid).decision is Decision.ALLOW
        naive.apply(t)

    # Permanent regression: the unrelated preservation edge must not become a
    # warrant parent.  After B's producing license is revoked, A's derived output
    # must remain usable by a fresh licensed transition.
    use = Transition("use-revised-A", writes=(Standing(use_key, "USED"),))
    nd = naive.apply(use)
    nn = nano.apply_transition(use, l_use.id).decision
    stats.legitimate(nd, nn)
    nano_retained = effective_value(nano, a_out) == new.short()
    return {
        "nano_unrelated_output_retained": nano_retained,
        "nano_post_revocation_use": nn.value,
        "mini_B_unchanged": org.active["B"].rule == b,
    }


def native_mini_lifecycle_trial(seed: int) -> dict:
    """Route actual Mini acquisition/revision commitments through Nano without changing Mini."""
    rng = random.Random(seed ^ 0xBEEF)
    a0, a1, b = choose_rules(rng)
    org = Organism()

    a_key = sk(seed, "life-A", "commitment", "A")
    b_key = sk(seed, "life-B", "commitment", "B")
    l_a0 = License(opaque(seed, "life-la0"), "commit-A0", allowed_writes=(WriteGrant(a_key, (a0.short(),)),))
    l_b = License(opaque(seed, "life-lb"), "commit-B", allowed_writes=(WriteGrant(b_key, (b.short(),)),))
    l_a1 = License(
        opaque(seed, "life-la1"),
        "revise-A",
        preconditions=(Precondition(a_key, a0.short()),),
        allowed_writes=(WriteGrant(a_key, (a1.short(),)),),
        required_preservation=(b_key,),
    )
    nano = Nano(licenses=(l_a0, l_b, l_a1))
    naive = NaivePersistence()

    ax0, ax1 = distinct_inputs(rng)
    org.observe("A", ax0, a0(ax0), "acquire")
    org.observe("A", ax1, a0(ax1), "acquire")
    assert org.active["A"].rule == a0
    t_a0 = Transition("commit-A0", writes=(Standing(a_key, a0.short()),))
    if nano.apply_transition(t_a0, l_a0.id).decision is not Decision.ALLOW:
        return {"pass": False, "failure": "A0 refused"}
    naive.apply(t_a0)

    bx0, bx1 = distinct_inputs(rng)
    org.observe("B", bx0, b(bx0), "acquire")
    org.observe("B", bx1, b(bx1), "acquire")
    assert org.active["B"].rule == b
    t_b = Transition("commit-B", writes=(Standing(b_key, b.short()),))
    if nano.apply_transition(t_b, l_b.id).decision is not Decision.ALLOW:
        return {"pass": False, "failure": "B refused"}
    naive.apply(t_b)

    # Burn A and let unchanged Mini determine when the replacement is identified.
    for x in range(MOD):
        if a0(x) != a1(x):
            org.observe("A", x, a1(x), "counterevidence")
            if len(org.lineage.get("A", [])) == 2:
                break
    if org.needs_probe("A"):
        for x in range(MOD):
            org.observe("A", x, a1(x), "active-probe")
            if not org.needs_probe("A"):
                break
    if org.active["A"].rule != a1:
        return {"pass": False, "failure": "Mini did not revise A"}

    t_a1 = Transition("revise-A", writes=(Standing(a_key, a1.short()),))
    nn = nano.apply_transition(t_a1, l_a1.id).decision
    nd = naive.apply(t_a1)
    active = {s.key: s.value for s in nano.effective_state().active}
    ok = (
        nn is Decision.ALLOW
        and nd is Decision.ALLOW
        and active.get(a_key) == a1.short()
        and active.get(b_key) == b.short()
        and naive.value(a_key) == a1.short()
        and naive.value(b_key) == b.short()
    )
    return {"pass": ok, "nano_revision": nn.value, "A": active.get(a_key), "B": active.get(b_key)}


def sweep(n: int, start_seed: int = 0) -> dict:
    families = {
        "role_laundering": PairStats(),
        "dependency_laundering": PairStats(),
        "acquisition_closure_composition": PairStats(),
        "authority_applicability": PairStats(),
        "stale_descendant": PairStats(),
        "preservation_not_warrant_regression": PairStats(),
    }
    lifecycle_pass = 0
    examples: dict[str, dict] = {}

    for seed in range(start_seed, start_seed + n):
        rows = {
            "role_laundering": role_laundering_trial(seed, families["role_laundering"]),
            "dependency_laundering": dependency_laundering_trial(seed, families["dependency_laundering"]),
            "acquisition_closure_composition": acquisition_closure_trial(seed, families["acquisition_closure_composition"]),
            "authority_applicability": authority_applicability_trial(seed, families["authority_applicability"]),
            "stale_descendant": stale_descendant_trial(seed, families["stale_descendant"]),
            "preservation_not_warrant_regression": preservation_regression_trial(seed, families["preservation_not_warrant_regression"]),
        }
        if seed == start_seed:
            examples = rows
        lifecycle_pass += int(native_mini_lifecycle_trial(seed)["pass"])

    summaries = {name: stat.summary() for name, stat in families.items()}
    attack_attempts = sum(s["attack_attempts"] for s in summaries.values())
    naive_attack_allows = sum(s["naive_attack_allows"] for s in summaries.values())
    nano_attack_allows = sum(s["nano_attack_allows"] for s in summaries.values())
    legit_attempts = sum(s["legitimate_attempts"] for s in summaries.values())
    nano_legit_allows = sum(s["nano_legitimate_allows"] for s in summaries.values())

    return {
        "n": n,
        "mini_sha256": file_sha(MINI_PATH),
        "nano_sha256": file_sha(NANO_PATH),
        "mini_unchanged": file_sha(MINI_PATH) == MINI_EXPECTED_SHA256,
        "nano_v0_unchanged": file_sha(NANO_PATH) == NANO_EXPECTED_SHA256,
        "families": summaries,
        "aggregate": {
            "attack_attempts": attack_attempts,
            "naive_attack_overreach": naive_attack_allows,
            "nano_attack_overreach": nano_attack_allows,
            "nano_attack_overreach_rate": nano_attack_allows / max(1, attack_attempts),
            "legitimate_attempts": legit_attempts,
            "nano_legitimate_allows": nano_legit_allows,
            "nano_legitimate_retention_rate": nano_legit_allows / max(1, legit_attempts),
            "native_mini_lifecycle_pass": lifecycle_pass,
            "native_mini_lifecycle_rate": lifecycle_pass / n,
        },
        "first_seed_examples": examples,
        "claim_boundary": (
            "constructed Mini+Nano composition assay only; external contracts supplied by harness; "
            "no claim of contract correctness, autonomous typing, dependency discovery, truth, or general reliable generalization"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", type=int, default=1000)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    if file_sha(MINI_PATH) != MINI_EXPECTED_SHA256:
        raise SystemExit(f"mini.py changed: {file_sha(MINI_PATH)}")
    if file_sha(NANO_PATH) != NANO_EXPECTED_SHA256:
        raise SystemExit(f"nano.py changed: {file_sha(NANO_PATH)}")

    out = sweep(args.sweep, args.start_seed)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")

    agg = out["aggregate"]
    ok = (
        agg["nano_attack_overreach"] == 0
        and agg["nano_legitimate_allows"] == agg["legitimate_attempts"]
        and agg["native_mini_lifecycle_pass"] == out["n"]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
