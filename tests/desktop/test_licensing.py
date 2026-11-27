"""Offline licence verification: valid, tampered, expired, wrong key, machine binding, test keys."""
import base64
import datetime as dt
import importlib.util
import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from osteoquant.licensing import (EVALUATION_WATERMARK, TEST_WATERMARK, current_status, install_licence,
                                  sign_licence, verify_envelope, verify_file)
from osteoquant.licensing.keys import PRODUCTION_KEYS, TEST_KEY_ID

TODAY = dt.date(2026, 11, 27)


def _key():
    k = Ed25519PrivateKey.generate()
    pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
    return k, pub


def _payload(**kw):
    p = {"licence_id": "L-1", "licensee": "Bone Lab", "edition": "academic", "issued": "2026-01-01",
         "expiry": "2027-12-31", "features": ["import", "viewer", "report"]}
    p.update(kw)
    return p


@pytest.fixture
def signed():
    k, pub = _key()
    keys = {"prod-x": (pub, False)}
    return k, keys, sign_licence(_payload(), k, "prod-x")


def test_valid(signed):
    _, keys, env = signed
    st = verify_envelope(env, keys, today=TODAY)
    assert st.state == "valid" and st.is_licensed and st.edition == "academic"
    assert st.licensee == "Bone Lab" and st.has("report") and not st.has("edit")
    assert st.watermark is None and st.days_remaining(TODAY) == (dt.date(2027, 12, 31) - TODAY).days


def test_tampered_payload(signed):
    _, keys, env = signed
    p = json.loads(env["payload"])
    p["edition"] = "commercial"
    bad = {**env, "payload": json.dumps(p, sort_keys=True, separators=(",", ":"))}
    st = verify_envelope(bad, keys, today=TODAY)
    assert st.state == "invalid" and "signature" in st.reason and st.watermark == EVALUATION_WATERMARK


def test_tampered_expiry_whitespace_and_signature(signed):
    _, keys, env = signed
    assert verify_envelope({**env, "payload": env["payload"] + " "}, keys, today=TODAY).state == "invalid"
    sig = bytearray(base64.b64decode(env["signature"]))
    sig[0] ^= 1
    assert verify_envelope({**env, "signature": base64.b64encode(bytes(sig)).decode()}, keys, today=TODAY).state == "invalid"
    assert verify_envelope({**env, "signature": "@@@"}, keys, today=TODAY).state == "invalid"


def test_expired(signed):
    k, keys, _ = signed
    env = sign_licence(_payload(expiry="2026-06-30"), k, "prod-x")
    st = verify_envelope(env, keys, today=TODAY)
    assert st.state == "expired" and "2026-06-30" in st.reason and not st.is_licensed
    assert st.watermark == EVALUATION_WATERMARK
    assert verify_envelope(env, keys, today=dt.date(2026, 6, 30)).state == "valid"   # last day still valid


def test_perpetual(signed):
    k, keys, _ = signed
    st = verify_envelope(sign_licence(_payload(expiry=None), k, "prod-x"), keys, today=dt.date(2099, 1, 1))
    assert st.state == "valid" and st.expiry is None


def test_wrong_key(signed):
    _, keys, _ = signed
    other, _ = _key()
    env = sign_licence(_payload(), other, "prod-x")       # claims the trusted key id
    assert verify_envelope(env, keys, today=TODAY).state == "invalid"
    env2 = sign_licence(_payload(), other, "unknown-key")
    st = verify_envelope(env2, keys, today=TODAY)
    assert st.state == "invalid" and "unknown key" in st.reason


def test_machine_binding(signed):
    k, keys, _ = signed
    env = sign_licence(_payload(machine="abc123"), k, "prod-x")
    assert verify_envelope(env, keys, today=TODAY, machine="abc123").state == "valid"
    st = verify_envelope(env, keys, today=TODAY, machine="zzz")
    assert st.state == "invalid" and "different machine" in st.reason


def test_malformed_inputs(signed, tmp_path):
    _, keys, env = signed
    assert verify_envelope({}, keys).state == "invalid"
    assert verify_envelope({**env, "format": "other"}, keys).state == "invalid"
    assert verify_envelope({**env, "payload": None}, keys).state == "invalid"
    p = tmp_path / "x.oqlic"
    p.write_text("{not json")
    assert verify_file(p, keys).state == "invalid"


def test_sign_rejects_bad_payload():
    k, _ = _key()
    from osteoquant.licensing import LicenceError
    with pytest.raises(LicenceError):
        sign_licence(_payload(edition="platinum"), k, "x")
    with pytest.raises(LicenceError):
        sign_licence(_payload(features=["teleport"]), k, "x")
    with pytest.raises(LicenceError):
        sign_licence(_payload(expiry="31/12/2027"), k, "x")


def _tool():
    p = Path(__file__).resolve().parents[2] / "tools" / "make_test_licence.py"
    spec = importlib.util.spec_from_file_location("make_test_licence", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_test_key_only_when_allowed(monkeypatch):
    tool = _tool()
    env = tool.make_test_licence("Test Lab", "commercial", 30)
    monkeypatch.delenv("OSTEOQUANT_ACCEPT_TEST_LICENCES", raising=False)
    st = verify_envelope(env)
    assert st.state == "invalid" and "TEST key" in st.reason
    monkeypatch.setenv("OSTEOQUANT_ACCEPT_TEST_LICENCES", "1")
    st = verify_envelope(env)
    assert st.state == "valid" and st.is_test and st.key_id == TEST_KEY_ID
    assert st.watermark == TEST_WATERMARK and "TEST LICENCE" in st.summary()


def test_no_production_key_shipped():
    assert PRODUCTION_KEYS == {}


def test_tool_keygen_and_install(tmp_path, monkeypatch):
    tool = _tool()
    assert tool.main(["--keygen", str(tmp_path / "k")]) == 0
    assert tool.main(["--key", str(tmp_path / "k" / "test_private.pem"), "--key-id", "mine", "-o",
                      str(tmp_path / "l.oqlic")]) == 0
    pub = (tmp_path / "k" / "test_public.hex").read_text().strip()
    assert verify_file(tmp_path / "l.oqlic", {"mine": (pub, True)}).state == "valid"
    # install: an untrusted licence is not copied; evaluation mode stays
    monkeypatch.setenv("OSTEOQUANT_LICENCE_FILE", str(tmp_path / "installed" / "licence.oqlic"))
    assert current_status().state == "evaluation"
    assert install_licence(tmp_path / "l.oqlic").state == "invalid"
    assert not (tmp_path / "installed" / "licence.oqlic").exists()
    st = install_licence(tmp_path / "l.oqlic", keys={"mine": (pub, True)})
    assert st.state == "valid" and (tmp_path / "installed" / "licence.oqlic").exists()
