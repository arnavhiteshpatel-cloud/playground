#!/usr/bin/env python3
"""Project Atlas driver-based financial model engine (Python mirror of the Excel formulas).

One generic engine covers recurring-service, distribution, brokerage and transactional businesses:
  new customers = founder pipeline (ramped, delayed by setup + sales cycle) + productive sales reps + referrals
  active customers = prior × (1 − churn) + new − shock losses
  revenue = active × recurring ARPC × price index + new × one-time revenue × price index
  gross profit, variable opex, acquisition cost → contribution → staff (capacity-triggered) → overhead
  → operating profit (EBITDA basis, BEFORE owner compensation) → taxes (cumulative, NOL-aware) → capex
  → working capital (DSO/DIO/DPO) → free cash flow → owner draw → retained cash → cash balance.
The Excel builder (build_fin_model.py) writes the same logic as live formulas; verify_fin_model.py checks
that a LibreOffice recalculation of the workbook matches this mirror.
"""
import copy, math

SCEN = ["conservative", "base", "optimistic"]
MONTHS = 60

# driver key -> (label, unit, default)
DRIVERS = [
 ("sales_start_delay_months", "Months of setup before selling can start (licensing, insurance, supplier onboarding)", "months", 1),
 ("sales_cycle_months", "Average sales cycle (lead to signed customer)", "months", 1),
 ("founder_ramp_months", "Months for founder selling to reach full pace", "months", 4),
 ("founder_leads_per_month", "Qualified conversations/leads the founder generates per month at full pace", "leads/mo", 20),
 ("lead_to_proposal_pct", "Qualified lead → proposal/quote", "%", 0.4),
 ("proposal_to_win_pct", "Proposal/quote → paying customer", "%", 0.25),
 ("rep_ramp_months", "Months before a new sales rep is productive", "months", 3),
 ("rep_new_customers_per_month", "New customers per productive sales rep per month", "cust/mo", 3),
 ("referral_new_per_100_active", "Referral/inbound new customers per month per 100 active customers", "cust/mo", 0.5),
 ("monthly_churn_pct", "Monthly customer churn", "%", 0.015),
 ("arpc_monthly", "Recurring revenue per active customer per month", "$/mo", 500),
 ("onetime_revenue_per_new_customer", "One-time revenue per new customer (setup, first order, first job)", "$", 0),
 ("arpc_annual_growth_pct", "Annual price/expansion growth on revenue per customer", "%/yr", 0.03),
 ("gross_margin_pct", "Gross margin on recurring revenue", "%", 0.4),
 ("onetime_gross_margin_pct", "Gross margin on one-time revenue", "%", 0.4),
 ("variable_opex_pct_revenue", "Variable opex as % of revenue (processing, commissions, fuel...)", "%", 0.03),
 ("cac_per_new_customer", "Variable acquisition cost per new customer (ads, leads, samples, travel)", "$", 200),
 ("fixed_marketing_per_month", "Fixed marketing / sales tools per month", "$/mo", 300),
 ("dso_days", "Days sales outstanding (negative = customer prepays)", "days", 30),
 ("inventory_days_cogs", "Inventory on hand, days of COGS", "days", 0),
 ("dpo_days", "Days payables outstanding (supplier credit)", "days", 15),
 ("tax_rate_pct", "Blended income-tax rate on profit after owner draw (pass-through; simplified)", "%", 0.30),
 ("founder_draw_per_month", "Owner draw / compensation per month", "$/mo", 0),
 ("founder_draw_start_month", "Month owner draw begins", "month", 13),
 ("start_capital_injection", "Owner capital injected in month 1 (for cash-balance tracking)", "$", 10000),
 ("shock_month", "Stress: month of a one-time customer loss (0 = none)", "month", 0),
 ("shock_loss_pct", "Stress: share of active customers lost in shock month", "%", 0),
 ("demand_multiplier", "Stress multiplier on all new-customer generation", "x", 1),
 ("churn_multiplier", "Stress multiplier on churn", "x", 1),
 ("labor_cost_multiplier", "Stress multiplier on staff cost", "x", 1),
 ("overhead_multiplier", "Stress multiplier on non-AI overhead", "x", 1),
 ("ai_cost_multiplier", "Stress multiplier on AI/software overhead items", "x", 1),
 ("staff_threshold_multiplier", "Stress multiplier on hiring thresholds (<1 = hire earlier)", "x", 1),
 # long-term (years 6-10) capital-accumulation drivers
 ("lt_growth_y6_pct", "Operating-profit growth in year 6", "%", 0.10),
 ("lt_growth_decay", "Annual decay factor of growth after year 6", "x", 0.85),
 ("incremental_roic_pct", "Incremental pre-tax return on growth reinvestment (years 6-10)", "%", 0.5),
 ("maint_capex_pct_op", "Maintenance capex as % of operating profit (years 6-10)", "%", 0.05),
 ("reserve_months", "Cash reserve target, months of cash operating costs", "months", 2),
 ("owner_comp_growth_pct", "Annual growth of owner/manager compensation (years 6-10)", "%", 0.03),
 ("ev_multiple", "Enterprise value multiple of operating profit (EBITDA/SDE basis)", "x", 3.0),
]
DRIVER_KEYS = [d[0] for d in DRIVERS]
DEFAULTS = {d[0]: d[3] for d in DRIVERS}


