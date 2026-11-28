"""Shared helpers for desktop tests (imported by test modules; fixtures live in conftest.py)."""
PW = "Correct-Horse-9"
REV_PW = "Reviewer-Pass-1"
DIR_PW = "Director-Pass-1"


def login_as(project, username, password):
    """A second Project handle on the same folder signed in as another user."""
    from osteoquant.desktop.project import Project
    p = Project(project.folder)
    assert p.login(username, password)
    return p


def current_assessment(endpoints, method="advisor_threshold"):
    """A measurement-support record as the current pipeline writes it (advisor version and support-rule stamps).
    Records without these stamps are treated as stale at read time (cycle-3 review C3-PRD-01)."""
    from osteoquant.advisor.integration import SUPPORT_RULES
    from osteoquant.advisor.separability import ADVISOR_VERSION
    return {"measurement_support": {"endpoints": endpoints, "advisor_version": ADVISOR_VERSION,
                                    "support_rules": SUPPORT_RULES},
            "segmentation": {"method": method}}
