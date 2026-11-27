"""Per-endpoint support status for analysis results.

``measurement_support(result)`` is the single hook that decides, for each reported endpoint,
whether the measurement is *supported*, *flagged* (reportable with caution) or *not supported*.
The current implementation only consumes flags that the pipeline already returns (QC verdict,
plausibility checks, abstention, ROI review requirement, voxel isotropy) plus the
measurement-support advisor output stored by the pipeline (``result["measurement_support"]``).
``_separability_assessment`` below is the plug-in point for the advisor; its contract is
documented there.
"""
from __future__ import annotations

SUPPORTED, FLAGGED, NOT_SUPPORTED = "supported", "flagged", "not supported"
_RANK = {SUPPORTED: 0, FLAGGED: 1, NOT_SUPPORTED: 2}

# endpoint key -> (label, unit, path inside result["metrics"], scale for display)
ENDPOINTS = [
    ("TV_mm3", "Defect TV", "mm³", "class_volumes.TV_mm3", 1.0),
    ("new_bone_volume_mm3", "New bone volume", "mm³", "class_volumes.new_bone_volume_mm3", 1.0),
    ("new_bone_fraction", "New bone BV/TV", "%", "class_volumes.new_bone_fraction", 100.0),
    ("residual_graft_fraction", "Residual graft", "%", "class_volumes.residual_graft_fraction", 100.0),
    ("mineralized_fraction", "Mineralised", "%", "class_volumes.mineralized_fraction", 100.0),
    ("uncertain_fraction", "Uncertain", "%", "class_volumes.uncertain_fraction", 100.0),
    ("Tb_Th_um", "Tb.Th (new bone)", "µm", "new_bone_architecture.Tb_Th_um", 1.0),
    ("Tb_Sp_um", "Tb.Sp (new bone)", "µm", "new_bone_architecture.Tb_Sp_um", 1.0),
    ("Tb_N_per_mm", "Tb.N (new bone)", "1/mm", "new_bone_architecture.Tb_N_per_mm", 1.0),
    ("projected_coverage", "Defect coverage", "%", "bridging_new_bone.projected_coverage", 100.0),
]


def get_path(d, path, default=None):
    cur = d
    for k in path.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur


def _worse(a, b):
    return a if _RANK[a] >= _RANK[b] else b


# advisor endpoint (osteoquant.advisor.integration.ENDPOINT_METRICS) -> desktop endpoint keys
ADVISOR_ENDPOINT_MAP = {
    "residual_graft_volume": ["residual_graft_fraction"],
    "graft_fraction_of_defect": ["residual_graft_fraction"],
    "new_bone_volume": ["new_bone_volume_mm3"],
    "new_bone_fraction_of_defect": ["new_bone_fraction", "projected_coverage"],
    "new_bone_thickness": ["Tb_Th_um", "Tb_Sp_um", "Tb_N_per_mm"],
    "mineral_fraction_of_defect": ["mineralized_fraction"],
}
ADVISOR_STATUS = {"supported": SUPPORTED, "supported_with_conditions": FLAGGED, "not_supported": NOT_SUPPORTED}


def _separability_assessment(result: dict) -> list[dict]:
    """HOOK for the separability / measurement-support advisor.

    Returns a list of ``{"status": supported|flagged|not supported, "reason": str,
    "endpoints": [desktop endpoint keys]}``. The default reads the advisor output that the
    pipeline stores in ``result["measurement_support"]["endpoints"]`` (advisor endpoint ->
    {status, reason, ...}); replace or extend this function to plug in a different advisor."""
    try:
        from ..advisor.integration import measurement_support as advisor_endpoints
        endpoints = advisor_endpoints(result or {}) or {}
    except ImportError:   # library without the advisor
        endpoints = ((result or {}).get("measurement_support") or {}).get("endpoints") or {}
    out = []
    for ep, info in endpoints.items():
        keys = ADVISOR_ENDPOINT_MAP.get(ep)
        st = ADVISOR_STATUS.get(str((info or {}).get("status")))
        if not keys or not st:
            continue
        reason = (info or {}).get("reason") or ep.replace("_", " ")
        out.append({"status": st, "reason": f"advisor: {reason}", "endpoints": keys})
    return out


