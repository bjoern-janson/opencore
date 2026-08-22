# T12e.4b / T12e.5 — Proof Closure

**Status:** `PROVED_AT_STATED_SCOPES`  
**Branch:** `opencore/t12e-anytime-separation`  
**Scope:** mathematical proof layer only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**T13 status:** closed

This note closes the two active proof obligations left by Mathematical Core v0.1:

```text
T12e.4b  anytime finite-horizon adjudication
T12e.5   sharp finite-horizon path-law characterization
```

The result is slightly sharper than the initial target.

1. A likelihood-ratio process gives **anytime wrong-attribution control** by Ville's inequality without bounded-increment or Freedman assumptions.
2. Anytime safety alone does **not** guarantee a decision by the deadline.
3. A terminal fallback test completes the finite-horizon guarantee.
4. Total variation is the exact terminal criterion for **equal-prior average error**.
5. For the stronger OpenCore criterion in which **each directed error** must be at most `delta`, total variation is necessary but not sufficient. The exact path-law criterion is the Neyman-Pearson / ROC testing tradeoff.

Thus the proof audit does not require a new primitive. It requires only a sharper statement of the statistical risk being controlled.

---

## 1. Conditional future path laws

Fix a current time `t`, current observed history `F_t`, a live pair `(H_i,H_j)`, and a pre-adjudication adaptive experiment policy `pi`.

Condition on a realized current history that lies in the common support of the two live hypotheses. For `k=0,...,H`, let

\[
\mathcal H_k
=
\sigma(A_{t+1},Z_{t+1},\ldots,A_{t+k},Z_{t+k})
\]

be the future-prefix filtration, with `H_0` trivial after conditioning on `F_t`.

Let

\[
P_{i,k}^{\pi}
\quad\text{and}\quad
P_{j,k}^{\pi}
\]

be the two conditional laws of the next `k` adaptive action-observation steps.

For the clean two-sided likelihood theorem, assume

\[
P_{i,k}^{\pi}\sim P_{j,k}^{\pi}
\qquad
k=1,\ldots,H.
\]

Singular observations can only make some decisions easier; they are excluded here so the finite log-likelihood process is well defined in both directions.

Define the conditional likelihood-ratio process

\[
\Lambda_k
=
\frac{dP_{i,k}^{\pi}}{dP_{j,k}^{\pi}},
\qquad
\Lambda_0=1,
\]

and

\[
L_k=\log\Lambda_k.
\]

By consistency of Radon-Nikodym derivatives across the filtration,

\[
(\Lambda_k)_{k\le H}
\]

is a nonnegative martingale under `P_j`, and

\[
(\Lambda_k^{-1})_{k\le H}
\]

is a nonnegative martingale under `P_i`, both starting at one.

This is the only machinery needed for the anytime-validity result.

---

# 2. T12e.4b — Anytime finite-horizon adjudication

## Theorem 4b.1 — Anytime wrong-attribution control

Fix directed error budgets

\[
\varepsilon_i,\varepsilon_j\in(0,1).
\]

Define

\[
a_i=\log\frac1{\varepsilon_i},
\qquad
a_j=\log\frac1{\varepsilon_j}.
\]

Consider the stopping rule

\[
\tau
=
\inf\left\{
1\le k\le H:
L_k\le-a_i
\text{ or }
L_k\ge a_j
\right\},
\]

with `tau=infinity` if neither boundary is crossed by `H`.

If the lower boundary is crossed first, attribute `H_j`. If the upper boundary is crossed first, attribute `H_i`.

Then

\[
\boxed{
P_i(\tau\le H,\widehat H=j\mid\mathcal F_t)
\le\varepsilon_i,
}
\]

and

\[
\boxed{
P_j(\tau\le H,\widehat H=i\mid\mathcal F_t)
\le\varepsilon_j.
}
\]

In fact the same bounds hold with `H=infinity` whenever the likelihood-ratio martingales are defined for all times.

### Proof

Under `H_i`, a wrong attribution to `H_j` requires the likelihood process to cross the lower boundary:

\[
\{\tau\le H,\widehat H=j\}
\subseteq
\left\{
\inf_{k\le H}L_k\le-a_i
\right\}.
\]

Equivalently,

\[
\left\{
\inf_{k\le H}L_k\le-a_i
\right\}
=
\left\{
\sup_{k\le H}\Lambda_k^{-1}
\ge e^{a_i}
\right\}.
\]

Because `(Lambda_k^{-1})` is a nonnegative `P_i`-martingale starting at one, Ville's inequality gives

