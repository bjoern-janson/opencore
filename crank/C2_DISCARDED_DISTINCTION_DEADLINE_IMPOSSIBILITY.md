# C2 — Discarded-Distinction Deadline Impossibility

**Status:** `PROVED_AT_STATED_SCOPE`  
**Scope:** represented finite-horizon adjudication only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**CWC definition changed:** no  
**T13 construction experiment authorized:** no

This note proves the second theorem in the post-freeze adaptive coarse-graining queue.

C1 identified the coarsest exact consequence-sufficient quotient for a frozen consequence question. C2 asks what follows when the current representation collapses a genuinely consequential distinction and the entire represented adaptive experiment remains observationally identical through the consequence-relevant deadline.

The result is an impossibility theorem:

\[
\boxed{
P_{a,t:H}^{\pi}=P_{b,t:H}^{\pi}
\quad\Longrightarrow\quad
\neg\mathsf{CWC}_{t,H,\delta}(a,b;\pi)
\ \text{for every }\delta<\tfrac12.
}
\]

The premises that \(s_a\not\sim_{P,h}s_b\) and \(\Pi(s_a)=\Pi(s_b)\) identify why this equality is consequential: the physical/system states differ in the frozen future consequence law, yet the current representation initially collapses them. The actual impossibility, however, is driven by equality of the full represented deadline path laws.

That distinction is essential:

```text
collapsed consequential distinction
!=
deadline impossibility
```

If a later reachable intervention re-exposes the distinction before the deadline, the represented path laws can separate and CWC may be restored.

---

## 1. Setup

Fix:

- two physical/system states \(s_a,s_b\in\mathcal X\);
- the frozen C1 consequence question \((P,h,Y)\), with consequence kernel \(K_{P,h}\);
- a current representation \(\Pi\);
- an adaptive represented-history policy \(\pi\);
- a current time \(t\);
- a consequence-relevant terminal deadline \(H>t\).

Assume the states are consequence-distinct:

\[
\boxed{
s_a\not\sim_{P,h}s_b,
}
\]

meaning

\[
K_{P,h}(s_a,\cdot)\neq K_{P,h}(s_b,\cdot).
\]

Assume the current representation initially collapses them:

\[
\boxed{
\Pi(s_a)=\Pi(s_b).
}
\]

Let

\[
P:=P_{a,t:H}^{\pi},
\qquad
Q:=P_{b,t:H}^{\pi}
\]

be the two complete represented adaptive path laws available to adjudication through the deadline. These laws include every represented action/observation variable exposed to the downstream adjudicator under the frozen policy protocol.

The decisive deadline premise is

\[
\boxed{
P=Q.
}
\]

Let a randomized terminal adjudicator be represented, as in T12e.5, by a measurable map

\[
\varphi:\Omega_{t:H}\to[0,1],
\]

where \(\varphi(\omega)\) is the probability of deciding \(a\) on represented history \(\omega\).

Define directed errors

\[
\alpha(\varphi)
:=
1-E_P[\varphi],
\]

and

\[
\beta(\varphi)
:=
E_Q[\varphi].
\]

The frozen closed-world certificate is

\[
\mathsf{CWC}_{t,H,\delta}(a,b;\pi)
\iff
\exists\varphi:
\alpha(\varphi)\le\delta,
\quad
\beta(\varphi)\le\delta.
\]

---

# 2. Main theorem

## Theorem C2.1 — Identical represented deadline laws force minimax error at least one half

If

\[
P_{a,t:H}^{\pi}=P_{b,t:H}^{\pi},
\]

then for every represented-history-measurable randomized adjudicator \(\varphi\),

\[
\boxed{
\alpha(\varphi)+\beta(\varphi)=1.
}
\]

Consequently,

\[
\boxed{
\max\{\alpha(\varphi),\beta(\varphi)\}\ge\frac12.
}
\]

Therefore, for every \(\delta<\tfrac12\),

\[
\boxed{
\neg\mathsf{CWC}_{t,H,\delta}(a,b;\pi).
}
\]

### Proof

Because \(P=Q\),

\[
E_P[\varphi]=E_Q[\varphi].
\]

Write

\[
p:=E_P[\varphi]=E_Q[\varphi].
\]

Then

