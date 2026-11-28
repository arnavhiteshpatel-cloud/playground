#!/usr/bin/env python3
"""Consolidate Stage D/E data files into deliverable databases.

Inputs : 09_databases/prospects/<ID>_prospects.csv, 09_databases/suppliers/<ID>_suppliers.csv,
         09_databases/sources.jsonl, 09_databases/opportunities.jsonl, 03_screening/stage_C_selected.json
Outputs: 10_deliverables/Atlas_Supplier_Partner_Database.xlsx (+ 09_databases/suppliers_all.csv)
         10_deliverables/Atlas_Customer_Prospect_Database.xlsx (+ 09_databases/prospects_all.csv)
         10_deliverables/Atlas_Commercial_Evidence_Database.xlsx (A/B/C evidence, claim→source map)
         09_databases/risk_register.csv (failure modes/risks for Stage C+ records)
"""
import csv, json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter as L

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, OUT = ROOT / "09_databases", ROOT / "10_deliverables"
HDR = PatternFill("solid", fgColor="1F3864"); HF = Font(bold=True, color="FFFFFF")


def read_csvs(folder, suffix):
    rows = []
    for p in sorted((DB / folder).glob(f"*_{suffix}.csv")) if (DB / folder).exists() else []:
        oid = p.name.replace(f"_{suffix}.csv", "")
        with p.open(encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f):
                r = {k.strip(): (v or "").strip() for k, v in r.items() if k}
                r["opportunity_id"] = oid
                rows.append(r)
    return rows


def sheet(wb, title, rows, cols, widths=None, table=True):
    ws = wb.create_sheet(title[:31])
    for j, c in enumerate(cols, 1):
        cell = ws.cell(row=1, column=j, value=c); cell.fill = HDR; cell.font = HF
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(rows, 2):
        for j, c in enumerate(cols, 1):
            v = r.get(c)
            if isinstance(v, (list, dict)):
                v = json.dumps(v, ensure_ascii=False)
            ws.cell(row=i, column=j, value=(str(v)[:32000] if v is not None else None))
    if table and rows:
        t = Table(displayName="".join(ch for ch in title if ch.isalnum())[:30] or "T",
                  ref=f"A1:{L(len(cols))}{len(rows)+1}")
        t.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
        ws.add_table(t)
    ws.freeze_panes = "B2"
    for j in range(1, len(cols) + 1):
        ws.column_dimensions[L(j)].width = (widths or {}).get(cols[j - 1], 24)
    return ws


