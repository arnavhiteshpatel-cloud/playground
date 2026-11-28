"""Build deliverables/OsteoQuant_Master_Workbook.xlsx from project files (no hand-typed results).

Sheets: README · Experiments · Benchmarks · Datasets · Competitors · Prospects · Funding · Collaborators ·
Phantom_BOM · Financial_Summary · Blockers · Remaining_Work, plus Generation-2 sheets: Advisor_Validation ·
Longitudinal_L3 · Transfer · Uncertainty_U1 · Runtime_O2 · Scorecard · Forensic_Audit · Baseline_Comparison ·
Founder_Decisions · Risks · Defects · QA_Defects · Reviews · Traceability · Datasets_R2 · Competitor_Matrix · Patents ·
Model_Registry
"""
import csv
import json
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "experiments" / "results"
HDR = PatternFill("solid", fgColor="DCE6F1")


def load(name):
    p = R / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else None


def sheet(wb, title, header, rows, widths=None):
    ws = wb.create_sheet(title[:31])
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HDR
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append([("" if v is None else (round(v, 4) if isinstance(v, float) else v)) for v in r])
    for i, h in enumerate(header, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, min(60, max(12, len(str(h)) + 4)))
    ws.freeze_panes = "A2"
    return ws


def csv_sheet(wb, title, path, keep=None):
    p = ROOT / path
    if not p.exists():
        return
    rows = list(csv.reader(open(p, newline="", encoding="utf-8")))
    if not rows:
        return
    hdr = rows[0]
    idx = [hdr.index(k) for k in keep if k in hdr] if keep else list(range(len(hdr)))
    sheet(wb, title, [hdr[i] for i in idx], [[r[i] if i < len(r) else "" for i in idx] for r in rows[1:]],
          {hdr[i]: 30 for i in idx})


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    for line in ["OsteoQuant master workbook — generated from repository files by scripts/build_master_spreadsheet.py",
                 "Experiment numbers are read from experiments/results/*.json. Synthetic results are labelled SYNTHETIC.",
                 "Prices, market sizes and financials are hypotheses unless labelled [V].",
                 "Evidence labels: [V] verified · [RF] research finding · [CC] company claim · [AE] analyst estimate · [HYP] hypothesis · [UNR] unresolved."]:
        ws.append([line])
    ws.column_dimensions["A"].width = 120

    reg = (ROOT / "EXPERIMENT_REGISTRY.md").read_text() if (ROOT / "EXPERIMENT_REGISTRY.md").exists() else ""
    exp_rows = []
    for m in re.finditer(r"^\| \*\*(\w+)\*\* \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", reg, re.M):
        exp_rows.append(list(m.groups()))
    sheet(wb, "Experiments", ["ID", "Question / hypothesis", "Data", "Status", "Key result", "Result file"], exp_rows,
          {"Question / hypothesis": 50, "Key result": 70, "Data": 30, "Result file": 30})

    bench = []
    a = load("exp_A_baselines")
    if a:
        for m, v in a["summary"].items():
            bench.append(["A", "SYNTHETIC test (16)", m, "graft Dice (ROI)", v["dice_graft"]["mean"], v["dice_graft"]["ci95"][0], v["dice_graft"]["ci95"][1]])
            bench.append(["A", "SYNTHETIC test (16)", m, "new-bone Dice (ROI)", v["dice_new_bone"]["mean"], v["dice_new_bone"]["ci95"][0], v["dice_new_bone"]["ci95"][1]])
    b = load("exp_B_unet")
    if b:
        for name, mdl in b["models"].items():
            for k in ("dice_new_roi", "dice_graft_roi", "dice_host_all", "ece_roi", "hd95_graft_um"):
                s = mdl["summary"][k]
                bench.append(["B", "SYNTHETIC test (16)", name, k, s["mean"], s["ci95"][0], s["ci95"][1]])
    c2 = load("exp_C2_ablation")
    if c2:
        for r in c2["rows"]:
            if "bayes" in r["features"]:
                continue   # superseded accuracy-optimal rule (review Q-01); oracle rows kept
            bench.append(["C2", f"SYNTHETIC overlap regime, {r['morphology']}", f"RF features={r['features']}", "graft Dice", r["dice_graft"], None, None])
    for name in ("exp_L_longitudinal", "exp_L2_strutlike"):
        L = load(name)
        if L:
            for k, v in L["summary"].items():
                if "bayes" in k:
                    continue
                bench.append([name.split("_")[1], "SYNTHETIC", k, "graft Dice", v["dice_graft"], None, None])
    g = load("exp_G_morphometry")
    if g:
        for k, v in g["agreement_vs_ipl"].items():
            bench.append(["G", "REAL public trabecular cubes vs Scanco IPL (n=8)", k, "ICC(2,1)", v["icc_2_1"]["icc"], v["icc_2_1"]["ci95_low"], v["icc_2_1"]["ci95_high"]])
            bench.append(["G", "REAL public trabecular cubes vs Scanco IPL (n=8)", k, "mean relative error", v["mean_rel_error"], None, None])
    for name, key in (("exp_H_I_real", "summary"),):
        h = load(name)
        if h:
            for m, v in h[key].items():
                bench.append(["H/I", "REAL dog forelimb micro-CT test (5)", m, "bone Dice", v["dice"], None, None])
    j = load("exp_J_adaptation")
    if j:
        for r in j["rows"]:
            bench.append(["J", "SYNTHETIC held-out materials (16)", f"{r['arm']} k={r['k']} rep={r['rep']}", "graft Dice", r["dice_graft"], None, None])
    k = load("exp_K_M_uncertainty")
    if k:
        bench.append(["K", "SYNTHETIC ID vs OOD", "scan mean entropy", "AUROC ID vs OOD", k["auroc_entropy_id_vs_ood"], None, None])
        for r in k["risk_coverage_id"]:
            bench.append(["K", "SYNTHETIC ID", f"coverage {r['coverage']}", "accuracy (retained)", r["accuracy"], None, None])
    f = load("exp_F_roi")
    if f:
        for m, v in f["summary"].items():
            bench.append(["F", "SYNTHETIC ROI", m, "ROI Dice mean", v["dice_mean"], v["dice_min"], None])
    n = load("exp_N_histology")
    if n and isinstance(n.get("N3"), dict) and n["N3"].get("mean_object_f1") is not None:
        bench.append(["N3", "REAL NuInsSeg H&E nuclei (60 held-out)", "classical nuclei", "pixel Dice", n["N3"]["mean_pixel_dice"], None, None])
        bench.append(["N3", "REAL NuInsSeg H&E nuclei (60 held-out)", "classical nuclei", "object F1@IoU0.5", n["N3"]["mean_object_f1"], None, None])
    o = load("exp_O_performance")
    if o:
        for s, v in o["stages"].items():
            bench.append(["O", "REAL ovine TXM / knee DICOM", s, "seconds", v.get("seconds"), None, None])
            bench.append(["O", "REAL ovine TXM / knee DICOM", s, "peak RSS MB", v.get("peak_rss_mb"), None, None])
    sheet(wb, "Benchmarks", ["Exp", "Data", "Method / condition", "Metric", "Value", "CI low / min", "CI high"], bench,
          {"Data": 40, "Method / condition": 45})

    csv_sheet(wb, "Competitors", "docs/research/competitors.csv")
    man = json.loads((ROOT / "data/manifest/datasets.json").read_text()) if (ROOT / "data/manifest/datasets.json").exists() else []
    sheet(wb, "Datasets", ["slug", "name", "doi", "license", "commercial_use", "species", "site", "modality", "voxel_um", "labels",
                           "size_bytes", "priority", "url"],
          [[d.get(k) if not isinstance(d.get(k), (list, dict)) else json.dumps(d.get(k))[:200] for k in
            ("slug", "name", "doi", "license", "commercial_use", "species", "site", "modality", "voxel_um", "labels", "size_bytes",
             "priority", "url")] for d in man], {"name": 40, "labels": 40, "url": 50})
    csv_sheet(wb, "Prospects", "business/prospects.csv")
    csv_sheet(wb, "Funding", "grants/funding_opportunities.csv")
    csv_sheet(wb, "Collaborators", "outreach/collaborators.csv")
    csv_sheet(wb, "Phantom_BOM", "validation/BILL_OF_MATERIALS.csv")
    fm = ROOT / "business" / "financial_model_outputs.json"
    if fm.exists():
        F = json.loads(fm.read_text())
        rows = []
        for scen, lines in F.items():
            for line, vals in lines.items():
                rows.append([scen, line] + list(vals))
        sheet(wb, "Financial_Summary", ["Structure — scenario", "Line", "2027", "2028", "2029", "2030", "2031"], rows,
              {"Structure — scenario": 32, "Line": 48})
    for title, path in (("Blockers", "BLOCKERS.md"), ("Remaining_Work", "REMAINING_WORK.md")):
        p = ROOT / path
        if p.exists():
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in p.read_text().splitlines()
                    if l.startswith("|") and not set(l.replace("|", "").strip()) <= set("-: ")]
            if rows:
                sheet(wb, title, rows[0], rows[1:], {h: 40 for h in rows[0]})
    gen2_sheets(wb)
    out = ROOT / "deliverables" / "OsteoQuant_Master_Workbook.xlsx"
    out.parent.mkdir(exist_ok=True)
    wb.save(out)
    print("saved", out, [s.title for s in wb.worksheets])


