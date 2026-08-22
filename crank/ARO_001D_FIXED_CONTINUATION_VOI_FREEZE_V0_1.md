# ARO-001d — Fixed-Continuation VOI Freeze v0.1

**Status:** `PROSPECTIVE_IMPLEMENTATION_FREEZE / NOT_RUN`  
**Canonical execution flag:** `STATUS = NOT_RUN`  
**Parent scientific freeze:** `ARO_001_ADAPTIVE_REPRESENTATION_OPERATIONS.md`  
**Parent result:** `ARO_001C_V0_1_RESULT.md`  
**Variant:** `ARO-A`  
**Representation invention:** no  
**Operation invention:** no  
**T13 reopened:** no

ARO-001c produced perfect descriptive rank ordering between evaluator-defined probe value and both learned first-stage Q-gap and greedy probe preference, but it failed its continuation-competence isolation gate. The q manipulation changed both upstream probe value and downstream continuation-learning difficulty.

ARO-001d makes one causal intervention:

\[
\boxed{
\mathrm{PROBE}_S
\rightarrow
\text{evaluator-fixed optimal continuation}
}
\]

while leaving first-stage value learning endogenous.

The assay asks:

\[
\boxed{
\textbf{Can learned first-stage acquisition value track true downstream value of information
when continuation competence is fixed by construction?}
}
\]

---

## 1. Invariants inherited from ARO-001c

The following remain unchanged:

```text
q grid = {0.60, 0.70, 0.75, 0.80, 0.85, 0.90}
world definitions and latent law
representation family
first-stage operation family and costs
Bayes predictor and tie rule
ARO-A information timing
training objective J = loss + 0.15 * cost
256 seeds per q condition
4000 training episodes per seed
uniform four-context distribution
Q initialization = 0
first-stage learning rate alpha_Q = 0.10
discount gamma = 1.0
epsilon start = 0.20
epsilon end = 0.01
linear epsilon schedule
forced PROBE_S exposure = 0.25 conditional on W3_VALUE training episodes
greedy unforced evaluation
matched empty-information loss gate = 0.5
claim ceilings
```

The six prospectively frozen true probe values remain:

```text
q       DeltaV_true
0.60    -0.100
0.70    -0.050
0.75    -0.025
0.80     0.000
0.85     0.025
0.90     0.045
```

---

## 2. Single intervention: fixed continuation

Whenever the first-stage action is `PROBE_S` in `W3_VALUE`, the evaluator supplies the continuation:

```text
S = 0  -> SELECT_G
S = 1  -> SELECT_I
```

with probability `1.0`.

No second-stage Q table exists in ARO-001d. No second-stage action is learned, explored, or selected.

The first-stage Q value of `PROBE_S` is still learned from the realized terminal return after the evaluator-fixed continuation. Therefore the intervention removes continuation-learning variance without directly assigning a probe value.

This freezes the intended causal structure:

\[
\boxed{
\text{fixed continuation}
+
\text{vary true }\Delta V_{\rm probe}
\rightarrow
\text{learn first-stage acquisition value}.
}
\]

---

## 3. Why the first-stage action family is not reduced to two actions

ARO-001d preserves the ARO-001c first-stage family:

```text
SELECT_G
SELECT_I
COMPOSE_GI
COMPOSE_GIS
PROBE_S
```

because the scientific quantity is value relative to the **best available non-probe alternative**.

Restricting the controller to `{PROBE_S, COMPOSE_GIS}` would change the comparator and destroy the frozen sign-changing true-VOI curve.

Thus:

\[
\boxed{
\Delta V_{\rm true}
=
J^*_{\rm best\ nonprobe}
-
J^*_{\rm probe,fixed\ continuation}
}
\]

and the learned readout is defined on the reward/Q scale as

\[
\boxed{
\widehat{\Delta V}_{\mu_1}
=
Q_1(\mathrm{PROBE}_S)
-
\max_{a\neq\mathrm{PROBE}_S}Q_1(a).
}
\]

