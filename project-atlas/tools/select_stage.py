#!/usr/bin/env python3
"""Stage B and Stage C selection (run after merge.py + score.py).

Stage B: top N_B eligible records by evidence-adjusted score (no FAIL gate, not a duplicate).
Stage C: from Stage B, top-ranked with a per-workstream cap, plus all synthesized bundles, plus 'wildcards'
         (high raw score but weak evidence — upside worth testing).
Every record gets a recorded disposition and reason in 03_screening/screening_dispositions.csv.
"""
import csv, pathlib, collections, json, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCR = ROOT / "03_screening"
N_B, N_C_CORE, WS_CAP, N_WILD = 130, 52, 7, 6


def main():
    rows = list(csv.DictReader((SCR / "scores.csv").open(encoding="utf-8")))
    for r in rows:
        r["adj"] = float(r["adj_score"]); r["raw"] = float(r["raw_score"])
    elig = [r for r in rows if not r["gate_fail"] and not r["duplicate_of"]]
    elig.sort(key=lambda r: -r["adj"])
    stage_b = elig[:N_B]
    b_ids = {r["id"] for r in stage_b}
    # Stage C core with workstream cap
    per_ws = collections.Counter(); core = []
    for r in stage_b:
        if r["workstream"] == "SYN":
            continue
        if per_ws[r["workstream"]] >= WS_CAP:
            continue
        core.append(r); per_ws[r["workstream"]] += 1
        if len(core) >= N_C_CORE:
            break
    c_ids = {r["id"] for r in core}
    syn = [r for r in rows if r["workstream"] == "SYN"]
    # wildcards: highest raw score among eligible, not yet selected, evidence D/E
    wild = [r for r in sorted(elig, key=lambda r: -r["raw"]) if r["id"] not in c_ids
            and r["workstream"] != "SYN" and r["evidence"] in ("D", "E")][:N_WILD]
    jp_path = SCR / "judgment_picks.json"
    picks = json.loads(jp_path.read_text())["picks"] if jp_path.exists() else {}
    sel = {r["id"] for r in core + syn + wild}
    judg = [r for r in elig if r["id"] in picks and r["id"] not in sel]
    stage_c = core + syn + wild + judg
    c_ids = {r["id"] for r in stage_c}
    disp = []
    for r in sorted(rows, key=lambda r: -r["adj"]):
        if r["duplicate_of"]:
            d, why = "merged", f"duplicate of {r['duplicate_of']}"
        elif r["gate_fail"]:
            d, why = "rejected_gate", f"FAIL gate(s): {r['gate_fail']}"
        elif r["id"] in c_ids:
            kind = ("bundle" if r["workstream"] == "SYN" else "wildcard" if r in wild
                    else f"judgment pick: {picks[r['id']]}" if r in judg else "core")
            d, why = "stage_C", f"{kind}; adj {r['adj']:.2f}, raw {r['raw']:.2f}, evidence {r['evidence']}"
        elif r["id"] in b_ids:
            d, why = "stage_B_only", (f"adj {r['adj']:.2f} within top {N_B} but below Stage C cut"
                                      + (" or workstream cap reached" if per_ws[r['workstream']] >= WS_CAP else ""))
        else:
            d, why = "deprioritized", f"adj {r['adj']:.2f} below Stage B cut (rank > {N_B})"
        disp.append({"id": r["id"], "title": r["title"], "workstream": r["workstream"], "disposition": d,
                     "reason": why, "adj_score": r["adj_score"], "raw_score": r["raw_score"], "evidence": r["evidence"],
                     "gate_warn": r["gate_warn"], "author_verdict": r["verdict"]})
    with (SCR / "screening_dispositions.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(disp[0].keys())); w.writeheader(); w.writerows(disp)
    json.dump([r["id"] for r in stage_c], open(SCR / "stage_C_selected.json", "w"), indent=1)
    c = collections.Counter(x["disposition"] for x in disp)
    print("dispositions:", dict(c))
    print(f"Stage C: {len(core)} core + {len(syn)} bundles + {len(wild)} wildcards + {len(judg)} judgment = {len(stage_c)}")
    print("Stage C per workstream:", dict(collections.Counter(r["workstream"] for r in stage_c)))
    for r in stage_c:
        print(f"  {r['id']:9} {r['adj']:.2f} raw {r['raw']:.2f} [{r['evidence']}] {r['title'][:80]}")


if __name__ == "__main__":
    main()
