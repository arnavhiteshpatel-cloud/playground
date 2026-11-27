"""Experiment O — processing speed and peak memory on real full-resolution data.

Each stage runs in a fresh child process (multiprocessing 'spawn'); peak resident memory is
ru_maxrss of that child. Hardware: this container (4 vCPU Xeon @2.3 GHz, 15 GB RAM, no GPU).
Data: Zenodo 17255310 ovine callus 18-day TXM (1016×1024×1001 uint16, 24.6 µm, 2.1 GB);
Zenodo 3909552 mouse knee DICOM series (829 slices, 983×1392, int16).
Stages: TXM header read; full TXM → chunked Zarr (slab-streamed); out-of-core Otsu threshold +
mineral volume by slab iteration (bounded memory); QC on full volume; segmental ROI detection on
×4-decimated volume; multi-Otsu segmentation + class volumes on a 384³ ROI crop; trabecular
morphometry (thickness, connectivity) on a 160³ crop; U-Net inference throughput on 96³;
DICOM series ingest (829 slices).
"""
import json
import multiprocessing as mp
import resource
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TXM = ROOT / "data" / "raw" / "zenodo_17255310" / "18DAYS_recon.txm"
ZARR = ROOT / "data" / "work" / "ovine18.zarr"
KNEE = ROOT / "data" / "raw" / "zenodo_3909552_mouse_oa_knee"


def _child(stage, q):
    sys.path.insert(0, str(ROOT))
    import numpy as np
    t = time.time()
    info = {}
    if stage == "txm_header":
        from osteoquant.io import txm_metadata
        md = txm_metadata(TXM)
        info = {"shape": [md["n_images"], md["height"], md["width"]], "pixel_um": md["pixel_size_um"]}
    elif stage == "txm_to_zarr_streamed":
        import zarr
        from osteoquant.io.readers import read_txm, txm_metadata
        md = txm_metadata(TXM)
        n = md["n_images"]
        ZARR.parent.mkdir(parents=True, exist_ok=True)
        g = zarr.open_group(str(ZARR), mode="w")
        a = g.create_array("image", shape=(n, md["height"], md["width"]), chunks=(64, 128, 128), dtype=np.uint16)
        for z0 in range(0, n, 64):
            v, _ = read_txm(TXM, zrange=(z0, min(n, z0 + 64)), do_hash=False)
            a[z0:z0 + v.shape[0]] = v.data
        g.attrs.update({"spacing_um": [md["pixel_size_um"]] * 3})
        info = {"voxels": int(np.prod(a.shape)), "zarr_bytes": sum(f.stat().st_size for f in ZARR.rglob("*") if f.is_file())}
    elif stage == "sha256_full_file":
        from osteoquant.io import sha256_file
        info = {"sha256": sha256_file(TXM)[:16], "bytes": TXM.stat().st_size}
    elif stage == "out_of_core_otsu_mineral":
        from osteoquant.io import iter_slabs
        from skimage.filters import threshold_otsu
        hist = np.zeros(65536, np.int64)
        for _, _, s, _ in iter_slabs(ZARR, 64):
            hist += np.bincount(s.ravel(), minlength=65536)
        centers = np.arange(65536)
        t_otsu = threshold_otsu(hist=(hist, centers))
        mineral = 0
        for _, _, s, _ in iter_slabs(ZARR, 64):
            mineral += int((s > t_otsu).sum())
        info = {"otsu": int(t_otsu), "mineral_voxels": mineral, "mineral_mm3": mineral * 24.6068 ** 3 * 1e-9}
    elif stage == "qc_full_volume":
        from osteoquant.io import read_volume
        from osteoquant.qc import run_qc
        v, _ = read_volume(ZARR)
        q = run_qc(v)
        info = {"verdict": q["verdict"], "n_warn": q["n_warn"], "voxels": int(v.data.size)}
    elif stage == "roi_detect_decimated_x4":
        from osteoquant.io import read_volume
        from osteoquant.roi import detect_segmental_gap
        v, _ = read_volume(ZARR, step=4)
        r = detect_segmental_gap(v.data, v.spacing)
        info = {"gap_um": r.diagnostics["gap_length_um"], "confidence": r.confidence}
    elif stage == "segment_classvolumes_384crop":
        from osteoquant.io import read_volume
        from osteoquant.segment.classical import seg_multiotsu
        from osteoquant.morphometry import class_volumes
        v, _ = read_volume(ZARR, zrange=(300, 684))
        d = v.data[:, 320:704, 300:684]
        roi = np.ones(d.shape, bool)
        lab, th = seg_multiotsu(d, roi, True)
        info = {"voxels": int(d.size), "class_volumes": class_volumes(lab, roi, v.spacing)}
    elif stage == "trabecular_morphometry_160crop":
        from osteoquant.io import read_volume
        from osteoquant.morphometry import trabecular_morphometry
        from skimage.filters import threshold_otsu
        v, _ = read_volume(ZARR, zrange=(420, 580))
        d = v.data[:, 440:600, 420:580]
        b = d > threshold_otsu(d)
        r = trabecular_morphometry(b, np.ones_like(b), v.spacing[0])
        info = {"voxels": int(d.size), "BV_TV": r["BV_TV"], "Tb_Th_um": r["Tb_Th_um"], "Conn_D": r["Conn_D_per_mm3"]}
    elif stage == "unet_inference_96cube":
        import torch
        from osteoquant.ml.train import load_model, predict_proba, Case
        torch.set_num_threads(4)
        m, ck = load_model("unet_noctx_s0")
        x = np.random.default_rng(0).normal(500, 100, (96, 96, 96)).astype(np.float32)
        t1 = time.time()
        predict_proba(m, Case("x", x, None, None, (40,) * 3), ck["cfg"])
        dt = time.time() - t1
        info = {"voxels": 96 ** 3, "voxels_per_s": 96 ** 3 / dt, "seconds_per_100M_voxels_est": 1e8 / (96 ** 3 / dt)}
    elif stage == "dicom_series_ingest":
        import zipfile, tempfile
        from osteoquant.io import read_volume
        from osteoquant.io.safe_archive import safe_extract
        d = ROOT / "data" / "work" / "knee_dcm"
        if not d.exists():
            safe_extract(KNEE / "ORIG-907-L.zip", d)
        src = next(p.parent for p in d.rglob("*.DCM"))
        t1 = time.time()
        v, rep = read_volume(src, do_hash=False)
        info = {"shape": list(v.shape), "spacing_um": list(v.spacing), "dtype": str(v.data.dtype),
                "read_s": time.time() - t1, "warnings": rep.warnings[:3], "missing_slices": len(rep.missing_slices)}
    info["seconds"] = round(time.time() - t, 2)
    info["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)
    q.put(info)


def run(stage):
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=_child, args=(stage, q))
    p.start()
    p.join()
    return q.get() if not q.empty() else {"error": f"exit {p.exitcode}"}


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    from experiments.common import save_result
    stages = ["txm_header", "sha256_full_file", "txm_to_zarr_streamed", "out_of_core_otsu_mineral", "qc_full_volume",
              "roi_detect_decimated_x4", "segment_classvolumes_384crop", "trabecular_morphometry_160crop",
              "unet_inference_96cube", "dicom_series_ingest"]
    out = {"experiment": "O", "hardware": "4 vCPU Xeon 2.3 GHz, 15 GB RAM, no GPU (cloud container)", "stages": {}}
    for s in stages:
        out["stages"][s] = run(s)
        print(s, json.dumps(out["stages"][s], default=str)[:300], flush=True)
    save_result("exp_O_performance", out)
