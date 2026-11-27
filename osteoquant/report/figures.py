"""Report figures: orthogonal overlay panels with scale bars, group dot plots, ingrowth profiles."""
from __future__ import annotations

import numpy as np

COLORS = {1: (0.902, 0.624, 0.0), 2: (0.337, 0.706, 0.914), 3: (0.8, 0.475, 0.655), 255: (0.94, 0.89, 0.26)}


def overlay_rgb(img2d, lab2d, alpha=0.45, window=None):
    lo, hi = window or (np.percentile(img2d, 1), np.percentile(img2d, 99.5))
    g = np.clip((img2d - lo) / max(hi - lo, 1e-6), 0, 1)
    rgb = np.stack([g, g, g], -1)
    for c, col in COLORS.items():
        m = lab2d == c
        rgb[m] = (1 - alpha) * rgb[m] + alpha * np.array(col)
    return rgb


def specimen_panel(img, lab, roi, spacing, path, title="", center=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    if center is None:
        c = np.argwhere(roi).mean(0).astype(int) if roi is not None and roi.any() else np.array(img.shape) // 2
    else:
        c = center
    win = (np.percentile(img, 1), np.percentile(img, 99.5))
    views = [("axial", img[c[0]], lab[c[0]], None if roi is None else roi[c[0]], (spacing[1], spacing[2])),
             ("coronal", img[:, c[1]], lab[:, c[1]], None if roi is None else roi[:, c[1]], (spacing[0], spacing[2])),
             ("sagittal", img[:, :, c[2]], lab[:, :, c[2]], None if roi is None else roi[:, :, c[2]], (spacing[0], spacing[1]))]
    fig, axs = plt.subplots(1, 6, figsize=(14, 2.6))
    for i, (name, im, lb, rm, sp) in enumerate(views):
        a0, a1 = axs[2 * i], axs[2 * i + 1]
        ext = [0, im.shape[1] * sp[1] / 1000, im.shape[0] * sp[0] / 1000, 0]
        a0.imshow(im, cmap="gray", vmin=win[0], vmax=win[1], extent=ext)
        a1.imshow(overlay_rgb(im, lb, window=win), extent=ext)
        if rm is not None and rm.any():
            a1.contour(np.linspace(0, ext[1], im.shape[1]), np.linspace(0, ext[2], im.shape[0]), rm, [0.5],
                       colors="white", linewidths=0.6)
        for a in (a0, a1):
            a.set_xticks([]); a.set_yticks([])
            bar = 1.0 if ext[1] > 2.5 else 0.5
            a.plot([ext[1] * 0.06, ext[1] * 0.06 + bar], [ext[2] * 0.92] * 2, color="white", lw=2)
            a.text(ext[1] * 0.06, ext[2] * 0.86, f"{bar:g} mm", color="white", fontsize=6)
        a0.set_title(name, fontsize=8)
        a1.set_title(name + " + labels", fontsize=8)
    if title:
        fig.suptitle(title, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return path


def group_dotplot(bundle, endpoints, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from .defectfill import _get
    n = len(endpoints)
    fig, axs = plt.subplots(1, n, figsize=(3.6 * n, 3.0))
    axs = np.atleast_1d(axs)
    keys = sorted({(str(s.get("timepoint")), str(s.get("group"))) for s in bundle["specimens"]})
    pal = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00"]
    groups = sorted({k[1] for k in keys})
    for ax, (key, label, unit) in zip(axs, endpoints):
        for i, (tp, g) in enumerate(keys):
            v = [_get(s["metrics"], key) for s in bundle["specimens"] if str(s.get("group")) == g and str(s.get("timepoint")) == tp]
            v = [x for x in v if np.isfinite(x)]
            x = i + np.random.default_rng(i).uniform(-0.12, 0.12, len(v))
            col = pal[groups.index(g) % len(pal)]
            ax.scatter(x, v, s=18, color=col, alpha=0.8, zorder=3)
            if len(v):
                m = np.mean(v)
                ax.plot([i - 0.25, i + 0.25], [m, m], color="k", lw=1.5, zorder=4)
                if len(v) > 1:
                    se = np.std(v, ddof=1) / np.sqrt(len(v))
                    ax.errorbar(i, m, yerr=1.96 * se, color="k", lw=0.8, capsize=3, zorder=4)
        ax.set_xticks(range(len(keys)))
        ax.set_xticklabels([f"{g}\n{tp}" for tp, g in keys], fontsize=6.5)
        ax.set_title(f"{label} ({unit})", fontsize=8)
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path
