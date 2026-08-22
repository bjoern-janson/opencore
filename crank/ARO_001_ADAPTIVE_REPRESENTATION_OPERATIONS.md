# ARO-001 — Adaptive Representation Operations

**Status:** `PROSPECTIVE_SCIENTIFIC_FREEZE / NOT_RUN`  
**Canonical execution flag:** `STATUS = NOT_RUN`  
**Scope:** empirical adaptive control over evaluator-supplied representations and evaluator-supplied bounded representation operations  
**Favored operation class:** none  
**Representation invention tested:** no  
**Operation invention tested:** no  
**New OpenCore primitive:** none  
**T13 reopened:** no  
**Authority / Gamma changed:** no  
**Implementation frozen:** no  
**Experiment run:** no  
**Results:** none

ARO-001 is a prospective **scientific fork detector**. It is not a commitment to an ontology of representation management.

The central question is:

\[
\boxed{
\textbf{Can adaptive control over a fixed representation/operation family discover
which supplied operations are actually needed for performance,
cost efficiency, and timely recovery?}
}
\]

The experiment is deliberately designed so that the supplied taxonomy may lose.

\[
\boxed{
\mathcal O_{\rm supplied}
\xrightarrow{\text{experiment}}
\begin{cases}
\text{collapse categories},\\
\text{retain categories},\\
\text{split categories in a later experiment},\\
\text{show that the supplied family is inadequate}.
\end{cases}
}
\]

The last outcome is **not** representation or operation invention inside ARO-001. It is only evidence that the supplied family is inadequate and that a new prospectively frozen experiment may be warranted.

The constitutional sentence is:

