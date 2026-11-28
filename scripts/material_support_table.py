#!/usr/bin/env python3
"""Per-material measurement-support table, generated from the shipped advisor (review C2-BIZ-01/-16).

Customer-facing per-material tables (website/science.html, docs/user/MATERIALS_AND_SUPPORT.md) are copied from this
script's output, never written by hand. The output carries ``ADVISOR_VERSION`` so a stale table is detectable, and
``scripts/check_claims.py`` checks that every advisor version cited in customer-facing documents equals it.

Illustrative setting (same as the website): noise 0.08 of the bone/soft-tissue contrast, 20 µm voxels, estimated
graft share 0.30 of mineral, no measured references. Day-0 columns assume a registered day-0 scan with QC passed,
5% untracked graft and the stated granule motion (the 200 µm policy tolerance applies).

    python3 scripts/material_support_table.py            # markdown table to stdout
    python3 scripts/material_support_table.py --json     # machine-readable
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osteoquant.advisor.separability import ADVISOR_VERSION, assess_support  # noqa: E402
from osteoquant.knowledge import load_materials  # noqa: E402

SETTING = {"noise_rel": 0.08, "voxel_um": 20.0, "graft_prior": 0.3}
COLUMNS = [("unknown", {"healing_weeks": None}), ("2 wk", {"healing_weeks": 2.0}), ("8 wk", {"healing_weeks": 8.0}),
           ("day-0, 0 µm, unknown wk", {"healing_weeks": None, "day0": 0.0}),
           ("day-0, 50 µm, unknown wk", {"healing_weeks": None, "day0": 50.0})]
SYMBOL = {"supported": "S", "supported_with_conditions": "C", "not_supported": "-"}


def _day0(disp):
    return {"registered": True, "qc_pass": True, "untracked_fraction": 0.05, "max_displacement_um": disp,
            "tolerance_um": 200}


def table() -> dict:
    kb = load_materials()
    rows = []
    for mid in kb:
        row = {"material": mid, "name": kb[mid].get("name", mid), "cells": {}}
        for col, opt in COLUMNS:
            kw = dict(SETTING, healing_weeks=opt["healing_weeks"])
            if "day0" in opt:
                kw["day0"] = _day0(opt["day0"])
            a = assess_support(mid, **kw)
            row["cells"][col] = {
                "graft": a.endpoints["residual_graft_volume"].status,
                "new_bone": a.endpoints["new_bone_volume"].status,
                "mineral": a.endpoints["total_mineral_volume"].status,
                "reason": a.endpoints["residual_graft_volume"].reason}
        rows.append(row)
    return {"advisor_version": ADVISOR_VERSION, "setting": SETTING, "rows": rows}


SCAN = {"model": "condyle", "shape": (40, 56, 56), "voxel_um": 40.0, "psf_um": 20.0, "noise_sigma": 40.0,
        "stage": 0.5, "diameter_um": 1400.0, "seed": 3}
SCAN_COLUMNS = [("unknown", {"healing_weeks": None}), ("2 wk", {"healing_weeks": 2.0}), ("8 wk", {"healing_weeks": 8.0}),
                ("day-0 scan, 4 wk", {"healing_weeks": 4.0, "day0": 0.0})]


def scan_table() -> dict:
    """Decisions of the FULL per-scan advisor (scan-measured noise, blur, granule thickness, graft level, ambiguous
    rim) on one synthetic condyle phantom per material (cycle-3 review C3-BIZ-01: the intensity-only table above skips
    the scan-measured checks that do most of the refusing, so it overstated new-bone support)."""
    from osteoquant.advisor.integration import support_for_scan
    from osteoquant.phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast
    kb = load_materials()
    rows = []
    for mid in kb:
        try:
            ph = generate_phantom(PhantomConfig(model=SCAN["model"], shape=SCAN["shape"], voxel_um=SCAN["voxel_um"],
                                                supersample=1, defect_diameter_um=SCAN["diameter_um"],
                                                healing_stage=SCAN["stage"], graft_material=mid, seed=SCAN["seed"]))
        except Exception as e:  # noqa: BLE001 - a material the phantom generator does not model
            rows.append({"material": mid, "name": kb[mid].get("name", mid), "error": str(e)[:80], "cells": {}})
            continue
        img = render_fast(ph.mu, SCAN["voxel_um"], ImagingConfig(psf_sigma_um=SCAN["psf_um"],
                                                                 noise_sigma=SCAN["noise_sigma"], seed=SCAN["seed"])).data
        row = {"material": mid, "name": kb[mid].get("name", mid), "cells": {}}
        for col, opt in SCAN_COLUMNS:
            cfg = {"material": mid, "healing_weeks": opt["healing_weeks"]}
            if "day0" in opt:
                cfg["day0"] = _day0(opt["day0"])
            d = support_for_scan(img, ph.roi_mask, (SCAN["voxel_um"],) * 3, cfg)["endpoints"]
            row["cells"][col] = {"graft": d["residual_graft_volume"]["status"], "new_bone": d["new_bone_volume"]["status"],
                                 "mineral": d["total_mineral_volume"]["status"],
                                 "reason": d["residual_graft_volume"]["reason"]}
        rows.append(row)
    return {"advisor_version": ADVISOR_VERSION, "scan": SCAN, "rows": rows, "mode": "scan"}


def scan_markdown(t: dict) -> str:
    head = ["Material"] + [c for c, _ in SCAN_COLUMNS]
    sc = t["scan"]
    out = [f"Generated by `scripts/material_support_table.py` from advisor **{t['advisor_version']}**, full per-scan "
           f"decision on one SYNTHETIC {sc['model']} phantom per material ({sc['voxel_um']:g} µm voxels, PSF "
           f"{sc['psf_um']:g} µm, noise σ {sc['noise_sigma']:g}, healing stage {sc['stage']}). Cell = graft / new bone / "
           "total mineral: S supported, C supported with conditions, - not supported. Day-0 column: registered day-0 "
           "scan with QC passed, no granule motion (the single-scan pipeline never applies it).", "",
           "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in t["rows"]:
        if not r["cells"]:
            out.append(f"| {r['name']} | " + " | ".join(["(not simulated)"] * len(SCAN_COLUMNS)) + " |")
            continue
        cells = [f"{SYMBOL[c['graft']]} / {SYMBOL[c['new_bone']]} / {SYMBOL[c['mineral']]}"
                 for c in (r["cells"][col] for col, _ in SCAN_COLUMNS)]
        out.append(f"| {r['name']} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def markdown(t: dict) -> str:
    head = ["Material"] + [c for c, _ in COLUMNS]
    out = [f"Generated by `scripts/material_support_table.py` from advisor **{t['advisor_version']}** "
           f"(noise {t['setting']['noise_rel']}, {t['setting']['voxel_um']:g} µm voxels, graft share "
           f"{t['setting']['graft_prior']}). Cell = graft / new bone / total mineral: S supported, C supported with "
           "conditions, - not supported.", "",
           "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in t["rows"]:
        cells = [f"{SYMBOL[c['graft']]} / {SYMBOL[c['new_bone']]} / {SYMBOL[c['mineral']]}"
                 for c in (r["cells"][col] for col, _ in COLUMNS)]
        out.append(f"| {r['name']} | " + " | ".join(cells) + " |")
    return "\n".join(out)


if __name__ == "__main__":
    # default: the full per-scan decision on a synthetic phantom; --intensity-only: the rule without scan-measured
    # checks (an upper bound on support; never published as the material table)
    if "--intensity-only" in sys.argv:
        t = table()
        print(json.dumps(t, indent=1) if "--json" in sys.argv else markdown(t))
    else:
        t = scan_table()
        print(json.dumps(t, indent=1) if "--json" in sys.argv else scan_markdown(t))
