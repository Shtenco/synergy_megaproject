# M3 — Provenance & Edge Curation

Status: **IMPLEMENTED — first full semantic/provenance curation pass**

Review date: **2026-09-27**

M3 replaces the M2 placeholder relations `MAPS_TO_TECHNOLOGY` and `CONTRIBUTES_TO_MEGAPROJECT` with the canonical vocabulary:
- `ENABLES`
- `REQUIRES`
- `VALIDATES`
- `DEPENDS_ON`
- `PROPOSED_BY`
- `FUNDED_BY`
- `USES`
- `PRODUCES`
- `CONSUMES`
- `REDUCES_COST_OF`
- `INCREASES_CAPACITY_OF`
- `COMPETES_WITH`
- `FALSIFIES`
- `RISKS`
- `GOVERNS`

Every edge carries evidence_source, evidence_scope, confidence, review_status, semantic_class, strong_edge and review_date.

## Evidence honesty

- `RELATION_DIRECT`: source materially supports the specific relation.
- `PROVENANCE`: source validates the existence/content of the target frontier node.
- `ATTRIBUTION`: representative authorship/program association.
- `CANONICAL_SYNTHESIS`: explicit SINERGY systems synthesis grounded in sourced component nodes.
- `NODE_SUPPORT_ONLY`: source supports the frontier node but **does not yet prove the cross-layer relation**.

## Counts

- 350 idea nodes: 150 M + 100 T + 100 F
- 1105 curated edges
- 136 strong edges
- 7 direct-relation evidence edges
- 701 edges still requiring relation-specific evidence

The full human-readable registry of all ideas and all edges is in README.md.
