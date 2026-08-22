# ARO-001b — Exposure-Controlled Sequential Learning Freeze v0.1

**Status:** `PROSPECTIVE_IMPLEMENTATION_FREEZE / NOT_RUN`  
**Canonical execution flag:** `STATUS = NOT_RUN`  
**Parent scientific freeze:** `ARO_001_ADAPTIVE_REPRESENTATION_OPERATIONS.md`  
**Parent negative result:** `ARO_001_V0_1_RESULT.md`  
**Variant:** `ARO-A`  
**Representation invention:** no  
**Operation invention:** no  
**T13 reopened:** no

ARO-001 v0.1 established, in the frozen finite assay,

\[
\boxed{
\text{perfect static supplied-operation control}
\not\Rightarrow
\text{sequential value-of-information control}.
}
\]

The information-matched oracle succeeded inside the supplied representation/operation family, while the learned controller selected the best one-shot map in all `256/256` seeds and never preferred `PROBE_S` in `W3_GATE`.

ARO-001b makes exactly one scientific intervention: **increase first-stage exposure to the already-supplied `PROBE_S` operation during training in `W3_GATE`**. The second-stage operation remains learned.

The assay asks:

\[
\boxed{
\textbf{Does controlled exposure to the probe remove the v0.1 sequential-control failure,
and if not, does failure remain in branch learning or in first-stage valuation?}
}
\]

---

## 1. Frozen invariants inherited unchanged from ARO-001 v0.1

The following remain exactly unchanged:

```text
worlds and latent law
representation family P
operation family O
operation semantics
operation costs
Bayes predictor and tie rule
ARO-A information timing
training objective J = loss + 0.15 * cost
256 seeds
4000 training episodes per seed
uniform context distribution
Q initialization = 0
learning rate alpha_Q = 0.10
discount gamma = 1.0
epsilon start = 0.20
epsilon end = 0.01
linear epsilon schedule
oracle policy
best one-shot oracle
exact-enumeration evaluation
H_recover = 1
matched nuisance gate
scientific claim ceilings
```

No result from v0.1 is used to change the worlds, costs, target functions, operator semantics, predictor, or scalar training objective.

---

## 2. Single intervention

Freeze the forced first-stage probe exposure rate at

\[
\boxed{\alpha_{\rm probe}=0.25}
\]

**conditional on a training episode being `W3_GATE`.**

For every `W3_GATE` training episode:

1. compute the ordinary v0.1 epsilon-greedy proposed first action;
2. independently draw the exposure-control coin;
3. with probability `0.25`, override the proposed first action with `PROBE_S`;
4. otherwise execute the proposed first action;
5. if `PROBE_S` is executed, choose the second-stage action by the same learned epsilon-greedy rule as v0.1;
6. update Q values from the same terminal return as v0.1.

No first-stage forcing occurs in `W1_G`, `W1_I`, or `W2_XOR`.

Evaluation is always greedy and **never forced**.

Thus the intervention is training exposure, not evaluation assistance.

The expected number of forced probe episodes is

\[
4000\times\frac14\times0.25=250
\]

per seed, before random variation.

---

## 3. What remains learned

The second-stage policy after the forced or voluntarily selected probe remains fully learned:

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

No teacher forcing of `SELECT_G` or `SELECT_I` is permitted.

The first-stage Q value of `PROBE_S` is also learned from the actual terminal return. Forced selection changes exposure frequency; it does not directly assign a favorable probe value.

This preserves the central diagnostic distinction:

\[
\boxed{
\text{learning what the probe enables}
\neq
\text{learning that the probe is worth buying}.
}
\]

---

## 4. Evaluation metrics

After training, evaluate the unforced greedy policy exactly over all `8` latent states in each of the four worlds.

Retain all v0.1 metrics and add exposure diagnostics:

```text
predictive_loss
representation_cost
J
oracle_regret_J
first_operation_accuracy
W3_branch_accuracy
oracle_equivalent_full_policy
P(T_recover <= 1)
W3_probe_preferred = greedy first action in W3_GATE is PROBE_S
W3_branch_full = S=0 -> SELECT_G and S=1 -> SELECT_I
forced_probe_count
executed_probe_count
```

Report seed rates for `W3_probe_preferred`, `W3_branch_full`, and full-oracle equivalence.

---

## 5. Frozen diagnostic interpretation

Let

```text
B = >= 95% of seeds learn both correct W3 second-stage branches
P = >= 95% of seeds greedily prefer PROBE_S in W3 at evaluation
F = >= 95% of seeds are full-oracle-equivalent
```

Interpret only as follows.

### D1 — exposure sufficient in this assay

```text
B = true
P = true
F = true
```

supports:

\[
\boxed{
\text{in this frozen assay, increasing first-stage probe exposure is sufficient
to remove the v0.1 sequential-control failure.}
}
\]

It does **not** establish that under-exposure is the unique mechanism, nor that the result generalizes beyond this controller/world family.

### D2 — branch learned, probe still not valued

```text
B = true
P = false
```

localizes first to:

```text
first-stage valuation / credit propagation / objective-exploration interaction
```

The learner has learned what the probe enables but does not prefer to buy it.

### D3 — branch itself not learned under controlled probe exposure

```text
B = false
```

localizes first to:

```text
second-stage learning / temporal-control / branch-exploration failure
```

This result alone does not prove a specific credit-assignment mechanism.

A later teacher-forced second-stage assay would be required to distinguish implementation/operator-interface failure from learning failure if D3 occurs.

### D4 — partial / heterogeneous

Any mixed result that misses the `0.95` gates is reported quantitatively without forcing it into D1–D3.

---

## 6. Frozen positive criteria

ARO-001b counts as a clean exposure-rescue result only if all of:

```text
E1  W3_branch_full seed rate >= 0.95
E2  W3_probe_preferred seed rate >= 0.95
E3  full-oracle-equivalent seed rate >= 0.95
E4  mean predictive_loss <= 0.01
E5  mean representation_cost <= 1.425
E6  mean oracle_regret_J <= 0.02
E7  P(T_recover <= 1) >= 0.95
E8  matched nuisance gate = exactly 0.5 in all worlds
```

The thresholds match the evidentiary intent of v0.1: a positive result must use the sequential route, not merely preserve perfect prediction with the richer one-shot operation.

---

## 7. Failure ceiling

ARO-001b cannot establish:

```text
representation invention
operation invention
T13 necessity
ARO taxonomy inadequacy
sequential transformation is generally difficult
under-exposure is the unique cause of v0.1
held-out semantic transfer
ARO-B preparedness
```

Because the oracle already succeeds inside the supplied family,

\[
\boxed{
\text{failure of ARO-001b remains a controller/learning-dynamics result first.}
}
\]

---

## 8. Execution constitution

Before execution, the following are frozen:

```text
alpha_probe = 0.25 conditional on W3_GATE training episodes
all inherited v0.1 constants and worlds
intervention logic
second-stage remains learned
evaluation remains unforced
metrics
diagnostic gates
success criteria
256 seeds
```

The executable is committed before any ARO-001b result is observed.

Any modification after result inspection creates a new version and cannot be reported as ARO-001b v0.1.
