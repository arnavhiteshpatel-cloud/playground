"""Deployment runtimes for locked segmentation models.

The desktop application should not need PyTorch at analysis time: PyTorch adds several hundred MB to an
installer, while ONNX Runtime (MIT licence) is ~20–60 MB and runs the same network on CPU (and on
DirectML/CoreML execution providers where available — not tested here). Workflow:

1. ``export_onnx(name)`` converts a registered PyTorch checkpoint to ``models/<name>.onnx`` and records its
   SHA-256 next to the PyTorch hash in ``models/registry.json`` (``onnx_sha256``) — the ONNX file is a
   *derived artefact* of the locked model and is verified before loading, like the checkpoint.
2. ``OnnxSegmenter(name).predict_proba(image, cfg)`` reproduces ``ml.train.predict_proba`` (same
   normalisation, patching and Gaussian blending), so outputs can be compared voxel-for-voxel
   (Experiment O2).

Batching: patches are evaluated ``batch`` at a time to amortise per-call overhead.
"""
from __future__ import annotations

import hashlib
import json
import re

import numpy as np

from .core import MODEL_DIR, MODEL_NAME_RE, Case, _gauss_window, build_input


def _registry() -> dict:
    p = MODEL_DIR / "registry.json"
    return json.loads(p.read_text()) if p.exists() else {}


def export_onnx(name: str, patch=(48, 48, 48), opset: int = 17) -> dict:
    import torch
    from .train import load_model, update_registry
    model, ck = load_model(name)
    model.eval()
    in_ch = model.hparams.get("in_ch", 1)
    dummy = torch.zeros((1, in_ch) + tuple(patch), dtype=torch.float32)
    out = MODEL_DIR / f"{name}.onnx"
    torch.onnx.export(model, dummy, str(out), input_names=["x"], output_names=["logits"], opset_version=opset,
                      dynamic_axes={"x": {0: "batch"}, "logits": {0: "batch"}}, dynamo=False)
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    if name in _registry():
        update_registry(name, merge={"onnx_sha256": sha, "onnx_patch": list(patch)})
    return {"path": str(out), "sha256": sha, "patch": list(patch)}


class OnnxSegmenter:
    def __init__(self, name: str, threads: int = 4, verify: bool = True, quantized: bool = False):
        import onnxruntime as ort
        if not re.fullmatch(MODEL_NAME_RE, str(name)):
            raise ValueError("Invalid model name")
        suffix = ".int8.onnx" if quantized else ".onnx"
        path = MODEL_DIR / f"{name}{suffix}"
        R = _registry()
        data = path.read_bytes()                  # verify and load the SAME bytes (no re-open by path; QA-023)
        if verify:
            key = "onnx_int8_sha256" if quantized else "onnx_sha256"
            want = R.get(name, {}).get(key)
            got = hashlib.sha256(data).hexdigest()
            if not want or want != got:
                raise RuntimeError(f"ONNX model {path.name} hash does not match the registry")
        so = ort.SessionOptions()
        so.intra_op_num_threads = threads
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.sess = ort.InferenceSession(data, so, providers=["CPUExecutionProvider"])
        self.reg = dict(R.get(name, {}))          # registry entry used for this session (identity, provenance)
        self.patch = tuple(R.get(name, {}).get("onnx_patch", (48, 48, 48)))
        self.cfg = R.get(name, {}).get("cfg", {})
        self.name = name

    def predict_proba(self, case: Case, cfg: dict | None = None, overlap: float = 0.5, batch: int = 4) -> np.ndarray:
        cfg = cfg or self.cfg
        x = build_input(case, cfg)
        ps = tuple(min(p, s) for p, s in zip(self.patch, x.shape[1:]))
        if ps != self.patch:
            pad = [(0, 0)] + [(0, max(0, p - s)) for p, s in zip(self.patch, x.shape[1:])]
            x = np.pad(x, pad, mode="edge")
            ps = self.patch
        w = _gauss_window(ps)
        steps = [max(1, int(p * (1 - overlap))) for p in ps]
        starts = [sorted(set(list(range(0, max(s - p, 0) + 1, st)) + [max(s - p, 0)]))
                  for s, p, st in zip(x.shape[1:], ps, steps)]
        coords = [(z, y, xx) for z in starts[0] for y in starts[1] for xx in starts[2]]
        out = None
        wsum = np.zeros(x.shape[1:], np.float32)
        for i in range(0, len(coords), batch):
            cb = coords[i:i + batch]
            xb = np.stack([x[:, z:z + ps[0], y:y + ps[1], xx:xx + ps[2]] for z, y, xx in cb]).astype(np.float32)
            logits = self.sess.run(None, {"x": xb})[0]
            e = np.exp(logits - logits.max(1, keepdims=True))
            p = e / e.sum(1, keepdims=True)
            if out is None:
                out = np.zeros((p.shape[1],) + x.shape[1:], np.float32)
            for k, (z, y, xx) in enumerate(cb):
                sl = (slice(z, z + ps[0]), slice(y, y + ps[1]), slice(xx, xx + ps[2]))
                out[(slice(None),) + sl] += p[k] * w
                wsum[sl] += w
        out = out / wsum[None]
        shp = case.image.shape
        return out[:, : shp[0], : shp[1], : shp[2]]


def quantize_int8_static(name: str, calib_cases: list[Case], n_patches: int = 32, seed: int = 0) -> dict:
    """Static int8 (QDQ) quantisation calibrated on patches from ``calib_cases`` (training data only)."""
    from onnxruntime.quantization import CalibrationDataReader, QuantFormat, QuantType, quantize_static
    from .train import update_registry
    R = _registry()
    cfg = R[name]["cfg"]
    patch = tuple(R[name].get("onnx_patch", (48, 48, 48)))
    rng = np.random.default_rng(seed)

    class Reader(CalibrationDataReader):
        def __init__(self):
            xs = []
            for _ in range(n_patches):
                c = calib_cases[rng.integers(len(calib_cases))]
                x = build_input(c, cfg)
                o = [int(rng.integers(0, max(1, s - p + 1))) for s, p in zip(x.shape[1:], patch)]
                xs.append(x[:, o[0]:o[0] + patch[0], o[1]:o[1] + patch[1], o[2]:o[2] + patch[2]][None])
            self.it = iter([{"x": v.astype(np.float32)} for v in xs])

        def get_next(self):
            return next(self.it, None)

    src = MODEL_DIR / f"{name}.onnx"
    dst = MODEL_DIR / f"{name}.int8.onnx"
    quantize_static(str(src), str(dst), Reader(), quant_format=QuantFormat.QDQ,
                    activation_type=QuantType.QUInt8, weight_type=QuantType.QInt8)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    update_registry(name, merge={"onnx_int8_sha256": sha})
    return {"path": str(dst), "sha256": sha}
