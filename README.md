# OpenCore

> Experimental substrate for **bounded epistemic compounding**: durable capability without self-erasure of the causal paths required for correction.

OpenCore studies how externally grounded consequence can become persistent, reusable, and revisable adaptive structure without allowing persistence to become self-protecting authority.

This branch is the active experimental lineage. The original K0 charter and kernel contract remain frozen historical artifacts and intentionally still describe the pre-code state from which the program began.

| Field | Current status |
| --- | --- |
| Research object | Inspectable persistence / correction membrane for adaptive systems |
| Phase | Empirical pressure-testing across constructed and foreign domains |
| Trusted core | `crank/nano.py` — semantically agnostic transition typechecker + append-only journal |
| Current experimental boundary | `FOREIGN-007`: `EPISTEMIC_FORECLOSURE_ESTABLISHED` |
| Current systems hypothesis | Capability may compound only safely if sufficient corrective topology remains live |
| Architecture status | No Nano V1, scheduler, reachability primitive, or new semantic primitive earned |
| External systems | AVO is pinned as a **foreign organism specimen**, not a foreign assay or evidence for OpenCore |

## Current research question

```text
Can useful capability compound while preserving sufficient corrective topology
for accumulated capability to remain externally corrigible?
```

Compactly:

```text
Can capability compound without consuming its own corrigibility?
```

The current analysis frame is the causal loop:

```text
L_t
-> Pi_t
-> pi_t
-> R_t
-> E_{t+1}
-> Delta A_{t+1}
```

where, provisionally:

- `L_t` — persistent / retained state;
- `Pi_t` — current effective representation or partition;
- `pi_t` — policy induced from that effective state;
- `R_t` — reachable interventions / observations under that policy;
- `E_{t+1}` — external consequence;
- `Delta A_{t+1}` — resulting change in persistent authority.

This tuple is an analysis frame, not an implemented cognitive architecture.

## The current boundary

The strongest systems-level invariant candidate is:

> **Persistent state may gain causal leverage over future behavior, but must not thereby eliminate all live routes by which external consequence can reduce that leverage.**

This remains a hypothesis, not a theorem.

A crucial architectural separation is now explicit:

```text
Nano protects authority acquisition
!=
Nano guarantees evidence reachability
```

A perfect final authority gate cannot repair an upstream system that never reaches the correcting observation.

## Experimental ladder

The foreign-pressure sequence now reads:

| Assay | Result | What it established on its frozen family |
| --- | --- | --- |
| [FOREIGN-001](crank/FOREIGN_001_MASTERMIND.md) | representation insufficiency | Search inside the current representation is not the same as discovering a better representation. |
| [FOREIGN-002](crank/FOREIGN_002_RESTLESS_BANDIT.md) | reactive vs prospective attention split | Reactive correction after contradiction is not prospective discovery before contradiction. |
| [FOREIGN-003](crank/FOREIGN_003.md) | `CLASSICAL_REPRODUCTION_ESTABLISHED` | A future-relevant distinction collapsed into one persistence identity can produce wrong cross-history authority inheritance. |
| [FOREIGN-004](crank/FOREIGN_004.md) | `SAFE_QUOTIENT_ESTABLISHED` | Some genuinely different histories can be safely quotiented when they are equivalent over the frozen future-consequence surface. |
| [FOREIGN-005](crank/FOREIGN_005.md) | `REOPENABLE_QUOTIENT_ESTABLISHED` | Safe effective forgetting is not identical to irreversible information destruction. |
| [FOREIGN-006](crank/FOREIGN_006.md) | `DISTINGUISHING_RANK_BOUNDARY_ESTABLISHED` | On one bounded binary linear family, exact blind reopenability compressed from 64 raw bits to the 6 independent future-distinguishing dimensions. |
| [FOREIGN-007](crank/FOREIGN_007.md) | `EPISTEMIC_FORECLOSURE_ESTABLISHED` | A safe-now quotient changed later policy support so that a physically available corrective experiment was no longer selected. |

The 003→007 sequence therefore separates:

```text
unsafe quotient
safe quotient
informational reopenability
compressed blind reopenability
topological foreclosure
```

For exact provenance, claim ceilings, execution repairs, hashes, and controls, read the individual frozen records rather than this summary.

## Three reopenability layers

The current program distinguishes three questions:

```text
informational reopenability
    Can the distinction still be reconstructed?

topological reopenability
    Can the system still reach the experiment that reconstructs it?

authority reopenability
    Can the resulting distinction still alter persistent authority?
```

`FOREIGN-005/006` pressure the first. `FOREIGN-007` pressures the second. Nano sits at the gate for the third.

This decomposition is useful precisely because the three can fail independently.

## Nano

[Nano](crank/nano.py) is intentionally boring.

It is a transition typechecker plus append-only journal whose trusted surface sees typed standings, exact preconditions, effect grants, preservation obligations, and license state. Payload semantics remain opaque.

Frozen Nano SHA-256 across the recent quotient / reopenability / foreclosure assays:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Git blob on this branch:

```text
d31dacaf893a58a8280c01704fe666a404c1f56c
```

Nano does not know whether a claim is true, whether an interface is sufficient, which probe should be selected, whether a world model is good, or whether a corrective path exists. Those are upstream empirical questions.

## Parallel pressure lines

The repository also retains complementary pressure surfaces:

- [Base — shared authority-filtered world](crank/BASE_001_SHARED_WORLD.md)
- [Base — global reopening pressure](crank/BASE_002_GLOBAL_REOPENING.md)
- [AF3-OC-001](crank/AF3_OC_001.md) — a narrow membrane test over real immutable AlphaFold 3 output objects
- OpenCore Quantum assays in `crank/` — apparatus identity / persistence pressure preceding the classical FOREIGN-003 reproduction

These lines are not collapsed into the FOREIGN ladder; they supply separate attribution and transfer pressure.

## Reopenability lineage records

- [REOPENABILITY_LINEAGE.md](crank/REOPENABILITY_LINEAGE.md) preserves the detailed FOREIGN-005 / FOREIGN-006 transport, hash, and capacity record.
- [TOPOLOGICAL_REOPENABILITY_LINEAGE.md](crank/TOPOLOGICAL_REOPENABILITY_LINEAGE.md) records the FOREIGN-007 transition from retained information to retained corrective paths and the current stopping boundary.

## Historical K0 artifacts

The following documents are historical prospective freezes and are intentionally **not rewritten to match current status**:

- [CHARTER.md](CHARTER.md)
- [KERNEL_CONTRACT.md](KERNEL_CONTRACT.md)
- [EXPERIMENT_001.md](EXPERIMENT_001.md)

They say “implementation none / results none” because that was true at the K0 freeze. Their historical wording is part of the lineage. The current branch status is this README plus the descendant assay records.

The governing methodological rule remains:

> **No new semantic primitive without a frozen counterexample, an unrepresentability argument, or a discriminating witness.**

And, operationally:

```text
when the abstraction gets beautiful, crank the abstraction
```

rather than building architecture from elegance alone.

## External specimen: NVIDIA AVO

NVIDIA's Agentic Variation Operators (AVO) is currently tracked only as a **foreign organism specimen**. NVIDIA describes a long-horizon agent system in which persistent memory, tools, feedback, supervision, recovery, and iterative search allow useful state to compound across extended work and across distinct task interfaces.

Source:

- [NVIDIA AVO on ARC-AGI-3](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/)

The public result does **not** isolate memory's contribution and does not establish an OpenCore claim. The relevant future foreign-pressure question is narrower:

```text
Does persistent state that improves long-horizon performance also change
which genuinely corrective interventions remain policy-reachable?
```

Until a real system exposes enough of:

```text
L_t -> pi_t -> R_t
```

to support controlled intervention / forced-path tests, AVO remains:

```text
foreign organism specimen
!=
foreign assay
```

## Claim ceiling

The current repository does **not** establish:

- a universal learner or general theory of intelligence;
- a universal corrigibility invariant;
- that every diagnostic action must remain reachable;
- a general law equating memory capacity with linear rank;
- that explicit world models are necessary or unnecessary;
- that AVO validates OpenCore;
- an exploration, curiosity, supervisor, reachability, or reopening primitive;
- automatic interface invention, quotient repair, or challenge discovery;
- Nano V1 or any Nano modification;
- a complete cognitive architecture.

## Current stop rule

No architecture expansion is currently earned.

The next move must come from an actual pressure surface that exposes enough of the persistent-state → policy → reachability coupling to test whether capability gains coincide with loss of corrective access.

Until then, the research target is frozen as:

> **Bounded epistemic compounding: allow useful state to acquire durable causal leverage while preserving live routes by which external consequence can reduce that leverage.**
