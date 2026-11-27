"""Experiment S2 (v2, revised after cycle-1 review ML-01…05) — closing the synthetic→real gap (FA-02).

Real data: SPROUT dog forelimb (10 train / 5 test specimens, 2-class bone labels in a band).
Gen-0 baseline: synthetic U-Net (unet_noctx_s0) zero-shot Dice 0.379; fine-tuned on 1 real scan 0.787;
real-only (10 scans, 800 iters) 0.826.

S2a  Diagnosis on TRAINING specimens only: Gen-0 model zero-shot with test-time rescaling (×0.5…×2).
     The zoom chosen here (best on training specimens) is the only zoom later applied to test specimens.
S2b  Domain-randomised synthetic pretraining (osteoquant.ml.synth_dr v2: whole-volume-like normalisation;
     phantom fractions from the 48 synthetic TRAINING specimens; no real data). Zoom selected on real
     training specimens, then evaluated once on test specimens.
S2c  Few-shot fine-tuning, k ∈ {1, 3} real training specimens × 3 seeds (subset per seed, identical across
     arms), 300 iterations, batch 2, identical LR 1e-3 for all arms, plus a scratch arm at LR 3e-3:
       scratch (2-class), gen0_synth (4-class head; real bone mapped to HOST class 3, the class of mature bone),
       dr_synth (2-class). Head sizes differ (stated limitation).
     Evaluation: 5 test specimens (primary) and the training specimens NOT used for that seed (secondary).
     Statistics: per specimen, mean over seeds; bootstrap over specimens (n = 5); paired per-specimen
     differences between arms with bootstrap 95% CI. Seeds are not treated as independent replicates.
"""
from __future__ import annotations

import glob
import json
import sys
import time

import numpy as np
from scipy import ndimage as ndi

from common import ROOT, save_result
from real_dog import split, score, bone_prob
from osteoquant.ml.synth_dr import DRSampler, DRConfig
from osteoquant.ml.train import Case, train_model, load_model, predict_proba, MODEL_DIR

STAGES = sys.argv[1:] or ["a", "b", "c"]
OUT = {"experiment": "S2v2", "rows": []}
train, test = split()


def dice_cases(model, cfg, cases, zoom=1.0):
    out = []
    for c in cases:
        cc = c if zoom == 1.0 else Case(c.case_id, ndi.zoom(c.image, zoom, order=1), None, None, c.spacing)
        p = bone_prob(predict_proba(model, cc, cfg, tta=False))
        if zoom != 1.0:
            p = ndi.zoom(p, np.array(c.image.shape) / np.array(p.shape), order=1)[: c.image.shape[0], : c.image.shape[1], : c.image.shape[2]]
        out.append({"case": c.case_id, "zoom": zoom, **score(p > 0.5, c)})
    return out


def boot_ci(x, n=4000, seed=0):
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    m = [rng.choice(x, x.size).mean() for _ in range(n)]
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def pick_zoom(model, cfg, tag):
    res = {}
    for z in (0.5, 0.75, 1.0, 1.5, 2.0):
        rr = dice_cases(model, cfg, train, z)
        for r in rr:
            OUT["rows"].append({"method": tag, "split": "train_diag", **r})
        res[z] = float(np.mean([r["dice"] for r in rr]))
        print(tag, "TRAIN zoom", z, round(res[z], 3), flush=True)
    return max(res, key=res.get), res


t0 = time.time()
STATE = MODEL_DIR.parent / "experiments" / "results" / "exp_S2_state.json"
state = json.loads(STATE.read_text()) if STATE.exists() else {}
if "a" in STAGES:
    m, ck = load_model("unet_noctx_s0")
    z, res = pick_zoom(m, ck["cfg"], "gen0_synth_zeroshot")
    state["gen0_zoom"] = z
    OUT["gen0_train_zoom_curve"] = res
    for zz in sorted({1.0, z}):
        for r in dice_cases(m, ck["cfg"], test, zz):
            OUT["rows"].append({"method": "gen0_synth_zeroshot", "split": "test", **r})
    print("gen0 test", {zz: round(np.mean([r["dice"] for r in OUT["rows"] if r["method"] == "gen0_synth_zeroshot" and r["split"] == "test" and r["zoom"] == zz]), 3) for zz in sorted({1.0, z})}, flush=True)

