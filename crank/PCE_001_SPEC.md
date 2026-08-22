# PCE-001 — Protected Corrective Exposure

**Status before execution:** `FROZEN_PROSPECTIVE_INTERVENTION_ASSAY`  
**Lineage:** descendant of BLITZCRANK-001/002  
**OpenCore components inside organism:** none  
**Nano:** absent  
**Autonomous challenge constitution:** not tested

## Frozen mechanistic core

PCE-001 intervenes on one edge only:

```text
E_t -> Pi_t -> pi_t -> A_t -> O_{t+1} -> W_{t+1} -> E_{t+1}
```

The environment is externally generated:

```text
O_{t+1} = g(X_t, A_t, epsilon_{t+1})
O_{t+1} independent of E_t | X_t, do(A_t)
```

The assay tests whether persistent epistemic state can nevertheless change the distribution of observations encountered by changing action selection.

The mechanism under test is **endogenous evidence acquisition**. The protected property under test is **non-collapsible corrective exposure**.

## Scientific question

> Given a prospectively identified corrective channel, does persistent learning consume exposure to it, and does protecting quantitative or state-independent exposure alter correction latency under matched conditions?

The assay does not ask whether generic exploration is good.

## Fixed candidate challenge channel and oracle

The physical candidate channel is fixed prospectively:

```text
candidate challenge action = probe
```

For the primary `WORLD_CORRECTIVE` condition after the shift:

```text
D_t^oracle = D_t^Pi = {probe}
```

The organism is never told `D_t^oracle`, the world class, or the hidden regime.

`WORLD_NULL` and `WORLD_INFORMATIVE` are matched controls that apply the same arm machinery to the same physical candidate action even though its consequence class differs. They exist to prevent the assay from equating more probing, more information, and more correction.

## Organism

The organism is a small persistent tabular learner in the Blitzcrank family.

Each episode has:

1. a reveal action: `skip | probe`;
2. an observation: `UNKNOWN | SAME | SIG_A | SIG_B`;
3. a downstream decision: `safe | left | right`;
4. a scalar return;
5. sample-average updates to the chosen reveal and decision values.

Reveal values are keyed by visible context (`train`, `target`). Decision values are keyed by observation. Optimistic initialization is `1.10`. `probe` costs `0.20`.

There is no latent-state model, curiosity bonus, uncertainty bonus, change detector, foreclosure detector, corrective scheduler, Nano, or OpenCore component inside the learner.

## Environment and schedule

Per run:

```text
episodes:       420
shift episode:  180
seeds:          256
contexts:       train -> target -> train -> target -> ...
```

Thus every run contains 90 pre-shift target encounters and 120 post-shift target encounters.

For each seed, all arms receive the identical pre-generated hidden schedule. `train` regimes and post-shift discriminating target regimes are independent deterministic draws from the same seed-derived schedule.

### `train`

Throughout the run, hidden regime is `A` or `B` with probability 1/2 per train encounter.

```text
probe -> SIG_A or SIG_B
skip  -> UNKNOWN
```

When a signal is present, downstream rewards are:

```text
A: left=1.40, right=0.60, safe=1.00
B: left=0.60, right=1.40, safe=1.00
```

When `UNKNOWN` is present, all downstream actions pay `1.00`. Thus skipping does not itself reveal the hidden A/B distinction through reward.

`train` exists only to let ordinary experience teach the learner the downstream meaning of `SIG_A` and `SIG_B`.

### Pre-shift `target`

All three world classes are identical before the frozen shift:

```text
regime = N
probe -> SAME
skip  -> UNKNOWN
all downstream actions -> 1.00
```

Therefore probing is wasteful by exactly the `0.20` probe cost and persistent reveal learning can suppress it.

### `WORLD_NULL`

Post-shift target remains nondiscriminating:

```text
regime = N
probe -> SAME
all downstream actions -> 1.00
```

The candidate challenge is useless and costly.

### `WORLD_INFORMATIVE`

Post-shift target becomes hidden `A/B` and:

```text
probe -> SIG_A or SIG_B
skip  -> UNKNOWN
```

but all target downstream actions pay exactly `1.00` regardless of regime or action. The probe is therefore discriminating and representationally preserved, but action-irrelevant and net-costly.

### `WORLD_CORRECTIVE`

