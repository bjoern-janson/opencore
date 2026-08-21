# OpenCore GW-001 — Guard / Warrant Repair Discrimination

**Status:** `CONSTRUCTED_REPAIR_DISCRIMINATION_RESULT`  
**Scientific role:** attack the live Base-002B wound without modifying Nano V0  
**Nano modified:** `NO`  
**Mini modified:** `NO`
**Publication:** experimental crank branch

## 1. Live wound

Base-002B established a concrete failure of Nano V0:

```text
execution precondition source -> warrant parent
```

is too strong.

In the strict reopening construction, `G_STATUS=EFFECTIVE` must hold for the
reopen transition to execute, but the resulting `G_STATUS=REOPENED` standing
must not depend on the continuing authority of the old `G` receipt that the
same transition revokes.

The earned distinction before GW-001 was:

```text
transition eligibility != post-transition authority provenance
```

What was **not** earned was a particular repair such as adding explicit
`Guard` and `WarrantPremise` schema types.

GW-001 asks whether smaller structural heuristics can explain the wound.

## 2. Competing parent-selection hypotheses

The harness keeps Nano V0's execution-time precondition checks unchanged and
varies only how successful precondition sources become continuing receipt
parents.

Six arms are compared:

```text
NANO_V0
    every satisfied precondition source becomes a warrant parent

SAME_KEY_EXEMPT
    if T writes the same key that a precondition checked, exclude that old
    standing from continuing warrant ancestry

REVOKED_SRC_EXEMPT
    if T revokes the producing license of a precondition source, exclude that
    source from continuing warrant ancestry

SELF_INVALIDATING_EXEMPT
    exclude a checked source only when T both overwrites that same key and
    revokes the source's producing license; this is the narrowest obvious
    Base-002B-specific structural repair

EXPLICIT_SELECTIVE
    every precondition is still checked for execution, but the harness declares
    which checked keys are execution-only; only the remaining checked sources
    become continuing warrant parents

DROP_ALL_PARENTS
    permissive control: check every precondition but retain none as parents
```

`EXPLICIT_SELECTIVE` is a **harness comparator**, not a Nano V1 proposal.

## 3. Four discriminating families

Each family is externally constituted so the intended execution and continuing
authority relationships are explicit.

### 3.1 Strict reopening — Base-002B geometry

Two facts are required to execute:

```text
G_STATUS == EFFECTIVE
E*       == REFUTES_G
```

but the output must depend only on the counterexample:

```text
Parents(REOPENED) = {E*}
```

The transition writes:

```text
G_STATUS = REOPENED
```

and revokes the producing license of old `G`.

Desired behavior:

```text
transition ALLOW
REOPENED remains effective
old G receipt is not a continuing parent
counterexample receipt is a continuing parent
```

This is the original wound. Both special-case heuristics can repair it.

### 3.2 Same-key genuine warrant

A same-key rewrite is constructed where the old standing is a real continuing
warrant:

```text
STAGE=PROVISIONAL -> STAGE=CERTIFIED
```

The transition is licensed because `PROVISIONAL` is effective, and the
constructed contract says `CERTIFIED` must lose current authority if the old
`PROVISIONAL` warrant is later revoked.

Desired behavior:

```text
old same-key receipt remains a warrant parent
later revocation of old warrant -> CERTIFIED becomes deferred
```

This attacks the hypothesis:

```text
same-key precondition => execution-only
```

### 3.3 Same-transition revoked genuine warrant

A different-key source is a genuine continuing warrant even though the same
transition retires that source:

```text
SOURCE=VALID
    -> write RESULT=DERIVED
    -> revoke SOURCE producing license
```

The write is permitted, but because `RESULT` genuinely derives its current
authority from `SOURCE`, it should be immediately deferred after the source
warrant is retired.

Desired behavior:

```text
SOURCE receipt remains a warrant parent
RESULT is deferred immediately after the transition
```

This attacks the hypothesis:

```text
precondition source revoked by T => execution-only
```

### 3.4 Mixed execution guard + genuine warrant

One transition has two simultaneously true, different-key preconditions:

```text
MODE     == OPEN
EVIDENCE == SUPPORTS_RESULT
```

Both must hold for execution.

But their continuing roles differ:

```text
MODE      = execution-only condition
EVIDENCE  = continuing warrant
```

The result should therefore have:

```text
Parents(RESULT) = {EVIDENCE}
```

The assay then independently revokes the two source licenses:

```text
revoke MODE     -> RESULT must remain effective
revoke EVIDENCE -> RESULT must become deferred
```

