# FOREIGN-005 — Reopenable Quotient

**Classification:** `REOPENABLE_QUOTIENT_ESTABLISHED`

## Scientific question

Can a distinction disappear from effective persistent state while remaining recoverable to a future interface that did not exist when the quotient was made?

FOREIGN-005 distinguishes:

```text
safe effective quotient
!= reopenable quotient
!= destructive quotient
```

The manipulated variable is whether opaque source substrate remains available behind an otherwise identical effective standing state.

## Prospective freeze

Specification SHA-256 before any execution:

```text
3ee7955a8f5eb6811473d7a89d5c0ddc1aad195a0aa43cab913b4af261d3cf68
```

Original harness SHA-256:

```text
a3985d79dcfecaf7e8aa2a0ad99177997bff4e36194417c3bcde8fd119b13dab
```

Frozen Nano SHA-256:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

### Execution-interface repair provenance

The first harness invocation failed before Nano construction because Python 3.13's `dataclass` machinery requires a dynamically imported module to be present in `sys.modules` during module execution.

No assay transition ran and no scientific result was observed.

The failed original harness remains frozen. A V2 harness made only the minimal loader compatibility repair:

```text
+ import sys
+ sys.modules[spec.name] = module
```

No world definition, result class, discriminator, Nano contract, expected result, or scientific control changed.

V2 harness SHA-256 before the successful execution:

```text
342e2d3da2357ea1d6aaa56417ab841dec5ec6d8a97cb4259b825695d7364e2d
```

The first failed run is retained separately as `run.log`; the successful repaired execution is `run_v2.log`.

## Foreign world

```text
H_A = (+1, -1, +1, -1)
H_B = (+1, +1, -1, -1)
```

Thus:

```text
H_A != H_B
```

The current interface is:

```text
Q0 = {mean, energy}
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

The initial quotient was safe on the frozen Q0 consequence.

## Initial persistence geometry

Two Nano branches were constructed.

### Reopenable branch

The shared Q0 standing is effective. The original temporal payloads exist only as opaque source objects whose IDs are digest-derived:

```text
opaque:0ef8548fd59908fd39d5
opaque:605cb9401437ac120cd1
```

The IDs do not encode A/B, autocorrelation, lag, or the future discriminator.

### Destructive branch

The same Q0 quotient standing is effective, but the temporal source payloads are absent.

Critically, the two branches have **identical effective standing state before interface expansion**.

In each branch, history A establishes the shared Q0 standing and the later B-directed consequence uses that standing:

```text
Q0 A admission -> ALLOW
Q0 B use       -> ALLOW
```

Causal receipt ancestry is explicit.

Reopenable branch:

```text
A Q0 receipt:          d0ceba69103303ba8326193b
B Q0 parent receipt:   d0ceba69103303ba8326193b
```

Destructive branch:

```text
A Q0 receipt:          faf8ec26dd8091cb82533e82
B Q0 parent receipt:   faf8ec26dd8091cb82533e82
```

Thus cross-history standing reuse genuinely occurred and was correct under Q0.

## Future interface expansion

The new interface is lag-one autocorrelation numerator:

```text
M*(H) = sum_t H_t H_{t+1}
```

Exact results:

```text
M*(H_A) = -3
M*(H_B) =  1
```

Therefore:

```text
H_A !~_{Q0 union {M*}} H_B
```

An independent arithmetic implementation reproduced the same Q0 collision and M* split.

### Reopenable branch

M* interrogated the retained opaque payload bytes, not semantic A/B labels.

The observations were admitted by unchanged Nano and each authorized its corresponding refined standing:

```text
M*(H_A) observation -> ALLOW
A refinement        -> ALLOW

M*(H_B) observation -> ALLOW
B refinement        -> ALLOW
```

Receipt ancestry again shows that the newly constituted observation, not the old Q0 standing alone, authorized refinement:

```text
A M* observation receipt:      2ac9e1242bdb656782721136
A refinement parent receipt:   2ac9e1242bdb656782721136

B M* observation receipt:      eeb34b2de54691f22cd59f30
B refinement parent receipt:   eeb34b2de54691f22cd59f30
```

The future semantic distinction was absent from effective state before M* and present only after the new observations and refinements.

### Destructive branch

Only the shared Q0 carrier remains:

```text
Q0(H_A) = Q0(H_B) = (0,4)
```

but the frozen M* targets differ:

```text
M*(H_A) = -3
M*(H_B) = 1
```

Therefore no deterministic function of Q0 alone can recover both targets on this frozen pair.

The harness records:

```text
deterministic_recovery_from_q0_impossible = true
```

An attempted refinement without an M* observation returned:

```text
DEFER
precondition:unestablished:destroyed-source|new-observation|M-star
```

and did not change effective standing state.

Thus smarter downstream authorization cannot reconstruct information that the upstream destructive quotient no longer exposes.

## New-interface null control

The second newly available interface is:

```text
N*(H) = sum_t |H_t|
```

Exact results:

```text
N*(H_A) = 4
N*(H_B) = 4
```

Under the same aliasing geometry:

```text
N* A admission -> ALLOW
N* B use       -> ALLOW
```

with causal parentage:

```text
A N* receipt:          4cb0265b5303465c7536824e
B N* parent receipt:   4cb0265b5303465c7536824e
```

The null interface therefore does not trigger an unnecessary split.

## Checks

```text
formal checks:       8 / 8 PASS
persistence checks: 28 / 28 PASS
```

Nano SHA-256 before and after:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Nano was not modified.

## Earned result

On this frozen constructed classical specimen:

> A history distinction was legitimately absent from effective state under the current Q0 interface. When a new consequence-relevant temporal interface became available, a branch that retained only opaque interrogable source substrate could recover and persist the newly exposed distinction, while an otherwise effectively identical branch that had destructively discarded that substrate could not identify the split. A newly available null interface remained safely quotiented.

This establishes, on the tested family:

```text
safe effective compression
!= irreversible information destruction
```

and experimentally separates:

```text
safe quotient
reopenable quotient
destructive quotient
```

## Candidate strengthened, not proven

A stronger hypothesis is now worth further attack:

> Intelligent compression may sometimes preserve not the currently meaningful distinction itself, but enough latent interrogable substrate for future interfaces to regenerate a distinction if later reality makes it consequential.

This is not yet a general design principle or architecture.

## Claim ceiling

FOREIGN-005 does **not** establish:

- a universal archival requirement;
- that raw source retention is the correct general solution;
- that all safe quotients should remain reopenable forever;
- that future interfaces can always recover destroyed distinctions;
- that lossless archival storage is intelligent compression;
- a `HistoryID`, `AcquisitionPath`, instrument, oscillatory, or reopenability primitive;
- automatic interface invention;
- automatic quotient refinement;
- Nano V1 or any Nano repair;
- a universal theory of memory.

## Diagnosis

`reopenability pressure established at the representation/substrate boundary upstream of unchanged Nano`
