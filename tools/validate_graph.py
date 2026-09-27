#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOWED=["ENABLES","REQUIRES","VALIDATES","DEPENDS_ON","PROPOSED_BY","FUNDED_BY","USES","PRODUCES","CONSUMES","REDUCES_COST_OF","INCREASES_CAPACITY_OF","COMPETES_WITH","FALSIFIES","RISKS","GOVERNS"]
errors=[]
def read(rel):
    with (ROOT/rel).open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))
m=read("data/megaproject_nodes.csv"); t=read("data/technology_nodes.csv"); f=read("data/frontier_nodes.csv")
a=read("data/authors.csv"); i=read("data/institutions.csv"); s=read("data/sources.csv"); e=read("data/frontier_edges.csv")
if len(m)!=150: errors.append(f"M={len(m)} expected 150")
if len(t)!=100: errors.append(f"T={len(t)} expected 100")
if len(f)!=100: errors.append(f"F={len(f)} expected 100")
ids=[r["id"] for r in m+t+f+a+i+s]; known=set(ids)
if len(ids)!=len(known): errors.append("duplicate node IDs")
for x in e:
    if x["source"] not in known: errors.append(f"{x['id']} missing source {x['source']}")
    if x["target"] not in known: errors.append(f"{x['id']} missing target {x['target']}")
    if x["relation_type"] not in ALLOWED: errors.append(f"{x['id']} forbidden relation {x['relation_type']}")
    for k in ("evidence_source","evidence_scope","confidence","review_status","semantic_class","review_date"):
        if not x.get(k): errors.append(f"{x['id']} missing {k}")
    try:
        c=float(x["confidence"])
        if not 0<=c<=1: errors.append(f"{x['id']} confidence out of range")
    except: errors.append(f"{x['id']} invalid confidence")
for fr in f:
    fid=fr["id"]
    if not any(x["target"]==fid and x["source"].startswith("S") and x["relation_type"]=="VALIDATES" for x in e):
        errors.append(f"{fid} has no source VALIDATES edge")
    if not any(x["source"]==fid and x["target"].startswith("T") for x in e): errors.append(f"{fid} has no T edge")
    if not any(x["source"]==fid and x["target"].startswith("M") for x in e): errors.append(f"{fid} has no M edge")
with (ROOT/"graph/frontier_graph.json").open(encoding="utf-8") as fh: g=json.load(fh)
if g.get("schema_version")!="3.0": errors.append("graph schema != 3.0")
if g["counts"]["edges"]!=len(e): errors.append("edge count mismatch")
if errors:
    print("SINERGY GRAPH M3 VALIDATION: FAILED")
    for z in errors: print(" -",z)
    sys.exit(1)
print("SINERGY GRAPH M3 VALIDATION: GREEN")
print(f"M={len(m)} T={len(t)} F={len(f)} Edges={len(e)}")
