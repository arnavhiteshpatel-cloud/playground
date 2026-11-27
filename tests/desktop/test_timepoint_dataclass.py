"""Cycle-2 review fixes: the desktop passes the timepoint to the measurement-support advisor (C2-BIZ-04) and
reports carry the study's data class, so synthetic/demo data are never labelled customer data (C2-BIZ-05)."""
import pytest

from osteoquant.desktop import services as S


@pytest.mark.parametrize("label, weeks", [
    ("Week 4", 4.0), ("week4", 4.0), ("W4", 4.0), ("4 weeks", 4.0), ("wk 8", 8.0), ("Day 28", 4.0), ("D14", 2.0),
    ("28 d", 4.0), ("Day 0", 0.0), ("3 months", round(3 * 30.4375 / 7, 3)),
    ("T2", None), ("Baseline", None), ("", None), (None, None), ("Week 4 / Day 28", None), ("4", None),
])
def test_parse_timepoint_weeks(label, weeks):
    assert S.parse_timepoint_weeks(label) == weeks


def test_resolve_healing_weeks_modes(analysed):
    project, sid, scan = analysed                    # imported without a timepoint
    assert S.resolve_healing_weeks(project, scan, "auto") == (None, "no timepoint assigned")
    assert S.resolve_healing_weeks(project, scan, "unknown")[0] is None
    assert S.resolve_healing_weeks(project, scan, 2) == (2.0, "entered by the user")
    with pytest.raises(ValueError):
        S.resolve_healing_weeks(project, scan, -1)


def _import_at(project, study, phantom_file, label, days):
    tp = S.get_or_create_timepoint(project, study, label, days)
    o = S.import_scan(project, S.ImportRequest(str(phantom_file), (40, 40, 40), True, study, timepoint_id=tp))
    assert o.scan_id, o.reason
    return o.scan_id


@pytest.mark.parametrize("label, days, expect", [("Week 4", None, 4.0), ("Late", 14, 2.0), ("T3", None, None)])
def test_analysis_passes_scan_timepoint_to_advisor(project, study, phantom_file, label, days, expect):
    scan = _import_at(project, study, phantom_file, label, days)
    r = S.analyze_scan(project, scan, {"defect_model": "condyle", "nominal_diameter_um": 1400, "material": "beta_tcp"})
    assert r["status"] == "complete_unreviewed", r
    m = project.store.latest_measurements(project.user, study)[0]["metrics"]
    assert m["config"].get("healing_weeks") == expect
    assert m["config"]["healing_weeks_source"]
    reasons = " ".join(str(v.get("reason")) for v in m["measurement_support"]["endpoints"].values())
    if expect is None:
        assert "timepoint: unknown" in reasons
    else:
        assert "timepoint: unknown" not in reasons


def test_explicit_weeks_override_scan_timepoint(project, study, phantom_file):
    scan = _import_at(project, study, phantom_file, "Week 12", 84)
    S.analyze_scan(project, scan, {"defect_model": "condyle", "nominal_diameter_um": 1400, "material": "beta_tcp",
                                   "healing_weeks": 3})
    m = project.store.latest_measurements(project.user, study)[0]["metrics"]
    assert m["config"]["healing_weeks"] == 3.0 and m["config"]["healing_weeks_source"] == "entered by the user"


def test_analysis_dialog_healing_weeks(qtbot):
    from osteoquant.desktop.dialogs import AnalysisDialog
    dlg = AnalysisDialog(2, "condyle")
    qtbot.addWidget(dlg)
    assert dlg.config()["healing_weeks"] == "auto" and not dlg.tp_weeks.isEnabled()
    dlg.tp_mode.setCurrentIndex(dlg.tp_mode.findData("weeks"))
    assert dlg.tp_weeks.isEnabled()
    dlg.tp_weeks.setValue(2.5)
    assert dlg.config()["healing_weeks"] == 2.5
    dlg.tp_mode.setCurrentIndex(dlg.tp_mode.findData("unknown"))
    assert dlg.config()["healing_weeks"] == "unknown"


# ------------------------------------------------------------------ data class
def test_report_data_class_mapping():
    from osteoquant.api.bundle import report_data_class
    assert report_data_class("synthetic") == "synthetic"
    assert report_data_class("demo") == "synthetic"
    assert report_data_class("research") == "research"      # was mapped to "customer" (QA-REG-15)
    assert report_data_class(None) == "research"
    assert report_data_class("customer") == "customer"
    assert report_data_class("nonsense") == "research"


def test_study_data_class_validated(project):
    with pytest.raises(ValueError):
        project.create_study("X", data_class="confidential-ish")


def test_new_study_dialog_offers_data_class(qtbot):
    from osteoquant.desktop.dialogs import NewStudyDialog
    dlg = NewStudyDialog()
    qtbot.addWidget(dlg)
    dlg.name.setText("S")
    assert dlg.values()["data_class"] == "research"
    dlg.data_class.setCurrentIndex(dlg.data_class.findData("synthetic"))
    assert dlg.values()["data_class"] == "synthetic"


def _pdf_text(path) -> str:
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(path))
    return "\n".join(doc[i].get_textpage().get_text_range() for i in range(len(doc)))


def test_synthetic_demo_report_is_labelled_synthetic(tmp_path):
    from osteoquant.desktop.demo import build_demo_project
    p, sid, _ = build_demo_project(tmp_path / "demo", n_animals=3, shape=(40, 56, 56))
    try:
        rep = S.generate_report(p, sid)
        text = _pdf_text(rep["pdf"])
        assert "SYNTHETIC DATA" in text and "CUSTOMER DATA" not in text
        assert "Research use only" in text                       # RUO line in the footer
        assert "None None" not in text
        csv_head = open(rep["csv"]).readline()
        assert csv_head.startswith("#") and "synthetic" in csv_head
        m = p.store.latest_measurements(p.user, sid)[0]["metrics"]
        assert m["config"]["healing_weeks"] == 4.0                # demo scans are "Week 4" / 28 days
    finally:
        p.close()


def test_own_research_study_is_not_labelled_customer(analysed):
    project, sid, _ = analysed
    from osteoquant.api.bundle import bundle_from_store
    b = bundle_from_store(project.store, project.user, sid)
    assert b["data_class"] == "research"
