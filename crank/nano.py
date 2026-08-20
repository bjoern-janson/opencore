"""OpenCore Nano: transition typechecker + append-only journal.

Nano is intentionally semantically agnostic. Payloads are opaque. The trusted
surface sees only typed standings, exact contract preconditions, effect grants,
preservation obligations, and license revocation state.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from typing import Iterable


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    DEFER = "DEFER"


@dataclass(frozen=True, order=True)
class StandingKey:
    object_id: str
    dimension: str
    scope: str = "global"


@dataclass(frozen=True)
class ObjectRecord:
    id: str
    payload_digest: str
    type_tag: str


@dataclass(frozen=True)
class Standing:
    key: StandingKey
    value: str


@dataclass(frozen=True)
class Precondition:
    key: StandingKey
    expected: str


@dataclass(frozen=True)
class WriteGrant:
    key: StandingKey
    allowed_values: tuple[str, ...]


@dataclass(frozen=True)
class License:
    id: str
    operation: str
    preconditions: tuple[Precondition, ...] = ()
    allowed_writes: tuple[WriteGrant, ...] = ()
    allowed_deletes: tuple[StandingKey, ...] = ()
    required_preservation: tuple[StandingKey, ...] = ()
    allowed_revocations: tuple[str, ...] = ()


@dataclass(frozen=True)
class Transition:
    operation: str
    writes: tuple[Standing, ...] = ()
    deletes: tuple[StandingKey, ...] = ()
    revoke_licenses: tuple[str, ...] = ()


@dataclass(frozen=True)
class CheckResult:
    decision: Decision
    reasons: tuple[str, ...]
    state_digest: str
    transition_digest: str
    license_id: str


@dataclass(frozen=True)
class Receipt:
    id: str
    sequence: int
    decision: Decision
    reasons: tuple[str, ...]
    transition_digest: str
    before_state_digest: str
    after_state_digest: str
    license_id: str
    parent_receipts: tuple[str, ...]
    writes: tuple[Standing, ...]
    deletes: tuple[StandingKey, ...]
    revoked_licenses: tuple[str, ...]


@dataclass(frozen=True)
class EffectiveState:
    active: tuple[Standing, ...]
    deferred: tuple[Standing, ...]


@dataclass(frozen=True)
class _Current:
    standing: Standing
    receipt_id: str | None
    license_id: str | None


def _canon(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _digest(value: object) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _key_id(key: StandingKey) -> str:
    return f"{key.object_id}|{key.dimension}|{key.scope}"


class Nano:
    """Small persistence boundary for externally constituted transition contracts."""

    def __init__(
        self,
        *,
        objects: Iterable[ObjectRecord] = (),
        standings: Iterable[Standing] = (),
        licenses: Iterable[License] = (),
    ) -> None:
        self.objects = {obj.id: obj for obj in objects}
        self.licenses = {lic.id: lic for lic in licenses}
        self.revoked_licenses: set[str] = set()
        self._current = {
            standing.key: _Current(standing, receipt_id=None, license_id=None)
            for standing in standings
        }
        self._journal: list[Receipt] = []
        self._receipts_by_id: dict[str, Receipt] = {}

    # ---------- public trusted surface ----------

    def check_transition(self, transition: Transition, license_id: str) -> CheckResult:
        before = self.state_digest()
        tdigest = _digest(asdict(transition))
        deny: list[str] = []
        defer: list[str] = []

        license_ = self.licenses.get(license_id)
        if license_ is None:
            defer.append("license:not_present")
            return CheckResult(Decision.DEFER, tuple(defer), before, tdigest, license_id)
        if license_id in self.revoked_licenses:
            deny.append("license:revoked")
        if transition.operation != license_.operation:
            deny.append("operation:not_licensed")

        # Preconditions use only effective, kernel-visible standings.
        for pre in license_.preconditions:
            current = self._effective_current(pre.key)
            if current is None:
                defer.append(f"precondition:unestablished:{_key_id(pre.key)}")
            elif current.standing.value != pre.expected:
                deny.append(f"precondition:contradicted:{_key_id(pre.key)}")

        # Every requested write/delete/revocation must fit inside the effect grant.
        grants = {grant.key: set(grant.allowed_values) for grant in license_.allowed_writes}
        for write in transition.writes:
            allowed = grants.get(write.key)
            if allowed is None or write.value not in allowed:
                deny.append(f"effect:write_not_licensed:{_key_id(write.key)}")
        allowed_deletes = set(license_.allowed_deletes)
        for key in transition.deletes:
            if key not in allowed_deletes:
                deny.append(f"effect:delete_not_licensed:{_key_id(key)}")
        allowed_revocations = set(license_.allowed_revocations)
        for target in transition.revoke_licenses:
            if target not in allowed_revocations:
                deny.append(f"effect:revocation_not_licensed:{target}")

        # Required preservation is value-preservation over current raw standing.
        writes = {standing.key: standing.value for standing in transition.writes}
        deletes = set(transition.deletes)
        for key in license_.required_preservation:
            current = self._current.get(key)
            if current is None:
                defer.append(f"preservation:unestablished:{_key_id(key)}")
                continue
            if key in deletes or (key in writes and writes[key] != current.standing.value):
                deny.append(f"preservation:violated:{_key_id(key)}")

        # Contradiction/effect violation dominates missing information.
        if deny:
            decision = Decision.DENY
            reasons = tuple(sorted(set(deny + defer)))
        elif defer:
            decision = Decision.DEFER
            reasons = tuple(sorted(set(defer)))
        else:
            decision = Decision.ALLOW
            reasons = ()
        return CheckResult(decision, reasons, before, tdigest, license_id)

    def apply_transition(self, transition: Transition, license_id: str) -> Receipt:
        # Authorization is checked at execution time, not cached from an earlier state.
        check = self.check_transition(transition, license_id)
        before = check.state_digest
        parent_receipts = self._parents_for(transition, self.licenses.get(license_id))

        if check.decision is Decision.ALLOW:
            for key in transition.deletes:
                self._current.pop(key, None)
            receipt_id = self._next_receipt_id(check, before)
            for standing in transition.writes:
                self._current[standing.key] = _Current(
                    standing=standing,
                    receipt_id=receipt_id,
                    license_id=license_id,
                )
            self.revoked_licenses.update(transition.revoke_licenses)
        else:
            receipt_id = self._next_receipt_id(check, before)

        after = self.state_digest()
        receipt = Receipt(
            id=receipt_id,
            sequence=len(self._journal),
            decision=check.decision,
            reasons=check.reasons,
            transition_digest=check.transition_digest,
            before_state_digest=before,
            after_state_digest=after,
            license_id=license_id,
            parent_receipts=parent_receipts,
            writes=transition.writes,
            deletes=transition.deletes,
            revoked_licenses=transition.revoke_licenses,
        )
        self._journal.append(receipt)
        self._receipts_by_id[receipt.id] = receipt
        return receipt

    def effective_state(self) -> EffectiveState:
        active: list[Standing] = []
        deferred: list[Standing] = []
        for key in sorted(self._current):
            current = self._current[key]
            if current.receipt_id is not None and not self._receipt_effective(current.receipt_id):
                deferred.append(current.standing)
            else:
                active.append(current.standing)
        return EffectiveState(tuple(active), tuple(deferred))

    def lineage(self, object_id: str) -> tuple[Receipt, ...]:
        out: list[Receipt] = []
        for receipt in self._journal:
            if any(s.key.object_id == object_id for s in receipt.writes) or any(
                key.object_id == object_id for key in receipt.deletes
            ):
                out.append(receipt)
        return tuple(out)

    @property
    def journal(self) -> tuple[Receipt, ...]:
        return tuple(self._journal)

    def state_digest(self) -> str:
        current = [
            {
                "key": asdict(key),
                "value": cur.standing.value,
                "receipt_id": cur.receipt_id,
                "license_id": cur.license_id,
            }
            for key, cur in sorted(self._current.items())
        ]
        objects = [asdict(self.objects[key]) for key in sorted(self.objects)]
        return _digest(
            {
                "objects": objects,
                "current": current,
                "revoked_licenses": sorted(self.revoked_licenses),
            }
        )

    # ---------- internal mechanics ----------

    def _effective_current(self, key: StandingKey) -> _Current | None:
        current = self._current.get(key)
        if current is None:
            return None
        if current.receipt_id is not None and not self._receipt_effective(current.receipt_id):
            return None
        return current

    def _receipt_effective(self, receipt_id: str, seen: set[str] | None = None) -> bool:
        receipt = self._receipts_by_id.get(receipt_id)
        if receipt is None or receipt.decision is not Decision.ALLOW:
            return False
        if receipt.license_id in self.revoked_licenses:
            return False
        seen = set() if seen is None else set(seen)
        if receipt_id in seen:
            return False
        seen.add(receipt_id)
        return all(self._receipt_effective(parent, seen) for parent in receipt.parent_receipts)

    def _parents_for(self, transition: Transition, license_: License | None) -> tuple[str, ...]:
        # Only warrant-bearing inputs become authority dependencies. Historical
        # ancestry remains recoverable from the append-only object lineage.
        keys: set[StandingKey] = set()
        if license_ is not None:
            keys.update(pre.key for pre in license_.preconditions)
        parents = {
            self._current[key].receipt_id
            for key in keys
            if key in self._current and self._current[key].receipt_id is not None
        }
        return tuple(sorted(parents))

    def _next_receipt_id(self, check: CheckResult, before: str) -> str:
        return _digest(
            {
                "sequence": len(self._journal),
                "decision": check.decision.value,
                "transition_digest": check.transition_digest,
                "before": before,
                "license_id": check.license_id,
            }
        )[:24]
