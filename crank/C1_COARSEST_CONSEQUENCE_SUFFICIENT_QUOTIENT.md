# C1 — Coarsest Consequence-Sufficient Quotient

**Status:** `PROVED_AT_STATED_SCOPE`  
**Scope:** task-relative exact predictive sufficiency only  
**Empirical authority added:** none  
**New architectural primitive:** none  
**CWC definition changed:** no  
**T13 construction experiment authorized:** no

This note proves the first theorem in the post-freeze adaptive coarse-graining queue.

The theorem gives a precise answer to:

> **For a fixed policy/regime, horizon, and consequential future variable, what is the coarsest exact representation that preserves all distinctions needed for prediction?**

It does **not** define a universally optimal representation. The quotient depends explicitly on the frozen consequence question.

The central result is:

\[
\boxed{
\Pi\text{ exact-sufficient}
\iff
q_{P,h}\text{ factors through }\Pi,
}
\]

where \(q_{P,h}\) is the quotient by equality of future consequence laws.

Equivalently, every exact-sufficient representation may split consequence-equivalent states, but it may not merge states whose specified future laws differ.

---

## 1. Setup

Fix:

- a state space \(\mathcal X\);
- a measurable consequential-future space \((\mathcal Y,\mathscr Y)\);
- a policy/intervention regime \(P\);
- a horizon \(h\);
- a specified consequential future random object \(Y_{P,h}\).

Rather than relying on a particular regular conditional distribution construction, take as primitive the frozen consequence kernel

\[
\boxed{
K_{P,h}(s,\cdot)
\in\mathcal P(\mathcal Y),
\qquad s\in\mathcal X,
}
\]

where \(K_{P,h}(s,\cdot)\) is the law of the specified future consequence when the current physical/system state is \(s\), under the fixed policy/regime and horizon.

When no ambiguity arises, write

\[
K_s:=K_{P,h}(s,\cdot).
\]

A representation is any map

\[
\Pi:\mathcal X\to\mathcal Z.
\]

No coordinate structure, metric, or causal interpretation of \(\mathcal Z\) is assumed.

---

## 2. Consequence equivalence

Define a relation on \(\mathcal X\):

