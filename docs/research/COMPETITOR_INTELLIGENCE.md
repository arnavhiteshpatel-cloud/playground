# OsteoQuant — Competitor Intelligence

**Research date:** 2026-11-27 · **Scope:** preclinical bone-defect micro-CT (and later histology) quantification for orthobiologic / bone-graft companies, preclinical CROs, implant makers, and academic bone labs.
**Companion file:** `docs/research/competitors.csv` (one row per competitor).

## Evidence tags

| Tag | Meaning |
|---|---|
| **[V]** | Verified on a primary or near-primary page fetched during this research (URL given) |
| **[CC]** | Company claim (marketing, press release, vendor blog) — URL given, not independently verified |
| **[RF]** | Published research finding (DOI / PMID / URL) |
| **[PK]** | Prior knowledge, not re-verified in this session |
| **[UNR]** | Unresolved: searched and could not confirm either way |

**Rules applied.** Absence statements are written as "not found in public materials" — never as "lacks". No prices are given unless a page stating them was fetched. **The founder playbook is not in this repository.** Only the three playbook claims quoted in the brief were checked (Section 4).

---

## 1. Summary table

Threat = how directly the player could deliver OsteoQuant's core promise (three-class new bone / residual graft / host bone in a defect ROI, plus validated endpoints, audit trail and report) within about 12–24 months. This is the analyst's judgement.

| Competitor | Category | Learned / DL segmentation | Bone morphometry | Graft vs new bone (3-class) | Report output | Audit trail / Part 11 | Price public? | Threat |
|---|---|---|---|---|---|---|---|---|
| **Dragonfly 3D World** (Comet Technologies Canada, ex-ORS) | General 3D platform | Yes: DL Tool, Segmentation Wizard, SAM, Cellpose-SAM, 3D classifier [V] | Bone Analysis module, Bouxsein indices, Kohler/Buie cortical–trabecular split [V] | Not found as a preset. Its generic multi-class DL could be trained for it [V/PK] | Report Builder PDF/HTML (Word on full license); LaTeX Report Generator for Bone Analysis [V] | Not found [V: not in 2027.1 release notes] | No. Academic license free but restricted [V] | **High** |
| **Amira / Avizo** (Thermo Fisher) + **BONe** | General 3D platform | AI-Assisted Segmentation (shallow/deep, multi-material); DL training modules; BONe DLFit/DLPred/IoU [V] | XImagePAQ bone extension [CC] | Not found as a preset | Not verified | Not found | No | **High** |
| **CTAn / CTVox / NRecon / DataViewer** (Bruker 3D.SUITE) | Scanner-vendor software | Not found. Thresholding and morphology plug-ins [V] | Yes, de-facto standard for 3D morphometry [V/PK] | Threshold-based "defect healing with biomaterials" pipeline [CC]. No learned 3-class model found | Datasheets / BatMan output [PK] | Not found [UNR] | Not found (bundled with scanners [PK]) | Medium (incumbent, owns workflow) |
| **Scanco IPL / Evaluation** | Scanner-vendor software + services | Not found [V] | Yes: standard trabecular/cortical scripts, µFE [V] | Not found | Database reporting, evaluation log [V] | Password/file protection, evaluation log. Part 11 not found [V] | No | Medium |
| **ZEISS** (Xradia ART, arivis Pro/Cloud, ZEN core GxP, Dragonfly ZEISS ed.) | Scanner vendor + software | DeepRecon/DeepScout (reconstruction) [V]; arivis Cloud DL training, ONNX import [CC] | Via Dragonfly ZEISS edition Bone module [V] | Not found | — | ZEN core GxP: audit trail + e-signatures [CC] (not shown for arivis or Xradia) | arivis Cloud free student tier; others quote-only [CC] | Medium |
| **Revvity Living Image Synergy AI** (+ Analyze for Quantum CT) | Scanner vendor software | AI segmentation and ROI quantification across optical/µCT/US [CC] | Not shown for bone [CC] | Not found | — | Not found | No (trial available) | Low–Medium |
| **Analyze 15 + BMA add-on** (AnalyzeDirect) | 3D platform | Not found | BMA add-on: cortical/trabecular, BMD [V/CC] | Not found | — | Not found | No (14-day trial) [V] | Low |
| **VivoQuant** (Perceptive) | Preclinical multimodal | Atlas-based, not AI [V] | Not found | Not found | Scripting / worklists [V] | Not found | No | Low |
| **BoneJ2 / BoneJ Headless** | Open source | No | Thickness, Conn.D, DA, EF, SMI etc. [V] | No | — | No | Free (BSD-2 / CC0). BoneJ+ paid add-on [V] | Reuse, not a threat |
| **Fiji, 3D Slicer, ITK-SNAP, napari, nnU-Net, MONAI** | Open source | nnU-Net/MONAI are SOTA trainers [RF/PK] | Via BoneJ | No | — | No | Free [V license files] | Reuse. Also enables in-house DIY |
| **Bioquant (Measurement / OSTEO)** | Histomorphometry | "BIOQUANT Ai Suite" (Stitch/Convert/Segment), Spring 2027 [V] | ASBMR/BMAS nomenclature templates [V] | Not found | — | Not found | Quote. Ai Suite included with Technical Service Plan [V] | Medium (histology phase) |
| **OsteoMeasure** (OsteoMetrics) | Histomorphometry | Not found (largely manual tracing) [RF] | Static + dynamic histomorphometry [RF] | Not found | — | Not found [UNR] | Not found | Low |
| **Visiopharm** | Digital pathology | DL APPs, AI module [V/RF] | Osteoclast Oc.S/BS app protocol [RF]; allograft new bone/cartilage/fibrous algorithm [RF] | **Histology yes** (allograft healing), micro-CT no [V formats doc] | — | Used GLP-compliant at 3 Charles River sites [CC] | Not found | Medium–High (histology) |
| **Deciphex Patholytix Preclinical** | Digital pathology (tox) | Patholytix AI module [CC] | Not found | Not found | — | Claims Part 11 / GAMP 5 [CC]; GLP-validated at Charles River [CC] | Not found | Low–Medium |
| **Aiforia** (Create / Studies) | Digital pathology (cloud) | Train-your-own DL [CC] | Not found | Not found | — | Studies module "within GLP framework", immutable study data [V press release] | Not found | Low–Medium |
| **HALO / HALO AI / HALO Link** (Indica Labs) | Digital pathology | HALO AI DL [CC] | Not found | Not found | — | HALO Link Compliance Add-on: system-wide audit, reason-for-change [V] | Not found | Medium (histology) |
| **Charles River** | CRO | In-house; Visiopharm, Patholytix [CC] | Manual + software histomorphometry [V] | Bone-substitute models [V] | Quantitative reports [V] | Offers "21 CFR Part 11-compliant custom algorithm development" [V] | Not found | **High** (owns the customer) |
| **NAMSA** | CRO (devices) | Not found | micro-CT, histomorphometry [CC] | Bone ingrowth / osseointegration endpoints [CC] | — | GLP [PK] | Not found | Medium (channel or competitor) |
| **Inotiv / Histion** | CRO (devices) | Not found | Histomorphometry "on validated systems" [V] | **% residual implant material in ROI** [V] | — | Histion "GLP compliant" [CC] | Not found | Medium |
| **AccelLAB, Altasciences, CSU PSRL, Labcorp** | CROs | Not found | Varies | AccelLAB/PSRL: graft models [V/CC] | — | PSRL GLP (21 CFR 58) [V] | Not found | Channel |
| **Academic µCT cores** (BIDMC, HSS, Rush…) | Fee-for-service | Not found | Yes, Scanco-based [V] | Not found | Spreadsheet + short report [V] | Not found | **HSS fees published** [V] | Low–Medium (cheap substitute) |
| **Evergen + UF** | Adjacent (human graft QC) | "AI-powered" CT bone-graft analysis [CC] | Density/structure [CC] | Not preclinical | Reports in < 10 s [CC] | Not found | — | Low (adjacent) |

