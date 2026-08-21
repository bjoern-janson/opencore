# OpenCore Crank

> **Experimental lineage. Not the formal K0/E001 program.**
>
> This directory is where OpenCore's deliberately breakable adaptive experiments live. The frozen formal branches and top-level K0/E001 documents are not amended by these crank experiments.

## The idea in one sentence

**OpenCore is testing whether a very small persistent computational world can let adaptive processes learn, revise, generalize, and self-correct without allowing every successful prediction, shortcut, or mistake to silently become durable authority.**

The current experimental split is:

```text
OpenCore Nano  -> tiny persistence substrate / transition checker
OpenCore Mini  -> tiny adaptive organism / proposer
OpenCore Base  -> shared authority-filtered world with heterogeneous local projections
```

The Nano/Mini/Base distinctions emerged experimentally rather than being imposed as a complete architecture in advance.

## Start here

| Document | Purpose |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Nano, Mini, Base, and the organism/world split |
| [`docs/EXPERIMENTAL_LINEAGE.md`](docs/EXPERIMENTAL_LINEAGE.md) | M1-M6, external attacks, R1, Nano, ablation, Base-001/002 |
| [`docs/DEVELOPMENTAL_THEORY.md`](docs/DEVELOPMENTAL_THEORY.md) | Frozen systems-level hypothesis: corrective exposure and persistent authority |
| [`docs/TRANSITION_INVARIANT.md`](docs/TRANSITION_INVARIANT.md) | Candidate common structure: premature quotient vs unauthorized refinement |
| [`docs/RELIABLE_GENERALIZATION.md`](docs/RELIABLE_GENERALIZATION.md) | Warranted invariance / transfer-boundary program and R1 |
| [`docs/RESEARCH_METHOD.md`](docs/RESEARCH_METHOD.md) | Crank-science discipline: build, attack, minimally repair, freeze |
| [`docs/CLAIM_BOUNDARIES.md`](docs/CLAIM_BOUNDARIES.md) | What is supported, candidate, open, or explicitly not claimed |
| [`NANO_V0.md`](NANO_V0.md) | Frozen Nano V0 scientific entry |
| [`MINI_NANO_COMPOSITION_V0.md`](MINI_NANO_COMPOSITION_V0.md) | First constructed Mini × Nano composition result |
| [`NANO_MINI_ABLATION_V0.md`](NANO_MINI_ABLATION_V0.md) | Subtractive decomposition of the Mini × Nano protection result |
| [`BASE_001_SHARED_WORLD.md`](BASE_001_SHARED_WORLD.md) | Shared authority-filtered world across 12 heterogeneous local units |
| [`BASE_002_GLOBAL_REOPENING.md`](BASE_002_GLOBAL_REOPENING.md) | Global reopening, replacement separation, and the guard/warrant wound |
| [`NANO_GUARD_WARRANT_DISCRIMINATION_V0.md`](NANO_GUARD_WARRANT_DISCRIMINATION_V0.md) | GW-001 repair-discrimination assay for Base-002B's live wound |
| [`FOREIGN_001_MASTERMIND.md`](FOREIGN_001_MASTERMIND.md) | First foreign pressure specimen: Mastermind representation/interface localization |
| [`FOREIGN_002_RESTLESS_BANDIT.md`](FOREIGN_002_RESTLESS_BANDIT.md) | Foreign scarce-attention specimen: restless-bandit allocation pressure |
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

Many critical distinctions in later experiments remain harness-supplied rather than autonomously discovered.

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

Its V0 checks include:

```text
current state satisfies license preconditions
requested effect stays inside license effect ceiling
required preservation remains preserved
warrant-parent authority remains live
```

The payload semantics remain opaque to Nano. The transition-contract surface is inspectable.

The compact V0 rule is:

> **Don't write beyond your effect capability. Don't erase beyond your preservation capability.**

Nano does not establish that an external contract is epistemically correct.

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

This remains a candidate compression, not a proven universal law or kernel primitive.

