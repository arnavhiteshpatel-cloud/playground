"""ONNX Runtime evaluation helper for experiments (bit-equivalent to PyTorch inference: max prob diff ~5e-6,
identical labels — Experiment O2 spot check). Exports a registered model once, then reuses it."""
from __future__ import annotations

from osteoquant.ml.core import MODEL_DIR

_cache = {}


def predictor(name: str, threads: int = 4):
    if name not in _cache:
        from osteoquant.ml.runtime import OnnxSegmenter, export_onnx, _registry
        reg = _registry().get(name, {})
        if not (MODEL_DIR / f"{name}.onnx").exists() or not reg.get("onnx_sha256"):
            export_onnx(name)
        _cache[name] = OnnxSegmenter(name, threads=threads)
    return _cache[name]


def predict(name: str, case, cfg: dict):
    return predictor(name).predict_proba(case, cfg)
