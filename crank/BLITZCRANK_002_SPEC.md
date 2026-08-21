# BLITZCRANK-002 — Regime-Change Adaptation of Policy Support

**Status before execution:** `FROZEN_PROSPECTIVE_ORGANISM_ASSAY`

## Purpose

Measure whether the same simple persistent-memory organism from BLITZCRANK-001 can restore policy support for a previously suppressed probe after ordinary reward consequence indicates that the old action-value regime has changed.

This is **not FOREIGN-008**, not an OpenCore architecture change, and contains no Nano. Blitzcrank remains an external organism under instrumentation.

The assay does not add curiosity, an uncertainty bonus, a regime-change detector, a foreclosure detector, or a corrective scheduler.

## Scientific question

> When persistent memory has learned that an action is usually not worth taking, how quickly can ordinary consequence make that action policy-reachable again after the reward regime changes?

The primary quantity is:

```text
tau_reopen = number of post-shift target encounters before `probe`
             first returns to exact greedy reveal-policy support
```

This is a policy-support recovery measurement, not a theorem about corrigibility.

## Organism

The learning rule is unchanged in substance from BLITZCRANK-001:

1. choose greedily between `skip` and `probe` from context-keyed reveal return estimates;
2. `probe` costs `0.20` and yields `SIG_A`, `SIG_B`, or `SAME`;
3. `skip` yields `UNKNOWN`;
4. choose greedily among `safe`, `left`, and `right` using observation-keyed decision values;
5. update chosen reveal and decision values by sample-average return.

Optimistic initialization is `1.10` for unseen actions. Exact ties are broken by a deterministic seeded tie-break function.

No hidden regime identity is supplied to the learner.

## Three conditions

All conditions receive the same pre-generated hidden-world schedule and reward function.

### 1. `persistent_ordinary`

One learner persists all Q-values across the entire run.

The visible reveal context remains `target` before and after the shift. No explicit shift signal is supplied.

### 2. `persistent_signaled`

The same persistent learner is used, but the environment exposes a generic visible context-key change from `target` to `target_shifted` at the exogenous shift.

This tells the learner only that the visible context identity changed. It does **not** reveal hidden regime, reward values, probe value, or which action should be selected.

Decision-value memory remains shared and persistent. Only the reveal-state key is new.

This is an attribution / upper-bound control for policy-support recovery when context change is externally observable. It is not a learned change detector.

### 3. `reset`

The identical learner is reset to optimistic initialization at the start of every episode, as in BLITZCRANK-001 memory-OFF.

## Environment

Visible base contexts cycle deterministically:

```text
train -> target -> null
```

Each episode contains one reveal decision and one downstream decision.

### Hidden regimes

`train`, all run:
- regime independently `A` or `B` with probability 1/2 per train episode;
- `probe -> SIG_A` or `SIG_B`.

`target`, before shift:
- regime `N`;
- `probe -> SAME`.

`target`, after shift:
- regime independently `A` or `B` with probability 1/2 per target episode;
- `probe -> SIG_A` or `SIG_B`.

`null`, all run:
- regime `N`;
- `probe -> SAME`.

The target shift is exogenous and independent of agent behavior.

### Decision rewards

For `A`:

```text
left  = 1.40
right = 0.60
safe  = 1.00
```

For `B`:

```text
left  = 0.60
right = 1.40
safe  = 1.00
```

For `N`:

```text
left = right = safe = 1.00
```

### Reveal costs

`probe` always costs `0.20`.

`skip` costs `0` everywhere except post-shift `target`, where it incurs an additional ordinary reward penalty of `0.35`.

Thus before the target shift:

```text
skip in target  -> 1.00 under the nondiscriminating N surface
probe in target -> 0.80 under the nondiscriminating N surface
```

After the target shift, continuing the old skip policy produces a lower ordinary return even though the hidden regime remains unobserved:

```text
skip -> UNKNOWN -> downstream reward - 0.35
```

The penalty is not a regime label and does not identify `A` versus `B`. It supplies only ordinary consequence that the old skip valuation is no longer fully valid.

A well-used probe can exploit signal semantics learned in `train`:

```text
probe -> SIG_A/SIG_B -> appropriate downstream action
```

