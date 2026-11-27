"""DefectFill Report generator (PDF via ReportLab + per-specimen CSV).

Input is a *bundle* dict (built from the study store or from experiment outputs):

  bundle = {
    "title", "study": {name, species, defect_model, graft_materials, blinded, glp_flag, sponsor},
    "data_class": "synthetic" | "public" | "customer",
    "review_status": "unreviewed_automated" | "reviewed",
    "specimens": [ {specimen_id, group, timepoint, scan:{source, sha256, shape, spacing_um, scanner,
                    acquisition}, qc:{verdict, checks}, roi:{...definition, definition_sha256, method,
                    confidence}, segmentation:{method, model_name, model_sha256, model_provenance},
                    corrections:[...], metrics:{class_volumes, ...}, uncertainty, plausibility,
                    figure: path } ],
    "endpoints": [ (key_path, label, unit) ],     # which metrics to tabulate / compare
    "reference_group": "...", "methods_text": "...", "limitations": [...],
    "reproducibility": {software_version, config_sha256, git_commit, ...},
    "reviewers": [...], "audit_excerpt": [...]
  }

Statistics are computed per group at the specimen level (never voxels); comparisons vs the
reference group use Welch t + Mann–Whitney with Holm adjustment and Hedges g with 95% CI;
n<5 per group triggers an explicit caution. No significance language is generated in prose.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

from xml.sax.saxutils import escape as esc   # neutralise ReportLab markup in user-supplied text (review S-04)

import numpy as np

from .. import __version__
from ..stats import describe, compare_two_groups, adjust_pvalues

BANNERS = {
    "synthetic": ("SYNTHETIC DATA — computational phantoms with known ground truth. "
                  "Not biological evidence. Not for study decisions."),
    "public": ("PUBLIC RESEARCH DATA — reanalysis of a publicly released dataset. "
               "Automated results; no expert ground truth available."),
    "customer": "CUSTOMER DATA — confidential.",
}
STATUS_BANNERS = {
    "unreviewed_automated": "UNREVIEWED AUTOMATED RESULT — research prototype output, not reviewed by a qualified analyst.",
    "reviewed": "REVIEWED — see sign-off section for reviewer identity and meaning of signature.",
}


def _get(d, path, default=float("nan")):
    cur = d
    for k in path.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur


def _per_animal(specimens, eps):
    """Collapse multiple scans of the same animal at the same timepoint to one mean value per
    endpoint (the animal is the experimental unit; review Q-05)."""
    by = {}
    for s in specimens:
        key = (s.get("animal_id") or s["specimen_id"], s.get("group", "—"), s.get("timepoint", "—"))
        by.setdefault(key, []).append(s)
    out = []
    for (aid, g, tp), ss in by.items():
        m = {}
        for k, _, _ in eps:
            vals = [_get(x["metrics"], k) for x in ss]
            vals = [v for v in vals if isinstance(v, (int, float)) and np.isfinite(v)]
            node = m
            parts = k.split(".")
            for p_ in parts[:-1]:
                node = node.setdefault(p_, {})
            node[parts[-1]] = float(np.mean(vals)) if vals else float("nan")
        out.append({"specimen_id": aid, "group": g, "timepoint": tp, "metrics": m, "n_scans": len(ss)})
    return out


def group_stats(bundle):
    eps = bundle["endpoints"]
    groups = {}
    for s in _per_animal(bundle["specimens"], eps):
        groups.setdefault((s.get("group", "—"), s.get("timepoint", "—")), []).append(s)
    table = []
    for (g, tp), ss in sorted(groups.items(), key=lambda x: (str(x[0][1]), str(x[0][0]))):
        row = {"group": g, "timepoint": tp, "n": len(ss)}
        for key, label, unit in eps:
            row[key] = describe([_get(s["metrics"], key) for s in ss])
        table.append(row)
    comps = []
    ref = bundle.get("reference_group")
    if ref:
        tps = sorted({k[1] for k in groups}, key=str)
        for tp in tps:
            if (ref, tp) not in groups:
                continue
            for (g, t2), ss in groups.items():
                if t2 != tp or g == ref:
                    continue
                for key, label, unit in eps:
                    a = [_get(s["metrics"], key) for s in ss]
                    b = [_get(s["metrics"], key) for s in groups[(ref, tp)]]
                    if len(a) >= 2 and len(b) >= 2:
                        c = compare_two_groups(a, b)
                        comps.append({"timepoint": tp, "group": g, "reference": ref, "endpoint": key, **c})
        if comps:
            adj = adjust_pvalues([c["welch_t"]["p"] for c in comps], "holm")
            for c, p in zip(comps, adj):
                c["p_holm"] = p
    return table, comps


def _csv_safe(v):
    """Neutralise spreadsheet formula injection (review S-19)."""
    if isinstance(v, str) and v[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + v
    return v


def _support(s: dict, key: str) -> str | None:
    """Measurement-support status of the endpoint that owns metric ``key`` (None when not assessed)."""
    from ..advisor.integration import ENDPOINT_METRICS
    ms = s.get("measurement_support") or {}
    if not ms:
        return None
    for ep, paths in ENDPOINT_METRICS.items():
        if any(key == p_ or key.startswith(p_ + ".") for p_ in paths):
            return (ms.get(ep) or {}).get("status")
    return "supported" if key.startswith("class_volumes.TV") or key.endswith("uncertain_fraction") else None


def _fmt_support(v, status):
    if status == "not_supported":
        return "n/m"
    t = _fmt(v)
    return t + " (c)" if status == "supported_with_conditions" else t


def write_csv(bundle, path):
    eps = bundle["endpoints"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["data_class", "review_status", "specimen_id", "group", "timepoint", "scan_sha256", "roi_sha256",
                    "segmentation_method", "model_sha256", "qc_verdict"] + [k for k, _, _ in eps]
                   + [f"{k}__support" for k, _, _ in eps])
        for s in bundle["specimens"]:
            w.writerow([_csv_safe(x) for x in [bundle["data_class"], bundle["review_status"], s["specimen_id"], s.get("group"), s.get("timepoint"),
                        _get(s, "scan.sha256", ""), _get(s, "roi.definition_sha256", ""),
                        _get(s, "segmentation.method", ""), _get(s, "segmentation.model_sha256", ""),
                        _get(s, "qc.verdict", "")] + [_get(s["metrics"], k) for k, _, _ in eps]
                        + [_support(s, k) or "not_assessed" for k, _, _ in eps]])


def _fmt(v, nd=3):
    if v is None:
        return "—"
    if isinstance(v, (float, np.floating)):
        if not np.isfinite(v):
            return "—"
        if abs(v) >= 1000 or (abs(v) < 0.001 and v != 0):
            return f"{v:.3g}"
        return f"{v:.{nd}f}"
    return str(v)


def build_pdf(bundle, pdf_path, csv_path=None, watermark: str | None = None) -> dict:
    """Render the report. ``watermark`` (optional) is drawn diagonally on every page, e.g. for
    reports produced by an unlicensed evaluation copy."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,
                                    KeepTogether)

    ss = getSampleStyleSheet()
    ACC = colors.HexColor("#1F4E79")
    H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=ACC, fontSize=17, spaceAfter=6)
    H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=ACC, fontSize=12.5, spaceBefore=10, spaceAfter=4)
    B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=8.8, leading=11.5)
    SM = ParagraphStyle("SM", parent=B, fontSize=7.4, leading=9.2, textColor=colors.HexColor("#333333"))
    BAN = ParagraphStyle("BAN", parent=B, textColor=colors.white, fontSize=8.6, leading=11)

    def banner(text, color):
        t = Table([[Paragraph(text, BAN)]], colWidths=[180 * mm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("BOX", (0, 0), (-1, -1), 0, color),
                               ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        return t

    def table(data, widths=None, fs=7.4, header=True):
        rows = [[Paragraph(esc(str(c)), SM) if isinstance(c, str) else c for c in r] for r in data]
        t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
        st = [("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#BBBBBB")),
              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), fs),
              ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
        if header:
            st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5"))]
        t.setStyle(TableStyle(st))
        return t

    gen_time = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    st = bundle["study"]
    flow = []
    flow.append(Paragraph("OsteoQuant · DefectFill Report", ParagraphStyle("k", parent=SM, textColor=ACC)))
    flow.append(Paragraph(esc(bundle["title"]), H1))
    flow.append(banner(BANNERS[bundle["data_class"]], colors.HexColor("#8B1E1E" if bundle["data_class"] == "synthetic"
                                                                         else "#7A5B00" if bundle["data_class"] == "public"
                                                                         else "#1F4E79")))
    flow.append(Spacer(1, 3))
    flow.append(banner(STATUS_BANNERS[bundle["review_status"]], colors.HexColor("#444444")))
    if any("synthetic" in str(_get(s, "segmentation.model_provenance", "")) for s in bundle["specimens"]):
        flow.append(Spacer(1, 3))
        flow.append(banner("SYNTHETIC-TRAINED MODEL used for segmentation — research prototype, not validated on real tissue.",
                           colors.HexColor("#8B1E1E")))
    flow.append(Spacer(1, 3))
    flow.append(banner("Research use only. Not a medical device. Not validated for GLP studies (21 CFR 58 / OECD GLP). "
                       "No claim of 21 CFR Part 11 compliance.", colors.HexColor("#555555")))
    flow.append(Spacer(1, 6))

    # ----------------------------------------------------------- 1 overview
    flow.append(Paragraph("1. Study overview", H2))
    ov = [["Field", "Value"], ["Study", st.get("name", "")], ["Species / model", f"{st.get('species','')} · {st.get('defect_model','')}"],
          ["Graft material(s)", st.get("graft_materials", "")], ["Groups", ", ".join(sorted({str(s.get('group')) for s in bundle['specimens']}))],
          ["Timepoints", ", ".join(sorted({str(s.get('timepoint')) for s in bundle['specimens']}))],
          ["Specimens", str(len(bundle["specimens"]))], ["Blinded analysis", "yes" if st.get("blinded") else "no"],
          ["Data class", bundle["data_class"]], ["Generated", gen_time], ["Software", f"OsteoQuant {__version__}"]]
    flow.append(table(ov, [45 * mm, 135 * mm]))
    if bundle.get("summary_text"):
        flow.append(Spacer(1, 4))
        flow.append(Paragraph(bundle["summary_text"], B))

    # ----------------------------------------------------------- 2 methods
    flow.append(Paragraph("2. Analysis methods", H2))
    flow.append(Paragraph(bundle.get("methods_text", ""), B))
    eps = bundle["endpoints"]
    flow.append(Spacer(1, 3))
    flow.append(table([["Endpoint", "Unit", "Definition key"]] + [[l, u, k] for k, l, u in eps], [70 * mm, 25 * mm, 85 * mm]))

    # ----------------------------------------------------------- 3 group results
    gt, comps = group_stats(bundle)
    flow.append(Paragraph("3. Group summaries (animal-level: repeated scans of an animal are averaged; mean ± SD [95% CI])", H2))
    hdr = ["Group", "Timepoint", "n"] + [l for _, l, _ in eps[:5]]
    rows = [hdr]
    for r in gt:
        cells = [str(r["group"]), str(r["timepoint"]), str(r["n"])]
        for k, _, _ in eps[:5]:
            d = r[k]
            if d.get("n", 0) >= 2:
                cells.append(f"{_fmt(d['mean'])} ± {_fmt(d['sd'])}\n[{_fmt(d['ci95_low'])}, {_fmt(d['ci95_high'])}]")
            elif d.get("n", 0) == 1:
                cells.append(_fmt(d["mean"]))
            else:
                cells.append("—")
        rows.append(cells)
    flow.append(table(rows))
    if any(r["n"] < 5 for r in gt):
        flow.append(Paragraph("<b>Caution:</b> one or more groups have n &lt; 5 specimens; confidence intervals are wide "
                              "and hypothesis tests have low power.", SM))
    if comps:
        flow.append(Spacer(1, 4))
        flow.append(Paragraph("Comparisons vs reference group (Welch t-test; Holm-adjusted across all comparisons; "
                              "Hedges g with approximate 95% CI). Reported for transparency; interpretation requires a "
                              "pre-specified analysis plan.", SM))
        crow = [["Timepoint", "Group vs ref", "Endpoint", "Mean diff", "Hedges g [95% CI]", "p (Welch)", "p (Holm)"]]
        for c in comps[:30]:
            hg = c["hedges_g"]
            crow.append([str(c["timepoint"]), f"{c['group']} vs {c['reference']}", c["endpoint"], _fmt(c["mean_diff"]),
                         f"{_fmt(hg['g'],2)} [{_fmt(hg.get('ci95_low'),2)}, {_fmt(hg.get('ci95_high'),2)}]",
                         _fmt(c["welch_t"]["p"]), _fmt(c["p_holm"])])
        flow.append(table(crow))
    for fig in bundle.get("group_figures", []):
        flow.append(Spacer(1, 4))
        flow.append(Image(fig, width=175 * mm, height=175 * mm * 0.42))

    # ----------------------------------------------------------- 4 per specimen
    flow.append(PageBreak())
    flow.append(Paragraph("4. Per-specimen results", H2))
    rows = [["Specimen", "Group", "TP", "QC"] + [l for _, l, _ in eps[:6]]]
    for s in bundle["specimens"]:
        rows.append([str(s["specimen_id"]), str(s.get("group")), str(s.get("timepoint")), _get(s, "qc.verdict", "—")] +
                    [_fmt_support(_get(s["metrics"], k), _support(s, k)) for k, _, _ in eps[:6]])
    flow.append(table(rows))
    if any("truth" in s for s in bundle["specimens"]):
        flow.append(Spacer(1, 4))
        flow.append(Paragraph("Ground truth (synthetic phantoms only): measured vs known-by-construction values.", SM))
        rows = [["Specimen", "New bone frac (meas / true)", "Graft frac (meas / true)", "Segmentation Dice new / graft"]]
        for s in bundle["specimens"]:
            if "truth" in s:
                rows.append([str(s["specimen_id"]),
                             f"{_fmt(_get(s['metrics'],'class_volumes.new_bone_fraction'))} / {_fmt(s['truth'].get('new_bone_fraction'))}",
                             f"{_fmt(_get(s['metrics'],'class_volumes.residual_graft_fraction'))} / {_fmt(s['truth'].get('graft_fraction'))}",
                             f"{_fmt(_get(s,'eval.dice_new'))} / {_fmt(_get(s,'eval.dice_graft'))}"])
        flow.append(table(rows))

    # ----------------------------------------------------------- 5 representative images
    figs = [s for s in bundle["specimens"] if s.get("figure")]
    if figs:
        flow.append(Paragraph("5. Representative images", H2))
        flow.append(Paragraph("Orthogonal mid-ROI slices with segmentation overlay (orange new bone, blue residual graft, "
                              "pink host bone, yellow uncertain) and ROI outline. Scale bar shown in each panel.", SM))
        for s in figs[: bundle.get("max_figures", 4)]:
            flow.append(KeepTogether([Paragraph(esc(f"Specimen {s['specimen_id']} — {s.get('group')} · {s.get('timepoint')}"), SM),
                                      Image(s["figure"], width=175 * mm, height=175 * mm * 0.36)]))

    # ----------------------------------------------------------- 6 imaging / QC / ROI / segmentation provenance
    flow.append(PageBreak())
    flow.append(Paragraph("6. Imaging metadata, quality control and ROI definitions", H2))
    rows = [["Specimen", "Source / SHA-256 (first 16)", "Voxel (µm)", "Shape", "QC verdict", "Warnings"]]
    for s in bundle["specimens"]:
        warns = [c["name"] for c in _get(s, "qc.checks", []) if c.get("status") in ("warn", "fail")] if isinstance(_get(s, "qc.checks", []), list) else []
        rows.append([str(s["specimen_id"]), f"{_get(s,'scan.source','')}\n{str(_get(s,'scan.sha256',''))[:16]}",
                     _fmt(_get(s, "scan.spacing_um", [float('nan')])[0] if isinstance(_get(s, "scan.spacing_um", None), list) else _get(s, "scan.spacing_um")),
                     "×".join(map(str, _get(s, "scan.shape", []))) if isinstance(_get(s, "scan.shape", None), list) else "",
                     _get(s, "qc.verdict", "—"), "; ".join(warns[:4])])
    flow.append(table(rows, [22 * mm, 45 * mm, 16 * mm, 24 * mm, 18 * mm, 55 * mm]))
    flow.append(Paragraph("QC checks marked 'heuristic' use developer-chosen thresholds and are not established standards.", SM))
    rows = [["Specimen", "ROI type / method", "Parameters (µm)", "Confidence", "Definition SHA-256 (first 16)"]]
    for s in bundle["specimens"]:
        r = s.get("roi", {})
        p = r.get("params", {})
        pstr = ", ".join(f"{k}={_fmt(v,1) if not isinstance(v, list) else '[' + ','.join(_fmt(x,1) for x in v) + ']'}"
                         for k, v in p.items() if not k.startswith("_"))
        rows.append([str(s["specimen_id"]), f"{r.get('kind','')} / {r.get('method','')}", pstr, _fmt(r.get("confidence"), 2),
                     str(r.get("definition_sha256", ""))[:16]])
    flow.append(table(rows, [22 * mm, 30 * mm, 80 * mm, 16 * mm, 32 * mm]))
    rows = [["Specimen", "Segmentation", "Model / SHA-256 (first 16)", "Model provenance", "Abstained (ROI)", "Plausibility failures"]]
    for s in bundle["specimens"]:
        pf = [p["check"] for p in s.get("plausibility", []) if not p.get("ok", True)]
        rows.append([str(s["specimen_id"]), _get(s, "segmentation.method", ""),
                     f"{_get(s,'segmentation.model_name','—')}\n{str(_get(s,'segmentation.model_sha256',''))[:16]}",
                     str(_get(s, "segmentation.model_provenance", "—")), _fmt(_get(s, "uncertainty.abstained_frac_roi")),
                     "; ".join(pf) or "none"])
    flow.append(table(rows, [22 * mm, 28 * mm, 40 * mm, 25 * mm, 20 * mm, 45 * mm]))

    # ----------------------------------------------------------- 7 corrections / audit
    flow.append(Paragraph("7. Human correction history and audit excerpt", H2))
    corr = [(s["specimen_id"], c) for s in bundle["specimens"] for c in s.get("corrections", [])]
    if corr:
        rows = [["Specimen", "Version", "User", "Time", "Edit summary"]]
        for sid, c in corr:
            rows.append([str(sid), str(c.get("version")), str(c.get("user")), str(c.get("time")), json.dumps(c.get("summary"))[:120]])
        flow.append(table(rows))
    else:
        flow.append(Paragraph("No manual corrections were recorded for this report.", B))
    if bundle.get("audit_excerpt"):
        rows = [["Seq", "Time", "User", "Action", "Object", "Row hash (first 12)"]]
        for e in bundle["audit_excerpt"][:25]:
            rows.append([str(e["seq"]), e["ts"][:19], str(e.get("user_id")), e["action"], f"{e.get('object_type')}:{e.get('object_id')}",
                         e["row_hash"][:12]])
        flow.append(table(rows))

    # ----------------------------------------------------------- exceptions
    if bundle.get("exceptions"):
        flow.append(Paragraph("Exceptions (specimens not analysed automatically)", H2))
        rows = [["Specimen", "Stage", "Reason", "Required action"]]
        for e in bundle["exceptions"]:
            rows.append([str(e.get("specimen_id")), str(e.get("stage")), str(e.get("reason")), str(e.get("action"))])
        flow.append(table(rows, [25 * mm, 25 * mm, 75 * mm, 55 * mm]))

    # ----------------------------------------------------------- measurement support (status, conditions)
    flow.append(Paragraph("Measurement support (identifiability) per specimen", H2))
    flow.append(Paragraph(
        "Each endpoint is classified by the measurement-support advisor before it is reported: <b>supported</b>, "
        "<b>supported with conditions</b> (values marked '(c)'; the conditions below are part of the result) or "
        "<b>not supported</b> (shown as 'n/m' = not measured; raw values are retained in the audit record only). "
        "Evidence stage of the advisor and models: computational (stage A of the validation programme) — no physical "
        "or in-vivo validation of graft/new-bone separation has been performed.", SM))
    sup_rows = []
    for s_ in bundle["specimens"]:
        ms = s_.get("measurement_support") or {}
        if not ms:
            sup_rows.append([str(s_.get("specimen_id")), "all", "not assessed",
                             Paragraph("analysis predates the measurement-support advisor; treat graft/new-bone "
                                       "values as unassessed", SM)])
            continue
        for ep, d in ms.items():
            if d.get("status") == "supported":
                continue
            text = d.get("reason", "") or ""
            if d.get("conditions"):
                text += " Conditions: " + "; ".join(d["conditions"])
            sup_rows.append([str(s_.get("specimen_id")), ep.replace("_", " "),
                             "conditional" if d.get("status") == "supported_with_conditions" else "not measured",
                             Paragraph(esc(text), SM)])
    if sup_rows:
        flow.append(table([["Specimen", "Endpoint", "Status", "Reason / conditions"]] + sup_rows,
                          [22 * mm, 38 * mm, 22 * mm, 98 * mm]))
    else:
        flow.append(Paragraph("All reported endpoints are supported for all specimens.", SM))
    par_rows = []
    for s_ in bundle["specimens"]:
        ap = s_.get("analysis_parameters") or {}
        if ap:
            par_rows.append([str(s_.get("specimen_id")), str(ap.get("method", "")),
                             _fmt(ap.get("t_mineral")), _fmt(ap.get("t_graft")),
                             _fmt(ap.get("estimated_graft_share")),
                             str(s_.get("advisor_version") or ap.get("advisor_version") or "—")])
    if par_rows:
        flow.append(Paragraph("Analysis parameters (grey-value thresholds are in the scan's units)", SM))
        flow.append(table([["Specimen", "Method", "Mineral thr.", "Graft thr.", "Graft share", "Advisor"]] + par_rows,
                          [25 * mm, 35 * mm, 25 * mm, 25 * mm, 25 * mm, 25 * mm]))

    # ----------------------------------------------------------- 8 limitations
    flow.append(Paragraph("8. Scientific limitations and exceptions", H2))
    for l in bundle.get("limitations", []):
        flow.append(Paragraph("• " + l, B))

    # ----------------------------------------------------------- 9 reproducibility
    flow.append(Paragraph("9. Reproducibility", H2))
    rep = bundle.get("reproducibility", {})
    flow.append(table([["Item", "Value"]] + [[k, str(v)] for k, v in rep.items()], [55 * mm, 125 * mm]))

    # ----------------------------------------------------------- 10 sign-off
    flow.append(Paragraph("10. Review and sign-off", H2))
    revs = bundle.get("reviewers", [])
    rows = [["Role", "Name", "Meaning of signature", "Decision", "Date/time (UTC)"]]
    for r in revs:
        rows.append([r.get("role", ""), r.get("name", ""), r.get("meaning", ""), r.get("decision", ""), r.get("time", "")])
    for role in ("Analyst", "Scientific reviewer", "Study director / sponsor representative"):
        if not any(r.get("role") == role for r in revs):
            rows.append([role, "", "", "", ""])
    flow.append(table(rows, [38 * mm, 35 * mm, 60 * mm, 20 * mm, 27 * mm]))
    flow.append(Paragraph("Blank fields indicate the report has not been signed. Electronic signatures in OsteoQuant are "
                          "recorded in the hash-chained audit trail; this prototype has not been validated as a "
                          "Part 11 electronic-signature system.", SM))

    def on_page(c, d):
        c.saveState()
        if watermark:
            c.saveState()
            c.setFillColor(colors.Color(0.55, 0.1, 0.1, alpha=0.16))
            c.setFont("Helvetica-Bold", 30)
            c.translate(105 * mm, 148 * mm)
            c.rotate(45)
            c.drawCentredString(0, 0, watermark[:60])
            c.restoreState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#666666"))
        c.drawString(15 * mm, 10 * mm, f"OsteoQuant DefectFill · {bundle['title'][:70]} · {bundle['data_class'].upper()} · "
                                       f"{bundle['review_status']}")
        c.drawRightString(195 * mm, 10 * mm, f"page {d.page}")
        c.restoreState()

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=14 * mm,
                            bottomMargin=16 * mm, title=bundle["title"], author="OsteoQuant research prototype")
    doc.build(flow, onFirstPage=on_page, onLaterPages=on_page)
    if csv_path:
        write_csv(bundle, csv_path)
    h = hashlib.sha256(Path(pdf_path).read_bytes()).hexdigest()
    return {"pdf": str(pdf_path), "csv": str(csv_path) if csv_path else None, "pdf_sha256": h}
