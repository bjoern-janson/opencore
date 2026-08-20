# OpenCore Mini × Nano — Composition V0

**Status:** `FIRST_CONSTRUCTED_RESULT`  
**Scientific role:** first composition assay between frozen wounded Mini and frozen Nano V0  
**Mini modified:** `NO`  
**Nano modified:** `NO`  
**Git publication:** experimental branch record

## 1. Question

Does Nano V0 change the persistence outcome of already-discovered Mini-stack authority failures without fixing Mini, while still admitting matched legitimate transitions?

The comparison is:

```text
same Mini/external proposer
same proposed transition
        |
        +--> naive persistence
        |
        +--> Nano V0 persistence boundary
```

Only the persistence boundary enforces externally constituted transition contracts.

## 2. Frozen component identities

```text
mini.py SHA-256
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55

nano.py SHA-256
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Both match their pre-composition frozen hashes after the run.

## 3. Reused attack families

No new authority-failure family was invented for this assay.

1. **Role laundering (SSI)** — correct self-prediction is transported as observational support.
2. **Dependency laundering (Correctable Lineage)** — repeated reports from one path are promoted to multiple independent corrective paths.
3. **Acquisition/closure composition (Cerebro / M2×M4)** — acquisition protocol changes after a closure license was valid; closure is attempted under the stale precondition.
4. **Authority/applicability crossing (SSI)** — closure authority is reused where applicability is no longer established.
5. **Stale descendant authority (Cerebro / Nano wound)** — a child standing remains after the warrant parent that licensed it loses authority.
6. **Preservation != warrant regression (Nano wound)** — revoking an unrelated preserved object's warrant must not demote a standing for which that object was only a preservation obligation.

Each illegal transition family has a matched legal counterpart except family 6, which is itself a legitimate-retention regression and is exercised by a fresh post-revocation use transition.

## 4. Final 10,000-seed result

### Illegal transitions

Five attack families × 10,000 seeds:

```text
ATTACK ATTEMPTS             50,000
NAIVE PERSISTENCE ALLOW     50,000 / 50,000
NANO V0 ALLOW                    0 / 50,000
NANO V0 OVERREACH RATE          0%
```

Nano dispositions:

| Family | DENY | DEFER | ALLOW |
|---|---:|---:|---:|
| Role laundering | 10,000 | 0 | 0 |
| Dependency laundering | 0 | 10,000 | 0 |
| Acquisition → closure stale precondition | 10,000 | 0 | 0 |
| Authority → applicability | 10,000 | 0 | 0 |
| Stale descendant | 0 | 10,000 | 0 |

`DEFER` occurs when a required contract-visible standing is absent because its warrant path is not effective. `DENY` occurs where a current standing contradicts the license precondition.

### Matched legitimate / retention paths

Six families × 10,000 seeds:

```text
LEGITIMATE ATTEMPTS         60,000
NANO V0 ALLOW               60,000 / 60,000
NANO LEGITIMATE RETENTION      100%
NANO FALSE REFUSAL               0%
```

The preservation/warrant regression is included here as a real post-revocation transition: after an unrelated preserved B standing loses its producing license, a derived A standing remains effective and successfully drives a fresh licensed use.

### Native Mini lifecycle control

A separate 10,000-seed adapter control routed actual unchanged Mini acquisition and A-revision commitments through both persistence boundaries while requiring B preservation.

```text
NATIVE MINI LIFECYCLE PASS  10,000 / 10,000
```

This checks the acquire → commit → challenge/revise → preserve-unaffected-B path. It does **not** establish complete M1–M6 compatibility.

## 5. Composition centerpiece

The acquisition/closure case explicitly checks stale authorization.

Initially:

```text
current acquisition protocol = UNIFORM
closure license requires      = UNIFORM
challenge count               = q
```

so Nano previews closure as:

```text
ALLOW
```

Then an independently licensed transition changes the protocol:

```text
UNIFORM -> ACTIVE
```

The closure license itself remains authentic, but its precondition is no longer true. At execution Nano rechecks current state and returns:

```text
DENY
```

while naive persistence accepts the same closure proposal.

Thus this constructed integration instantiates:

```text
license possession != current authorization
```

and:

```text
Valid(T1) AND Valid(T2) !=> Valid(T2 o T1)
```

when `Post(T1)` no longer satisfies `Pre(T2)`.

## 6. What changed relative to wounded Mini

Nano does not repair Mini's proposer.

In the role-laundering case, unchanged Mini still commits after one real observation plus one correct self-prediction. The difference appears only at persistence: the external license requires observational source role, so Nano denies the proposed authority-bearing write while naive persistence accepts it.

Likewise, Nano does not discover report dependence, sampling bias, validity boundaries, or warrant ancestry. Those contract-visible facts are supplied by the harness. Nano only prevents the proposed persistent effect from outrunning that supplied contract.

## 7. Claim ceiling

Maximum supported claim from this result:

> **On this constructed composition suite, unchanged wounded Mini/external-stack proposals routed through unchanged Nano V0 produced zero persistent overreach on five previously discovered authority-failure families while retaining every matched licensed transition and the tested native Mini acquire/revise lifecycle.**

Not established:

```text
CONTRACT CORRECTNESS                    NOT_ESTABLISHED
AUTONOMOUS EVIDENCE ROLE DISCOVERY      NOT_ESTABLISHED
AUTONOMOUS DEPENDENCY DISCOVERY         NOT_ESTABLISHED
AUTONOMOUS VALIDITY DISCOVERY           NOT_ESTABLISHED
FULL M1-M6 COMPATIBILITY                NOT_ESTABLISHED
GENERAL MINI+NANO COMPATIBILITY         NOT_ESTABLISHED
CRASH-DURABLE NANO JOURNAL              NOT_ESTABLISHED
CONCURRENT / MULTI-PROCESS SAFETY       NOT_ESTABLISHED
TRUTH / RELIABLE GENERALIZATION         NOT_ESTABLISHED
UNIVERSAL LAWFUL COMPOSITION            NOT_ESTABLISHED
```

The naive store is intentionally weak and should not be interpreted as a strong competing architecture.

## 8. Component regression checks

After the composition run:

```text
python crank/mini.py --seed 0 --sweep 10000
sweep=10000 pass=10000 fail=0

python crank/test_nano.py
7 tests passed
```

No component mutation is hidden by the composition result.

## 9. Local artifacts

```text
crank/mini_nano_composition.py
crank/results/mini_nano_composition_final_10000.json
```

Hashes at first final result:

```text
mini_nano_composition.py
116d6e285855081126608a962ad5bb3990f634c63bf76a40c19f7ad18027e7a2

mini_nano_composition_final_10000.json
f536e1418e48b1a9c6af0a37ba865cdf082f7f8d69fb19e428d689597d1d381f
```

## 10. Current disposition

```text
MINI_NANO_COMPOSITION_V0 = FIRST_CONSTRUCTED_RESULT
PUBLICATION               = EXPERIMENTAL_BRANCH_RECORD
FREEZE                     = NOT_DECLARED_BY_USER
NEXT EXPERIMENT            = NOT_IMPLIED
```
