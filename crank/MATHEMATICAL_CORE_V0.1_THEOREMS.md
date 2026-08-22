# Mathematical Core v0.1 — Theorem Frontier

**Status:** `THEOREM_SEEKING_DRAFT`  
**Scope:** mathematical synthesis above the frozen OpenCore empirical lineage  
**Empirical authority:** none added by this document  
**New architectural primitive:** none  
**Frozen empirical artifacts modified:** none

This document translates the current OpenCore/CEA synthesis into a candidate mathematical program for:

> **Adaptive empirical model revision under endogenous measurement selection and evidence-constrained causal authority.**

The governing invariant is:

> **Every unresolved consequential distinction must retain a high-probability path to sufficient statistical separation before its consequence-relevant deadline, and no evidence-grounded causal update may depend on distinctions that the evidence has not identified.**

The purpose of this file is theorem seeking: definitions, theorem statements, proofs/counterexamples where available, and explicit open boundaries. It does not upgrade any empirical OpenCore claim.

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
P_i^a(dy)=P(dY=y\mid do(a),H_i).
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

Let

\[
H_n=(A_1,Z_1,\ldots,A_n,Z_n).
\]

Under refinement `r_i`, suppose the adaptive path law is

\[
P_i^{\pi,n}(dh_n)
=
\prod_{t=1}^n
\pi_t(da_t\mid h_{t-1})
Q_i^{a_t}(dz_t),
\]

where the same represented-history policy kernel `pi_t` is used under every candidate and the required absolute-continuity conditions hold.

Then

\[
\frac{dP_i^{\pi,n}}{dP_j^{\pi,n}}(H_n)
=
\prod_{t=1}^n
\frac{dQ_i^{A_t}}{dQ_j^{A_t}}(Z_t),
\]

because the action-policy factors cancel conditionally on the same represented history.

Therefore

\[
\boxed{
D_{\mathrm{KL}}
(P_i^{\pi,n}\Vert P_j^{\pi,n})
=
\mathbb E_i
\left[
\sum_{t=1}^n
D_{\mathrm{KL}}
(Q_i^{A_t}\Vert Q_j^{A_t})
\right].
}
\]

This separates information potentially available from information actually acquired under endogenous selection.

---

## 8. T12b — Refinement entropy lower bound

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

A standard pairwise upper bound on mutual information combined with T12a yields an acquired-information quantity of the form

\[
I(J;H_n)
\le
\frac{1}{N^2}
\sum_{i,j}
\mathbb E_i
\sum_{t=1}^n
D_{\mathrm{KL}}
(Q_i^{A_t}\Vert Q_j^{A_t}).
\]

Define the average adaptive information rate

