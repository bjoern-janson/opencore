"""Frozen ordered-record query boundary for the E001 Archive rival."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol

try:
    from .archive_reducer import validate_record
    from .canonical import canonical_loads
    from .generic_index import GenericIndex
except ImportError:  # Direct execution from the apparatus directory.
    from archive_reducer import validate_record
    from canonical import canonical_loads
    from generic_index import GenericIndex


QUERY_SCHEMA = "opencore.e001.archive-query.v1"


class QueryOps(Protocol):
    def read_canonical(self, payload: bytes) -> bytes: ...

    def lookup_key(self, mapping: dict[str, Any], key: str) -> Any: ...


class ArchiveQuery:
    """Query immutable durable bytes in canonical sequence order.

    Exact-scope lookup is permitted only through the separately frozen generic
    index.  Record content is still fetched through `READ_CANONICAL`; the index
    never contains semantic content or a targeted active-state delta.
    """

    @staticmethod
    def run(
        ordered_canonical_record_stream: Sequence[bytes],
        reference_ops: QueryOps,
        *,
        exact_scope: str | None = None,
        index: GenericIndex | None = None,
    ) -> tuple[dict[str, Any], ...]:
        if exact_scope is not None and (not isinstance(exact_scope, str) or not exact_scope):
            raise ValueError("exact_scope must be null or a non-empty string")
        if exact_scope is not None and index is None:
            raise ValueError("exact-scope query requires the frozen generic index")
        if index is not None and len(index.all_record_ids) != len(
            ordered_canonical_record_stream
        ):
            raise ValueError("index and canonical record stream lengths differ")

        if exact_scope is None:
            positions = tuple(range(len(ordered_canonical_record_stream)))
            expected_ids: tuple[str, ...] | None = (
                None if index is None else index.all_record_ids
            )
        else:
            assert index is not None
            expected_ids = index.lookup_exact_scope(exact_scope, reference_ops)
            positions = tuple(
                index.lookup_position(record_id, reference_ops)
                for record_id in expected_ids
            )

        result: list[dict[str, Any]] = []
        prior_sequence = -1
        for offset, position in enumerate(positions):
            if position >= len(ordered_canonical_record_stream):
                raise ValueError("index position lies outside canonical record stream")
            raw = ordered_canonical_record_stream[position]
            if not isinstance(raw, bytes):
                raise ValueError("record stream entries must be canonical bytes")
            record = canonical_loads(reference_ops.read_canonical(raw))
            validate_record(record)
            if record["sequence"] <= prior_sequence:
                raise ValueError("query result is not in canonical sequence order")
            prior_sequence = record["sequence"]
            if exact_scope is not None and record["scope"] != exact_scope:
                raise ValueError("generic index returned a record outside exact scope")
            if expected_ids is not None and record["record_id"] != expected_ids[offset]:
                raise ValueError("index ID does not match canonical record bytes")
            result.append(record)
        return tuple(result)

