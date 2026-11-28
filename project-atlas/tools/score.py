#!/usr/bin/env python3
"""Compute composite scores, gate status, alternative rankings and weight-sensitivity rank stability.

Reads 09_databases/opportunities.jsonl (run tools/merge.py first).
Writes 03_screening/scores.csv, 03_screening/rankings.md, 03_screening/rank_stability.csv,
       03_screening/calibration.md (original vs blind score agreement, per workstream bias).
"""
import csv, json, pathlib, random, statistics, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, SCR = ROOT / "09_databases", ROOT / "03_screening"
KEYS = ["fcf","roic","access","scale","resilience","entry","delegation","cash","feasibility","ai"]
WEIGHTS_V1 = {"fcf":.18,"roic":.15,"access":.12,"scale":.12,"resilience":.10,"entry":.10,
              "delegation":.08,"cash":.05,"feasibility":.05,"ai":.05}
SHRINK = {"A":1.0,"B":0.95,"C":0.85,"D":0.70,"E":0.55}
SHRINK_STRICT = {"A":1.0,"B":0.9,"C":0.75,"D":0.5,"E":0.3}

# Alternative ranking profiles (founder section 47). Each is a weight vector over the same criteria.
PROFILES = {
 "overall_v1": WEIGHTS_V1,
 "highest_confidence": WEIGHTS_V1,  # same weights, strict shrinkage
 "profit_potential": {"fcf":.5,"scale":.3,"resilience":.1,"entry":.1},
 "return_on_capital": {"roic":.5,"cash":.25,"fcf":.25},
 "capital_efficiency": {"roic":.4,"cash":.3,"feasibility":.15,"access":.15},
 "cash_conversion": {"cash":.6,"roic":.2,"fcf":.2},
 "fastest_validation": {"access":.4,"feasibility":.3,"roic":.15,"cash":.15},
 "owner_distributions": {"fcf":.35,"cash":.2,"resilience":.2,"delegation":.15,"roic":.1},
 "management_delegation": {"delegation":.5,"resilience":.15,"fcf":.2,"scale":.15},
 "ai_leverage": {"ai":.4,"fcf":.2,"roic":.2,"access":.2},
 "geographic_expansion": {"scale":.5,"delegation":.25,"fcf":.25},
 "adjacent_expansion": {"scale":.4,"entry":.2,"fcf":.2,"resilience":.2},
 "holding_company_foundation": {"fcf":.25,"cash":.15,"delegation":.2,"resilience":.2,"roic":.2},
}


def load():
    p = DB / "opportunities.jsonl"
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def composite(scores, weights):
    tw = sum(weights.values())
    return sum(weights.get(k, 0) * float(scores.get(k) or 0) for k in KEYS) / tw


def adjust(raw, level, table=SHRINK):
    k = table.get(level or "E", 0.55)
    return 5 + (raw - 5) * k


def gate_status(o):
    fails, warns = [], []
    for g in o.get("gates") or []:
        g = str(g)
        if "FAIL" in g.upper():
            fails.append(g.split(":")[0])
        elif "WARN" in g.upper():
            warns.append(g.split(":")[0])
    for f in o.get("blind_flags") or []:
        if "FAIL" in f.upper() and f.split(":")[0] not in fails:
            fails.append(f.split(":")[0] + "(blind)")
    return fails, warns


