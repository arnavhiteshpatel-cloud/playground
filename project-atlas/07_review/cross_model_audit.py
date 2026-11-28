#!/usr/bin/env python3
"""Project Atlas - Stage F6 cross-finalist model consistency audit (reviewer script; READ-ONLY on model files).

Re-runs every finalist's BASE scenario through tools/fin_engine.py twice:
  (1) original drivers, (2) a harmonized "skeptic" driver set (rules H1-H8 below),
plus single-rule attributions, and writes results to an output directory (default: this script's folder).
Nothing under 08_financial_models/ is modified: overrides are passed to fin_engine.run() only.

Usage:  python3 cross_model_audit.py [PROJECT_ROOT] [OUT_DIR]   (defaults: /home/user/playground/project-atlas, /tmp/claude-0/atlas_scratch/F6)
Outputs: cross_model_audit_results.json, cross_model_audit_table.md, cross_model_audit_sensitivity.md/.json
"""
import json, os, sys, copy

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/playground/project-atlas"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-0/atlas_scratch/F6"
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import fin_engine as E  # noqa: E402

IDS = ["SYN-006", "SYN-004", "SYN-001", "WS05-007", "WS04-014", "WS18-003", "WS18-035",
       "WS13-014", "WS16-006", "WS12-012", "WS12-014"]
JOB_MODELS = {"WS18-003", "WS18-035"}          # churn = 100%, each "customer" = one job

# ---------------- Harmonization rules (skeptic set) ----------------
H = dict(
    # H1 founder qualified conversations at plateau (recurring B2B models): cap.
    #    Anchor: Bridge Group 2025 median SDR quota = 10 meetings held / month for a FULL-TIME SDR
    #    [D, F6-S004]; the founder also delivers the service. Cap = 1.5x that = 15 (generous: walk-ins/events).
    founder_conv_cap=15,
    # H2 combined conversation->customer conversion (lead_to_proposal x proposal_to_win) cap for an
    #    unknown newcomer in a displacement sale. 7 of 9 recurring models sit at 0.0875-0.105 and four use exactly
    #    the engine TEMPLATE DEFAULTS (0.40 x 0.25 = 0.10), i.e. unevidenced (E). Skeptic cap 0.08 (E, reviewer judgement).
    conv_cap=0.08,
    # H3 founder ramp >= 6 months (every recurring model but one already uses 6).
    ramp_floor=6,
    # H4 churn floor for recurring models = incumbent retention ~82-84%/yr ~= 1.5%/month
    #    (Paychex 82-83% [A, WS02-S022]; Rentokil NA 80.7% [B, C2-S009]; independent agencies 84% [C, E-SYN001-S012]).
    #    A newcomer should not out-retain incumbents.
    churn_floor=0.015,
    # H5 referral/inbound new customers per 100 active <= 1.0/month for recurring B2B (E everywhere).
    referral_cap=1.0,
    # H6 a hired rep cannot out-produce the harmonized founder funnel (same funnel, no founder credibility):
    #    rep_new_customers_per_month <= harmonized founder new customers / month.
    # H7 job models: plateau jobs/month = franchise all-unit MEDIAN volume, not averages or top cohorts
    #    (an unbranded independent without a call centre should not beat the median franchise unit).
    #    WS18-035: median of {Access all-unit median $389,856 / $575 model ticket; ProLift middle-50% avg
    #    $424,136 / $575; Precision smallest-band median $857,807 / $1,213 per job} = 58.9 jobs/month
    #    [B, DF-S001, DF-S002, C8-S019]. (Disagreeing figure kept: Precision CY2024 smallest band median
    #    $1,409,512 / $706 = 166 jobs/month [B, C8-S020].)
    #    WS18-003: Junk King median $436k / $389 median job = 93.4 jobs/month [B, WS18-S001];
    #    zone-2 expansion output scaled by the same ratio.
    job_targets={"WS18-035": 58.9, "WS18-003": 436000 / 389 / 12},
    # H8 long-term (years 6-10) and valuation drivers, all models:
    lt_growth_cap=0.05,        # incumbents' organic growth: Rollins commercial 7.6% [A]; staffing +2.4% [C]; promo +1.3-4.2% [C]
    lt_decay_cap=0.85,
    inc_roic_cap=0.60,         # pre-tax incremental return on growth reinvestment
    maint_capex_floor=0.03,
    ev_cap=3.0,                # ops profit here is SDE-basis (before owner pay); BizBuySell sold service median 2.38x SDE [D, E-WS05007-S007]
    ev_sdemedian=2.38,         # sensitivity only
    # H9 price/expansion growth on revenue per customer <= 3%/yr (inflation pass-through) where the excess
    #    is E-evidenced (SYN-001 9% "attach maturation", WS12-012 8% "seat expansion"); all other models use <=3%.
    arpc_growth_cap=0.03,
)

