"""Shared helpers for the QA test-suite (import as ``from qa_helpers import ...``)."""

PW = "Correct-Horse-9"


def make_users(st):
    """Two organisations; org A has one user per role, org B one admin. Returns {name: user dict}."""
    o1, o2 = st.create_org("LabA"), st.create_org("LabB")
    for org, n, r in [(o1, "adminA", "admin"), (o1, "anaA", "analyst"), (o1, "revA", "reviewer"),
                      (o1, "viewA", "viewer"), (o2, "adminB", "admin")]:
        st.create_user(org, n, PW, r)
    return {n: st.user_for_token(st.login(n, PW)) for n in ("adminA", "anaA", "revA", "viewA", "adminB")}