Post-shift target becomes hidden `A/B` with the same observation channel as `train`. With a signal, the A/B reward surface is active; with `UNKNOWN`, all downstream actions pay `1.00`.

Therefore a correctly used probe can yield:

```text
1.40 - 0.20 = 1.20
```

while continued skip yields `1.00` without exposing the hidden regime.

## Four frozen arms

All arms use the same learner. They differ only in post-shift `target` challenge selection.

### `ARM_ENDOGENOUS`

No intervention. Use the learner's exact greedy reveal policy.

### `ARM_SUPPORT`

If the learner's base greedy policy assigns zero probability to `probe`, retain nonzero but vanishing support:

```text
p_support(j) = 1 / (j + 2)^2
```

where `j` is the zero-based post-shift target encounter index.

This is deliberately not a uniform quantitative floor. `p_support(j) > 0` for every finite `j`, but `p_support(j) -> 0`.

### `ARM_FLOOR`

If the base policy would assign less than `epsilon` probability to `probe`, raise it to:

```text
epsilon = 0.05
```

Otherwise leave the base probability unchanged.

### `ARM_HAZARD`

At each post-shift target encounter, a deterministic seed/episode keyed hazard draw independent of learner state, world class, hidden regime, values, counts, observations, and confidence is evaluated.

```text
eta = 0.05
```

If the hazard fires, `probe` is forced. Otherwise the exact endogenous base policy acts.

This is the clean causal break of the state-to-challenge-timing path.

## RNG coupling

No mutable action-selection RNG is shared across branches.

Hidden schedules and policy draws are pure SHA-256 keyed functions. The same `(seed, episode, stage)` key produces the same variate across arms and worlds unless the frozen intervention semantics require a different stage key.

The hazard trigger key contains only `(seed, episode, "hazard")`; it cannot depend on agent state or world class.

## Correction gates

For every post-shift target challenge opportunity, record:

```text
C1   physical candidate action available
C2   candidate has positive effective policy probability
C3   candidate selected
C4a  selected candidate is environmentally discriminating
C4b  discrimination survives the observation representation
C5   signal is behaviorally recognized by a regime-consistent downstream choice
C6   corrective-world persistent reveal leverage revises so probe enters base greedy support
```

`C6` is an assay-local persistent-leverage revision proxy. It is not Nano authority and does not claim a formal authority mechanism exists inside Blitzcrank.

## Discriminating sets

Harness-side audit sets are:

```text
D_t^X  = physically discriminating actions for the live A/B distinction
D_t^Pi = those discriminators whose distinction survives the frozen observation representation
```

In this assay the representation preserves `SIG_A` versus `SIG_B`, so post-shift `WORLD_INFORMATIVE` and `WORLD_CORRECTIVE` satisfy:

```text
D_t^X = D_t^Pi = {probe}
```

while `WORLD_NULL` satisfies:

```text
D_t^X = D_t^Pi = {}
```

For the primary corrective world, `D_t^oracle = D_t^Pi`.

## Temporal quantities

Instantaneous effective challenge exposure is the effective probability assigned to the candidate probe at each post-shift target encounter.

The raw trace records realized challenge indicators. Empirical no-exposure survival is computed from paired trajectories rather than inferred from an independence approximation.

### `T_C`

`T_C` is the zero-based post-shift target encounter at which all of the following first hold on the realized trajectory:

1. `probe` was selected;
2. the observation was `SIG_A` or `SIG_B`;
3. the downstream decision was regime-consistent (`C5`);
4. after the resulting update, `probe` belongs to the learner's unprotected base greedy reveal support for `target` (`C6`).

If this never occurs within the 120-encounter post-shift target horizon, `T_C = null` and the censored analysis value is `121`.

### `T_L`

At every post-shift target encounter, the harness computes a one-step same-state forced-probe counterfactual without changing the endogenous trajectory.

`T_L` is the first zero-based encounter where:

```text
selected action != probe
and
forced_probe_return - realized_return >= 0.10
```

This is an assay-local consequential stale-leverage clock, not a universal harm metric.

## Primary contrast and stopping rule

Primary:

```text
(ARM_ENDOGENOUS, WORLD_CORRECTIVE)
vs
(ARM_HAZARD, WORLD_CORRECTIVE)
```

