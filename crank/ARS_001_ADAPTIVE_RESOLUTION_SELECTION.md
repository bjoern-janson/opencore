# ARS-001 — Adaptive Resolution Selection

**Status:** `PROSPECTIVE_FREEZE / NOT RUN`  
**Scope:** empirical adaptive control over a fixed representation ladder  
**Representation invention tested:** no  
**Predictor learning in first assay:** no — depth-specific predictors are frozen and competent  
**Selector learning:** yes  
**New OpenCore primitive:** none  
**T13 reopened:** no  
**Authority / Gamma changed:** no

ARS-001 is the first empirical continuation after the proof-first T13 closure.

The experiment asks one narrow question:

\[
\boxed{
\textbf{Can a learner learn when additional representational resolution is worth paying for?}
}
\]

The representation family is supplied in advance. ARS-001 does **not** construct a new representation and does not test the open Level-3 representation-invention problem.

The frozen boundary is

\[
\boxed{
\text{fixed representation family}
\longrightarrow
\text{adaptive depth selection}
}
\]

not

\[
\text{boundary failure}
\longrightarrow
\text{invent representation}.
\]

The hard claim boundary is therefore

\[
\boxed{
\text{ARS success}
\neq
\text{T13 representation-invention success}.
}
\]

Even a perfect ARS controller only learns how to choose among supplied representations. It does not learn how to construct a new rung.

---

## 1. Scientific target

Fix an ordered representation family

\[
\boxed{
\Pi_0\prec\Pi_1\prec\Pi_2\prec\Pi_3
}
\]

with increasing operating cost

\[
0<c_0<c_1<c_2<c_3.
\]

For each depth `d`, freeze a competent depth-specific predictor

\[
\boxed{
f_d:\Pi_d(X)\rightarrow \widehat Y.
}
\]

Only the resolution controller is learned:

\[
\boxed{
\mu_t:
H_{t-1}ightarrow d_t\in\{0,1,2,3\}.
}
\]

The controller history may contain only information available before the current outcome is revealed, including past:

- chosen depths;
- prediction residuals / losses;
- probe outcomes;
- budget state;
- task descriptors explicitly supplied by the protocol;
- elapsed time / episode state.

The first assay therefore isolates

```text
representation selection
```

from

```text
predictor optimization.
```

This avoids the ambiguity

\[
\boxed{
\text{bad depth selection}
\neq
\text{bad predictor training}.
}
\]

---

## 2. Frozen causal protocol

At prediction time `t`:

\[
\boxed{
H_{t-1}
\rightarrow
\mu_t
\rightarrow
d_t
\rightarrow
\Pi_{d_t}(X_t)
\rightarrow
f_{d_t}
\rightarrow
\widehat Y_t
\rightarrow
Y_t
\rightarrow
e_t
\rightarrow
H_t.
}
\]

The depth decision must be made before observing `Y_t`.

Formally:

\[
\begin{aligned}
d_t &= \mu(H_{t-1}),\\
Z_t &= \Pi_{d_t}(X_t),\\
\widehat Y_t &= f_{d_t}(Z_t),\\
Y_t &\text{ is then revealed},\\
e_t &= \ell(\widehat Y_t,Y_t).
\end{aligned}
\]

No label look-ahead is permitted.

A residual from example `t` may influence depth choice only for later predictions, unless a separately frozen within-example protocol is explicitly introduced in a later experiment.

This preserves the causal ordering

\[
\boxed{
\text{past evidence}
\rightarrow
\text{representation choice}
\rightarrow
\text{fresh prediction}
\rightarrow
\text{fresh residual}.
}
\]

---

## 3. Central scientific separation — control is not diagnosis

ARS-001 tests adaptive control, not semantic failure attribution.

The central non-implication is

\[
\boxed{
\text{adaptive depth selection}
\not\Rightarrow
\text{representation-failure diagnosis}.
}
\]

A controller may learn a policy that chooses useful depths without internally representing or correctly naming the causal source of failure.

Therefore the claim ladder is:

\[
\boxed{
\begin{aligned}
L_1 &: \text{adaptive allocation beats fixed baselines},\\
L_2 &: \text{allocation beats threshold and compute-matched random controls},\\
L_3 &: \text{allocation transfers to held-out matched regimes},\\
L_4 &: \text{explicit representation-insufficiency diagnosis}.
\end{aligned}}
\]

ARS-001 targets `L1–L3` only.

`L4` is not inferred from control success.

This preserves the CSD lesson:

\[
\boxed{
\text{correct action}
\not\Rightarrow
\text{correct failure-cause attribution}.
}
\]

---

## 4. Matched-residual gate — mandatory

