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
# no measurement-support assessment exists for the endpoint (advisor output missing or unreadable): never
# shown as supported and, like "not supported", reported without a number (C2-PRD-12)
NOT_ASSESSED = "not assessed"
_RANK = {SUPPORTED: 0, FLAGGED: 1, NOT_ASSESSED: 2, NOT_SUPPORTED: 3}
NO_NUMBER = (NOT_SUPPORTED, NOT_ASSESSED)
NO_ASSESSMENT_REASON = "no measurement-support assessment (advisor output missing or not recognised)"

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
# desktop endpoints whose support depends on graft / new-bone separability (assessed by the advisor)
ADVISOR_KEYS = sorted({k for keys in ADVISOR_ENDPOINT_MAP.values() for k in keys})


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
    covered: set = set()
    if not isinstance(endpoints, dict):
        endpoints = {}
    for ep, info in endpoints.items():
        keys = ADVISOR_ENDPOINT_MAP.get(ep)
        st = ADVISOR_STATUS.get(str((info or {}).get("status") if isinstance(info, dict) else None))
        if not keys or not st:
            continue           # unknown endpoint or status: not an assessment (handled below, fail closed)
        covered.update(keys)
        reason = (info or {}).get("reason") or ep.replace("_", " ")
        out.append({"status": st, "reason": f"advisor: {reason}", "endpoints": keys})
    # fail closed: graft / new-bone endpoints without a recognised assessment are "not assessed" (C2-PRD-12)
    missing = [k for k in ADVISOR_KEYS if k not in covered]
    if missing:
        out.append({"status": NOT_ASSESSED, "reason": NO_ASSESSMENT_REASON, "endpoints": missing})
    return out


def _qc_problem_names(qc: dict, statuses) -> list[str]:
    return [c.get("name", c.get("id", "?")) for c in qc.get("checks", []) if c.get("status") in statuses]


def roi_requires_review(result: dict) -> bool:
    roi = (result or {}).get("roi") or {}
    return bool((roi.get("diagnostics") or {}).get("requires_review"))


def measurement_support(result: dict, roi_accepted: bool = False, manual_roi_pending: bool = False) -> dict:
    """Return ``{"overall": status, "endpoints": {key: {"status", "reasons"}}, "reasons": [...]}``.

    ``overall`` is *supported* when every endpoint is supported, *not supported* when none is
    (or there is no analysis), otherwise *flagged* (some endpoints need caution or are not
    reportable; see the per-endpoint statuses).

    States are combined honestly: an endpoint is never *supported* while the scan's QC verdict is
    "review" or "unsuitable", or while an automatic ROI that requires review has not been accepted
    (``roi_accepted``: a reviewer signed "Accept ROI" for the ROI definition used by the result).

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
        failed = _qc_problem_names(qc, ("fail",))
        flag(all_keys, FLAGGED, "QC unsuitable: " + ", ".join(failed[:3]))
    elif verdict == "review":
        warned = _qc_problem_names(qc, ("warn", "fail"))
        flag(all_keys, FLAGGED, "QC verdict 'review'" + (": " + ", ".join(warned[:3]) if warned else ""))
    elif verdict != "suitable":       # QC missing or unknown verdict: never green (C2-PRD-12)
        flag(all_keys, FLAGGED, "QC not run" if verdict is None else f"QC verdict {verdict!r} not recognised")

    for p in result.get("plausibility") or []:
        if not p.get("ok", True):
            flag(all_keys, FLAGGED, f"plausibility: {p.get('check')}")

    if roi_requires_review(result):
        if roi_accepted:
            general.append("automatic ROI accepted by a reviewer")
        else:
            flag(all_keys, FLAGGED, "automatic ROI not yet accepted (review the ROI outline, then Accept ROI)")

    if manual_roi_pending:
        flag(all_keys, FLAGGED, "manual ROI not yet accepted by a second person (Accept ROI)")

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
    n_na = sum(s == NOT_ASSESSED for s in sts)
    reasons = general + ([f"{n_ns} of {len(sts)} endpoints not supported"] if n_ns and overall != NOT_SUPPORTED else []) \
        + ([f"{n_na} of {len(sts)} endpoints not assessed"] if n_na else []) \
        + sorted({r for e in eps.values() for r in e["reasons"]})
    return {"overall": overall, "endpoints": eps, "reasons": reasons}


def _norm_reason(r: str) -> str:
    r = (r or "").strip()
    return r[len("advisor:"):].strip() if r.lower().startswith("advisor:") else r


ENDPOINT_BY_KEY = {k: (label, unit, path, scale) for k, label, unit, path, scale in ENDPOINTS}


def endpoint_value(result: dict, support: dict, key: str) -> tuple:
    """(display value or None, status, reasons) for one endpoint.

    The single rule used by every view and export: an endpoint whose status is *not supported* or
    *not assessed* never yields a number, whatever the stored value; the reasons say why. Reasons are de-duplicated
    (advisor reasons appear once, with or without the "advisor:" prefix)."""
    _, _, path, scale = ENDPOINT_BY_KEY[key]
    e = (support or {}).get("endpoints", {}).get(key) or {"status": NOT_SUPPORTED, "reasons": []}
    v, why = reported_value(result, path)
    reasons: list[str] = []
    seen = set()
    for r in list(e["reasons"]) + ([why] if why else []):
        n = _norm_reason(r)
        if n and n not in seen:
            seen.add(n)
            reasons.append(r)
    if e["status"] == NOT_ASSESSED:
        return None, NOT_ASSESSED, reasons or [NO_ASSESSMENT_REASON]
    if e["status"] == NOT_SUPPORTED or not isinstance(v, (int, float)) or isinstance(v, bool):
        return None, NOT_SUPPORTED, reasons or ["not computed"]
    return float(v) * scale, e["status"], reasons


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
