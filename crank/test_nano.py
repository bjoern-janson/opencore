from nano import (
    Decision, License, Nano, ObjectRecord, Precondition, Standing, StandingKey,
    Transition, WriteGrant,
)


def O(name: str) -> ObjectRecord:
    return ObjectRecord(name, f"digest:{name}", f"type:{name}")


def K(obj: ObjectRecord, dim: str) -> StandingKey:
    return StandingKey(obj.id, dim, "scope")


def test_effect_ceiling_and_nonmutation():
    o = O("o")
    a, b = K(o, "a"), K(o, "b")
    L = License("L", "WRITE", allowed_writes=(WriteGrant(a, ("1",)),))
    n = Nano(objects=(o,), standings=(Standing(a, "0"),), licenses=(L,))
    before = n.state_digest()
    r = n.apply_transition(Transition("WRITE", writes=(Standing(a, "1"), Standing(b, "X"))), "L")
    assert r.decision is Decision.DENY
    assert n.state_digest() == before
    assert len(n.journal) == 1


def test_unknown_and_revoked_license():
    o = O("o")
    a = K(o, "a")
    L = License("L", "WRITE", allowed_writes=(WriteGrant(a, ("1",)),))
    R = License("R", "REVOKE", allowed_revocations=("L",))
    n = Nano(objects=(o,), licenses=(L, R))
    assert n.apply_transition(Transition("WRITE", writes=(Standing(a, "1"),)), "missing").decision is Decision.DEFER
    assert n.apply_transition(Transition("REVOKE", revoke_licenses=("L",)), "R").decision is Decision.ALLOW
    assert n.apply_transition(Transition("WRITE", writes=(Standing(a, "1"),)), "L").decision is Decision.DENY


def test_operation_and_delete_ceiling():
    o = O("o")
    a = K(o, "a")
    L = License("L", "WRITE", allowed_writes=(WriteGrant(a, ("1",)),))
    n = Nano(objects=(o,), standings=(Standing(a, "0"),), licenses=(L,))
    assert n.apply_transition(Transition("OTHER", writes=(Standing(a, "1"),)), "L").decision is Decision.DENY
    assert n.apply_transition(Transition("WRITE", deletes=(a,)), "L").decision is Decision.DENY


def test_missing_precondition_and_preservation_defer():
    o = O("o")
    a, b = K(o, "a"), K(o, "b")
    L1 = License("L1", "A", preconditions=(Precondition(a, "yes"),))
    L2 = License("L2", "B", required_preservation=(b,))
    n = Nano(objects=(o,), licenses=(L1, L2))
    assert n.apply_transition(Transition("A"), "L1").decision is Decision.DEFER
    assert n.apply_transition(Transition("B"), "L2").decision is Decision.DEFER


def test_revoked_source_becomes_deferred_but_history_survives():
    o = O("o")
    a, b = K(o, "a"), K(o, "b")
    L0 = License("L0", "MAKE", allowed_writes=(WriteGrant(a, ("yes",)),))
    LR = License("LR", "REVOKE", allowed_revocations=("L0",))
    LU = License("LU", "USE", preconditions=(Precondition(a, "yes"),), allowed_writes=(WriteGrant(b, ("used",)),))
    n = Nano(objects=(o,), licenses=(L0, LR, LU))
    created = n.apply_transition(Transition("MAKE", writes=(Standing(a, "yes"),)), "L0")
    assert created.decision is Decision.ALLOW
    assert n.apply_transition(Transition("REVOKE", revoke_licenses=("L0",)), "LR").decision is Decision.ALLOW
    eff = n.effective_state()
    assert Standing(a, "yes") in eff.deferred
    assert n.apply_transition(Transition("USE", writes=(Standing(b, "used"),)), "LU").decision is Decision.DEFER
    assert any(r.id == created.id for r in n.lineage(o.id))



def test_transitive_warrant_revocation_propagates():
    root, parent, child, use = O("root"), O("parent"), O("child"), O("use")
    kr, kp, kc, ku = K(root,"gate"), K(parent,"standing"), K(child,"standing"), K(use,"standing")
    L0 = License("L0", "MAKE_PARENT", preconditions=(Precondition(kr,"yes"),), allowed_writes=(WriteGrant(kp,("ok",)),))
    L1 = License("L1", "MAKE_CHILD", preconditions=(Precondition(kp,"ok"),), allowed_writes=(WriteGrant(kc,("ok",)),))
    LR = License("LR", "REVOKE", allowed_revocations=("L0",))
    LU = License("LU", "USE", preconditions=(Precondition(kc,"ok"),), allowed_writes=(WriteGrant(ku,("used",)),))
    n = Nano(objects=(root,parent,child,use), standings=(Standing(kr,"yes"),), licenses=(L0,L1,LR,LU))
    assert n.apply_transition(Transition("MAKE_PARENT", writes=(Standing(kp,"ok"),)), "L0").decision is Decision.ALLOW
    child_r = n.apply_transition(Transition("MAKE_CHILD", writes=(Standing(kc,"ok"),)), "L1")
    assert child_r.decision is Decision.ALLOW and child_r.parent_receipts
    assert n.apply_transition(Transition("REVOKE", revoke_licenses=("L0",)), "LR").decision is Decision.ALLOW
    assert Standing(kc,"ok") in n.effective_state().deferred
    assert n.apply_transition(Transition("USE", writes=(Standing(ku,"used"),)), "LU").decision is Decision.DEFER


def test_preservation_ancestry_is_not_authority_dependency():
    marker, out = O("marker"), O("out")
    km, ko = K(marker,"marker"), K(out,"out")
    L0 = License("L0", "MAKE_MARKER", allowed_writes=(WriteGrant(km,("m",)),))
    L1 = License("L1", "MAKE_OUT", allowed_writes=(WriteGrant(ko,("o",)),), required_preservation=(km,))
    LR = License("LR", "REVOKE", allowed_revocations=("L0",))
    n = Nano(objects=(marker,out), licenses=(L0,L1,LR))
    assert n.apply_transition(Transition("MAKE_MARKER", writes=(Standing(km,"m"),)), "L0").decision is Decision.ALLOW
    out_r = n.apply_transition(Transition("MAKE_OUT", writes=(Standing(ko,"o"),)), "L1")
    assert out_r.decision is Decision.ALLOW
    assert out_r.parent_receipts == ()
    assert n.apply_transition(Transition("REVOKE", revoke_licenses=("L0",)), "LR").decision is Decision.ALLOW
    assert Standing(ko,"o") in n.effective_state().active

def main():
    tests = [name for name in globals() if name.startswith("test_")]
    for name in sorted(tests):
        globals()[name]()
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    main()
