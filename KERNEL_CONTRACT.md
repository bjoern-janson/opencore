# OpenCore K0 Kernel Contract

> **STATUS: CANDIDATE / PRE-CODE / UNIMPLEMENTED / UNVERIFIED / NONCANONICAL**
>
> **PURPOSE: PROSPECTIVE REFERENCE SEMANTICS**
>
> **RESULTS: NONE**
>
> **AUTHORITY: NONE OVER CEA, FCD/OCC, CCA/CARS, ISSUE #44, OR ARC3**

This document freezes a candidate transaction contract for the first OpenCore
reference implementation. It defines observable semantic obligations. It does
not establish that these operations are sufficient for cognition, correction,
or cross-domain transfer.

The separations are load-bearing:

```text
contract != implementation != evaluator != assay != execution != witness != result
```

“Universal” is the transfer hypothesis under study, not K0's empirical status.

## 1. Protected reference contract

For each execution, the external harness freezes:

```text
ReferenceContract X = (
  P, h, B, Omega, Boundary_SE,
  protocol_epoch,
  world_oracle_id, world_epoch,
  observation_recorder_id, observation_epoch,
  evaluator_id, evaluator_epoch,
  authority_minter_id, authority_verifier_id, authority_epoch,
  clock_meter_id, meter_epoch,
  state_store_id, persistence_verifier_id, persistence_epoch,
  codec_id, codec_epoch,
  outcome_oracle_id, outcome_epoch,
  adjudicator_id, adjudicator_epoch
)

reference_contract_digest =
  H(DomainSepReferenceContract || Canonical(X))
```

where:

- `P` is the evaluation and revision protocol;
- `h` is the frozen causal/transition horizon;
- `B` is the evaluator-owned resource budget and accounting contract;
- `Omega` is the evaluator-defined challenge-opportunity universe;
- `Boundary_SE` fixes the system/environment boundary;
- every remaining identity and epoch binds a load-bearing external role.

The incumbent may propose a successor contract. It cannot constitute or install
that proposal, judge itself by it, narrow the current contract, or cause the
verifier to anchor its digest as the accepted contract for the current
transition. The digest is a public hash that any caller may compute; computing it
carries no authority.

Every load-bearing artifact from `Observation` through `PersistenceReceipt`
binds the same `reference_contract_digest`. A mismatch creates a typed protocol
or binding failure; it cannot be repaired by downstream interpretation.

## 2. Acyclic state and event identities

### 2.1 Semantic state

```text
K_t = SemanticState(U_t, R_t, T_t)
b_t = InternalResourceState_t
```

where:

- `U_t` is the effective semantic content and scope of commitments;
- `R_t` contains route descriptors and executable binding references, never
  incumbent-asserted reachability facts;
- `T_t` is the effective transition/routing substrate;
- `b_t` is a separately rooted operational resource ledger, not part of the
  semantic-state digest.

Warrant, authority, commit, receipt, and lineage records live in the external
event/provenance layer. An effective open-commitment view joins semantic content
from `K_t` with those independently verified records. Version and implementation
metadata are nonsemantic unless a successor contract explicitly promotes them.

### 2.2 Digests and heads

```text
StateDigest(K) = H(DomainSepState || Canonical(K))

CommitId = H(DomainSepCommit || Canonical(SemanticCommitBody))

ReceiptId = H(DomainSepReceipt || Canonical(PersistenceReceiptBody))

ReceiptLogHead_(n+1) =
  H(DomainSepReceiptChain || ReceiptLogHead_n || ReceiptId)

CanonicalHead_t = (StateDigest_t, ReceiptLogHead_t)
```

The candidate successor `StateDigest` is computable before persistence. A
receipt binds that precomputed successor digest and the previous receipt-log
head. The receipt itself remains outside the state digest it certifies, so no
self-hash or receipt/state fixed point occurs. After receipt verification, the
kernel computes the new `ReceiptLogHead` and advances the two-part
`CanonicalHead`.