def main():
    opps = load()
    rows = []
    for o in opps:
        sc = o.get("current_scores") or o.get("original_scores") or {}
        if any(sc.get(k) is None for k in KEYS):
            continue
        lvl = o.get("current_evidence_confidence") or "E"
        fails, warns = gate_status(o)
        r = {"id": o["id"], "title": o.get("title"), "workstream": o.get("workstream"),
             "industry": o.get("industry"), "evidence": lvl, "max_stage": o.get("max_stage", "A"),
             "duplicate_of": o.get("duplicate_of") or "", "gate_fail": ";".join(fails),
             "gate_warn": ";".join(warns), "score_basis": o.get("current_score_basis"),
             "launch_cap_low": o.get("current_launch_capital_usd_low"),
             "launch_cap_high": o.get("current_launch_capital_usd_high"),
             "yr3_op_low": o.get("current_yr3_operating_profit_usd_low"),
             "yr3_op_high": o.get("current_yr3_operating_profit_usd_high"),
             "ceiling": o.get("current_plausible_milestone_ceiling"),
             "ttfr_months": o.get("time_to_first_revenue_months"),
             "verdict": (o.get("latest_verdict") or "")[:160]}
        for k in KEYS:
            r[k] = sc.get(k)
            r[f"orig_{k}"] = (o.get("original_scores") or {}).get(k)
            r[f"blind_{k}"] = (o.get("blind_scores") or {}).get(k) if o.get("blind_scores") else None
        r["raw_score"] = round(composite(sc, WEIGHTS_V1), 3)
        r["orig_raw_score"] = round(composite(o.get("original_scores") or sc, WEIGHTS_V1), 3)
        r["adj_score"] = round(adjust(r["raw_score"], lvl), 3)
        for name, w in PROFILES.items():
            raw = composite(sc, w)
            table = SHRINK_STRICT if name == "highest_confidence" else SHRINK
            val = adjust(raw, lvl, table)
            if name == "fastest_validation" and isinstance(r["ttfr_months"], (int, float)):
                val -= 0.08 * max(0, r["ttfr_months"] - 2)
            r[f"p_{name}"] = round(val, 3)
        rows.append(r)

    eligible = [r for r in rows if not r["gate_fail"] and not r["duplicate_of"]]
    for name in PROFILES:
        ranked = sorted(eligible, key=lambda r: -r[f"p_{name}"])
        for i, r in enumerate(ranked, 1):
            r[f"rank_{name}"] = i

    # weight sensitivity: Dirichlet perturbation around v1 weights (concentration 40)
    rnd = random.Random(42)
    N = 1000
    top10 = collections.Counter(); top25 = collections.Counter()
    alpha = {k: v * 40 for k, v in WEIGHTS_V1.items()}
    for _ in range(N):
        g = {k: rnd.gammavariate(a, 1) for k, a in alpha.items()}
        s = sum(g.values()); w = {k: v / s for k, v in g.items()}
        ranked = sorted(eligible, key=lambda r: -adjust(composite(r, w), r["evidence"]))
        for r in ranked[:10]:
            top10[r["id"]] += 1
        for r in ranked[:25]:
            top25[r["id"]] += 1
    for r in rows:
        r["p_top10_weight_sens"] = round(top10[r["id"]] / N, 3)
        r["p_top25_weight_sens"] = round(top25[r["id"]] / N, 3)

    rows.sort(key=lambda r: -r["adj_score"])
    SCR.mkdir(exist_ok=True)
    cols = list(rows[0].keys()) if rows else []
    cols = list(dict.fromkeys(cols + [c for r in rows for c in r.keys()]))
    with (SCR / "scores.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)

    md = ["# Rankings (auto-generated by tools/score.py — inputs to judgment, not the decision)\n",
          f"Eligible (no FAIL gate, not duplicate): {len(eligible)} of {len(rows)} scored records.\n"]
    for name in PROFILES:
        ranked = sorted(eligible, key=lambda r: -r[f"p_{name}"])[:25]
        md.append(f"\n## {name}\n\n| # | ID | Title | Ev | Score | Raw v1 |\n|---|---|---|---|---|---|")
        for i, r in enumerate(ranked, 1):
            md.append(f"| {i} | {r['id']} | {r['title']} | {r['evidence']} | {r[f'p_{name}']:.2f} | {r['raw_score']:.2f} |")
    stab = sorted(eligible, key=lambda r: -r["p_top25_weight_sens"])[:40]
    md.append("\n## Weight-sensitivity stability (1,000 Dirichlet perturbations of v1 weights)\n")
    md.append("| ID | Title | P(top 10) | P(top 25) |\n|---|---|---|---|")
    for r in stab:
        md.append(f"| {r['id']} | {r['title']} | {r['p_top10_weight_sens']:.2f} | {r['p_top25_weight_sens']:.2f} |")
    (SCR / "rankings.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # calibration: original vs blind
    cal = ["# Calibration: original (author) vs blind re-scores\n"]
    pairs = [o for o in opps if o.get("blind_scores")]
    if pairs:
        cal.append(f"Records with blind scores: {len(pairs)}\n")
        cal.append("| Criterion | mean orig | mean blind | mean |diff| | share |diff|>2 |\n|---|---|---|---|---|")
        for k in KEYS:
            d = [o["original_scores"][k] - o["blind_scores"][k] for o in pairs]
            cal.append(f"| {k} | {statistics.mean(o['original_scores'][k] for o in pairs):.2f} | "
                       f"{statistics.mean(o['blind_scores'][k] for o in pairs):.2f} | "
                       f"{statistics.mean(abs(x) for x in d):.2f} | {sum(abs(x) > 2 for x in d)/len(d):.0%} |")
        cal.append("\n## Author inflation by workstream (mean original raw − mean blind raw)\n")
        cal.append("| Workstream | n | orig raw | blind raw | inflation |\n|---|---|---|---|---|")
        byws = collections.defaultdict(list)
        for o in pairs:
            byws[o.get("workstream")].append(o)
        for ws, lst in sorted(byws.items()):
            a = statistics.mean(composite(o["original_scores"], WEIGHTS_V1) for o in lst)
            b = statistics.mean(composite(o["blind_scores"], WEIGHTS_V1) for o in lst)
            cal.append(f"| {ws} | {len(lst)} | {a:.2f} | {b:.2f} | {a-b:+.2f} |")
        big = [(o["id"], o.get("title"), composite(o["original_scores"], WEIGHTS_V1) - composite(o["blind_scores"], WEIGHTS_V1))
               for o in pairs]
        big.sort(key=lambda x: -abs(x[2]))
        cal.append("\n## Largest disagreements (raw composite)\n\n| ID | Title | orig − blind |\n|---|---|---|")
        for i, t, d in big[:30]:
            cal.append(f"| {i} | {t} | {d:+.2f} |")
    else:
        cal.append("No blind scores yet.")
    (SCR / "calibration.md").write_text("\n".join(cal) + "\n", encoding="utf-8")
    print(f"scored={len(rows)} eligible={len(eligible)} -> 03_screening/scores.csv, rankings.md, calibration.md")
    for r in rows[:15]:
        print(f"  {r['id']:8} {r['adj_score']:.2f} [{r['evidence']}] {r['title'][:70]} {('FAIL:'+r['gate_fail']) if r['gate_fail'] else ''}")


if __name__ == "__main__":
    main()
