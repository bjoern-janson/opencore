# C4 — Equal Current Sufficiency Does Not Imply Equal Repairability

**Status:** `PROVED_EXISTENCE_COUNTEREXAMPLE_AT_STATED_SCOPE`  
**Scope:** finite task-relative predictive representations under an explicit coordinate-adjunction repair language  
**Empirical authority added:** none  
**New architectural primitive:** none  
**CWC definition changed:** no  
**T13 construction experiment authorized:** no

This note proves the third theorem in the post-freeze adaptive coarse-graining queue.

C1 established the coarsest exact consequence-sufficient quotient for a frozen consequence question. C2 established that if a later-consequential distinction remains absent from the entire represented deadline experiment, nontrivial CWC is impossible. C4 now asks a different question:

> **Can two representations be equally adequate for the current task, and equally large under simple current complexity measures, while having different costs of becoming adequate for a later task?**

Yes.

The result is deliberately negative and deliberately small:

\[
\boxed{
\text{equal current predictive sufficiency}
\not\Rightarrow
\text{equal future repairability}.
}
\]

In fact, under one explicit common refinement language, the repair-cost gap can be made arbitrarily large while the two current representations have the same output cardinality and the same entropy under a natural uniform state law.

The theorem does **not** define a universal repair metric. Repair cost is relative to an explicitly frozen admissible refinement language. That dependence is part of the result rather than something to hide.

---

## 1. State space and current task

Fix an integer

\[
m\ge 1.
\]

Let the physical/system state be

\[
\boxed{
X=(U,V_1,\ldots,V_m,W_1,\ldots,W_m)
\in\{0,1\}^{1+2m}.
}
\]

Write

\[
V:=(V_1,\ldots,V_m),
\qquad
W:=(W_1,\ldots,W_m).
\]

The current consequential task is deterministic:

\[
\boxed{
Y_0=U.
}
\]

Thus the C1 consequence-equivalence relation for the current task is

