# Candidate Transition Invariant

## Status

**Candidate common explanatory structure. Not a theorem. Not a promoted OpenCore primitive.**

Multiple independently constructed crank failures can currently be compressed into two opposing transition defects.

## 1. The transition, not only the state

Suppose an adaptive system moves from one epistemic state to another:

```text
X_i -> X_{i+1}
```

The crank experiments suggest that state correctness and transition correctness are different questions.

A datum can be true while the transition that promotes it is invalid.

A model can be locally supported while the transition that closes challenge is unauthorized.

A capability can be authentic while its preconditions no longer hold at execution.

## 2. Premature quotient

A transition merges states that future correction may still need to distinguish.

Conceptually:

```text
x !=_future y
but
T(x) = T(y)
```

Examples from the current lineage:

- aliased observation interfaces;
- over-generalizing one rule across contexts with different laws;
- treating historical authorization as equivalent to current authorization;
- allowing descendants to remain effective after a warrant ancestor loses authority;
- discarding a distinction needed for later challenge or reconciliation.

The common failure is loss of correction-relevant resolution.

## 3. Unauthorized refinement

A transition creates a stronger epistemic distinction, role, independence claim, applicability claim, or authority state than its inputs warrant.

Conceptually:

```text
x ==_evidence y
but
Authority(T(x)) != Authority(T(y))
```

Examples:

```text
prediction -> observation authority
correlated reports -> independent corrective paths
closure authority -> applicability
selected clean reports -> evidence with warrant of a different acquisition protocol
```

No false payload is required. The failure may be entirely in the role assigned downstream.

## 4. Two-sided candidate rule

A compact candidate requirement is:

> **An adaptive transition should neither erase distinctions still required for correction nor manufacture epistemic authority not supplied by its warrant.**

The Nano-facing operational form is deliberately weaker and more mechanical:

> **Don't write beyond your effect capability. Don't erase beyond your preservation capability.**

Nano does not know which distinctions *should* matter. Those obligations are constituted externally in V0.

## 5. Why composition is the adversary

Let:

```text
T1: X -> Y
T2: Y -> Z
```

Both transitions may be locally valid.

That does not establish:

```text
Valid(T2 o T1)
```

A particularly useful formulation is:

```text
Post(T1) does not satisfy Pre(T2)
```

The M2 × M4 acquisition/closure attack is the clearest example.

The closure capability is authentic, but an intervening acquisition-policy transition changes the condition under which the closure certificate is licensed.

Nano V0 therefore rechecks current preconditions at execution.

## 6. Relation to reliable generalization

A transfer relation can fail in both directions.

### Over-merge

Two contexts are treated as equivalent although different laws apply.

This is a premature quotient.

### Over-split

Every novel context is treated as a distinct class without evidence that the distinction matters.

This is an unauthorized refinement of the transfer partition.

The desired object is therefore close to:

> **the coarsest transfer relation currently warranted by evidence, while remaining open to correction.**

This motivates the phrase:

```text
reliable generalization ~= warranted quotient construction
```

but that remains a research target rather than an established result.

## 7. `DEFER` in this picture

Across the crank experiments, `DEFER` repeatedly means that a requested collapse or promotion is not licensed yet.

At the Nano layer specifically:

```text
DEFER = a required contract-visible proposition is not currently established
```

At higher epistemic layers, a related behavior is:

> preserve the unresolved distinction and seek discriminating evidence rather than forcing an unsupported merge or split.

This behavioral pattern may eventually deserve a more general abstraction. V0 does not promote one.

## 8. What would falsify or weaken this compression

The candidate invariant should lose authority if independent failure classes repeatedly require explanations that do not reduce to either:

- lost correction-relevant distinction; or
- manufactured unearned distinction/authority.

Likewise, a smaller competing formulation should replace it if it predicts the same experimental failures with fewer assumptions.

The research program therefore should keep attacking from domains not designed around this vocabulary.
