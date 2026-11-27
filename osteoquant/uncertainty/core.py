"""Uncertainty, abstention and failure detection.

* ``predictive_entropy``        — H(p̄) of the mean softmax (normalised to [0,1] by log C).
* ``mutual_information``        — epistemic part: H(p̄) − mean_m H(p_m) across ensemble/TTA members.
* ``abstain``                   — label 255 where confidence < τ (never force a class).
* ``risk_coverage``             — selective accuracy/Dice as abstention increases (AURC).
* ``temperature_scale``         — post-hoc calibration on a validation set (Guo et al. 2017).
* ``intensity_ood``             — Wasserstein-1 distance between a scan's normalised mineral
                                  intensity distribution and the training reference; flags
                                  unknown scanners/materials.
* ``plausibility_checks``       — anatomical/volume sanity rules (e.g. host bone inside defect,
                                  graft outside defect, class fractions outside expected ranges).
"""
from __future__ import annotations

import numpy as np

ABSTAIN = 255


def predictive_entropy(p: np.ndarray) -> np.ndarray:
    C = p.shape[0]
    return (-(p * np.log(np.clip(p, 1e-8, 1))).sum(0) / np.log(C)).astype(np.float32)


def mutual_information(members: list[np.ndarray]) -> np.ndarray:
    pm = np.mean(members, axis=0)
    C = pm.shape[0]
    h = -(pm * np.log(np.clip(pm, 1e-8, 1))).sum(0)
    eh = np.mean([-(m * np.log(np.clip(m, 1e-8, 1))).sum(0) for m in members], axis=0)
    return ((h - eh) / np.log(C)).astype(np.float32)


def abstain(p: np.ndarray, tau: float, mask: np.ndarray | None = None) -> np.ndarray:
    lab = p.argmax(0).astype(np.uint8)
    conf = p.max(0)
    a = conf < tau
    if mask is not None:
        a &= mask
    lab[a] = ABSTAIN
    return lab


def risk_coverage(p: np.ndarray, truth: np.ndarray, mask: np.ndarray, score: np.ndarray | None = None,
                  coverages=(1.0, 0.98, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6, 0.5), classes=(1, 2)) -> dict:
    """Selective accuracy and per-class Dice when the least-confident voxels (by ``score``,
    default 1−max p) are deferred to a human. Evaluated inside ``mask`` on mineral voxels."""
    pred = p.argmax(0)
    unc = (1 - p.max(0)) if score is None else score
    m = mask
    u, pr, t = unc[m], pred[m], truth[m]
    order = np.argsort(u)  # most confident first
    n = len(order)
    rows = []
    for c in coverages:
        k = int(round(c * n))
        sel = order[:k]
        acc = float(np.mean(pr[sel] == t[sel])) if k else float("nan")
        row = {"coverage": c, "accuracy": acc, "n_deferred": n - k}
        for cl in classes:
            ps, ts = pr[sel] == cl, t[sel] == cl
            den = ps.sum() + ts.sum()
            row[f"dice_{cl}"] = float(2 * (ps & ts).sum() / den) if den else float("nan")
        # "human-corrected" outcome: deferred voxels assumed corrected to truth by the reviewer
        full = pr.copy()
        full[order[k:]] = t[order[k:]]
        row["accuracy_after_review"] = float(np.mean(full == t))
        for cl in classes:
            ps, ts = full == cl, t == cl
            den = ps.sum() + ts.sum()
            row[f"dice_{cl}_after_review"] = float(2 * (ps & ts).sum() / den) if den else float("nan")
        rows.append(row)
    # AURC (area under risk-coverage curve)
    errs = (pr[order] != t[order]).astype(float)
    cum = np.cumsum(errs) / np.arange(1, n + 1)
    return {"rows": rows, "aurc": float(cum.mean()) if n else float("nan"), "n_voxels": int(n)}


def temperature_scale(logits_list, labels_list, mask_list=None, grid=np.linspace(0.5, 3.0, 26)) -> float:
    """Fit a single temperature T minimising NLL on validation voxels (sub-sampled)."""
    rng = np.random.default_rng(0)
    L, Y = [], []
    for i, (lg, y) in enumerate(zip(logits_list, labels_list)):
        m = np.ones(y.shape, bool) if mask_list is None else mask_list[i]
        idx = np.flatnonzero(m.ravel())
        idx = rng.choice(idx, min(200_000, idx.size), replace=False)
        L.append(lg.reshape(lg.shape[0], -1)[:, idx])
        Y.append(y.ravel()[idx])
    L, Y = np.concatenate(L, 1), np.concatenate(Y)
    best, bt = np.inf, 1.0
    for T in grid:
        z = L / T
        z = z - z.max(0)
        lp = z - np.log(np.exp(z).sum(0))
        nll = -lp[Y, np.arange(Y.size)].mean()
        if nll < best:
            best, bt = nll, float(T)
    return bt


def intensity_ood(img_norm: np.ndarray, mineral_mask: np.ndarray, reference_quantiles: np.ndarray) -> dict:
    """W1 distance between this scan's normalised mineral-intensity quantiles and the reference."""
    q = np.linspace(0.01, 0.99, len(reference_quantiles))
    v = img_norm[mineral_mask]
    if v.size < 100:
        return {"w1": float("nan"), "flag": True, "note": "too few mineral voxels"}
    qs = np.quantile(v, q)
    w1 = float(np.mean(np.abs(qs - reference_quantiles)))
    return {"w1": w1, "quantiles": qs.tolist()}


def plausibility_checks(labels: np.ndarray, roi: np.ndarray, expected: dict | None = None) -> list[dict]:
    exp = {"max_host_in_roi_frac": 0.02, "max_graft_outside_roi_frac": 0.05, "max_uncertain_frac": 0.25}
    exp.update(expected or {})
    out = []
    tv = max(1, roi.sum())
    host_in = float(((labels == 3) & roi).sum() / tv)
    out.append({"check": "host bone inside defect ROI", "value": host_in, "limit": exp["max_host_in_roi_frac"],
                "ok": host_in <= exp["max_host_in_roi_frac"]})
    g_all = max(1, (labels == 2).sum())
    g_out = float(((labels == 2) & ~roi).sum() / g_all)
    out.append({"check": "graft outside defect ROI (fraction of graft)", "value": g_out,
                "limit": exp["max_graft_outside_roi_frac"], "ok": g_out <= exp["max_graft_outside_roi_frac"]})
    unc = float(((labels == ABSTAIN) & roi).sum() / tv)
    out.append({"check": "uncertain fraction in ROI", "value": unc, "limit": exp["max_uncertain_frac"],
                "ok": unc <= exp["max_uncertain_frac"]})
    newf = float(((labels == 1) & roi).sum() / tv)
    out.append({"check": "new bone fraction in ROI within [0, 0.9]", "value": newf, "limit": 0.9, "ok": newf <= 0.9})
    return out