def write_csv(path, rows, cols):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    readme = lambda wb, lines: [wb.active.cell(row=i + 1, column=1, value=t) for i, t in enumerate(lines)]
    # suppliers
    sup = read_csvs("suppliers", "suppliers")
    scols = ["opportunity_id", "organization", "website", "categories", "program_or_page_url", "geography",
             "qualification_requirements", "published_pricing_or_terms", "restrictions", "accessibility",
             "evidence_level", "follow_up_questions"]
    scols += [c for c in dict.fromkeys(k for r in sup for k in r) if c not in scols]
    wb = Workbook(); wb.active.title = "README"
    readme(wb, ["Project Atlas — Supplier & Partner Database",
                "accessibility = 'documented' (published program/criteria) or 'assumed' (requires direct confirmation).",
                "No supplier has been contacted. Nothing here implies a supplier will work with the founder.",
                f"{len(sup)} rows across {len({r['opportunity_id'] for r in sup})} opportunities."])
    sheet(wb, "Suppliers", sup, scols, {"organization": 30, "qualification_requirements": 50, "follow_up_questions": 50})
    wb.save(OUT / "Atlas_Supplier_Partner_Database.xlsx"); write_csv(DB / "suppliers_all.csv", sup, scols)
    # prospects
    pro = read_csvs("prospects", "prospects")
    pcols = ["opportunity_id", "organization", "industry", "city", "county", "website", "public_phone_or_contact_page",
             "characteristics", "likely_need", "decision_maker_role", "acquisition_channel", "qualification_rationale",
             "evidence_source_url", "status"]
    pcols += [c for c in dict.fromkeys(k for r in pro for k in r) if c not in pcols]
    wb = Workbook(); wb.active.title = "README"
    readme(wb, ["Project Atlas — Customer Prospect Database",
                "Every row is a PROSPECT identified from public business information — not a lead, not a customer.",
                "No organization has been contacted. Use only for founder-approved outreach that complies with law (CAN-SPAM, TCPA).",
                f"{len(pro)} rows across {len({r['opportunity_id'] for r in pro})} opportunities."])
    sheet(wb, "Prospects", pro, pcols, {"organization": 32, "qualification_rationale": 50, "characteristics": 40})
    wb.save(OUT / "Atlas_Customer_Prospect_Database.xlsx"); write_csv(DB / "prospects_all.csv", pro, pcols)
    # evidence database
    srcs = [json.loads(l) for l in (DB / "sources.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    opps = {json.loads(l)["id"]: json.loads(l) for l in (DB / "opportunities.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    sel = set(json.loads((ROOT / "03_screening/stage_C_selected.json").read_text())) if (ROOT / "03_screening/stage_C_selected.json").exists() else set()
    claims = []
    for s in srcs:
        for oid in (s.get("opportunity_ids") or []):
            claims.append({"opportunity_id": oid, "opportunity_title": (opps.get(oid) or {}).get("title"),
                           "in_stage_C": "yes" if oid in sel else "", "claim": s.get("claim"),
                           "evidence_level": s.get("evidence_level"), "source_id": s.get("source_id"),
                           "organization": s.get("organization"), "url": s.get("url"),
                           "publication_date": s.get("publication_date"), "access_date": s.get("access_date"),
                           "excerpt": s.get("excerpt"), "limitations": s.get("limitations")})
    strong = [s for s in srcs if s.get("evidence_level") in ("A", "B")]
    wb = Workbook(); wb.active.title = "README"
    lv = {k: sum(1 for s in srcs if s.get("evidence_level") == k) for k in "ABCDE"}
    readme(wb, ["Project Atlas — Commercial Evidence Database",
                f"{len(srcs)} sources: " + ", ".join(f"{k}={v}" for k, v in lv.items()),
                "Claim_Map: one row per (source, opportunity) claim. Strong_Evidence: A/B sources only.",
                "Levels: A direct commercial evidence · B strong documentation · C industry evidence · D proxy · E assumption.",
                "Verified facts are the claims themselves as stated by the source; calculations and estimates live in the models."])
    sheet(wb, "Claim_Map", claims, list(claims[0].keys()) if claims else ["opportunity_id"],
          {"claim": 60, "excerpt": 50, "opportunity_title": 40, "url": 40})
    sheet(wb, "Strong_Evidence", strong, ["source_id", "evidence_level", "organization", "title", "url", "publication_date",
                                         "access_date", "claim", "excerpt", "limitations", "opportunity_ids"],
          {"claim": 60, "excerpt": 50, "title": 40, "url": 40})
    wb.save(OUT / "Atlas_Commercial_Evidence_Database.xlsx")
    # risk register
    risks = []
    for oid in sorted(sel):
        o = opps.get(oid) or {}
        for k, typ in (("failure_modes", "failure mode"), ("operational_risks", "operational"),
                       ("financial_risks", "financial"), ("regulatory_barriers", "regulatory")):
            v = o.get(k)
            items = v if isinstance(v, list) else [v] if v else []
            for it in items:
                risks.append({"opportunity_id": oid, "title": o.get("title"), "risk_type": typ, "risk": it,
                              "stage_recorded": "A", "status": "open"})
    write_csv(DB / "risk_register.csv", risks, ["opportunity_id", "title", "risk_type", "risk", "stage_recorded", "status"])
    print(f"suppliers={len(sup)} prospects={len(pro)} sources={len(srcs)} claims={len(claims)} risks={len(risks)}")


if __name__ == "__main__":
    main()
