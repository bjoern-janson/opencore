#!/usr/bin/env python3
"""AF3-OC-001 minimal reproducer: real AF3 payload identities, frozen Nano membrane."""
from __future__ import annotations

import hashlib, json
from pathlib import Path
import numpy as np
from nano import License, Nano, ObjectRecord, Precondition, Standing, StandingKey, Transition, WriteGrant

NANO_SHA256 = "8d820d8f8d9021c5b969659a845aefd2a16e39c24834f0a78e4b491c294b0329"
AF3_INTERFACE_COMMIT = "c0f97eda2f1f482fd94d3a38bece18c7069b4a5c"
CANDIDATES = [
    {
        "id": "af3-public-1phv-chain-a",
        "structure_git_blob_sha1": "0bea758ce798e3450571f45c8adf55910aae2900",
        "producer": "AlphaFold-beta-20231127 (3.0.0 @ 2025-04-14 15:50:05)",
        "confidence": {"global_plddt": 95.99},
    },
    {
        "id": "af3-public-pep-seed1-sample0",
        "structure_git_blob_sha1": "6493f320e156cc708afac5d7308e86700f44c375",
        "producer": "AlphaFold-beta-20231127 (3.0.0 @ 2025-12-17 14:52:00)",
        "confidence": {"global_plddt": 65.0, "ptm": 0.58, "ranking_score": 0.58},
    },
    {
        "id": "af3-public-prot-pep-top",
        "structure_git_blob_sha1": "b891bcb4d4ce630a1861b664ea710f715ba9bb19",
        "producer": "public AF3 output",
        "confidence": {"ptm": 0.25, "iptm": 0.45, "ranking_score": 0.45},
    },
]
AF3_CA = np.array([[16.925,4.729,5.802],[15.891,7.999,7.440],[13.173,10.025,5.712],[12.348,13.668,6.442],[8.879,15.107,5.850],[9.639,18.177,3.743],[8.202,16.081,0.903],[5.599,13.311,0.929]])
EXP_CA = np.array([[12.941,39.418,6.575],[14.536,38.012,9.717],[12.501,35.280,11.384],[13.268,34.250,14.936],[12.126,30.699,15.836],[10.041,31.041,19.031],[6.954,30.431,16.942],[6.524,28.182,13.907]])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rmsd_kabsch(p: np.ndarray, q: np.ndarray) -> float:
    pc, qc = p-p.mean(0), q-q.mean(0)
    v, _, wt = np.linalg.svd(pc.T @ qc)
    r = v @ np.diag([1.0, 1.0, np.sign(np.linalg.det(v @ wt))]) @ wt
    return float(np.sqrt(np.mean(np.sum((pc @ r - qc)**2, axis=1))))


def smoke(candidate: dict) -> dict:
    role = StandingKey(candidate["id"], "epistemic-role", "declared")
    conf = StandingKey(candidate["id"], "model-confidence", "prediction")
    cval = "AF3_CONFIDENCE:" + hashlib.sha256(json.dumps(candidate["confidence"], sort_keys=True).encode()).hexdigest()
    lic = License("store", "store", allowed_writes=(WriteGrant(role,("PREDICTION",)), WriteGrant(conf,(cval,))))
    obj = ObjectRecord(candidate["id"], candidate["structure_git_blob_sha1"], "AF3_PREDICTION_OPAQUE")
    n = Nano(objects=(obj,), licenses=(lic,))
    t1 = n.apply_transition(Transition("store", writes=(Standing(role,"PREDICTION"),Standing(conf,cval))), "store")
    t2 = n.apply_transition(Transition("store", writes=(Standing(role,"VALIDATED_FOR_SCOPE"),)), "store")
    return {"prediction_id":candidate["id"],"confidence":candidate["confidence"],"T1":t1.decision.value,"T2_confidence_only":t2.decision.value,"T2_reasons":list(t2.reasons)}


