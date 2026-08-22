# ARO-001d v0.1 — Fixed-Continuation VOI Result

**Status:** `RUN_COMPLETE / PRIMARY_VOI_CALIBRATION_FAILED`  
**Primary interpretation:** `FIRST_STAGE_ACQUISITION_VALUE_MISCALIBRATION`  
**Prospective freeze:** `ARO_001D_FIXED_CONTINUATION_VOI_FREEZE_V0_1.md`  
**Frozen executable:** `aro_001/run_001d_v0_1.py`  
**Freeze commit before execution:** `88c8702a69f471724b5780b46e01aed4da5d287b`  
**Repository-native workflow run:** `32575278744`  
**Seeds:** `256` per q condition  
**Representation invention:** no  
**Operation invention:** no  
**T13 reopened:** no

ARO-001d removed the ARO-001c continuation-learning confound by fixing the post-probe continuation with probability `1`:

```text
S=0 -> SELECT_G
S=1 -> SELECT_I
```

The first-stage value of `PROBE_S` remained learned from realized terminal return.

The assay therefore tested:

\[
\boxed{
\textbf{Does learned first-stage acquisition value track true downstream VOI
when continuation competence is fixed by construction?}
}
\]

The frozen answer is **no at the preregistered calibration criteria**.

---

## 1. Structural isolation gates passed

All construction gates passed:

```text
G0 fixed continuation used with probability 1        PASS
G1 true DeltaV vector matches prospective freeze     PASS
G2 empty-information Bayes loss = 0.5 every q        PASS
```

Thus the ARO-001c failure mode was removed by construction: continuation competence no longer had to be learned.

The frozen true curve was recovered exactly:

```text
q       true DeltaV_probe
0.60    -0.100
0.70    -0.050
0.75    -0.025
0.80     0.000
0.85     0.025
0.90     0.045
```

---

## 2. Learned first-stage value curve

The learned mean first-stage acquisition-value gaps were:

```text
q       true DeltaV    mean learned DeltaV_hat    P_greedy(PROBE_S)
0.60    -0.100         -0.03418                   0.44531
0.70    -0.050         +0.04727                   0.66797
0.75    -0.025         +0.07126                   0.76563
0.80     0.000         +0.08243                   0.81250
0.85    +0.025         +0.08317                   0.82813
0.90    +0.045         +0.07930                   0.83594
```

The learned curve is therefore strongly displaced toward buying information.

Unlike ARO-001c, the rank ordering is no longer perfect:

\[
\boxed{
\rho_Q = 0.82857 < 0.90.
}
\]

---

## 3. Frozen linear calibration test

The preregistered OLS fit

\[
\mathbb E[\widehat{\Delta V}_{\mu_1}]
=
a\,\Delta V_{\rm true}+b
\]

returned:

```text
slope a        0.76647     PASS frozen [0.75,1.25]
intercept b   +0.06829     FAIL frozen |b| <= 0.020
R^2            0.78629
zero crossing -0.08910     FAIL frozen |z| <= 0.020
```

The slope retains substantial sensitivity to true value, but the economic origin is badly displaced.

The implied learned indifference point is approximately

\[
\boxed{
\Delta V_{\rm true}\approx -0.089
}
\]

rather than the evaluator-defined boundary at `0`.

This is not a small threshold miss: the controller behaves as though substantially negative true information value can still justify acquisition.

---

## 4. Primary criteria

```text
G0 fixed continuation probability one               PASS
G1 true DeltaV vector                                PASS
G2 nuisance gate                                     PASS
V1 rho_Q >= 0.90                                    FAIL
V2 slope in [0.75,1.25]                             PASS
V3 |intercept| <= 0.020                             FAIL
V4 |zero crossing| <= 0.020                         FAIL
V5 negative true VOI -> negative mean learned gap   FAIL
V6 positive true VOI -> positive mean learned gap   PASS

PRIMARY_VOI_CALIBRATION_PASS                         FALSE
```

Secondary greedy behavioral calibration also failed:

