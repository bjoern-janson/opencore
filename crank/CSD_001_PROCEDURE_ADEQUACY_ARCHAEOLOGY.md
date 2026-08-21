# CSD-001 — Procedure-Adequacy Archaeology

**Status:** `PRE_CSD_PROCEDURE_ADEQUACY_ARCHAEOLOGY`  
**Scientific role:** post-negative target archaeology only  
**Source boundary:** pre-CSD repository state `opencore/pce-001`  
**CSD target outcome data used for candidate disposition:** none  
**New target selected:** no  
**New target frozen:** no  
**L2 mechanism added:** none  
**L3:** untouched  
**Nano change:** none

## 1. Purpose

This archaeology pass asks only whether the pre-CSD OpenCore lineage already contains an organism/controller state whose **native semantics concern the adequacy or applicability of its own evidence-acquisition procedure**.

It does not design a repair and does not search for a state merely because it correlates with CSD failure.

The governing rule is:

```text
Do not turn a discovered missing semantic degree of freedom
into an engineered semantic degree of freedom.
```

The earlier measurement gate remains intact:

```text
R3 measurability != L2 semantic sufficiency
```

Therefore an L2 target must satisfy both:

```text
1. a native endogenous state/behavior can be measured without adapter computation; and
2. the native semantics of that state already concern the adequacy/applicability
   of the evidence-acquisition procedure itself, with an admissible raw-evidence
   path into that state.
```

A state that is only object-local unresolvedness is not sufficient. A procedure-level state whose transition requires the harness to classify the event as procedure-level is also not sufficient.

## 2. Provenance boundary

All candidate semantics in this file are read from the parent branch:

```text
opencore/pce-001
```

The relevant pre-CSD source identities include:

```text
mini.py                                0837f8a0b75bb548f57d06e0b5c4eb5422559162
mini_004_budgeted_closure.py           70c4481165c91cdc2f7cad8553324fcb69f7281b
mini_005_closure_gravity.py            bd0071d1217d20480923efcafdac922bd1f7177c
mini_006_recursive_closure_grounding.py 36ecde0ac9eab6d421fc2c1e42d2fa1635ec31d8
mini_cerebro_attack.py                 9197d1ee82ce0fab299de5d536ee38a611c65828
mini_ssi_attack.py                     2c996f7fc4ecedc681ff63ba3d00d93b83b4a205
mini_nano_composition.py               8ff8f8ef4fba4d2a5854c04314007a5a38b90db7
nano.py                                 d31dacaf893a58a8280c01704fe666a404c1f56c
base_002_global_reopening.py           883e1090f9fe5d3786cb53d09a1cee20f340b247
foreign_007_v2.py                      1c29c5596c2f68b7be96335da752a3e5c4d3cd86
af3_oc_001.py                          6b2eeec71fc43c437380190a80b11c8b0e4ec313
blitzcrank_002_v2.py                   5f01bfb567e78dc2265dfdda896d8ea3c2eae05d
pce_001.py                             26bf0bea8b1c69a200db6a7293d1a8dcae9f3f86
```

No `CSD_001.md` result values, target traces, target classifications, or post-CSD organism changes are used to make the candidate dispositions below.

## 3. Admissibility discipline

The original adapter firewall remains authoritative:

```text
A1  native-state provenance
A2  failure-class blindness
A3  Gamma-blindness
A4  counterfactual invariance under harness-only changes
```

This pass adds no replacement for A1-A4.

It asks one additional selection question before a new adapter is even worth constructing:

> Can the candidate's procedure-level state be reached from its native/raw input surface without the transport first deciding that the observed failure is a procedure-adequacy failure?

If not, the candidate remains an `R2` semantic near-match: the state may look right, but the transport would perform the diagnosis.

## 4. Strongest semantic near-match — Mini-006

Source:

```text
crank/mini_006_recursive_closure_grounding.py
blob 36ecde0ac9eab6d421fc2c1e42d2fa1635ec31d8
```

Mini-006 contains genuinely procedure-level state:

```text
ClosurePolicy.require_explicit_contract
ClosurePolicy.revision_count
```

and this state has causal consequence for future closure behavior. `initial_closure_decision()` returns `DEFER / NO_EXPLICIT_SCOPE_CONTRACT` for an uncontracted scope when `require_explicit_contract` is true.

Its native semantic object is therefore much closer to L2 than Mini core's local `needs_probe` state:

```text
is this closure procedure authorized/applicable in this scope?
```

However, the transition into the revised policy state is not discovered from raw evidence by the controller. `respond()` receives a pre-typed:

```text
PolicyEvent.kind = OBJECT_LEVEL_SURPRISE
or
PolicyEvent.kind = POLICY_LEVEL_SURPRISE
```

and only the externally typed `POLICY_LEVEL_SURPRISE` branch changes `ClosurePolicy`.

Therefore a CSD transport would have to answer, before the state changes:

```text
is this merely object-level failure
or
is this failure of the evidence/closure procedure itself?
```

That is the L2 discrimination under test.

Disposition:

```text
R2 — strongest semantic near-match, but transport requires forbidden semantic injection.
NOT ELIGIBLE FOR TARGET FREEZE.
```

This is the central archaeology result.

## 5. Mini-004 — procedure contract exists, but outside native organism state

Source:

```text
crank/mini_004_budgeted_closure.py
blob 70c4481165c91cdc2f7cad8553324fcb69f7281b
```

The `contract_aware` controller has explicit procedure-level semantics. It stops only when an external `(p_min, delta)` challenge contract plus no-hit evidence licenses closure; otherwise it asks for more coverage or defers.

But the contract, its adequacy semantics, the hidden challenge population, and the controller logic are harness-side. Frozen Mini itself is imported unchanged and does not persist a native state meaning that its evidence-acquisition procedure is adequate or inadequate.

Treating CSD `Gamma` as the Mini-004 closure contract would also require a new semantic equivalence to be supplied by the transport.

Disposition:

```text
R0/R2 boundary — useful procedure-level control logic exists, but not as a native
organism state reachable without externally constituted contract semantics.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 6. Mini-005 — reopening semantics depend on typed event roles

Source:

```text
crank/mini_005_closure_gravity.py
blob bd0071d1217d20480923efcafdac922bd1f7177c
```

Mini-005 exposes behavior such as:

```text
REOPEN
FORK_SCOPE
KEEP_CLOSED
challenge_path_open
```

but `handle_event()` receives `PostClosureEvent` fields already carrying:

```text
kind = IN_SCOPE_COUNTEREXAMPLE / OUT_OF_SCOPE_COUNTEREXAMPLE / NUISANCE
scope
target_relevant
```

A raw CSD-to-Mini-005 transport would therefore have to decide the event's relevance/type before the controller acts.

Disposition:

```text
R2 — relevant procedure behavior, forbidden typed-event injection.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 7. SSI attack surface — applicability comparator, not native diagnosis

Source:

```text
crank/mini_ssi_attack.py
blob 2c996f7fc4ecedc681ff63ba3d00d93b83b4a205
```

This lineage contains applicability semantics: a transition receipt can be `CURRENT` or become `INAPPLICABLE` when independently constituted regime/applicability information changes.

That is semantically adjacent to procedure adequacy, but the decisive regime/applicability fact is external and the comparator is an assay/controller surface, not an endogenous adaptive organism state that diagnoses its own evidence-acquisition procedure from raw consequence.

Disposition:

```text
R2 — applicability semantics exist, but the applicability fact is externally constituted.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 8. Cerebro acquisition-aperture control — right question, no organism state

Source:

```text
crank/mini_cerebro_attack.py
blob 9197d1ee82ce0fab299de5d536ee38a611c65828
```

Attack A explicitly identifies a procedure mismatch:

```text
licensed sampling protocol = uniform
active selector protocol   = changed acquisition aperture
```

and states that selected clean evidence is not licensed evidence for the original protocol.

This is conceptually close to the desired semantic object. But the `protocol_aware` control is not implemented as a stateful organism that infers the mismatch. The harness already knows the two protocols; the control simply refuses to stop under that known mismatch.

Disposition:

```text
R0 — procedure-adequacy comparator exists only as external control logic;
no native candidate state to measure.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 9. Nano / Mini-Nano composition — semantic facts are external by design

Sources:

```text
crank/nano.py
blob d31dacaf893a58a8280c01704fe666a404c1f56c

crank/mini_nano_composition.py
blob 8ff8f8ef4fba4d2a5854c04314007a5a38b90db7
```

Nano's own source states that it is intentionally semantically agnostic: payloads are opaque and its trusted surface checks externally constituted standings, licenses, preconditions, effect grants, preservation obligations, and revocations.

The composition assay contains attractive standings such as acquisition protocol and applicability/validity state, but its own design says that a harness adapter turns externally constituted control facts into Nano's Standing/License/Transition surface.

Therefore Nano can protect a supplied procedure-validity fact; it does not natively infer that its evidence-acquisition procedure is inadequate.

Disposition:

```text
R0 for Nano-native L2 semantics;
R2 for composition standings whose meaning is supplied externally.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 10. Base-002 — native persistent reopening mechanics, externally constituted refutation role

Source:

```text
crank/base_002_global_reopening.py
blob 883e1090f9fe5d3786cb53d09a1cee20f340b247
```

Base-002 has real persistent intermediate state such as:

```text
G_STATUS = REOPENED
```

and cleanly separates `ADMIT(G)`, `REOPEN(G)`, and `REPLACE(G,G')`.

But the source explicitly constitutes the counterexample role externally as `REFUTES_G`, along with licenses, unit relevance, projections, and successor evidence. Reusing that state for CSD would require the transport to declare that the incoming consequence refutes the governing procedure/authority.

Its native object is also global invariant authority, not the sufficiency of an evidence-acquisition topology.

Disposition:

```text
R2 — meaningful persistent reopening state, but role constitution is external
and the semantic object is not acquisition-procedure adequacy.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 11. FOREIGN-007 — topology changes behavior, but no topology-adequacy self-state

Source:

```text
crank/foreign_007_v2.py
blob 1c29c5596c2f68b7be96335da752a3e5c4d3cd86
```

FOREIGN-007 is central evidence that representation can alter policy support and remove a physically available discriminator from execution. Its state includes candidate cells and the resulting policy support.

But there is no native meta-state asserting or withdrawing the adequacy of that evidence-acquisition topology. The assay constructs fine/coarse representations and measures the downstream policy consequence.

Disposition:

```text
R0 — topology state exists; topology-adequacy diagnosis state does not.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 12. AF3-OC-001 — epistemic standing, not acquisition-procedure adequacy

Source:

```text
crank/af3_oc_001.py
blob 6b2eeec71fc43c437380190a80b11c8b0e4ec313
```

AF3-OC-001 separates prediction, confidence, external validation, refutation, reopening, and successor evidence through Nano. These are important authority semantics, but the evidence roles and transition licenses are externally constituted.

It does not contain a native state that evaluates whether its own evidence-acquisition procedure is sufficient.

Disposition:

```text
R0/R2 — authority-state semantics exist, but no endogenous procedure-adequacy diagnosis.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 13. Blitz / PCE — learned policy state without procedure-adequacy semantics

Sources:

```text
crank/blitzcrank_002_v2.py
blob 5f01bfb567e78dc2265dfdda896d8ea3c2eae05d

crank/pce_001.py
blob 26bf0bea8b1c69a200db6a7293d1a8dcae9f3f86
```

These organisms carry learned Q/count state and can change corrective exposure. Their challenge-set and gate interpretations are harness instrumentation, not native organism semantics.

Deriving a new "procedure inadequate" state from Q/count trajectories would be the forbidden engineering step.

Disposition:

```text
R0 — no native procedure-adequacy degree of freedom identified.
NOT ELIGIBLE FOR TARGET FREEZE.
```

## 14. Mini core / FOREIGN-002 — measurement survives, semantics remain local

The pre-CSD Mini identity remains:

```text
crank/mini.py
blob 0837f8a0b75bb548f57d06e0b5c4eb5422559162
```

and FOREIGN-002 exposes the same nested Mini degree.

Their native `challenge_buffers / needs_probe(scope)` state is a legitimate R3 measurement surface. Its original semantics are local challenge/replacement underdetermination, not adequacy of the family of evidence-acquisition procedures.

This archaeology therefore preserves rather than rewrites the earlier target-selection result:

```text
R3 measurement admissibility survives.
Semantic eligibility for L2 does not follow from R3.
```

No CSD outcome data are needed for that source-level statement.

## 15. Archaeology result

Across the inspected pre-CSD organism/controller surfaces, no candidate satisfies all required properties simultaneously:

```text
native measurable state/behavior
+
native semantics about adequacy/applicability of the evidence-acquisition procedure
+
admissible raw-evidence transition into that state without external procedure-level typing
```

Result:

```text
NO_ADMISSIBLE_PRE_CSD_L2_TARGET_FOUND
```

The closest semantic near-match is Mini-006, but it fails at the transport boundary because `POLICY_LEVEL_SURPRISE` is already an externally supplied classification.

No new A4 target-adapter execution is warranted in this pass: no new candidate reaches the point where an admissible raw-evidence transport plus candidate adapter can be specified without first performing the L2 inference outside the organism. Running A4 on a downstream projection alone would not repair that upstream semantic leak.

## 16. Claim ceiling

This archaeology establishes only:

> Among the inspected OpenCore pre-CSD lineage surfaces, no existing candidate was found that simultaneously carries a native procedure-adequacy/applicability state and can reach that state from raw evidence without the transport or harness first supplying the procedure-level classification. Mini-006 is the strongest semantic near-match, but its policy revision is triggered by an externally typed `POLICY_LEVEL_SURPRISE` event.

It does **not** establish:

```text
L2 is impossible
no external organism could satisfy L2
no future pre-existing target can be found
Mini-006 cannot be redesigned
which L2 mechanism should be built
how procedure adequacy should be represented
how challenge repair should work
L3
```

No target is selected or frozen by this document.

## 17. Current boundary

```text
PCE-001                         L1 causal result closed
CSD-001 apparatus                validated
Mini target trial                clean negative / prior result preserved
R3 measurement criterion         survives
procedure-adequacy archaeology   no admissible pre-CSD target found
new L2 target                    NONE
L2 mechanism                     NOT AUTHORIZED
L3                               UNTOUCHED
```

The current scientific authority therefore remains the existing CSD-001-Mini negative result. The next move, if any, must not manufacture the missing semantic degree merely because archaeology failed to find it in the current lineage.
