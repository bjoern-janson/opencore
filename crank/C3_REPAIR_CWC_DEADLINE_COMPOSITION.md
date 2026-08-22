# C3 — Repair + CWC Deadline Composition

**Status:** `PROVED_AT_STATED_SCOPE`  
**Scope:** finite-horizon composition of repair/re-entry timing and already-frozen CWC adjudication risk  
**Empirical authority added:** none  
**New architectural primitive:** none  
**CWC definition changed:** no  
**T13.5 proved by this note:** no  
**Construction experiment authorized:** no

C1 identified the coarsest exact consequence-sufficient quotient for a frozen task. C4 showed that equal current predictive sufficiency need not imply equal future repairability. T13.1–T13.3 separated refinement attainability, constructive reachability, and selection-aware re-entry. C2 showed that if a consequential distinction remains absent from the entire represented deadline experiment, nontrivial CWC is impossible.

C3 now proves the elementary but operationally important composition step:

> **A repaired distinction is operationally recoverable only if a statistically legitimate adjudication can also finish correctly before the consequence-relevant deadline.**

The theorem does not turn repair cost into time, and it does not redefine CWC. It composes a repair/re-entry deadline event with the existing CWC error guarantee.

The central distinction is:

```text
repair attained
!=
timely adjudication completed
!=
correct adjudication by the deadline
```

---

## 1. Setup

Fix:

- a current time `t`;
- a consequence-relevant deadline `H > t`;
- an unresolved consequential pair `(i,j)`;
- the current information sigma-field `F_t`;
- a repair/refinement process;
- a post-repair experiment that is admissible under the T13.3 selection-aware re-entry condition;
- the already-frozen CWC terminal testing criterion.

Let

\[
T_R
\]

be the first time at which an adequate refinement for the pair has been reached. `T_R` is a stopping time with respect to the enlarged repair/search filtration. If no adequate refinement is ever reached, set `T_R = infinity`.

For a deterministic checkpoint

\[
t < n < H,
\]

define the repair-success event

\[
\boxed{
R_n := \{T_R \le n\}.
}
\]

The post-repair protocol may wait until time `n` before beginning the frozen adjudication window. This avoids silently treating the random repair time as though the fixed-horizon CWC certificate had already been proved uniformly over all possible stopping times.

For hypothesis `h in {i,j}`, let

\[
W_h
\]

be the event that the terminal adjudicator makes the wrong attribution under `h` by deadline `H`, conditional on the repaired experiment being available at checkpoint `n`.

Define the overall repair/adjudication failure event

\[
\boxed{
F_h := R_n^c \cup (R_n \cap W_h).
}
\]

Thus failure means either:

1. an adequate refinement was not reached by the checkpoint; or
2. repair succeeded in time, but the subsequent statistically legitimate adjudication was wrong.

---

# 2. C3.1 — Fixed-checkpoint deadline composition

## Theorem C3.1 — Repair deadline + conditional CWC error compose

Fix error budgets

\[
\delta_R,\delta_A \in [0,1].
\]

Suppose that, for each `h in {i,j}`,

\[
\boxed{
P_h(T_R>n\mid\mathcal F_t)\le\delta_R
}
\]

almost surely.

Suppose further that on `R_n`, after accounting for the selection mechanism that produced the refinement as required by T13.3, the post-repair path experiment from `n` through `H` admits a CWC-valid terminal adjudicator whose conditional directed error satisfies

\[
\boxed{
P_h(W_h\mid R_n,\mathcal F_t)\le\delta_A.
}
\]

Then

\[
\boxed{
P_h(F_h\mid\mathcal F_t)
\le
\delta_R+(1-\delta_R)\delta_A
\le
\delta_R+\delta_A.
}
\]

Therefore, for each hypothesis,

\[
\boxed{
P_h(\text{correct repair-and-adjudication by }H\mid\mathcal F_t)
\ge
(1-\delta_R)(1-\delta_A).
}
\]

### Proof

Let

\[
q_h:=P_h(R_n^c\mid\mathcal F_t).
\]

By assumption,

\[
0\le q_h\le\delta_R.
\]

Because `R_n^c` and `R_n cap W_h` are disjoint,

\[
\begin{aligned}
P_h(F_h\mid\mathcal F_t)
&=P_h(R_n^c\mid\mathcal F_t)
 +P_h(R_n\cap W_h\mid\mathcal F_t)\\
&=q_h
 +(1-q_h)P_h(W_h\mid R_n,\mathcal F_t)\\
&\le q_h+(1-q_h)\delta_A.
\end{aligned}
\]

For `delta_A <= 1`, the function

\[
f(q)=q+(1-q)\delta_A
\]

is nondecreasing in `q`. Hence

