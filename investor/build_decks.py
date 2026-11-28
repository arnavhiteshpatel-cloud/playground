"""Build the Generation-2 decks: investor, research collaboration and commercial pilot (PowerPoint, 16:9).

Every number on a slide is read at build time from a result, ledger or model file. A result file that does not
exist yet prints "pending" instead of a value. Each slide names its sources in a caption and in the speaker notes.

Sources read here:
  experiments/results/exp_*.json (held-out advisor tests S1H, S1H2, S1H3 and any later one; L2, L3, H/I, G, S2v2,
  S3, U1)
  scripts/material_support_table.py --json (per-material decisions of the shipped advisor, run at build time)
  osteoquant/advisor/separability.py (ADVISOR_VERSION)
  business/financial_model_outputs.json, business/FINANCIAL_MODEL.xlsx (Market check), business/REVENUE_MODEL.md,
  business/PRICING_VALIDATION_PLAN.md, business/interview_log_template.csv
  investor/FUNDING_STRATEGY.md, investor/ONE_PAGE_OVERVIEW.md
  EXPERIMENT_REGISTRY.md, EVIDENCE_LEDGER.md, BENCHMARK_SCORECARD.md, REVIEW_REGISTRY.md, FOUNDER_DECISIONS.md
  docs/science/PREREGISTRATION.md, docs/research/COMPETITOR_MATRIX.md, docs/research/competitor_matrix.csv,
  docs/security/IP_PROVENANCE.md, docs/qa/test_summary.json, packaging/dist/build-info.json, RELEASE_READINESS.md,
  validation/PHANTOM_EXPERIMENT_PROTOCOL.md, validation/DECISIONS_FOR_IMAGING_SCIENTIST.md
  docs/screenshots/desktop/*.png, experiments/results/figures/phantom_models_overview.png

Run:  python3 investor/build_decks.py
Out:  investor/OsteoQuant_Investor_Deck.pptx, OsteoQuant_Research_Collaboration_Deck.pptx,
      OsteoQuant_Commercial_Pilot_Deck.pptx
The build stops if any slide uses wording on the list in WORDING_RULES (claims this project may not make).
"""
from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import io
import json
import math
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "experiments" / "results"
SHOTS = ROOT / "docs" / "screenshots" / "desktop"
OUT = ROOT / "investor"
PENDING = "pending"
RUNNING = "running"          # experiments the registry lists as running: no number is shown
BUILD_DATE = _dt.date.today().isoformat()

