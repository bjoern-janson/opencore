# OpenCore FOREIGN-002 — Restless-Bandit Attention Pressure

**Status:** `CONSTRUCTED_FOREIGN_PRESSURE_RESULT`  
**Foreign task family:** restless multi-armed bandit / changing-environment bandit  
**Mini modified:** `NO`  
**Nano modified:** `NO`  
**Base extended:** `NO`  
**Publication:** experimental crank branch

## 1. Why this task

FOREIGN-001 hit frozen Mini's hypothesis topology before scarce-attention behavior could be tested. FOREIGN-002 therefore changes the pressure source again while controlling that already-known wound.

The foreign task family is the restless multi-armed bandit (RMAB): only a limited subset of arms can be played/observed at each time, while unselected arms continue evolving. RMABs are a standard sequential resource-allocation family used for changing environments, monitoring, scheduling, and related problems.

This assay uses a deliberately small deterministic finite RMAB instance:

```text
8 arms
80 scored rounds
1 observable/playable arm per round
all arms evolve independently while passive
per-arm hidden shift hazard = 0.05 per round
```

The key control is that every latent arm state is exactly one of frozen Mini's existing affine `Z_11` rules. Thus the current arm relation is always representable by Mini if the needed observations are actually acquired.

The experiment asks where corrective flow stops when:

```text
representation is available
+
Nano persistence authority is available
+
observation attention is scarce.
```

## 2. Foreign-task lineage

The task family is external to OpenCore. Relevant precedents include:

- Liu, Liu, and Zhao, *Learning in A Changing World: Restless Multi-Armed Bandit with Unknown Dynamics* (2010): unselected arms continue evolving under unknown dynamics while only a limited subset is played.
- Slivkins and Upfal, *Adapting to a Changing Environment: the Brownian Restless Bandits* (COLT 2008): changing arm rewards and exploration/exploitation under nonstationarity.
- Wang, Huang, and Lui, *Restless-UCB* (NeurIPS 2020): online learning in restless bandits with evolving arm state.

FOREIGN-002 does **not** claim to reproduce those papers' stochastic models or algorithms. It borrows the foreign failure geometry: partial observation + evolving unobserved alternatives + finite attention.

## 3. Construction

### 3.1 Latent arm state

Each arm `i` has a current hidden reward rule:

```text
y = a*x + c mod 11
```

with nonzero `a`, exactly frozen Mini's hypothesis class.

Operational round `t` uses:

```text
x = t mod 11
```

and pulling arm `i` returns its current `y`.

Reward is the integer `y in {0,...,10}`. The task objective is cumulative reward over 80 rounds.

### 3.2 Restless evolution

Before each scored round, every arm independently shifts with probability `0.05`.

A shift replaces its latent affine rule with a different random rule from the same frozen Mini hypothesis family.

Evolution is generated ex ante from the seed and is **policy-independent**. Therefore every compared policy receives the same hidden world trajectory for a given seed.

### 3.3 Common bootstrap

Before the scored horizon, every policy receives two distinct real observations per arm under the initial state.

Frozen Mini therefore begins with an exact active model for all eight arms.

Each initial Mini commitment is persisted through unchanged Nano under an externally supplied foreign-reward license.

This bootstrap exists to remove initial acquisition and FOREIGN-001's representational mismatch from the pressure surface. It is not counted in reward.

### 3.4 Base-facing world

For each arm, the current Nano-effective Mini model is the shared task-facing prediction surface.

No Base-001 12-unit relevance scaffold is added. `Base` here has only the same minimal role as FOREIGN-001:

```text
Nano-effective standing -> current shared model used by the task adapter
```

### 3.5 Scarce attention

Only one arm can be pulled per scored round.

A pull simultaneously:

```text
produces reward
+
provides one real observation to Mini.
```

All other arms continue evolving unobserved.

Thus:

```text
available reality contact per round = 1 arm
latent processes per round          = 8 arms
```

Exhaustive current-state observation is impossible.

## 4. Compared policies

These are harness controls. They are **not** new OpenCore components.

### `greedy`

Choose the arm with maximum current Base-predicted immediate reward.

```text
argmax_i  P_i(x_t)
```

This is the short-term score baseline.

### `mini_reactive`

Use frozen Mini's existing behavior only:

