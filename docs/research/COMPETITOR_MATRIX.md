# OsteoQuant: Competitor Capability Matrix

**Prepared:** 2026-11-27. **Scope:** software and services that could deliver (or substitute for) OsteoQuant's promise: offline micro-CT analysis that separates new bone, residual graft and host bone in a defect, with morphometry, longitudinal day-0 registration, uncertainty-aware abstention, an audit trail and study reports.
**Machine-readable matrix:** `docs/research/competitor_matrix.csv`: 39 rows (38 competitors plus OsteoQuant) × 40 dimensions = 1,560 cells. Each cell has a value, an evidence tag, a source URL and an access date.
**Supersedes for capability comparison:** `docs/research/competitors.csv`. That file and `docs/research/COMPETITOR_INTELLIGENCE.md` remain the narrative history.

> No vendor was contacted. Nothing was signed up for, bought or downloaded (other than public web pages and public PDFs). Absence statements mean "not found in the sources reviewed". They do not mean the product lacks the feature.

## 1. Method and evidence tags

| Tag | Meaning in this matrix |
|---|---|
| **V** | Verified this session from a primary source: a vendor page, a release-notes PDF, a manual, a paper via Crossref or Europe PMC, or OsteoQuant's own source code. Quotes or close paraphrases. "Not mentioned [V]" means the fetched primary page was read and does not mention the feature. |
| **CC** | Company claim that was not independently tested (e.g. "complies with Part 11"). Also used for facts carried from the earlier pass (`COMPETITOR_INTELLIGENCE.md`, same date) that were **not re-fetched**; those cells say "(prior pass; not re-fetched)". |
| **INF** | Analyst inference from verified facts (e.g. "desktop, implied"). |
| **U** | Unknown. Not found in the sources reviewed. The cell cites the page that was checked. |

**Cell counts:** V 338 · CC 26 · INF 60 · U 1,136.

Most cells are U because vendor pages rarely state negatives, and absence is not evidence. The U cells are the verification backlog (Section 7), not a finding that the features are missing.

**Pages that could not be read this session:**
- **Blocked:** NAMSA (HTTP 403), Revvity Quantum GX2 product page (403), Dragonfly help site (bot check), PubMed (cookie wall; Europe PMC and Crossref were used instead).
- **No product page found:** Siemens Inveon Research Workplace, Medtronic PRL, Alizée/StageBio service details.

**The 40 dimensions** (codes in the CSV):
- category, vendor/owner, input formats, native micro-CT raw formats, 3D visualisation
- classical segmentation, trainable DL segmentation, pretrained bone models
- graft vs new-bone vs host separation, graft-material awareness, implant/osseointegration metrics
- longitudinal registration, baseline (day-0) graft propagation
- morphometry indices, morphometry standard referenced, density calibration, defect-ROI automation
- histology correlation, uncertainty output, abstention/refusal, scan QC
- audit trail, e-signature/review, Part 11 claim, GLP claim, validation services (IQ/OQ/PQ)
- reporting, study/batch management, group statistics, scripting/API
- platform/OS, deployment (offline/cloud), licence model, published prices, regulatory statement
- target users, strengths, weaknesses for the graft use case, analysis services offered
- threat to OsteoQuant (judgement, always INF)

## 2. Condensed matrix (12 decision-relevant dimensions)

`—` = not found in the sources reviewed [U]. Cells are truncated; see the CSV for the full text and source URL of every cell.