if "b" in STAGES:
    files = sorted(glob.glob(str(ROOT / "data/processed/synth/train/*.npz")))
    frs = [np.load(f)["fractions"] for f in files]
    manifest = [{"case_id": f.split("/")[-1][:-4], "provenance": "synthetic", "commercial_use": "allowed"} for f in files]
    sampler = DRSampler(frs, DRConfig(target="mineral"), manifest=manifest)
    name = "unet_dr2_mineral_s0"
    cfg = dict(patch=(48, 48, 48), batch=2, iters=1500, lr=3e-3, base=12, levels=4, threads=4, n_classes=2,
               log_every=250, seed=0, sampler=sampler.name, extra_provenance=["synthetic"])
    if not (MODEL_DIR / f"{name}.pt").exists():
        train_model([], [], cfg, name, log=lambda s_: print(name, s_, flush=True), sample_fn=sampler)
    m, ck = load_model(name)
    z, res = pick_zoom(m, ck["cfg"], "dr_zeroshot")
    state["dr_zoom"] = z
    OUT["dr_train_zoom_curve"] = res
    for zz in sorted({1.0, z}):
        for r in dice_cases(m, ck["cfg"], test, zz):
            OUT["rows"].append({"method": "dr_zeroshot", "split": "test", **r})
    print("dr test", {zz: round(np.mean([r["dice"] for r in OUT["rows"] if r["method"] == "dr_zeroshot" and r["split"] == "test" and r["zoom"] == zz]), 3) for zz in sorted({1.0, z})}, flush=True)

if "c" in STAGES:
    arms = {"scratch_lr1e-3": (None, 1e-3), "scratch_lr3e-3": (None, 3e-3),
            "gen0_synth": ("unet_noctx_s0", 1e-3), "dr_synth": ("unet_dr2_mineral_s0", 1e-3)}
    for k in (1, 3):
        for seed in (0, 1, 2):
            rng = np.random.default_rng(100 + seed)
            idx = rng.choice(len(train), k, replace=False)
            sub = [train[i] for i in idx]
            unused = [c for i, c in enumerate(train) if i not in set(idx)]
            for arm, (src, lr) in arms.items():
                name = f"s2v2_{arm.replace('-', '').replace('.', '')}_k{k}_s{seed}"
                cases = sub
                if src:
                    _, ck0 = load_model(src)
                    cfg = {kk: v for kk, v in ck0["cfg"].items() if kk not in ("sampler", "extra_provenance")}
                    cfg.update(iters=300, lr=lr, val_every=10 ** 9, log_every=300, seed=seed, batch=2)
                    init_path = str(MODEL_DIR / f"{src}.pt")
                    if cfg.get("n_classes", 4) == 4:     # real bone = mature bone → HOST class (review ML-01)
                        cases = [Case(c.case_id, c.image, np.where(c.labels == 1, 3, c.labels).astype(np.uint8),
                                      c.roi, c.spacing, c.provenance, c.commercial_use, c.meta) for c in sub]
                else:
                    cfg = dict(patch=(48, 48, 48), batch=2, iters=300, lr=lr, base=12, levels=4, threads=4,
                               n_classes=2, log_every=300, val_every=10 ** 9, seed=seed)
                    init_path = None
                if not (MODEL_DIR / f"{name}.pt").exists():
                    train_model(cases, [], cfg, name, log=lambda s_: None, init_from=init_path)
                m, ck = load_model(name)
                for split_name, cs in (("test", test), ("unused_train", unused)):
                    for r in dice_cases(m, ck["cfg"], cs):
                        OUT["rows"].append({"method": f"fewshot_{arm}_k{k}", "split": split_name, "seed": seed,
                                            "train_cases": [c.case_id for c in sub], **r})
                print(arm, "k", k, "seed", seed, "test mean", round(np.mean([r["dice"] for r in OUT["rows"][-len(test) - len(unused):][:len(test)]]), 3), flush=True)
    summ, paired = {}, {}
    for k in (1, 3):
        per_arm = {}
        for arm in arms:
            rr = [r for r in OUT["rows"] if r["method"] == f"fewshot_{arm}_k{k}" and r["split"] == "test"]
            spec = {}
            for r in rr:
                spec.setdefault(r["case"], []).append(r["dice"])
            per_arm[arm] = {c: float(np.mean(v)) for c, v in spec.items()}
            vals = list(per_arm[arm].values())
            summ[f"{arm}_k{k}"] = dict(zip(("mean", "ci_lo", "ci_hi"), boot_ci(vals)), n_specimens=len(vals))
            uu = [r["dice"] for r in OUT["rows"] if r["method"] == f"fewshot_{arm}_k{k}" and r["split"] == "unused_train"]
            summ[f"{arm}_k{k}"]["unused_train_mean"] = float(np.mean(uu)) if uu else None
        for a_ in arms:
            for b_ in arms:
                if a_ < b_:
                    d = [per_arm[a_][c] - per_arm[b_][c] for c in per_arm[a_]]
                    paired[f"{a_}_minus_{b_}_k{k}"] = dict(zip(("mean", "ci_lo", "ci_hi"), boot_ci(d)))
    OUT["fewshot_summary"] = summ
    OUT["paired_differences"] = paired
    print(json.dumps(summ, indent=1))
    print(json.dumps(paired, indent=1))

STATE.write_text(json.dumps(state))
OUT["seconds"] = time.time() - t0
save_result(f"exp_S2v2_sim2real_{''.join(STAGES)}", OUT)
