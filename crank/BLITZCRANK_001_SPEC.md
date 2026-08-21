# BLITZCRANK-001 — Persistent Memory Under a Nonstationary Interactive World

**Status before execution:** `FROZEN_PROSPECTIVE_ORGANISM_ASSAY`

## Purpose

Construct the smallest controllable long-horizon organism in which persistent memory is genuinely useful, then measure—without installing Nano or a corrective scheduler—whether persistence changes the organism's later access to an informative action.

This is **not FOREIGN-008** and not an OpenCore architecture change. Blitzcrank is an external organism under instrumentation.

## Manipulated variable

Only memory persistence changes:

- `memory_on`: one tabular learner persists learned action values across episodes;
- `memory_off`: the identical learner is reset to the same optimistic initialization at the start of every episode.

Environment schedule, seeds, action set, reward function, learning rule, tie-breaking algorithm, and instrumentation are identical.

## Organism

The agent is deliberately ordinary:

1. At a reveal step, choose greedily between `skip` and `probe` from learned context-specific returns.
2. `probe` costs `0.20` and yields an observation; `skip` yields `UNKNOWN`.
3. At a decision step, choose greedily among `safe`, `left`, and `right` from learned observation-conditioned rewards.
4. Update both chosen action values by sample-average return.

There is no explicit latent-state model, curiosity bonus, uncertainty estimator, exploration scheduler, foreclosure detector, corrective rule, or Nano.

Optimistic initial Q value for every unseen action is `1.10`. Exact ties are broken by the seeded RNG.

## Environment

There are three visible contexts:

- `train`
- `target`
- `null`

They cycle deterministically in that order. Each episode has one reveal step and one decision step.

### Hidden regimes

`train`:
- hidden regime is independently `A` or `B` with equal probability for the whole run.
- `probe -> SIG_A` in `A`, `probe -> SIG_B` in `B`.

`target` before the shift:
- hidden regime is `N`.
- `probe -> SAME`.

`target` after the shift:
- hidden regime is independently `A` or `B` with equal probability.
- `probe -> SIG_A` in `A`, `probe -> SIG_B` in `B`.

`null` for the whole run:
- hidden regime is `N`.
- `probe -> SAME`.

The shift is exogenous and independent of agent state.

### Decision rewards

For regime `A`:
- `left = 1.40`
- `right = 0.60`
- `safe = 1.00`

For regime `B`:
- `left = 0.60`
- `right = 1.40`
- `safe = 1.00`

For regime `N`:
- `left = 1.00`
- `right = 1.00`
- `safe = 1.00`

Thus:

- probing is potentially useful in `A/B` because `probe + correct premium = 1.20 > safe = 1.00`;
- probing is wasteful in `N` because it only subtracts cost from an otherwise identical `1.00` decision surface;
- `safe` remains exactly `1.00` before and after the target shift, so continuing to choose `safe` does not itself reveal that the target context became discriminating.

## Shared signal semantics

Decision Q-values are keyed by observation (`SIG_A`, `SIG_B`, `SAME`, `UNKNOWN`) rather than visible context. This lets persistent experience in `train` transfer the meaning of `SIG_A` / `SIG_B` to `target` without encoding hidden regime identity in the policy.

Reveal Q-values are context-specific. Therefore the agent can separately learn whether probing tends to pay in `train`, `target`, and `null`.

## Horizon and seeds

Per run:
- `300` episodes;
- deterministic context cycle `train -> target -> null`;
- target shift at episode index `180` (zero-based; after 60 complete context cycles);
- `256` paired seeds;
- the same pre-generated environment schedule is used for memory-on and memory-off within each seed.

## Instrumentation

For every reveal decision, record:

- `L_t`: current persistent Q-table summary and visit counts;
- `Pi_t`: effective reveal abstraction for the current context: `PROBE_PREFERRED`, `SKIP_PREFERRED`, or `TIED`, determined only from the current two reveal Q-values;
- `pi_t`: exact greedy policy support (all actions tied for maximal Q) plus selected action;
- `R_available`: physically available reveal actions `{skip, probe}`;
- `a_t`: selected action;
- `E_{t+1}`: resulting reveal observation and later decision reward;
- hidden regime only in harness-side audit fields, never exposed to the agent.

## Primary measurements — orthogonal axes

No foreclosure classification is built into the learner. The harness reports two independent empirical axes.

### Axis A — persistent performance effect

Compare paired cumulative return:

`memory_on - memory_off`

for:
- whole run;
- pre-shift segment;
- post-shift segment.

Report mean, median, seed win-rate, and exact paired differences.

### Axis B — informative-action reachability

In post-shift `target` episodes, measure:

- fraction where `probe` is physically available;
- fraction where `probe` belongs to exact greedy policy support;
- fraction where `probe` is selected;
- first episode, if any, in which `probe` is absent from greedy support.

The same measurements are recorded for `null`.

## Conditional forced-action control

The forced-action control is **not** run unless the endogenous trajectory supplies the trigger.

Target trigger:
- post-shift `target` episode;
- `probe in R_available`;
- `probe not in pi_t.support` for `memory_on`.

If such an episode exists, clone the exact pre-reveal agent state and environment state, externally force `probe`, then allow the same unchanged decision policy to act on the resulting observation.

Record:
- forced observation;
- endogenous return;
- forced return;
- whether forced probing changes the effective observation class;
- whether forced probing changes the chosen decision action;
- whether forced return exceeds endogenous return.

Null trigger/control:
- apply the same procedure to the first post-shift `null` episode satisfying `probe not in pi_t.support`.

A useful target forced probe and a useless null forced probe are analytically distinct outcomes.

## Validity requirements

The run is `INVALID` if any of the following fail:

1. memory-on/off differ in anything other than cross-episode retention;
2. paired branches receive different environment schedules;
3. physical action availability differs between paired branches;
4. the target shift depends on agent behavior;
5. agent receives hidden regime identity directly;
6. forced control does not clone the exact pre-action state;
7. null context becomes discriminating;
8. target pre-shift context is discriminating;
9. instrumentation alters policy or reward;
10. code/spec bytes change after the first execution without preserving the original run.

## Interpretation discipline

Possible observations include, without privileging one prospectively:

- persistent memory improves performance and retains probe reachability;
- persistent memory improves performance while reducing probe reachability;
- persistent memory does not improve performance;
- memory-off reaches the probe less often;
- both policies retain the probe;
- no forced-action trigger occurs;
- a forced target probe helps, does nothing, or hurts;
- the null forced probe is harmless or reveals a design error.

No observation automatically earns a new OpenCore primitive, scheduler, memory architecture, Nano change, or universal corrigibility law.
