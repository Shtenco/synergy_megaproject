# M2 — Machine-Readable SINERGY Civilization Graph

Status: **implemented initial canonical build**

## Stable ID namespaces

- `M001..M150` — megaproject / historical-civilizational layer
- `T001..T100` — technology layer
- `F001..F100` — sourced frontier concepts
- `P...` — representative persons / named author groups
- `I...` — institutions / programs
- `S...` — sources
- `E...` — graph edges
- `EV...` — evidence records

## Canonical files

- `data/megaproject_nodes.csv`
- `data/technology_nodes.csv`
- `data/frontier_nodes.csv`
- `data/frontier_edges.csv`
- `data/authors.csv`
- `data/institutions.csv`
- `data/sources.csv`
- `data/evidence.csv`
- `graph/frontier_graph.json`
- `graph/frontier_graph.graphml`
- `graph/neo4j_import/nodes.csv`
- `graph/neo4j_import/relationships.csv`
- `schema/graph_schema.json`
- `tools/validate_graph.py`

## Important limitation

The M/T cross-layer edges are a **first deterministic semantic mapping** generated from the canonical README terminology. They are not claimed to be final expert-curated causal relationships. They are explicitly labeled as rule-based mappings in `frontier_edges.csv` and are intended to be reviewed and upgraded in M3.

Source provenance remains directly traceable to the F001–F100 canonical table.

## Validation invariant

Run:

```bash
python tools/validate_graph.py
```

A GREEN result requires:

- exactly 150 M-nodes;
- exactly 100 T-nodes;
- exactly 100 F-nodes;
- globally unique node IDs;
- all edge endpoints to exist;
- valid source URLs;
- every F-node to have at least one source edge;
- every F-node to have at least one technology mapping;
- every F-node to have at least one megaproject mapping.

## Next milestone

**M3 — Provenance & Edge Curation**

Replace rule-based cross-layer mappings with reviewed edges carrying:

- relation semantics;
- evidence source;
- confidence;
- causal vs enabling vs thematic distinction;
- reviewer;
- review date;
- falsification / invalidation condition.