Semantic state identity and event identity are distinct. Two independently
authorized events may produce the same `StateDigest` but different `CommitId`,
`ReceiptId`, and `CanonicalHead` values.

### 2.3 Namespace non-collapse

```text
b_t != B
R_t != Q_reach
stored(RouteDescriptor) != stored(ReopeningBinding)
stored(binding) != Reach(binding | K_t, b_t, policy_t, X)
StateDigest != CommitId != ReceiptId != CanonicalHead
```

The kernel must not serialize `reachable`, `live`, `effective`, or
`FCD/OCC-compliant` as incumbent-minted facts.

## 3. Trust and ownership matrix

### 3.1 Kernel

The kernel owns:

- canonical semantic-state reads;
- immutable proposal intake and deterministic candidate construction;
- typed guard sequencing;
- valid-at-commit capability verification and consumption semantics;
- the one-parent transaction state machine;
- canonical-head advancement after external durability verification;
- incorporation of externally verified receipts into the receipt chain.

The kernel cannot evaluate its own warrant, mint transition authority, certify
route liveness, or issue a final durability receipt.

### 3.2 Untrusted incumbent machinery

Representation, hypothesis generation, proposal generation, planning, action
selection, and incumbent-generated probes are untrusted inputs. They may create
immutable proposals and request external tests. They cannot write canonical
state or the reference contract; mint evaluation status, warrant, capability,
commit, or receipt; or declare reachability.

Domain adapters perform only declared translation and serialization. An adapter
that embeds evaluator, authority, hidden world truth, or solution logic moves
the demonstrated capability out of the kernel and invalidates a transfer claim.

### 3.3 External roles

The harness separately constitutes the identities frozen in `X`:

- world oracle;
- observation/provenance recorder;
- warrant evaluator;
- authority minter and separately callable verifier;
- clock and resource meter;
- state store and persistence verifier;
- codec;
- outcome oracle;
- attack adjudicator.

The persistence verifier is the sole `PersistenceReceipt` issuer. It may issue a
receipt only after exact write and readback verification in the named store and
epoch. The kernel independently verifies and records that receipt before
advancing the head. The verifier and store are explicit members of the K0
trusted computing base, remain logically distinct from the incumbent, and may
not derive success solely from incumbent-written data.

No single role may silently rewrite `X`. The decisive external challenge cannot
be self-generated or self-certified by the incumbent.

The first Python reference may place these roles in one process for inspection.
That provides logical separation only. It makes no security, affine-type, or
unforgeability claim against hostile same-process code.

## 4. Non-collapsing semantic types

The implementation must define distinct types for at least:

```text
ReferenceContract
ReferenceContractDigest
RawEvent
Observation
EvidenceBundle
EvaluationResult =
  WARRANTED | NOT_WARRANTED | UNDERDETERMINED | PROTOCOL_FAILURE
Warrant
ProposedCommitmentDelta
ProposedSubstrateDelta
RouteDescriptor
ReopeningBinding
TransitionProposal
CandidateState
TransitionCapability
OpenCommitResult =
  SEMANTIC_COMMITTED | REJECTED | DEFERRED | PROTOCOL_FAILURE
SemanticCommit
CommitJournalRecord
PersistencePending
PersistenceFailed
PersistenceReceipt
AppliedCommitmentDelta
AppliedSubstrateDelta
OpenCommitment
CommitmentKey
LineageRecord
InternalResourceState
ResourceLedgerRoot
StateDigest
CommitId
ReceiptId
ReceiptLogHead
CanonicalHead
```

Their meanings must not collapse:

- `RawEvent` is an occurrence supplied across `Boundary_SE`.
- `Observation` binds observed content to source, time, provenance, recorder
  identity/epoch, and `reference_contract_digest`.
