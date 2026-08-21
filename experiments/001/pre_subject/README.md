# Experiment 001 Pre-Subject Tooling

> **STATUS: FROZEN CANDIDATE PRE-SUBJECT APPARATUS AND SCHEMAS**
>
> **APPARATUS MANIFEST: POPULATED / SEED REGISTER: ABSENT**
>
> **EVALUATION SEEDS: NONE STORED OR GENERATED HERE**
>
> **EXECUTION: NOT STARTED**
>
> **RESULTS: NONE / TERMINAL STATUS UNASSIGNED**
>
> **AUTHORITY: NONE OVER K0, CEA, FCD/OCC, CCA/CARS, ISSUE #44, OR ARC3**

This directory freezes the deterministic pre-subject apparatus sources, their
populated hash manifest, prospective formats, and an offline custody application
for Experiment 001. It is an **apparatus/schema anchor candidate**, not the
completed E001 preimplementation anchor: no public commitments to externally
sealed evaluation seeds exist yet. It is not a final execution manifest.

The immutable K0 ancestor is
`c21693a593770ce31f89eb9e24b29e01ff75d392`. The bound
`EXPERIMENT_001.md` file at that commit has SHA-256
`166712a549318f53426b22cb0f0d49b3e4125cc39ad0887f3c0c650c8b3c687b`.

## Contents

- `PREIMPLEMENTATION_MANIFEST.json` binds the exact apparatus, protocol,
  interface, dependency, and role-plan bytes. Its OCJ-1 body digest is the
  ceremony input named `preimplementation_manifest_sha256`.
- `apparatus/` contains the eight minimum pre-subject components plus the
  load-bearing canonical utility, fixed proposer, and deterministic self-test.
- `APPARATUS_DEPENDENCIES.json`, `APPARATUS_INTERFACES.md`, and `ROLE_PLAN.md`
  freeze the source closure and logical trust boundary.
- `SEED_COMMITMENT_PROTOCOL.md` freezes the indexed binary commitment,
  encrypted-bundle, custody, and reveal-gate semantics.
- `PREIMPLEMENTATION_MANIFEST.schema.json` accepts only a complete prospective
  apparatus inventory with actual source and interface/dependency artifact
  hashes. A schema-conforming file still requires semantic and lineage review.
- `EXECUTION_MANIFEST.schema.json` defines the later immutable manifest instance
  that can be populated only after subject implementation and 32-seed
  development qualification, but before evaluation-seed reveal.
- `seed_custodian.html` is a self-contained, browser-only custody application.
  It generates seeds only after an explicit click and emits only public
  commitments and an encrypted reveal bundle.

None of these files contains a raw seed, passphrase, decryption key, execution
trace, gate decision, measurement, terminal status, or result.

## Recovered-worktree isolation repair

The recovered pre-freeze worktree exposed one apparatus-only isolation channel:
external scope tokens were seed-permuted, but their adapter-facing internal IDs
were constant across seeds. A subject could therefore learn a literal internal
ID -> A/B/C codebook on the 32 public development worlds and carry it unchanged
into fresh worlds. This did not amend K0: K0 requires opaque surface translation
but does not prescribe the internal-ID generation algorithm.

Before this apparatus anchor is frozen, `SurfaceCodec` therefore derives each
internal scope ID from the current seed under a separate domain. IDs remain
stable and deterministic within one world while changing across worlds. The
hash-bound apparatus self-test includes a regression assay that learns every
development-world ID and verifies that none reappears in 256 deterministic
non-evaluation audit worlds. Operation IDs remain fixed because the generic
`APPLY`/`SEQ` algebra is intentionally public; this repair closes only the
semantic scope-role codebook identified by the audit.

## External custody procedure

The populated apparatus manifest currently has:

```text
exact file SHA-256: 6555e028c3150d86bfa4cd5c70191702716942cee12146c9e904d2bc93f802cc
OCJ-1 body SHA-256: 8356e3a85fb7006b28e7b2b1cb4c4363fbfcfb4c9cc592397486ddcd581c1ad4
custodian ID:        opencore-e001-external-custodian
custodian epoch:     ceremony-v1
```

The OCJ-1 body digest—not the pretty-printed file digest—is the ceremony input.
The designated custodian must use the exact frozen ID and epoch; a replacement
ceremony requires an explicit successor artifact and cannot silently reuse
`ceremony-v1`.