\[
P_i\left(
\sup_{k\le H}\Lambda_k^{-1}\ge e^{a_i}
\mid\mathcal F_t
\right)
\le e^{-a_i}
=\varepsilon_i.
\]

The reverse bound follows identically under `H_j` from the nonnegative martingale `(Lambda_k)`:

\[
P_j\left(
\sup_{k\le H}\Lambda_k\ge e^{a_j}
\mid\mathcal F_t
\right)
\le e^{-a_j}
=\varepsilon_j.
\]

`QED`

### Interpretation

This proves the permanent distinction

\[
\boxed{
\text{terminal correctness}
\neq
\text{anytime-safe attribution}.
}
\]

The anytime-valid bound does **not** require a bounded likelihood increment, a variance bound, or a Freedman inequality. It follows directly from the likelihood-ratio martingale.

But it controls only **wrong commitment**. It does not guarantee that either boundary is reached by `H`.

---

## Proposition 4b.2 — Anytime safety does not imply deadline power

Theorem 4b.1 alone places no nontrivial upper bound on

\[
P_i(\tau>H)
\quad\text{or}\quad
P_j(\tau>H).
\]

For example, if the two path laws are identical through time `H`, then

\[
L_k=0
\qquad k\le H
\]

almost surely under both hypotheses. For every positive boundary,

\[
P_i(\tau>H)=P_j(\tau>H)=1.
\]

Thus

\[
\boxed{
\text{anytime validity}
\not\Rightarrow
\text{timely adjudication}.
}
\]

No new theoretical object is required; this is simply the difference between type-I/type-II control and finite-horizon power.

---

## Corollary 4b.3 — Boundary crossing plus terminal likelihood power

Retain the stopping rule of Theorem 4b.1. Suppose additionally

\[
P_i(L_H<a_j\mid\mathcal F_t)
\le\eta_i
\]

and

\[
P_j(L_H>-a_i\mid\mathcal F_t)
\le\eta_j.
\]

Then

\[
\boxed{
P_i(\text{correct attribution by }H\mid\mathcal F_t)
\ge1-\varepsilon_i-\eta_i,
}
\]

and

\[
\boxed{
P_j(\text{correct attribution by }H\mid\mathcal F_t)
\ge1-\varepsilon_j-\eta_j.
}
\]

### Proof

Under `H_i`, if `L_H>=a_j`, then the upper boundary has been reached by time `H`. The only way the sequential rule can fail to produce a correct attribution by `H` on this event is if the wrong lower boundary was crossed first. Hence

\[
P_i(\text{fail correct attribution by }H)
\le
P_i(L_H<a_j)
+
P_i(\text{wrong lower crossing by }H)
\le
\eta_i+\varepsilon_i.
\]

The reverse direction is identical. `QED`

This is already a finite-horizon sufficient theorem, but it still asks for a terminal likelihood-power condition. T12e.5 identifies the exact terminal path-law requirement.

---

# 3. T12e.5 — Sharp finite-horizon path-law characterization

Fix the two conditional `H`-step future path laws

\[
P=P_{i,H}^{\pi},
\qquad
Q=P_{j,H}^{\pi}
\]

on the complete adaptive future path through the deadline.

A randomized terminal test is represented by a measurable function

\[
\varphi:\Omega_H\to[0,1],
\]

where `varphi(x)` is the probability of deciding `H_i` after observing path `x`.

Its directed errors are

\[
\alpha(\varphi)=1-E_P[\varphi],
\qquad
\beta(\varphi)=E_Q[\varphi].
\]

---

## Theorem 5.1 — Total variation is exact for equal-prior average error

Define

\[
R_{\rm avg}^*(P,Q)
=
\inf_{0\le\varphi\le1}
\frac{\alpha(\varphi)+\beta(\varphi)}2.
\]

Then

\[
\boxed{
R_{\rm avg}^*(P,Q)
=
\frac12\left(1-\|P-Q\|_{\rm TV}\right).
}
\]

Therefore

\[
\boxed{
R_{\rm avg}^*(P,Q)\le\delta
\iff
\|P-Q\|_{\rm TV}\ge1-2\delta.
}
\]

### Proof

For any randomized test,

\[
\alpha+\beta
=
1-E_P[\varphi]+E_Q[\varphi]
=
1-(E_P[\varphi]-E_Q[\varphi]).
\]

Taking the infimum over tests is equivalent to taking the supremum of `E_P[varphi]-E_Q[varphi]` over measurable `0<=varphi<=1`. That supremum is exactly total variation. `QED`

### Scope

This is the exact statement previously intended by

\[
\|P-Q\|_{\rm TV}\ge1-2\delta.
\]

It is exact for **equal-prior average Bayes error**.

