# ARO-001c v0.1 — Probe-Value Calibration Result

**Status:** `RUN_COMPLETE / ISOLATION_GATE_FAILED`  
**Primary rank-ordering claim:** `NOT EARNED`  
**Secondary threshold-calibration claim:** `FAILED`  
**Prospective freeze:** `ARO_001C_PROBE_VALUE_CALIBRATION_FREEZE_V0_1.md`  
**Frozen executable:** `aro_001/run_001c_v0_1.py`  
**Freeze commit before execution:** `6e4adbb956ac5a4c0fc213cd511c0329046fef6e`  
**Repository-native workflow run:** `32574521609`  
**Seeds:** `256` per value condition  
**Representation invention:** no  
**Operation invention:** no  
**T13 reopened:** no

ARO-001c asked whether learned first-stage acquisition value tracks evaluator-defined downstream value of information:

\[
\Delta V_{\rm probe}
\longrightarrow
\widehat{\Delta V}_{\mu}
\longrightarrow
\mathbf 1\{\mu_{\rm greedy}=\mathrm{PROBE}_S\}.
\]

The assay produced a striking descriptive rank signal, but the prospectively frozen continuation-competence gate failed. Therefore the intended first-stage VOI-control claim is **not earned**.

---

## 1. Frozen true value curve

The executable recovered the prospectively frozen true values exactly:

```text
q       true DeltaV_probe
0.60    -0.100
0.70    -0.050
0.75    -0.025
0.80     0.000
0.85     0.025
0.90     0.045
```

The empty-information Bayes loss remained exactly `0.5` in every condition.

Thus the true-value construction and nuisance gate passed.

---

## 2. Observed learned curves

The learned first-stage Q-gap means were:

```text
q       true DeltaV    mean learned DeltaV_hat
0.60    -0.100         -0.05737
0.70    -0.050          0.02186
0.75    -0.025          0.05007
0.80     0.000          0.07632
0.85     0.025          0.07845
0.90     0.045          0.08188
```

Greedy probe-preference seed rates were:

```text
q       P_greedy(PROBE_S)
0.60    0.36328
0.70    0.60156
0.75    0.67969
0.80    0.76953
0.85    0.77734
0.90    0.80078
```

Both descriptive curves are perfectly rank ordered across the six frozen values:

\[
\boxed{
\rho_{Q}=1.0,
\qquad
\rho_{\rm probe}=1.0.
}
\]

However this correlation is not sufficient for the preregistered primary claim because the continuation-isolation gate failed.

---

## 3. The decisive failure: continuation competence did not remain fixed

ARO-001c prospectively required the correct post-probe branch policy to be learned in at least `95%` of seeds **at every q**.

Observed branch-full seed rates were:

```text
q       correct branch-full seed rate
0.60    0.56250
0.70    0.68359
0.75    0.69531
0.80    0.75781
0.85    0.79688
0.90    0.82812
```

Therefore:

```text
R0 continuation branch rate >= 0.95 every q    FAIL
R1 true DeltaV vector matches freeze           PASS
R2 rho_Q >= 0.90                               PASS
R3 rho_probe >= 0.90                           PASS
PRIMARY_RANK_ORDERING_PASS                      FALSE
```

The intended conditioning statement

\[
\boxed{
\text{continuation competence is available}
}
\]

was not preserved across the matched value family.

This blocks the stronger interpretation

\[
\text{true VOI}
\rightarrow
\text{learned first-stage VOI estimator}.
\]

The observed monotonicity is retained as a descriptive signal only.

---

## 4. Why the isolation failed

The only scientific parameter varied was the evaluator-side gate-activation probability `q`, but that parameter does more than change the **economic value** of probing.

It also changes the stochastic reward structure seen by the learned continuation actions after `PROBE_S`.

Thus the matched family changed, in effect:

```text
first-stage probe value
+
second-stage learning signal / reward noise
```

