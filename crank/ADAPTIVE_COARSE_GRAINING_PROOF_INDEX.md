# Adaptive Coarse-Graining — Proof Index

**Status:** living theorem index  
**Empirical authority:** none  
**Architectural status:** no new permanent OpenCore primitive or control surface  
**Current proof frontier:** T13 proof-first boundary-expansion sequence closed at stated mathematical scope

This file indexes the post-freeze mathematical results that grew out of the adaptive coarse-graining formulation. It is an index, not a replacement for the individual proof records.

The common conceptual phrase is:

\[
\boxed{
\textbf{adaptive coarse-graining under intervention and revision}
}
\]

The mathematical program remains task-relative and evidence-constrained. It does not posit a universal optimal representation.

---

## 1. Frozen representation ladder

The following are increasingly demanding properties, not implications:

\[
\boxed{
\text{regularity}
\not\Rightarrow
\text{compressibility}
\not\Rightarrow
\text{predictive sufficiency}
\not\Rightarrow
\text{causal relevance}
\not\Rightarrow
\text{causal modularity}.
}
\]

The predictive and revision problems remain separate:

\[
\boxed{
\min_{\Pi}\mathcal C(\Pi)
\quad\text{s.t.}\quad
\operatorname{Loss}_{P,h}(\Pi)\le\epsilon
}
\]

versus an explicitly repair-language-relative revision problem.

No universal repair metric, optionality variable, structural-density variable, or decoding-accessibility variable has been added to OpenCore.

---

## 2. C1 — Coarsest consequence-sufficient quotient

**File:** `C1_COARSEST_CONSEQUENCE_SUFFICIENT_QUOTIENT.md`  
**Status:** `PROVED_AT_STATED_SCOPE`

For a frozen policy/regime `P`, horizon `h`, consequential future variable `Y`, and consequence kernel

\[
K_{P,h}(s,\cdot),
\]

define