```text
if any scope has needs_probe:
    service the oldest pending Mini probe request
else:
    greedy
```

Mini itself supplies only the binary `needs_probe(scope)` state. The oldest-request tie break is deterministic harness transport, not a learned priority rule.

This is the key specimen: it tests whether Mini's existing challenge behavior becomes useful effort allocation under foreign resource pressure.

### `epsilon`

Classic exploration control:

```text
10% random arm
90% greedy arm
```

This is external exploration, not Mini behavior.

### `round_robin`

Uniform coverage control:

```text
arm = t mod 8
```

This deliberately buys broad observation coverage at potentially large reward cost.

### Oracle

The result bundle computes the true best reward each round as a reward ceiling. No oracle policy is fed to Mini or Nano.

## 5. Consequential hidden shifts

No arm is pre-labeled `easy`, `hard`, `rare`, or `important`.

A hidden shift is classified *after world construction* as **severe** if the shifted arm is oracle-best for at least eight rounds before that arm's next hidden shift or horizon end:

```text
best_rounds >= 8
```

Eight rounds is one full round-robin coverage cycle.

This produces rare consequential events without assigning semantic importance to any arm in advance.

Across 10,000 worlds:

```text
total hidden shifts        = 320,222
severe hidden shifts       = 20,440
severe fraction            = 6.3831%
mean shifts / world        = 32.0222
```

## 6. Final 10,000-world result

### 6.1 Reward / state-tracking summary

| Policy | Mean reward | Mean regret | True-best pull rate | Mean fresh arms at end |
|---|---:|---:|---:|---:|
| Greedy | **546.1941** | 191.6175 | 45.9502% | 1.9907 / 8 |
| Mini reactive | **563.8217** | **173.9899** | **51.9986%** | **4.5601 / 8** |
| Epsilon | 536.1406 | 201.6710 | 44.2304% | 2.3272 / 8 |
| Round robin | 399.8980 | 337.9136 | 17.4602% | 3.8398 / 8 |

Relative to greedy, `mini_reactive`:

```text
mean reward       +3.2274%
mean regret       -9.1994%
```

So honoring Mini's existing probe requests is not merely epistemically tidy; on this foreign constructed family it improves task reward.

### 6.2 First contact vs repair

| Policy | Detect any hidden shift | Detect severe shift | Detected -> repaired | Severe shift repaired |
|---|---:|---:|---:|---:|
| Greedy | 67.4429% | 94.2759% | 35.8337% | 57.9892% |
| Mini reactive | **58.5075%** | **91.1986%** | **91.0987%** | **90.3571%** |
| Epsilon | 67.5978% | 96.1497% | 40.5266% | 68.0969% |
| Round robin | **77.6721%** | **99.5939%** | 52.8833% | **96.6243%** |

This is the decisive separation.

`mini_reactive` is dramatically better at **finishing a correction after a contradiction has already been observed**:

```text
35.8337% -> 91.0987% detected-to-repaired
```

but it is *worse* than greedy and epsilon at obtaining first corrective contact with distinct hidden shifts:

```text
Mini reactive shift detection = 58.5075%
Greedy shift detection        = 67.4429%
Epsilon shift detection       = 67.5978%
Round-robin detection         = 77.6721%
```

The same pattern persists on the rare severe subset:

```text
Mini reactive severe detection = 91.1986%
Greedy severe detection        = 94.2759%
Epsilon severe detection       = 96.1497%
Round-robin severe detection   = 99.5939%
```

### 6.3 What Mini spends attention on

`mini_reactive` spends on average:

```text
21.1741 / 80 rounds
```

servicing an already-open `needs_probe` request.

On those follow-up pulls:

```text
86.2658%
```

select an arm whose **current Base-predicted immediate reward is lower than another available arm**.

Mean predicted immediate opportunity cost per reactive probe:

```text
4.4412 reward units
```

Mean actual oracle opportunity cost per reactive probe:

```text
4.2201 reward units
```

So frozen Mini's challenge signal causes a real short-term sacrifice under scarce attention.

But the signal is generated only **after contradiction has already entered the organism**.

It contains no mechanism for ranking unobserved arms by prospective corrective value.

### 6.4 Staleness

