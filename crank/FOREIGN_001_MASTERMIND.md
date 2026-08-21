# FOREIGN-001 — Frozen OpenCore Stack Under Mastermind Pressure

**Status:** `FOREIGN_PRESSURE_RESULT_WITH_TWO_LOCALIZED_BLOCKAGES`  
**Task family:** reduced Mastermind plus adaptive/dynamic Mastermind  
**OpenCore-native task design:** `NO`  
**Mini modified:** `NO`  
**Nano modified:** `NO`  
**Publication:** experimental crank branch

## 1. Purpose

FOREIGN-001 is the first crank assay deliberately chosen from outside the OpenCore toy lineage.

The experiment does not ask whether OpenCore can score well on a benchmark. It asks:

> **Where does corrective flow stop when the frozen Base + Mini + Nano picture is exposed to a task whose semantics and failure geometry were not designed around OpenCore?**

The frozen classifier is:

```text
insufficient evidence
|
insufficient authority
|
earned distinction / relation not expressible
```

No repair is performed in this experiment.

## 2. Foreign task

The task is Mastermind, reduced to the smallest exhaustive form that preserves the standard feedback semantics:

```text
positions = 2
colors = 3
repetition allowed
possible hidden codes = 3^2 = 9
possible guesses = 9
```

A guess receives the standard two-part response:

```text
black = correct color in correct position
white = correct color in wrong position
```

The reduced game has exactly five possible feedback classes:

```text
(0,0), (0,1), (0,2), (1,0), (2,0)
```

Two arms are used.

### STATIC

One hidden code remains fixed for the complete game.

### DYNAMIC

The codemaker is allowed to change its hidden code while preserving a non-empty set of codes consistent with the complete public feedback history.

The instantiated adversary chooses feedback leaving the largest surviving candidate set and changes its internal representative secret whenever possible.

This is a diagnostic realization of the pre-existing adaptive/dynamic Mastermind idea, not an OpenCore-native world-change mechanism.

## 3. Lossless boundary adapter

The adapter deliberately performs no Mastermind inference.

Each guess is encoded injectively as:

```text
x = base-3 index in {0,...,8}
```

Each of the five feedback classes is encoded injectively as:

```text
y in {0,...,4}
```

Therefore the foreign observation fits Mini's existing scalar observation surface without dropping task information:

```text
MM: x -> y
```

The adapter does not propose candidate codes, eliminate hypotheses for Mini, or translate Mastermind structure into affine structure.

A separate Mastermind candidate-set calculation is used only as a diagnostic oracle to answer whether the external evidence is already sufficient under the foreign task's own semantics.

## 4. Frozen stack use

### Mini

Frozen `mini.py` receives the losslessly encoded foreign feedback through one scope:

```text
scope = MM
```

Mini retains its original hypothesis family:

```text
y = ax + c mod 11

a in {1,...,10}
c in {0,...,10}
```

No Mastermind-specific cognition is inserted.

### Nano

When Mini emits a commitment or reopen commitment, the harness proposes exactly that current Mini rule as a `mini-model` standing.

Nano receives a narrow external license permitting persistence of a Mini-model standing while the foreign source role is `EXTERNAL_MASTERMIND_FEEDBACK`.

The contract does **not** assert that the Mini model is true. It authorizes persistence of the organism's current model under the supplied role contract.

### Base

Base is instantiated minimally as the currently effective shared Nano world rather than by importing the Base-001 12-unit geometry.

A task-facing projection reads the effective shared `mini-model` standing and uses it to predict the next encoded feedback.

Thus the path is:

```text
foreign feedback
-> Mini candidate / reopen
-> Nano-licensed mini-model persistence
-> effective shared world
-> task-facing prediction
```

## 5. Pre-run representability check

The foreign relation is outside frozen Mini's hypothesis class for a structural reason.

Every Mini rule has non-zero slope modulo 11 and is therefore injective on distinct inputs.

But for every one of the nine Mastermind secrets, multiple different guesses produce the same feedback class.

Exhaustive check:

```text
Mastermind secrets tested                       9
Mini affine hypotheses tested                 110
all foreign feedback functions have collisions YES
all Mini rules injective on x=0..8             YES
foreign functions representable by Mini          0 / 9
```

So the lossless task adapter does not merely happen to choose an unfortunate numeric encoding. Any injective encoding of feedback classes preserves equality of repeated feedback values, while the frozen Mini rule family cannot map two distinct inputs to the same output.

This establishes the foreign-task expressivity mismatch independently of the subsequent behavioral sweep.

## 6. STATIC arm — 10,000 worlds

Each world uses one fixed secret and a random order over all nine possible guesses.

### Evidence sufficiency

The foreign-task oracle reaches a unique secret in:

```text
10,000 / 10,000 worlds
```

Mean first unique step:

```text
2.0976 probes
```

Therefore by the end of every game, the public foreign evidence is sufficient to identify the hidden code under Mastermind semantics.

### Authority path

Explicit Nano execution-time authority control:

```text
ALLOW 10,000 / 10,000
```

All actual Mini model persistence proposals were also admitted:

```text
20,746 / 20,746 ALLOW
0 DENY
0 DEFER
```

Therefore the foreign failure is not caused by Nano refusing an otherwise expressible Mini model.

### Mini / Base behavior

```text
Mini ever committed                7,634 / 10,000
Mini commit events                20,746
Mini reopen events                13,112
Mini final needs-probe             7,048 / 10,000
Mini final globally consistent         0 / 10,000
```

The effective shared model produced:

```text
53,438 task-facing predictions
 2,603 correct
50,835 wrong
36,562 abstentions before an effective model existed
```

Prediction accuracy conditional on an effective Mini model:

```text
0.04871
```

This score is descriptive only; FOREIGN-001 is not a performance benchmark.

### Static classification

Every world simultaneously satisfies:

```text
foreign evidence sufficient                YES
Nano model-persistence authority live      YES
globally consistent Mini hypothesis exists NO
```

Therefore:

```text
EXPRESSIVE BLOCK AFTER SUFFICIENT EVIDENCE
10,000 / 10,000
```

The blockage is localized to the frozen organism/hypothesis representation, not Nano.

This does not establish that Mini should be generalized or replaced. Mini was already explicitly domain-specific. FOREIGN-001 supplies a foreign-task causal witness of that boundary.

## 7. DYNAMIC arm — 10,000 worlds

The same random-probe geometry is used, but the codemaker changes its internal representative secret whenever possible while keeping every public response jointly consistent.

### Hidden mechanism actually changes

```text
worlds with >=1 hidden secret change    10,000 / 10,000
hidden secret changes total             24,236
mean hidden secret changes / world       2.4236
```

### Yet the public history does not identify that change

Every complete dynamic trace remains exactly compatible with at least one single static code:

```text
10,000 / 10,000
```

The same public observations therefore admit both:

```text
static hidden code
```

and an actually changing hidden mechanism.

An interface-only learner is not entitled to infer the hidden change from this feedback stream.

This is a separate foreign-task result:

```text
mechanism change occurred
!=
mechanism change identifiable from standard task feedback
```

### Evidence for current code state

The candidate set nonetheless becomes unique in:

```text
10,000 / 10,000 worlds
```

Mean first unique step:

```text
2.8862 probes
```

### Authority path

```text
explicit authority control        10,000 / 10,000 ALLOW
Mini model persistence            23,466 / 23,466 ALLOW
DENY                                    0
DEFER                                   0
```

### Mini / Base behavior

```text
Mini ever committed                8,278 / 10,000
Mini commit events                23,466
Mini reopen events                15,188
Mini final needs-probe             7,595 / 10,000
Mini final globally consistent         0 / 10,000
```

Shared-world predictions:

```text
57,946 predictions
 2,643 correct
55,303 wrong
32,054 abstentions
```

Again, the score is descriptive only.

### Dynamic classification

The dynamic arm contains two independently localized limits.

#### A. Expressive blockage

Same as STATIC:

```text
sufficient task evidence + live authority path + no representable Mini model
= 10,000 / 10,000 expressive block
```