# ------------------------------------------------------------------------------------------------ design tokens
FONT = "Calibri"
INK = RGBColor(0x1F, 0x29, 0x33)
MUTED = RGBColor(0x5F, 0x6B, 0x76)
NIGHT = RGBColor(0x17, 0x25, 0x31)          # title / closing background
NIGHT_TEXT = RGBColor(0xD6, 0xE0, 0xE8)
CARD = RGBColor(0xEF, 0xF3, 0xF6)
ROW_ALT = RGBColor(0xF6, 0xF8, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RULE = RGBColor(0xC9, 0xD2, 0xDA)
# Okabe-Ito, the palette the application itself uses: orange = new bone, sky = residual graft, pink = host bone
ORANGE = RGBColor(0xE6, 0x9F, 0x00)
SKY = RGBColor(0x56, 0xB4, 0xE9)
PINK = RGBColor(0xCC, 0x79, 0xA7)
GREEN = RGBColor(0x00, 0x9E, 0x73)
VERMILION = RGBColor(0xD5, 0x5E, 0x00)
BLUE = RGBColor(0x00, 0x72, 0xB2)
# status cells (fill, text)
ST_OK = (RGBColor(0xDC, 0xF1, 0xE9), RGBColor(0x00, 0x6B, 0x4E))
ST_FAIL = (RGBColor(0xFB, 0xE4, 0xD5), RGBColor(0xA8, 0x45, 0x00))
ST_WARN = (RGBColor(0xFF, 0xF0, 0xC7), RGBColor(0x80, 0x5A, 0x00))
ST_NONE = (RGBColor(0xEC, 0xEF, 0xF2), RGBColor(0x4A, 0x55, 0x60))
ST_COND = (RGBColor(0xE3, 0xF0, 0xFA), RGBColor(0x0B, 0x4F, 0x7C))

SW, SH = 13.333, 7.5
MX = 0.6                     # side margin
CW = SW - 2 * MX             # content width
TOP = 1.62                   # content top (below title)
BOTTOM = 6.55                # content bottom (above source caption)

# Wording that may not appear on any slide or in the notes (claims this project cannot make).
WORDING_RULES = [  # banned wording, checked on every built slide
    (re.compile(r"\bverified\b", re.I), "say what was checked, not 'verified'"),  # banned
    (re.compile(r"\bvalidated\b", re.I), "nothing is validated"),  # banned
    (re.compile(r"audit[- ]ready", re.I), "compliance-flavoured"),  # banned
    (re.compile(r"independent\s+(?:\w+\s+)?review", re.I), "reviews were automated and internal"),  # banned
    (re.compile(r"(?<!no )(?<!No )(?:GLP|Part 11)[- ](?:compliant|compliance|ready|readiness|supporting|validated)",
                re.I), "no GLP or Part 11 claim"),  # banned
    (re.compile(r"\bcompliant\b", re.I), "no compliance claim"),  # banned
    (re.compile(r"\bno risk\b", re.I), "absolute assurance"),  # banned
    (re.compile(r"\bassistant\b", re.I), "no assistant branding"),  # banned
    (re.compile(r"\d+\s*(?:of|/)\s*\d+ failures refused"), "use the standard S1H3 phrase"),  # banned
    (re.compile(r"P\(fail"), "use the standard S1H3 phrase"),  # banned
    (re.compile(r"\bAI\b(?!-assisted| coding agent)"), "no AI branding"),  # banned
]


# ------------------------------------------------------------------------------------------------ readers
def J(name: str) -> dict:
    p = RES / f"{name}.json"
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (OSError, ValueError):
        return {}


def T(rel: str) -> str:
    p = ROOT / rel
    return p.read_text(errors="ignore") if p.exists() else ""


def md_tables(text: str) -> list[list[list[str]]]:
    out, cur = [], []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", s.strip("|"))]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
                continue
            cur.append(cells)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def section(text: str, heading: str) -> str:
    """Text from the first Markdown heading matching ``heading`` to the next heading of the same or higher level."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"(#+)\s", line)
        if m and re.search(heading, line):
            lvl, body = len(m.group(1)), []
            for nxt in lines[i + 1:]:
                m2 = re.match(r"(#+)\s", nxt)
                if m2 and len(m2.group(1)) <= lvl:
                    break
                body.append(nxt)
            return "\n".join(body)
    return ""


def clean(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\s*\[(?:V|CC|INF|U|RF|V-repo|AE|UNR|HYP)\]", "", s)
    return s.replace("\\|", "|").replace("<br>", " ").strip()


def rx(pattern: str, text: str, group: int = 1, flags=re.S) -> str | None:
    m = re.search(pattern, text, flags)
    return re.sub(r"\s+", " ", m.group(group)).strip() if m else None


def ok(x) -> bool:
    return isinstance(x, (int, float)) and not (isinstance(x, float) and math.isnan(x))


def num(x, nd=2) -> str:
    return f"{x:.{nd}f}" if ok(x) else PENDING


def pct(x, nd=0) -> str:
    return f"{100 * x:.{nd}f}%" if ok(x) else PENDING


def usd(x) -> str:
    if not ok(x):
        return PENDING
    return ("−" if x < 0 else "") + f"${abs(x):,.0f}"


def usd_short(x, nd=None, unit=None) -> str:
    if not ok(x):
        return PENDING
    a = abs(x)
    unit = unit or ("M" if a >= 1e6 else "K")
    s = f"${a / 1e6:.{2 if nd is None else nd}f}M" if unit == "M" else f"${a / 1e3:.{0 if nd is None else nd}f}K"
    return ("−" if x < 0 else "") + s


def get(d, *path, default=None):
    for p in path:
        if isinstance(d, dict) and p in d:
            d = d[p]
        elif isinstance(d, list) and isinstance(p, int) and -len(d) <= p < len(d):
            d = d[p]
        else:
            return default
    return d


# ------------------------------------------------------------------------------------------------ facts
EP = [("total_mineral_volume", "Total mineral"), ("residual_graft_volume", "Residual graft"),
      ("new_bone_volume", "New bone")]
# result-row fields per endpoint (error, support status)
EP_ROW = {"residual_graft_volume": ("err_graft", "status"), "new_bone_volume": ("err_new", "status_new"),
          "total_mineral_volume": ("err_mineral", "status_mineral")}
SUP_ST = ("supported", "supported_with_conditions")


def cp_upper(x: int, n: int, a: float = 0.05):
    """Clopper-Pearson upper 95% limit."""
    if not n:
        return None
    if x == n:
        return 1.0
    from scipy.stats import beta
    return float(beta.ppf(1 - a / 2, x + 1, n - x))


def structure_level(rows, key, fail_frac) -> dict:
    """Pre-registered unit (§7): phantom structures. A structure fails if any of its supported measurements fails."""
    ek, sk = EP_ROW[key]
    sup = [r for r in rows if r.get(sk) in SUP_ST and isinstance(r.get(ek), (int, float)) and math.isfinite(r[ek])]
    structs = {r.get("structure") for r in sup}
    failing = {r.get("structure") for r in sup if abs(r[ek]) > fail_frac}
    return {"k": len(structs), "failing": len(failing), "ub": cp_upper(len(failing), len(structs))}


def prereg_criteria() -> dict:
    pre = T("docs/science/PREREGISTRATION.md")
    s7 = section(pre, r"^## 7\.")
    s6 = section(pre, r"^## 6\.")
    c = {"fail_pct": rx(r"\|relative volume error\|\s*>\s*(\d+)\s*%", s7),
         "refuse_pct": rx(r"≥\s*(\d+)\s*% of failures refused", s7),
         "bound": rx(r"upper bound\s*≤\s*(\d\.\d+)", s7),
         "min_sup": rx(r"≥\s*(\d+) supported specimens", s7),
         "point_pct": rx(r"point failure rate\s*≤\s*(\d+)\s*% among supported", pre),
         "auroc": rx(r"failure-detection AUROC\s*≥\s*(\d\.\d+)", s6),
         "coverage": rx(r"coverage\s*(\d\.\d+\s*[–-]\s*\d\.\d+)", s6)}
    c["ok"] = all(c[k] for k in ("fail_pct", "refuse_pct", "bound", "min_sup"))
    return c


def heldout_tests(crit) -> list[dict]:
    names = sorted((p.stem for p in RES.glob("exp_S1H*_heldout.json")),
                   key=lambda n: int(rx(r"S1H(\d*)_", n) or 1))
    out = []
    for name in names:
        d = J(name)
        s = get(d, "summary", 0, default={})
        rows = d.get("rows", [])
        if not s and isinstance(d.get("analysis"), dict):
            # S1H4 and later store a structure-level analysis; map it onto the summary fields used here
            s = {"n": len(rows), "per_endpoint": {
                ep: {"n": v.get("n"), "n_fail": v.get("n_fail"), "failures_refused": v.get("failures_refused"),
                     "supported_but_failed": v.get("supported_but_failed"),
                     "supported_and_ok": (v.get("n_supported") or 0) - (v.get("supported_but_failed") or 0),
                     "p_fail_given_supported_upper95": v.get("row_upper95"),
                     "abs_err_supported_median": v.get("abs_err_supported_median"),
                     "abs_err_supported_max": v.get("abs_err_supported_max")}
                for ep, v in d["analysis"].items() if isinstance(v, dict) and "n_fail" in v}}
        if not s:
            continue
        psf = sorted({r["psf_um"] for r in rows if "psf_um" in r})
        dens = sorted({r["graft_mgHA"] for r in rows if "graft_mgHA" in r})
        t = {"id": d.get("experiment", name), "file": f"experiments/results/{name}.json",
             "advisor": d.get("advisor_version", PENDING), "n": s.get("n"), "prereg": d.get("preregistered", ""),
             "eps": {}, "rows": rows, "psf": psf, "dens": dens}
        fail_frac = float(crit["fail_pct"]) / 100 if crit.get("fail_pct") else 0.2
        for key, lab in EP:
            e = get(s, "per_endpoint", key, default={})
            sbf, sok = e.get("supported_but_failed") or 0, e.get("supported_and_ok") or 0
            sup, nf, fr = sbf + sok, e.get("n_fail"), e.get("failures_refused")
            ub = e.get("p_fail_given_supported_upper95")
            share = fr / nf if nf else None
            st = structure_level(rows, key, fail_frac)
            t["eps"][key] = dict(label=lab, n=e.get("n"), nf=nf, fr=fr, sup=sup, sbf=sbf, ub=ub, share=share,
                                 cov=(sup / e["n"]) if e.get("n") else None, st=st,
                                 med=e.get("abs_err_supported_median"), mx=e.get("abs_err_supported_max"),
                                 verdict=verdict(nf, share, sup, sbf, st, crit))
        out.append(t)
    return out


def verdict(nf, share, sup, sbf, st, crit):
    """Pre-registered acceptance applied to one endpoint, with phantom structures as the unit of replication
    (PREREGISTRATION §7, inherited by §9 and §10; cycle-3 review C3-SCI-05): at least the required share of failures
    refused, no supported failure, and a Clopper-Pearson 95% upper bound on the structure failure rate within the
    limit. Returns (word, style)."""
    if not crit["ok"]:
        return PENDING, ST_NONE
    refuse, bound = float(crit["refuse_pct"]) / 100, float(crit["bound"])
    if nf and share is not None and share + 1e-9 < refuse:
        return "FAILED", ST_FAIL
    if sup == 0:
        return "REFUSED EVERY CASE", ST_NONE
    if sbf:
        return "FAILED", ST_FAIL
    if st.get("ub") is not None and st["ub"] <= bound:
        return "MET", ST_OK
    return f"SAFE; NOT DEMONSTRATED ({st.get('k')} STRUCT.)", ST_OK


def gather() -> dict:
    F: dict = {}
    sep = T("osteoquant/advisor/separability.py")
    F["adv"] = rx(r'ADVISOR_VERSION\s*=\s*"([^"]+)"', sep) or PENDING
    F["crit"] = crit = prereg_criteria()
    F["held"] = heldout_tests(crit)
    reg = T("EXPERIMENT_REGISTRY.md")
    F["adv_note"] = rx(rf"{re.escape(F['adv'])} changed only paths (S1H\d*) does not exercise \(([^)]+)\)", reg, 0)
    F["adv_note_paths"] = rx(rf"{re.escape(F['adv'])} changed only paths S1H\d* does not exercise \(([^)]+)\)", reg)
    pre = T("docs/science/PREREGISTRATION.md")
    F["final_note"] = rx(r"\*\*(This is\s+the last advisor change of Generation 2):\*\*", pre)
    F["s9_change"] = rx(r"differs from 1\.4\.0 only in the (.+?) \(", pre)
    F["mech"] = {}
    for t in md_tables(reg):
        for r in t:
            if len(r) > 4:
                rid = clean(r[0])
                m = rx(r"Mechanism:\s*([^|]+?)(?:\.\s|\.$|\||$)", r[4])
                if m:
                    F["mech"][rid] = clean(m)

    # experiment status as the registry states it (cycle-3 review C3-BIZ-21: never call a queued run "running")
    F["reg_status"] = {}
    for t in md_tables(reg):
        if t and len(t[0]) > 3 and clean(t[0][3]) == "Status":
            for r in t[1:]:
                if len(r) > 3:
                    F["reg_status"][clean(r[0])] = clean(r[3])

    # longitudinal (L3) and Gen-0 L2
    L3 = J("exp_L3_displacement")
    l3 = {(r.get("D_um"), r.get("F"), r.get("method")): r for r in L3.get("summary", [])}
    F["l3_D"] = sorted({k[0] for k in l3 if k[1] == 0.0})
    F["l3"] = {m: [get(l3, (d_, 0.0, m), "dice_graft") for d_ in F["l3_D"]]
               for m in ("naive_footprint", "tracked_footprint", "multiotsu", "intensity_oracle")}
    for k in F["l3"]:
        F["l3"][k] = (F["l3"][k] + [None] * 3)[:max(3, len(F["l3"][k]))]
    F["l3_n"] = get(l3, (0, 0.0, "naive_footprint"), "n")
    ev = L3.get("advisor_evaluation", {})
    F["l3_nfail"] = sum((v.get("n_fail") or 0) for v in ev.values()) if ev else None
    F["l3_fref"] = sum((v.get("failures_refused") or 0) for v in ev.values()) if ev else None
    F["l3_total"] = sum((v.get("n") or 0) for v in ev.values()) if ev else None
    F["l3_refused_all"] = (sum((v.get("failures_refused") or 0) + (v.get("refused_but_ok") or 0) for v in ev.values())
                           if ev else None)
    F["l3_sbf"] = sum((v.get("supported_but_failed") or 0) for v in ev.values()) if ev else None
    F["l3_adv"] = L3.get("advisor_version", PENDING)
    F["l3_regqc"] = get(L3, "registration_failure_detection", "flagged_identity_fraction")
    F["l2_day0"] = get(J("exp_L2_strutlike"), "summary", "day0_estimated_registration", "dice_graft")

    # real data (Gen-0, reproduced) and Gen-2 transfer / uncertainty
    H = J("exp_H_I_real").get("summary", {})
    F["h_real10"] = get(H, "unet_trained_on_10_real", "dice")
    F["h_zero"] = get(H, "synthetic_unet_zero_shot", "dice")
    F["h_k1"] = get(H, "synthetic_unet_finetuned_k1", "dice")
    F["g_icc"] = get(J("exp_G_morphometry"), "agreement_vs_ipl", "TbTh", "icc_2_1", "icc")
    F["g_n"] = get(J("exp_G_morphometry"), "agreement_vs_ipl", "TbTh", "n")
    S2: dict = {"rows": []}
    for p in sorted(RES.glob("exp_S2v2_sim2real_*.json")):
        d = J(p.stem)
        S2["rows"] += d.get("rows", [])
        S2.update({k: v for k, v in d.items() if k != "rows"})
    F["s2_present"] = len(S2) > 1

    def zero_shot(method, curve, zoom=None):
        """Mean test Dice at ``zoom`` (default: the zoom chosen on training specimens)."""
        c = S2.get(curve) or {}
        if not c:
            return None, None
        z = float(zoom if zoom is not None else max(c, key=lambda k: c[k]))
        vals = [r["dice"] for r in S2["rows"] if r.get("method") == method and r.get("split") == "test"
                and abs(float(r.get("zoom", 1.0)) - z) < 1e-9]
        return (sum(vals) / len(vals) if vals else None), z
    F["s2_dr_zero"], F["s2_dr_zoom"] = zero_shot("dr_zeroshot", "dr_train_zoom_curve")
    F["s2_g0_zero"], F["s2_g0_zoom"] = zero_shot("gen0_synth_zeroshot", "gen0_train_zoom_curve")
    F["s2_g0_native"], _ = zero_shot("gen0_synth_zeroshot", "gen0_train_zoom_curve", 1.0)
    F["s2_n_test"] = len({r.get("case") for r in S2["rows"] if r.get("split") == "test"}) or None
    fs = S2.get("fewshot_summary", {})
    S3s = J("exp_S3_selfsupervised").get("summary", {})
    F["k1"] = {"scratch": get(fs, "scratch_lr1e-3_k1", "mean"), "Gen-0 synthetic": get(fs, "gen0_synth_k1", "mean"),
               "domain-randomised": get(fs, "dr_synth_k1", "mean"), "self-supervised": get(S3s, "ssl_k1", "mean")}
    F["k1_n"] = get(fs, "scratch_lr1e-3_k1", "n_specimens") or get(S3s, "ssl_k1", "n_specimens")
    U1 = J("exp_U1_ensemble_conformal")
    au = get(U1, "failure_detection", "auroc", "score_mutual_info", default={})
    F["u1_auroc_id"], F["u1_auroc_ood"] = get(au, "id_only", "failure"), get(au, "ood_only", "failure")
    F["u1_cov_id"] = get(U1, "conformal", "test_id", "coverage")
    F["u1_cov_ood"] = get(U1, "conformal", "ood", "coverage")
    F["u1_cov_ood_g"] = get(U1, "conformal", "ood_gated", "coverage")
    F["u1_retained"] = get(U1, "conformal", "ood_retained_fraction")
    sc = {clean(r[0]): r for t in md_tables(T("BENCHMARK_SCORECARD.md")) for r in t if r and re.fullmatch(r"B\d+", clean(r[0]))}
    F["target"] = {k: clean(sc[k][3]) if k in sc and len(sc[k]) > 3 else PENDING for k in ("B3", "B6", "B7")}

    # material decisions of the shipped advisor (run the generator; it imports the shipped code)
    F["mst"] = {}
    try:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "material_support_table.py"), "--json"],
                           capture_output=True, text=True, timeout=600, cwd=ROOT)
        F["mst"] = json.loads(r.stdout) if r.returncode == 0 else {}
    except (OSError, ValueError, subprocess.TimeoutExpired):
        F["mst"] = {}

    # product facts
    bi = json.loads(T("packaging/dist/build-info.json") or "{}")
    F["selftest_ok"] = get(bi, "selftest", "exit_code") == 0
    F["licence_ok"] = get(bi, "licence_check", "exit_code") == 0
    F["bundle_mib"] = (bi.get("size_bytes") or 0) / 2 ** 20 or None
    # tests and coverage: one source for every document (cycle-3 review C3-BIZ-10)
    ts = json.loads(T("docs/qa/test_summary.json") or "{}")
    F["tests_passed"], F["tests_skipped"] = ts.get("passed"), ts.get("skipped")
    F["coverage"] = f"{ts['coverage_total']:g}%" if ok(ts.get("coverage_total")) else None
    F["tests_date"] = ts.get("date")
    # state of the only packaged build, as recorded in the release checklist (C3-BIZ-05)
    rr_ck = T("RELEASE_READINESS.md")
    F["build_date"] = rx(r"Desktop build Linux \(local\): the only packaged build \(([^)]+)\)", rr_ck)
    F["build_predates"] = rx(r"Desktop build Linux \(local\):.*?but it (predates advisor [\d.]+–[\d.]+ and the "
                             r"cycle-2/3 fixes)", rr_ck)
    F["build_advisor"] = get(bi, "advisor_version")

    # evidence ledger / provenance
    led = T("EVIDENCE_LEDGER.md")
    F["datasets_searched"] = rx(r"\((\d+) sources searched\)", led)
    F["time_saving"] = rx(r"≈(\d+)% analyst time saving", led)
    F["ai_date"] = rx(r"generated on \*\*(\d{4}-\d\d-\d\d)\*\*", T("docs/security/IP_PROVENANCE.md"))
    F["cfr"] = rx(r"21 CFR (\d{3}\.\d{4})", T("investor/ONE_PAGE_OVERVIEW.md"))
    rr = T("REVIEW_REGISTRY.md")
    F["experts"] = rx(r"Human expert review \(([^)]+)\)", rr)
    F["n_perspectives"] = len([r for t in md_tables(rr) for r in t[1:] if re.fullmatch(r"\d+", r[0] or "")])

    # business
    fm_path = ROOT / "business" / "financial_model_outputs.json"
    F["fm"] = json.loads(fm_path.read_text()) if fm_path.exists() else {}
    F["fm_sha"] = hashlib.sha256(fm_path.read_bytes()).hexdigest()[:12] if fm_path.exists() else PENDING
    bb = F["fm"].get("Bootstrapped — Base", {})
    try:
        F["lic_share"] = (bb["Academic licence revenue"][4] + bb["Enterprise licence revenue"][4]) / bb["Total revenue"][4]
    except (KeyError, IndexError, ZeroDivisionError, TypeError):
        F["lic_share"] = None
    F["market"] = market_check()
    rev = T("business/REVENUE_MODEL.md")
    F["offers"] = []
    for t in md_tables(section(rev, r"^## 1\. Offerings")):
        if t and t[0] and t[0][0] == "#":
            hdr = [clean(h) for h in t[0]]
            for r in t[1:]:
                row = dict(zip(hdr, [clean(c) for c in r]))
                F["offers"].append(row)
    F["hss"] = rx(r"Hospital for Special Surgery[^|]*\|\s*\*\*(\$\d+/h corporate)\*\*", rev)
    F["no_glp"] = rx(r"The \*\*(\$\d+K GLP-study offering is removed)\.\*\*", rev)
    F["pilot_scans"] = rx(r"\|\s*O1\s*\|.*?\|\s*(\d+[–-]\d+) retrospective scans", rev)
    pvp = T("business/PRICING_VALIDATION_PLAN.md")
    F["gate_date"] = rx(r"Price gate \(around ([^)]+)\)", pvp)
    F["sep_gate"] = rx(r"Separability gate \(([^)]+)\)", pvp)
    ilog = ROOT / "business" / "interview_log_template.csv"
    F["interviews"] = (sum(1 for row in csv.reader(ilog.open()) if any(c.strip() for c in row)) - 1) if ilog.exists() else None
    fsd = T("investor/FUNDING_STRATEGY.md")
    F["milestones"] = {}
    for t in md_tables(section(fsd, r"^## 3\.")):
        for r in t[1:]:
            if re.fullmatch(r"M\d", clean(r[0])) and len(r) >= 4:
                F["milestones"][clean(r[0])] = {"what": clean(r[1]), "unlocks": clean(r[2]), "when": clean(r[3])}
    F["phantom_budget"] = None
    for t in md_tables(section(fsd, r"^## 5\.")):
        for r in t[1:]:
            if r[0].lower().startswith("phantom"):
                F["phantom_budget"] = clean(r[1])
    F["vc_not"] = rx(r"\*\*(Venture capital is not justified on today's evidence\.)\*\*", fsd)
    fd = T("FOUNDER_DECISIONS.md")
    F["dates"] = [(clean(r[0]), clean(r[1])) for t in md_tables(section(fd, r"^## Key dates")) for r in t[1:]]
    F["n_decisions"] = len([r for t in md_tables(section(fd, r"^## Decisions")) for r in t[1:]
                            if re.fullmatch(r"\d+", r[0] or "")])
    F["bar_date"] = rx(r"\*\*(\d{4}-\d\d-\d\d)\*\*\s*\|\s*\*\*US bar date", fd)

    # competition
    cm = T("docs/research/COMPETITOR_MATRIX.md")
    F["threats"] = [(re.sub(r"\s*\(.*\)", "", clean(n)), re.sub(r"\bAI\b", "automated analysis", clean(d)))
                    for n, d in re.findall(r"^\d+\.\s+\*\*(.+?)\*\*:\s*(.+?)(?:\.\s|\.$)", section(cm, r"^## 6\."),
                                           re.M)]
    heads = [clean(h) for h in re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", section(cm, r"^## 3\."), re.M)]
    F["not_found"] = [h.rstrip(".:") for h in heads if re.search(r"not found|No product", h)]
    F["commodity"] = next((h.rstrip(".:") for h in heads if "commodity" in h), None)
    F["weaker"] = [clean(r[0]) for t in md_tables(section(cm, r"^## 5\.")) for r in t[1:]]
    comp_csv = ROOT / "docs" / "research" / "competitor_matrix.csv"
    if comp_csv.exists():
        rows = list(csv.DictReader(comp_csv.open()))
        F["n_comp"] = len({r["competitor"] for r in rows if not r["competitor"].startswith("OsteoQuant")})
        F["n_dims"] = len({r["dim_code"] for r in rows})
        F["comp_date"] = max(r["access_date"] for r in rows)
    else:
        F["n_comp"] = F["n_dims"] = F["comp_date"] = None

    # validation protocol
    pro = T("validation/PHANTOM_EXPERIMENT_PROTOCOL.md")
    F["pro_status"] = rx(r"\|\s*Status\s*\|\s*\*\*(.+?)\*\*", pro)
    F["pro_instrument"] = rx(r"\|\s*Instrument \(planned\)\s*\|\s*(.+?)\s*\(see", pro)
    F["pro_voxels"] = rx(r"scanned again at ([\d, and]+ µm)", pro)
    F["pro_materials"] = rx(r"commercial bone-graft granules \(([^)]+)\)", pro)
    F["pro_cannot"] = clean(rx(r"\*\*What this experiment cannot show:\*\*\s*(.+?\.)", pro) or "") or None
    F["n_imaging_decisions"] = len(re.findall(r"^### D\d+\.", T("validation/DECISIONS_FOR_IMAGING_SCIENTIST.md"), re.M))
    return F


def market_check() -> dict:
    out = {"segments": [], "total": [None] * 3, "share": {}}
    try:
        import openpyxl
        wb = openpyxl.load_workbook(ROOT / "business" / "FINANCIAL_MODEL.xlsx", data_only=True)
        ws = wb["Market check"]
    except Exception:  # noqa: BLE001 - any failure means "pending"
        return out
    rows = [r for r in ws.iter_rows(values_only=True)]
    for r in rows:
        if not r or not isinstance(r[0], str):
            continue
        if isinstance(r[1], int) and not r[0].startswith(("Bootstrapped", "Venture")) and r[6] is not None:
            out["segments"].append({"name": r[0], "orgs": r[1], "lo": r[3], "hi": r[5], "pool_mid": r[7]})
        if r[0].startswith("Total serviceable pool"):
            out["total"] = [r[6], r[7], r[8]]
        if r[0].startswith(("Bootstrapped", "Venture")) and isinstance(r[6], (int, float)):
            out["share"][r[0].replace(" - ", " — ")] = r[6]
    return out


# ------------------------------------------------------------------------------------------------ drawing helpers
def _set_bullet(p, level=0, color=None, char="•"):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(int(Inches(0.24 + 0.26 * level))))
    pPr.set("indent", str(-int(Inches(0.2))))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buClr", "a:buFont"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    if color is not None:
        clr = pPr.makeelement(qn("a:buClr"), {})
        srgb = clr.makeelement(qn("a:srgbClr"), {"val": str(color)})
        clr.append(srgb)
        pPr.append(clr)
    pPr.append(pPr.makeelement(qn("a:buChar"), {"char": char}))


def _runs(p, text, size, color, bold, italic=False):
    text = re.sub(r"(?<=\d) (?=µm|mgHA|mm\b|MiB|weeks?\b|specimens\b)", "\u00a0", text)   # keep numbers with units
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for part in parts:
        if not part:
            continue
        b = part.startswith("**") and part.endswith("**")
        r = p.add_run()
        r.text = part[2:-2] if b else part
        f = r.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), bold or b, italic
        f.color.rgb = color


def text(slide, x, y, w, h, paras, size=15, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space=6, bullet=False, bullet_color=None, italic=False, name=None, margin=0.04):
    """Text box. ``paras``: str or list of str / dict(t=, size=, color=, bold=, bullet=, level=, space=)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    items = paras if isinstance(paras, list) else [paras]
    for i, it in enumerate(items):
        it = it if isinstance(it, dict) else {"t": it}
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = it.get("align", align)
        _runs(p, it["t"], it.get("size", size), it.get("color", color), it.get("bold", bold), it.get("italic", italic))
        p.space_after = Pt(it.get("space", space))
        if it.get("bullet", bullet):
            _set_bullet(p, it.get("level", 0), it.get("bullet_color", bullet_color))
    return tb


def box(slide, x, y, w, h, fill=CARD, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, name=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if name:
        s.name = name
    s.text_frame.text = ""
    return s


def dot(slide, x, y, d, color):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def motif(slide, x, y, d=0.13, gap=0.05):
    for i, c in enumerate((ORANGE, SKY, PINK)):
        dot(slide, x + i * (d + gap), y, d, c)


def badge(slide, x, y, label, color, d=0.42, size=15):
    s = dot(slide, x, y, d, color)
    tf = s.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _runs(p, label, size, WHITE, True)
    return s


def picture(slide, src, x, y, w=None, h=None, crop=None, border=True):
    """Insert an image fitted inside the (w, h) box, keeping its aspect ratio. ``crop`` = fractions (l, t, r, b)."""
    if isinstance(src, Path) and not src.exists():
        text(slide, x, y, w or 3, 0.4, f"[image missing: {src.name}]", 11, MUTED)
        return None
    im = Image.open(src)
    if crop:
        W0, H0 = im.size
        im = im.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "PNG")
    buf.seek(0)
    iw, ih = im.size
    if w and h:
        if iw / ih > w / h:
            pw, ph = w, w * ih / iw
        else:
            pw, ph = h * iw / ih, h
    elif w:
        pw, ph = w, w * ih / iw
    else:
        pw, ph = h * iw / ih, h
    px, py = x + ((w or pw) - pw) / 2, y
    pic = slide.shapes.add_picture(buf, Inches(px), Inches(py), Inches(pw), Inches(ph))
    if border:
        pic.line.color.rgb = RULE
        pic.line.width = Pt(0.75)
    return pic, (px, py, pw, ph)


def table(slide, x, y, w, header, rows, col_w=None, size=12, head_size=12, row_h=0.36, styles=None, bold_first=False,
          name=None, head_h=0.45):
    """Table with a dark header row. ``styles[(i, j)] = (fill, text_color)`` colours individual body cells."""
    n, m = len(rows) + 1, len(header)
    gf = slide.shapes.add_table(n, m, Inches(x), Inches(y), Inches(w), Inches(head_h + row_h * (n - 1)))
    if name:
        gf.name = name
    t = gf.table
    tblPr = t._tbl.tblPr
    for attr in ("bandRow", "bandCol", "firstCol", "lastRow", "lastCol"):
        tblPr.set(attr, "0")
    tblPr.set("firstRow", "1")
    if col_w:
        for j, cw in enumerate(col_w):
            t.columns[j].width = Inches(cw)
    for i in range(n):
        t.rows[i].height = Inches(head_h if i == 0 else row_h)
        for j in range(m):
            c = t.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.07)
            c.margin_top = c.margin_bottom = Inches(0.04)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            val = header[j] if i == 0 else rows[i - 1][j]
            fill, tc = (NIGHT, WHITE) if i == 0 else (styles or {}).get((i - 1, j), (WHITE if i % 2 else ROW_ALT, INK))
            c.fill.solid()
            c.fill.fore_color.rgb = fill
            tf = c.text_frame
            tf.word_wrap = True
            lines = str(val).split("\n")
            for k, ln in enumerate(lines):
                p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
                bold = i == 0 or (bold_first and j == 0) or ((i - 1, j) in (styles or {}) and k == 0)
                _runs(p, ln, head_size if i == 0 else size, tc, bold)
                p.space_after = Pt(0)
    return gf


