# T13.1 — Coverage Obstruction and Attainability Boundary

**Status:** `PROVED`  
**Scope:** Mathematical Core boundary-expansion layer only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**Constructor added:** none  
**T13 construction experiment authorized:** no

This note formalizes the coverage gate needed before constructive reachability can even be posed.

The central distinction is:

> **Empirical closure of a refinement language does not imply that an adequate refinement is actually present in that language.**

The exact finite-tolerance statement is slightly sharper than the informal rule `epsilon_R <= epsilon => an epsilon-adequate candidate exists`: equality at an unattained infimum is a boundary case where closure holds but the target set is empty.

---

## 1. Setup

Let `R` be a nonempty refinement language. Each refinement `r in R` induces an empirical experiment family `Q_r`. Let `P*` denote the target empirical law or experiment family and let

\[
\rho(P^\star,Q_r)\in[0,\infty]
\]

be the frozen empirical metric or pseudometric used to define adequacy.

Define the coverage error

\[
\boxed{
\epsilon_{\mathcal R}(P^\star)
:=
\inf_{r\in\mathcal R}
\rho(P^\star,Q_r).
}
\]

For a tolerance `epsilon >= 0`, define the actually attainable target region

\[
\boxed{
\mathcal R_\varepsilon^\star
:=
\left\{
r\in\mathcal R:
\rho(P^\star,Q_r)\le\varepsilon
\right\}.
}
\]

The distinction between these two objects is the entire theorem:

```text
coverage infimum
!=
nonempty attainable target region
```

When `rho` is a pseudometric, `rho(P*,Q_r)=0` means exact empirical equivalence at the resolution encoded by `rho`; it need not mean syntactic or ontological identity.

---

# 2. Theorem 13.1.1 — Exact Attainability Boundary

Let

\[
e:=\epsilon_{\mathcal R}(P^\star)
=
\inf_{r\in\mathcal R}\rho(P^\star,Q_r).
\]

Then for every finite tolerance `epsilon >= 0`:

### (i) Below the infimum

If

\[
\varepsilon<e,
\]

then

\[
\boxed{
\mathcal R_\varepsilon^\star=\varnothing.
}
\]

### (ii) Strictly above the infimum

If

\[
\varepsilon>e,
\]

then

\[
\boxed{
\mathcal R_\varepsilon^\star\neq\varnothing.
}
\]

### (iii) Exactly at the infimum

If

\[
\varepsilon=e,
\]

then

\[
\boxed{
\mathcal R_e^\star\neq\varnothing
\iff
\exists r^\star\in\mathcal R:
\rho(P^\star,Q_{r^\star})=e.
}
\]

Equivalently, the target set at the optimal tolerance is nonempty if and only if the defining infimum is attained.

## Proof

For (i), by definition of infimum,

\[
\rho(P^\star,Q_r)\ge e
\qquad
\forall r\in\mathcal R.
\]

If `epsilon < e`, no refinement can satisfy

\[
\rho(P^\star,Q_r)\le\varepsilon.
\]

Hence `R_epsilon*` is empty.

For (ii), suppose `epsilon > e`. Let

\[
\eta:=\varepsilon-e>0.
\]

By the defining property of the infimum, there exists some `r in R` such that

\[
\rho(P^\star,Q_r)<e+\eta=\varepsilon.
\]

Therefore `r in R_epsilon*`, so the target set is nonempty.

For (iii), because every distance is at least `e`, a refinement belongs to `R_e*` exactly when its distance equals `e`:

\[
r\in\mathcal R_e^\star
\iff
\rho(P^\star,Q_r)\le e
\iff
\rho(P^\star,Q_r)=e.
\]

Thus `R_e*` is nonempty exactly when the infimum is achieved by some member of `R`. `QED`

---

# 3. Corollary 13.1.2 — Exact Coverage versus Closure-Only Coverage

Set `epsilon = 0`.

