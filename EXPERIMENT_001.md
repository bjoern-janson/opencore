# Experiment 001: Scoped Reopening Versus Archive Replay

> **STATUS: FROZEN PROSPECTIVE PROTOCOL SHELL / UNIMPLEMENTED**
>
> **EXECUTION: BLOCKED PENDING SEED COMMITMENTS AND EXECUTION MANIFEST**
>
> **RESULTS: NONE RECORDED**
>
> **TARGET: THE OPENCORE K0 COMMIT CONTAINING THIS FILE**
>
> **TERMINAL STATUS: UNASSIGNED**

This document freezes the experimental decisions that may not be changed after
either implementation is profiled. The later execution manifest may instantiate
only the hashes, committed seeds, implementations, and measurements required
here; it may not alter the world family, controls, budgets, decision rule,
terminal statuses, or claim ceiling.

## 1. Question

With observations, hypothesis generation, evaluation, authority, persistent
capacity, and the transaction kernel held fixed, does a commitment-addressed
executable reopening path produce a prospectively measurable correction-cost
advantage over a usable archive-replay path?

This is a finite mechanism assay. It is not a learner benchmark or a test of
universal intelligence.

## 2. Arms and estimands

### 2.1 `OPEN`

Persistent scoped commitments bind executable reopening interfaces resolved
through the transition substrate. A valid external correction may address and
revise the affected commitment without reconstructing all active state.

### 2.2 `ARCHIVE_REPLAY`

The serious rival receives the same observations, admitted evidence, finite
hypothesis library, proposer, evaluator, authority verifier, persistent byte
budget, and generic composition operator. It may deterministically reconstruct
active state from its durable archive during a declared recovery/correction
window. It has no commitment-addressed incremental reopening operation.

It must receive generic indexing or cache capacity equal in bytes to the Open
route index. Its permitted mechanism is frozen operationally:

```text
fresh_state = ArchiveReducer.fold(
  empty_state,
  ArchiveQuery(ordered_canonical_record_stream, optional_exact_scope_filter)
)
```

`ArchiveQuery` may use the frozen generic index to return immutable record IDs in
canonical order, including an exact scope filter. `ArchiveReducer` must start
from fresh active state and fold the returned records. It may not address or
mutate an existing commitment, traverse `ReopeningBinding`, or apply a targeted
delta to current active state. An efficient indexed replay remains Archive; it
is not reclassified after results are seen. The reducer, query API, record
schema, and index are hashed before subject implementation. Starving replay or
forbidding this reconstruction invalidates the comparison.

### 2.3 `POINTER_ONLY`

The same history is retained, but neither executable reopening nor archive
reconstruction is allowed. This is a sanity negative control, never the serious
rival.

### 2.4 Two non-collapsing outcome views

The Open mechanism has the prospective witness vector:

```text
(M, R_chi, S, A)
```

where:

- `M` is functional persistence across restart;
- `R_chi` is causal mediation by the declared reopening interface;
- `S` is exact scoped composition and propagation;
- `A` is commit-boundary authority integrity.

The cross-arm comparison uses an implementation-neutral outcome vector:

```text
(M, C_corr, S, A)
```

where `C_corr` is correct, scoped, durable post-correction state with B and
unrelated scope invariant. `ARCHIVE_REPLAY` is not required to instantiate
`R_chi`; its inability to use `chi` cannot itself count as an Open advantage.

Both vectors are non-compensatory. No aggregate task score may trade one
dimension against another.

## 3. Frozen mainline

```text
A acquisition
  -> B acquisition
  -> restart and return to A
  -> A+B novel composition
  -> valid scoped correction of A
  -> capability-validity twin on a second scoped correction
```

Stable opaque scope tags for A, B, and C exist before Phase 1. Phase 2 adds a new
commitment; it does not rescope or reopen A. The first use of A's reopening path
is reserved for Phase 5, so the `-R` ablation has a prospectively localized first
divergence.

## 4. Exact synthetic world family

### 4.1 Payloads and hypotheses

The payload space is the prime field `Z_11`. The public finite hypothesis library
is:

```text
H = {x -> a*x + c mod 11 | a in {1,...,10}, c in Z_11}
```

Any two observations at distinct inputs identify one member of `H` uniquely.
The fixed external proposer enumerates `H` canonically and returns the unique
consistent candidate or `UNDERDETERMINED`. Proposal discovery is not an outcome
of this experiment.

### 4.2 Rule epochs

For each seed, the external generator deterministically selects an ordered
quadruple:

```text
(T_A0, T_A1, T_A2, T_B) in H^4
```