Positive values mean the learned controller values probing above every supplied non-probe alternative.

---

## 4. Primary scientific objects

For each q condition, report:

```text
true_DeltaV
mean learned_DeltaV_hat across seeds
sd / quantiles of learned_DeltaV_hat
greedy PROBE_S preference seed rate
best non-probe action under the evaluator oracle
```

The primary mechanism-level comparison is

\[
\boxed{
\Delta V_{\rm true}
\quad\text{vs}\quad
\widehat{\Delta V}_{\mu_1}.
}
\]

Greedy probe behavior is retained as a secondary thresholded readout only. Because evaluation is greedy, it is not an independently identified policy-conversion layer.

---

## 5. Frozen curve statistics

Across the six q conditions, fit the OLS relation

\[
\boxed{
\mathbb E[\widehat{\Delta V}_{\mu_1}\mid q]
=
a\,\Delta V_{\rm true}(q)+b.
}
\]

Report:

```text
Spearman rho_Q
OLS slope a
OLS intercept b
R^2
inferred zero crossing z = -b/a, when a != 0
```

The rank-ordering test and economic calibration test remain separate.

---

## 6. Frozen positive criteria

### Structural / provenance gates

```text
G0 fixed continuation used with probability 1 after every W3_VALUE probe
G1 true DeltaV vector matches the prospective freeze exactly
G2 empty-information Bayes loss = 0.5 for every q
```

### Primary value-learning criteria

A clean first-stage VOI-calibration result requires all of:

```text
V1 rho_Q >= 0.90
V2 OLS slope a in [0.75, 1.25]
V3 |OLS intercept b| <= 0.020
V4 |inferred zero crossing z| <= 0.020
V5 mean learned DeltaV_hat < 0 for q in {0.60,0.70,0.75}
V6 mean learned DeltaV_hat > 0 for q in {0.85,0.90}
```

The exact-zero condition `q=0.80` is reported separately and is not required to have exactly zero finite-sample mean.

`PRIMARY_VOI_CALIBRATION_PASS = G0 & G1 & G2 & V1 & ... & V6`.

### Secondary behavioral calibration

Report but do not use to identify a separate policy mechanism:

```text
B1 negative-VOI q conditions have greedy probe rate < 0.50
B2 positive-VOI q conditions have greedy probe rate > 0.50
B3 q=0.80 probe rate lies in [0.20,0.80]
```

---

## 7. Diagnostic interpretation

Interpret only at the shallowest earned level.

```text
G0/G1/G2 fail
-> implementation / world-construction / execution failure; no VOI interpretation

rho_Q fails
-> no evidence that learned first-stage value preserves true VOI ordering

rho_Q passes but slope/intercept/zero-crossing fail
-> ordinal sensitivity without economic calibration

primary calibration passes
-> evidence that this frozen tabular first-stage learner tracks evaluator-defined
   downstream information value when continuation is fixed by construction
```

Because greedy action choice is a deterministic thresholding of first-stage Q values, ARO-001d cannot separately identify a value-to-policy conversion mechanism.

---

## 8. Claim ceiling

A positive ARO-001d result may support only:

```text
in this frozen finite supplied-operation assay, the learned first-stage acquisition
value tracks evaluator-defined downstream value of information when continuation
competence is fixed by construction.
```

It does **not** establish:

```text
general-purpose VOI estimation
representation understanding
representation invention
operation invention
causal diagnosis
ARO-B preparedness
safe authority transfer
T13 success or necessity
```

---

## 9. Execution constitution

Before execution, freeze:

```text
q grid
true DeltaV vector
all inherited ARO-001c constants
fixed continuation rule
first-stage action family
forced probe exposure rate
learned DeltaV_hat definition
curve statistics
all thresholds above
256 seeds per q
4000 episodes per seed
repository-native workflow
```

The executable and workflow must be committed before result inspection.

Any post-result change creates a new version and cannot be reported as ARO-001d v0.1.
