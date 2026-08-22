# T13.3 — Selection-Aware Empirical Re-entry

**Status:** `PROVED_AT_STATED_SCOPES`  
**Scope:** Mathematical Core boundary-expansion layer only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**CWC definition changed:** no  
**Construction experiment authorized:** no

This note proves the calibration gate that must hold after T13.2 reaches a candidate and before that candidate may re-enter the already-frozen closed-world adjudication machinery.

The central rule is:

> **Evidence used after adaptive candidate selection is admissible for authorization only if the final error guarantee remains calibrated under the selection mechanism that produced the candidate.**

Literal sample disjointness is sufficient in common cases, but it is not the definition. The theorem permits fresh prospective evidence, explicit post-selection conditioning, and sequentially valid evidence, provided the relevant conditional calibration is valid.

T13.3 does **not** redefine `CWC`. It answers only whether the evidence/test supplied to the closed-world certificate remains statistically legitimate after adaptive refinement selection.

The theorem-level chain remains

```text
candidate selected
-> selection-aware calibration
-> fresh / valid path law
-> existing CWC machinery
-> scoped authority
```

not

```text
candidate selected
-> candidate validated.
```

---

## 1. Setup

Let all random objects live on a probability space `(Omega,F,P)` under a fixed data-generating law `P`.

Let

\[
E_D
\]

be discovery evidence and let

\[
\mathcal D:=\sigma(E_D)
\]

be its sigma-field.

Allow randomized selection through an auxiliary variable `U_S`, and define the full selection sigma-field

\[
\boxed{
\mathcal S:=\sigma(E_D,U_S).
}
\]

Let the selected refinement be

\[
\boxed{
R=S(E_D,U_S),
}
\]

so `R` is `S`-measurable.

Let the candidate space be a standard Borel space so regular conditional distributions may be used when conditioning on `R`.

Let

\[
E_A
\]

be the authorization evidence and allow independent or dependent authorization randomization `U_A`.

An authorization decision is a measurable test

\[
\boxed{
\Phi
=
\phi(R,E_A,U_A)
\in\{0,1\},
}
\]

where `Phi=1` means that the candidate passes the statistical authorization gate being tested.

For each candidate `r`, let

\[
\mathcal P_{0,r}
\]

be the candidate-specific null family: the set of data-generating laws under which authorizing `r` would count as a false authorization for this test.

For a fixed law `P`, define the set of selected candidates whose null is true under `P`:

\[
\boxed{
N_P
:=
\{r:P\in\mathcal P_{0,r}\}.
}
\]

Assume `N_P` is measurable in the candidate space.

The false-authorization event under `P` is

\[
\boxed{
F_P
:=
\{\Phi=1,\ R\in N_P\}.
}
\]

If every candidate the selector can output is null under `P`, then `R in N_P` almost surely and `F_P={Phi=1}`.

---

# 2. T13.3a — Generic selection-aware re-entry theorem

## Theorem 13.3.1 — Conditional calibration transports through adaptive selection

Fix `delta in [0,1]`.

Suppose that for the data-generating law `P`, the selected-candidate authorization test satisfies

\[
\boxed{
E_P[\Phi\mid R]
\le\delta
\qquad
P\text{-a.s. on }\{R\in N_P\}.
}
\]

Then

\[
\boxed{
P_P(F_P)
\le
\delta\,P_P(R\in N_P)
\le
\delta.
}
\]

In particular, if the selected candidate is null almost surely under `P`, then

\[
\boxed{
P_P(\Phi=1)\le\delta.
}
\]

### Proof

Because the event `{R in N_P}` is `sigma(R)`-measurable,

\[
\begin{aligned}
P_P(F_P)
&=
E_P\left[
\mathbf 1_{\{R\in N_P\}}\Phi
\right]\\
&=
E_P\left[
\mathbf 1_{\{R\in N_P\}}
E_P[\Phi\mid R]
\right]\\
&\le
E_P\left[
\mathbf 1_{\{R\in N_P\}}\delta
\right]\\
&=
\delta P_P(R\in N_P)\\
&\le\delta.
\end{aligned}
\]

`QED`

### Interpretation

The theorem is deliberately elementary. It identifies the exact statistical firewall:

\[
\boxed{
\text{selected-candidate validity}
=
\text{validity under the selected-candidate conditional law}.
}
\]

The selector may be arbitrarily adaptive and randomized. No independence between discovery and authorization evidence is required by the theorem itself.

What is required is that the claimed error rate remain valid **after conditioning on the fact that the candidate was selected**.

