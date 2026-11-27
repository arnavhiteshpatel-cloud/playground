"""Experiment S3 — self-supervised (masked denoising) pretraining on UNLABELLED real micro-CT, then few-shot.

Third route to the synthetic→real gap (FA-02), complementary to S2 (domain randomisation, Gen-0 synthetic).
Pretext task: reconstruct the clean normalised patch from a corrupted one (Gaussian noise + random 8³ cube
masking of 30% of the volume), MSE loss, same U-Net architecture with a 1-channel regression head.
Unlabelled data (labels never read): the 10 SPROUT dog TRAINING scans (images only) + mouse knee DICOM
(Zenodo 3909552, CC-BY-4.0, downsampled ×2). Test specimens are never used for pretraining.
Fine-tuning: identical protocol to S2v2 (k ∈ {1,3} × seeds {0,1,2}, same subsets, 300 iterations, LR 1e-3,
ignore-aware boundary weights), head replaced by a fresh 2-class head. Statistics as S2v2 (per-specimen means
over seeds, bootstrap over the 5 test specimens, paired differences vs S2v2 arms when available).
"""
from __future__ import annotations

import glob
import json
import time

import numpy as np
import torch
import torch.nn.functional as F

from common import ROOT, save_result, RESULTS
from real_dog import split, score, bone_prob
from onnx_eval import predict as onnx_predict
from osteoquant.ml.train import (Case, MODEL_DIR, build_input, predict_proba, sample_patch, save_model,
                                 seed_everything, train_model, load_model)
from osteoquant.ml.unet import UNet3D

train, test = split()
PRE = "unet_ssl_real_s0"


def unlabelled_volumes():
    vols = [build_input(c, {"norm": "percentile"}) for c in train]          # images only
    try:
        from osteoquant.io.readers import read_volume
        d = sorted(glob.glob(str(ROOT / "data/raw/zenodo_3909552_mouse_oa_knee/**/*.dcm"), recursive=True))
        if d:
            import os
            v = read_volume(os.path.dirname(d[0]), do_hash=False, step=2)
            a = v.data[:, ::2, ::2].astype(np.float32)
            vols.append(build_input(Case("knee", a, None, None), {"norm": "percentile"}))
    except Exception as e:
        print("knee volume skipped:", e, flush=True)
    return vols


def pretrain(iters=800, seed=0, ps=(48, 48, 48), bs=2):
    seed_everything(seed)
    torch.set_num_threads(4)
    rng = np.random.default_rng(seed)
    vols = unlabelled_volumes()
    print("unlabelled volumes", len(vols), [v.shape for v in vols], flush=True)
    model = UNet3D(in_ch=1, n_classes=1, base=12, levels=4)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-3, total_steps=iters, pct_start=0.1)
    t0 = time.time()
    hist = []
    for it in range(iters):
        xs, ys = [], []
        for _ in range(bs):
            v = vols[rng.integers(len(vols))]
            dummy = np.zeros(v.shape[1:], np.int64)
            xp, _ = sample_patch(v, dummy, None, ps, rng, 0.0)
            xp = np.pad(xp, [(0, 0)] + [(0, max(0, p - s)) for p, s in zip(ps, xp.shape[1:])], mode="edge")
            clean = xp.copy()
            noisy = xp + rng.normal(0, rng.uniform(0.02, 0.1), xp.shape).astype(np.float32)
            m = np.zeros(ps, bool)
            for _ in range(int(0.3 * np.prod(ps) / 512)):
                z, y, x = (int(rng.integers(0, p - 8)) for p in ps)
                m[z:z + 8, y:y + 8, x:x + 8] = True
            noisy[0][m] = 0.0
            xs.append(noisy)
            ys.append(clean)
        xb, yb = torch.from_numpy(np.stack(xs)), torch.from_numpy(np.stack(ys))
        loss = F.mse_loss(model(xb), yb)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if (it + 1) % 200 == 0:
            hist.append({"iter": it + 1, "mse": float(loss), "sec": round(time.time() - t0, 1)})
            print(hist[-1], flush=True)
    # save as a 2-class model whose head is freshly initialised (only the encoder/decoder are pretrained)
    m2 = UNet3D(in_ch=1, n_classes=2, base=12, levels=4)
    sd = {k: v for k, v in model.state_dict().items() if not k.startswith("head.")}
    m2.load_state_dict(sd, strict=False)
    cfg = dict(patch=list(ps), batch=bs, iters=iters, lr=3e-3, base=12, levels=4, threads=4, n_classes=2, seed=seed,
               pretext="masked_denoising", extra_provenance=["public-real"])
    cases = [Case(c.case_id, c.image, None, None, c.spacing, "public-real", "allowed") for c in train]
    return save_model(m2, cfg, PRE, cases, hist, time.time() - t0,
                      sampler_manifest=[{"case_id": c.case_id, "labels_used": False} for c in train])


def main():
    t0 = time.time()
    if not (MODEL_DIR / f"{PRE}.pt").exists():
        pretrain()
    rows = []
    for k in (1, 3):
        for seed in (0, 1, 2):
            rng = np.random.default_rng(100 + seed)                 # same subsets as S2v2
            idx = rng.choice(len(train), k, replace=False)
            sub = [train[i] for i in idx]
            name = f"s3_ssl_k{k}_s{seed}"
            cfg = dict(patch=(48, 48, 48), batch=2, iters=300, lr=1e-3, base=12, levels=4, threads=4, n_classes=2,
                       log_every=300, val_every=10 ** 9, seed=seed,
                       loss={"dice": 1.0, "ce": 1.0, "boundary_w": 1.0, "boundary_ignore_aware": True})
            if not (MODEL_DIR / f"{name}.pt").exists():
                train_model(sub, [], cfg, name, log=lambda s_: None, init_from=str(MODEL_DIR / f"{PRE}.pt"))
            ck = load_model(name)[1]
            for c in test:
                p = bone_prob(onnx_predict(name, c, ck["cfg"]))
                rows.append({"method": f"fewshot_ssl_k{k}", "seed": seed, "case": c.case_id, **score(p > 0.5, c)})
            print("ssl k", k, "seed", seed, round(np.mean([r["dice"] for r in rows[-len(test):]]), 3), flush=True)
    summ = {}
    rng = np.random.default_rng(0)
    for k in (1, 3):
        spec = {}
        for r in rows:
            if r["method"] == f"fewshot_ssl_k{k}":
                spec.setdefault(r["case"], []).append(r["dice"])
        v = np.array([np.mean(x) for x in spec.values()])
        bs = [rng.choice(v, v.size).mean() for _ in range(4000)]
        summ[f"ssl_k{k}"] = {"mean": float(v.mean()), "ci_lo": float(np.percentile(bs, 2.5)),
                             "ci_hi": float(np.percentile(bs, 97.5)), "n_specimens": int(v.size)}
    print(summ)
    save_result("exp_S3_selfsupervised", {"experiment": "S3", "summary": summ, "rows": rows,
                                          "seconds": time.time() - t0})


if __name__ == "__main__":
    main()