## Nano V0 isolated result

On the frozen constructed six-family matrix:

```text
Overreach       = 0 / 60,000
False refusal   = 0 / 60,000
Invariant fails = 0
```

Naive persistence accepted every illegal transition in the same matrix.

Two pre-repair failures are part of the result:

```text
lineage recorded != lineage causally governing authority
preservation dependency != warrant dependency
```

See [`NANO_V0.md`](NANO_V0.md) and [`nano_experiment_v0.md`](nano_experiment_v0.md).

## Mini × Nano Composition V0

The first integration kept wounded Mini and Nano V0 byte-identical and changed only the persistence boundary.

Across 10,000 seeds:

```text
illegal attempts accepted by naive persistence = 50,000 / 50,000
illegal attempts accepted by Nano V0           =      0 / 50,000
matched legitimate transitions accepted        = 60,000 / 60,000
native Mini lifecycle control                   = 10,000 / 10,000
```

The narrow causal interpretation is:

> **The same adaptive proposer can remain free to generate a bad epistemic proposal while a small external persistence boundary prevents that proposal from silently acquiring durable authority under the supplied transition contract.**

See [`MINI_NANO_COMPOSITION_V0.md`](MINI_NANO_COMPOSITION_V0.md).

## Nano × Mini ablation V0

The next experiment was subtractive rather than additive. The exact frozen Mini × Nano wound cases were routed through reduced persistence boundaries.

Final 10,000-seed overreach:

```text
naive                         50,000 / 50,000
EFFECT_CEILING_ONLY           50,000 / 50,000
LIVE_PRECONDITIONS_ONLY       10,000 / 50,000
LINEAGE_LIVENESS_ONLY         40,000 / 50,000
PRECONDITIONS_PLUS_LINEAGE         0 / 50,000
FULL_NANO                          0 / 50,000
```

Every arm retained all 60,000 matched legitimate transitions and all 10,000 tested Mini lifecycles.

On this frozen wound suite, full Nano's observed protection is reproduced by:

```text
execution-time live preconditions
+
causal warrant-dependency liveness
```

Neither mechanism alone is sufficient. The suite does **not** establish effect-ceiling or preservation enforcement as globally redundant; those dimensions were not identified as necessary by this intervention family.

See [`NANO_MINI_ABLATION_V0.md`](NANO_MINI_ABLATION_V0.md).

## Base-001: shared authority-filtered world

Base-001 constructed twelve heterogeneous local projectors over the unchanged Nano V0 substrate.

A single warranted global standing `G` was available to all units, affected only externally designated relevant units, and later lost authority through one upstream warrant revocation.

Across 10,000 worlds:

```text
Reach                    120,000 / 120,000
RelevantResponse          80,000 / 80,000
IrrelevantDisturbance          0 / 40,000
RevocationRecovery        80,000 / 80,000
NaiveRevocationRecovery        0 / 80,000
CollateralLoss                 0 / 120,000
```

No destructive local cleanup writes were required. Unrelated local adaptations created after `G` survived because temporal ancestry was not treated as warrant ancestry.

Base-001 also supplied independently motivated pressure on Nano's effect ceiling: a local derived standing could not be promoted into global authority without a separately licensed global-write edge.

See [`BASE_001_SHARED_WORLD.md`](BASE_001_SHARED_WORLD.md).

## Base-002: global reopening and a new Nano wound

Base-002 separated:

```text
ADMIT(G) != REOPEN(G) != REPLACE(G, G')
```

### Positive path

A target-bound counterexample-backed reopen capability could withdraw `G`'s authority, propagate constructed uncertainty through dependent local projections, preserve unrelated learning, and refuse to install `G'`. Later separately authorized evidence could install `G'`.

Thus, on the constructed path:

```text
refutation authority != replacement authority
```

### Negative strict control

A stricter natural reopen contract additionally required `G_STATUS=EFFECTIVE` as a precondition. Nano V0 automatically promoted every precondition source into a continuing warrant parent. The new `REOPENED` standing therefore depended on the old `G` standing whose authority the same transition revoked and self-invalidated in 10,000/10,000 strict controls.

