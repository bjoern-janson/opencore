# OpenCore

> Experimental substrate for **bounded epistemic compounding**: useful persistent state without self-erasure of the causal routes required for correction.

OpenCore studies how adaptive systems can accumulate persistent causal leverage while remaining exposed to externally grounded consequence capable of reducing that leverage.

This branch is the active experimental lineage. The original K0 charter, kernel contract, and E001 specification remain frozen historical artifacts and are not rewritten by crank results.

## Current status

| Field | Current status |
| --- | --- |
| Research object | Causal geometry of bounded epistemic compounding |
| Phase | Empirical pressure-testing of representation, exposure, recognition, and authority revision |
| Trusted persistence substrate | `crank/nano.py` — semantically agnostic transition typechecker + in-process append-only journal |
| Current completed intervention assay | `PCE-001`: protected corrective exposure |
| Current evidence boundary | **L1: challenge preservation given `D_t^oracle`** |
| Next open rung | **L2: diagnose that `D_t^agent` is insufficient** |
| Architecture status | No Nano V1, challenge generator, meta-exploration module, or corrigibility primitive earned |
| Formal K0/E001 status | E001 remains separate and unexecuted by the crank lineage |

## Mechanistic core

The current causal analysis frame is:

```text
E_t
-> Pi_t
-> pi_t
-> A_t
-> O_{t+1}
-> W_{t+1}
-> E_{t+1}
```

with external world state `X_t` entering the observation channel:

```text
O_{t+1} = g(X_t, A_t, epsilon_{t+1})
```

where:

- `E_t` — persistent epistemic state / accumulated leverage;
- `Pi_t` — effective representation or interface;
- `pi_t` — policy induced from that state;
- `A_t` — selected intervention/action;
- `O_{t+1}` — externally generated observation/consequence;
- `W_{t+1}` — warrant/recognition judgment;
- `E_{t+1}` — revised persistent state.

The load-bearing distinction is:

```text
exogenous outcome generation
!=
exogenous outcome exposure
```

Holding world state and intervention fixed, persistent state need not control what reality returns. But persistent state can still alter which interventions occur and therefore which observations become reachable.

The mechanism name used in the current lineage is:

```text
endogenous evidence acquisition
```

The property under pressure is:

```text
non-collapsible corrective exposure
```

Compactly:

> **External truth can remain independent while exposure to it becomes endogenous.**

## Six-gate correction chain

OpenCore now separates the path to correction into:

```text
C1  physical availability
C2  policy support
C3  actual selection
C4  discrimination
C5  recognition
C6  authority revision
```

`C4` has an important internal split:

```text
C4a  the environment produces different consequences under live alternatives
C4b  the current representation preserves that difference
```

A physically existing probe (`C1=1`) therefore says almost nothing by itself about corrigibility.

The current lineage pressures different gates:

```text
OQ / FOREIGN-003        representation / identity aliasing around C4b
FOREIGN-004             safe quotient control
FOREIGN-005/006         informational reopenability
FOREIGN-007             C2/C3 policy foreclosure
BLITZCRANK-001/002      learned C2/C3 contraction and temporal reopening
PCE-001                 direct intervention on the exposure edge
Mini role attacks       C5 recognition / epistemic-role assignment
Nano / Base             C6 persistent authority revision
```

## Discriminating intervention sets

For live alternatives `h_i, h_j`, distinguish:

```text
D_t^X
    physically discriminating interventions

D_t^Pi
    interventions whose discrimination survives the current representation
```

with, for an information-losing deterministic representation:

```text
D_t^Pi subseteq D_t^X
```

This separates two wounds:

```text
representational foreclosure:
D_t^X != empty
D_t^Pi = empty

policy foreclosure:
D_t^Pi != empty
D_t^Pi intersect support(pi_t) = empty
```

## Experimental progression

The current pressure sequence is:

| Assay | Scoped result |
| --- | --- |
| [FOREIGN-003](crank/FOREIGN_003.md) | Future-relevant quotient collapse can create wrong cross-history authority inheritance. |
| [FOREIGN-004](crank/FOREIGN_004.md) | Historical difference alone does not require separate persistence identity when the frozen future-consequence surface is equivalent. |
| [FOREIGN-005](crank/FOREIGN_005.md) | Safe effective compression is not identical to irreversible destruction; later distinctions can be reconstructed from retained substrate. |
| [FOREIGN-006](crank/FOREIGN_006.md) | On one bounded binary-linear family, exact blind reopenability compressed from 64 raw bits to 6 independent future-distinguishing dimensions. |
| [FOREIGN-007](crank/FOREIGN_007.md) | A safe-now quotient can change policy support so a later corrective experiment remains physically available but is not selected. |
| [BLITZCRANK-001](crank/BLITZCRANK_001.md) | Ordinary persistent learning can improve performance while suppressing an informative action from policy support. |
| [BLITZCRANK-002](crank/BLITZCRANK_002.md) | Reopening is temporally structured: first support return is not sustained exposure, and recovery can be slow. |
| [PCE-001](crank/PCE_001.md) | Directly intervening on corrective exposure changed correction dynamics in the prospectively predicted direction. |

The empirical transition is now:

```text
constructed foreclosure
-> learned foreclosure
-> temporal reopening
-> direct exposure-edge intervention
```

## PCE-001 — current intervention boundary

PCE-001 prospectively froze a challenge set supplied by the harness:

```text
D_t^oracle = D_t^Pi
```

and manipulated only challenge selection.

Primary contrast:

```text
ARM_ENDOGENOUS x WORLD_CORRECTIVE
vs
ARM_HAZARD x WORLD_CORRECTIVE
```

Frozen result:

```text
ENDOGENOUS finite T_C:   0 / 256
HAZARD finite T_C:     195 / 256 = 76.171875%

hazard faster: 195 / 256
tie:            61 / 256
hazard slower:    0 / 256
```

Secondary contrast:

```text
ARM_SUPPORT x WORLD_CORRECTIVE
vs
ARM_FLOOR x WORLD_CORRECTIVE
```

Frozen result:

```text
SUPPORT finite T_C:  64 / 256 = 25.000000%
FLOOR finite T_C:   205 / 256 = 80.078125%
```

Thus, on the frozen family:

```text
nonzero support
!=
timely corrective exposure
```

Matched `WORLD_NULL`, `WORLD_INFORMATIVE`, and `WORLD_CORRECTIVE` controls preserve the distinction:

```text
informative
!=
corrective
!=
authority-changing
```

The full result, custody hashes, claim ceiling, and trace commitment are in [PCE_001.md](crank/PCE_001.md) and `crank/results/`.

## Current evidence ladder

The next frontier is deliberately separated into three capabilities:

```text
L1  challenge preservation given D_t^oracle
L2  diagnosis that D_t^agent is insufficient
L3  construction of a better challenge set
```

PCE-001 supports **L1 only under an oracle-supplied challenge set**.

It does not test:

```text
D_t^agent =? D_t^oracle
```

A system may perfectly preserve the challenge set it knows while still preserving the wrong challenge set.

The next open scientific question is therefore:

> **Can an adaptive system detect that its current corrective-exposure topology is inadequate without being told which missing intervention would repair it?**

No L2 mechanism is currently implemented or pre-authorized.

## Reopenability layers

The current program distinguishes:

```text
informational reopenability
    Can the distinction still be reconstructed?

topological reopenability
    Can the system still reach the intervention that reconstructs it?

authority reopenability
    Can the resulting distinction still reduce or revise persistent authority?
```

PCE-001 adds an empirical temporal refinement to the middle layer:

```text
path exists
!=
path has support
!=
path receives sufficient exposure
!=
correction arrives before stale leverage matters
```

This motivates two clocks without collapsing them into a scalar corrigibility score:

```text
T_C  correction latency
T_L  latency until stale persistent leverage becomes consequential
```

A system can be eventually reopenable while remaining practically non-corrective when `T_C >> T_L`.

## Nano boundary

[Nano](crank/nano.py) remains deliberately narrow:

```text
transition typechecker + append-only in-process journal
```

It constrains persistent effects under externally supplied contracts. It does not establish:

- truth;
- correctness of a license;
- adequacy of a representation;
- which experiment should run;
- which distinction is missing;
- whether a challenge set is sufficient;
- whether a corrective path remains policy-reachable.

Therefore:

```text
Nano protects authority acquisition
!=
Nano guarantees evidence exposure
```

PCE-001 changes no Nano code and earns no Nano V1.

## Living synthesis records

- [QUOTIENT_PRESSURE_LINEAGE.md](crank/QUOTIENT_PRESSURE_LINEAGE.md) — quotient pressure through FOREIGN-004.
- [REOPENABILITY_LINEAGE.md](crank/REOPENABILITY_LINEAGE.md) — FOREIGN-005/006 informational reopenability and capacity record.
- [TOPOLOGICAL_REOPENABILITY_LINEAGE.md](crank/TOPOLOGICAL_REOPENABILITY_LINEAGE.md) — FOREIGN-007 through the learned-policy bridge.
- [CORRECTIVE_EXPOSURE_LINEAGE.md](crank/CORRECTIVE_EXPOSURE_LINEAGE.md) — Blitzcrank → PCE-001 causal intervention synthesis and L1/L2/L3 boundary.

Frozen assay/spec/result artifacts remain authoritative over living summaries.

## Historical K0 artifacts

The following are historical prospective freezes and intentionally remain unchanged:

- [CHARTER.md](CHARTER.md)
- [KERNEL_CONTRACT.md](KERNEL_CONTRACT.md)
- [EXPERIMENT_001.md](EXPERIMENT_001.md)

They describe the pre-code K0/E001 state because that was the state at freeze time. Crank execution does not complete or amend E001.

## Claim ceiling

The repository does **not** establish:

- a universal corrigibility law;
- a universal learner or theory of intelligence;
- that every informative action should remain supported;
- that exploration is universally beneficial;
- a scalar corrigibility metric;
- a universal memory-capacity/rank theorem;
- autonomous challenge-set diagnosis;
- autonomous challenge constitution;
- automatic interface invention or repair;
- correctness of externally constituted licenses or challenge sets;
- Nano V1 or a production authority ledger;
- a complete cognitive architecture.

## Research rule

The governing methodological rule remains:

> **No new semantic primitive without a frozen counterexample, an unrepresentability argument, or a discriminating witness.**

And after PCE-001, the stopping discipline is explicit:

```text
failed prospective prediction
-> mechanism loses authority

successful intervention
-> mechanism gains bounded authority only on the identified dimensions
```

The current OpenCore question is:

> **How can persistent epistemic state gain useful causal leverage over behavior without gaining enough leverage over evidence acquisition to suppress, delay, or extinguish the exposure required to reduce that leverage?**

The next conceptual update should come from a frozen L2 discrimination, not from pre-solving L2 architecturally.
