# Architecture: Organism, Substrate, and the "Tiny Computational World"

## Status

This document is an explanatory map of the current crank lineage.

- **Nano V0** has a constructed experimental result.
- **Mini** has a sequence of constructed adaptive experiments.
- **OpenCore Base** is still a mental model for a larger system, not an implemented or experimentally established architecture.

## 1. The organism/world split

A conventional adaptive-system picture often compresses everything into:

```text
experience -> learning -> new model -> use
```

OpenCore's crank experiments repeatedly found that the dangerous step was often not the model itself but the transition that made some internal result persistent or authoritative.

The current split is therefore:

```text
            adaptive proposer
                  |
            warrant / license
                  |
             +----------+
             |   Nano   |
             +----------+
                  |
          persistent standing
```

Mini is the adaptive process above the boundary.
Nano is the small persistence substrate at the boundary.

## 2. OpenCore Mini

Mini is deliberately domain-specific and cognitively active.

It can, in the current toy family:

- observe examples;
- infer finite affine hypotheses;
- persist commitments;
- compose known commitments;
- detect contradictions;
- maintain incumbent lineage;
- request additional evidence when a replacement is underdetermined;
- revise one scope while preserving another;
- participate in externally supplied closure/challenge protocols;
- and, in M6, use externally typed policy-level evidence to alter a future closure mechanism.

Mini asks questions such as:

```text
What rule fits?
What should replace my incumbent?
Do I need another probe?
Which scope changed?
```

Mini is not a general learner and does not autonomously discover all of the distinctions used by later harnesses.

## 3. OpenCore Nano

Nano is intentionally much smaller.

Its V0 model is:

```text
OpenCore Nano = transition typechecker + append-only in-process journal
```

Nano does not decide whether a payload is true, scientific, predictive, observational, causal, or useful.

The payload is opaque.

Nano can inspect only the transition-contract surface required to decide whether a persistent state change is licensed.

Conceptually:

```text
(S_t, T, L) -> ALLOW | DENY | DEFER
```

where:

- `S_t` is current transition-visible standing;
- `T` is a proposed state transition;
- `L` is an externally constituted license.

V0 checks:

```text
S_t satisfies Pre(L)
Effect(T) is contained by Effect(L)
Preserve(L) is preserved by T
warrant-parent receipts remain effective
```

`DEFER` is not anthropomorphic uncertainty. It means a contract-required proposition is not currently established by kernel-visible standing.

## 4. Opaque payload, inspectable control surface

The central Nano separation is:

```text
semantic payload                opaque
transition-contract surface     inspectable
```

A protocol may expose typed facts such as:

- object identity;
- scope;
- standing key/value;
- operation type;
- preconditions;
- write/delete/revocation effects;
- required preservation;
- warrant-parent dependency.

Nano compares these facts mechanically.

It does not infer their domain semantics.

## 5. Why this separation matters

The first Mini × Nano composition assay demonstrated a causal separation:

```text
Mini cognition unchanged
Nano implementation unchanged
same proposed transition
only persistence boundary changes
```

On the constructed suite, naive persistence accepted 50,000/50,000 known illegal promotions while Nano accepted 0/50,000, and Nano retained 60,000/60,000 matched legitimate transitions.

This supports an "authority firewall" interpretation only in a narrow operational sense:

> Nano can block persistent effects that exceed supplied transition contracts without fixing the proposer that generated them.

It is **not** a firewall against false thoughts or bad plans.

## 6. OpenCore Base

"OpenCore Base" is currently a useful systems picture, not an earned experimental object.

The idea is a broader environment in which multiple adaptive processes share a small persistent transition substrate:

```text
perception -----\
planning --------\
science ----------> proposals -> shared Nano-like boundary -> durable state
ARC/problem solving/
other tools ------/
```

A compact mental model is:

```text
Nano = world rules at the persistence boundary
Mini = one organism operating inside those rules
Base = the world + adaptive processes + interaction rules
```

The point of the analogy is separation of powers, not literal physics.

## 7. Composition is first-class

A license can be authentic and still not authorize execution now.

Suppose:

```text
S0 satisfies Pre(L2)
```

Then another valid transition changes the state:

```text
S0 --T1--> S1
```

Nano must re-evaluate:

```text
S1 satisfies Pre(L2) ?
```

This gives the V0 operational distinction:

```text
license possession != current authorization
```

and the broader composition warning:

```text
Valid(T1) AND Valid(T2) !=> Valid(T2 o T1)
```

when the postcondition of one stage no longer satisfies the warrant precondition of the next.

## 8. What stays outside Nano

V0 deliberately leaves these problems above or outside the kernel:

- truth;
- evidence-role discovery;
- dependency discovery;
- applicability discovery;
- challenge design;
- transfer-boundary discovery;
- hypothesis proposal;
- planning;
- loss/decision semantics;
- correctness of external licenses.

That boundary is a feature of the experiment. A Nano success is useful only if Nano remains small enough that hidden cognition cannot do the work for it.