rather than preserving continuation competence while varying only upstream value.

The 0.25 forced-probe exposure that yielded `256/256` branch competence in deterministic ARO-001b was not sufficient under these stochastic value worlds.

Therefore the shallowest failure locus is:

\[
\boxed{
\textbf{experimental isolation / continuation-competence preservation}
}
\]

before first-stage VOI formation.

This is a failure of the intended assay decomposition, not evidence that the representation or operation family is inadequate.

---

## 5. Threshold calibration also failed

The secondary economic-threshold criteria failed independently:

```text
C1 negative true VOI -> negative mean learned gap       FAIL
C2 q=0.80 mean learned gap near zero                    FAIL
C3 positive true VOI -> positive mean learned gap       PASS
C4 negative true VOI -> probe rate below 0.50           FAIL
C5 positive true VOI -> probe rate above 0.50           PASS
C6 q=0.80 probe rate in [0.20,0.80]                     PASS
SECONDARY_CALIBRATION_PASS                              FALSE
```

In particular:

```text
q=0.70   true DeltaV=-0.050   mean learned gap=+0.02186   probe rate=0.60156
q=0.75   true DeltaV=-0.025   mean learned gap=+0.05007   probe rate=0.67969
q=0.80   true DeltaV= 0.000   mean learned gap=+0.07632   probe rate=0.76953
```

So the controller exhibits a substantial positive acquisition-value bias around and below the true economic boundary.

Because continuation competence is itself unstable, ARO-001c does not identify whether that bias comes from first-stage value estimation, downstream-policy quality, historical credit propagation, or their interaction.

---

## 6. Identification boundary from the frozen controller

Final evaluation is greedy.

Therefore

\[
\mathbf 1\{\mu_{\rm greedy}=\mathrm{PROBE}_S\}
\]

is a deterministic thresholded readout of the learned first-stage Q values.

ARO-001c consequently does **not** identify a separate

```text
correct learned value -> incorrect policy conversion
```

mechanism.

The relevant unresolved object remains learned first-stage value formation under a controlled continuation.

---

## 7. Earned result

The strongest earned result is negative and methodological:

\[
\boxed{
\textbf{ARO-001c did not successfully isolate first-stage VOI formation,
because the value manipulation also changed learned continuation competence.}
}
\]

A secondary descriptive observation is:

\[
\boxed{
\text{true probe value increased monotonically}
\Rightarrow
\text{mean learned probe advantage and greedy probe rate also increased monotonically}
}
\]

in this run, with both Spearman correlations equal to `1.0`.

But because the frozen isolation gate failed, this observation does **not** earn the preregistered claim of upstream VOI control.

---

## 8. Next legitimate discriminating revision

The minimal next assay, if authorized, should remove continuation learning as a confound while preserving first-stage learning.

For example:

```text
PROBE_S
-> evaluator-fixed / teacher-forced optimal continuation by observed S
-> first-stage Q(PROBE_S) remains learned from the realized terminal return
```

with the same q grid, costs, first-stage action family, 0.25 probe exposure, seeds, and evaluation metrics.

That would test:

\[
\boxed{
\textbf{Can first-stage value learning track true downstream VOI
when continuation competence is held fixed by construction?}
}
\]

No additional representation theory is required.

---

## 9. What is not earned

ARO-001c does **not** establish:

```text
a learned general-purpose VOI estimator
successful first-stage VOI control
policy-conversion failure
representation-family inadequacy
operation-family inadequacy
representation invention
operation invention
T13 pressure
ARO-B failure
```

The result remains entirely below the representation-construction frontier.

---

## 10. Result compression

\[
\boxed{
\textbf{ARO-001c: the learned Q-gap and probe-choice curves were perfectly rank ordered
with true VOI, but the matched value manipulation also degraded continuation competence,
so the preregistered first-stage VOI claim is not earned; the next minimal revision is to
hold continuation fixed and test acquisition-value learning directly.}
}
\]