- `EvidenceBundle` is admitted material. Admission is not a warranted conclusion.
- `EvaluationResult` is the evaluator's decision under `P` for the exact
  evidence/candidate binding. Underdetermination is not acceptance or rejection.
- `Warrant` binds a `WARRANTED` result to the exact observation, evidence,
  proposal, candidate, parent head, scope, evaluator, protocol, and reference
  contract. It carries no mutation authority.
- `ProposedCommitmentDelta` and `ProposedSubstrateDelta` are untrusted proposed
  data. They contain no intrinsic authority bit.
- `RouteDescriptor` describes an externally attemptable challenge route.
- `ReopeningBinding` is a prospectively installed executable interface resolved
  through `T_t` to one commitment, scope, and typed reopening consequence.
  Presence still does not establish current reachability or liveness.
- `TransitionProposal` freezes the exact parent, candidate intent, scopes,
  proposed deltas, route/binding changes, contract, and resource demand.
- `CandidateState` is the deterministic, noncanonical semantic successor and its
  precomputed `StateDigest`.
- `TransitionCapability` is external, single-use semantic authority for one
  exact transition. It cannot supply epistemic warrant.
- `OpenCommitResult` is total and preserves rejection, deferral, and protocol
  failure as distinct results.
- `SemanticCommit` is an immutable accepted transition event stored in the
  transaction journal. It is not the current semantic state or final durability.
- `CommitJournalRecord` durably records the one pending semantic commit and its
  parent for recovery. It is not a final persistence receipt.
- `PersistencePending` and `PersistenceFailed` are typed storage outcomes. They
  are not success receipts and do not erase the semantic commit.
- `PersistenceReceipt` is external evidence that the exact commit and candidate
  state bytes passed write/readback verification in the named context.
- `AppliedCommitmentDelta` and `AppliedSubstrateDelta` are the exact proposed
  deltas after semantic acceptance and verified durability; no receipt may alter
  their bytes.
- `OpenCommitment` is the effective joined view of semantic content/scope,
  warrant, lineage, route descriptor, and reopening binding.
- `CommitmentKey` is a semantic address derived from commitment content and
  scope, distinct from event `CommitId`. A revision names the incumbent key and
  its proposed successor key, allowing bindings to be constructed without a
  commit-ID hash cycle.
- `LineageRecord` is a verified projection of linked semantic commits and
  receipts. It attests linked attribution under the named contract, not factual
  truth or warrant quality; a kernel-written history byte string alone is not
  lineage proof.
- `InternalResourceState` is a non-authoritative fold of externally metered
  resource events, distinct from protected `B`.
- `ResourceLedgerRoot` is the acyclic head
  `H(DomainSepResourceChain || previous_root || MeterEventDigest)`. It is external
  to `StateDigest`; `b_t` is recovered by folding its verified contiguous event
  chain. Authorization artifacts do not treat this root as authority. Receipts
  bind the starting and ending roots plus the exact metered-event record.
- identity/hash types are content references, never authority capabilities.

## 5. Authoritative transaction lifecycle

The only path from an event to canonical adaptive-state change is:

```text
RawEvent
  -> Observation
  -> EvidenceBundle

(K_t, Observation, EvidenceBundle)
  -> immutable TransitionProposal
  -> CandidateState

(EvidenceBundle, TransitionProposal, CandidateState)
  -> EvaluationResult::WARRANTED
  -> Warrant

(Warrant, CandidateState)
  -> externally minted TransitionCapability

OpenCommit(
  CanonicalHead_t,
  TransitionProposal,
  CandidateState,
  Warrant,
  TransitionCapability
)
  -> OpenCommitResult

OpenCommitResult::SEMANTIC_COMMITTED(SemanticCommit)
  -> verified PersistenceReceipt
  -> CanonicalHead_(t+1)
```

Therefore:

```text
RawEvent alone -/-> ProposedSubstrateDelta
RawEvent alone -/-> canonical semantic state
Observation alone -/-> Warrant
Warrant alone -/-> TransitionCapability
TransitionCapability alone -/-> Warrant
CandidateState -/-> CanonicalHead
SemanticCommit -/-> PersistenceReceipt
PersistenceReceipt -/-> TransitionCapability
```

`NOT_WARRANTED`, `UNDERDETERMINED`, and `PROTOCOL_FAILURE` cannot mint a
capability or mutate adaptive state. They may create separately typed audit
records, pending questions, or external probe requests.

The proposed commitment and substrate deltas exist in immutable candidate form
before authorization. A receipt neither creates nor authorizes them.

No lower stage may manufacture an upstream object. Adapter or proposer code
cannot mint `EvaluationResult`, `Warrant`, `TransitionCapability`,
`SemanticCommit`, or `PersistenceReceipt`.

## 6. Proposal and candidate binding

Every proposal binds:

```text
reference_contract_digest
parent CanonicalHead and parent StateDigest
protocol epoch and task/branch
observation and evidence digests
exact writable scope and collateral invariants
ProposedCommitmentDelta
RouteDescriptor delta
ReopeningBinding delta
ProposedSubstrateDelta
declared resource demand
```

Every `ReopeningBinding` in that proposal binds the exact incumbent or proposed
`CommitmentKey`, scope, resolver identity/epoch, allowed typed consequences, and
`reference_contract_digest`.

Candidate construction is a pure function of the exact parent semantic state
and proposal. It emits canonical candidate bytes and a precomputed successor
`StateDigest`. Candidate inspection or rejection cannot change either head.

The external evaluator prospectively checks scope and collateral invariants. A
proposal cannot authorize its own transfer scope by declaring it.

The `EvaluationResult` and any resulting `Warrant` bind the proposal digest,
candidate digest, successor `StateDigest`, parent head, exact scope, evidence,
all relevant role identities/epochs, and `reference_contract_digest`.

## 7. Capability validity

The authority minter may construct a capability only for a `WARRANTED` exact
candidate under the current contract. A capability is valid at the commit
linearization point only if it authenticates and matches:

```text
reference_contract_digest
parent CanonicalHead and StateDigest
candidate, proposal, and exact delta digests
successor StateDigest
observation, evidence, evaluation, and warrant digests
task/branch and exact scope
protocol, evaluator, authority, meter, and codec epochs
expiry, revocation, and declared change envelope
single-use consumption identity
```

The verifier fails closed on missing, ambiguous, stale, forged, replayed,
wrong-parent, wrong-scope, wrong-contract, or wrong-epoch values.

The semantic capability is affine: callers may move it into one commit attempt
but may not copy, split, widen, retarget, or reuse it. K0 Python can model those
state transitions; it cannot enforce them against hostile same-process code.

## 8. Frozen guard precedence and resource accounting

Commit guards execute in this order:

1. canonical decoding and type/version validation;
2. exact `reference_contract_digest`, role, and epoch validation;
3. exact current `CanonicalHead` and idle-parent validation;
4. observation/evidence/evaluation/warrant chain validation;
5. proposal/candidate re-derivation, scope, delta, and collateral validation;
6. external `h,B` meter validation and declared-demand admissibility;
7. capability authenticity, binding, expiry, and revocation validation;
8. single-use availability validation;
9. atomic capability consumption plus durable `Persisting` journal record and
   `SemanticCommit` creation.

Failure at any earlier guard emits the corresponding typed result, performs no
later authority-bearing step, and produces zero semantic delta. Capability
consumption and semantic-commit creation are one logical linearization event
only after all prior guards succeed.

The external meter debits actual cost at each declared accounting event,
including unsuccessful probes, evaluation, failed commit attempts, journal
writes, persistence, readback, and retry. Already spent budget is never refunded
by a semantic failure. The internal `b_t` ledger mirrors attributable events but
cannot reset, replace, or reinterpret `B`, `h`, `P`, `Omega`, or `Boundary_SE`.
Resource exhaustion produces a typed failure and zero semantic delta without
making the lost opportunity disappear from `Omega`.

