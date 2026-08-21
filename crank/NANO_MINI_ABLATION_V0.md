# OpenCore Nano × Mini — Subtraction / Ablation V0

**Status:** `FROZEN_CONSTRUCTED_DECOMPOSITION`  
**Publication:** experimental crank branch  
**Mini modified:** `NO`  
**Nano modified:** `NO`  
**Frozen composition cases modified:** `NO`

## 1. Question

After Nano V0 blocked the previously discovered wounded-Mini persistence failures,
the next question was subtractive:

> **What is the smallest persistence mechanism that still reproduces the observed boundary on the exact frozen Mini × Nano composition suite?**

No new attack family was introduced.

The existing trial functions in `mini_nano_composition.py` were reused unchanged.
The ablation harness changes only the persistence-boundary class instantiated by
those trials.

## 2. Frozen component identities

```text
mini.py
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55

nano.py
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329

mini_nano_composition.py
116d6e285855081126608a962ad5bb3990f634c63bf76a40c19f7ad18027e7a2
```

Post-run regressions:

```text
Mini sweep: 10,000 pass / 0 fail
Nano tests: 7 passed
```

## 3. Ablation arms

### Naive persistence

Applies every proposed persistent effect.

### Effect ceiling only

Checks only that the license exists, is not directly revoked, the operation
matches, and requested writes/deletes/revocations fit its effect envelope.

It does **not** check preconditions, preservation obligations, or warrant-parent
receipt liveness.

### Live preconditions only

Rechecks exact license preconditions against the current raw standing at
execution time.

It does **not** propagate warrant-parent receipt authority. A stale descendant
can therefore remain present in raw state after an upstream warrant is revoked.

### Lineage / liveness only

Tracks warrant-parent receipt ancestry and direct/upstream license liveness.

It deliberately ignores precondition values. Existing declared warrant inputs
must remain live, but this arm does not ask whether their current values satisfy
the semantic contract predicate.

### Preconditions + lineage

Rechecks exact preconditions against **liveness-filtered** current standing.

It intentionally omits both effect-ceiling checking and preservation checking.
This arm was added only after the single-feature ablations showed selective,
complementary failures.

### Full Nano V0

The unchanged 332-line frozen kernel.

## 4. Final 10,000-seed attack matrix

Each cell is `illegal transitions ALLOW / 10,000`. Lower is better.

| Frozen attack family | naive | effect only | preconditions only | lineage/liveness only | preconditions + lineage | full Nano |
|---|---:|---:|---:|---:|---:|---:|
| prediction → observation/support role | 10,000 | 10,000 | **0** | 10,000 | **0** | **0** |
| correlated reports → independent paths | 10,000 | 10,000 | **0** | 10,000 | **0** | **0** |
| active acquisition → stale closure | 10,000 | 10,000 | **0** | 10,000 | **0** | **0** |
| closure authority → applicability | 10,000 | 10,000 | **0** | 10,000 | **0** | **0** |
| stale warrant parent → descendant use | 10,000 | 10,000 | 10,000 | **0** | **0** | **0** |

Aggregate attack overreach:

```text
naive                         50,000 / 50,000
EFFECT_CEILING_ONLY           50,000 / 50,000
LIVE_PRECONDITIONS_ONLY       10,000 / 50,000
LINEAGE_LIVENESS_ONLY         40,000 / 50,000
PRECONDITIONS_PLUS_LINEAGE         0 / 50,000
FULL_NANO                          0 / 50,000
```

## 5. Disposition structure

The selective failures are deterministic on this constructed suite.

`LIVE_PRECONDITIONS_ONLY` reproduces full Nano on four families:

```text
role laundering             -> DENY
missing independence fact   -> DEFER
stale acquisition protocol  -> DENY
expired applicability       -> DENY
```

but fails completely on stale descendant authority:

```text
stale descendant use        -> ALLOW
```

`LINEAGE_LIVENESS_ONLY` produces the exact complementary result:

```text
stale descendant use        -> DEFER
```

but allows all four value/presence-precondition attacks.

The derived `PRECONDITIONS_PLUS_LINEAGE` arm matches full Nano's dispositions on
all five attack families.

