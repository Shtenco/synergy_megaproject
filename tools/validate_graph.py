#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def read_csv(rel):
    with (ROOT / rel).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

m = read_csv("data/megaproject_nodes.csv")
t = read_csv("data/technology_nodes.csv")
f = read_csv("data/frontier_nodes.csv")
a = read_csv("data/authors.csv")
i = read_csv("data/institutions.csv")
s = read_csv("data/sources.csv")
e = read_csv("data/frontier_edges.csv")

if len(m) != 150: errors.append(f"Expected 150 megaprojects, got {len(m)}")
if len(t) != 100: errors.append(f"Expected 100 technologies, got {len(t)}")
if len(f) != 100: errors.append(f"Expected 100 frontier nodes, got {len(f)}")

all_rows = m + t + f + a + i + s
ids = [r["id"] for r in all_rows]
if len(ids) != len(set(ids)):
    errors.append("Duplicate node IDs detected")

known = set(ids)
for edge in e:
    if edge["source"] not in known:
        errors.append(f"Missing edge source {edge['source']} for {edge['id']}")
    if edge["target"] not in known:
        errors.append(f"Missing edge target {edge['target']} for {edge['id']}")

by_f = {r["id"]: {"source":0,"tech":0,"mega":0} for r in f}
for edge in e:
    if edge["source"] in by_f:
        if edge["target"].startswith("S"): by_f[edge["source"]]["source"] += 1
        if edge["target"].startswith("T"): by_f[edge["source"]]["tech"] += 1
        if edge["target"].startswith("M"): by_f[edge["source"]]["mega"] += 1

for fid, c in by_f.items():
    for k,v in c.items():
        if v < 1: errors.append(f"{fid} has no {k} edge")

for src in s:
    if not src["url"].startswith(("http://","https://")):
        errors.append(f"Invalid source URL: {src['id']} {src['url']}")

with (ROOT / "graph/frontier_graph.json").open(encoding="utf-8") as fh:
    graph = json.load(fh)
if graph["counts"]["megaprojects"] != 150: errors.append("JSON count mismatch: megaprojects")
if graph["counts"]["technologies"] != 100: errors.append("JSON count mismatch: technologies")
if graph["counts"]["frontier"] != 100: errors.append("JSON count mismatch: frontier")

if errors:
    print("SINERGY GRAPH VALIDATION: FAILED")
    for err in errors: print(" -", err)
    sys.exit(1)

print("SINERGY GRAPH VALIDATION: GREEN")
print(f"Nodes={len(all_rows)} Edges={len(e)} M={len(m)} T={len(t)} F={len(f)} Sources={len(s)}")
