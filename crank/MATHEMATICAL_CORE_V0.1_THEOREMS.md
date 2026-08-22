# Mathematical Core v0.1 — Theorem Frontier

**Status:** `PROOF_FRONTIER`  
**Scope:** mathematical synthesis above the frozen OpenCore empirical lineage  
**Empirical authority:** none added by this document  
**New architectural primitive:** none  
**Frozen empirical artifacts modified:** none

This document translates the current OpenCore/CEA synthesis into a candidate mathematical program for:

> **Adaptive empirical model revision under endogenous measurement selection and evidence-constrained causal authority.**

The governing invariant is:

> **Every unresolved consequential distinction must retain a high-probability path to sufficient statistical separation before its consequence-relevant deadline, and no evidence-grounded causal update may depend on distinctions that the evidence has not identified.**

The purpose of this file is theorem seeking: definitions, theorem statements, proofs/counterexamples where available, and explicit open boundaries. It does not upgrade any empirical OpenCore claim.

The mathematical layer is explicitly quarantined from empirical authority:

```text
mathematical statement
!=
proved theorem
!=
empirical result
```

---

## 1. Core state and three adaptive surfaces

At time `t`, let

\[
\mathfrak S_t=(\Pi_t,\pi_t,\Gamma_t,\mathcal H_t),
\]

where:

- `Pi_t` is the current representation / quotient;
- `pi_t` is the current adaptive experiment or intervention policy;
- `Gamma_t` is the evidence-grounded authority map;
- `H_t` is the current live hypothesis family.

Let the world and measurement process generate

\[
X_{t+1}\sim K(\cdot\mid X_t,A_t),
\qquad
Y_{t+1}\sim M(\cdot\mid X_{t+1},A_t),
\]

and let

\[
Z_{t+1}=\Pi_t(Y_{t+1}).
\]

The adaptive empirical loop is

\[
\boxed{
\mathfrak S_t
\rightarrow
A_t
\rightarrow
Y_{t+1}
\rightarrow
Z_{t+1}
\rightarrow
\mathfrak S_{t+1}.
}
\]

The three adaptive control surfaces are deliberately distinct:

```text
Pi-failure     a needed distinction is erased by representation
pi-failure     a needed discriminator is not reached in a useful way
Gamma-failure  causal treatment depends on distinctions not identified by evidence
```

Ordinary inference/update correctness remains part of the transition mechanism `Phi`; the three surfaces are not claimed to exhaust every possible mechanism-level failure.

---

## 2. Closed-world questions and boundary questions

The current research hierarchy is diagnostic, not architectural:

```text
Q1  Representation
    Can the current representation preserve a live distinction?

Q2  Exposure
    Can the current policy reach a discriminator in time?

Q3  Attribution / authority
    Does evidence constrain causal treatment only along identified distinctions?

Q4  Boundary adequacy
    Can the system detect that the entire current empirical model class is inadequate?

Q5  Refinement construction
    Under what assumptions can a new empirical distinction / representation be constructed?

Q6  Empirical re-entry
    Once proposed, can the refinement be independently adjudicated and earn scoped authority?
```

`Q1-Q3` are closed-world relative to `(Pi_t,H_t)`. `Q4` diagnoses exhaustion of that boundary. `Q5` is construction. `Q6` returns the candidate to ordinary empirical adjudication.

The critical non-implications are:

\[
\boxed{
\text{permission to leave the current model}
\neq
\text{knowledge of the replacement}
\neq
\text{validation of the replacement}.
}
\]

---

## 3. Represented experiment kernels

For hypothesis `H_i` and intervention `a`, let the physical observation kernel be

\[
P_i^a(dy)=P(dY\in dy\mid do(a),H_i).
\]

The represented kernel is the pushforward

\[
\boxed{
Q_{i,t}^a=(\Pi_t)_\#P_i^a.
}
\]

Define the represented discriminating set

\[
\boxed{
D_t(i,j)=\{a:Q_{i,t}^a\neq Q_{j,t}^a\}.
}
\]

Representational collapse occurs when

\[
P_i^a\neq P_j^a
\quad\text{but}\quad
Q_{i,t}^a=Q_{j,t}^a.
\]

The evidence-grounded authority condition is stated through the evidence-induced equivalence relation:

\[
\boxed{
H_i\sim_{E_t}H_j
\Longrightarrow
\Gamma_t(E_t,H_i)=\Gamma_t(E_t,H_j).
}
\]

