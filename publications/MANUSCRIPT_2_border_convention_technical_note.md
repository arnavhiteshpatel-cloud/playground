# Technical note: the volume-border convention changes direct 3D trabecular thickness by ~18% — agreement of an open implementation with Scanco IPL

**Status: DRAFT (2026-11-27). Real public data (n=8). Important caveat: the "edge" convention was selected after
observing both conventions on these same 8 samples; a confirmatory comparison on independent reference data is required
before submission (planned: request IPL outputs on additional public cubes, or BoneJ comparisons).**

## Abstract (draft)
Direct 3D trabecular thickness (Tb.Th) and separation (Tb.Sp) by sphere fitting (Hildebrand & Rüegsegger 1997) are
standard micro-CT outcomes (Bouxsein et al. 2010), yet implementations differ in how they treat structures cut by the
analysed volume's border. Using eight segmented trabecular cubes (100³ voxels, ~17 µm) released with Scanco IPL
distance-transform thickness maps (Zenodo 10.5281/zenodo.11061947, CC-BY-4.0), we compared an open Python
implementation under two conventions. Treating the border as background under-read IPL by −17.6% (Tb.Th; ICC(2,1)
0.61) and −34.0% (Tb.Sp; ICC 0.55). Extending border structures by edge replication gave −2.4% (ICC 0.983) and −4.1%
(ICC 0.948). On analytic plates the implementation is exact for even voxel thicknesses (+1 voxel for odd); digitised rods
read ≈1 voxel thin. Methods sections should report the border convention; small VOIs are most affected.

## Methods
Implementation: `osteoquant/morphometry/core.py::local_thickness` (EDT → distance ridge → sphere painting; thickness
= 2·d_EDT; coverage |x−c| < d). Conventions: `background` (pad with background) vs `edge` (replicate border 24 voxels,
compute, crop). Agreement: ICC(2,1) absolute agreement (Koo & Li 2016), Bland–Altman, mean relative error. Script:
`experiments/exp_G_morphometry.py`; results `experiments/results/exp_G_morphometry.json`; Figure `exp_G_morphometry.png`.

## Results
Per-sample values in the JSON; summary above. Mean IPL Tb.Th 134–250 µm across samples.

## Limitations
n=8; post-hoc convention choice (above); header voxel sizes differ from the record description (16.56–17.59 µm vs
17.59 µm); IPL map interpretation (mean over structure voxels) assumed.

## Target
Short communication: Bone Reports, JBMR Plus (methods), or Journal of Microscopy [UNR — check scope].
