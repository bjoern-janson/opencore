"""Frozen generic exact-scope index for the E001 Archive rival."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Protocol

try:
    from .archive_reducer import validate_record
    from .canonical import canonical_bytes, canonical_loads
except ImportError:  # Direct execution from the apparatus directory.
    from archive_reducer import validate_record
    from canonical import canonical_bytes, canonical_loads


INDEX_SCHEMA = "opencore.e001.generic-exact-scope-index.v1"


class LookupOps(Protocol):
    def lookup_key(self, mapping: dict[str, Any], key: str) -> Any: ...


@dataclass(frozen=True, slots=True)
class GenericIndex:
    """Immutable IDs only; no record content, rule, answer, or authority data."""

    all_record_ids: tuple[str, ...]
    by_scope: dict[str, tuple[str, ...]]
    position_by_id: dict[str, int]
    last_sequence: int

    @classmethod
    def build(cls, records: Iterable[dict[str, Any]]) -> "GenericIndex":
        index = cls((), {}, {}, -1)
        for record in records:
            index = index.append(record)
        return index

    def append(self, record: dict[str, Any]) -> "GenericIndex":
        validate_record(record)
        if record["sequence"] <= self.last_sequence:
            raise ValueError("index records must have strictly increasing sequences")
        if record["record_id"] in self.all_record_ids:
            raise ValueError("index cannot contain a duplicate record ID")
        by_scope = {scope: tuple(ids) for scope, ids in self.by_scope.items()}
        by_scope[record["scope"]] = by_scope.get(record["scope"], ()) + (
            record["record_id"],
        )
        return GenericIndex(
            all_record_ids=self.all_record_ids + (record["record_id"],),
            by_scope=by_scope,
            position_by_id={
                **self.position_by_id,
                record["record_id"]: len(self.all_record_ids),
            },
            last_sequence=record["sequence"],
        )

    def lookup_exact_scope(self, scope: str, reference_ops: LookupOps) -> tuple[str, ...]:
        if not isinstance(scope, str) or not scope:
            raise ValueError("scope must be a non-empty string")
        result = reference_ops.lookup_key(
            {key: list(ids) for key, ids in self.by_scope.items()}, scope
        )
        if not isinstance(result, list) or not all(isinstance(item, str) for item in result):
            raise ValueError("meter returned an invalid index result")
        return tuple(result)

    def lookup_position(self, record_id: str, reference_ops: LookupOps) -> int:
        if not isinstance(record_id, str):
            raise ValueError("record_id must be a string")
        result = reference_ops.lookup_key(self.position_by_id, record_id)
        if isinstance(result, bool) or not isinstance(result, int) or result < 0:
            raise ValueError("meter returned an invalid record position")
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": INDEX_SCHEMA,
            "all_record_ids": list(self.all_record_ids),
            "by_scope": {scope: list(ids) for scope, ids in self.by_scope.items()},
            "position_by_id": dict(self.position_by_id),
            "last_sequence": self.last_sequence,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "GenericIndex":
        if not isinstance(value, dict) or set(value) != {
            "schema",
            "all_record_ids",
            "by_scope",
            "position_by_id",
            "last_sequence",
        }:
            raise ValueError("index fields do not match schema")
        if value["schema"] != INDEX_SCHEMA:
            raise ValueError("unknown index schema")
        if not isinstance(value["all_record_ids"], list) or not all(
            isinstance(item, str) for item in value["all_record_ids"]
        ):
            raise ValueError("all_record_ids must be a string list")
        if not isinstance(value["by_scope"], dict) or not all(
            isinstance(scope, str)
            and isinstance(ids, list)
            and all(isinstance(item, str) for item in ids)
            for scope, ids in value["by_scope"].items()
        ):
            raise ValueError("by_scope must map strings to string lists")
        if not isinstance(value["position_by_id"], dict) or not all(
            isinstance(record_id, str)
            and not isinstance(position, bool)
            and isinstance(position, int)
            and position >= 0
            for record_id, position in value["position_by_id"].items()
        ):
            raise ValueError("position_by_id must map strings to non-negative integers")
        last_sequence = value["last_sequence"]
        if isinstance(last_sequence, bool) or not isinstance(last_sequence, int) or last_sequence < -1:
            raise ValueError("last_sequence must be an integer >= -1")
        canonical_loads(canonical_bytes(value))
        index = cls(
            tuple(value["all_record_ids"]),
            {scope: tuple(ids) for scope, ids in value["by_scope"].items()},
            dict(value["position_by_id"]),
            last_sequence,
        )
        flattened = [item for ids in index.by_scope.values() for item in ids]
        if len(flattened) != len(set(flattened)) or set(flattened) != set(
            index.all_record_ids
        ):
            raise ValueError("index scope lists do not partition all record IDs")
        expected_positions = {
            record_id: position
            for position, record_id in enumerate(index.all_record_ids)
        }
        if index.position_by_id != expected_positions:
            raise ValueError("position_by_id does not match canonical record order")
        return index

    def canonical_size(self) -> int:
        return len(canonical_bytes(self.to_dict()))