The forced distinction is:

```text
execution guard != warrant dependency
```

or:

> **A fact can be required for a transition to occur without being something the resulting authority should continue to depend on.**

No Nano repair is made or implied by this publication.

See [`BASE_002_GLOBAL_REOPENING.md`](BASE_002_GLOBAL_REOPENING.md).


## GW-001 and foreign pressure specimens

The next crank sequence deliberately stopped extending the OpenCore-native architecture and instead applied discriminating and foreign pressure.

**GW-001** attacked Base-002B without modifying Nano. It established behaviorally that the facts required for transition execution need not be identical to the facts whose continuing authority should govern the result:

```text
CheckSet(T) != ParentSet(Result(T))
```

In the decisive mixed-role witness, two facts were both required for execution, but later revocation showed that only one should remain a continuing authority parent. Structural special-case repairs for same-key, revoked-source, and self-invalidating transitions all failed at least one control. Selective continuing ancestry is supported on the constructed family; a `Guard`/`WarrantPremise` schema and Nano V1 remain unearned.

**FOREIGN-001** then exposed the frozen stack to reduced Mastermind rather than another OpenCore-native task. Static worlds supplied sufficient evidence and a live Nano authority path, but frozen Mini had no affine hypothesis capable of representing any complete Mastermind feedback function. Dynamic worlds separately showed that a real hidden mechanism change can remain observationally compatible with an unchanged explanation.

**FOREIGN-002** changed pressure again to a small deterministic restless-bandit family while controlling FOREIGN-001's representation wound: every latent arm state was inside Mini's existing affine hypothesis class. Mini's existing `needs_probe` behavior usefully spent follow-up attention after contradiction and improved reward/repair completion, but it did not improve prospective discovery of still-hidden shifts. The candidate distinction is:

```text
reactive corrective attention != prospective discovery attention
```

No Mini repair, Nano repair, Base extension, attention scheduler, or universal foreign-task layer is earned by these specimens.

## Systems-level theory freeze

The current systems-level compression is deliberately frozen as a hypothesis:

```text
Reality
-> challenge / apparatus
-> consequence
-> organism interpretation
-> candidate transition
-> persistent authority
```

with:

```text
reality != measurement != interpretation != authority
```

The developmental hypothesis is:

> **Intelligence develops by constructing increasingly useful ways for reality to correct what currently governs it.**

A prospective developmental frontier requires:

```text
live alternatives
+
discriminable challenge
+
recoverable consequence
+
live authority-update path
```

The corresponding agency/authority split is:

> **The organism chooses where to risk being wrong.**
>
> **The persistence world constrains what the resulting consequence is allowed to change.**

This is not a demonstrated general developmental loop. See [`docs/DEVELOPMENTAL_THEORY.md`](docs/DEVELOPMENTAL_THEORY.md).

## Research posture

The discipline remains:

```text
build tiny thing
-> run it
-> attack it
-> localize the shallowest failure
-> make the minimal repair only when earned
-> preserve negative results
-> retest
-> freeze only what the evidence earned
```

A successful component does not certify its composition:

```text
Valid(T1) + Valid(T2) !=> Valid(T2 o T1)
```

And a clean benchmark result does not grant authority outside the tested family.

The current theory stop is intentional. The next useful advancement should be empirical rather than further conceptual elaboration.

## Formal lineage separation

The crank branch is deliberately separate from the formal OpenCore experiment lineage.

Nothing in this directory modifies K0, completes E001, supplies E001 evaluation evidence, reveals E001 evaluation seeds, or grants authority over the formal program.

## Frozen component hashes

```text
mini.py
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55

nano.py
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329

mini_nano_composition.py
116d6e285855081126608a962ad5bb3990f634c63bf76a40c19f7ad18027e7a2
```

Those identities remain load-bearing for the Nano V0, composition, ablation, and Base experiments that reuse them.