| Competitor | dl_segmentation_trainable | pretrained_bone_models | graft_vs_newbone_vs_host_separation | longitudinal_registration | baseline_day0_graft_propagation | uncertainty_output | abstention_or_refusal | audit_trail | part11_claim | glp_claim | reporting | published_prices |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OsteoQuant (this project, research prototype) | Own small 3D U-Net (CPU) and random forest; trainable [V] | Synthetic-trained 3-class models only, watermarked; dog-forelimb bone… [V] | 3-class new bone / residual graft / host; validated only in simulation [V] | Rigid registration (SimpleITK) to day-0, TRE tooling [V] | Yes: day0_propagation of registered graft footprint (simulation only) [V] | TTA softmax, predictive entropy, mutual information, risk-coverage [V] | Voxel abstention (tau) + plausibility checks; ROI detector raises exc… [V] | Append-only SQLite with SHA-256 hash chain and anchor verification [V] | Explicitly not claimed [V] | Explicitly not claimed [V] | DefectFill PDF/CSV report with model hashes, exceptions [V] | None [V] |
| Bruker 3D.SUITE (CTAn, CTVox, CTVol, DataViewer, NRecon, 3DxSUITE) | Not mentioned on product page [V] | Not mentioned; Bruker application scientist co-authored DL tibia fram… [V] | Threshold pipeline for 'defect healing with biomaterials' in 2017 web… [CC] | Not mentioned; DataViewer offers 'Differential image analysis between… [V] | — [U] | — [U] | — [U] | Not mentioned [V] | Not mentioned [V] | Not mentioned [V] | Not mentioned [V] | None [V] |
| MOLECUBES X-CUBE (a Bruker company) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| SCANCO Medical Evaluation / IPL (+ scan services) | Not mentioned [V] | Not mentioned [V] | Not mentioned [V] | 'Image Registration (3D)' / 'volume registration' [V] | — [U] | — [U] | — [U] | 'Evaluation log (for later retrieval)' [V] | Not mentioned [V] | Not mentioned [V] | Flexible database reporting (individual measurement or study) [V] | None [V] |
| Dragonfly 3D World 2027.1 (Comet Technologies Canada; formerly ORS) | Segment with AI: Grid-based SAM, Cellpose-SAM, 2.5D/3D deep classific… [V] | 'UniversalJawSeg' ready-to-use model (enamel, dentin, bone) [V] | No graft preset found; 'implant bone regrowth interdigitation' assess… [V] | Automatic mesh registration (scan-to-CAD); no longitudinal bone workf… [V] | — [U] | Confidence filtering of SAM instances only [V] | — [U] | No occurrence of 'audit' in 2027.1 release notes (text search) [V] | No occurrence of 'Part 11' / '21 CFR' in release notes [V] | No occurrence of 'GLP' in release notes [V] | Report Builder PDF/HTML (Word on full licence); LaTeX Report Generato… [V] | Academic: free of charge; commercial not published [V] |
| Thermo Fisher Amira / Avizo 3D (+ BONe tools) | AI-Assisted Segmentation: train shallow or deep models from ROI sets;… [V] | BONe BP-2D-03a bone vs medullary pores, mean IoU ~91% (5-fold CV) [V] | Not mentioned; BONe has no graft/implant class [V] | Overlay and register multiple imaging data types [V] | — [U] | — [U] | — [U] | Not mentioned [V] | Not mentioned [V] | Not mentioned [V] | Not mentioned [V] | None [V] |
| ZEISS arivis Pro / arivis Cloud / ZEN core GxP Toolkit (+ Dragonfly ZEISS edition) | ML/DL operators locally; cloud training; open-source model import [V] | Cellpose-SAM foundation model; pretrained spine detection (not bone) [V] | — [U] | — [U] | — [U] | — [U] | — [U] | ZEN core GxP: 'Audit Trail Tool for complete tracking of all changes'… [V] | ZEN core GxP: 'Compliance with CFR21 Part 11 and EU Annex 11' [CC] | ZEN core GxP lists GLP among standards [CC] | 3D/video export for reports (arivis) [V] | None on page [V] |
| Simpleware (Synopsys / Ansys) | Not mentioned on product page [V] | Automatic cancellous bone segmentation for femurs (2025.06) (prior pa… [CC] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | None [V] |
| VGSTUDIO MAX (Hexagon Volume Graphics) | 'Deep segmentation brings AI-powered segmentation to more users' [V] | — [U] | — [U] | 3-2-1 / simple alignment; nominal-actual comparison [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | Reports with images, histograms, tables; Q-DAS integration [V] | None [V] |
| Materialise Mimics Innovation Suite | Cloud component with 'AI-enabled segmentation' [V] | Bone segmentation tutorials; AI anatomy (clinical) [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | None [V] |
| Analyze 15 + BMA add-on (AnalyzeDirect) | Not mentioned [V] | — [U] | — [U] | Inter- and intra-modality registration [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | None [V] |
| Revvity Quantum GX2/GX3 software + Living Image Synergy AI (+ Analyze 14 for Quantum) | Synergy AI: 'AI algorithms automate image segmentation and ROI quanti… [CC] | Bone not mentioned in Synergy AI release [V] | — [U] | Longitudinal in vivo serial scans (acquisition); registration not des… [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | None (product page returned 403) [U] |
| Rigaku CT Lab HX / MILabs (Rigaku Group) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| Siemens Inveon Research Workplace | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| VivoQuant 6.0 (Perceptive) | AI not mentioned [V] | — [U] | Bone not mentioned [V] | Multi-atlas registration [V] | — [U] | — [U] | — [U] | — [U] | Not stated [V] | — [U] | ROI metric tables, histograms, publication-ready images [V] | — [U] |
| Imalytics Preclinical (Gremse-IT; distributed by Scintica) | AI not mentioned on distributor page [V] | — [U] | — [U] | Manual or marker-based fusion [V] | — [U] | — [U] | — [U] | Not described [V] | — [U] | — [U] | — [U] | None; quote [V] |
| MicroView (Parallax Innovations) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | None [V] |
| 3D Slicer (+ extensions: MONAI Label, DeepInfer, SlicerMorph) | MONAI Label, NVIDIA Clara, DeepInfer; TensorFlow/MONAI compatible [V] | — [U] | — [U] | Manual and automatic registration [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | Free [V] |
| Fiji/ImageJ + BoneJ2 (+ BoneJ Headless) | — [U] | — [U] | Graft/implant handling not mentioned [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | Free core; BoneJ+ token prices not on page [V] |
| ITK-SNAP | 'new AI features in v4.4.0'; Distributed Segmentation Service [V] | — [U] | — [U] | Manual and automatic registration [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| MITK Workbench | nnInteractive (v2.5), TotalSegmentator (v2.14) [V] | — [U] | Nothing bone- or micro-CT-specific [V] | Rigid and deformable registration across time points [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| napari (+ plugins) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| nnU-Net v2 / MONAI-based academic pipelines | Auto-configured 2D/3D U-Net training [V] | No downloadable pretrained weights described on README [V] | Best model in Mg-implant residual/degradation/bone benchmark (SRµCT) [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| BONe (Midwestern Univ.; runs in Amira/Avizo + standalone) | DLFit (train/fine-tune), DLPred (predict), IoU (score) [V] | BP-2D-03a bone vs pores, IoU ~91% [V] | No graft/implant class [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| Aivia (Leica Microsystems) | Enhance, segment and predict with AI tools [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| Imaris (Oxford Instruments) | 'Imaris AI' named; details not on page [V] | — [U] | CT/bone not mentioned [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| Charles River Laboratories (orthopedic device testing + digital pathology) | Machine/deep learning image analysis via Patholytix and Visiopharm (p… [V] | — [U] | Bone repair models incl. orthobiologics and 'evaluation of bone subst… [V] | — [U] | — [U] | — [U] | — [U] | — [U] | '21 CFR Part 11-compliant custom algorithm development for quantitati… [CC] | GLP assessments; Visiopharm GLP-compliant at DUR, EDI, EVR; Patholyti… [CC] | Quantitative pathology reports [V] | — [U] |
| Inotiv / Histion (histomorphometry) | — [U] | — [U] | 'Percent residual implant material as a function of a defined ROI'; '… [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | GLP not mentioned on page [V] | — [U] | — [U] |
| NAMSA (orthopedics CRO) | — [U] | — [U] | Bone ingrowth / osseointegration endpoints (prior pass; not re-fetche… [CC] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| StageBio (merged with Alizee Pathology, 2019) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | 'GLP-compliant research and preclinical histology' (press snippet) [CC] | — [U] | — [U] |
| Medtronic Physiological Research Laboratories (internal preclinical unit) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | GLP quality standards (job posting) [INF] | — [U] | — [U] |
| Labcorp nonclinical micro-CT | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | GLP not mentioned [V] | Complete dataset, tabular data and report; 1-2 week turnaround (ex vi… [V] | — [U] |
| Academic micro-CT cores (example: HSS, Scanco uCT35) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | $75/h NIH, $100/h academic, $200/h corporate; $25/h self-analysis [V] |
| BIOQUANT (Measurement/OSTEO + Ai Suite, Spring 2027) | Ai Suite 'Stitch, Convert, Segment' releasing Spring 2027 [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | 'Request Pricing' [V] |
| Visiopharm (digital pathology) | — [U] | — [U] | Healing allograft new bone / cartilage / fibrosis on WSI (Zhang 2016) [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | GLP-compliant at Charles River sites (per Charles River) [CC] | — [U] | — [U] |
| NeuroSimplicity (micro-CT analysis solutions) | — [U] | — [U] | Graft/implant not mentioned [V] | — [U] | — [U] | — [U] | — [U] | 'Deterministic, auditable batch processing across cohorts' [CC] | — [U] | — [U] | — [U] | — [U] |
| Artikode (AI for bone, Valencia region partners) | AI-driven models for preclinical bone tissue images [V] | — [U] | Grafts/implants not mentioned [V] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| Academic graft/scaffold pipelines (Beitlitum 2024; Ganeshaaraj 2022; Aboutaleb 2026 UIUC) | — [U] | — [U] | Beitlitum: Amira thresholds + manual refinement, new bone vs xenograf… [V] | Ganeshaaraj 3-stage pipeline (abstract mentions registration-related … [INF] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |
| Evergen + University of Florida (human graft QC, internal) | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] | — [U] |

## 3. What the evidence shows

1. **Learned segmentation is now commodity in general 3D platforms.**
   - **Dragonfly 2027.1** (release notes dated 2026-10-05, read in full this session) ships Grid-based SAM, Cellpose-SAM, 2.5D/3D deep classification and a Report Builder (PDF/HTML; Word on full licences). Its LaTeX Report Generator covers Bone Analysis wizard reports [V].
   - **Amira/Avizo 2024.2** trains shallow or deep models from ROI annotations, with multi-material VGG16/19 predictions [V].
   - **BONe** (Thermo blog, 2026-11-17) gives Amira/Avizo users trainable bone-vs-pore models with ~91 % IoU [V].
   - **ZEISS arivis Pro** imports open-source models and runs Cellpose-SAM [V]. **MITK** bundles nnInteractive and TotalSegmentator [V].
   - "Uses deep learning" is therefore not a differentiator.
2. **No product was found that ships a graft vs new-bone vs host-bone model or preset for micro-CT.** This holds across 38 entities [V/U].
   - The closest commercial signals are Dragonfly's "implant bone regrowth interdigitation" [V] and Revvity GX3's osseointegration workflow: bone-implant contact, peri-implant bone volume, ingrowth into lattices [CC].
   - Bruker's 2017 "defect healing with biomaterials" threshold pipeline [CC, prior pass] is the other.
   - All three are implant/osseointegration oriented. None separates a **resorbing, bone-like graft** from new bone.
3. **Graft-vs-new-bone separation is done today by three routes:**
   - (a) manual or threshold work in Amira, e.g. Beitlitum 2024 used "grayscale thresholds with appropriate manual refinement" with coaxial regions [V];
   - (b) academic CNN/U-Net pipelines for scaffolds: Ganeshaaraj 2022 (bioactive-glass scaffold/bone/pores) [V] and Aboutaleb 2026 (UIUC, ΔBGF endpoint metric) [V];
   - (c) histology at CROs: Inotiv sells "percent residual implant material as a function of a defined ROI" [V].
4. **Compliance features exist in adjacent markets but were not found in any micro-CT analysis product.**
   - ZEISS ZEN core GxP Toolkit (microscopy) advertises an audit trail, electronic signatures, "Compliance with CFR21 Part 11 and EU Annex 11" and IQ/OQ services [V page; compliance is CC].
   - Charles River advertises "21 CFR Part 11-compliant custom algorithm development" and GLP-validated Patholytix/Visiopharm [CC].
   - In micro-CT, Scanco has an "Evaluation log" and "Secure password and file protection" [V]. The Dragonfly 2027.1 release notes contain none of the strings audit, signature, Part 11, 21 CFR or GLP [V, text search]. Bruker's 3D.SUITE page mentions none of them [V].
5. **Longitudinal work is generic registration, not graft-footprint propagation.**
   - Scanco lists 3D image registration [V]. Analyze, MITK, Slicer and ITK-SNAP offer rigid/deformable registration [V]. Dragonfly's new registration is mesh-to-CAD [V].
   - The academic time-lapse literature registers consecutive scans and derives formation/resorption sites (Schulte 2011, doi:10.1016/j.bone.2010.10.007; Wehrle 2019, doi:10.1038/s41598-019-53822-x [V]). Wehrle builds VOIs from the post-operative scan.
   - No product was found that propagates a day-0 graft mask to label later mineral as residual graft vs new bone. The patent landscape (`docs/ip/PATENT_LANDSCAPE.md`) shows Nobel Biocare's active US9036899B2 on registered CT volume-change quantification, so the concept area is not empty.
6. **No product was found that exposes uncertainty or abstains on bone measurements.** Dragonfly filters SAM instances by confidence only [V]. The patent literature (GE, Sandia, EchoNous, Siemens) shows uncertainty gating is an active IP area.
7. **Prices are almost never published.**
   - Published: Dragonfly academic licence "free of charge" (non-commercial only) [V]; HSS core rates of $75/$100/$200 per hour and $25/h self-analysis [V]; 3D Slicer, BoneJ2, MITK and nnU-Net free [V].
   - Quote-only or trial-only: Bruker, Scanco, Avizo, arivis, Mimics, Analyze (14-day trial), VGSTUDIO (4-week trial), Imalytics, Bioquant [V].

## 4. Positioning gaps (white space)

These are judgement calls [INF] from the matrix. Each holds only "as far as public materials show".

| Gap | Evidence | How OsteoQuant could occupy it |
|---|---|---|
| **G1. Graft-aware three-class µCT endpoints with explicit "cannot separate" output** | No graft preset/model found in any product [V/U]. No product abstains [U]. | Material × timepoint separability verdict + abstention + "mineralized tissue" fallback reporting |
| **G2. Day-0 graft footprint protocol as a productised study design** | Academic time-lapse methods exist [V]. No product found [U]. | Study-design guidance + analysis. In simulation it kept graft Dice 0.816 where intensity oracle was 0.323 (`EXPERIMENT_REGISTRY.md`, L2) |
| **G3. Audit trail + review sign-off inside micro-CT analysis** | GxP layers exist only in microscopy (ZEISS), pathology (Patholytix, HALO) and CROs [V/CC]. Nothing found in Bruker/Scanco/Dragonfly/Avizo [V] | Hash-chained audit, object-hash-bound review, model/ROI hashes in report. Do **not** claim Part 11 compliance (not validated) |
| **G4. Pre-study feasibility ("can µCT see my graft at my voxel size?")** | No vendor offers it [U]. Academic papers report method accuracy after the fact [V] | Known-truth phantom benchmark per material (needs physical phantoms) |
| **G5. Vendor-neutral, sponsor-facing reporting for small orthobiologic firms** | CROs own sponsor reports [V]. Cores deliver spreadsheets/short reports [V prior/HSS] | DefectFill report with group statistics at animal level |

## 5. Where OsteoQuant is clearly weaker (do not hide these)

| Area | Competitor evidence | OsteoQuant today |
|---|---|---|
| **Validation on real grafts** | Vendors have years of field use. Scanco/CTAn are de-facto references. IPL vs CTAn cross-software study (Mys 2021) [V] | Three-class results are **simulation-only**. No real graft scan is labelled (`EXPERIMENT_REGISTRY.md`) [V] |
| **Native format breadth** | Dragonfly full licence reads Bruker `.log`, Scanco `.aim`, Nikon, Rigaku, Yxlon [V]. BoneJ reads Scanco ISQ via SCIFIO [V] | No Scanco ISQ/AIM reader in `osteoquant/io/readers.py` [V]. Bruker supported only as reconstructed slice folders |
| **DL scale and foundation models** | SAM/Cellpose-SAM (Dragonfly, arivis), GPU DL (Avizo needs CUDA) [V] | CPU-only small U-Net. ~34 min per 100 M voxels (Exp O) [V] |
| **Visualisation and UX maturity** | Commercial 3D engines (Dragonfly, Avizo, arivis, Aivia teravoxel) [V] | Browser viewer prototype [V] |
| **Registration** | Rigid + deformable in MITK/Slicer/Analyze [V] | Rigid only [V] |
| **Implant metrics** | Revvity GX3 lists BIC, bone-implant distance, peri-implant volume [CC]. Charles River lists BIC [V] | No BIC metric [V] |
| **Histology** | Visiopharm validated allograft histology algorithm (Zhang 2016) [V]. Bioquant Ai Suite Spring 2027 [V]. Inotiv residual-implant histomorphometry [V] | Histology module weak (bone-area ICC 0.35, Exp N) [V] |
| **Compliance credibility** | ZEISS sells IQ/OQ and claims Part 11 [V/CC]. Charles River claims Part 11 algorithm development [CC] | Technical controls only. No validation package, no CSV/IQ-OQ [V] |
| **Distribution and trust** | Scanner bundling (Bruker, Scanco, Revvity). CRO sponsor relationships [V/INF] | No customers, one founder, not incorporated [V] |
| **Price at the low end** | Dragonfly academic free [V]. Slicer/BoneJ/nnU-Net free [V]. HSS self-analysis $25/h [V] | Must justify paid service vs free DIY |

## 6. Top competitive threats (ranked judgement, INF)

1. **Comet Dragonfly**: fastest-moving platform (SAM, 3D DL, Report Builder, vendor raw formats, free academic licence). A bone-regeneration preset plus Session Viewer would cover most of OsteoQuant's academic value. Compliance terms are absent today [V].
2. **Charles River and other large CROs**: own the sponsor and the GLP framework, already claim Part 11 algorithm development [CC], and run bone-substitute models with micro-CT [V]. They are the likeliest builders of an in-house graft algorithm and also the best channel.
3. **Bruker (CTAn/3D.SUITE + MOLECUBES)**: installed base and de-facto morphometry. Its application staff co-author DL bone papers [V]. A bundled DL release would reset buyer expectations.
4. **Thermo Fisher Amira/Avizo + BONe**: trainable multi-material DL with an academic bone-model community [V]. Adding biomaterial classes is a small step.
5. **Revvity (Quantum GX3 + Living Image Synergy AI)**: integrated scanner + AI + osseointegration metrics marketed for "regulatory submissions" [CC]. A graft workflow would reach longitudinal in vivo users directly.

**Watch list:**
- NeuroSimplicity: markets "deterministic, auditable batch processing" for preclinical micro-CT [CC].
- Open nnU-Net DIY by customers [V].
- Academic scaffold-ingrowth pipelines (UIUC 2026) [V].
- Bioquant/Visiopharm on the histology side [V].

## 7. Verification backlog (highest value U cells)

1. Bruker CTAn current manual: OS, registration, reporting, any audit/user log. The product page is silent [V].
2. Dragonfly Bone Analysis help page: re-read when the bot check clears. Bouxsein indices are currently CC from the prior pass.
3. Scanco: whether the evaluation log is append-only or attributable, and Part 11 status.
4. Revvity GX3 / Synergy AI: reporting, audit trail, whether bone models exist (product page 403).
5. NAMSA, StageBio, Medtronic PRL: service sheets.
6. BONe licence (Dryad) before any reuse.
7. Siemens Inveon Research Workplace: current status (no product page found).

## 8. Sources

Every cell's URL is in `competitor_matrix.csv`. Principal primary sources fetched this session (2026-11-27):
- Bruker 3D.SUITE page; Scanco analysis page and spec sheet (V8/8-2021 PDF); Dragonfly 2027.1 release notes PDF, life-sciences page, academic-licence page, what's-new page
- Amira/Avizo 2024.2 release notes PDF and Avizo page; Thermo BONe blog (2026-11-17); ZEISS arivis Pro and ZEN core GxP Toolkit pages
- Ansys/Synopsys Simpleware page; VGSTUDIO MAX page; Mimics Innovation Suite page; AnalyzeDirect home page
- Revvity GX3 osseointegration technical brief PDF and Synergy AI release; Rigaku CT software blog; MILabs and MOLECUBES home pages
- VivoQuant page; Imalytics Preclinical (Scintica) page; MicroView (Parallax) page; 3D Slicer, BoneJ, ITK-SNAP, MITK, napari pages; nnU-Net GitHub README
- Aivia and Imaris home pages
- Charles River orthopedic-device and digital-pathology pages; Inotiv histomorphometry page; Labcorp CT page; HSS micro-CT core page
- Bioquant 2027 page; NeuroSimplicity and Artikode pages
- Crossref/Europe PMC records for every cited DOI: Aboutaleb 2026, Ganeshaaraj 2022, Beitlitum 2024, Hopkinson 2023, Marinho 2024, Lee 2025/26 (BONe), Lagzouli 2025 ×2, Zhang 2016, Mys 2021, Bouxsein 2010, Domander 2021, Isensee 2020, Wehrle 2019, Schulte 2011