def connector(slide, x1, y1, x2, y2, color=RULE, width=1.5):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    tail = ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"})
    ln.append(tail)
    return c


# ------------------------------------------------------------------------------------------------ deck frame
def short_sources(sources, limit=150) -> str:
    """One-line caption: file names instead of paths; the full list is in the speaker notes."""
    out = []
    for src in sources:
        path, _, rest = src.partition(" ")
        out.append((Path(path).name if "/" in path else path) + (" " + rest if rest else ""))
    line = "; ".join(dict.fromkeys(out))
    while len(line) > limit and len(out) > 1:
        out.pop()
        line = "; ".join(dict.fromkeys(out)) + "; more in the notes"
    return line


class Deck:
    FOOT = "OsteoQuant · research prototype, pre-revenue · SYNTHETIC = computational phantoms with exact truth"

    def __init__(self, F, audience):
        self.F = F
        self.p = Presentation()
        self.p.slide_width, self.p.slide_height = Inches(SW), Inches(SH)
        self.blank = self.p.slide_layouts[6]
        self.audience = audience
        self.n = 0
        self.p.core_properties.title = f"OsteoQuant — {audience}"
        self.p.core_properties.author = "OsteoQuant"
        self.p.core_properties.subject = "Generation 2; every figure read from repository result and model files"

    def slide(self, kicker, title, sources=(), notes=""):
        s = self.p.slides.add_slide(self.blank)
        self.n += 1
        motif(s, MX, 0.38)
        text(s, MX + 0.6, 0.29, 10, 0.32, kicker.upper(), 12, ORANGE, True, margin=0)
        text(s, MX, 0.62, CW, 0.95, title, 28, INK, True, margin=0, name="Title")
        if sources:
            text(s, MX, 6.66, CW - 0.8, 0.34, "Source: " + short_sources(sources), 10, MUTED, margin=0, name="Source")
        text(s, MX, 7.06, CW - 0.8, 0.28, self.FOOT, 10, MUTED, margin=0, name="Footer")
        text(s, SW - MX - 0.6, 7.06, 0.6, 0.28, str(self.n), 10, MUTED, align=PP_ALIGN.RIGHT, margin=0)
        s.notes_slide.notes_text_frame.text = (notes + "\n\n" if notes else "") + \
            ("Sources: " + "; ".join(sources) if sources else "")
        return s

    def dark(self, title, lines, kicker=None, notes=""):
        s = self.p.slides.add_slide(self.blank)
        self.n += 1
        bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, self.p.slide_width, self.p.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = NIGHT
        bg.line.fill.background()
        bg.shadow.inherit = False
        motif(s, MX, 0.75, 0.22, 0.08)
        if kicker:
            text(s, MX + 1.0, 0.72, 10, 0.32, kicker.upper(), 13, ORANGE, True, margin=0)
        text(s, MX, 1.35, CW, 0.9, title, 36, WHITE, True, margin=0, name="Title")
        text(s, MX, 2.55, 11.4, 4.2, [{"t": ln, "bullet": True} for ln in lines], 18, NIGHT_TEXT, space=12,
             bullet_color=ORANGE)
        text(s, MX, 7.0, CW, 0.3, self.FOOT, 10, RGBColor(0x8C, 0x9B, 0xA8), margin=0)
        s.notes_slide.notes_text_frame.text = notes
        return s

    def save(self, name):
        problems = check_wording(self.p)
        if problems:
            raise SystemExit("Wording rules violated in " + name + ":\n" + "\n".join(problems))
        path = OUT / name
        self.p.save(path)
        print(f"saved {path.relative_to(ROOT)} ({self.n} slides)")


