"""Build investor, research-collaboration and commercial-pilot decks (PowerPoint) from project results.

All numbers are read from experiments/results/*.json and business/financial_model_outputs.json.
Run: python investor/build_decks.py  → investor/*.pptx
"""
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt, Emu

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "experiments" / "results"
FIG = R / "figures"
SHOT = ROOT / "investor" / "screenshots"
NAVY = RGBColor(0x1F, 0x4E, 0x79)
INK = RGBColor(0x1D, 0x23, 0x30)
MUTED = RGBColor(0x6B, 0x72, 0x80)
RED = RGBColor(0x8B, 0x1E, 0x1E)
ORANGE = RGBColor(0xE6, 0x9F, 0x00)


def J(name):
    p = R / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else {}


A, B, C2, G, L, L2, Jd = (J("exp_A_baselines"), J("exp_B_unet"), J("exp_C2_ablation"), J("exp_G_morphometry"),
                          J("exp_L_longitudinal"), J("exp_L2_strutlike"), J("exp_J_adaptation"))
FM = json.loads((ROOT / "business" / "financial_model_outputs.json").read_text())


def fmt(x, nd=2):
    return f"{x:.{nd}f}" if isinstance(x, (int, float)) else str(x)


class Deck:
    def __init__(self):
        self.p = Presentation()
        self.p.slide_width, self.p.slide_height = Inches(13.333), Inches(7.5)
        self.blank = self.p.slide_layouts[6]

    def _text(self, s, x, y, w, h, text, size=16, bold=False, color=INK, align=PP_ALIGN.LEFT):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        lines = text if isinstance(text, list) else [text]
        for i, ln in enumerate(lines):
            par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            par.alignment = align
            r = par.add_run()
            r.text = ln
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
            par.space_after = Pt(6)
        return tb

    def slide(self, title, bullets=None, image=None, note=None, img_w=6.3, kicker=None):
        s = self.p.slides.add_slide(self.blank)
        band = s.shapes.add_shape(1, 0, 0, self.p.slide_width, Inches(0.12))
        band.fill.solid(); band.fill.fore_color.rgb = NAVY; band.line.fill.background()
        if kicker:
            self._text(s, 0.6, 0.3, 12, 0.4, kicker.upper(), 11, True, ORANGE)
        self._text(s, 0.6, 0.55, 12.2, 0.9, title, 28, True, NAVY)
        if bullets:
            w = 12.1 if image is None else 12.1 - img_w - 0.3
            self._text(s, 0.6, 1.55, w, 5.4, ["• " + b for b in bullets], 16)
        if image and Path(image).exists():
            x = 0.6 if not bullets else 13.333 - img_w - 0.5
            s.shapes.add_picture(str(image), Inches(x), Inches(1.6), width=Inches(img_w))
        foot = "OsteoQuant · research prototype · not validated · synthetic results are labelled as such"
        self._text(s, 0.6, 7.05, 12, 0.3, foot + (f" · {note}" if note else ""), 9, False, MUTED)
        return s

    def table(self, title, header, rows, kicker=None, col_w=None, note=None):
        s = self.slide(title, kicker=kicker, note=note)
        n, m = len(rows) + 1, len(header)
        shp = s.shapes.add_table(n, m, Inches(0.6), Inches(1.6), Inches(12.1), Inches(0.4 * n))
        t = shp.table
        for j, h in enumerate(header):
            c = t.cell(0, j); c.text = h
            c.text_frame.paragraphs[0].runs[0].font.size = Pt(13); c.text_frame.paragraphs[0].runs[0].font.bold = True
        for i, r in enumerate(rows, 1):
            for j, v in enumerate(r):
                c = t.cell(i, j); c.text = str(v)
                c.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
        if col_w:
            for j, w in enumerate(col_w):
                t.columns[j].width = Inches(w)
        return s

    def save(self, path):
        self.p.save(path)
        print("saved", path)


