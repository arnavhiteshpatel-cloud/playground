"""WS18-035 reviewer variants (read-only; overrides passed to fin_engine.run)."""
import json, sys
sys.path.insert(0, "/home/user/playground/project-atlas/tools")
import fin_engine as E
a = json.load(open("/home/user/playground/project-atlas/08_financial_models/WS18-035_assumptions.json"))
d0 = E.run(a, "base")["drivers"]

def leads_for(J, l2p, p2w, ref):
    return J * (1 - ref / 100) / (l2p * p2w)

def show(name, ov, a2=None):
    aa = a2 or a
    r = E.run(aa, "base", ov); S = r["summary"]
    nd = E.run(aa, "base", {**ov, "founder_draw_per_month": 0})["summary"]
    fdc5 = 12 * 6800 * 1.03 ** 4; fdc3 = 12 * 6800 * 1.03 ** 2
    print(f"{name:62s} y1 {S['y1_op']/1e3:7.0f}k y3 {S['y3_op']/1e3:7.0f}k y5 {S['y5_op']/1e3:7.0f}k | y5-FDC {(S['y5_op']-fdc5)/1e3:6.0f}k | "
          f"peak(draw) {S['peak_funding_need']/1e3:5.0f}k peak(no draw) {nd['peak_funding_need']/1e3:5.0f}k | 10y dep {S['lt_y10_cum_deployable']/1e3:6.0f}k | "
          f"jobs y5 {S['y5_active_end']:.0f} | y3op/peak {S['y3_op']/max(1,S['peak_funding_need']):.2f}")
    return S

show("Model base (as filed)", {})
show("H7 franchise-median volume (58.9 jobs/mo)", {"founder_leads_per_month": leads_for(58.9, .65, .85, 4)})
# Reviewer ticket: Raynor Chicago guides (May/Jun 2026) most repairs $150-500, opener installed $250-600 [D, F6-S001/S002]
# mix 78% repairs @ $350, 13% openers @ $650, 9% doors @ $2,100 => $546
show("Ticket $545 only", {"onetime_revenue_per_new_customer": 545})
# CAC: $64 blended per lead / (book 0.55 x paid 0.85 = 0.4675) = $137 per paid job
show("CAC $137 only (book 55%, paid 85%)", {"cac_per_new_customer": 137, "lead_to_proposal_pct": 0.55})
show("Margin 0.58 only", {"onetime_gross_margin_pct": 0.58})
rev = {"founder_leads_per_month": leads_for(58.9, .55, .85, 4), "lead_to_proposal_pct": 0.55,
       "onetime_revenue_per_new_customer": 545, "cac_per_new_customer": 137, "onetime_gross_margin_pct": 0.58}
S = show("REVIEWER BASE: 58.9 jobs, $545, CAC $137, GM 58%", rev)
show("Reviewer base + model volume (133 jobs)", {**rev, "founder_leads_per_month": leads_for(132.6/(1-0.04)*(1-0.04), .55, .85, 4)})
show("Reviewer base + 90 jobs/mo plateau", {**rev, "founder_leads_per_month": leads_for(90, .55, .85, 4)})
a45 = json.loads(json.dumps(a)); a45["staff"][0]["threshold"] = 45; a45["staff"][0]["per"] = 60
show("Reviewer base, founder field capacity 45 jobs/mo (tech at 45)", rev, a45)
show("Reviewer base, B2B share: CAC $90, ticket $575", {**rev, "cac_per_new_customer": 90, "onetime_revenue_per_new_customer": 575})
cons = {"founder_leads_per_month": leads_for(45, .45, .80, 3), "lead_to_proposal_pct": 0.45, "proposal_to_win_pct": 0.80,
        "referral_new_per_100_active": 3, "onetime_revenue_per_new_customer": 475, "cac_per_new_customer": 178,
        "onetime_gross_margin_pct": 0.52, "sales_start_delay_months": 3, "founder_ramp_months": 36}
show("REVIEWER CONSERVATIVE: 45 jobs, $475, CAC $178, GM 52%", cons)
opt = {"founder_leads_per_month": leads_for(120, .65, .85, 6), "referral_new_per_100_active": 6,
       "onetime_revenue_per_new_customer": 650, "cac_per_new_customer": 85, "onetime_gross_margin_pct": 0.62}
show("REVIEWER OPTIMISTIC: 120 jobs, $650, CAC $85, GM 62%", opt)
