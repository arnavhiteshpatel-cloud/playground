"""Seed a local demo database with clearly labelled demonstration studies.

  python scripts/demo_seed.py [--db runtime/demo.db]

Creates organisation "OsteoQuant Demo Lab" with users (password printed once):
  demo_admin (admin), demo_analyst (analyst), demo_reviewer (reviewer)
Study 1 "SYNTHETIC phantom study" — 6 phantoms (beta-TCP vs HA groups), data_class=synthetic.
Study 2 "PUBLIC ovine distraction callus (Zenodo 10.5281/zenodo.17255310)" — 2 real scans,
        decimated ×4 for the demo, data_class=public (only if the files were downloaded).
Nothing here is customer data.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from osteoquant.study.db import Store  # noqa: E402
from osteoquant.study.jobs import JobRunner  # noqa: E402
from osteoquant.api.app import HANDLERS, _store_path  # noqa: E402
from osteoquant.io import write_zarr, read_volume  # noqa: E402
from osteoquant.phantom import PhantomConfig, generate_phantom, render_fast, ImagingConfig  # noqa: E402

import os
import secrets
# Demo-only accounts. A random password is generated unless OQ_DEMO_PASSWORD is set (review S-18).
DEMO_PW = os.environ.get("OQ_DEMO_PASSWORD") or ("Demo-" + secrets.token_urlsafe(9) + "9a")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "runtime" / "demo.db"))
    ap.add_argument("--seg", default="multiotsu")
    a = ap.parse_args()
    Path(a.db).parent.mkdir(parents=True, exist_ok=True)
    st = Store(a.db)
    if st.q1("SELECT id FROM orgs WHERE name='OsteoQuant Demo Lab'"):
        print("already seeded"); return
    org = st.create_org("OsteoQuant Demo Lab")
    for u, r in [("demo_admin", "admin"), ("demo_analyst", "analyst"), ("demo_reviewer", "reviewer")]:
        st.create_user(org, u, DEMO_PW, r, full_name=u.replace("_", " ").title())
    admin = st.user_for_token(st.login("demo_admin", DEMO_PW))
    runner = JobRunner(st, HANDLERS)
    pid = st.create_project(admin, "OsteoQuant demonstration")
    # ---------------- synthetic study
    sid = st.create_study(admin, pid, "SYNTHETIC phantom study — beta-TCP vs HA (rabbit-condyle-like)", "synthetic",
                          "condyle", "beta-TCP; HA", blinded=False, data_class="synthetic")
    g = {m: st.add_group(admin, sid, m) for m in ("beta-TCP", "HA")}
    tp = st.add_timepoint(admin, sid, "stage 0.6 (synthetic)", None)
    for i in range(6):
        mat = "beta_tcp" if i % 2 == 0 else "ha"
        spec = st.add_specimen(admin, sid, f"PH{i+1:02d}", g["beta-TCP" if mat == "beta_tcp" else "HA"])
        ph = generate_phantom(PhantomConfig(model="condyle", shape=(64, 80, 80), voxel_um=40, defect_diameter_um=2000,
                                            graft_material=mat, healing_stage=0.6, seed=9000 + i))
        vol = render_fast(ph.mu, 40, ImagingConfig(psf_sigma_um=25, noise_sigma=60, seed=i))
        scan = st.register_scan(admin, sid, spec, tp, "", f"phantom_PH{i+1:02d}.nii.gz", "synthetic", f"synthetic-{9000+i}",
                                vol.content_hash(), list(vol.shape), list(vol.spacing), {"truth": ph.truth,
                                "ingest": {"metadata_found": {"spacing_um": list(vol.spacing)}}})
        p = _store_path(st, org, scan); write_zarr(vol, p)
        st.exec("UPDATE scans SET store_path=? WHERE id=?", (str(p), scan))
        runner.wait(runner.submit(admin, "qc", {"scan_id": scan}), 300)
        j = runner.submit(admin, "analyze", {"scan_id": scan, "config": {"defect_model": "condyle", "nominal_diameter_um": 2000,
                                                                         "segmentation": a.seg}})
        print("phantom", i, runner.wait(j, 900))
    # ---------------- public real data
    raw = ROOT / "data" / "raw" / "zenodo_17255310"
    files = [f for f in ("18DAYS_recon.txm", "161DAYS_recon.txm") if (raw / f).exists()]
    if files:
        sid2 = st.create_study(admin, pid, "PUBLIC ovine metatarsal distraction callus (Zenodo 17255310, CC-BY-4.0)",
                               "sheep", "segmental", "none (distraction osteogenesis)", data_class="public")
        gg = st.add_group(admin, sid2, "distraction")
        for f in files:
            days = int(f.split("DAYS")[0])
            t = st.add_timepoint(admin, sid2, f"day {days}", days)
            spec = st.add_specimen(admin, sid2, f"OV-{days}d", gg)
            vol, rep = read_volume(raw / f, step=4, do_hash=False)
            scan = st.register_scan(admin, sid2, spec, t, "", f + " (decimated x4)", "txm", f"zenodo17255310:{f}",
                                    vol.content_hash(), list(vol.shape), list(vol.spacing), {"ingest": rep.to_dict()})
            p = _store_path(st, org, scan); write_zarr(vol, p)
            st.exec("UPDATE scans SET store_path=? WHERE id=?", (str(p), scan))
            runner.wait(runner.submit(admin, "qc", {"scan_id": scan}), 600)
            j = runner.submit(admin, "analyze", {"scan_id": scan, "config": {"defect_model": "segmental", "graft_brighter": True,
                                                                             "thickness_metrics": False}})
            print("ovine", f, runner.wait(j, 1800))
    print(f"Seeded {a.db}. Users demo_admin / demo_analyst / demo_reviewer, password: {DEMO_PW}")


if __name__ == "__main__":
    main()
