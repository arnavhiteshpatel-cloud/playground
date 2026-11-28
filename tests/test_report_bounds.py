"""Report confidence limits respect the physical range of each endpoint (review CRO-11, C2-BIZ-06) and the report
labels the data class it was given (QA-REG-15, C2-BIZ-05)."""
import math

import pytest

from osteoquant.report.defectfill import (BANNERS, bounded_describe, build_pdf, endpoint_bounds, group_stats,
                                          unassigned_specimens)

EPS = [("class_volumes.new_bone_volume_mm3", "New bone volume", "mm³"),
       ("class_volumes.new_bone_fraction", "New bone BV/TV", "fraction")]


def _spec(i, group, vol, frac):
    return {"specimen_id": f"A{i}", "animal_id": f"A{i}", "group": group, "timepoint": "Week 4",
            "metrics": {"class_volumes": {"new_bone_volume_mm3": vol, "new_bone_fraction": frac}}}


def test_endpoint_bounds():
    assert endpoint_bounds("class_volumes.new_bone_fraction", "fraction") == (0.0, 1.0)
    assert endpoint_bounds("bridging_new_bone.projected_coverage", None) == (0.0, 1.0)
    lo, hi = endpoint_bounds("class_volumes.TV_mm3", "mm³")
    assert lo == 0.0 and math.isinf(hi)


def test_negative_volume_lower_limit_is_clipped_and_flagged():
    vals = [0.05, 0.1, 2.9]                       # skewed, small n: the t-interval goes below 0
    d = bounded_describe(vals, "class_volumes.new_bone_volume_mm3", "mm³")
    assert d["ci95_low_unclipped"] < 0
    assert d["ci95_low"] == 0.0 and d["ci95_clipped"] == ["low"]
    assert d["ci95_high"] > d["mean"]


def test_fraction_upper_limit_is_clipped():
    d = bounded_describe([0.97, 0.99, 0.5], "class_volumes.new_bone_fraction", "fraction")
    assert d["ci95_high"] == 1.0 and "high" in d["ci95_clipped"]
    assert 0.0 <= d["ci95_low"] <= d["ci95_high"] <= 1.0


def test_interval_inside_range_is_unchanged():
    d = bounded_describe([1.0, 1.1, 1.2, 0.9], "class_volumes.new_bone_volume_mm3", "mm³")
    assert "ci95_clipped" not in d and d["ci95_low"] > 0


def test_ci_withheld_for_n2():
    d = bounded_describe([0.1, 2.0], "class_volumes.new_bone_volume_mm3", "mm³")
    assert d.get("ci_withheld") and "ci95_low" not in d and d["n"] == 2


def _bundle(data_class="synthetic"):
    specs = [_spec(1, "Ctrl", 0.05, 0.1), _spec(2, "Ctrl", 0.1, 0.12), _spec(3, "Ctrl", 2.9, 0.4),
             _spec(4, None, 1.0, 0.2)]
    return {"title": "Bounds test", "study": {"name": "Bounds test"}, "data_class": data_class,
            "review_status": "unreviewed_automated", "specimens": specs, "endpoints": EPS}


def test_group_stats_never_negative_and_excludes_unassigned():
    table, _ = group_stats(_bundle())
    assert [r["group"] for r in table] == ["Ctrl"]           # the unassigned specimen is not a group "None"
    for r in table:
        for key, _, unit in EPS:
            d = r[key]
            if "ci95_low" in d:
                lo, hi = endpoint_bounds(key, unit)
                assert lo <= d["ci95_low"] <= d["ci95_high"] <= hi
    assert unassigned_specimens(_bundle()) == ["A4"]


def _pdf_text(path) -> str:
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(path))
    return "\n".join(doc[i].get_textpage().get_text_range() for i in range(len(doc)))


@pytest.mark.parametrize("data_class, banner_word", [("synthetic", "SYNTHETIC DATA"), ("research", "RESEARCH DATA"),
                                                      ("customer", "CUSTOMER DATA")])
def test_pdf_banner_and_bounds(tmp_path, data_class, banner_word):
    r = build_pdf(_bundle(data_class), tmp_path / "r.pdf", tmp_path / "r.csv")
    text = _pdf_text(r["pdf"])
    assert banner_word in text
    for other in {"SYNTHETIC DATA", "RESEARCH DATA", "CUSTOMER DATA"} - {banner_word}:
        assert other not in text
    assert "[-" not in text                                   # no negative confidence limit is printed
    assert "†" in text and "clipped" in text
    assert "Research use only" in text and "Customer approver" in text
    assert "Study director" not in text


def test_banners_cover_every_data_class():
    from osteoquant.api.bundle import DATA_CLASSES
    assert set(DATA_CLASSES) <= set(BANNERS)


def test_group_stats_ignore_refused_values_and_uncomputable_tests():
    from osteoquant.report.defectfill import group_stats
    eps = [("class_volumes.new_bone_volume_mm3", "New bone", "mm3"), ("class_volumes.mineral_volume_mm3", "Mineral", "mm3")]

    def spec(i, g, nb, mn):
        return {"specimen_id": f"A{i}", "animal_id": f"A{i}", "group": g, "timepoint": "w4",
                "metrics": {"class_volumes": {"new_bone_volume_mm3": nb, "mineral_volume_mm3": mn}}}
    specs = [spec(1, "ctrl", None, 1.0), spec(2, "ctrl", None, 1.2), spec(3, "ctrl", None, 1.1),
             spec(4, "trt", 0.5, 2.0), spec(5, "trt", None, 2.2), spec(6, "trt", 0.6, 2.1)]
    table, comps = group_stats({"endpoints": eps, "specimens": specs, "reference_group": "ctrl"})
    trt = next(r for r in table if r["group"] == "trt")
    assert trt["n"] == 3 and trt["class_volumes.new_bone_volume_mm3"]["n"] == 2
    # new-bone comparison is impossible (reference has no measured values): no test, no p = 1.000
    assert all(c["endpoint"] != "class_volumes.new_bone_volume_mm3" for c in comps)
    mineral = [c for c in comps if c["endpoint"] == "class_volumes.mineral_volume_mm3"]
    assert mineral and mineral[0]["p_holm"] is not None and mineral[0]["n_reference"] == 3