\[
\boxed{
s\sim_{P,h}s'
\iff
K_{P,h}(s,\cdot)=K_{P,h}(s',\cdot)
}
\]

where equality is equality as probability measures on \((\mathcal Y,\mathscr Y)\).

### Lemma C1.1 — \(\sim_{P,h}\) is an equivalence relation

It is reflexive, symmetric, and transitive because equality of probability measures has those properties. \(\square\)

Let

\[
\mathcal Q_{P,h}:=\mathcal X/{\sim_{P,h}}
\]

be the set of consequence-equivalence classes, and define the quotient map

\[
\boxed{
q_{P,h}:\mathcal X\to\mathcal Q_{P,h},
\qquad
q_{P,h}(s)=[s]_{P,h}.
}
\]

The quotient merges exactly those current states that induce the same specified future consequence law.

---

## 3. Exact task-relative predictive sufficiency

### Definition C1.2 — Exact \((P,h,Y)\)-sufficiency

A representation \(\Pi:\mathcal X\to\mathcal Z\) is **exactly sufficient** for the frozen consequence question if

\[
\boxed{
\Pi(s)=\Pi(s')
\Longrightarrow
K_s=K_{s'}.
}
\]

Equivalently, no representation cell may contain two states with different specified future consequence laws.

In the deterministic special case where

\[
Y_{P,h}=F_{P,h}(s),
\]

this reduces to

\[
\boxed{
\Pi(s)=\Pi(s')
\Longrightarrow
F_{P,h}(s)=F_{P,h}(s').
}
\]

This is the precise form of:

```text
compress everything except distinctions consequential for the frozen future question
```

---

# 4. Main theorem — coarsest consequence-sufficient quotient

## Theorem C1.3 — Quotient sufficiency and universal factorization

Fix the frozen consequence kernel \(K_{P,h}\).

Then:

1. the quotient map \(q_{P,h}\) is exactly sufficient;
2. for every exactly sufficient representation \(\Pi:\mathcal X\to\mathcal Z\), there exists a unique map on the attained representation image

\[
\boxed{
g_\Pi:\Pi(\mathcal X)\to\mathcal Q_{P,h}}
\]

such that

\[
\boxed{
q_{P,h}=g_\Pi\circ\Pi;
}
\]

3. conversely, if such a factorization exists, then \(\Pi\) is exactly sufficient.

Therefore

\[
\boxed{
\Pi\text{ is exact-sufficient}
\iff
q_{P,h}\text{ is a deterministic function of }\Pi.
}
\]

### Proof

#### Part 1 — quotient sufficiency

Suppose

\[
q_{P,h}(s)=q_{P,h}(s').
\]

Then \(s\) and \(s'\) belong to the same equivalence class, so by definition

\[
K_s=K_{s'}.
\]

Hence \(q_{P,h}\) is exactly sufficient. \(\square\)

#### Part 2 — factorization of every sufficient representation

Let \(\Pi\) be exactly sufficient.

For any attained representation value

\[
z\in\Pi(\mathcal X),
\]

choose any state \(s\in\mathcal X\) with \(\Pi(s)=z\) and define

\[
\boxed{
g_\Pi(z):=q_{P,h}(s).}
\]

We must show this is well-defined.

Suppose \(s'\) is another state with

\[
\Pi(s')=z=\Pi(s).
\]

Exact sufficiency gives

\[
K_s=K_{s'}.
\]

Thus

\[
s\sim_{P,h}s',
\]

and therefore

\[
q_{P,h}(s)=q_{P,h}(s').
\]

So \(g_\Pi(z)\) does not depend on the chosen representative.

For every \(s\in\mathcal X\),

\[
(g_\Pi\circ\Pi)(s)
=
g_\Pi(\Pi(s))
=
q_{P,h}(s).
\]

Hence

\[
q_{P,h}=g_\Pi\circ\Pi.
\]

Uniqueness on \(\Pi(\mathcal X)\) is immediate: if \(g\circ\Pi=q_{P,h}\), then for any attained \(z=\Pi(s)\), necessarily

\[
g(z)=q_{P,h}(s).
\]

#### Part 3 — converse

Suppose

\[
q_{P,h}=g\circ\Pi.
\]

If

\[
\Pi(s)=\Pi(s'),
\]

then

\[
q_{P,h}(s)
=
g(\Pi(s))
=
g(\Pi(s'))
=
q_{P,h}(s').
\]

Therefore

\[
s\sim_{P,h}s',
\]

so

\[
K_s=K_{s'}.
\]

Thus \(\Pi\) is exactly sufficient. \(\square\)

---

## 5. Partition interpretation

The fibers of a representation \(\Pi\) define a partition of \(\mathcal X\):

\[
\mathcal P_\Pi
:=
\{\Pi^{-1}(z):z\in\Pi(\mathcal X)\}.
\]

The consequence quotient defines

\[
\mathcal P_{P,h}
:=
\{q_{P,h}^{-1}(c):c\in\mathcal Q_{P,h}\}.
\]

Theorem C1.3 is exactly equivalent to

\[
\boxed{
\Pi\text{ exact-sufficient}
\iff
\mathcal P_\Pi\text{ refines }\mathcal P_{P,h}.
}
\]

That is:

- \(\Pi\) may split a consequence-equivalence class into several representation values;
- \(\Pi\) may not join pieces from two different consequence-equivalence classes.

So \(q_{P,h}\) is the **coarsest exact sufficient quotient** in the partition order.

This does not mean it is uniquely optimal under every possible complexity, computational, causal, or revision criterion.

---

# 6. Complexity lower bounds

## Corollary C1.4 — Finite cardinality lower bound

Suppose \(\mathcal Q_{P,h}\) is finite and \(\Pi\) is exactly sufficient.

Then

\[
\boxed{
|\Pi(\mathcal X)|
\ge
|\mathcal Q_{P,h}|.
}
\]

### Proof

By Theorem C1.3, \(g_\Pi:\Pi(\mathcal X)\to\mathcal Q_{P,h}\) is surjective because

\[
q_{P,h}=g_\Pi\circ\Pi
\]

and \(q_{P,h}\) reaches every quotient class. A surjection from a finite set onto \(\mathcal Q_{P,h}\) requires at least \(|\mathcal Q_{P,h}|\) elements. \(\square\)

Equality holds exactly when \(\Pi\) induces the same partition as \(q_{P,h}\), up to relabeling of representation values.

---

## Corollary C1.5 — Discrete entropy lower bound

Let \(X\) now be a discrete random state under any fixed state distribution for which the relevant entropies are finite. Define

\[
Q:=q_{P,h}(X),
\qquad
Z:=\Pi(X).
\]

If \(\Pi\) is exactly sufficient, then

\[
\boxed{
Q=g_\Pi(Z)
}
\]

almost surely, and therefore

\[
\boxed{
H(Q)\le H(Z).
}
\]

### Proof

The factorization theorem gives \(Q=g_\Pi(Z)\). Since \(Q\) is a deterministic function of \(Z\),

\[
H(Q\mid Z)=0.
\]

Hence

\[
H(Z)
=
H(Q)+H(Z\mid Q)-H(Q\mid Z)
=
H(Q)+H(Z\mid Q)
\ge H(Q).
\]

\(\square\)

Equality holds iff

\[
H(Z\mid Q)=0,
\]

so, on the support of the state distribution, \(Z\) is also a deterministic function of \(Q\). In that case the two representations encode the same consequence partition almost surely, up to relabeling.

This is a task-relative lower bound only. It is not a claim that entropy is the universal representation-complexity functional.

---

# 7. Deterministic factorization corollary

If the specified future consequence is deterministic,

\[
Y_{P,h}=F_{P,h}(X),
\]

then

\[
s\sim_{P,h}s'
\iff
F_{P,h}(s)=F_{P,h}(s').
\]

The quotient is therefore equivalent, up to relabeling, to the image of \(F_{P,h}\).

Every exact sufficient representation satisfies

\[
\boxed{
F_{P,h}=\widetilde F\circ\Pi
}
\]

for a unique \(\widetilde F\) on \(\Pi(\mathcal X)\).

Thus the familiar deterministic criterion

\[
\boxed{
\Pi(s)=\Pi(s')
\Rightarrow
Y_{P,h}(s)=Y_{P,h}(s')
}
\]

is exactly the factorization criterion.

---

# 8. Task dependence is structural, not a defect

The quotient is indexed by the consequence question.

Change any of

\[
(P,h,Y)
\]

and the kernel may change:

\[
K_{P,h,Y}
\neq
K_{P',h',Y'}.
\]

Therefore the equivalence relation may change:

\[
\boxed{
\sim_{P,h,Y}
\neq
\sim_{P',h',Y'}.
}
\]

and consequently

\[
\boxed{
q_{P,h,Y}
\neq
q_{P',h',Y'}
}
\]

in general.

### Tiny witness

Let

\[
\mathcal X=\{0,1\}\times\{0,1\}
\]

with state \(s=(u,v)\).

For consequence question A, let

\[
Y_A=u.
\]

Then the coarsest exact quotient retains only \(u\):

\[
q_A(u,v)=u.
\]

For consequence question B, let

\[
Y_B=v.
\]

Then the coarsest exact quotient retains only \(v\):

\[
q_B(u,v)=v.
\]

Thus

\[
q_A\neq q_B.
\]

Neither is a universally correct representation of the physical state. Each is coarsest exact only relative to its specified future consequence.

---

# 9. What C1 earns

C1 earns the following statements.

## Earned 1 — exact sufficiency is a partition constraint

\[
\boxed{
\Pi(s)=\Pi(s')
\Longrightarrow
K_s=K_{s'}.
}
\]

An exact sufficient representation cannot collapse a consequential distinction defined by the frozen future-law kernel.

## Earned 2 — canonical coarsest exact quotient

\[
\boxed{
q_{P,h}(s)=[s]_{P,h}
}
\]

is exact sufficient and every other exact sufficient representation deterministically maps onto it:

\[
\boxed{
q_{P,h}=g_\Pi\circ\Pi.
}
\]

## Earned 3 — lower bounds under explicit complexity choices

For finite quotient spaces:

\[
|\Pi(\mathcal X)|\ge|\mathcal Q_{P,h}|.
\]

For discrete random states with finite entropy:

\[
H(q_{P,h}(X))\le H(\Pi(X)).
\]

These are explicit lower bounds, not a universal complexity theorem.

## Earned 4 — task relativity

\[
\boxed{
\text{coarsest exact sufficient quotient is relative to }(P,h,Y).
}
\]

Changing the future question can change which distinctions may safely be collapsed.

---

# 10. What C1 does not earn

C1 does **not** establish:

- approximate sufficiency;
- a universal optimal representation;
- causal relevance of quotient coordinates;
- causal modularity;
- low repair cost under future task changes;
- constructive discoverability of the quotient;
- empirical identifiability of the quotient from finite data;
- deadline-valid challengeability;
- `CWC`;
- authority.

In particular:

\[
\boxed{
\text{predictive sufficiency}
\not\Rightarrow
\text{causal relevance}
\not\Rightarrow
\text{causal modularity}.
}
\]

And:

\[
\boxed{
\text{coarsest for the current consequence question}
\not\Rightarrow
\text{cheapest to repair after the question changes}.
}
\]

That latter separation is the target of C4, not C1.

---

# 11. Relation to the frozen architecture

C1 adds no control surface.

It sharpens the meaning of representation sufficiency for a fixed consequence question:

```text
physical/system states
-> consequence-law equivalence classes
-> coarsest exact predictive quotient
```

The larger proof queue remains:

```text
C1  coarsest consequence-sufficient quotient             PROVED AT STATED SCOPE
C2  discarded-distinction / deadline impossibility       NEXT
C4  equal predictive sufficiency != equal repairability  OPEN
C3  construction latency + CWC composition               OPEN; expected to feed T13.5
```

The intended bridge to C2 is immediate. If

\[
s_a\not\sim_{P,h}s_b
\]

but a current representation satisfies

\[
\Pi(s_a)=\Pi(s_b),
\]

then \(\Pi\) is not sufficient for that frozen consequence question. C2 will add the stronger deadline statement: if the represented adaptive path laws remain identical through the consequence horizon, no represented-history-measurable test can recover the lost distinction in time.

---

# 12. Freeze

The theorem-level compression is:

\[
\boxed{
\Pi\text{ exact-sufficient}
\iff
q_{P,h}=g_\Pi\circ\Pi.
}
\]

Therefore:

\[
\boxed{
\textbf{
The coarsest exact predictive representation for a specified future question
is the quotient that identifies exactly those current states with identical
future consequence laws.
}
}
\]

And the authority boundary remains unchanged:

```text
coarsest predictive quotient
!=
causal representation
!=
repairable representation
!=
validated refinement
!=
authority
```
