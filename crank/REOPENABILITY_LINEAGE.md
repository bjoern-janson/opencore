# OpenCore Reopenability Lineage — FOREIGN-005 / FOREIGN-006

**Publication status:** append-only experimental lineage record  
**Historical target branch:** `opencore/crank-mini-001`  
**Current continuation:** `TOPOLOGICAL_REOPENABILITY_LINEAGE.md` -> `CORRECTIVE_EXPOSURE_LINEAGE.md` on `opencore/pce-001`  
**Architecture change in FOREIGN-005/006:** none  
**Nano change in FOREIGN-005/006:** none

> This file remains the detailed custody record for FOREIGN-005/006. Later topology, Blitzcrank, and PCE-001 results do not rewrite these frozen assay claims; they continue the lineage in the documents named above.

Frozen Nano SHA-256 throughout both assays:

```text
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

## Result geometry

```text
FOREIGN-003  future-relevant quotient collapse -> wound
FOREIGN-004  tested-safe historical quotient    -> safe quotient
FOREIGN-005  safe effective quotient + latent opaque source -> reopenable quotient
FOREIGN-006  blind compressed latent + bounded unknown future selector -> rank-capacity boundary
```

The progression supports, only on the frozen constructed families:

```text
safe effective compression != irreversible information destruction
reopenability itself can be compressed relative to a bounded future interface class
```

No universal memory law, reopenability primitive, automatic compressor, automatic interface invention, Nano repair, or architectural change is claimed.

---

## Publication transport

For connector transport, each assay's complete local execution directory is also published as a deterministic `tar.gz` bundle with sorted members, zero mtimes, normalized ownership/modes, and an empty gzip filename. This does not replace the browsable scientific record/spec/harness files; it preserves the exact result/log/nonce artifacts in one lossless transport object.

```text
foreign_005_bundle.tar.gz
SHA-256 a8e9326844c896abf1e4e1722d79b73a1b8afc67e4691f225b84b0064e60bbb5

foreign_006_bundle.tar.gz
SHA-256 719b0c3ee06a71743bdbcd3fd7144d38aa3e4f07c9754865f53bef095ee5322a
```

Bundle extraction reconstructs the exact raw files whose individual SHA-256 values are recorded below.

```bash
mkdir foreign_006_bundle
tar -xzf crank/results/foreign_006_bundle.tar.gz -C foreign_006_bundle
sha256sum foreign_006_bundle/foreign_006_result_v2.json
```

---

## FOREIGN-005 — Reopenable Quotient

Classification:

```text
REOPENABLE_QUOTIENT_ESTABLISHED
```

Core witness:

```text
H_A != H_B
H_A ~_{Q0} H_B
Q0 = {mean, energy}
M*(H_A) = -3
M*(H_B) =  1
N*(H_A) = N*(H_B) = 4
```

Before `M*`, reopenable and destructive branches had identical effective standing state. Only the reopenable branch retained opaque source payloads. After `M*`, that branch reconstructed and persisted the new distinction; the destructive branch was non-identifiable and Nano deferred unsupported refinement. The null `N*` interface did not cause a split.

Checks:

```text
formal:       8 / 8 PASS
persistence: 28 / 28 PASS
```

### Execution-plumbing provenance

The original frozen harness failed before Nano construction under Python 3.13 because the dynamically imported module was not registered in `sys.modules`. No assay transition ran. V2 changed only the dynamic-loader plumbing and was frozen before the successful scientific execution.

### FOREIGN-005 SHA-256

```text
FOREIGN_005_SPEC.md
3ee7955a8f5eb6811473d7a89d5c0ddc1aad195a0aa43cab913b4af261d3cf68

FOREIGN_005.md
bb55648f881eadb6623a973f35332f4ee79f8e792c2f20fb78e8fccaff3511cc

foreign_005.py
 a3985d79dcfecaf7e8aa2a0ad99177997bff4e36194417c3bcde8fd119b13dab

foreign_005_v2.py
342e2d3da2357ea1d6aaa56417ab841dec5ec6d8a97cb4259b825695d7364e2d

foreign_005_result.json
6eafb08d9fefa84d3f1ee864fffe73c818435881890e9b8f0d21f0ef7ffa5d31

run.log
9b2dfc79e602471a940f3104c5878b06ddf7da86452fd8643252795ec70615cf

