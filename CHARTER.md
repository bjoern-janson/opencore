# OpenCore Charter

> **CANDIDATE UNIVERSAL ADAPTIVE TRANSACTION KERNEL**
>
> **STATUS: CANDIDATE EXPERIMENTAL SUBSTRATE**
>
> **PHASE: PRE-CODE / FROZEN FOR PROSPECTIVE IMPLEMENTATION AND ATTACK**
>
> **IMPLEMENTATION: NONE**
>
> **RESULTS: NONE**
>
> **AUTHORITY: NONE OVER CEA, FCD/OCC, CCA/CARS, ISSUE #44, OR ARC3**

## 1. Mission

OpenCore tests whether a small, inspectable, typed, deterministic, and
adversarially testable transaction substrate can convert externally grounded
experience into authorized, scoped, persistent, reusable, and reopenable
adaptive structure.

The governing research question is:

> Can experience become persistent adaptive structure without becoming an
> unchallengeable fact?

The first implementation must optimize for inspectability and causal
identification, not for apparent generality or benchmark performance.

“Universal” names the transfer hypothesis under investigation. It is not the
project's current empirical status.

## 2. What OpenCore is

OpenCore is a candidate **adaptive transaction kernel**. Its proposed role is to
own a three-way typed lifecycle: a proposal may be rejected or deferred before
authority; it may be semantically accepted while persistence remains pending or
failed; or it may be durably persisted and become canonical state.

The word **open** means that persistent structure carries a prospectively
defined path by which independently grounded evidence may warrant its scoped
reopening. It does not mean that every object is mutable by every caller.

The word **core** means that accepted changes affect the substrate through
which future cognition proceeds. An archive, benchmark wrapper, or provenance
log alone is not a core.

## 3. What OpenCore is not

This repository does not currently establish:

- a universal learner;
- general intelligence or open-ended intelligence;
- a complete cognitive architecture;
- a security boundary against hostile in-process code;
- the truth, necessity, or sufficiency of FCD/OCC;
- a realization, revision, or promotion of CEA;
- a composition witness for CLPR, Cognitive Core, AIEC, or Issue #44;
- cross-domain transfer;
- that executable reopening is necessary rather than merely useful in a
  declared experimental family.

Function names such as `observe`, `evaluate`, `commit`, and `reopen` state
functional obligations. They do not, by being named, solve perception,
representation, hypothesis formation, causal inference, warrant, or planning.

## 4. Candidate constitutional obligations

An implementation may count as an OpenCore implementation only if it preserves
all of the following separations.

### 4.1 Typed epistemic separation

An event is not an observation. An observation is not evidence. Evidence is not
a warrant. A warrant is not transition authority. Authority is not persistence.
A persistence receipt is not proof that the underlying belief is true.

### 4.2 No event-to-substrate shortcut

An occurrence cannot directly rewrite the cognitive substrate:

```text
RawEvent -/-> SubstrateDelta
```

Every canonical substrate change must traverse the lifecycle frozen in
[KERNEL_CONTRACT.md](KERNEL_CONTRACT.md).

### 4.3 External reference protection

The incumbent system cannot unilaterally define or narrow the protocol,
horizon, reference budget, challenge universe, system/environment boundary,
evaluator identity, or authority issuer against which its own transition is
judged.

### 4.4 Authority-bounded persistence

Warrant does not mint authority. Authority does not manufacture warrant.
Authority-looking data is not authority. A canonical transition requires both
sufficient warrant for the exact proposed change and a live capability bound to
that same change at commit time.

### 4.5 Reopenable commitments

Persistent adaptive content must expose both a typed challenge-route descriptor
and a prospectively bound executable reopening interface. Neither object's
presence is a self-issued assertion that the route is reachable, live, or
effective. Those are external, contract-relative empirical properties.

### 4.6 Scoped substrate plasticity

An accepted experience may change both retained content and future cognitive
routing, but only through an explicit, warranted, authorized, and receipt-bound
delta. Global retrievability does not license global application.

