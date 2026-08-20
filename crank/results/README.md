# Crank raw results

This directory preserves final constructed-suite outputs and diagnostically important negative results for the experimental `crank/` lineage.

Two files are historical pre-repair snapshots from Nano V0 implementation failures:

- `nano_descendant_attack_pre_repair_10000.json`
- `nano_preservation_dependency_pre_repair_10000.json`

The current `nano.py` contains the minimal repairs forced by those failures, so rerunning the current focused regression scripts is expected to produce the corresponding post-repair behavior rather than reproduce the historical failures. The failures themselves are preserved in `NANO_V0.md`, `nano_experiment_v0.md`, and these raw result snapshots.

Intermediate pilot runs are omitted when they do not change scientific interpretation.