ARS-001 is not admissible without at least one matched pair in which cheap-representation residuals are observationally matched while the value of additional resolution differs.

Without this gate, a selector may succeed through the trivial policy

\[
\text{large error}
\rightarrow
\text{spend more representation cost}.
\]

The assay must instead instantiate

\[
\boxed{
\text{similar observed cheap-depth failure}
+
\text{different value of deeper resolution}.
}
\]

### 4.1 Exact binary witness

Let

\[
U,V,N\overset{\text{iid}}{\sim}\operatorname{Bernoulli}(1/2).
\]

Take

\[
\Pi_0(X)=U,
\qquad
\Pi_1(X)=(U,V).
\]

Use two latent regimes.

#### Resolution-remediable world `W_R`

\[
\boxed{
Y=U\oplus V.
}
\]

At depth `0`, the optimal predictor using only `U` has Bayes error `1/2`.

At depth `1`, the competent predictor can recover

\[
Y=U\oplus V
\]

exactly, so Bayes error is `0`.

#### Irreducible-noise world `W_N`

\[
\boxed{
Y=U\oplus N,
}
\]

where `N` is independent of all represented coordinates.

At depth `0`, the Bayes error is again `1/2`.

At depth `1`, adding `V` does not reduce Bayes error, which remains `1/2`.

Therefore under the cheap representation,

\[
\boxed{
\mathcal L(e_t\mid W_R,\Pi_0)
=
\mathcal L(e_t\mid W_N,\Pi_0)
}
\]

for 0-1 loss under competent cheap-depth prediction, while

\[
\boxed{
\begin{aligned}
E[\ell\mid W_R,\Pi_1] &< E[\ell\mid W_R,\Pi_0],\\
E[\ell\mid W_N,\Pi_1] &= E[\ell\mid W_N,\Pi_0].
\end{aligned}}
\]

This is the minimal diagnostic pair.

Before probing a richer depth, the two regimes are intentionally non-identifiable from cheap-depth residual magnitude alone.

Thus a successful adaptive policy may need to learn the **value of resolution probes**, their timing, and their persistence consequences.

### 4.2 Gate requirement

Before any learned-selector result is interpreted, certify that the matched-world construction satisfies:

```text
G1  cheap-depth residual law is matched to the frozen tolerance
G2  richer depth reduces risk in the representation-remediable world
G3  richer depth does not materially reduce risk in the matched noise world
G4  regime identity is not directly exposed to the selector through a shortcut feature
```

Failure of any gate invalidates the intended ARS interpretation.

---

## 5. Fixed representation ladder

The mini assay may use the concrete state

\[
X=(U,V,W,Q)
\]

with

\[
\boxed{
\begin{aligned}
\Pi_0(X)&=U,\\
\Pi_1(X)&=(U,V),\\
\Pi_2(X)&=(U,V,W),\\
\Pi_3(X)&=(U,V,W,Q).
\end{aligned}}
\]

Example resolution-requiring task regimes may be

\[
\begin{aligned}
G_0 &: Y=U,\\
G_1 &: Y=U\oplus V,\\
G_2 &: Y=U\oplus V\oplus W,\\
G_3 &: Y=U\oplus V\oplus W\oplus Q.
\end{aligned}
\]

These give known minimum sufficient depths

\[
d^\star(G_k)=k.
\]

Matched noise regimes must be added so that residual magnitude is not itself an identifying label for `d^star`.

The precise final world family, regime lengths, shift schedule, cost vector, and training split must be prospectively frozen before execution.

ARS-001 does not infer generality from the toy XOR family. It uses the family as a controlled causal assay.

---

## 6. Frozen baseline matrix

The required comparison set is

\[
\boxed{
\begin{array}{lll}
M_0 &: \text{always cheapest depth }\Pi_0,\\
M_1 &: \text{always richest depth }\Pi_3,\\
M_2 &: \text{oracle minimum sufficient depth},\\
M_3 &: \text{learned adaptive depth selector},\\
M_4 &: \text{residual-threshold escalation},\\
M_5 &: \text{compute-matched random depth allocation}.
\end{array}}
\]

### `M0` — always cheap

Measures the failure cost of refusing resolution escalation.

### `M1` — always rich

Measures the robustness ceiling available from paying maximum standing representation cost.

### `M2` — oracle minimum sufficient depth

Uses evaluator knowledge of the current regime to choose the minimum sufficient depth. This is a control ceiling, not an implementable learner.

### `M3` — learned adaptive selector

The target system. It receives only admissible history and chooses depth prospectively.

### `M4` — residual-threshold escalation