by drawing canonical candidates and rejecting until all conditions hold:

1. every map is non-identity and all four maps are distinct;
2. `T_B o T_Ai` differs from `T_Ai`, `T_B`, and `T_Ai o T_B` for each
   `i in {0,1,2}`;
3. every pair of distinct maps disagrees on at least nine payloads;
4. the two evidence inputs for each map are distinct;
5. the remaining nine payloads are reserved for that map's held-out checks.

The environment epochs are:

```text
e0: A uses T_A0; B uses T_B
e1: A uses T_A1; B remains T_B
e2: A uses T_A2; B remains T_B
```

The public composition algebra is stable across epochs:

```text
SEQ(A, B)(x) = T_B(T_Ai(x))
```

No joint A+B example is supplied. C is a syntactically valid opaque scope with
no observations, warrant, rule, or transition authority in this experiment.

### 4.3 Surface isolation and adapter boundary

The seed independently permutes scope labels, operation labels, payload
presentation, and observation encoding. Randomization mitigates fixed-answer
hardcoding; the sealed-seed procedure below supplies the actual isolation.

The domain adapter may only:

- decode and encode a payload in `Z_11`;
- map an opaque scope token to an opaque internal identifier;
- parse the generic `SEQ(scope_1, scope_2)` syntax.

It cannot access the selected transformations, held-out answers, rule epoch,
phase label, evaluator decision, or authority status, and it cannot compute a
composition result. The same generic composition operator is used in every arm
and every seed.

## 5. Seed and implementation freeze

Before implementation begins, an external seed custodian must publish the world
generator, hypothesis library, surface codec, Archive reducer/query API, record
schema, generic index, and reference-meter interpreter source hashes plus
SHA-256 commitments to 64 independently sampled 256-bit evaluation seeds. Seed
values remain sealed until after the final subject implementation and
execution-manifest hashes are published. None of those pre-subject artifacts may
change after either arm is profiled.

Development uses exactly 32 seeds derived as:

```text
SHA256("OpenCore-K0-E001-development" || uint32_be(i)), i = 0..31
```

Evaluation uses the 64 committed seeds. No failed or inconvenient evaluation
seed may be removed or replaced. Every reported terminal status aggregates all
64.

The execution manifest must freeze:

- the K0 commit;
- pre-subject world-generator, hypothesis-library, surface-codec,
  Archive reducer/query, record-schema, index, and meter-interpreter hashes;
- the 64 seed commitments and later reveal procedure;
- kernel, proposer, adapter, state strategy, evaluator, authority, persistence,
  meter, and adjudicator hashes;
- external reference contract `(P,h,B,Omega,Boundary_SE)` and every role epoch;
- canonical codecs and all fault-injection component hashes;
- purge/recovery procedure and the measurement instrumentation.

Implementation may be debugged against the 32 development seeds. Final hashes
are then frozen, the 64 seeds are revealed, and exactly one predeclared
evaluation campaign runs. That campaign includes the deterministic duplicate
executions required by validity gate 15; they are validity checks, not optional
reruns or opportunities to alter an outcome. Any additional subject execution
or any code, threshold, metric, or seed change after reveal creates a successor
experiment.

## 6. Frozen Phase-5 cost model and comparison rule

Persistent capacity is fixed at 65,536 bytes per arm, including route or archive
indexes. Evaluator calls per correction are capped at four and semantic commit
attempts at two. These are validity limits, not differential metrics.

### 6.1 Causal metering window

The primary differential meters **Phase 5 only**. For each arm and seed, reset
the phase meter immediately before delivery of the already seed-fixed first
Phase-5 `Observation`. Start from the arm's semantically equivalent Phase-4
state. Stop only at a typed stop or after the external persistence verifier has
established `DurablyCommitted` and verified that the receipt's bound durable
result digest equals the canonical read-back digest of the ready active semantic
state. `SemanticCommitted`, `PersistencePending`, and a receipt issued before
active-state reconstruction or readback do not stop the meter. Phase-3 recovery,
Phase-4 composition, Phase-6 authority testing, and all post-correction held-out
queries are outside this differential meter.

After the meter stops, run `C_corr` and the post-correction portion of `S` with
updates disabled. Their pass/fail gates the correction result but their query
cost does not enter the reopening-cost comparison. `M` and `A` are separately
reported maximum-envelope gates.

### 6.2 Canonical meter units

All computation capable of influencing the Phase-5 proposal, candidate,
semantic commit, or durable active successor must cross the frozen
reference-meter API and be replayable by its deterministic interpreter. This
explicitly includes `ArchiveQuery`, `ArchiveReducer.fold`, persistence,
canonical readback, active-state reconstruction, and successor-digest
verification. The meter emits:

- `canonical_bytes_accessed`: every canonical byte returned from semantic state,
  archive, index, or cache, regardless of physical packing or cache hit;
- `reference_ops`: one count for each frozen operation
  `READ_CANONICAL`, `FOLD_RECORD`, `LOOKUP_KEY`, `APPLY_AFFINE`, `COMPOSE`,
  `BUILD_DELTA`, `COMPARE`, or `HASH_BLOCK_32`.

`READ_CANONICAL` reports exact canonical bytes and cannot bundle unmetered work.
An index lookup counts both its key and returned canonical bytes. Every reference
operation and every evaluator, authority, persistence, or readback call advances
the deterministic reference clock by one tick. Any candidate byte that the
external interpreter cannot reproduce from the metered arm-specific trace makes
the run invalid. The same applies to every result-affecting semantic-commit,
reconstruction, persistence, readback, and active-successor byte. Host-language
work between meter calls cannot influence any of those artifacts.

The Cartesian Phase-5 sweep is:

```text
canonical_bytes_accessed in {256, 512, 1024, 2048, 4096, 8192}
reference_ops in {32, 64, 128, 256, 512, 1024}
h = 1024 deterministic reference ticks
```

### 6.3 Decision rule

For arm `j` and seed `s`, let `CorrSuccess_j(s)` be the set of Phase-5 envelopes
in which the arm completes reconstruction and persistence, externally verifies
the canonical read-back active-state digest, and reaches the resulting durable
successor before the meter stops, then passes `C_corr` and the post-correction
`S` checks. If the durable active successor is not ready and verified inside an
envelope, that envelope is not in `CorrSuccess_j(s)`.

Both serious arms must pass the full implementation-neutral vector at the
maximum envelope on all 32 development seeds before evaluation; otherwise the
apparatus is not ready to freeze.

On the 64 evaluation seeds, a valid Open differential requires:

```text
for every seed s:
  CorrSuccess_ARCHIVE(s) is a subset of CorrSuccess_OPEN(s)
and
for at least one seed s:
  CorrSuccess_ARCHIVE(s) is a strict subset
```

`ARCHIVE_REPLAY` must pass Phase 5 at the maximum envelope on all 64 evaluation
seeds; otherwise the serious rival is underconstituted rather than defeated by a
broken control. If `OPEN` fails at the maximum envelope, the valid terminal
result is an OpenCore witness failure, not an invalid experiment.

If Archive weakly dominates, the sets are mixed/non-nested, or they are equal,
the terminal result is `VALID NO OPEN DIFFERENTIAL`; record subtype
`ARCHIVE_DOMINANT`, `MIXED`, or `PARITY`. Set inclusion does not assume that an
implementation's success is monotone in the envelope.

Phase-specific M-recovery and Phase-6 authority costs, wall-clock latency, and
actual persistent bytes are reported descriptively but cannot decide the
primary result.

## 7. Phase protocol

### Phase 0: apparatus validation

The external adjudicator verifies hashes, seed commitments, role separation,
budget meters, codecs, fault components, recovery controls, and both serious
arms' development-seed qualification. Failure or ambiguity yields
`INVALID / UNDERCONSTITUTED` and no evidence about the mechanism.

### Phase 1: acquire A

In epoch `e0`, expose the two seeded A observations. The fixed proposer returns
the unique `T_A0` candidate. The external evaluator issues the exact warrant and
the authority minter supplies a fresh capability bound to the candidate, A
scope, parent, protocol, branch, and epochs.

Persist `u_A0` and record its semantic-state digest, commit identifier, receipt,
lineage, scope, route descriptor, and—for `OPEN`—reopening binding.

### Phase 2: acquire B without reopening A

Expose the two seeded B observations and persist the uniquely warranted `T_B`
commitment through a fresh exact capability. A's content, scope, applicability,
and lineage identity remain unchanged. This phase must not traverse `chi_A`.

### Phase 3: restart and return to A

Terminate the subject process. Purge transient working memory, raw environment
event delivery, and non-durable caches. Retain only declared durable canonical
observation/evidence/commit/receipt records and the arm's allowed indexes.

During restart, `ARCHIVE_REPLAY` may reconstruct its active state from those
durable records. This is classified as recovery, not new observation, learning,
evaluation, or semantic commit. Every durable read and transition step is
metered. Once recovery closes, both arms answer held-out A payloads with probes,
learning, evaluator calls, and commits disabled.

