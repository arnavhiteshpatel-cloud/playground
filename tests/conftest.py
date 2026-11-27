"""Shared fixtures and hypothesis profiles for the OsteoQuant test-suite."""
import os

import numpy as np
import pytest

try:
    from hypothesis import HealthCheck, settings

    settings.register_profile("default", max_examples=25, deadline=None,
                              suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
    settings.register_profile("ci", max_examples=40, deadline=None, derandomize=True,
                              suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
    settings.register_profile("thorough", max_examples=300, deadline=None,
                              suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
    settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))
except ImportError:  # pragma: no cover
    pass


@pytest.fixture
def rng():
    return np.random.default_rng(12345)


@pytest.fixture
def store(tmp_path):
    from osteoquant.study.db import Store
    st = Store(tmp_path / "t.db", tmp_path / "data")
    yield st
    st.conn.close()
