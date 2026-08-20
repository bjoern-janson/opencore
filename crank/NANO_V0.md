# OpenCore Nano V0

**Status:** `FROZEN_LOCAL_EXPERIMENT`  
**Scientific standing:** `EXPERIMENTALLY_SUPPORTED_ON_FROZEN_CONSTRUCTED_MATRIX`  
**Date frozen:** 2026-08-21  
**Publication status:** experimental branch record  
**Mini + Nano at V0 freeze:** `NOT_OPENED`


> **Post-freeze lineage:** Mini + Nano was subsequently opened as a separate composition assay. See [`MINI_NANO_COMPOSITION_V0.md`](MINI_NANO_COMPOSITION_V0.md). This does not retroactively alter the Nano V0 freeze state.

## 1. Object

OpenCore Nano V0 is deliberately smaller than the theory that motivated it:

> **transition typechecker + in-process append-only journal**

Its hard boundary is:

```text
semantic payload                  = opaque to Nano
transition-contract surface       = inspectable by Nano
```

Nano does not decide truth, evidence semantics, applicability semantics, dependency semantics, or whether an external license is epistemically correct.

Its only prospective judgment is:

```text
(S_t, T, L) -> ALLOW | DENY | DEFER
```

under three externally constituted contract checks:

```text
S_t satisfies Pre(L)
Effect(T) subset Effect(L)
Preserve(L) subset Preserved(S_t, T)
```

Operationally:

```text
ALLOW  = required contract-visible conditions are established and the transition stays within license
DENY   = a required condition is contradicted or the transition exceeds effect/preservation bounds
DEFER  = a required contract-visible proposition is not currently established
```

The V0 kernel invariant is intentionally compact:

> **Don't write beyond your effect capability. Don't erase beyond your preservation capability.**

## 2. Implementation

Primary implementation:

- [`nano.py`](nano.py) — kernel
- [`nano_attack_matrix.py`](nano_attack_matrix.py) — isolated paired attack matrix
- [`test_nano.py`](test_nano.py) — focused kernel self-tests
- [`nano_experiment_v0.md`](nano_experiment_v0.md) — full experimental record

Final `nano.py`:

```text
332 lines total
60 lines  check_transition()
38 lines  apply_transition()
10 lines  effective_state()
11 lines  _receipt_effective()
```

SHA-256:

```text
nano.py                 8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
nano_attack_matrix.py   4f1f564ffb8b2dd43ad0738be17dbeb8f9ad7564551ce168ab1eb2a32dfc89da
test_nano.py            3d9e834c927d6adfc85b7281c83b9d4c207804f841aae687f80990dc791956a4
```

A static domain-term audit of the kernel found no hard-coded rules for `prediction`, `observation`, `closure`, `evidence`, `science`, `generalization`, or `corrigibility`.

## 3. First implementation failure — decorative lineage

The first Nano candidate recorded receipt ancestry but did not make that ancestry causally govern current authority.

Attack:

```text
L0 authorizes parent standing
parent standing is a precondition for L1
L1 authorizes child standing
revoke L0
attempt to use child standing
```

Pre-repair, across 10,000 seeds:

```text
child still effective after upstream revoke   10,000 / 10,000
illegal child use ALLOW                       10,000 / 10,000
```

The failure was:

```text
lineage recorded != lineage causally governing authority
```

### Minimal repair

A receipt is currently effective only when:

```text
its decision was ALLOW
its producing license remains active
all warrant-parent receipts remain effective
```

Warrant-parent effectiveness is checked recursively. Historical receipts remain append-only and unchanged.

Post-repair:

```text
child still effective after upstream revoke        0 / 10,000
illegal child use ALLOW                             0 / 10,000
illegal child use DEFER                        10,000 / 10,000
```

## 4. Second implementation failure — preservation was over-promoted into warrant

The first repair was too conservative: it initially treated required-preservation ancestry as though it were also authority ancestry.

Attack:

```text
L0 creates marker M
L1 independently creates output O but must preserve M
revoke L0
```

`M` constrained what L1 was allowed to erase. It was not a warrant premise for the authority of `O`.

