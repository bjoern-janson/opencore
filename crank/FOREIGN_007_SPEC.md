# FOREIGN-007 — Policy-Induced Epistemic Foreclosure

**Status before execution:** `FROZEN_PROSPECTIVE_ASSAY`

## Scientific question

Can a representation quotient that is safe over the complete currently available consequence surface alter later policy reachability so that a physically available experiment capable of exposing the quotient's future inadequacy is no longer selected?

The assay targets a coupling:

```text
representation
-> policy support
-> reachable corrective action
-> observation
-> authority-changing refinement
```

It does **not** propose a new OpenCore primitive, scheduler, exploration rule, or Nano change.

## Foreign world

There are two hidden deterministic regimes:

```text
W_A
W_B
```

At time `t0`, the current observation interface is identical:

```text
Phi_t0(W_A) = Phi_t0(W_B) = K
```

Two actions are physically available in every branch:

```text
a_act
a_probe
```

At `t0`, both actions are nondiscriminating:

```text
a_act(W_A)   = ACT_OK
a_act(W_B)   = ACT_OK

a_probe(W_A, t0) = NO_SIGNAL
a_probe(W_B, t0) = NO_SIGNAL
```

Therefore `W_A` and `W_B` are consequence-equivalent over the **complete frozen t0 action surface**, not merely over a selectively chosen subset.

At `t1`, an exogenous reveal window opens. `a_act` remains nondiscriminating:

```text
a_act(W_A, t1) = ACT_OK
a_act(W_B, t1) = ACT_OK
```

but in the targeted world the same physically available probe becomes discriminating:

```text
a_probe(W_A, t1) = SIG_A
a_probe(W_B, t1) = SIG_B
```

The reveal window is independent of the representation and policy branch.

## Representation manipulation

The current observation is `K` in both representation conditions.

### Fine / distinction-preserving representation

The model retains two unresolved candidate possibilities:

```text
candidate:A = POSSIBLE
candidate:B = POSSIBLE
```

It does **not** know which is true.

### Coarse quotient

The same two possibilities are represented as one effective candidate:

```text
candidate:K = POSSIBLE
```

No `A`/`B` candidate distinction remains effective.

The quotient is prospectively required to be safe over every frozen `t0` consequence.

## Frozen policy rule

The policy sees only the effective representation and the physically available action set. It does not see hidden regime identity.

```text
if number_of_effective_candidate_cells > 1:
    policy_support = {a_probe, a_act}
    selected_action = a_probe
else:
    policy_support = {a_act}
    selected_action = a_act
```

Probe cost is `1`; act cost is `0`.

The policy rule is identical in fine and coarse branches. Only the effective representation changes.

Thus at `t1` the prospective discriminator is:

```text
fine  -> a_probe remains policy-reachable and is selected
coarse -> a_probe is physically available but absent from policy support
```

## Targeted forced-probe control

For a separate copy of each coarse targeted branch, externally override the policy and execute the physically available `a_probe` at `t1`.

Required outcome:

```text
W_A -> SIG_A
W_B -> SIG_B
```

Each observation must be admissible to unchanged Nano and must authorize the corresponding regime-specific refined standing.

This control localizes any failure to:

```text
representation -> policy -> reachability
```

rather than apparatus inability or Nano inability.

## Nondiscriminating-probe null world

A separate null world has the same current observation, same representation manipulation, same physically available actions, same policy rule, and same probe cost.

At `t1` its probe remains nondiscriminating:

```text
a_probe(W_A^null, t1) = SAME
a_probe(W_B^null, t1) = SAME
```

The coarse policy therefore still excludes `a_probe`, but this exclusion must be harmless: no regime-specific distinction is available to lose.

The fine null branch may spend the probe cost and observe `SAME`, but it must not create a false A/B refinement.

This null control prevents the result from implying that policies should always probe.

## Nano boundary

Frozen Nano SHA-256:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Nano may only:

- persist externally supplied representation standings;
- admit externally constituted probe observations;
- authorize regime-specific refined standings when the matching observation standing exists;
- persist a shared null-probe standing from `SAME`;
- DEFER regime-specific refinement without matching probe evidence.

Nano must not:

- inspect hidden regime identity;
- choose actions;
- compute policy support;
- know physical action availability;
- open the reveal window;
- execute or force probes;
- decide that the quotient is inadequate.

## Prospective positive requirements

`EPISTEMIC_FORECLOSURE_ESTABLISHED` requires all of the following:

1. `W_A != W_B`.
2. `Phi_t0(W_A) = Phi_t0(W_B) = K`.
3. Both `a_act` and `a_probe` are physically available at `t0` and `t1` in fine and coarse branches.
4. At `t0`, both actions have identical consequences under `W_A` and `W_B`.
5. Fine and coarse use the same frozen policy rule.
6. Fine representation retains two unresolved candidate cells and policy support contains `a_probe`.
7. Coarse representation contains one quotient candidate and policy support excludes `a_probe` while physical availability still contains it.
8. At `t1` in the targeted world, `a_probe` is genuinely discriminating and is the only action that distinguishes `W_A` from `W_B`.
9. Fine targeted policy selects `a_probe`, obtains `SIG_A`/`SIG_B`, and unchanged Nano authorizes the matching refined standing.
10. Coarse targeted policy selects `a_act`, obtains only `ACT_OK`, and no regime-specific refined standing appears.
11. Externally forced `a_probe` on the coarse targeted branch obtains `SIG_A`/`SIG_B` and unchanged Nano authorizes the matching refined standing.
12. Thus the targeted discriminator intersects physical availability but not coarse policy support.
13. In the null world, `a_probe` returns `SAME` for both hidden regimes, coarse non-selection causes no missed distinction, and fine probing does not create a false regime-specific refinement.
14. Nano source SHA-256 is identical before and after execution.

## Result classes

### `EPISTEMIC_FORECLOSURE_ESTABLISHED`

All prospective positive requirements pass.

### `NO_FORECLOSURE`

The targeted discriminating probe remains policy-reachable under the coarse quotient, so the proposed representation-to-policy foreclosure does not occur.

### `INVALID`

Any required isolation fails, including if:

- `t0` is already discriminating;
- physical action availability differs between representation branches;
- the policy rule differs between fine and coarse;
- the coarse policy still contains the targeted probe but the harness calls it unreachable;
- forced targeted probing cannot recover the distinction;
- Nano blocks a correctly evidenced forced refinement;
- the null probe creates a false distinction;
- Nano changes.

## Claim ceiling

A positive result would establish only, on this constructed deterministic family:

> A representation quotient that was consequence-equivalent over the complete current action surface altered later policy support so that a physically available future discriminating probe was not selected; externally forcing that same probe recovered the distinction and enabled the same downstream authority update under unchanged Nano.

It would **not** establish:

- that all compression risks epistemic foreclosure;
- that all policies must preserve every diagnostic action;
- a universal corrigibility invariant;
- a new OpenCore reachability primitive;
- an exploration scheduler;
- automatic interface invention;
- automatic quotient repair;
- Nano V1 or any Nano modification;
- a general theory of agency or intelligence.
