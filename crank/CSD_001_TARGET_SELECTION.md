# CSD-001 — Target Selection Audit

**Status:** `PRE_CSD_TARGET_SELECTION_AUDIT`  
**Scientific role:** measurement-interface admissibility and target selection only  
**CSD-001 target evaluation:** not run  
**CSD outcome data used in this audit:** none  
**Nano change:** none  
**L2 mechanism added:** none

## 1. Purpose

CSD-001 has a validated assay apparatus but no frozen target organism. This document audits existing pre-CSD organism/state surfaces before any target is evaluated on the CSD failure classes.

The target-selection rule is:

```text
find an existing organism whose native state already contains
some potentially diagnostic degree of freedom, and require that
this degree of freedom can be measured without computing its meaning
```

This is not an L2 result and does not use CSD-001 outcome data.

## 2. Governing adapter invariant

An admissible measurement adapter has the form:

```text
Y_t = Adapter(S_t^org)
```

and not:

```text
Adapter(S_t^org, Gamma, F_i, D_oracle, T_W, c_star) -> diagnosis
```

The adapter may translate or project native organism state. It may not accumulate coverage, infer persistent ambiguity, evaluate the adequacy envelope, classify failure cause, or manufacture a new diagnostic state.

The adapter is required to be stateless except for state already contained in `S_t^org`.

## 3. Admissibility conditions

```text
A1  state provenance
    Every scored signal originates in pre-existing organism state/behavior.

A2  failure-class blindness
    The adapter receives no F1/F2/F3/F3u identity or equivalent oracle field.

A3  Gamma-blindness
    The adapter does not evaluate the adequacy envelope or a coverage certificate.

A4  counterfactual invariance
    Holding organism state fixed, changing harness-only truth cannot change output.
```

Executable form of A4:

```text
S_t^org = s
=>
Adapter(s; omega_1) = Adapter(s; omega_2)
```

for worlds differing in hidden failure class, adequacy truth, warrant time, or missing discriminator while preserving the exact organism state presented to the adapter.

## 4. Disposition ladder

```text
R0  no potentially relevant endogenous state exists
R1  potentially relevant state exists but cannot be exposed without adapter computation
R2  proposed measurement/interface path violates A1-A4 or requires forbidden semantic injection
R3  native degree of freedom exists and a stateless A1-A4-admissible projection exists
```

Only `R3` is eligible for a later target freeze. `R3` is not L2 evidence.

## 5. Pre-CSD provenance rule

Target choice is justified only from source/state semantics that predate CSD-001.

The candidate source files below are inherited unchanged from parent branch `opencore/pce-001`. CSD-001 adds apparatus artifacts but does not modify these candidate organism implementations.

The canonical pre-CSD Mini identity is also preserved in earlier frozen records as:

```text
mini.py SHA-256
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55
```

No CSD failure-class performance was consulted when assigning dispositions.

---

## 6. Candidate audit

### Candidate A — OpenCore Mini core organism

```text
file:      crank/mini.py
git blob:  0837f8a0b75bb548f57d06e0b5c4eb5422559162
role:      native adaptive organism
```

Native state surface:

```text
observations
lineage
active
challenge_buffers
trace
```

The pre-CSD organism creates `challenge_buffers[scope]` after contradictory evidence and leaves the scope in that state until its current challenge observations identify a unique replacement. Its native trace says:

```text
PROBE-REQUEST <scope>: challenge still underdetermined
```

and its native method is:

```text
needs_probe(scope) = scope in challenge_buffers
```

This is not named "challenge-set insufficiency." It is a pre-existing organism state meaning only that the current challenge/repair evidence is underdetermined.

Candidate degree of freedom:

```text
pending challenge scope(s)
```

Minimal candidate adapter:

```python
def mini_pending_adapter(state):
    return {
        "pending_challenge_scopes": tuple(sorted(state["challenge_buffers"].keys())),
        "has_pending_challenge": bool(state["challenge_buffers"]),
    }
```

Adapter inputs:

```text
challenge_buffers only
```

Adapter statefulness:

```text
none
```

Admissibility:

```text
A1 PASS  direct projection of native organism state
A2 PASS  no failure-class input
A3 PASS  no Gamma/coverage input
A4 PASS  executed counterfactual invariance test
```

Important boundary:

`challenge_buffers` is live organism state but is not included in Mini's `save()` payload. Therefore this candidate degree of freedom is not restart-durable in the frozen Mini implementation. Any later target freeze must either operate within the live organism lifetime or reject Mini if durability is made a target requirement. This audit does not repair persistence.

Disposition:

```text
R3 — eligible for target freeze
```

### Candidate B — FOREIGN-002 FrozenStack / Mini-reactive specimen

```text
file:      crank/foreign_002_restless_bandit.py
git blob:  5c6bf38510fa1d511925990c967eebb9060ed9d9
role:      foreign-pressure stack containing unchanged Mini
```

Native potentially relevant state:

```text
FrozenStack.org.challenge_buffers
FrozenStack.org.needs_probe(scope)
```

The `mini_reactive` policy already treats Mini's native `needs_probe` request as behaviorally consequential by selecting pending scopes before ordinary greedy choice. The stack adds `base_rules`, Nano receipts/counts, and policy machinery, but it adds no new diagnostic degree of freedom beyond unchanged Mini.

Minimal candidate adapter:

```python
def foreign2_nested_mini_adapter(state):
    return mini_pending_adapter(state["org"])
```

Admissibility:

```text
A1 PASS  projects nested native Mini state
A2 PASS  no failure-class input
A3 PASS  no Gamma/coverage input
A4 PASS  executed counterfactual invariance test
```

Disposition:

```text
R3 — technically eligible, but not selected as the canonical target candidate
```

Reason for non-selection is semantics/minimality, not CSD performance: this candidate exposes exactly the same relevant Mini state while adding Nano/Base/policy wrapper surfaces. The simpler Mini core dominates it for a first target freeze because it preserves the same endogenous degree with fewer attribution paths.

### Candidate C — BLITZCRANK-002 persistent learner

```text
file:      crank/blitzcrank_002_v2.py
git blob:  5f01bfb567e78dc2265dfdda896d8ea3c2eae05d
role:      external tabular organism
```

Native state surface:

```text
q_reveal
n_reveal
q_decision
n_decision
```

The organism has learned action values/counts and policy support derived from them. It has no native unresolved, abstention, challenge-adequacy, reopen-request, or procedure-withdrawal state.

A measurement layer could derive a statistic from Q-values/counts, but deciding that such a statistic means "current challenge set is inadequate" would be new epistemic computation in the adapter.

Disposition:

```text
R0 — no native candidate adequacy-withdrawal degree of freedom identified
```

This does not claim BLITZCRANK-002 lacks all useful uncertainty information; it says the frozen organism does not expose the specific pre-existing state required by this target-selection gate without constructing a new interpretation rule.

### Candidate D — PCE-001 tabular learner

```text
file:      crank/pce_001.py
git blob:  26bf0bea8b1c69a200db6a7293d1a8dcae9f3f86
role:      PCE-001 adaptive organism under exposure intervention
```

Native organism state remains:

```text
q_reveal
n_reveal
q_decision
n_decision
```

PCE-001's `D_oracle`, C1-C6 gates, evidence-role labels, counterfactual probe values, `T_C`, and related classifications are harness-side instrumentation. They are not native Agent state.

Any adapter that used those fields would fail provenance/blindness. Any adapter that inferred adequacy withdrawal directly from the native Q/count state would add the diagnostic rule being tested.

Disposition:

```text
R0 — no native candidate adequacy-withdrawal degree of freedom identified
```

### Candidate E — Mini-005 reopenable controller

```text
file:      crank/mini_005_closure_gravity.py
git blob:  bd0071d1217d20480923efcafdac922bd1f7177c
role:      typed post-closure experimental controller, not unchanged Mini cognition
```

Attractive apparent state/behavior:

```text
EventOutcome.action = REOPEN / KEEP_CLOSED / FORK_SCOPE
challenge_path_open
```

But those outputs are generated by `handle_event()` from a harness-supplied `PostClosureEvent` that already contains semantic fields including:

```text
kind
scope
target_relevant
```

Transporting raw CSD consequence into the `IN_SCOPE_COUNTEREXAMPLE` / relevance vocabulary would require the target interface to perform the semantic classification under test.

Disposition:

```text
R2 — relevant-looking state exists, but CSD transport would require forbidden semantic injection
```

### Candidate F — Mini-006 grounded closure-policy controller

```text
file:      crank/mini_006_recursive_closure_grounding.py
git blob:  36ecde0ac9eab6d421fc2c1e42d2fa1635ec31d8
role:      typed policy-level experimental controller
```

Attractive apparent state:

```text
ClosurePolicy.require_explicit_contract
ClosurePolicy.revision_count
```

The state is causally consequential for future closure behavior, but the `respond()` path receives an externally typed `PolicyEvent.kind` distinguishing:

```text
OBJECT_LEVEL_SURPRISE
POLICY_LEVEL_SURPRISE
```

and also receives externally supplied closure-authority semantics.