---

## Corollary 13.3.2 — Calibration conditional on the full selection history

A stronger sufficient condition is

\[
\boxed{
E_P[\Phi\mid\mathcal S]
\le\delta
\qquad
P\text{-a.s. on }\{R\in N_P\}.
}
\]

Because `R` is `S`-measurable, the tower property gives

\[
E_P[\Phi\mid R]
=
E_P[
E_P[\Phi\mid\mathcal S]
\mid R
]
\le\delta
\]

on the selected null region. Therefore Theorem 13.3.1 applies.

This form is useful when the authorization experiment depends on more of the discovery/selection history than the selected candidate label alone.

---

# 3. T13.3b — Fresh prospective evidence as a sufficient route

The first admissible route is genuine prospective re-entry.

The clean condition is not necessarily unconditional independence. The authorization experiment may depend on which candidate was selected.

Let

\[
K_{P,r}
\]

be the reference authorization-data law for candidate `r` under data-generating law `P`.

## Corollary 13.3.3 — Prospective kernel sufficiency

Suppose that, after selection, the authorization evidence is generated from a prospective mechanism satisfying

\[
\boxed{
\mathcal L_P(E_A,U_A\mid\mathcal S)
=
K_{P,R}
\qquad P\text{-a.s.}
}
\]

That is: conditional on the entire selection history, the law used for authorization depends on that history only through the selected candidate (and any candidate-indexed protocol encoded in `r`).

Suppose further that for every candidate `r` and every null law `P in P_{0,r}`, the fixed-candidate authorization rule is calibrated under that kernel:

\[
\boxed{
E_{K_{P,r}}
[\phi(r,E_A,U_A)]
\le\delta.
}
\]

Then

\[
\boxed{
P_P(F_P)\le\delta
}
\]

for every `P`.

### Proof

On `{R=r}` with `P in P_{0,r}`,

\[
E_P[\Phi\mid\mathcal S]
=
E_{K_{P,R}}
[\phi(R,E_A,U_A)]
\le\delta.
\]

Corollary 13.3.2 applies. `QED`

### What this includes

This covers, among other cases:

```text
independent holdout data
fresh randomized experiments chosen after R
prospective interventions whose design is a function of R
candidate-specific validation protocols fixed after selection
```

provided the test is calibrated for the actual prospective kernel.

---

## Corollary 13.3.4 — Conditional-independence special case

A commonly useful stronger condition is

\[
\boxed{
(E_A,U_A)
\perp\!\!\!\perp
\mathcal S
\mid R
}
\]

under `P`, together with correct calibration of `phi_r` under the conditional law

\[
\mathcal L_P(E_A,U_A\mid R=r).
\]

Then

\[
\mathcal L_P(E_A,U_A\mid\mathcal S)
=
\mathcal L_P(E_A,U_A\mid R),
\]

so Corollary 13.3.3 applies.

This is sufficient, not necessary.

In particular, literal sample disjointness is not the theorem definition. What matters is whether the prospective evidence law used in the calibration calculation is still the correct law after the selection history is known.

---

# 4. T13.3c — Explicit post-selection inference

Fresh data are not required if the reused evidence is analyzed under the correct selected-candidate law.

## Corollary 13.3.5 — Post-selection conditioning suffices

No independence between `E_A` and `E_D` is assumed.

Suppose that for every candidate `r` with positive selection probability and every `P in P_{0,r}`, the authorization test is calibrated under the actual conditional law after selection:

\[
\boxed{
E_P[
\phi(r,E_A,U_A)
\mid R=r
]
\le\delta.
}
\]

Then

\[
\boxed{
P_P(F_P)\le\delta.
}
\]

### Proof

The displayed condition is exactly the hypothesis of Theorem 13.3.1. `QED`

### Interpretation

This is the formal reason the same raw observations may sometimes be reused without violating the T13.4 firewall.

The prohibition is not

```text
E_D and E_A must be disjoint.
```

It is

```text
a selected candidate may not reuse a fixed-candidate calibration
that ignores the event/mechanism by which that candidate was selected.
```

If the post-selection law is used correctly, the data reuse is selection-aware.

---

## Corollary 13.3.6 — Conditioning on a richer selection summary

Sometimes conditioning on `R` alone is inconvenient or loses useful structure. Let

\[
\mathcal C
\]

be any sigma-field satisfying

\[
\sigma(R)\subseteq\mathcal C\subseteq\mathcal S.
\]

If

