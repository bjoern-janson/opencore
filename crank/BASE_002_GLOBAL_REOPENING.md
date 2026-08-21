# OpenCore Base-002 — Global Reopening

**Status:** `PARTIAL_POSITIVE_WITH_KERNEL_NEGATIVE_RESULT`  
**Scientific role:** constructed Base-level assay separating `ADMIT(G)`, `REOPEN(G)`, and `REPLACE(G,G')`  
**Nano modified:** `NO`  
**Base-001 modified:** `NO`  
**Publication:** experimental crank branch

## 1. Question

Can one globally available counterexample withdraw the current authority of a shared invariant and thereby propagate uncertainty through heterogeneous local cognition, while lacking authority to install a successor invariant until separately authorized later evidence exists?

The intended separation is:

```text
ADMIT(G) != REOPEN(G) != REPLACE(G,G')
```

and specifically:

```text
Auth(e*, REOPEN(G)) !=> Auth(e*, REPLACE(G,G'))
```

Base-002 reuses the 12-unit heterogeneous world geometry from Base-001 and Nano V0 unchanged.

## 2. Frozen component identities

```text
nano.py SHA-256
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329

base_001_shared_world.py SHA-256
e8b435da6b3e18a7d718d5add22d2c7575e23bae787bf92f3dc99827f9bc1463
```

Both remained byte-identical through Base-002. Nano's seven frozen self-tests still pass.

## 3. Constructed sequence

Each world contains 12 local units, 8 externally designated relevant to `G` and 4 irrelevant.

The assay performs:

```text
1. ADMIT(G)
   -> G content + G_STATUS=EFFECTIVE

2. Relevant units derive H_i from G_STATUS=EFFECTIVE.

3. All 12 units learn unrelated L_i after G with no G precondition.

4. Admit counterexample e* with externally constituted role REFUTES_G.

5. REOPEN(G)
   -> write G_STATUS=REOPENED
   -> revoke G's producing license
   -> issue no H_i/L_i cleanup writes or deletes

6. Using the same reopen capability, attempt to install G'.
   -> naive persistence ALLOW
   -> Nano DENY: replacement write outside effect envelope

7. Using the authentic replacement license before later evidence E' exists:
   -> naive persistence ALLOW
   -> Nano DEFER: successor evidence unestablished

8. Preserve the REOPENED world across an unrelated checkpoint transition.

9. Admit later evidence E' with role SUPPORTS_GPRIME.

10. REPLACE(G,G') under the separate replacement license.

11. Relevant units derive successor-specific K_i from G'.
```

## 4. Base-002A — target-bound global reopening

The first construction gives the reopen license explicit authority over the particular G-producing license and the G status key. Its warrant premise is the counterexample `e*`; it does **not** additionally list `G_STATUS=EFFECTIVE` as a precondition.

That matters for the negative control in section 6.

Across 10,000 worlds:

| Measure | Result |
|---|---:|
| Reopen transition allowed | 10,000 / 10,000 |
| `REOPENED` status effective | 10,000 / 10,000 |
| `REOPENED` survives unrelated checkpoint | 10,000 / 10,000 |
| Old G content withdrawn from effective state | 10,000 / 10,000 |
| G-derived H_i authority withdrawn | 80,000 / 80,000 |
| Relevant units enter constructed uncertainty projection | 80,000 / 80,000 |
| Irrelevant-unit reopening disturbance | 0 / 40,000 |
| Unrelated post-G L_i retained after reopen | 120,000 / 120,000 |
| G' absent before later evidence | 10,000 / 10,000 |
| Independent post-G L_i receipts parentless | 10,000 / 10,000 worlds |

The active `REOPENED` status is warranted by the counterexample receipt, not by the now-invalidated G receipt.

Thus, on this target-bound construction:

```text
historical G remains in the journal
current G authority is withdrawn
REOPENED remains effective
G-derived consequences lose effective authority
unrelated later learning remains effective
```

No local destructive cleanup is required.

## 5. Refutation authority does not become replacement authority

### Same counterexample / same reopen capability

After reopening, the same counterexample-backed reopen capability attempts to write `G'`.

Across 10,000 worlds:

```text
naive persistence: 10,000 / 10,000 ALLOW
Nano V0:                 0 / 10,000 ALLOW
Nano V0:            10,000 / 10,000 DENY
```

The denial reason is specifically:

```text
effect:write_not_licensed
```

The counterexample's reopening authority does not contain successor-install authority.

### Authentic replacement capability before E'

A separate authentic replacement license exists, but requires:

```text
G_STATUS = REOPENED
E'       = SUPPORTS_GPRIME
```

Before E' exists:

```text
naive persistence: 10,000 / 10,000 ALLOW
Nano V0:            10,000 / 10,000 DEFER
```

The Nano reason is specifically an unestablished successor-evidence precondition.

After E' is separately admitted:

```text
Nano V0 replacement: 10,000 / 10,000 ALLOW
```

Every replacement receipt has both:

```text
REOPENED status receipt as a parent
later-evidence E' receipt as a parent
```

Relevant successor projections then materialize in 80,000/80,000 cases, irrelevant units remain undisturbed in 40,000/40,000 cases, unrelated L_i remain live in 120,000/120,000 cases, and old G-derived H_i remain withdrawn in 80,000/80,000 cases.

