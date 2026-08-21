"""Small canonical primitives shared by the frozen E001 apparatus.

This module deliberately contains no experiment seed, world rule, warrant,
authority, or subject/kernel behavior.  It only fixes serialization and the
domain-separated deterministic byte stream used by the pre-subject apparatus.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, is_dataclass
from typing import Any


CANONICAL_VERSION = "opencore.e001.canonical-json.v1"
STREAM_DOMAIN = b"OpenCore-K0-E001-SHA256-Stream-v1\x00"


class CanonicalError(ValueError):
    """Raised when a value cannot be represented canonically."""


def _plain(value: Any) -> Any:
    """Convert apparatus values into the deliberately small JSON domain."""

    if is_dataclass(value) and not isinstance(value, type):
        return _plain(asdict(value))
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise CanonicalError("floating-point values are outside canonical v1")
    if isinstance(value, bytes):
        return {"$bytes_hex": value.hex()}
    if isinstance(value, Mapping):
        converted: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalError("canonical object keys must be strings")
            converted[key] = _plain(item)
        return converted
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    raise CanonicalError(f"unsupported canonical type: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    """Return the unique UTF-8 JSON representation used by E001."""

    try:
        text = json.dumps(
            _plain(value),
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise CanonicalError(str(exc)) from exc
    return text.encode("utf-8")


def canonical_loads(payload: bytes | bytearray | memoryview) -> Any:
    """Decode canonical JSON and reject alternate byte representations."""

    raw = bytes(payload)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CanonicalError("invalid canonical JSON") from exc
    if canonical_bytes(value) != raw:
        raise CanonicalError("JSON bytes are valid but not canonical v1")
    return value


def sha256_bytes(domain: str, value: Any) -> bytes:
    """Hash a canonical value under an explicit ASCII domain."""

    try:
        domain_bytes = domain.encode("ascii")
    except UnicodeEncodeError as exc:
        raise CanonicalError("hash domains must be ASCII") from exc
    return hashlib.sha256(domain_bytes + b"\x00" + canonical_bytes(value)).digest()


def sha256_hex(domain: str, value: Any) -> str:
    return sha256_bytes(domain, value).hex()


def require_uint(value: Any, name: str, upper_exclusive: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    if upper_exclusive is not None and value >= upper_exclusive:
        raise ValueError(f"{name} must be less than {upper_exclusive}")
    return value


class Sha256Stream:
    """Domain-separated deterministic stream derived from one 32-byte seed.

    This is a reproducibility construction, not a claim of unpredictable or
    cryptographically isolated randomness.  Bounded draws use rejection rather
    than modulo reduction, making the mapping precisely specified.
    """

    def __init__(self, seed: bytes, domain: str):
        if not isinstance(seed, bytes) or len(seed) != 32:
            raise ValueError("seed must be exactly 32 bytes")
        try:
            domain_bytes = domain.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ValueError("stream domain must be ASCII") from exc
        if not domain_bytes:
            raise ValueError("stream domain must not be empty")
        self._seed = seed
        self._domain = domain_bytes
        self._counter = 0
        self._buffer = b""

    def _block(self) -> bytes:
        counter = self._counter.to_bytes(8, "big")
        self._counter += 1
        return hashlib.sha256(
            STREAM_DOMAIN
            + len(self._domain).to_bytes(2, "big")
            + self._domain
            + self._seed
            + counter
        ).digest()

    def take(self, length: int) -> bytes:
        require_uint(length, "length")
        while len(self._buffer) < length:
            self._buffer += self._block()
        result, self._buffer = self._buffer[:length], self._buffer[length:]
        return result

    def uint_below(self, bound: int) -> int:
        if isinstance(bound, bool) or not isinstance(bound, int) or bound <= 0:
            raise ValueError("bound must be a positive integer")
        width = max(1, (bound.bit_length() + 7) // 8)
        ceiling = 1 << (8 * width)
        cutoff = ceiling - (ceiling % bound)
        while True:
            draw = int.from_bytes(self.take(width), "big")
            if draw < cutoff:
                return draw % bound

    def permutation(self, values: Sequence[Any] | Iterable[Any]) -> tuple[Any, ...]:
        items = list(values)
        for index in range(len(items) - 1, 0, -1):
            swap = self.uint_below(index + 1)
            items[index], items[swap] = items[swap], items[index]
        return tuple(items)


def assert_unique(values: Sequence[str], name: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{name} contains duplicate values")

