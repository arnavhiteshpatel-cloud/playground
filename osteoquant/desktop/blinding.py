"""Blinded review mode: masking of identifying information in every view.

Blinded mode replaces animal IDs, scan file names, group names and database IDs with random,
non-sequential codes stored per study in the project (``Project.blind_code``). Free text that
can carry identity (audit-trail details, report content) is masked with the functions below.
"""
from __future__ import annotations

import copy
import re

MASK = "(blinded)"
# detail keys whose values identify an animal, a source file or acquisition settings
SENSITIVE_KEYS = {"source", "source_name", "path", "paths", "files", "file", "filename", "folder", "dest",
                  "store_path", "animal_id", "acquisition", "meta", "metadata", "group", "group_name"}
SCAN_ID_KEYS = {"scan", "scan_id"}


class Masker:
    """Masks identifying strings and IDs for one project (strings are collected once)."""

    def __init__(self, project):
        self.project = project
        self.strings = project.identifying_strings()
        self._rx = (re.compile("(?<![A-Za-z0-9])(?:" + "|".join(re.escape(x) for x in self.strings) + ")(?![A-Za-z0-9])")
                    if self.strings else None)

    def text(self, s: str) -> str:
        return self._rx.sub(MASK, str(s)) if self._rx is not None else str(s)

    def object_label(self, object_type, object_id) -> str:
        if object_id in (None, ""):
            return str(object_type or "")
        try:
            oid = int(object_id)
        except (TypeError, ValueError):
            return f"{object_type} {MASK}"
        if object_type == "scan":
            return self.project.scan_code(oid)
        if object_type == "specimen":
            return self.project.animal_code(oid)
        if object_type == "group":
            return f"group {MASK}"
        return f"{object_type} {oid}"

    def value(self, v, key=None):
        if key in SENSITIVE_KEYS:
            return MASK
        if key in SCAN_ID_KEYS and isinstance(v, (int, str)) and str(v).isdigit():
            return self.project.scan_code(int(v))
        if isinstance(v, dict):
            return {k: self.value(x, k) for k, x in v.items()}
        if isinstance(v, list):
            return [self.value(x) for x in v]
        if isinstance(v, str):
            return self.text(v)
        return v

    def event(self, e: dict) -> dict:
        out = copy.deepcopy(e)
        out["details"] = self.value(out.get("details") or {})
        out["object_label"] = self.object_label(out.get("object_type"), out.get("object_id"))
        if out.get("object_type") in ("scan", "specimen", "group"):
            out["object_id"] = MASK
        return out
