"""Normative deterministic operation/byte/tick meter for E001 Phase 5.

The meter performs the frozen reference operations itself and emits a hash-
chained trace that this same source can replay.  It contains no world oracle,
evaluator, warrant, capability, persistence, or adjudication decision logic.
External calls are attributed tick markers whose supplied responses remain
external inputs.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, ClassVar

try:
    from .archive_reducer import fold_record_unmetered
    from .canonical import canonical_bytes, canonical_loads, sha256_hex
    from .hypothesis_library import AffineMap, compose
except ImportError:  # Direct execution from the apparatus directory.
    from archive_reducer import fold_record_unmetered
    from canonical import canonical_bytes, canonical_loads, sha256_hex
    from hypothesis_library import AffineMap, compose


TRACE_SCHEMA = "opencore.e001.reference-meter-trace.v1"
EVENT_DOMAIN = "OpenCore-K0-E001-MeterEvent-v1"
ZERO_EVENT_DIGEST = "0" * 64
REFERENCE_OPERATIONS = frozenset(
    {
        "READ_CANONICAL",
        "FOLD_RECORD",
        "LOOKUP_KEY",
        "APPLY_AFFINE",
        "COMPOSE",
        "BUILD_DELTA",
        "COMPARE",
        "HASH_BLOCK_32",
    }
)
EXTERNAL_CALLS = frozenset({"EVALUATOR", "AUTHORITY", "PERSISTENCE", "READBACK"})
EXTERNAL_STATUSES = {
    "EVALUATOR": frozenset(
        {"WARRANTED", "NOT_WARRANTED", "UNDERDETERMINED", "PROTOCOL_FAILURE"}
    ),
    "AUTHORITY": frozenset(
        {"VALID", "INVALID", "EXPIRED", "REVOKED", "PROTOCOL_FAILURE"}
    ),
    "PERSISTENCE": frozenset(
        {"DURABLE", "PENDING", "FAILED", "PROTOCOL_FAILURE"}
    ),
    "READBACK": frozenset(
        {"AVAILABLE", "MISSING", "MISMATCH", "PROTOCOL_FAILURE"}
    ),
}
ARTIFACT_REQUIRED_STATUSES = frozenset(
    {
        ("EVALUATOR", "WARRANTED"),
        ("AUTHORITY", "VALID"),
        ("PERSISTENCE", "DURABLE"),
        ("READBACK", "AVAILABLE"),
    }
)


class MeterLimitExceeded(RuntimeError):
    def __init__(self, dimension: str, attempted: int, maximum: int):
        super().__init__(f"{dimension} limit exceeded: {attempted} > {maximum}")
        self.dimension = dimension
        self.attempted = attempted
        self.maximum = maximum


class InvalidMeterTrace(ValueError):
    pass


def _optional_limit(value: Any, name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be null or a non-negative integer")
    return value


def _digest_or_none(value: Any, name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ValueError(f"{name} must be null or a lowercase SHA-256 digest")
    return value


@dataclass(frozen=True, slots=True)
class MeterLimits:
    max_canonical_bytes: int | None
    max_reference_ops: int | None
    max_ticks: int | None

    def __post_init__(self) -> None:
        _optional_limit(self.max_canonical_bytes, "max_canonical_bytes")
        _optional_limit(self.max_reference_ops, "max_reference_ops")
        _optional_limit(self.max_ticks, "max_ticks")

    @classmethod
    def unbounded(cls) -> "MeterLimits":
        return cls(None, None, None)

    def to_dict(self) -> dict[str, int | None]:
        return {
            "max_canonical_bytes": self.max_canonical_bytes,
            "max_reference_ops": self.max_reference_ops,
            "max_ticks": self.max_ticks,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "MeterLimits":
        if not isinstance(value, dict) or set(value) != {
            "max_canonical_bytes",
            "max_reference_ops",
            "max_ticks",
        }:
            raise ValueError("meter limit fields do not match schema")
        return cls(
            value["max_canonical_bytes"],
            value["max_reference_ops"],
            value["max_ticks"],
        )


@dataclass(frozen=True, slots=True)
class MeterTotals:
    canonical_bytes_accessed: int = 0
    reference_ops: int = 0
    ticks: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "canonical_bytes_accessed": self.canonical_bytes_accessed,
            "reference_ops": self.reference_ops,
            "ticks": self.ticks,
        }


class ReferenceMeter:
    """Frozen operation boundary and deterministic trace interpreter."""

    operation_names: ClassVar[frozenset[str]] = REFERENCE_OPERATIONS

    def __init__(self, limits: MeterLimits):
        if not isinstance(limits, MeterLimits):
            raise TypeError("limits must be MeterLimits")
        self.limits = limits
        self._totals = MeterTotals()
        self._events: list[dict[str, Any]] = []
        self._event_digest = ZERO_EVENT_DIGEST
        self._pending_artifact_digest: str | None = None

    @property
    def totals(self) -> MeterTotals:
        return self._totals

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(canonical_loads(canonical_bytes(item)) for item in self._events)

    def _admit(self, byte_delta: int, op_delta: int, tick_delta: int) -> None:
        attempted = {
            "canonical_bytes_accessed": self._totals.canonical_bytes_accessed
            + byte_delta,
            "reference_ops": self._totals.reference_ops + op_delta,
            "ticks": self._totals.ticks + tick_delta,
        }
        maxima = {
            "canonical_bytes_accessed": self.limits.max_canonical_bytes,
            "reference_ops": self.limits.max_reference_ops,
            "ticks": self.limits.max_ticks,
        }
        for name in ("canonical_bytes_accessed", "reference_ops", "ticks"):
            maximum = maxima[name]
            if maximum is not None and attempted[name] > maximum:
                raise MeterLimitExceeded(name, attempted[name], maximum)

    def _append(
        self,
        *,
        kind: str,
        name: str,
        arguments: Any,
        result: Any,
        byte_delta: int,
        op_delta: int,
    ) -> None:
        tick_delta = 1
        self._admit(byte_delta, op_delta, tick_delta)
        body = {
            "sequence": len(self._events),
            "kind": kind,
            "name": name,
            "arguments": arguments,
            "result": result,
            "canonical_bytes_delta": byte_delta,
            "reference_ops_delta": op_delta,
            "tick_delta": tick_delta,
            "previous_event_digest": self._event_digest,
        }
        event_digest = sha256_hex(EVENT_DOMAIN, body)
        event = canonical_loads(
            canonical_bytes({**body, "event_digest": event_digest})
        )
        self._events.append(event)
        self._event_digest = event_digest
        self._totals = MeterTotals(
            canonical_bytes_accessed=self._totals.canonical_bytes_accessed
            + byte_delta,
            reference_ops=self._totals.reference_ops + op_delta,
            ticks=self._totals.ticks + tick_delta,
        )

    def _operation(
        self,
        name: str,
        arguments: Any,
        result: Any,
        *,
        byte_delta: int = 0,
    ) -> Any:
        if name not in REFERENCE_OPERATIONS:
            raise ValueError("unknown reference operation")
        expected_artifact_digest = (
            arguments.get("expected_artifact_digest")
            if name == "READ_CANONICAL" and isinstance(arguments, dict)
            else None
        )
        if self._pending_artifact_digest is not None:
            if (
                name != "READ_CANONICAL"
                or expected_artifact_digest != self._pending_artifact_digest
            ):
                raise ValueError(
                    "pending external artifact must be the next reference operation"
                )
        elif expected_artifact_digest is not None:
            raise ValueError("artifact-bound read has no pending external envelope")
        self._append(
            kind="REFERENCE_OP",
            name=name,
            arguments=arguments,
            result=result,
            byte_delta=byte_delta,
            op_delta=1,
        )
        if expected_artifact_digest is not None:
            self._pending_artifact_digest = None
        return result

    def read_canonical(self, payload: bytes) -> bytes:
        return self._read_canonical(payload, expected_artifact_digest=None)

    def _read_canonical(
        self, payload: bytes, expected_artifact_digest: str | None
    ) -> bytes:
        if not isinstance(payload, bytes):
            raise ValueError("READ_CANONICAL payload must be bytes")
        canonical_loads(payload)
        if expected_artifact_digest is not None:
            _digest_or_none(expected_artifact_digest, "expected_artifact_digest")
            if hashlib.sha256(payload).hexdigest() != expected_artifact_digest:
                raise ValueError(
                    "external artifact bytes do not match expected artifact digest"
                )
        self._operation(
            "READ_CANONICAL",
            {
                "payload_hex": payload.hex(),
                "expected_artifact_digest": expected_artifact_digest,
            },
            {"payload_hex": payload.hex()},
            byte_delta=len(payload),
        )
        return payload

    def read_external_artifact(self, payload: bytes, artifact_digest: str) -> bytes:
        """Read externally supplied artifact bytes through `READ_CANONICAL`.

        `external_call` can carry only the artifact's raw SHA-256 digest and a
        typed status.  Any result-bearing canonical artifact must therefore be
        supplied separately here, where its exact bytes are charged and traced.
        """

        _digest_or_none(artifact_digest, "artifact_digest")
        if artifact_digest is None:
            raise ValueError("artifact_digest must not be null for an artifact read")
        if self._pending_artifact_digest != artifact_digest:
            raise ValueError("artifact digest does not match pending external envelope")
        if not isinstance(payload, bytes):
            raise ValueError("external artifact payload must be bytes")
        if hashlib.sha256(payload).hexdigest() != artifact_digest:
            raise ValueError("external artifact bytes do not match envelope digest")
        return self._read_canonical(
            payload, expected_artifact_digest=artifact_digest
        )

    def lookup_key(self, mapping: dict[str, Any], key: str) -> Any:
        if not isinstance(mapping, dict) or not all(
            isinstance(item, str) for item in mapping
        ):
            raise ValueError("LOOKUP_KEY mapping must have string keys")
        if not isinstance(key, str):
            raise ValueError("LOOKUP_KEY key must be a string")
        canonical_loads(canonical_bytes(mapping))
        result = mapping.get(key, [])
        byte_delta = len(canonical_bytes(key)) + len(canonical_bytes(result))
        return self._operation(
            "LOOKUP_KEY",
            {"mapping": mapping, "key": key},
            result,
            byte_delta=byte_delta,
        )

    def fold_record(
        self, state: dict[str, Any], record: dict[str, Any]
    ) -> dict[str, Any]:
        result = fold_record_unmetered(state, record)
        return self._operation(
            "FOLD_RECORD", {"state": state, "record": record}, result
        )

    def apply_affine(self, transform: dict[str, Any], x: int) -> int:
        affine = AffineMap.from_dict(transform)
        result = affine.apply(x)
        return self._operation(
            "APPLY_AFFINE", {"transform": transform, "x": x}, result
        )

    def compose(
        self, outer: dict[str, Any], inner: dict[str, Any]
    ) -> dict[str, Any]:
        result = compose(AffineMap.from_dict(outer), AffineMap.from_dict(inner)).to_dict()
        return self._operation(
            "COMPOSE", {"outer": outer, "inner": inner}, result
        )

    def build_delta(self, scope: str, before: Any, after: Any) -> dict[str, Any]:
        if not isinstance(scope, str) or not scope:
            raise ValueError("BUILD_DELTA scope must be a non-empty string")
        if before is None and after is None:
            raise ValueError("BUILD_DELTA cannot map null to null")
        result = {
            "schema": "opencore.e001.replacement-delta.v1",
            "scope": scope,
            "operation": "RETIRE" if after is None else "UPSERT",
            "before_digest": sha256_hex(
                "OpenCore-K0-E001-DeltaBefore-v1", before
            ),
            "after": after,
        }
        return self._operation(
            "BUILD_DELTA",
            {"scope": scope, "before": before, "after": after},
            result,
        )

    def compare(self, left: Any, right: Any) -> bool:
        result = canonical_bytes(left) == canonical_bytes(right)
        return self._operation("COMPARE", {"left": left, "right": right}, result)

    def hash_block_32(self, block: bytes) -> str:
        if not isinstance(block, bytes) or len(block) != 32:
            raise ValueError("HASH_BLOCK_32 requires exactly 32 bytes")
        result = hashlib.sha256(block).hexdigest()
        return self._operation(
            "HASH_BLOCK_32", {"block_hex": block.hex()}, result
        )

    def external_call(self, name: str, request: Any, response: Any) -> Any:
        """Attribute one external decision using a non-semantic envelope only.

        This method intentionally cannot return result-bearing object bytes.
        Requests bind only their already-canonical digest; responses contain a
        typed status and, optionally, the raw SHA-256 digest of a separately
        supplied canonical artifact.  The artifact must cross
        `read_external_artifact`, which emits and charges `READ_CANONICAL`.
        """

        if name not in EXTERNAL_CALLS:
            raise ValueError("unknown external call class")
        if self._pending_artifact_digest is not None:
            raise ValueError("pending external artifact must be read before another call")
        if not isinstance(request, dict) or set(request) != {"request_digest"}:
            raise ValueError("external request must be a digest-only envelope")
        _digest_or_none(request["request_digest"], "request_digest")
        if request["request_digest"] is None:
            raise ValueError("request_digest must not be null")
        if not isinstance(response, dict) or set(response) != {
            "status",
            "artifact_digest",
        }:
            raise ValueError("external response must be a status/digest-only envelope")
        if response["status"] not in EXTERNAL_STATUSES[name]:
            raise ValueError("external response status is invalid for call class")
        artifact_digest = _digest_or_none(
            response["artifact_digest"], "artifact_digest"
        )
        if (name, response["status"]) in ARTIFACT_REQUIRED_STATUSES and artifact_digest is None:
            raise ValueError("successful external status requires an artifact digest")
        self._append(
            kind="EXTERNAL_CALL",
            name=name,
            arguments={"request": request},
            result=response,
            byte_delta=0,
            op_delta=0,
        )
        self._pending_artifact_digest = artifact_digest
        return response

    def export_trace(self) -> dict[str, Any]:
        if self._pending_artifact_digest is not None:
            raise ValueError("cannot export a trace with an unread external artifact")
        return {
            "schema": TRACE_SCHEMA,
            "limits": self.limits.to_dict(),
            "events": list(self.events),
            "totals": self._totals.to_dict(),
            "final_event_digest": self._event_digest,
        }

    @classmethod
    def replay(cls, trace: Any) -> "ReferenceMeter":
        """Re-execute every normative operation and verify the exact trace."""

        if not isinstance(trace, dict) or set(trace) != {
            "schema",
            "limits",
            "events",
            "totals",
            "final_event_digest",
        }:
            raise InvalidMeterTrace("trace fields do not match schema")
        if trace["schema"] != TRACE_SCHEMA or not isinstance(trace["events"], list):
            raise InvalidMeterTrace("unknown trace schema or invalid events")
        try:
            replayed = cls(MeterLimits.from_dict(trace["limits"]))
            for expected in trace["events"]:
                if not isinstance(expected, dict):
                    raise InvalidMeterTrace("trace event must be an object")
                name = expected.get("name")
                arguments = expected.get("arguments")
                kind = expected.get("kind")
                if kind == "EXTERNAL_CALL":
                    replayed.external_call(
                        name, arguments["request"], expected.get("result")
                    )
                elif kind == "REFERENCE_OP":
                    replayed._replay_operation(name, arguments)
                else:
                    raise InvalidMeterTrace("unknown trace event kind")
                if replayed._events[-1] != expected:
                    raise InvalidMeterTrace("replayed event differs from trace")
        except InvalidMeterTrace:
            raise
        except Exception as exc:
            raise InvalidMeterTrace("trace operation could not be replayed") from exc
        if replayed._totals.to_dict() != trace["totals"]:
            raise InvalidMeterTrace("trace totals do not match replay")
        if replayed._pending_artifact_digest is not None:
            raise InvalidMeterTrace("trace ends with an unread external artifact")
        if replayed._event_digest != trace["final_event_digest"]:
            raise InvalidMeterTrace("trace final digest does not match replay")
        return replayed

    def _replay_operation(self, name: str, arguments: Any) -> None:
        if not isinstance(arguments, dict):
            raise InvalidMeterTrace("operation arguments must be an object")
        if name == "READ_CANONICAL":
            if set(arguments) != {"payload_hex", "expected_artifact_digest"}:
                raise InvalidMeterTrace("READ_CANONICAL arguments do not match schema")
            self._read_canonical(
                bytes.fromhex(arguments["payload_hex"]),
                arguments["expected_artifact_digest"],
            )
        elif name == "FOLD_RECORD":
            self.fold_record(arguments["state"], arguments["record"])
        elif name == "LOOKUP_KEY":
            self.lookup_key(arguments["mapping"], arguments["key"])
        elif name == "APPLY_AFFINE":
            self.apply_affine(arguments["transform"], arguments["x"])
        elif name == "COMPOSE":
            self.compose(arguments["outer"], arguments["inner"])
        elif name == "BUILD_DELTA":
            self.build_delta(
                arguments["scope"], arguments["before"], arguments["after"]
            )
        elif name == "COMPARE":
            self.compare(arguments["left"], arguments["right"])
        elif name == "HASH_BLOCK_32":
            self.hash_block_32(bytes.fromhex(arguments["block_hex"]))
        else:
            raise InvalidMeterTrace("unknown reference operation")


def _self_test() -> None:
    meter = ReferenceMeter(MeterLimits(4096, 32, 64))
    raw = canonical_bytes({"value": 3})
    assert meter.read_canonical(raw) == raw
    assert meter.lookup_key({"x": [1, 2]}, "x") == [1, 2]
    assert meter.apply_affine(AffineMap(3, 4).to_dict(), 2) == 10
    assert meter.compose(AffineMap(3, 4).to_dict(), AffineMap(2, 1).to_dict()) == AffineMap(
        6, 7
    ).to_dict()
    assert meter.compare({"x": 1}, {"x": 1})
    assert meter.hash_block_32(bytes(32)) == hashlib.sha256(bytes(32)).hexdigest()
    artifact = canonical_bytes({"status": "warranted", "scope": "fixture"})
    artifact_digest = hashlib.sha256(artifact).hexdigest()
    meter.external_call(
        "EVALUATOR",
        {"request_digest": hashlib.sha256(b"request").hexdigest()},
        {"status": "WARRANTED", "artifact_digest": artifact_digest},
    )
    before_read = meter.totals.canonical_bytes_accessed
    assert meter.read_external_artifact(artifact, artifact_digest) == artifact
    assert meter.totals.canonical_bytes_accessed - before_read == len(artifact)
    replayed = ReferenceMeter.replay(meter.export_trace())
    assert replayed.export_trace() == meter.export_trace()


if __name__ == "__main__":
    _self_test()