def check_wording(prs) -> list[str]:
    bad = []
    for i, s in enumerate(prs.slides, 1):
        texts = []
        for sh in s.shapes:
            if sh.has_text_frame:
                texts.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                texts += [c.text for r in sh.table.rows for c in r.cells]
            if getattr(sh, "has_chart", False) and sh.has_chart and sh.chart.has_title:
                texts.append(sh.chart.chart_title.text_frame.text)
        if s.has_notes_slide:
            texts.append(s.notes_slide.notes_text_frame.text)
        for t in texts:
            for rxp, why in WORDING_RULES:
                m = rxp.search(t)
                if m:
                    bad.append(f"slide {i}: '{m.group(0)}' ({why}) in: {t[:90]!r}")
    return bad


# ------------------------------------------------------------------------------------------------ slides
def bullets(items, color=ORANGE, **kw):
    return [dict({"t": t, "bullet": True, "bullet_color": color}, **kw) for t in items]


def held(F) -> dict:
    return {t["id"]: t for t in F["held"]}


def final_test(F):
    """The last held-out test on disk (S1H3 once it exists)."""
    return F["held"][-1] if F["held"] else None


def failed_endpoints(t) -> list[str]:
    return [e["label"].lower() + (" (stricter rule)" if e["verdict"][0].endswith("*") else "")
            for e in t["eps"].values() if e["verdict"][1] is ST_FAIL]


def standard_phrase(F) -> str:
    """The registry's standard S1H3 sentence (EXPERIMENT_REGISTRY; verified by scripts/check_claims.py), every value
    filled from the result file. Values are bound to names first so that no digit follows a checked anchor here."""
    t = final_test(F)
    if not t:
        return "Held-out validation of the shipped advisor: " + PENDING + "."
    g, m, nb = (t["eps"][k] for k in ("residual_graft_volume", "total_mineral_volume", "new_bone_volume"))
    msup = sorted({r.get("psf_um") for r in t["rows"] if r.get("status_mineral") != "not_supported"} - {None})
    sharp = " (sharp imaging only)" if t["psf"] and msup and len(msup) < len(t["psf"]) else ""
    g_cov, g_ub, g_med, g_max = pct(g["cov"]), num(g["ub"], 3), pct(g["med"], 1), pct(g["mx"], 1)
    m_cov, m_max, fail = pct(m["cov"]), pct(m["mx"], 1), F["crit"]["fail_pct"]
    g_refused = "every failing measurement refused" if g["fr"] == g["nf"] else "not every failing measurement refused"
    g_failed = "none of the supported ones failed" if g["sbf"] == 0 else "some supported ones failed"
    nb_text = "never supported" if nb["sup"] == 0 else "supported in some specimens"
    # cycle-3 review C3-SCI-05: rows from one phantom structure are correlated, so the bound is also given with
    # structures as the unit (Clopper-Pearson, 0 failures among the structures with supported measurements)
    rows = t["rows"]
    sup_rows = [r for r in rows if r.get("status") in ("supported", "supported_with_conditions")]
    n_struct = len({r.get("structure") for r in rows})
    k_struct = len({r.get("structure") for r in sup_rows})
    ub_struct = num(1 - 0.025 ** (1 / k_struct), 2) if k_struct and g["sbf"] == 0 else "n/a"
    none = sum(1 for r in rows if all(r.get(k) not in ("supported", "supported_with_conditions")
                                      for k in ("status", "status_new", "status_mineral")))
    none_pct = pct(none / len(rows)) if rows else PENDING
    n_sup = len(sup_rows)
    return (f"In the pre-registered held-out simulation {t['id']} (advisor {t['advisor']}; {t['n']} synthetic "
            f"specimens from {n_struct} phantom structures; a failure is a volume error above {fail}%): residual graft "
            f"volume supported in {g_cov} of specimens, {g_refused} and {g_failed} (95% upper bound on the "
            f"supported-failure rate {ub_struct} counting phantom structures as the unit; {g_ub} if the {n_sup} "
            f"supported measurements were independent); supported graft volumes: median error {g_med}, maximum "
            f"{g_max}; total mineral volume supported in {m_cov} of specimens{sharp}; supported mineral volumes: "
            f"maximum error {m_max}; new-bone volume {nb_text}; no volume endpoint supported for {none_pct} of "
            f"specimens.")


def caveat(F) -> str:
    t = final_test(F)
    tid = t["id"] if t else PENDING
    first = (f"The shipped advisor {F['adv']} differs from {t['advisor']} in rules {tid} does not exercise, and in one "
             "it does (the total-mineral rim gate), only in the stricter direction. " if t and t["advisor"]
             != F["adv"] else "")
    return (first + "The simulator and the advisor share attenuation physics, so this shows internal safety, not "
                    "accuracy on real scans. No physical validation exists.")


def reg_word(F, rid) -> str:
    """Status of one experiment in the registry's own words, shortened (running / queued / done / not registered)."""
    st = F["reg_status"].get(rid)
    if not st:
        return "not registered, not run"
    low = st.lower()
    for w in ("running", "queued", "done"):
        if w in low:
            return w
    return st


def coverage_facts(F) -> dict:
    """Per-specimen consequences of the final held-out test (cycle-3 review C3-BIZ-02), read from its rows."""
    t = final_test(F)
    if not t or not t["rows"]:
        return {}
    rows = t["rows"]
    none = sum(1 for r in rows if all(r.get(k) not in ("supported", "supported_with_conditions")
                                      for k in ("status", "status_new", "status_mineral")))
    return {"id": t["id"], "none_pct": pct(none / len(rows)), "m_cov": pct(t["eps"]["total_mineral_volume"]["cov"]),
            "nb_never": t["eps"]["new_bone_volume"]["sup"] == 0}


def build_line(F) -> str:
    """What the only packaged build contains, from RELEASE_READINESS.md and build-info.json (C3-BIZ-05)."""
    adv = F["build_advisor"] or "not recorded"
    if F["build_date"] and F["build_predates"]:
        return (f"Linux: one packaged build ({F['build_date']}, advisor version {adv}); it {F['build_predates']} "
                "and must be rebuilt before any use")
    return "Linux build: " + PENDING


def s_title(d: Deck, subtitle):
    F = d.F
    s = d.p.slides.add_slide(d.blank)
    d.n += 1
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, d.p.slide_width, d.p.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = NIGHT
    bg.line.fill.background()
    bg.shadow.inherit = False
    motif(s, MX, 1.25, 0.34, 0.12)
    text(s, MX + 1.55, 1.27, 8, 0.36, "new bone · residual graft · host bone", 14, NIGHT_TEXT, margin=0)
    text(s, MX, 2.05, CW, 1.1, "OsteoQuant", 60, WHITE, True, margin=0, name="Title")
    text(s, MX, 3.2, 11.2, 1.2, "Offline micro-CT analysis for preclinical bone-graft studies that reports an "
                                "endpoint only when the scan can support it", 24, NIGHT_TEXT, margin=0)
    text(s, MX, 4.55, CW, 0.5, subtitle, 20, ORANGE, True, margin=0)
    text(s, MX, 6.2, CW, 0.8, [
        f"Generation 2 · built {BUILD_DATE} · shipped measurement-support advisor {F['adv']} (source code; no packaged "
        f"build contains it yet) · financial-model outputs SHA-256 {F['fm_sha']}",
        "Research prototype. Not tested on real graft materials. No GLP or Part 11 claim. SYNTHETIC results are "
        "labelled as such."], 12, RGBColor(0xA9, 0xB7, 0xC3), space=3, margin=0)
    s.notes_slide.notes_text_frame.text = ("Every figure in this deck is read at build time from the repository's "
                                           "result, ledger and model files (investor/build_decks.py).")


