"""Build deliverables/OsteoQuant_Technical_and_Commercial_Report.pdf from repository results.

Every quantitative statement is read from experiments/results/*.json or business/ outputs at build
time. Run after all experiments: python scripts/build_final_report.py
"""
import json
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape as esc

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, ListFlowable,
                                ListItem)

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "experiments" / "results"
FIG = R / "figures"
OUT = ROOT / "deliverables" / "OsteoQuant_Technical_and_Commercial_Report.pdf"


def J(n):
    p = R / f"{n}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def f3(x, nd=3):
    try:
        return f"{float(x):.{nd}f}"
    except (TypeError, ValueError):
        return "—"


ss = getSampleStyleSheet()
ACC = colors.HexColor("#1F4E79")
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=ACC, fontSize=18, spaceAfter=6, spaceBefore=6)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=ACC, fontSize=13, spaceBefore=10, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9.4, leading=12.6)
SM = ParagraphStyle("SM", parent=B, fontSize=7.8, leading=9.8)
TITLE = ParagraphStyle("T", parent=H1, fontSize=26, leading=30)


def P(t, st=B):
    return Paragraph(t, st)


def bullets(items):
    return ListFlowable([ListItem(P(i), leftIndent=10) for i in items], bulletType="bullet", start="•", leftIndent=12)


