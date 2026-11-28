#!/usr/bin/env python3
"""Analytics on the -REV models for the capital-allocation and long-term-wealth reports (read-only)."""
import json, sys, copy, importlib.util
ROOT = "/home/user/playground/project-atlas"
sys.path.insert(0, ROOT + "/tools")
import fin_engine as E
spec = importlib.util.spec_from_file_location("cma", ROOT + "/07_review/cross_model_audit.py")
# cross_model_audit runs on import? guard by reading functions only
src = open(ROOT + "/07_review/cross_model_audit.py").read().split("\ndef main")[0]
cma = {}
exec(compile(src.split("if __name__")[0], "cma", "exec"), cma)
FM = ROOT + "/08_financial_models/"
IDS = ["WS12-014", "SYN-006", "SYN-004", "WS04-014"]
FDC_COST = {"WS12-014": 6900, "SYN-006": 6200, "SYN-004": 6000, "WS04-014": 7500}  # REV loaded cost of founder's delivery role
OUT = {}


def load(i):
    return json.load(open(FM + i + "_assumptions.json"))


def yr(R, k, y):
    return sum(R[k][(y - 1) * 12 + 1:y * 12 + 1])


def fdc(i, y):
    return 12 * FDC_COST[i] * 1.03 ** (y - 1)


for i in IDS:
    a = load(i + "-REV")
    o = OUT[i] = {}
    for s in E.SCEN:
        R = E.run(a, s); S = R["summary"]
        nd = E.run(a, s, {"founder_draw_per_month": 0})["summary"]
        lt = S["lt_table"]
        o[s] = dict(
            annual=[dict(y=y, rev=yr(R, "revenue", y), op=yr(R, "op", y), fcf=yr(R, "fcf", y), draw=yr(R, "draw", y),
                         retained=yr(R, "retained", y), active=R["active"][y * 12], heads=sum(h[y * 12] for h in R["headcount"]))
                    for y in range(1, 6)],
            lt=[{k: r[k] for k in ("year", "op", "owner_comp", "distributable", "deployable", "cum_deployable_positive", "ev")} for r in lt],
            peak=S["peak_funding_need"], peak_nodraw=nd["peak_funding_need"], breakeven=S["breakeven_month"],
            payback=S["payback_month"], first10k=S["first_month_op_10k"], first5k=S["first_month_op_5k"],
            min_cash_month=min(range(1, 61), key=lambda m: R["cum_retained"][m]),
            y3_op_after_fdc=S["y3_op"] - fdc(i, 3), y5_op_after_fdc=S["y5_op"] - fdc(i, 5),
            y10_op_after_fdc=lt[9]["op"] - 12 * FDC_COST[i] * 1.03 ** 9,
            owner_cash_3y=sum(r["owner_comp"] for r in lt[:3]) + lt[2]["cum_deployable_positive"],
            owner_cash_5y=sum(r["owner_comp"] for r in lt[:5]) + lt[4]["cum_deployable_positive"],
            owner_cash_10y=sum(r["owner_comp"] for r in lt) + lt[9]["cum_deployable_positive"],
        )
    # harmonized (audit H1-H9) applied to REV base
    ov = cma["harmonized_overrides"](i, a)
    R = E.run(a, "base", ov); S = R["summary"]
    nd = E.run(a, "base", {**ov, "founder_draw_per_month": 0})["summary"]
    o["harm"] = dict(overrides=ov, y3_op=S["y3_op"], y5_op=S["y5_op"], peak=S["peak_funding_need"], peak_nodraw=nd["peak_funding_need"],
                     dep10=S["lt_y10_cum_deployable"], y10_op=S["lt_y10_op"], y10_ev=S["lt_y10_ev"],
                     y3_after_fdc=S["y3_op"] - fdc(i, 3), y5_after_fdc=S["y5_op"] - fdc(i, 5),
                     dep3=S["lt_table"][2]["cum_deployable_positive"], dep5=S["lt_table"][4]["cum_deployable_positive"],
                     y10_after_fdc=S["lt_y10_op"] - 12 * FDC_COST[i] * 1.03 ** 9)
    # stresses (from built results)
    res = json.load(open(FM + i + "-REV_results.json"))
    o["stress"] = [{k: t[k] for k in ("test", "y3_op", "y5_op", "peak_funding_need")} for t in res["stress"]]
    o["worst_stress_peak"] = max(res["stress"], key=lambda t: t["peak_funding_need"])
    o["worst_stress_y3"] = min(res["stress"], key=lambda t: t["y3_op"])

