import json, sys
sys.path.insert(0, "/home/user/playground/project-atlas/tools")
import fin_engine as E
P = "/home/user/playground/project-atlas/08_financial_models/"
def load(i): return json.load(open(P + i + "_assumptions.json"))
def show(tag, a, scen="base", ov=None):
    S = E.run(a, scen, ov or {})["summary"]
    print(f"{tag:58s} y1 {S['y1_op']:>9,.0f} y2 {S['y2_op']:>9,.0f} y3 {S['y3_op']:>9,.0f} y5 {S['y5_op']:>9,.0f} | y3rev {S['y3_revenue']:>10,.0f} y5rev {S['y5_revenue']:>10,.0f} | peak {S['peak_funding_need']:>8,.0f} | act3 {S['y3_active_end']:5.1f} act5 {S['y5_active_end']:5.1f} | be {S['breakeven_month']} | y10dep {S['lt_y10_cum_deployable']:>10,.0f}")
    return S
# ---------------- WS12-012
a = load("WS12-012")
print("WS12-012")
show("Stage E base (as filed)", a)
show("Stage E conservative (as filed)", a, "conservative")
show("Stage E conservative, no draw", a, "conservative", {"founder_draw_per_month": 0})
C = {"arpc_monthly": 2700, "gross_margin_pct": 0.27, "founder_leads_per_month": 10,
     "lead_to_proposal_pct": 0.35, "proposal_to_win_pct": 0.22}
show("price only $2,250x1.2=$2,700", a, "base", {"arpc_monthly": 2700})
show("GM only 27%", a, "base", {"gross_margin_pct": 0.27})
show("funnel only 10x35%x22%", a, "base", {"founder_leads_per_month": 10, "lead_to_proposal_pct": 0.35, "proposal_to_win_pct": 0.22})
S = show("F5 corrected base", a, "base", C)
show("F5 corrected base, no draw", a, "base", dict(C, founder_draw_per_month=0))
show("F5 corrected base + churn 3.5% (AI)", a, "base", dict(C, monthly_churn_pct=0.035))
show("F5 corrected base + GM 25%", a, "base", dict(C, gross_margin_pct=0.25))
show("F5 corrected base + GM 29% (pilots beat)", a, "base", dict(C, gross_margin_pct=0.29))
show("F5 corrected base + recession", a, "base", dict(C, demand_multiplier=0.7, churn_multiplier=1.5))
show("F5 corrected base, entity +$500/mo (x overhead 1.2)", a, "base", dict(C, overhead_multiplier=1.2))
show("F5 corrected optimistic (GM .33, arpc 3000, leads 14)", a, "base", dict(C, gross_margin_pct=0.33, arpc_monthly=3000, founder_leads_per_month=14))
show("F5 corrected conservative = filed cons", a, "conservative")
# ---------------- WS12-014
b = load("WS12-014")
print("\nWS12-014")
show("Stage E base (as filed)", b)
show("Stage E conservative (as filed)", b, "conservative")
show("leads 9 x conv 0.22 only", b, "base", {"lead_to_proposal_pct": 0.22})
show("fill 0.15 only", b, "base", {"proposal_to_win_pct": 0.15})
show("ramp 15 only", b, "base", {"founder_ramp_months": 15})
D = {"lead_to_proposal_pct": 0.22, "proposal_to_win_pct": 0.15, "founder_ramp_months": 15,
     "arpc_monthly": 520, "monthly_churn_pct": 0.055, "sales_cycle_months": 5}
S2 = show("F5 corrected base", b, "base", D)
show("F5 corrected base, no draw", b, "base", dict(D, founder_draw_per_month=0))
show("F5 corrected base + 2023-type (new x0.75 churn x1.3)", b, "base", dict(D, demand_multiplier=0.75, churn_multiplier=1.3))
show("F5 corrected base + 2009-type (new x0.45 churn x2)", b, "base", dict(D, demand_multiplier=0.45, churn_multiplier=2))
show("F5 corrected base + fee 18%x80% realised", b, "base", dict(D, onetime_revenue_per_new_customer=105000*0.18*0.8))
show("F5 corrected optimistic = Stage E base", b, "base")
show("F5 corrected conservative = filed cons", b, "conservative")
R = E.run(b, "base", D)
print("placements y1-5 (first + repeat est):", [round(sum(R['new'][(y-1)*12+1:y*12+1]) + sum(R['rev_rec'][(y-1)*12+1:y*12+1])/ (17850*1.03**(y-1)),1) for y in range(1,6)])
R0 = E.run(b, "base")
print("Stage E base placements y1-5:", [round(sum(R0['new'][(y-1)*12+1:y*12+1]) + sum(R0['rev_rec'][(y-1)*12+1:y*12+1])/ (17850*1.03**(y-1)),1) for y in range(1,6)])
print("Stage E base new first-time clients y1-5:", [round(sum(R0['new'][(y-1)*12+1:y*12+1]),1) for y in range(1,6)], "rep_count m60", R0['rep_count'][60])
print("corrected rep_count m60", R['rep_count'][60], "headcount", [h[60] for h in R['headcount']])
