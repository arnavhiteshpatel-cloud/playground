"""Deuteranopia/protanopia simulation (Machado 2009, severity 1.0) of a viewer screenshot."""
import sys
import numpy as np
from PIL import Image
M = {"deutan": np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]),
     "protan": np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]])}
src, kind, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float64) / 255
lin = np.where(im <= 0.04045, im / 12.92, ((im + 0.055) / 1.055) ** 2.4)
sim = np.clip(lin @ M[kind].T, 0, 1)
s = np.where(sim <= 0.0031308, 12.92 * sim, 1.055 * sim ** (1 / 2.4) - 0.055)
Image.fromarray((s * 255).round().astype(np.uint8)).save(out)
