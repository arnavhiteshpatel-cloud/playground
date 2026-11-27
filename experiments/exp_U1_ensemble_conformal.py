"""Experiment U1 — multi-seed variance, deep ensembles, failure detection and conformal volume intervals.

Addresses FORENSIC_AUDIT FA-03 (weak OOD: AUROC 0.66), FA-15 (measurement-based selection), FA-17 (single seed).

Models: 3-class synthetic U-Net (unet_noctx config), seeds 0–4, each trained on the same 48 training specimens.
Data (synthetic, specimen-level): val 8 (seed selection), cal 40 (conformal calibration, in-distribution),
test 16 (in-distribution), ood_mat 40 (held-out materials: 45S5 bioglass, DBBM).

Q1  Seed variance: per-seed graft/new-bone Dice and graft-volume error on test.
Q2  Model selection: does ranking seeds by validation Dice pick the same seed as ranking by validation
    graft-volume error? (ADR-G2-05)
Q3  Ensemble (mean probability of 5 seeds) vs single models.
Q4  Failure detection. Failure := |graft-volume error| > 20% or graft Dice < 0.8 (per scan).
    Scores: single-model mean entropy in ROI; ensemble mutual information (epistemic); ensemble
    graft-volume coefficient of variation across members; advisor intensity-oracle Dice (1 − value);
    combination (rank average). AUROC over test+ood (n = 56), bootstrap 95% CI.
Q5  Conformal graft-volume intervals: split conformal with normalised nonconformity
    |V_ens − V_true| / (sd_members + 0.02·V_ens), calibrated on cal (n = 40), α = 0.1. Coverage on test (ID)
    and ood (shift). Also coverage after gating out scans the failure detector flags.
"""
from __future__ import annotations

import sys
import time

import numpy as np

from common import load_split, save_result
from osteoquant.advisor.integration import support_for_scan
from osteoquant.ml.train import train_model, load_model, predict_proba, MODEL_DIR
from osteoquant.uncertainty import predictive_entropy

SEEDS = [0, 1, 2, 3, 4]
FAIL_VOL, FAIL_DICE = 0.20, 0.80


def model_name(s):
    return "unet_noctx_s0" if s == 0 else f"unet_noctx_s{s}"


def ensure_models():
    _, ck0 = load_model("unet_noctx_s0")
    train = load_split("train")
    val = load_split("val")
    for s in SEEDS[1:]:
        if not (MODEL_DIR / f"{model_name(s)}.pt").exists():
            cfg = dict(ck0["cfg"], seed=s)
            train_model(train, val, cfg, model_name(s), log=lambda m: print(model_name(s), m, flush=True))


def per_scan(c, probs_list):
    roi = c.roi
    y = c.labels
    vt = float(((y == 2) & roi).sum())
    out = {"case": c.case_id, "material": c.meta["spec"]["material"], "graft_true_vox": vt, "members": []}
    vols = []
    for p in probs_list:
        lab = p.argmax(0)
        vp = float(((lab == 2) & roi).sum())
        vols.append(vp)
        out["members"].append(_scores(lab, y, roi, vp, vt))
    pm = np.mean(probs_list, 0)
    lab = pm.argmax(0)
    ve = float(((lab == 2) & roi).sum())
    out["ensemble"] = _scores(lab, y, roi, ve, vt)
    ent_single = predictive_entropy(probs_list[0])
    ent_mean = predictive_entropy(pm)
    mi = ent_mean - np.mean([predictive_entropy(p) for p in probs_list], 0)
    out["score_entropy_single"] = float(ent_single[roi].mean())
    out["score_mutual_info"] = float(mi[roi].mean())
    out["score_vol_cv"] = float(np.std(vols) / max(np.mean(vols), 1.0))
    out["V_ens"] = ve
    out["V_sd"] = float(np.std(vols))
    sup = support_for_scan(c.image, roi, c.spacing, {"material": c.meta["spec"]["material"]})
    out["score_oracle"] = 1.0 - float(sup["intensity"].get("dice_graft", 0.0) or 0.0)
    out["advisor_status"] = sup["endpoints"]["residual_graft_volume"]["status"]
    return out