\[
\bar\kappa_n
=
\frac{1}{nN^2}
\sum_{i,j}
\mathbb E_i
\sum_{t=1}^n
D_{\mathrm{KL}}
(Q_i^{A_t}\Vert Q_j^{A_t}).
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

Thus a necessary finite-horizon scaling relation is

\[
\boxed{
\log N_\varepsilon(\mathcal R)
\lesssim
I_\pi^{(n)}(\mathcal R),
}
\]

with constants and the exact empirical packing/separation criterion fixed by the theorem instance.

The distinctive coupling is that the refinement family can change the policy that determines `I_pi^(n)`.

---

## 9. T12c — Endogenous Refinement Collapse

**Status:** existence counterexample; not yet a robust policy theorem.

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

A concrete witness uses actions `{a,b}` and binary observations. For `0<delta<1/4`, define

| refinement | `Q^a(Z=1)` | `Q^b(Z=1)` |
| --- | ---: | ---: |
| `r0` | `0.75` | `0.75-delta` |
| `r1` | `0.25` | `0.75-delta` |
| `r*` | `0.75` | `0.75+delta` |
| `r2` | `0.25` | `0.75+delta` |

Let reality be `P*=Q_r*`, let

```text
R  = {r0,r1}
R' = {r0,r1,r*,r2}
```

and use the same optimistic class-dependent rule

\[
\pi_{\mathcal C}
=
\arg\max_{x\in\{a,b\}}
\sup_{r\in\mathcal C}\mathbb E_r[Z\mid x].
\]

For `R`, the rule selects `a`, which distinguishes `r0` and `r1` with positive KL. For `R'`, the rule selects `b`, but

\[
Q_{r^\star}^b=Q_{r_2}^b,
\]

so the relevant cumulative path information is exactly zero for every horizon.

At the same time, `R'` has exact empirical coverage of `P*` while `R` does not.

Therefore:

> **Improved representational coverage need not monotonically improve empirical learnability when the refinement language itself influences experiment selection.**

This proves possibility, not prevalence. T12d asks whether related collapse or slowdown survives under materially broader policy classes.

---

## 10. T12d — Policy robustness frontier

Test endogenous refinement collapse under progressively more standard adaptive policies:

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

Stronger forms reverse the policy quantifier and should not be asserted without proof.

The outcome should distinguish:

```text
foreclosure      finite total path information
sublinear        information diverges but slower than linearly
linear           positive asymptotic information rate
timely           enough statistical separation within the relevant deadline
```

---

## 11. T12e — From information availability to timely adjudication

T12e is a sequential-testing theorem program. It separates:

\[
\boxed{
\text{available information}
\neq
\text{mean acquired information}
\neq
\text{pathwise predictable information}
\neq
\text{realized evidence}
\neq
\text{timely identification}.
}
\]

### 11.1 Directed likelihood objects

For testing `H_i` against `H_j`, let the action be chosen before the observation and define the pre-observation filtration

\[
\mathcal G_t=\sigma(\mathcal F_{t-1},A_t).
\]

Define the directed log-likelihood increment

\[
\ell_t^{i\to j}
=
\log
\frac{dQ_i^{A_t}}{dQ_j^{A_t}}(Z_t).
\]

Its predictable drift under `H_i` is

\[
\boxed{
g_t^{i\to j}
=
\mathbb E_i[\ell_t^{i\to j}\mid\mathcal G_t]
=
D_{\mathrm{KL}}(Q_i^{A_t}\Vert Q_j^{A_t}).
}
\]

Define

\[
G_n^{i\to j}
=
\sum_{t=1}^n g_t^{i\to j},
\]

\[
M_n^{i\to j}
=
\sum_{t=1}^n(\ell_t^{i\to j}-g_t^{i\to j}),
\]

and

\[
\boxed{
L_n^{i\to j}
=
G_n^{i\to j}+M_n^{i\to j}.
}
\]

`G_n` can be random because adaptive actions are random. The deterministic directed path KL is

\[
\boxed{
K_n^{i\to j}
:=
D_{\mathrm{KL}}(P_i^{\pi,n}\Vert P_j^{\pi,n})
=
\mathbb E_i[G_n^{i\to j}].
}
\]

The reverse direction uses

\[
K_n^{j\to i}
=
D_{\mathrm{KL}}(P_j^{\pi,n}\Vert P_i^{\pi,n}),
\]

which need not equal the forward quantity.

The hierarchy is therefore:

```text
I*     information potentially available
K_n    mean path information acquired under the endogenous policy
G_n    predictable information budget on the realized action path
L_n    realized likelihood evidence
H_id   time until the evidence is statistically decisive
```

### T12e.1 — Divergent directed path information is necessary

Suppose binary tests have both errors tending to zero:

\[
\alpha_n\to0,
\qquad
\beta_n\to0.
\]

Data processing of KL through the binary decision implies

\[
D_{\mathrm{KL}}(P_i^{\pi,n}\Vert P_j^{\pi,n})\to\infty
\]

and, reversing the roles,

\[
D_{\mathrm{KL}}(P_j^{\pi,n}\Vert P_i^{\pi,n})\to\infty.
\]

Hence by T12a:

\[
\boxed{
K_n^{i\to j}\to\infty,
\qquad
K_n^{j\to i}\to\infty.
}
\]

This is necessary, not sufficient.

### T12e.2 — Divergent mean information is not sufficient

A rare-event construction defeats the tempting converse.

Take one experiment and independent binary observations. Under `H_i`, let

\[
Z_t\sim\mathrm{Bernoulli}(p_t),
\qquad
p_t=2^{-t}.
\]

Under `H_j`, let

\[
Z_t\sim\mathrm{Bernoulli}(q_t),
\qquad
q_t=p_t\exp\left(-\frac{1}{tp_t}\right).
\]

Then

\[
p_t\log\frac{p_t}{q_t}=\frac1t,
\]

while the zero-outcome contribution is `O(p_t)`. Therefore

\[
K_n^{i\to j}\sim\log n\to\infty.
\]

But

\[
\sum_t p_t<\infty,
\qquad
\sum_t q_t<\infty.
\]

The infinite all-zero trajectory consequently has positive probability under both hypotheses. The infinite path measures are not mutually singular, so no sequence of tests can drive both errors to zero.

Thus:

\[
\boxed{
K_n\to\infty
\not\Rightarrow
\text{consistent discrimination}.
}
\]

Expected path information can diverge because of increasingly rare, increasingly extreme evidence while typical histories remain ambiguous.

### T12e.3 — Pathwise predictable divergence plus controlled fluctuations is sufficient

A clean sufficient condition is:

under `H_i`,

\[
G_n^{i\to j}\to\infty
\quad P_i\text{-a.s.},
\]

and

\[
\frac{M_n^{i\to j}}{G_n^{i\to j}}
\to0
\quad P_i\text{-a.s.}.
\]

Then

\[
\frac{L_n^{i\to j}}{G_n^{i\to j}}\to1,
\]

so

\[
L_n^{i\to j}\to+\infty
\quad P_i\text{-a.s.}
\]

Require the corresponding reverse conditions under `H_j`; then the same log-likelihood ratio tends to `-infinity` under `H_j` and the likelihood-ratio decision is consistent.

The theorem is elementary once the pathwise assumptions are supplied. The technical research question is to identify the weakest useful conditions implying

\[
M_n/G_n\to0.
\]

Martingale strong laws, conditional variance control, and likelihood-process methods are candidate machinery.

### T12e.4 — Finite-horizon timely adjudication

For a consequence-relevant horizon `H`, define directed future predictable information

\[
G_{t,H}^{i\to j}
=
\sum_{k=1}^{H}
D_{\mathrm{KL}}
(Q_i^{A_{t+k}}\Vert Q_j^{A_{t+k}}),
\]

and analogously `G_{t,H}^{j->i}`.

A strong prospective condition under `H_i` is

\[
\boxed{
P_i
\left(
G_{t,H}^{i\to j}\ge\beta_i
\mid\mathfrak S_t
\right)
\ge1-\xi_i.
}
\]

The reverse direction requires its own `(beta_j,xi_j)` because KL is asymmetric.

Let the centered increments over the window satisfy a usable martingale concentration condition; for example, assume

\[
|\ell_{t+k}^{i\to j}-g_{t+k}^{i\to j}|\le b_i
\]

and conditional variance process at most `v_i`. A Freedman-type lower-tail bound then gives the schematic error control

\[
P_i(\text{choose }j\text{ by }t+H)
\le
\xi_i
+
\exp\left(
-\frac{\beta_i^2}{2(v_i+b_i\beta_i/3)}
\right),
\]

with an analogous bound under `H_j`.

The constants and minimal conditions are theorem work; the structural point is fixed:

```text
high expected information alone is insufficient
high-probability predictable information alone is insufficient without realization control
high-probability predictable information + likelihood concentration gives a deadline-error guarantee
```

### T12e.5 — Path-law separation is the target property

KL is sufficient machinery, not the final primitive.

For equal-prior binary testing, define the finite-window conditional path-law separation

\[
\boxed{
\mathsf{Sep}_{t,H}(i,j)
=
\left\|
P_i^{\pi,t:t+H}
-
P_j^{\pi,t:t+H}
\right\|_{\mathrm{TV}}.
}
\]

The optimal equal-prior binary error is

\[
P_e^\star
=
\frac12(1-\mathsf{Sep}_{t,H}).
\]

Therefore the sharp target condition for error at most `delta` is

\[
\boxed{
\mathsf{Sep}_{t,H}(i,j)
\ge
1-2\delta.
}
\]

Total variation / Hellinger path-process machinery is therefore the natural target for a sharp characterization. Predictable KL plus martingale concentration is a tractable sufficient route to that target.

---

## 12. Current mathematical chain

The current separation is:

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
H_{\rm identify}<H_{\rm consequence}.
}
\]