\[
P_h(F_h\mid\mathcal F_t)
\le
\delta_R+(1-\delta_R)\delta_A.
\]

Finally,

\[
\delta_R+(1-\delta_R)\delta_A
=
\delta_R+\delta_A-\delta_R\delta_A
\le
\delta_R+\delta_A.
\]

Taking complements gives

\[
P_h(F_h^c\mid\mathcal F_t)
\ge
(1-\delta_R)(1-\delta_A).
\]

`F_h^c` is exactly the event that repair is available by `n` and the subsequent adjudication is correct by `H`. `square`

---

## Corollary C3.2 — Union-bound form under weaker joint control

If instead one knows only

\[
P_h(R_n^c\mid\mathcal F_t)\le\delta_R
\]

and the unconditional-on-success joint error bound

\[
P_h(R_n\cap W_h\mid\mathcal F_t)\le\delta_A,
\]

then

\[
\boxed{
P_h(F_h\mid\mathcal F_t)
\le
\delta_R+\delta_A.
}
\]

This is the plain union/decomposition bound. The sharper multiplicative correction in Theorem C3.1 requires the conditional error statement on the repair-success event.

---

# 3. Exact relation to CWC

C3 does not replace the frozen CWC definition.

For the repaired candidate and its selection-aware post-repair policy `pi+`, let the path laws from checkpoint `n` through deadline `H` be

\[
P_{i,n:H}^{\pi^+},
\qquad
P_{j,n:H}^{\pi^+}.
\]

The already-frozen closed-world certificate remains

\[
\boxed{
\mathsf{CWC}_{n,H,\delta_A}(i,j;\pi^+)
\iff
\beta_{1-\delta_A}
\left(
P_{i,n:H}^{\pi^+},
P_{j,n:H}^{\pi^+}
\right)
\le\delta_A.
}
\]

C3 assumes that the evidence/path laws supplied to this certificate are statistically legitimate after adaptive refinement selection, as required by T13.3.

Thus the chain is

```text
repair reached by n
-> selection-aware post-repair experiment
-> existing CWC at risk delta_A
-> composition with repair miss risk delta_R
```

not

```text
repair reached
-> automatically validated.
```

---

# 4. C3.2 — Stopping-time operational recoverability

The fixed-checkpoint theorem separates the repair stage from a frozen adjudication window. A second formulation packages the timing into a total recovery duration without confusing deadline completion with correctness.

Measure time from the current time `t`.

Let

\[
R\ge0
\]

be the elapsed duration until an adequate refinement is reached.

After repair, let

\[
A\ge0
\]

be the additional elapsed duration required for the selection-aware post-repair experiment to reach its adjudication point.

Define

\[
\boxed{
T_{\rm rec}:=R+A.
}
\]

Let the available consequence budget be

\[
\boxed{
B:=H-t.
}
\]

The event

\[
\{T_{\rm rec}\le B\}
\]

means only that the repair-plus-adjudication procedure finishes by the deadline. It does **not** by itself mean that the terminal attribution is correct.

For hypothesis `h`, let `W_h` again denote wrong attribution.

Define operational recovery success as

\[
\boxed{
G_h
:=
\{T_{\rm rec}\le B\}\cap W_h^c.
}
\]

### Theorem C3.3 — Timely completion + conditional adjudication validity imply operational recovery

Suppose, for each `h in {i,j}`,

\[
\boxed{
P_h(T_{\rm rec}>B\mid\mathcal F_t)
\le\delta_T
}
\]

and

\[
\boxed{
P_h(W_h\mid T_{\rm rec}\le B,\mathcal F_t)
\le\delta_A.
}
\]

Then

\[
\boxed{
P_h(G_h^c\mid\mathcal F_t)
\le
\delta_T+(1-\delta_T)\delta_A
\le
\delta_T+\delta_A,
}
\]

and therefore

\[
\boxed{
P_h(G_h\mid\mathcal F_t)
\ge
(1-\delta_T)(1-\delta_A).
}
\]

### Proof

Let

\[
q_h:=P_h(T_{\rm rec}>B\mid\mathcal F_t)\le\delta_T.
\]

The operational failure event is the disjoint union

\[
G_h^c
=
\{T_{\rm rec}>B\}
\cup
\bigl(\{T_{\rm rec}\le B\}\cap W_h\bigr).
\]

Hence

\[
\begin{aligned}
P_h(G_h^c\mid\mathcal F_t)
&=q_h
 +(1-q_h)
 P_h(W_h\mid T_{\rm rec}\le B,\mathcal F_t)\\
&\le q_h+(1-q_h)\delta_A\\
&\le\delta_T+(1-\delta_T)\delta_A.
\end{aligned}
\]

Taking complements proves the claim. `square`

---

# 5. Definition — operational recoverability at deadline risk delta

