"""Shared loader for the SPROUT dog forelimb micro-CT dataset (Zenodo 10.5281/zenodo.24047383, CC-BY-4.0).

Same preprocessing as Experiment H: ×2 block-mean downsampling, labels by majority, binary bone label,
evaluation band = labelled bones dilated by 6 voxels; outside the band labels are IGNORE (255).
Official split (train_test_split.csv): 10 train / 5 test specimens. Splits are by specimen (dog).
"""
from __future__ import annotations

import csv

import numpy as np
import tifffile
from scipy import ndimage as ndi

from common import ROOT
from osteoquant.ml.train import Case
from osteoquant.phantom.imaging import downsample_labels
from osteoquant.segment.metrics import binary_metrics

D = ROOT / "data" / "raw" / "zenodo_24047383_sprout" / "extracted" / "data_dog_forelimb"


def load(name):
    img = tifffile.imread(D / "scans" / name).astype(np.float32)
    lab = tifffile.imread(D / "reference_seg" / name)
    s = [n // 2 * 2 for n in img.shape]
    img = img[: s[0], : s[1], : s[2]].reshape(s[0] // 2, 2, s[1] // 2, 2, s[2] // 2, 2).mean(axis=(1, 3, 5))
    lab = (downsample_labels(lab[: s[0], : s[1], : s[2]], 2) > 0).astype(np.uint8)
    roi = ndi.binary_dilation(lab > 0, iterations=6)
    lab = np.where(roi, lab, 255).astype(np.uint8)
    return Case(name, img, lab, roi, (1.0, 1.0, 1.0), "public-real", "allowed", {"dataset": "SPROUT dog forelimb"})


def split():
    sp = {r["filename"].strip(): r["split"].strip() for r in csv.DictReader(open(D / "train_test_split.csv"))}
    train = [load(f) for f, s in sorted(sp.items()) if s == "train"]
    test = [load(f) for f, s in sorted(sp.items()) if s == "test"]
    return train, test


def score(pred, c):
    m = binary_metrics(pred & c.roi, (c.labels == 1) & c.roi, spacing=(1, 1, 1))
    return {"dice": m["dice"], "hd95_vox": m["hd95_um"], "vol_err": m["volume_error_rel"]}


def bone_prob(prob):
    """Mineral probability from a 2-class (bg, bone) or 4-class (bg, new, graft, host) output."""
    return prob[1:].sum(0)
