# FOREIGN-005 — Reopenable Quotient

**Status before execution:** `FROZEN_PROSPECTIVE_ASSAY`

## Question

Can a distinction disappear from effective persistent state while remaining recoverable to a future interface that did not exist when the quotient was made?

The assay distinguishes:

1. **safe effective quotient** — the distinction is unnecessary under the current interface;
2. **reopenable quotient** — the distinction is absent from effective state but latent opaque substrate remains interrogable;
3. **destructive quotient** — only the effective quotient remains and the later distinction is no longer identifiable.

No `HistoryID`, oscillatory ontology, Nano repair, automatic interface invention, or automatic representation repair is assumed.

## Frozen foreign world

Two temporal histories:

```text
H_A = (+1, -1, +1, -1)
H_B = (+1, +1, -1, -1)
```

They are genuinely different:

```text
H_A != H_B
```

### Current interface Q0

The only current observables are:

```text
Q0 = {mean, energy}
```

with

```text
mean(H)   = (1/n) * sum_t H_t
energy(H) = sum_t H_t^2
```

For both histories:

```text
mean = 0
energy = 4
```

Therefore:

```text
H_A ~_{Q0} H_B
C_Q0(H_A) = C_Q0(H_B) = event:q0:mean=0:energy=4
```

The initial quotient must be safe across every frozen Q0 consequence used by the harness.

## Manipulated variable: latent substrate retention

### Reopenable condition

Effective state contains only the shared Q0 standing and its downstream consequence.

Separately, the original temporal payloads survive as opaque immutable source objects. Their object IDs are derived from payload digests and do not encode A/B, autocorrelation, frequency class, or the future discriminator. Nano stores only opaque object identities and payload digests; it does not inspect payload bytes.

The future semantic distinction is **not** present in effective standing before interface expansion.

### Destructive condition

Effective state is identical to the reopenable condition at the standing layer, but only the shared Q0 quotient object remains. The original temporal payloads are absent.

## Future interface expansion

A new independently meaningful temporal interface becomes available:

```text
M*(H) = sum_{t=1}^{n-1} H_t H_{t+1}
```

lag-one autocorrelation numerator.

Frozen expected values:

```text
M*(H_A) = -3
M*(H_B) =  1
```

Thus:

```text
H_A !~_{Q0 union {M*}} H_B
```

The interface operates on temporal payload bytes, not on A/B labels or a stored answer.

### New-interface null control

A second newly available observable is:

```text
N*(H) = sum_t |H_t|
```

with:

```text
N*(H_A) = N*(H_B) = 4
```

Therefore new interface availability alone must not force a split.

## Nano boundary

Frozen Nano SHA-256:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Nano may only:

- persist the initial Q0 standing;
- authorize a downstream Q0 consequence under that standing;
- admit externally constituted M*/N* observations;
- authorize refined standings when their externally supplied preconditions are satisfied;
- DEFER refinement when required new evidence is absent.

Nano must not:

- inspect temporal payloads;
- compute mean, energy, M*, or N*;
- decide that the old quotient is too coarse;
- invent the new interface;
- invent a new representation boundary.

## Prospective positive requirements

`REOPENABLE_QUOTIENT_ESTABLISHED` requires all of the following:

1. `H_A != H_B`.
2. `H_A ~_{Q0} H_B` exactly.
3. Initial cross-history reuse through the shared Q0 standing is Nano `ALLOW` and externally correct.
4. Reopenable and destructive branches have identical effective standing state before interface expansion.
5. No M*/N*-specific or refined standing exists in effective state before interface expansion.
6. Opaque retained source payloads permit M* to recover `-3` and `1` without using semantic history labels.
7. The two M* results are admitted and authorize distinct refined persistent standings under unchanged Nano.
8. In the destructive branch, M* is non-identifiable from Q0 alone because the same Q0 carrier has two different frozen M* targets.
9. A refinement attempt without M* evidence is Nano `DEFER` and does not alter effective standing state.
10. N* returns the same value for both retained sources and coarse reuse remains Nano `ALLOW` and externally correct.
11. Nano source SHA-256 is identical before and after execution.

## Result classes

### `REOPENABLE_QUOTIENT_ESTABLISHED`

All prospective positive requirements pass.

### `IRREVERSIBLE_QUOTIENT_WOUND`

The new interface genuinely distinguishes the original histories, but the condition intended to retain interrogable latent substrate cannot support the split.

### `INVALID`

Any constitutive control fails, including initial Q0 inequivalence, pre-encoded future semantics in effective state, failure of the null control, Nano mutation, or a discriminator that depends on A/B labels rather than payload structure.

## Claim ceiling

A positive result does **not** establish:

- that raw history must always be archived;
- that opaque source retention is a universal solution;
- that all safe quotients should remain reopenable forever;
- that future interfaces can always recover erased distinctions;
- that lossless archival storage is intelligent compression;
- a `HistoryID`, `AcquisitionPath`, instrument, oscillatory, or reopenability primitive;
- automatic interface invention;
- automatic quotient refinement;
- Nano V1 or any Nano repair;
- a universal law of memory.

The assay tests only whether effective quotienting and irreversible destruction are experimentally separable in this frozen constructed world.
