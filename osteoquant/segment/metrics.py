"""Segmentation agreement metrics (voxel-level; NOT biological replicates).

All distance metrics are in micrometres and respect anisotropic spacing.
Voxels labelled 255 ("uncertain/abstain") in the prediction are excluded from overlap metrics
when ``ignore_abstain=True`` and the abstention rate is reported separately (coverage).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

ABSTAIN = 255


def confusion(pred: np.ndarray, truth: np.ndarray, classes, mask=None) -> np.ndarray:
    p, t = pred, truth
    if mask is not None:
        p, t = p[mask], t[mask]
    p = p.ravel()
    t = t.ravel()
    k = len(classes)
    idx = {c: i for i, c in enumerate(classes)}
    lut_p = np.full(256, -1, np.int64)
    lut_t = np.full(256, -1, np.int64)
    for c, i in idx.items():
        lut_p[c] = i
        lut_t[c] = i
    pi, ti = lut_p[p], lut_t[t]
    ok = (pi >= 0) & (ti >= 0)
    return np.bincount(ti[ok] * k + pi[ok], minlength=k * k).reshape(k, k)  # rows truth, cols pred


def _surface(m: np.ndarray) -> np.ndarray:
    return m & ~ndi.binary_erosion(m, border_value=0)


def surface_distances(a: np.ndarray, b: np.ndarray, spacing) -> tuple[np.ndarray, np.ndarray]:
    """Distances (µm) from surface of a to surface of b and vice versa."""
    sa, sb = _surface(a), _surface(b)
    if not sa.any() or not sb.any():
        return np.array([np.inf]), np.array([np.inf])
    db = ndi.distance_transform_edt(~sb, sampling=spacing)
    da = ndi.distance_transform_edt(~sa, sampling=spacing)
    return db[sa], da[sb]


def binary_metrics(pred: np.ndarray, truth: np.ndarray, spacing=(1, 1, 1), distances=True) -> dict:
    p, t = pred.astype(bool), truth.astype(bool)
    tp = int(np.sum(p & t))
    fp = int(np.sum(p & ~t))
    fn = int(np.sum(~p & t))
    out = {
        "dice": 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else float("nan"),
        "iou": tp / (tp + fp + fn) if (tp + fp + fn) else float("nan"),
        "precision": tp / (tp + fp) if (tp + fp) else float("nan"),
        "recall": tp / (tp + fn) if (tp + fn) else float("nan"),
        "vol_pred_vox": int(p.sum()), "vol_true_vox": int(t.sum()),
    }
    out["volume_error_rel"] = (out["vol_pred_vox"] - out["vol_true_vox"]) / out["vol_true_vox"] \
        if out["vol_true_vox"] else float("nan")
    if distances:
        d1, d2 = surface_distances(p, t, spacing)
        if np.isinf(d1).any() or np.isinf(d2).any():
            out["hd95_um"] = float("nan")
            out["assd_um"] = float("nan")
        else:
            alld = np.concatenate([d1, d2])
            out["hd95_um"] = float(max(np.percentile(d1, 95), np.percentile(d2, 95)))
            out["assd_um"] = float(alld.mean())
    return out


def multiclass_metrics(pred: np.ndarray, truth: np.ndarray, classes=(1, 2, 3), spacing=(1, 1, 1),
                       mask=None, distances=True, ignore_abstain=True, names=None) -> dict:
    """Per-class metrics (+ macro mean) inside optional mask (e.g. defect ROI)."""
    names = names or {1: "new_bone", 2: "graft", 3: "host_bone"}
    m = np.ones(truth.shape, bool) if mask is None else mask.astype(bool)
    abst = (pred == ABSTAIN) & m
    coverage = 1.0 - abst.sum() / max(1, m.sum())
    eval_m = m & ~abst if ignore_abstain else m
    res = {"coverage": float(coverage), "per_class": {}}
    for c in classes:
        pm = (pred == c) & eval_m
        tm = (truth == c) & eval_m
        bm = binary_metrics(pm, tm, spacing, distances=distances)
        res["per_class"][names.get(c, str(c))] = bm
    ds = [v["dice"] for v in res["per_class"].values() if np.isfinite(v["dice"])]
    res["mean_dice"] = float(np.mean(ds)) if ds else float("nan")
    cm = confusion(pred, truth, (0,) + tuple(classes), eval_m)
    res["confusion"] = cm.tolist()
    res["accuracy"] = float(np.trace(cm) / cm.sum()) if cm.sum() else float("nan")
    return res


def expected_calibration_error(prob: np.ndarray, truth: np.ndarray, n_bins=15, mask=None) -> dict:
    """Top-label ECE. prob: (C, ...) softmax; truth: integer labels 0..C-1."""
    conf = prob.max(0)
    pred = prob.argmax(0)
    if mask is not None:
        conf, pred, truth = conf[mask], pred[mask], truth[mask]
    conf, correct = conf.ravel(), (pred == truth).ravel()
    bins = np.linspace(0, 1, n_bins + 1)
    ece, rows = 0.0, []
    for i in range(n_bins):
        sel = (conf > bins[i]) & (conf <= bins[i + 1])
        if sel.any():
            acc, c = correct[sel].mean(), conf[sel].mean()
            ece += sel.mean() * abs(acc - c)
            rows.append({"bin": float(bins[i + 1]), "conf": float(c), "acc": float(acc), "n": int(sel.sum())})
    return {"ece": float(ece), "bins": rows}