This is the central GW-001 witness because it requires **selective ancestry
within one precondition list**.

## 4. Final 10,000-world result

Every policy was evaluated on all four families in each of 10,000 worlds.

| Parent policy | Strict reopen | Same-key genuine warrant | Revoked-source genuine warrant | Mixed guard+warrant | All four |
|---|---:|---:|---:|---:|---:|
| Nano V0 | 0 / 10,000 | 10,000 / 10,000 | 10,000 / 10,000 | 0 / 10,000 | 0 / 10,000 |
| Same-key exemption | 10,000 / 10,000 | 0 / 10,000 | 10,000 / 10,000 | 0 / 10,000 | 0 / 10,000 |
| Revoked-source exemption | 10,000 / 10,000 | 10,000 / 10,000 | 0 / 10,000 | 0 / 10,000 | 0 / 10,000 |
| Self-invalidating conjunction | 10,000 / 10,000 | 10,000 / 10,000 | 10,000 / 10,000 | 0 / 10,000 | 0 / 10,000 |
| Explicit selective comparator | 10,000 / 10,000 | 10,000 / 10,000 | 10,000 / 10,000 | 10,000 / 10,000 | **10,000 / 10,000** |
| Drop-all-parents control | 0 / 10,000 | 0 / 10,000 | 0 / 10,000 | 0 / 10,000 | 0 / 10,000 |

No seed-dependent variation was observed.

Frozen Nano V0 still passes its seven-test self-test suite.

## 5. What the experiment earns

GW-001 rejects three attractive structural repairs on the constructed family, including the narrowest obvious Base-002B-specific conjunction:

```text
same-key overwrite exemption
same-transition revoked-source exemption
(same-key overwrite) AND (same-transition source revocation) exemption
```

All three repair Base-002B itself. The conjunction also preserves both genuine-warrant controls, but still fails the independent mixed-role witness.

The strongest narrow result is:

> **On the constructed four-family assay, a single transition can require multiple facts for execution while only a selected subset of those facts should govern the continuing authority of the result. Parent selection therefore cannot be identified with all checked preconditions, nor with the tested same-key, same-transition-revocation, or self-invalidating-conjunction heuristics.**

A compact behavioral witness is:

```text
CheckSet(T) = {MODE, EVIDENCE}
ParentSet(Result(T)) = {EVIDENCE}
```

with the independent interventions:

```text
revoke MODE     -> result stays effective
revoke EVIDENCE -> result loses effective authority
```

This gives stronger support to the semantic distinction:

```text
execution eligibility relationship != continuing authority relationship
```

and shows that the two relationships must be independently selectable **somehow**
on the tested family.

## 6. What is not earned

GW-001 does **not** establish that Nano should literally add:

```text
Guard(...)
WarrantPremise(...)
```

as schema primitives.

It does not establish the correct API, representation, or implementation of
selective ancestry. Other untested mechanisms may reproduce the same behavior.

Therefore:

```text
missing behavioral degree of freedom = SUPPORTED ON CONSTRUCTED FAMILY
specific typed repair                = NOT EARNED
Nano V1                              = NOT OPENED
```

The methodological rule remains:

```text
failure identifies a missing distinction
!=
failure identifies the correct repair
```

GW-001 narrows the repair space; it does not close it.

## 7. Relation to prior Nano wounds

The current forced distinctions are now:

```text
historical lineage       != warrant dependency
preservation obligation  != warrant dependency
execution eligibility    != continuing warrant dependency
```

The third distinction is stronger after GW-001 because the mixed-role witness
shows that two facts can occupy different relationships **inside the same
transition**, despite both being necessary for execution.

## 8. Frozen component identities

```text
nano.py SHA-256
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329

mini.py SHA-256
fd69206eff5443459a8eebed359a301443ae61e92e0e69eb7a1e6ca376ec5e55
```

GW-001 artifacts:

```text
crank/nano_guard_warrant_discrimination.py
crank/results/nano_guard_warrant_discrimination_final_10000.json
```

SHA-256 at final run:

```text
nano_guard_warrant_discrimination.py
57727bec155540213370c45f73d887e8f8a97fdd044e9c526007bdd7d0881c1a

nano_guard_warrant_discrimination_final_10000.json
1b8f45e2a78e716a30830e76755000c6b1749a0176ac0fd609f287fe562bedf9
```

## 9. Current stopping boundary

Do not patch Nano from this result alone.

The next useful pressure would discriminate **representations of selective
authority ancestry**, rather than merely demonstrating the need for selection
again.
