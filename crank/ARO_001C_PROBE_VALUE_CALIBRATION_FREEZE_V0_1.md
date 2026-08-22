# ARO-001c — Probe-Value Calibration Freeze v0.1

**Status:** `PROSPECTIVE_IMPLEMENTATION_FREEZE / NOT_RUN`  
**Canonical execution flag:** `STATUS = NOT_RUN`  
**Parent scientific freeze:** `ARO_001_ADAPTIVE_REPRESENTATION_OPERATIONS.md`  
**Parent results:** `ARO_001_V0_1_RESULT.md`, `ARO_001B_V0_1_RESULT.md`  
**Variant:** `ARO-A`  
**Representation invention:** no  
**Operation invention:** no  
**T13 reopened:** no

ARO-001 v0.1 established that perfect static operation control did not imply use of a cheaper supplied sequential information-seeking route. ARO-001b then changed only first-stage probe exposure and obtained:

```text
W3 conditional branch competence    256 / 256
W3 greedy probe preference          240 / 256
```

Thus controlled exposure made the continuation route learnable in every seed while leaving a residual first-stage valuation failure.

ARO-001c asks one narrower question:

\[
\boxed{
\textbf{Does learned first-stage acquisition value track the evaluator-defined
expected downstream value of information?}
}
\]

The intended chain is

\[
\boxed{
\Delta V_{\rm probe}
\longrightarrow
\widehat{\Delta V}_{\mu}
\longrightarrow
\mathbf 1\{\mu_{\rm greedy}=\mathrm{PROBE}_S\}.
}
\]

Because the inherited evaluation policy is greedy, the final behavioral choice is a deterministic thresholding of the learned first-stage Q-values. Therefore ARO-001c does **not** separately identify a learned-value / policy-conversion mechanism. Behavior is reported as seed-level threshold and calibration evidence, not as an independent policy layer.

---

## 1. Invariants inherited from ARO-001b

The following remain unchanged:

```text
representation family P
bounded operation family O
operation semantics
operation costs
Bayes-optimal frozen predictor
ARO-A timing
training objective J = loss + 0.15 * cost
Q initialization = 0
learning rate alpha_Q = 0.10
discount gamma = 1.0
epsilon start = 0.20
epsilon end = 0.01
linear epsilon schedule
256 seeds
4000 training episodes per seed
uniform training distribution over four task descriptors
forced first-stage probe exposure = 0.25 conditional on the W3 training context
second-stage choice remains learned
evaluation remains greedy and unforced
matched empty-information risk gate
claim ceilings
```

Each value condition is trained as its own matched replicate of the four-world ARO-001b assay. The original `W1_G`, `W1_I`, and `W2_XOR` worlds are unchanged. Only the evaluator-controlled value parameter of the fourth world varies.

---

## 2. Matched value family

Retain

\[
G,I,S\overset{\rm iid}{\sim}\operatorname{Bernoulli}(1/2).
\]

For the fourth world introduce one evaluator-side exogenous Bernoulli mode

\[
B_q\sim\operatorname{Bernoulli}(q),
\]

which is never represented to or observed by the learner.

The target in the fourth world is

\[
Y=
\begin{cases}
G,&B_q=0,\\
G,&B_q=1,\ S=0,\\
I,&B_q=1,\ S=1.
\end{cases}
\]

Equivalently, with probability `1-q` the target is `G`; with probability `q` the original gate task is active.

The evaluator prospectively freezes

\[
\boxed{
q\in\{0.60,0.70,0.75,0.80,0.85,0.90\}.
}
\]

Every condition keeps:

```text
P(G,I,S)
probe cost
action set
observation timing
training exposure rule
predictor class
controller class
training horizon
seed set
```

fixed. Only `q`, and therefore the downstream information value of `S`, changes.

The empty-information target remains exactly balanced for every frozen `q`, so the empty-information Bayes 0-1 loss must remain exactly `0.5` in every value condition.

---

## 3. Fixed operations and costs

Exactly as in ARO-001b:

```text
SELECT_G      observe G; terminal                         cost 1.0
SELECT_I      observe I; terminal                         cost 1.0
COMPOSE_GI    observe (G,I); terminal                     cost 1.6
COMPOSE_GIS   observe (G,I,S); terminal                   cost 2.3
PROBE_S       observe S; continue                         cost 1.0
```

After `PROBE_S`:

```text
SELECT_G      additionally observe G                      cost 1.0
SELECT_I      additionally observe I                      cost 1.0
COMPOSE_GI    additionally observe (G,I)                  cost 1.6
```

Sequential cost remains additive.

No operation exposes `B_q`. No new representation or operation is introduced.

---

## 4. True value of information

For each `q`, define

\[
\boxed{
\Delta V_{\rm probe}(q)
=
J^*_{\rm no\ probe}(q)
-
J^*_{\rm probe}(q)
}
\]

where lower `J` is better, so positive `Delta V_probe` means buying the probe is economically preferred.

`J^*_{no probe}` is the exact minimum expected `J` over the supplied one-shot first-stage actions excluding `PROBE_S`.

`J^*_{probe}` is the exact minimum expected `J` over `PROBE_S` followed by an information-matched second-stage action conditional on observed `S`.

The executable must recover the prospectively expected values:

```text
q       true Delta V_probe
0.60    -0.100
0.70    -0.050
0.75    -0.025
0.80     0.000
0.85     0.025
0.90     0.045
```