# Founder-delivery charge (FDC): a METRIC, not a driver. Operating profit in every model is before owner pay
# AND includes the founder personally doing a delivery role that the model's own staff notes price.
# FDC = 12 x loaded monthly cost of that role (base) x 1.03^(year-1), charged in a year unless the model has
# a manager on payroll who takes over that role. Role and monthly cost are read from each model's staff notes.
FOUNDER_ROLE = {
    "SYN-006": ("construction bookkeeper (founder covers first ~12 clients)", 5800, None),
    "SYN-004": ("energy analyst (founder analyses until 35 accounts)", 6000, None),
    "SYN-001": ("compliance coordinator (founder covers first 35 clients)", 5350, None),
    "WS05-007": ("pest technician (founder services first 110 accounts)", 5700, None),
    "WS04-014": ("field technician (founder covers first ~14 practices; L3 to 70 not charged)", 6500, None),
    "WS18-003": ("founder on truck/dispatch until operations manager is hired", 6500, "Operations manager"),
    "WS18-035": ("field technician pay ex-van (founder runs the first van)", 6800, "Operations / install manager"),
    "WS13-014": ("GPR technician salary load ex-kit/mileage (founder scans first ~20 accounts)", 6800, None),
    "WS16-006": ("account coordinator (founder does order entry up to $35k/mo sales)", 4800, None),
    "WS12-012": ("US account manager (founder manages accounts up to $70k/mo revenue)", 6000, None),
    "WS12-014": ("full-desk recruiter (founder is producer #1)", 6900, None),
}


def base_drivers(a):
    return E.run(a, "base")["drivers"]


def harmonized_overrides(i, a, rules=("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9")):
    d = base_drivers(a)
    ov = {}
    if i in JOB_MODELS:
        if "H7" in rules:
            J = H["job_targets"][i]
            conv = d["lead_to_proposal_pct"] * d["proposal_to_win_pct"]
            leads = J * (1 - d["referral_new_per_100_active"] / 100) / conv
            ratio = leads / d["founder_leads_per_month"]
            ov["founder_leads_per_month"] = leads
            if d["rep_new_customers_per_month"]:
                ov["rep_new_customers_per_month"] = d["rep_new_customers_per_month"] * ratio
    else:
        leads = d["founder_leads_per_month"]
        l2p, p2w = d["lead_to_proposal_pct"], d["proposal_to_win_pct"]
        if "H1" in rules:
            leads = min(leads, H["founder_conv_cap"])
            ov["founder_leads_per_month"] = leads
        if "H2" in rules and l2p * p2w > H["conv_cap"]:
            p2w = H["conv_cap"] / l2p
            ov["proposal_to_win_pct"] = p2w
        if "H3" in rules:
            ov["founder_ramp_months"] = max(d["founder_ramp_months"], H["ramp_floor"])
        if "H4" in rules:
            ov["monthly_churn_pct"] = max(d["monthly_churn_pct"], H["churn_floor"])
        if "H5" in rules:
            ov["referral_new_per_100_active"] = min(d["referral_new_per_100_active"], H["referral_cap"])
        if "H6" in rules:
            ov["rep_new_customers_per_month"] = min(d["rep_new_customers_per_month"], leads * l2p * p2w)
    if "H9" in rules:
        ov["arpc_annual_growth_pct"] = min(d["arpc_annual_growth_pct"], H["arpc_growth_cap"])
    if "H8" in rules:
        ov["lt_growth_y6_pct"] = min(d["lt_growth_y6_pct"], H["lt_growth_cap"])
        ov["lt_growth_decay"] = min(d["lt_growth_decay"], H["lt_decay_cap"])
        ov["incremental_roic_pct"] = min(d["incremental_roic_pct"], H["inc_roic_cap"])
        ov["maint_capex_pct_op"] = max(d["maint_capex_pct_op"], H["maint_capex_floor"])
        ov["ev_multiple"] = min(d["ev_multiple"], H["ev_cap"])
    # drop no-op overrides for readability
    return {k: v for k, v in ov.items() if abs(v - d[k]) > 1e-12}


def fdc(i, a, r, y):
    role, monthly, mgr = FOUNDER_ROLE[i]
    if mgr is not None:
        idx = [n for n, s in enumerate(a["staff"]) if s["role"].startswith(mgr)][0]
        if r["headcount"][idx][y * 12] >= 1:
            return 0.0
    return 12 * monthly * 1.03 ** (y - 1)


