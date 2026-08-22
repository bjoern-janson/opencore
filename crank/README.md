# OpenCore Crank

> **Experimental lineage. Not the formal K0/E001 program.**

`crank/` contains OpenCore's deliberately breakable experiments and living synthesis. Frozen experimental artifacts remain authoritative and are not rewritten when the research framing improves.

## Current one-sentence description

**OpenCore asks whether a persistent learner whose memory also changes evidence exposure can correctly distinguish failure of its current answer from failure of the procedure that produced it.**

## Start here

| Document | Purpose |
| --- | --- |
| [`RESEARCH_FREEZE.md`](RESEARCH_FREEZE.md) | Canonical compact empirical research boundary |
| [`T12E_4B_5_PROOF_CLOSURE.md`](T12E_4B_5_PROOF_CLOSURE.md) | Mathematical Core v0.1 proof closure for anytime adjudication and sharp terminal path-law testing |
| [`T13_1_COVERAGE_OBSTRUCTION.md`](T13_1_COVERAGE_OBSTRUCTION.md) | T13.1 proof: coverage infimum, attainable target regions, and closure-only obstruction |
| [`T13_4_SELF_VALIDATION_FIREWALL.md`](T13_4_SELF_VALIDATION_FIREWALL.md) | T13.4 counterexample: adaptive discovery fit cannot be reused as selection-naive validation |
| [`MATHEMATICAL_CORE_V0.1_THEOREMS.md`](MATHEMATICAL_CORE_V0.1_THEOREMS.md) | Mathematical Core v0.1 theorem lineage through T12e.4a; retained as the theorem-development record |
| [`MAB_OS_DIAGNOSTIC_EXPOSURE.md`](MAB_OS_DIAGNOSTIC_EXPOSURE.md) | Foreign MAB-OS source/world audit, native-horizon pair, negative exposure assay, and next gate |
| [`CSD_001.md`](CSD_001.md) | Frozen CSD apparatus and Mini target negative |
| [`CSD_001_PROCEDURE_ADEQUACY_ARCHAEOLOGY.md`](CSD_001_PROCEDURE_ADEQUACY_ARCHAEOLOGY.md) | Frozen post-negative archaeology |
| [`CORRECTIVE_EXPOSURE_LINEAGE.md`](CORRECTIVE_EXPOSURE_LINEAGE.md) | Blitzcrank -> PCE-001 causal exposure lineage |
| [`docs/EXPERIMENTAL_LINEAGE.md`](docs/EXPERIMENTAL_LINEAGE.md) | Historical crank sequence |
| [`docs/CLAIM_BOUNDARIES.md`](docs/CLAIM_BOUNDARIES.md) | Historical/living claim map; superseded where necessary by the current freeze |
| [`results/README.md`](results/README.md) | Frozen result/artifact index |

## Canonical compact model

```text
1. Preserve alternatives before authority.
2. Preserve causal boundaries before attribution.
3. Preserve independent, discriminating routes by which evidence can overturn confidence.
```

Witness roles:

```text
AF3-OC   preserve the candidate/evidence surface
PCE-001  show persistent state can constrict exposure
MAB-OS   supply native method reliance
```

The unresolved empirical operator is:

```text
observed failure
-> identifying evidence
-> failure attribution
-> method reliance
```

The active empirical question is:

> **When memory changes what a learner gets to observe, can it distinguish “my current answer is failing” from “my way of learning is failing”?**

## Current MAB-OS boundary

The public foreign substrate is pinned for analysis at:

```text
repo    BaratiLab/MAB-OS
commit  f38df7e85d588969005e2f59f2366dfe6a5a9861
blob    MABOS/MABOS.py
        851d6cc7e5e3fafbca381ccf0b0734659cc840ef
K       50
```

Current status:

```text
SOURCE_ADMISSIBLE
WORLD_INTERFACE_ADMISSIBLE
NATIVE_WORLD_PAIR        earned at mechanism-level provenance
DIAGNOSTIC_WORLD_PAIR    not earned
2x2 exposure assay       negative
```

The first native-horizon pair established a world-level WOA adequacy difference while retaining a viable DE alternative. But the forced-DE intervention produced approximately the same native DE evidence in both worlds.

Earned distinction:

```text
counterfactually discriminating
!=
observationally discriminating
```

and the first-principles result:

> **You can restore an evidence channel without restoring identifiability.**

So:

```text
availability
!=
diagnostic information
!=
warranted attribution
```

The next empirical gate is not another selector run. It is a new world-pair certification requiring:

```text
G1  focal-method adequacy differs
G2  learner-visible intervention evidence distinguishes the worlds
G3  the alternative remains viable
```

No selector `R_t`, `Q_t`, or native choice outcome may be used to construct that pair.

## OpenCore-native frozen results

### PCE-001

On the frozen family:

```text
ENDOGENOUS finite T_C:   0 / 256
HAZARD finite T_C:     195 / 256

SUPPORT finite T_C:     64 / 256
FLOOR finite T_C:      205 / 256
```

Earned:

```text
nonzero challenge support
!=
timely corrective exposure
```

### CSD-001 Mini target

```text
FAILURE_CAUSE_CONFLATION
```

Earned:

```text
local unresolvedness
!=
procedure inadequacy
```

and:

```text
R3 measurability
!=
L2 semantic sufficiency
```

Post-negative archaeology:

```text
NO_ADMISSIBLE_PRE_CSD_L2_TARGET_FOUND
```

## Mathematical Core v0.1 — closed-world proof freeze

The mathematical layer remains explicitly quarantined from empirical authority:

```text
mathematical statement
!=
proved theorem
!=
empirical result
```

Adaptive state remains:

```text
S_t = (Pi_t, pi_t, Gamma_t, H_t)
```

with the same three adaptive surfaces:

```text
Pi     what distinctions the system can represent
pi     which experiments / evidence it actually reaches
Gamma  what identified evidence is allowed to change
```

No fourth surface or new primitive was introduced by the proof closure.

The frozen closed-world mathematical hierarchy is:

```text
I*       potential discriminating information
K_n      expected path-space information under the endogenous policy
G_n      predictable information on the realized adaptive action path
L_n      realized likelihood evidence
ROC / testing tradeoff of the finite-horizon path laws
         exact two-sided terminal adjudication property
```

and therefore:

```text
I*
!=
K_n
!=
G_n
!=
L_n
!=
finite-horizon path-law adjudicability
```

The strongest closed-world theorem-level negative remains:

```text
K_n(i->j) -> infinity
and
K_n(j->i) -> infinity

does not imply

consistent discrimination
```

The closed-world theorem-status boundary is:

```text
T12a     PROVED
T12b     CLASSICAL MACHINERY specialized to adaptive path laws
T12c     PROVED EXISTENCE COUNTEREXAMPLE; not a robust policy theorem
T12d     OPEN / DEFERRED
T12e.1   PROVED
T12e.2   PROVED COUNTEREXAMPLE
T12e.3   PROVED UNDER STATED CONDITIONS
T12e.4a  PROVED UNDER EXPLICIT FREEDMAN CONDITIONS; terminal only
T12e.4b  PROVED; Ville likelihood martingales give anytime wrong-attribution control
T12e.5   PROVED WITH RISK-CRITERION CORRECTION
```

### T12e.4b result

For the conditional likelihood-ratio process, constant sequential boundaries give horizon-uniform wrong-attribution control by Ville's inequality:

```text
safe early commitment
!=
guaranteed decision by the deadline
```

A terminal fallback test supplies the missing deadline-completion property without weakening anytime validity.

### T12e.5 correction

Total variation remains exact for **equal-prior average Bayes error**:

```text
R_avg* = (1 - TV(P,Q)) / 2
```

but the stronger requirement

```text
error under H_i <= delta
and
error under H_j <= delta
```

is characterized sharply by the Neyman-Pearson testing tradeoff:

```text
beta_{1-delta}(P,Q) <= delta
```

TV >= 1 - 2 delta is necessary for that two-sided criterion but is not sufficient in general.

Thus the closed-world methodological rule is:

```text
K_n                     information accounting
L_n                     realized evidence
path-law testing risk   adjudication property
anytime-valid early commitment
+ bounded-error terminal fallback
                        timely corrigibility property
```

The theorem-compatible invariant is:

> **Every unresolved consequential distinction must retain a path-law testing regime that permits bounded-error attribution by its consequence-relevant deadline, while any earlier commitment remains anytime-valid at its claimed error level.**

See [`T12E_4B_5_PROOF_CLOSURE.md`](T12E_4B_5_PROOF_CLOSURE.md) for the proofs and the exact scope correction to T12e.5.

## T13 — boundary-expansion proof frontier

T13 is now open only as a mathematical boundary-expansion program. No construction experiment or new permanent control surface is authorized.

Current proof status:

```text
T13.1  coverage / attainability boundary              PROVED
T13.2  constructive reachability                      NEXT
T13.3  selection-aware empirical re-entry             OPEN
T13.4  selection-naive self-validation firewall       PROVED COUNTEREXAMPLE
T13.5  sufficient boundary-expansion / re-entry       OPEN
```

T13.1 establishes the exact tolerance boundary:

```text
epsilon < epsilon_R   -> R*_epsilon is empty
epsilon > epsilon_R   -> R*_epsilon is nonempty
epsilon = epsilon_R   -> nonempty iff the infimum is attained
```

Thus:

```text
empirical closure
!=
attainability at the boundary tolerance
```

T13.4 independently establishes:

```text
selected discovery fit
!=
selection-aware validation
```

The boundary-expansion chain therefore remains:

```text
coverage
-> constructive reachability
-> selection-aware validation
-> fresh CWC
-> scoped authority
```

The next proof target is T13.2. It must operate on an explicit nonempty target region

```text
R*_epsilon = {r : rho(P*,Q_r) <= epsilon}
```

rather than treating the scalar coverage infimum as if it were a constructible candidate.

## Research posture

```text
smallest discriminating assay
-> prospective freeze
-> execute
-> localize shallowest failure
-> preserve the negative
-> revise only what failed
```

Current empirical rule:

> **A diagnostic intervention must make the competing hypotheses distinguishable through the evidence it actually delivers to the system.**

Current mathematical rule:

> **Do not expand the theory to solve a proof problem. Proof failure, counterexample, or a genuinely necessary assumption may revise a theorem; proof inconvenience may not.**

No new architecture, trust variable, procedure-failure label, outer supervisor, or Nano version is authorized.