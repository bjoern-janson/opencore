# T13.5 — Bounded-Risk Boundary-Expansion Re-entry Sufficiency

**Status:** `PROVED_AT_STATED_SCOPE / SYNTHESIS THEOREM`  
**Scope:** Mathematical Core boundary-expansion layer only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**Constructor implementation added:** none  
**Construction experiment authorized:** no  
**CWC definition changed:** no  
**Gamma definition changed:** no

T13.5 closes the proof-first boundary-expansion sequence by composing only already-earned gates:

- T13.1: an adequate refinement region is actually attainable;
- T13.2: the repair/search process reaches that region with controlled deadline risk;
- T13.3: evidence used after adaptive candidate selection remains calibrated under the selection mechanism;
- T13.4: selection-naive reuse of discovery evidence is not generally valid;
- C3: repair/re-entry deadline risk composes with post-repair CWC error;
- frozen CWC: the repaired path experiment supports bounded-error two-sided adjudication;
- existing `Gamma`: any authority transition remains scoped by the already-frozen governance rule.

The theorem introduces no new object.

Its central result is:

\[
\boxed{
\Pr_h(
\text{adequate refinement reached and correctly adjudicated by }H
\mid \mathcal F_\tau)
\ge
(1-\delta_R)(1-\delta_A)
}
\]

for each member `h` of the unresolved consequential pair, under the stated gates below.

Equivalently,

\[
\boxed{
\Pr_h(
\text{boundary-expansion re-entry failure by }H
\mid \mathcal F_\tau)
\le
\delta_R+(1-\delta_R)\delta_A.
}
\]

This is a sufficient theorem. `Minimal` here means that no new architectural layer is added; it does **not** claim assumption-minimality among all possible boundary-expansion procedures.

---

## 1. Setup

Condition on a boundary-exhaustion history

\[
\mathcal F_\tau.
\]

Let `R` be the frozen refinement language, let `P*` denote the target empirical law/family used in the T13.1 adequacy criterion, and fix tolerance

\[
\varepsilon\ge0.
\]

Define the adequate region

\[
\boxed{
\mathcal B
:=
\mathcal R_\varepsilon^\star
=
\{r\in\mathcal R:
\rho(P^\star,Q_r)\le\varepsilon\}.
}
\]

### Analytic status of `B`

Membership in `B` is an analytic relation to `P*`. The learner is **not** assumed to observe the event

\[
r\in\mathcal B
\]

as a self-authenticating certificate.

This distinction is essential:

```text
candidate is adequate relative to the analysis
!=
learner has statistically warranted authorization for that candidate
```

The authorization route remains selection-aware evidence followed by the already-frozen CWC machinery.

Assume

\[
\boxed{
\mathcal B\neq\varnothing.
}
\]

This is the T13.1 attainability gate.

Let the adaptive constructor/search process produce candidates. Define the first calendar/adaptive time at which an adequate candidate is available:

\[
\boxed{
T_R
:=
\inf\{s>\tau:r_s\in\mathcal B\},
}
\]

with `T_R = infinity` if no adequate candidate is ever reached.

If the underlying T13.2 search is indexed by proposal number rather than physical/calendar time, `T_R` denotes the induced availability time of the first adequate proposal. T13.5 does not identify proposal count with elapsed time; it requires only the finite-horizon reachability bound stated below.

Fix a consequence deadline

\[
H>\tau
\]

and a deterministic repair checkpoint

\[
\tau<n<H.
\]

Define

\[
\boxed{
R_n:=\{T_R\le n\}.
}
\]

On `R_n`, let `R` (now capitalized as a random selected refinement when no confusion with the language arises) denote a measurable selected adequate candidate available by the checkpoint; for example, the first hit. Uniqueness is not assumed or required.

Fix an unresolved consequential pair

\[
(i,j).
\]

For each hypothesis `h in {i,j}`, let `P_h` denote the corresponding law of the full adaptive process conditional on the boundary history.

After the candidate is selected, let the post-repair policy/protocol be

\[
\pi^+_R,
\]

and let the resulting authorization evidence/path experiment from checkpoint `n` through deadline `H` be the input to the already-frozen CWC test.

---

# 2. The T13.5 gates

## Gate G1 — Attainable adequate region

\[
\boxed{
\mathcal B\neq\varnothing.
}
\]

