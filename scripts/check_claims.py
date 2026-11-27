"""Claims checker: numbers quoted in documents must match the result files they come from.

Each claim names a value in a result JSON and one or more regular-expression *anchors*. In every
scanned document, wherever an anchor matches, the first decimal number within ``window`` characters
after it must equal the JSON value rounded to the claim's precision. Mismatches and claims never
found are reported; exit status 1 on any mismatch (used in CI).

Add claims to CLAIMS when a number becomes load-bearing in customer-, investor- or grant-facing text.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "experiments" / "results"
SCAN_GLOBS = ["*.md", "docs/**/*.md", "publications/*.md", "investor/*.md", "investor/build_decks.py",
              "founder/*.md", "grants/*.md", "business/*.md", "scripts/build_final_report.py", "website/**/*.html",
              "web/landing/*.html"]

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
]


def get(d, path):
    for p in path.split("."):
        d = d[int(p)] if isinstance(d, list) else d[p]
    return d


def main(paths=None) -> int:
    files = []
    for g in SCAN_GLOBS:
        files += [p for p in ROOT.glob(g) if p.is_file()]
    if paths:
        files = [Path(p) for p in paths]
    num = re.compile(r"(?<![\d.])(\d+\.\d+)")
    bad, found = [], {c[0]: 0 for c in CLAIMS}
    for cid, jf, path, dec, anchors in CLAIMS:
        jp = RES / jf
        if not jp.exists():
            bad.append(f"{cid}: result file missing {jf}")
            continue
        want = round(float(get(json.loads(jp.read_text()), path)), dec)
        for f in sorted(set(files)):
            text = f.read_text(errors="ignore")
            for a in anchors:
                for m in re.finditer(a, text):
                    window = text[m.end(): m.end() + 40]
                    n = num.search(window)
                    if not n:
                        continue
                    got = float(n.group(1))
                    if len(n.group(1).split(".")[1]) < dec:     # quoted with fewer decimals: compare at that precision
                        ok = round(want, len(n.group(1).split(".")[1])) == got
                    else:
                        ok = round(got, dec) == want
                    found[cid] += 1
                    if not ok:
                        line = text[: m.start()].count("\n") + 1
                        bad.append(f"{cid}: {f.relative_to(ROOT)}:{line} quotes {got}, result is {want}")
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