Thus the family crosses the economic indifference boundary at `q=0.80`.

For every frozen `q > 0.5`, the optimal continuation after probing is prospectively expected to be:

```text
S=0 -> SELECT_G
S=1 -> SELECT_I
```

Continuation competence is an admissibility gate, not an assumed result.

---

## 5. Single retained exposure intervention

Exactly as in ARO-001b, during training only:

\[
\boxed{
P(\text{force }O_1=\mathrm{PROBE}_S\mid W3_q)=0.25.
}
\]

The second-stage action remains learned. The first-stage Q-value of `PROBE_S` remains learned from realized terminal return. Evaluation is never forced.

This conditions the assay on the already-earned fact that continuation competence can become available under controlled probe exposure.

---

## 6. Learned value readout

The Q learner maximizes reward `R=-J`.

For each seed and `q`, define the learned first-stage probe advantage

\[
\boxed{
\widehat{\Delta V}_{\mu}(q)
=
Q_1(W3_q,\mathrm{PROBE}_S)
-
\max_{a\neq\mathrm{PROBE}_S}Q_1(W3_q,a).
}
\]

Positive learned value therefore means the learned first-stage ranking favors probing.

Report, for every `q`:

```text
mean / sd / p05 / median / p95 learned Delta V_hat
W3 correct-branch seed rate
W3 greedy probe-preference seed rate
mean predictive loss
mean cost
mean J regret to the full information-matched oracle
forced probe count
executed probe count
```

The greedy behavioral readout is

\[
\mathbf 1\{\widehat{\Delta V}_{\mu}>0\}
\]

up to deterministic tie-breaking. It is therefore a threshold/calibration readout of learned value, not an independent policy mechanism.

---

## 7. Primary rank-ordering test

The primary scientific target is ordering, not absolute calibration.

Across the six frozen value conditions compute:

```text
rho_Q      = Spearman(true Delta V_probe, mean learned Delta V_hat)
rho_probe  = Spearman(true Delta V_probe, probe-preference seed rate)
```

Primary rank-sensitive VOI evidence requires all of:

```text
R0  continuation branch-full seed rate >= 0.95 in every q condition
R1  executable true Delta V values equal the frozen vector exactly within 1e-12
R2  rho_Q >= 0.90
R3  rho_probe >= 0.90
```

If `R0` fails, the valuation interpretation is blocked because continuation competence was not preserved.

If `R0` passes but `R2` fails, first localize to learned first-stage value formation / credit propagation under the frozen controller.

`R3` is behavioral threshold corroboration. Because behavior is greedy in this controller, `R2` and `R3` are not treated as identifying two independent mechanisms.

---

## 8. Secondary economic-threshold test

Calibration near the true `Delta V = 0` boundary is reported separately from rank ordering.

Secondary calibration requires all of:

```text
C1  mean learned Delta V_hat < 0 at q = 0.60, 0.70, 0.75
C2  abs(mean learned Delta V_hat) <= 0.02 at q = 0.80
C3  mean learned Delta V_hat > 0 at q = 0.85, 0.90
C4  probe-preference seed rate < 0.50 at each negative-VOI q
C5  probe-preference seed rate > 0.50 at each positive-VOI q
C6  probe-preference seed rate is in [0.20, 0.80] at q = 0.80
```

Failure of the calibration gate does not erase a positive rank-ordering result. It means ordering was learned more reliably than the economic switching threshold.

---

## 9. Diagnostic interpretation

Interpret shallowly:

```text
R0 fails
-> continuation-learning / isolation failure; do not infer first-stage VOI calibration

R0 passes, R2 fails
-> first-stage value-learning / temporal credit-propagation failure first

R0 and R2 pass, R3 fails
-> aggregate threshold behavior is unstable despite mean value ordering;
   under this greedy controller this is seed-level value dispersion / tie-threshold instability,
   not a separately identified policy-conversion mechanism

R0-R3 pass, calibration fails
-> rank-sensitive VOI control earned; economic threshold calibration not earned

R0-R3 pass, calibration passes
-> evidence for rank-sensitive and threshold-calibrated first-stage VOI control
```

No outcome licenses representation invention, operation invention, T13 reopening, or ARO taxonomy expansion.

---

## 10. Claim ceiling

A positive primary result may support only:

```text
under this frozen finite supplied-operation family, with controlled probe exposure
and learned continuation actions, the controller's learned first-stage acquisition
value is rank-sensitive to evaluator-defined downstream information value.
```

A positive secondary result may additionally support:

```text
the learned acquisition ranking switches near the evaluator-defined economic
indifference boundary in this assay.
```

It does not establish:

```text
general value-of-information reasoning
representation understanding
causal diagnosis
representation invention
operation invention
ARO-B preparedness
safe authority transfer
T13 success
```

---

## 11. Execution constitution

Before execution, freeze:

```text
q grid = [0.60, 0.70, 0.75, 0.80, 0.85, 0.90]
world law including evaluator-side B_q
all inherited ARO-001b controller and operation constants
alpha_probe = 0.25 conditional on W3_q training episodes
256 seeds per q condition
4000 training episodes per seed
same seed labels reused across q conditions
learned Delta V_hat definition
rank metrics
calibration metrics
all thresholds above
```

The executable and repository-native execution workflow are committed before any ARO-001c result is observed.

Any modification after result inspection creates a new version and cannot be reported as ARO-001c v0.1.
