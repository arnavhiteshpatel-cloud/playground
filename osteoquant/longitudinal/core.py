"""Longitudinal analysis: registration of timepoints, change maps, day-0 graft propagation.

Registration (SimpleITK):
  * rigid (Euler3D) and affine, Mattes mutual information, multi-resolution, linear interpolation;
  * deformable (B-spline FFD) as an experimental option — biological deformation and true
    tissue change are confounded, so deformable results must not be interpreted as ground truth.

Day-0 propagation method (DESIGN, tested in Experiment L):
  At day 0 (immediately post-implantation) every mineralised voxel inside the defect is graft.
  After registering a later scan to day 0, residual graft := later mineral ∩ day-0 graft
  footprint; new bone := later mineral outside that footprint. Known failure: new bone formed
  *inside* the original graft footprint (creeping substitution, bone in micro-pores) is labelled
  graft; graft that swelled/moved is mislabelled. Registration error displaces the footprint.
"""
from __future__ import annotations

import numpy as np
import SimpleITK as sitk


def to_sitk(arr, spacing_um):
    img = sitk.GetImageFromArray(np.ascontiguousarray(arr).astype(np.float32))
    img.SetSpacing(tuple(float(s) / 1000.0 for s in spacing_um[::-1]))  # mm, (x,y,z)
    return img


def register(fixed, moving, spacing_um, mode="rigid", mask=None, iters=300, seed=0, learning_rate_mm=None,
             metric="correlation", auto_mask=True):
    """Register ``moving`` onto ``fixed`` (both (z,y,x) arrays). Returns (transform, metric)."""
    F, M = to_sitk(fixed, spacing_um), to_sitk(moving, spacing_um)
    if learning_rate_mm is None:
        learning_rate_mm = 0.05
    R = sitk.ImageRegistrationMethod()
    if metric == "mi":
        R.SetMetricAsMattesMutualInformation(48)     # cross-scanner / cross-protocol
    else:
        R.SetMetricAsCorrelation()                   # same scanner & protocol (longitudinal)
    if mask is None and auto_mask:
        # central fixed-image mask (avoids optimum drifting to low-overlap / zero-padded borders)
        mask = np.zeros(fixed.shape, bool)
        sl = tuple(slice(int(n * 0.15), int(n * 0.85)) for n in fixed.shape)
        mask[sl] = True
    R.SetMetricSamplingStrategy(R.RANDOM)
    R.SetMetricSamplingPercentage(0.3, seed)
    R.SetInterpolator(sitk.sitkLinear)
    if mask is not None:
        R.SetMetricFixedMask(sitk.Cast(to_sitk(mask.astype(np.uint8), spacing_um), sitk.sitkUInt8))
    if mode in ("rigid", "affine"):
        base = sitk.Euler3DTransform() if mode == "rigid" else sitk.AffineTransform(3)
        init = sitk.CenteredTransformInitializer(F, M, base, sitk.CenteredTransformInitializerFilter.GEOMETRY)
        R.SetOptimizerAsRegularStepGradientDescent(learning_rate_mm, 1e-5, iters, relaxationFactor=0.7)
        # Explicit scales (rotation rad : translation mm). SetOptimizerScalesFromPhysicalShift() was
        # found to diverge on sub-millimetre micro-CT fields of view (Experiment L debugging, TRE ~2.5 mm);
        # explicit scales gave TRE ~1.5 µm on the same data.
        n_rot = 3 if mode == "rigid" else 9
        R.SetOptimizerScales([1.0] * n_rot + [0.1] * 3)
        R.SetInitialTransform(init, inPlace=False)
        R.SetShrinkFactorsPerLevel([2, 1])
        R.SetSmoothingSigmasPerLevel([1, 0])
        # NOTE: SimpleITK interprets pyramid sigmas in PHYSICAL units by default (mm here); on
        # micro-CT volumes that blurs everything away (Experiment L debugging: TRE >1 mm).
        R.SmoothingSigmasAreSpecifiedInPhysicalUnitsOff()
        tx = R.Execute(F, M)
    elif mode == "bspline":
        rig, _ = register(fixed, moving, spacing_um, "rigid", mask, iters, seed)
        mesh = [4] * 3
        bs = sitk.BSplineTransformInitializer(F, mesh)
        R.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5, numberOfIterations=60)
        R.SetMovingInitialTransform(rig)
        R.SetInitialTransform(bs, inPlace=True)
        R.SetShrinkFactorsPerLevel([2, 1])
        R.SetSmoothingSigmasPerLevel([1, 0])
        R.SmoothingSigmasAreSpecifiedInPhysicalUnitsOff()
        bs_out = R.Execute(F, M)
        tx = sitk.CompositeTransform([rig, bs_out])
    else:
        raise ValueError(mode)
    return tx, float(R.GetMetricValue())