Before Guard 9, the meter reserves the proposal's declared worst-case remaining
cost for journal persistence, semantic-state write, readback, and receipt
verification within `h,B`. Actual cost replaces the reservation as operations
complete; already incurred cost remains spent. Underestimated demand after
semantic acceptance leaves the exact commit pending and makes the execution
underconstituted—it does not expand the contract or authorize a rival commit.
On restart, `b_t` is reconstructed from the external meter's attributable
records and cannot move backward independently of them.

## 9. Semantic commit, durability, and recovery

### 9.1 One-parent state machine

K0 has no implicit branch/fork semantics:

```text
Idle(CanonicalHead_t)
  -> Persisting(SemanticCommit, CanonicalHead_t)
  -> Durable(PersistenceReceipt, CanonicalHead_(t+1))

Persisting
  -> PersistencePending
  -> PersistenceFailed
  -> retry the same immutable SemanticCommit
```

`PersistencePending` and `PersistenceFailed` leave the transaction in the
`Persisting` family. At most one canonicalizing semantic commit may exist for a
parent. New proposals may be prepared, but any new `OpenCommit` against that
parent returns `DEFERRED(PARENT_BUSY)` until the exact pending commit becomes
durable. K0 defines no authority-erasing abort shortcut.

Guard 9 succeeds only when capability consumption and a durable, readback-
verified `Persisting` journal record can be treated as one reference-semantic
event. If that journal operation fails before the event, no `SemanticCommit`
exists and the capability remains unconsumed, while metered costs remain spent.

The immutable `SemanticCommitBody` binds the reference-contract digest, parent
head, successor state digest, proposal and candidate digests, observation,
evidence, evaluation, and warrant digests, exact scope and deltas, consumed
capability identity, task/branch, relevant epochs, and reserved resource record.
The journal record binds that body and its `CommitId`.

### 9.2 Persistence outcomes

After semantic acceptance, the persistence layer may write only the immutable
commit and candidate state bytes. Retry resubmits those exact bytes and performs
no re-evaluation, new authority mint, scope widening, delta change, capability
reuse, or duplicate lineage append.

The persistence verifier is the sole receipt issuer. It emits a receipt only
after exact write and independent readback verification. The receipt body binds:

```text
reference_contract_digest
receipt issuer identity and persistence epoch
state store, codec, and their epochs
previous ReceiptLogHead and durable sequence/position
parent CanonicalHead and parent StateDigest
successor StateDigest, commit readback digest, and candidate-state readback digest
SemanticCommit and CommitId
observation, evidence, evaluation, and warrant digests
proposal, candidate, and exact proposed/applied delta digests
consumed capability identity and exact scope
task/branch and all relevant role epochs
metered resource record
starting and ending ResourceLedgerRoot
durable location and acknowledgement
```

The kernel verifies the receipt, computes its `ReceiptId` and the next
`ReceiptLogHead`, and only then advances `CanonicalHead` and exposes the applied
semantic state.

### 9.3 Recovery

Recovery first restores any durable `Persisting` journal record, blocking a
conflicting commit and retrying only its exact bytes. It then selects the longest
valid contiguous receipt chain whose previous-head, parent-state, successor-
state, store, codec, and sequence links verify. Orphaned, duplicate, malformed,
or noncontiguous records remain audit artifacts and cannot become current state
by storage position alone.

A receipt attests only that an exact semantically authorized commit became
durable in the named store and contract. It does not prove factual truth,
evaluation quality, task success, scope adequacy, causal reopening, current
route liveness, FCD/OCC coverage, identity, or universality.

## 10. Reopening semantics

A conforming K0 Open commitment has the joined conceptual shape:

```text
u = (
  CommitmentKey,
  semantic content,
  exact scope,
  warrant reference,
  lineage reference,
  RouteDescriptor,
  ReopeningBinding
)
```

