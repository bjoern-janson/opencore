#!/usr/bin/env python3
"""OpenCore Mini: a deliberately tiny crank-science organism.

One file. No claim beyond its trace.

Lifecycle exercised:
    experience -> candidate -> commit -> remember -> challenge -> reopen -> reuse

The organism learns scoped affine rules over Z_11, persists them, composes two
learned scopes without joint examples, detects contradictory evidence after a
world change, reopens only the affected scope, and preserves superseded lineage.
"""
from __future__ import annotations

import argparse
import json
import random
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

MOD = 11
HYPOTHESES = tuple((a, c) for a in range(1, MOD) for c in range(MOD))


@dataclass(frozen=True)
class Rule:
    a: int
    c: int

    def __call__(self, x: int) -> int:
        return (self.a * x + self.c) % MOD

    def short(self) -> str:
        return f"{self.a}x+{self.c} mod {MOD}"


@dataclass
class Observation:
    id: int
    scope: str
    x: int
    y: int
    phase: str


@dataclass
class Commitment:
    scope: str
    version: int
    rule: Rule
    status: str
    evidence_ids: list[int]
    parent_version: int | None
    reason: str


class World:
    def __init__(self, a0: Rule, a1: Rule, b: Rule):
        self.rules = {"A": a0, "B": b}
        self.a1 = a1
        self.epoch = 0

    def shift_a(self) -> None:
        self.rules["A"] = self.a1
        self.epoch = 1

    def observe(self, scope: str, x: int) -> int:
        return self.rules[scope](x)