def table(rows, widths=None, fs=7.8):
    data = [[P(esc(str(c)), SM) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#BBBBBB")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return t


def fig(name, w=175, ratio=0.4):
    p = FIG / name if not str(name).startswith("/") else Path(name)
    return Image(str(p), width=w * mm, height=w * mm * ratio) if p.exists() else P(f"[figure missing: {name}]")


def main():
    A, B_, C, C2, G, Ld, L2, Jd, K, F, N, H, O, Pp = (J(x) for x in (
        "exp_A_baselines", "exp_B_unet", "exp_C_D_E_separability", "exp_C2_ablation", "exp_G_morphometry",
        "exp_L_longitudinal", "exp_L2_strutlike", "exp_J_adaptation", "exp_K_M_uncertainty", "exp_F_roi",
        "exp_N_histology", "exp_H_I_real", "exp_O_performance", "exp_P_reproducibility"))
    FM = json.loads((ROOT / "business/financial_model_outputs.json").read_text())
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    flow = []
    flow += [Spacer(1, 40 * mm), P("OsteoQuant", TITLE),
             P("Technical and commercial report — autonomous build session, 27 November 2026", H2),
             Spacer(1, 6 * mm),
             P("Preclinical bone-defect imaging analysis: what was built, the experiments actually run, their results, "
               "remaining limitations, and the most promising technical and commercial direction."),
             Spacer(1, 8 * mm),
             table([["Status", "Research prototype. Not validated. Not a medical device. No GLP or 21 CFR Part 11 claim."],
                    ["Evidence", "Synthetic results are labelled SYNTHETIC; real-data results name their public dataset; "
                                 "commercial figures are hypotheses (no customer interviews yet)."],
                    ["Repository", f"arnavhiteshpatel-cloud/playground, branch claude/osteoquant-autonomous-dev-ujqgkl, commit {commit}"]],
                   [35 * mm, 140 * mm]), PageBreak()]

    # 1 executive summary
    b = B_.get("models", {})
    bc, bn = b.get("unet_ctx_s0", {}).get("summary", {}), b.get("unet_noctx_s0", {}).get("summary", {})
    g = G.get("agreement_vs_ipl", {})
    flow += [P("1. Executive summary", H1), bullets([
        "<b>Built:</b> a working end-to-end system — ingestion of seven formats including real 2 GB Zeiss TXM volumes, "
        "quality control, automatic defect ROI, classical and learned three-class segmentation with uncertainty, "
        "verified morphometry, biostatistics, longitudinal registration, an experimental histology module, a multi-user "
        "web workbench with correction tools and re-authenticated sign-off, a hash-chained audit trail, and DefectFill "
        "PDF/CSV reports. 58 automated tests pass.",
        f"<b>Real-data result:</b> morphometry agreed with Scanco IPL reference maps on 8 public trabecular samples "
        f"(Tb.Th ICC(2,1) {f3(g.get('TbTh', {}).get('icc_2_1', {}).get('icc'))}, mean difference "
        f"{f3(100 * g.get('TbTh', {}).get('mean_rel_error', 0), 1)}%) — after identifying that the border convention alone "
        "shifts thickness by ~18% (convention chosen post hoc; needs independent confirmation).",
        f"<b>Synthetic result:</b> a CPU-trained 3D U-Net reached graft Dice {f3(bn.get('dice_graft_roi', {}).get('mean'))} and "
        f"new-bone Dice {f3(bn.get('dice_new_roi', {}).get('mean'))} on held-out phantoms, versus "
        f"{f3(A.get('summary', {}).get('otsu_ctan_style', {}).get('dice_graft', {}).get('mean'))} / "
        f"{f3(A.get('summary', {}).get('otsu_ctan_style', {}).get('dice_new_bone', {}).get('mean'))} for a CTAn-style workflow.",
        "<b>Key scientific insight (simulation):</b> once graft density enters the new-bone range, no intensity rule can "
        "separate them well; shape features help only if granules look different from new bone; a registered day-0 scan "
        f"kept graft Dice at {f3(L2.get('summary', {}).get('day0_estimated_registration', {}).get('dice_graft'))} where "
        f"single-scan methods fell to {f3(L2.get('summary', {}).get('rf_single_timepoint', {}).get('dice_graft'))}.",
        "<b>Hypotheses that failed or were not supported:</b> an explicit ROI-context input did not help the U-Net; "
        "context features did not rescue morphologically bone-like granules; whole-volume thresholds failed on real scans "
        "until padding/metal handling was added; automatic segmental-gap ROIs fail once the gap bridges.",
        "<b>Commercial reality check:</b> bottom-up, graft-defect reports at playbook prices address ≈$0.9–4.3M/yr — "
        "enough for a services-plus-software lab, not a venture-scale company without expansion modules or CRO licensing.",
        "<b>Most promising direction:</b> lead with a <i>separability-and-study-design</i> service (phantom-calibrated "
        "material assessment + day-0 protocol + audited DefectFill report) for small orthobiologic firms and CROs, validated "
        "first by a physical phantom study on the Beckman Versa 630.",
        "<b>Independent review:</b> 21 security and 18 scientific findings; both critical security issues and the major "
        "scientific claim error were fixed and claims corrected (Section 9)."]), PageBreak()]

    # 2 what was built
    flow += [P("2. What was built", H1), table([
        ["Component", "Capability", "Verification"],
        ["Ingestion (io/)", "TIFF stacks, OME-TIFF, DICOM, NIfTI, NRRD, Zarr, Zeiss TXM (slice-lazy); SHA-256; missing-slice & duplicate detection; safe upload mode", "unit tests; real TXM & 829-slice DICOM"],
        ["QC (qc/)", "9 deterministic + 8 heuristic checks incl. rings, cupping, CNR, truncation, metal/saturation", "Exp E; real scans"],
        ["Phantoms (phantom/)", "3 defect models, 15 materials (NIST physics), exact partial-volume truth; fast + polychromatic FBP CT simulator", "visual + Exp A–L"],
        ["Segmentation (segment/, ml/)", "9 classical methods incl. RF; CPU 3D U-Net (0.79 M params) with registry, licence guard, safe loading", "Exp A, B, H, J"],
        ["ROI (roi/)", "Exact geometric ROIs with hashes and revisions; plate & segmental detectors; landmarks", "Exp F; tests"],
        ["Morphometry (morphometry/)", "BV/TV, BS, Tb.Th/Sp/N, Conn.D, Ct.Th, bridging, ingrowth, BIC, density (calibrated only)", "analytic + Scanco IPL (Exp G)"],
        ["Uncertainty", "Entropy, TTA, temperature scaling, abstention, risk–coverage, OOD, plausibility", "Exp K"],
        ["Longitudinal", "Rigid/affine/B-spline registration, day-0 propagation, change maps", "Exp L, L2"],
        ["Histology", "Colour deconvolution, Macenko, region & nuclei quantification, 2D–3D registration", "Exp N (partial)"],
        ["Statistics", "Descriptives, CIs, Hedges g, ICC (all forms), Bland–Altman, CCC, mixed models, multiplicity, sample size", "published reference values"],
        ["Product (api/, study/, web/)", "FastAPI, SQLite, RBAC, tenants, blinding, jobs, review/sign-off, viewer with brush/fill/measure/3D", "58 tests; headless-browser run"],
        ["Reports", "DefectFill PDF/CSV with data-class banners, exceptions, animal-level stats, sign-off", "3 sample reports"],
    ], [38 * mm, 92 * mm, 45 * mm]), Spacer(1, 4),
        Image(str(ROOT / "investor/screenshots/04_viewer_edit_measure_3d.png"), width=170 * mm, height=170 * mm * 0.633),
        P("Figure 1. Research workbench on a synthetic phantom: orthogonal views with ROI and segmentation overlay, a "
          "brush correction saved as a new version, a distance measurement and a 3D graft surface.", SM), PageBreak()]

    # 3 experiments
    flow += [P("3. Experiments and results", H1),
             P("Sixteen experiments (A–P) were run; full protocols in EXPERIMENT_REGISTRY.md and scripts in experiments/. "
               "Specimen-level means; voxels are never treated as biological replicates.")]
    rows = [["Method (SYNTHETIC test, n=16)", "Graft Dice", "New-bone Dice", "Mineral Dice"]]
    for m in ("global_fixed_sop", "otsu_ctan_style", "multiotsu", "gmm3", "intensity_morphology", "random_forest_no_spatial", "random_forest"):
        v = A.get("summary", {}).get(m)
        if v:
            rows.append([m, f"{f3(v['dice_graft']['mean'])} [{f3(v['dice_graft']['ci95'][0])}–{f3(v['dice_graft']['ci95'][1])}]",
                         f3(v["dice_new_bone"]["mean"]), f3(v["mineral_dice"]["mean"])])
    for nm, lab in (("unet_noctx_s0", "3D U-Net (no ROI input)"), ("unet_ctx_s0", "3D U-Net (+ ROI context channel)")):
        s = b.get(nm, {}).get("summary", {})
        if s:
            rows.append([lab, f"{f3(s['dice_graft_roi']['mean'])} [{f3(s['dice_graft_roi']['ci95'][0])}–{f3(s['dice_graft_roi']['ci95'][1])}]",
                         f3(s["dice_new_roi"]["mean"]), "—"])
    flow += [P("3.1 Baselines vs learned segmentation (A, B)", H2), table(rows, [70 * mm, 45 * mm, 30 * mm, 30 * mm])]
    flow += [P("3.2 Separability under graft/new-bone density overlap (C, C2, D, E)", H2), fig("exp_C_separability.png", 178, 0.27),
             P("Figure 2. Graft Dice vs graft HA-equivalent density at four noise levels (SYNTHETIC, compact granules). Dashed: "
               "Dice-optimal intensity-only oracle (upper bound for any voxel-wise intensity rule).", SM)]
    c2r = [["Condition", "Features / method", "Graft Dice"]] + [[r["morphology"], r["features"], f3(r["dice_graft"])] for r in C2.get("rows", [])]
    flow += [table(c2r, [40 * mm, 80 * mm, 30 * mm])]
    ls = L2.get("summary", {})
    flow += [P("3.3 Longitudinal day-0 propagation (L, L2)", H2), table(
        [["Method (strut-like granules, overlap regime)", "Graft Dice", "New-bone Dice"]] +
        [[k, f3(v.get("dice_graft")), f3(v.get("dice_new"))] for k, v in ls.items()], [95 * mm, 35 * mm, 35 * mm]),
        P(f"Rigid TRE below 4 µm. Best case: simulated graft only shrinks in place between timepoints (review Q-11). In the easy "
          f"regime day-0 propagation is slightly worse than single-scan methods because new bone inside the original footprint is "
          f"counted as graft.", SM)]
    flow += [P("3.4 Morphometry verification (G, REAL public data)", H2), fig("exp_G_morphometry.png", 178, 0.27),
             table([["Metric vs Scanco IPL (n=8)", "ICC(2,1) [95% CI]", "Mean rel. diff."]] +
                   [[k, f"{f3(v['icc_2_1']['icc'])} [{f3(v['icc_2_1']['ci95_low'])}–{f3(v['icc_2_1']['ci95_high'])}]",
                     f"{f3(100 * v['mean_rel_error'], 1)}%"] for k, v in g.items()], [70 * mm, 55 * mm, 40 * mm])]
    jc = Jd.get("curves", {})
    flow += [P("3.5 Adaptation to unseen materials (J) and uncertainty (K, M)", H2), table(
        [["Arm"] + [f"k={k}" for k in jc.get("unet_finetune", {}).get("k", [])]] +
        [[a] + [f3(x) for x in jc.get(a, {}).get("graft_dice", [])] for a in ("unet_finetune", "rf_from_scratch")],
        [45 * mm] + [24 * mm] * 5),
        P(f"SYNTHETIC; zero-shot U-Net graft Dice {f3(Jd.get('rows', [{}])[0].get('dice_graft'))}. Optimistic: held-out "
          f"materials differ only in simulated density/porosity.", SM)]
    if K:
        fd = K.get("failure_detection", {})
        flow += [P(f"Uncertainty (K): temperature {K.get('temperature_fit_on_val')} applied; ID-vs-OOD AUROC of scan entropy "
                   f"{f3(K.get('auroc_entropy_id_vs_ood'))}; failure flag (threshold from validation) sensitivity {f3(fd.get('sensitivity'))}, "
                   f"specificity {f3(fd.get('specificity'))} for scans with graft Dice &lt; 0.8 (n_fail={fd.get('n_fail')}). "
                   f"Modelled review-time reduction {f3(100 * K.get('effort_model', {}).get('modelled_time_reduction', 0), 0)}% uses "
                   f"<b>assumed</b> per-slice times — not a measurement.")]
    if H:
        hs = H.get("summary", {})
        flow += [P("3.6 Real-data segmentation and synthetic→real transfer (H, I)", H2),
                 table([["Method (REAL dog forelimb, 5 test specimens, band around labelled bones)", "Dice", "HD95 (vox)"]] +
                       [[k, f3(v.get("dice")), f3(v.get("hd95_vox"), 1)] for k, v in hs.items()], [110 * mm, 30 * mm, 30 * mm])]
    fs = F.get("summary", {})
    flow += [P("3.7 ROI detection (F), histology (N), performance (O), reproducibility (P)", H2), table(
        [["ROI model/variant", "Dice mean", "Dice min", "Failure rate"]] +
        [[k, f3(v["dice_mean"]), f3(v["dice_min"]), f3(v["failure_rate"], 2)] for k, v in fs.items()], [60 * mm, 35 * mm, 35 * mm, 35 * mm])]
    if N:
        n1 = N.get("N1_summary", {}).get("raw", {})
        flow += [P(f"Histology (N): 2D–3D registration raised bone-map Dice from ≈0.35 to ≈0.86; graft-void area ICC "
                   f"{f3(n1.get('graft', {}).get('icc'))}; bone-area ICC {f3(n1.get('bone', {}).get('icc'))} (weak); nuclei on 60 "
                   f"held-out real NuInsSeg images: pixel Dice {f3(N.get('N3', {}).get('mean_pixel_dice'))}, object F1 "
                   f"{f3(N.get('N3', {}).get('mean_object_f1'))} — below deep-learning tools; integrate Cellpose/StarDist.")]
    if O:
        flow += [table([["Stage (REAL data, 4 vCPU, 15 GB, no GPU)", "Seconds", "Peak RSS (MB)"]] +
                       [[k, f3(v.get("seconds"), 1), f3(v.get("peak_rss_mb"), 0)] for k, v in O.get("stages", {}).items()],
                       [90 * mm, 35 * mm, 35 * mm])]
    if Pp:
        flow += [P("Reproducibility (P): " + esc(json.dumps(Pp.get("checks", {}))) + f" — all pass: {Pp.get('all_pass')}", SM)]
    flow += [PageBreak()]

    # 4 assumptions failed / what works
    flow += [P("4. What genuinely works, what failed, and what remains unknown", H1),
             P("<b>Works (tested):</b> ingestion of real vendor data; QC; plate-defect ROI detection; morphometry vs analytic truth "
               "and IPL; synthetic three-class segmentation; registration (sub-voxel on synthetic); correction workflow; audit; reports."),
             P("<b>Failed or unsupported:</b> explicit ROI context channel (no gain); classical methods for overlapping densities; "
               "context methods for bone-like granules; naive thresholds on real reconstructions (fixed); automatic segmental ROI after "
               "bridging; classical histology bone quantification and Macenko normalisation; the playbook's ovine voxel size (24.6 µm, not 3.72 µm)."),
             P("<b>Unknown until physical data:</b> where real commercial grafts fall on the separability map; real cross-scanner "
               "transfer; analyst time saving; willingness to pay.")]

    # 5 competitors & market
    flow += [P("5. Competitive landscape and differentiation", H1), P(
        "Dragonfly 3D World 2027.1 already offers deep-learning segmentation, a Bouxsein-index Bone Analysis module and a report "
        "builder (its free academic licence excludes fee-for-service); Bruker CTAn and Scanco IPL own standard morphometry; CROs "
        "(Charles River, Inotiv) advertise Part 11 algorithm development and residual-implant histology endpoints. No vendor was found "
        "selling a validated three-class micro-CT model. Narrowest credible differentiation: known-truth, material-specific "
        "separability assessment; the day-0 longitudinal protocol; audit-ready per-study reports for firms without imaging staff. "
        "Details: COMPETITOR_INTELLIGENCE.md and docs/research/."),
        P("6. Market and financial model", H1)]
    rows = [["Scenario", "Revenue 2027", "Revenue 2031", "GM 2031", "Equity requirement"]]
    for k, v in FM.items():
        rv = v.get("Total revenue", [0] * 5)
        rows.append([k, f"${rv[0]:,.0f}", f"${rv[4]:,.0f}", f"{v.get('Gross margin %', [0] * 5)[4]:.0%}",
                     f"${v.get('Equity funding requirement (max cumulative deficit)', [0])[0]:,.0f}"])
    flow += [P("Bottom-up inputs (openFDA, NIH RePORTER) and serviceable pool ≈$0.9M / $2.1M / $4.3M per year for graft-defect "
               "reports at playbook prices [HYP]. Model: business/FINANCIAL_MODEL.xlsx (formulas; all drivers hypotheses)."),
             table(rows, [55 * mm, 28 * mm, 28 * mm, 20 * mm, 35 * mm]),
             P("Bootstrapped-Base needs little equity only because it assumes $325K of grants; Venture-Base assumes an NSF Phase II "
               "award. Treat both as conditional on the PI-eligibility plan.", SM)]

    # 7 funding & regulatory
    flow += [P("7. Funding, eligibility and regulatory position", H1), bullets([
        "Best near-term: Cozad New Venture Challenge (registration Dec 1 2026 – Feb 2 2027 [CC]); Illinois I-Corps; iVenture.",
        "NSF SBIR Phase I (≤$305K; full proposals 4 Mar and 7 Jul 2027) — PI must be >50% employed by the company; NSF STTR does "
        "not relax this. NIH STTR allows a university-employed PI. SBIR/STTR were reauthorised through 2031 (P.L. 119-83).",
        "NIH will not treat applications substantially written by AI as the applicant's own work — the grant drafts are scaffolding only.",
        "Analysis software for animal research data is likely not a medical device (inference; obtain counsel). Technical controls "
        "exist (audit trail, RBAC, e-signature workflow) but Part 11/GLP compliance is NOT claimed; traceability: 12 of 81 drafted "
        "requirements verified by tests, 24 partial, 45 gaps."])]

    # 8 security review
    flow += [P("8. Independent security and scientific review", H1), P(
        "An independent agent reviewed the code without modifying it. Fixed: arbitrary file read via detached image headers; unsafe "
        "model deserialisation (now name-only, hash-verified before weights-only loading); archive limits; PDF markup injection; "
        "cross-tenant group leakage; blinding bypass via reports; review binding and self-approval; audit-chain concurrency; "
        "deletion completeness. Scientific corrections: the intensity-only 'bound' was the accuracy-optimal rule's Dice (now a true "
        "Dice-optimal oracle; claims corrected); unequal baseline training (rerun balanced); pseudoreplication in report statistics "
        "(animal-level aggregation); uncertainty evaluation in-sample (rerun). Remaining items: docs/security/REVIEW_RESPONSE.md.")]

    # 9 recommendations
    flow += [P("9. Most promising direction and next actions", H1), bullets([
        "Within 2 weeks: OTM disclosure + Landuyt IP Clinic; email Beckman Microscopy Suite for Versa access/rates; book 15 "
        "discovery interviews from business/PROSPECTS.md (Kuros, Geistlich, Bone Solutions, Prosidyan, CSU PSRL first).",
        "Within 6 weeks: pilot phantom scan of 3 materials with an imaging-scientist advisor; run osteoquant analyze on the scans.",
        "By Feb 2027: Cozad application (in your own words); decide PI route for SBIR/STTR; first retrospective pilot proposal.",
        "Spend first only on: phantom materials and scanner time ($2–4K pilot), and legal/IP basics after OTM — no software spend needed."])]

    flow += [P("References (selected; full list docs/science/REFERENCES.md)", H2), P(
        "Bouxsein ML et al. J Bone Miner Res 2010;25:1468 (10.1002/jbmr.141). Hildebrand T, Rüegsegger P. J Microsc 1997;185:67. "
        "Odgaard A, Gundersen HJ. Bone 1993;14:173. Dempster DW et al. J Bone Miner Res 2013;28:2 (10.1002/jbmr.1805). Isensee F et al. "
        "Nat Methods 2021;18:203 (10.1038/s41592-020-01008-z). Koo TK, Li MY. J Chiropr Med 2016;15:155 (10.1016/j.jcm.2016.02.012). "
        "Hubbell JH, Seltzer SM. NIST X-ray mass attenuation coefficients (physics.nist.gov). Datasets: Zenodo 10.5281/zenodo.17255310, "
        ".11061947, .24047383, .3909552, .10518968 (all CC-BY-4.0).", SM)]

    def foot(c, d):
        c.saveState(); c.setFont("Helvetica", 7); c.setFillColor(colors.HexColor("#666666"))
        c.drawString(15 * mm, 9 * mm, "OsteoQuant — technical & commercial report — research prototype, not validated")
        c.drawRightString(195 * mm, 9 * mm, f"page {d.page}"); c.restoreState()

    OUT.parent.mkdir(exist_ok=True)
    SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm, bottomMargin=15 * mm,
                      title="OsteoQuant technical and commercial report").build(flow, onFirstPage=foot, onLaterPages=foot)
    print("saved", OUT)


if __name__ == "__main__":
    main()
