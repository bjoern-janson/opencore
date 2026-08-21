# MAB-OS Foreign Case — Diagnostic Exposure and Failure Attribution

**Status:** living foreign-case record  
**OpenCore code changes:** none  
**MAB-OS learner changes:** none in the source/world audits; the `2 x 2` intervention changes only one method-allocation edge for one native block  
**Execution provenance:** mechanism-level source-conformant transcription, not final authenticated stock-module execution  
**Current gate:** `DIAGNOSTIC_WORLD_PAIR` not earned

## 1. Why MAB-OS

The current OpenCore attribution question needs an existing system where method reliance is already behaviorally real.

MAB-OS provides:

```text
choose optimizer
-> apply optimizer
-> measure credited improvement
-> update native Q_i
-> allocate future control
```

Pinned source:

```text
repository  BaratiLab/MAB-OS
commit      f38df7e85d588969005e2f59f2366dfe6a5a9861
file        MABOS/MABOS.py
blob        851d6cc7e5e3fafbca381ccf0b0734659cc840ef
methods     HHO / DE / WOA
K           50
ratio       1
```

Because `ratio = 1`, the implementation effectively uses:

```text
Q_i <- latest credited reward for method i
```

rather than a stable long-horizon method-health estimate.

Therefore the clean dependent variable is:

```text
R_t = actual native method allocation
```

not an invented trust variable.

## 2. Source admissibility

The source audit established:

```text
SOURCE_ADMISSIBLE
```

because:

```text
1. selector can remain unchanged
2. native method allocation is directly observable
3. objective/problem enters through ordinary objective evaluations
4. the objective need not receive a hidden method-failure label
5. native credited improvement is distinct from absolute current solution quality
```

Important ceiling:

```text
method-attributed task progress
!=
independent diagnosis of method failure
```

## 3. World-interface admissibility

The world can change the relationship between future candidate proposals and objective consequence without changing optimizer identity or interface.

The admissible construction keeps:

```text
same inherited population
same global best
same RNG state
same selector state
same pre-diagnostic objective responses
```

and then changes only the optimizer-blind problem geometry away from the already observed population.

Therefore:

```text
WORLD_INTERFACE_ADMISSIBLE
```

was earned structurally.

## 4. First pair failure — wrong temporal object

An initial pair made WOA look degraded over a 12-step forced continuation.

Source-conformance then exposed the native temporal unit:

```text
K = 50
```

MAB-OS assigns block credit at that horizon.

At `K=50`, the initial ordering reversed; WOA in the supposed `F3` recovered strongly.

Earned distinction:

```text
SHORT_HORIZON_PAIR_CERTIFIED
!=
NATIVE_SELECTOR_PAIR_CERTIFIED
```

Validity rule:

> **Method adequacy must be evaluated on the same temporal unit that generates native method credit.**

No selector conclusion was drawn from the failed pair.

## 5. Native-horizon pair development

The pair search then used only forced valid continuations. Native selector outputs were sealed.

A first frozen `K=50` candidate failed one prospective criterion:

```text
WOA F2 median improvement: 4.772
WOA F3 median improvement: 3.016
DE  F3 median improvement: 4.999
```

The frozen WOA-F3 ceiling was `<= 2.5`, so that candidate was rejected and its held-out seeds were not reused for certification.

A second development round froze a narrower well geometry (`width = 0.28`) before a completely fresh holdout.

## 6. Native world-pair certification

Fresh held-out result, 128 seeds:

```text
exact F2/F3 common-prefix equality:              128 / 128

median Delta_WOA,F2^50:                            4.579
median Delta_WOA,F3^50:                            1.020
median Delta_DE,F3^50:                             4.986

P(Delta_WOA,F2^50 > Delta_WOA,F3^50):              91.4%
P(Delta_DE,F3^50  > Delta_WOA,F3^50):              96.9%
```

All frozen criteria passed.

Mechanism-level classification:

```text
NATIVE_WORLD_PAIR
```

The pair established:

```text
F2  WOA remains effective from the identical inherited state
F3  WOA is degraded from that state
F3  DE remains effective
```

The objective remained optimizer-blind.

## 7. Ironic exposure assay

The intended irony was:

> Temporarily take evidence selection away from the selector, then see whether the selector becomes better at selecting.

The intervention was:

```text
D = do(A_t = DE)
```

for exactly one native `K=50` block.

The action override did **not** directly alter:

```text
DE proposal kernel
objective function
DE reward
Q_DE update
counts after the native block update
population state
subsequent native selector logic
```

After the forced block, all subsequent method choices were native.

The four cells were:

```text
F2^E
F2^D
F3^E
F3^D
```

where `E` is fully endogenous allocation and `D` contains the one forced DE block.

## 8. Frozen endpoint

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

Prospective support criterion:

```text
I < 0
and
paired bootstrap 95% CI entirely below 0
```

The interaction, rather than raw forced-DE effect, controls for ordinary bandit learning caused by giving DE a real reward observation.

## 9. Negative result

Fresh assay result, 128 seeds:

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

Seedwise interaction:

```text
I_s < 0: 21.1%
I_s = 0: 56.25%
I_s > 0: 22.7%
```

Classification:

```text
NO_SELECTIVE_EXPOSURE_EFFECT
```

The preregistered target failed.

## 10. Failure localization

Secondary forced-continuation analysis found:

```text
median Delta_DE,F2^50: ~4.991
median Delta_DE,F3^50: ~4.991
```

Thus the forced DE block was highly useful in both worlds but approximately non-identifying.

The native selector was being shown:

```text
DE is good
```

in both `F2` and `F3`.

The experimenter knew that WOA differed across the worlds, but the forced DE observation itself did not reveal that fact.

Therefore:

```text
G1  focal-method adequacy differs       PASS
G2  intervention evidence identifies    FAIL
G3  alternative viable in F3            PASS
```

Shallowest failure locus:

```text
learner-visible intervention evidence non-identifying
```

## 11. First-principles result

The run earns:

> **You can restore an evidence channel without restoring identifiability.**

Hierarchy:

```text
availability
!=
diagnostic information
!=
warranted attribution
```

Further distinction:

```text
counterfactually discriminating
!=
observationally discriminating
```

A world can contain a real difference in WOA adequacy while:

```text
P(Y_DE | do(DE), H, F2)
≈
P(Y_DE | do(DE), H, F3)
```

If so, the selector cannot infer the world distinction from the DE intervention alone.

## 12. Diagnostic-world-pair gate

The next gate is:

```text
G1  the causal hypotheses differ

G2  the intervention's actual learner-visible evidence
    distinguishes the hypotheses

G3  the required alternative remains viable
```

For:

```text
D = do(A = DE)
```

define:

```text
Y_D = the native reward/evidence produced by the forced DE block
```

No harness-side interpretation is allowed.

No hidden world label is allowed.

No relative metric requiring an unobserved WOA counterfactual is sufficient.

Required prospective condition:

```text
P(Y_D | do(D), H, F2)
!=
P(Y_D | do(D), H, F3)
```

under the native `K=50` semantics.

Only after independent held-out certification of this condition may another selector assay be frozen.

## 13. Provenance ceiling

The numerical development/certification/assay work above was executed from a source-conformant transcription of the frozen public code and checked against the relevant source semantics.

It was not a byte-imported authenticated run of the exact stock module.

Therefore classify the current evidence as:

```text
MECHANISM_LEVEL
```

not:

```text
FINAL_AUTHENTICATED_STOCK_MODULE
```

A future final claim requires reproduction with authenticated stock-module execution.

## 14. OpenCore interpretation ceiling

This foreign negative does **not** establish:

```text
MAB-OS cannot diagnose method failure
P_L^cause is impossible
forced exploration is generally useless
DE is a diagnostic action
an outer selector is needed
a trust variable is needed
a new OpenCore primitive is needed
```

It establishes only that the tested exposure intervention failed because its delivered evidence did not identify the live causal hypotheses.

That is the boundary to preserve.