Because distances are nonnegative, there are three distinct cases.

## Case A — Exact attainable empirical coverage

If

\[
\epsilon_{\mathcal R}(P^\star)=0
\]

and there exists

\[
r^\star\in\mathcal R
\]

such that

\[
\rho(P^\star,Q_{r^\star})=0,
\]

then

\[
\boxed{
\mathcal R_0^\star\neq\varnothing.
}
\]

The language contains an empirically exact candidate.

## Case B — Closure-only coverage

If

\[
\epsilon_{\mathcal R}(P^\star)=0
\]

but

\[
\rho(P^\star,Q_r)>0
\qquad
\forall r\in\mathcal R,
\]

then

\[
\boxed{
\mathcal R_0^\star=\varnothing.
}
\]

Nevertheless, for every strictly positive tolerance

\[
\varepsilon>0,
\]

Theorem 13.1.1(ii) gives

\[
\boxed{
\mathcal R_\varepsilon^\star\neq\varnothing.
}
\]

Thus the language can approximate the target arbitrarily closely while containing no exact empirical refinement.

## Case C — Positive coverage obstruction

If

\[
\epsilon_{\mathcal R}(P^\star)=e>0,
\]

then for every

\[
\varepsilon<e,
\]

\[
\boxed{
\mathcal R_\varepsilon^\star=\varnothing.
}
\]

No constructor restricted to `R` can return an `epsilon`-adequate candidate at such a tolerance, regardless of search time, optimization power, or proposal policy.

At `epsilon=e`, existence again depends on whether the infimum is attained. For every `epsilon>e`, an `epsilon`-adequate refinement exists.

---

# 4. Counterexample 13.1.3 — Zero Infimum with No Exact Candidate

The closure-only case occurs even in the smallest standard statistical setting.

Let the observation space be

\[
\mathcal X=\{0,1\}.
\]

Let

\[
P^\star=\operatorname{Bernoulli}(0),
\]

and define the refinement language

\[
\mathcal R=\{r_n:n\ge1\}
\]

with

\[
Q_{r_n}
=
\operatorname{Bernoulli}\left(\frac1{n+1}\right).
\]

Take total variation as the empirical metric. For Bernoulli laws,

\[
\left\|
\operatorname{Bernoulli}(p)
-
\operatorname{Bernoulli}(q)
\right\|_{\rm TV}
=|p-q|.
\]

Therefore

\[
\rho(P^\star,Q_{r_n})
=
\frac1{n+1}.
\]

Hence

\[
\boxed{
\epsilon_{\mathcal R}(P^\star)
=
\inf_{n\ge1}\frac1{n+1}
=0.
}
\]

But for every finite `n`,

\[
\rho(P^\star,Q_{r_n})>0.
\]

Thus

\[
\boxed{
\mathcal R_0^\star=\varnothing.
}
\]

while for every `epsilon>0`, sufficiently large `n` gives

\[
\rho(P^\star,Q_{r_n})\le\varepsilon,
\]

so

\[
\boxed{
\mathcal R_\varepsilon^\star\neq\varnothing.
}
\]

This explicitly proves

\[
\boxed{
P^\star\in\overline{\mathcal Q_{\mathcal R}}^{\,\rho}
\not\Rightarrow
\exists r^\star\in\mathcal R:
\rho(P^\star,Q_{r^\star})=0.
}
\]

`QED`

---

# 5. Proposition 13.1.4 — Closure Coverage Is Not Yet a Constructive Target

Suppose

\[
\epsilon_{\mathcal R}(P^\star)=0
\]

but

\[
\mathcal R_0^\star=\varnothing.
\]

Then no `R`-valued constructor, deterministic or stochastic, can ever output an exactly adequate refinement, because no such member exists.

Formally, for every random variable

\[
R:\Omega\to\mathcal R,
\]

\[
\boxed{
P\left(
\rho(P^\star,Q_R)=0
\right)=0.
}
\]

