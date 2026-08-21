# FOREIGN-004 — Safe quotient under future-consequence equivalence

## Result

`SAFE_QUOTIENT_ESTABLISHED`

## Prospective freeze

The assay specification was frozen before execution:

```text
FOREIGN_004_SPEC.md SHA-256
6d86d2c8f7ea36e095a4a142e6f70007e0382f904e4773f7e0393cb05d27dd37
```

Harness before execution:

```text
foreign_004.py SHA-256
dbfc6ff62e5d36bea75f1f34b0f19bb17d96bd6808a2d921d05add4621d21a52
```

Frozen Nano V0:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Nano had the same SHA-256 before and after execution.

## Classical world

Two genuinely different histories begin at counter `0`:

```text
H_A: 0 -> 1 -> 2
H_B: 0 -> 3 -> 2
```

Their operation sequences and intermediate states differ, while the final operational state is identical:

```text
H_A != H_B
s'_A = s'_B = {counter: 2}
```

Each history emits `x ~ Bernoulli(1/2)` independently of history. The assay conditions on `x=0`.

## Frozen future-consequence surface

`Q = {X, Y, Z}` was fixed before execution.

At the converged state `counter=2`:

```text
X -> EVEN
Y -> HIGH
Z -> HALF
```

For every frozen probe:

```text
P_A(y | x=0, M) = P_B(y | x=0, M)
```

All 7 formal world/equivalence checks passed.

## Persistence manipulation

Coarse carrier:

```text
C_coarse(A,0) = C_coarse(B,0) = event:x:0
```

Complete carrier:

```text
C_complete(A,0) = event:A:x:0
C_complete(B,0) = event:B:x:0
```

No Nano modification or new semantic primitive was introduced.

## Results by probe

### X

Truth under A and B: `EVEN`.

Coarse:

```text
A profile receipt = 77851dd783e719f468350a43
B downstream decision = ALLOW
B persisted value = EVEN
external correctness = true
B receipt parent = 77851dd783e719f468350a43
```

Complete:

```text
before B standing = DEFER
B profile receipt = 1732c5bfca861e7d4ed76737
after B standing = ALLOW
persisted value = EVEN
external correctness = true
B downstream parent = 1732c5bfca861e7d4ed76737
```

Identical downstream transition digest in both regimes:

```text
a1db44b7c7e683d89634512ad6d0bad602bc8c064804f82128a68912da883b4c
```

### Y

Truth under A and B: `HIGH`.

Coarse:

```text
A profile receipt = 18061f7cdddf2862b3e4ec63
B downstream decision = ALLOW
B persisted value = HIGH
external correctness = true
B receipt parent = 18061f7cdddf2862b3e4ec63
```

Complete:

```text
before B standing = DEFER
B profile receipt = 1b2cef28f2838910915eb983
after B standing = ALLOW
persisted value = HIGH
external correctness = true
B downstream parent = 1b2cef28f2838910915eb983
```

Identical downstream transition digest:

```text
7c8a9b42a6b7997f7739ea2c4ef680e17e6979c7239228b1ea6decc6dcfb5259
```

### Z

Truth under A and B: `HALF`.

Coarse:

```text
A profile receipt = f9979da920fa91bb9af7ab64
B downstream decision = ALLOW
B persisted value = HALF
external correctness = true
B receipt parent = f9979da920fa91bb9af7ab64
```

Complete:

```text
before B standing = DEFER
B profile receipt = c633fb5a1a25645cf5be3dfc
after B standing = ALLOW
persisted value = HALF
external correctness = true
B downstream parent = c633fb5a1a25645cf5be3dfc
```

Identical downstream transition digest:

```text
57ac91805e93bc08c4439264fbfa8a66885baeaac5c926cbb6fc8e06b2e0104c
```

## Summary checks

```text
formal checks:      7 / 7 PASS
persistence checks: 40 / 40 PASS
```

The coarse carrier did permit cross-history warrant reuse. Unlike OQ-002 and FOREIGN-003, that authority transfer was safe across the entire frozen future-consequence surface because the two histories had converged to the same operational state and all constituted downstream consequences were identical.

The complete carrier preserved provenance separation and initially deferred until B-specific standing was established, but after establishment it produced exactly the same correct durable values as the coarse condition.

## Earned claim

> In this classical convergent-history specimen, preserving acquisition-history distinction was unnecessary for the frozen future-consequence surface: coarse cross-history standing reuse produced the same correct durable consequences as complete identity.

This falsifies the stronger candidate that all history aliasing is inherently unsafe.

## Candidate strengthened, not proven

A narrower candidate is now better supported:

> Persistence identity needs to preserve a historical distinction only to the extent that the distinction remains relevant to the constituted future consequence structure.

Equivalent compression:

```text
premature quotient != history quotient
premature quotient = collapse across a distinction still required downstream
```

This remains a candidate cross-domain mechanism, not a universal law or an automatically computable criterion.

## Not claimed

- history is generally irrelevant;
- provenance should be erased;
- future-consequence equivalence is universally sufficient for quotienting;
- the frozen probe surface is complete over every conceivable future query;
- OpenCore can automatically discover the correct quotient;
- a new OpenCore primitive is earned;
- Nano should be modified.

## Execution artifact

```text
foreign_004_result.json SHA-256
8fcb4d1de4889f3006e3aaf398951474d4c9149ddb46f0204725043ede86a048

run.log SHA-256
3578f14cc767669b41f3f7cad93c617a05c1ce674310bf1b65863692c1a07e02
```
