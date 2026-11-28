#!/usr/bin/env python3
"""Regenerate the Generation-2 sample DefectFill reports through the desktop code path (SYNTHETIC data only).

Each sample is a fresh desktop project in a temporary folder: synthetic condyle phantoms are written, imported through
the import wizard model, analysed with the desktop defaults (segmentation ``advisor_threshold``, the only method that
carries measurement support) and reported with ``services.generate_report``. The PDF and CSV are exported to
``reports_samples/``. Nothing here uses customer or real data; every report carries the SYNTHETIC DATA banner.

    python3 scripts/make_gen2_sample_reports.py          # writes reports_samples/DefectFill_SAMPLE4_*, _SAMPLE5_*

Sample 4: beta-TCP at week 4 — the advisor refuses graft/new-bone endpoints (knowledge base and physics model
disagree for beta-TCP, so a measured material reference would be needed).
Sample 5: sintered HA at week 8 — dense ceramic; the advisor decides per scan.
The file names state the material only; what is supported is whatever the shipped advisor decides.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MPLBACKEND", "Agg")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from osteoquant.advisor.separability import ADVISOR_VERSION  # noqa: E402
from osteoquant.desktop import services as S  # noqa: E402
from osteoquant.desktop.demo import DEMO_PASSWORD, write_phantom  # noqa: E402
from osteoquant.desktop.import_wizard import ImportModel  # noqa: E402
from osteoquant.desktop.project import Project  # noqa: E402

OUT = ROOT / "reports_samples"
SAMPLES = [
    {"tag": "SAMPLE4_gen2_synthetic_betatcp", "material": "beta_tcp", "label": "beta-TCP", "week": 4, "prefix": "T"},
    {"tag": "SAMPLE5_gen2_synthetic_ha", "material": "ha", "label": "HA", "week": 8, "prefix": "H"},
]
N_ANIMALS = 6
WATERMARK = "SAMPLE - SYNTHETIC DATA - NOT FOR STUDY DECISIONS"


def _clean_tree() -> bool:
    """Samples must be traceable to a commit (cycle-3 review C3-BIZ-16): the code under osteoquant/ must be committed."""
    import subprocess
    r = subprocess.run(["git", "status", "--porcelain", "--", "osteoquant"], capture_output=True, text=True, cwd=ROOT)
    return r.returncode == 0 and not r.stdout.strip()
SHAPE = (48, 72, 72)


def build(sample: dict, work: Path) -> list[str]:
    src = work / f"{sample['tag']}_sources"
    src.mkdir(parents=True)
    p = Project.create(work / sample["tag"], f"Synthetic condyle study ({sample['label']})", "analyst",
                       DEMO_PASSWORD, "A. Analyst")
    try:
        sid = p.create_study(f"Condyle defect, {sample['label']} (synthetic phantoms)", "rabbit", "condyle",
                             sample["label"], data_class="synthetic")
        groups = [p.store.add_group(p.user, sid, f"Control ({sample['label']})"),
                  p.store.add_group(p.user, sid, f"Treatment ({sample['label']} + additive)")]
        m = ImportModel(p, sid)
        for i in range(N_ANIMALS):
            stage = 0.35 + 0.15 * (i % 3) + (0.1 if i % 2 else 0.0)      # treatment heals a little further
            f = write_phantom(src / f"{sample['prefix']}{i + 1:02d}.nii.gz", seed=200 + i, shape=SHAPE,
                              stage=stage, diameter_um=1600.0, material=sample["material"])
            c = m.add_path(f)[0]
            c.animal_id = f"{sample['prefix']}{i + 1:02d}"
            c.group_id = groups[i % 2]
            c.timepoint, c.days = f"Week {sample['week']}", 7 * sample["week"]
        outcomes = m.run(None)
        for o in outcomes:
            if not o.scan_id:
                raise RuntimeError(f"import failed: {o.reason}")
            r = S.analyze_scan(p, o.scan_id, {"defect_model": "condyle", "nominal_diameter_um": 1600,
                                              "material": sample["material"]})
            print(sample["tag"], o.scan_id, r.get("status"))
        rep = S.generate_report(p, sid, watermark=WATERMARK)
        (work / "export").mkdir(exist_ok=True)
        files = S.export_report(p, rep["report_id"], work / "export")
        out = []
        for fpath in files:
            dest = OUT / f"DefectFill_{sample['tag']}{Path(fpath).suffix}"
            shutil.copyfile(fpath, dest)
            out.append(str(dest.relative_to(ROOT)))
        return out
    finally:
        p.close()


def main():
    if not _clean_tree() and "--allow-dirty" not in sys.argv:
        raise SystemExit("osteoquant/ has uncommitted changes: commit first so the samples name the code that made them "
                         "(or pass --allow-dirty for a local check; do not publish such samples)")
    OUT.mkdir(exist_ok=True)
    for old in ("DefectFill_SAMPLE4_gen2_synthetic_betatcp_refused", "DefectFill_SAMPLE5_gen2_synthetic_ha_supported",
                "DefectFill_SAMPLE4_gen2_synthetic_betatcp", "DefectFill_SAMPLE5_gen2_synthetic_ha"):
        for ext in (".pdf", ".csv"):
            (OUT / f"{old}{ext}").unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as td:
        for sample in SAMPLES:
            print("wrote", build(sample, Path(td)), "advisor", ADVISOR_VERSION)


if __name__ == "__main__":
    main()