Define `T_C* = T_C` when finite, otherwise `121`.

The prospectively predicted direction is:

```text
mean(T_C*_ENDOGENOUS - T_C*_HAZARD) > 0
and
finite_rate_HAZARD - finite_rate_ENDOGENOUS > 0
```

For the frozen coarse equivalence decision, treat the primary arms as approximately equivalent only if both:

```text
abs(mean paired T_C* difference) < 5 target encounters
abs(finite correction-rate difference) < 0.05
```

If the arms are approximately equivalent and all validity/manipulation checks pass, the current endogenous-evidence-acquisition causal explanation loses authority.

A positive mechanistic classification requires separation in the predicted direction on both frozen margins:

```text
mean paired (T_C*_ENDOGENOUS - T_C*_HAZARD) >= 5
finite_rate_HAZARD - finite_rate_ENDOGENOUS >= 0.05
```

Anything between those regions is `UNDERDETERMINED`, not a positive result.

## Secondary contrast

Secondary:

```text
(ARM_SUPPORT, WORLD_CORRECTIVE)
vs
(ARM_FLOOR, WORLD_CORRECTIVE)
```

Use the same 5-encounter and 0.05 directional margins. A positive secondary result supports only the narrow statement that nonzero support is insufficient for timely exposure in this assay while a uniform quantitative floor performs differently.

## Control expectations

`WORLD_NULL` should show that protected/forced probing can impose cost when the candidate channel is nondiscriminating.

`WORLD_INFORMATIVE` should show that discriminating observations can be obtained and behaviorally recognized without producing corrective reward value in the target world.

These controls prevent interpreting `more probing` or `more information` as correction by definition.

## Raw trace

The harness must emit a deterministic canonical JSONL trace for every post-shift target opportunity across every seed, world, and arm, containing at least:

```text
E_t, Pi_t, pi_t, D_t^oracle,
C1, C2, C3, C4a, C4b, C5, C6,
A_t, O_{t+1}, W_{t+1}, E_{t+1}
```

plus audit regime, effective exposure probability, realized reward, same-state forced-probe counterfactual, and arm intervention fields.

The canonical uncompressed trace SHA-256 is a result artifact. The gzip carrier is deterministic with `mtime=0` but the uncompressed canonical hash is authoritative.

## Validity and manipulation checks

The assay is `INVALID` if any of the following fail:

1. arms within a seed/world do not receive identical hidden schedules;
2. the physical reveal action set differs across arms;
3. the organism or reward function differs across arms;
4. the shift depends on behavior;
5. hidden regime or world class is supplied to the learner or arm selector;
6. the hazard draw depends on persistent state or world class;
7. `ARM_SUPPORT` imposes a nonvanishing uniform floor rather than the frozen vanishing schedule;
8. `ARM_FLOOR` fails to guarantee the frozen `0.05` floor when base probe probability is lower;
9. instrumentation or counterfactual evaluation modifies the endogenous trajectory;
10. `WORLD_NULL` becomes discriminating;
11. `WORLD_INFORMATIVE` makes target action choice reward-relevant;
12. `WORLD_CORRECTIVE` fails to make the signal-conditioned premium action reward-relevant;
13. the observation representation aliases `SIG_A` and `SIG_B`;
14. fewer than 95% of `ARM_ENDOGENOUS` corrective-world seeds have `probe` excluded from base greedy support at the first post-shift target encounter;
15. evaluation constants are changed after results are observed without declaring a new assay version;
16. Nano or another OpenCore authority component is introduced into the organism.

## Claim ceiling

A positive result may support only:

> In this frozen learned adaptive system, persistent state endogenously reduced exposure to a prospectively identified corrective intervention, and a state-independent or quantitatively protected exposure intervention reduced correction latency under matched conditions.

It does not establish:

- a universal requirement for epsilon exploration;
- autonomous challenge discovery;
- `D_t^agent = D_t^oracle`;
- a universal corrigibility metric;
- a universal time constant;
- a new OpenCore architecture;
- a Nano change;
- production safety guarantees.

## Epistemic stopping rule

```text
failed prospective intervention prediction -> mechanism loses authority
successful matched intervention            -> mechanism gains bounded authority
```

No post-hoc schedule tuning or mechanism proliferation is permitted under the PCE-001 label.
