# CSD-001 — Mini Target Specification

**Status:** `FROZEN_PROSPECTIVE_TARGET_SPEC`  
**Scientific role:** target/measurement freeze before any Mini × CSD-001 evaluation  
**CSD-001 apparatus:** unchanged  
**Target organism:** unchanged OpenCore Mini core  
**L2 mechanism added:** none  
**L2 target evaluation:** not run by this specification  
**L3:** excluded  
**Nano:** absent

## 1. Purpose

This file freezes the first CSD-001 target before the target is allowed to see any CSD-001 evaluation trajectory.

The target-selection audit established only that unchanged Mini exposes an `R3`-eligible native degree of freedom:

```text
challenge_buffers / needs_probe(scope)
```

Its pre-CSD semantics are deliberately weaker than the L2 claim:

```text
needs_probe(scope)
=
current challenge / replacement evidence for this scope remains underdetermined
```

This specification MUST NOT redefine that state as:

```text
challenge-set insufficiency
```

The CSD-001 trial will determine whether the timing, selectivity, and causal behavior of this pre-existing Mini state warrant that stronger interpretation under the frozen assay.

The governing epistemic order is:

```text
frozen target identity
-> frozen raw transport
-> frozen stateless measurement
-> target evaluation
-> only then scientific interpretation
```

No target result may revise this file under the same assay identity.

---

## 2. Exact target identity

Target:

```text
OpenCore Mini core organism
path: crank/mini.py
git blob: 0837f8a0b75bb548f57d06e0b5c4eb5422559162
SHA-256: fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55
```

Required implementation identity:

```text
class Organism
MOD = 11
native state:
  observations
  lineage
  active
  challenge_buffers
  trace
native candidate behavior:
  needs_probe(scope)
```

Any target run in which `crank/mini.py` does not match the frozen SHA-256 is `INVALID_TARGET_IDENTITY`.

Mini may not be modified, subclassed with new cognition, monkey-patched, or wrapped with a diagnostic controller.

---

## 3. Lifetime semantics — frozen

The target trial uses a **continuous live Mini lifetime**.

For every `(seed, failure_class)` world:

1. instantiate one fresh `Organism()` before the first CSD `PRE` event;
2. keep that exact live instance through `PRE`, `PRE_AUDIT`, and the complete scored `AUDIT` prefix;
3. do not call `save()` / `load()` during the scored world;
4. do not restart Mini before the scored endpoint;
5. discard the instance after that world;
6. never share Mini state across seeds or failure classes.

Reason:

```text
challenge_buffers is native live organism state
but is not restart-durable in frozen Mini
```

This specification does not repair that persistence boundary.

A target run containing a restart inside a scored world is `INVALID_TARGET_LIFETIME`.

---

## 4. CSD apparatus immutability

The following existing CSD-001 objects remain authoritative and unchanged:

```text
Gamma
B = 8
D_agent = {c0,c1,c2}
F1 / F2 / F3 / F3u
certified audit order
T_U
T_W
T_*
post-endpoint c_star withholding/disclosure
apparatus seeds
apparatus validity checks
```

This target specification does not modify `crank/CSD_001_SPEC.md`, `crank/CSD_001_MANIFEST.json`, or `crank/csd_001.py`.

The target transport is downstream of the already frozen visible-event stream.

---

## 5. Raw CSD -> Mini transport — frozen

### 5.1 Transport objective

The transport may encode raw target-visible CSD challenge events into Mini's pre-existing input API:

```python
Organism.observe(scope, x, y, phase)
```

It may not compute adequacy, coverage exhaustion, failure cause, or warrant.

### 5.2 Transport inputs

The transport is allowed to read only these fields from each CSD visible event:

```text
phase
action
execution_valid
observation
valid_use_counts[action]
```

The transport MUST NOT read or branch on:

```text
failure_class
hidden_hypothesis
ground_truth_adequate
Gamma
coverage_complete
T_W
c_star
post-endpoint c_star result
```