No unique `r*` is required. T13.5 targets a region, not an identity.

---

## Gate G2 — Timely constructive reachability

For each `h in {i,j}`, require

\[
\boxed{
P_h(T_R>n\mid\mathcal F_\tau)
\le
\delta_R
}
\]

almost surely, for some

\[
\delta_R\in[0,1].
\]

This is the finite-horizon form supplied by T13.2 or by any stronger reachability result compatible with its scope.

For example, if the T13.2 pre-hit hazard certificate yields

\[
H_n\ge c_n
\quad\text{on }\{T_R>n\},
\]

then one may take

\[
\boxed{
\delta_R=e^{-c_n}.
}
\]

Positive support or eventual reachability alone is insufficient for this gate.

---

## Gate G3 — Selection-aware empirical re-entry

Let

\[
\mathcal S
\]

be the selection history that produced the candidate/protocol used after repair.

The post-repair evidence must satisfy a T13.3-admissible calibration condition under the actual selection mechanism. This may be obtained through, for example:

- prospective/fresh evidence under the correctly specified candidate-indexed kernel;
- explicit post-selection conditioning under the actual selected-candidate law;
- a sequentially valid test/e-process under the candidate-dependent adaptive path law.

No literal sample-disjointness requirement is imposed.

The required boundary is:

\[
\boxed{
\text{fixed-candidate validity}
\not\Rightarrow
\text{selected-candidate validity}.
}
\]

Thus T13.4's forbidden shortcut remains forbidden:

```text
E_D -> selected r -> reuse fixed-r calibration on E_D -> authority
```

---

## Gate G4 — Conditional post-repair CWC

On `R_n`, after the T13.3 selection-aware gate has made the post-repair path law statistically legitimate, require that the consequence-relevant live pair `(i,j)` admit a terminal CWC-valid adjudicator over the remaining window `n:H` with directed error at most

\[
\delta_A\in[0,1].
\]

Equivalently, for the selected candidate/protocol, the conditional post-repair path laws satisfy the already-frozen two-sided testing criterion at level `delta_A`.

Operationally, let `W_h` be the event that the terminal adjudicator makes the wrong attribution under hypothesis `h`. Require

\[
\boxed{
P_h(W_h\mid R_n,\mathcal F_\tau)
\le
\delta_A
}
\]

for both

\[
h\in\{i,j\}.
\]

When expressed directly through the frozen certificate, the relevant candidate-conditioned path experiment must satisfy

\[
\mathsf{CWC}_{n,H,\delta_A}(i,j;\pi_R^+).
\]

T13.5 does not redefine `CWC`; it assumes the existing certificate on the selection-aware post-repair experiment.

---

# 3. Main synthesis theorem

## Theorem 13.5.1 — Bounded-risk successful boundary-expansion re-entry

Assume Gates G1–G4.

For each `h in {i,j}`, define the boundary-expansion failure event

\[
\boxed{
F_h
:=
R_n^c
\cup
(R_n\cap W_h).
}
\]

Then

\[
\boxed{
P_h(F_h\mid\mathcal F_\tau)
\le
\delta_R+(1-\delta_R)\delta_A
\le
\delta_R+\delta_A.
}
\]

Equivalently,

\[
\boxed{
P_h(
R_n\cap W_h^c
\mid\mathcal F_\tau)
\ge
(1-\delta_R)(1-\delta_A).
}
\]

Thus, under each member of the unresolved pair, an adequate refinement is available by checkpoint `n` and the resulting selection-aware CWC adjudication is correct by deadline `H` with probability at least

\[
\boxed{
(1-\delta_R)(1-\delta_A).
}
\]

### Proof

By Gate G2,

\[
q_h
:=
P_h(R_n^c\mid\mathcal F_\tau)
\le
\delta_R.
\]

By Gate G4, after Gate G3 has legitimized the selected post-repair experiment,

\[
P_h(W_h\mid R_n,\mathcal F_\tau)
\le
\delta_A.
\]

The two pieces of `F_h` are disjoint, so

\[
\begin{aligned}
P_h(F_h\mid\mathcal F_\tau)
&=
P_h(R_n^c\mid\mathcal F_\tau)
+
P_h(R_n\cap W_h\mid\mathcal F_\tau)\\
&=
q_h
+(1-q_h)
P_h(W_h\mid R_n,\mathcal F_\tau)\\
&\le
q_h+(1-q_h)\delta_A.
\end{aligned}
\]