# ---- special variants
a = load("WS12-014-REV")
D = {}
for tag, ov in [("2023-type", {"demand_multiplier": 0.75, "churn_multiplier": 1.3}),
                ("2009-type", {"demand_multiplier": 0.45, "churn_multiplier": 2}),
                ("fee 18% x 80%", {"onetime_revenue_per_new_customer": 105000 * 0.18 * 0.8}),
                ("no draw", {"founder_draw_per_month": 0})]:
    S = E.run(a, "base", ov)["summary"]; D[tag] = dict(y3=S["y3_op"], y5=S["y5_op"], peak=S["peak_funding_need"])
OUT["WS12-014"]["variants"] = D
# recruiter-hire incremental economics in the optimistic (= Stage E base) case
b = copy.deepcopy(a)
for s in b["staff"]:
    if s.get("is_sales_rep"):
        s["max_count"] = 0
Rh = E.run(a, "optimistic"); Rn = E.run(b, "optimistic")
OUT["WS12-014"]["hire_increment_opt"] = {f"y{y}": yr(Rh, "op", y) - yr(Rn, "op", y) for y in range(1, 6)}
OUT["WS12-014"]["hire_increment_opt"]["lt_y10_op"] = Rh["summary"]["lt_y10_op"] - Rn["summary"]["lt_y10_op"]
OUT["WS12-014"]["hire_month_opt"] = next((m for m in range(1, 61) if Rh["headcount"][0][m] >= 1), None)

# WS04-014 hire at 18 practices
w = load("WS04-014-REV"); w18 = copy.deepcopy(w)
for s in w18["staff"]:
    if s["role"].startswith("Field"):
        s["threshold"] = 18
S = E.run(w18, "base")["summary"]
OUT["WS04-014"]["hire18"] = dict(y3=S["y3_op"], y5=S["y5_op"], peak=S["peak_funding_need"], dep10=S["lt_y10_cum_deployable"])

# SYN-006 launched with hired staff (founder sells/manages only): bookkeeper from first client
sy = load("SYN-006-REV"); st = copy.deepcopy(sy)
for s in st["staff"]:
    if s["role"].startswith("Construction bookkeeper"):
        s["threshold"] = 0.01   # first bookkeeper as soon as there is a client; then one per 13
for scen in ("base", "conservative"):
    R = E.run(st, scen); S = R["summary"]; nd = E.run(st, scen, {"founder_draw_per_month": 0})["summary"]
    OUT["SYN-006"]["staffed_" + scen] = dict(y1=S["y1_op"], y2=S["y2_op"], y3=S["y3_op"], y5=S["y5_op"], peak=S["peak_funding_need"],
                                            peak_nodraw=nd["peak_funding_need"], dep10=S["lt_y10_cum_deployable"], y10_op=S["lt_y10_op"])
# staffed launch, no owner draw (the holding company funds it; founder is paid by the cash engine)
R = E.run(st, "base", {"founder_draw_per_month": 0}); S = R["summary"]
OUT["SYN-006"]["staffed_base_nodraw"] = dict(y1=S["y1_op"], y3=S["y3_op"], y5=S["y5_op"], peak=S["peak_funding_need"],
                                             cum_retained=[sum(R["retained"][1:12 * y + 1]) for y in range(1, 6)])