This statement is purely set-theoretic: the event is empty.

For approximate construction at tolerance `epsilon>0`, the relevant target is instead the nonempty set

\[
\mathcal R_\varepsilon^\star.
\]

Thus T13.2 must be parameterized by an explicit adequacy tolerance unless exact attainment has already been established.

---

# 6. The Exact Coverage Gate for T13.2

The constructive-reachability theorem should not use the scalar infimum by itself as its target.

The correct object is

\[
\boxed{
\mathcal R_\varepsilon^\star
=
\{r:\rho(P^\star,Q_r)\le\varepsilon\}.
}
\]

Before asking whether a constructor can reach that region, T13.1 requires

\[
\boxed{
\mathcal R_\varepsilon^\star\neq\varnothing.
}
\]

The exact relation to the coverage infimum is

\[
\boxed{
\begin{array}{lll}
\varepsilon<\epsilon_{\mathcal R} &\Rightarrow& \mathcal R_\varepsilon^\star=\varnothing,\\[1mm]
\varepsilon>\epsilon_{\mathcal R} &\Rightarrow& \mathcal R_\varepsilon^\star\neq\varnothing,\\[1mm]
\varepsilon=\epsilon_{\mathcal R} &\Rightarrow&
\mathcal R_\varepsilon^\star\neq\varnothing
\iff\text{the infimum is attained.}
\end{array}
}
\]

This is the complete coverage/attainability boundary needed by T13.2.

---

# 7. Relation to T13.4

T13.1 and T13.4 block different invalid transitions.

T13.1 proves:

\[
\boxed{
\text{empirical closure}
\not\Rightarrow
\text{attainable candidate at the boundary tolerance}.
}
\]

T13.4 proves:

\[
\boxed{
\text{selected discovery fit}
\not\Rightarrow
\text{selection-aware candidate validity}.
}
\]

These are independent obstructions.

A refinement language can contain an exact valid candidate and still suffer the T13.4 self-validation failure.

Conversely, a perfectly calibrated selection/validation procedure cannot construct an exact refinement from a language whose exact target set is empty.

Thus:

```text
coverage obstruction
!=
selection/calibration obstruction
```

---

# 8. Earned Claim Boundary

T13.1 earns only the following statements:

1. `epsilon_R` is an infimum, not an existence certificate.
2. Strictly exceeding the infimum guarantees a nonempty tolerance target set.
3. At the infimum itself, attainability is equivalent to attainment of the infimum.
4. Zero coverage error can therefore be exact-attainable or closure-only.
5. T13.2 must search a nonempty explicit target region `R_epsilon*`, not the scalar infimum.

T13.1 does **not** establish:

```text
that a constructor can find an adequate candidate
that adequacy can be recognized from available evidence
that a selected candidate is validated
that fresh CWC can be earned
that any authority transfer is justified
```

No constructor has been introduced.

---

# 9. Current T13 Proof Frontier

```text
T13.1  coverage / attainability boundary              PROVED
T13.2  constructive reachability                      NEXT
T13.3  selection-aware empirical re-entry             OPEN
T13.4  selection-naive self-validation firewall       PROVED COUNTEREXAMPLE
T13.5  sufficient boundary-expansion / re-entry       OPEN
```

The next legitimate question is therefore:

\[
\boxed{
P\left(
\exists n:\ r_n\in\mathcal R_\varepsilon^\star
\mid\mathcal F_\tau
\right)
\ge1-\eta\ ?
}
\]

but only after the target tolerance `epsilon` is fixed and `R_epsilon*` is known to be nonempty.

---

## 10. Stopping Rule

T13.1 is a coverage theorem only.

Do not convert closure into attainability, and do not convert attainability into reachability.

The next arrow must be proved separately:

\[
\boxed{
\text{nonempty adequate target region}
\not\Rightarrow
\text{constructor reaches it}.
}
\]
