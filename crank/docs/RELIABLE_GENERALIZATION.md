# Reliable Generalization: Warranted Invariance

## Status

This is an active research target. Reliable generalization is **not solved** by the current Mini/Nano stack.

The strongest current framing is:

```text
generalization performance != generalization authority
```

and:

```text
reliable generalization = discovery and governance of warranted invariance
```

A complementary view is:

```text
reliable generalization = warranted quotient construction
```

These are candidate formulations, not universal definitions.

## 1. What ordinary generalization leaves implicit

A conventional learner is usually evaluated by whether a learned rule predicts unseen cases:

```text
H: X -> Y
```

The OpenCore question is stricter:

> **What evidence licenses transporting H from one context into another?**

A prediction can succeed in a new context without establishing that the transformation connecting old and new contexts is target-irrelevant.

## 2. Candidate transfer structure

A useful conceptual object is:

```text
(H, ~_H)
```

where `~_H` is a candidate relation over contexts:

```text
a ~_H b
```

means that reusing `H` across `a` and `b` is currently supported.

But the relation itself needs governance:

```text
transfer relation
+ warrant
+ corrective access
+ reopening conditions
```

The representation of those terms is intentionally not frozen.

## 3. Three transfer statuses

A reliable system should not be forced into merge-or-split when the relation is not identified.

Conceptually:

```text
a ~_H b       transfer licensed
a !~_H b      transfer contradicted
a ?_H b       transfer unresolved
```

The unresolved state matters because:

```text
zero false transfer by splitting every context != reliable generalization
```

and:

```text
high transfer by merging everything != reliable generalization
```

The target lies between paralysis and over-generalization.

## 4. R1: active discrimination of transfer hypotheses

The first direct precursor was deliberately small.

Two opaque transfer hypotheses `T1` and `T2` were constructed such that the initial history was exactly observationally equivalent:

```text
T1(D_t) = T2(D_t)
```

There were eight opaque future contexts, with exactly two contexts where the candidates disagreed.

The controller had a one-probe budget.

Result over 10,000 constructed worlds:

```text
passive                    0.00% resolved
random                    25.12% resolved
transfer-discriminating  100.00% resolved
```

The random result matches the 2-of-8 geometry.

The transfer-aware controller selected a context where the live transfer hypotheses disagreed, observed one real consequence, and eliminated the wrong candidate in every tested world.

Narrow earned result:

> **Uncertainty over transfer structure can drive active evidence acquisition.**

## 5. R1 claim ceiling

R1 did **not** demonstrate:

- autonomous transfer-hypothesis invention;
- autonomous discovery of the disagreement-selection strategy;
- nuisance-dimension compression;
- arbitrary latent invariance discovery;
- transfer closure authority;
- reliable generalization generally.

The finite candidate set and selection logic were harness-supplied.

## 6. The next harder target

The real mountain is not choosing between two supplied transfer candidates.

It is constructing a useful transfer relation from experience.

A successful stronger system would need to:

```text
discover candidate invariances
-> seek contexts that discriminate them
-> license transport only over surviving structure
-> revoke/revise the boundary when reality breaks it
-> inherit the correction into future transfer decisions
```

Crucially, the boundary should generalize to new surface presentations rather than memorize context IDs.

## 7. Controls inherited from earlier attacks

A trustworthy transfer-boundary experiment has to survive the wounds already discovered elsewhere.

### Correctable Lineage

```text
many reports != many independent corrective paths
```

### Cerebro

```text
acquisition policy affects which evidence becomes available
```

### SSI

```text
prediction != observation
authority != applicability
```

### Nano

```text
license possession != current authorization
```

### Standing reconciliation

If a transfer rule is later invalidated, descendants that inherited authority from that rule may require reconsideration.

## 8. Why this is developmental

The target is not only to make one good transfer decision.

A stronger adaptive system should change how it tests future transfer boundaries after systematic failures.

That gives a developmental loop:

```text
candidate transfer
-> discriminating reality contact
-> licensed use
-> counterexample
-> boundary revision
-> changed future transfer policy
```

This is the point at which reliable generalization begins to overlap with recursive correctability.

## 9. Current position

The crank program has demonstrated useful **authority discipline around transfer** and one active-discrimination precursor.

It has not yet demonstrated autonomous discovery of the equivalence relation that determines where a learned rule is legitimately transportable.

That remains the central open problem.
