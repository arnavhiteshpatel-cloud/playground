"""Offline licence files signed with Ed25519.

File format (UTF-8 JSON, extension ``.oqlic``)::

    {
      "format": "osteoquant-licence/1",
      "key_id": "<id of the signing key>",
      "payload": "<canonical JSON string, see below>",
      "signature": "<base64 Ed25519 signature over the UTF-8 bytes of payload>"
    }

The signature is detached from the payload: it is computed over the exact payload string, so
verification never depends on re-serialising JSON. Payload fields::

    licence_id   str           unique id chosen by the licensor
    licensee     str           organisation / person
    edition      str           academic | commercial | evaluation
    features     list[str]     feature flags (see FEATURES)
    issued       "YYYY-MM-DD"
    expiry       "YYYY-MM-DD" | null   (null = perpetual)
    machine      str | null    optional machine fingerprint (see machine_fingerprint)
    product      "osteoquant-desktop"
    test         bool          true for test licences

Without a valid licence the application runs in evaluation mode: every feature is usable and
reports carry an evaluation watermark.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import platform
import shutil
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .keys import PRODUCTION_KEYS, TEST_KEYS

FORMAT = "osteoquant-licence/1"
PRODUCT = "osteoquant-desktop"
EDITIONS = ("academic", "commercial", "evaluation")
FEATURES = ("import", "viewer", "edit", "analyze", "review", "report", "batch")
EVALUATION_WATERMARK = "EVALUATION COPY - NOT FOR STUDY DECISIONS"
TEST_WATERMARK = "TEST LICENCE - NOT A VALID PRODUCT LICENCE"
LICENCE_FILENAME = "licence.oqlic"


class LicenceError(ValueError):
    """Raised for malformed licence files or when signing input is invalid."""


@dataclass(frozen=True)
class LicenceStatus:
    state: str                      # valid | evaluation | expired | invalid
    edition: str = "evaluation"
    licensee: str = ""
    features: frozenset = field(default_factory=lambda: frozenset(FEATURES))
    expiry: dt.date | None = None
    licence_id: str = ""
    key_id: str = ""
    is_test: bool = False
    reason: str = ""
    source: str | None = None

    @property
    def is_licensed(self) -> bool:
        return self.state == "valid" and self.edition != "evaluation"

    @property
    def watermark(self) -> str | None:
        if self.state == "valid" and self.is_test:
            return TEST_WATERMARK
        if not self.is_licensed:
            return EVALUATION_WATERMARK
        return None

    def has(self, feature: str) -> bool:
        return feature in self.features

    def days_remaining(self, today: dt.date | None = None) -> int | None:
        if self.expiry is None:
            return None
        return (self.expiry - (today or dt.date.today())).days

    def summary(self) -> str:
        if self.state == "valid":
            exp = "perpetual" if self.expiry is None else f"expires {self.expiry.isoformat()}"
            test = " (TEST LICENCE)" if self.is_test else ""
            return f"{self.edition.capitalize()} licence - {self.licensee} - {exp}{test}"
        if self.state == "evaluation" and not self.reason:
            return "Evaluation mode (no licence installed)"
        return f"Evaluation mode - licence {self.state}: {self.reason}"


def evaluation_status(reason: str = "", state: str = "evaluation", source: str | None = None) -> LicenceStatus:
    return LicenceStatus(state=state, reason=reason, source=source)


# ----------------------------------------------------------------------------- helpers
def machine_fingerprint() -> str:
    """Soft machine identity: SHA-256 over host name, primary MAC, OS and CPU architecture.

    This is a deterrent, not copy protection: changing the network adapter or host name
    changes the fingerprint, and on machines without a readable MAC ``uuid.getnode`` returns a
    random value per process (then the fingerprint is unstable and machine binding should not
    be used)."""
    raw = f"{platform.node()}|{uuid.getnode():012x}|{platform.system()}|{platform.machine()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def canonical_payload(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _parse_date(s) -> dt.date | None:
    if s in (None, ""):
        return None
    try:
        return dt.date.fromisoformat(str(s))
    except ValueError as e:
        raise LicenceError(f"invalid date {s!r}") from e


def trusted_keys(allow_test: bool | None = None) -> dict[str, tuple[str, bool]]:
    """Map key_id -> (public key hex, is_test_key)."""
    if allow_test is None:
        allow_test = os.environ.get("OSTEOQUANT_ACCEPT_TEST_LICENCES") == "1"
    keys = {k: (v, False) for k, v in PRODUCTION_KEYS.items()}
    if allow_test:
        keys.update({k: (v, True) for k, v in TEST_KEYS.items()})
    return keys


# ----------------------------------------------------------------------------- sign / verify
def sign_licence(payload: dict, private_key: Ed25519PrivateKey, key_id: str) -> dict:
    """Create a licence envelope. Used by the licensor tooling and by tests."""
    p = dict(payload)
    p.setdefault("product", PRODUCT)
    p.setdefault("features", list(FEATURES))
    p.setdefault("machine", None)
    p.setdefault("test", False)
    for k in ("licence_id", "licensee", "edition", "issued"):
        if not p.get(k):
            raise LicenceError(f"payload field {k!r} is required")
    if p["edition"] not in EDITIONS:
        raise LicenceError(f"edition must be one of {EDITIONS}")
    unknown = set(p["features"]) - set(FEATURES)
    if unknown:
        raise LicenceError(f"unknown features {sorted(unknown)}")
    _parse_date(p["issued"])
    _parse_date(p.get("expiry"))
    text = canonical_payload(p)
    sig = private_key.sign(text.encode("utf-8"))
    return {"format": FORMAT, "key_id": key_id, "payload": text, "signature": base64.b64encode(sig).decode()}


def verify_envelope(envelope: dict, keys: dict[str, tuple[str, bool]] | None = None,
                    today: dt.date | None = None, machine: str | None = None,
                    source: str | None = None) -> LicenceStatus:
    """Verify a licence envelope. Never raises for bad licences: returns a status with
    ``state`` in {valid, expired, invalid} and a human-readable ``reason``."""
    keys = trusted_keys() if keys is None else keys
    today = today or dt.date.today()

    def bad(reason, state="invalid"):
        return evaluation_status(reason, state, source)

    if not isinstance(envelope, dict) or envelope.get("format") != FORMAT:
        return bad("not an OsteoQuant licence file (unknown format)")
    kid = envelope.get("key_id")
    payload_text = envelope.get("payload")
    sig_b64 = envelope.get("signature")
    if not isinstance(payload_text, str) or not isinstance(sig_b64, str):
        return bad("licence file is incomplete")
    if not isinstance(kid, str):     # a list/dict key id must not raise before the signature check (C2-PRD-18)
        return bad("licence file is malformed (key id is not text)")
    if kid not in keys:
        if kid in TEST_KEYS:
            return bad("signed with the public TEST key; test licences are not accepted by this build")
        return bad(f"signed by an unknown key ({kid!r})")
    pub_hex, is_test_key = keys[kid]
    try:
        sig = base64.b64decode(sig_b64, validate=True)
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(sig, payload_text.encode("utf-8"))
    except (InvalidSignature, ValueError):
        return bad("signature does not match (file altered or signed with a different key)")
    try:
        p = json.loads(payload_text)
        if not isinstance(p, dict):
            return bad("payload is not a licence record")
        issued = _parse_date(p.get("issued"))
        expiry = _parse_date(p.get("expiry"))
    except (json.JSONDecodeError, LicenceError) as e:
        return bad(f"payload unreadable: {e}")
    if not isinstance(p.get("features", []), list) or not all(isinstance(f, str) for f in p.get("features", [])):
        return bad("payload field 'features' is malformed")
    if p.get("product") != PRODUCT:
        return bad(f"licence is for a different product ({p.get('product')!r})")
    if p.get("edition") not in EDITIONS:
        return bad(f"unknown edition {p.get('edition')!r}")
    if issued is None:
        return bad("licence has no issue date")
    feats = frozenset(f for f in p.get("features", []) if f in FEATURES)
    is_test = bool(is_test_key or p.get("test"))
    common = dict(edition=p["edition"], licensee=str(p.get("licensee", "")), features=feats, expiry=expiry,
                  licence_id=str(p.get("licence_id", "")), key_id=kid, is_test=is_test, source=source)
    if expiry is not None and expiry < today:
        return LicenceStatus(state="expired", reason=f"expired on {expiry.isoformat()}", **{**common,
                             "features": frozenset(FEATURES), "edition": "evaluation"})
    bound = p.get("machine")
    if bound:
        here = machine or machine_fingerprint()
        if bound != here:
            return LicenceStatus(state="invalid", reason="licence is bound to a different machine",
                                 **{**common, "features": frozenset(FEATURES), "edition": "evaluation"})
    return LicenceStatus(state="valid", **common)


def verify_file(path, keys=None, today=None, machine=None) -> LicenceStatus:
    """Total: any problem with the file gives an ``invalid`` status (evaluation mode), never an exception."""
    path = Path(path)
    try:
        env = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as e:
        return evaluation_status(f"cannot read licence file: {e}", "invalid", str(path))
    try:
        return verify_envelope(env, keys=keys, today=today, machine=machine, source=str(path))
    except Exception as e:  # noqa: BLE001 - a malformed or hostile file must never stop the application
        return evaluation_status(f"licence file is malformed ({type(e).__name__})", "invalid", str(path))


# ----------------------------------------------------------------------------- installation
def user_config_dir() -> Path:
    if sys.platform.startswith("win"):
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "OsteoQuant"


def default_licence_path() -> Path:
    env = os.environ.get("OSTEOQUANT_LICENCE_FILE")
    return Path(env) if env else user_config_dir() / LICENCE_FILENAME


def current_status(keys=None) -> LicenceStatus:
    """Status of the installed licence, or evaluation mode when none is installed."""
    try:
        p = default_licence_path()
        if not p.exists():
            return evaluation_status()
        return verify_file(p, keys=keys)
    except Exception as e:  # noqa: BLE001 - start in evaluation mode with a clear message (C2-PRD-18)
        return evaluation_status(f"licence could not be checked ({type(e).__name__}: {e})", "invalid")


def install_licence(src, keys=None) -> LicenceStatus:
    """Verify ``src`` and, if valid, copy it to the per-user licence location."""
    st = verify_file(src, keys=keys)
    if st.state != "valid":
        return st
    try:
        dest = default_licence_path()
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    except OSError as e:
        return evaluation_status(f"licence could not be installed: {e}", "invalid", str(src))
    return verify_file(dest, keys=keys)