---

## 2. Most decision-relevant findings

1. **No vendor or startup was found shipping a locked, validated three-class model (new bone / residual graft / host bone) for preclinical micro-CT.** Searches covered vendor sites, press, PubMed and startup-oriented web queries. Closest: academic CNNs for scaffold/bone/pore segmentation (EMBC 2022, Dice 90.1) [RF] and nnU-Net four-class Mg-implant segmentation (mIoU ≈ 91–94 %) [RF]. The wedge is real but narrow, and the academic prior art is public.
2. **Dragonfly 3D World 2027.1 (release notes dated 2026-10-05) is the strongest platform threat.** It already combines a DL training tool, Bouxsein-style Bone Analysis, a Report Builder (PDF/HTML, plus Word for full licenses), macros/Python, and loaders for Bruker `.log` and Scanco `.aim` [V]. Its academic license is free but excludes fee-for-service, industry collaborations and cloud/HPC deployment [V]. OsteoQuant itself cannot run on a free academic license.
3. **The GLP / Part 11 moat is held by CROs and pathology vendors, not by micro-CT software.** Charles River advertises "21 CFR Part 11-compliant custom algorithm development" and GLP-validated Visiopharm and Patholytix [V/CC]. HALO Link has an audit-trail add-on [V]. Patholytix claims Part 11 / GAMP 5 [CC]. No micro-CT analysis package (Bruker, Scanco, Dragonfly, Avizo) was found advertising Part 11 [UNR].
4. **Histology-side graft quantification already exists commercially.** Inotiv sells "% residual implant material" and "% bone ingrowth" per ROI [V]. A Visiopharm algorithm quantifies new bone, cartilage and fibrous tissue in healing allografts with ICC ≈ 1 vs OsteoMeasure [RF]. Bioquant's Ai Suite (Segment) ships Spring 2027 [V].
5. **Bruker's micro-CT application science is moving to deep learning.** Bruker's Phil Salmon co-authors the 2025 Sci Rep DL framework for mouse tibia compartments [RF]. Hopkinson et al. (2023), the automated CTAn callus method from the same RVC group, cut segmentation time about 30× [RF].
6. **A UIUC lab published (Oct/Nov 2026) U-Net segmentation of scaffolds with ingrown bone**, with an application-specific error metric ΔBGF (bone-growth-fraction difference; Bland–Altman bias < 1.5 pp) [RF, PMID 42832161]. This is directly adjacent prior art at the founder's own institution. Treat it as a potential collaborator, a licensing/IP check, and a citation.
7. **Reusable open-source building blocks are mature and permissively licensed:** nnU-Net (Apache-2.0), MONAI (Apache-2.0), napari (BSD-3), BoneJ2 (BSD-2) and FDA's BoneJ Headless (CC0, in the FDA Regulatory Science Tool catalog) [V].
8. **Cross-software morphometry is not interchangeable.** IPL and CTAn agree only on BV/TV; Tb.Th is offset about 15 % [RF]. Locking algorithm versions and reporting the software and version is a real, documentable customer need.

---

## 3. Detailed profiles

### 3A. Scanner-vendor software

#### Bruker micro-CT 3D.SUITE — CTAn (CT-Analyser), CTVox, CTVol, DataViewer, NRecon, 3DxSUITE
- **Components:**
  - DataViewer: slice and orthogonal inspection, "differential image analysis between samples".
  - CTVox / CTVol: volume and surface rendering, STL export.
  - CTAn: density, open/closed porosity, 3D distances and angles, thickness and separation, ROI selection, thresholding, morphological operations, filtering, "Automated batch analysis".
  - NRecon: Feldkamp reconstruction with beam-hardening correction and GPU support.
  - 3DxSUITE: user and data management. [V] https://www.bruker.com/en/products-and-solutions/preclinical-imaging/micro-ct/3d-suite-software.html
- **Segmentation:** threshold and morphology. The product page mentions no AI/ML or DL segmentation [V]. Reseller notes list watershed separation, seed-growing ROI and anisotropic diffusion (v1.18) [CC: blue-scientific.com]. CTAn's BatMan batch manager runs saved task lists over datasets [CC: blue-scientific.com; PK].
- **Bone tools:** the standard rodent trabecular/cortical morphometry, widely cited [PK]. Bruker's "Universal microCT analysis pipeline" webinar (2017) covers "fracture callus" and "defect healing with biomaterials" using a binary-threshold segmentation step [CC] https://www.bruker.com/events/webinars/a-universal-microct-analysis-pipeline-for-bone-preclinical-disease-models.html
- **Graft-specific:** No Bruker app note on separating graft from new bone was found. The Bruker "micro-CT boosts bone graft research" note (rat calvarial GBR) names no segmentation method [V] https://www.bruker.com/en/resources/library/application-notes-mr/micro-ct-boosts-bone-graft-research.html. In literature, a Bruker osseointegration routine of concentric peri-implant rings (OV/TV) is described [RF via search snippet; PMC5832531 not fetched → treat as UNR].
- **Automated callus method (PMC10947128):** Hopkinson et al., J Orthop Res 2023;41(8):1717–1728, doi:10.1002/jor.25507 [RF, V fetched].
  - Two global thresholds (150–255 and 120–255) plus erosion/closing/despeckle/dilation in CTAn plug-ins subtract cortex from callus.
  - Mouse: BV r = 0.990, BV/TV r = 0.972 (bias −3.5 %). Rat: BV/TV r = 0.897 (bias +7.8 %).
  - About 1 min per dataset vs about 30 min manual.
  - Does **not** distinguish graft. Thresholds needed adjustment per scanner. No histology validation.
- **Audit / Part 11:** not found in public materials [UNR].
- **Pricing:** not found. Bruker software is commonly distributed with its scanners [PK].
- **Deployment / licensing:** Windows desktop [PK].
- **Customers:** Bruker SkyScan users in academic and industry labs [PK].
- **Signal:** Bruker application scientist Phil Salmon is a co-author on Lagzouli et al. 2025 (DL framework for mouse tibia, doi:10.1038/s41598-025-19698-w) [RF, V author list].

