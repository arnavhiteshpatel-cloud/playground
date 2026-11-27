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
