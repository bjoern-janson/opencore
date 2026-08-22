# ARO-001b v0.1 — Exposure-Controlled Sequential Learning Result

**Status:** `RUN_COMPLETE / NEGATIVE_AT_FROZEN_95_PERCENT_RESCUE_GATE`  
**Diagnostic classification:** `D2_BRANCH_LEARNED_PROBE_NOT_VALUED`  
**Variant:** `ARO-A`  
**Parent result:** `ARO_001_V0_1_RESULT.md`  
**Prospective freeze:** `ARO_001B_EXPOSURE_CONTROLLED_FREEZE_V0_1.md`  
**Frozen executable:** `aro_001/run_001b_v0_1.py`  
**Executable freeze commit before result inspection:** `dd072f344f5e152933290c0c8be064a150787290`  
**Seeds:** `256`  
**Representation invention:** no  
**Operation invention:** no  
**T13 reopened:** no

ARO-001b intervened on exactly one variable relative to ARO-001 v0.1:

\[
\boxed{
P(\text{force }O_1=\mathrm{PROBE}_S\mid W3\_GATE)=0.25
}
\]

during training only.

The second-stage action remained learned and evaluation remained unforced.

---

## 1. Frozen result

The intervention completely rescued conditional second-stage learning:

```text
W3 correct conditional branches      256 / 256 = 1.0000
```

Every seed learned

\[
\boxed{
\mathrm{PROBE}_S
\rightarrow
\begin{cases}
\mathrm{SELECT}_G,&S=0,\\
\mathrm{SELECT}_I,&S=1.
\end{cases}
}
\]

However only

```text
W3 greedy PROBE_S preference          240 / 256 = 0.9375
full-oracle-equivalent policy         240 / 256 = 0.9375
```

crossed from the learned branch to a greedy first-stage preference for buying the probe.

The frozen positive threshold was `>= 0.95`, requiring at least `244/256` successful seeds.

Therefore ARO-001b remains **negative at the frozen clean-rescue gate**.

---

## 2. Aggregate performance

```text
mean predictive loss                  0.000244140625
mean representation cost              1.403417968750
full-oracle cost                       1.400000000000
best one-shot oracle cost              1.475000000000
mean J                                 0.210756835938
full-oracle J                          0.210000000000
mean J regret                          0.000756835938
P(T_recover <= 1)                      0.984375
```

The controlled-exposure controller is therefore very close to the full sequential oracle in aggregate cost and objective value, but the prospectively frozen seed-level reliability gate prevents calling it a positive rescue.

---

## 3. Frozen criteria

```text
E1  W3 branch-full seed rate >= 0.95       PASS   1.0000
E2  W3 probe-preferred seed rate >= 0.95   FAIL   0.9375
E3  full-oracle seed rate >= 0.95           FAIL   0.9375
E4  mean predictive loss <= 0.01            PASS
E5  mean cost <= 1.425                      PASS
E6  mean oracle regret <= 0.02              PASS
E7  P(T_recover <= 1) >= 0.95               PASS   0.984375
E8  matched nuisance gate                   PASS

ALL_FROZEN_CRITERIA_PASS                    FALSE
```

---

## 4. Comparison to ARO-001 v0.1

ARO-001 v0.1 learned the best one-shot first-stage map in all seeds and selected `PROBE_S` greedily in

```text
0 / 256
```

seeds.

ARO-001b, after changing only first-stage probe exposure, selected `PROBE_S` greedily in

```text
240 / 256
```

seeds and learned the correct conditional second-stage route in

```text
256 / 256
```

seeds.

Thus the intervention produced a large and highly specific change in the failed behavior.

The earned causal statement is bounded:

\[
\boxed{
\text{increased first-stage probe exposure is sufficient to make the correct
second-stage route learnable in every seed and to make probe preference emerge
in most seeds under this frozen assay.}
}
\]

Because the frozen `0.95` first-stage gate was not reached, ARO-001b does **not** establish that under-exposure alone fully explains the v0.1 failure.

---

## 5. Shallowest localization

The result rejects the strongest form of the second-stage-learning explanation under the exposure intervention:

\[
\boxed{
\text{controlled probe exposure}
\rightarrow
\text{correct branch learning in }256/256.
}
\]

Therefore the remaining failure is first localized to the first-stage value layer:

```text
first-stage value estimation
/
credit propagation from learned branch behavior
/
exploration-induced value noise or finite-sample convergence
```

not to representation-family inadequacy, operation-family inadequacy, or predictor competence.

The fixed objective itself prefers the correct greedy sequential policy in `W3_GATE`:

```text
PROBE_S -> correct conditional projection    J = 0.300
COMPOSE_GIS                                  J = 0.345
```

so a seed that has learned both correct branches but still chooses `COMPOSE_GIS` has not reliably converted the learned downstream route into the correct first-stage greedy value ranking.

This does not yet identify which learning-dynamics mechanism causes that residual failure.

---

## 6. OpenCore analogue

ARO-001b cleanly separates:

\[
\boxed{
\text{available discriminator}
\neq
\text{learned conditional use of discriminator}
\neq
\text{reliably valued first-stage acquisition of discriminator}.
}
\]

The result therefore supports the narrower empirical distinction:

\[
\boxed{
\text{learning what a probe enables}
\not\Rightarrow
\text{reliably learning when the probe is worth buying}.
}
\]

No causal authority beyond that distinction is earned.

---

## 7. What is not earned

ARO-001b does **not** establish:

```text
under-exposure is the unique cause of v0.1
objective misspecification is the cause
credit assignment is the unique cause
sequential transformation is generally hard
ARO taxonomy is inadequate
representation invention is required
operation invention is required
T13 is implicated
ARO-B failure
```

The supplied representation and operation family remains adequate because the information-matched oracle succeeds inside it.

---

## 8. Execution provenance

The executable and intervention freeze were committed before ARO-001b result inspection.

A repository-native GitHub Actions audit then:

1. checked out the committed PR branch;
2. installed the frozen runtime dependency;
3. preserved the committed expected JSON;
4. executed `crank/aro_001/run_001b_v0_1.py` from the checkout;
5. verified that the generated JSON was semantically identical to the committed result JSON.

The audit job completed successfully.

Thus the committed result is independently reproduced by the committed executable under the repository-native execution path.

---

## 9. Result compression

\[
\boxed{
\textbf{ARO-001b: forced probe exposure made the correct conditional route learnable
in every seed and raised greedy probe selection from 0/256 to 240/256,
but missed the frozen 95% reliability gate; the residual failure is now localized
to reliable first-stage valuation of an already-learned sequential route.}
}
\]

This remains a controller/learning-dynamics result. No new representation-management ontology is introduced.
