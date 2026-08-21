# CSD-001 — Frozen Analysis Plan

**Status:** `FROZEN_PROSPECTIVE_ANALYSIS`  
**Target mechanism at initial apparatus freeze:** none

## Primary scientific contrast

The eventual target evaluation will compare:

```text
F2  adequate D_agent + bounded stochastic miss
vs
F3  inadequate D_agent
```

after identical certified current-set exposure.

The target must diagnose F3 without diagnosing F2 and before any missing discriminator is disclosed.

## Secondary controls

```text
F1   adequate set + poor prior execution
F3u  truly inadequate set + incomplete warrant
```

F1 detects failure-to-use / failure-of-set conflation.

F3u detects privileged ground-truth guessing or premature diagnosis.

## Prospectively frozen adequacy envelope

```text
D_agent = {c0,c1,c2}
B = 8 valid audit executions per current challenge
```

Adequate worlds must produce at least one representation-preserved h_A/h_B discriminator by completion of this certificate.

The envelope is constituted before any target evaluation and may not be revised from target outcomes.

## Event timing

For each trajectory derive:

```text
T_U
T_W
T_D
T_*
```

A valid F3 diagnosis requires:

```text
T_U <= T_W <= T_D < T_*
```

`T_D - T_W` is reported as diagnostic latency.

## Event-rate reporting

Report separately:

```text
P(DIAG | F1)
P(DIAG | F2)
P(DIAG | F3)
P(DIAG | F3u)
```

Do not combine these into one scalar.

## Apparatus implementation checks

Before any target exists, the harness must verify:

1. pre-transition D_agent adequacy in every family;
2. F1 adequacy under Gamma;
3. F2 adequacy under Gamma for every seed;
4. a non-empty F2 boundary subset with first signal on c2-use B;
5. F3 and F3u have no current-set discriminator;
6. post-endpoint c_star distinguishes F3/F3u;
7. F2/F3 audit schedules are identical;
8. target-visible payloads omit all harness-only labels;
9. F3u ends before the Gamma coverage certificate completes;
10. the same generic FAIL consequence can occur in F1/F2/F3/F3u.

These checks establish only apparatus validity. They do not establish L2.

## Future target-adapter freeze

A later target evaluation must prospectively freeze:

- exact target version/hash;
- adapter mapping from target state/behavior to adequacy withdrawal;
- what downstream behavior makes the withdrawal causal rather than decorative;
- evaluation seeds;
- any target-visible training/calibration exposure;
- no direct reward for the diagnosis;
- stopping and classification thresholds.

No such target is frozen by the initial apparatus implementation.

## Classification discipline

The initial apparatus run may report only:

```text
APPARATUS_READY_FOR_TARGET_FREEZE
```

or:

```text
INVALID_APPARATUS
```

It may not report:

```text
CHALLENGE_SET_INSUFFICIENCY_DIAGNOSIS_ESTABLISHED
```

because no L2 target mechanism is evaluated.

A future target evaluation uses the result classes frozen in CSD_001_SPEC.md.
