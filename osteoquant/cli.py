"""OsteoQuant command-line interface.

  osteoquant init-admin --org "My Lab" --user admin            create first org + admin (prompts for password)
  osteoquant serve [--host 127.0.0.1 --port 8765]              start web app (local only by default)
  osteoquant ingest PATH [--spacing 10] [--out scan.zarr]       import a volume, print provenance
  osteoquant qc PATH [--spacing 10]                             run QC and print checks
  osteoquant analyze PATH --model condyle [--seg multiotsu]     run DefectFill pipeline, write JSON
  osteoquant phantom --model condyle --material beta_tcp --out case.nii.gz
  osteoquant audit-verify                                        verify the audit hash chain
  osteoquant backup DEST                                         consistent DB backup with SHA-256
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

DB = os.environ.get("OQ_DB", str(Path.cwd() / "runtime" / "osteoquant.db"))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="osteoquant", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("init-admin"); a.add_argument("--org", required=True); a.add_argument("--user", required=True)
    a.add_argument("--password", default=None)
    s = sub.add_parser("serve"); s.add_argument("--host", default="127.0.0.1"); s.add_argument("--port", type=int, default=8765)
    for name in ("ingest", "qc", "analyze"):
        p = sub.add_parser(name); p.add_argument("path"); p.add_argument("--spacing", type=float, default=None)
        p.add_argument("--step", type=int, default=1)
        if name == "ingest":
            p.add_argument("--out", default=None)
        if name == "analyze":
            p.add_argument("--model", default="condyle"); p.add_argument("--seg", default="multiotsu")
            p.add_argument("--diameter", type=float, default=None); p.add_argument("--json", default="analysis.json")
    ph = sub.add_parser("phantom"); ph.add_argument("--model", default="condyle"); ph.add_argument("--material", default="beta_tcp")
    ph.add_argument("--stage", type=float, default=0.5); ph.add_argument("--seed", type=int, default=0); ph.add_argument("--out", required=True)
    sub.add_parser("audit-verify")
    b = sub.add_parser("backup"); b.add_argument("dest")
    args = ap.parse_args(argv)

    if args.cmd == "init-admin":
        from .study.db import Store
        st = Store(DB)
        pw = args.password or getpass.getpass("Admin password (≥10 chars, upper-case, digit): ")
        oid = st.create_org(args.org)
        uid = st.create_user(oid, args.user, pw, "admin", args.user)
        print(json.dumps({"org_id": oid, "user_id": uid, "db": DB}))
    elif args.cmd == "serve":
        import uvicorn
        from .api.app import create_app
        if args.host not in ("127.0.0.1", "localhost"):
            print("WARNING: binding to a non-local interface exposes data on the network.", file=sys.stderr)
        uvicorn.run(create_app(DB), host=args.host, port=args.port)
    elif args.cmd in ("ingest", "qc", "analyze"):
        from .io import read_volume, write_zarr
        vol, rep = read_volume(args.path, spacing_um=args.spacing, step=args.step)
        if args.cmd == "ingest":
            print(json.dumps({"summary": vol.summary(), "report": rep.to_dict()}, indent=1, default=str))
            if args.out:
                print("content_sha256", write_zarr(vol, args.out))
        elif args.cmd == "qc":
            from .qc import run_qc
            q = run_qc(vol)
            for c in q["checks"]:
                print(f"{c['id']:7s} {c['status']:5s} {c['basis']:13s} {c['name']}: {c['value']} {c['message']}")
            print("verdict:", q["verdict"])
        else:
            from .pipeline import analyze, public
            r = analyze(vol, {"defect_model": args.model, "segmentation": args.seg, "nominal_diameter_um": args.diameter})
            Path(args.json).write_text(json.dumps(public(r), indent=1, default=str))
            print(json.dumps({"status": r["status"], "class_volumes": r.get("metrics", {}).get("class_volumes"),
                              "timings": r["timings"]}, indent=1, default=str))
    elif args.cmd == "phantom":
        from .phantom import PhantomConfig, generate_phantom, render_fast, ImagingConfig
        from .io import write_nifti
        from .volume import Volume
        ph = generate_phantom(PhantomConfig(model=args.model, graft_material=args.material, healing_stage=args.stage, seed=args.seed))
        v = render_fast(ph.mu, ph.config.voxel_um, ImagingConfig(psf_sigma_um=25, noise_sigma=60, seed=args.seed))
        write_nifti(v, args.out)
        lab = args.out.replace(".nii", "_labels.nii")
        write_nifti(Volume(ph.labels, v.spacing), lab, labels=True)
        print(json.dumps({"image": args.out, "labels": lab, "truth": ph.truth}, indent=1))
    elif args.cmd == "audit-verify":
        from .study.db import Store
        print(json.dumps(Store(DB).audit.verify_chain()))
    elif args.cmd == "backup":
        from .study.db import Store
        print(json.dumps(Store(DB).backup(args.dest)))


if __name__ == "__main__":
    main()