def resample(moving, fixed_shape, spacing_um, tx, labels=False):
    ref = to_sitk(np.zeros(fixed_shape, np.float32), spacing_um)
    out = sitk.Resample(to_sitk(moving, spacing_um), ref, tx, sitk.sitkNearestNeighbor if labels else sitk.sitkLinear, 0.0)
    a = sitk.GetArrayFromImage(out)
    return a.astype(np.uint8) if labels else a


def apply_rigid(arr, spacing_um, rot_deg=(0, 0, 0), trans_um=(0, 0, 0), labels=False):
    """Apply a known rigid motion (for simulation). Rotation about volume centre; (x,y,z) order
    for SimpleITK parameters is handled internally from (z,y,x) inputs."""
    img = to_sitk(arr, spacing_um)
    t = sitk.Euler3DTransform()
    c = img.TransformContinuousIndexToPhysicalPoint([(n - 1) / 2 for n in img.GetSize()])
    t.SetCenter(c)
    rz, ry, rx = np.deg2rad(rot_deg)
    t.SetRotation(float(rx), float(ry), float(rz))
    tz, ty, tx_ = [v / 1000.0 for v in trans_um]
    t.SetTranslation((tx_, ty, tz))
    out = sitk.Resample(img, img, t, sitk.sitkNearestNeighbor if labels else sitk.sitkLinear, 0.0)
    a = sitk.GetArrayFromImage(out)
    return (a.astype(np.uint8) if labels else a), t


def target_registration_error(tx_true, tx_est, points_mm) -> dict:
    """TRE (µm). moved(p) = img(T_true(p)); registration finds T_est with moved(T_est(p)) ≈ fixed(p),
    so perfect recovery means T_true(T_est(p)) = p. TRE = |T_true(T_est(p)) − p|."""
    errs = []
    for p in points_mm:
        q = tx_true.TransformPoint(tx_est.TransformPoint(tuple(float(v) for v in p)))
        errs.append(np.linalg.norm(np.array(q) - np.array(p)) * 1000)
    e = np.array(errs)
    return {"mean_um": float(e.mean()), "max_um": float(e.max()), "p95_um": float(np.percentile(e, 95))}


def day0_propagation(later_mineral: np.ndarray, day0_graft: np.ndarray, roi: np.ndarray,
                     erode_vox: int = 0, host: np.ndarray | None = None) -> np.ndarray:
    from scipy import ndimage as ndi
    g = ndi.binary_erosion(day0_graft, iterations=erode_vox) if erode_vox else day0_graft
    lab = np.zeros(later_mineral.shape, np.uint8)
    lab[later_mineral & ~roi] = 3
    lab[later_mineral & roi] = 1
    lab[later_mineral & roi & g] = 2
    if host is not None:
        lab[host] = 3
    return lab


def change_map(lab_a: np.ndarray, lab_b: np.ndarray) -> dict:
    """Voxel transitions between two registered label maps (counts)."""
    out = {}
    for a in (0, 1, 2, 3):
        for b in (0, 1, 2, 3):
            n = int(((lab_a == a) & (lab_b == b)).sum())
            if n and a != b:
                out[f"{a}->{b}"] = n
    return out


def class_volume_change(labs, roi, spacing_um, times) -> list[dict]:
    vox = float(np.prod(spacing_um)) * 1e-9
    rows = []
    for lab, t in zip(labs, times):
        rows.append({"time": t, **{n: float(((lab == c) & roi).sum() * vox) for c, n in
                                   ((1, "new_bone_mm3"), (2, "graft_mm3"), (3, "host_mm3"))}})
    g0 = rows[0]["graft_mm3"]
    for r in rows:
        r["graft_remaining_frac"] = r["graft_mm3"] / g0 if g0 else float("nan")
    return rows


