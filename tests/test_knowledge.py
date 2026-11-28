"""Materials knowledge base: schema and citation integrity.

Every reference key used in ``osteoquant/knowledge/materials.json`` must exist in ``docs/science/references.bib``
(no invented citations), and the advisor profile must be internally consistent.
"""
import copy
import json
from pathlib import Path

import pytest

from osteoquant.knowledge import (bib_keys_from_file, load_document, load_materials, validate_materials)

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "docs" / "science" / "references.bib"
KB = ROOT / "osteoquant" / "knowledge" / "materials.json"


def _write(tmp_path, doc) -> Path:
    p = tmp_path / "materials.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def test_shipped_knowledge_base_is_valid_and_fully_cited():
    keys = bib_keys_from_file(BIB)
    assert len(keys) > 10
    assert validate_materials(bib_keys=keys) == []


def test_load_materials_and_document():
    mats = load_materials()
    doc = load_document()
    assert set(mats) == {m["id"] for m in doc["materials"]}
    for mid in ("ha", "beta_tcp", "bcp", "xenograft_dbbm", "allograft", "titanium"):
        assert mid in mats
    assert mats["xenograft_dbbm"]["advisor_profile"]["bone_derived"] is True
    assert mats["ha"]["advisor_profile"]["bone_derived"] is False


def test_bib_parser_reads_entry_keys(tmp_path):
    b = tmp_path / "r.bib"
    b.write_text("@article{smith2020,\n  title={x}\n}\n  @book{ jones_1999 ,\nnot an entry\n", encoding="utf-8")
    assert bib_keys_from_file(b) == {"smith2020", "jones_1999"}


def test_unknown_reference_key_is_reported(tmp_path):
    doc = load_document()
    bad = copy.deepcopy(doc)
    bad["materials"][0].setdefault("references", []).append("invented2099")
    probs = validate_materials(_write(tmp_path, bad), bib_keys=bib_keys_from_file(BIB))
    assert any("invented2099" in p and "not in references.bib" in p for p in probs)
    bad2 = copy.deepcopy(doc)
    bad2["unsupported_material_workflow"]["references"] = ["ghost2001"]
    probs = validate_materials(_write(tmp_path, bad2), bib_keys=bib_keys_from_file(BIB))
    assert any(p.startswith("workflow: reference 'ghost2001'") for p in probs)


@pytest.mark.parametrize("mutate, expect", [
    (lambda d: d.pop("schema_version"), "missing top-level key 'schema_version'"),
    (lambda d: d["materials"].append(copy.deepcopy(d["materials"][0])), "duplicate id"),
    (lambda d: d["materials"][0].pop("advisor_profile"), "advisor_profile keys"),
    (lambda d: d["materials"][0]["advisor_profile"].update(rel_mean="dense"), "rel_mean/rel_sd must be numbers"),
    (lambda d: d["materials"][0]["advisor_profile"].update(radiolucent=not d["materials"][0]["advisor_profile"]["radiolucent"]),
     "radiolucent flag inconsistent"),
    (lambda d: d["materials"][0]["advisor_profile"].update(morphology="blob"), "morphology 'blob'"),
    (lambda d: d["materials"][0]["advisor_profile"].update(struct_um=0), "struct_um must be a positive number"),
    (lambda d: d["materials"][0]["advisor_profile"].update(bone_derived="no"), "bone_derived/radiolucent must be booleans"),
    (lambda d: d["materials"][0]["separability_intensity_only"].update(rating="excellent"), "separability rating"),
])
def test_schema_violations_are_reported(tmp_path, mutate, expect):
    doc = copy.deepcopy(load_document())
    mutate(doc)
    probs = validate_materials(_write(tmp_path, doc))
    assert any(expect in p for p in probs), probs


def test_missing_required_entry_key_and_unreadable_file(tmp_path):
    doc = copy.deepcopy(load_document())
    doc["materials"][0].pop("name")
    assert any("missing 'name'" in p for p in validate_materials(_write(tmp_path, doc)))
    (tmp_path / "broken.json").write_text("{not json", encoding="utf-8")
    assert validate_materials(tmp_path / "broken.json")[0].startswith("cannot read materials file")
    assert validate_materials(tmp_path / "absent.json")[0].startswith("cannot read materials file")