def get(a, key, scen):
    v = a["drivers"].get(key)
    if v is None:
        return DEFAULTS[key]
    if isinstance(v, dict):
        x = v.get(scen, v.get("base"))
        return DEFAULTS[key] if x is None else x
    return v


def sval(v, scen):
    if isinstance(v, dict):
        return v.get(scen, v.get("base"))
    return v


def run(a, scen="base", overrides=None):
    """Return dict of monthly rows + summary for one scenario. overrides: {driver_key: value} applied after lookup."""
    ov = overrides or {}
    d = {k: (ov[k] if k in ov else get(a, k, scen)) for k in DRIVER_KEYS}
    staff = a.get("staff", [])
    overhead = a.get("overhead", [])
    capex_items = a.get("capex", [])
    M = MONTHS
    R = {k: [0.0] * (M + 1) for k in ["ramp","founder_new","rep_count","productive_reps","rep_new","referral_new",
         "new","churned","active","price_index","rev_rec","rev_one","revenue","cogs","gp","var_opex","acq",
         "contribution","staff_cost","overhead","op","capex","ar","inv","ap","nwc","dnwc","draw","cum_taxable",
         "tax","fcf","retained","cum_retained","cash","breakeven_helper"]}
    hc = [[0.0] * (M + 1) for _ in staff]
    for m in range(1, M + 1):
        yr = (m - 1) // 12 + 1
        start = d["sales_start_delay_months"] + d["sales_cycle_months"]
        R["ramp"][m] = 0 if m <= start else min(1.0, (m - start) / max(1, d["founder_ramp_months"]))
        R["founder_new"][m] = (R["ramp"][m] * d["founder_leads_per_month"] * d["lead_to_proposal_pct"]
                               * d["proposal_to_win_pct"] * d["demand_multiplier"])
        prev_active = R["active"][m - 1]
        prev_rev = R["revenue"][m - 1]
        # staff headcount (uses previous-month drivers -> no circularity)
        for i, s in enumerate(staff):
            trig = s.get("trigger", "month")
            st = s.get("start_month", 1)
            thr = (s.get("threshold") or 0) * d["staff_threshold_multiplier"]
            per = max(1e-9, (s.get("per") or 1) * d["staff_threshold_multiplier"])
            if trig == "month":
                h = s.get("count", 1) if m >= st else 0
            elif trig == "active_customers":
                h = (math.floor((prev_active - thr) / per) + 1) if (m >= st and prev_active >= thr) else 0
            elif trig == "revenue":
                h = (math.floor((prev_rev - thr) / per) + 1) if (m >= st and prev_rev >= thr) else 0
            else:
                raise ValueError(trig)
            if s.get("max_count") is not None:
                h = min(h, s["max_count"])
            hc[i][m] = h
        R["rep_count"][m] = sum(hc[i][m] for i, s in enumerate(staff) if s.get("is_sales_rep"))
        lag = int(d["rep_ramp_months"])
        R["productive_reps"][m] = R["rep_count"][m - lag] if m - lag >= 1 else 0
        R["rep_new"][m] = R["productive_reps"][m] * d["rep_new_customers_per_month"] * d["demand_multiplier"]
        R["referral_new"][m] = prev_active / 100 * d["referral_new_per_100_active"] * d["demand_multiplier"]
        R["new"][m] = R["founder_new"][m] + R["rep_new"][m] + R["referral_new"][m]
        R["churned"][m] = (prev_active * d["monthly_churn_pct"] * d["churn_multiplier"]
                           + (prev_active * d["shock_loss_pct"] if m == d["shock_month"] else 0))
        R["active"][m] = prev_active + R["new"][m] - R["churned"][m]
        R["price_index"][m] = (1 + d["arpc_annual_growth_pct"]) ** (yr - 1)
        R["rev_rec"][m] = R["active"][m] * d["arpc_monthly"] * R["price_index"][m]
        R["rev_one"][m] = R["new"][m] * d["onetime_revenue_per_new_customer"] * R["price_index"][m]
        R["revenue"][m] = R["rev_rec"][m] + R["rev_one"][m]
        R["cogs"][m] = R["rev_rec"][m] * (1 - d["gross_margin_pct"]) + R["rev_one"][m] * (1 - d["onetime_gross_margin_pct"])
        R["gp"][m] = R["revenue"][m] - R["cogs"][m]
        R["var_opex"][m] = R["revenue"][m] * d["variable_opex_pct_revenue"]
        R["acq"][m] = R["new"][m] * d["cac_per_new_customer"] + d["fixed_marketing_per_month"]
        R["contribution"][m] = R["gp"][m] - R["var_opex"][m] - R["acq"][m]
        sc = 0.0
        cap_hire = 0.0
        for i, s in enumerate(staff):
            cost = sval(s["monthly_cost"], scen)
            sc += hc[i][m] * cost * (1 + s.get("annual_raise_pct", 0.03)) ** (yr - 1) * d["labor_cost_multiplier"]
            cap_hire += max(0, hc[i][m] - hc[i][m - 1]) * (sval(s.get("capex_per_hire", 0), scen) or 0)
        R["staff_cost"][m] = sc
        oh = 0.0
        for it in overhead:
            if m >= it.get("start_month", 1):
                mult = d["ai_cost_multiplier"] if it.get("is_ai") else d["overhead_multiplier"]
                oh += sval(it["monthly"], scen) * (1 + it.get("annual_growth_pct", 0.03)) ** (yr - 1) * mult
        R["overhead"][m] = oh
        R["op"][m] = R["contribution"][m] - R["staff_cost"][m] - R["overhead"][m]
        cx = sum(sval(c["amount"], scen) for c in capex_items if c.get("month", 1) == m)
        R["capex"][m] = cx + cap_hire
        R["ar"][m] = R["revenue"][m] * d["dso_days"] / 30
        R["inv"][m] = R["cogs"][m] * d["inventory_days_cogs"] / 30
        R["ap"][m] = R["cogs"][m] * d["dpo_days"] / 30
        R["nwc"][m] = R["ar"][m] + R["inv"][m] - R["ap"][m]
        R["dnwc"][m] = R["nwc"][m] - R["nwc"][m - 1]
        R["draw"][m] = d["founder_draw_per_month"] if m >= d["founder_draw_start_month"] else 0
        R["cum_taxable"][m] = R["cum_taxable"][m - 1] + R["op"][m] - R["draw"][m]
        R["tax"][m] = d["tax_rate_pct"] * max(0, R["cum_taxable"][m]) - d["tax_rate_pct"] * max(0, R["cum_taxable"][m - 1])
        R["fcf"][m] = R["op"][m] - R["tax"][m] - R["capex"][m] - R["dnwc"][m]
        R["retained"][m] = R["fcf"][m] - R["draw"][m]
        R["cum_retained"][m] = R["cum_retained"][m - 1] + R["retained"][m]
        R["cash"][m] = d["start_capital_injection"] + R["cum_retained"][m]
        R["breakeven_helper"][m] = (R["breakeven_helper"][m - 1] if R["breakeven_helper"][m - 1] > 0
                                    else (m if R["op"][m] > 0 else 0))
    R["headcount"] = hc
    R["drivers"] = d
    R["summary"] = summarize(R, d, a, scen)
    return R


