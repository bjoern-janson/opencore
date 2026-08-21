# BLITZCRANK-001 — Persistent Memory Under a Nonstationary Interactive World

**Organism:** Blitzcrank  
**Status:** completed controlled external-organism assay  
**OpenCore components inside organism:** none  
**Nano:** absent  
**FOREIGN-008:** not declared

## Scientific question

Can persistent memory measurably improve long-horizon performance while also changing the set of informative actions retained in the organism's endogenous greedy policy support?

Blitzcrank was intentionally not given a foreclosure detector, curiosity module, uncertainty-to-probe rule, or corrective scheduler. It is a small tabular return learner interacting with a nonstationary world.

## Prospective freeze

Specification SHA-256 before first execution:

```text
a3cf6dd0fe90fc844caff6dbe4ca90e774722ea0929ad575b126333961ef7dad
```

Original V1 harness SHA-256:

```text
b687e6bc22c5a7bc34b6768273e0ef166a0bd2bacd65572599d2a5fddc6c29c1
```

## V1 validity failure

The first execution was classified `INVALID` on audit.

The environment schedule was correctly paired, but V1 initialized the agent tie-break RNG differently in the two memory conditions:

```python
Agent(seed ^ (0x1111 if memory_on else 0x2222))
```

That violated the prospectively frozen requirement that cross-episode memory retention be the only manipulated variable.

V1 artifacts are preserved. No V1 numerical result is used as scientific evidence.

V1 result SHA-256:

```text
8666ec116df33f73e9f60fb1874183b167d17d1ce398b41f98fc6d81f5912ab0
```

V1 log SHA-256:

```text
9bb37aa61e8b3e5d0485589ec77193c597e9d4d02ebec57c5d05afff5c939185
```

## V2 validity repair

V2 changes exactly one line:

```diff
- agent = Agent(seed ^ (0x1111 if memory_on else 0x2222))
+ agent = Agent(seed ^ 0x1111)
```

No environment, reward, action, horizon, shift, learner, policy, instrumentation, forced-control rule, or seed count changed.

V2 harness SHA-256:

```text
dc39f1cb77ae7832551525eecd643b3adbca47736590eba3a73fbe934fa74337
```

## Frozen organism and world

The exact same learner is run in two conditions:

```text
memory_on  -> learned Q-values persist across episodes
memory_off -> learned Q-values reset each episode
```

Everything else is paired.

Each episode has:

```text
reveal action:   skip | probe
decision action: safe | left | right
```

The agent greedily selects from learned returns with optimistic initialization and seeded tie-breaking.

Three visible contexts cycle:

```text
train -> target -> null
```

`train` is always an A/B world in which probing can reveal `SIG_A` or `SIG_B` and support a premium action.

`target` begins as a null world in which probing returns `SAME` and only wastes its cost. At the prospectively frozen exogenous shift, `target` becomes A/B and the same physical probe becomes informative.

`null` remains nondiscriminating throughout.

Critically, the ordinary `safe` action pays exactly `1.00` before and after the target shift. Therefore an organism that has learned to skip the target probe can continue receiving its expected safe reward without the cheap action itself revealing the new hidden distinction.

## Exact V2 run

```text
paired seeds:   256
episodes/seed:  300
shift episode:  180
probe cost:     0.20
```

All frozen validity requirements passed after the RNG repair.

## Axis A — persistent performance effect

Mean cumulative return:

```text
memory_on:   305.40390625
memory_off:  270.33125000
Delta:       +35.07265625
```

Pre-shift:

```text
memory_on - memory_off = +20.71640625
```

Post-shift:

```text
memory_on - memory_off = +14.35625000
```

Paired total-return win rate:

```text
256 / 256 = 100%
```

Thus persistent memory is genuinely useful in this organism over the frozen long horizon.

This is important because the later reachability effect is not being produced by an organism that is simply worse overall.

## Axis B — informative-action policy reachability

In every post-shift `target` episode, `probe` remains physically available in both memory conditions.

Mean fraction of post-shift target episodes in which `probe` belongs to exact greedy policy support:

```text
memory_on:   0.0000
memory_off:  1.0000
```

Mean fraction actually selecting `probe`:

```text
memory_on:   0.000000
memory_off:  0.497852
```

Every memory-on seed therefore supplies the prospective forced-control trigger:

```text
probe in R_available
probe not in pi_t.support
```

The first such target trigger occurs at episode `181` in all 256 seeds.

The same contraction occurs in the null context:

```text
memory_on null probe support:  0.0000
memory_off null probe support: 1.0000
```

This shows that memory learned an efficiency policy: probing had been wasteful in target/null and was removed from greedy support.

## Conditional forced target control

For each memory-on target trigger, the exact pre-reveal agent and RNG state was cloned. The excluded physically available `probe` was externally forced, after which the same unchanged downstream decision policy acted on the observation.

In all 256 seeds:

```text
forced probe changed UNKNOWN -> SIG_A or SIG_B
```

So the excluded action was genuinely informative after the shift.

However, informational value did not imply universal immediate utility.

Forced target return delta distribution:

```text
+0.60 :  30 seeds
+0.20 : 117 seeds
-0.20 :  76 seeds
-0.60 :  31 seeds
-1.00 :   2 seeds
```

Therefore:

```text
forced target probe improves return: 147 / 256 = 57.421875%
forced target probe harms return:    109 / 256 = 42.578125%
mean forced target delta:            +0.021875
```

This is a useful boundary result.

Persistent memory removed an informative action from policy support in every seed, but only a subset of those exclusions were already actionable corrective losses under the organism's same stored downstream policy.

The assay therefore does **not** justify equating:

```text
informative path excluded
=
corrective path lost
```

without the forced-action consequence test.

## Null forced control

The same forced procedure was applied to the first memory-on `null` trigger in every seed.

The null probe always produced `SAME` and never improved return:

```text
forced null delta:  -0.20 in 256 / 256 seeds
positive rate:       0 / 256
```

Thus the assay rejects the rule:

```text
keep every physically available probe in policy support
```

The learned support contraction is useful in the null world and sometimes costly in the shifted target world.

## What Blitzcrank earned

On this frozen constructed organism/environment family:

1. Persistent memory produced a large, reproducible long-horizon performance benefit.
2. The same persistent learning eliminated a physically available probe from greedy policy support in a context where the probe later became informative.
3. In 147/256 paired trajectories, externally restoring that excluded probe improved immediate return under the exact same stored agent state and downstream policy.
4. In the matched null context, restoring the excluded probe was uniformly wasteful.

The strongest scoped statement is therefore:

> **Useful persistent capability and contraction of informative-action policy support can coexist. In a substantial subset of otherwise higher-performing persistent-memory trajectories, the contracted action was a physically available, immediately beneficial corrective path when restored; in the matched null world, preserving the same path would only waste reward.**

This is the first controlled organism result in the program where:

```text
memory benefit
and
corrective-path contraction
```

are measured in the same agent rather than stipulated as separate assay branches.

## What Blitzcrank did not earn

BLITZCRANK-001 does **not** establish:

- a universal epistemic-foreclosure law;
- that persistent memory generally reduces corrigibility;
- that every informative action is corrective;
- that a 57.4% forced-benefit rate is a general constant;
- that memory-off is a desirable architecture;
- that all exploration should remain live;
- an exploration or curiosity module;
- a reachability primitive;
- automatic challenge discovery;
- an OpenCore memory architecture;
- a Nano change;
- FOREIGN-008;
- a result about AVO, ARC-AGI-3, or any external deployed agent.

## Current interpretation

The frozen systems hypothesis survives a first controlled-organism attack, but in a more discriminating form:

```text
positive compounding
!=
corrigible compounding
```

and also:

```text
informative-action reachability
!=
corrective-action value
```

The correct causal question remains consequence-based:

```text
persistent state
-> policy support
-> available/selected intervention
-> observation
-> downstream consequence
```

Blitzcrank supplies a controllable bridge between the FOREIGN-007 constructed topology and future real-agent specimens, without importing Nano or declaring a new OpenCore architecture.
