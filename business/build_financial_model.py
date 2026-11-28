"""Build business/FINANCIAL_MODEL.xlsx and business/financial_model_outputs.json.

Formula-driven 5-year model (2027-2031) for OsteoQuant, an offline desktop micro-CT analysis application sold
together with analysis services. Every driver is an assumption [AE] or a pricing/conversion hypothesis [HYP];
no interviews, pilots or sales have happened. See business/REVENUE_MODEL.md for the rationale of each input.

Offerings (founder pricing hypotheses, to be tested - not facts):
  paid pilot $2.5-5K | non-GLP study analysis $8-15K | material characterisation $5-15K
  academic desktop licence $4-10K/yr | enterprise desktop licence $30-75K/yr

Structures: 'Bootstrapped' (founder-led services + desktop licences) and 'Venture' (pre-seed funded team,
same prices and conversion rates, more conversations and expansion modules from year 3).
Scenarios: Conservative / Base / Optimistic.

Timing and grants (cycle-2 review C2-BIZ-12, INV-04/05/06/07):
  * No revenue before incorporation and a first signed pilot. Paid pilots (and everything that follows from them)
    are scaled by the share of each year in which selling is possible (after M0 entity + IP clearance + insurance +
    counsel-reviewed contracts, and M3 first signed pilot): 2027 = 0 / 0.25 / 0.5 (Conservative / Base /
    Optimistic), later years 1. Licences need a licence/EULA and a production signing key and start only after the
    first signed pilot: 0 in 2027 in every scenario.
  * Grants are NOT operating cash. The lead case is cash WITHOUT grants. Grant awards are conditional (eligibility
    unresolved; nothing applied for); an award is restricted to its project (incl. the >=30% research-institution
    subaward of an STTR) and only its fee share plus the planned costs the project legitimately pays (e.g. the
    phantom study) improve operating cash. Both cash paths are reported; the equity requirement headline is the
    no-grant one.
  * Licence revenue has no enforceable basis while the source is public with no licence/EULA (founder decision):
    2031 revenue without licence revenue is reported alongside.

Reproducibility:
  python business/build_financial_model.py
  * writes the workbook (all outputs are Excel formulas that reference the 'Inputs' sheet);
  * evaluates the same model in Python (the 'mirror') and writes financial_model_outputs.json and
    revenue_model_sensitivity.json;
  * checks that no formula references its own cell;
  * if LibreOffice is installed, recalculates a temporary copy of the workbook headlessly and asserts that every
    output cell agrees with the Python mirror (and that no cell evaluates to an error).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.series import SeriesLabel
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
YEARS = [2027, 2028, 2029, 2030, 2031]
SC = ["Conservative", "Base", "Optimistic"]
STRUCTS = ["Bootstrapped", "Venture"]
HDR = PatternFill("solid", fgColor="DCE6F1")
INP = PatternFill("solid", fgColor="FFF2CC")
FTE_HOURS = 1600  # productive delivery hours per full-time analyst per year [AE]


def S(c, b, o):
    return {"Conservative": c, "Base": b, "Optimistic": o}


# ---------------------------------------------------------------------------------------------------------------
# Inputs: key -> (label, unit, evidence, {structure: S(...)}). A value is a scalar (same every year) or 5 values.
# ---------------------------------------------------------------------------------------------------------------
def same(v):
    return {"Bootstrapped": v, "Venture": v}


P = {}  # ordered


def add(key, label, unit, evidence, per_struct):
    P[key] = (label, unit, evidence, per_struct)


# Industry funnel ------------------------------------------------------------------------------------------------
add("conv", "Qualified industry discovery conversations (distinct buying units)", "#",
    "[AE] founder capacity; capped by ~200 US-visible industry buying units (MARKET_MODEL_INPUTS.md §1b, §2)",
    {"Bootstrapped": S([12, 20, 25, 25, 25], [20, 30, 35, 35, 35], [25, 40, 45, 50, 50]),
     "Venture": S([20, 30, 40, 45, 45], [30, 45, 55, 60, 60], [35, 55, 70, 80, 80])})
add("sell", "Share of year in which paid work can be sold (after M0 entity/IP/insurance/contracts and M3 first signed pilot)",
    "%", "[AE] FUNDING_STRATEGY.md §3 milestones: M0 Dec 2026-Feb 2027, M3 first paid pilot mid-2027 at the earliest",
    same(S([0.0, 1, 1, 1, 1], [0.25, 1, 1, 1, 1], [0.5, 1, 1, 1, 1])))
add("lic_avail", "Share of year in which licences can be sold (EULA + production signing key, after the first signed pilot)",
    "%", "[AE] no production key or EULA exists (PACKAGING.md); founder decision on the code licence",
    same(S([0.0, 0.5, 1, 1, 1], [0.0, 1, 1, 1, 1], [0.0, 1, 1, 1, 1])))
add("r_pilot", "Conversation -> paid pilot rate", "%", "[HYP] untested; decision threshold in PRICING_VALIDATION_PLAN.md",
    same(S(0.08, 0.15, 0.22)))
add("r_cust", "Paid pilot -> recurring study customer rate", "%", "[HYP] untested", same(S(0.25, 0.40, 0.50)))
add("ret_cust", "Study customer annual retention", "%", "[HYP] untested", same(S(0.60, 0.75, 0.85)))
add("studies", "Non-GLP studies per active study customer per year", "#",
    "[AE] BVF firms 0.5/1.5/3 per year (MARKET_MODEL_INPUTS.md §4)", same(S(1.0, 1.5, 1.8)))
add("p_pilot", "Price: paid pilot", "$", "[HYP] founder range $2.5-5K", same(S(2500, 3500, 5000)))
add("p_study", "Price: non-GLP study analysis", "$", "[HYP] founder range $8-15K", same(S(8000, 11000, 15000)))
add("r_char", "Material characterisations per paid pilot (attach rate)", "%", "[HYP] untested", same(S(0.20, 0.40, 0.50)))
add("p_char", "Price: material characterisation", "$", "[HYP] founder range $5-15K", same(S(5000, 9000, 15000)))
# Academic ---------------------------------------------------------------------------------------------------------
add("evals", "Academic labs/cores starting a licence evaluation", "#",
    "[AE] vs 45-49 orgs with NIH micro-CT bone-repair projects (MARKET_MODEL_INPUTS.md §3); capped so that active "
    "licences stay well below the 49 [V] organisations (review INV-06)",
    {"Bootstrapped": S([2, 4, 6, 8, 8], [4, 8, 10, 12, 12], [6, 10, 12, 14, 14]),
     "Venture": S([4, 8, 10, 12, 12], [6, 10, 12, 14, 16], [8, 12, 16, 18, 20])})
add("r_acad", "Evaluation -> academic licence rate", "%", "[HYP] untested", same(S(0.20, 0.35, 0.45)))
add("ret_acad", "Academic licence annual retention", "%", "[HYP] grant-cycle dependent", same(S(0.70, 0.80, 0.85)))
add("p_acad", "Price: academic desktop licence per year", "$", "[HYP] founder range $4-10K/yr", same(S(4000, 6000, 10000)))
# Enterprise -------------------------------------------------------------------------------------------------------
add("ent_new", "New enterprise licences signed (CROs / high-volume manufacturers)", "#", "[HYP] untested; long sales cycle",
    {"Bootstrapped": S([0, 0, 0, 0, 1], [0, 0, 1, 0, 1], [0, 0, 1, 1, 1]),
     "Venture": S([0, 0, 1, 1, 1], [0, 1, 1, 2, 2], [0, 1, 1, 2, 2])})
add("ret_ent", "Enterprise licence annual retention", "%", "[HYP] untested", same(S(0.80, 0.85, 0.90)))
add("p_ent", "Price: enterprise desktop licence per year", "$", "[HYP] founder range $30-75K/yr", same(S(30000, 45000, 75000)))
add("exp", "Expansion-module revenue (% of core revenue)", "%",
    "[HYP] osseointegration / spine fusion / histology modules - not built",
    {"Bootstrapped": S(0, 0, 0),
     "Venture": S([0, 0, 0, 0.05, 0.10], [0, 0, 0.05, 0.15, 0.25], [0, 0, 0.10, 0.25, 0.40])})
add("exp_cogs", "Expansion-module delivery cost (% of its revenue)", "%", "[AE]", same(S(0.40, 0.30, 0.25)))
# Delivery cost ----------------------------------------------------------------------------------------------------
add("h_pilot", "Analyst hours per paid pilot", "h", "[AE] 10-20 retrospective scans; measure in first pilot", same(S(35, 25, 15)))
add("h_study", "Analyst hours per non-GLP study", "h",
    "[AE] intake/QC, ROI review, material adaptation, review, statistics, report, calls; learning curve",
    {"Bootstrapped": S([90, 80, 70, 60, 55], [60, 50, 42, 36, 32], [45, 36, 30, 25, 22]),
     "Venture": S([80, 65, 55, 45, 40], [55, 42, 34, 28, 24], [40, 30, 24, 20, 16])})
add("h_char", "Analyst hours per material characterisation", "h", "[AE]", same(S(60, 40, 30)))
add("h_acad", "Support hours per academic licence per year", "h", "[AE]", same(S(16, 10, 6)))
add("h_ent", "Support hours per enterprise licence per year", "h", "[AE] onboarding, validation-evidence pack, support",
    same(S(120, 80, 50)))
add("rate", "Loaded analyst cost per hour", "$", "[AE] PhD-level imaging analyst incl. overhead", same(S(65, 60, 55)))
add("data", "Data handling per pilot/study/characterisation (compute ~$0: runs on local desktop)", "$",
    "[AE] encrypted drives, shipping, backup storage", same(S(75, 40, 25)))
add("pass", "Pass-through per material characterisation (scanner time, reference samples)", "$",
    "[AE] ~6-20 scanner h at $60-79/h (Beckman external rates [V], validation/BILL_OF_MATERIALS.csv)",
    same(S(1500, 1000, 500)))
# Operating costs --------------------------------------------------------------------------------------------------
add("sal", "Founder & non-delivery staff salaries", "$", "[AE] stipend -> salaries as revenue / grants allow",
    {"Bootstrapped": S([0, 12000, 24000, 36000, 48000], [12000, 40000, 60000, 80000, 100000],
                       [24000, 60000, 90000, 120000, 150000]),
     "Venture": S([150000, 400000, 650000, 850000, 1000000], [200000, 500000, 800000, 1050000, 1250000],
                  [250000, 600000, 950000, 1250000, 1500000])})
add("val", "Validation & QA spend", "$", "[AE] phantom study Y1 ($10-20K, validation/BILL_OF_MATERIALS.csv); evidence packs",
    {"Bootstrapped": S([15000, 20000, 15000, 15000, 15000], [15000, 35000, 30000, 20000, 20000],
                       [20000, 50000, 40000, 30000, 30000]),
     "Venture": S([30000, 100000, 120000, 100000, 100000], [40000, 120000, 150000, 120000, 120000],
                  [50000, 150000, 180000, 150000, 150000])})
add("opex", "Other opex (legal, insurance, software, code signing, travel)", "$", "[AE]",
    {"Bootstrapped": S([12000, 15000, 18000, 20000, 22000], [15000, 22000, 28000, 34000, 40000],
                       [20000, 30000, 40000, 50000, 60000]),
     "Venture": S([50000, 100000, 150000, 200000, 240000], [60000, 120000, 180000, 240000, 300000],
                  [80000, 150000, 220000, 290000, 360000])})
add("sm", "Sales & marketing cost per conversation / evaluation", "$", "[AE] travel, conference share, demo media",
    {"Bootstrapped": S(200, 150, 120), "Venture": S(400, 350, 300)})
add("grant", "Grant / prize AWARDS - CONDITIONAL (none applied for; eligibility unresolved)", "$",
    "[HYP] Phase I up to $305K NSF [V]; PI-eligibility unresolved (grants/NSF_vs_NIH_ELIGIBILITY.md); "
    "restricted to the funded project",
    {"Bootstrapped": S([0, 0, 0, 0, 0], [20000, 150000, 155000, 0, 0], [40000, 150000, 155000, 0, 0]),
     "Venture": S([0, 150000, 155000, 0, 0], [20000, 150000, 155000, 500000, 750000],
                  [40000, 150000, 155000, 500000, 750000])})

add("g_fee", "Grant share that is unrestricted (SBIR/STTR fee / profit)", "%",
    "[AE] up to ~7% fee on SBIR/STTR awards; prizes treated the same way for prudence", same(S(0.0, 0.07, 0.07)))
add("g_offset", "Share of restricted grant spend that pays costs already in this plan (e.g. phantom study, stipend)",
    "%", "[AE] the rest is new project work (incl. STTR subaward >=30%) that would not otherwise be done",
    same(S(0.10, 0.25, 0.40)))

KEYS = list(P.keys())


def val(key, st, sc, j):
    v = P[key][3][st][sc]
    return v[j] if isinstance(v, list) else v


# ---------------------------------------------------------------------------------------------------------------
# Line definitions: (name, fmt, bold, python_fn(ctx, j), excel_fn(X, j))
#   ctx.i(key, j)  -> input value ; ctx.l(name, j) -> line value (j may be -1 => 0)
#   X.i(key, j)    -> Inputs!cell ; X.l(name, j)  -> P&L cell (j == -1 => "0")
# ---------------------------------------------------------------------------------------------------------------
LINES = [
    ("Industry conversations", "0", False, lambda c, j: c.i("conv", j), lambda x, j: x.i("conv", j)),
    ("Paid pilots", "0.0", False, lambda c, j: c.i("conv", j) * c.i("r_pilot", j) * c.i("sell", j),
     lambda x, j: f"{x.i('conv', j)}*{x.i('r_pilot', j)}*{x.i('sell', j)}"),
    ("New study customers", "0.0", False, lambda c, j: c.l("Paid pilots", j) * c.i("r_cust", j),
     lambda x, j: f"{x.l('Paid pilots', j)}*{x.i('r_cust', j)}"),
    ("Active study customers (year end)", "0.0", False,
     lambda c, j: c.l("Active study customers (year end)", j - 1) * c.i("ret_cust", j) + c.l("New study customers", j),
     lambda x, j: f"{x.l('Active study customers (year end)', j - 1)}*{x.i('ret_cust', j)}+{x.l('New study customers', j)}"),
    ("Non-GLP studies analysed", "0.0", False,
     lambda c, j: (c.l("Active study customers (year end)", j - 1) * c.i("ret_cust", j)
                   + 0.5 * c.l("New study customers", j)) * c.i("studies", j),
     lambda x, j: f"({x.l('Active study customers (year end)', j - 1)}*{x.i('ret_cust', j)}"
                  f"+0.5*{x.l('New study customers', j)})*{x.i('studies', j)}"),
    ("Material characterisations", "0.0", False, lambda c, j: c.l("Paid pilots", j) * c.i("r_char", j),
     lambda x, j: f"{x.l('Paid pilots', j)}*{x.i('r_char', j)}"),
    ("Academic evaluations", "0", False, lambda c, j: c.i("evals", j), lambda x, j: x.i("evals", j)),
    ("New academic licences", "0.0", False, lambda c, j: c.i("evals", j) * c.i("r_acad", j) * c.i("lic_avail", j),
     lambda x, j: f"{x.i('evals', j)}*{x.i('r_acad', j)}*{x.i('lic_avail', j)}"),
    ("Active academic licences", "0.0", False,
     lambda c, j: c.l("Active academic licences", j - 1) * c.i("ret_acad", j) + c.l("New academic licences", j),
     lambda x, j: f"{x.l('Active academic licences', j - 1)}*{x.i('ret_acad', j)}+{x.l('New academic licences', j)}"),
    ("Active enterprise licences", "0.0", False,
     lambda c, j: c.l("Active enterprise licences", j - 1) * c.i("ret_ent", j) + c.i("ent_new", j) * c.i("lic_avail", j),
     lambda x, j: f"{x.l('Active enterprise licences', j - 1)}*{x.i('ret_ent', j)}+{x.i('ent_new', j)}*{x.i('lic_avail', j)}"),
    ("Pilot revenue", "#,##0", False, lambda c, j: c.l("Paid pilots", j) * c.i("p_pilot", j),
     lambda x, j: f"{x.l('Paid pilots', j)}*{x.i('p_pilot', j)}"),
    ("Study analysis revenue", "#,##0", False, lambda c, j: c.l("Non-GLP studies analysed", j) * c.i("p_study", j),
     lambda x, j: f"{x.l('Non-GLP studies analysed', j)}*{x.i('p_study', j)}"),
    ("Material characterisation revenue", "#,##0", False,
     lambda c, j: c.l("Material characterisations", j) * c.i("p_char", j),
     lambda x, j: f"{x.l('Material characterisations', j)}*{x.i('p_char', j)}"),
    ("Academic licence revenue", "#,##0", False, lambda c, j: c.l("Active academic licences", j) * c.i("p_acad", j),
     lambda x, j: f"{x.l('Active academic licences', j)}*{x.i('p_acad', j)}"),
    ("Enterprise licence revenue", "#,##0", False, lambda c, j: c.l("Active enterprise licences", j) * c.i("p_ent", j),
     lambda x, j: f"{x.l('Active enterprise licences', j)}*{x.i('p_ent', j)}"),
]
CORE_REV = ["Pilot revenue", "Study analysis revenue", "Material characterisation revenue", "Academic licence revenue",
            "Enterprise licence revenue"]
LINES += [
    ("Expansion-module revenue", "#,##0", False, lambda c, j: sum(c.l(n, j) for n in CORE_REV) * c.i("exp", j),
     lambda x, j: f"({'+'.join(x.l(n, j) for n in CORE_REV)})*{x.i('exp', j)}"),
    ("Total revenue", "#,##0", True, lambda c, j: sum(c.l(n, j) for n in CORE_REV + ["Expansion-module revenue"]),
     lambda x, j: "+".join(x.l(n, j) for n in CORE_REV + ["Expansion-module revenue"])),
    ("Delivery hours", "#,##0", False,
     lambda c, j: (c.l("Paid pilots", j) * c.i("h_pilot", j) + c.l("Non-GLP studies analysed", j) * c.i("h_study", j)
                   + c.l("Material characterisations", j) * c.i("h_char", j)
                   + c.l("Active academic licences", j) * c.i("h_acad", j)
                   + c.l("Active enterprise licences", j) * c.i("h_ent", j)),
     lambda x, j: f"{x.l('Paid pilots', j)}*{x.i('h_pilot', j)}+{x.l('Non-GLP studies analysed', j)}*{x.i('h_study', j)}"
                  f"+{x.l('Material characterisations', j)}*{x.i('h_char', j)}"
                  f"+{x.l('Active academic licences', j)}*{x.i('h_acad', j)}"
                  f"+{x.l('Active enterprise licences', j)}*{x.i('h_ent', j)}"),
    ("Implied delivery FTE", "0.00", False, lambda c, j: c.l("Delivery hours", j) / FTE_HOURS,
     lambda x, j: f"{x.l('Delivery hours', j)}/{FTE_HOURS}"),
    ("Analyst & support labour (COGS)", "#,##0", False, lambda c, j: c.l("Delivery hours", j) * c.i("rate", j),
     lambda x, j: f"{x.l('Delivery hours', j)}*{x.i('rate', j)}"),
    ("Data handling (COGS)", "#,##0", False,
     lambda c, j: (c.l("Paid pilots", j) + c.l("Non-GLP studies analysed", j) + c.l("Material characterisations", j))
     * c.i("data", j),
     lambda x, j: f"({x.l('Paid pilots', j)}+{x.l('Non-GLP studies analysed', j)}+{x.l('Material characterisations', j)})"
                  f"*{x.i('data', j)}"),
    ("Characterisation pass-through (COGS)", "#,##0", False,
     lambda c, j: c.l("Material characterisations", j) * c.i("pass", j),
     lambda x, j: f"{x.l('Material characterisations', j)}*{x.i('pass', j)}"),
    ("Expansion-module delivery (COGS)", "#,##0", False,
     lambda c, j: c.l("Expansion-module revenue", j) * c.i("exp_cogs", j),
     lambda x, j: f"{x.l('Expansion-module revenue', j)}*{x.i('exp_cogs', j)}"),
]
COGS = ["Analyst & support labour (COGS)", "Data handling (COGS)", "Characterisation pass-through (COGS)",
        "Expansion-module delivery (COGS)"]
LINES += [
    ("Gross profit", "#,##0", True, lambda c, j: c.l("Total revenue", j) - sum(c.l(n, j) for n in COGS),
     lambda x, j: f"{x.l('Total revenue', j)}-" + "-".join(x.l(n, j) for n in COGS)),
    ("Gross margin %", "0%", False,
     lambda c, j: 0 if c.l("Total revenue", j) == 0 else c.l("Gross profit", j) / c.l("Total revenue", j),
     lambda x, j: f"IF({x.l('Total revenue', j)}=0,0,{x.l('Gross profit', j)}/{x.l('Total revenue', j)})"),
    ("Salaries", "#,##0", False, lambda c, j: c.i("sal", j), lambda x, j: x.i("sal", j)),
    ("Validation & QA", "#,##0", False, lambda c, j: c.i("val", j), lambda x, j: x.i("val", j)),
    ("Other opex", "#,##0", False, lambda c, j: c.i("opex", j), lambda x, j: x.i("opex", j)),
    ("Sales & marketing", "#,##0", False, lambda c, j: (c.i("conv", j) + c.i("evals", j)) * c.i("sm", j),
     lambda x, j: f"({x.i('conv', j)}+{x.i('evals', j)})*{x.i('sm', j)}"),
]
OPEX = ["Salaries", "Validation & QA", "Other opex", "Sales & marketing"]
LINES += [
    ("EBITDA", "#,##0", True, lambda c, j: c.l("Gross profit", j) - sum(c.l(n, j) for n in OPEX),
     lambda x, j: f"{x.l('Gross profit', j)}-" + "-".join(x.l(n, j) for n in OPEX)),
    ("Cumulative cash - NO grants (lead case)", "#,##0", True,
     lambda c, j: c.l("Cumulative cash - NO grants (lead case)", j - 1) + c.l("EBITDA", j),
     lambda x, j: (x.l("EBITDA", j) if j == 0
                   else f"{x.l('Cumulative cash - NO grants (lead case)', j - 1)}+{x.l('EBITDA', j)}")),
    ("Grant awards - CONDITIONAL, not operating cash", "#,##0", False, lambda c, j: c.i("grant", j),
     lambda x, j: x.i("grant", j)),
    ("Restricted grant project spend (incl. STTR subaward)", "#,##0", False,
     lambda c, j: c.l("Grant awards - CONDITIONAL, not operating cash", j) * (1 - c.i("g_fee", j)),
     lambda x, j: f"{x.l('Grant awards - CONDITIONAL, not operating cash', j)}*(1-{x.i('g_fee', j)})"),
    ("Grant effect on operating cash IF awarded", "#,##0", False,
     lambda c, j: c.l("Grant awards - CONDITIONAL, not operating cash", j) * c.i("g_fee", j)
     + c.l("Restricted grant project spend (incl. STTR subaward)", j) * c.i("g_offset", j),
     lambda x, j: f"{x.l('Grant awards - CONDITIONAL, not operating cash', j)}*{x.i('g_fee', j)}"
                  f"+{x.l('Restricted grant project spend (incl. STTR subaward)', j)}*{x.i('g_offset', j)}"),
    ("Cumulative cash - WITH grants IF awarded (conditional)", "#,##0", False,
     lambda c, j: c.l("Cumulative cash - WITH grants IF awarded (conditional)", j - 1) + c.l("EBITDA", j)
     + c.l("Grant effect on operating cash IF awarded", j),
     lambda x, j: (f"{x.l('EBITDA', j)}+{x.l('Grant effect on operating cash IF awarded', j)}" if j == 0
                   else f"{x.l('Cumulative cash - WITH grants IF awarded (conditional)', j - 1)}+{x.l('EBITDA', j)}"
                        f"+{x.l('Grant effect on operating cash IF awarded', j)}")),
]
LINE_NAMES = [n for n, *_ in LINES]


# ---------------------------------------------------------------------------------------------------------------
# Python mirror
# ---------------------------------------------------------------------------------------------------------------
class Ctx:
    def __init__(self, st, sc, override=None):
        self.st, self.sc, self.override = st, sc, override or {}
        self.v = {}

    def i(self, key, j):
        if key in self.override:
            o = self.override[key]
            return o[j] if isinstance(o, list) else o
        return val(key, self.st, self.sc, j)

    def l(self, name, j):
        return 0.0 if j < 0 else self.v[(name, j)]


def compute(st, sc, override=None):
    c = Ctx(st, sc, override)
    for j in range(5):
        for name, _fmt, _b, pf, _xf in LINES:
            c.v[(name, j)] = pf(c, j)
    out = {n: [c.v[(n, j)] for j in range(5)] for n in LINE_NAMES}
    # headline equity requirement = NO-grant lead case (grants are conditional and restricted)
    out["Equity funding requirement (max cumulative deficit)"] = -min(0.0, min(out["Cumulative cash - NO grants (lead case)"]))
    out["Equity requirement WITH grants IF awarded (conditional)"] = -min(
        0.0, min(out["Cumulative cash - WITH grants IF awarded (conditional)"]))
    lic = [out["Academic licence revenue"][j] + out["Enterprise licence revenue"][j] for j in range(5)]
    out["Total revenue without licence revenue"] = [
        out["Total revenue"][j] - lic[j] * (1 + (c.i("exp", j) if j < 5 else 0)) for j in range(5)]
    return out


# ---------------------------------------------------------------------------------------------------------------
# Workbook
# ---------------------------------------------------------------------------------------------------------------
def build_workbook(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    notes = [
        "OsteoQuant 5-year revenue and cash model (2027-2031). DRAFT. Every revenue driver is a hypothesis.",
        "Status: pre-revenue, unincorporated, no customer interviews, no pilots, no letters of intent. Prices are the founder's "
        "pricing hypotheses to test, not quotes and not market facts.",
        "Offerings: paid pilot $2.5-5K | non-GLP study analysis $8-15K | material characterisation $5-15K | academic desktop "
        "licence $4-10K/yr | enterprise desktop licence $30-75K/yr. No GLP-study offering is modelled; no GLP, Part 11 or "
        "regulatory-acceptance claim is made.",
        "Yellow cells on 'Inputs' are editable. Every number on the P&L, Unit economics and Market check sheets is a formula. "
        "The 'Sensitivity' sheet holds values computed by build_financial_model.py with a Python mirror of the same formulas.",
        "Compute cost is ~$0 per study because the application runs on the analyst's or customer's desktop; the dominant "
        "cost is analyst time, which is an assumption to measure in the first pilot.",
        "Revenue timing: new study customers contribute half a year of studies in the year they convert; licences are booked "
        "for the full year in which they are active.",
        "Structures: 'Bootstrapped' = founder-led services + desktop licences; 'Venture' = pre-seed funded team with the same "
        "prices and conversion rates, more conversations, and hypothetical expansion modules from 2029.",
        "No revenue before incorporation and a first signed pilot: paid work is scaled by the share of each year in which it "
        "can be sold (2027: 0 / 25% / 50%); licences start only after the first signed pilot (none in 2027).",
        "Grants are NOT operating cash. The lead case is 'Cumulative cash - NO grants'. Grant awards are conditional (none "
        "applied for; SBIR/STTR PI-eligibility for a full-time student is unresolved, grants/NSF_vs_NIH_ELIGIBILITY.md) and "
        "restricted to the funded project (an STTR needs a >=30% research-institution subaward); only the fee share and the "
        "planned costs the project legitimately pays reach operating cash ('WITH grants IF awarded').",
        "Licence revenue needs an enforceable licence/EULA and a production signing key (neither exists); the JSON output "
        "also reports total revenue without licence revenue.",
        "Rationale for every input: business/REVENUE_MODEL.md. Rebuild: python business/build_financial_model.py",
    ]
    for i, n in enumerate(notes, 1):
        ws.cell(i, 1, n).alignment = Alignment(wrap_text=True)
    ws.column_dimensions["A"].width = 150

    inp = wb.create_sheet("Inputs")
    inp.append(["Structure", "Parameter", "Unit", "Evidence / rationale", "Scenario"] + YEARS)
    for c in inp[1]:
        c.font = Font(bold=True)
        c.fill = HDR
    ref = {}
    r = 2
    for st in STRUCTS:
        for k in KEYS:
            label, unit, ev, _ = P[k]
            for sc in SC:
                inp.cell(r, 1, st)
                inp.cell(r, 2, label)
                inp.cell(r, 3, unit)
                inp.cell(r, 4, ev)
                inp.cell(r, 5, sc)
                for j in range(5):
                    c = inp.cell(r, 6 + j, val(k, st, sc, j))
                    c.fill = INP
                    c.number_format = "0%" if unit == "%" else "#,##0.0" if k == "studies" else "#,##0"
                ref[(st, sc, k)] = r
                r += 1
    for col, w in zip("ABCDE", (14, 62, 6, 70, 13)):
        inp.column_dimensions[col].width = w
    inp.freeze_panes = "F2"

    line_cells = {}  # (st, sc, line) -> row on P&L sheet
    for st in STRUCTS:
        sh = wb.create_sheet(f"P&L {st}")
        row = 1
        for sc in SC:
            sh.cell(row, 1, f"{st} - {sc} (all drivers hypothetical)").font = Font(bold=True, size=12, color="1F4E79")
            row += 1
            sh.cell(row, 1, "Line")
            for j, y in enumerate(YEARS):
                sh.cell(row, 2 + j, y)
            for c in sh[row]:
                c.font = Font(bold=True)
                c.fill = HDR
            row += 1
            # pre-assign rows so formulas can reference any line
            rows = {}
            for name in LINE_NAMES:
                rows[name] = row
                row += 1

            class X:
                @staticmethod
                def i(key, j, _st=st, _sc=sc):
                    return f"Inputs!{get_column_letter(6 + j)}{ref[(_st, _sc, key)]}"

                @staticmethod
                def l(name, j, _rows=rows):
                    return "0" if j < 0 else f"{get_column_letter(2 + j)}{_rows[name]}"

            for name, fmt, bold, _pf, xf in LINES:
                rr = rows[name]
                sh.cell(rr, 1, name).font = Font(bold=bold)
                for j in range(5):
                    c = sh.cell(rr, 2 + j, "=" + xf(X, j))
                    c.number_format = fmt
                    if bold:
                        c.font = Font(bold=True)
                line_cells[(st, sc, name)] = rr
            sh.cell(row, 1, "Equity funding requirement (max cumulative deficit) - NO grants").font = Font(bold=True, color="8B1E1E")
            cr = rows["Cumulative cash - NO grants (lead case)"]
            c = sh.cell(row, 2, f"=-MIN(0,MIN(B{cr}:F{cr}))")
            c.number_format = "#,##0"
            c.font = Font(bold=True, color="8B1E1E")
            line_cells[(st, sc, "Equity funding requirement (max cumulative deficit)")] = row
            row += 1
            sh.cell(row, 1, "Equity requirement WITH grants IF awarded (conditional)")
            nr = rows["Cumulative cash - WITH grants IF awarded (conditional)"]
            c = sh.cell(row, 2, f"=-MIN(0,MIN(B{nr}:F{nr}))")
            c.number_format = "#,##0"
            line_cells[(st, sc, "Equity requirement WITH grants IF awarded (conditional)")] = row
            row += 2
        sh.column_dimensions["A"].width = 52
        for j in range(5):
            sh.column_dimensions[get_column_letter(2 + j)].width = 14
        sh.freeze_panes = "B1"
        ch = LineChart()
        ch.title = f"{st}: total revenue by scenario (hypothetical)"
        ch.y_axis.title = "$"
        for sc in SC:
            rr = line_cells[(st, sc, "Total revenue")]
            ch.add_data(Reference(sh, min_col=2, max_col=6, min_row=rr, max_row=rr), from_rows=True, titles_from_data=False)
        for s_, sc in zip(ch.series, SC):
            s_.tx = SeriesLabel(v=sc)
        ch.height, ch.width = 8, 18
        sh.add_chart(ch, "H2")

    # Unit economics (formulas) -------------------------------------------------------------------------------
    ue = wb.create_sheet("Unit economics")
    ue.append(["Contribution per unit = price - (analyst hours x loaded rate) - data handling - pass-through. "
               "Bootstrapped structure; year shown in column header. All inputs hypothetical."])
    ue.append([])
    ue.append(["Offering", "Scenario", "Price 2027", "Delivery cost 2027", "Contribution 2027", "Margin 2027",
               "Price 2031", "Delivery cost 2031", "Contribution 2031", "Margin 2031"])
    for c in ue[3]:
        c.font = Font(bold=True)
        c.fill = HDR
    offers = [("Paid pilot", "p_pilot", "h_pilot", True, False), ("Non-GLP study analysis", "p_study", "h_study", True, False),
              ("Material characterisation", "p_char", "h_char", True, True),
              ("Academic licence (per year)", "p_acad", "h_acad", False, False),
              ("Enterprise licence (per year)", "p_ent", "h_ent", False, False)]
    r = 4
    unit_rows = {}
    for name, pk, hk, has_data, has_pass in offers:
        for sc in SC:
            I = lambda k, j: f"Inputs!{get_column_letter(6 + j)}{ref[('Bootstrapped', sc, k)]}"
            ue.cell(r, 1, name)
            ue.cell(r, 2, sc)
            for off, j in ((3, 0), (7, 4)):
                cost = f"{I(hk, j)}*{I('rate', j)}"
                if has_data:
                    cost += f"+{I('data', j)}"
                if has_pass:
                    cost += f"+{I('pass', j)}"
                pc, cc, kc = (get_column_letter(off + n) for n in range(3))
                ue.cell(r, off, f"={I(pk, j)}").number_format = "#,##0"
                ue.cell(r, off + 1, f"={cost}").number_format = "#,##0"
                ue.cell(r, off + 2, f"={pc}{r}-{cc}{r}").number_format = "#,##0"
                ue.cell(r, off + 3, f"=IF({pc}{r}=0,0,{kc}{r}/{pc}{r})").number_format = "0%"
            unit_rows[(name, sc)] = r
            r += 1
    ue.column_dimensions["A"].width = 32
    ue.column_dimensions["B"].width = 13
    for col in "CDEFGHIJ":
        ue.column_dimensions[col].width = 15

    # Market check (formulas) ---------------------------------------------------------------------------------
    mk = wb.create_sheet("Market check")
    mk.append(["Serviceable pool at the Base price hypotheses vs modelled revenue. Counts are [V] (openFDA / NIH RePORTER, "
               "business/MARKET_MODEL_INPUTS.md); volumes are [AE]; prices are [HYP]."])
    mk.append([])
    mk.append(["Segment", "Organisations", "Evidence", "Studies/org/yr low", "mid", "high", "Pool low $", "Pool mid $",
               "Pool high $"])
    for c in mk[3]:
        c.font = Font(bold=True)
        c.fill = HDR
    pb = f"Inputs!F{ref[('Bootstrapped', 'Base', 'p_study')]}"
    pa = f"Inputs!F{ref[('Bootstrapped', 'Base', 'p_acad')]}"
    segs = [("Ortho bone-void-filler manufacturers (active 2023-26)", 41, "[V] openFDA", 0.5, 1.5, 3, pb),
            ("Dental graft + barrier manufacturers (active 2023-26)", 24, "[V] openFDA", 0.5, 1, 2, pb),
            ("Spine fusion firms (graft-related studies only)", 117, "[V] count; [AE] share", 0.1, 0.2, 0.3, pb),
            ("PMA biologic sponsors", 3, "[V] openFDA PMA", 1, 2, 4, pb)]
    r = 4
    for name, n, ev, lo, mid, hi, pr in segs:
        mk.append([name, n, ev, lo, mid, hi])
        for k, col in enumerate("DEF"):
            mk.cell(r, 7 + k, f"=B{r}*{col}{r}*{pr}").number_format = "#,##0"
        r += 1
    mk.cell(r, 1, "Industry per-study pool").font = Font(bold=True)
    for k, col in enumerate("GHI"):
        mk.cell(r, 7 + k, f"=SUM({col}4:{col}{r - 1})").number_format = "#,##0"
    ind_row = r
    r += 1
    mk.cell(r, 1, "Academic licences (labs: 49 [V] lower bound / 100 / 250 [AE])")
    mk.cell(r, 3, "[V]/[AE]")
    for k, n in enumerate((49, 100, 250)):
        mk.cell(r, 7 + k, f"={n}*{pa}").number_format = "#,##0"
    acad_row = r
    r += 1
    mk.cell(r, 1, "Total serviceable pool (excl. characterisation, enterprise overlap)").font = Font(bold=True)
    for k, col in enumerate("GHI"):
        mk.cell(r, 7 + k, f"={col}{ind_row}+{col}{acad_row}").number_format = "#,##0"
    tot_row = r
    r += 2
    mk.cell(r, 1, "Modelled 2031 revenue as share of the MID pool").font = Font(bold=True)
    r += 1
    mk.append(["Structure - scenario", "2031 study revenue", "share of mid industry pool", "2031 academic revenue",
               "share of mid academic pool", "2031 total revenue", "share of mid total pool",
               "Cumulative industry conversations 2027-31", "vs ~200 US-visible industry buying units"])
    for c in mk[r]:
        c.font = Font(bold=True)
        c.fill = HDR
    r += 1
    for st in STRUCTS:
        for sc in SC:
            sheet = f"'P&L {st}'"
            sr = line_cells[(st, sc, "Study analysis revenue")]
            ar = line_cells[(st, sc, "Academic licence revenue")]
            tr = line_cells[(st, sc, "Total revenue")]
            cv = line_cells[(st, sc, "Industry conversations")]
            mk.cell(r, 1, f"{st} - {sc}")
            mk.cell(r, 2, f"={sheet}!F{sr}").number_format = "#,##0"
            mk.cell(r, 3, f"=B{r}/H{ind_row}").number_format = "0%"
            mk.cell(r, 4, f"={sheet}!F{ar}").number_format = "#,##0"
            mk.cell(r, 5, f"=D{r}/H{acad_row}").number_format = "0%"
            mk.cell(r, 6, f"={sheet}!F{tr}").number_format = "#,##0"
            mk.cell(r, 7, f"=F{r}/H{tot_row}").number_format = "0%"
            mk.cell(r, 8, f"=SUM({sheet}!B{cv}:F{cv})").number_format = "#,##0"
            mk.cell(r, 9, f"=H{r}/200").number_format = "0%"
            r += 1
    mk.cell(r + 1, 1, "Read: a share above ~30% of the mid pool, or cumulative conversations above ~100% of US-visible "
                      "buying units, means the scenario depends on non-US sponsors, higher volumes or expansion modules.")
    mk.column_dimensions["A"].width = 58
    for col in "BCDEFGHI":
        mk.column_dimensions[col].width = 18

    wb.save(path)
    return line_cells, unit_rows, (ind_row, acad_row, tot_row)


# ---------------------------------------------------------------------------------------------------------------
# Sensitivity (Python mirror, Bootstrapped Base)
# ---------------------------------------------------------------------------------------------------------------
SENS_KEYS = ["p_study", "studies", "r_cust", "r_pilot", "conv", "ret_cust", "h_study", "rate", "p_acad", "r_acad",
             "evals", "p_ent", "ent_new", "p_char", "r_char", "p_pilot"]


def sensitivity(st="Bootstrapped"):
    base = compute(st, "Base")
    b_rev = base["Total revenue"][4]
    b_cum = sum(base["EBITDA"])
    rows = []
    for k in SENS_KEYS:
        res = {}
        for sc in ("Conservative", "Optimistic"):
            ov = {k: P[k][3][st][sc]}
            o = compute(st, "Base", ov)
            res[sc] = (o["Total revenue"][4], sum(o["EBITDA"]))
        rows.append({"parameter": P[k][0], "key": k,
                     "low_value": P[k][3][st]["Conservative"], "base_value": P[k][3][st]["Base"],
                     "high_value": P[k][3][st]["Optimistic"],
                     "rev2031_low": round(res["Conservative"][0]), "rev2031_high": round(res["Optimistic"][0]),
                     "cum_ebitda_low": round(res["Conservative"][1]), "cum_ebitda_high": round(res["Optimistic"][1]),
                     "rev2031_swing": round(abs(res["Optimistic"][0] - res["Conservative"][0]))})
    rows.sort(key=lambda d: -d["rev2031_swing"])
    # two-way grid: study price x pilot->customer conversion (2031 revenue)
    grid = {"rows_p_study": [8000, 11000, 15000], "cols_r_cust": [0.25, 0.40, 0.50], "rev2031": []}
    for p in grid["rows_p_study"]:
        grid["rev2031"].append([round(compute(st, "Base", {"p_study": p, "r_cust": rc})["Total revenue"][4])
                                for rc in grid["cols_r_cust"]])
    # break-even: lowest study price at which Base cumulative 5-yr EBITDA + grants >= 0 (bisection)
    def cum_cash(p):
        return compute(st, "Base", {"p_study": p})["Cumulative cash - NO grants (lead case)"][4]
    lo, hi = 0.0, 200000.0
    be = None
    if cum_cash(hi) >= 0:
        for _ in range(60):
            mid = (lo + hi) / 2
            if cum_cash(mid) >= 0:
                hi = mid
            else:
                lo = mid
        be = round(hi)
    return {"structure": st, "base_rev2031": round(b_rev), "base_cum_ebitda": round(b_cum), "one_way": rows,
            "two_way_rev2031": grid, "breakeven_study_price_no_grants_cum_cash_2031": be}


def write_sensitivity_sheet(path, sens_b, sens_v):
    wb = load_workbook(path)
    sh = wb.create_sheet("Sensitivity")
    sh.append(["One-way sensitivity on the Base scenario: each parameter moved to its Conservative and Optimistic value "
               "with all others at Base. VALUES computed by build_financial_model.py (Python mirror of the sheet formulas)."])
    for sens in (sens_b, sens_v):
        sh.append([])
        sh.append([f"{sens['structure']} - Base: 2031 revenue {sens['base_rev2031']:,} ; cumulative 2027-31 EBITDA "
                   f"{sens['base_cum_ebitda']:,}"])
        sh.cell(sh.max_row, 1).font = Font(bold=True)
        sh.append(["Parameter", "Low value", "Base value", "High value", "2031 revenue (low)", "2031 revenue (high)",
                   "Swing", "Cum. EBITDA (low)", "Cum. EBITDA (high)"])
        for c in sh[sh.max_row]:
            c.font = Font(bold=True)
            c.fill = HDR
        for d in sens["one_way"]:
            fmt = lambda v: json.dumps(v) if isinstance(v, list) else v
            sh.append([d["parameter"], fmt(d["low_value"]), fmt(d["base_value"]), fmt(d["high_value"]), d["rev2031_low"],
                       d["rev2031_high"], d["rev2031_swing"], d["cum_ebitda_low"], d["cum_ebitda_high"]])
        g = sens["two_way_rev2031"]
        sh.append([])
        sh.append(["2031 revenue: study price (rows) x pilot->customer rate (columns)"] + [f"{c:.0%}" for c in g["cols_r_cust"]])
        sh.cell(sh.max_row, 1).font = Font(bold=True)
        for p, vals in zip(g["rows_p_study"], g["rev2031"]):
            sh.append([f"${p:,}"] + vals)
        be = sens["breakeven_study_price_no_grants_cum_cash_2031"]
        sh.append(["Study price at which Base cumulative cash WITHOUT grants reaches 0 by 2031",
                   "not reached below $200K" if be is None else be])
    sh.column_dimensions["A"].width = 64
    for col in "BCDEFGHI":
        sh.column_dimensions[col].width = 17
    wb.save(path)


# ---------------------------------------------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------------------------------------------
REF_RE = re.compile(r"(?:(?:'([^']+)'|([A-Za-z][\w&]*))!)?\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?")


def check_no_self_reference(path):
    from openpyxl.utils import column_index_from_string as ci
    wb = load_workbook(path)
    n = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    n += 1
                    for m in REF_RE.finditer(cell.value[1:]):
                        sheet = m.group(1) or m.group(2) or ws.title
                        if sheet != ws.title:
                            continue
                        c1, r1 = ci(m.group(3)), int(m.group(4))
                        c2, r2 = (ci(m.group(5)), int(m.group(6))) if m.group(5) else (c1, r1)
                        if c1 <= cell.column <= c2 and r1 <= cell.row <= r2:
                            raise AssertionError(f"self-reference in {ws.title}!{cell.coordinate}: {cell.value}")
    return n


XL_ERRORS = {"#DIV/0!", "#REF!", "#NAME?", "#VALUE!", "#N/A", "#NUM!", "#NULL!"}


def libreoffice_check(path, results, line_cells):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        return "LibreOffice not found - skipped recalculation check"
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "in.xlsx"
        shutil.copy(path, src)
        outdir = Path(td) / "out"
        subprocess.run([exe, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(outdir), str(src)],
                       check=True, capture_output=True, timeout=180)
        wb = load_workbook(outdir / "in.xlsx", data_only=True)
        errors = []
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and (cell.value.startswith("Err:") or cell.value in XL_ERRORS):
                        errors.append(f"{ws.title}!{cell.coordinate}={cell.value}")
        if errors:
            raise AssertionError("formula errors after recalculation: " + ", ".join(errors[:10]))
        worst = 0.0
        for (st, sc, name), rr in line_cells.items():
            ws = wb[f"P&L {st}"]
            exp = results[f"{st} — {sc}"][name]
            exp = exp if isinstance(exp, list) else [exp]
            for j, e in enumerate(exp):
                got = ws.cell(rr, 2 + j).value
                if got is None:
                    raise AssertionError(f"no cached value for {st}/{sc}/{name}/{j}")
                worst = max(worst, abs(got - e) / max(1.0, abs(e)))
        if worst > 1e-9:
            raise AssertionError(f"Excel/LibreOffice and Python mirror disagree (max rel diff {worst})")
        # keep the recalculated copy (formulas + cached values) so that readers without a calculation engine
        # (openpyxl data_only=True, previewers) see the numbers (review INV-13)
        shutil.copy(outdir / "in.xlsx", path)
        return (f"LibreOffice recalculation matches the Python mirror on {len(line_cells)} lines (max rel diff {worst:.1e}); "
                "workbook saved with cached values")


def main(path=HERE / "FINANCIAL_MODEL.xlsx"):
    path = Path(path)
    results = {f"{st} — {sc}": compute(st, sc) for st in STRUCTS for sc in SC}
    line_cells, _unit_rows, _mk = build_workbook(path)
    sens_b, sens_v = sensitivity("Bootstrapped"), sensitivity("Venture")
    write_sensitivity_sheet(path, sens_b, sens_v)
    nf = check_no_self_reference(path)
    print(f"{nf} formulas, no self-references")
    print(libreoffice_check(path, results, line_cells))

    keep = ["Total revenue"] + CORE_REV + ["Expansion-module revenue", "Paid pilots", "Non-GLP studies analysed",
                                             "Material characterisations", "Active study customers (year end)",
                                             "Active academic licences", "Active enterprise licences",
                                             "Implied delivery FTE", "Gross margin %", "EBITDA",
                                             "Cumulative cash - NO grants (lead case)",
                                             "Grant awards - CONDITIONAL, not operating cash",
                                             "Restricted grant project spend (incl. STTR subaward)",
                                             "Grant effect on operating cash IF awarded",
                                             "Cumulative cash - WITH grants IF awarded (conditional)",
                                             "Total revenue without licence revenue"]
    out = {}
    for k, v in results.items():
        d = {}
        for n in keep:
            if n == "Gross margin %":
                d[n] = [round(x, 2) for x in v[n]]
            elif n in ("Paid pilots", "Non-GLP studies analysed", "Material characterisations", "Implied delivery FTE",
                       "Active study customers (year end)", "Active academic licences", "Active enterprise licences"):
                d[n] = [round(x, 1) for x in v[n]]
            else:
                d[n] = [round(x) for x in v[n]]
        d["Equity funding requirement (max cumulative deficit)"] = [
            round(v["Equity funding requirement (max cumulative deficit)"]), None, None, None, None]
        d["Equity requirement WITH grants IF awarded (conditional)"] = [
            round(v["Equity requirement WITH grants IF awarded (conditional)"]), None, None, None, None]
        out[k] = d
    (HERE / "financial_model_outputs.json").write_text(json.dumps(out, indent=1, ensure_ascii=True) + "\n")
    (HERE / "revenue_model_sensitivity.json").write_text(
        json.dumps({"Bootstrapped": sens_b, "Venture": sens_v}, indent=1) + "\n")
    print("saved", path, "and JSON outputs")
    for k, v in out.items():
        print(f"{k:28s} rev {v['Total revenue']}  GM31 {v['Gross margin %'][4]:.0%}  "
              f"cash31 no-grants {v['Cumulative cash - NO grants (lead case)'][4]:,}  "
              f"with-grants {v['Cumulative cash - WITH grants IF awarded (conditional)'][4]:,}  "
              f"equity(no grants) {v['Equity funding requirement (max cumulative deficit)'][0]:,}  rev27 {v['Total revenue'][0]:,}")


if __name__ == "__main__":
    main()
