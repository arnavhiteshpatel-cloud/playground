# Glossary

Terms as used in OsteoQuant documents, the application and its reports. Endpoint formulas are authoritative in
[ENDPOINT_DEFINITIONS.md](../science/ENDPOINT_DEFINITIONS.md).

| Term | Meaning |
|---|---|
| **Abstention** | Declining to report. At voxel level, labelling a voxel *uncertain*; at endpoint level, reporting *not measured* because the advisor does not support the endpoint |
| **Advisor** (measurement-support advisor) | The component (`osteoquant/advisor/`, version 1.2.1) that decides, before reporting, whether each endpoint is supported for the material and scan |
| **Allograft** | Bone from another individual of the same species; bone-derived, so never separable from new bone by intensity |
| **Anchor** | The sequence number and head hash of the audit trail, recorded outside the project so that truncation of recent events can be detected |
| **Audit trail** | Append-only, SHA-256 hash-chained log of every action in a project |
| **AUROC** | Area under the receiver-operating-characteristic curve; 0.5 is chance, 1.0 perfect |
| **Autograft** | The animal's own bone used as graft; identical in material to host and new bone |
| **β-TCP** | Beta-tricalcium phosphate, a resorbable calcium-phosphate ceramic |
| **BCP** | Biphasic calcium phosphate (HA plus β-TCP) |
| **Bland–Altman analysis** | Agreement analysis reporting the mean difference (bias) and 95% limits of agreement (LoA) between two methods |
| **Bone-derived graft** | Allograft, autograft, xenograft (DBBM) and DBM; chemically bone-like |
| **Bridging** | Fraction of ROI cross-sections, along the defect axis, containing a connected mineral path from host to host |
| **BV/TV** | Bone volume fraction: new-bone volume divided by ROI volume |
| **Conn.D** | Connectivity density, (1 − Euler characteristic) / TV, per mm³ |
| **Creeping substitution** | Replacement of resorbing graft by new bone in the same place; the day-0 footprint counts this bone as graft |
| **Data class** | Whether a result comes from synthetic phantoms (SYNTHETIC), real public data (REAL) or is an assumption or hypothesis. Every quantitative claim names it |
| **Day-0 scan** | A scan taken at implantation, before new bone forms, used to locate the original graft |
| **Day-0 footprint** | The graft mineral on the day-0 scan, propagated by registration to later scans |
| **DBBM** | Deproteinised bovine bone mineral (a xenograft) |
| **DBM** | Demineralised bone matrix; near-radiolucent but bone-derived |
| **DefectFill report** | OsteoQuant's study report (PDF and CSV) with per-specimen endpoints, images, QC and suppressed endpoints |
| **Deterministic QC check** | A fact about the file (spacing, missing slices, saturation); compare *heuristic QC check* |
| **Dice coefficient** | Overlap between two segmentations: twice the shared volume divided by the sum of both volumes; 1 is perfect. OsteoQuant ranks models on volume error first, Dice second |
| **Edge / background convention** | Two ways of treating the analysis-region border in thickness computation; `edge` is the pre-registered primary convention |
| **Evaluation mode** | How the application runs without a valid licence: all functions, watermarked reports |
| **Experiment IDs** | A–P (Generation 1), S1/S1b/S1c, F2, L3, L4, S2, U1, O2 (Generation 2); listed in EXPERIMENT_REGISTRY.md |
| **Failed measurement** | In simulation experiments: graft-volume error >20% or graft Dice <0.8 |
| **Graft share** | Residual graft as a fraction of mineral in the ROI; the advisor requires support at the estimated share and at half of it, and refuses graft volume below 5% |
| **HA** | Hydroxyapatite, the mineral of bone and a synthetic ceramic graft |
| **HA calibration** | Scanning a phantom of known hydroxyapatite densities so that grey values convert to mgHA/cm³ |
| **HD95** | 95th-percentile Hausdorff distance between segmentation surfaces |
| **Heuristic QC check** | A score with a developer-chosen threshold that flags a scan for attention; not an established standard |
| **Host bone** | Pre-existing bone around the defect (label 3) |
| **ICC(2,1)** | Intraclass correlation, two-way random effects, absolute agreement, single measurement |
| **Intensity-only oracle** | The best possible voxel-wise intensity rule for given class distributions; an upper bound for every threshold workflow |
| **Mineral rule** | The advisor's check (since 1.2.0) that new bone can be separated from soft tissue including partial-volume halos; it gates mineral and new-bone endpoints |
| **Multi-Otsu** | Classical multi-level automatic thresholding; the desktop's default segmentation |
| **New bone** | Bone formed after implantation inside the defect ROI (label 1) |
| **Noise (relative)** | Noise standard deviation divided by the host-bone minus soft-tissue grey-level contrast; mineral endpoints need <0.35 |
| **Not measured** | How an unsupported endpoint appears in results and reports |
| **ONNX Runtime** | An inference engine that runs exported models without PyTorch |
| **OOD** | Out-of-distribution: data unlike the training data |
| **Partial-volume effect** | Voxels straddling two materials take intermediate grey values |
| **Pre-registration** | Writing down analysis conventions and acceptance criteria before the data are seen |
| **Project** | A folder containing `osteoquant-project.json`, `osteoquant.db` and `data/` |
| **Radiolucent** | Nearly invisible to X-rays (attenuation close to soft tissue), e.g. collagen sponge, PLGA, PCL |
| **Registration QC** | Check that the alignment of a later scan to day 0 is good enough: block-wise residual displacement ≤2 voxels |
| **Relative mineral units** | r = (x − soft tissue)/(host bone − soft tissue); soft tissue ≈ 0, host bone ≈ 1 |
| **Reported metrics** | The metrics view used by reports and exports, with unsupported endpoints blanked |
| **Residual graft** | Graft material still present in the defect (label 2) |
| **Revision** | A saved segmentation version; corrections never overwrite earlier versions |
| **ROI** | Region of interest; here the defect volume in which endpoints are computed. TV is its volume |
| **Self-test** | `--selftest`: an 8-step end-to-end check of an installation |
| **Stage A–F** | The validation programme: computational, ex vivo phantom, material characterisation, retrospective partner data, prospective pilot with histology, independent multi-site |
| **Supported / supported with conditions / not supported** | The three endpoint statuses from the advisor; the desktop summarises a scan as *supported*, *flagged* or *not supported* |
| **Synthetic phantom** | A computer-generated defect with exact ground-truth labels, imaged by a simulator |
| **Tb.N** | Trabecular number, 1/(Tb.Th + Tb.Sp), per mm |
| **Tb.Sp** | Trabecular separation: local thickness of the space between new-bone structures, µm |
| **Tb.Th** | Trabecular thickness by sphere fitting (Hildebrand–Rüegsegger), µm |
| **TMD** | Tissue mineral density, mgHA/cm³; reported only with HA calibration |
| **TV / TV<sub>certain</sub>** | ROI volume; ROI volume minus uncertain voxels |
| **Uncertain voxel** | Voxel whose maximum class probability is below τ = 0.6 (label 255); only probabilistic methods produce them |
| **Voxel spacing** | Physical size of a voxel in µm (z, y, x); must come from the file or be confirmed at import |
| **Watermark** | Text printed on reports from unlicensed (EVALUATION COPY) or test-licensed (TEST LICENCE) installations |
| **Xenograft** | Graft from another species, here DBBM |