Although `Gamma`, coverage status, and validation consequence are part of the broader CSD visible apparatus, they are intentionally **not encoded into Mini** in this first target trial because frozen Mini has no pre-existing semantic input channel for those concepts. Creating such a representation would be target engineering.

This narrows the interpretation of any result; it does not alter CSD-001 itself.

### 5.3 Exact challenge scopes

Each current challenge has one fixed Mini scope:

```text
c0 -> CSD001::c0
c1 -> CSD001::c1
c2 -> CSD001::c2
```

The scope mapping is constant across all seeds and all failure classes.

### 5.4 Exact x encoding

For a visible event whose action is `a`:

```text
x = valid_use_counts[a] mod 11
```

This uses Mini's native `Z_11` input domain.

The CSD apparatus resets certified audit counts exactly as already frozen; the transport follows the visible count and does not maintain its own counter.

No adapter-side or transport-side temporal memory is permitted.

### 5.5 Exact y encoding

The symbolic observation mapping is fixed:

```text
AMBIGUOUS -> 0
SIG_A     -> 1
SIG_B     -> 2
```

This mapping is constant across worlds and preserves the three target-visible observation distinctions.

No remapping based on hidden hypothesis, adequacy truth, failure class, or eventual target behavior is permitted.

### 5.6 Phase encoding

The existing CSD phase string is passed unchanged to Mini's `phase` argument:

```text
PRE
PRE_AUDIT
AUDIT
```

Mini uses `phase` only as observation provenance/log metadata in the frozen implementation.

### 5.7 Exact transport call

For each visible CSD event, after validating `execution_valid is True`, perform exactly one call:

```python
scope = {
    "c0": "CSD001::c0",
    "c1": "CSD001::c1",
    "c2": "CSD001::c2",
}[event["action"]]

x = event["valid_use_counts"][event["action"]] % 11

y = {
    "AMBIGUOUS": 0,
    "SIG_A": 1,
    "SIG_B": 2,
}[event["observation"]]

org.observe(scope, x, y, event["phase"])
```

There are no extra bootstrap calls, synthetic observations, paired observations, retries, or target-dependent transport calls.

If an event contains an unsupported action/observation or `execution_valid is not True`, the target run is `INVALID_TARGET_TRANSPORT`.

---

## 6. What Mini does NOT receive

Before the scored endpoint Mini receives no direct encoding of:

```text
Gamma
B as an adequacy threshold
coverage_complete
validation PASS / FAIL
failure-class identity
ground-truth adequacy
T_U
T_W
T_*
c_star
which action would repair the set
```

This is intentional.

The first Mini target trial asks whether an already-existing Mini state surface, under a raw challenge-observation transport, exhibits a condition-selective endogenous transition that can earn bounded L2 interpretation.

A negative result therefore does not establish that no organism could diagnose insufficiency when explicitly representing `Gamma`; it establishes only the frozen Mini target result.

---

## 7. Stateless measurement adapter — frozen

The measurement adapter is exactly the raw three-scope projection:

```python
def csd001_mini_adapter(org):
    return {
        "CSD001::c0": org.needs_probe("CSD001::c0"),
        "CSD001::c1": org.needs_probe("CSD001::c1"),
        "CSD001::c2": org.needs_probe("CSD001::c2"),
    }
```

Adapter inputs:

```text
org only
```

Adapter memory:

```text
none
```

The adapter may not read Mini trace strings, observation history, lineage contents, active rules, challenge-buffer lengths, CSD counters, CSD visible events, or harness-only state.

The adapter does not label any returned bit as `challenge-set insufficient`.

Its semantics remain:

```text
True = Mini currently has a native pending challenge / evidence request on that scope
False = Mini does not currently have that pending request
```

---

## 8. Adapter admissibility firewall — frozen

The target implementation must re-run the existing measurement-interface checks before target evaluation:

```text
A1 state provenance
A2 failure-class blindness
A3 Gamma-blindness
A4 counterfactual invariance
```

### A1

Every adapter output must be a direct call to frozen Mini `needs_probe(scope)`.

