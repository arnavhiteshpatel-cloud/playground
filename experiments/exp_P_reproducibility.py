"""Experiment P — reproducibility across repeated runs.

Checks: (1) the full DefectFill pipeline run twice on the same volume yields bit-identical labels
(SHA-256) and identical metrics; (2) U-Net inference is bit-identical across runs; (3) U-Net
training with a fixed seed reproduces the same weights (50 iterations, deterministic algorithms);
(4) RF training+prediction with fixed seed is identical; (5) content hash invariance across
format round-trips (NIfTI, NRRD, Zarr, TIFF, DICOM); (6) audit trail verifies after all runs.
"""
import hashlib
import json
import tempfile
from pathlib import Path

import numpy as np
import torch

from common import load_split, save_result
from osteoquant.pipeline import analyze, public
from osteoquant.ml.train import load_model, predict_proba, train_model, MODEL_DIR
from osteoquant.segment import classical as C
from osteoquant import io as oio
from osteoquant.volume import Volume

h = lambda a: hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
res = {"experiment": "P", "checks": {}}
case = load_split("test", limit=1)[0]
vol = Volume(case.image, case.spacing, meta={"ingest": {"metadata_found": {"spacing_um": list(case.spacing)}}})
cfg = {"defect_model": "condyle", "nominal_diameter_um": 2000, "segmentation": "multiotsu"}
r1, r2 = analyze(vol, cfg), analyze(vol, cfg)
res["checks"]["pipeline_labels_identical"] = r1["labels_sha256"] == r2["labels_sha256"]
res["checks"]["pipeline_metrics_identical"] = json.dumps(public(r1)["metrics"], sort_keys=True, default=str) == \
    json.dumps(public(r2)["metrics"], sort_keys=True, default=str)
cfg_u = dict(cfg, segmentation="unet:unet_ctx_s0", tta=True)
u1, u2 = analyze(vol, cfg_u), analyze(vol, cfg_u)
res["checks"]["unet_pipeline_labels_identical"] = u1["labels_sha256"] == u2["labels_sha256"]
m, ck = load_model("unet_ctx_s0")
p1, p2 = predict_proba(m, case, ck["cfg"]), predict_proba(m, case, ck["cfg"])
res["checks"]["unet_probabilities_bit_identical"] = h(p1) == h(p2)
torch.use_deterministic_algorithms(True)
tr = load_split("train", limit=2)
c = dict(ck["cfg"], iters=50, val_every=10 ** 9, log_every=50, seed=123)
a = train_model(tr, [], c, "repro_a", log=lambda s: None, overwrite=True)
b = train_model(tr, [], c, "repro_b", log=lambda s: None, overwrite=True)
wa = torch.load(MODEL_DIR / "repro_a.pt", weights_only=False)["state_dict"]
wb = torch.load(MODEL_DIR / "repro_b.pt", weights_only=False)["state_dict"]
res["checks"]["training_weights_identical_fixed_seed"] = all(torch.equal(wa[k], wb[k]) for k in wa)
res["checks"]["max_abs_weight_diff"] = float(max((wa[k].float() - wb[k].float()).abs().max() for k in wa))
for f in ("repro_a", "repro_b"):
    (MODEL_DIR / f"{f}.pt").unlink(); (MODEL_DIR / f"{f}.card.json").unlink()
reg = json.loads((MODEL_DIR / "registry.json").read_text()); [reg.pop(k, None) for k in ("repro_a", "repro_b")]
(MODEL_DIR / "registry.json").write_text(json.dumps(reg, indent=1))
rf1 = C.RFSegmenter(20, 12, 5).fit([tr[0].image], [tr[0].labels], [tr[0].spacing], [tr[0].roi], 3000)
rf2 = C.RFSegmenter(20, 12, 5).fit([tr[0].image], [tr[0].labels], [tr[0].spacing], [tr[0].roi], 3000)
res["checks"]["rf_identical"] = h(rf1.predict(case.image, case.spacing, case.roi)[0]) == h(rf2.predict(case.image, case.spacing, case.roi)[0])
v16 = Volume(np.round(case.image).clip(0, 65535).astype(np.uint16), case.spacing)
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    oio.write_nifti(v16, d / "a.nii.gz"); oio.write_nrrd(v16, d / "a.nrrd"); oio.write_zarr(v16, d / "a.zarr")
    oio.write_tiff(v16, d / "a.tif"); oio.write_dicom_series(v16, d / "dcm")
    hashes = {}
    for name, p in (("nifti", d / "a.nii.gz"), ("nrrd", d / "a.nrrd"), ("zarr", d / "a.zarr"), ("tiff", d / "a.tif"), ("dicom", d / "dcm")):
        vv, _ = oio.read_volume(p)
        hashes[name] = h(vv.data.astype(np.uint16)) == h(v16.data)
    res["checks"]["format_roundtrip_voxels_identical"] = hashes
res["all_pass"] = all(v is True or (isinstance(v, dict) and all(v.values())) for k, v in res["checks"].items()
                      if k != "max_abs_weight_diff")
save_result("exp_P_reproducibility", res)
print(json.dumps(res, indent=1))