\[
\boxed{
E_P[\Phi\mid\mathcal C]
\le\delta
\quad
\text{on }\{R\in N_P\},
}
\]

then marginal false-authorization probability is at most `delta`.

Thus selective inference may condition on the selected model, the complete selection event, or another sufficient selection summary. T13.3 does not privilege one conditioning granularity.

---

# 5. T13.3d — Sequentially valid re-entry

The candidate may alter which future experiments are run. This does not invalidate re-entry if the sequential test is calibrated under the resulting adaptive law.

Let selection occur at a stopping time `tau` with respect to a larger filtration and let

\[
\mathcal S=\mathcal F_\tau.
\]

The candidate `R` is `F_tau`-measurable.

After `tau`, let a candidate-dependent adaptive experiment policy `pi^+` generate a future path

\[
H_k^+
=
(A_{\tau+1},Z_{\tau+1},\ldots,A_{\tau+k},Z_{\tau+k}).
\]

## Corollary 13.3.7 — Conditional sequential test sufficiency

Suppose that for every selected-null candidate and every relevant null law,

\[
\boxed{
P_P(
\Phi=1
\mid\mathcal F_\tau
)
\le\delta
\qquad
P\text{-a.s. on }\{R\in N_P\}.
}
\]

where `Phi` may depend on the entire adaptive future path and may stop at an authorization stopping time.

Then

\[
\boxed{
P_P(F_P)\le\delta.
}
\]

This is immediate from Corollary 13.3.2.

---

## Corollary 13.3.8 — e-process / test-martingale re-entry

A useful sufficient construction is the following.

For each selected candidate `r`, suppose there is a nonnegative process

\[
(M_k^{(r)})_{k\ge0}
\]

adapted to the post-selection filtration such that under every `P in P_{0,r}`,

\[
E_P[M_0^{(r)}\mid\mathcal F_\tau]\le1
\]

and, conditional on `F_tau`,

\[
(M_k^{(r)})
\]

is a nonnegative supermartingale under the actual candidate-dependent adaptive experiment policy.

Use the authorization rule

\[
\boxed{
\Phi
=
\mathbf 1\left\{
\sup_{k\ge0}M_k^{(R)}
\ge\frac1\delta
\right\}.
}
\]

Conditional Ville inequality gives

\[
P_P(\Phi=1\mid\mathcal F_\tau)
\le\delta
\]

for every selected-null candidate. Therefore

\[
\boxed{
P_P(F_P)\le\delta.
}
\]

### Relation to T12e

This is a calibration bridge back into the closed-world machinery. It does not replace or weaken the existing finite-horizon `CWC` requirement.

T13.3 establishes that the selected candidate's post-selection evidence can be statistically legitimate. `CWC` must still separately establish the required two-sided path-law adjudicability by the consequence-relevant deadline.

Thus

\[
\boxed{
\text{selection-aware validity}
\neq
\mathsf{CWC}.
}
\]

The first is an admissibility/calibration property of the re-entry evidence. The second is the already-frozen closed-world adjudication property.

---

# 6. Negative theorem — fixed-candidate calibration can inflate under search

T13.4 already gives a concrete self-validation counterexample. The following finite-class proposition isolates the multiplicity/search burden abstractly.

## Proposition 13.3.9 — Finite search can inflate fixed-candidate size to `min(1,m delta)`

Fix an integer `m>=1` and `delta in (0,1)`.

There exist:

- `m` candidate-specific tests `phi_1,...,phi_m`;
- a data-generating law `P` under which every candidate null is true;
- a selector `R=S(E_D)` using the same evidence on which those tests are evaluated;

such that every candidate fixed in advance satisfies

\[
\boxed{
P(\phi_j=1)\le\delta,
\qquad j=1,\ldots,m,
}
\]

while the selected-candidate false-authorization probability is

\[
\boxed{
P(\phi_R=1)
=
\min\{1,m\delta\}.
}
\]

### Construction when `m delta <= 1`

Take disjoint measurable events

\[
B_1,\ldots,B_m
\]

with

\[
P(B_j)=\delta.
\]

Set

\[
\phi_j=\mathbf 1_{B_j}.
\]

Define the selector by choosing `R=j` on `B_j`; outside the union choose any candidate whose rejection event does not occur there.

Then each fixed test has size `delta`, while

\[
P(\phi_R=1)
=
P\left(\bigcup_{j=1}^mB_j\right)
=m\delta.
\]

### Construction when `m delta >= 1`

Partition the sample space into `m` measurable events

\[
B_1,\ldots,B_m
\]