C3 does not add a new OpenCore state variable or control surface. For compact theorem statements, however, it is useful to name the derived event-level property.

For a consequential pair under hypothesis `h`, say the distinction is **operationally recoverable by deadline `H` at risk `delta`** if

\[
\boxed{
P_h(
\text{selection-aware correct adjudication completed by }H
\mid\mathcal F_t
)
\ge1-\delta.
}
\]

For two-sided recovery, require the bound under both members of the pair.

By Theorem C3.3, a sufficient condition is

\[
\boxed{
\delta_T+(1-\delta_T)\delta_A\le\delta.
}
\]

The looser but simpler sufficient budget is

\[
\boxed{
\delta_T+\delta_A\le\delta.
}
\]

This is a derived deadline/risk property, not a fourth adaptive control surface.

---

# 6. Three temporal notions must remain distinct

C3 preserves the following hierarchy:

### 6.1 Repair existence

\[
\boxed{
P(T_R<\infty\mid\mathcal F_t)>0.
}
\]

This says only that repair can occur with positive probability eventually.

### 6.2 Timely repair reachability

For a repair checkpoint `n`,

\[
\boxed{
P(T_R\le n\mid\mathcal F_t)
\ge1-\delta_R.
}
\]

This says an adequate refinement is likely to be reached by the time reserved for adjudication.

### 6.3 Operational recovery

\[
\boxed{
P(
\text{correct selection-aware adjudication by }H
\mid\mathcal F_t
)
\ge1-\delta.
}
\]

This is the consequential property.

Therefore

\[
\boxed{
\text{repair existence}
\neq
\text{timely repair reachability}
\neq
\text{operational recovery}.
}
\]

In particular,

\[
P(T_R<\infty)=1
\]

is compatible with

\[
P(\text{correct adjudication by }H)=0.
\]

A trivial witness is a deterministic repair time strictly after the deadline.

Thus:

\[
\boxed{
\text{eventual correction}
\not\Rightarrow
\text{correction before consequential leverage expires}.
}
\]

---

# 7. Composition with T13.2 reachability bounds

T13.2 supplies explicit finite-horizon bounds for reaching a fixed nonempty adequate refinement region.

Let `T_R` be the first hit time and suppose the T13.2 pre-hit hazard satisfies

\[
H_n\ge c_n
\quad\text{on }\{T_R>n\}.
\]

Then T13.2 gives

\[
\boxed{
P(T_R>n\mid\mathcal F_t)
\le e^{-c_n}.
}
\]

Set

\[
\delta_R(n):=e^{-c_n}.
\]

If the selection-aware post-repair experiment from `n` to `H` satisfies

\[
\mathsf{CWC}_{n,H,\delta_A},
\]

then C3.1 gives

\[
\boxed{
P(\text{repair/adjudication failure by }H\mid\mathcal F_t)
\le
 e^{-c_n}
 +(1-e^{-c_n})\delta_A.
}
\]

Hence T13.2's constructive reachability bound and CWC's adjudication risk combine without identifying them:

\[
\boxed{
\text{construction risk}
\neq
\text{adjudication risk},
}
\]

but their deadline failure probabilities can be composed.

---

# 8. Relation to C4

C4 proved, under one explicit common repair language, that two representations can be equally sufficient for the current task yet have repair costs

\[
C_{\rm repair}(\Pi_1;Y_1)
\neq
C_{\rm repair}(\Pi_2;Y_1).
\]

C3 does not identify repair cost with repair time.

A translation from C4's repair cost into a distribution for `T_R` requires an explicit execution model for the repair language. Once such a model is frozen, different repair geometries can induce different timely-recovery probabilities.

Therefore the theorem-level statement is deliberately conditional:

\[
\boxed{
\text{equal present sufficiency}
\not\Rightarrow
\text{equal future repair geometry},
}
\]

and, under an execution model where that geometry changes the law of `T_R`, it may yield unequal operational recovery probabilities.

C3 itself does not claim such a mapping universally.

---

# 9. Relation to C2

C2 supplies the hard impossibility boundary.

If after the attempted refinement/re-entry process the represented deadline path laws remain identical,

\[
P_{i,n:H}^{\pi^+}=P_{j,n:H}^{\pi^+},
\]

then for every

\[
\delta_A<\tfrac12,
\]

nontrivial CWC is impossible.

Therefore C3 cannot manufacture a small deadline-risk budget from repair timing alone.

Even perfect repair reachability,

\[
\delta_R=0,
\]

is insufficient when the post-repair experiment remains non-identifying.

Thus:

\[
\boxed{
\text{timely repair}
\not\Rightarrow
\text{timely adjudicability}.
}
\]

---

# 10. Relation to T13.3 selection-aware re-entry

C3 assumes the evidence supplied to CWC remains calibrated under the adaptive selection mechanism that produced the refinement.