run_v2.log
dfed2a012f5f8bffb977c1d2114ca1e6b2750293856c56d9e30792b211aff1e6
```

---

## FOREIGN-006 — Blind Reopenability Under a Bounded Future Interface Class

Classification:

```text
DISTINGUISHING_RANK_BOUNDARY_ESTABLISHED
BLIND_REOPENABILITY_ESTABLISHED
```

Frozen family:

```text
H in F_2^64
|M| = 24
rank(A) = 6
```

Retention regimes:

```text
raw archive:        64 bits
blind compressed:    6 bits
undersized control:  5 bits
destructive:          0 future-distinguishing bits
```

The Phase-A latent artifact was serialized and SHA-256 sealed before any reveal nonce existed. Only after the seal was fixed was a fresh nonce generated and the selected future interface derived from `SHA256(phase_a_artifact_bytes || reveal_nonce) mod 24`.

Phase-A checks:

```text
13 / 13 PASS
selector present: false
```

Complete-family audit over all 64 pre-frozen histories:

```text
raw archive exact:       24 / 24
blind 6-bit exact:       24 / 24
undersized 5-bit exact:  15 / 24
undersized 5-bit lost:    9 / 24
```

The 24-interface family induced exactly 64 joint future-response profiles. Therefore, for this frozen deterministic fixed-length binary linear family, any exact latent requires at least `ceil(log2(64)) = 6` bits. The six-bit blind representation met that bound exactly.

Successful final checks:

```text
formal/capacity: 22 / 22 PASS
persistence:     17 / 17 PASS
```

### Harness-assertion provenance

The original Phase-B scientific calculations already produced `22 / 22` formal checks, but two persistence assertions compared tuple-valued `parent_receipts` against Python lists, yielding `15 / 17`. The actual receipt contents were correct. V2 changed only those assertion literal container types. Phase A was not rerun, the reveal nonce was not regenerated, and the selected interface was not changed.

### FOREIGN-006 SHA-256

```text
FOREIGN_006_SPEC.md
80e57352a36301e617310e10cb11acda03008c49f715f2131316bda03745a848

FOREIGN_006.md
74d7ea43bdc5bc7a18087e23ad0b114505cff69bcf9ef4822b48d5a8f1b0d0ee

foreign_006.py
fb202e13214524759d57a0d69a018dd3b9ebfd29620568969271c6cb4fdc52e2

foreign_006_v2.py
7abfb4ae76e83475ee772428231c1aa51114433bd9812c7914dcdc07bcb1dadb

phase_a_latent.json
2d7226395bf086efb7d8badd03a33968955ac4e30738e74ebc93f35b418ba342

reveal_nonce.txt
366add04221364f2b1d5e5ce828be4c753eb83d38bca40f9dacc01de6c75512f

foreign_006_result.json (original assertion run)
a2d45f79769e6c3d28c4c7868b64aaa20dda1adc5a11631a33fd25c6f4062cfa

foreign_006_result_v2.json (canonical successful result)
29c4e184875733a75c9f79dbe0d042298a2826563216868d49a355c4a06085d5

FOREIGN_006_SHA256.txt
4e253a057a6935480b748e8213169b2a528b5fdce58becb1fc9799fdb59a440a

phase_a.log
0394d555b23473b6d06c1a00c606aaa0dda93b61b2d76d38acff438db9077e91

phase_b.log
190c891986e0066ee7c40a407fba72036403562aeab6e7b13584010b64abc111

phase_b_v2.log
fedd940f0dcd1a7623d23466752ba197039d9aa0d9e3dfc5bc10d67792e7919a
```

## Current candidate — not a law

The combined pressure now supports further investigation of:

```text
required reopenable capacity
~ future distinguishing complexity
```

rather than raw history size or raw future-probe count.

FOREIGN-006 establishes the exact equality with `rank(A)` only for its prospectively bounded deterministic fixed-length binary linear family. Nonlinear, stochastic, approximate, continuous, variable-length, learned-family, and unbounded-interface cases remain open.

## Claim ceiling

Not earned by FOREIGN-005/006:

- universal archivalism;
- universal reopenable memory architecture;
- a general law equating memory with linear rank;
- a new `HistoryID`, `AcquisitionPath`, reopenability, oscillatory, or instrument primitive;
- automatic discovery of admissible future interface classes;
- automatic compression;
- automatic interface invention;
- automatic quotient refinement;
- Nano V1 or any Nano repair;
- neural or biological memory mechanism;
- physical ontology.
