# T13.2 — Constructive Reachability of an Adequate Refinement Region

**Status:** `PROVED_AT_STATED_SCOPES`  
**Scope:** Mathematical Core boundary-expansion layer only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**Constructor implementation added:** none  
**Construction experiment authorized:** no

This note proves the reachability layer that follows T13.1.

T13.1 established that a finite constructive question is meaningful only after fixing a nonempty attainable target region

\[
\mathcal R_\varepsilon^\star
=
\{r\in\mathcal R:\rho(P^\star,Q_r)\le\varepsilon\}
\neq\varnothing.
\]

T13.2 asks only whether an adaptive constructor/search process can reach that already-defined region. It does **not** ask whether a reached candidate is valid. T13.4 already proves that selection and validation are different questions.

The central distinctions are

\[
\boxed{
\text{positive proposal support}
\neq
\text{eventual constructive reachability}
\neq
\text{timely constructive reachability}.
}
\]

No independence assumption is required for the main hazard theorem.

---

## 1. Setup

Condition on the boundary-exhaustion history \(\mathcal F_\tau\). All probabilities below may therefore be read as regular conditional probabilities given that history.

Let

\[
\mathcal B:=\mathcal R_\varepsilon^\star
\]

be a fixed nonempty adequate target region.

Let

\[
r_1,r_2,\ldots
\]

be the sequence of candidates proposed by a possibly adaptive and randomized constructor \(G\). Let

\[
(\mathcal F_k)_{k\ge0}
\]

be the constructor filtration after conditioning on \(\mathcal F_\tau\), with \(r_k\) measurable at time \(k\).

Define the hit event at proposal \(k\):

\[
A_k:=\{r_k\in\mathcal B\}\in\mathcal F_k.
\]

Define the first hitting time

\[
\boxed{
T:=\inf\{k\ge1:A_k\},
}
\]

with \(T=\infty\) if the target region is never reached.

The finite-horizon construction probability is

\[
\boxed{
p_{\rm hit}(n)
:=P(T\le n\mid\mathcal F_\tau).
}
\]

After conditioning on \(\mathcal F_\tau\), we suppress that conditioning from the notation when no ambiguity arises.

For each proposal time define the one-step conditional target mass

\[
\boxed{
q_k
:=P(A_k\mid\mathcal F_{k-1}).
}
\]

The survival indicator before proposal \(k\) is

\[
S_{k-1}:=\mathbf 1_{\{T>k-1\}}.
\]

The relevant predictable proposal mass is the **pre-hit cumulative hazard**

\[
\boxed{
H_n
:=
\sum_{k=1}^n S_{k-1}q_k.
}
\]

Proposal mass after the first adequate candidate has already been reached is irrelevant to first-hit reachability, so it is deliberately excluded.

---

# 2. T13.2a — Finite-horizon construction probability

## Theorem 13.2.1 — Pre-hit hazard supermartingale

Define

\[
S_n:=\mathbf 1_{\{T>n\}}
\]

and

\[
\boxed{
Y_n:=S_n e^{H_n},
\qquad Y_0=1.
}
\]

Then \((Y_n)_{n\ge0}\) is a nonnegative supermartingale.

### Proof

Because \(S_{n-1}\) is \(\mathcal F_{n-1}\)-measurable,

\[
E[S_n\mid\mathcal F_{n-1}]
=
S_{n-1}(1-q_n).
\]

Also

\[
H_n=H_{n-1}+S_{n-1}q_n.
\]

Therefore

\[
\begin{aligned}
E[Y_n\mid\mathcal F_{n-1}]
&=
E\left[
S_n e^{H_{n-1}+S_{n-1}q_n}
\mid\mathcal F_{n-1}
\right]\\
&=
S_{n-1}e^{H_{n-1}}e^{q_n}(1-q_n).
\end{aligned}
\]

For \(q\in[0,1]\),

\[
e^q(1-q)\le1,
\]

because \(\log(1-q)\le-q\). Hence

\[
E[Y_n\mid\mathcal F_{n-1}]
\le
S_{n-1}e^{H_{n-1}}
=Y_{n-1}.
\]

Thus \((Y_n)\) is a nonnegative supermartingale. \(\square\)

---

## Corollary 13.2.2 — Finite-horizon hazard certificate

Suppose there is a deterministic constant \(c_n\ge0\) such that

\[
\boxed{
H_n\ge c_n
\qquad\text{on }\{T>n\}.
}
\]

Then

\[
\boxed{
P(T>n)\le e^{-c_n},
}
\]

and therefore

\[
\boxed{
p_{\rm hit}(n)\ge1-e^{-c_n}.
}
\]

### Proof

On \(\{T>n\}\), \(S_n=1\) and \(H_n\ge c_n\). Therefore

\[
S_n
\le
e^{-c_n}S_ne^{H_n}
=e^{-c_n}Y_n.
\]

Taking expectations and using the supermartingale property,

\[
P(T>n)=E[S_n]
\le
e^{-c_n}E[Y_n]
\le
e^{-c_n}E[Y_0]
=e^{-c_n}.
\]

\(\square\)