whose probabilities are all at most `delta` and whose union has probability one. Set `phi_j=1_{B_j}` and select the unique `j` whose event occurs.

Then every fixed-candidate test has size at most `delta`, yet

\[
P(\phi_R=1)=1.
\]

`QED`

### Interpretation

Fixed-candidate calibration alone yields at best a multiplicity-style bound over a finite searched family:

\[
\boxed{
P(\text{some fixed test rejects})
\le
m\delta,
}
\]

and the factor can be attained.

Thus

\[
\boxed{
\text{fixed-candidate size}
\neq
\text{selected-candidate size}.
}
\]

The effective search family can therefore create a selection burden. T13.3 does not freeze a universal complexity penalty such as `log m`; the correct adjustment depends on the selection and testing procedure. The theorem only establishes that ignoring the selection mechanism can produce arbitrarily severe inflation.

---

# 7. Relation to T13.4

T13.4 proved by explicit empirical-fitting witness that

\[
\boxed{
E_D\to R
\not\Rightarrow
E_D\text{ validates }R.
}
\]

T13.3 supplies the positive converse direction at the correct scope:

\[
\boxed{
\text{conditional calibration under the selected-candidate law}
\Rightarrow
\text{marginal false-authorization control}.
}
\]

Together:

```text
selection-naive reuse can fail
but
selection-aware reuse can be valid.
```

This is the exact firewall intended by the T13 admission rule.

---

# 8. Re-entry routes now formally admitted

The theorem permits three generic routes.

## Route R1 — prospective / fresh evidence

A post-selection experiment is generated from the correct candidate-indexed kernel and the test is calibrated for that kernel.

Symbolically:

\[
R
\to
\pi_R^+
\to
E_A
\to
\text{conditional calibration}.
\]

## Route R2 — post-selection inference

Authorization may reuse discovery-overlapping evidence, but the test is calibrated under the actual conditional law induced by selection.

Symbolically:

\[
(E_D,E_A)
\to
R
\to
\mathcal L(E_A\mid R)
\to
\text{valid selected-candidate test}.
\]

## Route R3 — sequentially valid evidence

The selected candidate can adapt future experimentation, provided the resulting test/e-process is valid conditional on the selection filtration under the actual adaptive path law.

Symbolically:

\[
\mathcal F_\tau
\to
R
\to
\pi_R^+
\to
\text{conditional test martingale / e-process}
\to
\text{valid re-entry evidence}.
\]

No one route is privileged as the definition.

---

# 9. What T13.3 proves — and what it does not

T13.3 proves:

\[
\boxed{
\text{selection-aware conditional validity}
\Longrightarrow
\text{marginal false-authorization control}.
}
\]

It also proves that fixed-candidate calibration can incur an arbitrarily large multiplicity penalty when used after adaptive search without correction.

T13.3 does **not** prove:

```text
that a reached candidate is empirically adequate
that a candidate is constructively reachable
that fresh data must be literally independent
that discovery data can always be reused
that one universal multiplicity correction is sufficient
that selection-aware validity alone implies CWC
that CWC should be redefined
that the candidate earns authority
```

The final two gates remain separate:

\[
\boxed{
\text{selection-aware valid evidence}
\neq
\mathsf{CWC}
\neq
\text{scoped authority}.
}
\]

---

# 10. T13 status after this proof

The boundary-expansion proof chain now reads:

```text
T13.1  coverage / attainability boundary              PROVED
T13.2  constructive reachability                      PROVED AT STATED SCOPES
T13.3  selection-aware empirical re-entry             PROVED AT STATED SCOPES
T13.4  selection-naive self-validation firewall       PROVED COUNTEREXAMPLE
T13.5  sufficient boundary-expansion / re-entry       NEXT
```

The earned chain is now

\[
\boxed{
\mathcal R_\varepsilon^\star\neq\varnothing
\rightarrow
\text{constructive hit}
\rightarrow
\text{selection-aware valid evidence}
\rightarrow
\mathsf{CWC}
\rightarrow
\Gamma.
}
\]

The first three arrows are no longer allowed to collapse into one another.

---

## 11. Stopping rule

No constructor implementation or construction experiment follows from T13.3.

The next theorem target is T13.5 only:

> **State and prove the minimal sufficient boundary-expansion theorem that composes T13.1 attainability, T13.2 reachability, T13.3 selection-aware re-entry, and the already-frozen `CWC` certificate into scoped authority.**

Any further assumptions must be introduced only if that composition theorem mathematically requires them.