#### B. Evidence/interface non-identifiability

Despite actual hidden mechanism change:

```text
public feedback history remains compatible with a static code
= 10,000 / 10,000
```

Therefore the correct response to the hidden shift is **not** to grant Mini more authority to declare a distribution shift.

The task interface has not earned that distinction.

## 8. What FOREIGN-001 supports

### Result F1 — foreign expressive boundary

On this reduced Mastermind family:

> **The frozen stack receives losslessly encoded external feedback, reaches states where the foreign task's own evidence uniquely identifies the hidden code, and has a live Nano persistence path, but frozen Mini has no hypothesis capable of representing the foreign guess-to-feedback relation. Corrective flow therefore stops at the organism's hypothesis representation before the persistence boundary.**

This is a foreign-task witness of an already explicit Mini limitation, not a claim that the OpenCore architecture generally fails outside affine domains.

### Result F2 — hidden change is not automatically observable change

On the adaptive/dynamic arm:

> **The hidden generating mechanism changed in every tested world while every public feedback history remained exactly compatible with a static hidden code. Mechanism shift therefore did not acquire identification authority through the standard Mastermind feedback interface.**

This independently reproduces the discipline:

```text
real hidden difference
!=
observable identifying difference
```

## 9. The three-way blockage classifier survived this pressure

FOREIGN-001 produces examples of two of the frozen categories without needing to invent a fourth.

### Expressive blockage

```text
STATIC / DYNAMIC Mini failure
-> evidence sufficient
-> authority path live
-> required foreign relation unavailable in hypothesis topology
```

### Evidence/interface blockage

```text
DYNAMIC hidden change
-> change occurred in generating process
-> public feedback does not identify that change
-> no authority to infer hidden mechanism transition
```

### Authority blockage

Not observed in this assay.

Nano admitted every in-contract Mini-model proposal and every explicit authority-control check.

This is important negative localization:

```text
FOREIGN-001 does not pressure a Nano repair.
```

## 10. What did not happen

```text
Nano V1 opened                               NO
Mini modified                                NO
Base-001 scaffold imported                   NO
Mastermind solver inserted into Mini         NO
hidden dynamic shift granted by fiat         NO
foreign-task performance claim               NO
generalization claim                         NO
```

No architectural repair is earned by this result.

The immediate blockage occurs at a boundary already known to be narrow: Mini's fixed affine hypothesis family.

## 11. Regression / integrity

Frozen identities after the final run:

```text
mini.py
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55

nano.py
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

Regressions:

```text
Mini native 10,000-seed sweep  10,000 pass / 0 fail
Nano frozen tests              7 / 7 pass
```

## 12. Claim ceiling

FOREIGN-001 does **not** establish:

```text
OpenCore general foreign-task competence
Mastermind solving competence
need for a general-purpose Mini
need for Nano changes
need for Base changes
correct representation for foreign task cognition
autonomous task-interface invention
distribution-shift detection
hidden-mechanism identification
reliable generalization
```

The narrow result is simply that independent foreign pressure reached the frozen stack and localized where correction stopped.

## 13. Artifacts

```text
crank/foreign_001_mastermind.py
crank/results/foreign_001_mastermind_final_10000.json
```

SHA-256:

```text
foreign_001_mastermind.py
6d736cd3eba4a51df56bbf8fa2fa5328dec32f0bf90e8090b5c5f1111106dca6

foreign_001_mastermind_final_10000.json
8c2d42f62b9276e36846722fb7ade6fa248a47641e45ac48fe673d3227bf8c56
```

## 14. Current posture

The foreign pressure did not reveal a reason to repair Nano.

It showed first that the frozen organism is not a task-neutral cognitive surface, and second that a genuine hidden mechanism shift can remain unidentifiable through a foreign task's observation channel.

Therefore the next scientific move is **not** to generalize Mini merely to make Mastermind work.

The wound remains:

```text
foreign relation required
-> current organism cannot express it
```

but the correct replacement organism/interface is not identified by this experiment.

Water found the first foreign obstruction. It still did not design the pipe.
