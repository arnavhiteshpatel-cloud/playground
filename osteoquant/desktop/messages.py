"""Human-readable error messages.

Exceptions are shown to people as a plain sentence; the technical text (exception class, file
paths, library messages) stays available under "Details". ``friendly(text)`` takes the
``"ExceptionClass: message"`` strings that jobs and services produce.
"""
from __future__ import annotations

import re

# (pattern on the technical text, plain sentence). First match wins.
_RULES = [
    (r"lacks permission 'write'", "Your role cannot change data (import, analyse, edit or define ROIs). "
                                  "Ask an analyst or administrator."),
    (r"lacks permission 'review'", "Your role cannot sign reviews. Reviewer, study director or administrator "
                                   "role required."),
    (r"lacks permission 'manage_users'", "Only an administrator can manage user accounts."),
    (r"lacks permission '(\w+)'", "Your role is not allowed to do this ({0})."),
    (r"Separation of duties", None),                      # already a sentence: keep the message itself
    (r"Re-authentication failed", "The password is incorrect. After 5 failed attempts the account is locked "
                                  "for 15 minutes."),
    (r"Duplicate of scan", "This volume was already imported into the project (identical content)."),
    (r"no analysed scans", "This study has no analysed scans yet. Run the analysis first, then generate the report."),
    (r"not a gzip file|ImageFileError|CorruptInput|Could not read|truncated|cannot identify|Unreadable",
     "The file could not be read. It may be damaged, incomplete or not a supported volume format."),
    (r"not a supported volume|No reader|Unknown format|unsupported format", "This is not a supported volume format."),
    (r"Voxel spacing", None),
    (r"(MemoryError|Unable to allocate|ArrayMemoryError)", "There is not enough memory for this operation. Close "
                                                           "other scans or applications and try again."),
    (r"No space left on device", "The disk is full. Free some space and try again."),
    (r"Permission denied", "The file or folder cannot be written (no permission). Choose another location."),
    (r"needs_manual_roi|ROI not detected", "The defect could not be found automatically. Define a manual ROI "
                                           "(Study > Define cylindrical ROI at crosshair) and run the analysis again."),
    (r"cancelled", "The job was cancelled."),
]

_PREFIX = re.compile(r"^(?:[A-Z][A-Za-z]*(?:Error|Exception|Cancelled|Input)|KeyError|ValueError|OSError|RuntimeError)"
                     r":\s*")


def strip_exception_prefix(text: str) -> str:
    t = str(text or "").strip()
    while True:
        n = _PREFIX.sub("", t, count=1)
        if n == t:
            return t
        t = n


def friendly(text) -> str:
    """Plain-language sentence for a technical error text (or exception)."""
    if isinstance(text, BaseException):
        text = f"{type(text).__name__}: {text}"
    raw = str(text or "")
    for pat, msg in _RULES:
        m = re.search(pat, raw, flags=re.IGNORECASE)
        if m:
            if msg is None:
                return _sentence(strip_exception_prefix(raw[m.start():] if pat.startswith("Separation") else raw))
            return msg.format(*m.groups()) if m.groups() else msg
    return _sentence(strip_exception_prefix(raw)) or "An unexpected error occurred."


def _sentence(t: str) -> str:
    t = t.strip().strip("'\"")
    if not t:
        return ""
    t = t[0].upper() + t[1:]
    return t if t.endswith((".", "!", "?")) else t + "."


def show_error(parent, title: str, technical, icon=None):
    """Message box with the plain sentence and the technical text under "Show Details"."""
    from PySide6.QtWidgets import QMessageBox
    box = QMessageBox(icon or QMessageBox.Warning, title, friendly(technical), parent=parent)
    tech = technical if isinstance(technical, str) else f"{type(technical).__name__}: {technical}"
    if tech and tech.strip() != box.text().strip():
        box.setDetailedText(tech)
    box.setAttribute(__import__("PySide6.QtCore", fromlist=["Qt"]).Qt.WA_DeleteOnClose)
    box.open()
    return box
