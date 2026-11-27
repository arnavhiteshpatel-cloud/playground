"""Generate the synthetic three-class phantom dataset used by Experiments B, C, J, K, M.

Each case is saved as data/processed/synth/<split>/<case_id>.npz containing:
  image (float32, simulated micro-CT, mode A), labels (uint8 0..3), roi (bool),
  fractions (uint8, class fractions*255 for boundary/partial-volume analysis)
and a JSON sidecar with generator config, imaging config and ground-truth morphometry.

Splits (all specimens independent; split by specimen, never by patch):
  train   : beta_tcp, bcp, ha, calcium_sulfate; 3 models; stages 0.15–0.9
  val     : same distribution, new seeds
  test    : same distribution, new seeds (in-distribution test)
  ood_mat : bioglass_45s5 and xenograft_dbbm (held-out materials, Experiment J)
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "processed" / "synth"
MODELS = {"condyle": dict(shape=(72, 80, 80), defect_diameter_um=2000.0),
          "calvarial": dict(shape=(40, 96, 96), defect_diameter_um=2400.0),
          "segmental": dict(shape=(80, 72, 72), gap_length_um=1600.0)}


def case_specs():
    specs = []
    rng = np.random.default_rng(2026)
    splits = {"train": (48, ["beta_tcp", "bcp", "ha", "calcium_sulfate"], 1000),
              "val": (8, ["beta_tcp", "bcp", "ha", "calcium_sulfate"], 2000),
              "test": (16, ["beta_tcp", "bcp", "ha", "calcium_sulfate"], 3000),
              "ood_mat": (24, ["bioglass_45s5", "xenograft_dbbm"], 4000)}
    for split, (n, mats, seed0) in splits.items():
        for i in range(n):
            model = list(MODELS)[i % 3]
            mat = mats[(i // 3) % len(mats)]
            stage = float(rng.uniform(0.15, 0.9))
            img = dict(psf_sigma_um=float(rng.uniform(15, 35)), noise_sigma=float(rng.uniform(30, 110)),
                       gain=float(rng.uniform(0.85, 1.15)), shift=float(rng.uniform(-80, 80)))
            specs.append(dict(split=split, case_id=f"{split}_{i:03d}_{model}_{mat}", model=model, material=mat,
                              stage=stage, seed=seed0 + i, imaging=img))
    return specs


def make_case(spec):
    out = OUT / spec["split"]
    out.mkdir(parents=True, exist_ok=True)
    f = out / f"{spec['case_id']}.npz"
    if f.exists():
        return spec["case_id"], 0.0
    t = time.time()
    m = MODELS[spec["model"]]
    cfg = PhantomConfig(model=spec["model"], voxel_um=40.0, graft_material=spec["material"],
                        healing_stage=spec["stage"], seed=spec["seed"], **m)
    ph = generate_phantom(cfg)
    ic = ImagingConfig(seed=spec["seed"], **spec["imaging"])
    vol = render_fast(ph.mu, cfg.voxel_um, ic)
    fr = np.stack([ph.class_fractions[c] for c in range(4)])
    np.savez_compressed(f, image=vol.data.astype(np.float32), labels=ph.labels, roi=ph.roi_mask,
                        fractions=np.round(fr * 255).astype(np.uint8))
    meta = {"spec": spec, "phantom_config": cfg.to_dict(), "imaging_config": ic.to_dict(), "truth": ph.truth,
            "roi": ph.roi, "generator_meta": {k: v for k, v in ph.meta.items() if k != "tissue_highres"},
            "provenance": "synthetic", "voxel_um": cfg.voxel_um}
    (out / f"{spec['case_id']}.json").write_text(json.dumps(meta, indent=1, default=float))
    return spec["case_id"], time.time() - t


if __name__ == "__main__":
    specs = case_specs()
    workers = int(os.environ.get("WORKERS", "3"))
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        for cid, dt in ex.map(make_case, specs):
            print(f"{cid} {dt:.1f}s", flush=True)
    print(f"done {len(specs)} cases in {time.time()-t0:.0f}s")
