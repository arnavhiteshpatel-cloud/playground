#!/usr/bin/env python3
"""Build an editable, formula-driven XLSX financial model from an assumptions JSON.

Usage: python3 tools/build_fin_model.py 08_financial_models/<ID>_assumptions.json [...]
       python3 tools/build_fin_model.py --all
Writes 08_financial_models/<ID>_model.xlsx and <ID>_results.json (Python-mirror results incl. stress tests).
Verify formulas against the mirror with tools/verify_fin_model.py.

Assumptions JSON schema (see 08_financial_models/TEMPLATE_assumptions.json):
{ "id", "name", "summary", "evidence_notes": [..], "drivers": {key: number | {conservative, base, optimistic},
  "<key>__evidence": "C", "<key>__source": "..."}, "staff": [...], "overhead": [...], "capex": [...],
  "transactions": [{"name", "revenue", "lines": [{"item","amount"}], "notes", "evidence"}] }
"""
import json, sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fin_engine as E

ROOT = pathlib.Path(__file__).resolve().parents[1]
FM = ROOT / "08_financial_models"
SC_COL = {"conservative": "D", "base": "E", "optimistic": "F"}
SHEET = {"conservative": "M_Conservative", "base": "M_Base", "optimistic": "M_Optimistic"}
M = E.MONTHS
FIRST, LAST = "C", L(M + 2)          # month 1 = column C ... month 60
BOLD = Font(bold=True)
HDR = PatternFill("solid", fgColor="1F3864"); HFont = Font(bold=True, color="FFFFFF")
INPUT = PatternFill("solid", fgColor="FFF2CC")
SECTION = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="BFBFBF")
PCT_KEYS = {k for k, lab, u, dflt in E.DRIVERS if u in ("%", "%/yr")}


def hdr(ws, row, values):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v); c.fill = HDR; c.font = HFont
        c.alignment = Alignment(wrap_text=True, vertical="top")