Because

\[
q\mapsto q+(1-q)\delta_A
\]

is nondecreasing on `[0,1]`,

\[
P_h(F_h\mid\mathcal F_\tau)
\le
\delta_R+(1-\delta_R)\delta_A.
\]

Taking complements yields

\[
P_h(R_n\cap W_h^c\mid\mathcal F_\tau)
\ge
(1-\delta_R)(1-\delta_A).
\]

This is exactly C3 instantiated with the T13.1–T13.3 boundary-expansion gates. `square`

---

# 4. Corollary 13.5.2 — T13.2 hazard-to-re-entry bound

Suppose T13.2 supplies the finite-horizon hazard certificate

\[
P_h(T_R>n\mid\mathcal F_\tau)
\le
e^{-c_n}
\]

under each `h`.

Then Theorem 13.5.1 gives

\[
\boxed{
P_h(F_h\mid\mathcal F_\tau)
\le
e^{-c_n}+(1-e^{-c_n})\delta_A.
}
\]

Equivalently,

\[
\boxed{
P_h(
\text{adequate refinement + correct adjudication by }H
\mid\mathcal F_\tau)
\ge
(1-e^{-c_n})(1-\delta_A).
}
\]

This is the explicit path from constructor proposal mass to deadline-valid re-entry risk.

---

# 5. Corollary 13.5.3 — Stopping-time operational form

Let

\[
T_{\rm rec}
\]

be the total elapsed duration from boundary time `tau` until both:

1. an adequate refinement is reached; and
2. the selection-aware post-repair adjudication reaches its terminal decision point.

The event

\[
\{T_{\rm rec}\le H-\tau\}
\]

means timely completion only.

Suppose, under each `h`,

\[
P_h(T_{\rm rec}>H-\tau\mid\mathcal F_\tau)
\le
\delta_T
\]

and

\[
P_h(
\text{wrong adjudication}
\mid
T_{\rm rec}\le H-\tau,
\mathcal F_\tau
)
\le
\delta_A,
\]

where the latter guarantee is selection-aware and CWC-valid.

Then

\[
\boxed{
P_h(
\text{operational boundary-expansion failure by }H
\mid\mathcal F_\tau)
\le
\delta_T+(1-\delta_T)\delta_A.
}
\]

Therefore

\[
\boxed{
\text{eventual construction}
\neq
\text{timely re-entry}
\neq
\text{correct deadline adjudication}.
}
\]

This is C3's stopping-time form applied to the complete T13 boundary-expansion pipeline.

---

# 6. Adequacy region does not imply unique refinement identity

T13.5 never assumes

\[
\exists!\,r^\star\in\mathcal R.
\]

There may be many candidates satisfying

\[
\rho(P^\star,Q_r)\le\varepsilon.
\]

The target is therefore

\[
\boxed{
\mathcal B=\mathcal R_\varepsilon^\star,
}
\]

not a unique candidate label.

This matters because the theorem certifies region entry plus subsequent empirical adjudication. It does not claim that boundary pressure identifies a unique ontological representation.

Thus:

\[
\boxed{
\text{adequate empirical refinement}
\neq
\text{unique refinement identity}
\neq
\text{universal causal truth}.
}
\]

---

# 7. Authority corollary — statistical preconditions, not automatic permission

T13.5 ends statistically at successful deadline-valid adjudication.

Let the already-existing authority map `Gamma` specify what scoped permission, if any, may follow from that adjudication.

If `Gamma` is configured so that:

1. no boundary-generated candidate receives authority merely from discovery/selection;
2. the relevant permission is enabled only after the selection-aware CWC outcome required above; and
3. the granted permission does not exceed the distinction actually adjudicated,

then Theorem 13.5.1 provides the bounded-risk statistical preconditions for that `Gamma` transition by deadline `H`.

Symbolically:

\[
\boxed{
E_D
\to
R
\to
\pi_R^+
\to
E_A^{\rm selection-aware}
\to
\mathsf{CWC}
\to
\Gamma.
}
\]

The theorem does **not** prove that `Gamma` must grant authority, that any particular permission is correct outside the adjudicated scope, or that the governance implementation itself is error-free.

The existing invariant remains:

\[
\boxed{
\text{authority scope}
\le
\text{warranted discrimination scope}.
}
\]

---