It is not, by itself, the exact criterion for requiring **both directed errors** to be at most `delta`.

---

## Theorem 5.2 — TV is necessary but not sufficient for two-sided `delta` error

Suppose a test satisfies

\[
\alpha(\varphi)\le\delta,
\qquad
\beta(\varphi)\le\delta.
\]

Then

\[
E_P[\varphi]-E_Q[\varphi]
\ge1-2\delta,
\]

so necessarily

\[
\boxed{
\|P-Q\|_{\rm TV}\ge1-2\delta.
}
\]

The converse is false.

### Counterexample

Let the sample space be `{x_1,x_2}` and take

\[
P=(1,0),
\qquad
Q=(0.8,0.2),
\qquad
\delta=0.4.
\]

Then

\[
\|P-Q\|_{\rm TV}=0.2=1-2\delta.
\]

Write the randomized test as

\[
\varphi(x_1)=r,
\qquad
\varphi(x_2)=s,
\qquad
0\le r,s\le1.
\]

The requirement `alpha<=0.4` forces

\[
r\ge0.6.
\]

But then

\[
\beta
=0.8r+0.2s
\ge0.48
>0.4.
\]

Therefore no test has both directed errors at most `0.4`, despite satisfying the TV threshold for average error.

Hence

\[
\boxed{
\|P-Q\|_{\rm TV}\ge1-2\delta
\not\Rightarrow
\exists\varphi:\alpha,\beta\le\delta.
}
\]

`QED`

This is the theorem-driven correction to the earlier T12e.5 target. No new architecture is introduced; the error criterion is simply made explicit.

---

## Theorem 5.3 — Exact two-sided characterization by the testing tradeoff

For `gamma in [0,1]`, define the Neyman-Pearson testing function

\[
\beta_{\gamma}(P,Q)
=
\inf\left\{
E_Q[\varphi]:
0\le\varphi\le1,
E_P[\varphi]\ge\gamma
\right\}.
\]

Then a terminal test with both directed errors at most `delta` exists **if and only if**

\[
\boxed{
\beta_{1-\delta}(P,Q)\le\delta.
}
\]

Equivalently, if

\[
R_{\max}^*(P,Q)
=
\inf_{0\le\varphi\le1}
\max\{\alpha(\varphi),\beta(\varphi)\},
\]

then

\[
\boxed{
R_{\max}^*(P,Q)
=
\inf\left\{
\delta\in[0,1]:
\beta_{1-\delta}(P,Q)\le\delta
\right\}.
}
\]

### Proof

A test has `alpha<=delta` exactly when

\[
E_P[\varphi]\ge1-\delta.
\]

Among all tests satisfying that constraint, the smallest possible reverse error `beta=E_Q[varphi]` is, by definition,

\[
\beta_{1-\delta}(P,Q).
\]

Therefore there exists a test with both

\[
\alpha\le\delta
\quad\text{and}\quad
\beta\le\delta
\]

if and only if

\[
\beta_{1-\delta}(P,Q)\le\delta.
\]

The formula for `R_max^*` follows by taking the smallest feasible `delta`. `QED`

By the Neyman-Pearson lemma, an optimizer is a likelihood-ratio threshold test with possible randomization on the threshold set.

### Consequence

For the stronger OpenCore adjudication requirement

```text
error under H_i <= delta
and
error under H_j <= delta
```

the sharp terminal path-law property is the **testing tradeoff / ROC feasibility condition**, not TV alone.

Total variation remains exact for equal-prior average error and remains a useful necessary bound for the two-sided criterion. Hellinger or KL can provide tractable bounds, but neither is the definition of the sharp two-sided property.

---

# 4. Combined theorem — anytime-safe and deadline-complete adjudication

The previous results combine without adding any new statistical primitive.

## Theorem 4b/5.4 — Early-safe sequential attribution with terminal fallback

Fix an overall directed error target `delta` and split it as

\[
\delta_E+\delta_T\le\delta,
\qquad
\delta_E,\delta_T>0.
\]

Assume the future prefix path laws are mutually absolutely continuous through `H` so that the likelihood-ratio martingale is available for early stopping.

Assume also that the terminal `H`-step path laws satisfy

\[
\boxed{
\beta_{1-\delta_T}(P,Q)\le\delta_T.
}
\]

Construct the following sequential procedure.

1. For `k=1,...,H-1`, use the likelihood-ratio boundaries
   \[
   \pm\log(1/\delta_E).
   \]
   If a boundary is crossed, commit immediately to the corresponding hypothesis.
2. If neither boundary is crossed before `H`, apply at time `H` a terminal Neyman-Pearson test with both directed errors at most `delta_T`.

