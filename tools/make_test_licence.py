#!/usr/bin/env python
"""Create TEST licences for the OsteoQuant desktop application.

TEST ONLY. The signing key used here is derived from a seed that is published in this file,
so anyone can create licences with it. The application accepts such licences only when test
licences are explicitly allowed (OSTEOQUANT_ACCEPT_TEST_LICENCES=1, unit tests, CI) and always
labels them "TEST LICENCE". This tool must never be used to issue licences to customers, and it
never handles a production key.

Examples
  python tools/make_test_licence.py --licensee "Test Lab" --edition academic --days 365 -o test.oqlic
  python tools/make_test_licence.py --edition commercial --bind-this-machine -o bound.oqlic
  python tools/make_test_licence.py --keygen keys/          # fresh random TEST keypair (PEM)
  python tools/make_test_licence.py --key keys/test_private.pem --key-id my-test -o x.oqlic
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cryptography.hazmat.primitives import serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

from osteoquant.licensing import FEATURES, machine_fingerprint, sign_licence  # noqa: E402
from osteoquant.licensing.keys import TEST_KEY_ID, TEST_KEY_SEED_TEXT, TEST_KEYS  # noqa: E402


def test_private_key() -> Ed25519PrivateKey:
    """The well-known TEST private key (public half embedded as keys.TEST_KEYS)."""
    k = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(TEST_KEY_SEED_TEXT).digest())
    pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
    assert pub == TEST_KEYS[TEST_KEY_ID], "embedded test public key does not match the test seed"
    return k


def make_test_licence(licensee="TEST LICENSEE", edition="academic", days: int | None = 365,
                      features=None, machine=None, key: Ed25519PrivateKey | None = None,
                      key_id: str = TEST_KEY_ID, issued: dt.date | None = None) -> dict:
    issued = issued or dt.date.today()
    payload = {
        "licence_id": "TEST-" + uuid.uuid4().hex[:12].upper(),
        "licensee": licensee, "edition": edition,
        "features": list(features or FEATURES),
        "issued": issued.isoformat(),
        "expiry": None if days is None else (issued + dt.timedelta(days=days)).isoformat(),
        "machine": machine, "test": True,
    }
    return sign_licence(payload, key or test_private_key(), key_id)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--licensee", default="TEST LICENSEE")
    ap.add_argument("--edition", default="academic", choices=["academic", "commercial", "evaluation"])
    ap.add_argument("--days", type=int, default=365, help="validity in days; 0 = perpetual")
    ap.add_argument("--features", default=",".join(FEATURES))
    ap.add_argument("--bind-this-machine", action="store_true")
    ap.add_argument("--key", help="PEM private key from --keygen (default: well-known TEST key)")
    ap.add_argument("--key-id", default=None)
    ap.add_argument("--keygen", metavar="DIR", help="write a fresh random TEST keypair to DIR and exit")
    ap.add_argument("-o", "--out", default="test_licence.oqlic")
    a = ap.parse_args(argv)

    if a.keygen:
        d = Path(a.keygen)
        d.mkdir(parents=True, exist_ok=True)
        k = Ed25519PrivateKey.generate()
        (d / "test_private.pem").write_bytes(k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                              serialization.NoEncryption()))
        pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
        (d / "test_public.hex").write_text(pub + "\n")
        print(json.dumps({"private_key": str(d / "test_private.pem"), "public_key_hex": pub,
                          "note": "TEST keypair only; not trusted by the application unless passed explicitly"}))
        return 0
    key, kid = None, a.key_id or TEST_KEY_ID
    if a.key:
        key = serialization.load_pem_private_key(Path(a.key).read_bytes(), password=None)
        kid = a.key_id or "custom-test-key"
    env = make_test_licence(a.licensee, a.edition, None if a.days == 0 else a.days,
                            [f for f in a.features.split(",") if f],
                            machine_fingerprint() if a.bind_this_machine else None, key, kid)
    Path(a.out).write_text(json.dumps(env, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"written": a.out, "key_id": kid, "payload": json.loads(env["payload"]),
                      "note": "TEST LICENCE: accepted only with OSTEOQUANT_ACCEPT_TEST_LICENCES=1"}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