In words:

```text
available information
!=
mean information acquired under the policy
!=
reliably available predictable information on the realized action path
!=
realized likelihood evidence
!=
timely identification
```

This is the mathematical version of the empirical distinctions accumulated across PCE/CSD/MAB-OS:

```text
availability
!=
diagnostic information
!=
realized evidence
!=
warranted timely attribution
```

No empirical result is upgraded by this analogy.

---

## 13. Immediate proof program

The next work is deliberately narrow:

```text
T12e.1  formal proof with exact filtration / absolute-continuity assumptions
T12e.2  verify rare-event counterexample and both directed divergences
T12e.3  prove useful martingale sufficient conditions for M_n/G_n -> 0
T12e.4  derive rigorous finite-window error bounds and identify which assumptions are dispensable
T12e.5  seek a sharper TV / Hellinger-process characterization
```

Only after T12e is stable should T13 return to refinement construction / empirical re-entry.

---

## 14. Claim ceiling and open boundary

This document does **not** establish:

```text
a universal theory of scientific discovery
a universal creativity mechanism
a fourth adaptive control surface
a universal scalar objective
that KL is the correct final notion of challengeability
that richer refinement classes generally self-seal
that T12c survives natural policy classes
that model-class inadequacy identifies representation failure
that boundary pressure contains the successor representation
```

The hardest open arrow remains:

\[
\boxed{
\texttt{CURRENT_MODEL_CLASS_INADEQUATE}
\rightarrow
?
\rightarrow
(\Pi_{t+1},\mathcal H_{t+1}).
}
\]

The present theorem program only asks which assumptions make that search scientifically adjudicable after a candidate is proposed.

---

## 15. Frozen field-level description

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

with the current theorem-level meaning of the last clause:

> **Every unresolved consequential distinction must retain a high-probability path to sufficient statistical separation before its consequence-relevant deadline.**
