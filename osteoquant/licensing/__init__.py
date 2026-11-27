"""Offline, signature-verified licensing for the OsteoQuant desktop application."""
from .core import (EDITIONS, FEATURES, FORMAT, PRODUCT, EVALUATION_WATERMARK, TEST_WATERMARK,  # noqa: F401
                   LicenceError, LicenceStatus, canonical_payload, current_status, default_licence_path,
                   evaluation_status, install_licence, machine_fingerprint, sign_licence, trusted_keys,
                   user_config_dir, verify_envelope, verify_file)