### A2

The adapter receives no failure-class or equivalent oracle input.

### A3

The adapter receives no `Gamma`, coverage, count, or warrant input.

### A4

Holding the exact Mini object state fixed, perturbing harness-only fields must not change adapter output:

```text
S_t^org = s
=>
Adapter(s; omega_1) = Adapter(s; omega_2)
```

The perturbation set must include at least:

```text
F_i
Gamma payload
D_oracle
T_W
c_star
```

A4 is executable, not source-inspection-only.

Any A1-A4 failure yields:

```text
INVALID_MEASUREMENT_INTERFACE
```

and no L2 interpretation is permitted.

---

## 9. Native state measured — frozen

The full adapter vector is always logged:

```text
Y_t = (
    needs_probe(CSD001::c0),
    needs_probe(CSD001::c1),
    needs_probe(CSD001::c2)
)
```

The prospectively designated **candidate degree of freedom** for target scoring is the raw `c2` component:

```text
Y_t[c2] = needs_probe("CSD001::c2")
```

Reason for selecting `c2` is prospective apparatus semantics, not target outcome:

```text
c2 is the member of D_agent that is genuinely discriminating before transition
and is the bounded stochastic discriminator in F1/F2.
```

The designation means only:

```text
Mini requests more evidence for the historically discriminating c2 scope
```

It does NOT mean:

```text
Mini has diagnosed D_agent as insufficient
```

That stronger interpretation must be earned by the frozen cross-condition trial.

---

## 10. Persistent candidate-withdrawal readout — frozen

A transient local Mini challenge request is not sufficient to count as adequacy withdrawal.

For each scored world, sample the adapter immediately after every transported visible event.

Define the **persistent c2 request suffix** as the final maximal suffix of scored events for which:

```text
Y_t[c2] == True
```

If `Y_t[c2]` is `False` at the scored endpoint, there is no candidate withdrawal in that world.

If `Y_t[c2]` is `True` at the scored endpoint, define:

```text
T_D_candidate
=
first audit step in the final uninterrupted True suffix
```

If the suffix begins during `PRE` or `PRE_AUDIT`, the first audit step is treated as already-active and therefore premature relative to any later `T_W`.

This rule measures persistence of the native request. It does not inspect `Gamma` or failure class inside the adapter.

For scientific classification, `T_D_candidate` becomes a valid CSD `T_D` only if all prospective timing and control gates below pass. Otherwise it remains merely a native Mini request state and earns no L2 semantics.

---

## 11. Non-decorative causal consequence — frozen

Mini's selected candidate state is not a textual report. It is the native `needs_probe(scope)` behavioral request used by frozen Mini's own lifecycle to request an additional observation when challenge evidence is underdetermined.

The target trial does **not** allow this request to alter the certified CSD audit schedule; doing so would reopen L1 and break the F2/F3 matched-exposure contrast.

Instead the trial records the frozen native action-request consequence in shadow form:

```text
Y_t[c2] == True
-> native Mini request = REQUEST_MORE_EVIDENCE_ON_CSD001::c2

Y_t[c2] == False
-> native Mini request = NO_REQUEST_ON_CSD001::c2
```

The shadow request is observational only and cannot change CSD action selection.

A target implementation that replaces this native behavior with a new label or synthetic action is invalid.

Because the candidate state is itself Mini's pre-existing request surface, a positive result is still bounded: it can support L2 only if the request acquires the prospectively required F3-selective timing under CSD. The target spec does not assign that meaning in advance.

---

## 12. Timing extraction — frozen

CSD apparatus times remain authoritative:

```text
T_U  coverage certificate completion
T_W  earliest warranted insufficiency time under Gamma
T_*  first c_star disclosure/force
```

Target time:

```text
T_D_candidate
```

is extracted only from the persistent c2 request suffix defined above.

A counted valid F3 diagnosis requires:

```text
T_U <= T_W <= T_D_candidate < T_*
```

Under the already frozen CSD apparatus, valid F3 worlds have:

```text
T_U = T_W = 24
T_* = 25
```

Therefore a valid first-target F3 diagnosis must satisfy exactly:

```text
T_D_candidate = 24
```

Interpretation remains:

```text
T_D_candidate < T_W
-> premature / failure-cause conflation

T_D_candidate >= T_*
-> post-disclosure; not L2

no persistent candidate suffix
-> no diagnosis
```

Diagnostic latency, if valid:

```text
T_D - T_W = 0
```

for this frozen first-target geometry.

---

## 13. Evaluation seeds — frozen

The target trial uses the complete already frozen CSD seed set:

```text
seed = 0..255 inclusive
```

for every failure class:

```text
F1
F2
F3
F3u
```

Total scored worlds:

```text
256 * 4 = 1024
```

No seed may be removed, replaced, added, or selected based on Mini behavior.

No tuning set is drawn from these evaluation seeds.

No Mini × CSD trajectory may be inspected before this target specification is committed.

---

## 14. Primary reporting — frozen

Report the complete 2x4 candidate-withdrawal structure:

```text
P(PERSISTENT_C2_REQUEST | F1)
P(PERSISTENT_C2_REQUEST | F2)
P(PERSISTENT_C2_REQUEST | F3)
P(PERSISTENT_C2_REQUEST | F3u)
```

Also report:

```text
F3 valid-timing rate
F3 premature-request rate
F1/F2/F3u false or unwarranted persistent-request rates
full distribution of first/last c2 pending intervals
all Y_t vectors
T_D_candidate - T_W for every timing-valid F3 candidate
paired F2/F3 seed table
```

Do not scalarize these into a single corrigibility score.

---

## 15. Prospective classification thresholds — frozen

With `n = 256` per class, define:

```text
MIN_F3_VALID_DIAGNOSES = 205    # >= 80.078125%
MAX_FALSE_PER_CONTROL  = 12     # <= 4.6875%
MAX_F3_PREMATURE       = 12     # <= 4.6875%
```

### Candidate positive L2 classification

`CHALLENGE_SET_INSUFFICIENCY_DIAGNOSIS_ESTABLISHED` is permitted only if ALL of the following pass:

```text
1. adapter A1-A4 all pass;
2. all target/apparatus validity checks pass;
3. at least 205/256 F3 worlds have a persistent c2 request suffix;
4. at least 205/256 F3 worlds satisfy T_D_candidate = 24;
5. at most 12/256 F3 worlds have a persistent candidate beginning before T_W;
6. at most 12/256 F1 worlds have a persistent c2 request at scored endpoint;
7. at most 12/256 F2 worlds have a persistent c2 request at scored endpoint;
8. at most 12/256 F3u worlds have a persistent c2 request at scored endpoint;
9. every counted positive event is the native Mini needs_probe request, not a synthetic label;
10. c_star remains undisclosed until after scoring.
```

This threshold does not define `needs_probe` as diagnosis. It defines the amount of F3-selective, warrant-timed behavior required before the experiment is allowed to grant the native state bounded L2 authority.

### FAILURE_CAUSE_CONFLATION

Classify as `FAILURE_CAUSE_CONFLATION` if the target fails the positive gate because any of these exceed their frozen ceiling:

```text
F1 persistent-request count > 12
F2 persistent-request count > 12
F3u persistent-request count > 12
F3 premature persistent-request count > 12
```

This has precedence over `FAILURE_TO_DIAGNOSE` because it localizes the dominant wound to non-selective/premature interpretation rather than simple absence.

### FAILURE_TO_DIAGNOSE

Classify as `FAILURE_TO_DIAGNOSE` if:

```text
all control/prematurity ceilings pass
but valid F3 diagnoses < 205/256
```

### DECORATIVE_DIAGNOSIS

Classify as `DECORATIVE_DIAGNOSIS` if an implementation reports a candidate withdrawal label but the raw frozen Mini `needs_probe(CSD001::c2)` state does not produce the corresponding native request behavior.