def yearly(R, key, y):
    return sum(R[key][(y - 1) * 12 + 1: y * 12 + 1])


def summarize(R, d, a, scen):
    S = {}
    for y in range(1, 6):
        for k in ["revenue", "gp", "op", "tax", "capex", "dnwc", "fcf", "draw", "retained"]:
            S[f"y{y}_{k}"] = yearly(R, k, y)
        S[f"y{y}_active_end"] = R["active"][y * 12]
        S[f"y{y}_headcount_end"] = sum(h[y * 12] for h in R["headcount"])
    S["breakeven_month"] = R["breakeven_helper"][MONTHS]
    S["peak_funding_need"] = -min(0, min(R["cum_retained"][1:]))
    S["min_cash_balance"] = min(R["cash"][1:])
    cap = max(S["peak_funding_need"], 1.0)
    S["y3_op_over_peak_funding"] = S["y3_op"] / cap
    # payback: first month cumulative retained >= 0 after having been negative
    pb = 0
    neg = False
    for m in range(1, MONTHS + 1):
        if R["cum_retained"][m] < 0:
            neg = True
        if neg and R["cum_retained"][m] >= 0:
            pb = m
            break
    S["payback_month"] = pb if neg else 0
    # first month operating profit >= milestone thresholds
    for label, thr in [("1k", 1000), ("5k", 5000), ("10k", 10000), ("25k", 25000)]:
        S[f"first_month_op_{label}"] = next((m for m in range(1, MONTHS + 1) if R["op"][m] >= thr), 0)
    # 10-year capital accumulation
    lt = long_term(R, d)
    S.update({f"lt_{k}": v for k, v in lt.items() if not isinstance(v, list)})
    S["lt_table"] = lt["table"]
    return S