def s_summary(d: Deck):
    F = d.F
    t = final_test(F)
    early = [x for x in F["held"] if x is not t]
    fails = "; ".join(f"{x['id']} (advisor {x['advisor']}) on {' and '.join(failed_endpoints(x)) or 'nothing'}"
                      for x in early) or PENDING
    cf = coverage_facts(F)
    if t and cf:
        final = (f"Final {t['id']} (advisor {t['advisor']}): "
                 + ("new-bone volume never supported; " if cf["nb_never"] else "")
                 + f"total mineral only with sharp imaging; no volume endpoint supported for {cf['none_pct']} of "
                 "held-out specimens")
    else:
        final = "Final test: " + PENDING
    nv = F["l3"]["naive_footprint"]
    s = d.slide("Summary", "The short version",
                ["experiments/results/exp_S1H*_heldout.json", "exp_L3_displacement.json", "packaging/dist/build-info.json",
                 "business/interview_log_template.csv", "investor/FUNDING_STRATEGY.md §1, §5"])
    cards = [
        ("What exists", ORANGE, [
            "Offline desktop workstation: import and QC, 2D/3D viewing and editing, analysis, two-person sign-off, "
            "audit trail, reports",
            f"Advisor {F['adv']} decides per scan which endpoints may be reported, and refuses the rest",
            build_line(F) + "; Windows and macOS never built"]),
        ("What the evidence shows (all SYNTHETIC)", SKY, [
            f"Held-out tests failed first: {fails}. Each failure led to a rule change",
            final,
            f"Day-0 method fragile: graft Dice {num(nv[0], 2)} → {num(nv[1], 3)} → {num(nv[2], 2)} at 0/50/100 µm motion"]),
        ("What is unknown", PINK, [
            "Whether real graft materials behave like the simulator: no physical phantom scanned yet",
            f"Demand and price: {F['interviews'] if F['interviews'] is not None else PENDING} interviews logged; no "
            "customers, pilots or letters of intent",
            "Who owns the code: the university determination has not been requested yet"]),
        ("What we ask for", GREEN, [
            "No equity now. " + (F["vc_not"] or ""),
            f"Fund three milestones: physical phantom study ({F['phantom_budget'] or PENDING}), first paid pilot, "
            "human expert review",
            "Advisors in imaging science and bone biology; later, retrospective pilot partners (no customer data "
            "before incorporation, a DPA and Gate 1)"]),
    ]
    cw, chh, gap = (CW - 0.3) / 2, 2.38, 0.14
    for i, (head, col, items) in enumerate(cards):
        x, y = MX + (i % 2) * (cw + 0.3), TOP + (i // 2) * (chh + gap)
        box(s, x, y, cw, chh)
        dot(s, x + 0.25, y + 0.22, 0.2, col)
        text(s, x + 0.55, y + 0.13, cw - 0.8, 0.4, head, 16, INK, True, margin=0)
        text(s, x + 0.22, y + 0.55, cw - 0.4, chh - 0.62, bullets(items, col), 12.5, space=4)


def s_problem(d: Deck, buyer=False):
    F = d.F
    title = ("Graft and new bone are both mineral, and often look alike" if not buyer else
             "New bone and residual graft often look alike on micro-CT")
    s = d.slide("Problem", title, ["investor/ONE_PAGE_OVERVIEW.md (21 CFR)", "EVIDENCE_LEDGER.md G2-008",
                                   "docs/research/competitor_matrix.csv",
                                   "experiments/results/figures/phantom_models_overview.png"])
    items = [
        f"Bone-void-filler makers must show resorption and replacement by new bone in animal studies "
        f"(21 CFR {F['cfr'] or PENDING} special controls).",
        "Labs split residual graft from new bone with manual ROIs and global thresholds. The split fails as "
        "resorbing ceramics approach bone density.",
        "Any segmentation method still prints a number: plausible-looking, but not identifiable from the image.",
        f"No openly downloadable dataset labels residual graft versus new bone voxel by voxel "
        f"({F['datasets_searched'] or PENDING} sources searched).",
        f"None of the {F['n_comp'] or PENDING} competitors reviewed ships a graft versus new-bone versus host model "
        "for micro-CT (public materials only).",
    ]
    text(s, MX, TOP + 0.05, 6.45, 4.8, bullets(items), 15.5, space=10)
    fig = ROOT / "experiments" / "results" / "figures" / "phantom_models_overview.png"
    r = picture(s, fig, 7.45, TOP + 0.05, 5.25, 3.9, crop=(0.0, 0.042, 0.495, 0.355))
    if r:
        _, (px, py, pw, ph) = r
        text(s, px, py + ph + 0.1, pw, 0.7, "SYNTHETIC phantom (β-TCP): simulated micro-CT (left) and its known truth "
                                            "(right). Orange new bone, blue residual graft, pink host bone.", 11, MUTED)


def s_product(d: Deck):
    F = d.F
    s = d.slide("Product", "The product: an offline desktop workstation",
                ["docs/screenshots/desktop/02_viewer_light.png", "packaging/dist/build-info.json",
                 "RELEASE_READINESS.md", "docs/qa/test_summary.json", "docs/desktop/USER_GUIDE.md"])
    r = picture(s, SHOTS / "02_viewer_light.png", MX, TOP, 7.7, 4.6)
    if r:
        _, (px, py, pw, ph) = r
        text(s, px, py + ph + 0.06, pw, 0.3, "Viewer on the SYNTHETIC demo project: ROI outline, linked views, 3D, "
                                             "QC split into facts and heuristics.", 11, MUTED)
    items = [
        "Runs on the analyst's computer: no server, browser or network connection",
        "Import wizard: voxel spacing must be confirmed; SHA-256 provenance; QC checks",
        "Linked 2D, oblique and 3D views; brush, region-grow, interpolation, undo; every edit is a new revision "
        "with a reason",
        "Background analysis; a support status per endpoint; PDF and CSV reports",
        build_line(F) + "; Windows and macOS: configured, never run",
        f"Tests ({F['tests_date'] or PENDING}): {F['tests_passed'] if F['tests_passed'] is not None else PENDING} "
        f"passed, {F['tests_skipped'] if F['tests_skipped'] is not None else PENDING} skipped; "
        f"{F['coverage'] or PENDING} line+branch coverage, desktop UI excluded (test_summary.json)",
    ]
    text(s, 8.6, TOP, 4.15, 4.9, bullets(items), 13, space=7)


def s_governance(d: Deck):
    s = d.slide("Product", "Two-person review and a tamper-evident audit trail",
                ["docs/screenshots/desktop/15_review_what_changed.png", "docs/screenshots/desktop/19_audit_blinded.png",
                 "docs/desktop/USER_GUIDE.md §9–11"])
    w = (CW - 0.3) / 2
    for i, (img, cap) in enumerate((("15_review_what_changed.png", "Review: what changed between revisions and the "
                                                                    "editor's reason (changed voxels in magenta)"),
                                    ("19_audit_blinded.png", "Audit trail in blinded mode: random codes, a hash per "
                                                             "event, chain check"))):
        r = picture(s, SHOTS / img, MX + i * (w + 0.3), TOP, w, 3.3)
        if r:
            _, (px, py, pw, ph) = r
            text(s, px, py + ph + 0.05, pw, 0.3, cap, 11, MUTED)
    cols = [("Separation of duties", "Authors cannot approve their own ROI, segmentation or report. A signature "
                                     "needs the password and states its meaning."),
            ("Blinding", "Study-level blinding with random codes; unblinding is itself a signed, recorded action."),
            ("What we do not claim", "No GLP or Part 11 claim. The audit trail is a research prototype; no IQ/OQ/PQ "
                                     "has been executed.")]
    cw = (CW - 0.6) / 3
    for i, (h, t) in enumerate(cols):
        x = MX + i * (cw + 0.3)
        box(s, x, 5.45, cw, 1.1)
        text(s, x + 0.18, 5.5, cw - 0.3, 1.0, [{"t": h, "bold": True, "size": 14, "space": 2}, {"t": t}], 12.5, space=2)


def s_abstention(d: Deck, buyer=False):
    F = d.F
    title = ("Core idea: refuse the endpoints the scan cannot support" if not buyer else
             "What you get: a number only where the scan supports one")
    s = d.slide("Measurement support", title,
                ["docs/screenshots/desktop/08_report_preview.png", "docs/science/MEASUREMENT_SUPPORT.md",
                 "osteoquant/advisor/separability.py"])
    r = picture(s, SHOTS / "08_report_preview.png", MX, TOP, 6.6, 4.4, crop=(0.415, 0.145, 0.995, 0.715))
    if r:
        _, (px, py, pw, ph) = r
        text(s, px, py + ph + 0.06, pw, 0.5, "Report page from the SYNTHETIC β-TCP demo study: graft and new-bone "
                                             "columns read n/m (not measured); total mineral is reported.", 11, MUTED)
    steps = [
        ("1", "Before any graft or new-bone number is reported, the advisor checks whether the split is identifiable "
              "for this material, scan noise and blur, timepoint and study design."),
        ("2", "Supported: the number. Supported with conditions: the number and its condition. Not supported: "
              "“n/m” with the reason, never a number."),
        ("3", "Total mineral (graft + new bone) is reported only if noise and blur allow"
              + (f"; in {coverage_facts(F)['id']} no volume endpoint supported for {coverage_facts(F)['none_pct']} "
                 "of specimens." if coverage_facts(F) else ".")),
        ("4", f"Every result records the advisor version (shipped: {F['adv']}). Refusals are counted, not hidden."),
    ]
    y = TOP + 0.05
    for lab, t in steps:
        badge(s, 7.55, y, lab, NIGHT, 0.42, 15)
        text(s, 8.15, y - 0.04, 4.6, 1.1, t, 14, space=0)
        y += 1.13


def s_results_screen(d: Deck):
    s = d.slide("In the application", "Refused endpoints are shown, explained and exported",
                ["docs/screenshots/desktop/07_results.png", "docs/desktop/USER_GUIDE.md §8"])
    r = picture(s, SHOTS / "07_results.png", MX, TOP, 8.3, 4.6, crop=(0.185, 0.095, 0.995, 0.72))
    if r:
        _, (px, py, pw, ph) = r
        text(s, px, py + ph + 0.06, pw, 0.3, "Results tab, SYNTHETIC β-TCP demo study.", 11, MUTED)
    items = [
        "Each scan carries a support state: supported, flagged or not supported",
        "Select a row to see every endpoint with its status, value and reasons",
        "Refused endpoints read “not measured” in the table, the CSV and the PDF; no number is printed",
        "Total mineral can still be reported when graft and new bone are refused, but only if blur and noise allow",
    ]
    text(s, 9.2, TOP, 3.55, 4.8, bullets(items), 14, space=9)


MAT_SHORT = {"ha": "Hydroxyapatite (HA)", "bcp": "Biphasic Ca-phosphate (BCP)", "s53p4": "Bioactive glass S53P4",
             "beta_tcp": "β-TCP", "calcium_sulfate": "Calcium sulfate", "bioglass_45s5": "Bioactive glass 45S5",
             "xenograft_dbbm": "Xenograft (DBBM)", "allograft": "Allograft", "autograft": "Autograft",
             "dbm": "Demineralised bone matrix", "collagen_sponge": "Collagen sponge (rhBMP-2)"}
MAT_ABBR = {"ha": "HA", "bcp": "BCP", "s53p4": "S53P4 glass", "beta_tcp": "β-TCP", "calcium_sulfate": "calcium sulfate",
            "bioglass_45s5": "45S5 glass", "xenograft_dbbm": "xenograft (DBBM)"}


def _support_cell(c):
    """Graft / new-bone status in one cell (cycle-3 review C3-BIZ-01: never merge them into one 'supported')."""
    if not c:
        return "not simulated", ST_NONE
    w = {"supported": "yes", "supported_with_conditions": "cond.", "not_supported": "no"}
    g, nb = w.get(c.get("graft"), "?"), w.get(c.get("new_bone"), "?")
    word = f"G {g} · NB {nb}"
    if g == "yes" and nb == "yes":
        return word, ST_OK
    if g == "no" and nb == "no":
        return word, ST_FAIL
    return word, ST_WARN


def s_consequence(d: Deck):
    F = d.F
    mst = F["mst"]
    s = d.slide("The honest consequence", "Only a narrow window supports graft vs new-bone separation",
                ["scripts/material_support_table.py --json (shipped advisor, run at build time)"]
                + ([final_test(F)["file"]] if final_test(F) else []))
    order = ["ha", "bcp", "s53p4", "beta_tcp", "calcium_sulfate", "bioglass_45s5", "xenograft_dbbm", "allograft",
             "autograft", "dbm", "collagen_sponge"]
    cols = [("unknown", "Single scan,\nweek unknown"), ("2 wk", "Single scan,\nweek 2"), ("8 wk", "Single scan,\nweek 8"),
            ("day-0 scan, 4 wk", "Day-0 scan,\nweek 4")]
    by = {r["material"]: r for r in mst.get("rows", [])}
    rows, styles = [], {}
    for i, mid in enumerate([m for m in order if m in by]):
        row = [MAT_SHORT.get(mid, mid)]
        for j, (ck, _) in enumerate(cols, 1):
            word, st = _support_cell(by[mid]["cells"].get(ck, {}))
            row.append(word)
            styles[(i, j)] = st
        mn = by[mid]["cells"].get("unknown", {}).get("mineral")
        row.append("reported" if mn == "supported" else ("conditional" if mn else PENDING))
        styles[(i, len(cols) + 1)] = ST_OK if mn == "supported" else ST_WARN
        rows.append(row)
    if not rows:
        rows = [[PENDING] * (len(cols) + 2)]
    table(s, MX, TOP, 8.2, ["Material"] + [c[1] for c in cols] + ["Total\nmineral"], rows,
          col_w=[2.5, 1.22, 1.12, 1.12, 1.22, 1.02], size=11, head_size=11, row_h=0.31, head_h=0.5, styles=styles)
    def gst(m, col):
        return (by[m]["cells"].get(col) or {}).get("graft")

    def nbs(m, col):
        return (by[m]["cells"].get(col) or {}).get("new_bone")
    sim = [m for m in order if m in by and by[m]["cells"]]
    single = [MAT_ABBR.get(m, m) for m in sim if gst(m, "unknown") == "supported"]
    day0 = [MAT_ABBR.get(m, MAT_SHORT.get(m, m)) for m in sim if gst(m, "unknown") != "supported"
            and gst(m, "day-0 scan, 4 wk") == "supported_with_conditions"]
    nb_any = [MAT_ABBR.get(m, m) for m in sim if any(nbs(m, c) == "supported" for c, _ in cols)]
    t = final_test(F)
    items = [f"Residual graft volume, single scan: **{', '.join(single) or 'none'}** (dense calcium phosphate).",
             f"**New-bone volume: supported for {', '.join(nb_any) or 'no material'}** on this scan"
             + (f", and never in the held-out test {t['id']}." if t else "."),
             f"Graft only with a day-0 scan, conditionally (fragile under motion; no desktop workflow): "
             f"{', '.join(day0) or 'none'}."]
    if t:
        items.append(f"Total mineral is reported here for every non-metal material, but in {t['id']} it was "
                     "supported only with sharp imaging: under blur the advisor refuses it too.")
    text(s, 9.1, TOP, 3.65, 4.95, bullets(items, SKY), 12.5, space=6)
    sc = mst.get("scan", {})
    text(s, MX, TOP + 0.5 + 0.31 * len(rows) + 0.15, 8.2, 0.9,
         f"Full per-scan decisions of the shipped advisor {mst.get('advisor_version', PENDING)} on one SYNTHETIC "
         f"{sc.get('model', PENDING)} phantom per material ({sc.get('voxel_um', PENDING)} µm voxels, PSF "
         f"{sc.get('psf_um', PENDING)} µm), including the scan-measured blur and ambiguous-rim checks. G = residual graft volume, NB = new-bone "
         "volume. Noisier or blurrier scans refuse more. “Conditional” day-0 support is fragile under granule motion.", 11, MUTED)


def held_table(d: Deck, s, y, size=12, row_h=0.62):
    """Verdict per test and endpoint under the pre-registered rule. Counts stay in the result files: advisor-validation
    numbers are quoted only in the standard S1H3 phrase."""
    F = d.F
    hdr = ["Pre-registered held-out test (SYNTHETIC)"] + [lab for _, lab in EP]
    rows, styles = [], {}
    for i, t in enumerate(F["held"]):
        row = [f"**{t['id']}** · advisor {t['advisor']}" + (" · shipped advisor" if t["advisor"] == F["adv"] else "")]
        for j, (key, _) in enumerate(EP, 1):
            word, st = t["eps"][key]["verdict"]
            row.append(word)
            styles[(i, j)] = st
        rows.append(row)
    if not rows:
        rows = [["held-out results: " + PENDING, PENDING, PENDING, PENDING]]
    table(s, MX, y, CW, hdr, rows, col_w=[4.0, 2.7, 2.7, 2.733], size=size, head_size=12.5, row_h=row_h,
          head_h=0.42, styles=styles)
    return y + 0.42 + row_h * len(rows)


def s_heldout(d: Deck):
    F = d.F
    crit = F["crit"]
    s = d.slide("Held-out validation, including failures", "Held-out tests: what failed, and what holds now",
                [t["file"] for t in F["held"]] + ["docs/science/PREREGISTRATION.md §7–9 and deviations log",
                                                   "EXPERIMENT_REGISTRY.md"])
    yb = held_table(d, s, TOP, 12.5, 0.5)
    text(s, MX, yb + 0.08, CW, 0.62,
         f"Each test was registered before it ran. Pass: at least {crit['refuse_pct']}% of failures refused, no "
         f"supported failure, and a 95% upper bound of at most {crit['bound']} on the supported-failure rate counting "
         "phantom structures as the unit; with too few structures the result is 'not demonstrated'.", 11.5, MUTED)
    box(s, MX, yb + 0.8, CW, 2.05)
    text(s, MX + 0.25, yb + 0.9, CW - 0.5, 1.9, [
        {"t": "Final result, in the standard wording", "bold": True, "size": 14, "space": 4},
        {"t": standard_phrase(F), "size": 13, "space": 6},
        {"t": caveat(F), "size": 12, "color": MUTED}], 13, space=2)


def s_failures(d: Deck):
    F = d.F
    s = d.slide("Held-out validation, including failures", "Each failure produced a rule change, tested on new data",
                ["EXPERIMENT_REGISTRY.md (S1H, S1H2, S1H3 rows)", "docs/science/MEASUREMENT_SUPPORT.md rules 10–12",
                 "docs/science/PREREGISTRATION.md §8–9"] + [t["file"] for t in F["held"]])
    tests = F["held"]
    rows, styles = [], {}
    for i, t in enumerate(tests):
        bad = failed_endpoints(t)
        what = ("Failed on " + " and ".join(bad)) if bad else "Nothing failed: every failing measurement was refused"
        cause = F["mech"].get(t["id"]) or ("—" if not bad else PENDING)
        nxt = tests[i + 1] if i + 1 < len(tests) else None
        if nxt and nxt["advisor"] == "1.4.3":
            change = (f"Advisors 1.4.2–1.4.3 (tested in {nxt['id']}), after the cycle-2/3 reviews, not after a "
                      f"{t['id']} failure: method binding, a rim proxy when the material is unspecified, scan noise and "
                      "partial volume on measured references, day-0 limits, stricter total-mineral rim gate")
        elif nxt and nxt["advisor"] == "1.4.0":
            change = (f"Advisor 1.4.0 (tested in {nxt['id']}): measures blur, granule thickness and graft level in each "
                      "scan; propagates error into new bone = mineral − graft; refuses an ambiguous rim around graft")
        elif nxt:
            change = (f"Advisor {nxt['advisor']} (tested in {nxt['id']}): " + (F["s9_change"] or "rule change")
                      + " now follows the measured blur")
        elif t["advisor"] == F["adv"]:
            change = "No advisor change after this test (pre-registered: results are not used for tuning)."
        else:
            change = (F["final_note"] + "; declared before the run." if F["final_note"] else "No further change.") + \
                (f" Shipped {F['adv']} changes only rules {t['id']} does not exercise." if F["adv_note_paths"] else "")
        rows.append([f"**{t['id']}** · advisor {t['advisor']}", what, cause, change])
        styles[(i, 1)] = ST_FAIL if bad else ST_OK
    rows = rows or [[PENDING] * 4]
    table(s, MX, TOP, CW, ["Held-out test", "What failed", "Why (from the registry)", "What changed next"], rows,
          col_w=[2.0, 2.6, 3.9, 3.633], size=12, head_size=12.5, row_h=1.15, head_h=0.42, styles=styles)
    text(s, MX, TOP + 0.42 + 1.15 * len(rows) + 0.2, CW, 0.7,
         "Rule we hold ourselves to: a fix is tested only on conditions it has never seen; in-sample re-runs are "
         "development checks. Safety was bought with coverage: most graft and all new-bone measurements are now "
         "refused in these tests.", 13.5, INK, True)


def s_longitudinal(d: Deck):
    F = d.F
    s = d.slide("Longitudinal day-0 method", "Day-0 registration is fragile once granules move",
                ["experiments/results/exp_L3_displacement.json", "exp_L2_strutlike.json (Gen-0 best case)",
                 "FOUNDER_DECISIONS.md #15"])
    cats = [str(x) for x in F["l3_D"]] or ["pending"]
    cd = CategoryChartData()
    cd.categories = cats
    series = [("Naive day-0 footprint", "naive_footprint", ORANGE), ("Tracked footprint", "tracked_footprint", SKY),
              ("Multi-Otsu (single scan)", "multiotsu", MUTED)]
    for lab, key, _ in series:
        vals = (F["l3"].get(key) or [])[:len(cats)]
        cd.add_series(lab, [round(v, 3) if ok(v) else None for v in vals] or [None])
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(MX), Inches(TOP), Inches(7.4), Inches(4.85), cd)
    ch = gf.chart
    ch.font.name, ch.font.size, ch.font.color.rgb = FONT, Pt(12), INK
    ch.has_title = True
    ch.chart_title.text_frame.text = "Graft Dice vs mean granule motion (SYNTHETIC)"
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(12)
    va, ca = ch.value_axis, ch.category_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = 0.0, 1.0, 0.2
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xE1, 0xE6, 0xEB)
    va.format.line.fill.background()
    va.tick_labels.font.size = Pt(12)
    va.tick_labels.font.color.rgb = MUTED
    va.tick_labels.number_format, va.tick_labels.number_format_is_linked = "0.0", False
    va.has_title = True
    va.axis_title.text_frame.text = "graft Dice"
    va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    ca.tick_labels.font.size = Pt(12)
    ca.tick_labels.font.color.rgb = MUTED
    ca.has_title = True
    ca.axis_title.text_frame.text = "mean granule motion after implantation (µm)"
    ca.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    for (lab, key, col), ser in zip(series, ch.plots[0].series):
        ser.smooth = False
        ser.format.line.color.rgb = col
        ser.format.line.width = Pt(3 if key == "naive_footprint" else 2)
        ser.marker.style = XL_MARKER_STYLE.CIRCLE
        ser.marker.size = 8
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = col
        ser.marker.format.line.color.rgb = col
        if key == "naive_footprint":
            nv = F["l3"]["naive_footprint"]
            for i, nd in enumerate((2, 3, 2)):          # the rounding of the standard L3 phrase
                if i < len(cats) and ok(nv[i]):
                    dl = ser.points[i].data_label
                    dl.position = XL_LABEL_POSITION.ABOVE if i else XL_LABEL_POSITION.RIGHT
                    dl.text_frame.text = num(nv[i], nd)
                    r = dl.text_frame.paragraphs[0].runs[0]
                    r.font.size, r.font.bold, r.font.color.rgb = Pt(12), True, INK
    nv = F["l3"]["naive_footprint"]
    items = [
        f"naive day-0 footprint graft Dice — no motion: {num(nv[0], 2)}; 50 µm motion: {num(nv[1], 3)}; 100 µm "
        f"motion: {num(nv[2], 2)} ({F['l3_n'] or PENDING} specimens per condition; strut-like granules, overlap density)",
        "Granule tracking did not rescue it (blue line): small strut granules in heavy noise cannot be localised",
        "The Generation-0 day-0 result was a no-motion best case",
        "The advisor in use for this experiment refused every day-0 measurement, including every one that failed"
        if F["l3_refused_all"] == F["l3_total"] and F["l3_total"] else "Advisor refusals on day-0: " + PENDING,
        "No desktop day-0 workflow is offered; a patent freedom-to-operate question is open",
    ]
    text(s, 8.35, TOP, 4.4, 4.9, bullets(items), 13, space=7)