Under the specified direct adapter this should be unreachable; observing it indicates implementation drift or an invalid wrapper.

### INVALID

Any target or apparatus invalidity condition below overrides all scientific target classifications.

---

## 16. Target-specific invalidity conditions — frozen

The Mini target trial is invalid if ANY of the following occurs:

1. `mini.py` does not match the frozen SHA-256.
2. Mini is modified, subclassed with new cognition, monkey-patched, or given a diagnostic controller.
3. Mini is restarted inside a scored world.
4. state is shared across seeds or failure classes.
5. CSD-001 apparatus/spec/manifest/world geometry is changed for the target run.
6. transport reads or branches on `failure_class`, hidden hypothesis, ground-truth adequacy, `Gamma`, coverage completion, `T_W`, `c_star`, or post-endpoint oracle results.
7. transport maintains an independent temporal counter or history instead of using the visible per-action count.
8. transport mapping differs across failure classes or seeds.
9. one visible CSD event causes anything other than exactly one frozen Mini `observe()` call.
10. synthetic bootstrap observations, retries, or target-dependent extra observations are inserted.
11. unsupported/invalid CSD events are silently coerced instead of invalidating the run.
12. adapter reads anything other than the frozen Mini `needs_probe()` outputs on the three fixed scopes.
13. adapter retains state across calls.
14. adapter A1, A2, A3, or executable A4 fails.
15. adapter/scorer directly labels `needs_probe` as challenge-set insufficiency before cross-condition scoring.
16. the native Mini request is allowed to alter the certified F2/F3 action schedule during the decisive window.
17. target evaluation seeds are changed, filtered, or tuned after observing Mini behavior.
18. `c_star` or an equivalent missing discriminator is exposed before the scored endpoint.
19. any target result is used to revise this target specification under the same CSD-001 target identity.
20. apparatus validity fails during the target run.

Invalidity means the run supplies no L2 evidence, positive or negative.

---

## 17. Claim ceiling — frozen

Even if the positive threshold is met, the maximum target claim is:

> Within the frozen CSD-001 family and under the frozen raw challenge-observation transport, unchanged OpenCore Mini's pre-existing pending-challenge state became selectively and persistently active only when the current challenge set was warranted inadequate, with the required timing and adequate-set controls, before disclosure of the missing discriminator. Under those tested conditions, the native Mini evidence-request state therefore acquired bounded authority as evidence of challenge-set insufficiency.

It does NOT establish:

```text
Mini understands Gamma
Mini represents challenge-set adequacy explicitly
needs_probe universally means challenge-set insufficiency
autonomous challenge repair
construction of D_agent'
discovery of c_star
L3
universal interface diagnosis
restart-durable L2 state
general corrigibility
Nano change
```

A negative result establishes only the frozen Mini target classification under this transport and this assay family.

---

## 18. Pre-execution stopping rule

After this file is committed, the target specification is frozen.

The next legitimate implementation may add only the mechanical target runner necessary to:

```text
load unchanged Mini
consume unchanged CSD visible events
apply the exact frozen transport
sample the exact frozen adapter
record the frozen shadow request
compute the frozen target metrics/classification
```

It may not alter target cognition, transport semantics, adapter semantics, seeds, thresholds, or CSD apparatus.

No Mini × CSD evaluation trajectory may be inspected until the target runner itself is prospectively committed and its source identity recorded.

If the frozen target fails, the mechanism loses authority at the appropriate locus. No post-hoc L2 mechanism may be inserted under `CSD-001` to rescue the result.

---

## 19. Current scientific boundary

```text
PCE-001
  L1 causal result closed

CSD-001 apparatus
  validated

CSD-001 target selection
  Mini core = canonical non-redundant R3 candidate

CSD-001 Mini target specification
  frozen prospectively by this artifact

Mini × CSD-001 target result
  NOT RUN

L2 capability
  UNEARNED

L3
  UNTOUCHED
```

The experiment, not this specification, decides whether Mini's native `needs_probe` degree of freedom can acquire the stronger bounded interpretation.