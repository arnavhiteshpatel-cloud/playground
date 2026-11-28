"""Shared helpers for experiment scripts."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import os  # noqa: E402
RESULTS = Path(os.environ["OQ_RESULTS"]) if os.environ.get("OQ_RESULTS") else ROOT / "experiments" / "results"
FIG = RESULTS / "figures"
SYNTH = ROOT / "data" / "processed" / "synth"
RESULTS.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

from osteoquant.ml.train import Case  # noqa: E402


def load_split(split: str, limit: int | None = None, materials=None) -> list[Case]:
    cases = []
    for f in sorted((SYNTH / split).glob("*.npz")):
        meta = json.loads(f.with_suffix(".json").read_text())
        if materials and meta["spec"]["material"] not in materials:
            continue
        d = np.load(f)
        cases.append(Case(f.stem, d["image"], d["labels"], d["roi"], (meta["voxel_um"],) * 3,
                          "synthetic", "allowed", meta))
        if limit and len(cases) >= limit:
            break
    return cases


def save_result(name: str, obj: dict):
    obj = dict(obj)
    obj.setdefault("saved", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    # provenance (cycle-3 review, C2-SCI-22): the commit the result was produced from, and whether the code was dirty
    try:
        import subprocess
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain", "--", "osteoquant", "experiments/*.py"],
                                    capture_output=True, text=True, cwd=ROOT).stdout.strip())
        obj.setdefault("git_commit", head + ("-dirty" if dirty else ""))
    except Exception:  # noqa: BLE001 - provenance is best effort
        pass
    p = RESULTS / f"{name}.json"
    p.write_text(json.dumps(obj, indent=1, default=_default))
    return p


def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def mean_ci(x):
    from osteoquant.stats import describe
    d = describe(x)
    return {"mean": d.get("mean"), "ci95": [d.get("ci95_low"), d.get("ci95_high")], "n": d.get("n"),
            "sd": d.get("sd")}