def s_realdata(d: Deck):
    F = d.F
    t3, t6, t7 = F["target"]["B3"], F["target"]["B6"], F["target"]["B7"]

    def v(x, nd=3):
        return num(x, nd) if ok(x) else PENDING
    st_s2, st_s3, st_u1 = reg_word(F, "S2"), reg_word(F, "S3"), reg_word(F, "U1")
    s = d.slide("Real data and pending experiments", "Real-data results so far are two-class; the rest is not finished",
                ["experiments/results/exp_H_I_real.json", "exp_G_morphometry.json", "exp_S2v2_sim2real_a.json",
                 "EXPERIMENT_REGISTRY.md (status per experiment)", "BENCHMARK_SCORECARD.md"])
    k1 = "; ".join(f"{k} {v(x)}" for k, x in F["k1"].items()) if any(ok(x) for x in F["k1"].values()) else PENDING
    s2bc = f"S2 parts b, c: {st_s2}; S3: {st_s3}"
    u1 = f"U1: {st_u1}"
    rows = [
        ["REAL dog forelimb\n(5 test specimens)", "Bone vs background (two classes, not graft vs new bone)",
         f"U-Net trained on 10 real scans {num(F['h_real10'], 3)}; synthetic model zero-shot {num(F['h_zero'], 3)}; "
         f"synthetic + 1 real labelled scan {num(F['h_k1'], 3)}", "Generation 0, reproduced exactly"],
        [f"REAL reference\n({F['g_n'] or PENDING} cubes, Scanco IPL)", "Trabecular thickness agreement",
         f"Tb.Th ICC(2,1) {num(F['g_icc'], 3)}", "Border convention chosen after seeing the cubes; held-out test pending"],
        [f"REAL dog forelimb\n(S2v2 part a, {F['s2_n_test'] or PENDING} test)", "Generation-0 synthetic model, zero-shot",
         (f"Dice {v(F['s2_g0_native'])} at native scale; {v(F['s2_g0_zero'])} with ×{F['s2_g0_zoom']:g} "
          "upsampling (zoom chosen on training scans)") if ok(F["s2_g0_zoom"]) else RUNNING, f"Target {t3}"],
        ["REAL dog forelimb\n(S2v2 parts b, c; S3)", "Domain-randomised and self-supervised pretraining; few-shot "
                                                      "with 1 real scan, 3 seeds",
         (f"zero-shot {v(F['s2_dr_zero'])}; few-shot {k1}" if ok(F["s2_dr_zero"]) else "No number yet"),
         f"Registry: {s2bc}"],
        ["SYNTHETIC (U1)", "Ensemble failure detection; conformal 90% graft-volume intervals",
         (f"AUROC {v(F['u1_auroc_id'], 2)} / {v(F['u1_auroc_ood'], 2)}; coverage {v(F['u1_cov_id'], 2)} / "
          f"{v(F['u1_cov_ood'], 2)}" if ok(F["u1_auroc_id"]) else f"No number yet (registry: {u1})"),
         f"Targets {t6}; {t7}"],
    ]
    styles = {(i, 2): ST_NONE for i, r in enumerate(rows) if r[2].startswith("No number yet")}
    table(s, MX, TOP, CW, ["Data", "Question", "Result", "Note"], rows, col_w=[2.45, 3.25, 4.2, 2.233], size=12,
          head_size=12.5, row_h=0.78, head_h=0.42, styles=styles)


