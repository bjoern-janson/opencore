# OpenCore Research Freeze — Failure Attribution Frontier

**Status:** `RESEARCH_FREEZE`  
**Scope:** living synthesis only; frozen assay/spec/target/runner/result artifacts remain unchanged  
**OpenCore-native causal result:** PCE-001 at externally constituted challenge scope  
**Current attribution frontier:** open  
**New OpenCore mechanism:** none  
**New primitive:** none  
**New architecture:** none

## 1. Canonical compact model

The current OpenCore synthesis is:

```text
1. Preserve alternatives before authority.
2. Preserve causal boundaries before attribution.
3. Preserve independent, discriminating routes by which evidence can overturn confidence.
```

The unresolved operator is:

```text
observed failure
-> identifying evidence
-> failure attribution
-> method reliance
```

The active question is:

> **When memory changes what a learner gets to observe, can it distinguish “my current answer is failing” from “my way of learning is failing”?**

Equivalent local question:

> **Given a bad outcome, does the available evidence warrant blaming the current answer or the procedure that produced it?**

No broader theory is required to state the frontier.

## 2. Three witness roles

The current witnesses have different jobs:

```text
AF3-OC   preserve the candidate/evidence surface
PCE-001  demonstrate that persistent state can constrict exposure
MAB-OS   provide native method reliance that can potentially respond
```

These roles must not be collapsed.

### AF3-OC

Foreign case-study lesson:

```text
candidate exposure
!=
candidate validation
!=
method validity
```

Its useful architectural distinctions include:

```text
requested input
!=
effective inference input

internal confidence
!=
external authority

hypothesis diversity
!=
epistemic independence
```

AF3-OC does not answer the attribution question. It shows why causal-stage separation and alternative preservation are prerequisites for asking it responsibly.

### PCE-001

Frozen OpenCore result:

> Within the tested constructed family, persistent learned state can causally reduce exposure to a prospectively identified corrective channel, and exogenizing or quantitatively protecting that exposure can materially reduce correction latency.

PCE-001 establishes exposure coupling at externally constituted challenge scope. It does not establish autonomous diagnosis.

### MAB-OS

MAB-OS is a foreign adaptive supervisor in which method allocation is already native. It therefore provides a substrate for testing attribution without adding a trust variable.

Pinned source identity used for the audit:

```text
repository  BaratiLab/MAB-OS
commit      f38df7e85d588969005e2f59f2366dfe6a5a9861
file        MABOS/MABOS.py
blob        851d6cc7e5e3fafbca381ccf0b0734659cc840ef
native K    50
```

Its public implementation has `ratio = 1`, so the active method's `Q_i` is effectively overwritten by the latest credited reward rather than maintained as a long-horizon calibrated method-health estimate.

Therefore the clean behavioral observable is:

```text
R_t = actual native allocation of control among HHO / DE / WOA
```

not a synthetic trust state.

## 3. Historical OpenCore-native attribution boundary

CSD-001 prospectively separated adequate-method failure from inadequate-method failure, but unchanged Mini produced:

```text
FAILURE_CAUSE_CONFLATION
```

The decisive lesson was:

```text
local unresolvedness
!=
procedure inadequacy
```

and:

```text
R3 measurability
!=
semantic sufficiency for procedure diagnosis
```

Post-negative archaeology found:

```text
NO_ADMISSIBLE_PRE_CSD_L2_TARGET_FOUND
```

within the audited pre-CSD repository surface.

This remains a scoped negative, not an impossibility theorem.

## 4. MAB-OS source and world gates

The foreign audit progressed through distinct gates:

```text
SOURCE_ADMISSIBLE
-> WORLD_INTERFACE_ADMISSIBLE
-> NATIVE_WORLD_PAIR
-> DIAGNOSTIC_WORLD_PAIR
-> selector assay
```

The first two gates passed.

The initial world pair then exposed a temporal-definition error:

```text
SHORT_HORIZON_PAIR_CERTIFIED
!=
NATIVE_SELECTOR_PAIR_CERTIFIED
```

A 12-step WOA degradation did not survive the native `K=50` method-credit interval.

Earned validity rule:

> **Method adequacy must be evaluated on the same temporal unit that generates native method credit.**

This was a gate failure, not a selector result.

## 5. Native `K=50` world pair

A revised optimizer-blind pair was selected and evaluated using forced valid continuations only. Native selector allocation, `Q_t`, and selector choices were sealed during construction/certification.

Mechanism-level held-out result, 128 seeds:

```text
exact common prefix match:                  128 / 128

median Delta_WOA,F2^50:                       4.579
median Delta_WOA,F3^50:                       1.020
median Delta_DE,F3^50:                        4.986

P(Delta_WOA,F2^50 > Delta_WOA,F3^50):         91.4%
P(Delta_DE,F3^50  > Delta_WOA,F3^50):         96.9%
```

This earned, at the current mechanism-level execution provenance:

```text
NATIVE_WORLD_PAIR
```

meaning:

```text
F2  WOA remains effective at native K=50
F3  WOA is degraded at native K=50
F3  DE remains effective
```

The objective remained optimizer-blind and the inherited state / pre-diagnostic history was exactly matched.

## 6. The ironic `2 x 2` exposure assay — negative

The frozen intervention was:

```text
D = do(A_t = DE)
```

for exactly one native `K=50` block.

Inside that block, DE's native proposals, objective evaluations, reward calculation, `Q_DE` update, population effects, and subsequent native selection were left untouched. The intervention changed only which method received control for that block.

Cells:

```text
F2^E
F2^D
F3^E
F3^D
```

Primary endpoint:

```text
R_WOA = WOA allocation over the next four complete native blocks
```

Primary interaction:

```text
I =
  (R_WOA(F3^D) - R_WOA(F3^E))
-
  (R_WOA(F2^D) - R_WOA(F2^E))
```

Prospective support required:

```text
I < 0
with paired bootstrap 95% CI entirely below zero
```

Mechanism-level result, 128 fresh assay seeds:

```text
mean R_WOA(F2^E): 0.3086
mean R_WOA(F2^D): 0.2871
mean R_WOA(F3^E): 0.3086
mean R_WOA(F3^D): 0.2949

Delta_D^F2:      -0.0215
Delta_D^F3:      -0.0137

I:               +0.0078125
95% CI:          [-0.0488, 0.0645]
```

Classification:

```text
NO_SELECTIVE_EXPOSURE_EFFECT
```

The primary criterion failed.

## 7. Failure localization

The negative does not establish that MAB-OS cannot reassess methods.

The shallowest failure is the intervention evidence itself.

Secondary forced-continuation check on the same assay states:

```text
median Delta_DE,F2^50: ~4.991
median Delta_DE,F3^50: ~4.991
```

So the forced DE block produced approximately the same excellent learner-visible evidence in both worlds.

The native bandit therefore had no reason to infer `F2` versus `F3` from that intervention alone.

Earned distinctions:

```text
useful intervention
!=
diagnostic intervention
```

and:

```text
counterfactually discriminating
!=
observationally discriminating
```

The first-principles result is:

> **You can restore an evidence channel without restoring identifiability.**

Therefore:

```text
evidence availability
!=
diagnostic information
!=
warranted attribution
```

## 8. Current diagnostic gate

The next world-pair gate has exactly three requirements:

```text
G1  the causal hypotheses really differ

G2  the proposed intervention produces learner-visible evidence
    that distinguishes those hypotheses

G3  the required alternative remains viable
```

For the current intervention proposal:

```text
D = do(A = DE)
```

define:

```text
Y_D = the native evidence generated by the forced DE block
```

with no harness-side interpretation and no hidden `F2/F3` label.

The required condition is:

```text
P(Y_D | do(D), H, F2)
!=
P(Y_D | do(D), H, F3)
```

under the frozen native `K=50` semantics.

A harness-side relative metric that requires observing the unselected method is not sufficient. The evidence actually delivered to MAB-OS must identify the live hypotheses.

Current gate status:

```text
NATIVE_WORLD_PAIR      earned at mechanism-level provenance
DIAGNOSTIC_WORLD_PAIR  NOT EARNED
```

No new `2 x 2` selector assay is authorized until `G1-G3` pass prospectively on independent held-out seeds.

## 9. Execution provenance ceiling

The MAB-OS numerical work recorded above used a source-conformant transcription of the frozen public implementation and source-checked optimizer/selector semantics.

It was **not** a byte-imported authenticated execution of the frozen stock module.

Therefore:

```text
source-faithful / mechanism-level execution evidence
!=
final authenticated stock-module execution evidence
```

The current numbers may guide the next discriminating gate, but any final MAB-OS empirical claim should be rerun against the exact frozen stock module with authenticated execution provenance.

## 10. Current OpenCore boundary

The conceptual center is now deliberately small:

```text
bad result
!=
bad method
```

and:

```text
observed failure
-> identifying evidence
-> failure attribution
-> method reliance
```

The strongest current OpenCore-specific question remains:

> **When memory changes what a learner gets to observe, can it distinguish “my current answer is failing” from “my way of learning is failing”?**

Current status:

```text
PCE-001                   exposure effect causally supported at oracle scope
CSD-001 Mini              FAILURE_CAUSE_CONFLATION
MAB-OS native pair        mechanism-level earned
MAB-OS diagnostic pair    open
MAB-OS 2x2                negative; intervention evidence non-identifying
L3 / better-method invention  untouched
```

## 11. Claim ceiling

The current evidence does **not** establish:

```text
P_L^cause
autonomous failure attribution
autonomous challenge discovery
autonomous challenge constitution
universal exploration requirements
universal method-selection corrigibility
a new trust state
a procedure-failure primitive
an outer selector
Nano V1
a production architecture
```

No new OpenCore mechanism follows from the foreign negative.

## 12. Research rule

The operative rules are:

```text
change the world, not the learner
```

and:

> **Evidence must be bound to the causal object whose authority it is being used to support.**

and now, more specifically:

> **A diagnostic intervention must make the competing hypotheses distinguishable through the evidence it actually delivers to the system.**

The next legitimate operation is only to construct and prospectively certify a `DIAGNOSTIC_WORLD_PAIR`.

## 13. Authoritative frozen records

Frozen OpenCore experimental records remain authoritative over this living synthesis, including:

- `PCE_001_SPEC.md`, `PCE_001_MANIFEST.json`, `pce_001.py`, `PCE_001.md`
- `CSD_001_SPEC.md`, `CSD_001_MANIFEST.json`, `CSD_001_ANALYSIS.md`, `csd_001.py`, `CSD_001.md`
- `CSD_001_TARGET_SELECTION.md`
- `CSD_001_TARGET_SPEC.md`
- `csd_001_target_mini.py`
- `CSD_001_PROCEDURE_ADEQUACY_ARCHAEOLOGY.md`
- committed result and trace commitments under `crank/results/`

This file is a living research boundary. It does not rewrite any frozen assay or result.
