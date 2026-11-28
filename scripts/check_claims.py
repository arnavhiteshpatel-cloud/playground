"""Claims checker: numbers quoted in documents must match the result files they come from.

Each claim names a value in a result JSON and one or more regular-expression *anchors*. In every
scanned document, wherever an anchor matches, the first decimal number within ``window`` characters
after it must equal the JSON value rounded to the claim's precision. Mismatches and claims never
found are reported; exit status 1 on any mismatch (used in CI).

Add claims to CLAIMS when a number becomes load-bearing in customer-, investor- or grant-facing text.

Cycle-2 additions (review C2-BIZ-01/-02/-14/-20):
* ``docs/reviews/`` is not scanned: reviews quote historical numbers on purpose.
* MONEY_CLAIMS check dollar / percentage figures from the financial-model outputs ($259K, $4.2M, 56%).
* BANNED phrases (compliance-flavoured or overclaiming wording, GLP-supporting offers, advisor-validation numbers from
  superseded advisor versions) fail the check in customer-, investor- and grant-facing files.
* Every advisor version cited in website/, docs/user/ and docs/quality/ must equal ``ADVISOR_VERSION``.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "experiments" / "results"
EXCLUDE_DIRS = ("docs/reviews/",)
SCAN_GLOBS = ["*.md", "docs/**/*.md", "publications/*.md", "investor/*.md", "investor/build_decks.py",
              "founder/*.md", "grants/*.md", "business/*.md", "scripts/build_final_report.py", "website/**/*.html",
              "web/landing/*.html", "investor/*.pptx"]

CLAIMS = [
    # id, json file, path, decimals, anchors
    ("H_unet_real", "exp_H_I_real.json", "summary.unet_trained_on_10_real.dice", 3,
     [r"U-Net\s*\(10 real scans\)", r"U-Net trained on 10 real scans Dice", r"real-only \(10 scans, 800 iters\)"]),
    ("I_zeroshot", "exp_H_I_real.json", "summary.synthetic_unet_zero_shot.dice", 3,
     [r"zero-shot Dice (?=0\.3)", r"[Ss]ynthetic U-Net zero-shot \*{0,2}", r"fails zero-shot \(", r"zero-shot on real data \("]),
    ("I_k1", "exp_H_I_real.json", "summary.synthetic_unet_finetuned_k1.dice", 3,
     [r"\+ 1 real labelled scan \*{0,2}", r"fine-tuning on ONE real labelled scan", r"fine-tuned on 1 real scan"]),
    ("H_otsu", "exp_H_I_real.json", "summary.otsu_in_band.dice", 3, [r"vs Otsu ", r"Dice: Otsu "]),
    ("G_tbth_icc", "exp_G_morphometry.json", "agreement_vs_ipl.TbTh.icc_2_1.icc", 3,
     [r"Tb\.Th ICC(?:\(2,1\))?\s*=?\s*", r"Tb\.Th ICC "]),
    ("G_tbsp_icc", "exp_G_morphometry.json", "agreement_vs_ipl.TbSp.icc_2_1.icc", 3,
     [r"Tb\.Sp ICC(?:\(2,1\))?\s*=?\s*"]),
    ("K_auroc", "exp_K_M_uncertainty.json", "auroc_entropy_id_vs_ood", 2,
     [r"OOD AUROC\s*", r"ID-vs-OOD AUROC\s*", r"\(AUROC\s*"]),
    ("F_day18_conf", "exp_F_roi.json", "real_ovine.0.confidence", 2,
     [r"confidence\s*", r"\(conf\s*"]),
    # Longitudinal day-0 method under granule motion (Experiment L3, naive footprint, no fragmentation). Standard
    # phrase: "naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion: 0.35".
    ("L3_dice_0um", "exp_L3_displacement.json", "summary.0.dice_graft", 2, [r"no motion:\s*"]),
    ("L3_dice_50um", "exp_L3_displacement.json", "summary.8.dice_graft", 3, [r"50 µm motion:\s*"]),
    ("L3_dice_100um", "exp_L3_displacement.json", "summary.16.dice_graft", 2, [r"100 µm motion:\s*"]),
    # Held-out advisor validation (Experiment S1H3, advisor 1.4.1 frozen; 1.4.2 changed only paths S1H3 does not
    # exercise). Standard phrase — quote it whole, with the advisor version and the word SYNTHETIC/simulation:
    # "In the pre-registered held-out simulation S1H3 (advisor 1.4.1; 216 synthetic specimens; a failure is a volume
    # error above 20%): residual graft volume supported in 37% of specimens, every failing measurement refused and none
    # of the supported ones failed (95% upper bound on the supported-failure rate 0.045); supported graft volumes:
    # median error 4.2%, maximum 13.0%; total mineral volume supported in 10% of specimens (sharp imaging only);
    # supported mineral volumes: maximum error 3.2%; new-bone volume never supported."
    # Percent claims carry a scale (6th field); a callable path computes the value.
    ("S1H3_graft_cov", "exp_S1H3_heldout.json", lambda d: _cov(d, "residual_graft_volume"), 0,
     [r"residual graft volume supported in\s*"], 100),
    # C3-SCI-05: rows from one phantom structure are correlated, so the structure-level bound leads
    ("S1H3_graft_bound_struct", "exp_S1H3_heldout.json", lambda d: _struct_bound(d), 2,
     [r"upper bound on the supported-failure rate (?=\d)"]),     # a quoted value, not rule text ("of at most 0.10")
    ("S1H3_graft_bound", "exp_S1H3_heldout.json",
     "summary.0.per_endpoint.residual_graft_volume.p_fail_given_supported_upper95", 3,
     [r"counting phantom structures as the unit;\s*"]),
    ("S1H3_n_struct", "exp_S1H3_heldout.json", lambda d: len({r["structure"] for r in d["rows"]}), 0,
     [r"synthetic specimens from\s*"], 1),
    ("S1H3_no_endpoint", "exp_S1H3_heldout.json", lambda d: _none_share(d), 0,
     [r"no volume endpoint supported for\s*"], 100),
    ("S1H3_graft_median", "exp_S1H3_heldout.json",
     "summary.0.per_endpoint.residual_graft_volume.abs_err_supported_median", 1,
     [r"supported graft volumes: median error\s*"], 100),
    ("S1H3_graft_max", "exp_S1H3_heldout.json",
     "summary.0.per_endpoint.residual_graft_volume.abs_err_supported_max", 1,
     [r"supported graft volumes: median error [\d.]+%, maximum\s*"], 100),
    ("S1H3_mineral_cov", "exp_S1H3_heldout.json", lambda d: _cov(d, "total_mineral_volume"), 0,
     [r"total mineral volume supported in\s*"], 100),
    ("S1H3_mineral_max", "exp_S1H3_heldout.json",
     "summary.0.per_endpoint.total_mineral_volume.abs_err_supported_max", 1,
     [r"supported mineral volumes: maximum error\s*"], 100),
    ("S1H3_n", "exp_S1H3_heldout.json", "summary.0.n", 0, [r"held-out simulation S1H3 \(advisor [\d.]+; "], 1),
]
# guard: S1H3 claims must come from the pre-registered, frozen run
S1H3_REQUIRED = {"preregistered": "docs/science/PREREGISTRATION.md §9", "advisor_version": "1.4.1"}


_SUP = ("supported", "supported_with_conditions")


def _struct_bound(d):
    """Clopper-Pearson 95% upper bound with phantom structures as the unit (0 failing structures)."""
    k = len({r["structure"] for r in d["rows"] if r["status"] in _SUP})
    return 1 - 0.025 ** (1 / k)


def _none_share(d):
    rows = d["rows"]
    return sum(1 for r in rows if all(r[k] not in _SUP for k in ("status", "status_new", "status_mineral"))) / len(rows)


def _cov(d, ep):
    e = d["summary"][0]["per_endpoint"][ep]
    return (e["supported_and_ok"] + e["supported_but_failed"]) / e["n"]
# guard: the L3 rows above must be the naive footprint without fragmentation at 0 / 50 / 100 µm
L3_ROWS = {"L3_dice_0um": (0, 0.0), "L3_dice_50um": (50, 0.0), "L3_dice_100um": (100, 0.0)}

FM = ROOT / "business" / "financial_model_outputs.json"
BB, VB = "Bootstrapped — Base", "Venture — Base"


def _fm(d, key, line, j):
    return d[key][line][j]


def _lic_share(d, key, j=4):
    v = d[key]
    return (v["Academic licence revenue"][j] + v["Enterprise licence revenue"][j]) / v["Total revenue"][j]


# id, value function of the outputs JSON, anchors. The quoted figure after the anchor ($96K, $4.2M, 56%) must equal
# the value at the precision quoted.
MONEY_CLAIMS = [
    ("FM_BB_rev2031", lambda d: _fm(d, BB, "Total revenue", 4),
     [r"Bootstrapped Base 2031 revenue ", r"revenue reaches ", r"2031 revenue \*\*"]),
    ("FM_BB_equity_nogrant", lambda d: _fm(d, BB, "Equity funding requirement (max cumulative deficit)", 0),
     [r"Bootstrapped Base needs about ", r"largest cumulative deficit is about ", r"max deficit ~", r"needs about (?=\$96K)"]),
    ("FM_BB_equity_grant", lambda d: _fm(d, BB, "Equity requirement WITH grants IF awarded (conditional)", 0),
     [r"need would fall to about ", r"deficit would fall to about ", r"reduce that to about "]),
    ("FM_BB_cash2031_nogrant", lambda d: _fm(d, BB, "Cumulative cash - NO grants (lead case)", 4),
     [r"cumulative cash is still about "]),
    ("FM_BB_rev2031_nolicence", lambda d: _fm(d, BB, "Total revenue without licence revenue", 4),
     [r"without licence revenue Base 2031 revenue is ", r"Without licence revenue, 2031 Base revenue is "]),
    ("FM_BB_licence_share", lambda d: _lic_share(d, BB),
     [r"Licences are ", r"Licences make up \*\*", r"Licences are (?=\d+% of Bootstrapped)"]),
    ("FM_VB_equity_nogrant", lambda d: _fm(d, VB, "Equity funding requirement (max cumulative deficit)", 0),
     [r"needs about \*\*(?=\$\d)"]),
    ("FM_VB_equity_grant", lambda d: _fm(d, VB, "Equity requirement WITH grants IF awarded (conditional)", 0),
     [r"\(about (?=\$\d\.\dM if the assumed awards)"]),
    ("FM_VB_rev2031", lambda d: _fm(d, VB, "Total revenue", 4), [r"to reach (?=\$\d)"]),
]
MONEY_RE = re.compile(r"([−-])?\$?(\d+(?:\.\d+)?)\s?([KM%])")
SCALE = {"K": 1e3, "M": 1e6, "%": 0.01}

# Customer-, investor- and grant-facing files and phrases that must not appear in them.
FACING_GLOBS = ["website/*.html", "docs/user/*.md", "investor/*.md", "investor/build_decks.py", "grants/*.md",
                "business/*.md", "business/templates/*.md", "investor/*.pptx", "publications/*.md", "web/landing/*.html",
                "outreach/*.md", "founder/*.md", "FOUNDER_EXECUTIVE_SUMMARY.md"]
BANNED = [
    (r"audit[- ]ready", "compliance-flavoured: use 'tamper-evident audit trail (research prototype; not validated)'"),
    (r"validated (?:analysis )?services?", "no service is validated"),
    (r"validated model", "no model is validated"),
    (r"independent (?:security|science|scientific|expert)?\s*(?:\+ science )?review\b", "reviews are internal and automated"),
    (r"verified morphometry", "use 'agrees with Scanco IPL on 8 public cubes (convention chosen post hoc)'"),
    (r"GLP[- ]supporting|GLP[- ]readiness", "no GLP-related offer may be made"),
    (r"defensible numbers", "overclaim"),
    (r"[Cc]alibrated uncertainty on every endpoint", "not achieved (Experiment K)"),
    (r"\d+\s*(?:of|/)\s*\d+ failures refused", "advisor-validation numbers: use the standard S1H3 phrase (CLAIMS)"),
    (r"P\(fail\s*\\?\|\s*supported\)\s*\d", "advisor-validation numbers: use the standard S1H3 phrase (CLAIMS)"),
    (r"automated tests", "use the CI-generated test count, not a hard-coded one"),
    (r"proven (?:to be )?safe|proves? (?:that )?(?:the advisor|it|OsteoQuant) is safe|guarantee[sd]? (?:that )?(?:no|every)",
     "overclaim: simulation evidence shows internal safety only (C3-SCI-13)"),
]
# bare 'verified' as a quality claim is banned on the website and in the investor one-pager
BANNED_STRICT = {"website/*.html": [r"(?<![Uu]n)(?<!not )\bverified\b"], "investor/ONE_PAGE_OVERVIEW.md": [r"\bverified\b"]}
ALLOW_LINE = re.compile(r"[Nn]ot offered|not sold|[Nn]o GLP|do not|Do not|banned|retired", re.I)

VERSION_GLOBS = ["website/*.html", "docs/user/*.md", "docs/quality/*.md", "investor/*.md", "founder/*.md", "business/*.md",
                 "grants/*.md", "FOUNDER_EXECUTIVE_SUMMARY.md", "deliverables/README.md", "investor/*.pptx",
                 "publications/*.md", "web/landing/*.html"]   # scope widened (C3-BIZ-17)
VERSION_RE = re.compile(r"(?:[Aa]dvisor(?: version)?|ADVISOR_VERSION = \")\s*\**(\d+\.\d+\.\d+)")
VERSION_ALLOW = re.compile(r"history|histor|changelog|earlier|previous|superseded|since|until|before|motivated", re.I)


def _read(f: Path) -> str:
    """Text of a checked file. Decks (.pptx) and PDFs are checked on their extracted text (cycle-3 review C3-BIZ-17:
    the generated decks were outside the checker)."""
    suf = f.suffix.lower()
    if suf == ".pptx":
        try:
            from pptx import Presentation
            prs = Presentation(str(f))
            out = []
            for slide in prs.slides:
                for sh in slide.shapes:
                    if sh.has_text_frame:
                        out.append(sh.text_frame.text)
                    if getattr(sh, "has_table", False) and sh.has_table:
                        out += [c.text for r in sh.table.rows for c in r.cells]
            return "\n".join(out)
        except Exception as e:  # noqa: BLE001
            return f"[unreadable deck: {e}]"
    if suf == ".pdf":
        try:
            import pypdfium2 as pdfium
            doc = pdfium.PdfDocument(str(f))
            return "\n".join(doc[i].get_textpage().get_text_range() for i in range(len(doc)))
        except Exception:  # noqa: BLE001 - pypdfium2 optional
            return ""
    return f.read_text(errors="ignore")


def get(d, path):
    for p in path.split("."):
        d = d[int(p)] if isinstance(d, list) else d[p]
    return d


def _advisor_version() -> str:
    m = re.search(r'ADVISOR_VERSION = "([^"]+)"', (ROOT / "osteoquant" / "advisor" / "separability.py").read_text())
    return m.group(1)


def _excluded(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix() if p.is_absolute() and p.is_relative_to(ROOT) else p.as_posix()
    return any(rel.startswith(d) for d in EXCLUDE_DIRS)


def check_money(files) -> tuple[list[str], dict]:
    bad, found = [], {c[0]: 0 for c in MONEY_CLAIMS}
    if not FM.exists():
        return [f"financial outputs missing: {FM}"], found
    d = json.loads(FM.read_text())
    for cid, fn, anchors in MONEY_CLAIMS:
        want = float(fn(d))
        for f in files:
            text = _read(f)
            for a in anchors:
                for m in re.finditer(a, text):
                    n = MONEY_RE.match(text, m.end()) or MONEY_RE.search(text[m.end(): m.end() + 12])
                    if not n:
                        continue
                    sign = -1 if n.group(1) else 1
                    got = sign * float(n.group(2))
                    nd = len(n.group(2).split(".")[1]) if "." in n.group(2) else 0
                    found[cid] += 1
                    if round(want / SCALE[n.group(3)], nd) != got:
                        line = text[: m.start()].count("\n") + 1
                        bad.append(f"{cid}: {f.relative_to(ROOT)}:{line} quotes {n.group(0)}, model output is "
                                   f"{want:,.0f}" + (" (ratio)" if n.group(3) == "%" else ""))
    return bad, found


def check_banned() -> list[str]:
    bad = []
    files = sorted({p for g in FACING_GLOBS for p in ROOT.glob(g) if p.is_file()})
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        pats = [(re.compile(p, re.I if "verified" not in p else 0), why) for p, why in BANNED]
        for g, extra in BANNED_STRICT.items():
            if f in set(ROOT.glob(g)):
                pats += [(re.compile(p), "quality claim: say what was checked, not 'verified'") for p in extra]
        for i, line in enumerate(_read(f).splitlines(), 1):
            for rx, why in pats:
                if rx.search(line) and not ALLOW_LINE.search(line):
                    bad.append(f"BANNED {rel}:{i}: '{rx.search(line).group(0)}' ({why})")
    return bad


VALIDATION_RUNS = {"S1H3": "exp_S1H3_heldout.json", "S1H2": "exp_S1H2_heldout.json", "S1H": "exp_S1H_heldout.json"}


def _run_versions() -> dict:
    out = {}
    for rid, fn in VALIDATION_RUNS.items():
        try:
            out[rid] = json.loads((RES / fn).read_text()).get("advisor_version")
        except (OSError, ValueError):
            pass
    return out


def check_versions() -> list[str]:
    """Every advisor version cited must be the shipped one, except on history lines or on a line that names a
    validation run (S1H, S1H2, S1H3) whose result file records exactly that version."""
    cur, bad = _advisor_version(), []
    runs = _run_versions()
    files = sorted({p for g in VERSION_GLOBS for p in ROOT.glob(g) if p.is_file()})
    for f in files:
        for i, line in enumerate(_read(f).splitlines(), 1):
            for m in VERSION_RE.finditer(line):
                named = {rid for rid in runs if re.search(rf"\b{rid}\b", line)}
                if any(runs[rid] == m.group(1) for rid in named):
                    continue
                if m.group(1) != cur and not VERSION_ALLOW.search(line):
                    bad.append(f"VERSION {f.relative_to(ROOT)}:{i}: cites advisor {m.group(1)}, shipped is {cur}")
    return bad


def main(paths=None) -> int:
    files = []
    for g in SCAN_GLOBS:
        files += [p for p in ROOT.glob(g) if p.is_file() and not _excluded(p)]
    if paths:
        files = [Path(p).resolve() for p in paths]
    files = sorted(set(files))
    num = re.compile(r"(?<![\d.])(\d+\.\d+)")
    num_scaled = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)")     # percentages and counts may be integers
    bad, found = [], {c[0]: 0 for c in CLAIMS}
    for cid, jf, path, dec, anchors, *rest in CLAIMS:
        scale = rest[0] if rest else None
        jp = RES / jf
        if not jp.exists():
            bad.append(f"{cid}: result file missing {jf}")
            continue
        jd = json.loads(jp.read_text())
        if cid.startswith("S1H3_") and any(jd.get(k) != v for k, v in S1H3_REQUIRED.items()):
            bad.append(f"{cid}: {jf} is not the pre-registered frozen run ({S1H3_REQUIRED})")
        raw = float(path(jd) if callable(path) else get(jd, path)) * (scale or 1)
        want = round(raw, dec)
        for f in sorted(set(files)):
            text = _read(f)
            for a in anchors:
                for m in re.finditer(a, text):
                    window = text[m.end(): m.end() + 40]
                    n = (num_scaled if scale else num).search(window)
                    if not n:
                        continue
                    got = float(n.group(1))
                    qd = len(n.group(1).split(".")[1]) if "." in n.group(1) else 0
                    if qd < dec:     # quoted with fewer decimals: compare at that precision
                        # ...but a non-zero quantity may not be quoted as zero ("0.0" for 0.045, C3-SCI-13)
                        ok = round(raw, qd) == got and not (got == 0 and round(raw, dec) != 0)
                    else:
                        ok = round(got, dec) == want
                    found[cid] += 1
                    if not ok:
                        line = text[: m.start()].count("\n") + 1
                        bad.append(f"{cid}: {f.relative_to(ROOT)}:{line} quotes {got}, result is {want}")
    # L3 rows must be what the claims say they are
    l3 = json.loads((RES / "exp_L3_displacement.json").read_text())["summary"]
    for cid, (dum, frag) in L3_ROWS.items():
        idx = int(next(c[2] for c in CLAIMS if c[0] == cid).split(".")[1])
        r = l3[idx]
        if (r["D_um"], r["F"], r["method"]) != (dum, frag, "naive_footprint"):
            bad.append(f"{cid}: summary row {idx} is {r['method']} D={r['D_um']} F={r['F']}, not naive D={dum} F={frag}")
    mbad, mfound = check_money(files)
    bad += mbad
    found.update(mfound)
    if not paths:
        bad += check_banned()
        bad += check_versions()
    for cid, k in found.items():
        print(f"{cid}: {k} occurrence(s) checked")
    if bad:
        print("\nMISMATCHES:")
        print("\n".join(sorted(set(bad))))
        return 1
    print("All checked claims match their result files.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or None))
