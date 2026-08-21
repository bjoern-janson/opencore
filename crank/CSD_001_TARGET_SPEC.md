# CSD-001 — Mini Target Specification

**Status:** `FROZEN_PROSPECTIVE_TARGET_SPEC`  
**Scientific role:** target/measurement freeze before any Mini × CSD-001 evaluation  
**CSD-001 apparatus:** unchanged  
**Target organism:** unchanged OpenCore Mini core  
**L2 mechanism added:** none  
**L2 target evaluation:** not run by this specification  
**L3:** excluded  
**Nano:** absent

## 1. Purpose

This file freezes the first CSD-001 target before the target is allowed to see any CSD-001 evaluation trajectory.

The target-selection audit established only that unchanged Mini exposes an `R3`-eligible native degree of freedom:

```text
challenge_buffers / needs_probe(scope)
```

Its pre-CSD semantics are deliberately weaker than the L2 claim:

```text
needs_probe(scope)
=
current challenge / replacement evidence for this scope remains underdetermined
```

This specification MUST NOT redefine that state as:

```text
challenge-set insufficiency
```

The CSD-001 trial will determine whether the timing, selectivity, and causal behavior of this pre-existing Mini state warrant that stronger interpretation under the frozen assay.

The governing epistemic order is:

```text
frozen target identity
-> frozen raw transport
-> frozen stateless measurement
-> target evaluation
-> only then scientific interpretation
```

No target result may revise this file under the same assay identity.
