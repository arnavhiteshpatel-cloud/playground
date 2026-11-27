"""Synthetic demonstration data (computational phantoms with known ground truth) for the
self-test and documentation screenshots. Data produced here is labelled synthetic."""
from __future__ import annotations

from pathlib import Path

import numpy as np

DEMO_PASSWORD = "Demo-Password-2026"
REVIEWER_PASSWORD = "Review-Password-2026"


def write_phantom(path, seed=3, shape=(40, 56, 56), voxel_um=40.0, diameter_um=1400.0, stage=0.5,
                  material="beta_tcp", fmt="nifti") -> Path:
    from ..io import write_nifti
    from ..phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast
    ph = generate_phantom(PhantomConfig(model="condyle", shape=shape, voxel_um=voxel_um, supersample=1,
                                        defect_diameter_um=diameter_um, healing_stage=stage, graft_material=material,
                                        seed=seed))
    v = render_fast(ph.mu, voxel_um, ImagingConfig(psf_sigma_um=20, noise_sigma=40, seed=seed))
    path = Path(path)
    if fmt == "npy":
        np.save(path, v.data)
    else:
        write_nifti(v, path)
    return path


def build_demo_project(folder, n_animals=4, shape=(48, 72, 72), analyze=True, ctx=None):
    """Project with one blinded-capable study, two groups, ``n_animals`` phantom scans, analysed."""
    from . import services as S
    from .import_wizard import ImportModel
    from .project import Project
    folder = Path(folder)
    src = folder.parent / (folder.name + "_sources")
    src.mkdir(parents=True, exist_ok=True)
    p = Project.create(folder, "Synthetic condyle study (demo)", "analyst", DEMO_PASSWORD, "A. Analyst")
    oid = p.user["org_id"]
    p.store.create_user(oid, "reviewer", REVIEWER_PASSWORD, "reviewer", "R. Reviewer", actor=p.user)
    sid = p.create_study("Condyle defect, beta-TCP (synthetic phantoms)", "rabbit", "condyle", "beta-TCP",
                         data_class="synthetic")
    g1 = p.store.add_group(p.user, sid, "Control (beta-TCP)")
    g2 = p.store.add_group(p.user, sid, "Treatment (beta-TCP + additive)")
    m = ImportModel(p, sid)
    for i in range(n_animals):
        stage = 0.35 + 0.15 * (i % 3)
        f = write_phantom(src / f"R{i + 1:02d}_week4.nii.gz", seed=10 + i, shape=shape, stage=stage,
                          diameter_um=1600.0)
        c = m.add_path(f)[0]
        c.animal_id = f"R{i + 1:02d}"
        c.group_id = g1 if i % 2 == 0 else g2
        c.timepoint, c.days = "Week 4", 28
    raw = write_phantom(src / "R99_export.npy", seed=99, shape=shape, fmt="npy")
    c = m.add_path(raw)[0]
    c.animal_id, c.timepoint, c.days = "R99", "Week 4", 28
    c.spacing, c.confirmed = [40.0, 40.0, 40.0], True
    (src / "corrupt_scan.nii.gz").write_bytes(b"not a NIfTI file")
    m.add_path(src / "corrupt_scan.nii.gz")
    outcomes = m.run(ctx)
    if analyze:
        for o in outcomes:
            if o.scan_id:
                S.analyze_scan(p, o.scan_id, {"defect_model": "condyle", "nominal_diameter_um": 1600,
                                              "material": "beta_tcp"}, ctx)
    return p, sid, outcomes