This theorem is path-adaptive: \(q_k\) may depend arbitrarily on the prior constructor history. No conditional independence among proposals is required.

---

## Corollary 13.2.3 — Deterministic lower proposal schedule

Suppose there are deterministic \(\alpha_k\in[0,1]\) such that whenever the target has not yet been hit,

\[
\boxed{
q_k
\ge
\alpha_k.
}
\]

Then

\[
\boxed{
P(T>n)
\le
\prod_{k=1}^n(1-\alpha_k)
\le
\exp\left(-\sum_{k=1}^n\alpha_k\right).
}
\]

Hence

\[
\boxed{
p_{\rm hit}(n)
\ge
1-\prod_{k=1}^n(1-\alpha_k)
\ge
1-\exp\left(-\sum_{k=1}^n\alpha_k\right).
}
\]

### Proof

On \(\{T>k-1\}\), the conditional probability of surviving proposal \(k\) is

\[
1-q_k\le1-\alpha_k.
\]

Therefore recursively

\[
P(T>k)
=E[S_{k-1}(1-q_k)]
\le
(1-\alpha_k)P(T>k-1).
\]

Iteration gives the product bound. The exponential bound follows from \(1-x\le e^{-x}\). \(\square\)

For the uniform lower bound \(\alpha_k\equiv\alpha>0\),

\[
\boxed{
p_{\rm hit}(n)\ge1-(1-\alpha)^n.}
\]

This recovers the simple sufficient condition proposed at the start of T13.2, but shows that uniform exploration is unnecessary.

---

# 3. T13.2b — Eventual constructive reachability

## Theorem 13.2.4 — Indefinite miss implies finite pre-hit proposal mass

For the first-hitting process above,

\[
\boxed{
P\bigl(T=\infty,\ H_\infty=\infty\bigr)=0,
}
\]

where

\[
H_\infty:=\lim_{n\to\infty}H_n\in[0,\infty].
\]

Equivalently, with probability one, every path on which the constructor misses the adequate region forever has only finite cumulative pre-hit conditional proposal mass:

\[
\boxed{
T=\infty
\Longrightarrow
H_\infty<\infty
\qquad\text{a.s.}
}
\]

### Proof

By Theorem 13.2.1, \((Y_n)\) is a nonnegative supermartingale. Hence by the nonnegative supermartingale convergence theorem,

\[
Y_n\to Y_\infty<\infty
\qquad\text{a.s.}
\]

On the event \(\{T=\infty\}\), we have \(S_n=1\) for every \(n\), so

\[
Y_n=e^{H_n}.
\]

If additionally \(H_\infty=\infty\), then \(Y_n\to\infty\), contradicting almost-sure finiteness of the supermartingale limit. Therefore

\[
P(T=\infty,H_\infty=\infty)=0.
\]

\(\square\)

### Interpretation

This is the constructor analogue of the earlier exposure result.

A constructor can miss an available adequate region forever only on histories along which its cumulative conditional mass assigned to that region remains finite.

No independence assumption is required.

---

## Corollary 13.2.5 — Divergent pre-hit fairness implies almost-sure hitting

Suppose the constructor satisfies the following fairness property:

\[
\boxed{
T=\infty
\Longrightarrow
\sum_{k=1}^\infty q_k=\infty
\qquad\text{a.s.}
}
\]

On \(\{T=\infty\}\), \(S_{k-1}=1\) for all \(k\), so this is equivalent to

\[
T=\infty
\Longrightarrow
H_\infty=\infty.
\]

Then

\[
\boxed{P(T<\infty)=1.}
\]

### Proof

The fairness assumption says that every forever-miss path would lie in \(\{T=\infty,H_\infty=\infty\}\), but Theorem 13.2.4 gives that event probability zero. \(\square\)

This is the appropriate first-hit version of a conditional Borel--Cantelli principle. It is stronger and cleaner for T13 because proposal mass is accumulated only while the target remains unreached.

---

## Corollary 13.2.6 — Nonuniform deterministic fairness

If on every pre-hit history

\[
q_k\ge\alpha_k
\]

for deterministic \(\alpha_k\ge0\) satisfying

\[
\boxed{
\sum_{k=1}^\infty\alpha_k=\infty,
}
\]

then

\[
\boxed{P(T<\infty)=1.}
\]

Thus a uniform positive exploration floor is not necessary. Proposal mass may vanish with time, provided its cumulative pre-hit lower mass diverges.

For example,

\[
\alpha_k=\frac1{k+1}
\]

has \(\alpha_k\to0\) but still guarantees eventual construction.

---

# 4. Positive support is not eventual reachability

## Proposition 13.2.7 — Positive support can still miss forever

There exists a constructor with

\[
q_k>0
\qquad\text{for every pre-hit }k
\]

but

\[
\boxed{P(T=\infty)>0.}
\]

### Construction

Let proposals be conditionally independent and let

\[
q_k=2^{-k}.
\]

Then every proposal gives the target region positive probability. However,

\[
\sum_{k=1}^\infty q_k=1<\infty,
\]

and

\[
P(T=\infty)
=
\prod_{k=1}^\infty(1-2^{-k})
>0.
\]

