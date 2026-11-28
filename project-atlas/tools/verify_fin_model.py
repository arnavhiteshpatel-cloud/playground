#!/usr/bin/env python3
"""Recalculate a model workbook in LibreOffice (headless) and compare its Summary sheet to the Python mirror.

Usage: python3 tools/verify_fin_model.py 08_financial_models/<ID>_model.xlsx [...] | --all
Exit 0 if every compared metric matches within tolerance (max(1.0, 0.1%)).
"""
import json, pathlib, subprocess, sys, tempfile, shutil
from openpyxl import load_workbook

ROOT = pathlib.Path(__file__).resolve().parents[1]
FM = ROOT / "08_financial_models"
MAP = {  # Summary row label prefix -> python summary key
 "Year 1 revenue": "y1_revenue", "Year 2 revenue": "y2_revenue", "Year 3 revenue": "y3_revenue", "Year 5 revenue": "y5_revenue",
 "Year 1 operating profit": "y1_op", "Year 2 operating profit": "y2_op", "Year 3 operating profit": "y3_op", "Year 5 operating profit": "y5_op",
 "Year 1 free cash flow": "y1_fcf", "Year 3 free cash flow": "y3_fcf", "Year 5 free cash flow": "y5_fcf",
 "Active customers end of year 5": "y5_active_end", "Headcount end of year 5": "y5_headcount_end",
 "First month of positive operating profit": "breakeven_month", "Peak funding need": "peak_funding_need",
 "Minimum cash balance": "min_cash_balance", "Payback month": "payback_month",
 "First month op profit ≥ $10k": "first_month_op_10k", "Cumulative deployable capital by year 10": "lt_y10_cum_deployable",
 "Indicative enterprise value, year 10": "lt_y10_ev",
}


def recalc(xlsx):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="atlas_lo_"))
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(tmp), str(xlsx)],
                   check=True, capture_output=True, timeout=300)
    return tmp / xlsx.name, tmp


def verify(xlsx):
    xlsx = pathlib.Path(xlsx)
    oid = xlsx.name.replace("_model.xlsx", "")
    res = json.loads((FM / f"{oid}_results.json").read_text())
    out, tmp = recalc(xlsx)
    wb = load_workbook(out, data_only=True)
    ws = wb["Summary"]
    bad, n = [], 0
    for row in ws.iter_rows(min_row=4, values_only=True):
        label = row[0]
        if not label:
            continue
        key = next((v for k, v in MAP.items() if str(label).startswith(k)), None)
        if not key:
            continue
        for j, s in enumerate(["conservative", "base", "optimistic"]):
            xv = row[1 + j]; pv = res["scenarios"][s].get(key)
            if pv is None or isinstance(xv, str):
                continue
            n += 1
            if xv is None or abs(float(xv) - float(pv)) > max(1.0, abs(float(pv)) * 0.001):
                bad.append((label, s, xv, pv))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[{oid}] compared {n} values, mismatches {len(bad)}")
    for b in bad[:20]:
        print("   MISMATCH", b)
    return not bad and n > 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        args = [str(p) for p in sorted(FM.glob("*_model.xlsx"))]
    ok = all([verify(p) for p in args])
    sys.exit(0 if ok else 1)
