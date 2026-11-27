"""Assemble a DefectFill report bundle from the study store."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np

from .. import __version__

ENDPOINTS = [
    ("class_volumes.TV_mm3", "Defect TV", "mm³"),
    ("class_volumes.new_bone_volume_mm3", "New bone volume", "mm³"),
    ("class_volumes.new_bone_fraction", "New bone BV/TV", "fraction"),
    ("class_volumes.residual_graft_fraction", "Residual graft volume fraction", "fraction"),
    ("class_volumes.mineral_volume_mm3", "Total mineral volume in defect (new bone + graft)", "mm³"),
    ("class_volumes.mineralized_fraction", "Total mineralised fraction", "fraction"),
    ("bridging_new_bone.projected_coverage", "Projected defect coverage by new bone", "fraction"),
    ("class_volumes.uncertain_fraction", "Uncertain (abstained) fraction", "fraction"),
]


# Data classes a study can carry (set at study creation and recorded in the audit trail). The report banner and
# footer follow the study's class; synthetic or demo data are never labelled as customer data (review QA-REG-15,
# C2-BIZ-05). Unknown or missing values fall back to "research" (the store default), not to "customer".
DATA_CLASSES = ("synthetic", "public", "research", "customer")
_DATA_CLASS_ALIASES = {"demo": "synthetic", "phantom": "synthetic", "simulated": "synthetic", "own": "research",
                       "own_research": "research", "confidential": "customer", "sponsor": "customer"}


def report_data_class(value) -> str:
    v = str(value or "").strip().lower()
    v = _DATA_CLASS_ALIASES.get(v, v)
    return v if v in DATA_CLASSES else "research"


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                              cwd=Path(__file__).parent).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def bundle_from_store(store, user, sid, ctx=None) -> dict:
    import zarr
    from ..report.figures import specimen_panel
    st = store.study(user, sid)
    specs = {s["id"]: s for s in store.specimens(user, sid)}
    tps = {t["id"]: t["label"] for t in store.q("SELECT * FROM timepoints WHERE study_id=?", (sid,))}
    out_specs = []
    figdir = store.data_dir / f"org{user['org_id']}" / "reports" / "fig"
    figdir.mkdir(parents=True, exist_ok=True)
    reviewed_all = True
    meas = store.latest_measurements(user, sid)
    for i, m in enumerate(meas):
        if ctx:
            ctx.progress(0.1 + 0.7 * i / max(1, len(meas)), f"specimen {i+1}/{len(meas)}")
        sc = store.scan(user, m["scan_id"])
        seg = store.q1("SELECT * FROM segmentations WHERE id=?", (m["segmentation_id"],))
        revs = store.reviews(user, "segmentation", seg["id"])
        latest = revs[-1] if revs else None   # the latest decision governs; a later rejection voids an approval
        if not latest or latest["decision"] != "approved" or latest.get("object_sha256") not in (None, seg["labels_sha256"]):
            reviewed_all = False
        sp = specs.get(sc["specimen_id"], {})
        res = m["metrics"]
        corr = [{"version": s["version"], "user": s["created_by"], "time": s["created"], "summary": s["edits"].get("voxel_count_change")}
                for s in store.segmentations(user, m["scan_id"]) if s["kind"] == "corrected"]
        fig = None
        try:
            g = zarr.open_group(sc["store_path"], mode="r")
            img = np.asarray(g["image"][:])
            lab = np.asarray(g[f"labels/{seg['labels_key']}"][:])
            roi = np.asarray(g["labels/roi_current"][:]).astype(bool) if "labels/roi_current" in g else None
            fig = str(figdir / f"scan{m['scan_id']}_seg{seg['id']}.png")
            specimen_panel(img, lab, roi, sc["spacing_um"], fig, title=f"scan {m['scan_id']}")
        except Exception:
            fig = None
        roi_row = store.q1("SELECT * FROM rois WHERE id=?", (m["roi_id"],)) if m["roi_id"] else None
        roi_def = json.loads(roi_row["definition"]) if roi_row else {}
        out_specs.append({
            "specimen_id": sp.get("animal_id", f"scan{m['scan_id']}"), "animal_id": sp.get("animal_id"),
            "group": sp.get("group_name", "—"),
            "timepoint": tps.get(sc["timepoint_id"], "—"),
            "scan": {"source": sc["source_name"], "sha256": sc["file_sha256"], "shape": sc["shape"],
                     "spacing_um": sc["spacing_um"], "acquisition": sc.get("acquisition")},
            "qc": sc.get("qc") or {}, "roi": roi_def,
            "segmentation": {"method": seg["method"], "model_name": seg["model_name"], "model_sha256": seg["model_sha256"],
                             "model_provenance": res.get("segmentation", {}).get("model_provenance")},
            # Reports use the measurement-support view: endpoints the advisor refused are None (shown as "not
            # measured") and listed with their reason (cycle-1 review STAT-01). Raw values stay in the audit record.
            "corrections": corr, "metrics": res.get("reported_metrics", res.get("metrics", {})),
            "suppressed_metrics": res.get("suppressed_metrics", []),
            "measurement_support": {k: {"status": v.get("status"), "reason": v.get("reason"),
                                        "mechanism": v.get("mechanism"), "conditions": v.get("conditions", [])}
                                    for k, v in (res.get("measurement_support") or {}).get("endpoints", {}).items()},
            "advisor_version": (res.get("measurement_support") or {}).get("advisor_version"),
            "analysis_parameters": {k: v for k, v in (res.get("segmentation") or {}).items()
                                    if k in ("method", "t_mineral", "t_graft", "t_graft_rel", "thresholds",
                                             "estimated_graft_share", "advisor_version", "runtime", "onnx_sha256",
                                             "validation_record", "model_name")}
                                   | {k: (res.get("config") or {}).get(k) for k in ("healing_weeks", "healing_weeks_source")
                                      if k in (res.get("config") or {})},
            "uncertainty": res.get("uncertainty", {}),
            "plausibility": res.get("plausibility", []), "figure": fig,
            "reviews": revs})
    data_class = report_data_class(st.get("data_class"))
    return {
        "title": st["name"], "study": {"name": st["name"], "species": st["species"], "defect_model": st["defect_model"],
                                       "graft_materials": st["graft_materials"], "blinded": bool(st["blinded"])},
        "data_class": data_class, "review_status": "reviewed" if (reviewed_all and out_specs) else "unreviewed_automated",
        "specimens": out_specs, "endpoints": ENDPOINTS,
        "methods_text": ("Reconstructed micro-CT volumes were imported with SHA-256 hashing and converted to a chunked store. "
                         "Automated QC was run. The defect ROI was detected automatically or defined manually and stored as an exact "
                         "geometric definition. Segmentation assigned voxels to new bone, residual graft, host bone or background; "
                         "voxels with insufficient confidence were labelled uncertain. Volumes are voxel counts × voxel volume within "
                         "the ROI. Statistics are computed at the specimen level."),
        "limitations": ["Research prototype; methods not validated for regulatory use.",
                        "Graft vs new-bone separation has not been validated on physical ground truth for this material.",
                        "Density values are uncalibrated grey values unless an HA calibration is recorded."],
        "reproducibility": {"software_version": __version__, "git_commit": git_commit()},
        "reviewers": [{"role": "Scientific reviewer", "name": r["full_name"] or r["username"], "meaning": r["meaning"],
                       "decision": r["decision"], "time": r["created"]} for s in out_specs for r in s["reviews"]][:6],
        "audit_excerpt": store.audit.events(org_id=user["org_id"], limit=25),
    }