The infinite product is strictly positive because \(\sum_k2^{-k}<\infty\).

Therefore

\[
\boxed{
\text{positive proposal support}
\not\Rightarrow
\text{eventual constructive reachability}.
}
\]

This is the exact analogue of the earlier distinction

```text
nonzero challenge support
!=
timely corrective exposure
```

but now at the temporary refinement-search layer.

---

# 5. T13.2c — Timely construction

Eventual constructive reachability is not enough when a candidate must be available before a consequence-relevant deadline.

Let \(N\) be the maximum number of constructor proposals available before re-entry must begin.

Define \((N,\eta)\)-timely constructibility by

\[
\boxed{
P(T\le N\mid\mathcal F_\tau)\ge1-\eta.
}
\]

By Corollary 13.2.2, a sufficient path-adaptive certificate is

\[
\boxed{
H_N\ge\log\frac1\eta
\quad\text{on }\{T>N\}.
}
\]

Then

\[
\boxed{P(T\le N)\ge1-\eta.}
\]

Under a deterministic lower proposal schedule \(\alpha_k\), it is enough that

\[
\boxed{
\prod_{k=1}^N(1-\alpha_k)\le\eta,
}
\]

or more conservatively

\[
\boxed{
\sum_{k=1}^N\alpha_k\ge\log\frac1\eta.
}
\]

---

## Proposition 13.2.8 — Eventual reachability need not be timely

There exist constructors that reach the target almost surely but have arbitrarily poor finite-deadline guarantees.

Take independent proposals with

\[
q_k=\frac1{k+1}.
\]

Then

\[
\sum_{k=1}^\infty q_k=\infty,
\]

so \(T<\infty\) almost surely. But

\[
P(T>n)
=
\prod_{k=1}^n\left(1-\frac1{k+1}\right)
=
\frac1{n+1},
\]

and therefore

\[
\boxed{
p_{\rm hit}(n)=\frac{n}{n+1}.}
\]

For any fixed proposal deadline \(N\), the miss probability remains \(1/(N+1)\). By choosing slower divergent proposal schedules, convergence to one can be made much slower still.

Hence

\[
\boxed{
\text{eventual constructive reachability}
\not\Rightarrow
\text{timely constructive reachability}.
}
\]

---

# 6. What is and is not the relevant fairness condition

A naive condition such as

\[
\sum_k P(A_k\mid\mathcal F_{k-1})=\infty
\]

over the entire future is sufficient in many conditional Borel--Cantelli formulations, but it is not the natural T13 object because a constructor may stop allocating proposal mass after the first successful hit.

The first-hit process instead isolates

\[
\boxed{
H_n
=
\sum_{k=1}^n
\mathbf 1_{\{T>k-1\}}
P(A_k\mid\mathcal F_{k-1}).
}
\]

This makes the gate exact at the level needed for construction:

```text
mass assigned before success
!=
mass assigned after success
```

Theorem 13.2.4 then gives the key structural fact:

\[
\boxed{
\text{forever miss}
\Longrightarrow
\text{finite cumulative pre-hit proposal mass}
\quad\text{a.s.}
}
\]

Thus no conditional-independence assumption is needed to obtain the main eventual-reachability result.

---

# 7. Relation to T13.1 and T13.4

T13.1 establishes the existence gate:

\[
\boxed{
\mathcal R_\varepsilon^\star\neq\varnothing.
}
\]

T13.2 establishes the search/reachability gate:

\[
\boxed{
P(T\le N)\ge1-\eta
\quad\text{or}\quad
P(T<\infty)=1,
}
\]

depending on whether timely or eventual construction is required.

T13.4 establishes the validation firewall:

\[
\boxed{
E_D\to r
\not\Rightarrow
E_D\text{ validates }r.
}
\]

These are logically distinct:

\[
\boxed{
\text{attainability}
\neq
\text{reachability}
\neq
\text{validation}.
}
\]

A constructor may have a nonempty adequate target region and still fail to reach it. A constructor may reach an adequate candidate and still lack selection-aware evidence authorizing it.

---

# 8. T13.2 theorem status

The layered reachability result is now:

```text
T13.2a  finite-horizon construction probability
         PROVED via pre-hit hazard supermartingale

T13.2b  eventual constructive reachability
         PROVED under divergent pre-hit fairness;
         no conditional independence required

T13.2c  timely construction before a proposal deadline
         PROVED via finite cumulative hazard / lower-schedule certificates
```

Negative boundaries:

```text
positive proposal support
!=
eventual reachability

eventual reachability
!=
timely reachability
```

No claim is made that the hazard condition is the uniquely weakest possible representation of reachability. It is a minimal, adaptive, first-hit sufficient framework with an exact structural obstruction: indefinite miss can occur only on histories with finite cumulative pre-hit conditional target mass.

---

# 9. Next gate

T13.2 does not validate any constructed candidate.

The next proof target is T13.3:

> **Given an adaptively selected candidate, what conditions make subsequent authorization evidence calibrated under the selection mechanism and therefore admissible for fresh closed-world CWC re-entry?**

No constructor experiment is authorized by T13.2.