class Organism:
    def __init__(self) -> None:
        self.observations: list[Observation] = []
        self.lineage: dict[str, list[Commitment]] = {}
        self.active: dict[str, Commitment] = {}
        self.challenge_buffers: dict[str, list[int]] = {}
        self.trace: list[str] = []

    def _log(self, msg: str) -> None:
        self.trace.append(msg)

    def _obs(self, oid: int) -> Observation:
        return self.observations[oid]

    @staticmethod
    def _unique_rule(obs: Iterable[Observation]) -> Rule | None:
        data = list(obs)
        if len({o.x for o in data}) < 2:
            return None
        matches: list[Rule] = []
        for a, c in HYPOTHESES:
            r = Rule(a, c)
            if all(r(o.x) == o.y for o in data):
                matches.append(r)
                if len(matches) > 1:
                    # We only care whether the candidate is unique.
                    pass
        return matches[0] if len(matches) == 1 else None

    def observe(self, scope: str, x: int, y: int, phase: str) -> None:
        oid = len(self.observations)
        obs = Observation(oid, scope, x, y, phase)
        self.observations.append(obs)
        self._log(f"EXPERIENCE {scope}: x={x} -> y={y} [{phase}]")

        incumbent = self.active.get(scope)
        if incumbent is None:
            relevant = [o for o in self.observations if o.scope == scope]
            candidate = self._unique_rule(relevant)
            if candidate is not None:
                self._log(f"CANDIDATE {scope}: {candidate.short()}")
                self._commit(scope, candidate, [o.id for o in relevant], reason="acquisition")
            return

        predicted = incumbent.rule(x)
        if scope not in self.challenge_buffers and predicted == y:
            return

        if scope not in self.challenge_buffers:
            self.challenge_buffers[scope] = []
            self._log(
                f"CHALLENGE {scope}: incumbent v{incumbent.version} predicted {predicted}, observed {y}"
            )

        self.challenge_buffers[scope].append(oid)
        challenge_obs = [self._obs(i) for i in self.challenge_buffers[scope]]
        candidate = self._unique_rule(challenge_obs)
        if candidate is not None and candidate != incumbent.rule:
            self._log(f"REOPEN-CANDIDATE {scope}: {candidate.short()}")
            self._reopen(scope, candidate, list(self.challenge_buffers[scope]))
            del self.challenge_buffers[scope]
        else:
            self._log(f"PROBE-REQUEST {scope}: challenge still underdetermined")

    def needs_probe(self, scope: str) -> bool:
        return scope in self.challenge_buffers

    def _commit(self, scope: str, rule: Rule, evidence_ids: list[int], reason: str) -> None:
        version = len(self.lineage.get(scope, [])) + 1
        commit = Commitment(
            scope=scope,
            version=version,
            rule=rule,
            status="active",
            evidence_ids=evidence_ids,
            parent_version=None,
            reason=reason,
        )
        self.lineage.setdefault(scope, []).append(commit)
        self.active[scope] = commit
        self._log(f"COMMIT {scope} v{version}: {rule.short()}")

    def _reopen(self, scope: str, rule: Rule, evidence_ids: list[int]) -> None:
        old = self.active[scope]
        old.status = "superseded"
        version = old.version + 1
        commit = Commitment(
            scope=scope,
            version=version,
            rule=rule,
            status="active",
            evidence_ids=evidence_ids,
            parent_version=old.version,
            reason="counterevidence",
        )
        self.lineage[scope].append(commit)
        self.active[scope] = commit
        self._log(
            f"REOPEN {scope}: v{old.version} -> v{version}; old preserved as superseded"
        )

    def answer(self, scope: str, x: int) -> int | None:
        commit = self.active.get(scope)
        return None if commit is None else commit.rule(x)

    def compose(self, first: str, second: str, x: int) -> int | None:
        a = self.active.get(first)
        b = self.active.get(second)
        if a is None or b is None:
            return None
        return b.rule(a.rule(x))

    def save(self, path: Path) -> None:
        payload = {
            "observations": [asdict(o) for o in self.observations],
            "lineage": {
                scope: [
                    {
                        **asdict(c),
                        "rule": asdict(c.rule),
                    }
                    for c in commits
                ]
                for scope, commits in self.lineage.items()
            },
            "trace": self.trace,
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Organism":
        raw = json.loads(path.read_text(encoding="utf-8"))
        obj = cls()
        obj.observations = [Observation(**o) for o in raw["observations"]]
        for scope, rows in raw["lineage"].items():
            commits: list[Commitment] = []
            for row in rows:
                row = dict(row)
                row["rule"] = Rule(**row["rule"])
                commits.append(Commitment(**row))
            obj.lineage[scope] = commits
            active = [c for c in commits if c.status == "active"]
            if len(active) != 1:
                raise ValueError(f"scope {scope} has {len(active)} active commitments")
            obj.active[scope] = active[0]
        obj.trace = list(raw["trace"])
        obj._log("REMEMBER restart: durable commitments reloaded")
        return obj


def choose_rules(rng: random.Random) -> tuple[Rule, Rule, Rule]:
    rules = [Rule(a, c) for a, c in HYPOTHESES]
    a0, a1, b = rng.sample(rules, 3)
    return a0, a1, b


def distinct_inputs(rng: random.Random) -> tuple[int, int]:
    x0 = rng.randrange(MOD)
    x1 = rng.randrange(MOD - 1)
    if x1 >= x0:
        x1 += 1
    return x0, x1


def run_once(seed: int, verbose: bool = False) -> dict:
    rng = random.Random(seed)
    a0, a1, b = choose_rules(rng)
    world = World(a0, a1, b)
    org = Organism()

    # Acquire A and B from two points each.
    for scope in ("A", "B"):
        x0, x1 = distinct_inputs(rng)
        org.observe(scope, x0, world.observe(scope, x0), "acquire")
        org.observe(scope, x1, world.observe(scope, x1), "acquire")

    # Restart: only durable organism state survives.
    with tempfile.TemporaryDirectory() as td:
        state_path = Path(td) / "organism.json"
        org.save(state_path)
        org = Organism.load(state_path)

    probe = rng.randrange(MOD)
    remembered_a = org.answer("A", probe) == a0(probe)

    # Never saw A+B jointly.
    composed_before = org.compose("A", "B", probe) == b(a0(probe))
    unknown_defers = org.compose("A", "C", probe) is None

    # Burn A with a world change; B is stable.
    world.shift_a()
    before_b = org.answer("B", probe)
    cx0, cx1 = distinct_inputs(rng)
    org.observe("A", cx0, world.observe("A", cx0), "counterevidence")
    org.observe("A", cx1, world.observe("A", cx1), "counterevidence")

    # If the first post-change point happened to be the unique old/new crossing,
    # contradiction appears only on the second point. The organism then asks for
    # one more observation instead of pretending one contradictory point is enough.
    if org.needs_probe("A"):
        used = {cx0, cx1}
        px = next(x for x in range(MOD) if x not in used)
        org.observe("A", px, world.observe("A", px), "active-probe")

    corrected_a = org.answer("A", probe) == a1(probe)
    unchanged_b = org.answer("B", probe) == before_b == b(probe)
    composed_after = org.compose("A", "B", probe) == b(a1(probe))
    lineage_ok = (
        len(org.lineage.get("A", [])) == 2
        and org.lineage["A"][0].status == "superseded"
        and org.lineage["A"][1].status == "active"
        and org.lineage["A"][1].parent_version == 1
    )

    checks = {
        "remembered_A": remembered_a,
        "novel_A_then_B": composed_before,
        "unknown_A_then_C_defers": unknown_defers,
        "corrected_A": corrected_a,
        "B_unchanged": unchanged_b,
        "composition_updated": composed_after,
        "old_A_preserved_in_lineage": lineage_ok,
    }
    result = {
        "seed": seed,
        "truth": {"A0": a0.short(), "A1": a1.short(), "B": b.short()},
        "probe": probe,
        "checks": checks,
        "pass": all(checks.values()),
        "trace": org.trace,
    }

    if verbose:
        print("OPENCORE MINI / CRANK RUN")
        print(f"seed={seed}")
        print(f"hidden truth: A0={a0.short()} | A1={a1.short()} | B={b.short()}")
        print("\nTRACE")
        for line in org.trace:
            print("  " + line)
        print("\nCHECKS")
        for name, ok in checks.items():
            print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        print(f"\nRESULT: {'PASS' if result['pass'] else 'FAIL'}")
    return result


def sweep(n: int, start_seed: int = 0) -> int:
    failures: list[dict] = []
    for seed in range(start_seed, start_seed + n):
        r = run_once(seed)
        if not r["pass"]:
            failures.append(r)
    print(f"sweep={n} pass={n-len(failures)} fail={len(failures)}")
    if failures:
        first = failures[0]
        print(f"first_failure_seed={first['seed']}")
        print(json.dumps(first["checks"], indent=2, sort_keys=True))
        return 1
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--sweep", type=int, default=0)
    args = p.parse_args()
    if args.sweep:
        return sweep(args.sweep, args.seed)
    run_once(args.seed, verbose=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
