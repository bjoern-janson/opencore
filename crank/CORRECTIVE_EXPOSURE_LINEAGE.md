# OpenCore Corrective Exposure Lineage

> Living synthesis for the learned-policy and intervention sequence from FOREIGN-007 through Blitzcrank and PCE-001. Frozen assay/spec/result artifacts remain authoritative over this summary.

**Target branch:** `opencore/pce-001`  
**Architecture change through PCE-001:** none  
**Nano change through PCE-001:** none  
**Current evidence boundary:** `L1 = challenge preservation given D_t^oracle`

## Mechanistic core

The current causal frame is:

```text
E_t
-> Pi_t
-> pi_t
-> A_t
-> O_{t+1}
-> W_{t+1}
-> E_{t+1}
```

with external world state:

```text
O_{t+1} = g(X_t, A_t, epsilon_{t+1})
```

The key distinction is:

```text
exogenous outcome generation
!=
exogenous outcome exposure
```

Persistent state need not alter what the world returns under a fixed intervention. It can still alter which interventions are selected and therefore which outcomes are encountered.

The pathology name used here is:

```text
endogenous evidence acquisition
```

The target property is:

```text
non-collapsible corrective exposure
```

## Correction chain

The causal route is decomposed into:

```text
C1  physical availability
C2  policy support
C3  selected action
C4  discrimination
C5  recognition
C6  authority revision
```

with:

```text
C4a  environmental discrimination
C4b  representation-preserved discrimination
```

Correction requires a chain, not a single boolean.

## Discriminating sets

For live alternatives `h_i, h_j`:

```text
D_t^X(h_i,h_j)
    = physically discriminating interventions

D_t^Pi(h_i,h_j)
    = discriminating interventions whose difference survives Pi_t
```

For deterministic information-losing `Pi_t`:

```text
D_t^Pi subseteq D_t^X
```

Two distinct wounds follow:

```text
representational foreclosure:
D_t^X != empty
D_t^Pi = empty

policy foreclosure:
D_t^Pi != empty
D_t^Pi intersect support(pi_t) = empty
```

## FOREIGN-007 — constructed policy foreclosure

FOREIGN-007 established on a frozen constructed family that a quotient safe over the complete current action surface can later alter policy support such that a physically available discriminating probe is omitted.

The forced-probe control recovered the distinction immediately under unchanged Nano.

This localized the wound upstream of authority gating:

```text
representation
-> policy support
-> corrective exposure
```

and established:

```text
absence of contradiction
!=
survival under physically available contradiction
```

## BLITZCRANK-001 — learned foreclosure

BLITZCRANK-001 removed the hand-constructed policy mapping.

A small ordinary tabular learner with persistent memory:

- outperformed its reset control on every paired seed;
- learned that probing was wasteful in target/null contexts;
- retained zero greedy probe support after the target context became discriminating;
- remained physically capable of probing;
- produced changed observations under forced target probing in every seed;
- obtained immediate positive return from the forced target probe in a substantial subset while the matched null probe remained uniformly wasteful.

The earned result was not `information = correction`.

It was:

```text
useful persistent capability
+
contraction of informative-action policy support
can coexist
```

## BLITZCRANK-002 — temporal reopening

BLITZCRANK-002 added ordinary post-shift consequence that made the old skip valuation costly without revealing the hidden A/B regime.

Persistent memory still improved total and post-shift return over reset on every paired seed.

The probe was initially suppressed in the ordinary persistent condition but eventually returned to support in every seed within the long frozen horizon.

Recovery was neither immediate nor equivalent to sustained exposure:

```text
first reopening
!=
sustained reopening
```

Some seeds spent almost the entire post-shift target horizon with the probe absent from support despite eventual reopening.

This forced temporal questions:

```text
support exists?
selection occurs?
when does exposure return?
how persistently does it remain?
```

## PCE-001 — direct exposure-edge intervention

PCE-001 froze the candidate corrective set externally:

```text
D_t^oracle = D_t^Pi
```

and intervened on challenge selection only.

World classes:

```text
WORLD_NULL
    probe is costly and nondiscriminating

WORLD_INFORMATIVE
    probe discriminates and is recognized but is not correction-relevant

WORLD_CORRECTIVE
    probe discriminates and can revise stale persistent reveal leverage
```

Policy arms:

```text
ARM_ENDOGENOUS
    ordinary learned policy

ARM_SUPPORT
    nonzero but vanishing challenge support

ARM_FLOOR
    quantitative lower bound on challenge exposure

ARM_HAZARD
    state-independent challenge hazard
```

### Primary contrast

Frozen primary comparison:

```text
ARM_ENDOGENOUS x WORLD_CORRECTIVE
vs
ARM_HAZARD x WORLD_CORRECTIVE
```

Result over 256 paired seeds and 120 post-shift target encounters:

```text
ENDOGENOUS finite T_C:   0 / 256
HAZARD finite T_C:     195 / 256 = 76.171875%

mean paired censored T_C* difference: 66.421875
median paired difference:             84.0

hazard faster: 195 / 256
tie:            61 / 256
hazard slower:    0 / 256
```

Frozen classification:

```text
CAUSALLY_LOCALIZED_ENDOGENOUS_EVIDENCE_ACQUISITION_FAILURE
```

The result upgrades the lineage from observed association to intervention-localized mechanism on the frozen family:

```text
persistent state
-> policy
-> challenge timing
-> corrective exposure
```

### Secondary contrast

Frozen comparison:

```text
ARM_SUPPORT x WORLD_CORRECTIVE
vs
ARM_FLOOR x WORLD_CORRECTIVE
```

Result:

```text
SUPPORT finite T_C:  64 / 256 = 25.000000%
FLOOR finite T_C:   205 / 256 = 80.078125%

mean paired censored difference: 40.16796875
median paired difference:        30.5
```

Therefore:

```text
nonzero policy support
!=
timely corrective exposure
```

### Control interpretation

PCE-001 does not reduce to `more probing is better`.

The same protected intervention was:

```text
WORLD_NULL:
    costly + nondiscriminating

WORLD_INFORMATIVE:
    discriminating + recognized + non-corrective

WORLD_CORRECTIVE:
    discriminating + recognized + persistent-leverage-changing
```

This preserves:

```text
information
!=
correction
!=
authority revision
```

### Two clocks

PCE-001 records:

```text
T_C  latency to effective correction
T_L  latency until stale persistent leverage becomes consequential
```

In the endogenous corrective arm, `T_C` was censored beyond the frozen horizon in every seed while finite `T_L` occurred in every seed with mean approximately `1.09765625` target encounters.

The important temporal relation on this specimen is therefore:

```text
T_C >> T_L
```

Eventual theoretical reachability is not enough if stale leverage causes consequence first.

## Current earned mechanism statement

The strongest scoped statement is:

> **Within the tested constructed family, persistent learned state can causally reduce exposure to a prospectively identified corrective channel, and exogenizing or quantitatively protecting that exposure can materially reduce correction latency.**

Scope words are load-bearing:

```text
within the tested constructed family
prospectively identified channel
can
materially reduce
```

PCE-001 does not establish a universal exploration law or general corrigibility theorem.

## L1 / L2 / L3 boundary

The next ladder is:

```text
L1  challenge preservation given D_t^oracle
L2  diagnosis that D_t^agent is insufficient
L3  construction of a better challenge set
```

PCE-001 supports only:

```text
L1 under oracle-supplied D_t
```

It does not test:

```text
D_t^agent =? D_t^oracle
```

`L2` and `L3` must remain separate.

A system can correctly infer that its current challenge set is inadequate without knowing which missing intervention would repair it.

The current open question is:

> **Can an adaptive system detect that its current corrective-exposure topology is inadequate without being told which missing intervention would repair it?**

No L2 module, challenge generator, meta-exploration primitive, or architectural repair is earned.

## Methodological stopping rule

PCE-001 prospectively froze the following epistemic rule:

```text
primary intervention fails to separate
-> current endogenous-evidence-acquisition mechanism loses authority

primary intervention separates in the frozen direction
-> mechanism gains bounded authority on the identified dimensions
```

The positive result therefore authorizes the scoped causal statement above, not post-hoc expansion.

The next conceptual update should come from a frozen experiment that separates:

```text
adequate challenge set + failure to use it
```

from:

```text
challenge set itself inadequate
```

without telling the organism which missing intervention repairs the second case.

## Claim ceiling

FOREIGN-007 → BLITZCRANK-001/002 → PCE-001 does **not** establish:

- a universal corrigibility invariant;
- that every informative action should remain policy-supported;
- that exploration is always beneficial;
- a universal epsilon floor;
- a scalar corrigibility metric;
- autonomous challenge-set diagnosis;
- autonomous challenge construction;
- automatic interface invention;
- correctness of `D_t^oracle` outside the harness;
- Nano V1 or a Nano modification;
- a production safety architecture.

## Artifact custody

PCE-001 prospective freeze commit:

```text
b26cd933f38f96acb53d9590e3a5d2055b3c4382
```

Canonical trace commitment:

```text
records: 368,640
uncompressed SHA-256:
d9d263930fef627b059e18690af76ae2f0469d788760c0f328742d8617f6e816

deterministic gzip SHA-256:
7a03aedff6b50e1309baf08bd7f403d9668a55d0756962672618ba4650b56ebb
```

See:

- `PCE_001_SPEC.md`
- `PCE_001_MANIFEST.json`
- `PCE_001_ANALYSIS.md`
- `pce_001.py`
- `PCE_001.md`
- `results/pce_001_result_index.json`
- `results/pce_001_trace_commitment.json`