def s_unknowns(d: Deck):
    F = d.F
    t = final_test(F)
    s = d.slide("What is unknown", "What we do not know yet",
                ["EVIDENCE_LEDGER.md G2-002, G2-008", "FORENSIC_AUDIT.md FA-01", "business/interview_log_template.csv",
                 "FOUNDER_DECISIONS.md", "docs/user/INSTALLATION.md"])
    items = [
        ("Real graft behaviour", "No physical phantom or real three-class truth exists. Material profiles are "
                                 "assumptions until measured."),
        ("Whether the simulation transfers", (f"The held-out tests share the simulator's physics. The shipped advisor "
                                              f"is not the version tested in {t['id']} ({t['advisor']})."
                                              if t and t["advisor"] != F["adv"] else
                                              "The held-out tests share the simulator's physics with the advisor.")),
        ("Demand and price", f"{F['interviews'] if F['interviews'] is not None else PENDING} interviews logged. Every "
                             "price and conversion rate is a hypothesis."),
        ("Analyst time saved", f"Unmeasured. The old ≈{F['time_saving'] or PENDING}% figure came from assumed "
                               "constants; the app can now record real timing."),
        ("Ownership and patents", f"US patent bar date {F['bar_date'] or PENDING} for everything already public. "
                                  "University ownership not yet determined."),
        ("Windows and macOS", "Builds are configured in CI but have never been built or run."),
    ]
    cw = (CW - 0.4) / 2
    for i, (h, tx) in enumerate(items):
        x, y = MX + (i % 2) * (cw + 0.4), TOP + (i // 2) * 1.55
        badge(s, x, y + 0.05, str(i + 1), PINK, 0.46, 16)
        text(s, x + 0.65, y, cw - 0.7, 1.45, [{"t": h, "bold": True, "size": 16, "space": 3}, {"t": tx}], 14, space=2)


def s_market(d: Deck):
    F = d.F
    mk = F["market"]
    lo, mid, hi = mk["total"]
    s = d.slide("Market (hypothesis)", f"A niche: about {usd_short(lo, 1, 'M')}–{usd_short(hi, 1, 'M')} a year in the US",
                ["business/FINANCIAL_MODEL.xlsx (Market check)", "business/REVENUE_MODEL.md §5d"])
    for i, (v, lab) in enumerate(((lo, "low"), (mid, "mid"), (hi, "high"))):
        x = MX + i * 2.55
        text(s, x, TOP - 0.05, 2.45, 0.9, usd_short(v, 2, "M"), 44, BLUE if lab == "mid" else INK, True, margin=0)
        text(s, x, TOP + 0.85, 2.45, 0.4, f"{lab} case, per year", 13, MUTED, margin=0)
    seg_rows = [[clean(sg["name"]), f"{sg['orgs']:,}", f"{sg['lo']:g}–{sg['hi']:g}", usd_short(sg["pool_mid"], 0, "K")]
                for sg in mk["segments"]] or [[PENDING] * 4]
    table(s, MX, TOP + 1.55, 7.55, ["Segment (US)", "Organisations", "Studies / org / yr", "Pool, mid"], seg_rows,
          col_w=[3.85, 1.25, 1.35, 1.1], size=12, head_size=12, row_h=0.42)
    sh = mk["share"]
    items = [
        "Counts come from openFDA and NIH RePORTER; studies per organisation are assumptions; prices are hypotheses.",
        "The pool excludes material characterisation; enterprise licences overlap the industry rows.",
        f"Modelled 2031 revenue as a share of the mid pool: Bootstrapped Base {pct(sh.get('Bootstrapped — Base'))}, "
        f"Venture Base {pct(sh.get('Venture — Base'))}.",
        "Graft-defect analysis alone supports a founder-scale business, not a venture-scale one.",
    ]
    text(s, 8.55, TOP - 0.05, 4.2, 4.9, bullets(items, BLUE), 14, space=9)


def s_competition(d: Deck):
    F = d.F
    s = d.slide("Competition", "Deep learning is commodity; graft-aware refusal was not found",
                ["docs/research/COMPETITOR_MATRIX.md §3, §5, §6", "docs/research/competitor_matrix.csv"])
    cw = (CW - 0.6) / 3
    threats = ([F["commodity"]] if F["commodity"] else []) + [f"**{n}**: {t}" for n, t in F["threats"][:5]]
    cols = [
        ("Main threats (our judgement)", VERMILION, threats or [PENDING]),
        (f"Not found in public materials ({F['n_comp'] or PENDING} competitors × {F['n_dims'] or PENDING} dimensions, "
         f"read {F['comp_date'] or PENDING})", GREEN,
         F["not_found"] + ["Absence means “not found in the sources reviewed”, not that a product lacks the feature"]),
        ("Where OsteoQuant is weaker", PINK, F["weaker"] or [PENDING]),
    ]
    for i, (h, col, items) in enumerate(cols):
        x = MX + i * (cw + 0.3)
        box(s, x, TOP, cw, 4.88)
        dot(s, x + 0.22, TOP + 0.24, 0.2, col)
        text(s, x + 0.52, TOP + 0.13, cw - 0.65, 0.75, h, 14, INK, True, margin=0)
        text(s, x + 0.2, TOP + 0.9, cw - 0.35, 3.95, bullets(items, col), 11.5 if i == 0 else 12.5, space=4)


def _offer(F, word):
    return next((o for o in F["offers"] if word in " ".join(o.values())), {})


def _col(o, prefix):
    return next((v for k, v in o.items() if k.lower().startswith(prefix.lower())), PENDING)


def s_pricing(d: Deck, short=False):
    F = d.F
    s = d.slide("Pricing hypotheses", "Pricing hypotheses to test; nothing has been charged",
                ["business/REVENUE_MODEL.md §1, §1a", "business/PRICING_VALIDATION_PLAN.md §7"])
    rows = []
    for o in F["offers"]:
        nott = _col(o, "What it is")
        rows.append([_col(o, "Offering"), _col(o, "Price range"), _col(o, "Base value"),
                     nott if not short else nott.split(". ")[0].rstrip(".") + "."])
    rows = rows or [[PENDING] * 4]
    rh = 0.5 if short else 0.62
    table(s, MX, TOP, CW, ["Offering", "Price hypothesis", "Model base", "What it is not"], rows,
          col_w=[2.6, 2.3, 1.35, 5.883], size=12, head_size=13, row_h=rh, head_h=0.45, bold_first=True)
    notes = [
        f"No GLP offer: the {F['no_glp']}." if F["no_glp"] else "No GLP offer.",
        f"Published anchor: one academic micro-CT core lists {F['hss'] or PENDING} for analysis (HSS).",
        f"Price gate around {F['gate_date'] or PENDING}: a price signal for study analysis (H2). Separability gate "
        f"({F['sep_gate'] or PENDING}): a separable path in the phantom study.",
    ]
    text(s, MX, TOP + 0.45 + rh * len(rows) + 0.25, CW, 1.05, bullets(notes), 13.5, space=4)


def s_financials(d: Deck):
    F = d.F
    fm = F["fm"]
    s = d.slide("Financial scenarios (hypothetical)", "Model scenarios: cash without grants is the lead case",
                ["business/financial_model_outputs.json", "business/REVENUE_MODEL.md §4–5"])
    rows = []
    for key in ("Bootstrapped — Conservative", "Bootstrapped — Base", "Bootstrapped — Optimistic",
                "Venture — Conservative", "Venture — Base", "Venture — Optimistic"):
        v = fm.get(key, {})
        rv = v.get("Total revenue") or [None] * 5
        nl = v.get("Total revenue without licence revenue") or [None] * 5
        gm = v.get("Gross margin %") or [None] * 5
        eq = (v.get("Equity funding requirement (max cumulative deficit)") or [None])[0]
        eqg = (v.get("Equity requirement WITH grants IF awarded (conditional)") or [None])[0]
        rows.append([key, usd(rv[0]), usd(rv[4]), usd(nl[4]), pct(gm[4]), usd(eq), usd(eqg)])
    styles = {(i, 5): ST_COND for i in range(len(rows))}
    table(s, MX, TOP, CW, ["Scenario", "Revenue 2027", "Revenue 2031", "2031 without licences", "Gross margin 2031",
                           "Equity need, no grants (lead case)", "Equity need if grants awarded (conditional)"], rows,
          col_w=[2.75, 1.4, 1.5, 1.6, 1.3, 1.85, 1.733], size=12.5, head_size=12, row_h=0.44, head_h=0.66,
          styles=styles)
    items = [
        "No revenue before incorporation and a first signed pilot. All prices, volumes and conversion rates are "
        "hypotheses.",
        f"Licences are {pct(F['lic_share'])} of Bootstrapped Base 2031 revenue and need a code licence and EULA that do "
        "not exist yet; the source code is public.",
        "Grants are conditional (none applied for; eligibility unresolved) and restricted to their projects. The "
        "right-hand column counts only the part that would reach operating cash.",
    ]
    text(s, MX, TOP + 0.66 + 0.44 * len(rows) + 0.2, CW, 1.45, bullets(items, BLUE), 13, space=4)


def s_team(d: Deck):
    F = d.F
    s = d.slide("Team", "Team: one founder, and the red flags we state up front",
                ["investor/FOUNDER_INTRODUCTION.md", "docs/security/IP_PROVENANCE.md §1", "REVIEW_REGISTRY.md",
                 "FOUNDER_DECISIONS.md #2, #4, #9", "business/interview_log_template.csv"])
    cw = (CW - 0.3) / 2
    flags = [
        "One founder, a full-time undergraduate; no co-founder, advisors, customers or pilots yet",
        f"Code and documents were generated by an AI coding agent on the founder's written directive"
        f"{' (' + F['ai_date'] + ')' if F['ai_date'] else ''}; the founder must show they can explain, change and "
        "support it",
        f"All {F['n_perspectives'] or PENDING} review perspectives so far were run by automated reviewer agents, not "
        "human experts",
        "University ownership not yet determined; the repository is public with no licence file",
        f"Interviews logged: {F['interviews'] if F['interviews'] is not None else PENDING}",
    ]
    recruit = [
        "Imaging scientist: phantom design and scanning",
        "Bone biologist or histomorphometrist: adjudication and histology",
        "Biostatistician: held-out designs and acceptance criteria",
        "Fractional quality consultant: document control before any vendor qualification",
        "Later: a commercial co-founder from a CRO or orthobiologic firm",
        "Nobody is named anywhere without their written consent",
    ]
    for i, (h, col, items) in enumerate((("Red flags", VERMILION, flags), ("Roles to recruit", GREEN, recruit))):
        x = MX + i * (cw + 0.3)
        box(s, x, TOP, cw, 4.88)
        dot(s, x + 0.25, TOP + 0.25, 0.22, col)
        text(s, x + 0.6, TOP + 0.15, cw - 0.8, 0.45, h, 18, INK, True, margin=0)
        text(s, x + 0.25, TOP + 0.75, cw - 0.45, 4.0, bullets(items, col), 14, space=8)


KEY_DATE_LABELS = [(r"Cozad registration deadline", "Cozad registration deadline"),
                   (r"Price gate", "price gate"), (r"phantom scans", "Beckman phantom scans at the earliest"),
                   (r"Cozad Demo Showcase", "Cozad finals"), (r"first paid pilot", "earliest first paid pilot"),
                   (r"provisional", "decide on a US provisional"), (r"bar date", "US patent bar date")]


def key_dates(F) -> list[tuple[str, str]]:
    out = []
    for pat, label in KEY_DATE_LABELS:
        for dt, w in F["dates"]:          # every matching row (two bar dates since the 28 Nov pushes)
            if re.search(pat, w):
                out.append((dt, label))
    return out


def s_milestones(d: Deck):
    F = d.F
    ms = F["milestones"]
    s = d.slide("Fundable milestones", "Three milestones that would change what we can claim",
                ["investor/FUNDING_STRATEGY.md §3, §5", "validation/PHANTOM_EXPERIMENT_PROTOCOL.md",
                 "business/REVENUE_MODEL.md O1", "REVIEW_REGISTRY.md", "FOUNDER_DECISIONS.md (key dates)"])
    m2, m3 = dict(ms.get("M2") or {}), dict(ms.get("M3") or {})
    for m in (m2, m3):
        if "what" in m:
            m["what"] = re.sub(r"^Physical phantom study:\s*", "", m["what"])
        for k in ("what", "unlocks"):
            if k in m:
                m[k] = re.sub(r"\s*\([\w/.]+\.md[^)]*\)", "", m[k])
        if "what" in m:
            m["what"] = re.split(r"\.\s*Prerequisites", m["what"])[0]
    cards = [
        ("Physical phantom study", SKY, [
            f"**What**: {m2.get('what', PENDING)}",
            f"**Budget**: {F['phantom_budget'] or PENDING} · **When**: {m2.get('when', PENDING)}",
            f"**Protocol status**: {F['pro_status'] or PENDING}",
            f"**Unlocks**: {m2.get('unlocks', PENDING)}"]),
        ("First paid pilot", ORANGE, [
            f"**What**: {m3.get('what', PENDING)}",
            f"**Price hypothesis**: {_col(_offer(F, 'Paid pilot'), 'Price range')} · **When**: {m3.get('when', PENDING)}",
            "**Needs first**: M0 (entity, university IP determination, insurance, counsel-reviewed contracts) and "
            "Gate 2 (real-data validation for one task, closed human expert review); none met",
            f"**Unlocks**: {m3.get('unlocks', PENDING)}"]),
        ("Human expert review", GREEN, [
            f"**Who**: {F['experts'] or PENDING}",
            "**What**: the advisor rules, held-out designs and every external claim",
            "**Cost**: not yet estimated in any project file (founder decision)",
            "**Unlocks**: replaces reviews by automated agents; required before a pilot-ready release (Gate 2)"]),
    ]
    cw = (CW - 0.6) / 3
    for i, (h, col, items) in enumerate(cards):
        x = MX + i * (cw + 0.3)
        box(s, x, TOP, cw, 3.95)
        badge(s, x + 0.22, TOP + 0.2, str(i + 1), col, 0.42, 15)
        text(s, x + 0.78, TOP + 0.22, cw - 0.95, 0.45, h, 16, INK, True, margin=0)
        text(s, x + 0.22, TOP + 0.8, cw - 0.4, 3.1, items, 13, space=7)
    kd = key_dates(F)
    line = "  ·  ".join(f"**{dt}** {lab}" for dt, lab in kd) or PENDING
    text(s, MX, TOP + 4.12, CW, 0.75, [{"t": "Key dates", "bold": True, "size": 13, "space": 2}, {"t": line}], 12.5,
         space=2)


def s_collab(d: Deck):
    F = d.F
    s = d.slide("Proposed collaboration", "Proposal: a physical known-truth phantom study",
                ["validation/PHANTOM_EXPERIMENT_PROTOCOL.md", "validation/DECISIONS_FOR_IMAGING_SCIENTIST.md",
                 "investor/FUNDING_STRATEGY.md §5", "FOUNDER_DECISIONS.md #11"])
    left = [
        f"**Instrument (planned)**: {F['pro_instrument'] or PENDING}",
        f"**Design**: bovine bone cores with drilled defects, scanned empty, then filled with weighed commercial "
        f"granules ({F['pro_materials'] or PENDING}) or bone chips, and scanned at {F['pro_voxels'] or PENDING}",
        "**Truth by construction**: gravimetric fill and an empty-core pre-scan; scan–rescan; HA calibration",
        f"**Limit**: {F['pro_cannot'] or PENDING}",
        f"**Status**: {F['pro_status'] or PENDING} **Budget**: {F['phantom_budget'] or PENDING}",
    ]
    text(s, MX, TOP, 7.2, 3.3, bullets(left, SKY), 14.5, space=8)
    flow = ["Scan the empty bone core", "Fill the defect with weighed granules",
            f"Rescan at {F['pro_voxels'] or PENDING}", "Compare with truth by construction"]
    bw, gap = (7.2 - 0.3 * 3) / 4, 0.3
    for i, t in enumerate(flow):
        bx = MX + i * (bw + gap)
        box(s, bx, TOP + 3.45, bw, 1.4, CARD)
        badge(s, bx + 0.15, TOP + 3.57, str(i + 1), SKY, 0.36, 13)
        text(s, bx + 0.15, TOP + 4.0, bw - 0.25, 0.85, t, 12.5, space=0)
        if i < 3:
            connector(s, bx + bw + 0.03, TOP + 4.15, bx + bw + gap - 0.03, TOP + 4.15, MUTED, 1.5)
    x, w = 8.15, CW - 7.55
    box(s, x, TOP, w, 4.88)
    text(s, x + 0.25, TOP + 0.15, w - 0.5, 0.45, "What we would ask of you", 17, INK, True, margin=0)
    asks = [
        f"Sign off the {F['n_imaging_decisions'] or PENDING} open protocol decisions (voxel sizes, calibration, "
        "acceptance criteria fixed before unblinding)",
        "Advice on phantom design and endpoint definitions",
        "Co-authorship on a publishable benchmark dataset",
        "Facility-use, data-ownership and IP terms agreed with the university before any scan",
    ]
    text(s, x + 0.25, TOP + 0.7, w - 0.45, 4.1, bullets(asks, GREEN), 14, space=9)


def s_pilot(d: Deck):
    F = d.F
    price = _col(_offer(F, "Paid pilot"), "Price range")
    s = d.slide("Planned pilot", "Planned pilot: a retrospective comparison on scans you already have",
                ["business/REVENUE_MODEL.md O1, §2a", "docs/user/DATA_PROTECTION.md", "RELEASE_READINESS.md",
                 "FOUNDER_DECISIONS.md #5, #7, #18"])
    steps = [
        ("1", f"You choose {F['pilot_scans'] or PENDING} completed scans from a finished study"),
        ("2", "We analyse them alongside your own analysis, blind to your results"),
        ("3", "You receive agreement statistics (ICC, Bland–Altman), every refused endpoint with its reason, and "
              "hands-on time per scan"),
        ("4", "Your study and your own analysis stay exactly as they are"),
    ]
    bw, gap = (CW - 0.4 * 3) / 4, 0.4
    for i, (lab, t) in enumerate(steps):
        x = MX + i * (bw + gap)
        box(s, x, TOP, bw, 2.45)
        badge(s, x + 0.2, TOP + 0.2, lab, ORANGE, 0.44, 15)
        text(s, x + 0.2, TOP + 0.8, bw - 0.35, 1.6, t, 15, space=0)
        if i < 3:
            connector(s, x + bw + 0.05, TOP + 1.12, x + bw + gap - 0.05, TOP + 1.12, MUTED, 2)
    terms = [
        "**Today**: no pilot or evaluation on customer scans is offered, paid or free. Planned only after "
        "incorporation, a data-processing agreement and Gate 1 (not met); offering it is a founder decision.",
        f"**Paid pilot (planned)**: a hypothesised {price}, after Gate 2 as well; the price is part of what we are testing.",
        "**Your data (planned terms)**: a written DPA and data-handling procedure before any scan changes hands; no "
        "training on your scans without your written opt-in; adapted models never used for other customers.",
        "**Scope**: research use. No GLP or Part 11 claim; not for regulatory submission without your own QA review.",
    ]
    text(s, MX, TOP + 2.8, CW, 2.1, bullets(terms), 16, space=10)


def s_evidence_compact(d: Deck):
    F = d.F
    nv = F["l3"]["naive_footprint"]
    t = final_test(F)
    early = [x for x in F["held"] if x is not t]
    s = d.slide("Evidence so far, including failures", "Evidence so far, including what failed",
                [x["file"] for x in F["held"]] + ["exp_L3_displacement.json", "exp_H_I_real.json",
                                                   "exp_G_morphometry.json"])
    box(s, MX, TOP, CW, 2.2)
    text(s, MX + 0.25, TOP + 0.12, CW - 0.5, 2.0, [
        {"t": "Measurement support: final held-out test, in the standard wording", "bold": True, "size": 14,
         "space": 4},
        {"t": standard_phrase(F), "space": 6},
        {"t": caveat(F), "size": 12, "color": MUTED}], 13, space=2)
    items = [
        ("Earlier held-out tests failed before the rules were changed: "
         + "; ".join(f"{x['id']} (advisor {x['advisor']}) on {' and '.join(failed_endpoints(x)) or 'no endpoint'}"
                     for x in early) + ". Each fix was then tested on new, unseen conditions.") if early else
        "Earlier held-out tests: none.",
        f"Day-0 registration (SYNTHETIC): naive day-0 footprint graft Dice — no motion: {num(nv[0], 2)}; 50 µm motion: "
        f"{num(nv[1], 3)}; 100 µm motion: {num(nv[2], 2)}. We do not offer day-0 analysis.",
        f"Real public data, two-class only: U-Net trained on 10 real scans {num(F['h_real10'], 3)} (bone vs "
        f"background); Tb.Th ICC(2,1) {num(F['g_icc'], 3)} against Scanco IPL on {F['g_n'] or PENDING} cubes (border "
        "convention chosen post hoc).",
        "No real graft material has been measured yet. A pilot on real scans, once possible (after incorporation, a "
        "DPA and Gate 1), would be the first real-data test of the refusals.",
    ]
    text(s, MX, TOP + 2.4, CW, 2.5, bullets(items, SKY), 13, space=6)


# ------------------------------------------------------------------------------------------------ decks
def build_investor(F):
    d = Deck(F, "Investor overview")
    s_title(d, "Investor overview · pre-revenue, unincorporated research prototype")
    for f in (s_summary, s_problem, s_product, s_governance, s_abstention, s_consequence, s_heldout, s_failures,
              s_longitudinal, s_realdata, s_unknowns, s_market, s_competition, s_pricing, s_financials, s_team,
              s_milestones):
        f(d)
    d.dark("What we are asking for", [
        "No equity now. " + (F["vc_not"] or "") + " Raising before the phantom result and a paid pilot would sell "
                                                 "equity at maximum uncertainty.",
        "Seeking advisors in imaging science and bone biology, later retrospective pilot partners (no customer data "
        "before incorporation, a DPA and Gate 1), and non-dilutive programmes the founder is eligible for.",
        f"Price gate around {F['gate_date'] or PENDING}; separability gate {F['sep_gate'] or PENDING}. Both must "
        "pass before selling study analysis.",
        "Before any external use of this deck: the founder approves the model assumptions and the university "
        "ownership determination is requested (founder decisions).",
    ], kicker="The ask", notes="Sources: investor/FUNDING_STRATEGY.md §1, §4; business/PRICING_VALIDATION_PLAN.md §7; "
                               "FOUNDER_DECISIONS.md #4, #8.")
    d.save("OsteoQuant_Investor_Deck.pptx")


def build_research(F):
    d = Deck(F, "Research collaboration proposal")
    s_title(d, "Research collaboration proposal · physical phantom benchmark")
    for f in (s_problem, s_abstention, s_consequence, s_heldout, s_failures, s_longitudinal, s_realdata, s_collab,
              s_product, s_team):
        f(d)
    d.dark("What we are asking for", [
        "Twenty minutes of advice on phantom design and endpoint definitions.",
        "If it is useful to you: a joint, publishable benchmark, with university IP and data terms agreed first.",
        "Critical review of the advisor rules and the held-out designs by a human expert.",
    ], kicker="The ask", notes="Sources: validation/PHANTOM_EXPERIMENT_PROTOCOL.md; REVIEW_REGISTRY.md.")
    d.save("OsteoQuant_Research_Collaboration_Deck.pptx")


def build_pilot(F):
    d = Deck(F, "Commercial pilot proposal")
    s_title(d, "Commercial pilot proposal for orthobiologic R&D and CRO imaging teams")
    s_problem(d, buyer=True)
    s_product(d)
    s_abstention(d, buyer=True)
    s_results_screen(d)
    s_consequence(d)
    s_evidence_compact(d)
    s_governance(d)
    s_pilot(d)
    s_pricing(d)
    d.dark("Questions for you", [
        "Which recent study would suit a retrospective comparison once pilots are possible, and which graft "
        "materials and timepoints does it use?",
        "Do your studies acquire a post-operative (day-0) scan, and do you have matched histology?",
        "Who owns the micro-CT analysis decision and its budget?",
    ], kicker="Next step", notes="Sources: business/INTERVIEW_GUIDE.md; business/templates/PILOT_PROPOSAL.md.")
    d.save("OsteoQuant_Commercial_Pilot_Deck.pptx")


def main():
    F = gather()
    if not F["held"]:
        print("warning: no held-out advisor results found; slides print 'pending'")
    if not F["mst"]:
        print("warning: material support table could not be generated; slide prints 'pending'")
    build_investor(F)
    build_research(F)
    build_pilot(F)


if __name__ == "__main__":
    main()