The `null` context never shifts and receives no skip penalty, preserving a stationary case where probing remains wasteful.

## Horizon and pairing

Per seed:

```text
episodes:      900
shift episode: 180
seeds:         256
```

Contexts continue to cycle every three episodes, yielding 60 pre-shift and 240 post-shift target encounters.

The same hidden-world schedule is supplied to all three conditions for each seed.

Tie-breaking is a pure deterministic function of `(seed, episode, stage, support)` so branch divergence cannot create an RNG-state confound.

## Instrumentation

For each reveal decision record:

- `L_t`: current relevant Q-values and counts;
- `Pi_t`: `PROBE_PREFERRED`, `SKIP_PREFERRED`, or `TIED`;
- `pi_t`: exact greedy policy support and selected action;
- `R_available = {skip, probe}`;
- `a_t`: selected action;
- `E_{t+1}`: reveal observation;
- downstream action, reward, costs, and total return;
- hidden regime only in harness-side audit fields.

## Primary measurements

### Axis A — capability compounding

Compare paired cumulative return for:

```text
persistent_ordinary - reset
persistent_signaled - reset
persistent_signaled - persistent_ordinary
```

for total, pre-shift, and post-shift segments.

### Axis B — policy-support reopening

For post-shift target encounters, measure for each condition:

- `tau_reopen_support`: first target-encounter index (0-based) where `probe` belongs to exact greedy support;
- `tau_reopen_selected`: first target-encounter index where `probe` is selected;
- fraction of target encounters with probe in support;
- fraction with probe selected;
- whether reopening occurs within the frozen horizon.

For `persistent_ordinary`, `tau_reopen_support` is the primary quantity.

### Axis C — counterfactual value while suppressed

For every post-shift target encounter in `persistent_ordinary` where:

```text
probe in R_available
probe not in pi_t.support
```

clone the exact pre-reveal agent state and externally force `probe` for one episode without altering the endogenous trajectory.

Record:

- forced observation;
- endogenous one-step return;
- forced one-step return under the same stored downstream policy;
- one-step return delta;
- whether the forced probe changes observation and downstream action.

These are per-state one-step counterfactuals. They are **not** summed as a claim about the return of a counterfactual learning trajectory.

Apply the same forced procedure to excluded `probe` actions in stationary `null` as a matched wastefulness control.

## Descriptive outcome classes

These labels describe measurements only; they do not award an OpenCore mechanism.

### `POLICY_SUPPORT_REOPENING_OBSERVED`

`persistent_ordinary` excludes `probe` immediately after shift but `probe` later returns to greedy support within the frozen horizon.

### `PERSISTENT_SUPPRESSION_WITHIN_HORIZON`

`persistent_ordinary` excludes `probe` immediately after shift and it never returns to greedy support within the frozen horizon.

### `NO_INITIAL_SUPPRESSION`

`probe` remains in support at the first post-shift target encounter.

### `INVALID`

Any validity requirement fails.

## Validity requirements

The run is `INVALID` if any of the following fail:

1. all three conditions do not receive identical hidden-world schedules;
2. physically available actions differ between conditions;
3. reward functions differ between conditions;
4. the target shift depends on behavior;
5. hidden regime identity is supplied directly to the learner;
6. `persistent_ordinary` receives an explicit shift marker;
7. `persistent_signaled` receives more than the generic context-key change;
8. `reset` retains values across episodes;
9. forced controls do not clone exact pre-action state;
10. forced controls modify endogenous trajectories;
11. null becomes discriminating or receives the target skip penalty;
12. instrumentation changes policy or reward;
13. Nano or any OpenCore component is present inside the organism.

## Interpretation discipline

A result may show fast reopening, slow reopening, no reopening, or no initial suppression.

Even a clean reopening result does **not** establish:

- a universal reopening time constant;
- that reward surprise is the correct repair mechanism;
- that explicit shift signals are generally desirable;
- that curiosity should be added;
- that every informative action should remain policy-reachable;
- an exploration or reachability primitive;
- a memory architecture for OpenCore;
- a Nano change;
- a universal corrigibility law.

The intended scientific pressure is narrower:

> persistent action-value memory can be useful, can suppress actions, and can be tested for how quickly ordinary consequence restores support after the reasons for suppression change.
