# ARO-001 v0.1 — Frozen Result

**Status:** `RUN_COMPLETE / NEGATIVE_AT_FROZEN_SUCCESS_CRITERIA`  
**Variant:** `ARO-A`  
**Prospective implementation freeze:** `ARO_001_IMPLEMENTATION_FREEZE_V0_1.md`  
**Executable:** `aro_001/run_v0_1.py`  
**Freeze commit before run:** `9c8dcf38a285a63705d0623ee5d43d40f64384c4`  
**Seeds:** `256`  
**Post-result rerun:** none  
**Post-result hyperparameter change:** none

ARO-001 v0.1 did **not** satisfy its frozen positive criteria.

The result is nevertheless sharply localized:

\[
\boxed{
\textbf{static supplied-operation control succeeded;
cheaper sequential operation utilization failed.}
}
\]

No representation invention or operation invention was attempted.

---

## 1. Frozen admissibility gate passed

The empty-information Bayes loss was exactly

\[
\boxed{0.5}
\]

in every world:

```text
W1_G      0.5
W1_I      0.5
W2_XOR    0.5
W3_GATE   0.5
```

Thus residual magnitude alone could not identify which supplied operation was useful.

`S7` passed.

---

## 2. Oracle baselines

The information-matched full oracle achieved

```text
loss  0.000
cost  1.400
J     0.21000
```

The best one-shot oracle achieved

```text
loss  0.000
cost  1.475
J     0.22125
```

The difference comes entirely from `W3_GATE`:

```text
one-shot oracle:
COMPOSE_GIS
cost 2.3

full sequential oracle:
PROBE_S
-> SELECT_G if S=0
-> SELECT_I if S=1
cost 2.0
```

So the frozen environment contained a real, bounded value-of-information advantage for sequential operation.

---

## 3. Learned result

Across all `256/256` seeds, the final greedy first-stage policy was:

```text
W1_G      SELECT_G
W1_I      SELECT_I
W2_XOR    COMPOSE_GI
W3_GATE   COMPOSE_GIS
```

Therefore the learner exactly recovered the **best one-shot operation map** and never selected the cheaper sequential first step `PROBE_S` in `W3_GATE`.

Frozen aggregate metrics:

```text
predictive loss                     0.00000
representation cost                 1.47500
J                                   0.22125
J regret to full oracle             0.01125
full-oracle-equivalent seed rate    0 / 256 = 0.000
first-operation accuracy            0.750
P(T_recover <= 1)                   0.750
```

The predictive task was solved perfectly. The remaining gap is entirely an operation-cost / sequential-control gap.

---

## 4. Frozen success criteria

```text
S1  full-policy seed rate >= 0.95        FAIL
S2  mean J regret <= 0.02                PASS
S3  mean predictive loss <= 0.01         PASS
S4  mean cost <= 1.425                   FAIL
S5  mean W3 branch accuracy >= 0.95       FAIL
S6  P(T_recover <= 1) >= 0.95            FAIL
S7  matched nuisance gate                 PASS

ALL_FROZEN_CRITERIA_PASS                  FALSE
```

`S5` must be interpreted cautiously: because the final first-stage policy never chooses `PROBE_S`, second-stage Q values are largely off-policy and are not evidence that the learned controller possessed a usable sequential branch policy.

---

## 5. Shallowest failure localization

The frozen failure map points first to:

```text
cost calibration / sequential-use failure
+
controller learning / exploration failure
```

not predictor failure.

The following facts are directly observed:

1. the sequential policy is available in the supplied family;
2. the evaluator proves it has lower frozen cost at equal zero loss in `W3_GATE`;
3. the learner selects the static rich composition in every seed;
4. the learner therefore fails to exploit the supplied sequential value-of-information path.

A plausible mechanism is **nested exploration / credit-assignment foreclosure**:

```text
PROBE_S must be selected
-> useful conditional second-stage actions must be learned
-> only then does the lower total cost become visible to the first-stage controller
```

while the immediately successful one-shot `COMPOSE_GIS` supplies zero loss without requiring that nested learning path.

However that mechanism is **not yet causally established by this run**. It remains a competing explanation to be discriminated in a new prospective experiment.

Therefore the earned result is only:

\[
\boxed{
\text{availability of a cheaper sequential information-seeking operation}
\not\Rightarrow
\text{learned utilization of that operation under the frozen controller.}
}
\]

and, more specifically for this assay:

\[
\boxed{
\text{perfect static operation control}
\not\Rightarrow
\text{sequential value-of-information control}.
}
\]

---

## 6. What is not earned

ARO-001 v0.1 does **not** establish:

```text
sequential transformation is generally hard
nested exploration is the proven cause
ARO taxonomy is inadequate
representation invention is required
T13 is implicated
static composition is universally superior
ARO-B failure
```

The supplied family was sufficient: the oracle succeeds inside it.

Therefore this is **not**

```text
SUPPLIED_REPRESENTATION_OPERATION_FAMILY_INADEQUATE
```

and does not create pressure toward T13.

---

## 7. Next legitimate discriminating question

The next experiment, if authorized, should discriminate at least:

```text
H1  sequential operation is under-exposed because its first-step value is learned
    only through rare nested visits

H2  the tabular update / credit assignment is inadequate even with sufficient exposure

H3  the scalar training objective or exploration schedule biases the controller toward
    immediately terminal rich operations
```

The minimal next revision should alter only the variable needed to distinguish these explanations—for example, forced balanced exposure of first-stage operations while preserving the same frozen worlds and operation costs.

No v0.1 parameter may be changed retroactively.

---

## 8. Result compression

\[
\boxed{
\textbf{ARO-001 v0.1: the learner found the correct static operation for every task,
but failed in every seed to exploit a cheaper supplied sequential information-seeking route.}
}
\]

This is a negative result at the representation-operation **policy** layer, with predictor competence and supplied-family adequacy preserved.
