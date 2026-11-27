"""Material-specific validation records for segmentation models.

The measurement-support advisor allows a learned (texture/morphology) model to support graft/new-bone endpoints
for a material whose intensity alone is insufficient **only** when the model has validation evidence for that
material on non-synthetic data within the scan's protocol envelope (ADR-G2-04, MEASUREMENT_SUPPORT rule 6).

Records live in ``models/validation_records.json`` keyed by model name. A record is evidence, not a claim of
regulatory validation: it states what was measured, on what data, with what error.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass

from .core import MODEL_DIR

QUALIFYING_DATA_CLASSES = ("physical_phantom", "ex_vivo", "in_vivo")   # synthetic never qualifies
MAX_P95_ABS_REL_ERROR = 0.15                                           # graft-volume error bound to qualify


@dataclass
class ValidationRecord:
    model_name: str
    model_sha256: str
    material: str
    data_class: str                 # synthetic | physical_phantom | ex_vivo | in_vivo
    n_specimens: int
    voxel_um_range: tuple
    scanner_class: str              # e.g. "desktop micro-CT 50–70 kVp"
    graft_volume_abs_rel_error_p95: float
    reference_method: str           # e.g. "gravimetric fill", "blinded histomorphometry"
    evidence_location: str          # report or dataset path
    date: str = ""
    notes: str = ""

    def qualifies(self, voxel_um: float) -> tuple[bool, str]:
        if self.data_class not in QUALIFYING_DATA_CLASSES:
            return False, f"evidence class '{self.data_class}' does not qualify (synthetic evidence is never sufficient)"
        if self.n_specimens < 8:
            return False, f"only {self.n_specimens} specimens (≥8 required)"
        lo, hi = self.voxel_um_range
        if not (lo <= voxel_um <= hi):
            return False, f"voxel size {voxel_um:.1f} µm outside validated range {lo}–{hi} µm"
        if self.graft_volume_abs_rel_error_p95 > MAX_P95_ABS_REL_ERROR:
            return False, f"validated error p95 {self.graft_volume_abs_rel_error_p95:.0%} exceeds {MAX_P95_ABS_REL_ERROR:.0%}"
        return True, "qualifying validation record"


def _path():
    return MODEL_DIR / "validation_records.json"


FORMAT = "oq-validation-records-1"


def _sign(records: dict, private_key, key_id: str) -> dict:
    import base64
    from ..licensing.core import canonical_payload
    text = canonical_payload(records)
    return {"format": FORMAT, "key_id": key_id, "payload": text,
            "signature": base64.b64encode(private_key.sign(text.encode("utf-8"))).decode()}


def load_records(keys: dict | None = None) -> dict:
    """Load validation records. They are vendor evidence and must carry a valid Ed25519 signature from a key the
    application trusts (the licensing keys; test keys only when test licences are explicitly allowed). A record file
    edited or created locally — including by an administrator — is rejected (cycle-2 review: forgeable records)."""
    import base64
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from ..licensing.core import trusted_keys
    p = _path()
    if not p.exists():
        return {}
    env = json.loads(p.read_text())
    if not isinstance(env, dict) or env.get("format") != FORMAT:
        raise RuntimeError("validation_records.json is not a signed record file")
    keys = trusted_keys() if keys is None else keys
    if env.get("key_id") not in keys:
        raise RuntimeError(f"validation records signed with an untrusted key ({env.get('key_id')})")
    pub_hex, _is_test = keys[env["key_id"]]
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(
            base64.b64decode(env["signature"]), env["payload"].encode("utf-8"))
    except Exception as e:
        raise RuntimeError("validation records signature is invalid: records were modified") from e
    return json.loads(env["payload"])


def add_record(rec: ValidationRecord, private_key, key_id: str, audit=None, user_id=None, org_id=None,
               keys: dict | None = None) -> None:
    """Vendor tooling: append a record and re-sign the file with the vendor key."""
    R = load_records(keys) if _path().exists() else {}
    d = asdict(rec)
    d["date"] = d["date"] or time.strftime("%Y-%m-%d")
    R.setdefault(rec.model_name, []).append(d)
    env = _sign(R, private_key, key_id)
    _path().write_text(json.dumps(env, indent=1))
    if audit is not None:
        audit.record("model.validation_record_added", user_id, org_id, "model", rec.model_name,
                     {"material": rec.material, "data_class": rec.data_class, "key_id": key_id})


def validated_for(model_name: str, model_sha256: str, material: str, voxel_um: float,
                  keys: dict | None = None) -> tuple[bool, str]:
    """True only if a record for this exact model version (SHA-256) and material qualifies at this voxel size."""
    reasons = []
    try:
        records = load_records(keys)
    except RuntimeError as e:
        return False, str(e)
    for d in records.get(model_name, []):
        if d.get("model_sha256") != model_sha256 or d.get("material") != material:
            continue
        d = dict(d)
        d["voxel_um_range"] = tuple(d["voxel_um_range"])
        ok, why = ValidationRecord(**d).qualifies(voxel_um)
        if ok:
            return True, f"{why}: {d['data_class']}, n={d['n_specimens']}, {d['evidence_location']}"
        reasons.append(why)
    return False, "; ".join(reasons) or f"no validation record for model {model_name} and material {material}"
