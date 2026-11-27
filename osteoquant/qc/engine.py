"""Micro-CT scan quality-control engine.

Each check returns a record::

    {"id", "name", "status": pass|warn|fail|info, "value", "threshold", "basis", "message"}

``basis`` is one of:
* "deterministic" — a factual property of the file/metadata (e.g. spacing present, missing
  slice indices, saturated voxel count). These are exact, not statistical judgements.
* "heuristic"     — an OsteoQuant-defined score with a threshold chosen by the developers
  (ring score, cupping index, noise CNR, partial-volume risk...). Heuristic thresholds are NOT
  established scientific standards; they flag scans for analyst attention only. Their
  sensitivity on controlled synthetic artefacts is measured in Experiment E.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

from ..volume import Volume

QC_VERSION = "0.1.0"

REQUIRED_METADATA = ["spacing_um", "scanner_model", "voltage_kv", "current_ua", "filter",
                     "exposure_ms", "reconstruction_software", "calibration", "species",
                     "anatomical_site", "timepoint", "specimen_id"]


def _rec(id_, name, status, value=None, threshold=None, basis="heuristic", message=""):
    return {"id": id_, "name": name, "status": status, "value": value, "threshold": threshold,
            "basis": basis, "message": message}


def _sample(vol: Volume, max_vox=2_000_000):
    d = vol.data
    step = max(1, int(np.ceil((d.size / max_vox) ** (1 / 3))))
    return d[::step, ::step, ::step].astype(np.float32), step


def _modes(x):
    """Two-class Otsu split of a sample; returns (t, low-mode stats, high-mode stats)."""
    from skimage.filters import threshold_otsu
    v = x.ravel()
    v = v[np.isfinite(v)]
    t = float(threshold_otsu(v))
    lo, hi = v[v <= t], v[v > t]
    return t, lo, hi


def metadata_completeness(vol: Volume, extra: dict | None = None) -> dict:
    meta = dict(vol.meta)
    ing = meta.get("ingest", {})
    found = dict(ing.get("metadata_found", {}))
    found.update(extra or {})
    present = {}
    for k in REQUIRED_METADATA:
        v = found.get(k, meta.get(k))
        if k == "spacing_um":
            v = found.get("spacing_um") or found.get("spacing_um_user")
        if k == "calibration":
            v = meta.get("calibration")
        if k == "voltage_kv" and not v:
            v = found.get("recon:SourceVoltage") or found.get("Source Voltage (kV)")
        present[k] = v not in (None, "", 0, 0.0)
    score = sum(present.values()) / len(present)
    return {"score": score, "present": present, "assumed": ing.get("metadata_assumed", {})}


def ring_score(vol: Volume, n_slices=12) -> dict:
    """Ring-artefact score: radial profile of the angular mean of a high-pass-filtered axial
    slice, about the reconstruction centre (assumed = image centre). Rings are concentric and
    survive angular averaging; anatomy mostly does not. Score = std of that radial profile
    divided by the image noise σ (MAD of the high-pass image)."""
    d = vol.data
    Z, Y, X = d.shape
    yy, xx = np.mgrid[:Y, :X]
    r = np.sqrt((yy - (Y - 1) / 2) ** 2 + (xx - (X - 1) / 2) ** 2).astype(int)
    rmax = int(0.85 * min(Y, X) / 2)  # stay inside reconstruction circle / away from FOV edge
    profs, noise = [], []
    for z in np.linspace(Z * 0.2, Z * 0.8, n_slices).astype(int):
        s = d[z].astype(np.float32)
        hp = s - ndi.gaussian_filter(s, 2.0)
        noise.append(1.4826 * np.median(np.abs(hp - np.median(hp))))
        valid = (s != 0) & (r < rmax)
        prof = np.array(ndi.mean(hp, np.where(valid, r, rmax + 1), index=np.arange(rmax)))
        profs.append(prof)
    prof = np.mean(profs, axis=0)
    sig = float(np.median(noise)) + 1e-9
    # ignore centre few pixels (few samples)
    prof = np.nan_to_num(prof)
    score = float(np.std(prof[5:]) / sig)
    return {"score": score, "limitation": "concentric anatomy or a cylindrical sample holder also raises this score", "radial_profile": prof.tolist(), "noise_sigma": sig}


def cupping_index(vol: Volume, mask_low=None) -> dict:
    """Beam-hardening-like cupping: relative difference between mean intensity of the lower
    (soft-tissue/background) mode near the centre vs near the periphery of the FOV."""
    x, step = _sample(vol)
    t, _, _ = _modes(x)
    Z, Y, X = x.shape
    yy, xx = np.mgrid[:Y, :X]
    r = np.sqrt((yy - (Y - 1) / 2) ** 2 + (xx - (X - 1) / 2) ** 2) / (min(Y, X) / 2)
    low = (x <= t) & (x > np.percentile(x, 1))
    inner = low & (r < 0.3)[None]
    outer = low & ((r > 0.6) & (r < 0.9))[None]
    if inner.sum() < 100 or outer.sum() < 100:
        return {"index": float("nan"), "note": "insufficient homogeneous low-density region"}
    a, b = float(x[inner].mean()), float(x[outer].mean())
    spread = float(np.percentile(x, 99) - np.percentile(x, 1)) + 1e-9
    return {"index": (b - a) / spread, "inner_mean": a, "outer_mean": b}


def noise_cnr(vol: Volume) -> dict:
    x, _ = _sample(vol)
    t, lo, hi = _modes(x)
    hp = x - ndi.gaussian_filter(x, 1.5)
    sig = float(1.4826 * np.median(np.abs(hp[x <= t] - np.median(hp[x <= t])))) + 1e-9
    cnr = float((np.median(hi) - np.median(lo)) / sig) if hi.size and lo.size else float("nan")
    return {"noise_sigma": sig, "cnr_bone_soft": cnr, "otsu_t": t}


def saturation(vol: Volume) -> dict:
    d = vol.data
    if np.issubdtype(d.dtype, np.integer):
        info = np.iinfo(d.dtype)
        lo, hi = info.min, info.max
    else:
        lo, hi = float(d.min()), float(d.max())
    x, _ = _sample(vol)
    f_hi = float((x >= hi).mean())
    f_lo = float((x <= lo).mean())
    return {"frac_at_max": f_hi, "frac_at_min": f_lo, "dtype": str(d.dtype)}


def slice_consistency(vol: Volume) -> dict:
    """Blank slices and abrupt slice-to-slice jumps in mean intensity (motion / stitching /
    reconstruction-segment boundaries)."""
    d = vol.data
    step = max(1, d.shape[1] // 128)
    m = d[:, ::step, ::step].reshape(d.shape[0], -1).astype(np.float32)
    means, stds = m.mean(1), m.std(1)
    blank = np.where(stds < 1e-6 * (np.abs(means) + 1))[0].tolist()
    dm = np.abs(np.diff(means))
    mad = 1.4826 * np.median(np.abs(dm - np.median(dm))) + 1e-9
    jumps = np.where(dm > np.median(dm) + 8 * mad)[0].tolist()
    return {"blank_slices": blank, "jump_after_slices": jumps[:50], "n_jumps": len(jumps)}


def truncation(vol: Volume) -> dict:
    """Fraction of each face of the volume occupied by mineral (bone cut by the FOV)."""
    x, _ = _sample(vol)
    t, _, _ = _modes(x)
    m = x > t
    faces = {"z0": m[0], "z1": m[-1], "y0": m[:, 0], "y1": m[:, -1], "x0": m[:, :, 0], "x1": m[:, :, -1]}
    return {k: float(v.mean()) for k, v in faces.items()}


def orientation(vol: Volume) -> dict:
    """Principal axis of mineralised voxels (PCA) and its angle to the nearest image axis."""
    x, step = _sample(vol, 500_000)
    t, _, _ = _modes(x)
    pts = np.argwhere(x > t).astype(float) * np.asarray(vol.spacing) * step
    if len(pts) < 50:
        return {"angle_deg": float("nan")}
    pts -= pts.mean(0)
    w, v = np.linalg.eigh(np.cov(pts.T))
    ax = v[:, -1]
    ang = float(np.degrees(np.arccos(np.max(np.abs(ax)))))
    elong = float(np.sqrt(w[-1] / max(w[-2], 1e-9)))
    return {"principal_axis_zyx": ax.tolist(), "angle_to_nearest_axis_deg": ang, "elongation": elong}


def partial_volume_risk(vol: Volume) -> dict:
    """Median local half-thickness of mineral structures in voxels (EDT on a sub-volume).
    Structures < ~2–3 voxels across are dominated by partial-volume effects (heuristic)."""
    d = vol.data
    c = [n // 2 for n in d.shape]
    h = [min(48, n // 2) for n in d.shape]
    sub = d[c[0] - h[0]:c[0] + h[0], c[1] - h[1]:c[1] + h[1], c[2] - h[2]:c[2] + h[2]].astype(np.float32)
    t, _, _ = _modes(sub)
    m = sub > t
    if m.sum() < 100:
        return {"median_thickness_vox": float("nan")}
    edt = ndi.distance_transform_edt(m)
    ridge = (edt >= ndi.maximum_filter(edt, 3) - 1e-6) & m
    th = 2 * edt[ridge]
    return {"median_thickness_vox": float(np.median(th)), "p10_thickness_vox": float(np.percentile(th, 10))}


def histogram(vol: Volume, bins=256) -> dict:
    x, _ = _sample(vol)
    h, e = np.histogram(x, bins=bins)
    return {"counts": h.tolist(), "edges": e.tolist()}


def run_qc(vol: Volume, extra_metadata: dict | None = None, intended_analysis: str = "defect_fill") -> dict:
    checks = []
    ing = vol.meta.get("ingest", {})
    # ---------------- deterministic
    md = metadata_completeness(vol, extra_metadata)
    sp_found = md["present"]["spacing_um"] and "spacing_um" not in md["assumed"]
    checks.append(_rec("QC-D01", "Voxel spacing from metadata", "pass" if sp_found else "fail",
                       list(vol.spacing), None, "deterministic",
                       "" if sp_found else "Spacing was assumed — all physical measurements invalid until confirmed"))
    checks.append(_rec("QC-D02", "Isotropic voxels", "pass" if vol.is_isotropic else "warn", list(vol.spacing),
                       None, "deterministic", "" if vol.is_isotropic else "Thickness metrics require isotropic resampling"))
    ms = ing.get("missing_slices", [])
    checks.append(_rec("QC-D03", "Missing slices", "fail" if ms else "pass", len(ms), 0, "deterministic",
                       f"Missing indices: {ms[:10]}" if ms else ""))
    errs = ing.get("errors", [])
    checks.append(_rec("QC-D04", "Ingest errors (corrupt/inconsistent slices)", "fail" if errs else "pass",
                       len(errs), 0, "deterministic", "; ".join(errs[:3])))
    sat = saturation(vol)
    s_stat = "warn" if sat["frac_at_max"] > 0.001 else "pass"
    checks.append(_rec("QC-D05", "Saturated voxels (at dtype max)", s_stat, sat["frac_at_max"], 0.001, "deterministic",
                       "Clipped high values bias density and BV of dense materials" if s_stat == "warn" else ""))
    sc = slice_consistency(vol)
    checks.append(_rec("QC-D06", "Blank slices", "warn" if sc["blank_slices"] else "pass", len(sc["blank_slices"]), 0,
                       "deterministic", str(sc["blank_slices"][:10]) if sc["blank_slices"] else ""))
    calib = "calibration" in vol.meta
    checks.append(_rec("QC-D07", "Density calibration available", "pass" if calib else "info", calib, None,
                       "deterministic", "" if calib else "No HA calibration: density reported as uncalibrated grey"))
    checks.append(_rec("QC-D08", "Acquisition metadata completeness", "pass" if md["score"] >= 0.75 else "warn",
                       round(md["score"], 2), 0.75, "deterministic",
                       "Missing: " + ", ".join(k for k, v in md["present"].items() if not v)))
    res = vol.meta.get("resampling", [])
    up = any(np.max(np.array(r["from_um"]) / np.array(r["to_um"])) > 1.5 for r in res)
    checks.append(_rec("QC-D09", "Excessive upsampling", "warn" if up else "pass", res, 1.5, "deterministic",
                       "Volume was upsampled >1.5x; apparent resolution exceeds true resolution" if up else ""))
    # ---------------- heuristic
    nc = noise_cnr(vol)
    checks.append(_rec("QC-H01", "Bone/soft-tissue CNR", "pass" if nc["cnr_bone_soft"] >= 5 else "warn",
                       round(nc["cnr_bone_soft"], 2), 5.0, "heuristic",
                       "Low CNR: threshold-based segmentation unreliable" if nc["cnr_bone_soft"] < 5 else ""))
    rs = ring_score(vol)
    checks.append(_rec("QC-H02", "Ring artefact score", "warn" if rs["score"] > 0.25 else "pass", round(rs["score"], 3),
                       0.25, "heuristic", "Concentric ring pattern detected" if rs["score"] > 0.25 else ""))
    cu = cupping_index(vol)
    ci = cu.get("index", float("nan"))
    checks.append(_rec("QC-H03", "Beam-hardening-like cupping index", "warn" if np.isfinite(ci) and abs(ci) > 0.03 else
                       ("info" if not np.isfinite(ci) else "pass"), None if not np.isfinite(ci) else round(ci, 4), 0.03,
                       "heuristic", cu.get("note", "")))
    checks.append(_rec("QC-H04", "Slice-to-slice intensity jumps (motion/stitching; also fires on anatomy)", "info" if sc["n_jumps"] else "pass",
                       sc["n_jumps"], 0, "heuristic", f"after slices {sc['jump_after_slices'][:10]}" if sc["n_jumps"] else ""))
    tr = truncation(vol)
    mt = max(tr.values())
    checks.append(_rec("QC-H05", "Anatomy truncated by field of view", "warn" if mt > 0.05 else "pass", round(mt, 3), 0.05,
                       "heuristic", "Mineral touches volume border; ensure ROI is fully inside FOV" if mt > 0.05 else ""))
    ori = orientation(vol)
    ang = ori.get("angle_to_nearest_axis_deg", float("nan"))
    checks.append(_rec("QC-H06", "Long-axis alignment", "warn" if np.isfinite(ang) and ang > 15 and ori.get("elongation", 1) > 1.5
                       else "pass", None if not np.isfinite(ang) else round(ang, 1), 15, "heuristic",
                       "Specimen oblique to image axes; axis-based ROIs/profiles need reorientation" if np.isfinite(ang) and ang > 15 else ""))
    pv = partial_volume_risk(vol)
    mtv = pv.get("median_thickness_vox", float("nan"))
    checks.append(_rec("QC-H07", "Partial-volume risk (median structure thickness)", "warn" if np.isfinite(mtv) and mtv < 3
                       else "pass", None if not np.isfinite(mtv) else round(mtv, 2), 3.0, "heuristic",
                       "Structures < 3 voxels thick: BV and Tb.Th strongly resolution-dependent" if np.isfinite(mtv) and mtv < 3 else ""))
    n_fail = sum(c["status"] == "fail" for c in checks)
    n_warn = sum(c["status"] == "warn" for c in checks)
    verdict = "unsuitable" if n_fail else ("review" if n_warn else "suitable")
    return {"qc_version": QC_VERSION, "intended_analysis": intended_analysis, "verdict": verdict,
            "n_fail": n_fail, "n_warn": n_warn, "checks": checks,
            "maps": {"ring_radial_profile": rs["radial_profile"], "histogram": histogram(vol)},
            "metadata_completeness": md, "summary": vol.summary(),
            "disclaimer": "Heuristic checks use developer-chosen thresholds; they are not established standards."}