def long_term(R, d):
    rows = []
    op_prev = None
    comp_prev = None
    reserve_prev = 0.0
    cum_deploy = 0.0
    for y in range(1, 11):
        if y <= 5:
            op = yearly(R, "op", y)
            comp = yearly(R, "draw", y)
            tax = yearly(R, "tax", y)
            reinvest = yearly(R, "capex", y) + yearly(R, "dnwc", y)
            maint = 0.0
            cash_costs = yearly(R, "revenue", y) - op
        else:
            g = d["lt_growth_y6_pct"] * d["lt_growth_decay"] ** (y - 6)
            op = op_prev * (1 + g)
            comp = comp_prev * (1 + d["owner_comp_growth_pct"])
            tax = d["tax_rate_pct"] * max(0, op - comp)
            maint = d["maint_capex_pct_op"] * max(0, op)
            reinvest = max(0, op - op_prev) / max(1e-9, d["incremental_roic_pct"])
            cash_costs = rows[-1]["cash_costs"] * (1 + g)
        distributable = op - comp - tax - maint - reinvest
        reserve = d["reserve_months"] * cash_costs / 12
        d_res = reserve - reserve_prev
        deploy = distributable - d_res
        cum_deploy += max(0, deploy)
        rows.append({"year": y, "op": op, "owner_comp": comp, "tax": tax, "maint_capex": maint,
                     "growth_reinvest": reinvest, "distributable": distributable, "reserve_target": reserve,
                     "delta_reserve": d_res, "deployable": deploy, "cum_deployable_positive": cum_deploy,
                     "ev": op * d["ev_multiple"], "cash_costs": cash_costs})
        op_prev, comp_prev, reserve_prev = op, comp, reserve
    return {"table": rows, "y5_cum_deployable": rows[4]["cum_deployable_positive"],
            "y10_cum_deployable": rows[9]["cum_deployable_positive"], "y5_ev": rows[4]["ev"],
            "y10_ev": rows[9]["ev"], "y10_op": rows[9]["op"],
            "cum_owner_comp_10y": sum(r["owner_comp"] for r in rows),
            "owner_wealth_y10": rows[9]["cum_deployable_positive"] + sum(r["owner_comp"] for r in rows) + rows[9]["ev"]}