# 8. Hard obstruction inherited from C2

Suppose the repaired candidate is reached, but the complete represented post-repair path laws remain identical through deadline `H`:

\[
P_{i,n:H}^{\pi_R^+}
=
P_{j,n:H}^{\pi_R^+}.
\]

Then C2 gives

\[
\neg\mathsf{CWC}_{n,H,\delta_A}(i,j;\pi_R^+)
\qquad
\forall\delta_A<\tfrac12.
\]

Therefore Gate G4 cannot hold at any nontrivial two-sided risk level.

So:

\[
\boxed{
\text{refinement reached}
\not\Rightarrow
\text{identifiability restored}.
}
\]

T13.5 does not bypass representational or experimental foreclosure.

---

# 9. Firewall inherited from T13.4

T13.5 also cannot replace Gate G3 with selection-naive reuse of discovery evidence.

T13.4 already provides a finite counterexample in which the candidate class contains the true law, adaptive selection achieves arbitrarily good discovery fit, yet fixed-candidate calibration fails after selection.

Therefore the invalid chain remains

\[
\boxed{
E_D
\to
R
\to
\text{reuse }E_D\text{ under fixed-}R\text{ calibration}
\to
\Gamma.
}
\]

The valid theorem chain is instead

\[
\boxed{
E_D
\to
R
\to
\pi_R^+
\to
E_A^{\rm selection-aware}
\to
\mathsf{CWC}
\to
\Gamma.
}
\]

---

# 10. Exact claim ceiling

T13.5 proves only a sufficient bounded-risk re-entry statement at the stated scope.

It does **not** prove:

1. boundary exhaustion identifies the correct successor representation;
2. the adequate region contains a unique candidate;
3. `rho <= epsilon` implies ontological or causal truth;
4. every constructor can reach the adequate region;
5. eventual reachability implies timely reachability;
6. discovery evidence must always be disjoint from authorization evidence;
7. selection-aware validity implies CWC;
8. CWC implies authority outside its adjudicated distinction;
9. repair cost equals repair time;
10. the C1 coarsest current quotient is optimal for unknown future tasks;
11. T13.5 supplies an implementation, constructor, or empirical demonstration;
12. any new permanent OpenCore surface is required.

The theorem also does not claim to be assumption-minimal among all conceivable valid re-entry procedures.

---

# 11. Final T13 boundary-expansion chain

At the theorem level, the boundary-expansion sequence is now:

\[
\boxed{
\begin{array}{rcl}
\text{T13.1} &:& \mathcal R_\varepsilon^\star\neq\varnothing\\
\downarrow&&\\
\text{T13.2} &:& \Pr(T_R\le n\mid\mathcal F_\tau)\ge1-\delta_R\\
\downarrow&&\\
\text{T13.3} &:& E_A\text{ remains calibrated after candidate selection}\\
\downarrow&&\\
\text{CWC/C3} &:& \text{correct adjudication by }H\text{ with composed risk}\\
\downarrow&&\\
\Gamma &:& \text{only the already-permitted scoped authority may follow.}
\end{array}
}
\]

T13.4 remains the firewall showing why the T13.3 selection-aware gate cannot be replaced by naive self-validation.

The compact admission rule is:

\[
\boxed{
\textbf{
A boundary-generated refinement may acquire scoped authority only after
an attainable candidate has been reached in time and the resulting
selection-aware experiment has passed the already-frozen deadline-valid
adjudication gate.
}
}
\]

And the quantitative re-entry guarantee is:

\[
\boxed{
\Pr_h(\text{successful re-entry by }H\mid\mathcal F_\tau)
\ge
(1-\delta_R)(1-\delta_A).
}
\]

---

# 12. Proof-program status after T13.5

At the stated mathematical scope:

```text
T13.1  coverage / attainability                         PROVED
T13.2  constructive reachability                       PROVED AT STATED SCOPES
T13.3  selection-aware empirical re-entry              PROVED AT STATED SCOPES
T13.4  selection-naive self-validation firewall        PROVED COUNTEREXAMPLE
T13.5  bounded-risk boundary-expansion synthesis       PROVED AT STATED SCOPE
```

Thus the proof-first T13 boundary-expansion sequence is closed at its stated conceptual/mathematical scope.

This closure does not authorize a representation-invention system or construction experiment. Empirical implementation/validation remains a separate future gate.