def metrics(a, ov, i=None):
    r = E.run(a, "base", ov)
    S = r["summary"]
    nd = E.run(a, "base", {**ov, "founder_draw_per_month": 0})["summary"]
    d = r["drivers"]
    founder_new = d["founder_leads_per_month"] * d["lead_to_proposal_pct"] * d["proposal_to_win_pct"]
    return dict(y3_op=S["y3_op"], y5_op=S["y5_op"], y5_rev=S["y5_revenue"],
                peak_with_draw=S["peak_funding_need"], peak_no_draw=nd["peak_funding_need"],
                cum_deploy_10y=S["lt_y10_cum_deployable"], y10_op=S["lt_y10_op"], y10_ev=S["lt_y10_ev"],
                y10_ev_at_2_38=S["lt_y10_op"] * min(d["ev_multiple"], H["ev_sdemedian"]),
                y5_active=S["y5_active_end"], founder_new_per_month=founder_new,
                breakeven=S["breakeven_month"], first_10k_month=S["first_month_op_10k"],
                y3_op_after_fdc=S["y3_op"] - fdc(i, a, r, 3), y5_op_after_fdc=S["y5_op"] - fdc(i, a, r, 5))


def rank(rows, key, reverse=True):
    order = sorted(rows, key=lambda i: rows[i][key], reverse=reverse)
    return {i: n + 1 for n, i in enumerate(order)}


# Composite ordering (stated rule): mean of four ranks - Y5 op after FDC (desc), Y3 op after FDC (desc),
# 10-yr cumulative deployable (desc), peak funding without draw (asc); ties broken by Y5 op after FDC.
COMPOSITE = [("y5_op_after_fdc", True), ("y3_op_after_fdc", True), ("cum_deploy_10y", True), ("peak_no_draw", False)]


def composite_rank(rows):
    rk = {key: rank(rows, key, rev) for key, rev in COMPOSITE}
    score = {i: sum(rk[key][i] for key, _ in COMPOSITE) / len(COMPOSITE) for i in rows}
    order = sorted(rows, key=lambda i: (score[i], -rows[i]["y5_op_after_fdc"]))
    return {i: (n + 1, score[i]) for n, i in enumerate(order)}