Then the procedure always decides by `H` and satisfies

\[
\boxed{
P_i(\widehat H=j\text{ by }H\mid\mathcal F_t)
\le\delta_E+\delta_T
\le\delta,
}
\]

and

\[
\boxed{
P_j(\widehat H=i\text{ by }H\mid\mathcal F_t)
\le\delta_E+\delta_T
\le\delta.
}
\]

Moreover, every **intermediate** commitment before `H` is controlled by the anytime-valid Ville bound with directed error at most `delta_E`.

### Proof

Under `H_i`, split the error event into two disjoint modes:

```text
E_early     wrong lower-boundary commitment before H
E_terminal  no early commitment and terminal fallback chooses H_j
```

Theorem 4b.1 gives

\[
P_i(E_{\rm early}\mid\mathcal F_t)\le\delta_E.
\]

The fallback error event is a subset of the error event of the same terminal test viewed on the full `H`-step path space, so

\[
P_i(E_{\rm terminal}\mid\mathcal F_t)\le\delta_T.
\]

Therefore

\[
P_i(\widehat H=j\text{ by }H\mid\mathcal F_t)
\le\delta_E+\delta_T.
\]

The reverse direction is identical. The terminal fallback guarantees a decision at `H` if no earlier commitment occurred. `QED`

### Operational meaning

This closes the mathematical gap between

```text
safe to commit early
```

and

```text
must have a bounded-error attribution by the deadline.
```

The result is intentionally modular:

```text
Ville likelihood martingale
    -> anytime wrong-attribution control

terminal path-law testing tradeoff
    -> deadline power / terminal fallback
```

Freedman / predictable KL conditions from T12e.4a remain useful sufficient machinery for certifying concrete terminal likelihood behavior. They are not required by the abstract anytime theorem.

---

# 5. Final proof status

The theorem frontier now reads:

```text
T12a     adaptive path-KL identity                         PROVED
T12b     refinement entropy lower bound                    CLASSICAL MACHINERY
T12c     endogenous refinement collapse                    PROVED EXISTENCE COUNTEREXAMPLE
T12d     robustness under broader policy classes           OPEN / DEFERRED
T12e.1   two-directed KL necessary                         PROVED
T12e.2   two-directed expected KL insufficient             PROVED COUNTEREXAMPLE
T12e.3   pathwise drift + relative-noise sufficiency       PROVED UNDER CONDITIONS
T12e.4a  terminal finite-horizon sufficiency               PROVED UNDER FREEDMAN CONDITIONS
T12e.4b  anytime-safe finite-horizon adjudication          PROVED
T12e.5   sharp terminal path-law characterization          PROVED, WITH RISK-CRITERION CORRECTION
T13      refinement construction                           CLOSED
```

The T12e.5 correction is:

\[
\boxed{
\text{TV is exact for equal-prior average error,}
}
\]

whereas

\[
\boxed{
\beta_{1-\delta}(P,Q)\le\delta
}
\]

is the exact terminal criterion for a test whose **two directed errors are each at most `delta`**.

This is a minimal theorem-driven revision, not an architectural expansion.

---

# 6. Mathematical Core v0.1 freeze

The core hierarchy is now:

\[
\boxed{
I^\star
\neq
K_n
\neq
G_n
\neq
L_n
\neq
\text{finite-horizon testing tradeoff}.
}
\]

Interpretation:

```text
I*      potential discriminating information
K_n     expected path-space information
G_n     predictable information on the realized adaptive action path
L_n     realized likelihood evidence
path-law testing tradeoff
        exact finite-horizon adjudication property
```

The methodological rule is:

> **Expected information is an accounting quantity. Realized likelihood is evidence. Path-law testing risk is the adjudication property. Anytime-valid early attribution plus bounded-error terminal adjudication is the timely corrigibility property.**

The theorem-compatible invariant is therefore:

> **Every unresolved consequential distinction must retain a path-law testing regime that permits bounded-error attribution by its consequence-relevant deadline, while any earlier commitment remains anytime-valid at its claimed error level.**

No broader claim is earned.

In particular, these proofs do **not** establish:

```text
a universal discovery mechanism
refinement construction
T12d robustness under natural policy families
a fourth adaptive control surface
a universal scalar corrigibility measure
that KL or TV alone is the final notion of challengeability
```

The conceptual architecture remains unchanged.

---

## 7. Stopping rule

Mathematical Core v0.1 is now at a defensible proof freeze for the closed-world adjudication problem.

Any reopening must be theorem-driven:

```text
proof contradiction
counterexample
missing assumption required by a stated theorem
new empirical evidence
```

Proof inconvenience alone is not authority for conceptual expansion.
