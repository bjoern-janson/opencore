"""Frozen fresh-state reducer for the E001 `ARCHIVE_REPLAY` rival."""

from __future__ import annotations

import re
from typing import Any, Iterable, Protocol

try:
    from .canonical import canonical_bytes, canonical_loads, sha256_hex
except ImportError:  # Direct execution from the apparatus directory.
    from canonical import canonical_bytes, canonical_loads, sha256_hex


RECORD_SCHEMA = "opencore.e001.archive-record.v1"
ACTIVE_STATE_SCHEMA = "opencore.e001.archive-active-state.v1"
RECORD_ID_DOMAIN = "OpenCore-K0-E001-ArchiveRecord-v1"
OPERATIONS = frozenset({"UPSERT", "RETIRE", "UNRESOLVED"})
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_RECORD_FIELDS = frozenset(
    {
        "schema",
        "record_id",
        "sequence",
        "scope",
        "operation",
        "commitment_key",
        "content",
        "parent_record_id",
        "evidence_digest",
        "warrant_digest",
        "commit_id",
        "receipt_id",
        "reference_contract_digest",
    }
)


class FoldOps(Protocol):
    def fold_record(self, state: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]: ...


def empty_state() -> dict[str, Any]:
    return {
        "schema": ACTIVE_STATE_SCHEMA,
        "entries": {},
        "scope_heads": {},
        "last_sequence": -1,
    }


def record_body(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key != "record_id"}


def compute_record_id(record_without_id: dict[str, Any]) -> str:
    if "record_id" in record_without_id:
        raise ValueError("record body must omit record_id")
    return sha256_hex(RECORD_ID_DOMAIN, record_without_id)


def make_record(
    *,
    sequence: int,
    scope: str,
    operation: str,
    commitment_key: str,
    content: Any,
    parent_record_id: str | None,
    evidence_digest: str,
    warrant_digest: str,
    commit_id: str,
    receipt_id: str,
    reference_contract_digest: str,
) -> dict[str, Any]:
    body = {
        "schema": RECORD_SCHEMA,
        "sequence": sequence,
        "scope": scope,
        "operation": operation,
        "commitment_key": commitment_key,
        "content": content,
        "parent_record_id": parent_record_id,
        "evidence_digest": evidence_digest,
        "warrant_digest": warrant_digest,
        "commit_id": commit_id,
        "receipt_id": receipt_id,
        "reference_contract_digest": reference_contract_digest,
    }
    record = {**body, "record_id": compute_record_id(body)}
    validate_record(record)
    return record


def validate_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict) or frozenset(record) != _RECORD_FIELDS:
        raise ValueError("archive record fields do not match record schema")
    if record["schema"] != RECORD_SCHEMA:
        raise ValueError("unknown archive record schema")
    sequence = record["sequence"]
    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
        raise ValueError("record sequence must be a non-negative integer")
    for name in ("scope", "commitment_key"):
        if not isinstance(record[name], str) or not record[name]:
            raise ValueError(f"{name} must be a non-empty string")
    if record["operation"] not in OPERATIONS:
        raise ValueError("unknown archive operation")
    if record["operation"] == "UPSERT" and record["content"] is None:
        raise ValueError("UPSERT content must not be null")
    if record["operation"] != "UPSERT" and record["content"] is not None:
        raise ValueError("RETIRE and UNRESOLVED content must be null")
    parent = record["parent_record_id"]
    if parent is not None and (not isinstance(parent, str) or _DIGEST.fullmatch(parent) is None):
        raise ValueError("parent_record_id must be null or a lowercase SHA-256 digest")
    for name in (
        "record_id",
        "evidence_digest",
        "warrant_digest",
        "commit_id",
        "receipt_id",
        "reference_contract_digest",
    ):
        if not isinstance(record[name], str) or _DIGEST.fullmatch(record[name]) is None:
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")
    if compute_record_id(record_body(record)) != record["record_id"]:
        raise ValueError("archive record_id does not match canonical body")
    # Reject values that canonical JSON v1 cannot round-trip.
    canonical_loads(canonical_bytes(record))
    return record


def validate_state(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict) or set(state) != {
        "schema",
        "entries",
        "scope_heads",
        "last_sequence",
    }:
        raise ValueError("active state fields do not match schema")
    if state["schema"] != ACTIVE_STATE_SCHEMA:
        raise ValueError("unknown active state schema")
    if not isinstance(state["entries"], dict) or not isinstance(state["scope_heads"], dict):
        raise ValueError("entries and scope_heads must be objects")
    last_sequence = state["last_sequence"]
    if isinstance(last_sequence, bool) or not isinstance(last_sequence, int) or last_sequence < -1:
        raise ValueError("last_sequence must be an integer >= -1")
    canonical_loads(canonical_bytes(state))
    return state


def fold_record_unmetered(
    state: dict[str, Any], record: dict[str, Any]
) -> dict[str, Any]:
    """Normative single-record semantics, called only inside the meter API."""

    validate_state(state)
    validate_record(record)
    if record["sequence"] <= state["last_sequence"]:
        raise ValueError("records must be folded in strictly increasing sequence order")
    scope = record["scope"]
    expected_parent = state["scope_heads"].get(scope)
    if record["parent_record_id"] != expected_parent:
        raise ValueError("record parent does not match current exact-scope head")

    successor = canonical_loads(canonical_bytes(state))
    operation = record["operation"]
    if operation == "UPSERT":
        successor["entries"][scope] = {
            "status": "ACTIVE",
            "commitment_key": record["commitment_key"],
            "content": record["content"],
            "source_record_id": record["record_id"],
        }
    elif operation == "RETIRE":
        successor["entries"].pop(scope, None)
    else:
        successor["entries"][scope] = {
            "status": "UNRESOLVED",
            "commitment_key": record["commitment_key"],
            "content": None,
            "source_record_id": record["record_id"],
        }
    successor["scope_heads"][scope] = record["record_id"]
    successor["last_sequence"] = record["sequence"]
    return validate_state(successor)


class ArchiveReducer:
    """Replay immutable records into fresh active state; never patch current state."""

    @staticmethod
    def fold(
        initial_state: dict[str, Any],
        records: Iterable[dict[str, Any]],
        reference_ops: FoldOps,
    ) -> dict[str, Any]:
        if canonical_bytes(initial_state) != canonical_bytes(empty_state()):
            raise ValueError("ArchiveReducer must start from exact fresh empty state")
        state = empty_state()
        for record in records:
            state = reference_ops.fold_record(state, record)
        return state

