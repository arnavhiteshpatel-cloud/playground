"""Experiment J — low-label adaptation to unseen graft materials.

Hypothesis (playbook U3): a model pre-trained on synthetic data for four materials can be adapted
to a new material with ≤10 labelled scans to reach graft Dice ≥ 0.8.
Data: ood_mat split (bioglass 45S5 and deproteinised bovine bone mineral = held-out materials).
Specimens 0–23: adaptation pool; 24–39: fixed test set (16), split by specimen.
Arms: (a) zero-shot U-Net (unet_ctx_s0); (b) U-Net fine-tuned on k ∈ {1,3,5,10,20} pool scans
(300 iterations, lr 1e-3, 2 random draws for k ≤ 5); (c) RF trained from scratch on the same k scans.
Metric: graft and new-bone Dice in ROI on the test set; per-material breakdown; learning-curve fit.
CAVEAT: synthetic materials differ from training materials only by simulated density/porosity
and resorption — real new materials also differ in morphology, so this is an optimistic bound.
"""
import numpy as np
from common import load_split, save_result
from osteoquant.ml.train import train_model, load_model, predict_proba, MODEL_DIR
from osteoquant.segment.metrics import multiclass_metrics
from osteoquant.segment import classical as C
from osteoquant.stats import learning_curve_fit

ood = load_split("ood_mat")
pool, test = ood[:24], ood[24:40]
print("pool", len(pool), "test", len(test), flush=True)


def eval_unet(name):
    m, ck = load_model(name)
    out = []
    for c in test:
        pred = predict_proba(m, c, ck["cfg"]).argmax(0).astype(np.uint8)
        r = multiclass_metrics(pred, c.labels, spacing=c.spacing, mask=c.roi, classes=(1, 2), distances=False)
        out.append((c.meta["spec"]["material"], r["per_class"]["graft"]["dice"], r["per_class"]["new_bone"]["dice"]))
    return out


def eval_rf(rf):
    out = []
    for c in test:
        pred = rf.predict(c.image, c.spacing, c.roi)[0]
        r = multiclass_metrics(pred, c.labels, spacing=c.spacing, mask=c.roi, classes=(1, 2), distances=False)
        out.append((c.meta["spec"]["material"], r["per_class"]["graft"]["dice"], r["per_class"]["new_bone"]["dice"]))
    return out


def summarize(arm, k, rep, res):
    row = {"arm": arm, "k": k, "rep": rep, "dice_graft": float(np.mean([r[1] for r in res])),
           "dice_new": float(np.mean([r[2] for r in res]))}
    for mat in sorted({r[0] for r in res}):
        row[f"graft_{mat}"] = float(np.mean([r[1] for r in res if r[0] == mat]))
    print(row, flush=True)
    return row


rows = [summarize("unet_zero_shot", 0, 0, eval_unet("unet_ctx_s0"))]
base_cfg = load_model("unet_ctx_s0")[1]["cfg"]
rng = np.random.default_rng(0)
for k in (1, 3, 5, 10, 20):
    for rep in range(2 if k <= 5 else 1):
        idx = rng.choice(len(pool), k, replace=False)
        sub = [pool[i] for i in idx]
        cfg = dict(base_cfg, iters=300, lr=1e-3, val_every=10 ** 9, log_every=300, seed=100 + rep)
        name = f"adapt_k{k}_r{rep}"
        train_model(sub, [], cfg, name, log=lambda s: None, init_from=str(MODEL_DIR / "unet_ctx_s0.pt"), overwrite=True)
        rows.append(summarize("unet_finetune", k, rep, eval_unet(name)))
        rf = C.RFSegmenter(40, 16, 0).fit([c.image for c in sub], [c.labels for c in sub], [c.spacing for c in sub],
                                          [c.roi for c in sub], n_per_class=max(4000, 20000 // k))
        rows.append(summarize("rf_from_scratch", k, rep, eval_rf(rf)))
curves = {}
for arm in ("unet_finetune", "rf_from_scratch"):
    ks = sorted({r["k"] for r in rows if r["arm"] == arm})
    ys = [float(np.mean([r["dice_graft"] for r in rows if r["arm"] == arm and r["k"] == k])) for k in ks]
    curves[arm] = {"k": ks, "graft_dice": ys, "fit": learning_curve_fit(ks, ys),
                   "min_k_reaching_0.8": next((k for k, y in zip(ks, ys) if y >= 0.8), None)}
save_result("exp_J_adaptation", {"experiment": "J", "rows": rows, "curves": curves, "n_test": len(test)})
print(curves)