### 4.7 Resource non-collapse

Mutable incumbent resource state and the evaluator-protected reference budget
are distinct objects. Exhausting or redefining internal resources cannot launder
the external contract.

### 4.8 Deterministic reference semantics

Given identical canonical inputs, protocol version, and external decisions, the
reference kernel must produce identical candidate bytes, state digests,
decisions, and head advancement for the same externally issued persistence
outcome or receipt. The separate persistence verifier must canonically issue the
same receipt body for identical store, write, readback, codec, meter, and contract
inputs. The kernel verifies and incorporates that receipt; it does not issue it.
Nondeterministic learning may exist outside the reference boundary, but its
concrete proposal becomes immutable before evaluation.

## 5. Trust boundary

The initial implementation may run in one Python process for inspection and
speed. That supplies **logical separation**, not adversarial isolation or
unforgeability.

The kernel may own canonical state and transaction sequencing. It may not own
the external world truth, protected reference contract, decisive warrant
evaluation, capability minting, persistence verification, or terminal
experimental adjudication.

Any later claim of affine authority or hostile-code resistance requires a
stronger process, language, or cryptographic boundary and a new prospective
test. Passing Python tests cannot earn that claim.

## 6. Primitive-growth rule

> **No new semantic primitive without a frozen counterexample, an
> unrepresentability argument, or a discriminating witness—and no primitive
> earns credit unless its targeted ablation causes the predicted localized
> failure.**

A failure alone does not authorize architecture growth. Before adding a
primitive, the experiment must prospectively identify the missing functional
obligation, exclude relevant implementation/resource/apparatus defects, and
show that a simpler rival cannot realize the same obligation.

Lines of code are reported as an inspectability measure, never as proof of
minimality. Dependency, adapter, evaluator, proposer, and harness complexity
must be reported with kernel complexity rather than hidden outside it.

## 7. Evidence ladder and claim ceilings

The project uses the following non-collapsing ladder:

```text
prospective specification
    -> valid execution
    -> localized mechanism witness
    -> rival exclusion
    -> independently authored domain transfer
    -> repeated cross-domain transfer
    -> universality candidate
```

A successful first experiment can establish only the claim ceiling written in
[EXPERIMENT_001.md](EXPERIMENT_001.md). It cannot establish universality.

Reuse of a generic interface across domains shows interface reuse. A serious
**substrate universality** claim additionally requires an unchanged kernel,
primitive vocabulary, trust contract, and non-solution-bearing adapter across
independently authored domains. A **universal learner** claim is stronger still:
the proposal/inference engine must also remain unchanged.

## 8. Lineage and freeze discipline

The repository was initialized at
[`2bc13bb25482173a1206453266172cba447e1158`](https://github.com/bjoern-janson/opencore/commit/2bc13bb25482173a1206453266172cba447e1158).

The motivating candidate synthesis is recorded in the CEA repository at
[`0c65b9a4ba56d84d509157a11bea45633f02e0ba`](https://github.com/bjoern-janson/cognitive-evolution-architecture/commit/0c65b9a4ba56d84d509157a11bea45633f02e0ba).
That relationship supplies research lineage, not authority movement.

The first commit containing this charter, `KERNEL_CONTRACT.md`, and
`EXPERIMENT_001.md` in their complete reviewed form is the **K0 prospective
specification anchor**.

After K0 is frozen:

- implementations and executions must name the exact K0 commit;
- no result may be written into the prospective specification;
- an invalid or underconstituted execution motivates a repaired apparatus, not
  a favorable result;
- a counterexample may motivate K1, but K1 must be a distinct descendant and
  must not rewrite K0's historical content;
- no single experiment may award constitution-level or universality survival.

## 9. Immediate program

The first authorized work is exactly:

1. freeze this charter;
2. freeze the typed kernel contract;
3. freeze Experiment 001;
4. implement only what those artifacts require;
5. freeze an execution manifest before observing results;
6. execute and record the result in a later artifact.

No implementation result exists at this freeze.