Do not run the custody application in this repository workspace. Transfer the
reviewed file and its independently obtained SHA-256 digest to an externally
controlled offline machine that is inaccessible to subject developers and
automation. Use a fresh browser profile with telemetry, synchronization,
extensions, clipboard history, and crash upload disabled.

Before generation, the custodian must have:

1. a complete instance of `PREIMPLEMENTATION_MANIFEST.schema.json` containing
   the actual hashes of all required pre-subject apparatus;
2. independent verification of K0, Experiment 001, the commitment protocol, the
   execution-manifest schema, and the custody-application bytes;
3. a unique custodian ID and ceremony epoch; and
4. a high-entropy passphrase held separately from the encrypted bundle.

Open `seed_custodian.html` directly as a local `file:` URL. Enter the complete
apparatus-manifest digest, custodian identity/epoch, and passphrase; attest the
offline boundary; and press **Generate and encrypt once**. The application makes
64 separate 32-byte `crypto.getRandomValues` calls only then. Download both the
public register and encrypted reveal bundle. Verify both copies before closing
the browser. Publish only the public register and its anchor; retain the
encrypted bundle and passphrase in separate protected custody.

The application deliberately has no decryption or plaintext-export function.
The final execution-manifest instance must bind a separately frozen reveal
procedure and reveal-record schema. Losing the encrypted bundle or passphrase,
or revealing it before the exact final subject hashes and populated execution
manifest are publicly anchored, yields `INVALID / UNDERCONSTITUTED`; it does not
authorize seed regeneration.

Browser JavaScript cannot prove perfect erasure or host integrity. AES-GCM only
protects the stored bundle to the strength of the passphrase and custody
environment. Phase 0 and the external adjudicator must assess the custody claim.

## Staged lineage

```text
K0 c21693a... + Experiment 001
  -> this protocol/schema/custody-application bundle
  -> complete apparatus-manifest instance
  -> externally generated public commitments + encrypted reveal custody
  -> distinct E001 preimplementation anchor binding all preceding digests
  -> subject implementations + 32-development-seed qualification
  -> populated final execution-manifest instance + public anchor
  -> separate reveal record
  -> exactly one predeclared evaluation campaign
  -> separate traces, gate decision, adjudication, and result
```

The containing Git commit can serve as an anchor only after publication; a file
must not embed the hash of the commit that contains itself. Descendants point
backward to published anchors. Frozen artifacts are never edited later to fill
unknown hashes, seed values, measurements, decisions, or results. A protocol,
schema, helper, apparatus, metric, threshold, seed, or campaign-plan change
after freeze creates a named successor.

## Schema and hash validation

Both schemas use JSON Schema Draft 2020-12, local references only, closed
objects, lowercase nonzero SHA-256 values, and no result-bearing fields. Schema
validation cannot prove that bytes match a digest, paths exist, Git ancestry is
correct, roles are separate, seeds were independently sampled or sealed, or a
campaign is valid. Those are mandatory semantic checks.

Artifact SHA-256 values use exact file bytes unless a field explicitly says
`UTF8_OCJ-1_CANONICAL_JSON` or `CANONICAL_TREE_MANIFEST`. Do not interchange a
Git object ID, raw-file digest, OCJ-1 body digest, or content digest.

Before publication, at minimum:

```powershell
Get-Content -Raw PREIMPLEMENTATION_MANIFEST.schema.json | ConvertFrom-Json | Out-Null
Get-Content -Raw EXECUTION_MANIFEST.schema.json | ConvertFrom-Json | Out-Null
Get-FileHash -Algorithm SHA256 SEED_COMMITMENT_PROTOCOL.md
Get-FileHash -Algorithm SHA256 PREIMPLEMENTATION_MANIFEST.schema.json
Get-FileHash -Algorithm SHA256 EXECUTION_MANIFEST.schema.json
Get-FileHash -Algorithm SHA256 seed_custodian.html
```

Static inspection must also confirm there is no network API, storage API,
clipboard path, console output, plaintext-seed DOM path, plaintext-seed Blob, or
automatic generation path in the custody application. Running the helper for a
test is a separate, explicitly controlled non-evaluation procedure; this
repository freeze does not execute it.
