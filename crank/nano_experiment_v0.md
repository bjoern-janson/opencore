# OpenCore Nano — first isolated implementation experiment

**Status:** local crank artifact; uncommitted; unpublished  
**Kernel object:** transition typechecker + in-process append-only journal  
**Mini coupling:** none  
**Semantic payload interpretation:** none

## Frozen question

> Given externally constituted, kernel-visible transition contracts, can a small semantically agnostic persistence kernel reject persistent effects that exceed those contracts while admitting matched licensed transitions?

The frozen decision surface is:

```text
(S_t, T, L) -> ALLOW | DENY | DEFER
```

with three checks:

```text
S_t satisfies Pre(L)
Effect(T) subset Effect(L)
Preserve(L) subset Preserved(S_t,T)
```

`DENY` means a visible contradiction or contract violation. `DEFER` means a required contract-visible proposition is not currently established.

## Implementation

`nano.py` implements opaque `ObjectRecord` payload references plus typed `Standing`, `License`, `Transition`, and append-only `Receipt` records.

The kernel does not contain domain rules for prediction, observation, evidence, closure, science, generalization, or corrigibility.

Final implementation size:

```text
nano.py                  332 lines
check_transition()        60 lines
apply_transition()        38 lines
effective_state()         10 lines
_receipt_effective()      11 lines
```

The journal is append-only for the lifetime of the process. Crash durability / replay across process restart is **not tested in V0**.

## Initial paired matrix

The first six-family matrix covered:

```text
role
dependency
applicability
revocation
preservation
composition
```

with a matched licensed transition for every illegal transition.

The first 10,000-seed run reported:

```text
Nano overreach       0 / 60,000
Nano false refusal   0 / 60,000
Naive overreach     60,000 / 60,000
```

This first result was **not accepted as sufficient** because a code-level audit exposed a stronger descendant case missing from the revocation fixture.

## Negative result 1 — descendant authority did not propagate

Focused construction:

```text
L0 authorizes parent standing
parent standing -> precondition for L1
L1 authorizes child standing
revoke L0
attempt to use child standing
```

The original Nano stored the parent receipt ID in the child receipt but did not use that dependency when computing current effectiveness.

Pre-repair, 10,000 seeds:

```text
child still effective after upstream revoke   10,000 / 10,000
illegal child use ALLOW                       10,000 / 10,000
```

This reproduced the standing-inertia failure inside Nano itself.

### Minimal repair 1

A standing produced by a receipt is effective only if:

```text
producing receipt decision == ALLOW
producing license is active
all warrant-parent receipts remain effective
```

Receipt effectiveness is checked recursively. Historical receipts remain unchanged.

Post-repair, 10,000 seeds:

```text
child still effective after upstream revoke        0 / 10,000
illegal child use ALLOW                             0 / 10,000
illegal child use DEFER                        10,000 / 10,000
```

## Negative result 2 — preservation ancestry was over-promoted into authority dependency

The first repair initially treated both precondition inputs and required-preservation inputs as authority parents.

Focused construction:

```text
L0 creates marker M
L1 independently creates output O but must preserve M
revoke L0
```

`M` was a preservation obligation, not a warrant premise for `O`.

Pre-repair, 10,000 seeds:

```text
legitimate O effective after L0 revoke       0 / 10,000
legitimate O wrongly deferred            10,000 / 10,000
```

This was the conservative mirror failure: Nano could reduce overreach by inventing authority dependencies and creating false refusals.

### Minimal repair 2

Only contract **preconditions** become receipt authority parents.

Required preservation remains enforced as a transition constraint but does not automatically become a standing-warrant dependency.

This preserves:

```text
historical / protected relation != authority dependency
```

Post-repair, 10,000 seeds:

```text
legitimate O effective after L0 revoke  10,000 / 10,000
legitimate O deferred                         0 / 10,000
```

The earlier descendant attack still remains blocked after this narrowing.

## Final strengthened matrix

The final revocation family uses the transitive descendant construction rather than the easier direct-license case.

10,000 opaque-ID seeds, six families, paired illegal/legal transitions:

| Family | Illegal outcome | Legal outcome |
|---|---:|---:|
| role | 10,000 DENY | 10,000 ALLOW |
| dependency | 10,000 DEFER | 10,000 ALLOW |
| applicability | 10,000 DENY | 10,000 ALLOW |
| revocation (transitive) | 10,000 DEFER | 10,000 ALLOW |
| preservation | 10,000 DENY | 10,000 ALLOW |
| composition | 10,000 DENY | 10,000 ALLOW |

Primary metrics:

```text
Overreach       = 0 / 60,000 = 0.000000%
False refusal   = 0 / 60,000 = 0.000000%
Invariant fails = 0
Naive overreach = 60,000 / 60,000 = 100.000000%
```

Seven focused kernel self-tests also pass.

## Composition centerpiece

The composition fixture deliberately creates a stale authorization preview:

```text
t0: Pre(L2) established
preview(T2) = ALLOW
apply(T1) = ALLOW
T1 changes a Pre(L2) standing
t1: Post(T1) no longer satisfies Pre(L2)
apply(T2) rechecks current state = DENY
```

The matched legal case changes an orthogonal standing and still admits `T2`.

Thus the implemented runtime enforces on this constructed fixture:

```text
license possession != current transition authorization
```

and does not treat an earlier `ALLOW` preview as a capability token for later execution.

## What V0 did not establish

V0 does **not** establish:

```text
contract correctness
truth of opaque payloads
autonomous evidence typing
autonomous dependency discovery
reliable generalization
FCD completeness
universal lawful composition
cryptographic license authenticity
multi-process concurrency safety
crash durability / journal replay
Mini + Nano compatibility
OpenCore primitive status
```

The initial state and license registry are trusted inputs to this assay. A bad external contract can still authorize bad epistemology.

## Narrow result

On this frozen constructed matrix, the final Nano candidate provides evidence for the narrow proposition:

> Given externally constituted kernel-visible preconditions, effect ceilings, preservation obligations, and license-revocation state, a small semantically agnostic transition kernel can reject tested transitions that exceed those contracts while admitting their matched licensed counterparts.

The two pre-freeze negative results are part of the result. They specifically forced the distinction between:

```text
lineage != warrant dependency
```

and made receipt dependency causally operative rather than decorative.
