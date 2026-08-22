# T13.4 — Selection-Naive Self-Validation Firewall

**Status:** `PROVED_COUNTEREXAMPLE / SELECTION-NAIVE IMPOSSIBILITY`  
**Scope:** Mathematical Core boundary-expansion layer only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**T13 construction mechanism added:** none

This note proves the first T13 firewall:

> **A candidate selected because it fits discovery evidence cannot treat that same fit as unselected confirmation.**

The result is deliberately narrower than the statement that discovery data can never be reused. Selection-aware post-selection or sequential inference may reuse data when its calibration explicitly accounts for the selection mechanism. What fails is the selection-naive implication

\[
\boxed{
\text{good fit on the evidence that selected }r
\Longrightarrow
\text{validity of }r.
}
\]

The counterexample is finite, contains the true empirical law inside the candidate class, and can be made mutually absolutely continuous throughout. Thus the failure is not caused by lack of coverage, infinite model classes, or singular likelihoods.

---

## 1. Setup

Fix an integer

\[
N\ge 2
\]

and sample space

\[
\mathcal X=\{1,\ldots,N\}.
\]

Let the true empirical law be uniform:

\[
\boxed{
P^\star(x)=\frac1N,
\qquad x\in\mathcal X.
}
\]

The refinement language contains the true candidate

\[
r_0,
\qquad
Q_{r_0}=P^\star,
\]

and `N` concentrated alternatives

\[
r_1,\ldots,r_N.
\]

Fix

\[
q\in\left(\frac1N,1\right)
\]

and define, for `m=1,...,N`,

\[
Q_{r_m}(x)
=
\begin{cases}
q,&x=m,\\[1mm]
\dfrac{1-q}{N-1},&x\neq m.
\end{cases}
\]

Every candidate has full support. Hence all candidate laws and the true law are mutually absolutely continuous.

Let the discovery evidence consist of one draw

\[
X\sim P^\star.
\]

Define the empirical discovery law

\[
\widehat P_D=\delta_X.
\]

Select a candidate by maximum discovery likelihood:

\[
\widehat r
\in
\arg\max_{r\in\mathcal R} Q_r(X),
\qquad
\mathcal R=\{r_0,r_1,\ldots,r_N\}.
\]

Because

\[
q>\frac1N
\]

and

\[
q>\frac{1-q}{N-1},
\]

the maximizer is unique:

\[
\boxed{
\widehat r=r_X.
}
\]

The discovery sample therefore chooses the candidate whose distinguished coordinate is exactly the observation that occurred.

---

# 2. Theorem 13.4.1 — Arbitrarily Good Selected In-Sample Fit with Arbitrarily Bad Population Validity

For every discovery-fit tolerance

\[
\varepsilon_D>0
\]

and every target population discrepancy

\[
\gamma<1,
\]

there exist finite `N` and `q in (1/N,1)` such that:

1. the candidate class contains the exact true law `P*`;
2. maximum-likelihood selection on the discovery evidence chooses `r_X`, not the true candidate `r_0`;
3. the selected candidate fits the discovery empirical law within `epsilon_D` in total variation almost surely;
4. the selected candidate remains at least `gamma` away from the true empirical law in total variation almost surely.

Formally,

\[
\boxed{
\|\widehat P_D-Q_{\widehat r}\|_{\rm TV}
\le\varepsilon_D
\quad P^\star\text{-a.s.},
}
\]

while

\[
\boxed{
\|P^\star-Q_{\widehat r}\|_{\rm TV}
\ge\gamma
\quad P^\star\text{-a.s.}
}
\]

for suitable finite `N,q`.

## Proof

Condition on `X=m`. The selected candidate is `r_m`.

For the one-sample empirical law `delta_m`,