\[
\alpha(\varphi)=1-p
\]

and

\[
\beta(\varphi)=p.
\]

Hence

\[
\boxed{
\alpha(\varphi)+\beta(\varphi)=1.
}
\]

At least one of two nonnegative numbers summing to one must be at least \(1/2\). Thus

\[
\max\{\alpha(\varphi),\beta(\varphi)\}\ge\frac12.
\]

If \(\delta<1/2\), no test can have both directed errors at most \(\delta\). By the definition of CWC,

\[
\neg\mathsf{CWC}_{t,H,\delta}(a,b;\pi).
\]

\(\square\)

---

# 3. Sharpness at the threshold

## Corollary C2.2 — The one-half threshold is exact for randomized adjudication

Under \(P=Q\), the constant randomized test

\[
\varphi\equiv\frac12
\]

has

\[
\alpha=\beta=\frac12.
\]

Therefore

\[
\boxed{
R_{\max}^*(P,Q)=\frac12.
}
\]

So C2 is sharp:

\[
\boxed{
\mathsf{CWC}_{t,H,\delta}(a,b;\pi)
\text{ is impossible for }\delta<\frac12,
}
\]

while the trivial randomized half-half decision meets the two-sided risk criterion at \(\delta=1/2\).

This does not constitute informative adjudication; it merely shows that the impossibility threshold cannot be strengthened beyond one half without changing the risk criterion.

---

# 4. Equivalent proof through the frozen Neyman–Pearson tradeoff

T12e.5 defines

\[
\beta_\gamma(P,Q)
:=
\inf\left\{
E_Q[\varphi]:
0\le\varphi\le1,
E_P[\varphi]\ge\gamma
\right\}.
\]

If \(P=Q\), then every feasible \(\varphi\) satisfies

\[
E_Q[\varphi]=E_P[\varphi]\ge\gamma.
\]

The constant test \(\varphi\equiv\gamma\) attains equality. Hence

\[
\boxed{
\beta_\gamma(P,P)=\gamma.
}
\]

Set

\[
\gamma=1-\delta.
\]

Then

\[
\boxed{
\beta_{1-\delta}(P,P)=1-\delta.
}
\]

The exact CWC criterion is

\[
\beta_{1-\delta}(P,Q)\le\delta.
\]

Under identical path laws this becomes

\[
1-\delta\le\delta,
\]

which is equivalent to

\[
\boxed{
\delta\ge\frac12.
}
\]

Thus the elementary error-sum proof and the frozen sharp path-law characterization agree exactly.

---

# 5. Pushforward / downstream-algorithm form

The impossibility is not specific to one test implementation.

Let \(A\) be any measurable downstream algorithm receiving only the represented deadline history, together with hypothesis-independent auxiliary randomization \(U\). Let its output be

\[
D=A(H_{t:H}^{\Pi},U).
\]

If

\[
\mathcal L_a(H_{t:H}^{\Pi})
=
\mathcal L_b(H_{t:H}^{\Pi}),
\]

and \(U\) has the same law under both hypotheses, then by equality of pushforwards,

\[
\boxed{
\mathcal L_a(D)=\mathcal L_b(D).
}
\]

Therefore no downstream post-processing of the same represented experiment can manufacture a distinction absent from that experiment.

In compressed form:

\[
\boxed{
\text{identical represented path experiment}
\Longrightarrow
\text{identical law for every represented-history post-processing}.
}
\]

This is the precise meaning of:

> **Once the representation-induced path experiment is observationally identical through the deadline, no downstream algorithm operating solely on that experiment can recover the discarded distinction before the deadline.**

---

# 6. C1 → C2 bridge

C1 states that exact sufficiency requires

