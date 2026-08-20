# OpenCore Crank

> **Experimental lineage. Not the formal K0/E001 program.**
>
> This directory is where OpenCore's deliberately breakable adaptive experiments live. The frozen formal branches and top-level K0/E001 documents are not amended by these crank experiments.

## The idea in one sentence

**OpenCore is testing whether a very small persistent computational world can let adaptive processes learn, revise, generalize, and self-correct without allowing every successful prediction, shortcut, or mistake to silently become durable authority.**

The current experimental split is:

```text
OpenCore Nano  -> tiny persistence substrate / transition typechecker
OpenCore Mini  -> tiny adaptive organism / proposer
OpenCore Base  -> mental model for a broader world containing adaptive processes + a shared persistence substrate
```

The Nano/Mini distinction was not imposed at the start. It emerged from attacks on Mini's persistence and authority transitions.

## Start here

| Document | Purpose |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Nano, Mini, Base, and the organism/world split |
| [`docs/EXPERIMENTAL_LINEAGE.md`](docs/EXPERIMENTAL_LINEAGE.md) | M1-M6, external attacks, R1, Nano V0, Mini × Nano |
| [`docs/TRANSITION_INVARIANT.md`](docs/TRANSITION_INVARIANT.md) | Candidate common structure: premature quotient vs unauthorized refinement |
| [`docs/RELIABLE_GENERALIZATION.md`](docs/RELIABLE_GENERALIZATION.md) | Warranted invariance / transfer-boundary program and R1 |
| [`docs/RESEARCH_METHOD.md`](docs/RESEARCH_METHOD.md) | Crank-science discipline: build, attack, minimally repair, freeze |
| [`docs/CLAIM_BOUNDARIES.md`](docs/CLAIM_BOUNDARIES.md) | What is supported, candidate, open, or explicitly not claimed |
| [`NANO_V0.md`](NANO_V0.md) | Frozen Nano V0 scientific entry |
| [`MINI_NANO_COMPOSITION_V0.md`](MINI_NANO_COMPOSITION_V0.md) | First constructed Mini × Nano composition result |
| [`results/`](results/) | Raw decisive result snapshots |

## Mini: the adaptive process

[`mini.py`](mini.py) is intentionally tiny and wounded.

It can learn simple affine rules, persist them, compose them, detect some contradictions, request further probes when a replacement is underdetermined, revise locally, and preserve unaffected commitments.

The point of Mini is not to look generally intelligent. The point is to expose where apparently successful adaptive behavior still makes unjustified epistemic moves.

A compressed trajectory is:

```text
experience
  -> candidate
  -> commit
  -> reuse
  -> challenge
  -> reopen
  -> revise
  -> alter some future closure behavior
```

The experimentally important gaps are just as important as the successes: many critical distinctions are still supplied by the harness rather than discovered autonomously.

## Nano: the persistence boundary

[`nano.py`](nano.py) is not a learner.

The frozen V0 mental model is:

```text
OpenCore Nano = transition typechecker + append-only in-process journal
```

Nano receives a current transition-visible state `S_t`, a proposed transition `T`, and an externally constituted license `L`:

```text
(S_t, T, L) -> ALLOW | DENY | DEFER
```

Its V0 checks are deliberately small:

```text
current state satisfies license preconditions
requested effect stays inside license effect ceiling
required preservation remains preserved
warrant-parent authority remains live
```

The payload semantics remain opaque to Nano. The contract surface is inspectable.

The compact V0 rule is:

> **Don't write beyond your effect capability. Don't erase beyond your preservation capability.**

Nano does not establish that the external contract is correct.

## Why transitions became central

The crank sequence repeatedly found states that looked individually acceptable but transitions between them that were not.

Examples:

```text
correct prediction        -> observation authority        [invalid promotion]
correlated reports        -> independent corrective paths [invalid promotion]
closure authority         -> applicability                [invalid promotion]
old authorization token   -> current authorization        [stale precondition]
aliased states            -> one observed state           [lost distinction]
revoked warrant ancestor  -> descendant still effective   [stale standing]
```

This produced a candidate two-sided failure family:

```text
premature quotient       = erase a distinction future correction still needs
unauthorized refinement  = create a distinction/authority not warranted upstream
```

This is a **candidate common substrate**, not a proven law and not yet an OpenCore kernel primitive.

## Nano V0 isolated result

On the frozen constructed six-family matrix:

```text
Overreach       = 0 / 60,000
False refusal   = 0 / 60,000
Invariant fails = 0
```

Naive persistence accepted every illegal transition in the same matrix.

The more important V0 result was that Nano itself failed twice before this result:

```text
lineage recorded != lineage causally governing authority
preservation dependency != warrant dependency
```

Those failures forced the implementation to distinguish historical lineage, warrant dependency, and preservation obligation.

See [`NANO_V0.md`](NANO_V0.md) and [`nano_experiment_v0.md`](nano_experiment_v0.md).

## Mini × Nano composition result

The first integration kept both components frozen and changed only the persistence boundary.

Across 10,000 seeds:

```text
illegal attempts accepted by naive persistence = 50,000 / 50,000
illegal attempts accepted by Nano V0           =      0 / 50,000
matched legitimate transitions accepted        = 60,000 / 60,000
native Mini lifecycle control                   = 10,000 / 10,000
```

The strongest causal interpretation is narrow:

> **The same adaptive proposer can remain free to generate a bad epistemic proposal while a small external persistence boundary prevents that proposal from silently acquiring durable authority under the supplied transition contract.**

This does **not** establish general Mini+Nano compatibility, contract correctness, truth, reliable generalization, or universal lawful composition.

See [`MINI_NANO_COMPOSITION_V0.md`](MINI_NANO_COMPOSITION_V0.md).

## Current research frontier

The reliable-generalization program reframes transfer as a question of **warranted invariance**:

```text
not merely:  can H predict in a new context?

but:         what evidence licenses treating the old and new contexts
             as equivalent for transport of H?
```

The first precursor, R1, has been run locally: given two opaque transfer hypotheses that are observationally equivalent on the initial history, the transfer-aware controller used a one-probe budget to select a discriminating future context and resolve the correct candidate in 10,000/10,000 constructed worlds. Passive control resolved 0%; random probing resolved about 25% in the 2-of-8 geometry.

R1 does **not** establish autonomous transfer-boundary discovery. The candidate transfer hypotheses and disagreement-selection machinery were externally constituted.

See [`docs/RELIABLE_GENERALIZATION.md`](docs/RELIABLE_GENERALIZATION.md).

## Research posture

The discipline is intentionally conservative about abstraction and aggressive about failure:

```text
build tiny thing
-> run it
-> attack it
-> localize the shallowest failure
-> make the minimal repair
-> preserve negative results
-> retest
-> freeze only what the evidence earned
```

A mechanism is not promoted merely because it sounds elegant.

A successful component does not certify its composition:

```text
Valid(T1) + Valid(T2) !=> Valid(T2 o T1)
```

And a clean benchmark result does not grant authority outside the tested family.

## Formal lineage separation

The crank branch is deliberately separate from the formal OpenCore experiment lineage.

The formal artifacts remain governed by their own freezes, claim ceilings, and seed-custody rules. Nothing in this directory modifies K0, completes E001, supplies E001 evaluation evidence, or grants authority over the formal program.

## Current component hashes

```text
mini.py
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55

nano.py
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

These hashes are load-bearing for the published Nano V0 / Mini × Nano V0 records.
