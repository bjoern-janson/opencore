# Quotient-pressure lineage — OQ-001 through FOREIGN-004

**Status:** frozen crank evidence lineage

**Architecture changes:** none

**Nano changes:** none

This record freezes a four-assay sequence that pressured the candidate notion of a premature quotient without introducing a new OpenCore primitive.

## Result geometry

| Assay | History differs | Tested future consequence differs | Persistence result |
|---|---:|---:|---|
| [OQ-001](OQ_001.md) | yes | yes | apparatus expressive wound; Nano not used |
| [OQ-002](OQ_002.md) | yes | yes | persistent-authority wound upstream of unchanged Nano |
| [FOREIGN-003](FOREIGN_003.md) | yes | yes | classical reproduction of the persistence wound |
| [FOREIGN-004](FOREIGN_004.md) | yes | no on frozen future surface | safe quotient |

The supported compression is deliberately local:

```text
A distinction can be persistence-relevant when collapsing it changes a warranted
future consequence. History difference alone is not sufficient to require
persistence-distinct identity.
```

FOREIGN-004 therefore falsifies the stronger reading:

```text
H_A != H_B  =>  H_A and H_B must always remain persistence-distinct
```

It does **not** establish universal future equivalence or an algorithm for deciding when a history is safe to forget.

## Frozen Nano identity

OQ-002, FOREIGN-003, and FOREIGN-004 reuse the unchanged Nano V0 implementation:

```text
SHA-256
8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329
```

OQ-001 does not use Nano.

## Frozen artifact identities

### OQ-001

```text
OQ_001.md
SHA-256 9118a1e24b5e6049e64672049b233c07a87b6899596d35f24c0c9e21e99ac6c3
Git blob 2617a7b0242035a4956dfc25541c0b3cec696ecf

oq_001.py
SHA-256 548d7403ad380d92e422360fa41463f3ce4e52a0ba66d8cd4e8d5139afdfc7a3
Git blob b7dba2509fbdf8bb0da1cddfddc931ea369049c5

oq_001_result.json
SHA-256 ce98421bf07751295e0c029807ce2514117a0c090c5b83c06fa1b26e6ac78a0a
Git blob aa76cd5b905c46644c11843ebf6ec42113804d73
```

### OQ-002

```text
OQ_002.md
SHA-256 21072179061daea6e418f2d981a45c7a5c3334760d87faac2f896d0371821305
Git blob 2e0bb9d9a2ac726dc306426bcac2169c659e0181

oq_002.py
SHA-256 2e79b24e4dd26b9c7bced1db8d004a94d10b409dc32433c00c5c1b436b3c36f8
Git blob 63537a8378629a39be2e3b872d4c5679936eadc5

oq_002_result.json
SHA-256 81a72a63fce10c8761707f810681a53498f8136018e2d621249e60ed263b5d07
Git blob e5f2aa3b1413f42bf7b5ae6bb5fd52c409d20b58
```

### FOREIGN-003

```text
FOREIGN_003.md
SHA-256 030f6e4792184884ed30f81f6f6f25a27774c251a438f13950e1c9877e8800c4
Git blob df4bd8eb9bdbca487b5d6f1791e6dfbb87745a02

foreign_003.py
SHA-256 6667263a717a644d2a4de8ed33287617e17420187672897670fdecfd5689dd37
Git blob 1db272da5168bb6f5fcf889101304006e220a860

foreign_003_result.json (uncompressed frozen result)
SHA-256 d46ca19661c0cad46d36c7a5be0d77010ad985cea76930739f4f6f36c8c81b5a
Git blob f955e641de88582fca53d97280be8d9fbb71674b

published transport: results/foreign_003_result.json.gz
compressed SHA-256 f1b4b3f84f4f606f7b3f1aa3c1d5cb8d074431742701f6d4d110fccb803c2243
compressed Git blob eccee1b83d3301de8e0c61a716f886587932afac
```

### FOREIGN-004

```text
FOREIGN_004_SPEC.md
SHA-256 6d86d2c8f7ea36e095a4a142e6f70007e0382f904e4773f7e0393cb05d27dd37
Git blob cf2d7a8a0b28492c3e99a98bcc7c57a2e039dddb

FOREIGN_004.md
SHA-256 93da66277e1a7a51f7795714d160a7ce641032ca20befc28043c8439298f1340
Git blob 029bda2c3d8af4c52325e607117af7ebf722fde8

foreign_004.py
SHA-256 dbfc6ff62e5d36bea75f1f34b0f19bb17d96bd6808a2d921d05add4621d21a52
Git blob 98bcd40081ab96d515d6faa40ceeb1361d486e3b

foreign_004_result.json (uncompressed frozen result)
SHA-256 8fcb4d1de4889f3006e3aaf398951474d4c9149ddb46f0204725043ede86a048
Git blob dd368d200c42008713317f0a665464568023f5f8

published transport: results/foreign_004_result.json.gz
compressed SHA-256 2beb9fc25f40a7d8428604a186cd8d66aa2d36f0ab4c8c6d50b544f580c8e03c
compressed Git blob fae579ef39ed43ebffacd4dfc030a65d1ffe20e7
```

The `.json.gz` files are deterministic gzip encodings (`mtime=0`, no filename) of the exact frozen JSON bytes. Reconstruct and verify with, for example:

```bash
gzip -dc crank/results/foreign_003_result.json.gz > /tmp/foreign_003_result.json
sha256sum /tmp/foreign_003_result.json
# expected d46ca19661c0cad46d36c7a5be0d77010ad985cea76930739f4f6f36c8c81b5a

gzip -dc crank/results/foreign_004_result.json.gz > /tmp/foreign_004_result.json
sha256sum /tmp/foreign_004_result.json
# expected 8fcb4d1de4889f3006e3aaf398951474d4c9149ddb46f0204725043ede86a048
```

## Claim ceiling

This lineage supports a candidate cross-domain pattern:

```text
premature apparatus quotient
-> identity aliasing
-> warrant aliasing when the erased distinction remains consequence-relevant
-> possible wrong persistent consequence
```

and one constructed counterexample to mandatory history preservation:

```text
different history
+ tested future-consequence equivalence
-> safe quotient on the frozen tested surface
```

Not earned:

```text
universal quotient law
HistoryID primitive
AcquisitionPath primitive
post_state field
quantum-specific Nano
Nano repair
algorithm for permanent safe merging
universal future-consequence equivalence
```
