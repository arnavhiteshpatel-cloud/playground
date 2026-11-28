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


def _supported_bundle():
    """Bundle exercising the honesty features: refused values print as 'n/m' with the reason, conditional values are
    marked, analysis parameters and the advisor version are listed, exceptions and a reference-group comparison."""
    eps = EPS + [("class_volumes.residual_graft_fraction", "Residual graft fraction", "fraction"),
                 ("class_volumes.mineral_volume_mm3", "Total mineral volume", "mm³")]
    ms_ok = {"residual_graft_volume": {"status": "supported"}, "graft_fraction_of_defect": {"status": "supported"},
             "new_bone_volume": {"status": "not_supported", "reason": "ambiguous graft rim exceeds 10% of new bone"},
             "new_bone_fraction_of_defect": {"status": "not_supported", "reason": "ambiguous graft rim"},
             "total_mineral_volume": {"status": "supported_with_conditions", "reason": "",
                                      "conditions": ["graft has no mineral phase"]},
             "mineral_fraction_of_defect": {"status": "supported"}}
    specs = []
    # refused new-bone values get magnitudes no supported endpoint produces (≈7 mm³, fraction ≈0.93), so the leak
    # check below cannot collide with a supported number or a confidence limit
    for i, (g, nb, gf, mv) in enumerate([("Ctrl", 7.2137, 0.10, 1.0), ("Ctrl", 7.3141, 0.12, 1.1),
                                          ("Ctrl", 7.2718, 0.11, 1.2), ("Tx", 7.5413, 0.08, 1.5),
                                          ("Tx", 7.6029, 0.07, 1.6), ("Tx", 7.5557, 0.09, 1.4)]):
        specs.append({"specimen_id": f"S{i}", "animal_id": f"S{i}", "group": g, "timepoint": "Week 4",
                      "qc": {"verdict": "pass"},
                      "metrics": {"class_volumes": {"new_bone_volume_mm3": nb, "new_bone_fraction": nb / 8,
                                                    "residual_graft_fraction": gf, "mineral_volume_mm3": mv}},
                      "measurement_support": ms_ok, "advisor_version": "1.4.2",
                      "segmentation": {"model_provenance": ["synthetic"]},
                      "analysis_parameters": {"method": "advisor_threshold", "t_mineral": 410.0, "t_graft": 1530.0,
                                              "estimated_graft_share": 0.31, "healing_weeks": 4.0,
                                              "healing_weeks_source": "timepoint label"},
                      "truth": {"new_bone_fraction": 0.25, "graft_fraction": gf},
                      "eval": {"dice_new": 0.8, "dice_graft": 0.9}})
    return {"title": "Support test", "study": {"name": "Support test"}, "data_class": "synthetic",
            "review_status": "unreviewed_automated", "specimens": specs, "endpoints": eps, "reference_group": "Ctrl",
            "summary_text": "Six synthetic specimens.",
            "exceptions": [{"specimen_id": "S9", "stage": "import", "reason": "corrupt file", "action": "re-export"}],
            "signature_note": "Signed copy: approvals recorded in the audit trail."}


def test_report_prints_refused_values_as_not_measured_with_reasons(tmp_path):
    r = build_pdf(_supported_bundle(), tmp_path / "s.pdf", tmp_path / "s.csv", watermark="EVALUATION COPY")
    text = _pdf_text(r["pdf"])
    assert "n/m" in text                                         # refused new-bone values are never printed as numbers
    assert "ambiguous graft rim exceeds 10% of new bone" in text and "not measured" in text
    assert text.count("ambiguous graft rim exceeds 10% of new bone") == 1 and "all 6" in text   # grouped (C3-PRD-17)
    assert "conditional" in text and "graft has no mineral phase" in text
    assert "SYNTHETIC-TRAINED MODEL" in text and "EVALUATION COPY" in text
    assert "advisor_threshold" in text and "1.4.2" in text and "timepoint label" in text
    assert "corrupt file" in text and "re-export" in text
    assert "Signed copy: approvals recorded in the audit trail." in text
    assert "Six synthetic specimens." in text and "meas / true" in text
    for s in _supported_bundle()["specimens"]:                  # no refused new-bone value leaks into the PDF
        cv = s["metrics"]["class_volumes"]
        for v in (cv["new_bone_volume_mm3"], cv["new_bone_fraction"]):
            assert f"{v:.3f}" not in text and f"{v:.4f}" not in text
    csv = (tmp_path / "s.csv").read_text()
    assert "not_supported" in csv


def test_report_without_groups_and_legacy_specimen_without_support(tmp_path):
    b = _bundle()
    for s in b["specimens"]:
        s["group"] = None
    b["specimens"][0]["analysis_parameters"] = {"method": "multiotsu"}
    text = _pdf_text(build_pdf(b, tmp_path / "n.pdf")["pdf"])
    assert "No group statistics: no specimen is assigned to a group." in text


def test_renderer_enforces_refusal_in_group_stats_and_csv(tmp_path):
    """C3-PRD-07: even when a caller passes raw numbers for refused endpoints, no group mean, CI or p-value is
    computed from them and the CSV cell is empty; C3-PRD-08: a flagged value is exported as 'flagged' and marked."""
    import csv as _csv
    b = _supported_bundle()
    table, comps = group_stats(b)
    for row in table:
        assert row["class_volumes.new_bone_volume_mm3"].get("n", 0) == 0
    assert not [c for c in comps if c["endpoint"].startswith("class_volumes.new_bone")]
    b["specimens"][0]["metric_status"] = {"class_volumes.residual_graft_fraction": {"status": "flagged",
                                                                                 "reasons": ["QC verdict review"]}}
    r = build_pdf(b, tmp_path / "g.pdf", tmp_path / "g.csv")
    rows = list(_csv.DictReader(x for x in open(r["csv"]) if not x.startswith("#")))
    assert all(x["class_volumes.new_bone_volume_mm3"] == "" for x in rows)
    assert rows[0]["class_volumes.residual_graft_fraction__support"] == "flagged"
    text = _pdf_text(r["pdf"])
    assert "(f)" in text and "7.267" not in text and "7.567" not in text


def test_group_statistics_count_conditional_values(tmp_path):
    """C3-SCI-11: a group statistic that includes conditional or flagged values says how many."""
    b = _supported_bundle()
    table, _ = group_stats(b)
    ctrl = next(r for r in table if r["group"] == "Ctrl")
    assert ctrl["class_volumes.mineral_volume_mm3"]["n_conditional"] == 3       # total mineral is conditional
    assert ctrl["class_volumes.residual_graft_fraction"]["n_conditional"] == 0
    text = _pdf_text(build_pdf(b, tmp_path / "c.pdf")["pdf"])
    import re
    assert re.search(r"incl\.\s*3\s*c/f", text)

