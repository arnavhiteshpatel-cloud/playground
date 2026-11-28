"""Report integrity and separation of duties for report sign-off (cycle-2 review C2-PRD-04/05/06).

At generation the desktop records the SHA-256 of the exact report bundle bytes (the JSON the PDF was
rendered from) and of the PDF, both in ``desktop_report_meta`` / ``reports`` and in the hash-chained
``report.generate`` audit event. Before a report is approved, and before a signed copy is rendered,
the bundle and the PDF on disk are re-hashed and compared with both records. Any mismatch, a missing
file or a missing record fails closed: the signature or the signed copy is refused.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


class ReportIntegrityError(PermissionError):
    """The report's bundle or PDF no longer matches what was recorded at generation."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class MultipleGenerateEvents(ValueError):
    """More than one ``report.generate`` event for one report: the trail was extended after generation."""


def generate_event(store, report_id: int) -> dict | None:
    """The hash-chained ``report.generate`` audit event of a report (None if absent).

    Exactly one is written per report. A second one can only come from appending to the trail, so it is refused
    rather than letting the newest event win (cycle-3 review C3-PRD-03)."""
    evs = [e for e in store.audit.events(object_type="report", object_id=report_id, limit=10000)
           if e["action"] == "report.generate"]
    if len(evs) > 1:
        raise MultipleGenerateEvents(f"{len(evs)} report.generate events")
    return evs[0] if evs else None


def _fail(project, report_id, reason: str):
    u = project.user or {}
    try:
        project.store.audit.record("report.integrity_failed", u.get("id"), u.get("org_id"), "report", report_id,
                                   {"reason": reason})
    except Exception:  # noqa: BLE001 - the refusal must not depend on bookkeeping
        pass
    raise ReportIntegrityError(f"Report {report_id} failed its integrity check: {reason}. Nothing was signed; "
                               "generate a new report.")


def verify_report(project, report_id: int, check_pdf: bool = True) -> dict:
    """Return the verified report bundle (dict) or raise ``ReportIntegrityError``.

    Checks: the bundle SHA-256 recorded in the database equals the one in the audit trail and the
    bytes on disk; with ``check_pdf`` also the PDF on disk against ``reports.sha256`` and the audit
    trail."""
    store = project.store
    rep = store.q1("SELECT * FROM reports WHERE id=?", (report_id,))
    if not rep:
        raise KeyError("report not found")
    meta = store.q1("SELECT * FROM desktop_report_meta WHERE report_id=?", (report_id,)) or {}
    try:
        ev = generate_event(store, report_id)
    except MultipleGenerateEvents as e:
        _fail(project, report_id, f"the audit trail holds more than one generation record ({e})")
    if ev is None:
        _fail(project, report_id, "no report.generate event in the audit trail")
    if rep.get("created_by") is not None and str(ev.get("user_id")) != str(rep["created_by"]):
        _fail(project, report_id, "the generation record was not written by the report's creator")
    det = ev.get("details") or {}
    rec, aud = meta.get("bundle_sha256"), det.get("bundle_sha256")
    if not rec or not aud:
        _fail(project, report_id, "no bundle hash was recorded at generation (report made by an earlier version)")
    if rec != aud:
        _fail(project, report_id, "the bundle hash in the database differs from the audit trail")
    bp = meta.get("bundle_path")
    if not bp or not Path(bp).is_file():
        _fail(project, report_id, "the report bundle file is missing")
    data = Path(bp).read_bytes()
    if sha256_bytes(data) != rec:
        _fail(project, report_id, "the report bundle was modified after generation")
    if check_pdf:
        pdf = rep.get("pdf_path")
        if not pdf or not Path(pdf).is_file():
            _fail(project, report_id, "the report PDF is missing")
        h = sha256_bytes(Path(pdf).read_bytes())
        if h != rep.get("sha256") or h != det.get("sha256"):
            _fail(project, report_id, "the report PDF was modified after generation")
    try:
        bundle = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        _fail(project, report_id, "the report bundle is unreadable")
    return bundle


def review_status(project, report_id: int, bundle: dict) -> str | None:
    """Review status recorded at generation (database), else the verified bundle's."""
    meta = project.store.q1("SELECT review_status FROM desktop_report_meta WHERE report_id=?", (report_id,)) or {}
    return meta.get("review_status") or bundle.get("review_status")


def report_author_ids(project, bundle: dict) -> set[int]:
    """Users who authored any reported segmentation (including the versions it was derived from) or the
    ROI it was measured in. None of them may approve the report (C2-PRD-06)."""
    store = project.store
    out: set[int] = set()
    for spec in bundle.get("specimens") or []:
        sid, seen = spec.get("segmentation_id"), set()
        while sid is not None and sid not in seen:
            seen.add(sid)
            seg = store.q1("SELECT parent_id, created_by, roi_id FROM segmentations WHERE id=?", (sid,))
            if not seg:
                break
            if seg["created_by"] is not None:
                out.add(int(seg["created_by"]))
            if seg["roi_id"] is not None:
                roi = store.q1("SELECT created_by FROM rois WHERE id=?", (seg["roi_id"],))
                if roi and roi["created_by"] is not None:
                    out.add(int(roi["created_by"]))
            sid = seg["parent_id"]
        if spec.get("roi_id") is not None:
            roi = store.q1("SELECT created_by FROM rois WHERE id=?", (spec["roi_id"],))
            if roi and roi["created_by"] is not None:
                out.add(int(roi["created_by"]))
    return out


def audited_signature_roles(store, report_id: int) -> dict[int, str]:
    """review id -> signature role key, as recorded in the hash-chained audit trail."""
    out = {}
    # oldest first, first record per review wins: an appended record cannot re-label a signature (C3-PRD-03)
    for e in reversed(store.audit.events(object_type="report", object_id=report_id, limit=10000)):
        if e["action"] == "review.signature_role":
            d = e.get("details") or {}
            if d.get("review_id") is not None and d.get("signature_role_key") and int(d["review_id"]) not in out:
                out[int(d["review_id"])] = d["signature_role_key"]
    return out