def build(path):
    a = json.loads(pathlib.Path(path).read_text())
    oid = a["id"]
    wb = Workbook()
    # ---------------- README
    ws = wb.active; ws.title = "README"
    lines = [f"Project Atlas financial model — {a['name']} ({oid})", "",
             a.get("summary", ""), "",
             "HOW TO USE: yellow cells on Assumptions/Staff/Overhead/Capex are inputs. Every other number is a live formula.",
             "Three scenario sheets (M_Conservative, M_Base, M_Optimistic) each read their own assumption column.",
             "Operating profit is EBITDA-basis and BEFORE owner compensation; owner draw is shown separately.",
             "Taxes: simplified pass-through estimate on cumulative profit after owner draw (loss-aware). Get real tax advice.",
             "Stress and Sensitivity sheets are static values computed by tools/fin_engine.py (Python mirror) at build time;",
             "re-run tools/build_fin_model.py after changing the JSON to refresh them. Staff trigger types are structural.",
             "Evidence levels: A direct / B strong documentation / C industry / D proxy / E assumption (see EVIDENCE_STANDARDS.md).",
             "", "Key evidence and caveats:"] + [f"• {n}" for n in a.get("evidence_notes", [])]
    for i, t in enumerate(lines, 1):
        ws.cell(row=i, column=1, value=t)
    ws["A1"].font = Font(bold=True, size=14); ws.column_dimensions["A"].width = 140
    # ---------------- Assumptions
    wa = wb.create_sheet("Assumptions")
    wa["A1"] = f"Assumptions — {a['name']}"; wa["A1"].font = Font(bold=True, size=13)
    hdr(wa, 3, ["Key", "Driver", "Unit", "Conservative", "Base", "Optimistic", "Evidence", "Source / rationale"])
    arow = {}
    for i, (k, lab, unit, dflt) in enumerate(E.DRIVERS):
        r = 4 + i; arow[k] = r
        wa.cell(row=r, column=1, value=k); wa.cell(row=r, column=2, value=lab); wa.cell(row=r, column=3, value=unit)
        for j, s in enumerate(E.SCEN):
            c = wa.cell(row=r, column=4 + j, value=E.get(a, k, s)); c.fill = INPUT
            if k in PCT_KEYS:
                c.number_format = "0.0%"
            elif unit.startswith("$"):
                c.number_format = "#,##0"
        wa.cell(row=r, column=7, value=a["drivers"].get(f"{k}__evidence", "E" if k in a["drivers"] else "default"))
        wa.cell(row=r, column=8, value=a["drivers"].get(f"{k}__source", "" if k in a["drivers"] else "engine default (not researched)"))
    for col, wdt in zip("ABCDEFGH", [30, 70, 9, 13, 13, 13, 9, 90]):
        wa.column_dimensions[col].width = wdt
    wa.freeze_panes = "D4"
    A = lambda k, s: f"Assumptions!${SC_COL[s]}${arow[k]}"
    # ---------------- Staff
    wsf = wb.create_sheet("Staff")
    hdr(wsf, 3, ["Role", "Trigger", "Threshold", "Per (capacity)", "Start month", "Count (month trigger)", "Max count",
                 "Capex per hire", "Sales rep (1/0)", "Annual raise", "Monthly loaded cost — Cons", "Base", "Opt", "Notes / evidence"])
    srow = []
    for i, s in enumerate(a.get("staff", [])):
        r = 4 + i; srow.append(r)
        vals = [s["role"], s.get("trigger", "month"), s.get("threshold", 0), s.get("per", 1), s.get("start_month", 1),
                s.get("count", 1), s.get("max_count"), s.get("capex_per_hire", 0), 1 if s.get("is_sales_rep") else 0,
                s.get("annual_raise_pct", 0.03), E.sval(s["monthly_cost"], "conservative"), E.sval(s["monthly_cost"], "base"),
                E.sval(s["monthly_cost"], "optimistic"), s.get("notes", "")]
        for j, v in enumerate(vals, 1):
            c = wsf.cell(row=r, column=j, value=v)
            if 3 <= j <= 13 and j != 9:
                c.fill = INPUT
    wsf.column_dimensions["A"].width = 34; wsf.column_dimensions["N"].width = 80
    STAFF_COST_COL = {"conservative": "K", "base": "L", "optimistic": "M"}
    # ---------------- Overhead
    wo = wb.create_sheet("Overhead")
    hdr(wo, 3, ["Item", "Start month", "Monthly — Cons", "Base", "Opt", "Annual growth", "AI/software (1/0)", "Notes / evidence"])
    orow = []
    for i, it in enumerate(a.get("overhead", [])):
        r = 4 + i; orow.append(r)
        vals = [it["item"], it.get("start_month", 1), E.sval(it["monthly"], "conservative"), E.sval(it["monthly"], "base"),
                E.sval(it["monthly"], "optimistic"), it.get("annual_growth_pct", 0.03), 1 if it.get("is_ai") else 0, it.get("notes", "")]
        for j, v in enumerate(vals, 1):
            c = wo.cell(row=r, column=j, value=v)
            if 2 <= j <= 6:
                c.fill = INPUT
    wo.column_dimensions["A"].width = 40; wo.column_dimensions["H"].width = 80
    OH_COL = {"conservative": "C", "base": "D", "optimistic": "E"}
    # ---------------- Capex
    wc = wb.create_sheet("Capex")
    hdr(wc, 3, ["Item", "Month", "Amount — Cons", "Base", "Opt", "Notes / evidence"])
    cx = a.get("capex", [])
    for i, it in enumerate(cx):
        r = 4 + i
        vals = [it["item"], it.get("month", 1), E.sval(it["amount"], "conservative"), E.sval(it["amount"], "base"),
                E.sval(it["amount"], "optimistic"), it.get("notes", "")]
        for j, v in enumerate(vals, 1):
            c = wc.cell(row=r, column=j, value=v)
            if 2 <= j <= 5:
                c.fill = INPUT
    wc.column_dimensions["A"].width = 40; wc.column_dimensions["F"].width = 80
    CX_COL = {"conservative": "C", "base": "D", "optimistic": "E"}
    cx_last = 3 + max(1, len(cx))
    # ---------------- Monthly scenario sheets
    rowmaps = {}
    for s in E.SCEN:
        wm = wb.create_sheet(SHEET[s])
        R = {}
        rows = []  # (key, label, formula_fn or None for section, is_stock)
        staff = a.get("staff", [])

        def add(key, label, fn=None, stock=False, fmt="#,##0"):
            rows.append((key, label, fn, stock, fmt))
        add("_s1", "CUSTOMER ACQUISITION")
        add("ramp", "Founder selling ramp factor", lambda X, W: f"=IF({X}$2<={A('sales_start_delay_months',s)}+{A('sales_cycle_months',s)},0,MIN(1,({X}$2-{A('sales_start_delay_months',s)}-{A('sales_cycle_months',s)})/MAX(1,{A('founder_ramp_months',s)})))", fmt="0.00")
        add("founder_new", "New customers — founder pipeline", lambda X, W: f"={X}{R['ramp']}*{A('founder_leads_per_month',s)}*{A('lead_to_proposal_pct',s)}*{A('proposal_to_win_pct',s)}*{A('demand_multiplier',s)}", fmt="0.0")
        for i, st in enumerate(staff):
            r = srow[i]
            thr = f"Staff!$C${r}*{A('staff_threshold_multiplier',s)}"
            per = f"MAX(0.000000001,Staff!$D${r}*{A('staff_threshold_multiplier',s)})"
            trig = st.get("trigger", "month")
            def fn(X, W, r=r, thr=thr, per=per, trig=trig, st=st):
                if trig == "month":
                    core = f"IF({X}$2>=Staff!$E${r},Staff!$F${r},0)"
                elif trig == "active_customers":
                    core = f"IF(AND({X}$2>=Staff!$E${r},{W}{R['active']}>={thr}),INT(({W}{R['active']}-{thr})/{per})+1,0)"
                else:
                    core = f"IF(AND({X}$2>=Staff!$E${r},{W}{R['revenue']}>={thr}),INT(({W}{R['revenue']}-{thr})/{per})+1,0)"
                if st.get("max_count") is not None:
                    core = f"MIN({core},Staff!$G${r})"
                return "=" + core
            add(f"hc{i}", f"Headcount — {st['role']}", fn, stock=True, fmt="0")
        rep_idx = [i for i, st in enumerate(staff) if st.get("is_sales_rep")]
        add("rep_count", "Sales reps employed", (lambda X, W: "=" + ("+".join(f"{X}{R[f'hc{i}']}" for i in rep_idx) if rep_idx else "0")), fmt="0")
        add("productive_reps", "Productive sales reps (hired ≥ ramp months ago)", lambda X, W: f"=IF({X}$2-INT({A('rep_ramp_months',s)})>=1,INDEX(${FIRST}${R['rep_count']}:${LAST}${R['rep_count']},1,{X}$2-INT({A('rep_ramp_months',s)})),0)", fmt="0")
        add("rep_new", "New customers — sales reps", lambda X, W: f"={X}{R['productive_reps']}*{A('rep_new_customers_per_month',s)}*{A('demand_multiplier',s)}", fmt="0.0")
        add("referral_new", "New customers — referrals/inbound", lambda X, W: f"={W}{R['active']}/100*{A('referral_new_per_100_active',s)}*{A('demand_multiplier',s)}", fmt="0.0")
        add("new", "New customers — total", lambda X, W: f"={X}{R['founder_new']}+{X}{R['rep_new']}+{X}{R['referral_new']}", fmt="0.0")
        add("churned", "Customers lost", lambda X, W: f"={W}{R['active']}*{A('monthly_churn_pct',s)}*{A('churn_multiplier',s)}+IF({X}$2={A('shock_month',s)},{W}{R['active']}*{A('shock_loss_pct',s)},0)", fmt="0.0")
        add("active", "Active customers (end of month)", lambda X, W: f"={W}{R['active']}+{X}{R['new']}-{X}{R['churned']}", stock=True, fmt="0.0")
        add("_s2", "REVENUE AND GROSS PROFIT")
        add("price_index", "Price index", lambda X, W: f"=(1+{A('arpc_annual_growth_pct',s)})^({X}$3-1)", fmt="0.000")
        add("rev_rec", "Recurring revenue", lambda X, W: f"={X}{R['active']}*{A('arpc_monthly',s)}*{X}{R['price_index']}")
        add("rev_one", "One-time revenue", lambda X, W: f"={X}{R['new']}*{A('onetime_revenue_per_new_customer',s)}*{X}{R['price_index']}")
        add("revenue", "TOTAL REVENUE", lambda X, W: f"={X}{R['rev_rec']}+{X}{R['rev_one']}", stock=True)
        add("cogs", "Cost of goods / direct cost of service", lambda X, W: f"={X}{R['rev_rec']}*(1-{A('gross_margin_pct',s)})+{X}{R['rev_one']}*(1-{A('onetime_gross_margin_pct',s)})")
        add("gp", "GROSS PROFIT", lambda X, W: f"={X}{R['revenue']}-{X}{R['cogs']}")
        add("gm", "Gross margin %", lambda X, W: f"=IF({X}{R['revenue']}>0,{X}{R['gp']}/{X}{R['revenue']},0)", fmt="0.0%")
        add("var_opex", "Variable operating expense", lambda X, W: f"={X}{R['revenue']}*{A('variable_opex_pct_revenue',s)}")
        add("acq", "Customer acquisition cost (variable + fixed marketing)", lambda X, W: f"={X}{R['new']}*{A('cac_per_new_customer',s)}+{A('fixed_marketing_per_month',s)}")
        add("contribution", "CONTRIBUTION PROFIT", lambda X, W: f"={X}{R['gp']}-{X}{R['var_opex']}-{X}{R['acq']}")
        add("_s3", "STAFF AND OVERHEAD")
        for i, st in enumerate(staff):
            r = srow[i]
            add(f"sc{i}", f"Staff cost — {st['role']}", (lambda X, W, i=i, r=r: f"={X}{R[f'hc{i}']}*Staff!${STAFF_COST_COL[s]}${r}*(1+Staff!$J${r})^({X}$3-1)*{A('labor_cost_multiplier',s)}"))
        add("staff_cost", "Total staff cost", lambda X, W: "=" + ("+".join(f"{X}{R[f'sc{i}']}" for i in range(len(staff))) if staff else "0"))
        for i, it in enumerate(a.get("overhead", [])):
            r = orow[i]; mult = 'ai_cost_multiplier' if it.get("is_ai") else 'overhead_multiplier'
            add(f"oh{i}", f"Overhead — {it['item']}", (lambda X, W, r=r, mult=mult: f"=IF({X}$2>=Overhead!$B${r},Overhead!${OH_COL[s]}${r}*(1+Overhead!$F${r})^({X}$3-1)*{A(mult,s)},0)"))
        nOH = len(a.get("overhead", []))
        add("overhead", "Total overhead", lambda X, W: "=" + ("+".join(f"{X}{R[f'oh{i}']}" for i in range(nOH)) if nOH else "0"))
        add("op", "OPERATING PROFIT (EBITDA basis, before owner compensation)", lambda X, W: f"={X}{R['contribution']}-{X}{R['staff_cost']}-{X}{R['overhead']}")
        add("_s4", "CASH FLOW")
        add("capex_items", "Capex — planned items", lambda X, W: f"=SUMPRODUCT((Capex!$B$4:$B${cx_last}={X}$2)*Capex!${CX_COL[s]}$4:${CX_COL[s]}${cx_last})")
        add("capex_hire", "Capex — per new hire (vehicles, tools)", lambda X, W: "=" + ("+".join(f"MAX(0,{X}{R[f'hc{i}']}-{W}{R[f'hc{i}']})*Staff!$H${srow[i]}" for i in range(len(staff))) if staff else "0"))
        add("capex", "Total capex", lambda X, W: f"={X}{R['capex_items']}+{X}{R['capex_hire']}")
        add("ar", "Accounts receivable", lambda X, W: f"={X}{R['revenue']}*{A('dso_days',s)}/30", stock=True)
        add("inv", "Inventory", lambda X, W: f"={X}{R['cogs']}*{A('inventory_days_cogs',s)}/30", stock=True)
        add("ap", "Accounts payable", lambda X, W: f"={X}{R['cogs']}*{A('dpo_days',s)}/30", stock=True)
        add("nwc", "Net working capital", lambda X, W: f"={X}{R['ar']}+{X}{R['inv']}-{X}{R['ap']}", stock=True)
        add("dnwc", "Increase in working capital", lambda X, W: f"={X}{R['nwc']}-{W}{R['nwc']}")
        add("draw", "Owner draw / compensation", lambda X, W: f"=IF({X}$2>={A('founder_draw_start_month',s)},{A('founder_draw_per_month',s)},0)")
        add("cum_taxable", "Cumulative taxable profit after owner draw", lambda X, W: f"={W}{R['cum_taxable']}+{X}{R['op']}-{X}{R['draw']}", stock=True)
        add("tax", "Income taxes (simplified, loss-aware)", lambda X, W: f"={A('tax_rate_pct',s)}*MAX(0,{X}{R['cum_taxable']})-{A('tax_rate_pct',s)}*MAX(0,{W}{R['cum_taxable']})")
        add("fcf", "FREE CASH FLOW (before owner draw)", lambda X, W: f"={X}{R['op']}-{X}{R['tax']}-{X}{R['capex']}-{X}{R['dnwc']}")
        add("retained", "Cash retained after owner draw", lambda X, W: f"={X}{R['fcf']}-{X}{R['draw']}")
        add("cum_retained", "Cumulative retained cash (excl. owner injection)", lambda X, W: f"={W}{R['cum_retained']}+{X}{R['retained']}", stock=True)
        add("cash", "Cash balance (incl. owner injection)", lambda X, W: f"={A('start_capital_injection',s)}+{X}{R['cum_retained']}", stock=True)
        add("_s5", "HELPERS")
        add("be", "First month of positive operating profit (0 = not yet)", lambda X, W: f"=IF({W}{R['be']}>0,{W}{R['be']},IF({X}{R['op']}>0,{X}$2,0))", stock=True, fmt="0")
        add("pb", "Payback month (cumulative retained cash back to ≥ 0)", lambda X, W: f"=IF({W}{R['pb']}>0,{W}{R['pb']},IF(AND(MIN(${FIRST}{R['cum_retained']}:{X}{R['cum_retained']})<0,{X}{R['cum_retained']}>=0),{X}$2,0))", stock=True, fmt="0")
        for lab, thr in [("1k", 1000), ("5k", 5000), ("10k", 10000), ("25k", 25000)]:
            add(f"ms{lab}", f"First month operating profit ≥ ${thr:,}", (lambda X, W, lab=lab, thr=thr: f"=IF({W}{R[f'ms{lab}']}>0,{W}{R[f'ms{lab}']},IF({X}{R['op']}>={thr},{X}$2,0))"), stock=True, fmt="0")
        # assign rows
        for idx, (key, *_rest) in enumerate(rows):
            R[key] = 5 + idx
        wm["A1"] = f"{a['name']} — {s.upper()} scenario (monthly, 60 months)"; wm["A1"].font = Font(bold=True, size=13)
        wm["A2"] = "Month"; wm["A3"] = "Year"; wm["B2"] = 0; wm["B3"] = 0; wm["B4"] = "M0 (opening)"
        for m in range(1, M + 1):
            X = L(m + 2)
            wm[f"{X}2"] = m; wm[f"{X}3"] = f"=INT(({X}2-1)/12)+1"
            wm[f"{X}2"].font = BOLD
        for key, label, fn, stock, fmt in rows:
            r = R[key]
            c = wm.cell(row=r, column=1, value=label)
            if fn is None:
                c.font = BOLD; c.fill = SECTION
                continue
            if label.isupper() or label.startswith(("TOTAL", "GROSS", "CONTRIB", "OPERATING", "FREE")):
                c.font = BOLD
            wm.cell(row=r, column=2, value=0)
            for m in range(1, M + 1):
                X, W = L(m + 2), L(m + 1)
                cell = wm.cell(row=r, column=m + 2, value=fn(X, W)); cell.number_format = fmt
        wm.column_dimensions["A"].width = 58; wm.freeze_panes = "C5"
        rowmaps[s] = dict(R)
    # ---------------- Annual
    wy = wb.create_sheet("Annual")
    wy["A1"] = "Annual summary (years 1–5) — all scenarios, live formulas"; wy["A1"].font = Font(bold=True, size=13)
    flows = [("revenue", "Revenue"), ("gp", "Gross profit"), ("contribution", "Contribution profit"),
             ("staff_cost", "Staff cost"), ("overhead", "Overhead"), ("op", "Operating profit (pre-owner comp)"),
             ("tax", "Income taxes"), ("capex", "Capex"), ("dnwc", "Increase in working capital"),
             ("fcf", "Free cash flow (pre-owner draw)"), ("draw", "Owner draw"), ("retained", "Retained cash after draw"),
             ("new", "New customers")]
    stocks = [("active", "Active customers (year end)"), ("cash", "Cash balance (year end)"), ("nwc", "Net working capital (year end)")]
    yrow = {}
    r = 3
    for s in E.SCEN:
        N = SHEET[s]; R = rowmaps[s]
        wy.cell(row=r, column=1, value=s.upper()).font = BOLD
        for y in range(1, 6):
            wy.cell(row=r, column=1 + y, value=f"Year {y}").font = BOLD
        r += 1
        for key, lab in flows:
            wy.cell(row=r, column=1, value=lab)
            for y in range(1, 6):
                c = wy.cell(row=r, column=1 + y, value=f"=SUMIF({N}!${FIRST}$3:${LAST}$3,{y},{N}!${FIRST}${R[key]}:${LAST}${R[key]})")
                c.number_format = "#,##0"
            yrow[(s, key)] = r; r += 1
        for key, lab in stocks:
            wy.cell(row=r, column=1, value=lab)
            for y in range(1, 6):
                c = wy.cell(row=r, column=1 + y, value=f"=INDEX({N}!${FIRST}${R[key]}:${LAST}${R[key]},1,{12*y})")
                c.number_format = "#,##0"
            yrow[(s, key)] = r; r += 1
        wy.cell(row=r, column=1, value="Headcount (year end)")
        for y in range(1, 6):
            parts = [f"INDEX({N}!${FIRST}${R[f'hc{i}']}:${LAST}${R[f'hc{i}']},1,{12*y})" for i in range(len(a.get('staff', [])))]
            wy.cell(row=r, column=1 + y, value="=" + ("+".join(parts) if parts else "0"))
        yrow[(s, "headcount")] = r; r += 2
    wy.column_dimensions["A"].width = 40
    # ---------------- Long term (10 years)
    wl = wb.create_sheet("LongTerm_10yr")
    wl["A1"] = "Capital accumulation — years 1–10 (years 1–5 from monthly model; 6–10 extrapolated with decaying growth)"
    wl["A1"].font = Font(bold=True, size=13)
    ltrow = {}
    r = 3
    for s in E.SCEN:
        wl.cell(row=r, column=1, value=s.upper()).font = BOLD
        for y in range(1, 11):
            wl.cell(row=r, column=1 + y, value=f"Year {y}").font = BOLD
        r += 1
        keys = ["growth", "op", "owner_comp", "tax", "maint_capex", "growth_reinvest", "distributable", "cash_costs",
                "reserve_target", "delta_reserve", "deployable", "cum_deployable", "ev"]
        labels = {"growth": "Operating-profit growth (yrs 6–10)", "op": "Operating profit (pre-owner comp)",
                  "owner_comp": "Owner / manager compensation", "tax": "Income taxes",
                  "maint_capex": "Maintenance capex", "growth_reinvest": "Growth reinvestment (capex + working capital)",
                  "distributable": "Distributable cash after reinvestment", "cash_costs": "Cash operating costs",
                  "reserve_target": "Cash reserve target", "delta_reserve": "Reserve build (−release)",
                  "deployable": "Deployable surplus capital", "cum_deployable": "Cumulative deployable capital (positive years)",
                  "ev": "Indicative enterprise value (op profit × multiple)"}
        rr = {k: r + i for i, k in enumerate(keys)}
        for k in keys:
            wl.cell(row=rr[k], column=1, value=labels[k])
        for y in range(1, 11):
            C, P = L(1 + y), L(y)
            if y <= 5:
                f = {"growth": "",
                     "op": f"=Annual!{C}{yrow[(s,'op')]}",
                     "owner_comp": f"=Annual!{C}{yrow[(s,'draw')]}",
                     "tax": f"=Annual!{C}{yrow[(s,'tax')]}",
                     "maint_capex": "=0",
                     "growth_reinvest": f"=Annual!{C}{yrow[(s,'capex')]}+Annual!{C}{yrow[(s,'dnwc')]}",
                     "cash_costs": f"=Annual!{C}{yrow[(s,'revenue')]}-Annual!{C}{yrow[(s,'op')]}"}
            else:
                f = {"growth": f"={A('lt_growth_y6_pct',s)}*{A('lt_growth_decay',s)}^({y}-6)",
                     "op": f"={P}{rr['op']}*(1+{C}{rr['growth']})",
                     "owner_comp": f"={P}{rr['owner_comp']}*(1+{A('owner_comp_growth_pct',s)})",
                     "tax": f"={A('tax_rate_pct',s)}*MAX(0,{C}{rr['op']}-{C}{rr['owner_comp']})",
                     "maint_capex": f"={A('maint_capex_pct_op',s)}*MAX(0,{C}{rr['op']})",
                     "growth_reinvest": f"=MAX(0,{C}{rr['op']}-{P}{rr['op']})/MAX(0.000000001,{A('incremental_roic_pct',s)})",
                     "cash_costs": f"={P}{rr['cash_costs']}*(1+{C}{rr['growth']})"}
            f["distributable"] = f"={C}{rr['op']}-{C}{rr['owner_comp']}-{C}{rr['tax']}-{C}{rr['maint_capex']}-{C}{rr['growth_reinvest']}"
            f["reserve_target"] = f"={A('reserve_months',s)}*{C}{rr['cash_costs']}/12"
            f["delta_reserve"] = f"={C}{rr['reserve_target']}" + (f"-{P}{rr['reserve_target']}" if y > 1 else "")
            f["deployable"] = f"={C}{rr['distributable']}-{C}{rr['delta_reserve']}"
            f["cum_deployable"] = (f"={P}{rr['cum_deployable']}+" if y > 1 else "=") + f"MAX(0,{C}{rr['deployable']})"
            f["ev"] = f"={C}{rr['op']}*{A('ev_multiple',s)}"
            for k in keys:
                if f.get(k):
                    c = wl.cell(row=rr[k], column=1 + y, value=f[k])
                    c.number_format = "0.0%" if k == "growth" else "#,##0"
        ltrow[s] = rr
        r += len(keys) + 2
    wl.column_dimensions["A"].width = 48
    # ---------------- Summary
    wsu = wb.create_sheet("Summary", 1)
    wsu["A1"] = f"Summary — {a['name']}"; wsu["A1"].font = Font(bold=True, size=14)
    hdr(wsu, 3, ["Metric", "Conservative", "Base", "Optimistic"])
    metrics = []
    for y in (1, 2, 3, 5):
        metrics.append((f"Year {y} revenue", lambda s, y=y: f"=Annual!{L(1+y)}{yrow[(s,'revenue')]}", "#,##0"))
    for y in (1, 2, 3, 5):
        metrics.append((f"Year {y} operating profit (pre-owner comp)", lambda s, y=y: f"=Annual!{L(1+y)}{yrow[(s,'op')]}", "#,##0"))
    for y in (1, 2, 3, 5):
        metrics.append((f"Year {y} free cash flow (pre-owner draw)", lambda s, y=y: f"=Annual!{L(1+y)}{yrow[(s,'fcf')]}", "#,##0"))
    metrics += [
        ("Year 3 operating margin", lambda s: f"=IF(Annual!D{yrow[(s,'revenue')]}>0,Annual!D{yrow[(s,'op')]}/Annual!D{yrow[(s,'revenue')]},0)", "0.0%"),
        ("Active customers end of year 1", lambda s: f"=Annual!B{yrow[(s,'active')]}", "#,##0"),
        ("Active customers end of year 2", lambda s: f"=Annual!C{yrow[(s,'active')]}", "#,##0"),
        ("Active customers end of year 5", lambda s: f"=Annual!F{yrow[(s,'active')]}", "#,##0"),
        ("Headcount end of year 5 (excl. founder)", lambda s: f"=Annual!F{yrow[(s,'headcount')]}", "0"),
        ("First month of positive operating profit (0 = none in 60 mo)", lambda s: f"={SHEET[s]}!{LAST}{rowmaps[s]['be']}", "0"),
        ("First month op profit ≥ $1k", lambda s: f"={SHEET[s]}!{LAST}{rowmaps[s]['ms1k']}", "0"),
        ("First month op profit ≥ $5k", lambda s: f"={SHEET[s]}!{LAST}{rowmaps[s]['ms5k']}", "0"),
        ("First month op profit ≥ $10k", lambda s: f"={SHEET[s]}!{LAST}{rowmaps[s]['ms10k']}", "0"),
        ("First month op profit ≥ $25k", lambda s: f"={SHEET[s]}!{LAST}{rowmaps[s]['ms25k']}", "0"),
        ("Peak funding need (max cumulative cash deficit)", lambda s: f"=-MIN(0,MIN({SHEET[s]}!{FIRST}{rowmaps[s]['cum_retained']}:{LAST}{rowmaps[s]['cum_retained']}))", "#,##0"),
        ("Minimum cash balance (with owner injection)", lambda s: f"=MIN({SHEET[s]}!{FIRST}{rowmaps[s]['cash']}:{LAST}{rowmaps[s]['cash']})", "#,##0"),
        ("Payback month of cumulative deficit (0 = never negative or not repaid)", lambda s: f"={SHEET[s]}!{LAST}{rowmaps[s]['pb']}", "0"),
        ("Year-3 operating profit ÷ peak funding need", lambda s: f"=IF(-MIN(0,MIN({SHEET[s]}!{FIRST}{rowmaps[s]['cum_retained']}:{LAST}{rowmaps[s]['cum_retained']}))>1,Annual!D{yrow[(s,'op')]}/(-MIN(0,MIN({SHEET[s]}!{FIRST}{rowmaps[s]['cum_retained']}:{LAST}{rowmaps[s]['cum_retained']})))),\"self-funding\")", '0.0"x"'),
        ("Cumulative owner draw, years 1–5", lambda s: "=" + "+".join(f"Annual!{L(1+y)}{yrow[(s,'draw')]}" for y in range(1, 6)), "#,##0"),
        ("Cumulative deployable capital by year 5", lambda s: f"=LongTerm_10yr!F{ltrow[s]['cum_deployable']}", "#,##0"),
        ("Cumulative deployable capital by year 10", lambda s: f"=LongTerm_10yr!K{ltrow[s]['cum_deployable']}", "#,##0"),
        ("Year-10 operating profit", lambda s: f"=LongTerm_10yr!K{ltrow[s]['op']}", "#,##0"),
        ("Indicative enterprise value, year 5", lambda s: f"=LongTerm_10yr!F{ltrow[s]['ev']}", "#,##0"),
        ("Indicative enterprise value, year 10", lambda s: f"=LongTerm_10yr!K{ltrow[s]['ev']}", "#,##0"),
    ]
    for i, (lab, fn, fmt) in enumerate(metrics):
        rr_ = 4 + i
        wsu.cell(row=rr_, column=1, value=lab)
        for j, s in enumerate(E.SCEN):
            c = wsu.cell(row=rr_, column=2 + j, value=fn(s)); c.number_format = fmt
    wsu.column_dimensions["A"].width = 66
    for col in "BCD":
        wsu.column_dimensions[col].width = 16
    # ---------------- Stress + sensitivity (static, from Python mirror)
    st = E.stress(a)
    wst = wb.create_sheet("Stress")
    wst["A1"] = "Stress tests on the BASE scenario (static values computed by tools/fin_engine.py at build time)"
    wst["A1"].font = Font(bold=True, size=13)
    cols = ["test", "y1_revenue", "y1_op", "y2_op", "y3_op", "y5_op", "y3_fcf", "breakeven_month", "peak_funding_need",
            "payback_month", "y5_active_end", "lt_y10_cum_deployable"]
    hdr(wst, 3, ["Stress test", "Y1 revenue", "Y1 op profit", "Y2 op profit", "Y3 op profit", "Y5 op profit", "Y3 FCF",
                 "Breakeven month", "Peak funding need", "Payback month", "Active cust. Y5", "10-yr cum. deployable"])
    for i, row in enumerate(st):
        for j, k in enumerate(cols):
            c = wst.cell(row=4 + i, column=1 + j, value=round(row[k], 0) if isinstance(row[k], float) else row[k])
            if j:
                c.number_format = "#,##0"
    wst.column_dimensions["A"].width = 60
    tor = E.tornado(a)
    wt = wb.create_sheet("Sensitivity")
    wt["A1"] = "One-at-a-time sensitivity: each driver ×0.75 and ×1.25 on the BASE scenario (static values)"
    wt["A1"].font = Font(bold=True, size=13)
    hdr(wt, 3, ["Driver", "Base value", "Y3 op profit @ ×0.75", "Y3 op profit @ ×1.25", "Peak funding @ ×0.75",
                "Peak funding @ ×1.25", "5-yr retained cash @ ×0.75", "5-yr retained cash @ ×1.25"])
    for i, row in enumerate(tor):
        vals = [row["driver"], row["base_value"], row["y3_op_low"], row["y3_op_high"], row["peak_funding_low"],
                row["peak_funding_high"], row["y5_cum_retained_low"], row["y5_cum_retained_high"]]
        for j, v in enumerate(vals):
            c = wt.cell(row=4 + i, column=1 + j, value=round(v, 4) if isinstance(v, float) else v)
            if j >= 2:
                c.number_format = "#,##0"
    wt.column_dimensions["A"].width = 36
    # ---------------- Unit economics
    tx = a.get("transactions", [])
    if tx:
        wu = wb.create_sheet("UnitEconomics", 2)
        wu["A1"] = "Representative transactions (contribution after direct costs)"; wu["A1"].font = Font(bold=True, size=13)
        r = 3
        for t in tx:
            wu.cell(row=r, column=1, value=t["name"]).font = BOLD
            wu.cell(row=r, column=3, value=f"Evidence: {t.get('evidence','E')}")
            r += 1
            wu.cell(row=r, column=1, value="Revenue"); c = wu.cell(row=r, column=2, value=t["revenue"]); c.fill = INPUT; c.number_format = "#,##0.00"
            rev_r = r; r += 1
            first = r
            for ln in t.get("lines", []):
                wu.cell(row=r, column=1, value=f"  less: {ln['item']}")
                c = wu.cell(row=r, column=2, value=ln["amount"]); c.fill = INPUT; c.number_format = "#,##0.00"
                if ln.get("note"):
                    wu.cell(row=r, column=3, value=ln["note"])
                r += 1
            wu.cell(row=r, column=1, value="Contribution").font = BOLD
            wu.cell(row=r, column=2, value=f"=B{rev_r}-SUM(B{first}:B{max(first, r-1)})" if r > first else f"=B{rev_r}").number_format = "#,##0.00"
            r += 1
            wu.cell(row=r, column=1, value="Contribution margin")
            wu.cell(row=r, column=2, value=f"=IF(B{rev_r}>0,B{r-1}/B{rev_r},0)").number_format = "0.0%"
            r += 1
            if t.get("notes"):
                wu.cell(row=r, column=1, value=t["notes"]); r += 1
            r += 1
        wu.column_dimensions["A"].width = 60; wu.column_dimensions["C"].width = 90
    out = FM / f"{oid}_model.xlsx"
    wb.save(out)
    # results JSON (python mirror)
    res = {"id": oid, "name": a["name"], "scenarios": {}, "stress": st, "tornado": tor}
    for s in E.SCEN:
        S = E.run(a, s)["summary"]
        res["scenarios"][s] = {k: v for k, v in S.items()}
    (FM / f"{oid}_results.json").write_text(json.dumps(res, indent=1, default=float))
    print(f"built {out.name}")
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        args = [str(p) for p in sorted(FM.glob("*_assumptions.json")) if not p.name.startswith("TEMPLATE")]
    for p in args:
        build(p)
