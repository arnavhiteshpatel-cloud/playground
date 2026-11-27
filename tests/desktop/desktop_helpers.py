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