# ----------------------------------------------------------------------------- v2: QC and granule tracking
def registration_qc(fixed: np.ndarray, moved_back: np.ndarray, exclude: np.ndarray | None = None,
                    spacing_um=(1.0, 1.0, 1.0), tolerance_um: float | None = None, shell_vox: int = 12,
                    min_host_dice: float = 0.85, min_ncc: float = 0.6, n_blocks: int = 8,
                    aperture_ratio: float = 0.1) -> dict:
    """Registration quality from anatomy that should not change (host bone around the defect).

    Primary criterion (Gen-2 revision after review IMG-07): the *residual displacement* between the two
    registered scans, estimated by masked normalised cross-correlation (integer voxels) in ``n_blocks`` blocks of the
    peri-defect shell (8 octant blocks). Each block's shift is projected onto the directions its structure tensor can
    constrain (eigenvalue ≥ ``aperture_ratio`` × largest); shifts along featureless directions (e.g. a tube's axis)
    cannot be verified and are reported, not guessed. The maximum block displacement captures residual translation and the local effect of
    residual rotation, in µm, and is compared with ``tolerance_um`` (default: 2 voxels). Correlation over whole
    blocks is far less noise-sensitive than thresholded mask overlap. Host-mineral Dice and NCC are reported as
    secondary diagnostics (they were the Gen-2.0 criteria and failed perfect alignment at high noise).
    """
    from scipy import ndimage as ndi
    from skimage.registration import phase_cross_correlation
    from ..segment.classical import threshold_otsu
    sp = np.asarray(spacing_um, float)
    if tolerance_um is None:
        tolerance_um = float(2 * sp.mean())
    valid = (moved_back != 0)
    region = valid.copy()
    if exclude is not None:
        region &= ~ndi.binary_dilation(exclude, iterations=3)
        if shell_vox:
            region &= ndi.binary_dilation(exclude, iterations=3 + shell_vox)
    # secondary diagnostics
    a = threshold_otsu(fixed)[0] & region
    b = threshold_otsu(moved_back)[0] & region
    dice = 2 * int((a & b).sum()) / max(1, int(a.sum() + b.sum()))
    hr = ndi.binary_dilation(a | b, iterations=2) & region
    x, y = fixed[hr].astype(np.float64), moved_back[hr].astype(np.float64)
    ncc = float(np.corrcoef(x, y)[0, 1]) if x.size > 10 else float("nan")
    # primary: block-wise residual displacement, projected onto directions the block can constrain (aperture problem:
    # a diaphyseal tube is nearly translation-invariant along its axis — cycle-2 review C2-SCI-04)
    shifts, blocks = [], []
    cover = np.zeros((3, 3))          # sum of projectors onto the directions each block can verify
    if region.any():
        zz, yy, xx = np.nonzero(region)
        lo = np.array([zz.min(), yy.min(), xx.min()])
        hi = np.array([zz.max(), yy.max(), xx.max()]) + 1
        mid = (lo + hi) // 2
        for oz in (0, 1):
            for oy in (0, 1):
                for ox in (0, 1):                        # octants around the defect (covers the circumference)
                    l2 = np.array([lo[0] if oz == 0 else mid[0], lo[1] if oy == 0 else mid[1], lo[2] if ox == 0 else mid[2]])
                    h2 = np.array([mid[0] if oz == 0 else hi[0], mid[1] if oy == 0 else hi[1], mid[2] if ox == 0 else hi[2]])
                    if np.any(h2 - l2 < 8):
                        continue
                    sl = tuple(slice(int(a_), int(b_)) for a_, b_ in zip(l2, h2))
                    m = region[sl]
                    if m.mean() < 0.05:
                        continue
                    f = fixed[sl].astype(np.float32)
                    g = moved_back[sl].astype(np.float32)
                    if f[m].std() == 0 or g[m].std() == 0:
                        continue
                    sh = np.asarray(phase_cross_correlation(f, g, reference_mask=m, moving_mask=m)[0], float)
                    # structure tensor of the (smoothed) fixed block inside the mask: directions with little gradient
                    # energy cannot be verified, so the shift component along them is dropped and reported
                    fs = ndi.gaussian_filter(f, 1.0)
                    grads = [ndi.sobel(fs, axis=k)[m] for k in range(3)]
                    J = np.array([[float(np.mean(gi * gj)) for gj in grads] for gi in grads])
                    w, V = np.linalg.eigh(J)
                    ok_dir = w >= aperture_ratio * max(float(w.max()), 1e-12)
                    proj = V[:, ok_dir] @ (V[:, ok_dir].T @ (sh * sp)) if ok_dir.any() else np.zeros(3)
                    cover += V[:, ok_dir] @ V[:, ok_dir].T
                    # the eigen-projection reintroduces floating-point noise (an exact 2-voxel shift came out as
                    # 80.00000000000001 µm and failed an 80 µm tolerance): round to 1 nm before comparing
                    mag = round(float(np.linalg.norm(proj)), 3)
                    shifts.append(mag)
                    blocks.append({"shift_um_raw": float(np.linalg.norm(sh * sp)), "shift_um_constrained": mag,
                                   "n_unconstrained_directions": int((~ok_dir).sum())})
    max_shift = float(max(shifts)) if shifts else float("nan")
    unverifiable = bool(blocks) and all(b_["n_unconstrained_directions"] > 0 for b_ in blocks)
    # fail closed (cycle-3 review C3-SCI-04): if no block constrains some direction (e.g. the axis of a diaphyseal
    # tube), a shift along it cannot be measured, so the registration is NOT verified — it must not pass
    w_c, V_c = np.linalg.eigh(cover)
    blind = bool(blocks) and float(w_c.min()) < 0.5
    blind_dir = [float(x) for x in V_c[:, int(np.argmin(w_c))]] if blind else None
    ok = bool(shifts) and max_shift <= round(float(tolerance_um), 3) and not blind
    return {"residual_shift_um_max": max_shift, "residual_shift_um_blocks": shifts, "blocks": blocks,
            "tolerance_um": tolerance_um, "host_dice": float(dice), "host_ncc": ncc, "pass": ok,
            "partially_unverifiable": unverifiable, "unverifiable_direction": blind_dir,
            "reason": ("alignment along direction (z, y, x) ≈ " + ", ".join(f"{x:.2f}" for x in blind_dir)
                       + " cannot be verified (no structure constrains it)") if blind else
                      ("ok" if ok else "residual displacement exceeds tolerance"),
            "policy": {"criterion": "max block residual displacement along constrained directions ≤ tolerance",
                       "tolerance_um": tolerance_um, "aperture_ratio": aperture_ratio,
                       "secondary_min_host_dice": min_host_dice, "secondary_min_ncc": min_ncc}}