def md_rows(path):
    """All Markdown table rows in a file (separator rows dropped); header = first row of the first table."""
    p = ROOT / path
    if not p.exists():
        return []
    rows = []
    for line in p.read_text().splitlines():
        if line.strip().startswith("|"):
            cells = [c.strip().replace("**", "").replace("`", "") for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
                continue
            rows.append(cells)
    return rows


def md_sheet(wb, title, path, first_only=True):
    rows = md_rows(path)
    if not rows:
        return
    hdr = rows[0]
    body = []
    for r in rows[1:]:
        if first_only and r == hdr:
            continue
        if first_only and len(r) != len(hdr):
            continue
        body.append(r)
    sheet(wb, title, hdr, body, {h: 45 for h in hdr})


_EP_ROW = {"residual_graft_volume": ("err_graft", "status"), "new_bone_volume": ("err_new", "status_new"),
           "total_mineral_volume": ("err_mineral", "status_mineral")}


def _struct_bound(rows, ep):
    """Structures with support and the Clopper-Pearson 95% upper bound with phantom structures as the unit
    (pre-registered unit; cycle-3 review C3-SCI-05). None when the rows carry no structure or endpoint fields."""
    if ep not in _EP_ROW or not rows or "structure" not in rows[0]:
        return None, None
    ek, sk = _EP_ROW[ep]
    if ek not in rows[0] and ek == "err_graft":
        ek = "err"
    sup = [r for r in rows if r.get(sk) in ("supported", "supported_with_conditions") and r.get(ek) is not None]
    k = len({r["structure"] for r in sup})
    x = len({r["structure"] for r in sup if abs(r[ek]) > 0.2})
    if not k:
        return 0, None
    from scipy.stats import beta
    return k, (1.0 if x == k else float(beta.ppf(0.975, x + 1, k - x)))


def gen2_sheets(wb):
    # advisor validation, per endpoint
    rows = []
    for name in ("exp_S1H5_heldout", "exp_S1H4_heldout", "exp_S1H3_heldout", "exp_S1H2_heldout", "exp_S1H_heldout",
                 "exp_S1b_advisor_threshold", "exp_S1c_control_reference", "exp_S1_advisor"):
        d = load(name)
        if not d:
            continue
        kind = "held-out (pre-registered)" if "heldout" in name else "in-sample (development)"
        summaries = d.get("summary", [])
        if not summaries and isinstance(d.get("analysis"), dict):        # S1H4 format
            summaries = [{"method": "advisor_threshold", "per_endpoint": {
                ep: {"n": v["n"], "n_fail": v["n_fail"], "failures_refused": v["failures_refused"],
                     "supported_but_failed": v["supported_but_failed"],
                     "supported_and_ok": v["n_supported"] - v["supported_but_failed"],
                     "refused_but_ok": (v["n"] - v["n_supported"]) - v["failures_refused"],
                     "p_fail_given_supported_upper95": v["row_upper95"],
                     "abs_err_supported_median": v["abs_err_supported_median"],
                     "abs_err_supported_max": v["abs_err_supported_max"]}
                for ep, v in d["analysis"].items() if isinstance(v, dict) and "n_fail" in v}}]
        for s_ in summaries:
            for ep, v in (s_.get("per_endpoint") or {}).items():
                ns = (v["supported_and_ok"] or 0) + (v["supported_but_failed"] or 0)
                bound = 1.0 if ns and v["supported_but_failed"] == ns else v["p_fail_given_supported_upper95"]
                k, sb = _struct_bound(d.get("rows") or [], ep) if "heldout" in name else (None, None)
                rows.append([name, kind, d.get("advisor_version"), s_["method"], ep, v["n"], v["n_fail"], v["failures_refused"],
                             v["supported_but_failed"], v["supported_and_ok"], v["refused_but_ok"], ns / v["n"],
                             k, sb, bound, v["abs_err_supported_median"], v["abs_err_supported_max"]])
    sheet(wb, "Advisor_Validation", ["Experiment", "Kind", "Advisor", "Method", "Endpoint", "n", "Failures (>20%)",
                                     "Failures refused", "Supported & failed", "Supported & OK", "Refused but OK",
                                     "Coverage (share supported)", "Structures with support",
                                     "95% upper, structures as unit (pre-registered)",
                                     "95% upper, rows as if independent",
                                     "Median |err| supported", "Max |err| supported"], rows,
          {"Experiment": 28, "Kind": 24, "Method": 22, "Endpoint": 24})
    b4 = load("analysis_B4_volume_agreement")
    if b4:
        sheet(wb, "Volume_Agreement_B4", ["Endpoint", "n supported", "Structures", "Bias", "Bias CI low (bootstrap)",
                                          "Bias CI high", "LoA low", "LoA high", "Max |err|", "B4 met"],
              [[ep, v.get("n_supported"), v.get("n_structures"), v.get("bias"),
                *(v.get("bias_ci95_bootstrap_structures") or [None, None]), *(v.get("loa95") or [None, None]),
                v.get("max_abs"), v.get("b4_met")] for ep, v in b4["endpoints"].items()], {"Endpoint": 26})
    rows = []
    for name in ("exp_L4_registration_qc", "exp_F2_roi_propagation"):
        d = load(name)
        if d:
            for k, v in (d.get("summary") or {}).items():
                rows.append([name, k, v])
    if rows:
        sheet(wb, "Registration_QC_L4_F2", ["Experiment", "Quantity", "Value"], rows, {"Experiment": 28, "Quantity": 34})
    L3 = load("exp_L3_displacement")
    if L3:
        sheet(wb, "Longitudinal_L3", ["Displacement mean (µm)", "Fragment prob.", "Method", "Graft Dice", "Mean |graft vol err|", "n"],
              [[r["D_um"], r["F"], r["method"], r["dice_graft"], r["abs_vol_err"], r["n"]] for r in L3["summary"]])
    rows = []
    for name in ("exp_S2v2_sim2real_a", "exp_S2v2_sim2real_b"):
        d = load(name)
        if d:
            for key in ("gen0_train_zoom_curve", "dr_train_zoom_curve"):
                for z, v in (d.get(key) or {}).items():
                    rows.append([name, key, f"zoom {z}", "train Dice", v, None, None])
    c = load("exp_S2v2_sim2real_c")
    if c:
        for k, v in c.get("fewshot_summary", {}).items():
            rows.append(["S2v2c", "few-shot test (5 specimens, 3 seeds)", k, "Dice", v.get("mean"), v.get("ci_lo"), v.get("ci_hi")])
        for k, v in c.get("paired_differences", {}).items():
            rows.append(["S2v2c", "paired per-specimen difference", k, "Dice diff", v.get("mean"), v.get("ci_lo"), v.get("ci_hi")])
    s3 = load("exp_S3_selfsupervised")
    if s3:
        for k, v in s3.get("summary", {}).items():
            rows.append(["S3", "few-shot test (5 specimens, 3 seeds)", k, "Dice", v.get("mean"), v.get("ci_lo"), v.get("ci_hi")])
    sheet(wb, "Transfer", ["Experiment", "Data / quantity", "Arm", "Metric", "Value", "CI low", "CI high"], rows)
    u = load("exp_U1_ensemble_conformal")
    if u:
        rows = [["seed", s_["seed"], k, v] for s_ in u.get("seeds", []) for k, v in s_.items() if k != "seed"]
        rows += [["ensemble", "", k, v] for k, v in u.get("ensemble", {}).items()]
        for sc_, v in u.get("failure_detection", {}).get("auroc", {}).items():
            for st, vv in v.items():
                rows.append(["failure AUROC", sc_, st, vv.get("failure") if isinstance(vv, dict) else vv])
        for k, v in u.get("conformal", {}).items():
            rows.append(["conformal", k, "", json.dumps(v) if isinstance(v, dict) else v])
        sheet(wb, "Uncertainty_U1", ["Block", "Item", "Quantity", "Value"], rows, {"Value": 60})
    o2 = load("exp_O2_runtime")
    if o2:
        sheet(wb, "Runtime_O2", ["Variant", "Median voxels/s", "Min label agreement vs PyTorch", "Mean |graft vol err|"],
              [[k, v["median_voxels_per_s"], v["min_label_agreement"], v["mean_abs_graft_vol_err"]] for k, v in o2["summary"].items()])
    for title, path in (("Scorecard", "BENCHMARK_SCORECARD.md"), ("Forensic_Audit", "FORENSIC_AUDIT.md"),
                        ("Baseline_Comparison", "BASELINE_COMPARISON.md"), ("Founder_Decisions", "FOUNDER_DECISIONS.md"),
                        ("Risks", "RISK_REGISTER.md"), ("Defects", "DEFECT_REGISTRY.md"), ("QA_Defects", "docs/qa/DEFECTS_FOUND.md"),
                        ("Reviews", "REVIEW_REGISTRY.md")):
        md_sheet(wb, title, path)
    csv_sheet(wb, "Traceability", "docs/quality/traceability_matrix.csv")
    csv_sheet(wb, "Datasets_R2", "docs/research/datasets_r2.csv")
    csv_sheet(wb, "Competitor_Matrix", "docs/research/competitor_matrix.csv")
    csv_sheet(wb, "Patents", "docs/ip/patents.csv")
    reg = ROOT / "models" / "registry.json"
    if reg.exists():
        R = json.loads(reg.read_text())
        sheet(wb, "Model_Registry", ["Model", "Provenance", "Licence tag", "n train", "Parent", "SHA-256 (12)", "ONNX"],
              [[k, ", ".join(v.get("provenance", [])), v.get("licence_tag"), v.get("n_train"), v.get("parent"),
                (v.get("sha256") or "")[:12], "yes" if v.get("onnx_sha256") else ""] for k, v in sorted(R.items())])


if __name__ == "__main__":
    main()
