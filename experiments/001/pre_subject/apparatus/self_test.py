"""Deterministic, standard-library-only tests for the E001 apparatus sources."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import archive_reducer
import canonical
import hypothesis_library
import proposer
import reference_meter
import surface_codec
import world_generator
from archive_query import ArchiveQuery
from archive_reducer import ArchiveReducer, empty_state, make_record
from canonical import canonical_bytes
from generic_index import GenericIndex
from hypothesis_library import AffineMap, HYPOTHESES, MODULUS, compose
from reference_meter import MeterLimitExceeded, MeterLimits, ReferenceMeter


HERE = Path(__file__).resolve().parent


def _digest(label: str) -> str:
    return hashlib.sha256(label.encode("ascii")).hexdigest()


def _rechain_trace(trace: dict) -> None:
    previous = reference_meter.ZERO_EVENT_DIGEST
    for event in trace["events"]:
        event["previous_event_digest"] = previous
        body = {key: value for key, value in event.items() if key != "event_digest"}
        event["event_digest"] = canonical.sha256_hex(
            reference_meter.EVENT_DOMAIN, body
        )
        previous = event["event_digest"]
    trace["final_event_digest"] = previous


def test_modules() -> None:
    canonical.assert_unique(("a", "b"), "fixture")
    hypothesis_library._self_test()
    surface_codec._self_test()
    world_generator._self_test()
    proposer._self_test()
    reference_meter._self_test()



def _adapter_scope_ids(codec: surface_codec.SurfaceCodec) -> dict[str, str]:
    """Recover only the adapter-facing IDs attached to legal public surfaces."""

    a_id = codec.scope_to_internal(codec.encode_scope("A"))
    b_id = codec.scope_to_internal(codec.encode_scope("B"))
    parsed = codec.parse_scope_expression(codec.encode_scope_expression(("A", "C")))
    c_id = parsed.scope_ids[1]
    return {"A": a_id, "B": b_id, "C": c_id}


def test_scope_id_isolation() -> None:
    """Reject the recovered fixed-ID channel without changing K0 semantics.

    A subject trained on the 32 public development worlds must not be able to
    carry a literal adapter-facing scope-ID -> A/B/C codebook into fresh worlds.
    The identifiers remain deterministic within a world, but their bytes must be
    seed-derived across worlds.  The audit seeds below are synthetic test inputs,
    not the sealed E001 evaluation seeds.
    """

    development_codebook: dict[str, str] = {}
    development_ids: set[str] = set()
    for index in range(32):
        codec = surface_codec.SurfaceCodec(world_generator.development_seed(index))
        first = _adapter_scope_ids(codec)
        second = _adapter_scope_ids(surface_codec.SurfaceCodec(world_generator.development_seed(index)))
        assert first == second
        assert len(set(first.values())) == len(surface_codec.SCOPE_NAMES)
        for logical, scope_id in first.items():
            previous = development_codebook.setdefault(scope_id, logical)
            assert previous == logical
            development_ids.add(scope_id)

    # With seed-derived 96-bit IDs, the public development set should not reuse
    # an adapter-facing scope identifier at all.  This is an apparatus invariant,
    # not a probabilistic security claim.
    assert len(development_ids) == 32 * len(surface_codec.SCOPE_NAMES)

    fresh_ids: set[str] = set()
    for index in range(256):
        seed = hashlib.sha256(
            b"OpenCore-E001-scope-id-isolation-audit-v1"
            + index.to_bytes(4, "big")
        ).digest()
        ids = _adapter_scope_ids(surface_codec.SurfaceCodec(seed))
        assert len(set(ids.values())) == len(surface_codec.SCOPE_NAMES)
        for scope_id in ids.values():
            # The exact exploit found in the recovered worktree was a literal
            # cross-seed codebook.  No fresh adapter-facing ID may hit it.
            assert scope_id not in development_codebook
            assert scope_id not in fresh_ids
            fresh_ids.add(scope_id)


def test_world_and_proposer() -> None:
    world = world_generator.generate_world(world_generator.development_seed(0))
    for role in world_generator.MAP_ROLES:
        decoded = tuple(
            world.codec.decode_observation(item) for item in world.encoded_evidence(role)
        )
        meter = ReferenceMeter(MeterLimits.unbounded())
        result = proposer.propose(((item.x, item.y) for item in decoded), meter)
        assert result.status == "UNIQUE"
        assert result.candidate == world.transformations[role]
        assert ReferenceMeter.replay(meter.export_trace()).export_trace() == meter.export_trace()

    assert world.apply_sequence("A", "B", "e0", 4) == compose(
        world.transformations["B"], world.transformations["A0"]
    ).apply(4)
    assert world.apply_sequence("A", "C", "e0", 4) is None


def _archive_records() -> tuple[dict, dict, dict]:
    common = {
        "evidence_digest": _digest("evidence"),
        "warrant_digest": _digest("warrant"),
        "reference_contract_digest": _digest("contract"),
    }
    a0 = make_record(
        sequence=0,
        scope="scope-a",
        operation="UPSERT",
        commitment_key="A0",
        content=AffineMap(2, 3).to_dict(),
        parent_record_id=None,
        commit_id=_digest("commit-a0"),
        receipt_id=_digest("receipt-a0"),
        **common,
    )
    b = make_record(
        sequence=1,
        scope="scope-b",
        operation="UPSERT",
        commitment_key="B",
        content=AffineMap(5, 1).to_dict(),
        parent_record_id=None,
        commit_id=_digest("commit-b"),
        receipt_id=_digest("receipt-b"),
        **common,
    )
    a1 = make_record(
        sequence=2,
        scope="scope-a",
        operation="UPSERT",
        commitment_key="A1",
        content=AffineMap(7, 4).to_dict(),
        parent_record_id=a0["record_id"],
        commit_id=_digest("commit-a1"),
        receipt_id=_digest("receipt-a1"),
        **common,
    )
    return a0, b, a1


def test_archive_rival() -> None:
    records = _archive_records()
    stream = tuple(canonical_bytes(record) for record in records)
    index = GenericIndex.build(records)
    assert GenericIndex.from_dict(index.to_dict()).to_dict() == index.to_dict()
    assert index.canonical_size() == len(canonical_bytes(index.to_dict()))

    meter = ReferenceMeter(MeterLimits.unbounded())
    queried = ArchiveQuery.run(stream, meter, index=index)
    state = ArchiveReducer.fold(empty_state(), queried, meter)
    assert state["entries"]["scope-a"]["commitment_key"] == "A1"
    assert state["entries"]["scope-b"]["commitment_key"] == "B"
    trace = meter.export_trace()
    assert ReferenceMeter.replay(trace).export_trace() == trace

    scoped_meter = ReferenceMeter(MeterLimits.unbounded())
    scoped = ArchiveQuery.run(
        stream, scoped_meter, exact_scope="scope-a", index=index
    )
    assert tuple(record["record_id"] for record in scoped) == (
        records[0]["record_id"],
        records[2]["record_id"],
    )
    scoped_state = ArchiveReducer.fold(empty_state(), scoped, scoped_meter)
    assert set(scoped_state["entries"]) == {"scope-a"}
    assert scoped_state["entries"]["scope-a"]["commitment_key"] == "A1"

    try:
        ArchiveReducer.fold(state, (), ReferenceMeter(MeterLimits.unbounded()))
    except ValueError as exc:
        assert "fresh empty state" in str(exc)
    else:
        raise AssertionError("ArchiveReducer accepted existing active state")


def test_meter_limits_and_trace_integrity() -> None:
    raw = canonical_bytes({"payload": list(range(20))})
    meter = ReferenceMeter(MeterLimits(len(raw) - 1, 10, 10))
    try:
        meter.read_canonical(raw)
    except MeterLimitExceeded as exc:
        assert exc.dimension == "canonical_bytes_accessed"
        assert meter.totals.canonical_bytes_accessed == 0
    else:
        raise AssertionError("byte envelope was not enforced")

    meter = ReferenceMeter(MeterLimits.unbounded())
    meter.hash_block_32(bytes(range(32)))
    trace = meter.export_trace()
    tampered = json.loads(json.dumps(trace))
    tampered["events"][0]["result"] = "0" * 64
    try:
        ReferenceMeter.replay(tampered)
    except reference_meter.InvalidMeterTrace:
        pass
    else:
        raise AssertionError("tampered trace replayed successfully")


def test_external_call_payload_boundary() -> None:
    request_digest = _digest("external-request")
    artifact = canonical_bytes(
        {"schema": "fixture.external-artifact.v1", "payload": "x" * 512}
    )
    artifact_digest = hashlib.sha256(artifact).hexdigest()
    meter = ReferenceMeter(MeterLimits.unbounded())

    try:
        meter.external_call(
            "EVALUATOR",
            {"request_digest": request_digest},
            {
                "status": "WARRANTED",
                "artifact_digest": artifact_digest,
                "semantic_payload": artifact.hex(),
            },
        )
    except ValueError as exc:
        assert "status/digest-only" in str(exc)
        assert meter.totals.ticks == 0
    else:
        raise AssertionError("external_call accepted unmetered semantic payload")

    envelope = meter.external_call(
        "EVALUATOR",
        {"request_digest": request_digest},
        {"status": "WARRANTED", "artifact_digest": artifact_digest},
    )
    assert envelope == {"status": "WARRANTED", "artifact_digest": artifact_digest}
    assert meter.totals.canonical_bytes_accessed == 0
    assert meter.totals.ticks == 1
    try:
        meter.export_trace()
    except ValueError as exc:
        assert "unread external artifact" in str(exc)
    else:
        raise AssertionError("trace exported before its external artifact was read")

    assert meter.read_external_artifact(artifact, artifact_digest) == artifact
    assert meter.totals.canonical_bytes_accessed == len(artifact)
    assert meter.totals.reference_ops == 1
    assert meter.totals.ticks == 2

    try:
        meter.read_external_artifact(artifact, "0" * 64)
    except ValueError as exc:
        assert "does not match" in str(exc)
        assert meter.totals.canonical_bytes_accessed == len(artifact)
    else:
        raise AssertionError("external artifact digest mismatch was accepted")

    replayed = ReferenceMeter.replay(meter.export_trace())
    assert replayed.export_trace() == meter.export_trace()

    rebound = json.loads(json.dumps(meter.export_trace()))
    bound_read = next(
        event
        for event in rebound["events"]
        if event["name"] == "READ_CANONICAL"
        and event["arguments"]["expected_artifact_digest"] is not None
    )
    bound_read["arguments"]["expected_artifact_digest"] = "0" * 64
    _rechain_trace(rebound)
    try:
        ReferenceMeter.replay(rebound)
    except reference_meter.InvalidMeterTrace:
        pass
    else:
        raise AssertionError("rebound artifact digest replayed successfully")


def test_schema_and_source_boundary() -> None:
    schema = json.loads((HERE / "record_schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["schema"]["const"] == archive_reducer.RECORD_SCHEMA
    assert set(schema["required"]) == archive_reducer._RECORD_FIELDS

    source_names = {
        "canonical.py",
        "hypothesis_library.py",
        "world_generator.py",
        "surface_codec.py",
        "archive_query.py",
        "archive_reducer.py",
        "record_schema.json",
        "generic_index.py",
        "reference_meter.py",
        "proposer.py",
        "self_test.py",
    }
    assert source_names == {path.name for path in HERE.iterdir() if path.is_file()}
    forbidden = ("TransitionCapability(", "mint_warrant", "mint_authority")
    for path in HERE.iterdir():
        if path.suffix != ".py" or path.name == "self_test.py":
            continue
        text = path.read_text(encoding="utf-8")
        assert not any(token in text for token in forbidden), path.name


def main() -> None:
    test_modules()
    test_scope_id_isolation()
    test_world_and_proposer()
    test_archive_rival()
    test_meter_limits_and_trace_integrity()
    test_external_call_payload_boundary()
    test_schema_and_source_boundary()
    print("E001 pre-subject apparatus self-test: PASS")
    print(f"hypotheses={len(HYPOTHESES)} modulus={MODULUS} development_worlds=32")


if __name__ == "__main__":
    main()