### Phase 4: novel A+B composition

With learning and commits still disabled, query held-out payloads in the unseen
`SEQ(A,B)` context. The answer must be `T_B(T_A0(x))`. Query A+C and require
`DEFER/UNRESOLVED`, not extrapolation or invention.

### Phase 5: valid correction of A

Move the world to epoch `e1` and supply the two seeded observations that uniquely
identify `T_A1`. The external evaluator issues a warrant for exactly the scoped A
revision. The authority minter supplies a fresh single-use capability bound to
the exact parent, candidate, evidence, warrant, A scope, reference contract, and
epochs.

Both serious arms may use their declared correction path. The resulting durable
state must satisfy held-out corrected A, unchanged B, and
`SEQ(A,B)=T_B(T_A1(x))`, with A+C still unresolved.

For `OPEN`, the correction must causally traverse `u_A0`'s reopening binding and
produce a `REVISE` descendant whose exact effective A consequence is `T_A1`.
An append-only rescope may accompany that revision, but a rescope label without
the content successor cannot pass. In-place mutation is not required. An
unrelated exception or hidden full replay is not an `R_chi` witness.

### Phase 6: capability-validity twin

Move the world to `e2` and construct identical observation, evidence, warrant,
proposal, candidate, parent, scope, contract, and resource state for the unique
`T_A2` revision. Fork immediately before the kernel's capability guard:

- the positive twin receives the authentic capability envelope and must commit;
- the attack twin receives the same declared capability body and byte length but
  an invalid authority-brand/authentication field and must not commit.

Only the capability envelope's authenticity differs. The attack branch is the
canonical mainline. Its semantic state digest, active commitments, and effective
policy must remain unchanged; an external audit journal may append a rejection
record without that append counting as semantic mutation.

Malformed, stale, replayed, wrong-parent, wrong-scope, and wrong-epoch
capabilities are secondary mandatory controls. They cannot replace the primary
authentication twin.

## 8. Prospective oracles

### 8.1 `M`: functional persistence

After Phase 3 restart and recovery, held-out A answers are correct without new
environment observations, evaluator calls, learning, or semantic commits.
Direct commitment access and archive replay can both pass. Their paths and
resource costs are recorded rather than smuggled into the functional verdict.

### 8.2 `C_corr`: implementation-neutral correction

After Phase 5, held-out A reflects `T_A1`, B remains exactly `T_B`, A+B reflects
the declared composition, A+C remains unresolved, and the accepted correction is
durable with attributable epistemic and authority lineage.

### 8.3 `R_chi`: Open-only causal mediation

The Phase 5 Open successor is a verifiable descendant of `u_A0`; its receipt
binds the decisive observation, evidence, warrant, capability, exact delta, and
durable result; and its effective A applicability changes.

From the identical Phase 4 root, `do(disconnect chi_A)` must prevent this exact
incremental transition and yield the declared pending/defer/stop state. If the
same transition succeeds through another path, `chi_A` receives no causal credit.

### 8.4 `S`: scope and composition

Phase 4 A+B is correct without joint examples or state update; A+C defers. After
Phase 5, only A and its declared A+B dependent consequence change; B and
unrelated scope are invariant.

### 8.5 `A`: authority integrity

The Phase 6 authentic twin commits and the forged twin does not. Because all
upstream objects are identical, the contrast isolates valid-at-commit authority.
Every secondary control listed in Phase 6 must also produce zero semantic delta.

## 9. Fault interventions and predicted first divergence

`FULL` means `OPEN` with the null `FaultProfile`. The same hashed kernel and
proposer are used throughout. Ablations are separately
hashed injected components selected by an external frozen `FaultProfile`; no
component may read a phase label or held-out answer.

Run at minimum:

```text
FULL
ARCHIVE_REPLAY
POINTER_ONLY
-M_A
-R
-S
-A
```

Predicted first divergences and failure cones are:

- `-M_A`: remove durable A access after Phase 2; first divergence is Phase 3.
  Later A-dependent failures are descendants, not new evidence.
- `-R`: disconnect only `chi_A`; Phases 1-4 pass and Phase 5 cannot execute the
  incremental Open correction. Generic replay would reclassify the arm as
  `ARCHIVE_REPLAY`.
- `-S`: disable only the generic composition resolver; local A and B pass, while
  Phase 4 A+B and the derived post-correction A+B fail or defer. A+C still must
  not be invented.
- `-A`: bypass only commit-time capability authenticity on an isolated sandbox
  branch; Phases 1-5 pass and the Phase 6 forged twin mutates semantic state.