A deliberately strong simple heuristic. It tests whether `M3` has learned anything beyond

```text
large recent error -> increase depth.
```

### `M5` — compute-matched random allocation

Randomly allocates richer depths while matching `M3`'s average representation cost or depth-frequency profile.

It tests whether occasional extra resolution is sufficient without meaningful adaptive selection.

---

## 7. Primary outcomes

Do not collapse the experiment to one loss-plus-cost scalar.

Report the risk / representation-cost Pareto relation and the following primary readouts separately.

Let

\[
\boxed{
L(M)=\text{predictive risk of method }M
}
\]

and

\[
\boxed{
C(M)=E[c_{d_t}\mid M]
}
\]

be average standing representation cost.

Let

\[
\boxed{
T_R(M)=\text{shift-to-restored-prediction recovery latency}
}
\]

for genuine resolution-requiring shifts.

Let

\[
\boxed{
F_N(M)=\text{false escalation rate in matched irreducible-noise regimes}.
}
\]

Also report:

\[
\begin{aligned}
E_{\rm under}(M)&=P(d_t<d^\star_t),\\
E_{\rm over}(M)&=P(d_t>d^\star_t),\\
P_H(M)&=P(T_R(M)\le H_R)
\end{aligned}
\]

for evaluator-defined regimes where `d^star_t` is known.

The scientific result is multi-objective. Any scalar Lagrangian used for training is not itself the scientific estimand.

---

## 8. Central estimand — frontier gain, not a universal scalar

Let

\[
\mathcal M_{\rm nonadapt}:=\{M_0,M_1\}
\]

be the fixed-depth / nonadaptive controls for the primary frontier comparison. `M4` and `M5` remain mandatory diagnostic controls.

Define the best nonadaptive risk achievable at cost budget `c`:

\[
\boxed{
L^\star_{\rm NA}(c)
:=
\inf\{L(M):M\in\mathcal M_{\rm nonadapt},\ C(M)\le c\}.
}
\]

For the learned adaptive selector, define

\[
L_{\rm ARS}(c)
\]

from the frozen family of selector cost settings / operating budgets.

The primary frontier estimand is the matched-cost risk gain

\[
\boxed{
\Delta_{\rm ARS}(c)
:=
L^\star_{\rm NA}(c)-L_{\rm ARS}(c).
}
\]

Positive values mean the adaptive selector achieves lower risk than the best nonadaptive control at the same or lower average representation cost.

The dual matched-risk cost saving may also be reported:

\[
\boxed{
\Delta^C_{\rm ARS}(\ell)
:=
C^\star_{\rm NA}(\ell)-C_{\rm ARS}(\ell),
}
\]

where `C^star_NA(ell)` is the least nonadaptive cost achieving risk at most `ell`.

No universal scalarization across loss, cost, latency, and false escalation is frozen.

The shorthand scientific comparison is therefore

\[
\boxed{
\text{frontier}(M_3)
\text{ versus }
\text{best nonadaptive frontier},
}
\]

with `M4` and `M5` used to identify whether any gain is more than thresholding or random compute allocation.

---

## 9. Positive target pattern

The aspirational positive signature is

\[
\boxed{
\begin{aligned}
L(M_3)&\approx L(M_1),\\
C(M_3)&\ll C(M_1),\\
T_R(M_3)&\approx T_R(M_2),\\
F_N(M_3)&\ll F_N(M_4),
\end{aligned}}
\]

plus transfer to held-out matched regimes.

This is not required as an exact equality claim. Prospective tolerances must be frozen before execution.

A positive ARS-001 result requires more than `M3 > M0`.

At minimum, the learned selector must show a favorable risk/cost tradeoff and meaningful separation from both:

\[
M_4
\]

and

\[
M_5.
\]

---

## 10. Held-out transfer gate

A controller can appear adaptive by memorizing superficial regime identifiers.

Therefore the test set must contain held-out matched regimes in which:

```text
same resolution requirement
+ different surface distribution / nuisance statistics
+ no direct regime identifier
```

The intended positive claim requires that the useful selection policy transfer across this change.

Interpretation boundary:

\[
\boxed{
\text{in-distribution depth selection}
\neq
\text{transferable adaptive resolution control}.
}
\]

If `M3` succeeds only on seen regime templates, the result is localized to regime memorization or narrow policy fitting.

---

## 11. Negative-result localization

ARS-001 is designed to fail informatively.

### N1 — threshold equivalence

If

\[
M_3\approx M_4,
\]

then the learned controller may have learned error magnitude rather than a materially richer adaptive resolution policy.

Earned ceiling:

```text
learned adaptive selector
!=
representation-insufficiency discrimination
```

