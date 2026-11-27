"""Build business/FINANCIAL_MODEL.xlsx — formula-driven 5-year model (2027–2031).

Every input is on the 'Inputs' sheet with an evidence label ([V], [AE], [HYP]). Two structures:
  * Bootstrapped services lab (lean, hire against revenue)
  * Venture-backed platform (seed raise, earlier hires, expansion modules from year 3)
Three scenarios each: Conservative / Base / Optimistic. Outputs use Excel formulas only.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, Reference

YEARS = [2027, 2028, 2029, 2030, 2031]
SC = ["Conservative", "Base", "Optimistic"]
BLUE = Font(color="1F4E79")
HDR = PatternFill("solid", fgColor="DCE6F1")
INP = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="BBBBBB")

# name -> (unit, label, {structure: {scenario: value or [5 yearly values]}})
def S(c, b, o):
    return {"Conservative": c, "Base": b, "Optimistic": o}

INPUTS = {
    "Bootstrapped": {
        "Study customers (paying, cumulative active)": ("#", "[HYP]", S([1, 4, 7, 10, 13], [2, 6, 11, 16, 22], [3, 9, 17, 26, 36])),
        "Studies per customer per year": ("#", "[AE] BVF firms 0.5–3/yr", S(1.2, 1.5, 2.0)),
        "Blended price per study": ("$", "[HYP] playbook $12K non-GLP/$25K GLP", S(9000, 14600, 18000)),
        "Academic subscriptions": ("#", "[HYP]", S([0, 2, 5, 9, 13], [1, 5, 12, 20, 30], [3, 10, 22, 36, 50])),
        "Academic price per year": ("$", "[HYP] playbook $4K", S(3000, 4000, 5000)),
        "CRO enterprise licences": ("#", "[HYP]", S([0, 0, 0, 1, 1], [0, 0, 1, 2, 3], [0, 1, 2, 4, 6])),
        "CRO licence price per year": ("$", "[HYP] playbook $40K", S(30000, 40000, 50000)),
        "Expansion-module revenue share of core": ("%", "[HYP] osseointegration/spine/histology", S([0, 0, 0, 0, 0], [0, 0, 0, 0.05, 0.1], [0, 0, 0.05, 0.1, 0.15])),
        "Analyst hours per study": ("h", "[AE] intake, QC, ROI, material labels, review, statistics, report, client calls; falls as models generalise", S([110, 95, 80, 70, 60], [85, 70, 55, 45, 38], [65, 50, 40, 32, 26])),
        "Loaded analyst cost per hour": ("$", "[AE]", S(60, 55, 55)),
        "Compute + storage per study": ("$", "[AE] cloud GPU hours + storage", S(250, 150, 120)),
        "Validation & QA spend": ("$", "[AE] phantoms Y1; CSV package Y2–3; audits", S([12000, 40000, 60000, 30000, 30000], [15000, 60000, 80000, 40000, 40000], [20000, 80000, 100000, 50000, 50000])),
        "Founder & staff salaries": ("$", "[AE] stipend → salaries as revenue allows", S([0, 30000, 90000, 160000, 230000], [12000, 60000, 140000, 240000, 330000], [24000, 90000, 200000, 330000, 450000])),
        "Other opex (legal, IP, insurance, software, travel)": ("$", "[AE]", S([20000, 30000, 40000, 50000, 60000], [25000, 40000, 55000, 70000, 85000], [30000, 50000, 70000, 90000, 110000])),
        "Customer acquisition cost per new customer": ("$", "[AE] travel, conferences, pilots", S(6000, 5000, 4000)),
        "Non-dilutive grants & prizes received": ("$", "[HYP] Cozad/I-Corps/SBIR (see grants/)", S([10000, 50000, 0, 0, 0], [25000, 150000, 150000, 0, 0], [50000, 305000, 300000, 0, 0])),
    },
    "Venture": {
        "Study customers (paying, cumulative active)": ("#", "[HYP]", S([2, 6, 12, 20, 30], [3, 10, 22, 38, 58], [5, 15, 35, 60, 95])),
        "Studies per customer per year": ("#", "[AE]", S(1.3, 1.7, 2.2)),
        "Blended price per study": ("$", "[HYP]", S(10000, 15000, 19000)),
        "Academic subscriptions": ("#", "[HYP]", S([1, 5, 12, 22, 35], [3, 12, 30, 55, 85], [5, 20, 50, 90, 140])),
        "Academic price per year": ("$", "[HYP]", S(3000, 4000, 5000)),
        "CRO enterprise licences": ("#", "[HYP]", S([0, 0, 1, 2, 4], [0, 1, 3, 6, 10], [0, 2, 5, 10, 16])),
        "CRO licence price per year": ("$", "[HYP]", S(35000, 45000, 60000)),
        "Expansion-module revenue share of core": ("%", "[HYP] modules launched from Y3", S([0, 0, 0.05, 0.15, 0.25], [0, 0, 0.1, 0.25, 0.4], [0, 0.05, 0.2, 0.4, 0.6])),
        "Analyst hours per study": ("h", "[AE] as bootstrapped, faster automation from platform investment", S([100, 80, 62, 50, 42], [80, 60, 45, 35, 28], [60, 45, 34, 26, 20])),
        "Loaded analyst cost per hour": ("$", "[AE]", S(60, 55, 55)),
        "Compute + storage per study": ("$", "[AE]", S(250, 150, 120)),
        "Validation & QA spend": ("$", "[AE]", S([30000, 120000, 150000, 120000, 120000], [40000, 150000, 200000, 150000, 150000], [50000, 180000, 250000, 200000, 200000])),
        "Founder & staff salaries": ("$", "[AE] 3–4 FTE Y2, 8–12 FTE Y4", S([150000, 450000, 750000, 1000000, 1250000], [200000, 600000, 1000000, 1400000, 1800000], [250000, 750000, 1300000, 1900000, 2500000])),
        "Other opex (legal, IP, insurance, software, travel)": ("$", "[AE]", S([60000, 120000, 180000, 240000, 300000], [80000, 150000, 220000, 300000, 380000], [100000, 180000, 260000, 360000, 460000])),
        "Customer acquisition cost per new customer": ("$", "[AE]", S(9000, 8000, 7000)),
        "Non-dilutive grants & prizes received": ("$", "[HYP]", S([25000, 305000, 300000, 0, 0], [50000, 305000, 1250000, 0, 0], [100000, 305000, 1250000, 0, 0])),
    },
}
ORDER = list(INPUTS["Bootstrapped"].keys())


def main(path="business/FINANCIAL_MODEL.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    notes = ["OsteoQuant 5-year financial model (2027–2031) — DRAFT, all revenue drivers are hypotheses.",
             "No customer interviews have been conducted. Prices are the founder playbook's unvalidated hypotheses.",
             "Yellow cells on 'Inputs' are editable; every other number is a formula.",
             "Market sanity check: the bottom-up serviceable pool for graft-defect reports at playbook prices is ≈$0.9M/$2.1M/$4.3M per year "
             "(business/MARKET_MODEL_INPUTS.md). Revenue above that requires CRO licences, academic subscriptions or expansion modules.",
             "Structures: 'Bootstrapped' = services-plus-software lab; 'Venture' = seed-funded platform with expansion modules.",
             "Outputs per structure × scenario: revenue lines, COGS, gross margin, opex, EBITDA, grants, cumulative cash before equity, "
             "and the equity funding requirement (= most negative cumulative cash)."]
    for i, n in enumerate(notes, 1):
        ws.cell(i, 1, n)
    ws.column_dimensions["A"].width = 140

    inp = wb.create_sheet("Inputs")
    inp.append(["Structure", "Parameter", "Unit", "Evidence", "Scenario"] + YEARS)
    for c in inp[1]:
        c.font = Font(bold=True); c.fill = HDR
    ref = {}  # (structure, scenario, param) -> row
    r = 2
    for st in ("Bootstrapped", "Venture"):
        for p in ORDER:
            unit, lab, vals = INPUTS[st][p]
            for sc in SC:
                v = vals[sc]
                yearly = v if isinstance(v, list) else [v] * 5
                inp.cell(r, 1, st); inp.cell(r, 2, p); inp.cell(r, 3, unit); inp.cell(r, 4, lab); inp.cell(r, 5, sc)
                for j, y in enumerate(yearly):
                    c = inp.cell(r, 6 + j, y)
                    c.fill = INP
                    c.number_format = "0%" if unit == "%" else ("#,##0" if unit in ("$", "#", "h") else "0.0")
                ref[(st, sc, p)] = r
                r += 1
    for col, w in zip("ABCDE", (14, 48, 6, 44, 13)):
        inp.column_dimensions[col].width = w

    for st in ("Bootstrapped", "Venture"):
        sh = wb.create_sheet(f"P&L {st}")
        row = 1
        summary_rows = {}
        for sc in SC:
            sh.cell(row, 1, f"{st} — {sc}").font = Font(bold=True, size=12, color="1F4E79")
            row += 1
            sh.cell(row, 1, "Line")
            for j, y in enumerate(YEARS):
                sh.cell(row, 2 + j, y)
            for c in sh[row]:
                c.font = Font(bold=True); c.fill = HDR
            row += 1
            I = lambda p, j: f"Inputs!{get_column_letter(6 + j)}{ref[(st, sc, p)]}"
            lines = {}

            def add(name, f, fmt="#,##0", bold=False):
                nonlocal row
                lines[name] = row
                sh.cell(row, 1, name).font = Font(bold=bold)
                for j in range(5):
                    c = sh.cell(row, 2 + j, "=" + f(j))
                    c.number_format = fmt
                    if bold:
                        c.font = Font(bold=True)
                lines[name] = row
                row += 1

            col = lambda name, j: f"{get_column_letter(2 + j)}{lines[name]}"
            add("Studies analysed", lambda j: f"{I('Study customers (paying, cumulative active)', j)}*{I('Studies per customer per year', j)}", "0.0")
            add("Study revenue", lambda j: f"{col('Studies analysed', j)}*{I('Blended price per study', j)}")
            add("Academic subscription revenue", lambda j: f"{I('Academic subscriptions', j)}*{I('Academic price per year', j)}")
            add("CRO licence revenue", lambda j: f"{I('CRO enterprise licences', j)}*{I('CRO licence price per year', j)}")
            add("Expansion-module revenue", lambda j: f"({col('Study revenue', j)}+{col('Academic subscription revenue', j)}+{col('CRO licence revenue', j)})*{I('Expansion-module revenue share of core', j)}")
            add("Total revenue", lambda j: "+".join(col(n, j) for n in ("Study revenue", "Academic subscription revenue", "CRO licence revenue", "Expansion-module revenue")), bold=True)
            add("Analyst labour (COGS)", lambda j: f"{col('Studies analysed', j)}*{I('Analyst hours per study', j)}*{I('Loaded analyst cost per hour', j)}")
            add("Compute & storage (COGS)", lambda j: f"{col('Studies analysed', j)}*{I('Compute + storage per study', j)}")
            add("Gross profit", lambda j: f"{col('Total revenue', j)}-{col('Analyst labour (COGS)', j)}-{col('Compute & storage (COGS)', j)}", bold=True)
            add("Gross margin %", lambda j: f"IF({col('Total revenue', j)}=0,0,{col('Gross profit', j)}/{col('Total revenue', j)})", "0%")
            add("Salaries", lambda j: I("Founder & staff salaries", j))
            add("Validation & QA", lambda j: I("Validation & QA spend", j))
            add("Other opex", lambda j: I("Other opex (legal, IP, insurance, software, travel)", j))
            prevcust = lambda j: "0" if j == 0 else I("Study customers (paying, cumulative active)", j - 1)
            add("Customer acquisition", lambda j: f"MAX(0,{I('Study customers (paying, cumulative active)', j)}-{prevcust(j)})*{I('Customer acquisition cost per new customer', j)}")
            add("EBITDA", lambda j: f"{col('Gross profit', j)}-{col('Salaries', j)}-{col('Validation & QA', j)}-{col('Other opex', j)}-{col('Customer acquisition', j)}", bold=True)
            add("Grants & prizes (non-dilutive)", lambda j: I("Non-dilutive grants & prizes received", j))
            add("Net cash flow before equity", lambda j: f"{col('EBITDA', j)}+{col('Grants & prizes (non-dilutive)', j)}", bold=True)
            add("Cumulative cash before equity", lambda j: col("Net cash flow before equity", 0) if j == 0 else f"{col('Cumulative cash before equity', j - 1)}+{col('Net cash flow before equity', j)}", bold=True)
            sh.cell(row, 1, "Equity funding requirement (max cumulative deficit)").font = Font(bold=True, color="8B1E1E")
            c = sh.cell(row, 2, f"=-MIN(0,MIN(B{lines['Cumulative cash before equity']}:F{lines['Cumulative cash before equity']}))")
            c.number_format = "#,##0"; c.font = Font(bold=True, color="8B1E1E")
            summary_rows[sc] = (lines, row)
            row += 2
        sh.column_dimensions["A"].width = 52
        for j in range(5):
            sh.column_dimensions[get_column_letter(2 + j)].width = 14
        ch = LineChart()
        ch.title = f"{st}: cumulative cash before equity"
        ch.y_axis.title = "$"
        for sc in SC:
            lines, _ = summary_rows[sc]
            rr = lines["Cumulative cash before equity"]
            data = Reference(sh, min_col=2, max_col=6, min_row=rr, max_row=rr)
            ch.add_data(data, from_rows=True, titles_from_data=False)
        for s_, sc in zip(ch.series, SC):
            from openpyxl.chart.series import SeriesLabel
            s_.tx = SeriesLabel(v=sc)
        ch.height, ch.width = 8, 18
        sh.add_chart(ch, "H2")
    wb.save(path)
    print("saved", path)


if __name__ == "__main__":
    main()