def track_granules(day0_img: np.ndarray, later_img: np.ndarray, day0_graft: np.ndarray, spacing_um,
                   search_um: float = 400.0, min_vox: int = 8, margin: int = 1, min_score: float = 0.5,
                   min_gain: float = 0.05, min_peak_margin: float = 0.05, distance_penalty: float = 0.10) -> dict:
    """Per-granule template matching of day-0 graft pieces in the registered later image.

    Each connected component of the day-0 graft mask (touching granules move as one) is matched by
    normalised cross-correlation within ±search_um, with a mild distance prior. Each component is classified:
    *stationary* (the zero-shift match is good and moving does not improve it by ``min_gain``), *moved* (a
    distinct peak — better than any candidate outside its neighbourhood by ``min_peak_margin`` — that improves on
    zero shift), or *ambiguous* (kept in place and counted as untracked: fragmented, heavily resorbed, overgrown,
    or too small/noisy to localise). Revised after Experiment L3, where unconstrained matching produced spurious
    ~700 µm shifts on strut-like granules in noisy scans.
    """
    from scipy import ndimage as ndi
    from skimage.feature import match_template
    lab, n = ndi.label(day0_graft)
    objs = ndi.find_objects(lab)
    sv = int(np.ceil(search_um / float(np.mean(spacing_um))))
    foot = np.zeros(day0_graft.shape, bool)
    recs = []
    for i, sl in enumerate(objs, start=1):
        if sl is None:
            continue
        comp = lab[sl] == i
        size = int(comp.sum())
        if size < min_vox:
            foot[sl] |= comp
            recs.append({"id": i, "voxels": size, "tracked": False, "reason": "too small"})
            continue
        t_sl = tuple(slice(max(0, a.start - margin), min(N, a.stop + margin)) for a, N in zip(sl, day0_img.shape))
        tmpl = day0_img[t_sl].astype(np.float32)
        w_sl = tuple(slice(max(0, a.start - sv), min(N, a.stop + sv)) for a, N in zip(t_sl, day0_img.shape))
        win = later_img[w_sl].astype(np.float32)
        if any(w < t for w, t in zip(win.shape, tmpl.shape)) or tmpl.std() == 0:
            foot[sl] |= comp
            recs.append({"id": i, "voxels": size, "tracked": False, "reason": "window"})
            continue
        cc = match_template(win, tmpl)
        # zero-shift position of the template inside the window
        zero = tuple(t.start - w.start for t, w in zip(t_sl, w_sl))
        score0 = float(cc[zero]) if all(0 <= z < n for z, n in zip(zero, cc.shape)) else -1.0
        # distance prior: prefer small motions (Experiment L3: unpenalised search found spurious matches)
        grids = np.meshgrid(*[np.arange(n) - z for n, z in zip(cc.shape, zero)], indexing="ij")
        dist_um = np.sqrt(sum((g * sp) ** 2 for g, sp in zip(grids, spacing_um)))
        pen = cc - distance_penalty * dist_um / max(search_um, 1e-6)
        best = np.unravel_index(int(np.argmax(pen)), pen.shape)
        score = float(cc[best])
        shift = np.array([w.start + b - t.start for w, b, t in zip(w_sl, best, t_sl)])
        # peak distinctiveness: best must beat every candidate outside its ±2-voxel neighbourhood by a margin
        excl = np.ones(cc.shape, bool)
        excl[tuple(slice(max(0, b - 2), b + 3) for b in best)] = False
        second = float(cc[excl].max()) if excl.any() else -1.0
        if score0 >= min_score and score - score0 < min_gain:
            status, shift, score = "stationary", np.zeros(3, int), score0
        elif score >= min_score and score - second >= min_peak_margin and score - score0 >= min_gain:
            status = "moved"
        else:
            status = "ambiguous"
            shift = np.zeros(3, int)
        ok = status in ("stationary", "moved")
        full = np.zeros(day0_graft.shape, bool)
        full[sl] = comp
        foot |= ndi.shift(full, shift, order=0, mode="constant", cval=False) if shift.any() else full
        recs.append({"id": i, "voxels": size, "tracked": bool(ok), "status": status, "score": score,
                     "score_zero_shift": score0, "second_peak": second,
                     "shift_um": [float(s * sp) for s, sp in zip(shift, spacing_um)],
                     "shift_mag_um": float(np.linalg.norm(shift * np.asarray(spacing_um, float)))})
    tracked = [r for r in recs if r.get("tracked")]
    vox_total = sum(r["voxels"] for r in recs) or 1
    untracked_frac = sum(r["voxels"] for r in recs if not r.get("tracked")) / vox_total
    mags = [r["shift_mag_um"] for r in tracked]
    return {"footprint": foot, "components": recs,
            "summary": {"n_components": len(recs), "n_tracked": len(tracked),
                        "n_moved": sum(1 for r in recs if r.get("status") == "moved"),
                        "n_ambiguous": sum(1 for r in recs if r.get("status") == "ambiguous"),
                        "untracked_volume_fraction": float(untracked_frac),
                        "median_shift_um": float(np.median(mags)) if mags else 0.0,
                        "p90_shift_um": float(np.percentile(mags, 90)) if mags else 0.0}}


