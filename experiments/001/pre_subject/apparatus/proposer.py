"""Fixed canonical proposer for E001; proposal discovery is not an outcome."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Protocol

try:
    from .hypothesis_library import HYPOTHESES, AffineMap, field
except ImportError:  # Direct execution from the apparatus directory.
    from hypothesis_library import HYPOTHESES, AffineMap, field


PROPOSER_SCHEMA = "opencore.e001.canonical-proposer.v1"


class ReferenceOps(Protocol):
    """Only metered operations capable of influencing a Phase-5 candidate."""

    def apply_affine(self, transform: dict[str, Any], x: int) -> int: ...

    def compare(self, left: Any, right: Any) -> bool: ...


@dataclass(frozen=True, slots=True)
class ProposalResult:
    status: str
    candidate: AffineMap | None
    candidate_count: int
    observations: tuple[tuple[int, int], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": PROPOSER_SCHEMA,
            "status": self.status,
            "candidate": None if self.candidate is None else self.candidate.to_dict(),
            "candidate_count": self.candidate_count,
            "observations": [list(item) for item in self.observations],
        }


def _normalize(observations: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    normalized = tuple((field(x, "observation x"), field(y, "observation y")) for x, y in observations)
    return tuple(sorted(normalized))


def propose(
    observations: Iterable[tuple[int, int]], reference_ops: ReferenceOps
) -> ProposalResult:
    """Enumerate H in a-major/c-major order and return the unique candidate.

    Any non-unique or inconsistent set is deliberately `UNDERDETERMINED`; this
    function never mints an evaluator result, warrant, or authority artifact.
    The caller must supply the frozen reference-operation boundary so every
    result-affecting affine application and comparison is traceable.
    """

    normalized = _normalize(observations)
    candidates: list[AffineMap] = []
    for hypothesis in HYPOTHESES:
        consistent = True
        for x, expected in normalized:
            actual = reference_ops.apply_affine(hypothesis.to_dict(), x)
            if not reference_ops.compare(actual, expected):
                consistent = False
                break
        if consistent:
            candidates.append(hypothesis)
    if len(candidates) == 1:
        return ProposalResult("UNIQUE", candidates[0], 1, normalized)
    return ProposalResult("UNDERDETERMINED", None, len(candidates), normalized)


def _self_test() -> None:
    try:
        from .reference_meter import MeterLimits, ReferenceMeter
    except ImportError:
        from reference_meter import MeterLimits, ReferenceMeter

    target = AffineMap(7, 4)
    meter = ReferenceMeter(MeterLimits.unbounded())
    result = propose(((8, target.apply(8)), (2, target.apply(2))), meter)
    assert result.status == "UNIQUE" and result.candidate == target
    assert result.observations == tuple(sorted(result.observations))

    meter = ReferenceMeter(MeterLimits.unbounded())
    ambiguous = propose(((3, target.apply(3)),), meter)
    assert ambiguous.status == "UNDERDETERMINED"
    assert ambiguous.candidate is None and ambiguous.candidate_count == 10


if __name__ == "__main__":
    _self_test()