def measurement_support(result: dict) -> dict:
    """Return ``{"overall": status, "endpoints": {key: {"status", "reasons"}}, "reasons": [...]}``.

    ``overall`` is *supported* when every endpoint is supported, *not supported* when none is
    (or there is no analysis), otherwise *flagged* (some endpoints need caution or are not
    reportable; see the per-endpoint statuses).

    ``result`` is a stored measurement (``public(analyze(...))`` or a corrected-version record)
    or a job result; missing parts are treated conservatively."""
    eps = {k: {"status": SUPPORTED, "reasons": []} for k, *_ in ENDPOINTS}
    general: list[str] = []

    def flag(keys, status, reason):
        for k in keys:
            e = eps[k]
            e["status"] = _worse(e["status"], status)
            if reason not in e["reasons"]:
                e["reasons"].append(reason)

    all_keys = list(eps)
    status = (result or {}).get("status")
    metrics = (result or {}).get("metrics") or {}
    if status == "needs_manual_roi" or not metrics:
        flag(all_keys, NOT_SUPPORTED, "no analysis result (ROI not detected or analysis not run)")
        return {"overall": NOT_SUPPORTED, "endpoints": eps, "reasons": ["no analysis result"]}

    qc = result.get("qc") or {}
    verdict = qc.get("verdict")
    if verdict == "unsuitable":
        failed = [c["name"] for c in qc.get("checks", []) if c.get("status") == "fail"]
        flag(all_keys, FLAGGED, "QC unsuitable: " + ", ".join(failed[:3]))
    elif verdict == "review":
        general.append("QC requires review")

    for p in result.get("plausibility") or []:
        if not p.get("ok", True):
            flag(all_keys, FLAGGED, f"plausibility: {p.get('check')}")

    roi = result.get("roi") or {}
    if (roi.get("diagnostics") or {}).get("requires_review"):
        general.append("automatic ROI requires review")
        flag(all_keys, FLAGGED, "automatic ROI requires review")

    unc = get_path(metrics, "class_volumes.uncertain_fraction", 0.0) or 0.0
    if unc > 0.25:
        flag(all_keys, NOT_SUPPORTED, f"uncertain fraction {unc:.0%} > 25%")
    elif unc > 0.10:
        flag(all_keys, FLAGGED, f"uncertain fraction {unc:.0%} > 10%")

    arch = metrics.get("new_bone_architecture") or {}
    if "Tb_Th_um" not in arch:
        flag(["Tb_Th_um", "Tb_Sp_um", "Tb_N_per_mm"], NOT_SUPPORTED,
             arch.get("note", "thickness metrics not computed"))
    else:
        sp = get_path(result, "qc.summary.spacing_um") or []
        tbth = arch.get("Tb_Th_um")
        if sp and tbth and tbth < 2.5 * min(sp):
            flag(["Tb_Th_um"], FLAGGED, "Tb.Th below 2.5 voxels: partial-volume dominated")

    cfg = result.get("config") or {}
    if cfg.get("no_graft"):
        flag(["residual_graft_fraction"], NOT_SUPPORTED, "no-graft configuration")

    for sep in _separability_assessment(result):
        if sep["status"] != SUPPORTED:
            flag(sep["endpoints"], sep["status"], sep["reason"])

    sts = [e["status"] for e in eps.values()]
    if all(s == SUPPORTED for s in sts):
        overall = SUPPORTED
    elif all(s == NOT_SUPPORTED for s in sts):
        overall = NOT_SUPPORTED
    else:
        overall = FLAGGED
    n_ns = sum(s == NOT_SUPPORTED for s in sts)
    reasons = general + ([f"{n_ns} of {len(sts)} endpoints not supported"] if n_ns and overall != NOT_SUPPORTED else []) \
        + sorted({r for e in eps.values() for r in e["reasons"]})
    return {"overall": overall, "endpoints": eps, "reasons": reasons}


def suppressed_reasons(result: dict) -> dict:
    """metric path -> reason for metrics the advisor suppressed (reported value is None)."""
    return {d.get("metric"): d.get("reason", "") for d in (result or {}).get("suppressed_metrics") or []}


def reported_value(result: dict, path: str):
    """(value, reason). Uses ``reported_metrics`` (unsupported endpoints are None) when the
    pipeline produced it, else the raw metrics. ``reason`` explains a None value."""
    rep = (result or {}).get("reported_metrics")
    src = rep if isinstance(rep, dict) else (result or {}).get("metrics") or {}
    v = get_path(src, path)
    if v is not None:
        return v, ""
    sup = suppressed_reasons(result)
    for m, r in sup.items():
        if m and (path == m or path.startswith(m + ".")):
            return None, r or "not supported by the measurement-support advisor"
    if rep is not None and get_path(result.get("metrics") or {}, path) is not None:
        return None, "not supported by the measurement-support advisor"
    return None, "not computed"
