import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools" / "science_contracts.py"
spec = importlib.util.spec_from_file_location("science_contracts", PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def test_megaproject_stages_science_evidence_without_auto_mutation():
    q = mod.science_package_to_review_queue({
        "research_question": "Q",
        "status": "CANDIDATE",
        "sources": [{"source_id":"S1","locator":"paper","sha256":"1"*64}],
        "claims": [
            {"claim_id":"C1","text":"measured","epistemic_status":"MEASURED","source_ids":["S1"]},
            {"claim_id":"C2","text":"hypothesis","epistemic_status":"HYPOTHESIS","source_ids":[]},
            {"claim_id":"C3","text":"counterevidence","epistemic_status":"FALSIFIED","source_ids":["S1"]},
        ],
    })
    assert q["canonical_graph_mutation"] is False
    assert q["claim_review_queue"][0]["proposed_relation_type"] == "VALIDATES"
    assert q["claim_review_queue"][1]["proposed_relation_type"] is None
    assert q["claim_review_queue"][2]["proposed_relation_type"] == "FALSIFIES"
    assert all(not x["auto_create_graph_edge"] for x in q["claim_review_queue"])