| Policy | Mean stale arm-rounds | Mean stale oracle-best arm-rounds |
|---|---:|---:|
| Greedy | 376.5990 | 66.0525 |
| Mini reactive | **248.4457** | **43.2855** |
| Epsilon | 362.9767 | 63.6559 |
| Round robin | 309.5520 | 54.1836 |

Reactive follow-up therefore substantially reduces how long stale models remain in the effective prediction world, despite making fewer first detections.

## 7. Nano / authority control

Every current arm state is in Mini's hypothesis class.

Every actual Mini model commitment/reopening proposal was sent through unchanged Nano.

Across all four policy arms:

```text
Nano allow rate = 100%
Nano denies     = 0
Nano defers     = 0
```

Therefore the observed resource-allocation failures are not localized to persistence authority.

Nano has no basis in this experiment for deciding which arm is worth observing, and no Nano change is earned.

## 8. Failure localization

FOREIGN-002 does **not** reproduce FOREIGN-001's expressive wound:

```text
current latent relation representable by frozen Mini = YES, by construction
```

It does **not** expose a Nano authority blockage:

```text
actual Mini persistence proposals authorized = 100%
```

The pressure surface is earlier:

```text
which reality contact gets acquired under scarce attention?
```

The narrow localization is therefore:

```text
EVIDENCE / ACQUISITION PRESSURE
```

not a new fourth blockage class.

The world contains corrective evidence that would expose an unobserved stale arm, but that evidence does not enter Mini unless the arm is selected.

## 9. What the result supports

The narrow supported result is:

> **On this constructed deterministic restless-bandit family, frozen Mini's existing contradiction-triggered probe requests usefully allocate follow-up attention after corrective contact: servicing them improves cumulative reward, sharply increases detected-to-repaired completion, and reduces stale effective models. However, the same mechanism does not improve prospective discovery of distinct hidden changes; simple external coverage/exploration controls acquire first corrective contact more often, including on the rare severe subset.**

A compact earned separation is:

```text
repair attention after contradiction
!=
prospective discovery attention before contradiction
```

This is an experimental description of this foreign family, not yet a promoted OpenCore primitive.

## 10. What is not earned

FOREIGN-002 does **not** establish:

```text
CHALLENGE CALIBRATION SOLVED                    NOT_ESTABLISHED
MINI SHOULD GAIN AN ATTENTION SCHEDULER        NOT_ESTABLISHED
A NEW OPENCORE COMPONENT                       NOT_ESTABLISHED
A FOURTH BLOCKAGE CLASS                        NOT_ESTABLISHED
UTILITY / CONSEQUENCE REPRESENTATION IN NANO   NOT_ESTABLISHED
PROACTIVE EXPLORATION AS UNIVERSALLY BETTER    NOT_ESTABLISHED
ROUND-ROBIN AS A GOOD POLICY                    NOT_ESTABLISHED
EPSILON-GREEDY AS A REPAIR                      NOT_ESTABLISHED
GENERAL RESTLESS-BANDIT COMPETENCE              NOT_ESTABLISHED
GENERAL RESOURCE-LIMITED LEARNING               NOT_ESTABLISHED
```

Round-robin illustrates the other extreme: it detects almost every severe shift but loses enormous reward.

Therefore the experiment does not identify an optimal exploration rate or a correct challenge-calibration mechanism.

## 11. Candidate interpretation, not claim

The foreign pressure suggests a possible distinction:

```text
local correction completion
!=
where to seek first corrective contact
```

or informally:

```text
repair attention != discovery attention
```

This remains a candidate compression until independent pressure reproduces it.

The experiment does **not** authorize adding either relation to Mini or Nano.

## 12. Frozen component integrity

After the final sweep:

```text
mini.py SHA-256
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55

nano.py SHA-256
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Regressions:

```text
Mini native lifecycle: 10,000 / 10,000 PASS
Nano frozen tests:      7 / 7 PASS
```

## 13. Execution note

The final population is seeds `0..9999`.

Because one monolithic run exceeded the execution envelope, the population was evaluated as 20 disjoint 500-seed chunks and merged by additive sufficient statistics.

No completed chunk was rerun or selected based on outcome.

## 14. Artifacts

```text
crank/foreign_002_restless_bandit.py
crank/results/foreign_002_restless_bandit_final_10000.json
crank/FOREIGN_002_RESTLESS_BANDIT.md
```