def main():
    out = {"rules": {k: v for k, v in H.items()}, "founder_roles": FOUNDER_ROLE, "models": {}}
    orig, harm = {}, {}
    for i in IDS:
        a = json.load(open(os.path.join(ROOT, "08_financial_models", f"{i}_assumptions.json")))
        ov = harmonized_overrides(i, a)
        orig[i] = metrics(a, {}, i)
        harm[i] = metrics(a, ov, i)
        # single-rule attribution on y5 op and 10-yr deployable
        attrib = {}
        for rule in ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"]:
            ovr = harmonized_overrides(i, a, (rule,) if rule != "H6" else ("H1", "H2", "H6"))
            if not ovr:
                continue
            m = metrics(a, ovr, i)
            attrib[rule] = {"overrides": ovr, "y5_op": m["y5_op"], "cum_deploy_10y": m["cum_deploy_10y"],
                            "y5_op_after_fdc": m["y5_op_after_fdc"]}
        out["models"][i] = {"name": a["name"], "overrides": ov, "original": orig[i],
                            "harmonized": harm[i], "attribution": attrib}
    for lab, rows in [("original", orig), ("harmonized", harm)]:
        for key, rev in [("y3_op", True), ("y5_op", True), ("cum_deploy_10y", True), ("peak_no_draw", False),
                         ("y5_op_after_fdc", True)]:
            rk = rank(rows, key, rev)
            for i in IDS:
                out["models"][i][lab][f"rank_{key}"] = rk[i]
    for lab, rows in [("original", orig), ("harmonized", harm)]:
        cr = composite_rank(rows)
        for i in IDS:
            out["models"][i][lab]["composite_rank"], out["models"][i][lab]["composite_score"] = cr[i]
    json.dump(out, open(os.path.join(OUT, "cross_model_audit_results.json"), "w"), indent=1, default=float)

    def k(x):
        return f"${x/1000:,.0f}k" if abs(x) < 1e6 else f"${x/1e6:,.2f}M"
    L = ["| ID | Y3 op orig → harm | Y5 op orig → harm | Peak funding no draw orig → harm | "
         "10-yr deployable orig → harm | Rank Y5 op o→h | Rank 10-yr o→h |", "|---|---|---|---|---|---|---|"]
    for i in sorted(IDS, key=lambda i: out["models"][i]["harmonized"]["rank_y5_op"]):
        o, h = out["models"][i]["original"], out["models"][i]["harmonized"]
        L.append(f"| {i} | {k(o['y3_op'])} → {k(h['y3_op'])} | {k(o['y5_op'])} → {k(h['y5_op'])} | "
                 f"{k(o['peak_no_draw'])} → {k(h['peak_no_draw'])} | {k(o['cum_deploy_10y'])} → {k(h['cum_deploy_10y'])} | "
                 f"{o['rank_y5_op']} → {h['rank_y5_op']} | {o['rank_cum_deploy_10y']} → {h['rank_cum_deploy_10y']} |")
    L += ["", "| Composite rank (harmonized) | ID | score | Composite rank (original) |", "|---|---|---|---|"]
    for i in sorted(IDS, key=lambda i: out["models"][i]["harmonized"]["composite_rank"]):
        h, o = out["models"][i]["harmonized"], out["models"][i]["original"]
        L.append(f"| {h['composite_rank']} | {i} | {h['composite_score']:.2f} | {o['composite_rank']} ({o['composite_score']:.2f}) |")
    L += ["", "| ID | Founder delivery role charged | FDC $/mo | Y5 op after FDC orig → harm | Rank o→h |", "|---|---|---|---|---|"]
    for i in sorted(IDS, key=lambda i: out["models"][i]["harmonized"]["rank_y5_op_after_fdc"]):
        o, h = out["models"][i]["original"], out["models"][i]["harmonized"]
        L.append(f"| {i} | {FOUNDER_ROLE[i][0]} | {FOUNDER_ROLE[i][1]:,} | {k(o['y5_op_after_fdc'])} → {k(h['y5_op_after_fdc'])} | "
                 f"{o['rank_y5_op_after_fdc']} → {h['rank_y5_op_after_fdc']} |")
    open(os.path.join(OUT, "cross_model_audit_table.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))
    print()
    for i in IDS:
        m = out["models"][i]
        print(i, "overrides:", {kk: round(v, 4) for kk, v in m["overrides"].items()})
        for r, v in m["attribution"].items():
            print("   ", r, "y5_op", round(v["y5_op"]), "y5_after_fdc", round(v["y5_op_after_fdc"]), "deploy", round(v["cum_deploy_10y"]))


if __name__ == "__main__":
    main()


# ---------------- Rule-dropping sensitivity (which rankings survive if one rule is relaxed) ----------------
ALL = ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9")


def sensitivity(out_path=None):
    variants = {"harmonized (all rules)": ALL,
                "drop H1 (no conversation cap)": tuple(r for r in ALL if r != "H1"),
                "drop H2 (template 10% conversion kept)": tuple(r for r in ALL if r != "H2"),
                "drop H6 (rep output not capped)": tuple(r for r in ALL if r != "H6"),
                "drop H5 (referrals not capped)": tuple(r for r in ALL if r != "H5"),
                "drop H7 (job-model volumes kept)": tuple(r for r in ALL if r != "H7"),
                "original": ()}
    res = {}
    for name, rules in variants.items():
        rows = {}
        for i in IDS:
            a = json.load(open(os.path.join(ROOT, "08_financial_models", f"{i}_assumptions.json")))
            ov = harmonized_overrides(i, a, rules) if rules else {}
            rows[i] = metrics(a, ov, i)
        cr = composite_rank(rows)
        res[name] = {i: {"composite_rank": cr[i][0], "y5_op": rows[i]["y5_op"], "y5_op_after_fdc": rows[i]["y5_op_after_fdc"],
                         "cum_deploy_10y": rows[i]["cum_deploy_10y"],
                         "rank_y5_op_after_fdc": rank(rows, "y5_op_after_fdc")[i],
                         "rank_y5_op": rank(rows, "y5_op")[i]} for i in IDS}
    L = ["| Variant | " + " | ".join(IDS) + " |", "|---|" + "---|" * len(IDS)]
    for name in variants:
        L.append(f"| {name} (COMPOSITE rank) | " + " | ".join(str(res[name][i]["composite_rank"]) for i in IDS) + " |")
    for name in variants:
        L.append(f"| {name} (rank by Y5 op after FDC) | " + " | ".join(str(res[name][i]["rank_y5_op_after_fdc"]) for i in IDS) + " |")
    for name in variants:
        L.append(f"| {name} (Y5 op after FDC, $k) | " + " | ".join(f"{res[name][i]['y5_op_after_fdc']/1000:,.0f}" for i in IDS) + " |")
    txt = "\n".join(L) + "\n"
    if out_path:
        open(out_path, "w").write(txt)
        json.dump(res, open(out_path.replace(".md", ".json"), "w"), indent=1)
    print(txt)
    return res


if __name__ == "__main__" and os.environ.get("ATLAS_SENS", "1") == "1":
    sensitivity(os.path.join(OUT, "cross_model_audit_sensitivity.md"))
