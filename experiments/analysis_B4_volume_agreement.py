#!/usr/bin/env python3
"""Benchmark B4: volume bias and 95% limits of agreement in supported regimes (SYNTHETIC).

Derived analysis of the pre-registered held-out run S1H3 (``results/exp_S1H3_heldout.json``, advisor 1.4.1 frozen);
no new simulation. For each endpoint, the signed relative volume errors of the specimens the advisor *supported* are
summarised as bias (mean), SD and Bland–Altman 95% limits of agreement (bias ± 1.96 SD). Because several specimens
share a phantom structure, a bootstrap over structures gives a 95% CI for the bias (2000 resamples, seed 0).

B4 target (BENCHMARK_SCORECARD): |bias| ≤ 5% and 95% LoA within ±15%.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RES = Path(__file__).resolve().parent / "results"
SRC = RES / "exp_S1H3_heldout.json"
EPS = {"residual_graft_volume": ("err_graft", "status"),
       "total_mineral_volume": ("err_mineral", "status_mineral"),
       "new_bone_volume": ("err_new", "status_new")}


def summarise(rows, err_key, status_key, rng):
    sup = [r for r in rows if r[status_key] in ("supported", "supported_with_conditions")]
    if not sup:
        return {"n_supported": 0}
    e = np.array([r[err_key] for r in sup], float)
    bias, sd = float(e.mean()), float(e.std(ddof=1)) if len(e) > 1 else float("nan")
    structs = sorted({r["structure"] for r in sup})
    by = {s: np.array([r[err_key] for r in sup if r["structure"] == s]) for s in structs}
    boot = []
    for _ in range(2000):
        pick = rng.choice(structs, len(structs), replace=True)
        boot.append(float(np.concatenate([by[s] for s in pick]).mean()))
    loa = (bias - 1.96 * sd, bias + 1.96 * sd)
    return {"n_supported": len(e), "n_structures": len(structs), "bias": bias, "sd": sd,
            "bias_ci95_bootstrap_structures": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
            "loa95": list(loa), "max_abs": float(np.abs(e).max()),
            "b4_met": bool(abs(bias) <= 0.05 and loa[0] >= -0.15 and loa[1] <= 0.15)}


def main():
    d = json.loads(SRC.read_text())
    rng = np.random.default_rng(0)
    out = {"experiment": "B4 from S1H3 (derived)", "source": SRC.name, "advisor_version": d["advisor_version"],
           "preregistered_source": d.get("preregistered"), "data_class": "SYNTHETIC",
           "endpoints": {ep: summarise(d["rows"], ek, sk, rng) for ep, (ek, sk) in EPS.items()}}
    (RES / "analysis_B4_volume_agreement.json").write_text(json.dumps(out, indent=1))
    for ep, s in out["endpoints"].items():
        print(ep, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()})


if __name__ == "__main__":
    main()