\[
\Pi(s)=\Pi(s')
\Longrightarrow
K_{P,h}(s,\cdot)=K_{P,h}(s',\cdot).
\]

So if

\[
s_a\not\sim_{P,h}s_b
\]

but

\[
\Pi(s_a)=\Pi(s_b),
\]

then the current representation is not exact-sufficient for the frozen consequence question.

C2 adds the stronger deadline premise

\[
P_{a,t:H}^{\pi}=P_{b,t:H}^{\pi}
\]

and concludes

\[
\boxed{
\text{current insufficiency}
+
\text{no represented separation by deadline}
\Longrightarrow
\text{no nontrivial deadline adjudication}.
}
\]

Thus:

\[
\boxed{
\text{coarsening across a consequential distinction}
\to
\text{identical represented deadline experiment}
\to
\neg\mathsf{CWC}_{\delta<1/2}.
}
\]

---

# 7. Essential boundary — collapse alone does not imply impossibility

C2 must not be read as

\[
\Pi(s_a)=\Pi(s_b)
\Longrightarrow
\neg\mathsf{CWC}.
\]

That implication is false in general.

The representation can initially collapse two states while the adaptive experiment later applies an intervention whose represented outcomes differ. In that case

\[
P_{a,t:H}^{\pi}\neq P_{b,t:H}^{\pi},
\]

and the hidden distinction may become adjudicable before the deadline.

Therefore the theorem's decisive premise is not merely initial representational collapse but

\[
\boxed{
P_{a,t:H}^{\pi}=P_{b,t:H}^{\pi}.
}
\]

The correct non-implication is

\[
\boxed{
\text{lost distinction}
\not\Rightarrow
\text{deadline impossibility}.
}
\]

What C2 proves is

\[
\boxed{
\text{lost consequential distinction}
+
\text{no deadline-valid represented recovery route}
\Rightarrow
\text{unavoidable nontrivial adjudication failure}.
}
\]

This preserves the OpenCore distinction between:

```text
initial representation failure
!=
permanent observational foreclosure
```

and remains compatible with later representation refinement or discriminating intervention.

---

# 8. Relation to total variation and information quantities

Under identical represented path laws,

\[
\|P-Q\|_{\mathrm{TV}}=0.
\]

Thus the equal-prior average Bayes risk is

\[
R_{\mathrm{avg}}^*(P,Q)
=
\frac12(1-0)
=
\frac12.
\]

Every directed path divergence also vanishes when defined:

\[
D_{\mathrm{KL}}(P\Vert Q)=0,
\qquad
D_{\mathrm{KL}}(Q\Vert P)=0.
\]

But C2 is stated directly at the testing-risk level because the frozen hierarchy remains

\[
I^\star
\neq
K_n
\neq
G_n
\neq
L_n
\neq
\mathsf{CWC}.
\]

No information proxy is needed for the theorem.

---

# 9. Exact theorem compression

The theorem may be frozen as:

\[
\boxed{
\begin{aligned}
s_a\not\sim_{P,h}s_b
&\land
\Pi(s_a)=\Pi(s_b)\\
&\land
P_{a,t:H}^{\pi}=P_{b,t:H}^{\pi}
\\[1mm]
&\Longrightarrow
\neg\mathsf{CWC}_{t,H,\delta}(a,b;\pi)
\quad
\forall\delta<\tfrac12.
\end{aligned}
}
\]

with the scope note:

\[
\boxed{
\text{The first two premises establish consequential representational loss;}
\quad
\text{the third premise establishes deadline observational foreclosure.}
}
\]

Only the third premise is mathematically required for the testing impossibility itself.

---

# 10. What C2 does not establish

C2 does **not** establish:

- that every insufficient representation causes deadline failure;
- that an initially collapsed distinction can never be re-exposed;
- that the physical/system states are globally indistinguishable;
- that no richer representation could restore adjudicability;
- that no different experiment policy could separate the states;
- that causal modularity follows from predictive sufficiency;
- that repair is constructively reachable;
- that T13.5 is proved;
- any empirical result;
- any new architectural primitive.

The theorem is exactly a finite-horizon represented-experiment impossibility result.

---

# 11. Status after C2

The post-freeze theorem queue is now:

```text
C1  coarsest consequence-sufficient quotient           PROVED AT STATED SCOPE
C2  discarded-distinction deadline impossibility       PROVED AT STATED SCOPE
C4  equal predictive sufficiency != equal repair cost  NEXT
C3  construction latency + CWC composition             OPEN; intended to feed T13.5
```

The resulting chain is:

\[
\boxed{
\text{quotient}
\to
\text{lost consequential distinction}
\to
\text{deadline path-law separation or foreclosure}
\to
\mathsf{CWC}\text{ or impossibility}.
}
\]

No construction experiment is authorized by this proof.