# ---------------------------------------------------------------- shared slides
def s_title(d, subtitle):
    s = d.p.slides.add_slide(d.blank)
    bg = s.shapes.add_shape(1, 0, 0, d.p.slide_width, d.p.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
    d._text(s, 0.8, 2.2, 11.5, 1.2, "OsteoQuant", 54, True, RGBColor(255, 255, 255))
    d._text(s, 0.8, 3.4, 11.5, 1.2, "Known-truth imaging analysis for bone-graft and bone-healing studies", 26, False, RGBColor(0xDC, 0xE6, 0xF1))
    d._text(s, 0.8, 4.6, 11.5, 0.8, subtitle, 18, False, ORANGE)
    d._text(s, 0.8, 6.6, 11.5, 0.5, "Research prototype · not validated for GLP or regulatory use · prepared 27 Nov 2026", 12, False, RGBColor(0xDC, 0xE6, 0xF1))


def s_problem(d):
    d.slide("The measurement bone-graft companies must make is still drawn by hand", [
        "FDA special controls for resorbable calcium-salt bone void fillers require animal data characterising resorption and replacement by new bone [V: 21 CFR 888.3046].",
        "Separating new bone, residual graft and host bone in micro-CT is done with manual ROIs and global thresholds; labs build their own methods study by study [RF: Sci Rep 2024; PMC10947128].",
        "Thresholds only work when graft and bone differ in density; many resorbable ceramics converge toward bone density as they remodel [RF; docs/science].",
        "Small orthobiologic firms (5–200 staff) run 1–4 animal studies a year without in-house imaging analysts [HYP, playbook].",
    ], kicker="Problem")


def s_built(d):
    d.slide("What exists today (built and tested, 27 Nov 2026)", [
        "Ingestion of TIFF/DICOM/NIfTI/NRRD/OME-TIFF/Zarr/Zeiss TXM with SHA-256 provenance; QC engine",
        "Automatic defect ROI (plate & segmental), 3-class segmentation (classical, RF, 3D U-Net), uncertainty & abstention",
        "Morphometry verified vs analytic truth and vs Scanco IPL on public data",
        "Web workbench: orthogonal viewer, brush correction with versioning, 3D surfaces, re-authenticated sign-off",
        "Hash-chained audit trail, RBAC, tenant isolation, blinding; DefectFill PDF/CSV reports",
        "49 automated tests; 16 computational experiments; 3 sample reports",
    ], image=SHOT / "04_viewer_edit_measure_3d.png", img_w=6.4, kicker="Product")


def s_evidence(d):
    b = B.get("models", {}).get("unet_ctx_s0", {}).get("summary", {})
    a = A.get("summary", {})
    g = G.get("agreement_vs_ipl", {}).get("TbTh", {})
    rows = [["Morphometry vs Scanco IPL (Tb.Th), 8 public samples", "REAL public data", f"ICC {fmt(g.get('icc_2_1', {}).get('icc', float('nan')), 3)}, mean diff {fmt(100*g.get('mean_rel_error', 0), 1)}%"],
            ["3-class U-Net, 16 held-out phantoms: graft / new bone Dice", "SYNTHETIC", f"{fmt(b.get('dice_graft_roi', {}).get('mean', 0), 3)} / {fmt(b.get('dice_new_roi', {}).get('mean', 0), 3)}"],
            ["CTAn-style two-threshold workflow, same phantoms", "SYNTHETIC", f"{fmt(a.get('otsu_ctan_style', {}).get('dice_graft', {}).get('mean', 0), 3)} / {fmt(a.get('otsu_ctan_style', {}).get('dice_new_bone', {}).get('mean', 0), 3)}"],
            ["Day-0 registration when graft mimics new bone (graft Dice)", "SYNTHETIC", f"{fmt(L2.get('summary', {}).get('day0_estimated_registration', {}).get('dice_graft', 0), 3)} vs single-scan {fmt(L2.get('summary', {}).get('rf_single_timepoint', {}).get('dice_graft', 0), 3)}"],
            ["Adaptation to unseen material: labelled scans to reach graft Dice ≥0.8", "SYNTHETIC", str(Jd.get("curves", {}).get("unet_finetune", {}).get("min_k_reaching_0.8"))],
            ["Real graft vs new bone on physical samples", "NOT YET TESTED", "phantom protocol ready; needs scanner time"]]
    d.table("Evidence so far — and what it does not show", ["Result", "Data", "Value"], rows, kicker="Technical evidence",
            col_w=[6.2, 2.4, 3.5], note="synthetic = computational phantoms with exact ground truth; not proof of real-world performance")


def s_insight(d):
    d.slide("Key finding: when is graft separable from new bone?", [
        "If graft density stays well above new bone: thresholds suffice.",
        "If densities overlap: intensity alone collapses (oracle bound graft Dice 0.30–0.65 at high noise).",
        "Shape/context recovers it only when granules look different from new bone (0.88 compact vs 0.70 strut-like).",
        "A registered day-0 scan keeps graft Dice ≥0.8 in both cases → study-design advice is part of the product.",
        "All of this is simulation; the physical phantom study decides where real materials fall.",
    ], image=FIG / "exp_C_separability.png", img_w=7.0, kicker="Science")


def s_comp(d):
    d.table("Competitive landscape (public materials, Nov 2026)", ["Player", "Has", "Not found publicly"], [
        ["Dragonfly 3D World (Comet)", "DL segmentation, Bone Analysis (Bouxsein), report builder", "graft preset, audit trail/GLP package; academic licence bars fee-for-service"],
        ["Bruker CTAn / Scanco IPL", "standard morphometry; threshold graft workflows", "learned 3-class model; Part 11 features"],
        ["Avizo/Amira + BONe", "AI multi-material segmentation", "graft-specific validation"],
        ["Charles River / Inotiv (CROs)", "Part 11 custom algorithms [CC]; % residual implant (histology)", "productised micro-CT graft report"],
        ["Visiopharm / Bioquant", "histology AI; allograft-healing app [CC]", "micro-CT"],
        ["Academic papers", "CNNs for scaffold/bone, Mg implants", "multi-material known-truth benchmark"],
    ], kicker="Market context", col_w=[3.2, 4.6, 4.3], note="full evidence: docs/research/COMPETITOR_INTELLIGENCE.md")


def s_market(d):
    d.table("Bottom-up market (no top-down TAM)", ["Input", "Value", "Label"], [
        ["Bone-void-filler 510(k)s per year (MQV/MBP/QRR/PJN, 2016–25)", "≈16 / yr; 41 applicants active 2023–26", "[V] openFDA"],
        ["Dental graft & membrane applicants active", "24", "[V] openFDA"],
        ["NIH bone-repair projects mentioning micro-CT (FY2026)", "67 (lower bound)", "[V] NIH RePORTER"],
        ["CROs with bone/orthopaedic scope confirmed", "6 of 9 identified", "[V] fetched pages"],
        ["Serviceable pool for graft-defect reports at playbook prices", "$0.9M / $2.1M / $4.3M per year", "[HYP] low/mid/high"],
        ["Implication", "Graft reports alone support a services lab, not a venture-scale company", "[INF]"],
    ], kicker="Market", col_w=[6.0, 3.8, 2.3], note="business/MARKET_MODEL_INPUTS.md")


def s_model(d):
    rows = []
    for key in ("Bootstrapped — Base", "Venture — Base", "Venture — Conservative"):
        v = FM.get(key, {})
        rev = v.get("Total revenue", [0] * 5)
        rows.append([key, f"${rev[0]:,.0f}", f"${rev[4]:,.0f}", f"{v.get('Gross margin %', [0]*5)[4]:.0%}",
                     f"${v.get('Equity funding requirement (max cumulative deficit)', [0])[0]:,.0f}"])
    d.table("Two ways to build it (all drivers are hypotheses)", ["Scenario", "Revenue 2027", "Revenue 2031", "GM 2031", "Equity need"],
            rows, kicker="Business model", col_w=[4.2, 2.0, 2.0, 1.6, 2.3],
            note="business/FINANCIAL_MODEL.xlsx — Bootstrapped Base assumes $325K grants; Venture Base assumes NSF Phase II")


def s_pricing(d):
    d.slide("Pricing hypotheses to test, not claims", [
        "Per non-GLP study ≈$12K; GLP ≈$25K; academic licence ≈$4K/yr; CRO licence ≈$40K/yr [HYP, playbook]",
        "Test three formats in interviews: per scan, per study, subscription (business/PRICING_EXPERIMENT.md)",
        "Go signal: ≥3 of 15 buyers willing to pay ≥$10K per study; pivot signal: <$5K or analysis <5% of study cost",
        "First offer: free/discounted retrospective pilot on 20–30 scans alongside the customer's own analysis",
    ], kicker="Pricing")


def s_milestones(d):
    d.table("Milestones (next 12 months)", ["When", "Milestone", "Unlocks"], [
        ["Dec 2026", "OTM disclosure & IP clinic; 15 discovery interviews started", "clean title; demand signal"],
        ["Jan–Feb 2027", "Beckman Versa access; pilot phantom scans (3 materials)", "first real separability data"],
        ["Feb 2027", "Cozad registration (window Dec 1 – Feb 2) ; NSF Project Pitch", "prize money; SBIR invitation"],
        ["Mar–May 2027", "Full phantom study; retrospective pilot with 1 company/CRO", "validation evidence; LOI"],
        ["Jul 2027", "NSF SBIR Phase I (if eligible PI) or NIH STTR with UIUC PI", "$305K–$336K non-dilutive"],
        ["H2 2027", "First paid non-GLP study; ORS/TERMIS abstract; manuscript", "revenue; credibility"],
    ], kicker="Plan", col_w=[1.8, 6.2, 4.1])


def s_risks(d):
    d.table("Biggest risks and how we test them", ["Risk", "Test / mitigation"], [
        ["Real graft and new bone inseparable on micro-CT", "phantom study (E2); fall back to day-0 protocol or histology-first"],
        ["Buyers won't pay ≥$10K", "15 interviews + price ladder; pivot to CRO licences / academic recharge"],
        ["CROs already satisfied in-house", "CRO interviews (U4); position as partner"],
        ["Dragonfly/Bruker add graft presets", "own material reference library + validation data + study design service"],
        ["Founder eligibility for SBIR (student)", "full-time co-founder PI or NIH STTR with faculty PI"],
        ["University IP claims", "OTM disclosure before using Beckman equipment"],
    ], kicker="Risks", col_w=[5.0, 7.1])


def s_team(d):
    d.slide("Team today and roles to recruit", [
        "Founder: UIUC undergraduate; orthopaedic imaging, fracture detection, regenerative-medicine research experience",
        "Built with AI-assisted development; needs domain validation, not more code",
        "Recruit: bone-biology/histomorphometry scientist (adjudication), micro-CT imaging scientist (phantoms),",
        "   faculty advisor (e.g. Mariana Kersh — Versa-experienced bone biomechanics), fractional GxP/CSV consultant,",
        "   later a commercial co-founder from CRO/orthobiologic industry",
    ], kicker="Team")


def s_funds(d):
    d.table("Use of funds (pre-seed scenario, illustrative)", ["Item", "Amount", "Why"], [
        ["Phantom validation study (materials, scanner, calibration)", "$10–20K", "first real separability evidence"],
        ["Founder/early-hire stipends (12 months)", "$60–150K", "interviews, pilots, engineering"],
        ["Cloud GPU for nnU-Net-scale training", "$3–8K", "replace CPU prototype models"],
        ["CSV/QA consultant scoping + Part 11 gap work", "$15–40K", "GLP-readiness"],
        ["Legal (incorporation, IP, MSA/DPA templates)", "$10–25K", "contracts with first customers"],
        ["Conferences, travel, pilots", "$10–20K", "ORS/TERMIS; on-site pilots"],
    ], kicker="Funding", col_w=[6.0, 2.0, 4.1], note="ranges from validation/BILL_OF_MATERIALS.csv and business/FINANCIAL_MODEL.xlsx")


def s_ask(d, text):
    d.slide("The ask", text, kicker="Next step")


def s_collab_project(d):
    d.slide("Proposed collaboration: a physical known-truth phantom benchmark", [
        "3–5 commercial graft materials (HA, β-TCP, BCP, bioactive glass, CaSO4) in ex vivo bone defects",
        "Truth by construction: empty-defect scan + gravimetric fill + post-fill scans; pure-material reference scans",
        "Zeiss Xradia 630 Versa at 10/20/40 µm; HA calibration phantom; repeat scans for test–retest",
        "Outputs: per-material separability map, ICC vs truth, a publishable benchmark dataset",
        "Collaborator contributes phantom design and scanning expertise; co-authorship; IP terms agreed first (OTM)",
    ], kicker="Research collaboration")


def s_pilot(d):
    d.slide("Commercial pilot offer (retrospective, no risk to your study)", [
        "You share 20–30 completed micro-CT scans under a data-processing agreement",
        "We run DefectFill alongside your own analysis; you keep using your results",
        "Deliverables: per-specimen comparison, ICC and Bland–Altman vs your analyst, hands-on time per scan",
        "Material-specific separability assessment for your graft (incl. whether a day-0 scan would help)",
        "Price: free or discounted pilot; success = LOI or paid next study (pricing to be agreed)",
    ], image=ROOT / "reports_samples" / "fig" / "r1_groups.png", img_w=5.6, kicker="Pilot")


def main():
    out = ROOT / "investor"
    d = Deck(); s_title(d, "Investor overview — pre-seed, pre-revenue")
    for f in (s_problem, s_built, s_evidence, s_insight, s_comp, s_market, s_pricing, s_model, s_milestones, s_risks, s_team, s_funds):
        f(d)
    s_ask(d, ["Not raising equity before the phantom result and first pilot (Feb–May 2027).",
              "Seeking: advisors (bone biology, CRO operations), pilot partners, and non-dilutive funding (Cozad, I-Corps, SBIR/STTR).",
              "Decision gate (~25 Feb 2027): ≥3/15 buyers at ≥$10K/study AND phantom shows a separable path (single-scan or day-0)."])
    d.save(out / "OsteoQuant_Investor_Deck.pptx")
    d = Deck(); s_title(d, "Research collaboration proposal")
    for f in (s_problem, s_insight, s_evidence, s_collab_project, s_built, s_team):
        f(d)
    s_ask(d, ["20 minutes of advice on phantom design and endpoint definitions.",
              "If useful: a joint, publishable benchmark with IP terms agreed first and academic outputs kept separate."])
    d.save(out / "OsteoQuant_Research_Collaboration_Deck.pptx")
    d = Deck(); s_title(d, "Commercial pilot proposal for orthobiologic R&D and CRO teams")
    for f in (s_problem, s_built, s_evidence, s_insight, s_pilot, s_pricing):
        f(d)
    s_ask(d, ["Which of your recent studies could we analyse retrospectively?",
              "Who owns the micro-CT analysis decision and budget?"])
    d.save(out / "OsteoQuant_Commercial_Pilot_Deck.pptx")


if __name__ == "__main__":
    main()