\[
x\sim_0 x'
\iff
u(x)=u(x'),
\]

and the coarsest exact current quotient is simply

\[
\boxed{
q_0(X)=U.
}
\]

The coordinates \(V\) and \(W\) are both currently consequence-irrelevant.

---

## 2. Two equally sufficient current representations

Define

\[
\boxed{
\Pi_V(X):=(U,V_1,\ldots,V_m)
}
\]

and

\[
\boxed{
\Pi_W(X):=(U,W_1,\ldots,W_m).
}
\]

### Lemma C4.1 — Both representations are exactly sufficient for the current task

If

\[
\Pi_V(x)=\Pi_V(x'),
\]

then in particular

\[
u(x)=u(x'),
\]

so

\[
Y_0(x)=Y_0(x').
\]

Hence \(\Pi_V\) is exactly sufficient for the current task.

The same argument applies to \(\Pi_W\). Therefore

\[
\boxed{
\Pi_V,\Pi_W
\text{ are both exact-sufficient for }Y_0=U.
}
\]

Both strictly refine the coarsest current quotient \(q_0=U\), but they preserve different currently dormant distinctions.

This is important: C4 does **not** require either representation to be the coarsest current quotient. It asks whether current predictive adequacy determines future repairability. The counterexample will show that it does not.

\(\square\)

---

## 3. Matching current representation size

The counterexample can be made stronger than merely equal predictive adequacy.

Both representations have the same attained cardinality:

\[
\boxed{
|\Pi_V(\mathcal X)|
=
|\Pi_W(\mathcal X)|
=
2^{m+1}.
}
\]

Now let \(X\) be uniformly distributed on \(\{0,1\}^{1+2m}\). Then the retained coordinates are mutually independent fair bits, so

\[
\boxed{
H(\Pi_V(X))
=
H(\Pi_W(X))
=
m+1
\text{ bits}.
}
\]

Thus the two current representations agree on:

- exact predictive sufficiency for the current task;
- output cardinality;
- entropy under the frozen uniform state law.

Yet they will have different future repair costs.

---

## 4. Future task change

Now change the consequential future question.

Let the new task require the vector \(V\):

\[
\boxed{
Y_1:=V=(V_1,\ldots,V_m).
}
\]

Equivalently, the previously dormant distinction

\[
\boxed{
d^\star(X)=V
}
\]

has become consequential.

The new exact consequence-equivalence relation is

\[
x\sim_1 x'
\iff
V(x)=V(x').
\]

A representation is exactly sufficient for the new task iff it never merges two states with different \(V\) values.

---

## 5. Frozen admissible repair language

Repairability is not intrinsic to predictive sufficiency. It must be evaluated relative to an admissible refinement language.

For this counterexample, freeze the following simple common repair language for both starting representations.

A representation is a coordinate projection onto a subset of the raw state coordinates.

From any current coordinate set \(S\), one admissible repair step may append one previously unrepresented raw coordinate:

\[
\boxed{
\Pi_S
\longrightarrow
\Pi_{S\cup\{j\}}
}
\]

at unit cost.

No deletion is required. Reordering and relabeling retained coordinates have zero cost and do not change sufficiency.

Define the repair cost for the new task as

\[
\boxed{
C_{\rm repair}(\Pi;Y_1)
:=
\min\{k:\text{there is a }k\text{-step admissible refinement of }\Pi
\text{ that is exact-sufficient for }Y_1\}.
}
\]

This is a counterexample-specific operational cost, not a new permanent OpenCore primitive.

The same repair language is used for \(\Pi_V\) and \(\Pi_W\).

---

# 6. Main theorem

## Theorem C4.2 — Equal current sufficiency and equal current size can have unequal future repair cost

For every integer \(m\ge1\), the representations \(\Pi_V\) and \(\Pi_W\) defined above satisfy:

\[
\boxed{
\begin{aligned}
&\Pi_V,\Pi_W
\text{ are both exact-sufficient for }Y_0=U,\\[1mm]
&|\Pi_V(\mathcal X)|=|\Pi_W(\mathcal X)|=2^{m+1},\\[1mm]
&H(\Pi_V(X))=H(\Pi_W(X))=m+1
\quad\text{under uniform }X,
\end{aligned}
}
\]

but after the task change to \(Y_1=V\),

\[
\boxed{
C_{\rm repair}(\Pi_V;Y_1)=0,
}
\]

while

\[
\boxed{
C_{\rm repair}(\Pi_W;Y_1)=m.
}
\]

Hence

\[
\boxed{
\text{equal current predictive sufficiency}
\not\Rightarrow
\text{equal repairability},
}
\]

and the repair-cost gap can be arbitrarily large.

### Proof

### Part 1 — \(\Pi_V\) needs no repair

By definition,

\[
\Pi_V(X)=(U,V).
\]

Therefore \(V\) is already a deterministic function of \(\Pi_V(X)\): simply project onto the last \(m\) coordinates.

Thus if

\[
\Pi_V(x)=\Pi_V(x'),
\]

then

\[
V(x)=V(x'),
\]

so \(\Pi_V\) is already exact-sufficient for the new task \(Y_1=V\).

Therefore

\[
\boxed{
C_{\rm repair}(\Pi_V;Y_1)=0.
}
\]

### Part 2 — \(\Pi_W\) can be repaired in \(m\) steps

Start from

\[
\Pi_W(X)=(U,W_1,\ldots,W_m).
\]

Append the coordinates

\[
V_1,V_2,\ldots,V_m
\]

one at a time.

After \(m\) admissible repair steps, the representation contains the full vector \(V\), and is therefore exact-sufficient for \(Y_1=V\).

Hence

\[
C_{\rm repair}(\Pi_W;Y_1)\le m.
\]

### Part 3 — fewer than \(m\) steps cannot suffice

Suppose fewer than \(m\) new coordinates have been appended to \(\Pi_W\).

Then at least one coordinate \(V_j\) remains unrepresented.

Choose two states \(x,x'\in\mathcal X\) that agree on:

- \(U\);
- every \(W_i\);
- every appended \(V_i\);
- every other represented coordinate;

but differ on the still-unrepresented bit \(V_j\).

Then the repaired representation takes the same value on \(x\) and \(x'\), while

\[
Y_1(x)=V(x)\neq V(x')=Y_1(x').
\]

Therefore the repaired representation is not exact-sufficient for the new task.

So no repair using fewer than \(m\) coordinate-adjunction steps can succeed:

\[
C_{\rm repair}(\Pi_W;Y_1)\ge m.
\]

Combining with the upper bound gives

\[
\boxed{
C_{\rm repair}(\Pi_W;Y_1)=m.
}
\]

The claimed gap follows. \(\square\)

---

# 7. What the counterexample proves

The theorem establishes all of the following at its stated scope:

\[
\boxed{
\text{current exact sufficiency}
\not\Rightarrow
\text{future repair cost}.
}
\]

Even adding equal current output cardinality does not determine repair cost:

\[
\boxed{
\text{equal sufficiency}
+
\text{equal current cardinality}
\not\Rightarrow
\text{equal repairability}.
}
\]

Even adding equal entropy under the frozen uniform law does not determine repair cost:

\[
\boxed{
\text{equal sufficiency}
+
\text{equal entropy}
\not\Rightarrow
\text{equal repairability}.
}
\]

The reason is structural rather than predictive:

\[
\boxed{
\text{the two representations preserve different dormant distinctions.}
}
\]

Both answer today's question equally well. Only one already contains tomorrow's newly consequential distinction.

---

# 8. Current quotient versus dormant retained distinctions

For the current task, the C1 coarsest quotient is

\[
q_0(X)=U.
\]

Both representations refine it:

\[
q_0=g_V\circ\Pi_V
\]

and

\[
q_0=g_W\circ\Pi_W.
\]

But their extra retained distinctions differ:

\[
\Pi_V\text{ preserves }V,
\qquad
\Pi_W\text{ preserves }W.
\]

Therefore current predictive adequacy does not determine which currently irrelevant distinctions remain available for later reuse.

This is the exact mathematical content of:

\[
\boxed{
\textbf{Task-specific predictive adequacy is not future-task robustness.}
}
\]

---

# 9. Why C4 does not define "optionality" as a new primitive

One may informally say that \(\Pi_V\) preserves more optionality for the later task \(Y_1=V\) than \(\Pi_W\).

C4 does not add an `optionality` state variable or control surface.

Everything needed for the theorem is already specified by:

1. the current representation;
2. the later consequence question;
3. the admissible repair/refinement language;
4. the induced minimum repair cost.

Thus:

\[
\boxed{
\text{future-task optionality}
\text{ is treated here as a derived property of }(\Pi,\mathcal G_{\rm repair},Y_1),
}
\]

not as a new architectural primitive.

---

# 10. Important scope boundary — identical current partitions are not proved here

The theorem proves **equal current predictive sufficiency**, not identity of the two representation partitions.

Indeed,

\[
\Pi_V
\]

and

\[
\Pi_W
\]

split the currently consequence-equivalent states in different ways.

This is deliberate.

If two representations induce exactly the same partition of \(\mathcal X\), then as extensional quotient maps they differ only by a relabeling of attained cells. To obtain different repair costs from such extensionally identical partitions, one must specify additional refinement geometry, implementation structure, coordinate constraints, or another admissible-edit notion not contained in the partition alone.

C4 does **not** smuggle such extra structure into the theorem.

Therefore the stronger claim

\[
\boxed{
\text{identical current partition}
\not\Rightarrow
\text{equal repair cost}
}
\]

is **not proved here**.

What is proved is already sufficient for the intended negative result:

\[
\boxed{
\text{predictive equivalence at the current task}
\text{ is too weak to determine future repairability}.
}
\]

---

# 11. Relation to C1

C1 says that exact sufficiency for the current task requires only that the current consequence quotient factor through the representation.

Both \(\Pi_V\) and \(\Pi_W\) satisfy that requirement.

C1 does not constrain which additional currently irrelevant distinctions a sufficient representation may preserve.

C4 shows that those extra distinctions can matter after a task change.

Thus:

\[
\boxed{
\text{C1 current sufficiency class}
\text{ contains representations with different future repair costs}.
}
\]

So the coarsest current quotient characterizes minimal exact predictive distinction, but not future corrigibility geometry.

---

# 12. Relation to the multi-task quotient observation

If both the current task \(Y_0=U\) and the future task \(Y_1=V\) had been known to be consequential from the start, the joint C1 quotient would preserve both:

\[
q_{\{0,1\}}(X)=(U,V)
\]

up to relabeling.

In that case \(\Pi_V\) already realizes a jointly sufficient representation, while \(\Pi_W\) does not.

C4 therefore exhibits the representational price of not knowing which currently irrelevant distinctions will matter later:

\[
\boxed{
\text{current-task sufficiency}
\neq
\text{joint current+future-task sufficiency}.
}
\]

But C4 does not conclude that all dormant distinctions should be preserved. The identity map trivially preserves all distinctions and defeats the purpose of coarse-graining.

The theorem establishes a tradeoff, not a design rule.

---

# 13. Relation to C2 and T13

C4 ends at repairability.

It does not say that a representation with positive repair cost is unsafe or non-corrigible.

If \(\Pi_W\) can append the missing \(V\) coordinates quickly enough, and the resulting post-repair experiment is selection-aware and satisfies the frozen CWC certificate before the consequence deadline, then the system may remain corrigible.

Thus:

\[
\boxed{
C_{\rm repair}>0
\not\Rightarrow
\neg\mathsf{CWC}.
}
\]

C2 applies only if the consequential distinction remains absent from the complete represented path experiment through the deadline.

The full escalation remains:

```text
new task
-> current representation insufficient
-> repair/refinement required
-> repair reachable or not
-> selection-aware re-entry
-> represented path laws separate or not
-> CWC
-> scoped authority
```

---

# 14. Claim ceiling

C4 proves only an existence counterexample under the stated coordinate-adjunction repair language.

It does **not** prove:

- a universal repair-cost functional;
- that retaining more dormant information is always better;
- that larger representations are always more repairable;
- that entropy predicts repairability;
- that identical current partitions necessarily have different repair costs;
- that causal modularity has been established;
- that any particular latent coordinate is causally manipulable;
- that repair cost should become a fourth adaptive control surface;
- that any empirical OpenCore system has the C4 property;
- that a construction experiment is authorized.

The theorem is a negative separation result only.

---

# 15. Earned compression

The exact theorem-level compression is:

\[
\boxed{
\textbf{
Current predictive sufficiency constrains which distinctions may be merged
for today's consequence question; it does not determine which currently
dormant distinctions remain cheaply recoverable after the question changes.
}
}
\]

Or more compactly:

\[
\boxed{
\textbf{Predictive adequacy does not determine escape cost.}
}
\]

Together with C1 and C2:

```text
C1  what may be collapsed for the frozen consequence question
C4  equally adequate current representations can differ in repair cost
C2  if the needed distinction remains absent through the deadline, CWC fails
```

The next theorem in the frozen queue is C3: compose repair/construction latency with fresh CWC adjudication into an explicit deadline failure budget, feeding T13.5 rather than creating a new conceptual layer.
