# Crank Result Snapshots

This directory contains raw result snapshots used by the published Nano V0 and Mini × Nano V0 records.

The JSON files are evidence for specific constructed assays. They are not universal benchmark claims and do not amend formal K0/E001 artifacts.

## Published decisive results

| File | Role |
|---|---|
| [`nano_attack_matrix_final_10000.json`](nano_attack_matrix_final_10000.json) | Final strengthened isolated Nano V0 six-family matrix |
| [`nano_experiment_v0_results.json`](nano_experiment_v0_results.json) | Compact Nano V0 result bundle and hashes |
| [`mini_nano_composition_final_10000.json`](mini_nano_composition_final_10000.json) | Final 10,000-seed wounded Mini × Nano composition suite |

## Preserved Nano negative results

These are intentionally retained because they forced the final V0 design.

| File | Meaning |
|---|---|
| [`nano_descendant_attack_pre_repair_10000.json`](nano_descendant_attack_pre_repair_10000.json) | Decorative lineage bug: stale descendant authority survived upstream revocation |
| [`nano_descendant_attack_post_repair_current_10000.json`](nano_descendant_attack_post_repair_current_10000.json) | Current regression after warrant-parent liveness repair |
| [`nano_preservation_dependency_pre_repair_10000.json`](nano_preservation_dependency_pre_repair_10000.json) | Over-repair bug: preservation ancestry was incorrectly treated as warrant ancestry |
| [`nano_preservation_dependency_post_repair_current_10000.json`](nano_preservation_dependency_post_repair_current_10000.json) | Current regression after separating preservation from warrant dependency |

## Additional local crank results

The working checkout may contain additional untracked result files from Mini 003-006, external attacks, R1, and exploratory harnesses. Those are not automatically part of the published Nano V0 / composition record.

Promotion into this directory's published index should remain deliberate: include the harness identity, claim ceiling, and enough provenance to distinguish a final result from exploratory debris.