\[
\begin{aligned}
\|\delta_m-Q_{r_m}\|_{\rm TV}
&=
\frac12
\left(
|1-q|
+
\sum_{x\neq m}
\left|0-\frac{1-q}{N-1}\right|
\right)\\
&=
\frac12\left((1-q)+(1-q)\right)\\
&=1-q.
\end{aligned}
\]

Therefore

\[
\boxed{
\|\widehat P_D-Q_{\widehat r}\|_{\rm TV}=1-q
}
\]

almost surely.

Now compare the selected candidate to the true uniform law. Again for `X=m`,

\[
\begin{aligned}
\|P^\star-Q_{r_m}\|_{\rm TV}
&=
\frac12
\left(
\left|q-\frac1N\right|
+
(N-1)
\left|
\frac{1-q}{N-1}-\frac1N
\right|
\right).
\end{aligned}
\]

Since `q>1/N`, both absolute-value contributions equal `q-1/N` in total, giving

\[
\boxed{
\|P^\star-Q_{r_m}\|_{\rm TV}=q-\frac1N.
}
\]

Thus

\[
\boxed{
\|P^\star-Q_{\widehat r}\|_{\rm TV}
=q-\frac1N
}
\]

almost surely.

Choose `N` large enough that

\[
\frac1N<1-\gamma.
\]

Then choose

\[
q
>
\max\left\{
1-\varepsilon_D,
\gamma+\frac1N,
\frac1N
\right\}
\]

with `q<1`, which is possible by the choice of `N`.

This gives

\[
1-q<\varepsilon_D
\]

and

\[
q-\frac1N>\gamma.
\]

The true candidate `r_0` remains in the class throughout, but the discovery-likelihood selector chooses the concentrated candidate because `q>1/N`.

Therefore arbitrarily good selected discovery fit can coexist with arbitrarily poor population validity even under finite attainable coverage. `QED`

---

## 3. Fresh-observation failure

Let

\[
Y\sim P^\star
\]

be independent fresh evidence after selection.

Conditional on the discovery sample `X=m`, the selected candidate is `r_m`. The fresh observation lands on its high-probability coordinate only when `Y=m`. Therefore

\[
\boxed{
P^\star(Y=X\mid X)=\frac1N.
}
\]

Equivalently, if the candidate's distinguished prediction is scored by

\[
\ell_m(y)=\mathbf 1\{y\neq m\},
\]

then the selected candidate has discovery loss

\[
\ell_{\widehat r}(X)=0
\]

almost surely, but fresh conditional risk

\[
\boxed{
\mathbb E[\ell_{\widehat r}(Y)\mid X]
=1-\frac1N.
}
\]

Thus

\[
\boxed{
\text{zero selected discovery error}
\not\Rightarrow
\text{fresh predictive validity}.
}
\]

The failure can approach its maximal value as `N -> infinity`.

---

# 4. Theorem 13.4.2 — Fixed-Candidate Calibration Does Not Survive Adaptive Selection

The same witness shows why discovery evidence cannot be reused **as though the candidate had been fixed in advance**.

For a fixed concentrated candidate `r_m`, define the high-fit event

\[
C_m
=
\{x:Q_{r_m}(x)=q\}
=
\{m\}.
\]

Under the true law,

\[
\boxed{
P^\star(C_m)=\frac1N.
}
\]

So for a candidate fixed independently of the discovery draw, the high-fit event occurs with probability only `1/N`.

After adaptive selection, however,

\[
\widehat r=r_X,
\]

and therefore

\[
X\in C_{\widehat r}
\]

for every realized discovery sample. Hence

\[
\boxed{
P^\star(X\in C_{\widehat r})=1.
}
\]

The fixed-candidate calibration `1/N` has been transformed into probability one solely by selecting the candidate using the same observation.

Consequently, no uniformly valid rule may take the fixed-candidate probability of the observed fit event and reuse it unchanged after arbitrary adaptive selection.

More sharply, for any nominal level

\[
\alpha>0,
\]

choose `N` so that

\[
\frac1N\le\alpha.
\]

