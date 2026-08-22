# FOREIGN-007 — Policy-Induced Epistemic Foreclosure

**Classification:** `EPISTEMIC_FORECLOSURE_ESTABLISHED`

## Scientific question

Can a representation quotient that is consequence-equivalent over the complete current action surface alter later policy support so that a physically available future experiment capable of exposing the quotient's inadequacy is not selected?

## Prospective freeze

Specification SHA-256 before execution:

```text
b51a4bddbf6d09aa84a064a8ed4489cc97e35fff7cc95e0277b53169a18b28cd
```

Original frozen harness SHA-256:

```text
88a7905cd34d2fa67f2326e6dc4995724d3952d58bbd6d4b32099cb996574748
```

Frozen Nano SHA-256:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

No architecture or Nano change was made.

## Frozen world and current safety

Two hidden regimes exist:

```text
W_A
W_B
```

At `t0`:

```text
Phi_t0(W_A) = Phi_t0(W_B) = K
```

Both physically available actions are nondiscriminating:

```text
a_act(W_A)   = ACT_OK
a_act(W_B)   = ACT_OK

a_probe(W_A) = NO_SIGNAL
a_probe(W_B) = NO_SIGNAL
```

Therefore the coarse quotient is safe over the **complete frozen t0 action surface**.

At `t1`, an exogenous reveal window opens. Physical availability remains:

```text
R_available = {a_act, a_probe}
```

in every targeted representation branch.

The act remains nondiscriminating:

```text
a_act(W_A) = ACT_OK
a_act(W_B) = ACT_OK
```

while the targeted probe becomes the sole discriminator:

```text
a_probe(W_A) = SIG_A
a_probe(W_B) = SIG_B
```

## Representation-to-policy coupling

Fine representation retains two unresolved candidate cells:

```text
candidate:A = POSSIBLE
candidate:B = POSSIBLE
```

Coarse representation retains one quotient cell:

```text
candidate:K = POSSIBLE
```

The same frozen policy rule is used in both branches:

```text
if effective candidate-cell count > 1:
    support = {a_probe, a_act}
    select a_probe
else:
    support = {a_act}
    select a_act
```

Probe cost is 1; act cost is 0.

Observed target policy topology:

```text
fine:
  R_policy = {a_probe, a_act}
  selected = a_probe

coarse:
  R_policy = {a_act}
  selected = a_act
```

Thus the exact foreclosure witness is:

```text
D(Pi_t) = {a_probe}
D(Pi_t) intersect R_available != empty
D(Pi_t) intersect R_policy_coarse = empty
```

Physical availability did not change. Policy reachability did.

## Targeted branch result

### Fine representation

For `W_A`:

```text
a_probe -> SIG_A
observation receipt: 512fc0712f2b0f1dcb7107ef
refinement receipt:  0aee0851bdaccb85157038de
refinement parent:   512fc0712f2b0f1dcb7107ef
identified regime:   A
```

For `W_B`:

```text
a_probe -> SIG_B
observation receipt: a6e5d5e86b5af3269035abcc
refinement receipt:  2c0fc677a5e962d0fb8bc642
refinement parent:   a6e5d5e86b5af3269035abcc
identified regime:   B
```

Each observation and refinement was Nano `ALLOW`.

### Coarse quotient under its own policy

For both hidden regimes:

```text
policy support = {a_act}
selected       = a_act
observation    = ACT_OK
identified regime = absent
```

The discriminating experiment remained physically available but was not policy-reachable.

## Forced-probe causal control

A separate copy of the same coarse branch was externally forced to execute the excluded `a_probe`.

For `W_A`:

```text
forced a_probe -> SIG_A
observation receipt: 6b75b3f79bc126ccc486a1f7
refinement receipt:  26e27eb9ff5b63e068ed7a00
refinement parent:   6b75b3f79bc126ccc486a1f7
identified regime:   A
```

For `W_B`:

```text
forced a_probe -> SIG_B
observation receipt: 206c0bffd1e2d11a438a8dc9
refinement receipt:  fadab7cad5dd8fd11fa6fbbc
refinement parent:   206c0bffd1e2d11a438a8dc9
identified regime:   B
```

The forced path used the same unchanged Nano contracts and produced the same type of authority-changing refinement as the fine branch.

Therefore apparatus availability and Nano authorization were not the obstruction. The obstruction was localized to:

```text
representation -> policy support -> corrective reachability
```

## Nondiscriminating-probe null control

A separate null world retained the same observation K, same representation manipulation, same physical action set, same policy rule, and same probe cost.

At `t1`:

```text
a_probe(W_A^null) = SAME
a_probe(W_B^null) = SAME
```

The coarse policy again selected `a_act` and excluded `a_probe`, but no hidden distinction was missed.

Fine and externally forced coarse null probes both admitted `SAME` and correctly persisted only:

```text
null-probe-profile = NONDISCRIMINATING
```

Both A-specific and B-specific false refinements from `SAME` were explicitly Nano `DENY` in the audited V2 run.

This control shows that probe exclusion alone is not the wound. It becomes a wound only when the excluded physically available path is genuinely discriminating.

## Exact checks

Canonical V2 run:

```text
formal checks:       47 / 47 PASS
persistence checks:  33 / 33 PASS
```

Nano SHA-256 before and after:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Nano was unchanged.

## V1 -> V2 audit provenance

The original frozen V1 harness completed scientifically positive:

```text
classification:      EPISTEMIC_FORECLOSURE_ESTABLISHED
formal:              47 / 47 PASS
persistence:         29 / 29 PASS
```

Post-run audit found one **test-coverage asymmetry** in the null control: V1 explicitly attempted the false A-specific refinement from `SAME`, but did not separately attempt the symmetric false B-specific refinement.

The effective null state was unsplit and no scientific result was contradicted. V2 made only the coverage repair:

```text
false A refinement from SAME -> DENY
false B refinement from SAME -> DENY
```

No world definition, policy rule, representation condition, physical availability, forced-probe control, result class, or Nano contract changed.

V1 artifacts:

```text
harness SHA-256: 88a7905cd34d2fa67f2326e6dc4995724d3952d58bbd6d4b32099cb996574748
result  SHA-256: ae3865cac53d75c4f913ab6cb474dccc9a0fe956e171c870889b59da21e82a28
run log SHA-256: fe77b7f4e378ae883a3c25a1547bd2ed0110d1424cd5844b7c0fac91769b9a8d
```

V2 artifacts:

```text
harness SHA-256: e128428c325cf1bc0d4d4462685ffaa09477c01015fa516495d96d57d180eee2
result  SHA-256: eb7491264b30fca38c3a60bacb35075021d95563552e46b18d1bbcd403a92e4a
run log SHA-256: 4ce83a78203097b55e186698dcb622a7950491475f41e9252e4be4cef1a2381b
```

## Earned result

On this constructed deterministic family:

> A representation quotient that was consequence-equivalent over the complete current action surface altered later policy support so that a physically available future discriminating probe was not selected. The coarse policy therefore remained at the shared representation. Externally forcing that same excluded probe recovered the hidden distinction and, under unchanged Nano, authorized the same regime-specific persistent refinement observed in the distinction-preserving branch. Excluding an otherwise identical nondiscriminating probe was harmless.

This establishes the tested causal topology:

```text
currently safe quotient
-> policy simplification
-> discriminating action absent from policy support
-> no discriminating evidence under endogenous policy
-> apparent stability of coarse representation
```

while the forced control establishes:

```text
physical path still available
-> forced probe
-> discriminating evidence
-> authority-changing refinement
```

## Candidate strengthened, not proven

A stronger hypothesis is now worth attacking:

> Corrigibility may require not only informational reopenability, but preservation of live policy-reachable causal paths through which a future discrepancy can become observable, discriminating, and authority-changing.

Equivalently, provisionally:

```text
informational reopenability != topological reopenability
```

and:

```text
absence of contradiction != survival under physically available contradiction
```

## Claim ceiling

FOREIGN-007 does **not** establish:

- that all locally safe quotients risk foreclosure;
- that every diagnostic action must remain policy-reachable;
- that probe-preserving policies are generally optimal;
- a universal corrigibility law;
- a universal distinction between `R_available`, `R_policy`, and `R_realized`;
- a new reachability, topology, scheduler, or exploration primitive;
- automatic discovery of discriminating interventions;
- automatic quotient repair;
- Nano V1 or any Nano modification;
- a general theory of agency, intelligence, or world models.

## Diagnosis

`policy-induced corrective-path foreclosure upstream of unchanged Nano`
