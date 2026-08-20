# E001 Evaluation-Seed Commitment Protocol

> **STATUS: FROZEN CANDIDATE PROTOCOL / UNEXECUTED / UNVERIFIED**
>
> **SEEDS: NONE GENERATED OR STORED BY THIS REPOSITORY ARTIFACT**
>
> **RESULTS: NONE**
>
> **AUTHORITY: NONE OVER K0, CEA, FCD/OCC, CCA/CARS, ISSUE #44, OR ARC3**

## 1. Scope

This protocol defines the exact cryptographic commitment made to each of the 64
sealed evaluation-seed values required by OpenCore Experiment 001. The public
objects are **cryptographic seed commitments**. They are not K0
`OpenCommitment`, `SemanticCommit`, warrant, transition authority, persistence
receipt, evidence of proper custody, or an experimental result.

The K0 ancestor is:

```text
c21693a593770ce31f89eb9e24b29e01ff75d392
```

The bound Experiment 001 artifact is `EXPERIMENT_001.md` at that commit, whose
UTF-8 file bytes, including its final LF, have SHA-256:

```text
166712a549318f53426b22cb0f0d49b3e4125cc39ad0887f3c0c650c8b3c687b
```

Publishing commitments freezes seed identity. It does not establish that the
seeds were independently sampled, stayed secret, or were handled by a properly
separated custodian. Those are custody and later adjudication questions.

## 2. Ceremony inputs

Before a custodian may generate evaluation seeds, all of the following values
must exist and be independently verified:

| Field | Canonical form |
| --- | --- |
| `k0_commit` | The 40 lowercase hexadecimal characters above |
| `experiment_sha256` | The 64 lowercase hexadecimal characters above |
| `protocol_sha256` | SHA-256 of the exact UTF-8 bytes of this file |
| `preimplementation_manifest_sha256` | SHA-256 of the OCJ-1 canonical bytes of one complete manifest instance |
| `execution_manifest_schema_sha256` | SHA-256 of the exact UTF-8 bytes of `EXECUTION_MANIFEST.schema.json` |
| `custodian_id` | 1-128 ASCII characters from `[A-Za-z0-9._:@/-]` |
| `custodian_epoch` | 1-64 ASCII characters from `[A-Za-z0-9._:-]` |

The preimplementation manifest must contain actual content hashes for every
required pre-subject apparatus artifact. A placeholder, schema-only document,
or planned path is not a complete manifest instance.

## 3. Primitive encodings

All strings use UTF-8 without a byte-order mark. Hexadecimal values are decoded
to their raw bytes before use in a commitment preimage. Hexadecimal output is
lowercase. Integers use unsigned 32-bit big-endian encoding.

For a byte string `x`, define:

```text
LP(x) = uint32_be(length_in_bytes(x)) || x
```

The exact ASCII domain separator is:

```text
OpenCore-E001-EvaluationSeedCommitment-v1
```

No newline or NUL byte follows that string inside its `LP` field.

## 4. Seed sampling and commitment

For each index `i` from 0 through 63, the external custodian obtains one fresh
32-byte value from the browser's `crypto.getRandomValues` CSPRNG. The helper
makes 64 separate calls. The deterministic development-seed derivation in
Experiment 001 must not be used for evaluation seeds.

For each seed `seed_i`, construct:

```text
preimage_i =
    LP(UTF8("OpenCore-E001-EvaluationSeedCommitment-v1"))
 || LP(raw_hex(k0_commit))
 || LP(raw_hex(experiment_sha256))
 || LP(raw_hex(protocol_sha256))
 || LP(raw_hex(preimplementation_manifest_sha256))
 || LP(raw_hex(execution_manifest_schema_sha256))
 || LP(UTF8(custodian_id))
 || LP(UTF8(custodian_epoch))
 || uint32_be(i)
 || LP(seed_i)

commitment_i = SHA256(preimage_i)
```

The published register contains exactly one indexed commitment for each integer
in `[0,63]`, in ascending order. It contains no seed value. If the helper detects
an exact duplicate seed during an unpublished ceremony, it aborts the entire
ceremony and emits no artifact. A new ceremony requires a new
`custodian_epoch`; individual seeds are never selectively replaced.

After a register has been published, no failed, inconvenient, lost, or otherwise
undesired seed may be removed, replaced, or reordered. Loss of the reveal bundle
or its decryption material makes the experiment `INVALID / UNDERCONSTITUTED`; it
does not authorize regeneration under the same experiment instance.

## 5. OCJ-1 canonical JSON

The helper uses the following deliberately narrow canonical JSON profile for
register, reveal, and additional-authenticated-data bodies:

1. Objects contain only JSON-compatible values and are serialized with keys in
   ascending UTF-16 code-unit order.
2. Arrays preserve their declared order.
3. Strings use the escaping produced by ECMAScript `JSON.stringify`.
4. Numbers are finite integers in this protocol and use the decimal form
   produced by ECMAScript `JSON.stringify`.
