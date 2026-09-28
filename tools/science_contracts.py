from __future__ import annotations

from typing import Any


UPSTREAM_CONTRACT_ID = "synergy.science.evidence-package/v1"

DIRECT_EVIDENCE = {"SOURCE", "MEASURED", "DERIVED"}
NON_DIRECT = {"SIMULATION", "HYPOTHESIS", "UNRESOLVED"}


def science_package_to_review_queue(payload: dict[str, Any]) -> dict[str, Any]:
    sources = payload.get("sources")
    claims = payload.get("claims")
    if not isinstance(sources, list) or not isinstance(claims, list):
        raise ValueError("science package requires sources and claims arrays")

    source_ids = set()
    source_records = []
    for src in sources:
        sid = str(src.get("source_id", ""))
        digest = str(src.get("sha256", "")).lower()
        if not sid or sid in source_ids:
            raise ValueError("source ids must be unique")
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError(f"invalid source hash: {sid}")
        source_ids.add(sid)
        source_records.append({
            "external_source_id": sid,
            "locator": str(src.get("locator", "")),
            "sha256": digest,
            "review_status": "PENDING_SOURCE_IMPORT",
        })

    review_items = []
    seen_claims = set()
    for claim in claims:
        cid = str(claim.get("claim_id", ""))
        epistemic = str(claim.get("epistemic_status", "")).upper()
        refs = [str(x) for x in claim.get("source_ids", [])]
        if not cid or cid in seen_claims:
            raise ValueError("claim ids must be unique")
        if any(x not in source_ids for x in refs):
            raise ValueError(f"claim {cid} references unknown source")
        seen_claims.add(cid)

        if epistemic in DIRECT_EVIDENCE:
            proposed_relation = "VALIDATES"
            auto_edge = False
            review_status = "CURATION_REQUIRED"
        elif epistemic == "FALSIFIED":
            proposed_relation = "FALSIFIES"
            auto_edge = False
            review_status = "CURATION_REQUIRED"
        elif epistemic in NON_DIRECT:
            proposed_relation = None
            auto_edge = False
            review_status = "NON_DIRECT_EVIDENCE"
        else:
            raise ValueError(f"unknown epistemic status: {epistemic}")

        review_items.append({
            "claim_id": cid,
            "text": str(claim.get("text", "")),
            "epistemic_status": epistemic,
            "source_ids": refs,
            "proposed_relation_type": proposed_relation,
            "auto_create_graph_edge": auto_edge,
            "review_status": review_status,
        })

    return {
        "research_question": str(payload.get("research_question", "")),
        "package_status": str(payload.get("status", "")),
        "source_records": source_records,
        "claim_review_queue": review_items,
        "canonical_graph_mutation": False,
    }