`ReopeningBinding` is distinct from descriptive provenance. It resolves through
the current transition substrate to one commitment and typed consequence:

```text
RETAIN | RESCOPE | REVISE | RETIRE | UNRESOLVED
```

A conforming binding's prospectively allowed consequence set must contain at
least one of `RESCOPE`, `REVISE`, `RETIRE`, or `UNRESOLVED`. `RETAIN` may be an
additional outcome but cannot be the only executable consequence.

An append-only `RESCOPE`, `REVISE`, `RETIRE`, or `UNRESOLVED` event is valid if
external counterevidence causally traverses the binding, changes the
commitment's warranted future applicability, and preserves verified event
lineage. In-place mutation is not required. Appending an unrelated exception or
overwriting content without traversing that path is not a reopening witness.

The `ARCHIVE_REPLAY` arm in Experiment 001 is a serious rival realization, not a
K0 Open-commitment conformance witness. It may satisfy the same external
correction obligation through full replay without receiving `R_chi` credit.

The kernel exposes descriptors, bindings, candidate pairs, and traces for an
external bounded exercise:

```text
Reach(
  binding |
  K_t, b_t, policy_t,
  P, h, B, Omega, Boundary_SE,
  evaluator_id, evaluator_epoch
)
```

Descriptor presence, binding presence, API permission, historical success, and
certificate validity do not establish current causal reachability or
effectiveness. K0 defines no `LiveCert` and no permanent liveness flag:

```text
ActuallyLive != ObservedLive != CertificateValid
```

Any future liveness certificate is a distinct post-K0 candidate mechanism. It
must be externally exercised, scoped, time-bounded, and prospectively tested.

## 11. FCD/OCC boundary

K0 exposes state pairs, descriptors, bindings, receipts, meters, and traces to
an external FCD/OCC assay. It does not implement a trusted Boolean
`is_fcd_occ_compliant` or a complete estimator for corrective coverage.

An external finite assay may return:

```text
PASS | FAIL | UNDERCONSTITUTED
```

only under its own frozen reference contract and witness set.
`UNDERCONSTITUTED` cannot become `PASS` by incumbent interpretation, and no
finite result proves a universal invariant.

## 12. Determinism and observability

The reference kernel must provide:

- a versioned canonical encoding for every semantic type;
- deterministic state, commit, receipt, resource-ledger, and head identities;
- explicit rejection, deferral, pending, and failure reasons;
- immutable proposal, candidate, commit, and receipt digests;
- a replayable typed transition trace;
- independent receipt and readback verification;
- explicit clock, randomness, role, and resource inputs;
- no ambient-clock, ambient-randomness, or hidden-global input inside reference
  transition functions.

The harness must reconstruct every candidate, state digest, commit, receipt, and
head from frozen inputs. Every execution manifest defines resource units and
accounting events. Changing a protected field creates a new attributable
experiment instance, never a favorable reinterpretation of the old one.

## 13. K0 exclusions and claim ceiling

K0 does not freeze or establish:

- a neural, symbolic, or programmatic representation strategy;
- a general hypothesis generator, planner, learner, or world model;
- an operational estimator for universal corrective coverage;
- a cross-domain adapter beyond non-solution-bearing translation;
- cryptographic or process-level authority security;
- a scalar intelligence, corrigibility, or OpenCore score;
- route liveness from descriptor/binding presence;
- conservation of route identity or route count;
- a claim that every warranted cognitive proposal is authorized;
- any experiment result, mechanism necessity, CEA composition, FCD/OCC support,
  or universality.

Lines of code are inspectability metadata, not scientific minimality. The full
trusted computing base, dependencies, adapters, proposer, evaluator, and harness
must be reported rather than hidden outside the kernel count.

Any extension requires a prospectively reviewed successor under
[CHARTER.md](CHARTER.md). K0 remains the attacked ancestor.