Then every fixed candidate has a high-fit event of probability at most `alpha`, yet the adaptively selected candidate realizes such an event with probability one.

Thus:

\[
\boxed{
\text{fixed-candidate calibration}
\not\Rightarrow
\text{post-selection calibration}.
}
\]

`QED`

---

# 5. Why this is a T13 firewall rather than an overfitting slogan

The counterexample isolates the exact T13 failure mode.

The discovery evidence is

\[
E_D=X.
\]

The selection mechanism is

\[
\widehat r=S(E_D)=r_X.
\]

If the selected candidate is then evaluated by the same discovery fit while pretending `r_hat` was fixed independently of `E_D`, the validation calculation uses the wrong reference law.

The invalid chain is

\[
\boxed{
E_D
\longrightarrow
\widehat r
\longrightarrow
\text{reuse }E_D\text{ under fixed-}r\text{ calibration}
\longrightarrow
\text{spurious authorization}.
}
\]

The admissible chain must instead be

\[
\boxed{
E_D
\longrightarrow
\widehat r
\longrightarrow
\text{selection-aware adjudication}
\longrightarrow
\mathsf{CWC}
\longrightarrow
\Gamma.
}
\]

Selection-aware adjudication can be supplied by fresh prospective evidence, held-out evidence, or a post-selection/sequential method whose validity theorem explicitly conditions on or otherwise accounts for the selection rule.

Literal dataset independence is sufficient but not necessary.

---

# 6. What is and is not proved

## Earned

The finite witness proves:

\[
\boxed{
\text{in-sample fit after adaptive candidate selection}
\not\Rightarrow
\text{candidate validity}.
}
\]

It also proves the stronger calibration statement:

\[
\boxed{
\text{a fixed-candidate validation calculation need not remain valid after candidate selection on the same evidence}.
}
\]

The failure persists even when:

```text
- the candidate class is finite;
- the true empirical law is exactly contained in the class;
- every candidate has full support;
- the selector is the ordinary maximum-likelihood rule;
- the discovery sample is generated exactly from the covered true law.
```

Thus the firewall cannot be dismissed as a consequence of coverage failure or singular models.

## Not earned

This theorem does **not** establish:

```text
- that discovery evidence can never contribute to later validation;
- that sample splitting is always necessary;
- that post-selection inference is impossible;
- that maximum likelihood generally fails;
- that rich refinement languages generally overfit;
- that a particular T13 constructor G should be used;
- that refinement construction has been demonstrated;
- that any new OpenCore architectural surface is required.
```

A selection-aware procedure may legitimately reuse discovery information if its error guarantee remains calibrated under the full selection-and-testing procedure.

---

# 7. T13 admission rule earned by the theorem

The precise firewall is:

> **A boundary-generated candidate may not inherit a fixed-candidate validity calculation from evidence used to select it. Any authorization claim must remain calibrated under the selection mechanism that produced the candidate.**

Symbolically,

\[
\boxed{
E_D
\rightarrow
r
\not\Rightarrow
E_D\text{ validates }r.
}
\]

Instead:

\[
\boxed{
E_D
\rightarrow
r
\rightarrow
a_r
\rightarrow
E_A^{\rm selection-aware}
\rightarrow
\mathsf{CWC}
\rightarrow
\Gamma.
}
\]

This is a theorem-level constraint on re-entry, not a new state variable or control surface.

---

# 8. Next proof

No construction experiment is authorized by this result.

The next proof should isolate T13.1 coverage with the exact distinction

\[
\boxed{
\inf_{r\in\mathcal R}\rho(P^\star,Q_r)\le\varepsilon
\quad\neq\quad
\exists r\in\mathcal R:\rho(P^\star,Q_r)\le\varepsilon
}
\]

at boundary cases where the infimum is not attained.

Only after coverage and constructive reachability are formalized should the program return to selection-aware empirical re-entry.