T13.3 already established sufficient routes:

```text
R1  prospective/fresh evidence under a calibrated candidate-indexed kernel
R2  explicit post-selection inference under the actual conditional law
R3  sequentially valid evidence under the candidate-dependent adaptive path law
```

C3 adds no fourth route.

The valid chain is

\[
\boxed{
E_D
\to r
\to \pi^+
\to E_A^{\rm selection-aware}
\to \mathsf{CWC}
\to \text{deadline composition}.
}
\]

The invalid shortcut remains

\[
\boxed{
E_D\to r\to\Gamma.
}
\]

---

# 11. The operating objective becomes a deadline/risk constraint

The earlier informal design objective was

\[
\min_{\Pi_k}\mathcal C_{\rm operating}(\Pi_k)
\]

subject to a vague requirement that important distinctions remain cheap to restore.

C3 makes the consequential constraint probabilistic and temporal.

For each consequential task `T` with deadline `H_T` and allowed total failure risk `delta_T`, require

\[
\boxed{
P(
\text{correct selection-aware re-entry and adjudication for }T
\text{ by }H_T
)
\ge1-\delta_T.
}
\]

Equivalently, under a decomposition into deadline-miss risk `delta_{time,T}` and CWC error `delta_{A,T}`, it is sufficient that

\[
\boxed{
\delta_{time,T}
+(1-\delta_{time,T})\delta_{A,T}
\le\delta_T.
}
\]

The looser sufficient constraint

\[
\delta_{time,T}+\delta_{A,T}\le\delta_T
\]

may be used when only union-bound components are available.

This does **not** imply that all distinctions should be kept active. It quantifies the alternative:

```text
low standing representational cost
+
sufficient probability of timely repair/re-entry
+
selection-aware deadline-valid adjudication
```

---

# 12. What C3 proves

At its stated scope, C3 proves:

\[
\boxed{
\text{repair deadline risk}
+
\text{conditional adjudication risk}
\Longrightarrow
\text{an explicit total deadline failure bound}.
}
\]

More sharply,

\[
\boxed{
\delta_{\rm total}
\le
\delta_R+(1-\delta_R)\delta_A.
}
\]

It also proves the stopping-time version:

\[
\boxed{
P(T_{\rm rec}>H-t)\le\delta_T
\quad\land\quad
P(\text{wrong}\mid T_{\rm rec}\le H-t)\le\delta_A
}
\]

implies

\[
\boxed{
P(\text{operational recovery failure by }H)
\le
\delta_T+(1-\delta_T)\delta_A.
}
\]

The central earned distinction is:

\[
\boxed{
\text{eventual repair}
\neq
\text{timely repair}
\neq
\text{correct deadline adjudication}.
}
\]

---

# 13. What C3 does not prove

C3 does **not** prove:

1. that any adequate refinement exists;
2. that any constructor can reach one;
3. that repair cost equals repair time;
4. that selection-naive evidence becomes valid after repair;
5. that CWC holds for any post-repair experiment;
6. that any particular distinction is worth preserving;
7. that operational recovery requires a new OpenCore control surface;
8. that authority follows automatically from successful adjudication;
9. that T13.5 is already proved.

Those boundaries remain exactly where the earlier results placed them.

---

# 14. The post-freeze theorem chain

The adaptive coarse-graining / boundary-expansion chain is now:

\[
\boxed{
\begin{array}{rcl}
C1&:&\text{current consequence-sufficient quotient}\\
C4&:&\text{current adequacy does not determine future repairability}\\
T13.1&:&\text{adequate refinement attainability}\\
T13.2&:&\text{constructive reachability / timing}\\
T13.3&:&\text{selection-aware empirical re-entry}\\
C3&:&\text{repair timing + CWC risk composition}\\
C2&:&\text{deadline impossibility if represented path laws remain identical}\\
CWC&:&\text{exact finite-horizon adjudication criterion}\\
\Gamma&:&\text{scoped authority, only after the preceding gates.}
\end{array}
}
\]

C3 supplies the missing quantitative meaning of:

> **A discarded consequential distinction is acceptable only when the repair/re-entry process and a fresh, selection-aware adjudication remain sufficiently likely to complete correctly before the consequence-relevant deadline.**

---

# 15. Next theorem target

C3 is intended to feed T13.5; it does not replace it.

The next proof target is therefore:

\[
\boxed{
\textbf{T13.5 — minimal sufficient boundary-expansion / re-entry theorem.}
}
\]

T13.5 should compose only already-earned gates:

```text
attainable adequate region
-> sufficiently probable timely construction
-> selection-aware valid post-selection evidence
-> deadline-valid CWC
-> scoped authority permitted by Gamma
```

No representation-invention experiment or new architecture is authorized by C3.
