# FOREIGN-004 — Safe quotient under future-consequence equivalence

## Status before execution

`FROZEN_PROSPECTIVE_ASSAY`

## Question

Can two genuinely different acquisition/control histories be safely collapsed to one persistence identity when they converge to the same operational state and are equivalent across an explicitly frozen future-consequence surface?

The assay attacks the stronger hypothesis:

> Different acquisition history always requires persistence-distinct identity.

It does **not** assume a `HistoryID`, provenance primitive, richer Nano relation, or any schema repair.

## Classical foreign world

Initial state:

```text
counter = 0
```

History A:

```text
0 --(+1)--> 1 --(+1)--> 2
```

History B:

```text
0 --(+3)--> 3 --(-1)--> 2
```

Therefore the histories and intermediate states differ, but the final operational state converges:

```text
H_A != H_B
s'_A = s'_B = counter:2
```

Each history emits a first observation bit `x ~ Bernoulli(1/2)` independently of history. The frozen specimen conditions on `x=0`.

## Frozen future-consequence surface Q

The tested future surface is exactly `Q = {X, Y, Z}`:

- `X`: parity of the converged counter. At `counter=2`, profile = `EVEN`.
- `Y`: threshold test `counter >= 2`. At `counter=2`, profile = `HIGH`.
- `Z`: fair stochastic probe whose distribution is independent of history. Profile = `HALF`.

Prospective requirement:

```text
for every M in Q:
    P_A(y | x=0, M) = P_B(y | x=0, M)
```

This is a scoped future-consequence equivalence claim, not a claim that the complete histories are identical or indistinguishable under every conceivable query.

## Carrier manipulation

Coarse:

```text
C_coarse(A,0) = C_coarse(B,0) = event:x:0
```

Complete:

```text
C_complete(A,0) = event:A:x:0
C_complete(B,0) = event:B:x:0
```

The only manipulated variable at the persistence boundary is event identity resolution.

## Persistence assay

Use the exact frozen Nano V0:

```text
SHA-256 = 8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

For each probe in `Q`:

1. Admit the legitimate A-profile standing.
2. Propose the same downstream B transition under coarse and complete carriers.
3. Under the coarse carrier, A's standing is visible at B's aliased event identity and should `ALLOW`; because A and B are future-consequence equivalent, that durable result must be externally correct.
4. Under the complete carrier, the same transition should initially `DEFER` because B-specific standing is unestablished.
5. Admit the independently constituted B-profile standing.
6. Reapply the identical downstream transition; it should `ALLOW` and produce exactly the same durable value as the coarse condition.

The downstream `Transition` object must be identical between coarse and complete regimes for each probe. The complete-carrier post-admission receipt must depend on the B-profile receipt; the coarse-carrier receipt may depend on the A-profile receipt because the quotient is the object under test.

## Frozen result classes

### `SAFE_QUOTIENT_ESTABLISHED`

Assigned only if:

- histories are genuinely different;
- final operational state is identical;
- first observation distribution is identical;
- all frozen future probes are consequence-equivalent;
- exact Nano bytes are unchanged;
- coarse identity aliases the histories;
- complete identity distinguishes them;
- the downstream transition object is identical across carrier regimes;
- coarse A-standing reuse is `ALLOW` and externally correct for every probe;
- complete carrier initially `DEFER`s for every probe;
- after B-specific standing is admitted, complete carrier `ALLOW`s the same downstream proposal;
- coarse and complete regimes persist the same correct value for every probe.

### `HISTORY_ALIASING_WOUND_ESTABLISHED`

Assigned only if the formal future-equivalence conditions hold but coarse identity reuse produces an externally incorrect durable consequence or a durable consequence that disagrees with the complete-carrier result.

### `ASSAY_INVALID_OR_UNDERCONSTITUTED`

Assigned otherwise.

## Claim ceiling

A positive safe-quotient result earns only:

> In this classical convergent-history specimen, preserving acquisition-history distinction was unnecessary for the frozen future-consequence surface: coarse cross-history standing reuse produced the same correct durable consequences as complete identity.

It does **not** establish that history is generally irrelevant, that future-consequence equivalence is universally sufficient for quotienting, or that OpenCore should erase provenance.