def propagate_roi(reference_img: np.ndarray, reference_roi: np.ndarray, current_img: np.ndarray, spacing_um,
                  exclude_margin_vox: int = 3) -> dict:
    """Carry a defect ROI from an earlier (unbridged) timepoint to a later scan of the same animal.

    Segmental-gap detection fails once regenerate bridges the gap (Experiment F); the gap is still known
    from an early timepoint. The current scan is the fixed image; the reference is registered onto it
    (host anatomy only, ROI excluded) and the ROI mask is resampled with nearest-neighbour interpolation.
    Returns the propagated mask plus registration QC (``registration_qc``); callers must treat a failed
    QC as "manual ROI required".
    """
    from scipy import ndimage as ndi
    # Two passes (review IMG-13): the fixed-frame (current) ROI is unknown, so pass 1 uses the default central
    # mask; pass 2 re-registers with the pass-1 ROI (dilated) EXCLUDED, so healing inside the defect does not
    # drive the rigid fit.
    tx, metric = register(current_img, reference_img, spacing_um, "rigid", mask=None)
    roi1 = resample(reference_roi.astype(np.uint8), current_img.shape, spacing_um, tx, labels=True) > 0
    host_mask = ~ndi.binary_dilation(roi1, iterations=exclude_margin_vox)
    tx, metric = register(current_img, reference_img, spacing_um, "rigid", mask=host_mask)
    roi = resample(reference_roi.astype(np.uint8), current_img.shape, spacing_um, tx, labels=True) > 0
    moved_ref = resample(reference_img, current_img.shape, spacing_um, tx)
    excl = ndi.binary_dilation(roi, iterations=exclude_margin_vox)
    qc = registration_qc(current_img, moved_ref, exclude=excl, spacing_um=spacing_um)
    return {"roi": roi, "qc": qc, "metric": metric, "transform": tx}