\[
s\sim_{P,h}s'
\iff
K_{P,h}(s,\cdot)=K_{P,h}(s',\cdot).
\]

Let

\[
q_{P,h}:\mathcal X\to\mathcal X/{\sim_{P,h}}
\]

be the quotient map.

Then

\[
\boxed{
\Pi\text{ exact-sufficient}
\iff
q_{P,h}=g_\Pi\circ\Pi
}
\]

for a unique map `g_Pi` on the attained image of `Pi`.

Earned:

```text
an exact-sufficient representation may split consequence-equivalent states
but may not merge states with different frozen future consequence laws
```

Finite/discrete corollaries:

\[
|\Pi(\mathcal X)|\ge|\mathcal X/{\sim_{P,h}}|
\]

and, for discrete `X`,

\[
H(q_{P,h}(X))\le H(\Pi(X)).
\]

Scope boundary:

```text
coarsest exact sufficient quotient
!=
universally optimal representation
```

The quotient is relative to `(P,h,Y)`.

---

## 3. C2 — Discarded-distinction deadline impossibility

**File:** `C2_DISCARDED_DISTINCTION_DEADLINE_IMPOSSIBILITY.md`  
**Status:** `PROVED_AT_STATED_SCOPE`

If two states differ in the frozen consequence law,

\[
s_a\not\sim_{P,h}s_b,
\]

and the current representation initially collapses them,

\[
\Pi(s_a)=\Pi(s_b),
\]

while the complete represented adaptive path laws through deadline `H` remain identical,

\[
P_{a,t:H}^{\pi}=P_{b,t:H}^{\pi},
\]

then every represented-history-measurable randomized adjudicator has

\[
\alpha+\beta=1
\]

and therefore

\[
\boxed{
\neg\mathsf{CWC}_{t,H,\delta}(a,b;\pi)
\quad\forall\delta<\tfrac12.
}
\]

The threshold is sharp: under identical path laws, the frozen T12e.5 criterion gives CWC iff `delta >= 1/2`.

Essential boundary:

```text
initial consequential collapse
!=
deadline impossibility
```

A reachable intervention may still re-expose the distinction before the deadline.

---

## 4. C4 — Equal current sufficiency does not imply equal repairability

**File:** `C4_EQUAL_SUFFICIENCY_UNEQUAL_REPAIRABILITY.md`  
**Status:** `PROVED_EXISTENCE_COUNTEREXAMPLE_AT_STATED_SCOPE`

For arbitrary `m >= 1`, let

\[
X=(U,V_1,\ldots,V_m,W_1,\ldots,W_m),
\qquad
Y_0=U.
\]

Define

\[
\Pi_V=(U,V_1,\ldots,V_m),
\qquad
\Pi_W=(U,W_1,\ldots,W_m).
\]

Both are exact-sufficient for the current task, have equal output cardinality, and under uniform independent bits have equal entropy.

Change the task to

\[
Y_1=V=(V_1,\ldots,V_m).
\]

Under one common coordinate-adjunction repair language,

\[
\boxed{
C_{\rm repair}(\Pi_V;Y_1)=0,
\qquad
C_{\rm repair}(\Pi_W;Y_1)=m.
}
\]

Thus

\[
\boxed{
\text{equal current predictive sufficiency}
\not\Rightarrow
\text{equal future repairability}.
}
\]

The repair-cost gap is arbitrarily large even with equal simple current complexity measures.

Important boundary:

```text
identical current partition
!=
proved unequal repair cost
```

The stronger identical-partition claim would require extra implementation/refinement geometry not contained in the extensional quotient.

---

## 5. C3 — Repair + CWC deadline composition

**File:** `C3_REPAIR_CWC_DEADLINE_COMPOSITION.md`  
**Status:** `PROVED_AT_STATED_SCOPE`

Let `T_R` be first time an adequate refinement is reached. Choose a deterministic checkpoint `n < H` and define

\[
R_n=\{T_R\le n\}.
\]

If, under each member of the unresolved pair,

\[
P(T_R>n\mid\mathcal F_t)\le\delta_R
\]

and, conditional on successful repair by `n`, the selection-aware post-repair experiment has CWC-directed error at most `delta_A`, then

\[
\boxed{
P(\text{repair/adjudication failure by }H\mid\mathcal F_t)
\le
\delta_R+(1-\delta_R)\delta_A
\le
\delta_R+\delta_A.
}
\]

Equivalently,

\[
\boxed{
P(\text{correct repair and adjudication by }H\mid\mathcal F_t)
\ge
(1-\delta_R)(1-\delta_A).
}
\]

Stopping-time form: if

\[
T_{\rm rec}=R+A
\]

is repair duration plus post-repair adjudication duration, then

\[
P(T_{\rm rec}>H-t\mid\mathcal F_t)\le\delta_T
\]

and

\[
P(\text{wrong}\mid T_{\rm rec}\le H-t,\mathcal F_t)\le\delta_A
\]

imply

\[
\boxed{
P(\text{operational recovery failure by }H)
\le
\delta_T+(1-\delta_T)\delta_A.
}
\]

The event `T_rec <= H-t` is timely completion only; operational recovery additionally requires correct attribution.

Earned distinction:

\[
\boxed{
\text{eventual repair}
\neq
\text{timely repair}
\neq
\text{correct deadline adjudication}.
}
\]

T13.2 hazard composition: if

\[
P(T_R>n)\le e^{-c_n},
\]

then with post-repair CWC error `delta_A`,

\[
\boxed{
P(\text{deadline failure})
\le
 e^{-c_n}+(1-e^{-c_n})\delta_A.
}
\]

C3 does not prove that repair cost equals repair time, that CWC holds, or that authority follows.

---

## 6. T13.5 — Bounded-risk boundary-expansion synthesis

**File:** `T13_5_BOUNDARY_EXPANSION_SUFFICIENCY.md`  
**Status:** `PROVED_AT_STATED_SCOPE / SYNTHESIS THEOREM`

Fix the T13.1 attainable adequate region

\[
\mathcal B
=
\mathcal R_\varepsilon^\star
\neq\varnothing.
\]

Let `T_R` be the first time an adequate candidate is available and choose a deterministic checkpoint `n < H`.

If, under each member `h` of the unresolved consequential pair,

\[
P_h(T_R>n\mid\mathcal F_\tau)\le\delta_R,
\]

and on successful repair by `n` the post-selection experiment is T13.3-valid and supports the already-frozen CWC adjudicator with conditional directed error at most `delta_A`, then

\[
\boxed{
P_h(\text{boundary-expansion failure by }H\mid\mathcal F_\tau)
\le
\delta_R+(1-\delta_R)\delta_A.
}
\]

Equivalently,

\[
\boxed{
P_h(\text{adequate refinement + correct adjudication by }H\mid\mathcal F_\tau)
\ge
(1-\delta_R)(1-\delta_A).
}
\]

If T13.2 supplies

\[
P_h(T_R>n\mid\mathcal F_\tau)\le e^{-c_n},
\]

then

\[
\boxed{
P_h(\text{failure by }H\mid\mathcal F_\tau)
\le
e^{-c_n}+(1-e^{-c_n})\delta_A.
}
\]

T13.5 targets an adequate **region**, not a unique refinement identity. Membership in that region is an analytic property relative to `P*`; it is not a self-authenticating observation available to the learner.

The observable admission route remains:

```text
E_D
-> selected refinement
-> candidate-dependent post-repair policy
-> selection-aware authorization evidence
-> frozen CWC
-> existing Gamma rule
```

T13.5 certifies bounded-risk statistical preconditions for `Gamma`; it does not compel authority, redefine `Gamma`, or grant authority outside the adjudicated distinction.

Hard boundaries remain:

```text
adequate candidate reached
!=
identifiability restored

selected discovery fit
!=
selection-aware validation

selection-aware validity
!=
CWC

CWC
!=
unscoped authority
```

If the repaired represented path laws remain identical, C2 blocks nontrivial CWC for `delta_A < 1/2`.

The proof-first T13 sequence is therefore closed at its stated mathematical scope:

```text
T13.1  coverage / attainability                    PROVED
T13.2  constructive reachability                  PROVED AT STATED SCOPES
T13.3  selection-aware empirical re-entry         PROVED AT STATED SCOPES
T13.4  selection-naive self-validation firewall   PROVED COUNTEREXAMPLE
T13.5  bounded-risk boundary-expansion synthesis  PROVED AT STATED SCOPE
```

No representation-invention implementation or construction experiment is authorized by this closure.

---

## 7. Derived multi-task quotient observation

No separate theorem file is currently required for this corollary of C1.

For a finite consequential task family

\[
\mathcal T=\{T_1,\ldots,T_m\},
\]

with task relations `~_i`, define

\[
\boxed{
\sim_{\mathcal T}=\bigcap_i\sim_i.
}
\]

The quotient by `~_T` is the coarsest exact representation jointly sufficient for all specified tasks.

Thus task quotients need not be nested, and joint sufficiency may require a strictly finer representation than any one task alone.

Earned interpretation:

```text
task-specific optimality
!=
future-task robustness
```

No monotone-refinement doctrine follows: if tasks cease to be consequential, legitimate coarsening may again be possible.

---

## 8. Music-derived representation observations — not new primitives

The music probes suggested useful derived axes:

\[
\begin{aligned}
S&=\text{current-task sufficiency},\\
R&=\text{repair/re-entry cost},\\
D&=\text{task-relative structural density},\\
U(b)&=\text{recoverable utility under decoding budget }b.
\end{aligned}
\]

No default implication is assumed among them.

The key boundary is

\[
\boxed{
\text{progressive decoding}
\neq
\text{representation repair}.
}
\]

If a distinction is already encoded but computationally expensive to extract, more decoding may reveal it. If the distinction is absent from the operative representation, more computation over that representation alone cannot recover it; re-exposure/refinement is required.

These are conceptual diagnostics only. `D` and `U(b)` are not OpenCore state variables or control surfaces.

---

## 9. Current theorem chain

The current mathematical lineage is:

```text
C1      current task-relative consequence quotient
C4      equal current adequacy can hide unequal repair geometry
T13.1   adequate refinement attainability
T13.2   constructive reachability and timing
T13.3   selection-aware empirical re-entry
T13.4   self-validation firewall
C3      deadline/risk composition of repair and CWC
T13.5   bounded-risk boundary-expansion synthesis
C2      impossibility if represented deadline path laws remain identical
CWC     exact finite-horizon two-sided adjudication criterion
Gamma   scoped authority only after warranted adjudication
```

The compact chain is

\[
\boxed{
\text{quotient}
\to
\text{task change}
\to
\text{repair geometry}
\to
\text{attainability}
\to
\text{reachability}
\to
\text{selection-aware evidence}
\to
\text{deadline-valid CWC}
\to
\Gamma.
}
\]

The central invariant is:

> **A robust abstraction need not keep every distinction active. It must preserve sufficiently probable and timely routes to restore distinctions that may become consequential, and restored distinctions must still pass fresh, selection-aware adjudication before authority follows.**

---

## 10. Current proof boundary

The post-freeze adaptive coarse-graining theorem queue is closed at the intended proof-first scope:

```text
C1 -> C2 -> C4 -> C3 -> T13.5   CLOSED AT STATED MATHEMATICAL SCOPE
```

This is not an empirical closure and does not authorize a representation-invention system.

The next legitimate work, if resumed, must be explicitly scoped as either:

1. theorem refinement/counterexample against the frozen statements; or
2. a separately authorized empirical implementation/validation program.

No further conceptual layer is implied by the proof closure.