Equivalently, an evidence-grounded authority rule must factor through the evidence quotient.

---

## 4. Closed-world theorem targets T1-T5

### T1 — Representation impossibility

If two live hypotheses induce the same represented conditional law for every action reachable by a common represented-history policy, then they induce the same represented adaptive path law. No estimator measurable with respect to that history can consistently distinguish them.

This is the base interface impossibility.

### T2 — Exposure impossibility

Even when `D(i,j)` is nonempty, consistent discrimination can fail if the endogenous policy supplies insufficient cumulative information to the distinguishing actions.

This formalizes:

```text
physical / represented identifiability
!=
actual identifying exposure
```

### T3 — Authority factorization

For evidence `E`, let

\[
q_E:\mathcal H\to\mathcal H/{\sim_E}
\]

be the quotient map. A deterministic authority rule is calibrated to `E` iff there exists `Gamma_tilde_E` such that

\[
\boxed{
\Gamma_E=\widetilde\Gamma_E\circ q_E.
}
\]

Thus evidence-indistinguishable worlds cannot receive different evidence-grounded treatment.

### T4 — Timeliness

Positive support and even eventual exposure need not imply useful correction latency. Timeliness must be expressed at the level of statistical separation achieved before a consequence-relevant deadline.

### T5 — Safe compression

A coarser representation is weakly safe for the current live consequential family only if it preserves the required discriminating relations. A stronger notion is Blackwell equivalence of the induced statistical experiments on the relevant family.

No scalar optimization over representation, policy, and authority complexity is frozen.

---

## 5. Boundary adequacy and representation invention

Mathematical Core v0.1 is closed-world with respect to the current empirical representation and live hypothesis family. It does not guarantee discovery of distinctions outside that boundary.

### T6 — Closed-boundary impossibility

If two possible worlds induce the same complete represented adaptive path law under the current experiment/representation boundary, every history-confined detector has the same law in the two worlds. No internal procedure can identify the missing distinction from that history.

### T7 — Model-class inadequacy detectability

Let `P*` be the true represented empirical process and `P(H_t)` the current represented model family. Under sufficient adaptive exposure and positive separation, seek conditions under which a sequential procedure can earn only:

```text
CURRENT_MODEL_CLASS_INADEQUATE
```

meaning

\[
P^\star\notin\overline{\mathcal P(\Pi_t,\mathcal H_t)}
\]

under the frozen empirical topology and discrepancy criterion.

This does not imply that `Pi_t` is the failure locus and does not identify a successor.

### T8 — No-free representation invention

Boundary-inadequacy evidence alone cannot uniquely determine a correct successor refinement when multiple successor worlds are observationally equivalent through the boundary-detection time but require incompatible refinements.

### T9 — Refinement constructibility under search coverage

Given a refinement language `R` and constructor/search mechanism `G`, characterize the conditions under which an empirically adequate refinement is constructively reachable.

Necessary distinctions include:

```text
refinement exists in R
!=
constructor can reach it
!=
refinement is empirically adjudicable
```

### T10 — Empirical re-entry

Once a refinement is proposed, it must return to the closed-world core: derive a prospective discriminator, obtain fresh evidence, and earn only the authority that evidence identifies.

Discovery evidence does not automatically authorize the representation it generated.

---

## 6. T11 — Empirical coverage of a refinement language

Let a refinement `r in R` induce an experiment-indexed represented family

\[
Q_r=\{Q_r^a:a\in\mathcal A\}.
\]

Choose an empirical metric or pseudometric `rho` on these experiment families and define

\[
\mathcal Q_{\mathcal R}=\{Q_r:r\in\mathcal R\}.
\]

For the true empirical law `P*`, define

\[
\boxed{
\epsilon_{\mathcal R}(P^\star)
=
\inf_{r\in\mathcal R}
\rho(P^\star,Q_r).
}
\]

The foundational coverage statement is

\[
\boxed{
P^\star\notin\overline{\mathcal Q_{\mathcal R}}^{\,\rho}
\iff
\epsilon_{\mathcal R}(P^\star)>0.
}
\]

The closure must be empirical, not merely syntactic. A successor representation can be absent from the syntactic language while its observable behavior is arbitrarily approximable by members of the language.

Thus:

```text
epsilon_R = 0 and P* in Q_R
    exact empirical coverage

epsilon_R = 0 and P* not in Q_R
    arbitrarily good approximate coverage

epsilon_R > 0
    irreducible empirical coverage failure
```

This preserves the physics lesson:

> **Preserve successful empirical behavior, not necessarily the old ontology.**

---

## 7. T12a — Adaptive Path Information Identity

**Status:** `PROVED`.

Let

\[
H_n=(A_1,Z_1,\ldots,A_n,Z_n),
\qquad
\mathcal F_{t-1}=\sigma(A_1,Z_1,\ldots,A_{t-1},Z_{t-1}).
\]

Assume:

1. under every hypothesis, the action is selected from the same stochastic kernel
   \[
   \pi_t(da_t\mid h_{t-1});
   \]
2. for the forward `i -> j` identity, `Q_i^a << Q_j^a` for every action relevant under `P_i` and the policy;
3. the likelihood-ratio integrals are interpreted in the extended sense when necessary.

Under `H_i`, the adaptive path law is

\[
P_i^{\pi,n}(dh_n)
=
\prod_{t=1}^n
\pi_t(da_t\mid h_{t-1})
Q_i^{a_t}(dz_t).
\]

Because the policy kernel is the same conditional on the represented history,

\[
\frac{dP_i^{\pi,n}}{dP_j^{\pi,n}}(H_n)
=
\prod_{t=1}^n
\frac{dQ_i^{A_t}}{dQ_j^{A_t}}(Z_t).
\]

Define

\[
\ell_t^{i\to j}
=
\log\frac{dQ_i^{A_t}}{dQ_j^{A_t}}(Z_t),
\qquad
\mathcal G_t=\sigma(\mathcal F_{t-1},A_t).
\]

Then

\[
g_t^{i\to j}
:=
\mathbb E_i[\ell_t^{i\to j}\mid\mathcal G_t]
=
D_{\mathrm{KL}}(Q_i^{A_t}\Vert Q_j^{A_t}).
\]

Let

\[
G_n^{i\to j}=\sum_{t=1}^n g_t^{i\to j},
\qquad
K_n^{i\to j}=\mathbb E_i[G_n^{i\to j}].
\]

Taking the expectation of the path log-likelihood ratio gives

\[
\boxed{
K_n^{i\to j}
=
D_{\mathrm{KL}}(P_i^{\pi,n}\Vert P_j^{\pi,n})
=
\mathbb E_i
\left[
\sum_{t=1}^n
D_{\mathrm{KL}}(Q_i^{A_t}\Vert Q_j^{A_t})
\right].
}
\]

The reverse identity is a separate statement using `Q_j^a << Q_i^a`. If finite likelihood ratios in both directions are desired on all relevant experiments, one may impose mutual absolute continuity `Q_i^a ~ Q_j^a`.

**Interpretation:** potential experiment information and path information actually acquired under endogenous selection are different objects.

---

## 8. T12b — Refinement Entropy Lower Bound

**Status:** classical information-theoretic machinery specialized to the adaptive path law.

Let

\[
\{r_1,\ldots,r_N\}\subset\mathcal R
\]

be a finite empirically separated candidate set and let `J` be uniform on `{1,...,N}`.

For any estimator `J_hat(H_n)`, Fano gives

\[
P_e
\ge
1-
\frac{I(J;H_n)+\log 2}{\log N}.
\]

Writing `P_bar=(1/N) sum_j P_j`, convexity of KL in its second argument gives

\[
I(J;H_n)
=
\frac1N\sum_i D_{\mathrm{KL}}(P_i^{\pi,n}\Vert P_{\rm bar}^{\pi,n})
\le
\frac{1}{N^2}\sum_{i,j}
D_{\mathrm{KL}}(P_i^{\pi,n}\Vert P_j^{\pi,n}).
\]

Using T12a,

\[
I(J;H_n)
\le
\frac{1}{N^2}
\sum_{i,j}
\mathbb E_i
\sum_{t=1}^n
D_{\mathrm{KL}}(Q_i^{A_t}\Vert Q_j^{A_t}).
\]

Define

\[
\bar\kappa_n
=
\frac{1}{nN^2}
\sum_{i,j}
\mathbb E_i
\sum_{t=1}^n
D_{\mathrm{KL}}(Q_i^{A_t}\Vert Q_j^{A_t}).
\]

Then

\[
\boxed{
P_e
\ge
1-
\frac{n\bar\kappa_n+\log2}{\log N}.
}
\]