Using this controller as a CSD target would require an input translation that decides whether the observed CSD history constitutes `POLICY_LEVEL_SURPRISE`. That translation would perform the diagnosis before the organism state changed.

Disposition:

```text
R2 — relevant-looking state exists, but CSD transport would require forbidden semantic injection
```

---

## 7. Executed A4 audit

A4 was executed on the two R3 measurement candidates using a fixed organism-state snapshot and paired harness worlds that differed in hidden failure class, Gamma payload, oracle set, warrant time, and missing-discriminator identity.

The accepted adapter functions had exactly one positional input and no epistemically meaningful adapter memory.

Execution result:

```json
{
  "foreign2_nested_mini_adapter": {
    "A4_counterfactual_invariance": true,
    "forbidden_code_names": [],
    "output": {
      "has_pending_challenge": true,
      "pending_challenge_scopes": ["A"]
    },
    "repeat_same_state_equal": true,
    "single_positional_input": true
  },
  "mini_pending_adapter": {
    "A4_counterfactual_invariance": true,
    "forbidden_code_names": [],
    "output": {
      "has_pending_challenge": true,
      "pending_challenge_scopes": ["A"]
    },
    "repeat_same_state_equal": true,
    "single_positional_input": true
  },
  "negative_control_hidden_oracle": {
    "A4_counterfactual_invariance": false,
    "caught": true,
    "expected": false,
    "forbidden_code_names": []
  }
}
```

Audit-output SHA-256:

```text
60f63927d63e84b003bf7adccf21e0a0bf665a9e9332522e653eee714f72667f
```

The negative control deliberately hid failure-class dependence behind a generically named global variable rather than an obvious forbidden identifier. Static name inspection therefore did not catch it, while the counterfactual A4 perturbation did. This is why A4 is retained as an executable invariance test rather than only a source-inspection rule.

The A4 test is a measurement-interface test only. It does not execute CSD failure-class trajectories and supplies no L2 evidence.

## 8. Selection result

The audit produces two R3 surfaces:

```text
Mini core
FOREIGN-002 stack through the exact same nested Mini state
```

They do not provide two independent diagnostic degrees of freedom. FOREIGN-002 inherits Mini's degree and adds attribution surface.

Therefore the canonical candidate for the next **target-freeze** step is:

```text
OpenCore Mini core organism
crank/mini.py
git blob 0837f8a0b75bb548f57d06e0b5c4eb5422559162
SHA-256 fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55
candidate native state: challenge_buffers / needs_probe(scope)
```

This is a target-selection result, not yet a target freeze. No adapter-to-CSD scoring semantics, target evaluation seeds, or L2 classification thresholds are frozen here.

The selection is based only on pre-CSD semantics and minimality:

```text
native underdetermination state exists
+
state is organism-generated
+
stateless raw projection passes A1-A4
+
no additional wrapper required
```

It is explicitly **not** based on observed CSD performance.

## 9. What remains to freeze before any L2 trial

A descendant target freeze must still specify prospectively:

```text
exact Mini target invocation/state lifetime
exact environment-to-Mini observation transport
exact stateless Mini-state adapter
which raw Mini state transition counts as the CSD-visible candidate withdrawal signal
what behavioral consequence makes the signal non-decorative
how T_D is read from that native transition
all target evaluation seeds and classification thresholds
```

The environment-to-Mini transport must not translate CSD histories into privileged semantic labels. In particular, it must not compute Gamma violation, failure class, challenge-set insufficiency, or the missing discriminator.

## 10. Claim ceiling

This audit establishes only:

> Among the inspected pre-CSD repository candidates, frozen Mini exposes a native underdetermination/request state that can be projected by a stateless A1-A4-admissible measurement adapter. The FOREIGN-002 stack exposes the same underlying Mini degree with additional wrapper surface. The inspected Blitz/PCE learners do not expose a comparable native state without adding interpretive computation, and the inspected Mini-005/006 controllers require harness-typed semantic inputs that would contaminate CSD transport.

It does not establish:

```text
Mini has L2 capability
Mini will diagnose F3
Mini will distinguish F2 from F3
needs_probe means challenge-set insufficiency
Mini should be modified
an L2 mechanism
challenge repair
challenge constitution
```

## 11. Current boundary

```text
PCE-001       L1 causal result closed
CSD-001       L2 apparatus validated
TARGET AUDIT  Mini core is R3-eligible candidate
TARGET FREEZE not yet performed
L2            still unearned
L3            untouched
```

The next legitimate artifact is a separately prospective target/adapter freeze. CSD-001 itself remains unchanged.