\[
\boxed{
\textbf{The experiment may invalidate the supplied operation taxonomy;
the taxonomy may not determine the interpretation of the experiment's result.}
}
\]

---

## 1. Hard boundary

ARO-001 studies

\[
\boxed{
\text{fixed supplied representations}
+
\text{fixed bounded supplied operations}
\longrightarrow
\text{adaptive operation control}.
}
\]

It does **not** study

\[
\text{failure}
\longrightarrow
\text{invent a new representation or operation}.
\]

Therefore:

\[
\boxed{
\text{ARO success}
\neq
\text{T13 representation-invention success}.
}
\]

and

\[
\boxed{
\text{failure of all supplied operations}
\not\Rightarrow
\text{representation invention is required}.
}
\]

The learner may choose only from evaluator-supplied objects whose semantics are frozen prospectively.

---

## 2. Irreducible scientific objects

ARO-001 freezes the following abstract fields before implementation details are chosen:

\[
\boxed{
\begin{aligned}
\mathcal P&=\text{fixed supplied representation family},\\
\mathcal O&=\text{fixed supplied bounded operation family},\\
\mathcal D^\star&=\text{externally constituted challenge process},\\
\mu&=\text{learned operation-selection policy},\\
\mathcal M&=\text{matched-world construction},\\
\mathcal I&=\text{information-timing rule},\\
o^\star&=\text{information-matched operation oracle},\\
\mathcal Y&=\text{predefined evaluation metrics},\\
\mathcal F&=\text{failure-localization map}.
\end{aligned}
}
\]

These are assay roles, not new permanent OpenCore state variables or control surfaces.

---

## 3. Supplied representation family

The evaluator supplies a finite family

\[
\boxed{
\mathcal P
=
\{\Pi_1,\ldots,\Pi_k\}.
}
\]

ARO-001 does not require the family to be nested.

Pairs may satisfy

\[
\Pi_i\preceq\Pi_j,
\]

be incomparable in the refinement order, or expose different relational structures altogether.

The experiment must document, prospectively, for each `Pi_j`:

- its input domain;
- its output semantics;
- its cost;
- what information it can expose by construction;
- any nesting/refinement relation to other supplied representations;
- any known overlap or redundancy;
- any constraints on downstream predictors or operations.

No hidden evaluator-only representation may be made available to the learner except where explicitly designated as an oracle-only benchmark object.

---

## 4. Supplied bounded operation family

The evaluator supplies

\[
\boxed{
\mathcal O
=
\{O_1,\ldots,O_m\}.
}
\]

The initial candidate taxonomy may include bounded versions of:

\[
\boxed{
\mathcal O_{m candidate}
=
\{
O_{\rm select},
O_{\rm compose},
O_{\rm route},
O_{\rm translate},
O_{\rm resolve},
O_{\rm compress}
\}.
}
\]

This list is **not** asserted to be complete or fundamental.

### 4.1 Bounded-semantics requirement

Every operation must have an evaluator-defined contract specifying:

- admissible inputs;
- admissible outputs;
- access to supplied representations;
- compute / representation cost accounting;
- allowed internal state;
- whether the operation can call sub-operations;
- whether the operation can preserve, drop, combine, or transform information;
- maximum depth / breadth / number of representation accesses;
- prohibition on unrestricted search over unsupplied representations.

The decisive anti-cheating rule is:

\[
\boxed{
O_t\text{ is an evaluator-defined bounded operator, not an API label around an unrestricted solver.}
}
\]

In particular:

\[
\boxed{
O_{\rm compose}\neq\text{unbounded synthesis},
\qquad
O_{\rm route}\neq\text{unbounded decomposition},
\qquad
O_{\rm translate}\neq\text{representation invention},
\qquad
O_{\rm compress}\neq\text{unrestricted redesign}.
}
\]

Any new operation discovered or proposed after observing ARO-001 results requires a **new prospectively frozen evaluation version**. It cannot be inserted retroactively into ARO-001.

---

## 5. Learned controller

The learner chooses among supplied operations:

\[
\boxed{
\mu_t:
\mathcal H_{t-1}^{\rm admissible}
\longrightarrow
O_t\in\mathcal O.
}
\]

The admissible history may contain only information frozen by the protocol, for example:

- task descriptors when the task is revealed;
- prior operation choices;
- prior predictions and residuals;
- prior operation outputs;
- budget state;
- elapsed time;
- evaluator-supplied challenge metadata explicitly authorized for the learner;
- previous probe or routing outcomes if permitted.

No outcome, future-task label, hidden world identifier, oracle action, or sealed evaluation metadata may leak into the decision history unless the assay variant explicitly permits it.

Control success remains distinct from semantic diagnosis:

\[
\boxed{
\text{correct operation control}
\not\Rightarrow
\text{correct diagnosis of why that operation works}.
}
\]

---

## 6. Two information-timing variants

ARO-001 keeps two scientifically distinct variants separate.

### 6.1 ARO-A — task-conditioned operation control

The task is revealed before the learner chooses the operation:

\[
\boxed{
T_t
\longrightarrow
O_t.
}
\]

Question:

> Given the current consequential question, can the learner choose the supplied operation with the best cost-performance-recovery tradeoff?

ARO-A isolates operation choice for a known question.

### 6.2 ARO-B — preparedness under future-task uncertainty

The operation is chosen before the consequential future task is revealed:

\[
\boxed{
O_t
\longrightarrow
T_{t+1}.
}
\]

Question:

> Can the learner choose an operation that preserves useful future optionality before the next consequential task is known?

ARO-B is closer to the C4 motivation that equal present adequacy need not imply equal future repairability.

### 6.3 No cross-variant claim leakage

Success in ARO-A does not imply success in ARO-B:

\[
\boxed{
\text{task-conditioned operation control}
\not\Rightarrow
\text{future-task preparedness}.
}
\]

ARO-A and ARO-B must be analyzed separately unless a later prospectively frozen experiment explicitly composes them.

---

## 7. Oracle construction

The primary benchmark is an **information-matched operation oracle**.

The governing rule is:

\[
\boxed{
\textbf{oracle advantage may be computational, never informational.}
}
\]

### 7.1 ARO-A oracle

When the current task is known before action, define an evaluator benchmark of the form

\[
\boxed{
o_A^\star(\omega)
\in
\arg\min_{o\in\mathcal O}
\left\{
C(o):
L(o;\omega)\le L_{\rm target}(\omega)
\right\}.
}
\]

The exact loss, cost, tie-breaking rule, and admissible oracle knowledge must be prospectively frozen.

### 7.2 ARO-B oracle

ARO-B must not use a hindsight oracle that observes the realized future task before choosing.

For learner-visible history `h`, the benchmark must act on the same information state:

\[
\boxed{
o_B^\star(h)
\in
\arg\min_{o\in\mathcal O}
\left\{
C(o):
\Pr_{\omega\sim\mathcal D^\star(\cdot\mid h)}
\big(
L(o;\omega)\le L_{\rm target}(\omega)
\big)
\ge1-\delta
\right\}.
}
\]

This form is illustrative. The exact frozen oracle criterion may use a different prospectively specified performance/recovery constraint, but it may not condition on information unavailable to the learner at the decision time.

A clairvoyant oracle may be reported only as a separate upper bound and must not be the primary regret benchmark.

---

## 8. Externally constituted challenge process

The challenge process is evaluator-controlled:

\[
\boxed{
\omega\sim\mathcal D^\star.
}
\]

The learner may generate policy-dependent histories

\[
H^\mu(\omega),
\]

and may causally affect the interactive trajectory where the environment permits it.

What it may not do is select or modify the evaluation law used to judge itself.

The constitutional rule is:

\[
\boxed{
\textbf{The learner may adapt to and causally affect the evaluated trajectory;
the constitution governing how that interaction is judged may not adapt post hoc
to the learner or its observed results.}
}
\]

Before execution, the evaluator constitution must freeze at least:

- challenge/world generator or held-out episode set;
- train/development/final-evaluation partition;
- matched-world families;
- task and shift distributions;
- noise distributions;
- horizon `T`;
- consequence deadlines `H`;
- operation/representation cost accounting;
- success tolerances;
- seed-generation procedure;
- stopping rule;
- metrics;
- oracle definition;
- information access boundary;
- version identifier.

Any post-freeze change produces a new evaluation version rather than silently modifying the existing assay.

---

## 9. Mandatory matched-world gate

ARO-001 is not scientifically admissible without matched worlds that make trivial scalar alarm policies insufficient.

The core condition is:

\[
\boxed{
\mathcal L(H_{\rm pre}\mid W_i)
\approx
\mathcal L(H_{\rm pre}\mid W_j)
\quad\land\quad
o^\star(W_i)\neq o^\star(W_j).
}
\]

The matching target should be as strong as the world construction permits.

At minimum, the worlds should match important pre-operation learner-visible failure statistics such as:

- residual magnitude;
- residual variance;
- recent loss trend;
- cheap/default representation cost;
- elapsed time;
- any obvious task-frequency cue not intended to carry the discrimination.

Stronger versions should match the complete learner-visible pre-operation history law over a finite diagnostic window whenever feasible.

### 9.1 Required interpretation

The gate is intended to block rules like:

\[
\text{large error}
\longrightarrow
\text{spend more representation resources}.
\]

A positive ARO result should instead require evidence that the controller can exploit whatever learner-visible structure legitimately distinguishes the **value of different operations**.

### 9.2 Example operation-heterogeneous world family

An implementation may use a latent state such as

\[
X=(G,I,T),
\]

where `G`, `I`, and `T` denote geometry-like, identity-like, and temporal-like information.

A prospectively frozen matched family might include worlds in which the minimum-cost adequate operation is respectively:

\[
\boxed{
\begin{array}{c|c}
W_G & O_{\rm select}(\Pi_G)\\
W_{GI} & O_{\rm compose}(\Pi_G,\Pi_I)\\
W_R & O_{\rm route}(\Pi_G,\Pi_I)\\
W_D & O_{\rm resolve}(\Pi_G,+1)\\
W_C & O_{\rm compress}
\end{array}
}
\]

This table is illustrative, not yet an implementation freeze. The exact worlds must be separately fixed before execution.

---

## 10. No favored operation class

ARO-001 must not be designed so that one operation family wins by construction except where necessary for matched positive controls.

The scientific null posture is symmetric:

\[
\boxed{
O_{\rm select},
O_{\rm compose},
O_{\rm route},
O_{\rm translate},
O_{\rm resolve},
O_{\rm compress}
\text{ have no prior claim to privileged status.}
}
\]

World construction should include, where feasible:

- cases where each operation is uniquely or near-uniquely cost-effective;
- cases where several operations are equivalent;
- cases where one apparent taxonomy distinction collapses empirically;
- cases where a mixed policy is better than any single fixed operation;
- cases where every supplied operation is inadequate.

The experiment is explicitly allowed to show that some supplied categories are redundant or badly drawn.

---

## 11. Baseline and control family

Before execution, the exact baselines must be frozen. The scientific freeze requires at least the following roles:

### M0 — fixed single-operation controls

One policy per supplied operation class, using that class whenever admissible.

### M1 — cost-matched random operation allocation

Randomly choose among supplied operations subject to matching the learned controller's expected operation cost or a prospectively frozen cost schedule.

### M2 — simple heuristic controller

A low-capacity rule based on residual magnitude, task label, or another prospectively specified scalar cue.

This is the analogue of the residual-threshold control in ARS-001.

### M3 — learned adaptive operation controller

The target policy `mu`.

### M4 — information-matched operation oracle

Primary oracle benchmark as defined above.

Additional controls may be added before the implementation freeze, but none may be added after final evaluation outcomes are inspected without creating a new evaluation version.

---

## 12. Evaluation metrics

ARO-001 is a multi-objective assay. No universal scalar utility is frozen as the scientific result.

The metric family `Y` must prospectively include at least:

\[
\boxed{
\begin{aligned}
L&=\text{predictive / task loss},\\
C&=\text{mean operation and representation cost},\\
T_R&=\text{recovery latency after a consequential shift},\\
P_H&=\Pr(T_{\rm recover}\le H),\\
R_O&=\text{regret to the information-matched operation oracle},\\
F_O&=\text{false or unnecessary expensive-operation rate},\\
U_O&=\text{under-operation rate when richer/different operation is needed},\\
X_{\rm transfer}&=\text{held-out transfer performance}.
\end{aligned}
}
\]

Where operations are heterogeneous, the cost definition must count the actual representation accesses and transformations induced by the operation, not only an operation label.

### 12.1 Oracle-regret view

A generic benchmark quantity is

\[
\boxed{
R_{\rm ARO}(\mu)
=
\mathbb E_{\omega\sim\mathcal D^\star}
\left[
J(\mu;\omega)-J(o^\star;\omega)
\right],
}
\]

where `J` is prospectively frozen.

However, the primary scientific presentation should preserve the underlying Pareto coordinates rather than allowing one scalarization to hide tradeoffs.

### 12.2 Frontier view

Preferred reporting:

\[
\boxed{
\text{distance of learned }\mu
\text{ from the evaluator-defined operation-oracle frontier}
}
\]

across cost, performance, and recovery constraints.

---

## 13. Primary scientific outcomes

ARO-001 is intended to discriminate among several possible empirical geometries.

### Outcome A — category collapse

If two or more supplied operation classes are empirically interchangeable across the frozen challenge family after cost normalization, then the taxonomy is over-refined for that scope.

Earned statement:

\[
\boxed{
\text{the frozen assay does not require those operation distinctions.}
}
\]

Not earned:

\[
\text{those distinctions never matter elsewhere}.
\]

### Outcome B — category retention

If distinct supplied operations are selectively necessary in different matched worlds, the heterogeneity is empirically supported at the frozen scope.

Earned statement:

\[
\boxed{
\text{no single tested operation class suffices across the frozen world family.}
}
\]

### Outcome C — adaptive mixed-operation advantage

If the learned controller approaches the oracle frontier while every fixed-operation policy is materially worse, then adaptive operation control is supported.

This is stronger than any one ARS/APS/SCS-like specialization.

### Outcome D — taxonomy pressure / possible split

If an operation class contains systematically heterogeneous subcases that require different policies or costs, the current category may be too coarse.

ARO-001 may justify a **new prospectively frozen follow-up** that splits the category.

It does not retroactively split the category within the same evaluation.

### Outcome E — supplied-family inadequacy

If all supplied operations fail under a world family that passes the other assay checks, the only immediate result is:

\[
\boxed{
\texttt{SUPPLIED_REPRESENTATION_OPERATION_FAMILY_INADEQUATE}.
}
\]

This does **not** identify a missing operation and does not imply T13.

### Outcome F — apparent missing operation class

If post-run diagnostics repeatedly indicate that failures share structure not captured by any supplied operation contract, the admissible conclusion is:

\[
\boxed{
\text{the current operation taxonomy may be incomplete at this scope}.
}
\]

A named new operation class becomes scientifically testable only in a new prospectively constituted assay.

Thus:

\[
\boxed{
\text{evidence of incompleteness}
\neq
\text{validated new operation class}.
}
\]

---

## 14. Failure-localization map

A failed learned controller must be localized at the shallowest supported layer.

Define the failure candidate set

\[
\boxed{
\mathcal F
=
\{
F_{\mathcal P},
F_{\mathcal O},
F_\mu,
F_{\rm exposure},
F_{\rm deadline},
F_{\rm predictor},
F_{\rm evaluation}
\}.
}
\]

Interpretation:

- `F_P`: supplied representations do not expose the required distinction;
- `F_O`: supplied bounded operations cannot exploit the available representations adequately;
- `F_mu`: controller fails despite adequate supplied representations and operations;
- `F_exposure`: learner-visible history does not contain timely information needed to choose the useful operation;
- `F_deadline`: useful operation exists and is learnable but cannot complete before the consequence deadline;
- `F_predictor`: downstream predictor/executor is inadequate despite correct operation choice;
- `F_evaluation`: world construction, cost accounting, oracle, matching, leakage, or metric design invalidates interpretation.

The governing rule is:

\[
\boxed{
\neg\text{success}
\Rightarrow
\text{localize within }
(\mathcal P,\mathcal O,\mu,\text{exposure},\text{deadline},\text{predictor},\text{evaluation})
}
\]

not

\[
\neg\text{success}
\Rightarrow
\text{T13}.
\]

A deeper revision requires independent discriminating evidence.

---

## 15. Ontology-falsification rule

ARO-001 is not allowed to interpret every result through the supplied taxonomy.

The experiment must permit all of the following:

\[
\boxed{
\begin{array}{rcl}
\text{collapse} &:& \text{two labels behave as one empirical class},\\
\text{retain} &:& \text{labels correspond to distinct required operations},\\
\text{split pressure} &:& \text{one label hides reproducible heterogeneous subcases},\\
\text{incompleteness pressure} &:& \text{none of the supplied labels captures the failure geometry}.
\end{array}
}
\]

The strongest methodological rule is:

\[
\boxed{
\textbf{Do not make our vocabulary determine the answer.}
}
\]

If the taxonomy fails, that is an experimental result, not a protocol defect by default.

---

## 16. Claim ceiling

A positive ARO-001 result may support:

\[
\boxed{
\text{adaptive control can learn useful policies over the supplied representation-operation family}
}
\]

at the frozen scope.

It does **not** by itself establish:

- explicit semantic diagnosis;
- representation invention;
- operation invention;
- universal optimality of the supplied family;
- universal necessity of the empirically successful operation class;
- causal modularity outside the frozen world family;
- safe authority transfer;
- T13 construction success;
- a new permanent OpenCore primitive.

The key non-implications are:

\[
\boxed{
\begin{aligned}
\text{correct operation control}
&\not\Rightarrow
\text{correct failure diagnosis},\\
\text{operation adaptivity}
&\not\Rightarrow
\text{representation construction},\\
\text{supplied-family failure}
&\not\Rightarrow
\text{T13 necessity},\\
\text{taxonomy incompleteness pressure}
&\not\Rightarrow
\text{validated missing operation class}.
\end{aligned}
}
\]

---

## 17. Relationship to ARS / APS / SCS

ARO-001 sits **above** the current specialized assay ideas as a fork detector, not as a new architectural layer.

Potential empirical branches include:

\[
\boxed{
\begin{array}{rcl}
O_{\rm resolve}\text{ dominates} &\Rightarrow& \text{ARS-like specialization may be justified},\\
O_{\rm select}\text{ dominates} &\Rightarrow& \text{APS-like specialization may be justified},\\
O_{\rm compress}\text{ matters} &\Rightarrow& \text{SCS-like specialization may be justified},\\
O_{\rm compose}\text{ matters} &\Rightarrow& \text{multi-view branch},\\
O_{\rm route}\text{ matters} &\Rightarrow& \text{decomposition/routing branch},\\
O_{\rm translate}\text{ matters} &\Rightarrow& \text{conversion branch},\\
\text{mixed optimum} &\Rightarrow& \text{adaptive operation-policy branch},\\
\text{taxonomy fails} &\Rightarrow& \text{localize before naming a new branch}.
\end{array}
}
\]

These arrows are **research decisions conditioned on evidence**, not theorem implications.

ARO-001 does not supersede ARS-001's prospective freeze. ARS-001 remains a valid specialized assay; ARO-001 asks whether depth is actually the right coordinate to privilege in the next empirical program.

---

## 18. Evaluation constitution and provenance requirement

ARO-001 inherits the same constitutional discipline developed for ARS.

The mathematical / statistical result is conditional on the evaluation process being prospectively constituted.

The execution stack is:

\[
\boxed{
\text{scientific freeze}
\rightarrow
\text{evaluation constitution}
\rightarrow
\text{implementation freeze}
\rightarrow
\text{sealed execution}
\rightarrow
\text{audit witness}
\rightarrow
\text{admissible claim}.
}
\]

The evaluator constitution must separate:

\[
\boxed{
\begin{aligned}
C_0 &: \text{what is fixed, when, and by whom/what},\\
C_1 &: \text{what the learner/training process may observe or influence},\\
C_2 &: \text{what immutable provenance proves about execution compliance}.
\end{aligned}
}
\]

The non-interference invariant is:

\[
\boxed{
\textbf{No unauthorized causal path from the evaluated controller,
its training outputs, or post-hoc development results to the final evaluation specification.}
}
\]

A failed constitutional audit invalidates the intended ARO evidentiary claim even if raw performance is high.

---

## 19. Required pre-execution freeze checklist

ARO-001 must remain `NOT_RUN` until a separate implementation/evaluation freeze fixes all of the following:

1. exact representation family `P`;
2. exact bounded operator contracts `O`;
3. exact ARO-A and/or ARO-B variant;
4. exact challenge/world generators `D*`;
5. matched-world construction `M` and matching tolerances;
6. learner-visible history and information timing `I`;
7. controller class `mu` and training procedure;
8. downstream predictors/executors and competency checks;
9. operation and representation cost accounting;
10. oracle construction and tie-breaking;
11. baseline implementations;
12. train/development/final split;
13. seed-generation procedure;
14. horizon and consequence deadlines;
15. metrics `Y` and primary estimands;
16. success/failure thresholds;
17. stopping rule;
18. failure-localization procedure `F`;
19. evaluation constitution / access boundary;
20. immutable audit-witness format;
21. version identifier and amendment rule.

No execution is authorized by this scientific freeze alone.

---

## 20. Frozen status

```text
ARO-001 scientific boundary       FROZEN
favored operation class           NONE
representation family             ABSTRACT ROLE ONLY — IMPLEMENTATION NOT FROZEN
operation family                  ABSTRACT ROLE ONLY — IMPLEMENTATION NOT FROZEN
challenge process                 ABSTRACT ROLE ONLY — IMPLEMENTATION NOT FROZEN
matched worlds                    REQUIRED — IMPLEMENTATION NOT FROZEN
ARO-A / ARO-B                     DISTINCT — EXECUTION CHOICE NOT FROZEN
information-matched oracle        REQUIRED — IMPLEMENTATION NOT FROZEN
evaluation constitution           REQUIRED — NOT YET FROZEN
implementation                    NOT FROZEN
experiment                        NOT RUN
results                           NONE
T13 reopened                      NO
new OpenCore primitive            NO
```

Canonical flag:

\[
\boxed{\texttt{STATUS = NOT\_RUN}}
\]

---

## 21. Final scientific compression

ARO-001 asks:

\[
\boxed{
\textbf{Can adaptive control discover which supplied representational operation
has the best cost-performance-recovery tradeoff for the current challenge?}
}
\]

Its methodological purpose is broader:

\[
\boxed{
\textbf{Do not decide the geometry of representation management in advance.
Construct competing bounded operations, expose them to discriminating matched worlds,
and let failure or dominance tell us which coordinate actually matters.}
}
\]

And its strongest protection is:

\[
\boxed{
\textbf{The experiment is designed so that our own categories are allowed to lose.}
}
\]