STRESS_TESTS = [
 ("CAC doubles", lambda d: {"cac_per_new_customer": d["cac_per_new_customer"] * 2, "fixed_marketing_per_month": d["fixed_marketing_per_month"] * 2}),
 ("Win rate 40% below plan", lambda d: {"proposal_to_win_pct": d["proposal_to_win_pct"] * 0.6, "rep_new_customers_per_month": d["rep_new_customers_per_month"] * 0.6}),
 ("Sales cycle doubles", lambda d: {"sales_cycle_months": max(d["sales_cycle_months"] * 2, d["sales_cycle_months"] + 2), "rep_ramp_months": d["rep_ramp_months"] * 2}),
 ("Gross margin −5 pts", lambda d: {"gross_margin_pct": d["gross_margin_pct"] - 0.05, "onetime_gross_margin_pct": d["onetime_gross_margin_pct"] - 0.05}),
 ("Gross margin −10 pts", lambda d: {"gross_margin_pct": d["gross_margin_pct"] - 0.10, "onetime_gross_margin_pct": d["onetime_gross_margin_pct"] - 0.10}),
 ("Key supplier refuses (3-mo delay, −5 pts margin)", lambda d: {"sales_start_delay_months": d["sales_start_delay_months"] + 3, "gross_margin_pct": d["gross_margin_pct"] - 0.05, "onetime_gross_margin_pct": d["onetime_gross_margin_pct"] - 0.05}),
 ("Largest customers leave (25% of base lost in month 18)", lambda d: {"shock_month": 18, "shock_loss_pct": 0.25}),
 ("Customers pay 30 days later", lambda d: {"dso_days": d["dso_days"] + 30}),
 ("Slow inventory (+30 days)", lambda d: {"inventory_days_cogs": d["inventory_days_cogs"] + 30}),
 ("Labor cost +20%", lambda d: {"labor_cost_multiplier": 1.2}),
 ("Insurance/overhead +50%", lambda d: {"overhead_multiplier": 1.5}),
 ("AI/software cost ×3", lambda d: {"ai_cost_multiplier": 3}),
 ("Hires needed 30% sooner", lambda d: {"staff_threshold_multiplier": 0.7}),
 ("Recession (new −30%, churn ×1.5)", lambda d: {"demand_multiplier": 0.7, "churn_multiplier": 1.5}),
 ("Competitor response (no price growth, −3 pts margin, churn ×1.3)", lambda d: {"arpc_annual_growth_pct": 0.0, "gross_margin_pct": d["gross_margin_pct"] - 0.03, "churn_multiplier": 1.3}),
 ("Founder capacity 40% lower", lambda d: {"founder_leads_per_month": d["founder_leads_per_month"] * 0.6}),
 ("Growth takes twice as long", lambda d: {"founder_ramp_months": d["founder_ramp_months"] * 2, "founder_leads_per_month": d["founder_leads_per_month"] * 0.5, "referral_new_per_100_active": d["referral_new_per_100_active"] * 0.5}),
]

TORNADO = ["founder_leads_per_month", "proposal_to_win_pct", "arpc_monthly", "gross_margin_pct",
           "monthly_churn_pct", "cac_per_new_customer", "dso_days", "referral_new_per_100_active",
           "labor_cost_multiplier", "overhead_multiplier", "onetime_revenue_per_new_customer"]


def stress(a):
    base = run(a, "base")
    out = [{"test": "Base case", **pick(base["summary"])}]
    for name, fn in STRESS_TESTS:
        r = run(a, "base", fn(base["drivers"]))
        out.append({"test": name, **pick(r["summary"])})
    return out


def tornado(a):
    base = run(a, "base")
    d = base["drivers"]
    out = []
    for k in TORNADO:
        lo = run(a, "base", {k: d[k] * 0.75})["summary"]
        hi = run(a, "base", {k: d[k] * 1.25})["summary"]
        out.append({"driver": k, "base_value": d[k], "low_value": d[k] * 0.75, "high_value": d[k] * 1.25,
                    "y3_op_low": lo["y3_op"], "y3_op_high": hi["y3_op"],
                    "peak_funding_low": lo["peak_funding_need"], "peak_funding_high": hi["peak_funding_need"],
                    "y5_cum_retained_low": sum(lo[f"y{y}_retained"] for y in range(1, 6)),
                    "y5_cum_retained_high": sum(hi[f"y{y}_retained"] for y in range(1, 6))})
    out.sort(key=lambda r: -abs(r["y3_op_high"] - r["y3_op_low"]))
    return out


def pick(S):
    return {k: S[k] for k in ["y1_revenue", "y1_op", "y2_op", "y3_op", "y5_op", "y3_fcf", "breakeven_month",
                              "peak_funding_need", "payback_month", "y5_active_end", "lt_y10_cum_deployable"]}
