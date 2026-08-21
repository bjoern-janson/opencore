# OpenCore Base 001 — Shared Authority-Filtered World

**Status:** `CONSTRUCTED_BASE_LEVEL_RESULT`  
**Publication:** experimental crank branch  
**Nano modified:** `NO`  
**Nano V0 SHA-256:** `8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329`

## 1. Hypothesis

Base-001 tests the first executable version of the architectural hypothesis:

> **Warranted shared-world changes can globally influence heterogeneous local cognition, while remaining globally attributable and revocable, without granting local projections automatic authority to rewrite the shared world.**

The experiment does **not** model literal neurons and does not implement a new learning algorithm.

It builds twelve tiny local projectors over one shared Nano V0 persistence substrate.

The central object is:

```text
shared authority-filtered world
        |
        +-- heterogeneous local projection 0
        +-- heterogeneous local projection 1
        +-- ...
        +-- heterogeneous local projection 11
```

Each local unit can inspect the same effective global standing but may respond differently according to externally supplied relevance and private state.

## 2. Question

Can one admitted global standing `G`:

1. become available to every local unit;
2. cause persistent changes only in units for which `G` is relevant;
3. lose its current authority through one upstream warrant revocation;
4. make only warrant-dependent downstream consequences ineffective;
5. preserve unrelated local learning that merely happened later;
6. preserve historical receipts rather than destructively rewriting local state; and
7. prevent a local projection from silently promoting its derived state into a new global standing without a separately licensed edge?

## 3. Construction

Each world contains exactly 12 units.

- 8 units are externally marked relevant to `G`.
- 4 units can see `G` but are externally marked irrelevant.
- Relevant units use four small projection modes (`AMPLIFY`, `INVERT`, `GATE`, `ROUTE`) plus private opaque tokens, producing heterogeneous local outputs.
- Relevance, projection functions, licenses, and dependency semantics are harness-supplied.

### 3.1 Admit the shared standing

Nano receives a licensed transition:

```text
G: ABSENT -> EFFECTIVE
```

All twelve units read the same effective shared world.

### 3.2 Relevant local consequences

For each relevant unit `i`, the harness proposes a persistent local standing `H_i` under a license with the explicit precondition:

```text
G == EFFECTIVE
```

Because Nano V0 records effective precondition receipts as warrant parents, each accepted `H_i` receives causal authority ancestry from `G`.

Irrelevant units see `G` but their local projection is unchanged, and they make no `G`-derived persistence proposal.

### 3.3 Temporal-ancestry control

After `G` and `H_i` exist, **all twelve units** acquire an unrelated local standing `L_i`.

Those licenses have no `G` or `H_i` precondition.

Therefore these local adaptations happen later in time but do not acquire `G` as warrant ancestry.

This is the permanent control for:

```text
historical / temporal ancestry != authority ancestry
```

### 3.4 Local descendant

One relevant unit uses its `H_i` under a separately licensed local-use edge to produce a local descendant `D_i`.

This gives a two-step authority chain:

```text
G -> H_i -> D_i
```

### 3.5 Local-to-global escalation attack

The same unit then attempts:

```text
G -> H_i -> J_global
```

using only its local-use license.

The `H_i` precondition is valid and live. The attack differs only in requested effect: the transition tries to write a global standing that the local-use license does not grant.

Naive persistence accepts the write.

Nano V0 returns:

```text
DENY
reason = effect:write_not_licensed
```

### 3.6 Matched licensed re-export

A separate externally constituted global-export license explicitly allows:

```text
H_i -> J_global_licensed
```

Nano accepts it.

The accepted `J_global_licensed` receipt has `H_i` as a warrant parent, while `H_i` has `G` as a warrant parent:

```text
G receipt -> H_i receipt -> J receipt
```

This creates a transitive globally visible consequence without losing attribution to `G`.

### 3.7 Revoke only the upstream warrant

Finally the harness issues one transition:

```text
revoke producing license of G
```

The revocation transition contains:

```text
local writes  = 0
local deletes = 0
```

No cleanup, replay, undo, or local rewrite is sent to any unit.

## 4. Metrics

The frozen metrics are:

```text
Reach
RelevantResponse
IrrelevantDisturbance
RevocationRecovery
CollateralLoss
```

with additional controls for:

```text
naive revocation recovery
local->global authority escalation
matched licensed global re-export
transitive re-export revocation
transitive local-descendant revocation
history preservation without cleanup
post-G independent learning warrant-parent count
```

## 5. Final 10,000-world result

Each world contains 12 units, so the final sweep contains:

```text
120,000 unit-level reach opportunities
 80,000 relevant-response/revocation opportunities
 40,000 irrelevant-unit opportunities
120,000 unrelated post-G local adaptations
 10,000 illegal local->global export attempts
 10,000 matched licensed global exports
```

Results:

| Metric | Result |
|---|---:|
| Reach | **120,000 / 120,000 = 100%** |
| RelevantResponse | **80,000 / 80,000 = 100%** |
| IrrelevantDisturbance | **0 / 40,000 = 0%** |
| RevocationRecovery | **80,000 / 80,000 = 100%** |
| NaiveRevocationRecovery | **0 / 80,000 = 0%** |
| CollateralLoss | **0 / 120,000 = 0%** |
| Illegal global export — naive | **10,000 / 10,000 ALLOW** |
| Illegal global export — Nano | **0 / 10,000 ALLOW; 10,000 DENY** |
| Matched licensed global export | **10,000 / 10,000 ALLOW** |
| `G -> H_i -> J` receipt ancestry correct | **10,000 / 10,000** |
| Licensed `J` loses effective authority after `G` revocation | **10,000 / 10,000** |
| Local `D_i` loses effective authority after `G` revocation | **10,000 / 10,000** |
| History preserved without local cleanup | **10,000 / 10,000** |
| All independent post-G `L_i` have zero warrant parents | **10,000 / 10,000 worlds** |
| Revocation uses zero local writes/deletes | **10,000 / 10,000 worlds** |

No failing world was observed in the 10,000-world sweep.

Nano's frozen seven-test self-test suite still passes after the experiment.

## 6. First-world state shape after revocation

In the first world, immediately after the single upstream revocation:

```text
active standings   = 12
deferred standings = 11
```

The 12 active standings are exactly the unrelated local `L_i` adaptations.

The 11 deferred standings are:

```text
1 x G
8 x H_i
1 x local H_i-derived D_i
1 x explicitly licensed global re-export J
```

Nothing was destructively deleted.

This is the central Base-001 behavior:

```text
upstream warrant dies
-> authority-effective world changes
-> all causally dependent local/global consequences stop being effective
-> unrelated later local learning remains effective
-> historical receipts remain present
```

## 7. What this supports

The narrow supported result is:

> **On this constructed 12-unit world, a single warranted shared standing influenced all local projectors, produced heterogeneous persistent effects only in externally designated relevant units, and one upstream warrant revocation removed all tested warrant-dependent effective consequences without local cleanup or collateral loss of unrelated post-event learning. Nano also prevented an unlicensed local-to-global promotion while admitting a matched explicitly licensed re-export.**

A useful mechanical compression is:

```text
raw persistent state
-> authority-filtered effective world
-> heterogeneous local projection
-> local proposal
-> Nano admission
```

and on revocation:

```text
warrant invalidated
-> effective world changes
-> dependent projections/standings lose current force
```

without:

```text
iterate through every local memory and destructively undo it
```

## 8. What the experiment adds to Nano evidence

The prior Mini x Nano ablation found that the frozen Mini wound suite identified:

```text
live preconditions + warrant liveness
```

as sufficient for all five tested protections, while effect-ceiling and preservation enforcement were not identified as necessary by that intervention family.

Base-001 naturally introduces a different failure:

```text
local authority -> unauthorized global write
```

The relevant Nano denial contains only:

```text
effect:write_not_licensed
```

while its `H_i` precondition is established and its warrant ancestry is live.

Therefore Base-001 provides direct constructed pressure on the **effect ceiling** that the Mini wound suite did not provide.

This does **not** establish global Nano minimality.

Actual preservation-violation enforcement is still not tested by Base-001.

## 9. What is scaffolded

The harness supplies all of the following:

```text
which units exist
which units are relevant to G
the local projection functions
the global and local standing vocabulary
the licenses
which preconditions constitute warrant ancestry
which local->global edge is licensed
```

The units do not discover relevance.

Nano does not discover warrant structure.

The shared world does not learn its own transition laws.

The experiment therefore does not establish autonomous distributed cognition.

## 10. Explicit non-claims

```text
OPENCORE BASE IMPLEMENTED GENERALLY          NOT_ESTABLISHED
AUTONOMOUS RELEVANCE DISCOVERY               NOT_ESTABLISHED
AUTONOMOUS WARRANT DISCOVERY                 NOT_ESTABLISHED
DISTRIBUTED LEARNING                         NOT_ESTABLISHED
SCALING BEYOND THIS 12-UNIT FAMILY           NOT_ESTABLISHED
CONCURRENT / ASYNCHRONOUS UNIT SAFETY        NOT_ESTABLISHED
CRASH-DURABLE SHARED JOURNAL                 NOT_ESTABLISHED
PRESERVATION ENFORCEMENT NECESSITY           NOT_ESTABLISHED HERE
GLOBAL NANO MINIMALITY                       NOT_ESTABLISHED
TRUTH / RELIABLE GENERALIZATION              NOT_ESTABLISHED
```

## 11. Current interpretation

The experiment makes one part of the myelin/world analogy computationally tangible:

> **A warranted experience can become part of the effective world seen by every local unit, while the current influence of that experience remains attributable to a live authority path rather than being destructively copied into every local memory.**

The stronger candidate idea is:

```text
global learning without global destructive rewriting
```

Base-001 supports that phrase only for this explicit constructed authority-dependency family.

## 12. Artifacts

```text
crank/base_001_shared_world.py
crank/results/base_001_shared_world_final_10000.json
```

SHA-256 at final run:

```text
base_001_shared_world.py
e8b435da6b3e18a7d718d5add22d2c7575e23bae787bf92f3dc99827f9bc1463

base_001_shared_world_final_10000.json
f63f9e750c5059df3c7c28ccd2ad3d62158dc354d2d0f7fc20490e932eef9802

nano.py
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```