If an ablation causes a first divergence outside its declaration, or unrelated
effects outside the causal failure cone, the mechanism is underidentified. A
functional `FULL` with a failed `-R` contrast is classified as attribution
failure, not as functional failure.

## 10. Validity gates

The external attack adjudicator may assign a non-invalid result only if all are
true:

1. K0, seed commitments/reveals, and manifest hashes match.
2. The kernel, proposer, evaluator, authority verifier, and generic composition
   implementation are byte-identical across serious arms.
3. Only the named state strategy/index and frozen fault component differ.
4. The adapter satisfies the exact boundary in Section 4.3 and contains no
   transformation, composition-answer, phase, or authority logic.
5. Candidate uniqueness is externally verified for every observation set.
6. Raw event delivery and transient cache are purged while durable archive
   reconstruction remains available and metered.
7. The Archive arm uses only the pre-frozen ordered-record query and fresh-state
   reducer boundary from Section 2.2.
8. World truth, observation, warrant, authority, meter, persistence, outcome, and
   attack-adjudication roles remain separately attributable.
9. The decisive corrections and capability twin are externally generated.
10. Candidate, semantic-commit, durable, audit-journal, and active semantic state
   are distinguishable.
11. Both serious arms passed the maximum envelope on all development seeds before
    the evaluation implementation freeze.
12. `ARCHIVE_REPLAY` passes Phase 5 and the neutral outcome vector at the maximum
    envelope on all 64 evaluation seeds.
13. The normative meter interpreter reproduces every Phase-5 candidate and no
    result-affecting computation bypasses its trace.
14. Instrumentation can record and adjudicate a minimal trace for every Open
    witness and prospectively localized ablation, whether it passes or fails.
15. The predeclared duplicate executions within the single evaluation campaign
    are byte-deterministic from identical frozen inputs; any unexplained
    nondeterminism invalidates the run.

A failed or undecidable gate yields `INVALID / UNDERCONSTITUTED`, not a favorable
or unfavorable mechanism result.

## 11. Terminal statuses

Exactly one primary status is assigned to the 64-seed execution family.

### `DIFFERENTIAL MECHANISM WITNESS`

All validity gates pass; Open satisfies `(M,R_chi,S,A)`; every targeted ablation
has its declared first divergence; and the `CorrSuccess` inclusion rule in
Section 6 establishes a strict Open advantage.

### `VALID NO OPEN DIFFERENTIAL`

All validity gates pass; Open satisfies `(M,R_chi,S,A)` and its targeted
ablations; but the envelope sets are equal, Archive dominates, or the sets are
mixed/non-nested. Record subtype `PARITY`, `ARCHIVE_DOMINANT`, or `MIXED`.

### `VALID OPENCORE WITNESS FAILURE`

All apparatus and serious-control validity gates pass, but Open fails. Record
exactly one first-cause subtype:

- `FUNCTIONAL`: one of `M`, `C_corr`, `S`, or `A` fails;
- `ATTRIBUTION`: functional outcomes pass but `R_chi` or a targeted ablation
  lacks its declared causal divergence.

### `INVALID / UNDERCONSTITUTED`

The apparatus, seed isolation, world family, arm matching, serious rival,
resource comparison, or adjudication is invalid or insufficient.

No status is constitution-level survival, primitive necessity, or universality.

## 12. Claim ceiling

If and only if `DIFFERENTIAL MECHANISM WITNESS` is assigned, the strongest
licensed claim is:

> Across all 64 frozen evaluation instances sampled from this finite affine
> family and declared Phase-5 resource-envelope sweep, one
> fixed OpenCore K0 realization exhibited commitment-addressed causal reopening,
> persistent scoped composition, and commit-boundary authority integrity, and
> the named valid archive-replay rival's successful-envelope set was a subset of
> Open's on every evaluation seed and a strict subset on at least one.

`VALID NO OPEN DIFFERENTIAL` licenses only the bounded observation that the Open
mechanism was causally witnessed while no preregistered Open advantage appeared.

The assay cannot establish:

- a universal adaptive substrate or universal learner;
- intelligence emergence or general systematicity;
- primitive necessity;
- actual general `Q_reach`, long-horizon openness, or FCD/OCC truth;
- CEA composition or authority movement;
- cryptographic or hostile-process security;
- transfer to ARC3, Procgen, Retro, or another independently authored domain.

The dimensions remain narrow: `M` is one restart/recovery protocol, `R_chi` one
configured route, `S` one finite declared algebra, and `A` one declared
commit-boundary forgery family. Later claims require new prospective artifacts.