#### Scanco Medical — Evaluation program / IPL / µFE / scan services
- **Features:** all programs database-integrated; "Automation via scripting/batch mode processing"; segmentation, filtering, object separation/combination; regular/irregular ROI/VOI; automatic contouring; 3D morphing; 2D/3D morphometry; porosity; density (mg HA/ccm); 3D registration; "Evaluation log (for later retrieval)"; import/export DICOM, TIFF, JPG, EPS, STL; web-browser database access; "Secure password and file protection capabilities" [V] (Scanco spec sheet V8/8-2021, https://qd-europe.com/fileadmin/Mediapool/products/x-ray-scanner/Software-micro-CT_Analysis.pdf).
- **IPL:** "Evaluation of 3D scan data is handled by IPL (Image Processing Language)". Protocols are built interactively, then scripted, and run "non-interactively in batch mode". Standard scripts cover trabecular and cortical evaluation [V] https://www.scanco.ch/analysis.html. µFE (IPLFE) available [RF/V via search; https://www.scanco.ch/feanalysis.html listed].
- **AI / ML, biomaterial or implant handling, multiphase segmentation:** not found on the analysis page [V].
- **Native formats:** ISQ/AIM [PK]. Dragonfly full licenses read Scanco `.aim` [V].
- **Services:** "offers scanning, analysis and consulting services". Samples range "from mouse vertebra to human femur" and include medical implants. Synchrotron option down to 370 nm. Priced by estimate [V] https://www.scanco.ch/scanservice.html. GLP not mentioned [V].
- **Part 11:** not found [UNR].
- **Cross-software caveat:** IPL vs CTAn agree only on BV/TV; Tb.Th is offset about 15 % (Mys et al., Bone 2021;142:115653, doi:10.1016/j.bone.2020.115653) [RF].

#### ZEISS — Xradia ART, arivis, ZEN core GxP, Dragonfly ZEISS edition
- **Advanced Reconstruction Toolbox:** [V] https://www.zeiss.com/microscopy/en/products/software/advanced-reconstruction-toolbox.html
  - DeepRecon Pro: DL reconstruction, "up to 10x" throughput.
  - DeepScout: CNN super-resolution.
  - PhaseEvolve: contrast "for easier segmentation".
  - MARS: beam-hardening compensation, with an example of "implants next to bone".
  - OptiRecon: iterative reconstruction.
  - Cloud with one-year licenses. Up to three users per license.
  - These modules improve images; none segments graft vs bone.
- **arivis Cloud / Pro:** cloud DL training (semantic and instance). Models run in arivis Pro / ZEN. ONNX 3D model import. Supports CT/µCT data. Free student tier; premium tiers by quote [CC: zeiss.com arivis pricing page, via search snippet].
- **ZEN core GxP toolkit:** audit trail of changes and e-signatures, two-signature release, checksums. ZEISS states that Part 11 validation/qualification "need to be performed separately". IQ/OQ/PQ services offered [CC: knowledge.zeiss.com, zeiss.com GxP pages via search]. This shows a scanner/software vendor productising GxP for image analysis.
- **Dragonfly 3D World ZEISS edition:** DL module "bundled with pre-built and pre-trained neural networks"; Bone Analysis module with "automated separation of cortical and trabecular bone"; node-locked; 30-day trial; no price [V] https://www.zeiss.com/microscopy/en/products/software/dragonfly-3d-world-zeiss-edition.html

#### Revvity — Living Image Synergy AI; Quantum GX µCT
- Launched 2025-09-29 (WMIC). Unified optical / µCT / ultrasound analysis. "AI algorithms automate image segmentation and region-of-interest quantification" [CC] https://ir.revvity.com/news/investor-news/news-details/2025/Revvity-Unveils-New-AI-Software-Offering-to-Transform-Preclinical-Imaging-Analysis/default.aspx (press syndication fetched via search; primary page not fetched).
- The µCT example shown is lung segmentation. No bone/graft model found [CC].

### 3B. General 3D analysis platforms

#### Dragonfly 3D World (Comet Technologies Canada Inc.; formerly ORS — Object Research Systems)
Primary sources: https://comet.tech/dragonfly; license models and academic license pages; What's New; 2027.1 release notes PDF (dated 2026-10-05) https://brand.comet-group.com/asset/1cf5d871-74d9-47d5-bc7f-cf67c20043bd/Dragonfly-3D-World-Release-Notes-Version-2027-1-10.pdf

- **Status:** "Dragonfly 3D World 2027 has arrived! With improved AI-powered segmentation, advanced measurement capabilities, and integrated reporting" [V].
- **Formats:** BMP/JPEG/PNG/TIFF stacks, RAW, Analyze 7.5, Avizo `.am`, DICOM, NIfTI, MRC, VFF, REK. CZI and Zeiss TXM on Pro builds [V help page]. Full licenses add Bruker `.log`, Nikon `.nhdr`, Rigaku `.prm`, Comet Yxlon, Scanco `.aim` [V release notes]. The academic license excludes "proprietary formats (.am, .aim, .nhdr, etc.)" [V].
- **Segmentation:**
  - Deep Learning Tool (train segmentation and regression models) and Segmentation Wizard (guided DL / classical ML) [V Licenses help page].
  - Segment with AI is limited to classical ML without the DL license [V].
  - 2027.1 adds Grid-based SAM and Cellpose-SAM instance segmentation, 2.5D/3D deep classification, and Fast Split (GPGPU). The classical ML segmentation plug-in is deprecated [V release notes].
  - A "UniversalJawSeg" ready-to-use deep model with enamel/dentin/bone classes is shown [V life-sciences page].
- **Bone tools:** Bone Analysis module, "separately licensed", "pre-clinical research application". Automated cortical/trabecular separation (Kohler, Buie methods). Indices per Bouxsein et al. 2010. Anisotropy and volume-fraction maps. Slice-by-slice analysis. CSV export [V] https://www.theobjects.com/dragonfly/dfhelp/Content/Specialized%20Workflows/Bone%20Analysis/Bone%20Analysis.htm
- **Implants / graft:** "Those working on therapeutic implant studies can visually and numerically assess implant bone regrowth interdigitation" [CC life-sciences page]. No graft-vs-new-bone preset or pretrained model found.
- **Automation:** "macros, Python scripting, or plug-ins" [V]. Auto Process (serial-section stacks) [V].
- **Reporting:** Report Builder ("end-to-end analysis and reporting environment"; "macro compliant"). PDF/HTML for all licenses; Word export, custom headers and embedded meshes on full licenses. LaTeX "Report Generator" for Bone Analysis wizard reports and macro outputs. Free Session Viewer lets clients review results [V release notes].
- **Statistics:** measurement/statistics tables from "Analyze and Classify Measurements" [V]. No inferential study statistics found.
- **Audit trail / Part 11 / GLP:** the strings audit, Part 11, GLP and signature do not appear in the 2027.1 release notes [V by text search]. Not found in public materials.
- **Licensing and pricing:**
  - Annual or perpetual commercial ("Full") licenses, priced by quote; no price published [V].
  - Academic license free for individuals at degree-granting institutions, museums and teaching hospitals. It explicitly excludes "contract research for industry, fee-for-service analysis, or product development", "academic collaborations with industry partners", and government labs. It is local-only (no cloud/HPC/remote) [V].
  - Academic licenses lose Advanced Report Builder, Session Viewer and proprietary formats from 2027.1 [V].
- **Customers:** academia, research facilities, industry (QA, AM, materials) [V].
- **Implication:** OsteoQuant cannot build its commercial service on a free Dragonfly academic license. Academic customers can, however, get Dragonfly's DL and Bone Analysis free.

#### Thermo Fisher Amira / Avizo (Amira-Avizo 3D) + BONe
- **2024.2 release notes:** AI-Assisted Segmentation in the Segmentation+ workroom trains "shallow or deep models" from ROI annotations, with multi-material VGG16/VGG19 predictions. Models are reusable in project DL modules. DL packages install by default (Python 3.11). AI segmentation needs "Advanced packages" licensing [V] https://documents.thermofisher.com/TFS-Assets/MSD/Software-Updates/amira-avizo3d-20242-release-notes.pdf. The 2D/3D DL training modules date from 2022.1 [CC via search snippet of release notes].
- **BONe (Bone One-shot Network):** Andrew H. Lee (Midwestern University). DLFit (train/fine-tune), DLPred (predict), IoU (score), running in Amira/Avizo and as standalone Python apps. The BP-2D-03a bone/pores model reports mean IoU ≈ 91 % (range ≈ 85–97 %) in five-fold CV [V Thermo blog dated 11.17.2026] https://www.thermofisher.com/blog/atomic-resolution/biomedical-image-segmentation-supports-micro-ct-analysis-bone-segmentation/ ; Lee et al., Front Bioinform 2025, doi:10.3389/fbinf.2025.1677527 [RF]. Code and models are on Dryad (doi:10.5061/dryad.4j0zpc8qq) [RF]; license terms [UNR]. Trained on mammalian bone with pores. **No graft class.**
- **Bone tools:** XImagePAQ extension: bone segmentation, trabecular/cortical separation [CC via search snippet]. Marketing claims bone-implant contact / osseointegration gap analysis [CC].
- **Audit / Part 11:** not found. **Pricing:** not found. **Deployment:** desktop (Windows/Linux/macOS) [PK].
- Used by the Sci Rep 2024 rabbit calvarial study (Amira 6.3) [RF].

#### Analyze 15 (AnalyzeDirect) — BMA add-on
- Analyze 15.0 covers segmentation, measurement, registration, display, processing and transforms. The BMA add-on provides "bone microarchitecture analysis for MicroCT data". 14-day trial [V] https://analyzedirect.com/
- BMA: Segment Cortex / Segment Trabeculae / Measure Bone; HU→BMD conversion [CC: SoftwareOne listing; RF: JoVE tutorial via snippet].
- Graft, DL, Part 11 and pricing: not found.

#### VivoQuant (Perceptive; historically Invicro)
- "Quantify PET, SPECT, CT, MRI, and optical data in one unified environment". ROIs by manual, threshold, spline and atlas methods. VivoScript and Worklists for batch work. Version 6.0 (Feb 2026) infrastructure overhaul [V] https://www.perceptive.com/vivoquant-preclinical-imaging-analysis-software/
- Bone tools, AI, Part 11/GLP and pricing: not mentioned [V]. The Perceptive preclinical page mentions "regulatory-ready reporting" [CC]. The Invicro→Perceptive relationship is not stated on the fetched page [UNR].

#### Others found (not in the playbook) — see Section 5(d)
- **Hexagon VGSTUDIO MAX:** Deep Segmentation Module + VGTRAINER [CC].
- **Synopsys Simpleware:** AI auto-segmentation; 2025.06 adds automatic cancellous bone segmentation for femurs [CC].
- **Materialise Mimics:** AI-enabled segmentation, clinical CT [CC].
- **MIM Software:** no preclinical micro-CT bone offering found [UNR].

### 3C. Open-source tools (reuse candidates)

| Tool | What it gives OsteoQuant | License | Evidence |
|---|---|---|---|
| **BoneJ2** | Area/volume fraction, thickness (Hildebrand), connectivity (Euler), anisotropy (MIL), ellipsoid factor, particle analyser, skeletonise, inter-trabecular angles, "Calibrate SCANCO (WIP)". Paid GPU "BoneJ+" via BeanCounter voucher | BSD-2-Clause | [V] https://imagej.net/plugins/bonej ; LICENSE file. Domander et al. 2021 doi:10.12688/wellcomeopenres.16619.2 [RF]; Doube et al. 2010 doi:10.1016/j.bone.2010.08.023 [RF] |
| **BoneJ Headless** (FDA CDRH/OSEL DIDSR) | Python wrapper over Fiji+BoneJ; primary metrics Th, Sp, DA, EF, BV/TV, Conn. FDA reports values identical to GUI BoneJ. Linux only, "in development, use with caution". In FDA RST catalog (RST24AI03.01). Not a qualified MDDT | CC0-1.0 | [V] https://github.com/DIDSR/BoneJ_Headless |
| **Fiji / ImageJ** | Host for BoneJ; huge plug-in ecosystem | GPL-family (Fiji distribution) | [PK] |
| **nnU-Net** | Self-configuring 2D/3D segmentation; best model in the Mg-implant 4-class comparison | Apache-2.0 | [V LICENSE]; Isensee et al., Nat Methods 2021, doi:10.1038/s41592-020-01008-z [RF] |
| **MONAI** (+ MONAI Label) | PyTorch medical-imaging DL, active-learning labelling | Apache-2.0 | [V LICENSE]; MONAI Label [PK] |
| **napari** | n-D viewer/annotator in Python; good base for review/correction UI | BSD-3-Clause | [V LICENSE] |
| **3D Slicer** | DICOM, Segment Editor, extensions (MONAI Label, SlicerMorph) | BSD-style Slicer license | [V License.txt]; features [PK] |
| **ITK-SNAP** | Semi-automatic active-contour 3D segmentation; manual correction | GPL-3.0 | [V COPYING]; features [PK] |
| **QuPath** | 2D whole-slide histology analysis, pixel/object classifiers, scripting | GPL-3.0 | [V LICENSE]; features [PK] |
| **ilastik, Cellpose(-SAM), SAM** | Interactive pixel classification; instance segmentation; promptable annotation | ilastik GPL-family [V header]; Cellpose BSD-style (HHMI) [V]; SAM Apache-2.0 [PK] | — |

**GPL caution:** ITK-SNAP and QuPath are GPL-3.0. Use them as separate processes or tools, not linked into a proprietary binary [PK legal-general; confirm with counsel].

### 3D. Histology / histomorphometry / digital pathology

#### Bioquant (BIOQUANT Image Analysis Corp.)
- BIOQUANT Measurement 2025 consolidates OSTEO and Life Science. "Follows ASBMR and BMAS Nomenclature". Human bone biopsy, cortical bone structure, skeletal phenotyping and stereology templates. SVG, PLY and 4 GB TIFF export. Non-commercial licensing options [V] https://www.bioquant.com/measurement/overview
- **BIOQUANT Ai Suite** ("Stitch, Convert, Segment", "Slide to publishable histomorphometry") ships with the BIOQUANT 2027 Update in **Spring 2027**. It is included for labs on an active Technical Service Plan [V] https://www.bioquant.com/bioquant2027
- **Services:** non-decalcified bone histology (resin, ground sections), slide scanning, trabecular/cortical phenotyping. Pricing by request. GLP and micro-CT not mentioned [V] https://www.bioquant.com/services/overview
- Part 11: not found. The Sci Rep 2024 rabbit study used Bioquant Osteo for histology [RF].
- **SkeleTech** (bone CRO historically linked with Bioquant-style histomorphometry): current status [UNR].

#### OsteoMeasure (OsteoMetrics, Atlanta/Decatur GA)
- Semi-automated, "largely based on manual tracing"; static and dynamic parameters [RF via PMC4717440 and others]. Official site not fetched. Part 11 [UNR]. Used as the reference standard against which Visiopharm was validated [RF].

#### Visiopharm
- **Products:** Discovery (train DL APPs), Phenoplex, APP Center (>130 APPs), Quickstart APPs, CE-IVD APPs, IMS/LIMS integrations [V] https://visiopharm.com/
- **Formats:** whole-slide and 2D microscopy formats only (Aperio, Hamamatsu, Leica, Philips iSyntax, CZI, OME-TIFF, etc.). No volumetric or micro-CT format is listed. DICOM appears only as Ventana DP600 `.dicom` and DICOMweb import [V] https://cpwebapps.azurewebsites.net/docs/next/database/supported-image-formats
- **Bone evidence:**
  - Zhang et al., Bone Res 2016;4:15037, doi:10.1038/boneres.2015.37: automated new bone / cartilage / fibrous tissue in healing murine femoral **allografts**, ICC vs OsteoMeasure "very close to one" [RF, abstract via PubMed].
  - An AI-assisted osteoclast Oc.S/BS protocol (TRAP / cathepsin K) with overnight batch processing [RF] https://pmc.ncbi.nlm.nih.gov/articles/PMC8374260
- **GLP:** Charles River lists Visiopharm "GLP-compliant in DUR, EDI, and EVR" [CC/V on criver.com]. A vendor Part 11 statement was not found.

#### Deciphex Patholytix Preclinical
- **GLP:** GLP peer review and primary-evaluation workflows (GLP study flags, logged events) [CC patholytix.com news]. Charles River validated it "for GLP peer review in 2021" and GLP primary review in 2022 [V criver.com digital pathology page].
- **Part 11:** "full compliance with FDA 21 CFR Part 11, validation under ISPE GAMP 5" [CC via search snippet; https://www.patholytix.com/glp-services returned 404 when fetched → UNR on current wording].
- **Deployment:** cloud SaaS (EU PATH-TOX project) [CC CORDIS].
- **Bone / µCT:** not found.

#### Aiforia
- **Aiforia Studies** (2024-03-06): AI-assisted image analysis "within the framework of Good Laboratory Practices (GLP)", with the ability to "export and store immutable study data" [V] https://www.aiforia.com/press-releases/aiforia-releases-aiforia-studies
- Cloud platform; Create trains DL models [CC]. Charles River case study [CC]. Bone not found.

#### Indica Labs HALO / HALO AI / HALO Link
- **HALO Link Compliance Add-on:** system-wide auditing of study, slide, annotation and metadata actions in HALO Link, plus analysis/classifier setting changes in HALO. It logs timestamp, event, original/new values and operator, with an optional reason-for-change and CSV export. Positioned "to aid adherence to GLP"; Part 11 not claimed on the page [V] https://indicalab.com/news/halo-link-compliance-add-on-promoting-best-practices-in-digital-pathology-laboratories/
- Bone-specific module: not found.

### 3E. Preclinical CROs and service providers

| Provider | Relevant verified facts | Evidence |
|---|---|---|
| **Charles River** | Bone repair incl. "evaluation of bone substitutes" and orthobiologics; critical-size segmental defects; spinal fusion; micro-CT; "manual and software-guided automated histomorphometry"; up to "GLP assessments". Digital pathology: Visiopharm GLP at 3 sites, Patholytix GLP-validated, **"21 CFR Part 11-compliant custom algorithm development"**, "black box" verification for GLP algorithms | [V] criver.com orthopedic-device-testing; [V] criver.com digital-pathology |
| **NAMSA** | Pathology services list micro-CT, histomorphometry, SEM/TEM, IHC; orthopedics CRO lists bone ingrowth, osseointegration endpoints | [CC via search snippets; namsa.com fetch returned 403] |
| **Inotiv / Histion** | "Percent bone ingrowth" and **"Percent residual implant material as a function of a defined ROI (e.g., defect or fusion mass)"**, "on validated systems". Histion described as a GLP-compliant lab | [V] https://inotiv.com/solutions/histomorphometric-analysis ; [CC] inotiv.com/histion |
| **AccelLAB** | Management bought AccelLAB from Charles River in 2024; about 100 staff, Boisbriand/Terrebonne QC; medical-device and biologics CRO. Orthopedic µCT services not verified | [CC] privsource.com deal summary; [UNR] services |
| **Altasciences** | No orthopedic micro-CT page found | [UNR] |
| **CSU PSRL** (Preclinical Surgical Research Lab) | "Bone healing studies", "Allograft, autograft, and xenograft testing", spine fusion, CT/DEXA imaging; GLP per 21 CFR Part 58; ex vivo via Orthopaedic Bioengineering Research Lab | [V] https://vetmedbiosci.colostate.edu/psrl/services/ ; TMI not fetched [UNR] |
| **Labcorp** | In vivo / ex vivo micro-CT; bone density/microstructure, remodeling; implanted devices/biomaterials; ex vivo turnaround 1–2 weeks with dataset, tables and report | [V] labcorp.com computed-tomography |
| **Scanco services** | Scanning, analysis, consulting incl. implants; quote-based | [V] scanco.ch/scanservice.html |
| **Bioquant services** | Undecalcified histology, slide scanning, phenotyping | [V] |
| **Academic cores** | BIDMC (Bouxsein): 2× Scanco µCT40, academic + industry clients, spreadsheet + images + short report [V]. **HSS: scanning or analysis $75/h NIH-funded, $100/h academic, $200/h corporate; $25/h self-analysis** [V] https://www.hss.edu/research/core-facilities/micro-computed-tomography-core. Rush: Scanco µCT 45/50 + undecalcified histology, quotes on request [V] | [V] |
| **Numira Biosciences** | Crunchbase describes imaging CRO services; current µCT offering not confirmed | [CC/UNR] |
| **Perceptive Instruments** | Now under Instem; Comet Assay IV (genetic-tox imaging) with audit trails / Part 11 claims. Not a bone competitor, but a precedent for Part 11 image-analysis software | [CC] https://www.instem.com/solutions/comet-assay-iv/ |

### 3F. Published automated bone / callus / graft segmentation pipelines (2019–2026)

| Paper | Task | Method | Key result | Relevance |
|---|---|---|---|---|
| Hopkinson et al., J Orthop Res 2023, doi:10.1002/jor.25507 (PMC10947128) | Callus vs cortex, mouse/rat femur | CTAn thresholds + morphology | BV r = 0.99; ~30× faster; no graft class | Shows CTAn-only automation is publishable and adoptable [RF] |
| Liu et al., Bone Rep 2024;20:101743, doi:10.1016/j.bonr.2024.101743 (PMID 38390284) | Callus tissue classes on synchrotron PCI-CT | DL segmentation (histology-trained) | Dice 0.72 / 0.83 / 0.76 for reserve-proliferative / hypertrophic / mineralized cartilage | Histology-derived labels, multi-class callus [RF] |
| Beitlitum et al., Sci Rep 2024;14:4321, doi:10.1038/s41598-024-54313-4 (PMC10881464) | Rabbit calvaria: new bone vs xenograft by region | Amira 6.3 grayscale thresholds + manual refinement; coaxial cylinders (outer/middle/inner) + pristine-bone reference | Inner-region bone 15.9 % (PCM) to 53 % (DBBM) of pristine; thresholds not reported; no quantitative histology agreement | Regional endpoint design to emulate; manual-heavy [RF] |
| Ganeshaaraj et al., IEEE EMBC 2022, doi:10.1109/EMBC48229.2022.9870828 | **Scaffold (bioactive glass) / bone / pores** | CNN + registration + ingrowth / degradation metrics | Dice 90.1, IoU 83.9 | **Closest 3-class prior art** [RF] |
| Marinho et al., Front Phys 2024, doi:10.3389/fphy.2024.1257512 | Mg implant: residual / degradation layer / bone / background (SRµCT) | U-Net variants vs nnU-Net | 2D nnU-Net mIoU 94.4 % / 91.5 %; degradation layer hardest | nnU-Net is the baseline to beat [RF] |
| Baltruschat et al., Sci Rep 2021, doi:10.1038/s41598-021-03542-y | Biodegradable implant segmentation, SRµCT | Scaled U-Net | — | Prior art [RF] |
| Aboutaleb … Wagoner Johnson, Med Biol Eng Comput 2026;64(11):4121, doi:10.1007/s11517-026-03686-x (PMID 42832161) | Scaffolds with ingrown bone (UIUC) | 3 U-Nets, different losses | ΔBGF bias < 1.5 pp; Accuracy best correlates with endpoint error | **Same institution**; endpoint-centric validation metric [RF] |
| Lagzouli et al., Sci Rep 2025;15:8656, doi:10.1038/s41598-025-92954-1 | Cortical / trabecular, mouse tibia | DBAHNet (transformer-CNN) | DSC 98.4 % control; 0.90 on external sets; code on GitHub | Generalisation drop across studies [RF] |
| Lagzouli et al., Sci Rep 2025;15:35807, doi:10.1038/s41598-025-19698-w | Tibia compartments + VOI landmarks | 2D classifier + DL seg | F1 0.92–0.99 | Co-author from Bruker [RF] |
| Lee et al., Front Bioinform 2025, doi:10.3389/fbinf.2025.1677527 | Bone vs pores, 5 species | BONe 2D model | IoU ~91 % CV | Avizo ecosystem [RF] |
| MiceBoneChallenge, arXiv 2411.17260 | Growth-plate plane detection, 83 mice | 6 team solutions | MAE 1.91 ± 0.87 planes | Industry-organised ("Anonymous Company") public dataset [RF] |
| Lesage et al., JoVE 2024, doi:10.3791/67235 | Ex vivo sheep femoral-head defect + BMP2 bone substitute | µCT + DL to "enhance discrimination of mineralized tissues" + histology / SEM / Raman | Workflow paper | Multimodal ground-truth template [RF] |

**Gap confirmed in the literature:** a Boston University dental thesis (2022) applied CNN multi-level segmentation to grafted samples [RF, open.bu.edu, not fetched]. No paper was found that validates a three-class new-bone / CaP-or-glass-graft / host-bone model across multiple graft chemistries against registered undecalcified histology [UNR — absence after limited search].

### 3G. Evergen + University of Florida
- Evergen (formerly RTI Surgical; CDMO and UF startup) launched AI image-processing software (Feb 2025) for "CT bone graft scans". It is used to "assess bone density and structure" to decide graft use. It replaces multi-technician subjective review and can "analyze hundreds of images and produce reports in under 10 seconds". Built over 2 years with UF Mechanical & Aerospace Engineering [V UF Innovate] https://innovate.research.ufl.edu/evergen-launches-ai-powered-bone-graft-image-processing-software/
- Over 50 successful scans in a Dec 2024 pilot [CC press release via search].
- No accuracy data or external sale was found; it appears to be internal tissue-processing QC [V: page frames benefits as Evergen's own processing efficiency].
- **Relevance:** proves graft processors will fund in-house AI CT analysis. Evergen is a potential *customer or partner* more than a competitor.

### 3H. Startup search
Queries run: "AI micro-CT bone graft analysis startup preclinical orthobiologic" (extended), "automated bone histomorphometry AI company…", "preclinical imaging analysis software orthopedic implant AI segmentation micro-CT company 2025", "startup AI histopathology bone implant osseointegration…" (extended).
- **Result:** no dedicated startup selling AI analysis of preclinical bone-graft micro-CT or orthobiologic studies was found.
- **Adjacent items surfaced:** Revvity Synergy AI, Simpleware, Mimics, RSIP Vision (clinical arthroplasty), Evergen, and academic projects (University of Kentucky self-supervised histomorphometry; ADAM pipeline for undecalcified biopsies) [CC/RF via snippets].
- **Caveat:** absence in web search ≠ absence in market. Stealth startups and CRO in-house tools are likely [UNR].

---

## 4. Playbook claim check

| Playbook claim | Verdict | Evidence |
|---|---|---|
| "CTAn: no three-class graft/bone learning" | **Confirmed as far as public materials go (not contradicted).** No ML/DL segmentation appears on Bruker's 3D.SUITE page; segmentation there is threshold + morphology. Caveats: (i) CTAn multi-threshold pipelines are used for "defect healing with biomaterials" [CC] and can separate graft from bone when attenuations differ [PK]; (ii) Bruker's application scientist co-authors DL bone papers [RF], so a Bruker DL release is plausible; (iii) "no learning" ≠ "cannot do three-class". Reword as "CTAn: threshold-based; no learned graft/new-bone/host model found in public materials (Nov 2026)." | [V] bruker.com 3d-suite page; [RF] doi:10.1038/s41598-025-19698-w |
| "Dragonfly: no study-endpoint reports or GLP package" | **Partly contradicted.** Reports: Dragonfly 2027.1 ships a Report Builder (PDF/HTML; Word on full license, "macro compliant"). Its LaTeX Report Generator produces Bone Analysis wizard reports, the Bone Analysis module computes Bouxsein-style indices with CSV export, and a free Session Viewer shares results. "No reports" is wrong. "No *study-level endpoint* reports" (group comparisons, defect-ROI endpoints, statistics) remains plausible: not found. GLP package: **not contradicted.** No audit trail, Part 11 or GLP text appears in the 2027.1 release notes or product pages. | [V] Dragonfly 2027.1 release notes; [V] Bone Analysis help |
| "Visiopharm: no micro-CT" | **Confirmed (public materials).** The Visiopharm supported-formats manual lists only 2D/whole-slide formats; no volumetric µCT format. Caveat: Visiopharm is strong in the *histology* phase of the same studies (validated allograft new-bone/cartilage/fibrous algorithm; GLP use at Charles River). Do not dismiss it for OsteoQuant's histology roadmap. | [V] Visiopharm formats doc; [RF] doi:10.1038/boneres.2015.37; [CC/V] criver.com |

Other playbook claims could not be checked because the playbook is not in the repo [UNR].

---

## 5. Strategic analysis

### (a) Reuse rather than rebuild

| Need | Reuse | Why / caveat |
|---|---|---|
| 3-class segmentation trainer | **nnU-Net v2** (Apache-2.0); MONAI for custom pipelines | nnU-Net was best in the closest multi-class implant benchmark [RF]. Value is in data, labels and validation, not architecture |
| Interactive labelling / correction UI | **napari** (BSD-3) plugin; or 3D Slicer (BSD-style) + MONAI Label | Permissive licenses suit a proprietary product [V]. Avoid embedding GPL ITK-SNAP / QuPath code [V licenses] |
| Promptable annotation acceleration | SAM / Cellpose-SAM | Same components Dragonfly ships, so parity, not differentiation [V] |
| Morphometry (BV/TV, Tb.Th, Tb.Sp, Conn.D, DA, SMI…) | **BoneJ2** algorithms (BSD-2) via **BoneJ Headless** (CC0, FDA DIDSR) or reimplement against them | FDA-catalogued tool; FDA reports identical values to GUI BoneJ [V]. Pin versions; cite. Expect IPL/CTAn offsets [RF] and publish a cross-walk |
| Reading Bruker / Scanco / Nikon / Zeiss data | SimpleITK / ITK readers, TIFF/DICOM stacks; Scanco ISQ/AIM readers [PK] | Format breadth is table stakes: Dragonfly full license reads all of these [V] |
| Reference VOI / regional endpoint design | Bouxsein 2010 guidelines (doi:10.1002/jbmr.141) [RF]; Beitlitum 2024 coaxial-cylinder regions [RF] | Adopt published conventions so reports map to how reviewers read them |
| Validation metric | Endpoint-level error (ΔBGF-style), Bland–Altman, ICC (Aboutaleb 2026; Hopkinson 2023) [RF] | Report endpoint error, not just Dice |
| Audit trail / e-signatures pattern | Copy feature checklists from ZEN core GxP and HALO Link (timestamp, old/new value, operator, reason-for-change, two-signature release) [CC/V] | Build to Part 11 §11.10(e) expectations; customers still validate [PK] |
| Bone-pores pretrained weights | BONe models (Dryad) for transfer learning | Check license first [UNR] |

### (b) Narrowest credible differentiation

> **"A locked, versioned, validated three-class segmentation (new bone / residual graft / host bone) inside a defined defect ROI, for named graft chemistries (CaP, bioactive glass, xenograft) in named models (e.g., rat/rabbit calvarial and femoral-condyle critical-size defects). Every study ships with a model-version-pinned PDF/CSV endpoint report and an audit trail, plus a per-study agreement dossier vs expert manual labels (and, where available, registered undecalcified histology). Vendor-neutral input (Bruker, Scanco, Nikon, ZEISS)."**

Why this is defensible (for now):
- None of the vendors found ships a graft-vs-new-bone preset or validated model [V/UNR]. Their DL tools are generic trainers that leave labelling, validation and documentation to the user [V].
- Labelled ground truth across graft chemistries (where new bone and CaP overlap in attenuation) is the scarce asset. Histology-registered labels are scarcer still [RF: Liu 2024 used histology to train; Beitlitum 2024 could not reconcile µCT vs histology].
- No micro-CT tool advertises audit trail or Part 11 [UNR], while the CROs that do (Charles River) build bespoke algorithms per client [V]. A productised, validated endpoint package can be *sold to* CROs as well as competing with them.

What is **not** differentiating: "uses deep learning", "BV/TV", "batch processing", "PDF report", "SAM-assisted labelling". Dragonfly, Avizo and Scanco already have these [V].

### (c) Capabilities competitors have that the playbook may understate

1. **Dragonfly:**
   - Separately licensed Bone Analysis module with Bouxsein indices [V].
   - Multi-class DL training and Segmentation Wizard [V].
   - SAM / Cellpose-SAM, 3D DL classification (2027.1) [V].
   - Report Builder and Report Generator for bone reports [V].
   - Python/macros [V].
   - Reads Scanco/Bruker/Nikon raw formats [V].
   - Free Session Viewer for client review [V].
   - Free academic license, which undercuts OsteoQuant's academic segment [V].
2. **Amira/Avizo:** multi-material deep AI-assisted segmentation [V]; BONe bone models and training/scoring tools [V/RF]; XImagePAQ bone extension [CC].
3. **Scanco:** "Evaluation log", database-integrated reporting, scripted batch IPL, password/file protection [V]; contract scanning and analysis including implants [V].
4. **Bruker:** BatMan batch automation [CC]; published fully automated CTAn callus pipeline [RF]; DL research by application staff [RF].
5. **CROs:** Charles River offers Part 11-compliant custom algorithm development and GLP-validated AI pathology [V]. Inotiv already sells % residual implant material [V].
6. **Histology vendors:** HALO Link audit trail [V]; Patholytix Part 11 claim [CC]; Aiforia GLP "Studies" [V]; Visiopharm validated allograft-healing algorithm [RF]; Bioquant Ai Suite in Spring 2027 [V].
7. **ZEISS:** ZEN core GxP toolkit (audit trail, e-signatures) [CC] shows vendors can bolt on compliance. DeepRecon improves input quality and may shift the accuracy baseline [V].
8. **Academic open science:** a CNN scaffold/bone/pore three-class pipeline exists (Dice 90) [RF]. A UIUC U-Net scaffold-ingrowth pipeline with endpoint metric was published Oct/Nov 2026 [RF].

### (d) Missing competitors / players the playbook did not list

- **Revvity Living Image Synergy AI** (micro-CT AI segmentation, 2025) [CC]; Revvity Quantum GX3 osseointegration tech note [CC: resources.revvity.com].
- **ZEISS ZEN core GxP toolkit, arivis Cloud/Pro, ART/DeepRecon** [CC/V].
- **Hexagon Volume Graphics VGSTUDIO MAX** Deep Segmentation Module + VGTRAINER [CC].
- **Synopsys Simpleware** (AI auto-segmentation; cancellous bone segmentation, 2025.06) [CC]; **Materialise Mimics** (AI segmentation; also used with BoneJ in preclinical pipelines) [CC/RF].
- **Inotiv / Histion** (residual implant material histomorphometry) [V]; **Labcorp** micro-CT (ex vivo bone reports in 1–2 weeks) [V].
- **Academic µCT cores selling to industry** (HSS corporate $200/h [V], BIDMC [V], Rush [V]): the cheapest substitute for small graft companies.
- **BoneJ Headless (FDA DIDSR)**: reuse, and a signal that FDA researchers value reproducible bone metrics [V].
- **UIUC Wagoner Johnson lab** (scaffold ingrowth U-Net) [RF]; **Midwestern Univ. BONe** [RF]; **RVC/QUT Lagzouli–Pivonka–Pitsillides group with Bruker co-author** [RF]; **MiceBoneChallenge consortium** [RF].
- **Evergen** (UF) as a potential customer/partner archetype [V].
- **Instem (ex-Perceptive Instruments)** as a template for Part 11 image-analysis software [CC].

### (e) Threat scenarios (judgement; likelihood over 24 months)

| # | Scenario | Likelihood | Impact | Early signal to watch | Mitigation |
|---|---|---|---|---|---|
| T1 | **Comet ships a "bone regeneration / implant" Dragonfly preset** (graft/new-bone DL model + Bone Analysis + Report Builder) | Medium | High: kills the academic segment, pressures pricing | Dragonfly release notes, life-science app notes, "implant interdigitation" examples [V current marketing] | Compete on validation dossier, audit trail and GLP-readiness Dragonfly does not advertise; partner (OsteoQuant models as a Dragonfly plug-in?) |
| T2 | **Bruker releases DL segmentation in CTAn** or a free Bruker AI bone toolkit, bundled with scanners | Medium | High for Bruker-installed base | Bruker staff DL co-authorships [RF]; CTAn release notes | Be vendor-neutral (Scanco/Nikon/ZEISS); sell validation and endpoints, not segmentation alone |
| T3 | **Thermo extends BONe / Avizo AI with biomaterial classes** | Low–Medium | Medium | BONe Dryad updates; Thermo blog (latest 2026-11-17) [V] | Same as T1 |
| T4 | **Large CROs (Charles River, NAMSA, Inotiv) build in-house µCT graft algorithms** under their Part 11 frameworks | Medium–High | High: they own sponsor relationships | CR "custom algorithm development" [V]; Inotiv residual-implant offering [V] | Position as a CRO supplier (white-label, validation package that reduces their CSV burden) rather than a competitor |
| T5 | **Open-source release of trained graft/bone models** (UIUC, BONe, EMBC group), commoditising segmentation | Medium | Medium | GitHub/Dryad releases with weights | Make data, validation, reporting and compliance the product; collaborate with or license from the UIUC lab early |
| T6 | **Histology incumbents add AI first** (Bioquant Ai Suite Spring 2027; Visiopharm/HALO bone APPs) and capture the "correlated µCT + histology" story | High (Bioquant dated) | Medium for OsteoQuant's histology roadmap | Bioquant 2027 launch at ASBMR [V] | Focus on µCT→histology *registration and concordance*, which none was found to offer |
| T7 | **Customers DIY** (graft-company scientists with Dragonfly + nnU-Net) | High | Medium | Job posts, publications | Sell time-to-validated-endpoint and audit trail, not tooling |
| T8 | **Academic cores undercut on price** ($75–200/h) [V] | High | Low–Medium | Core fee schedules | Target GLP/IDE-supporting studies where cores do not offer audit trails |
| T9 | **Regulatory expectation shift** (FDA reviewers request histology concordance or locked algorithm documentation) | Low–Medium | Positive if ready, negative if not | FDA RST catalog additions; guidance | Build the validation dossier template now |

---

## 6. Open questions / next verification steps

1. Bruker: obtain the current CTAn release notes and ask about Part 11 and any DL roadmap [UNR].
2. Scanco: confirm Part 11 status of the evaluation log and whether IPL has multiphase/biomaterial scripts [UNR].
3. Dragonfly: request a commercial quote (Full + DL + Bone Analysis), and ask whether audit-trail or GLP features are planned [UNR].
4. Amira/Avizo: confirm BONe license and Avizo AI pricing; check for a Thermo GxP offering for Amira [UNR].
5. NAMSA, AccelLAB, Altasciences: get service sheets (403s / no pages found) [UNR].
6. Read the UIUC 2026 paper in full (PMC13777832) for data/code availability and IP; consider contacting the lab [RF].
7. Patholytix Part 11 page returned 404; re-check current wording [UNR].
8. SkeleTech, Numira, CSU TMI current status [UNR].

---

## 7. Sources

**Bruker**
- https://www.bruker.com/en/products-and-solutions/preclinical-imaging/micro-ct/3d-suite-software.html [V]
- https://www.bruker.com/en/resources/library/application-notes-mr/micro-ct-boosts-bone-graft-research.html [V]
- https://www.bruker.com/events/webinars/a-universal-microct-analysis-pipeline-for-bone-preclinical-disease-models.html [V]
- https://blue-scientific.com/?p=15507 ; https://blue-scientific.com/?p=6806 (reseller) [CC]

**Scanco**
- https://www.scanco.ch/ ; https://www.scanco.ch/analysis.html ; https://www.scanco.ch/scanservice.html [V]
- https://qd-europe.com/fileadmin/Mediapool/products/x-ray-scanner/Software-micro-CT_Analysis.pdf [V]
- https://qd-europe.com/fileadmin/Mediapool/products/x-ray-scanner/Application_Note-Bioengineering.pdf [V]

**Dragonfly**
- https://comet.tech/dragonfly ; https://comet.tech/dragonfly/products/license-models ; https://comet.tech/dragonfly/products/license-models/academic-license ; https://comet.tech/dragonfly/what-s-new-in-dragonfly ; https://comet.tech/dragonfly/applications/life-sciences [V]
- https://brand.comet-group.com/asset/1cf5d871-74d9-47d5-bc7f-cf67c20043bd/Dragonfly-3D-World-Release-Notes-Version-2027-1-10.pdf [V]
- https://www.theobjects.com/dragonfly/dfhelp/Content/Getting%20Started/Licenses.htm ; .../Key%20Features/Supported%20File%20Formats.htm ; .../Specialized%20Workflows/Bone%20Analysis/Bone%20Analysis.htm [V]
- https://www.zeiss.com/microscopy/en/products/software/dragonfly-3d-world-zeiss-edition.html [V]

**Thermo Fisher Amira/Avizo**
- https://documents.thermofisher.com/TFS-Assets/MSD/Software-Updates/amira-avizo3d-20242-release-notes.pdf [V]
- https://www.thermofisher.com/blog/atomic-resolution/biomedical-image-segmentation-supports-micro-ct-analysis-bone-segmentation/ [V/CC]
- https://datadryad.org/dataset/doi:10.5061/dryad.4j0zpc8qq [RF]

**ZEISS**
- https://www.zeiss.com/microscopy/en/products/software/advanced-reconstruction-toolbox.html [V]
- https://www.zeiss.com/microscopy/en/products/software/zen-core/gxp-toolkit.html ; https://www.zeiss.com/microscopy/en/products/software/arivis-cloud-ai/pricing.html [CC via search]

**Other 3D / preclinical platforms**
- https://ir.revvity.com/news/investor-news/news-details/2025/Revvity-Unveils-New-AI-Software-Offering-to-Transform-Preclinical-Imaging-Analysis/default.aspx [CC]
- https://analyzedirect.com/ [V]
- https://www.perceptive.com/vivoquant-preclinical-imaging-analysis-software/ ; https://www.perceptive.com/preclinical-imaging/ [V]
- https://hexagon.com/customer-stories/ai-powered-medical-segmentation-anatomikmodeling ; https://materialise.com/en/healthcare/mimics-innovation-suite/ai-enabled-segmentation ; https://origin-www.synopsys.com/simpleware/news-and-events/simpleware-x-2025-06.html [CC via search]

**Open source**
- https://imagej.net/plugins/bonej ; https://bonej.org/ ; https://github.com/DIDSR/BoneJ_Headless [V]
- License files (raw.githubusercontent.com) for MIC-DKFZ/nnUNet, napari/napari, Slicer/Slicer, pyushkevich/itksnap, qupath/qupath, bonej-org/BoneJ2, Project-MONAI/MONAI, ilastik/ilastik, MouseLand/cellpose [V]

**Histology / pathology**
- https://www.bioquant.com/ ; https://www.bioquant.com/bioquant2027 ; https://www.bioquant.com/measurement/overview ; https://www.bioquant.com/services/overview [V]
- https://visiopharm.com/ ; https://cpwebapps.azurewebsites.net/docs/next/database/supported-image-formats [V]
- https://indicalab.com/news/halo-link-compliance-add-on-promoting-best-practices-in-digital-pathology-laboratories/ [V]
- https://www.aiforia.com/press-releases/aiforia-releases-aiforia-studies [V]
- https://www.patholytix.com/news-and-events/patholytix-preclinical-2-0 ; https://www.patholytix.com/glp-services (404 at fetch) [CC/UNR]

**CROs and services**
- https://www.criver.com/industry/medical-device/preclinical-medical-device-testing/orthopedic-device-testing ; https://www.criver.com/products-services/safety-assessment/pathology-services/digital-pathology [V]
- https://inotiv.com/solutions/histomorphometric-analysis [V]
- https://namsa.com/services/preclinical/pathology-services/ (403) ; https://www.namsa.com/services/therapies/orthopedics/ [CC via search]
- https://vetmedbiosci.colostate.edu/psrl/services/ [V]
- https://www.labcorp.com/biopharma/nonclinical/disciplines/support-services/tools/computed-tomography [V]
- https://research.bidmc.org/mary-bouxsein/services/uct ; https://www.hss.edu/research/core-facilities/micro-computed-tomography-core ; https://www.rushu.rush.edu/sites/default/files/2026-06/Rush_MicroCT_Histo_Brochure_2026.pdf [V]
- https://www.privsource.com/acquisitions/deal/zqS9bG (AccelLAB) [CC]
- https://www.instem.com/solutions/comet-assay-iv/ [CC]

**Evergen**
- https://innovate.research.ufl.edu/evergen-launches-ai-powered-bone-graft-image-processing-software/ [V]
- https://hitconsultant.net/2025/02/03/evergen-launches-ai-powered-image-processing-to-optimize-bone-graft-analysis [CC]

**Research (DOIs)**
- 10.1002/jor.25507 (PMC10947128)
- 10.1016/j.bonr.2024.101743 (PMID 38390284)
- 10.1038/s41598-024-54313-4 (PMC10881464)
- 10.1109/EMBC48229.2022.9870828 (PMID 36086069)
- 10.3389/fphy.2024.1257512
- 10.1038/s41598-021-03542-y
- 10.1007/s11517-026-03686-x (PMID 42832161)
- 10.1038/s41598-025-92954-1
- 10.1038/s41598-025-19698-w
- 10.3389/fbinf.2025.1677527
- arXiv:2411.17260
- 10.3791/67235
- 10.1016/j.bone.2020.115653
- 10.1038/boneres.2015.37 (PMID 26816658)
- PMC8374260 (Visiopharm osteoclast protocol)
- 10.1038/s41592-020-01008-z (nnU-Net)
- 10.1002/jbmr.141 (Bouxsein)
- 10.12688/wellcomeopenres.16619.2 (BoneJ2)
- 10.1016/j.bone.2010.08.023 (BoneJ)