This constructed path therefore supports:

```text
G effective
  -> e*
G reopened
  -> distributed uncertainty
  -> E'
G' installed
```

without allowing `e*` alone to manufacture G'.

## 6. Negative result — strict reopening self-invalidates

Before freezing the positive result, a stricter and more natural contract was tested.

A strict reopening transition plausibly wants to require both:

```text
e*       = REFUTES_G
G_STATUS = EFFECTIVE
```

before it may execute.

But Nano V0 currently has one precondition class. Its `_parents_for()` rule treats **every precondition source receipt as a warrant parent** of the resulting standing.

Therefore the strict reopen receipt acquires:

```text
parent 1 = counterexample e*
parent 2 = old G_STATUS=EFFECTIVE receipt
```

The same transition then revokes G's producing license.

Result across 10,000 strict controls:

```text
strict reopen transition decision = ALLOW     10,000 / 10,000
new REOPENED standing active       =              0 / 10,000
new REOPENED standing deferred     =         10,000 / 10,000
old G included as warrant parent   =         10,000 / 10,000
counterexample included as parent  =         10,000 / 10,000
```

So the transition succeeds syntactically and immediately destroys the effective authority of its own output.

The concrete failure is:

```text
transition eligibility condition
!=
authority / warrant dependency
```

or, operationally:

```text
"G must currently be effective for this transition to make sense"
!=
"the authority of the resulting REOPENED standing must continue to depend on G"
```

This is distinct from Nano V0's earlier separation:

```text
preservation obligation != warrant dependency
```

Base-002 exposes a second dependency-type collapse:

```text
execution guard != warrant-bearing premise
```

No repair is made here.

## 7. Failure localization

The shallow failure locus is the Nano V0 transition-contract representation / dependency-construction mechanism:

```text
License.preconditions
        |
        +-- used for execution-time checking
        |
        +-- automatically promoted to receipt warrant parents
```

Base-002 demonstrates a case where those two roles should not automatically coincide.

A future repair might require typed preconditions, explicit warrant-parent declaration, or some other separation, but **no representation choice is earned by this assay alone**.

Nano V0 remains frozen.

## 8. What Base-002 actually earned

### Supported on the constructed family

> **With an externally target-bound reopen capability whose warrant derives from a counterexample rather than from the invalidated incumbent, a shared invariant can be globally reopened, its warrant-dependent local consequences can lose effective authority without destructive cleanup, the counterexample cannot install a successor, and separately authorized later evidence can install that successor.**

### Negative result

> **Nano V0 cannot simultaneously encode the natural strict guard `G_STATUS=EFFECTIVE` as an ordinary precondition and keep the resulting `REOPENED` standing effective after revoking G, because every precondition is currently promoted to warrant ancestry.**

These two statements must remain together.

## 9. Claim ceiling

Not established:

```text
GENERAL GLOBAL REOPENING                  NOT_ESTABLISHED
AUTONOMOUS COUNTEREXAMPLE CONSTITUTION     NOT_ESTABLISHED
AUTONOMOUS SUCCESSOR DISCOVERY             NOT_ESTABLISHED
AUTONOMOUS RELEVANCE DISCOVERY             NOT_ESTABLISHED
DISTRIBUTED LEARNING GENERALLY             NOT_ESTABLISHED
GENERAL OPENCORE BASE                      NOT_ESTABLISHED
CORRECT PRECONDITION/WARRANT TYPE SYSTEM   NOT_ESTABLISHED
NANO V1 REPAIR                             NOT_OPENED
CRASH-DURABLE REOPENED WORLD STATE         NOT_ESTABLISHED
```

The local projection map, relevance map, counterexample role, later-evidence role, and all licenses are external harness scaffolding.

`REOPENED` persistence here means current in-process Nano standing. Nano V0 crash durability remains unestablished.

## 10. Execution provenance

The final population is exactly seeds `0..9999`.

Because the execution environment terminates a single long CLI process before the full 10,000-world sweep completes, the population was executed as five disjoint calls to the unchanged `sweep()` path:

```text
0..1999
2000..3999
4000..5999
6000..7999
8000..9999
```

Additive counts were summed and metrics recomputed using the same frozen formulas. No seed was duplicated or omitted.

## 11. Artifacts

```text
crank/base_002_global_reopening.py
crank/results/base_002_global_reopening_final_10000.json
```

Hashes:

```text
base_002_global_reopening.py
babfbf78b70be7dad43a571e7ce2d4642d8437a93af3fde175eb274ab7477b83

base_002_global_reopening_final_10000.json
0e6fb9f96228d8c169effa87b57805e2c2876b90043d7d55553ec1b9923e8fd2
```

## 12. Current disposition

```text
BASE_002_TARGET_BOUND_REOPENING = SUPPORTED_ON_CONSTRUCTED_12_UNIT_FAMILY
BASE_002_STRICT_REOPENING       = FAILED_ON_NANO_V0
NANO_V0                         = UNCHANGED
NANO_V1                         = NOT_OPENED
NEXT EXPERIMENT                 = NOT_IMPLIED
```

The strongest new implementation distinction is:

```text
execution guard != warrant dependency
```

Base-002 therefore does not merely add a new Base behavior. It exposes a concrete place where Nano V0's current contract surface is too coarse.
