"""Machine-readable graft-material knowledge (data in ``materials.json``).

``load_materials()`` returns ``{material_id: entry}``. It has no side effects and uses only
``json`` and ``pathlib``. ``validate_materials()`` checks the file against the schema below and
returns a list of problems (empty list = valid); it never raises on content problems.
"""
from __future__ import annotations

import json
from pathlib import Path

_PATH = Path(__file__).with_name("materials.json")

REQUIRED_ENTRY_KEYS = (
    "id", "name", "aliases", "composition", "theoretical_density_g_cm3", "typical_porosity",
    "typical_granule_size_um", "ha_equivalent_mgHA_cm3", "resorption", "separability_intensity_only",
    "recommended_measurement_strategy", "endpoints", "references", "evidence_level", "advisor_profile",
)
ADVISOR_KEYS = ("rel_mean", "rel_sd", "struct_um", "morphology", "radiolucent", "bone_derived",
                "evidence", "source")
MORPHOLOGIES = ("granular", "strut", "trabecular_like", "paste", "membrane", "solid", "metal")
RATINGS = ("good", "partial", "poor", "unknown")
RADIOLUCENT_REL = 0.15


def _read(path: Path | None = None) -> dict:
    return json.loads((path or _PATH).read_text(encoding="utf-8"))


def load_materials(path: str | Path | None = None) -> dict[str, dict]:
    """Return the material entries keyed by id."""
    doc = _read(Path(path) if path else None)
    return {m["id"]: m for m in doc["materials"]}


def load_document(path: str | Path | None = None) -> dict:
    """Return the whole document (conventions, materials, unsupported_material_workflow)."""
    return _read(Path(path) if path else None)


def validate_materials(path: str | Path | None = None, bib_keys: set[str] | None = None) -> list[str]:
    """Schema check. ``bib_keys`` (optional) are the keys of docs/science/references.bib; when given,
    every reference key used in the file must be one of them."""
    problems: list[str] = []
    try:
        doc = _read(Path(path) if path else None)
    except (OSError, ValueError) as exc:
        return [f"cannot read materials file: {exc}"]
    for k in ("schema_version", "materials", "unsupported_material_workflow"):
        if k not in doc:
            problems.append(f"missing top-level key '{k}'")
    seen: set[str] = set()
    for i, m in enumerate(doc.get("materials", [])):
        mid = m.get("id", f"#{i}")
        if mid in seen:
            problems.append(f"{mid}: duplicate id")
        seen.add(mid)
        for k in REQUIRED_ENTRY_KEYS:
            if k not in m:
                problems.append(f"{mid}: missing '{k}'")
        ap = m.get("advisor_profile", {})
        if set(ap) != set(ADVISOR_KEYS):
            problems.append(f"{mid}: advisor_profile keys {sorted(ap)} != {sorted(ADVISOR_KEYS)}")
        else:
            if not isinstance(ap["rel_mean"], (int, float)) or not isinstance(ap["rel_sd"], (int, float)):
                problems.append(f"{mid}: rel_mean/rel_sd must be numbers")
            elif ap["radiolucent"] != (ap["rel_mean"] < RADIOLUCENT_REL):
                problems.append(f"{mid}: radiolucent flag inconsistent with rel_mean")
            if ap["morphology"] not in MORPHOLOGIES:
                problems.append(f"{mid}: morphology '{ap['morphology']}' not in {MORPHOLOGIES}")
            if not isinstance(ap["struct_um"], (int, float)) or ap["struct_um"] <= 0:
                problems.append(f"{mid}: struct_um must be a positive number")
            if not isinstance(ap["bone_derived"], bool) or not isinstance(ap["radiolucent"], bool):
                problems.append(f"{mid}: bone_derived/radiolucent must be booleans")
        sep = m.get("separability_intensity_only", {})
        if sep.get("rating") not in RATINGS:
            problems.append(f"{mid}: separability rating '{sep.get('rating')}' not in {RATINGS}")
        if bib_keys is not None:
            for key in _collect_refs(m):
                if key not in bib_keys:
                    problems.append(f"{mid}: reference '{key}' not in references.bib")
    if bib_keys is not None:
        for key in doc.get("unsupported_material_workflow", {}).get("references", []):
            if key not in bib_keys:
                problems.append(f"workflow: reference '{key}' not in references.bib")
    return problems


def _collect_refs(obj) -> set[str]:
    out: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("references", "source") and isinstance(v, list):
                out.update(x for x in v if isinstance(x, str))
            else:
                out |= _collect_refs(v)
    elif isinstance(obj, list):
        for v in obj:
            out |= _collect_refs(v)
    return out


def bib_keys_from_file(path: str | Path) -> set[str]:
    """Parse entry keys from a BibTeX file (``@type{key,``)."""
    keys = set()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("@") and "{" in s:
            keys.add(s.split("{", 1)[1].rstrip(",").strip())
    return keys


__all__ = ["load_materials", "load_document", "validate_materials", "bib_keys_from_file"]
