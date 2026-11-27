"""Classical segmentation baselines.

Two families:
1. Mineralised-vs-background (binary) methods: global, Otsu, adaptive, GMM, k-means,
   region growing, watershed separation of particles.
2. Three-class (new bone / residual graft / host bone) methods built on a *spatial prior*:
   host bone := mineralised voxels outside the defect ROI; inside the ROI, mineralised voxels
   are split into new bone vs graft by intensity (multi-Otsu, GMM, k-means), by intensity +
   morphology (granule detection), or by a voxel Random Forest on multi-scale features
   (an ilastik/Trainable-Weka-style pixel classifier, implemented independently).

The "CTAn-style" baseline reproduces the *common workflow* (manual cylindrical ROI + global
threshold for mineral + a second, higher global threshold for graft); it is an independent
implementation of a generic procedure, not a copy of any proprietary software.

``graft_brighter`` encodes prior material knowledge: True for HA/TCP/BCP-type ceramics that are
denser than new bone; False for materials less attenuating than bone (e.g. Mg alloys, some
glasses at low energy). Classical intensity methods must be told this; it is a real
limitation (they cannot discover the ordering).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

BG, NEW, GRAFT, HOST = 0, 1, 2, 3


# ----------------------------------------------------------------------------- helpers
def _sample(x, mask=None, n=400_000, seed=0):
    v = x[mask] if mask is not None else x.ravel()
    if v.size > n:
        v = np.random.default_rng(seed).choice(v, n, replace=False)
    return v.astype(np.float64)


def compose_three_class(mineral: np.ndarray, graft_in_roi: np.ndarray, roi: np.ndarray) -> np.ndarray:
    lab = np.zeros(mineral.shape, np.uint8)
    lab[mineral & ~roi] = HOST
    lab[mineral & roi] = NEW
    lab[graft_in_roi & roi & mineral] = GRAFT
    return lab


# ----------------------------------------------------------------------------- binary
def threshold_global(x, t):
    return x > t


def threshold_otsu(x, mask=None):
    from skimage.filters import threshold_otsu as _o
    t = float(_o(_sample(x, mask)))
    return x > t, t


def threshold_adaptive(x, block_um=600.0, spacing=(1, 1, 1), offset=0.0):
    """Local-mean threshold: voxel > local mean (box of ``block_um``) + offset."""
    size = [max(3, int(round(block_um / s)) | 1) for s in spacing]
    loc = ndi.uniform_filter(x.astype(np.float32), size)
    return x > loc + offset


def gmm_threshold(x, mask=None, k=2, seed=0):
    from sklearn.mixture import GaussianMixture
    v = _sample(x, mask, 200_000, seed)[:, None]
    g = GaussianMixture(k, random_state=seed).fit(v)
    order = np.argsort(g.means_.ravel())
    return g, order


def kmeans_levels(x, mask=None, k=3, seed=0):
    from sklearn.cluster import KMeans
    v = _sample(x, mask, 200_000, seed)[:, None]
    km = KMeans(k, n_init=4, random_state=seed).fit(v)
    c = np.sort(km.cluster_centers_.ravel())
    return (c[:-1] + c[1:]) / 2  # thresholds between sorted centres


def region_grow(x, seeds: np.ndarray, lo: float, hi: float = np.inf) -> np.ndarray:
    """Connected voxels within [lo, hi] reachable from seed mask (26-connectivity)."""
    cand = (x >= lo) & (x <= hi)
    lab, _ = ndi.label(cand, structure=np.ones((3, 3, 3)))
    ids = np.unique(lab[seeds & cand])
    ids = ids[ids > 0]
    return np.isin(lab, ids)


def watershed_particles(mask: np.ndarray, spacing=(1, 1, 1), min_distance_um=150.0) -> np.ndarray:
    """Split touching particles via distance-transform watershed (instance labels)."""
    from skimage.segmentation import watershed
    from skimage.feature import peak_local_max
    d = ndi.distance_transform_edt(mask, sampling=spacing)
    md = max(1, int(min_distance_um / min(spacing)))
    pk = peak_local_max(d, min_distance=md, labels=mask.astype(int), exclude_border=False)
    markers = np.zeros(mask.shape, np.int32)
    markers[tuple(pk.T)] = np.arange(1, len(pk) + 1)
    return watershed(-d, markers, mask=mask)


def clean_binary(m, min_size_vox=8, close_iter=0):
    if close_iter:
        m = ndi.binary_closing(m, iterations=close_iter)
    lab, n = ndi.label(m)
    if n == 0:
        return m
    sizes = ndi.sum(m, lab, range(1, n + 1))
    keep = np.zeros(n + 1, bool)
    keep[1:] = sizes >= min_size_vox
    return keep[lab]


# ----------------------------------------------------------------------------- three-class
def seg_ctan_style(x, roi, t_mineral, t_graft, graft_brighter=True, despeckle=8):
    """Manual-ROI + two global thresholds (common CTAn/Scanco-style workflow)."""
    mineral = clean_binary(x > t_mineral, despeckle)
    g = (x > t_graft) if graft_brighter else ((x > t_mineral) & (x < t_graft))
    g = clean_binary(g, despeckle)
    return compose_three_class(mineral, g, roi)


def seg_multiotsu(x, roi, graft_brighter=True, smooth_sigma=0.0):
    """Multi-Otsu with 3 classes inside the ROI; mineral threshold from Otsu on whole image."""
    from skimage.filters import threshold_multiotsu
    xs = ndi.gaussian_filter(x.astype(np.float32), smooth_sigma) if smooth_sigma else x
    mineral, t_min = threshold_otsu(xs)
    v = _sample(xs, roi & mineral) if (roi & mineral).sum() > 100 else _sample(xs, roi)
    try:
        t1 = float(threshold_multiotsu(v, classes=2)[0])
    except Exception:
        t1 = float(np.median(v))
    g = xs > t1 if graft_brighter else (xs < t1)
    lab = compose_three_class(mineral, g, roi)
    return lab, {"t_mineral": float(t_min), "t_graft": t1}


def seg_gmm(x, roi, graft_brighter=True, seed=0):
    """3-component GMM in ROI (background, lower-, higher-attenuating mineral)."""
    g, order = gmm_threshold(x, roi, k=3, seed=seed)
    comp = g.predict(x[roi].reshape(-1, 1).astype(np.float64))
    rank = np.empty(3, int)
    rank[order] = np.arange(3)
    r = rank[comp]
    # mineral outside ROI: threshold between background mean and lower mineral mean
    mu = np.sort(g.means_.ravel())
    t_min = (mu[0] + mu[1]) / 2
    mineral = x > t_min
    lab = np.zeros(x.shape, np.uint8)
    lab[mineral & ~roi] = HOST
    sub = np.zeros(r.shape, np.uint8)
    hi_cls, lo_cls = (GRAFT, NEW) if graft_brighter else (NEW, GRAFT)
    sub[r == 1] = lo_cls
    sub[r == 2] = hi_cls
    lab[roi] = sub
    return lab, {"means": mu.tolist()}


def seg_kmeans(x, roi, graft_brighter=True, seed=0):
    t = kmeans_levels(x, roi, 3, seed)
    mineral = x > t[0]
    g = (x > t[1]) if graft_brighter else (x < t[1])
    return compose_three_class(mineral, g, roi), {"thresholds": t.tolist()}


def seg_morphology(x, roi, spacing, t_mineral, t_graft, graft_brighter=True,
                   granule_diam_um=(200, 1200), min_solidity=0.75):
    """Intensity + shape: graft candidates are compact, roughly convex objects in the
    granule size range; elongated/plate-like high-density objects are reassigned to new bone."""
    from skimage.measure import regionprops, label as sklabel
    mineral = clean_binary(x > t_mineral, 8)
    cand = (x > t_graft) if graft_brighter else ((x > t_mineral) & (x < t_graft))
    cand = ndi.binary_opening(cand & roi, iterations=1)
    lab_c = sklabel(cand)
    graft = np.zeros(x.shape, bool)
    vox = float(np.prod(spacing))
    vmin = 4 / 3 * np.pi * (granule_diam_um[0] / 2) ** 3 / vox * 0.3
    for rp in regionprops(lab_c):
        if rp.area < vmin:
            continue
        if rp.solidity < min_solidity:
            continue
        sl = rp.slice
        graft[sl][rp.image] = True
    graft = ndi.binary_dilation(graft, iterations=1) & cand
    return compose_three_class(mineral, graft, roi)


# ----------------------------------------------------------------------------- features + RF
def voxel_features(x: np.ndarray, spacing=(1, 1, 1), roi: np.ndarray | None = None,
                   scales_um=(0, 40, 80, 160), include_spatial=True) -> tuple[np.ndarray, list[str]]:
    """Multi-scale voxel features (float32, shape (N_features, *x.shape))."""
    from skimage.feature import hessian_matrix, hessian_matrix_eigvals
    x = x.astype(np.float32)
    feats, names = [], []
    vs = float(np.mean(spacing))
    for s_um in scales_um:
        s = s_um / vs
        g = ndi.gaussian_filter(x, s) if s > 0 else x
        feats.append(g)
        names.append(f"gauss_{s_um}")
        if s > 0:
            gm = ndi.gaussian_gradient_magnitude(x, s)
            feats.append(gm)
            names.append(f"gradmag_{s_um}")
            lg = ndi.gaussian_laplace(x, s)
            feats.append(lg)
            names.append(f"log_{s_um}")
            m2 = ndi.gaussian_filter(x * x, s)
            feats.append(np.sqrt(np.maximum(m2 - g * g, 0)))
            names.append(f"std_{s_um}")
    s = 80.0 / vs
    H = hessian_matrix(x, sigma=s, order="rc", use_gaussian_derivatives=False)
    ev = hessian_matrix_eigvals(H)
    for i in range(3):
        feats.append(ev[i].astype(np.float32))
        names.append(f"hess_ev{i}_80")
    # distance-to-bright-object features (granule interior depth)
    if include_spatial and roi is not None:
        d_in = ndi.distance_transform_edt(roi, sampling=spacing).astype(np.float32)
        feats.append(d_in)
        names.append("dist_to_roi_boundary_um")
    return np.stack(feats), names


class RFSegmenter:
    """Random-forest voxel classifier (sparse training on labelled voxels)."""

    def __init__(self, n_estimators=60, max_depth=18, seed=0, scales_um=(0, 40, 80, 160), feature_set="full"):
        from sklearn.ensemble import RandomForestClassifier
        self.clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, n_jobs=-1,
                                          random_state=seed, class_weight="balanced_subsample")
        self.scales_um = scales_um
        self.seed = seed
        self.feature_set = feature_set  # full | no_spatial | intensity_scales | raw
        self.feature_names = None

    def _feats(self, x, spacing, roi):
        if self.feature_set == "raw":
            self.feature_names = ["raw"]
            return x.astype(np.float32)[None]
        f, names = voxel_features(x, spacing, roi, self.scales_um, include_spatial=self.feature_set == "full")
        if self.feature_set == "intensity_scales":
            keep = [i for i, n in enumerate(names) if n.startswith("gauss_")]
            f, names = f[keep], [names[i] for i in keep]
        self.feature_names = names
        return f

    def fit(self, images, labels, spacings, rois, n_per_class=20000):
        rng = np.random.default_rng(self.seed)
        Xs, ys = [], []
        for x, y, sp, roi in zip(images, labels, spacings, rois):
            f = self._feats(x, sp, roi)
            for c in np.unique(y):
                idx = np.flatnonzero(y.ravel() == c)
                if idx.size == 0:
                    continue
                sel = rng.choice(idx, min(n_per_class, idx.size), replace=False)
                Xs.append(f.reshape(f.shape[0], -1)[:, sel].T)
                ys.append(np.full(sel.size, c))
        self.clf.fit(np.concatenate(Xs), np.concatenate(ys))
        return self

    def predict_proba(self, x, spacing, roi):
        f = self._feats(x, spacing, roi)
        F = f.reshape(f.shape[0], -1).T
        out = np.zeros((F.shape[0], len(self.clf.classes_)), np.float32)
        for i in range(0, F.shape[0], 500_000):
            out[i:i + 500_000] = self.clf.predict_proba(F[i:i + 500_000])
        return out.T.reshape((len(self.clf.classes_),) + x.shape), self.clf.classes_

    def predict(self, x, spacing, roi):
        p, cls = self.predict_proba(x, spacing, roi)
        return cls[p.argmax(0)].astype(np.uint8), p
