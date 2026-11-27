"""Experiment S2 — closing the synthetic→real gap (FORENSIC_AUDIT FA-02).

Real data: SPROUT dog forelimb (10 train / 5 test specimens, 2-class bone labels in a band).
Gen-0 baseline: synthetic U-Net (unet_noctx_s0) zero-shot Dice 0.379; fine-tuned on 1 real scan 0.787;
real-only (10 scans, 800 iters) 0.826.

S2a  Diagnosis: zero-shot Gen-0 model with test-time rescaling (×0.5…×2) — is the gap a structure-scale
     mismatch?
S2b  Domain-randomised synthetic pretraining (osteoquant.ml.synth_dr, phantom fractions from the 48
     synthetic TRAINING specimens only; no real data): zero-shot on real test specimens.
S2c  Few-shot fine-tuning, k ∈ {1, 3} real training specimens × 3 seeds (subset drawn per seed), 300
     iterations, from three initialisations: scratch, Gen-0 synthetic model, DR model. Specimen-level
     Dice mean and 95% bootstrap CI over the 5 test specimens × 3 seeds.
All selection decisions use training specimens only; the 5 test specimens are evaluated once per model.
"""
from __future__ import annotations

import glob
import sys
import time

import numpy as np
from scipy import ndimage as ndi

from common import ROOT, save_result
from real_dog import split, score, bone_prob
from osteoquant.ml.synth_dr import DRSampler, DRConfig
from osteoquant.ml.train import train_model, load_model, predict_proba, MODEL_DIR

STAGES = sys.argv[1:] or ["a", "b", "c"]
OUT = {"experiment": "S2", "rows": []}
train, test = split()


def evaluate(tag, model, cfg, cases=test, zoom=1.0, extra=None):
    res = []
    for c in cases:
        cc = c
        if zoom != 1.0:
            from osteoquant.ml.train import Case
            cc = Case(c.case_id, ndi.zoom(c.image, zoom, order=1), None, None, c.spacing)
        p = bone_prob(predict_proba(model, cc, cfg, tta=False))
        if zoom != 1.0:
            p = ndi.zoom(p, np.array(c.image.shape) / np.array(p.shape), order=1)[: c.image.shape[0], : c.image.shape[1], : c.image.shape[2]]
        r = {"method": tag, "case": c.case_id, "zoom": zoom, **score(p > 0.5, c), **(extra or {})}
        OUT["rows"].append(r)
        res.append(r["dice"])
    print(tag, "zoom", zoom, "mean Dice", round(float(np.mean(res)), 3), flush=True)
    return float(np.mean(res))


def boot_ci(x, n=2000, seed=0):
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    m = [rng.choice(x, x.size).mean() for _ in range(n)]
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


t0 = time.time()
if "a" in STAGES:
    m, ck = load_model("unet_noctx_s0")
    for z in (0.5, 0.75, 1.0, 1.5, 2.0):
        evaluate("gen0_synth_zeroshot", m, ck["cfg"], zoom=z)

if "b" in STAGES:
    frs = [np.load(f)["fractions"] for f in sorted(glob.glob(str(ROOT / "data/processed/synth/train/*.npz")))]
    sampler = DRSampler(frs, DRConfig(target="mineral"))
    for seed in (0,):
        name = f"unet_dr_mineral_s{seed}"
        cfg = dict(patch=(48, 48, 48), batch=2, iters=1500, lr=3e-3, base=12, levels=4, threads=4, n_classes=2,
                   log_every=250, seed=seed, sampler=sampler.name, extra_provenance=["synthetic"])
        if not (MODEL_DIR / f"{name}.pt").exists():
            train_model([], [], cfg, name, log=lambda s: print(name, s, flush=True), sample_fn=sampler)
        m, ck = load_model(name)
        for z in (0.75, 1.0, 1.5):
            evaluate(f"dr_s{seed}_zeroshot", m, ck["cfg"], zoom=z)

if "c" in STAGES:
    inits = {"scratch": None, "gen0_synth": "unet_noctx_s0", "dr_synth": "unet_dr_mineral_s0"}
    for k in (1, 3):
        for seed in (0, 1, 2):
            rng = np.random.default_rng(100 + seed)
            sub = [train[i] for i in rng.choice(len(train), k, replace=False)]
            for init, src in inits.items():
                name = f"s2c_{init}_k{k}_s{seed}"
                if src:
                    _, ck0 = load_model(src)
                    cfg = dict(ck0["cfg"], iters=300, lr=1e-3, val_every=10 ** 9, log_every=300, seed=seed)
                    cfg.pop("sampler", None); cfg.pop("extra_provenance", None)
                    init_path = str(MODEL_DIR / f"{src}.pt")
                else:
                    cfg = dict(patch=(48, 48, 48), batch=2, iters=300, lr=3e-3, base=12, levels=4, threads=4,
                               n_classes=2, log_every=300, val_every=10 ** 9, seed=seed)
                    init_path = None
                if not (MODEL_DIR / f"{name}.pt").exists():
                    train_model(sub, [], cfg, name, log=lambda s: None, init_from=init_path)
                m, ck = load_model(name)
                evaluate(f"fewshot_{init}_k{k}", m, ck["cfg"], extra={"seed": seed, "train_cases": [c.case_id for c in sub]})
    summ = {}
    for init in ("scratch", "gen0_synth", "dr_synth"):
        for k in (1, 3):
            d = [r["dice"] for r in OUT["rows"] if r["method"] == f"fewshot_{init}_k{k}"]
            if d:
                summ[f"{init}_k{k}"] = dict(zip(("mean", "ci_lo", "ci_hi"), boot_ci(d)), n=len(d))
    OUT["fewshot_summary"] = summ
    print(summ)

OUT["seconds"] = time.time() - t0
save_result(f"exp_S2_sim2real_{''.join(STAGES)}", OUT)