# SYN-004: reviewer's own conservative case (base drivers + overrides) for reference
s4 = load("SYN-004")
S = E.run(s4, "base", {"sales_cycle_months": 12, "founder_leads_per_month": 5, "proposal_to_win_pct": 0.15, "arpc_monthly": 650, "monthly_churn_pct": 0.018})["summary"]
OUT["SYN-004"]["reviewer_cons"] = dict(y3=S["y3_op"], y5=S["y5_op"], peak=S["peak_funding_need"])
# SYN-004 no draw until month 25 / no draw
for tag, ov in [("draw from m25", {"founder_draw_start_month": 25}), ("no draw", {"founder_draw_per_month": 0})]:
    S = E.run(load("SYN-004-REV"), "base", ov)["summary"]; OUT["SYN-004"][tag] = dict(y3=S["y3_op"], peak=S["peak_funding_need"])

# Stage E originals for comparison
OUT["stageE"] = {}
for i in IDS:
    r = json.load(open(FM + i + "_results.json"))
    OUT["stageE"][i] = {s: {k: r["scenarios"][s][k] for k in ("y3_op", "y5_op", "peak_funding_need", "lt_y10_cum_deployable", "lt_y10_ev")} for s in E.SCEN}

json.dump(OUT, open("/tmp/claude-0/atlas_scratch/WEALTH/analytics.json", "w"), indent=1, default=float)

k = lambda v: f"{v/1000:,.1f}k"
for i in IDS:
    o = OUT[i]
    print(f"\n===== {i}-REV")
    for s in E.SCEN:
        x = o[s]
        print(f" {s[:4]} op y1-5 " + " ".join(k(r['op']) for r in x['annual']) + f" | peak {k(x['peak'])} nodraw {k(x['peak_nodraw'])} | BE m{x['breakeven']} PB m{x['payback']} 5k m{x['first5k']} 10k m{x['first10k']} trough m{x['min_cash_month']}")
        print(f"      fcf y1-5 " + " ".join(k(r['fcf']) for r in x['annual']) + " | active " + " ".join(f"{r['active']:.1f}" for r in x['annual']) + " | heads " + " ".join(str(r['heads']) for r in x['annual']))
        lt = x["lt"]
        print(f"      LT op y3/5/10 {k(lt[2]['op'])} {k(lt[4]['op'])} {k(lt[9]['op'])} | cumdep y3/5/10 {k(lt[2]['cum_deployable_positive'])} {k(lt[4]['cum_deployable_positive'])} {k(lt[9]['cum_deployable_positive'])} | EV y3/5/10 {k(lt[2]['ev'])} {k(lt[4]['ev'])} {k(lt[9]['ev'])}")
        print(f"      after FDC y3 {k(x['y3_op_after_fdc'])} y5 {k(x['y5_op_after_fdc'])} y10 {k(x['y10_op_after_fdc'])} | owner cash 3/5/10y {k(x['owner_cash_3y'])} {k(x['owner_cash_5y'])} {k(x['owner_cash_10y'])}")
        print("      deployable by yr " + " ".join(k(r['deployable']) for r in lt))
    h = o["harm"]
    print(f" HARM ov={ {kk: round(v,3) for kk,v in h['overrides'].items()} }")
    print(f"      y3 {k(h['y3_op'])} y5 {k(h['y5_op'])} peak {k(h['peak'])} nd {k(h['peak_nodraw'])} dep3/5/10 {k(h['dep3'])} {k(h['dep5'])} {k(h['dep10'])} y10op {k(h['y10_op'])} ev10 {k(h['y10_ev'])} | afterFDC y3 {k(h['y3_after_fdc'])} y5 {k(h['y5_after_fdc'])} y10 {k(h['y10_after_fdc'])}")
    print(" worst peak stress:", o["worst_stress_peak"]["test"], k(o["worst_stress_peak"]["peak_funding_need"]), "| worst y3:", o["worst_stress_y3"]["test"], k(o["worst_stress_y3"]["y3_op"]))
    for t in o["stress"]:
        print(f"    {t['test'][:55]:55s} y3 {k(t['y3_op']):>9} y5 {k(t['y5_op']):>9} peak {k(t['peak_funding_need']):>9}")
    for kk in ("variants", "hire_increment_opt", "hire_month_opt", "hire18", "staffed_base", "staffed_conservative", "staffed_base_nodraw", "reviewer_cons", "draw from m25", "no draw"):
        if kk in o:
            print(" ", kk, o[kk])