5. No insignificant whitespace or trailing newline occurs in canonical bytes.
6. The canonical byte sequence is UTF-8 without a byte-order mark.

This profile is named `OCJ-1`. It is not claimed to be RFC 8785.

The public download is an envelope:

```text
{
  "schema": "opencore.e001.seed-commitment-register-envelope.v1",
  "body": <public register body>,
  "body_sha256": SHA256(UTF8(OCJ-1(body)))
}
```

The envelope itself is pretty-printed for inspection. Verification hashes only
the OCJ-1 bytes of `body`.

## 6. Public non-evaluation known-answer vector

Implementations must reproduce this fixed vector before they are used. It is a
codec test only and is never an evaluation seed or commitment:

```text
k0_commit = c21693a593770ce31f89eb9e24b29e01ff75d392
experiment_sha256 = 166712a549318f53426b22cb0f0d49b3e4125cc39ad0887f3c0c650c8b3c687b
protocol_sha256 = 0000000000000000000000000000000000000000000000000000000000000000
preimplementation_manifest_sha256 = 1111111111111111111111111111111111111111111111111111111111111111
execution_manifest_schema_sha256 = 2222222222222222222222222222222222222222222222222222222222222222
custodian_id = PUBLIC-TEST
custodian_epoch = v1
i = 7
seed_i = 000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
commitment_i = 02116812d760ae300a98a643fab6534eff3a3aa6ac5dfe5e22e26f057ab7f448
```

The encoded preimage is 274 bytes. A mismatch is a protocol failure; the helper
must not generate ceremony artifacts.

## 7. Encrypted reveal bundle

The custody helper constructs a plaintext OCJ-1 reveal body in memory containing
the commitment context and all 64 indexed 32-byte seed values in lowercase hex.
It never renders, logs, copies, or downloads that plaintext.

Encryption is:

```text
KDF:       PBKDF2-HMAC-SHA-256
iterations: 600000
salt:      16 fresh CSPRNG bytes
key:       256-bit AES-GCM key
IV:        12 fresh CSPRNG bytes
tag:       128 bits (appended by Web Crypto to ciphertext)
plaintext: UTF8(OCJ-1(reveal_body))
AAD:       UTF8(OCJ-1(aad_body))
```

The `aad_body` binds the public-register body digest, K0, Experiment 001,
protocol, preimplementation manifest, execution-manifest schema, custodian, and
custodian epoch. The encrypted envelope publishes the KDF parameters, salt, IV,
AAD body, and base64 ciphertext. It contains no passphrase or plaintext seed.

AES-GCM protects the stored bundle only to the strength of the passphrase and
custody environment. It does not protect against a compromised browser or host,
and JavaScript garbage collection cannot guarantee immediate erasure of every
temporary plaintext copy.

## 8. Required custody boundary

The ceremony must run on an externally controlled offline machine and browser
that are not available to the subject implementation, its developers, or its
automation. The custodian must:

- verify the helper, protocol, schema, K0, Experiment, and complete apparatus
  manifest hashes before generation;
- keep the encrypted bundle and passphrase in separate protected custody;
- prevent the seed values and passphrase from entering repository history, pull
  requests, issue text, chat, Codex output, CI logs, shell history, cloud sync,
  telemetry, clipboard history, crash reports, or subject-accessible storage;
- publish only the commitment-register envelope before the reveal gate;
- retain both public and encrypted downloads exactly as emitted; and
- close the browser and power down or destroy the ceremony environment after
  verifying custody copies.

The helper's source can enforce neither externality nor custody. Phase 0 and the
attack adjudicator remain responsible for judging those claims.

## 9. Reveal gate and verification

The seeds remain sealed until all final subject implementations pass the 32-seed
development qualification and the exact populated execution-manifest instance,
all final subject hashes, and its public anchor are published. A schema, draft,
placeholder manifest, or private hash does not satisfy the gate.

At reveal, a separately reviewed reveal procedure must:

1. authenticate and decrypt the envelope using its exact KDF, AES-GCM, and AAD;
2. parse the OCJ-1 reveal body without altering it;
3. verify the public-register body digest;
4. recompute all 64 indexed commitments from the revealed seed bytes;
5. require exact equality at every index with no omission or extra value; and
6. publish the immutable reveal record before the single evaluation campaign.

The present custody helper intentionally does not decrypt or publish plaintext
seeds. A reveal tool and reveal-record schema are later prospective apparatus;
they must be frozen before they are used.

## 10. Lineage and claim ceiling

The intended acyclic lineage is:

```text
K0 + Experiment 001
  -> protocol + schemas + custody-helper source
  -> complete preimplementation-manifest instance
  -> public seed-commitment register
  -> E001 preimplementation anchor
  -> subject implementation and development qualification
  -> populated final execution-manifest instance and public hash
  -> seed reveal record
  -> one evaluation campaign
  -> traces, gate decision, adjudication, and result
```

Future artifacts point backward by digest. Frozen prospective artifacts are
never edited to fill reveal values, measurements, validity decisions, terminal
statuses, or results. Any repair creates a distinctly named successor.