Pre-repair, across 10,000 seeds:

```text
legitimate O effective after L0 revoke       0 / 10,000
legitimate O wrongly deferred            10,000 / 10,000
```

The failure forced the distinction:

```text
preservation dependency != warrant dependency
```

### Minimal repair

Only contract **preconditions** become receipt authority parents.

Required preservation remains an enforced state-protection constraint but does not automatically propagate authority dependency.

Post-repair:

```text
legitimate O effective after L0 revoke  10,000 / 10,000
legitimate O deferred                         0 / 10,000
```

The transitive descendant-revocation attack remains blocked after this narrowing.

## 5. Final strengthened matrix

The final matrix uses 10,000 opaque-ID seeds and six paired attack families. Every illegal transition has an otherwise matched licensed counterpart.

| Family | Illegal result | Matched legal result |
|---|---:|---:|
| role | 10,000 `DENY` | 10,000 `ALLOW` |
| dependency | 10,000 `DEFER` | 10,000 `ALLOW` |
| applicability | 10,000 `DENY` | 10,000 `ALLOW` |
| revocation — transitive | 10,000 `DEFER` | 10,000 `ALLOW` |
| preservation | 10,000 `DENY` | 10,000 `ALLOW` |
| composition | 10,000 `DENY` | 10,000 `ALLOW` |

Primary result:

```text
Overreach       = 0 / 60,000 = 0.000000%
False refusal   = 0 / 60,000 = 0.000000%
Invariant fails = 0
Naive overreach = 60,000 / 60,000 = 100.000000%
```

Seven focused kernel self-tests also pass.

## 6. Composition centerpiece

The composition fixture tests stale authorization directly:

```text
t0: Pre(L2) established
preview(T2) = ALLOW
apply(T1) = ALLOW
T1 changes a Pre(L2) standing
t1: Post(T1) no longer satisfies Pre(L2)
apply(T2) rechecks current state = DENY
```

The matched legal case changes an orthogonal standing and still admits `T2`.

V0 therefore operationalizes on this constructed family:

```text
license possession != current transition authorization
```

A historically valid license does not bypass current-state precondition checking.

## 7. Experimentally forced decomposition

The implementation that survived the frozen matrix currently decomposes behaviorally into:

```text
precondition checking
+ effect ceiling
+ preservation checking
+ warrant-dependency liveness
+ append-only history
```

This is **not** promoted as OpenCore's final ontology or primitive set. It is the smallest decomposition forced by the V0 implementation failures and repairs.

The two negative results preserve an important three-way distinction:

```text
lineage != warrant dependency != preservation obligation
```

## 8. Narrow earned claim

> **On the tested transition family, a 332-line semantically agnostic kernel enforced externally supplied effect, precondition, and preservation contracts, including transitive authority invalidation, without deciding the contracts' semantic correctness.**

This result supports only:

```text
NANO_V0 = EXPERIMENTALLY_SUPPORTED_ON_FROZEN_CONSTRUCTED_MATRIX
```

It does not establish general epistemic correctness.

## 9. Explicit claim ceiling

V0 does **not** establish:

```text
truth checking
correctness of external licenses
autonomous evidence typing
autonomous dependency discovery
reliable generalization
FCD completeness
universal lawful composition
cryptographic license authenticity
multi-process concurrency safety
crash-durable journal persistence / replay
Mini + Nano compatibility
OpenCore primitive status
```

The initial state and license registry are trusted assay inputs. A bad external contract can still authorize bad epistemology.

The append-only journal is demonstrated only for the lifetime of the current process. Crash durability and replay are explicitly untested.

## 10. Freeze boundary

Nano V0 is frozen at the isolated-kernel result.

Do not infer or automatically open:

```text
Nano V1
Mini + Nano
persistent crash-safe journal
cryptographic licenses
schema expansion
kernel primitive promotion
```

The next experiment, if separately opened, must preserve the two failed implementation variants and the final V0 result as part of the scientific lineage.

The central V0 compression is:

> **Nano turned “licensed adaptive transition” from an explanatory idea into an implementation that could itself fail in precise, falsifiable ways.**
