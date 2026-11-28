"""Experiments H and I — real public micro-CT: bone segmentation and cross-domain transfer.

Data: SPROUT dog forelimb micro-CT (Zenodo 10.5281/zenodo.24047383, CC-BY-4.0): 15 specimens,
manually corrected reference segmentations of 4 bones; official split train 10 / test 5 (by
specimen). Task: bone vs non-bone WITHIN A BAND around the labelled bones (union of the 4 forelimb-bone
labels dilated by 6 voxels at the ×2 working resolution). The scans contain the whole thoracic
region and only the forelimb bones are labelled, so whole-volume bone-vs-background is ill-posed
(unlabelled vertebrae/ribs would count as false positives — observed in a first run and corrected).
Outside the band labels are set to IGNORE (255) for training and excluded from evaluation. Voxel spacing is not stored in
the files, so surface distances are reported in voxels. Volumes are block-mean downsampled ×2
(labels by majority) for all methods to bound CPU time.

H (real-data segmentation): Otsu, GMM-2, Random Forest (all 10 training specimens), and a 2-class
  U-Net trained on the 10 training specimens (licence: CC-BY-4.0 → commercial-eligible with
  attribution; provenance 'public-real').
I (cross-domain generalisation): the SYNTHETIC-trained 3-class U-Net (unet_noctx_s0) applied
  zero-shot to real dog bone (mineral := any of new/graft/host), then fine-tuned on k ∈ {1, 3}
  real training specimens (300 iterations).
Metrics: Dice, HD95 (voxels), relative volume error; specimen-level mean (n = 5 test).
"""
import csv

import numpy as np
import tifffile

from common import ROOT, save_result
from osteoquant.ml.train import Case, train_model, load_model, predict_proba, MODEL_DIR
from osteoquant.phantom.imaging import downsample_labels
from osteoquant.segment import classical as C
from osteoquant.segment.metrics import binary_metrics
from scipy import ndimage as ndi

D = ROOT / "data" / "raw" / "zenodo_24047383_sprout" / "extracted" / "data_dog_forelimb"


def load(name):
    img = tifffile.imread(D / "scans" / name).astype(np.float32)
    lab = tifffile.imread(D / "reference_seg" / name)
    s = [n // 2 * 2 for n in img.shape]
    img = img[: s[0], : s[1], : s[2]].reshape(s[0] // 2, 2, s[1] // 2, 2, s[2] // 2, 2).mean(axis=(1, 3, 5))
    lab = (downsample_labels(lab[: s[0], : s[1], : s[2]], 2) > 0).astype(np.uint8)
    roi = ndi.binary_dilation(lab > 0, iterations=6)
    lab = np.where(roi, lab, 255).astype(np.uint8)       # ignore outside the evaluation band
    return Case(name, img, lab, roi, (1.0, 1.0, 1.0), "public-real", "allowed", {"dataset": "SPROUT dog forelimb"})


split = {r["filename"].strip(): r["split"].strip() for r in csv.DictReader(open(D / "train_test_split.csv"))}
train = [load(f) for f, s in split.items() if s == "train"]
test = [load(f) for f, s in split.items() if s == "test"]
print("train", len(train), "test", len(test), [c.image.shape for c in test], flush=True)


def score(pred, c):
    m = binary_metrics(pred & c.roi, (c.labels == 1) & c.roi, spacing=(1, 1, 1))
    return {"dice": m["dice"], "hd95_vox": m["hd95_um"], "vol_err": m["volume_error_rel"]}


rows = []


def add(method, c, pred):
    r = {"method": method, "case": c.case_id, **score(pred, c)}
    rows.append(r)
    print(r, flush=True)


# ---------------------------------------------------------------- H: classical + RF
# RF trained on ALL 10 training specimens (same data as the U-Net; review finding Q-03)
rf = C.RFSegmenter(40, 16, 0, scales_um=(0, 1, 2, 4), feature_set="no_spatial").fit(
    [c.image for c in train], [c.labels for c in train], [x.spacing for x in train], [x.roi for x in train], 6000)
for c in test:
    add("otsu_in_band", c, c.image > C.threshold_otsu(c.image, c.roi)[1])
    g, order = C.gmm_threshold(c.image, c.roi, k=2)
    mu = np.sort(g.means_.ravel())
    add("gmm2", c, c.image > mu.mean())
    add("random_forest_10train", c, rf.predict(c.image, c.spacing, None)[0] > 0)

# ---------------------------------------------------------------- H: real-trained U-Net
cfg = dict(patch=(48, 48, 48), batch=2, iters=800, lr=3e-3, base=12, levels=4, threads=4, n_classes=2, log_every=200,
           val_every=10 ** 9, loss={"dice": 1.0, "ce": 1.0}, seed=0, fg_prob=0.6)
if not (MODEL_DIR / "unet_dog_bone_real.pt").exists():
    train_model(train, [], cfg, "unet_dog_bone_real", log=lambda s: print("dog", s, flush=True), overwrite=True)
m, ck = load_model("unet_dog_bone_real")
for c in test:
    add("unet_trained_on_10_real", c, predict_proba(m, c, ck["cfg"]).argmax(0) > 0)

# ---------------------------------------------------------------- I: synthetic → real transfer
ms, cks = load_model("unet_noctx_s0")
for c in test:
    add("synthetic_unet_zero_shot", c, predict_proba(ms, c, cks["cfg"]).argmax(0) > 0)
for k in (1, 3):
    sub = train[:k]
    sub3 = [Case(c.case_id, c.image, np.where(c.labels == 1, 3, c.labels).astype(np.uint8), c.roi, c.spacing, c.provenance,
                 c.commercial_use) for c in sub]   # map real bone -> 'host bone' class of the 3-class model
    ft = dict(cks["cfg"], iters=300, lr=1e-3, val_every=10 ** 9, log_every=300, seed=7)
    train_model(sub3, [], ft, f"unet_synth_ft_dog_k{k}", log=lambda s: None, init_from=str(MODEL_DIR / "unet_noctx_s0.pt"),
                overwrite=True)
    mf, ckf = load_model(f"unet_synth_ft_dog_k{k}")
    for c in test:
        add(f"synthetic_unet_finetuned_k{k}", c, predict_proba(mf, c, ckf["cfg"]).argmax(0) > 0)

summary = {}
for meth in dict.fromkeys(r["method"] for r in rows):
    R = [r for r in rows if r["method"] == meth]
    summary[meth] = {k: float(np.nanmean([r[k] for r in R])) for k in ("dice", "hd95_vox", "vol_err")}
save_result("exp_H_I_real", {"experiment": "H/I", "dataset": "SPROUT dog forelimb, Zenodo 10.5281/zenodo.24047383, CC-BY-4.0",
                             "n_train": len(train), "n_test": len(test), "downsample": 2, "rows": rows, "summary": summary})
for k, v in summary.items():
    print(f"{k:34s} Dice {v['dice']:.3f}  HD95 {v['hd95_vox']:.1f} vox  vol err {v['vol_err']:+.3f}")