## 6. Legitimate-transition retention

All persistence-boundary arms retained every matched legitimate transition:

```text
60,000 / 60,000 ALLOW
```

for each arm.

All also preserved the actual unchanged Mini lifecycle control:

```text
10,000 / 10,000 pass
```

The permanent Nano wound regression also remained clean in every arm:
revoking an unrelated preserved object's warrant did not demote the derived A
standing for which that object was only a preservation obligation.

## 7. Main result

On this exact frozen composition suite:

```text
EFFECT_CEILING_ONLY     contributes no observed blocking power
LIVE_PRECONDITIONS      blocks four of five known attack families
WARRANT_LIVENESS        blocks the complementary stale-descendant family
PRECONDITIONS + LIVENESS reproduces FULL_NANO
```

Therefore the narrow supported compression is:

> **For the five frozen wounded-Mini authority attacks, execution-time exact precondition checking over warrant-lineage-filtered current state is sufficient to reproduce full Nano V0's persistence decisions while retaining all tested legitimate transitions.**

Equivalently, on this suite:

```text
current contract state
        +
warrant ancestry liveness
        =
full observed Mini-protection effect
```

## 8. What this does *not* establish

This result does **not** establish that Nano should globally be reduced to those
two mechanisms.

Two important mechanisms are not identifiable as necessary from this particular
composition suite:

### Effect ceiling

The frozen Mini × Nano attack set contains no direct attempt to write a value,
delete a key, revoke a license, or invoke an operation outside the license's
effect envelope.

The SSI role-laundering case is encoded in the frozen harness as a source-role
**precondition**. Therefore effect-only has no opportunity to distinguish it.

So:

```text
effect ceiling not load-bearing here
!=
effect ceiling globally redundant
```

### Preservation checking

The frozen preservation case is a **false-refusal regression**:

```text
preservation relation != warrant dependency
```

It tests that Nano does not over-propagate authority through preservation ancestry.
It does not propose a transition that actually violates a required preservation
obligation.

Therefore an arm with no preservation enforcement can still pass this suite.

So:

```text
preservation check not load-bearing here
!=
preservation check globally redundant
```

The isolated Nano V0 matrix does contain direct effect/preservation violations;
this composition ablation deliberately did not replace that experiment with a
new one.

## 9. Scientific interpretation

The result is the selective-ablation outcome hoped for, with one additional
compression.

The frozen Mini wounds separate into two causal classes:

```text
contract-state failures
    role
    dependency
    acquisition/closure composition
    applicability

warrant-liveness failure
    stale descendant
```

Neither mechanism alone is sufficient.

Their composition is sufficient on the frozen suite.

That gives a lower-level executable instance of the recurring composition theme:
components can have individually limited coverage while their interaction closes
a failure family neither covers alone.

But this is not evidence that the two-mechanism pair is universally sufficient.
It is a local minimality result over a frozen constructed family.

## 10. Frozen claim ceiling

Maximum claim supported by this ablation:

> **On the frozen Mini × Nano composition suite, full Nano V0's observed protection can be reproduced by the combination of execution-time exact precondition checking and warrant-dependency liveness; neither mechanism alone reproduces the result, and the suite does not identify effect-ceiling or preservation enforcement as necessary.**

Not established:

```text
GLOBAL NANO MINIMALITY                    NOT_ESTABLISHED
EFFECT CEILING REDUNDANCY                 NOT_ESTABLISHED
PRESERVATION CHECK REDUNDANCY             NOT_ESTABLISHED
GENERAL MINI+NANO COMPATIBILITY           NOT_ESTABLISHED
CONTRACT CORRECTNESS                      NOT_ESTABLISHED
AUTONOMOUS CONTRACT DISCOVERY             NOT_ESTABLISHED
TRUTH / RELIABLE GENERALIZATION           NOT_ESTABLISHED
UNIVERSAL COMPOSITION SUFFICIENCY         NOT_ESTABLISHED
```

## 11. Artifacts

```text
crank/nano_ablation.py
crank/results/nano_mini_ablation_final_10000.json
```

The ablation harness is intentionally separate from `nano.py`; Nano V0 remains
byte-identical.
