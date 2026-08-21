# OpenCore Topological Reopenability Lineage — FOREIGN-007

**Publication status:** append-only experimental lineage record  
**Target branch:** `opencore/crank-mini-001`  
**Architecture change:** none  
**Nano change:** none

Frozen Nano SHA-256 throughout FOREIGN-007:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

## Result geometry

```text
FOREIGN-003  future-relevant quotient collapse -> wound
FOREIGN-004  tested-safe historical quotient -> safe quotient
FOREIGN-005  safe effective quotient + latent source -> informational reopenability
FOREIGN-006  bounded blind compression -> compressed informational reopenability / rank boundary
FOREIGN-007  safe-now quotient -> policy support collapse -> corrective-path foreclosure
```

## FOREIGN-007 result

Classification:

```text
EPISTEMIC_FORECLOSURE_ESTABLISHED
```

Scientific question:

> Can a currently acceptable quotient change policy reachability so that a physically available experiment capable of exposing the quotient's later inadequacy is no longer selected?

The frozen witness isolates:

```text
representation
-> policy support
-> corrective reachability
-> future evidence acquisition
```

At the initial time, the quotient is safe over the complete frozen action surface: both `a_act` and `a_probe` are nondiscriminating across the two hidden regimes.

At the later reveal window, physical action availability remains identical in fine and coarse branches, but the targeted probe becomes discriminating. The same frozen policy retains the probe in support for the distinction-preserving representation and removes it from support for the coarse quotient.

Thus the targeted coarse branch satisfies:

```text
D(Pi_t) intersect R_available != empty
D(Pi_t) intersect R_policy    = empty
```

The endogenous coarse policy executes only the nondiscriminating action and therefore receives no corrective evidence.

## Forced-probe attribution control

The same probe excluded by the endogenous coarse policy is externally forced on separate copies of the coarse branches.

It immediately produces the correct hidden-regime signals and those observations authorize the corresponding refinements under unchanged Nano.

Therefore the wound is not attributable to:

```text
apparatus failure
Nano failure
physical action unavailability
missing discriminating consequence
```

It is localized to:

```text
representation-induced loss of corrective policy reachability
```

## Null control

A separate null world preserves the same representation manipulation, policy rule, probe cost, and physical action set while the later probe remains nondiscriminating.

The coarse policy again omits the probe, but this omission is harmless. Forced probing returns only the shared `SAME` observation, and both false regime-specific refinements are explicitly denied.

The result therefore does not imply that policies should always probe.

## Exact checks

Canonical V2:

```text
formal checks:       47 / 47 PASS
persistence checks: 33 / 33 PASS
```

## Prospective and execution hashes

```text
FOREIGN_007_SPEC.md
b51a4bddbf6d09aa84a064a8ed4489cc97e35fff7cc95e0277b53169a18b28cd

foreign_007.py  (prospectively frozen V1)
88a7905cd34d2fa67f2326e6dc4995724d3952d58bbd6d4b32099cb996574748

foreign_007_v2.py  (canonical coverage-repaired harness)
e128428c325cf1bc0d4d4462685ffaa09477c01015fa516495d96d57d180eee2

foreign_007_result.json  (V1)
ae3865cac53d75c4f913ab6cb474dccc9a0fe956e171c870889b59da21e82a28

foreign_007_result_v2.json  (canonical V2)
eb7491264b30fca38c3a60bacb35075021d95563552e46b18d1bbcd403a92e4a

FOREIGN_007.md
feab10589e869a020b0ff1f7f7bc7fd31421b6f71b6ecf312bf7ceca327bf565
```

## V1 -> V2 provenance

V1 already produced the positive classification with all formal checks passing. Post-run audit found only a null-control coverage asymmetry: the harness explicitly attempted a false A refinement from the nondiscriminating `SAME` observation but did not separately attempt the symmetric false B refinement.

V2 adds only the missing symmetric denial test. No world definition, policy rule, action availability, quotient, forced-probe witness, Nano contract, or result class changed.

## Earned claim

On this constructed deterministic family:

> A representation quotient that was safe over the complete current action surface changed later policy support so that a physically available future corrective experiment was no longer selected. Externally restoring that excluded path immediately restored discrimination and authority-changing correction.

This establishes pressure for a distinction between:

```text
informational reopenability
!=
topological reopenability
```

## Claim ceiling

FOREIGN-007 does **not** establish:

- a universal corrigibility invariant;
- that every physically available probe must remain policy-reachable;
- a curiosity or exploration module;
- a reachability primitive;
- automatic discriminator discovery;
- automatic quotient repair;
- a general theorem over policies or control systems;
- Nano V1 or any Nano repair;
- that utility-induced foreclosure has been established.

## Candidate next pressure, not executed here

A genuinely independent next assay would hold representation expressivity fixed while suppressing a corrective probe through objective/cost optimization, testing:

```text
representation-induced foreclosure
!=
utility-induced foreclosure
```

No such result is claimed by FOREIGN-007.
