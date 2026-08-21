# FOREIGN-003 — History-Dependent Outcome Equivalence

**Status:** `CLASSICAL_REPRODUCTION_ESTABLISHED`

## Frozen question

Can the OQ-002 causal topology reproduce in a purely classical stateful world when quantum mechanics is removed but the acquisition-history geometry is preserved?

The prospective discriminator was:

- same first observed event distribution under histories A and B;
- one later probe whose distribution differs by history;
- one null probe whose distribution does not differ;
- coarse apparatus identity aliases A and B;
- complete apparatus identity distinguishes A and B;
- unchanged Nano and the same downstream transition object are used in both carrier regimes.

A positive result required the coarse carrier to cause cross-history warrant reuse and a wrong durable targeted-probe consequence, while the complete carrier blocked that transfer and the null probe remained harmless.

## Classical foreign world

Initial state: `s0`.

Both interventions emit a fair classical bit:

```text
P_A(x=0) = P_B(x=0) = 1/2
P_A(x=1) = P_B(x=1) = 1/2
```

The interventions differ only in the hidden classical state they leave behind:

```text
I_A -> hidden = 0
I_B -> hidden = 1
```

Condition on the same first event `x=0`.

Targeted probe `X` reads the hidden bit exactly:

```text
A/X -> ZERO with probability 1
B/X -> ONE  with probability 1
```

Null probe `Y` ignores the history-sensitive bit and returns a fair coin:

```text
A/Y -> HALF
B/Y -> HALF
```

Thus the classical witness satisfies:

```text
same first outcome distribution
+ different targeted future consequence
+ identical null-control future consequence
```

No quantum state, instrument, amplitude, Born rule, qubit, or quantum simulator is used.

## Persistence geometry

Coarse carrier:

```text
C_coarse(A,0) = C_coarse(B,0) = event:x:0
```

Complete carrier:

```text
C_complete(A,0) = event:A:x:0
C_complete(B,0) = event:B:x:0
```

The Nano payload remains opaque. The manipulated variable is only apparatus-event identity resolution.

### Targeted X branch

History A legitimately establishes:

```text
A/X = ZERO
```

Under the coarse carrier, the A standing is attached to the aliased key `event:x:0`. When history B arrives, the same key satisfies the B downstream license precondition.

Observed result:

```text
coarse B/X use: ALLOW
persisted B/X: ZERO
external B/X truth: ONE
oracle_correct: false
```

The bad B/X receipt has the A-profile receipt as its sole warrant parent:

```text
A profile receipt:       e15c971ccb25bc0e5db52f65
bad B/X parent receipt:  e15c971ccb25bc0e5db52f65
```

Therefore the A-derived standing causally authorized the wrong B-history persistent transition.

Under the complete carrier:

```text
before B profile exists:         DEFER
old A-profile use after B truth:  DENY
correct B-profile use:            ALLOW
persisted value:                  ONE
```

The downstream transition object used before B-profile constitution is identical between the coarse and complete X conditions.

### Null-control Y branch

A/Y and B/Y are both `HALF`.

Under the same coarse aliasing:

```text
coarse B/Y use: ALLOW
persisted B/Y: HALF
oracle_correct: true
```

So aliasing alone is not sufficient for failure; the erased distinction must be relevant to a later consequence.

## Exact checks

Formal classical witness:

```text
4 / 4 PASS
```

Persistence pressure:

```text
18 / 18 PASS
```

Frozen Nano SHA-256 before and after:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Nano was not modified.

A seeded 100,000-trial-per-history sanity trace was also retained, but the result classification follows from the exact constructed probabilities and Nano receipts, not Monte Carlo sampling.

## Earned claim

The OQ-002 causal topology reproduced in a purely classical stateful world:

> Outcome-equivalent acquisition histories with different future consequence structure, when collapsed to one persistence identity, caused an A-derived standing to authorize a wrong durable B-history targeted-probe profile. Preserving opaque history identity blocked the transfer; the null probe remained harmless under the same aliasing.

This supports a cross-domain candidate pattern:

```text
premature apparatus quotient
-> identity aliasing
-> cross-history warrant reuse
-> wrong persistent consequence
```

## Claim ceiling

FOREIGN-003 does **not** establish that:

- the pattern is universal across all domains;
- quantum mechanics is irrelevant to future OpenCore Quantum work;
- Nano is defective;
- Nano requires new semantics;
- history identity is a universal OpenCore primitive;
- a schema repair is earned.

## Diagnosis

`cross-domain persistence wound caused by premature apparatus identity quotienting upstream of unchanged Nano`

The correct next move is not architecture. The quantum-specific branch and this classical control should remain frozen while another genuinely different domain tests whether the same causal topology survives again.
