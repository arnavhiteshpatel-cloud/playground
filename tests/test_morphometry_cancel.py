"""Long morphometry loops stop when the analysis is cancelled (cycle-3 review C3-PRD-20)."""
import numpy as np
import pytest

from osteoquant.morphometry.core import CANCEL_CHECK, local_thickness
from osteoquant.pipeline import analyze
from osteoquant.volume import Volume


class Stop(Exception):
    pass


def _balls():
    z, y, x = np.mgrid[:40, :40, :40]
    m = np.zeros((40, 40, 40), bool)
    for cz, cy, cx, r in ((10, 10, 10, 6), (28, 28, 28, 9), (12, 28, 20, 4)):
        m |= (z - cz) ** 2 + (y - cy) ** 2 + (x - cx) ** 2 <= r * r
    return m


def test_local_thickness_checks_for_cancellation_inside_its_loop():
    calls = []

    def check():
        calls.append(1)
        if len(calls) > 2:
            raise Stop()
    token = CANCEL_CHECK.set(check)
    try:
        with pytest.raises(Stop):
            local_thickness(_balls(), 10.0)
    finally:
        CANCEL_CHECK.reset(token)
    assert len(calls) == 3
    assert local_thickness(_balls(), 10.0).max() > 0          # no check set: unaffected


def test_analyze_passes_check_and_restores_it(rng):
    img = (rng.normal(0, 30, (32, 32, 32)) + 600 * _balls()[:32, :32, :32]).astype(np.float32)
    vol = Volume(img, (20.0, 20.0, 20.0))

    def check():
        raise Stop()
    roi = {"kind": "box", "params": {"min_um": [0, 0, 0], "max_um": [1e9, 1e9, 1e9]}}
    with pytest.raises(Stop):
        analyze(vol, {"qc": False, "segmentation": "ctan_style", "t_mineral": 0.5, "t_graft": 1.5,
                      "measurement_support": False}, roi_dict=roi, check=check)
    assert CANCEL_CHECK.get() is None
