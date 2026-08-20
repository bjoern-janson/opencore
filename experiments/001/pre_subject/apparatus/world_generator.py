"""Deterministic external world generator for the frozen E001 family."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

try:
    from .canonical import Sha256Stream, require_uint, sha256_hex
    from .hypothesis_library import (
        HYPOTHESES,
        IDENTITY,
        MODULUS,
        AffineMap,
        compose,
        disagreement_count,
        field,
    )
    from .surface_codec import SCOPE_NAMES, SurfaceCodec
except ImportError:  # Direct execution from the apparatus directory.
    from canonical import Sha256Stream, require_uint, sha256_hex
    from hypothesis_library import (
        HYPOTHESES,
        IDENTITY,
        MODULUS,
        AffineMap,
        compose,
        disagreement_count,
        field,
    )
    from surface_codec import SCOPE_NAMES, SurfaceCodec


WORLD_SCHEMA = "opencore.e001.affine-world.v1"
DEVELOPMENT_SEED_DOMAIN = b"OpenCore-K0-E001-development"
MAP_ROLES = ("A0", "A1", "A2", "B")
EPOCHS = ("e0", "e1", "e2")


def development_seed(index: int) -> bytes:
    """Implement the exact public 32-seed derivation frozen in E001 section 5."""

    require_uint(index, "development seed index", 32)
    return hashlib.sha256(DEVELOPMENT_SEED_DOMAIN + index.to_bytes(4, "big")).digest()


def _valid_quadruple(maps: tuple[AffineMap, ...]) -> bool:
    if len(maps) != 4:
        return False
    a0, a1, a2, b = maps
    if any(item == IDENTITY for item in maps) or len(set(maps)) != 4:
        return False
    for a_map in (a0, a1, a2):
        b_after_a = compose(b, a_map)
        if b_after_a in (a_map, b, compose(a_map, b)):
            return False
    return all(
        disagreement_count(left, right) >= 9
        for index, left in enumerate(maps)
        for right in maps[index + 1 :]
    )


def _draw_quadruple(seed: bytes) -> tuple[AffineMap, AffineMap, AffineMap, AffineMap]:
    stream = Sha256Stream(seed, "world/ordered-affine-quadruple")
    while True:
        candidate = tuple(
            HYPOTHESES[stream.uint_below(len(HYPOTHESES))] for _ in MAP_ROLES
        )
        if _valid_quadruple(candidate):
            return candidate  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class InputPartition:
    evidence: tuple[int, int]
    held_out: tuple[int, ...]

    def __post_init__(self) -> None:
        combined = self.evidence + self.held_out
        if len(self.evidence) != 2 or len(self.held_out) != 9:
            raise ValueError("input partition must contain 2 evidence and 9 held-out inputs")
        if len(set(combined)) != MODULUS or set(combined) != set(range(MODULUS)):
            raise ValueError("input partition must be a permutation of Z_11")


@dataclass(frozen=True, slots=True)
class WorldInstance:
    """External-oracle state; this object must never be handed to the subject."""

    seed_fingerprint: str
    transformations: dict[str, AffineMap]
    partitions: dict[str, InputPartition]
    codec: SurfaceCodec

    def __post_init__(self) -> None:
        if tuple(self.transformations) != MAP_ROLES:
            raise ValueError("transformations must use canonical role order")
        if tuple(self.partitions) != MAP_ROLES:
            raise ValueError("partitions must use canonical role order")
        maps = tuple(self.transformations[role] for role in MAP_ROLES)
        if not _valid_quadruple(maps):
            raise ValueError("world transformations violate E001 constraints")

    def public_surface(self) -> dict[str, Any]:
        return {
            "schema": WORLD_SCHEMA,
            "seed_fingerprint": self.seed_fingerprint,
            "payload_modulus": MODULUS,
            "surface": self.codec.public_descriptor(),
        }

    def oracle_descriptor(self) -> dict[str, Any]:
        """Canonical truth for the external world oracle, never the adapter."""

        return {
            "schema": WORLD_SCHEMA,
            "seed_fingerprint": self.seed_fingerprint,
            "transformations": {
                role: self.transformations[role].to_dict() for role in MAP_ROLES
            },
            "partitions": {
                role: {
                    "evidence": list(self.partitions[role].evidence),
                    "held_out": list(self.partitions[role].held_out),
                }
                for role in MAP_ROLES
            },
            "codec_id": self.codec.codec_id,
        }

    def encoded_evidence(self, role: str) -> tuple[dict[str, Any], dict[str, Any]]:
        if role not in MAP_ROLES:
            raise ValueError("unknown map role")
        logical_scope = "A" if role.startswith("A") else "B"
        transform = self.transformations[role]
        return tuple(
            self.codec.encode_observation(logical_scope, x, transform.apply(x))
            for x in self.partitions[role].evidence
        )  # type: ignore[return-value]

    def transform_for(self, logical_scope: str, epoch: str) -> AffineMap | None:
        if logical_scope not in SCOPE_NAMES:
            raise ValueError("unknown logical scope")
        if epoch not in EPOCHS:
            raise ValueError("unknown world epoch")
        if logical_scope == "C":
            return None
        if logical_scope == "B":
            return self.transformations["B"]
        return self.transformations[{"e0": "A0", "e1": "A1", "e2": "A2"}[epoch]]

    def apply(self, logical_scope: str, epoch: str, x: int) -> int | None:
        transform = self.transform_for(logical_scope, epoch)
        return None if transform is None else transform.apply(field(x, "x"))

    def apply_sequence(
        self, first_scope: str, second_scope: str, epoch: str, x: int
    ) -> int | None:
        first = self.transform_for(first_scope, epoch)
        second = self.transform_for(second_scope, epoch)
        if first is None or second is None:
            return None
        return second.apply(first.apply(field(x, "x")))


def generate_world(seed: bytes) -> WorldInstance:
    """Generate exactly one deterministic E001 world from a 32-byte seed."""

    if not isinstance(seed, bytes) or len(seed) != 32:
        raise ValueError("seed must be exactly 32 bytes")
    maps = _draw_quadruple(seed)
    transformations = dict(zip(MAP_ROLES, maps, strict=True))
    partitions = {
        role: InputPartition(
            evidence=permutation[:2],
            held_out=permutation[2:],
        )
        for role in MAP_ROLES
        for permutation in (
            Sha256Stream(seed, f"world/input-partition/{role}").permutation(
                range(MODULUS)
            ),
        )
    }
    return WorldInstance(
        seed_fingerprint=sha256_hex(
            "OpenCore-K0-E001-SeedFingerprint-v1", {"seed": seed}
        ),
        transformations=transformations,
        partitions=partitions,
        codec=SurfaceCodec(seed),
    )


def _self_test() -> None:
    for index in range(32):
        seed = development_seed(index)
        first = generate_world(seed)
        second = generate_world(seed)
        assert first.oracle_descriptor() == second.oracle_descriptor()
        assert first.public_surface() == second.public_surface()
        maps = tuple(first.transformations[role] for role in MAP_ROLES)
        assert _valid_quadruple(maps)
        for role in MAP_ROLES:
            encoded = first.encoded_evidence(role)
            decoded = tuple(first.codec.decode_observation(item) for item in encoded)
            assert len({item.x for item in decoded}) == 2
        for x in range(MODULUS):
            assert first.apply_sequence("A", "B", "e1", x) == first.transformations[
                "B"
            ].apply(first.transformations["A1"].apply(x))
            assert first.apply_sequence("A", "C", "e1", x) is None


if __name__ == "__main__":
    _self_test()

