# BLITZCRANK-002 — Regime-Change Adaptation of Policy Support

**Canonical descriptive outcome:** `POLICY_SUPPORT_REOPENING_OBSERVED` in `256 / 256` paired seeds

**Organism status:** external controllable organism; **not FOREIGN-008**; **no Nano**; **no OpenCore architecture change**.

## Scientific question

When persistent memory has learned that an action is usually not worth taking, how quickly can ordinary consequence make that action policy-reachable again after the reasons for suppression change?

The prospectively frozen primary quantity was:

```text
tau_reopen = number of post-shift target encounters before `probe`
             first returns to exact greedy reveal-policy support
```

## Prospective freeze

```text
BLITZCRANK_002_SPEC.md
SHA-256 e3f9c5473b4af0ae261d6f7115ce7dae4a6f0558d88d5be449e7e572ff473513

blitzcrank_002.py (V1 frozen apparatus)
SHA-256 0139574a3f72b2b0c556f4dd5851e87ee7fbda70cde575b4e3af0702e93533a4
```

The first V1 execution exceeded the runtime ceiling before producing any result file. `run.log` remained empty. This was classified as execution/apparatus pressure only.

V2 changed execution mechanics only: full state snapshots are created only when a forced counterfactual is actually eligible, metrics are accumulated online, and only one exemplar trace is retained.

```text
blitzcrank_002_v2.py
SHA-256 5807ed5d4a087b7fb3c64c8a5a4a550fd26f9d31d66afe2350a583eda78bdd6a
```

A post-freeze seed-0 audit found V1 and V2 episode-for-episode identical across all three 900-episode conditions and identical on all 239 target and 240 null forced controls for that seed.

## Organism

The learner is deliberately ordinary:

```text
context-keyed reveal Q values:  skip / probe
observation-keyed decision Qs:  safe / left / right
sample-average updates
optimistic unseen value = 1.10
exact greedy support
pure deterministic seeded tie breaking
```

There is no curiosity bonus, uncertainty model, change detector, exploration scheduler, corrective rule, foreclosure detector, world model, Nano, or OpenCore component.

## Three conditions

```text
persistent_ordinary
    all learned values persist;
    visible target key remains `target` across the shift.

persistent_signaled
    all learned values persist;
    after the exogenous shift only the reveal context key becomes
    `target_shifted`; no regime or action-value information is supplied.

reset
    identical learner resets to optimistic initialization every episode.
```

All three receive the exact same pre-generated hidden-world schedule and reward function for each paired seed.

## World

Contexts cycle:

```text
train -> target -> null
```

`train` teaches reusable `SIG_A` / `SIG_B` semantics.

Before the target shift, target is nondiscriminating:

```text
regime N
skip  -> UNKNOWN -> return 1.00
probe -> SAME    -> return 0.80
```

Thus persistent memory correctly learns to suppress probing in target.

At episode 180, target changes exogenously to hidden `A/B`. The ordinary skip path remains physically available but now incurs a `0.35` reward penalty:

```text
skip -> UNKNOWN -> ordinary downstream consequence - 0.35
```

This is a non-diagnostic surprise: it says the old skip valuation is no longer fully valid, but it does not reveal `A` versus `B` or tell the learner to probe.

The probe remains cost `0.20` and now exposes:

```text
SIG_A or SIG_B
```

which can exploit signal-action knowledge acquired in `train`.

`null` never changes and retains:

```text
skip  -> 1.00
probe -> 0.80
```

so continued probe suppression remains correct there.

## Exact run

```text
seeds:          256
episodes/seed:  900
shift episode:  180
post-shift target encounters/seed: 240
```

All frozen validity conditions passed the post-run structural audit.

## Result 1 — persistent capability still wins

Persistent ordinary memory beat the reset learner on **every paired seed**:

```text
memory win rate, whole run: 256 / 256
memory win rate, post shift: 256 / 256
```

Paired return advantage:

```text
persistent_ordinary - reset

whole run:
  mean    +141.4306640625
  median  +139.475
  min      +20.35
  max     +220.00

post shift:
  mean    +119.8634765625
  median  +122.125
  min       +6.55
  max     +186.40
```

So the organism is not being punished for persistence in order to manufacture a reopening effect. Persistent capability remains strongly advantageous even after the regime change.

## Result 2 — ordinary consequence reopens support, but slowly

Immediately after the shift:

```text
probe in persistent_ordinary greedy support: 0 / 256 seeds
```

Yet ordinary reward consequence eventually restored `probe` to exact greedy support in:

```text
256 / 256 seeds
```

The prospectively declared first-reopening time was:

```text
tau_reopen_support, target encounters after shift

mean:    80.52734375
median:  79
min:     47
max:    215
```

Because target appears every three episodes, mean first reopening occurs roughly:

```text
3 * 80.52734375 + 1 = 242.58203125 global episodes after the shift
```

So an old, genuinely useful memory policy can remain closed to a newly valuable action for hundreds of ordinary interaction steps even while accumulating reward feedback that the old valuation has changed.

## Result 3 — an external context-change signal makes first reopening immediate

For both `persistent_signaled` and `reset`:

```text
tau_reopen_support = 0 target encounters
```

in all 256 seeds because the first post-shift target state has a fresh reveal-action support surface.

The signaled persistent condition also outperformed reset on every total-run seed:

```text
persistent_signaled - reset, whole-run mean = +178.88203125
```

and improved post-shift return over ordinary persistence on average:

```text
persistent_signaled - persistent_ordinary, post-shift mean = +37.4513671875
```

but this was **not universal**:

```text
signaled better than ordinary post-shift: 215 / 256 seeds
exactly tied:                              11 / 256
signaled worse:                            30 / 256
```

Therefore the result does not license “reset on change” or “always expose a shift marker” as a repair.

## Result 4 — first reopening is not sustained reopening

This was not the primary prospective endpoint, but it is visible directly in the frozen per-seed support fractions.

For `persistent_ordinary` over the full post-shift target horizon:

```text
mean probe-support fraction:   0.5440104167
median probe-support fraction: 0.6708333333
min:                           0.0041666667
max:                           0.8041666667
```

Despite `256 / 256` seeds registering a first reopening, **45 / 256** seeds kept `probe` in support for at most 1% of post-shift target encounters.

Thus:

```text
first reopening
!=
sustained corrective reachability
```

The prospectively useful `tau_reopen` metric is therefore insufficient by itself. A support path can reopen transiently and then close again.

This is a post-run secondary interpretation, not a new prospectively validated metric.

## Result 5 — suppressed target probes were often, but not always, immediately valuable

Across every post-shift target state in `persistent_ordinary` where `probe` was physically available but absent from greedy support, exact state-clone forced controls produced:

```text
excluded target states:          28,016
forced observation changed:      100%
forced one-step return positive: 24,140 / 28,016 = 86.1650485%
mean one-step return delta:       +0.3563392347
median one-step delta:            +0.55
min:                              -0.65
max:                              +0.95
```

So the suppressed action was very often genuinely beneficial under the organism's already stored downstream policy—but not always.

This preserves the BLITZCRANK-001 distinction:

```text
informative action
!=
corrective / reward-improving action
```

## Result 6 — matched null says not to preserve every probe

In stationary `null`, the same persistent organism correctly suppresses `probe`.

Forced controls across every excluded post-shift null state gave:

```text
excluded null states:       61,440
positive forced rate:       0 / 61,440
mean forced delta:          -0.20
min = median = max:         -0.20
```

The observation changes from `UNKNOWN` to `SAME`, but the new information has no decision value and only incurs probe cost.

Therefore:

```text
information acquisition alone
!=
reason to preserve policy support
```

## What BLITZCRANK-002 earns

On this frozen deterministic organism family:

> A persistent-memory learner that substantially outperformed an otherwise identical reset learner initially excluded a later-valuable probe from exact greedy policy support. After an exogenous reward-regime change, ordinary non-diagnostic consequence eventually restored that probe to support in all 256 seeds, but first reopening was delayed by a median of 79 target encounters and was not necessarily sustained. While the probe was suppressed, forcing it was immediately reward-improving in 86.2% of the tested target states, whereas forcing the matched stationary-null probe was uniformly harmful.

This strengthens the empirical tension:

```text
capability compounding
+
policy-support contraction
+
finite / sometimes transient reopening under changed consequence
```

## What it does not earn

BLITZCRANK-002 does **not** establish:

- a universal reopening time constant;
- that every persistent learner will reopen under reward surprise;
- that first reopening is sufficient corrigibility;
- a general definition of sustained corrective topology;
- that context-change signaling is the correct repair;
- that memory should be reset on detected change;
- that curiosity or exploration bonuses are needed;
- that every informative action should remain supported;
- a new OpenCore primitive;
- a Nano change;
- FOREIGN-008;
- a universal law of bounded epistemic compounding.

## New pressure exposed

The strongest unexpected boundary is:

```text
reopening event
!=
reopening persistence
```

The next question, if independently earned, is no longer merely “how fast does a path reopen?” but whether a path that reappears remains available long enough to affect subsequent learning and authority.

No repair is proposed here.
