# E001 Pre-Subject Apparatus Interface Contract

> **STATUS: FROZEN CANDIDATE INTERFACE CONTRACT / UNEXECUTED / UNVERIFIED**
>
> **SUBJECT IMPLEMENTATION: NOT STARTED**
>
> **RESULTS: NONE / AUTHORITY MOVEMENT: NONE**

This file fixes the public boundary of the deterministic Experiment 001
apparatus sources. It does not make those sources valid, secure, complete, or
an implementation of K0.

## World and surface

- `world_generator.generate_world(seed: bytes) -> WorldInstance` accepts exactly
  one 32-byte seed and deterministically constructs the frozen `Z_11` family.
- A `WorldInstance` and its oracle descriptor are external truth objects and
  must never be passed to a subject arm, proposal engine, or adapter.
- `SurfaceCodec` may encode/decode payloads, map opaque scope tokens to opaque
  internal identifiers, and parse the generic one- or two-scope expression.
  Its adapter-facing descriptor carries no affine rule, epoch, held-out answer,
  evaluator decision, authority status, or phase label. Internal scope IDs are
  deterministic within a seeded world but seed-derived across worlds; a literal
  adapter-facing ID therefore cannot serve as a fixed A/B/C codebook across the
  development/evaluation population.
- The same `SurfaceCodec` and generic composition direction are used for every
  arm at a given seed. The adapter may not compute a task answer.

## Hypothesis and proposal

- `HYPOTHESES` is the complete canonical `a`-major, `c`-minor enumeration of
  `x -> a*x+c mod 11` for `a in {1,...,10}` and `c in Z_11`.
- `proposer.propose(observations, reference_ops)` enumerates that fixed library
  and returns either the unique consistent affine map or `UNDERDETERMINED`.
- Every candidate-affecting application and comparison crosses the reference
  operation boundary. The proposer does not emit evidence status, warrant,
  transition authority, a semantic commit, a durability receipt, or a result.

## Archive rival

- `ArchiveQuery.run(...)` reads an immutable ordered stream of canonical durable
  records. Exact-scope filtering is permitted only through `GenericIndex`.
- `GenericIndex` contains record IDs, exact-scope membership, canonical
  positions, and sequence metadata only. It contains no rule, answer, warrant,
  authority, or active-state delta.
- `ArchiveReducer.fold(empty_state(), records, reference_ops)` always rebuilds
  a fresh active state by folding ordered records. It may not address or mutate
  an existing active commitment and may not traverse a reopening binding.
- An efficient indexed replay remains `ARCHIVE_REPLAY`; it is not disqualified
  merely for performing well. A mechanism that directly mutates an existing
  commitment is not this archive rival.

## Reference meter

- The normative reference operations are `READ_CANONICAL`, `FOLD_RECORD`,
  `LOOKUP_KEY`, `APPLY_AFFINE`, `COMPOSE`, `BUILD_DELTA`, `COMPARE`, and
  `HASH_BLOCK_32`.
- `canonical_bytes_accessed` charges exact bytes returned through
  `READ_CANONICAL` and the key plus returned bytes of `LOOKUP_KEY`.
- Every normative operation and every evaluator, authority, persistence, or
  readback call advances the deterministic clock by one tick.
- An external call carries only a request digest plus typed status and optional
  artifact digest. It cannot carry semantic payload bytes. Any external
  artifact capable of affecting the candidate, commit, persistence, readback,
  reconstruction, or successor must traverse the digest-bound canonical-read
  operation and be charged in full.
- The meter rejects an over-envelope operation before appending its event. Its
  hash-chained trace must replay byte-for-byte under the same source.

## Fixed non-collapses

```text
world truth != subject observation
candidate != evaluation != warrant != transition capability
semantic commit != durable persistence != receipt
archive record != active commitment != reopening binding
stored descriptor != causal reachability != liveness
meter trace != apparatus validity != experiment result
```

No source in this apparatus may mint warrant or authority, write canonical
subject state, issue a persistence receipt, certify its own reachability, or
assign an Experiment 001 terminal status.
