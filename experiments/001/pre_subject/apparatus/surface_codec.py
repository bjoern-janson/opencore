"""Seeded opaque surfaces for E001 without rule or authority information."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any

try:
    from .canonical import Sha256Stream, assert_unique, sha256_hex
    from .hypothesis_library import MODULUS, field
except ImportError:  # Direct execution from the apparatus directory.
    from canonical import Sha256Stream, assert_unique, sha256_hex
    from hypothesis_library import MODULUS, field


CODEC_SCHEMA = "opencore.e001.surface-codec.v1"
OBSERVATION_SCHEMA = "opencore.e001.opaque-observation.v1"
SCOPE_NAMES = ("A", "B", "C")
OPERATION_NAMES = ("APPLY", "SEQ")
OBSERVATION_FIELDS = ("scope", "input", "output")
_EXPRESSION = re.compile(r"^([0-9a-f]{24})\(([0-9a-f]{24})(?:,([0-9a-f]{24}))?\)$")


def _token(namespace: str, index: int) -> str:
    return hashlib.sha256(
        b"OpenCore-K0-E001-Opaque-Token-v1\x00"
        + namespace.encode("ascii")
        + b"\x00"
        + index.to_bytes(2, "big")
    ).hexdigest()[:24]


def _pool(namespace: str, size: int) -> tuple[str, ...]:
    values = tuple(_token(namespace, index) for index in range(size))
    assert_unique(values, f"{namespace} token pool")
    return values


_SCOPE_TOKEN_POOL = _pool("scope", len(SCOPE_NAMES))
_OPERATION_TOKEN_POOL = _pool("operation", len(OPERATION_NAMES))
_PAYLOAD_TOKEN_POOL = _pool("payload", MODULUS)
_INTERNAL_OPERATION_IDS = _pool("internal-operation", len(OPERATION_NAMES))


@dataclass(frozen=True, slots=True)
class DecodedObservation:
    scope_id: str
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class ParsedScopeExpression:
    operation_id: str
    scope_ids: tuple[str, ...]


class SurfaceCodec:
    """Four independently derived permutations and their generic codecs.

    The instance contains no affine transformation, epoch, held-out answer,
    evaluator decision, capability, or phase label.  Its adapter-facing scope
    values are opaque internal identifiers rather than the logical A/B/C names.
    Scope identifiers are stable within one seeded world but are independently
    seed-derived so they cannot form a fixed cross-seed A/B/C codebook.
    """

    def __init__(self, seed: bytes):
        if not isinstance(seed, bytes) or len(seed) != 32:
            raise ValueError("seed must be exactly 32 bytes")

        scope_tokens = Sha256Stream(seed, "surface/scope-labels").permutation(
            _SCOPE_TOKEN_POOL
        )
        operation_tokens = Sha256Stream(
            seed, "surface/operation-labels"
        ).permutation(_OPERATION_TOKEN_POOL)
        payload_tokens = Sha256Stream(seed, "surface/payload-presentation").permutation(
            _PAYLOAD_TOKEN_POOL
        )
        observation_order = Sha256Stream(
            seed, "surface/observation-encoding"
        ).permutation(OBSERVATION_FIELDS)

        self._scope_token_by_logical = dict(zip(SCOPE_NAMES, scope_tokens, strict=True))
        self._logical_by_scope_token = {
            token: logical for logical, token in self._scope_token_by_logical.items()
        }
        internal_scope_ids = tuple(
            Sha256Stream(seed, f"surface/internal-scope-id/{logical}").take(12).hex()
            for logical in SCOPE_NAMES
        )
        assert_unique(internal_scope_ids, "seed-derived internal scope identifiers")
        self._scope_id_by_logical = dict(
            zip(SCOPE_NAMES, internal_scope_ids, strict=True)
        )
        self._logical_by_scope_id = {
            scope_id: logical for logical, scope_id in self._scope_id_by_logical.items()
        }
        self._operation_token_by_logical = dict(
            zip(OPERATION_NAMES, operation_tokens, strict=True)
        )
        self._logical_by_operation_token = {
            token: logical
            for logical, token in self._operation_token_by_logical.items()
        }
        self._operation_id_by_logical = dict(
            zip(OPERATION_NAMES, _INTERNAL_OPERATION_IDS, strict=True)
        )
        self._logical_by_operation_id = {
            operation_id: logical
            for logical, operation_id in self._operation_id_by_logical.items()
        }
        self._payload_token_by_value = dict(
            zip(range(MODULUS), payload_tokens, strict=True)
        )
        self._value_by_payload_token = {
            token: value for value, token in self._payload_token_by_value.items()
        }
        self._observation_order = tuple(observation_order)

        self.codec_id = sha256_hex(
            "OpenCore-K0-E001-SurfaceCodec-v1",
            {
                "scope_tokens": scope_tokens,
                "operation_tokens": operation_tokens,
                "payload_tokens": payload_tokens,
                "observation_order": observation_order,
                "internal_scope_ids": internal_scope_ids,
                "internal_operation_ids": tuple(_INTERNAL_OPERATION_IDS),
            },
        )

    def public_descriptor(self) -> dict[str, Any]:
        """Return surface vocabulary without its hidden logical assignment."""

        return {
            "schema": CODEC_SCHEMA,
            "codec_id": self.codec_id,
            "scope_tokens": sorted(self._logical_by_scope_token),
            "operation_tokens": sorted(self._logical_by_operation_token),
            "payload_tokens": sorted(self._value_by_payload_token),
            "observation_arity": 3,
            "scope_expression_grammar": "OP(SCOPE) | OP(SCOPE,SCOPE)",
        }

    def encode_scope(self, logical_scope: str) -> str:
        try:
            return self._scope_token_by_logical[logical_scope]
        except KeyError as exc:
            raise ValueError("unknown logical scope") from exc

    def scope_to_internal(self, scope_token: str) -> str:
        try:
            logical = self._logical_by_scope_token[scope_token]
            return self._scope_id_by_logical[logical]
        except KeyError as exc:
            raise ValueError("unknown opaque scope token") from exc

    def encode_payload(self, value: int) -> str:
        return self._payload_token_by_value[field(value, "payload")]

    def decode_payload(self, token: str) -> int:
        try:
            return self._value_by_payload_token[token]
        except KeyError as exc:
            raise ValueError("unknown opaque payload token") from exc

    def encode_observation(self, logical_scope: str, x: int, y: int) -> dict[str, Any]:
        fields = {
            "scope": self.encode_scope(logical_scope),
            "input": self.encode_payload(x),
            "output": self.encode_payload(y),
        }
        return {
            "schema": OBSERVATION_SCHEMA,
            "codec_id": self.codec_id,
            "cells": [fields[name] for name in self._observation_order],
        }

    def decode_observation(self, encoded: Any) -> DecodedObservation:
        if not isinstance(encoded, dict) or set(encoded) != {"schema", "codec_id", "cells"}:
            raise ValueError("observation fields do not match schema")
        if encoded["schema"] != OBSERVATION_SCHEMA or encoded["codec_id"] != self.codec_id:
            raise ValueError("observation codec binding mismatch")
        cells = encoded["cells"]
        if not isinstance(cells, list) or len(cells) != 3 or not all(
            isinstance(cell, str) for cell in cells
        ):
            raise ValueError("observation cells must be three strings")
        fields = dict(zip(self._observation_order, cells, strict=True))
        return DecodedObservation(
            scope_id=self.scope_to_internal(fields["scope"]),
            x=self.decode_payload(fields["input"]),
            y=self.decode_payload(fields["output"]),
        )

    def encode_scope_expression(self, logical_scopes: tuple[str, ...]) -> str:
        if len(logical_scopes) == 1:
            operation = "APPLY"
        elif len(logical_scopes) == 2:
            operation = "SEQ"
        else:
            raise ValueError("scope expression must contain one or two scopes")
        token = self._operation_token_by_logical[operation]
        arguments = ",".join(self.encode_scope(scope) for scope in logical_scopes)
        return f"{token}({arguments})"

    def parse_scope_expression(self, expression: str) -> ParsedScopeExpression:
        if not isinstance(expression, str):
            raise ValueError("scope expression must be a string")
        match = _EXPRESSION.fullmatch(expression)
        if match is None:
            raise ValueError("invalid scope expression syntax")
        operation_token, first, second = match.groups()
        try:
            logical_operation = self._logical_by_operation_token[operation_token]
        except KeyError as exc:
            raise ValueError("unknown opaque operation token") from exc
        scope_tokens = (first,) if second is None else (first, second)
        expected_arity = 1 if logical_operation == "APPLY" else 2
        if len(scope_tokens) != expected_arity:
            raise ValueError("operation arity mismatch")
        return ParsedScopeExpression(
            operation_id=self._operation_id_by_logical[logical_operation],
            scope_ids=tuple(self.scope_to_internal(token) for token in scope_tokens),
        )

    # World-oracle helpers.  These are not part of the adapter-facing surface.
    def _logical_scope_from_id(self, scope_id: str) -> str:
        try:
            return self._logical_by_scope_id[scope_id]
        except KeyError as exc:
            raise ValueError("unknown internal scope identifier") from exc

    def _logical_operation_from_id(self, operation_id: str) -> str:
        try:
            return self._logical_by_operation_id[operation_id]
        except KeyError as exc:
            raise ValueError("unknown internal operation identifier") from exc


def _self_test() -> None:
    seed = hashlib.sha256(b"OpenCore-E001-surface-codec-self-test").digest()
    first = SurfaceCodec(seed)
    second = SurfaceCodec(seed)
    assert first.public_descriptor() == second.public_descriptor()
    for logical_scope in SCOPE_NAMES:
        for x in range(MODULUS):
            encoded = first.encode_observation(logical_scope, x, (x + 3) % MODULUS)
            decoded = first.decode_observation(encoded)
            assert first._logical_scope_from_id(decoded.scope_id) == logical_scope
            assert decoded.x == x and decoded.y == (x + 3) % MODULUS
    for scopes in (("A",), ("A", "B"), ("A", "C")):
        parsed = first.parse_scope_expression(first.encode_scope_expression(scopes))
        assert tuple(first._logical_scope_from_id(item) for item in parsed.scope_ids) == scopes
    descriptor = first.public_descriptor()
    assert "logical_scope_map" not in descriptor
    assert set(descriptor["scope_tokens"]).isdisjoint(SCOPE_NAMES)


if __name__ == "__main__":
    _self_test()
