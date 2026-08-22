# ARO-001 — Implementation Freeze v0.1

**Status:** `PROSPECTIVE_IMPLEMENTATION_FREEZE / NOT_RUN`  
**Canonical execution flag:** `STATUS = NOT_RUN`  
**Parent scientific freeze:** `ARO_001_ADAPTIVE_REPRESENTATION_OPERATIONS.md`  
**Variant executed by this freeze:** `ARO-A` only  
**ARO-B:** not run in v0.1  
**Representation invention:** no  
**Operation invention:** no  
**Favored operation class:** none  
**Post-hoc taxonomy expansion:** forbidden

This document freezes the first executable ARO-001 assay before any run is performed.

The purpose is deliberately small:

\[
\boxed{
\textbf{Can a learned task-conditioned controller distinguish when a supplied
one-shot representation operation is sufficient from when a bounded
sequential information-seeking operation is cheaper?}
}
\]

The assay does **not** test T13 representation construction, operation invention, held-out semantic transfer, or ARO-B future-task preparedness.

---

## 1. Implementation-level correction to the matched-world gate

The scientific freeze wrote the motivating gate schematically as

\[
\mathcal L(H_{\rm pre}\mid W_i)\approx\mathcal L(H_{\rm pre}\mid W_j),
\qquad o^\star(W_i)\neq o^\star(W_j).
\]

For an information-matched oracle, exact equality of the **entire admissible history** would make different first decisions impossible without extra information.

Therefore v0.1 freezes the executable anti-cheating gate at the intended level:

\[
\boxed{
\mathcal L(R_{\rm base}\mid W_i)
=
\mathcal L(R_{\rm base}\mid W_j)
}
\]

for the nuisance/error summary `R_base`, while the evaluator supplies the same task descriptor to both learner and oracle.

In v0.1, the empty-representation predictor has exact 0-1 risk `1/2` in every world. Thus residual magnitude alone cannot identify the useful operation.

The controller may use the prospectively supplied task descriptor; it may not use latent bits before buying the corresponding operation.

This is a scope clarification for execution, not a new scientific object.

---

## 2. Fixed latent world

Each episode samples independently

\[
G,I,S\overset{\rm iid}{\sim}\operatorname{Bernoulli}(1/2).
\]

The evaluator supplies one of four task descriptors uniformly during training:

```text
W1_G      Y = G
W1_I      Y = I
W2_XOR    Y = G xor I
W3_GATE   Y = G if S=0 else I
```

All four targets are marginally balanced, so an empty-information Bayes predictor has risk `1/2` in every world.

The task descriptor is visible before the first operation. The latent bits are not.

---

## 3. Fixed representation family P

The supplied representations are exactly

\[
\boxed{
\mathcal P=\{\Pi_G,\Pi_I,\Pi_S\}
}
\]

with

\[
\Pi_G(X)=G,\qquad
\Pi_I(X)=I,\qquad
\Pi_S(X)=S.
\]

No other representation is available.

The learner cannot construct, modify, fine-tune, or add a representation.

---

## 4. Fixed bounded operation family O

### First-stage operations

```text
SELECT_G      observe G; terminal prediction                 cost 1.0
SELECT_I      observe I; terminal prediction                 cost 1.0
COMPOSE_GI    observe (G,I) simultaneously; terminal         cost 1.6
COMPOSE_GIS   observe (G,I,S) simultaneously; terminal       cost 2.3
PROBE_S       observe S; continue to a second operation      cost 1.0
```

### Second-stage operations after PROBE_S

```text
SELECT_G      additionally observe G; terminal               cost 1.0
SELECT_I      additionally observe I; terminal               cost 1.0
COMPOSE_GI    additionally observe (G,I); terminal           cost 1.6
```

The sequential cost is additive:

\[
\boxed{
C_{\rm seq}=\sum_j C(O_j).
}
\]

There is no free retry and no unpriced information acquisition.

