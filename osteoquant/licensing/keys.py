"""Public keys trusted for licence verification.

Only PUBLIC keys live in the application. The matching private keys are held offline by the
licensor and are never part of this repository or of any build.

PRODUCTION_KEYS
    Empty in this source tree. No production signing key has been generated yet. The licensor
    creates one on an offline machine (see docs/desktop/PACKAGING.md, "Licence signing key")
    and adds the raw 32-byte Ed25519 public key here as hex, keyed by a key id.

TEST_KEYS
    A test key whose private half is derived from a published seed in
    ``tools/make_test_licence.py``. Anyone can sign with it, so licences signed by it prove
    nothing. They are accepted only when the caller explicitly allows test licences (unit tests,
    CI, or the environment variable ``OSTEOQUANT_ACCEPT_TEST_LICENCES=1``) and are always
    reported as "TEST LICENCE".
"""
from __future__ import annotations

PRODUCTION_KEYS: dict[str, str] = {
    # "oq-prod-2027-01": "<64 hex chars: raw Ed25519 public key>",
}

TEST_KEY_ID = "oq-test-1"
TEST_KEY_SEED_TEXT = b"OSTEOQUANT-TEST-LICENCE-KEY-NOT-FOR-PRODUCTION-v1"
TEST_KEYS: dict[str, str] = {
    TEST_KEY_ID: "6a3be54a8b4ca103045ab0ec25ac707e5de85496781b3cbeaa2fce9a72988425",
}