unless independent evidence shows otherwise.

### N2 — random-allocation equivalence

If

\[
M_3\approx M_5,
\]

then occasional extra resolution may explain the gain; adaptive diagnosis/control adds little beyond compute allocation.

### N3 — overspending

If prediction improves but

\[
C(M_3)\approx C(M_1),
\]

then the controller has poor cost calibration. It has not demonstrated the intended cheap-standing-cost advantage.

### N4 — under-escalation after genuine shifts

If `M3` fails to request sufficient depth after a representation-remediable shift, localize as a resolution-exposure / control failure.

### N5 — false escalation under matched noise

If `M3` escalates similarly in `W_R` and `W_N` despite deeper resolution helping only in `W_R`, then the selector has not learned to control resolution selectively.

This does not by itself establish why it failed.

### N6 — transfer failure

If `M3` succeeds on training-like regimes but fails on held-out matched regimes, localize as policy memorization / regime identification rather than transferable adaptive resolution control.

### N7 — oracle gap remains large

If

\[
T_R(M_3)\gg T_R(M_2)
\]

or risk remains far above `M2` at comparable feasible cost, the experiment establishes a substantial control gap even though the representation ladder itself is adequate.

---

## 12. Claim ceiling

A positive result may support only the following class of statement:

\[
\boxed{
\textbf{
Given a fixed ordered representation family and competent frozen predictors,
a learned controller can be tested for whether it allocates representational
resolution more efficiently than fixed, threshold, and compute-matched random
policies, including under matched residual regimes and held-out shifts.
}
}
\]

If the prospective positive criteria are met, the strongest intended empirical compression is:

\[
\boxed{
\textbf{
Representation resolution can function as an adaptively allocated resource
within a fixed admissible representation family.
}
}
\]

This does **not** establish:

- representation invention;
- unique diagnosis of representation insufficiency;
- causal understanding of why the selector chose a depth;
- universal optimality of the supplied ladder;
- safe authority transfer;
- T13 construction success;
- generalization beyond the frozen and held-out assay family without further evidence.

In particular:

\[
\boxed{
\text{ARS success}
\neq
\text{T13 success}.
}
\]

A perfect ARS controller still cannot construct

\[
\Pi_4
\]

when the fixed family ends at

\[
\Pi_3.
\]

---

## 13. Relationship to the mathematical closure

ARS-001 sits after the mathematical results without modifying them.

The research ladder is

\[
\boxed{
\begin{array}{rcl}
\text{C1--C4 / T13}
&\longrightarrow&
\text{conditions for representation sufficiency, repair, and re-entry},\\
\text{ARS-001}
&\longrightarrow&
\text{adaptive management of a fixed resolution ladder},\\
\text{future unopened frontier}
&\longrightarrow&
\text{construction of a genuinely new rung}.
\end{array}}
\]

ARS-001 uses the existing representation-control surface. It adds no fourth permanent control surface.

The representation ladder is evaluator-supplied:

\[
\boxed{
\{\Pi_0,\Pi_1,\Pi_2,\Pi_3\}
\text{ is fixed before learning }\mu.
}
\]

Thus

\[
\boxed{
\text{representation invention in ARS-001}=0.
}
\]

---

## 14. What must be frozen before execution

This document freezes the scientific architecture but does not yet authorize an implementation run with unspecified degrees of freedom.

Before execution, freeze at minimum:

1. exact world family and matched-world tolerance;
2. exact representation maps `Pi_0 ... Pi_3`;
3. depth costs `c_0 ... c_3`;
4. frozen predictor construction / competency verification;
5. selector model class and training algorithm;
6. regime durations and shift schedule;
7. training / validation / held-out test split;
8. admissible selector history variables;
9. residual definition and windowing;
10. `M4` threshold selection procedure;
11. `M5` compute-matching rule;
12. recovery-latency definition;
13. false-escalation definition;
14. prospective positive / equivalence tolerances;
15. seed count and statistical intervals;
16. stopping / exclusion rules.

No result should be interpreted before those execution details are prospectively frozen.

---

## 15. Current status

```text
ARS-001 scientific boundary   FROZEN
matched-residual gate         REQUIRED
fixed representation ladder   REQUIRED
frozen competent predictors   REQUIRED IN FIRST ASSAY
learned selector mu           TARGET
M0--M5 controls               REQUIRED
held-out transfer             REQUIRED
implementation                NOT YET FROZEN
experiment                    NOT RUN
results                       NONE
```

The next legitimate step is an ARS-001 execution freeze: specify the exact synthetic worlds, predictor bank, selector class, cost schedule, split, metrics, tolerances, and seeds before running anything.