def primary() -> dict:
    g="af3-public-1phv-chain-a"; gp=g+":successor"
    G=StandingKey(g,"epistemic-role","A:1-8_CA"); C=StandingKey(g,"model-confidence","prediction")
    E=StandingKey(g+":external","evidence-role","A:1-8_CA"); R=StandingKey(g+":refute","evidence-role","A:1-8_CA")
    H=StandingKey(g+":H","standing","A:1-8_CA"); U=StandingKey(g+":U","standing","independent")
    GP=StandingKey(gp,"epistemic-role","A:1-8_CA"); EP=StandingKey(gp+":external","evidence-role","A:1-8_CA")
    cv="AF3_CONFIDENCE:95.99"; measured=rmsd_kabsch(AF3_CA,EXP_CA); ev=f"EXTERNAL_KABSCH_RMSD:{measured:.6f}A"
    licenses=(
      License("store","store",allowed_writes=(WriteGrant(G,("PREDICTION",)),WriteGrant(C,(cv,)))),
      License("admitE","admitE",allowed_writes=(WriteGrant(E,(ev,)),)),
      License("validate","validate",preconditions=(Precondition(E,ev),),allowed_writes=(WriteGrant(G,("VALIDATED_FOR_SCOPE",)),)),
      License("deriveH","deriveH",preconditions=(Precondition(G,"VALIDATED_FOR_SCOPE"),),allowed_writes=(WriteGrant(H,("DERIVED_FROM_G",)),)),
      License("storeU","storeU",allowed_writes=(WriteGrant(U,("INDEPENDENT",)),)),
      License("admitR","admitR",allowed_writes=(WriteGrant(R,("CONTROLLED_REFUTES_G",)),)),
      License("reopen","reopen",preconditions=(Precondition(R,"CONTROLLED_REFUTES_G"),),allowed_writes=(WriteGrant(G,("REOPENED",)),),allowed_revocations=("validate",)),
      License("succ","succ",preconditions=(Precondition(EP,"EXTERNAL_SUPPORTS_GPRIME"),),allowed_writes=(WriteGrant(GP,("VALIDATED_FOR_SCOPE",)),)),
      License("admitEP","admitEP",allowed_writes=(WriteGrant(EP,("EXTERNAL_SUPPORTS_GPRIME",)),)),
    )
    n=Nano(objects=(ObjectRecord(g,CANDIDATES[0]["structure_git_blob_sha1"],"AF3_PREDICTION_OPAQUE"),ObjectRecord(gp,"successor-placeholder","AF3_PREDICTION_OPAQUE")),licenses=licenses)
    rows=[]
    def go(label,t,l,expect):
        rec=n.apply_transition(t,l); rows.append({"label":label,"decision":rec.decision.value,"expected":expect,"reasons":list(rec.reasons),"receipt":rec.id,"parents":list(rec.parent_receipts)}); return rec
    go("T1",Transition("store",writes=(Standing(G,"PREDICTION"),Standing(C,cv))),"store","ALLOW")
    go("T2",Transition("store",writes=(Standing(G,"VALIDATED_FOR_SCOPE"),)),"store","DENY")
    e=go("E1",Transition("admitE",writes=(Standing(E,ev),)),"admitE","ALLOW")
    gval=go("T3",Transition("validate",writes=(Standing(G,"VALIDATED_FOR_SCOPE"),)),"validate","ALLOW")
    h=go("H",Transition("deriveH",writes=(Standing(H,"DERIVED_FROM_G"),)),"deriveH","ALLOW")
    go("U",Transition("storeU",writes=(Standing(U,"INDEPENDENT"),)),"storeU","ALLOW")
    go("E2",Transition("admitR",writes=(Standing(R,"CONTROLLED_REFUTES_G"),)),"admitR","ALLOW")
    go("T4",Transition("reopen",writes=(Standing(G,"REOPENED"),),revoke_licenses=("validate",)),"reopen","ALLOW")
    def kid(s): return f"{s.key.object_id}|{s.key.dimension}|{s.key.scope}"
    after={kid(s):{"value":s.value,"status":"ACTIVE"} for s in n.effective_state().active}
    after.update({kid(s):{"value":s.value,"status":"DEFERRED"} for s in n.effective_state().deferred})
    go("T5a",Transition("reopen",writes=(Standing(GP,"VALIDATED_FOR_SCOPE"),)),"reopen","DENY")
    go("T5b",Transition("succ",writes=(Standing(GP,"VALIDATED_FOR_SCOPE"),)),"succ","DEFER")
    go("E3",Transition("admitEP",writes=(Standing(EP,"EXTERNAL_SUPPORTS_GPRIME"),)),"admitEP","ALLOW")
    go("T5c",Transition("succ",writes=(Standing(GP,"VALIDATED_FOR_SCOPE"),)),"succ","ALLOW")
    return {
      "measurement":{"scope":"PDB 1HPV chain A residues 1-8 C-alpha","kabsch_rmsd_angstrom":measured,"experimental_method":"X-RAY DIFFRACTION","resolution_angstrom":1.90,"pdb_id":"1HPV"},
      "transitions":rows,
      "prospective_matrix_match":all(r["decision"]==r["expected"] for r in rows),
      "ancestry":{"T3_parent_is_external_measurement":e.id in gval.parent_receipts,"H_parent_is_validated_G":gval.id in h.parent_receipts},
      "after_reopen":after,
      "dependency_withdrawal_match":after[f"{g}|epistemic-role|A:1-8_CA"]["value"]=="REOPENED" and after[f"{g}|epistemic-role|A:1-8_CA"]["status"]=="ACTIVE" and after[f"{g}:H|standing|A:1-8_CA"]["status"]=="DEFERRED" and after[f"{g}:U|standing|independent"]["status"]=="ACTIVE",
    }


def main():
    here=Path(__file__).resolve().parent
    got=sha256(here/"nano.py")
    if got != NANO_SHA256: raise RuntimeError(f"frozen Nano hash mismatch: {got}")
    out={"object":"AF3_OC_001","status":"EXECUTED_FROZEN_MEMBRANE_ASSAY_WITH_REAL_AF3_PAYLOADS","frozen":{"nano_sha256":got,"af3_interface_commit":AF3_INTERFACE_COMMIT,"fresh_af3_inference":False},"smoke":[smoke(c) for c in CANDIDATES],"primary":primary()}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
