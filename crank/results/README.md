# Crank Result Snapshots

This directory contains result snapshots, deterministic bundles, compact indexes, and artifact commitments used by published crank scientific records.

These artifacts are evidence for specific frozen assays. They are not universal benchmark claims and do not amend formal K0/E001 artifacts.

## Published decisive results

| Artifact | Role |
| --- | --- |
| [`nano_attack_matrix_final_10000.json`](nano_attack_matrix_final_10000.json) | Final strengthened isolated Nano V0 six-family matrix |
| [`nano_experiment_v0_results.json`](nano_experiment_v0_results.json) | Compact Nano V0 result bundle and hashes |
| [`mini_nano_composition_final_10000.json`](mini_nano_composition_final_10000.json) | Final 10,000-seed wounded Mini × Nano composition suite |
| [`nano_mini_ablation_final_10000.json`](nano_mini_ablation_final_10000.json) | Final 10,000-seed subtractive persistence-boundary ablation |
| [`base_001_shared_world_final_10000.json`](base_001_shared_world_final_10000.json) | Final 10,000-world Base-001 shared-world assay |
| [`base_002_global_reopening_final_10000.json`](base_002_global_reopening_final_10000.json) | Final Base-002 global-reopening assay including strict negative control |
| [`nano_guard_warrant_discrimination_final_10000.json`](nano_guard_warrant_discrimination_final_10000.json) | Final GW-001 repair-discrimination assay |
| [`foreign_001_mastermind_final_10000.json`](foreign_001_mastermind_final_10000.json) | FOREIGN-001 Mastermind pressure assay |
| [`foreign_002_restless_bandit_final_10000.json`](foreign_002_restless_bandit_final_10000.json) | FOREIGN-002 restless-bandit pressure assay |
| [`foreign_003_result.json.gz`](foreign_003_result.json.gz) | Deterministic compressed FOREIGN-003 classical quotient-failure result |
| [`foreign_004_result.json.gz`](foreign_004_result.json.gz) | Deterministic compressed FOREIGN-004 safe-quotient result |
| [`foreign_005_bundle.tar.gz`](foreign_005_bundle.tar.gz) | Deterministic lossless FOREIGN-005 execution bundle |
| [`foreign_006_bundle.tar.gz`](foreign_006_bundle.tar.gz) | Deterministic lossless FOREIGN-006 execution bundle |
| [`pce_001_result_index.json`](pce_001_result_index.json) | Compact PCE-001 completed-run summary and full-result hash commitment |
| [`pce_001_trace_commitment.json`](pce_001_trace_commitment.json) | PCE-001 canonical 368,640-record trace commitment and regeneration metadata |

Additional OQ and AF3 compact results in this directory are governed by their corresponding scientific records in `../`.

## PCE-001 custody

PCE-001 was prospectively frozen before evaluation at commit:

```text
b26cd933f38f96acb53d9590e3a5d2055b3c4382
```

The canonical full trace contains:

```text
368,640 records
```

Commitment:

```text
uncompressed SHA-256:
d9d263930fef627b059e18690af76ae2f0469d788760c0f328742d8617f6e816

deterministic gzip SHA-256:
7a03aedff6b50e1309baf08bd7f403d9668a55d0756962672618ba4650b56ebb
```

The full result/trace are large generated artifacts. The repository commits compact hash-bearing indexes/commitments and the exact frozen harness required to regenerate the byte-addressed artifacts.

This distinction is deliberate:

```text
committed compact custody record
!=
claim that the large generated payload is present as an ordinary Git blob
```

See:

- `../PCE_001_SPEC.md`
- `../PCE_001_MANIFEST.json`
- `../PCE_001_ANALYSIS.md`
- `../pce_001.py`
- `../PCE_001.md`

## Blitzcrank custody

BLITZCRANK-001/002 scientific records include the canonical numerical results and executed harness identities.

The branch does not pretend that every locally generated Blitz result JSON is committed in this directory. The authoritative published objects are the frozen specs, browsable harnesses, scientific records, and recorded hashes.

This is an explicit reproducibility boundary rather than an implicit omission.

## Reopenability bundle custody

FOREIGN-005/006 use deterministic `tar.gz` bundles because their exact execution directories include artifacts that are awkward to expose individually through the publication transport.

See [`../REOPENABILITY_LINEAGE.md`](../REOPENABILITY_LINEAGE.md) for member ordering, normalized tar metadata, hashes, and V1/V2 provenance.

The bundle does not replace the browsable spec/result narrative where those files are present.

## Preserved Nano negative results

These are intentionally retained because they forced distinctions in the persistence model.

| File | Meaning |
| --- | --- |
| [`nano_descendant_attack_pre_repair_10000.json`](nano_descendant_attack_pre_repair_10000.json) | Decorative lineage bug: stale descendant authority survived upstream revocation |
| [`nano_descendant_attack_post_repair_current_10000.json`](nano_descendant_attack_post_repair_current_10000.json) | Regression after warrant-parent liveness repair |
| [`nano_preservation_dependency_pre_repair_10000.json`](nano_preservation_dependency_pre_repair_10000.json) | Over-repair bug: preservation ancestry incorrectly treated as warrant ancestry |
| [`nano_preservation_dependency_post_repair_current_10000.json`](nano_preservation_dependency_post_repair_current_10000.json) | Regression after separating preservation from warrant dependency |

Base-002's guard/warrant negative result is preserved inside its result file and `../BASE_002_GLOBAL_REOPENING.md`. GW-001 preserves the subsequent discrimination result without publishing a Nano repair.

## Publication discipline

Promotion into this directory should remain deliberate.

A published evidence artifact should have enough provenance to identify:

```text
prospective specification
executed harness
input / seed regime
result payload or deterministic regeneration path
hash commitment
claim ceiling
repair provenance when relevant
```

Intermediate exploratory debris should not be promoted merely because it exists.

Conversely, if a scientific record relies on a generated artifact not stored directly as a Git blob, that fact and its byte commitment should be explicit rather than implied away.