Thus a necessary finite-horizon scaling relation is schematically

\[
\boxed{
\log N_\varepsilon(\mathcal R)
\lesssim
I_\pi^{(n)}(\mathcal R),
}
\]

with constants and the exact empirical packing/separation criterion fixed by the theorem instance.

The distinctive coupling is not Fano itself. It is that the refinement family can change the endogenous policy that determines `I_pi^(n)`.

---

## 9. T12c — Endogenous Refinement Collapse

**Status:** `PROVED_EXISTENCE_COUNTEREXAMPLE`; not a robust policy theorem.

There exist nested finite refinement languages

\[
\mathcal R\subset\mathcal R',
\]

a fixed true empirical process `P*`, and a single class-dependent experiment-selection rule such that

\[
\epsilon_{\mathcal R'}(P^\star)
<
\epsilon_{\mathcal R}(P^\star),
\]

while an unresolved pair has strictly less acquired discriminating information under the richer class, in the minimal construction collapsing to exactly zero.

Take actions `{a,b}`, binary observations, and `0<delta<1/4`:

| refinement | `Q^a(Z=1)` | `Q^b(Z=1)` |
| --- | ---: | ---: |
| `r0` | `0.75` | `0.75-delta` |
| `r1` | `0.25` | `0.75-delta` |
| `r*` | `0.75` | `0.75+delta` |
| `r2` | `0.25` | `0.75+delta` |

Let reality be `P*=Q_r*`, and let

```text
R  = {r0,r1}
R' = {r0,r1,r*,r2}
```

Use the same class-dependent rule

\[
\pi_{\mathcal C}
=
\arg\max_{x\in\{a,b\}}
\sup_{r\in\mathcal C}\mathbb E_r[Z\mid x].
\]

For `R`, the rule selects `a`, which distinguishes `r0` from `r1` with positive KL. For `R'`, the rule selects `b`, but

\[
Q_{r^\star}^b=Q_{r_2}^b,
\]

so

\[
\boxed{
K_n(r^\star,r_2;\pi_{\mathcal R'})=0
\quad\text{for every }n.
}
\]

At the same time, `R'` contains the truth exactly while `R` has positive empirical coverage error under the max-action total-variation metric.

Therefore:

> **Improved representational coverage need not monotonically improve empirical learnability when the refinement language itself influences experiment selection.**

This proves possibility, not prevalence.

---

## 10. T12d — Policy Robustness Frontier

**Status:** `OPEN`.

Test endogenous refinement collapse or slowdown under progressively more standard adaptive policies:

```text
P1  posterior-greedy task utility
P2  Thompson sampling
P3  UCB
P4  myopic expected information gain
P5  finite-horizon Bayes-optimal experiment design
```

The quantifiers must remain explicit.

Weak form:

\[
\exists\Psi\in\mathfrak P\;\exists\mathcal R\subset\mathcal R'\;\exists P^\star:
\text{collapse or slowdown occurs}.
\]

Stronger forms reverse or move the policy quantifier and should not be asserted without proof.

The outcome should distinguish:

```text
foreclosure      finite total path information
sublinear        information diverges but slower than linearly
linear           positive asymptotic information rate
timely           enough statistical separation within the relevant deadline
```

---

## 11. T12e — From Information Accounting to Timely Adjudication

T12e is a sequential-testing theorem program. The frozen hierarchy is

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
\mathsf{Sep}_{t,H}.
}
\]

Interpretation:

```text
I*          potential discriminating information
K_n         expected path-space information under the endogenous policy
G_n         predictable information budget on the realized adaptive action path
L_n         realized likelihood evidence
Sep_{t,H}   finite-horizon statistical separability of the conditional path laws
```

No implication between adjacent objects is granted without explicit conditions.

### 11.1 Directed likelihood objects

For testing `H_i` against `H_j`, define

\[
\ell_t^{i\to j}
=
\log\frac{dQ_i^{A_t}}{dQ_j^{A_t}}(Z_t),
\qquad
\mathcal G_t=\sigma(\mathcal F_{t-1},A_t),
\]

and

\[
g_t^{i\to j}
=
\mathbb E_i[\ell_t^{i\to j}\mid\mathcal G_t]
=
D_{\mathrm{KL}}(Q_i^{A_t}\Vert Q_j^{A_t}).
\]

Let

\[
G_n^{i\to j}=\sum_{t=1}^n g_t^{i\to j},
\]

\[
M_n^{i\to j}
=
\sum_{t=1}^n
(\ell_t^{i\to j}-g_t^{i\to j}),
\]

and

\[
\boxed{
L_n^{i\to j}
=
G_n^{i\to j}+M_n^{i\to j}.
}
\]

Under the forward absolute-continuity and integrability conditions, `M_n^{i->j}` is a martingale under `P_i` with respect to the filtration after observation `Z_t` is incorporated.

The deterministic expected path information is

\[
\boxed{
K_n^{i\to j}
:=D_{\mathrm{KL}}(P_i^{\pi,n}\Vert P_j^{\pi,n})
=\mathbb E_i[G_n^{i\to j}].
}
\]

The reverse direction is separate:

\[
K_n^{j\to i}
=D_{\mathrm{KL}}(P_j^{\pi,n}\Vert P_i^{\pi,n}),
\]

and need not equal the forward quantity.

---

### T12e.1 — Necessary Directed Divergence

**Status:** `PROVED`.

Let `phi_n in {i,j}` be any sequence of binary tests and define

\[
\alpha_n=P_i(\phi_n=j),
\qquad
\beta_n=P_j(\phi_n=i).
\]

If

\[
\alpha_n\to0,
\qquad
\beta_n\to0,
\]

then

\[
\boxed{
K_n^{i\to j}\to\infty,
\qquad
K_n^{j\to i}\to\infty.
}
\]

#### Proof

Map the path `H_n` to the binary decision `1{phi_n=i}`. Under `P_i` this decision has law `Bernoulli(1-alpha_n)`; under `P_j` it has law `Bernoulli(beta_n)`.

By data processing,

\[
D_{\mathrm{KL}}(P_i^{\pi,n}\Vert P_j^{\pi,n})
\ge
D_{\mathrm{KL}}
\left(
\mathrm{Bern}(1-\alpha_n)
\Vert
\mathrm{Bern}(\beta_n)
\right).
\]

The right-hand side diverges when `alpha_n -> 0` and `beta_n -> 0`, because its leading term contains

\[
(1-\alpha_n)
\log\frac{1-\alpha_n}{\beta_n}
\to\infty.
\]

Therefore `K_n^{i->j} -> infinity` by T12a. Exchanging `i` and `j` gives the reverse conclusion. `QED`

No pathwise conclusion about `G_n` follows from this theorem.

---

### T12e.2 — Two-Directed Expected Divergence Is Insufficient

**Status:** `PROVED_COUNTEREXAMPLE`.

There exist two hypothesis laws for which

\[
K_n^{i\to j}\to\infty
\quad\text{and}\quad
K_n^{j\to i}\to\infty,
\]

while no sequence of tests has both errors tending to zero.

#### Construction

Let

\[
p_t=2^{-t},
\qquad
q_t=p_t\exp\left(-\frac{1}{tp_t}\right),
\]

and let `Z_t in {0,+,-}` be independent across time.

Under `H_i`,

\[
P_i^t(+)=p_t,
\qquad
P_i^t(-)=q_t,
\qquad
P_i^t(0)=1-p_t-q_t.
\]

Under `H_j`, swap `+` and `-`:

\[
P_j^t(+)=q_t,
\qquad
P_j^t(-)=p_t,
\qquad
P_j^t(0)=1-p_t-q_t.
\]

For one observation,

\[
\begin{aligned}
D_{\mathrm{KL}}(P_i^t\Vert P_j^t)
&=
p_t\log\frac{p_t}{q_t}
+q_t\log\frac{q_t}{p_t}\\
&=(p_t-q_t)\log\frac{p_t}{q_t}\\
&=\frac{1-q_t/p_t}{t}.
\end{aligned}
\]

Since

\[
q_t/p_t
=\exp\left(-\frac{1}{tp_t}\right)
\to0,
\]

we have

\[
D_{\mathrm{KL}}(P_i^t\Vert P_j^t)\sim\frac1t.
\]

By symmetry the reverse divergence is identical. Independence gives

\[
\boxed{
K_n^{i\to j}\sim\log n,
\qquad
K_n^{j\to i}\sim\log n.
}
\]

However,

\[
\sum_t(p_t+q_t)<\infty,
\]

so

\[
\prod_{t=1}^{\infty}(1-p_t-q_t)>0.
\]

Thus the all-zero infinite trajectory is a common atom with positive probability under both infinite product measures. The two infinite path laws are therefore not mutually singular.

If tests with `alpha_n -> 0` and `beta_n -> 0` existed, their error sum would tend to zero, forcing the total variation distance of the finite-prefix laws to tend to one. The limiting infinite path laws would then be mutually singular, contradiction. `QED`

Therefore

\[
\boxed{
K_n^{i\to j}\to\infty
\;\land\;
K_n^{j\to i}\to\infty
\not\Rightarrow
\text{consistent discrimination}.
}
\]

**Interpretation:** even unlimited expected path information in both directions can be carried by increasingly rare, increasingly extreme evidence while typical histories remain ambiguous.

---

### T12e.3 — Pathwise Divergence plus Relative-Noise Control

**Status:** `PROVED_UNDER_STATED_CONDITIONS`.

Assume under `H_i`:

\[
G_n^{i\to j}\to\infty
\quad P_i\text{-a.s.},
\]

and

\[
\frac{M_n^{i\to j}}{G_n^{i\to j}}
\to0
\quad P_i\text{-a.s.}
\]

Assume separately under `H_j`:

\[
G_n^{j\to i}\to\infty
\quad P_j\text{-a.s.},
\]

and

\[
\frac{M_n^{j\to i}}{G_n^{j\to i}}
\to0
\quad P_j\text{-a.s.}
\]

Then the likelihood-ratio sign decision is strongly consistent.

#### Proof

Under `H_i`,

\[
\frac{L_n^{i\to j}}{G_n^{i\to j}}
=
1+
\frac{M_n^{i\to j}}{G_n^{i\to j}}
\to1
\quad P_i\text{-a.s.},
\]

and `G_n^{i->j} -> infinity`, so

\[
L_n^{i\to j}\to+\infty
\quad P_i\text{-a.s.}
\]

Under `H_j`, the corresponding argument gives

\[
L_n^{j\to i}\to+\infty
\quad P_j\text{-a.s.}
\]

When the two likelihood ratios are mutually well-defined,

\[
L_n^{j\to i}=-L_n^{i\to j},
\]

so

\[
L_n^{i\to j}\to-\infty
\quad P_j\text{-a.s.}
\]

Hence the decision

\[
\phi_n=
\begin{cases}
i,&L_n^{i\to j}\ge0,\\
j,&L_n^{i\to j}<0
\end{cases}
\]

is eventually correct almost surely under either hypothesis. In particular,

\[
P_i(\phi_n=j\ \text{i.o.})=0,
\qquad
P_j(\phi_n=i\ \text{i.o.})=0.
\]

Therefore both ordinary error probabilities tend to zero. `QED`

The foundational theorem intentionally leaves `M_n/G_n -> 0` as an assumption. Bounded-increment, predictable-variance, sub-Gaussian, sub-exponential, or self-normalized conditions belong in separate corollaries.

---

### T12e.4a — Terminal Finite-Horizon Adjudication Sufficiency

**Status:** `PROVED_UNDER_EXPLICIT_FREEDMAN_CONDITIONS`.

This theorem concerns a **terminal** decision at `t+H`. It does not authorize commitment at arbitrary intermediate times.

Fix a current time `t` and condition on the full current filtration `F_t`. If a particular model assumes that `S_t` is sufficient for the future conditional experiment law, `F_t` may then be replaced by `S_t` as a corollary.

For the forward direction define

\[
G_{t,H}^{i\to j}
=
\sum_{k=1}^{H}
g_{t+k}^{i\to j},
\]

\[
M_{t,H}^{i\to j}
=
\sum_{k=1}^{H}
(\ell_{t+k}^{i\to j}-g_{t+k}^{i\to j}),
\]

and

\[
L_{t,H}^{i\to j}
=
G_{t,H}^{i\to j}+M_{t,H}^{i\to j}.
\]

Assume under `H_i`, almost surely conditional on `F_t`:

1. high-probability predictable information:
   \[
   P_i\left(
   G_{t,H}^{i\to j}\ge\beta_i
   \mid\mathcal F_t
   \right)
   \ge1-\xi_i;
   \]
2. centered increments
   \[
   X_{t+k}^{i\to j}
   :=\ell_{t+k}^{i\to j}-g_{t+k}^{i\to j}
   \]
   satisfy `|X_{t+k}^{i->j}| <= b_i`;
3. the predictable quadratic variation over the window satisfies
   \[
   V_{t,H}^{i\to j}
   :=
   \sum_{k=1}^{H}
   \mathbb E_i\left[
   (X_{t+k}^{i\to j})^2
   \mid\mathcal G_{t+k}
   \right]
   \le v_i.
   \]

Consider the conditional window likelihood-ratio test with zero threshold:

\[
\widehat H_{t+H}
=
\begin{cases}
i,&L_{t,H}^{i\to j}\ge0,\\
j,&L_{t,H}^{i\to j}<0.
\end{cases}
\]

Then

\[
\boxed{
P_i(
\widehat H_{t+H}=j
\mid\mathcal F_t)
\le
\xi_i+
\exp\left[
-\frac{\beta_i^2}
{2(v_i+b_i\beta_i/3)}
\right].
}
\]

#### Proof

On the event `G_{t,H}^{i->j} >= beta_i`, a terminal error requires

\[
L_{t,H}^{i\to j}<0,
\]

hence

\[
M_{t,H}^{i\to j}< -G_{t,H}^{i\to j}\le-\beta_i.
\]

Therefore, by a union bound,

\[
P_i(\widehat H_{t+H}=j\mid\mathcal F_t)
\le
P_i(G_{t,H}^{i\to j}<\beta_i\mid\mathcal F_t)
+
P_i(M_{t,H}^{i\to j}\le-\beta_i\mid\mathcal F_t).
\]

The first term is at most `xi_i`. Applying the lower-tail form of Freedman's inequality to the bounded martingale differences gives

\[
P_i(M_{t,H}^{i\to j}\le-\beta_i\mid\mathcal F_t)
\le
\exp\left[
-\frac{\beta_i^2}
{2(v_i+b_i\beta_i/3)}
\right].
\]

Combining the two terms proves the claim. `QED`

The reverse direction is **not** hidden in symmetry. Assume separately under `H_j` corresponding constants `(beta_j,xi_j,b_j,v_j)` for `G_{t,H}^{j->i}` and its martingale differences. Then

\[
\boxed{
P_j(
\widehat H_{t+H}=i
\mid\mathcal F_t)
\le
\xi_j+
\exp\left[
-\frac{\beta_j^2}
{2(v_j+b_j\beta_j/3)}
\right].
}
\]

If both directed upper bounds are at most `delta`, the pair is terminally `(H,delta)`-adjudicable from time `t` under these sufficient conditions.

For nonzero prior log-odds or another terminal decision threshold, the proof carries through with the corresponding threshold shift; the zero-threshold statement is the clean equal-prior/window-likelihood form.

---

### T12e.4b — Anytime Finite-Horizon Adjudication

**Status:** `OPEN`.

A terminal guarantee does not control a procedure allowed to make an irrevocable attribution at an arbitrary intermediate time `t+1,...,t+H`.

The relevant bad event is pathwise, for example

\[
\left\{
\exists k\le H:
L_{t,k}^{i\to j}\le c_k
\right\},
\]

for a sequential decision boundary `c_k`.

A single-terminal-time Freedman application is insufficient. Candidate machinery includes Ville-type likelihood bounds, test martingales, mixture martingales, maximal martingale inequalities, and confidence-sequence boundaries.

The permanent distinction is

\[
\boxed{
\text{correct at the deadline}
\neq
\text{safe to commit at every time before the deadline}.
}
\]

---

### T12e.5 — Sharp Path-Law Separation Characterization

**Status:** `OPEN`.

KL is accounting and sufficient machinery, not the final adjudication property.

Condition on the current history `F_t` and let

\[
P_{i,t:H}^{\pi}
\quad\text{and}\quad
P_{j,t:H}^{\pi}
\]

be the two conditional future path laws over the next `H` adaptive action-observation steps.

Define terminal finite-horizon separation by total variation:

\[
\boxed{
\mathsf{Sep}_{t,H}(i,j)
=
\left\|
P_{i,t:H}^{\pi}
-
P_{j,t:H}^{\pi}
\right\|_{\mathrm{TV}}.
}
\]

For equal-prior binary testing of these two conditional path laws,

\[
P_e^\star
=
\frac12
\left(1-\mathsf{Sep}_{t,H}(i,j)\right).
\]

Therefore the sharp terminal target for Bayes error at most `delta` is

\[
\boxed{
\mathsf{Sep}_{t,H}(i,j)
\ge1-2\delta.
}
\]

The open work is to characterize this separation sharply for adaptive filtered experiments, likely using total variation, Hellinger affinity/processes, likelihood processes, or equivalent sequential-statistical objects.

Predictable KL plus concentration is one tractable sufficient route. It is not the target property itself.

---

## 12. Current Mathematical Chain

The frozen separation is

\[
\boxed{
I^\star
\not\Rightarrow
K_n
\not\Rightarrow
G_n
\not\Rightarrow
L_n
\not\Rightarrow
\mathsf{Sep}_{t,H}.
}
\]

In words:

```text
potential discriminating information
!=
expected path-space information under the policy
!=
predictable information on the realized adaptive action path
!=
realized likelihood evidence
!=
finite-horizon statistical separation
```

The strongest negative currently proved in this chain is

\[
\boxed{
K_n^{i\to j}\to\infty
\;\land\;
K_n^{j\to i}\to\infty
\not\Rightarrow
\text{consistent discrimination}.
}
\]

This is the mathematical analogue of the empirical distinctions accumulated across PCE/CSD/MAB-OS, but it does not upgrade those empirical claims.

The methodological rule is:

\[
\boxed{
\begin{aligned}
K_n &: \text{information accounting},\\
L_n &: \text{realized evidence},\\
\mathsf{Sep} &: \text{adjudication property},\\
\mathsf{Sep}_{t,H}\text{ before the deadline} &: \text{corrigibility property}.
\end{aligned}
}
\]

---

## 13. Theorem Status and Immediate Proof Frontier

| Result | Status | Scope |
| --- | --- | --- |
| `T12a` | **PROVED** | adaptive path-KL identity under stated kernel/absolute-continuity conditions |
| `T12b` | **CLASSICAL MACHINERY** | Fano/pairwise-KL lower bound specialized to adaptive path laws |
| `T12c` | **PROVED EXISTENCE COUNTEREXAMPLE** | richer empirical coverage can induce lower identifying information under a class-dependent policy |
| `T12d` | **OPEN** | robustness under natural policy classes |
| `T12e.1` | **PROVED** | vanishing two-sided testing error requires both directed path KLs to diverge |
| `T12e.2` | **PROVED COUNTEREXAMPLE** | both directed expected path KLs can diverge while consistent testing remains impossible |
| `T12e.3` | **PROVED UNDER CONDITIONS** | pathwise predictable divergence plus relative-noise control gives strong consistency |
| `T12e.4a` | **PROVED UNDER FREEDMAN CONDITIONS** | terminal finite-horizon sufficient error bound |
| `T12e.4b` | **OPEN** | anytime finite-horizon adjudication |
| `T12e.5` | **OPEN** | sharp TV/Hellinger/path-process characterization |

The next proof effort is deliberately restricted to:

```text
T12e.4b  derive an anytime finite-horizon guarantee with explicit sequential boundaries
T12e.5   identify the sharp path-law separation characterization
```

`T13` remains closed until these questions are resolved or produce a counterexample requiring revision.

---

## 14. Claim Ceiling and Open Boundary

This document does **not** establish:

```text
a universal theory of scientific discovery
a universal creativity mechanism
a fourth adaptive control surface
a universal scalar objective
that KL is the final notion of challengeability
that richer refinement classes generally self-seal
that T12c survives natural policy classes
that model-class inadequacy identifies representation failure
that boundary pressure contains the successor representation
that terminal correctness implies anytime-safe authority transfer
```

The hardest open construction arrow remains

\[
\boxed{
\texttt{CURRENT_MODEL_CLASS_INADEQUATE}
\rightarrow
?
\rightarrow
(\Pi_{t+1},\mathcal H_{t+1}).
}
\]

That arrow is intentionally not being worked while T12e.4b/e.5 remain open.

---

## 15. Frozen Field-Level Description

> **Adaptive empirical model revision under endogenous measurement selection and evidence-constrained causal authority.**

Operationally:

```text
compress
-> test
-> identify
-> attribute
-> authorize
-> act
-> remain challengeable
```

The current theorem-compatible meaning of the last clause is:

> **Every unresolved consequential distinction must retain a high-probability route to sufficient statistical separation before its consequence-relevant deadline.**

The conceptual phase is frozen. New authority at this layer now comes from proofs, counterexamples, or explicit failure of the stated assumptions.