```text
negative-VOI probe rates < 0.50                     FAIL
positive-VOI probe rates > 0.50                     PASS
zero-VOI probe rate in [0.20,0.80]                  FAIL  (0.8125)
```

---

## 5. The decisive localization

ARO-001c could not distinguish

```text
upstream value bias
vs
downstream continuation contamination
```

because continuation competence changed with q.

ARO-001d fixes continuation by construction and the positive displacement remains.

Therefore the remaining failure is now genuinely upstream of continuation learning:

\[
\boxed{
\textbf{fixed downstream exploitation competence
\not\Rightarrow
calibrated first-stage acquisition value.}
}
\]

The shallowest earned locus is:

```text
first-stage action-value formation / comparison
```

under the frozen tabular controller and exposure process.

This is stronger than the ARO-001c localization because downstream-policy quality is no longer a competing explanation.

---

## 6. Constant-comparator check near the boundary

The evaluator's best non-probe action is `SELECT_G` throughout:

```text
q = 0.70, 0.75, 0.80, 0.85
```

while the corresponding learned gaps are:

```text
+0.04727, +0.07126, +0.08243, +0.08317
```

for true values

```text
-0.050, -0.025, 0.000, +0.025.
```

Thus the local positive displacement around the economic boundary is present even before the best non-probe comparator switches to `COMPOSE_GIS` at `q=0.90`.

The comparator switch may contribute to the global non-monotonic tail, but it does not explain the near-boundary sign/calibration failure.

---

## 7. What mechanism is still not identified

ARO-001d identifies the locus, not the internal cause.

Because

\[
\widehat{\Delta V}
=Q(\mathrm{PROBE}_S)-\max_{a\ne\mathrm{PROBE}_S}Q(a),
\]

the run does not distinguish among:

```text
probe-value overestimation
non-probe value underestimation
policy-dependent sampling / unequal action exposure
constant-step-size estimation effects
finite-sample convergence
interaction with epsilon-greedy control
other first-stage learning-dynamics effects
```

No one of these mechanisms is causally established by v0.1d.

Also, because final behavior is greedy, probe choice remains a deterministic thresholded readout of the learned first-stage Q values. There is no independently identified policy-conversion layer.

---

## 8. Earned empirical ladder

The ARO sequence now supports the following finite-assay decomposition:

\[
\boxed{
\text{available operation}
\neq
\text{conditional competence}
\neq
\text{acquisition valuation}
\neq
\text{calibrated acquisition valuation}.
}
\]

Observed progression:

```text
ARO-001    supplied sequential operation available; 0/256 probe preference
ARO-001b   continuation learned 256/256; probe preference 240/256
ARO-001c   apparent VOI rank sensitivity, but continuation isolation failed
ARO-001d   continuation fixed; first-stage VOI calibration still fails
```

This is a controller/learning-dynamics result entirely within the supplied representation/operation family.

---

## 9. Next legitimate discriminating revision

If another assay is authorized, the minimal next question is no longer about continuation.

It should decompose the first-stage gap itself by prospectively measuring or controlling the two terms:

\[
Q(\mathrm{PROBE}_S)
\quad\text{and}\quad
Q(a^*_{\rm nonprobe}).
\]

A clean intervention would equalize or evaluator-control first-stage action exposure while keeping fixed continuation, then compare each learned action value against its known evaluator expected return.

That would discriminate:

```text
value-estimation bias under unequal/policy-dependent exposure
vs
persistent action-value miscalibration even under controlled exposure.
```

No new representation theory is required.

---

## 10. What is not earned

ARO-001d does **not** establish:

```text
general inability to estimate VOI
a unique credit-assignment mechanism
probe overvaluation as the unique cause
non-probe undervaluation as the unique cause
representation-family inadequacy
operation-family inadequacy
representation invention
operation invention
T13 pressure
ARO-B failure
```

---

## 11. Result compression

\[
\boxed{
\textbf{ARO-001d: after downstream continuation was fixed by construction,
the learned first-stage VOI estimate remained strongly positively displaced
(intercept +0.068, zero crossing -0.089), so the residual failure is now localized
to first-stage acquisition-value formation/comparison rather than continuation learning.}
}
\]
