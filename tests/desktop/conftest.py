"""Fixtures for desktop tests. All GUI tests run off-screen (QT_QPA_PLATFORM=offscreen)."""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np  # noqa: E402
import pytest  # noqa: E402

PW = "Correct-Horse-9"


@pytest.fixture(scope="session")
def phantom_file(tmp_path_factory):
    from osteoquant.desktop.demo import write_phantom
    d = tmp_path_factory.mktemp("phantom")
    return write_phantom(d / "ph.nii.gz", shape=(40, 56, 56), diameter_um=1400.0)


@pytest.fixture
def project(tmp_path):
    from osteoquant.desktop.project import Project
    p = Project.create(tmp_path / "proj", "Test project", "admin", PW, "Admin User")
    yield p
    p.close()


@pytest.fixture
def study(project):
    return project.create_study("S1", "rabbit", "condyle", "beta-TCP")


@pytest.fixture
def analysed(project, study, phantom_file):
    """Project with one imported and analysed phantom scan: (project, study_id, scan_id)."""
    from osteoquant.desktop import services as S
    o = S.import_scan(project, S.ImportRequest(str(phantom_file), (40, 40, 40), True, study))
    assert o.scan_id, o.reason
    r = S.analyze_scan(project, o.scan_id, {"defect_model": "condyle", "nominal_diameter_um": 1400,
                                            "material": "beta_tcp"})
    assert r["status"] == "complete_unreviewed", r
    return project, study, o.scan_id


@pytest.fixture
def labels():
    rng = np.random.default_rng(0)
    lab = np.zeros((20, 30, 40), np.uint8)
    lab[5:15, 10:20, 10:30] = 1
    lab[8:12, 12:16, 15:20] = 2
    lab[:, :3] = 3
    lab[rng.random(lab.shape) < 0.01] = 255
    return lab


from desktop_helpers import DIR_PW, REV_PW  # noqa: E402


@pytest.fixture
def window(qtbot, tmp_path):
    """Off-screen main window (modules may override this fixture)."""
    from PySide6.QtCore import QSettings
    from PySide6.QtWidgets import QApplication
    from osteoquant.desktop import theme
    from osteoquant.desktop.main_window import MainWindow
    from osteoquant.desktop.settings import AppSettings
    from osteoquant.licensing import evaluation_status
    theme.apply_theme(QApplication.instance(), "light")
    w = MainWindow(AppSettings(QSettings(str(tmp_path / "s.ini"), QSettings.IniFormat)), evaluation_status())
    qtbot.addWidget(w)
    w.resize(1300, 850)
    w.show()
    yield w
    w.jobs.wait()


@pytest.fixture
def team(analysed):
    """The analysed project plus a reviewer and a study director: (project, sid, scan, reviewer_id, director_id)."""
    project, sid, scan = analysed
    rid = project.add_user("rev", "Rita Reviewer", "reviewer", REV_PW)
    did = project.add_user("dir", "Dora Director", "study_director", DIR_PW)
    return project, sid, scan, rid, did
