"""The complete, public E001 affine hypothesis library over Z_11."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

try:
    from .canonical import require_uint
except ImportError:  # Direct execution from the apparatus directory.
    from canonical import require_uint


MODULUS = 11
HYPOTHESIS_SCHEMA = "opencore.e001.affine-map.v1"


def field(value: Any, name: str = "field element") -> int:
    return require_uint(value, name, MODULUS)


@dataclass(frozen=True, order=True, slots=True)
class AffineMap:
    """One map x -> a*x + c mod 11 with non-zero slope."""

    a: int
    c: int

    def __post_init__(self) -> None:
        if isinstance(self.a, bool) or not isinstance(self.a, int):
            raise ValueError("a must be an integer")
        if self.a < 1 or self.a >= MODULUS:
            raise ValueError("a must be in {1,...,10}")
        field(self.c, "c")

    def apply(self, x: int) -> int:
        return (self.a * field(x, "x") + self.c) % MODULUS

    def to_dict(self) -> dict[str, Any]:
        return {"schema": HYPOTHESIS_SCHEMA, "a": self.a, "c": self.c}

    @classmethod
    def from_dict(cls, value: Any) -> "AffineMap":
        if not isinstance(value, dict):
            raise ValueError("affine map must be an object")
        if set(value) != {"schema", "a", "c"}:
            raise ValueError("affine map fields do not match schema")
        if value["schema"] != HYPOTHESIS_SCHEMA:
            raise ValueError("unknown affine map schema")
        return cls(value["a"], value["c"])


IDENTITY = AffineMap(1, 0)
HYPOTHESES: tuple[AffineMap, ...] = tuple(
    AffineMap(a, c) for a in range(1, MODULUS) for c in range(MODULUS)
)


def compose(outer: AffineMap, inner: AffineMap) -> AffineMap:
    """Return outer(inner(x)); this fixes the E001 composition direction."""

    return AffineMap(
        (outer.a * inner.a) % MODULUS,
        (outer.a * inner.c + outer.c) % MODULUS,
    )


def disagreement_count(left: AffineMap, right: AffineMap) -> int:
    return sum(left.apply(x) != right.apply(x) for x in range(MODULUS))


def consistent_hypotheses(observations: Iterable[tuple[int, int]]) -> tuple[AffineMap, ...]:
    normalized = tuple((field(x, "x"), field(y, "y")) for x, y in observations)
    return tuple(
        hypothesis
        for hypothesis in HYPOTHESES
        if all(hypothesis.apply(x) == y for x, y in normalized)
    )


def library_descriptor() -> dict[str, Any]:
    return {
        "schema": "opencore.e001.hypothesis-library.v1",
        "modulus": MODULUS,
        "canonical_order": "a-major-then-c",
        "size": len(HYPOTHESES),
        "hypotheses": [hypothesis.to_dict() for hypothesis in HYPOTHESES],
    }


def _self_test() -> None:
    assert len(HYPOTHESES) == 110
    assert len(set(HYPOTHESES)) == 110
    for hypothesis in HYPOTHESES:
        observations = ((2, hypothesis.apply(2)), (7, hypothesis.apply(7)))
        assert consistent_hypotheses(observations) == (hypothesis,)
    for index, left in enumerate(HYPOTHESES):
        for right in HYPOTHESES[index + 1 :]:
            assert disagreement_count(left, right) >= 10
    assert compose(AffineMap(3, 4), AffineMap(2, 1)) == AffineMap(6, 7)


if __name__ == "__main__":
    _self_test()

