#!/usr/bin/env python3
"""Merge all discovery workstreams into canonical databases (idempotent).

Inputs
  02_discovery/WS*_opportunities.jsonl, WS*_sources.jsonl          (Stage A raw)
  03_screening/dedupe_decisions.json   {"WS05-003": {"duplicate_of": "WS15-007", "note": "..."}}
  03_screening/blind_scores/*.jsonl     {"id":..., "scores":{...}, "evidence_confidence":..., "rationale":...}
  03_screening/stage_updates/*.jsonl    {"id":..., "stage": "C|D|E|F", "scores":{...}, "evidence_confidence":...,
                                         "yr3_operating_profit_usd_low":..., ..., "verdict":..., "note":...}
Outputs
  09_databases/opportunities.jsonl + .csv   (one row per opportunity; original + blind + latest scores)
  09_databases/sources.jsonl + .csv
  03_screening/duplicate_candidates.csv     (title-similarity pairs across workstreams for manual review)
"""
import csv, json, pathlib, re, itertools, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
DISC, SCR, DB = ROOT / "02_discovery", ROOT / "03_screening", ROOT / "09_databases"
SCORE_KEYS = ["fcf","roic","access","scale","resilience","entry","delegation","cash","feasibility","ai"]
STOP = set("and or of the a an for to in on with by services service business company niche b2b commercial "
           "specialty specialized local regional illinois chicago brokerage distribution".split())


def jl(path):
    out = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def tokens(t):
    return {w for w in re.findall(r"[a-z0-9]+", (t or "").lower()) if w not in STOP and len(w) > 2}


def main():
    DB.mkdir(exist_ok=True); SCR.mkdir(exist_ok=True)
    opps, srcs = [], []
    for p in sorted(DISC.glob("WS*_opportunities.jsonl")):
        opps.extend(jl(p))
    for p in sorted(DISC.glob("WS*_sources.jsonl")):
        srcs.extend(jl(p))
    # de-duplicate exact id collisions (keep last written)
    by_id = collections.OrderedDict()
    for o in opps:
        by_id[o.get("id")] = o
    opps = list(by_id.values())

    dd_path = SCR / "dedupe_decisions.json"
    dedupe = json.loads(dd_path.read_text()) if dd_path.exists() else {}

    blind = collections.defaultdict(list)
    for p in sorted((SCR / "blind_scores").glob("*.jsonl")) if (SCR / "blind_scores").exists() else []:
        for r in jl(p):
            blind[r.get("id")].append(r)

    updates = collections.defaultdict(list)
    order = {"B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    for p in sorted((SCR / "stage_updates").glob("*.jsonl")) if (SCR / "stage_updates").exists() else []:
        for r in jl(p):
            updates[r.get("id")].append(r)

    for o in opps:
        oid = o.get("id")
        o["original_scores"] = {k: (o.get("scores") or {}).get(k) for k in SCORE_KEYS}
        o["original_evidence_confidence"] = o.get("evidence_confidence")
        d = dedupe.get(oid)
        o["duplicate_of"] = d.get("duplicate_of") if d else None
        o["dedupe_note"] = d.get("note") if d else None
        b = blind.get(oid, [])
        if b:
            o["blind_scores"] = {k: round(sum(x["scores"][k] for x in b) / len(b), 2) for k in SCORE_KEYS}
            o["blind_evidence_confidence"] = b[-1].get("evidence_confidence")
            o["blind_rationale"] = " | ".join(x.get("rationale", "") for x in b)
            o["blind_flags"] = sorted({f for x in b for f in x.get("flags", [])})
        else:
            o["blind_scores"] = None
        u = sorted(updates.get(oid, []), key=lambda r: order.get(r.get("stage"), 0))
        o["stage_history"] = u
        o["max_stage"] = u[-1]["stage"] if u else "A"
        latest = u[-1] if u else None
        if latest and latest.get("scores"):
            o["current_scores"] = {k: latest["scores"][k] for k in SCORE_KEYS}
            o["current_score_basis"] = f"stage {latest['stage']} revision"
        elif o["blind_scores"]:
            o["current_scores"] = {k: round((o["original_scores"][k] + o["blind_scores"][k]) / 2, 2)
                                   for k in SCORE_KEYS}
            o["current_score_basis"] = "mean(original, blind)"
        else:
            o["current_scores"] = dict(o["original_scores"])
            o["current_score_basis"] = "original"
        if latest and latest.get("evidence_confidence"):
            o["current_evidence_confidence"] = latest["evidence_confidence"]
        else:
            o["current_evidence_confidence"] = o.get("evidence_confidence")
        for k in ("yr3_operating_profit_usd_low", "yr3_operating_profit_usd_high", "launch_capital_usd_low",
                  "launch_capital_usd_high", "validation_cost_usd", "plausible_milestone_ceiling"):
            if latest and latest.get(k) is not None:
                o[f"current_{k}"] = latest[k]
            else:
                o[f"current_{k}"] = o.get(k)
        o["latest_verdict"] = (latest or {}).get("verdict") or o.get("preliminary_verdict")

    with (DB / "opportunities.jsonl").open("w", encoding="utf-8") as f:
        for o in opps:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    with (DB / "sources.jsonl").open("w", encoding="utf-8") as f:
        for s in srcs:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    def flat(v):
        if isinstance(v, (list, dict)):
            return json.dumps(v, ensure_ascii=False)
        return v
    if opps:
        cols = list(dict.fromkeys(k for o in opps for k in o.keys() if k != "stage_history"))
        with (DB / "opportunities.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for o in opps:
                w.writerow({k: flat(o.get(k)) for k in cols})
    if srcs:
        cols = list(dict.fromkeys(k for s in srcs for k in s.keys()))
        with (DB / "sources.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for s in srcs:
                w.writerow({k: flat(s.get(k)) for k in cols})

    # duplicate candidates across workstreams
    toks = [(o["id"], o.get("workstream"), o.get("title"), tokens(o.get("title", "") + " " + o.get("product_service", "")[:120]))
            for o in opps]
    pairs = []
    for a, b in itertools.combinations(toks, 2):
        if a[1] == b[1] or not a[3] or not b[3]:
            continue
        j = len(a[3] & b[3]) / len(a[3] | b[3])
        if j >= 0.30:
            pairs.append((round(j, 2), a[0], a[2], b[0], b[2]))
    pairs.sort(reverse=True)
    with (SCR / "duplicate_candidates.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["jaccard", "id_a", "title_a", "id_b", "title_b"])
        w.writerows(pairs)
    ws_counts = collections.Counter(o.get("workstream") for o in opps)
    print(f"merged opportunities={len(opps)} sources={len(srcs)} blind_scored={sum(1 for o in opps if o['blind_scores'])} "
          f"updated={sum(1 for o in opps if o['stage_history'])} dup_candidates={len(pairs)}")
    print("per workstream:", dict(sorted(ws_counts.items())))


if __name__ == "__main__":
    main()