def _scores(lab, y, roi, vp, vt):
    d = {}
    for cl, n in ((1, "new"), (2, "graft")):
        a, b = (lab == cl) & roi, (y == cl) & roi
        d[f"dice_{n}"] = float(2 * (a & b).sum() / max(1, a.sum() + b.sum()))
    d["graft_vol_err"] = vp / vt - 1 if vt else float("nan")
    return d


def auroc(score, label):
    s, l = np.asarray(score, float), np.asarray(label, bool)
    pos, neg = s[l], s[~l]
    if not len(pos) or not len(neg):
        return float("nan")
    return float((np.sum(pos[:, None] > neg[None, :]) + 0.5 * np.sum(pos[:, None] == neg[None, :])) / (len(pos) * len(neg)))


def boot_auroc(score, label, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    s, l = np.asarray(score), np.asarray(label)
    vals = []
    for _ in range(n):
        i = rng.integers(0, len(s), len(s))
        v = auroc(s[i], l[i])
        if np.isfinite(v):
            vals.append(v)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def run_split(name, models):
    rows = []
    for c in load_split(name):
        probs = [predict_proba(m, c, ck["cfg"], tta=False) for m, ck in models]
        r = per_scan(c, probs)
        r["split"] = name
        rows.append(r)
        print(name, c.case_id, "ens graft Dice", round(r["ensemble"]["dice_graft"], 3), "vol err",
              round(r["ensemble"]["graft_vol_err"], 3), flush=True)
    return rows


def main():
    t0 = time.time()
    if "train" in sys.argv:
        ensure_models()
        return
    models = [load_model(model_name(s)) for s in SEEDS]
    rows = run_split("val", models) + run_split("cal", models) + run_split("test", models) + run_split("ood_mat", models)
    R = {"experiment": "U1", "rows": rows}
    # Q1/Q2 seeds
    def agg(split, key, member=None):
        rr = [r for r in rows if r["split"] == split]
        v = [(r["members"][member] if member is not None else r["ensemble"])[key] for r in rr]
        return float(np.mean(np.abs(v) if key == "graft_vol_err" else v))
    R["seeds"] = [{"seed": s, **{f"{sp}_{k}": agg(sp, k, i) for sp in ("val", "test", "ood_mat")
                                 for k in ("dice_graft", "dice_new", "graft_vol_err")}} for i, s in enumerate(SEEDS)]
    R["ensemble"] = {f"{sp}_{k}": agg(sp, k) for sp in ("val", "test", "ood_mat") for k in ("dice_graft", "dice_new", "graft_vol_err")}
    by_dice = int(np.argmax([s["val_dice_graft"] for s in R["seeds"]]))
    by_vol = int(np.argmin([s["val_graft_vol_err"] for s in R["seeds"]]))
    R["selection"] = {"best_val_dice_seed": SEEDS[by_dice], "best_val_volerr_seed": SEEDS[by_vol],
                      "test_abs_volerr_of_dice_choice": R["seeds"][by_dice]["test_graft_vol_err"],
                      "test_abs_volerr_of_vol_choice": R["seeds"][by_vol]["test_graft_vol_err"],
                      "note": "n_val = 8: selection is noisy; reported for transparency"}
    # Q4 failure detection on test + ood
    ev = [r for r in rows if r["split"] in ("test", "ood_mat")]
    fail = [abs(r["ensemble"]["graft_vol_err"]) > FAIL_VOL or r["ensemble"]["dice_graft"] < FAIL_DICE for r in ev]
    is_ood = [r["split"] == "ood_mat" for r in ev]
    scores = {k: [r[k] for r in ev] for k in ("score_entropy_single", "score_mutual_info", "score_vol_cv", "score_oracle")}
    ranks = {k: np.argsort(np.argsort(v)) for k, v in scores.items()}
    scores["combined_rank"] = list(np.mean([ranks["score_mutual_info"], ranks["score_vol_cv"], ranks["score_oracle"]], 0))
    # Stratified by split (review ML-11/STAT-07): pooled AUROC partly re-measures OOD membership.
    strata = {"pooled": [True] * len(ev), "id_only": [not o for o in is_ood], "ood_only": list(is_ood)}
    R["failure_detection"] = {"n": len(ev), "n_fail": int(np.sum(fail)),
                              "n_fail_by_stratum": {k: int(np.sum(np.array(fail)[np.array(m)])) for k, m in strata.items()},
                              "definition": f"|vol err|>{FAIL_VOL} or graft Dice<{FAIL_DICE}",
                              "auroc": {k: {st: {"failure": auroc(np.array(v)[np.array(m)], np.array(fail)[np.array(m)]),
                                                 "ci95": boot_auroc(np.array(v)[np.array(m)], np.array(fail)[np.array(m)])}
                                            for st, m in strata.items()} | {"ood_membership": auroc(v, is_ood)}
                                        for k, v in scores.items()},
                              "note": "materials cluster within splits; bootstrap resamples scans, not materials"}
    # Q5 conformal
    cal = [r for r in rows if r["split"] == "cal"]
    nc = sorted(abs(r["V_ens"] - r["graft_true_vox"]) / (r["V_sd"] + 0.02 * r["V_ens"] + 1.0) for r in cal)
    alpha = 0.1
    k = int(np.ceil((len(nc) + 1) * (1 - alpha))) - 1
    q = nc[min(k, len(nc) - 1)]
    from scipy.stats import beta as _beta

    def _q(cal_rows):
        sc = sorted(abs(r["V_ens"] - r["graft_true_vox"]) / (r["V_sd"] + 0.02 * r["V_ens"] + 1.0) for r in cal_rows)
        kk = int(np.ceil((len(sc) + 1) * (1 - alpha))) - 1
        return sc[min(kk, len(sc) - 1)] if sc else float("nan")

    def cover(rr, qq=None):
        qq = q if qq is None else qq
        if not rr:
            return None
        hits = [abs(r["V_ens"] - r["graft_true_vox"]) <= qq * (r["V_sd"] + 0.02 * r["V_ens"] + 1.0) for r in rr]
        widths = [2 * qq * (r["V_sd"] + 0.02 * r["V_ens"] + 1.0) / max(r["V_ens"], 1.0) for r in rr]
        k_, n_ = int(np.sum(hits)), len(hits)
        lo = float(_beta.ppf(0.025, k_, n_ - k_ + 1)) if k_ > 0 else 0.0           # Clopper–Pearson 95%
        hi = float(_beta.ppf(0.975, k_ + 1, n_ - k_)) if k_ < n_ else 1.0
        return {"n": n_, "coverage": k_ / n_, "coverage_ci95": [lo, hi], "q": float(qq),
                "median_rel_width": float(np.median(widths))}
    test, ood = [r for r in rows if r["split"] == "test"], [r for r in rows if r["split"] == "ood_mat"]
    # gate: abstain where the combined failure score is in the top tercile of the CAL distribution
    cal_mi = np.array([r["score_mutual_info"] for r in cal]); cal_cv = np.array([r["score_vol_cv"] for r in cal])
    gate = lambda r: r["score_mutual_info"] <= np.percentile(cal_mi, 90) and r["score_vol_cv"] <= np.percentile(cal_cv, 90)
    q_g = _q([r for r in cal if gate(r)])     # recalibrated on the gated calibration subset (review ML-12)
    R["conformal"] = {"alpha": alpha, "q": float(q), "n_cal": len(cal), "test_id": cover(test), "ood": cover(ood),
                      "q_gated": float(q_g), "n_cal_gated": int(sum(gate(r) for r in cal)),
                      "test_id_gated": cover([r for r in test if gate(r)], q_g), "ood_gated": cover([r for r in ood if gate(r)], q_g),
                      "gate": "keep scans with MI and volume-CV ≤ 90th percentile of calibration scans",
                      "ood_retained_fraction": float(np.mean([gate(r) for r in ood])),
                      "test_retained_fraction": float(np.mean([gate(r) for r in test]))}
    R["seconds"] = time.time() - t0
    save_result("exp_U1_ensemble_conformal", R)
    print({k: v for k, v in R.items() if k not in ("rows",)})


if __name__ == "__main__":
    main()