`PROBE_S` does not contain an unrestricted solver. It only reveals the evaluator-supplied representation `Pi_S` and opens one frozen second-stage choice.

No operation can create a new representation.

---

## 5. Frozen prediction rule

Prediction is evaluator-defined to isolate operation control from predictor learning.

After the purchased observations are available, the predictor outputs the Bayes-optimal binary prediction under the frozen iid latent law and the known task descriptor.

Ties predict `0`.

Therefore predictor competency is exact and no predictor parameters are learned.

This preserves

\[
\boxed{
\text{operation-control failure}
\neq
\text{predictor-training failure}.
}
\]

---

## 6. Why the four worlds discriminate supplied operations

### W1_G

`SELECT_G` gives zero loss at cost `1.0`.

### W1_I

`SELECT_I` gives zero loss at cost `1.0`.

### W2_XOR

Both `G` and `I` are required. `COMPOSE_GI` gives zero loss at cost `1.6`; a single projection leaves risk `1/2`.

### W3_GATE

The relevant second projection depends on `S`.

The bounded sequential policy

\[
\boxed{
\Pi_S
\rightarrow
\begin{cases}
\Pi_G,&S=0,\\
\Pi_I,&S=1
\end{cases}
}
\]

has zero loss and total cost `2.0`.

The one-shot rich operation `COMPOSE_GIS` also has zero loss but costs `2.3`.

Thus W3 creates the frozen distinction

\[
\boxed{
\text{static rich composition}
\neq
\text{sequential information-seeking transformation}.
}
\]

No claim of representation invention follows.

---

## 7. Learned controller mu

The controller is a tabular epsilon-greedy Q learner.

### First-stage state

The state is the visible task descriptor in

```text
{W1_G, W1_I, W2_XOR, W3_GATE}.
```

### Second-stage state

After `PROBE_S`, the state is

```text
(task descriptor, observed S in {0,1}).
```

### Training objective

Only for controller training, freeze the scalar objective

\[
J=\ell_{0/1}+\lambda C,
\qquad
\boxed{\lambda=0.15}.
\]

Scientific reporting remains decomposed into loss, cost, oracle regret, and recovery; the scalar is not treated as a universal scientific utility.

### Training constants

```text
seeds                 256
training episodes     4000 per seed
context distribution  uniform over four worlds
Q initialization      0
learning rate alpha   0.10
discount gamma        1.0
epsilon start         0.20
epsilon end           0.01
epsilon schedule      linear over training episodes
```

At a terminal prediction the controller receives reward

\[
R=-J.
\]

For `PROBE_S`, the first-stage Q value is updated from the same terminal return, so the learner pays for the entire sequence.

No evaluation episodes update Q.

---

## 8. Information timing I

v0.1 is `ARO-A`:

\[
\boxed{
T_t\rightarrow O_t.
}
\]

The task descriptor is visible before the first operation.

Latent `G,I,S` values are visible only after purchasing an operation that exposes them.

For the sequential branch, `S` becomes visible only after `PROBE_S`; the second operation may condition on that purchased observation.

No future episode, held-out seed, or unrevealed latent bit is visible to either learner or oracle.

ARO-B is not evaluated in v0.1.

---

## 9. Information-matched oracle o*

The oracle has exactly the same task descriptor and purchased observations available at each decision point as the learner, but unlimited computation over the supplied policy space.

Frozen oracle policy:

```text
W1_G      SELECT_G
W1_I      SELECT_I
W2_XOR    COMPOSE_GI
W3_GATE   PROBE_S; then SELECT_G if S=0 else SELECT_I
```

Thus:

\[
\boxed{
\text{oracle advantage may be computational, never informational}.
}
\]

The best one-shot oracle is separately reported. It is prohibited from using `PROBE_S` and therefore uses `COMPOSE_GIS` in `W3_GATE`.

---

## 10. Baselines

Report at least:

```text
ORACLE_FULL       information-matched sequential oracle
ORACLE_ONESHOT    best supplied one-shot operation by task
ALWAYS_RICH       COMPOSE_GIS in every world
ALWAYS_G          SELECT_G in every world
RANDOM            uniform first-stage action; uniform second-stage action after probe
LEARNED           frozen greedy policy after training
```

The learned controller is not compared only against a weak cheap baseline.

---

## 11. Evaluation metrics Y

For each trained seed, evaluate the greedy policy exactly by enumerating all `2^3=8` latent states in every world.

Primary metrics:

```text
predictive_loss          mean 0-1 loss
representation_cost      mean cumulative operation cost
training_objective_J     loss + 0.15 * cost
oracle_regret_J          J(LEARNED) - J(ORACLE_FULL)
first_operation_accuracy fraction of worlds with oracle first operation
W3_branch_accuracy       correctness of second operation for S=0 and S=1
```

Report also the best one-shot oracle cost so the value of sequential control is directly visible.

### Recovery sanity check

After training, evaluate all ordered task changes using the frozen greedy controller.

Define episode-level recovery time as the first post-change episode whose executed supplied policy is oracle-equivalent for that task.

Freeze

```text
H_recover = 1 episode
```

because ARO-A reveals the new task descriptor before operation choice.

Report

\[
P(T_{\rm recover}\le1).
\]

This is only an ARO-A responsiveness sanity check; it is not a quickest-change-detection claim.

### Matched nuisance gate

Exact enumeration must verify

```text
empty-information Bayes loss = 0.5
```

in every world.

---

## 12. Frozen success criteria

A positive v0.1 control result requires all of:

```text
S1  >= 95% of seeds learn the oracle-equivalent full policy
S2  mean oracle_regret_J <= 0.02
S3  mean predictive_loss <= 0.01
S4  mean representation_cost <= 1.425
S5  mean W3_branch_accuracy >= 0.95
S6  P(T_recover <= 1) >= 0.95
S7  matched nuisance gate holds exactly at 0.5 in all four worlds
```

The cost threshold in S4 sits below the best one-shot oracle average cost:

\[
(1.0+1.0+1.6+2.3)/4=1.475.
\]

The full oracle average cost is

\[
(1.0+1.0+1.6+2.0)/4=1.4.
\]

Thus S4 requires evidence of value from the sequential option rather than merely matching the rich static policy.

---

## 13. Failure-localization map F

Interpret failures shallowly.

```text
S1/S2 fail, predictors exact
-> controller-learning / exploration failure first

S3 fails while oracle has zero loss
-> operation-selection failure first

S4 fails with S3 passing
-> cost calibration / sequential-use failure

S5 fails
-> conditional second-stage routing failure

S6 fails
-> task-conditioned responsiveness failure

S7 fails
-> world-construction / evaluation bug

all supplied policies fail target loss
-> SUPPLIED_REPRESENTATION_OPERATION_FAMILY_INADEQUATE
```

None of these implies T13 representation invention.

---

## 14. Claim ceiling

A positive result may support only:

```text
in this frozen finite assay, a learned controller can discover a task-conditioned
mixture of supplied one-shot and bounded sequential representation operations
that approaches the information-matched oracle and beats the best one-shot
oracle on average operating cost.
```

It does **not** establish:

```text
representation invention
operation invention
explicit causal diagnosis
held-out semantic transfer
ARO-B preparedness
universal optimality of sequential transformation
safe authority transfer
T13 success
```

The key non-implication remains

\[
\boxed{
\text{successful sequential transformation control}
\not\Rightarrow
\text{representation invention}.
}
\]

---

## 15. Execution constitution

Before the run, the following are immutable for v0.1:

```text
world definitions
representation family
operation semantics and costs
Bayes predictor
lambda
training algorithm and hyperparameters
seed count
metric definitions
success thresholds
oracle policies
recovery definition
```

The executable script is frozen in the same repository branch before execution.

Any change after inspecting results creates v0.2 and cannot be reported as v0.1.

The prospective freeze file itself is not rewritten after execution; results are recorded in a separate artifact.
