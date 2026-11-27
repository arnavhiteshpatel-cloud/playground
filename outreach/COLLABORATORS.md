# OsteoQuant: Collaborator Map

Prepared 2026-11-27. Status of OsteoQuant at time of writing: pre-incorporation research prototype (software) plus synthetic-phantom benchmark. There are no physical scans, no customer data and no validated results on real graft tissue. Nobody has been contacted. All emails are drafts in `OUTREACH_EMAILS.md`.

## Evidence labels

| Label | Meaning |
|---|---|
| **[V]** | Verified on 2026-11-27 against an official page (university, faculty or facility site) or a PubMed/Crossref record. |
| **[CC]** | Cross-checked: two or more independent sources agree, but none of them is the primary official page. |
| **[RF]** | Reported by a single secondary source, such as a search-engine summary or a news item. Not confirmed on a primary page. |
| **[INF]** | My inference from verified facts. |
| **[HYP]** | Hypothesis or proposal that has not been tested. |
| **[UNR]** | Unresolved. I could not verify it, so do not rely on it. |

**Contact-info rule:** an email or phone appears here only if I saw it on an official page, or as the corresponding-author address printed in a peer-reviewed paper (flagged as such). Where none was found, the entry says so. **Do not guess addresses.**

**DOIs:** every paper DOI below was retrieved from PubMed E-utilities or Crossref on 2026-11-27 **[V]**. "bioRxiv" items are preprints, not peer-reviewed.

---

## 0. Quick ranking (who first and why)

| Rank | Contact | Why now | Ask |
|---|---|---|---|
| 0 | **UIUC OTM** and the **Landuyt Center IP Clinic** (not collaborators) | Before any faculty conversation turns technical, establish who owns what. See `IP_AND_OTM_QUESTIONS.md`. | Ownership determination and guidance |
| 1 | **Beckman Microscopy Suite** (Versa 630 staff) | Access is the gating item for the physical phantom. The answer on which billing category a pre-incorporation founder qualifies for decides cost and IP exposure. | Access path, rate category, training, and tissue/biosafety rules |
| 2 | **Mariana Kersh** (MechSE, Beckman 4043, Carle Illinois HIP) | Bone-imaging and biomechanics PI based in Beckman. Her Tissue Biomechanics Lab was named as an early Versa 630 user. She is the best fit as imaging-science supervisor for the phantom experiment. | 20-minute meeting, and a possible advisor/supervisor role for the phantom |
| 3 | **Amy Wagoner Johnson** (MechSE) | Co-author on the closest local prior art: automated micro-CT segmentation of bone vs calcium-phosphate scaffold (Polak et al. 2012). | Critique of the ground-truth design; BCP know-how |
| 4 | **Brendan Harley** (ChBE/BIOE/MSE) | Mineralized-collagen bone scaffolds. Co-author on a 2026 Current Protocols micro-CT segmentation protocol for mineral in scaffolds. | Scientific critique; later, a properly papered dataset or benchmark collaboration |
| 5 | **Justine C. Lee** (UCLA) | Senior author of that 2026 micro-CT segmentation protocol, and runs a calvarial-defect lab. | Comparison against their protocol; future validation partner |
| 6 | **Kirk McGilvray** (CSU OBRL / TMI) | Large-animal orthopaedic preclinical work. A potential end user and validation partner. | Customer-discovery interview plus a validation conversation |
| 7 | **Andrew H. Lee** (Midwestern Univ.) | BONe deep-learning bone segmentation. Paper is CC BY; models are on Dryad. | Use BONe as a benchmark comparator; joint benchmark |
| 8 | **Mark Anastasio** (now WashU; ex-UIUC BIOE head) | Imaging-science rigor: virtual imaging trials, stochastic numerical phantoms, AI hallucination taxonomy. | Critique of the synthetic-phantom benchmark methodology |

Second wave (no email drafted): Steven Boyd, Robert Guldberg, Christian Puttlitz, Jeremiah Easley/PSRL, Brad Sutton, Iwona Jasiuk, Annette McCoy, Matthew Wheeler, Timothy Fan, Rohit Bhargava, the UIUC Veterinary Diagnostic Lab, Markus Laubach and Ralph Müller.

---

## 1. University of Illinois Urbana-Champaign

### 1.1 Beckman Institute Microscopy Suite: ZEISS Xradia Versa 630

- **Institution / unit:** Beckman Institute, UIUC. Microscopy Suite, 405 N. Mathews Ave, Urbana IL 61801. Versa is in room B0530 **[V]**.
- **Instrument:** ZEISS Xradia Versa 630. Source 160 kV / 25 W. Spatial resolution 500 nm. Objectives 0.4X/4X/20X/40X plus flat panel. Automated filter wheel. LabDCT. Deben in-situ tension/compression stage **[V]** ([equipment page](https://microscopy.beckman.illinois.edu/equipment/zeiss-versa-630)). Installed January 2024, and described as the first 630 in the U.S. for life-science applications **[CC]** ([Beckman news 2024-04-29](https://beckman.illinois.edu/news/article/2024/04/29/ct-ing-is-believing-beckman-s-new-microct-scanner-supports-foundational-materials-research)).
- **Staff contacts on the Versa page [V]:**
  - Primary: Josh Gibson, jcgibso2@illinois.edu
  - Secondary: Cate Wallace, ctopha2@illinois.edu
  - Secondary: T Josek, josek1@illinois.edu
  - Suite: itg-ms@beckman.illinois.edu, (217) 333-5493
  - A search result also showed (217) 300-0566 for the suite **[UNR]**. Use 333-5493, which is on the current pages.
- **Relevant facts:** The Beckman 2024 article names T. Josek and Josh Gibson as microscopists working with the scanner. It also names a Tissue Biomechanics Lab researcher (Kersh lab) using the Deben stage with digital volume correlation on bone **[V]**.
- **Rates and access:** see `../validation/BECKMAN_ACCESS.md`.
- **Why relevant:** This is the local instrument for the first physical phantom experiment. Staff can also advise on settings, beam hardening and sample containment.
- **Proposed project:** a fee-for-service phantom scan series (Protocol v1), with staff consultation on scan-parameter choices.
- **Founder contributes:** prepared specimens, the scan plan, the analysis pipeline, and documentation.
- **Founder needs:** training, instrument time, guidance on containment of biological tissue, and **a billing pathway that matches the founder's status** (see the IP notes).

### 1.2 Mariana E. Kersh, PhD: top-priority faculty contact

- **Role [V]:** Associate Professor, Mechanical Science & Engineering. Director, Office of Community, Opportunity, and Engagement (MechSE). Directs the Tissue Biomechanics Lab ([profile](https://mechse.illinois.edu/people/profile/mkersh)). She is a Health Innovation Professor at Carle Illinois College of Medicine **[RF]**, per search summary of the Beckman/MechSE directory.
- **Contact [V]:** mkersh@illinois.edu, (217) 300-0495, 4043 Beckman Institute. Lab site: http://uitbl.mechse.illinois.edu
- **Research [V]:** mechanical properties of musculoskeletal tissues, structure–function, imaging and finite-element modelling. Current work includes bone adaptation and fatigue in human and equine athletes.
- **Recent papers [V]:**
  1. Moshage SG, McCoy AM, Kersh ME. *Elastic Modulus and Its Relation to Apparent Mineral Density in Juvenile Equine Bones of the Lower Limb.* J Biomech Eng 2023. doi:10.1115/1.4062488
  2. Manandhar S, …, Kersh ME. *Spatial Variation in Young Ovine Cortical Bone Properties.* J Biomech Eng 2023. doi:10.1115/1.4056586
  3. Rogalski MP, Martelli S, Pandy MG, Kersh ME. *Role of muscle forces on strain distributions in the proximal femur.* J Biomech 2025. doi:10.1016/j.jbiomech.2025.112743
  - Also: Minton DM, …, Kersh ME, …, Konopka AR. *The common marmoset as a translational model of age-related osteoarthritis.* GeroScience 2024. doi:10.1007/s11357-024-01103-5
- **Why relevant [INF]:** Her density-calibration and CT-derived mechanics work matches OsteoQuant's need for HA-calibrated, audited morphometry. She is in the Beckman building, and her lab already uses the Versa 630.
- **Proposed project [HYP]:** She acts as faculty advisor or imaging-science reviewer for the ex vivo phantom (Protocol v1). She helps set acceptance criteria and reviews the calibration plan. A later step could compare OsteoQuant's calibrated BV/TV and TMD against her lab's established workflow, **using public or newly generated, properly licensed data only**.
- **Founder contributes:** pipeline, synthetic benchmark, audit/QC reports, specimen preparation and analysis labour.
- **Founder needs:** imaging-science supervision, a decision on scan parameters, and possibly a sponsored-access route. Any such route requires an IP determination first.

### 1.3 Amy J. Wagoner Johnson, PhD

- **Role [V]:** Professor and Andersen Faculty Scholar, MechSE. Former Head of Biomedical & Translational Sciences, Carle Illinois (2019–2024) ([profile](https://mechse.illinois.edu/people/profile/ajwj)).
- **Contact [V]:** ajwj@illinois.edu, (217) 265-5581, 2101A Mechanical Engineering Laboratory
- **Research [V]:** bone tissue engineering, including the design, fabrication and microstructural characterization of calcium-phosphate (BCP/HA) scaffolds with multiscale porosity. Her recent publications move toward collagen mechanics and reproductive tissue **[V, PubMed list]**.
- **Papers [V]:**
  1. Polak SJ, Candido S, Levengood SK, Johnson AJ. *Automated segmentation of micro-CT images of bone formation in calcium phosphate scaffolds.* Comput Med Imaging Graph 2012. doi:10.1016/j.compmedimag.2011.07.004. This is the closest prior art; it is older than the 2022–26 window but essential.
  2. Lan Levengood SK, Polak SJ, Wheeler MB, …, Wagoner Johnson AJ. *Multiscale osteointegration as a new paradigm for the design of calcium phosphate scaffolds for bone regeneration.* Biomaterials 2010. doi:10.1016/j.biomaterials.2010.01.052
  3. Recent work, not bone-specific: Ostadi Moghaddam A, …, Wagoner Johnson AJ. *Orientation-dependent indentation reveals the crosslink-mediated deformation mechanisms of collagen fibrils.* Acta Biomater 2023. doi:10.1016/j.actbio.2023.01.005
- **Why relevant:** Polak 2012 addresses the same problem, separating bone from CaP scaffold when attenuations overlap. OsteoQuant must cite it and show what it adds: audit trail, uncertainty, calibration, and multi-material support.
- **Proposed project [HYP]:** a critique of the ground-truth design for the BCP/HA arm of the phantom. She may also advise on microporous BCP granules (sub-voxel porosity is a key confound).
- **Founder needs:** materials-science input on microporosity and density, and possibly access to BCP fabrication know-how. Fabrication would be done only under a written agreement.

### 1.4 Brendan A. C. Harley, ScD

- **Role [V]:** Robert W. Schaefer Professor (ChBE). Profile lists Bioengineering, MSE and IGB affiliations, and program leadership in the Cancer Center ([profile](https://bioengineering.illinois.edu/people/bharley)).
- **Contact [V]:** bharley@illinois.edu, (217) 244-7112, 110 Roger Adams Laboratory. Lab: http://publish.illinois.edu/harleylab/
- **Research [V]:** biomaterials that mimic tissue microenvironments, including mineralized collagen scaffolds for craniofacial bone, tendon-to-bone interfaces, and marrow niches.
- **Recent papers [V]:**
  1. Kang Y, Shariati K, Cascavita CT, Ren X, **Harley BAC**, Xu S, Lee JC. *Evaluating Mineral Deposition in Bone-Regenerative Collagen-Based Scaffolds Using High-Resolution microCT and 3D Computational Segmentation.* Curr Protoc 2026. doi:10.1002/cpz1.70306
  2. Kolliopoulos V, Harley BA. *Mineralized collagen scaffolds for regenerative engineering applications.* Curr Opin Biotechnol 2024. doi:10.1016/j.copbio.2024.103080
  3. Ren X, …, Harley BAC, Lee JC. *Osteoprotegerin-eluting nanoparticulate mineralized collagen scaffolds improve skull regeneration.* Biomater Adv 2023. doi:10.1016/j.bioadv.2022.213262
  - Background: Dewey MJ, Milner DJ, …, Wheeler MB, Harley BAC. *Repair of critical-size porcine craniofacial bone defects using a collagen–polycaprolactone composite biomaterial.* Biofabrication 2021. doi:10.1088/1758-5090/ac30d5
  - Preprint: Adorno GR, …, Bhargava R, …, Harley BAC. *Multi-material delivery strategies to create deferoxamine-functionalized collagen scaffolds for craniofacial bone repair.* bioRxiv 2026. doi:10.64898/2026.11.07.765092 (preprint)
- **Why relevant:** Mineralized scaffolds are exactly the "residual graft" class that is hard to separate from new bone. The 2026 protocol paper is a methodological reference point.
- **Proposed project [HYP]:** a non-confidential scientific critique first. Later, possibly, a benchmark of OsteoQuant vs the Curr Protoc segmentation workflow on **published or newly generated, licensed** data.
- **Founder must not** use Harley-lab data or resources without a written agreement and OTM clearance.
- **Founder needs:** domain knowledge of mineralized-scaffold radiodensity, and in the future, licensed reference datasets.

### 1.5 Mark A. Anastasio, PhD: moved to WashU

- **Current role [V]:** Vice Chair, Imaging Sciences and AI Research; Mallinckrodt Endowed Professor in Imaging Sciences; Director, Center for Computational and AI-Enabled Imaging Sciences, Washington University in St. Louis (ESE / MIR). He was Head of UIUC Bioengineering from 2019 to 2025 ([WashU profile](https://engineering.washu.edu/faculty/Mark-Anastasio.html)).
  - **Some Illinois pages still list him as BIOE head. They are outdated [V].**
- **Contact [V]:** anastasio@wustl.edu. Lab: https://anastasiolab.wustl.edu. No phone is listed.
- **Research [V]:** computational and AI-enabled imaging science, tomographic reconstruction and inverse problems, observer-based image quality, and virtual imaging trials.
- **Recent papers [V]:**
  1. Brooks FJ, Anastasio MA. *A Taxonomy of Machine Hallucination in Radiology.* Radiol Artif Intell 2026. doi:10.1148/ryai.250203
  2. Lu C, Sengupta S, Li H, Anastasio MA. *Observer-Usable Information as a Task-Specific Image Quality Metric.* IEEE Trans Med Imaging 2026. doi:10.1109/TMI.2026.3680092
  3. Huang HK, Kuo J, Park S, Villa U, Wang LV, Anastasio MA. *Stochastic numerical head phantoms to enable virtual imaging studies of transcranial photoacoustic computed tomography.* Photoacoustics 2026. doi:10.1016/j.pacs.2026.100859
  - Also: Jin R, Mohamadi S, Bramlet MT, Anastasio MA, Sutton BP. *Machine Learning-Based Privacy Preserving via CT/MRI and Organ Metadata Prediction.* J Imaging Inform Med 2026. doi:10.1007/s10278-026-02117-5
- **Why relevant [INF]:** OsteoQuant's synthetic-phantom benchmark is a form of virtual imaging trial. His stochastic-phantom and hallucination work bears directly on whether a deep-learning segmenter "invents" bone inside graft.
- **Proposed project [HYP]:** a methodology critique of the phantom generator and its task-based metrics. Possibly a student project on hallucination testing of bone/graft segmenters.
- **Founder needs:** imaging-science rigor, including task-based evaluation and the realism of the forward model.

### 1.6 Brad Sutton, PhD

- **Role [V]:** Founder Professor in Bioengineering. Health Innovation Professor, Carle Illinois (2022–2027). Technical Director of the Beckman Biomedical Imaging Center since 2014 ([profile](https://bioengineering.illinois.edu/people/bsutton)). A 2026 Beckman article states he became **director** of BIC on June 15 **[V]** ([article](https://beckman.illinois.edu/news/article/2026/07/07/sutton--webb-named-to-mri-research-leadership-positions)).
- **Contact [V]:** bsutton@illinois.edu, (217) 244-5154, 1215C Beckman Institute
- **Research [V]:** MRI physics: image reconstruction, diffusion, elastography and dynamic imaging.
- **Papers [V]:**
  1. Sutton BP, …, Malandraki GA. *SimulScan and Partial Least Squares…* Magn Reson Med 2026. doi:10.1002/mrm.70481
  2. Lin S, Sutton BP, …, Klatt D. *Simultaneous Acquisition of MRE and DTI…* Magn Reson Med 2026. doi:10.1002/mrm.70396
  3. Jin R, …, Anastasio MA, Sutton BP. J Imaging Inform Med 2026. doi:10.1007/s10278-026-02117-5
- **Why relevant [INF]:** moderate. He runs imaging-core infrastructure, and his work on reconstruction and imaging-data governance is relevant. He is not a micro-CT bone specialist.
- **Proposed project:** advice on imaging-core data governance and reconstruction QA. Low priority.

### 1.7 Iwona M. Jasiuk, PhD

- **Role [V]:** Professor and Richard W. Kritzer Faculty Scholar, MechSE. Health Innovation Professor, Carle Illinois ([profile](https://mechse.illinois.edu/people/profile/ijasiuk)).
- **Contact [V]:** ijasiuk@illinois.edu, (217) 333-9259, 2023 Sidney Lu Mechanical Engineering Building
- **Papers [V]:**
  1. Rezapourian M, Kamboj N, Jasiuk I, Hussainova I. *Biomimetic design of implants for long bone critical-sized defects.* J Mech Behav Biomed Mater 2022. doi:10.1016/j.jmbbm.2022.105370
  2. Schwarcz HP, Jasiuk I. *The function of citrate in bone: platelet adhesion and mineral nucleation.* J Mech Behav Biomed Mater 2025. doi:10.1016/j.jmbbm.2025.107077
  3. Pang S, Jasiuk I. *Correlation between reference point indentation and mechanical properties of 3D-printed polymers.* Rev Sci Instrum 2023. doi:10.1063/5.0149701
- **Why relevant:** bone hierarchical structure and critical-size defect implant design. A possible reviewer for bone-surrogate choice.

### 1.8 Annette M. McCoy, DVM, MS, PhD, DACVS: Veterinary Medicine

- **Role [V]:** Associate Professor, Equine Surgery, Department of Veterinary Clinical Medicine. Associate Professor, Beckman Institute ([profile](https://vetmed.illinois.edu/directory/profile?id=mccoya)).
- **Contact:** phone (217) 300-3492 **[V]**. **No email appears in the profile text [UNR].** Do not infer one; ask by phone or through the department.
- **Papers [V]:**
  1. McCoy AM, …, Easley J, Gadomski BC, …, Goodman SB. *2026 International Consensus Meeting on Preclinical Models of Osteoarthritis: Summary From the Workgroup on Post-Traumatic Osteoarthritis.* J Orthop Res 2026. doi:10.1002/jor.70330
  2. McCoy AM, …, Kemper AM. *Natural progression of tarsal osteochondrosis in Standardbred pacers and trotters.* Vet Surg 2026. doi:10.1111/vsu.70073
  3. Moshage SG, McCoy AM, Kersh ME. J Biomech Eng 2023. doi:10.1115/1.4062488
- **Why relevant:** a large-animal orthopaedic clinician-scientist who collaborates with Kersh. She co-authored the 2026 preclinical-model consensus alongside the CSU PSRL team, which makes her a bridge to preclinical end users.

### 1.9 Veterinary pathology: UIUC Veterinary Diagnostic Laboratory (Anatomic Pathology)

- **What I found [V]:** The VDL anatomic pathology service offers histopathology, special stains, IHC, biopsy and necropsy. **Decalcification and research histology are not listed** ([page](https://vdl.vetmed.illinois.edu/anatomic-pathology)). Contact: 2001 S Lincoln Ave, Urbana. 217-333-1620.
- **Named bone pathologist:** **not identified [UNR]**. A search surfaced Anne Barger (Pathobiology/VDL, bone-tumor RANKL work with Tim Fan) **[RF]**, but her bone-histomorphometry expertise is unverified.
- **Why relevant:** Histology is needed later, for in vivo validation where real new bone exists. It is **not** needed for Protocol v1, which uses ex vivo butcher bone with no new bone.

### 1.10 Timothy M. Fan, DVM, PhD

- **Role [V]:** Professor, Veterinary Clinical Medicine. Khan Family Chair in Veterinary Oncology Research. Associate Director for Translational R&D, Cancer Center at Illinois.
- **Contact [V]:** t-fan@illinois.edu, (217) 333-5375 ([profile](https://vetmed.illinois.edu/directory/profile?id=t-fan))
- **Relevance:** low to moderate. He works on the bone tumor microenvironment and osteolysis in canine osteosarcoma, which is an adjacent micro-CT use case. Papers were not reviewed in depth, and none are listed here to avoid padding.

### 1.11 Matthew B. Wheeler, PhD

- **Role [V]:** Professor of Animal Sciences and of Bioengineering, Biomedical and Translational Sciences, IGB, Beckman, and others ([Illinois Experts](https://experts.illinois.edu/en/persons/matthew-b-wheeler)).
- **Contact:** **email not captured from an official page [UNR]**.
- **Papers [V]:**
  1. Dewey MJ, …, Wheeler MB, Harley BAC. Biofabrication 2021. doi:10.1088/1758-5090/ac30d5 (porcine critical-size craniofacial)
  2. Ho NC, …, Sangiorgio SN. *Evaluation of Topology Optimization Using 3D Printing for Bioresorbable Fusion Cages: A Biomechanical Study in a Porcine Model.* Spine 2023. doi:10.1097/BRS.0000000000004491
  3. Capron G, …, Wheeler MB. *3D-Printed Gastrointestinal Stents: In Vivo Evaluation in a Swine Small Bowel Perforation Model.* Adv Healthc Mater 2026. doi:10.1002/adhm.202505169
- **Relevance:** porcine large-animal models. He is a later-stage contact for in vivo validation data.

### 1.12 Rohit Bhargava, PhD

- **Role [V]:** Grainger Distinguished Chair; Professor of Bioengineering; Director of the Cancer Center at Illinois ([profile](https://bioengineering.illinois.edu/people/rxb)).
- **Contact [V]:** rxb@illinois.edu
- **Relevance [INF]:** chemical (IR/Raman) imaging could become an *orthogonal* ground truth for mineral phase (HA vs β-TCP vs biological apatite) in histological sections. He co-authored Harley's 2026 craniofacial preprint (doi:10.64898/2026.11.07.765092, preprint). Later stage.

---

## 2. Colorado State University: Translational Medicine Institute (TMI)

### 2.1 Kirk C. McGilvray, PhD: priority CSU contact

- **Role [V]:** Associate Director, Orthopaedic Bioengineering Research Laboratory (OBRL). Associate Department Head for Graduate Programs. Associate Professor, Mechanical Engineering and School of Biomedical Engineering. Core faculty, TMI ([profile](https://www.engr.colostate.edu/me/faculty/dr-kirk-mcgilvray)).
- **Contact [V]:** kirk.mcgilvray@colostate.edu, 970-491-1319, A105 Engineering
- **Interests [V]:** fracture-healing prediction, preclinical model development, biomaterial assessment, orthopaedic device R&D.
- **Papers [V]:**
  1. Winston SE, …, Puttlitz C, Pezzanite LM, McGilvray KC. *Fuzzy-logic-driven predictions of multi-tissue ingrowth for rapid screening of mechanically instructive tissue-engineering scaffolds.* Biomed Mater 2026. doi:10.1088/1748-605X/ae574d
  2. Bisazza KT, Nelson BB, Anthony RV, Goodrich LR, McGilvray KC, Easley JT. *A comprehensive longitudinal study quantifying the systemic effects associated with ovariectomy and high-dose corticosteroids in a sheep model of osteoporosis.* Ann Transl Med 2026. doi:10.21037/atm-2026-0112
  3. Labus KM, Dunn J, Ilić M, Notaroš BM, McGilvray KC, Puttlitz CM. *Remote monitoring of bone healing via bending with direct electromagnetic coupling sensing in an exploratory tibial fracture study.* Injury 2025. doi:10.1016/j.injury.2025.112771
- **Why relevant:** OBRL and PSRL run ovine and other large-animal orthopaedic studies, often for device sponsors. Labs like this are the likely *users* of audited graft/bone morphometry.
- **Proposed project [HYP]:** a 30-minute customer-discovery interview about how they currently separate graft from new bone, and what an audit trail must contain for GLP or sponsor reports. Later, a blinded re-analysis of **sponsor-released or public** scans under a data-use agreement.
- **Founder contributes:** free pilot analysis on released data, and an audit-report format.
- **Founder needs:** real-world requirements, GLP context, and eventually licensed validation data.

### 2.2 Christian M. Puttlitz, PhD

- **Role [V]:** Department Head and Professor, Mechanical Engineering. Director, OBRL. Professor in Clinical Sciences, School of Advanced Materials Discovery and School of Biomedical Engineering ([profile](https://www.engr.colostate.edu/me/faculty/dr-christian-m-puttlitz)).
- **Contact [V]:** christian.puttlitz@colostate.edu
- **Papers [V]:** Labus 2025 Injury (doi:10.1016/j.injury.2025.112771). Winston 2026 Biomed Mater (doi:10.1088/1748-605X/ae574d). Gadomski BC, …, Puttlitz CM, McGilvray KC, Regan DP, Easley JT. *A Large Animal Model for Orthopedic Foot and Ankle Research.* Front Vet Sci 2022. doi:10.3389/fvets.2022.816529
- **Note:** As department head he is a better second contact, after McGilvray.

### 2.3 Jeremiah T. Easley, DVM, and the Preclinical Surgical Research Laboratory (PSRL)

- **Role [V]:** PSRL team page lists "Jeremiah Easley, D.V.M., Director, GLP Test Facility Manager" ([team](https://vetmedbiosci.colostate.edu/psrl/team/)). PSRL is housed in TMI and does GLP and non-GLP in vivo preclinical testing. It partners with OBRL for ex vivo services **[V]** ([PSRL](https://vetmedbiosci.colostate.edu/psrl/)).
- **Contact [V]:** **no email is listed**. Use the PSRL contact form (https://vetmedbiosci.colostate.edu/psrl/contact/) or call (970) 682-0079. The page shows two different Campus Delivery addresses **[UNR]**.
- **Papers [V]:**
  1. Koch DW, Johnson JW, Smith QE, Brekhus C, Gadomski BC, Palmer RH, Easley JT, Nelson BB. *Biomechanical evaluation of interlocking nail and locking compression plating for stabilization of ovine critical-sized segmental tibia defects.* Ann Transl Med 2023. doi:10.21037/atm-22-4886
  2. Bisazza 2026 Ann Transl Med. doi:10.21037/atm-2026-0112
  3. Bonilla AF, …, Easley JT. *Ovine models of intervertebral disc degeneration.* Ann Transl Med 2025. doi:10.21037/atm-25-136
- **Relevance:** a GLP preclinical facility running ovine critical-sized defect models. This is a key future customer/validator. Contact after the McGilvray conversation.
- Other PSRL scientists listed **[V]**: Brad Nelson, Drew Koch, Katie Bisazza, Andrés Bonilla. Ben Gadomski appears as co-author on many OBRL/PSRL papers **[V, PubMed]**.

---

## 3. External investigators: micro-CT of grafts and defects, and DL segmentation

### 3.1 Justine C. Lee, MD, PhD (UCLA)

- **Role [V]:** Professor of Surgery and of Orthopaedic Surgery. Bernard G. Sarnat Endowed Chair in Craniofacial Biology. Craniofacial Regeneration Laboratory ([UCLA Profiles](https://profiles.ucla.edu/justine.lee)).
- **Contact [V]:** justinelee@mednet.ucla.edu. Lab phone (310) 794-7616 **[RF]**, from search summary of the lab site.
- **Papers [V]:**
  1. Kang Y, …, Harley BAC, Xu S, Lee JC. Curr Protoc 2026. doi:10.1002/cpz1.70306 (micro-CT plus 3D segmentation of mineral in scaffolds)
  2. Chen W, Bedar M, …, Harley BAC, Lee JC. *Correlating Material Properties to Osteoprotegerin Expression on Nanoparticulate Mineralized Collagen Glycosaminoglycan Scaffolds.* Adv Healthc Mater 2024. doi:10.1002/adhm.202401037
  3. Ren X, …, Harley BAC, Lee JC. Biomater Adv 2023. doi:10.1016/j.bioadv.2022.213262
- **Why relevant:** calvarial defect models with mineralized scaffolds, where residual scaffold and new bone coexist. Their protocol is a natural baseline for OsteoQuant to compare against.
- **Proposed project [HYP]:** run OsteoQuant against the Curr Protoc workflow on a shared phantom, then on licensed calvarial scans. Report agreement and audit differences.

### 3.2 Andrew H. Lee, PhD (Midwestern University, Glendale AZ): BONe

- **Role:** listed as Professor, Anatomy, in the Midwestern AZ catalog **[RF]**. Paper affiliations include Anatomy, the Arizona College of Osteopathic Medicine, the College of Veterinary Medicine and Core Facilities–Glendale **[V, paper]**.
- **Contact:** corresponding-author address printed in the 2026 Front Bioinform paper: **alee712@gmail.com** **[V, as printed in PMC12868216]**. **No institutional profile page was found [UNR].** Prefer this address only because it is the one the author published.
- **Papers [V]:**
  1. Lee AH, Talluri G, Damani M, …, Al-Nakkash L. *Deep learning software and revised 2D model to segment bone in micro-CT scans.* Front Bioinform 2025/2026. doi:10.3389/fbinf.2025.1677527. The article is CC BY. Models and code are on Dryad, doi:10.5061/dryad.4j0zpc8qq **[V, PMC page]**. Reported grand-mean IoU 0.9133 ± 0.0476 in 5-fold CV **[V, paper]**.
  2. Lee AH, Moore JM, Covarrubias BV, Lynch LM. *Segmentation of cortical bone, trabecular bone, and medullary pores from micro-CT images using 2D and 3D deep learning models.* Anat Rec 2025. doi:10.1002/ar.25633
- **Why relevant:** BONe is an openly available bone-vs-background deep-learning baseline. It is not trained for graft, which makes it a useful comparator for showing where generic bone segmenters mislabel graft as bone. Confirm the license of the Dryad model files before redistribution or commercial use **[UNR]**.
- **Proposed project [HYP]:** a joint benchmark on the OsteoQuant synthetic phantoms plus the ex vivo phantom: BONe vs OsteoQuant on graft-containing volumes. Co-authored technical note.

### 3.3 Steven K. Boyd, PhD, PEng (University of Calgary)

- **Role [V]:** Professor, Department of Radiology, Cumming School of Medicine. Joint appointments in Mechanical & Manufacturing Engineering and Biomedical Engineering ([profile](https://profiles.ucalgary.ca/steven-boyd)).
- **Contact [V]:** skboyd@ucalgary.ca, +1 (403) 220-3664
- **Papers [V]:**
  1. Neeteson NJ, Besler BA, Whittier DE, Boyd SK. *Automatic segmentation of trabecular and cortical compartments in HR-pQCT images using an embedding-predicting U-Net and morphological post-processing.* Sci Rep 2023. doi:10.1038/s41598-022-27350-0
  2. Walle M, Matheson BE, Boyd SK. *Comparing linear and nonlinear finite element models of vertebral strength across the thoracolumbar spine: a benchmark from density-calibrated computed tomography.* GigaScience 2025. doi:10.1093/gigascience/giaf094
  3. Neeteson NJ, Hasick SM, Souza R, Boyd SK. *Automated quantitative analysis of peri-articular bone microarchitecture in HR-pQCT knee images.* Comput Methods Programs Biomed 2025. doi:10.1016/j.cmpb.2025.108882
  - Co-author on the micro-CT reporting guideline: Bouxsein ML, Boyd SK, Christiansen BA, Guldberg RE, …, Müller R. JBMR 2010. doi:10.1002/jbmr.141
- **Relevance:** density calibration, DL compartment segmentation, and reproducible open benchmarks. Second wave.

### 3.4 Robert E. Guldberg, PhD (University of Oregon, Knight Campus)

- **Role [V]:** Vice President and Robert and Leona DeArmond Executive Director, Knight Campus. PI of the Guldberg Lab ([profile](https://knightcampus.uoregon.edu/robert-guldberg)). His profile states he has co-founded six start-ups **[V]**.
- **Contact [V]:** guldberg@uoregon.edu
- **Papers [V]:**
  1. Strait LK, …, Guldberg RE. *Local and systemic immune responses during rhBMP-2 mediated bone regeneration are dose-dependent in rat model of critical-sized bone defect healing.* Bone 2026. doi:10.1016/j.bone.2026.118084
  2. Williams KE, …, Guldberg RE. *Early resistance rehabilitation improves functional regeneration following segmental bone defect injury.* NPJ Regen Med 2024. doi:10.1038/s41536-024-00377-9
  3. Muhib F, Williams KE, LaBelle SA, Lin ASP, Guldberg RE, Weiss JA. *Development of a subject-specific finite element analysis workflow to assess local biomechanics during segmental bone defect healing.* J Mech Behav Biomed Mater 2025. doi:10.1016/j.jmbbm.2025.107065
- **Relevance:** the canonical rat segmental-defect micro-CT model, plus startup experience. An advisor-type contact after there is real-data evidence.

### 3.5 Markus Laubach, MD (LMU Munich / formerly QUT)

- **Role [RF]:** surgeon-scientist at the LMU University Hospital Musculoskeletal University Center Munich (from a search summary and a Bayern Innovativ listing). **Contact not verified [UNR].**
- **Papers [V]:**
  1. Cheers GM, …, Holzapfel BM, Laubach M. *Mechanobiological compartmentalization in scaffold-guided bone regeneration for large segmental long-bone defects.* Biomaterials 2027 (online 2026). doi:10.1016/j.biomaterials.2026.124676
  2. Laubach M, …, Hutmacher DW, Medeiros Savi F. *In vivo characterization of 3D-printed polycaprolactone-hydroxyapatite scaffolds with Voronoi design…* Front Bioeng Biotechnol 2023. doi:10.3389/fbioe.2023.1272348
  3. Laubach M, …, Bock N. *An innovative intramedullary bone graft harvesting concept as a fundamental component of scaffold-guided bone regeneration…* J Orthop Translat 2024. doi:10.1016/j.jot.2024.05.002
- **Relevance:** ovine large-segmental-defect scaffold-guided regeneration with PCL-HA (scaffold plus graft plus new bone). Third wave.

### 3.6 Ralph Müller, PhD (ETH Zürich)

- **Contact: not verified [UNR].** bone.ethz.ch could not be reached from this environment; the host would need allowing in network settings.
- **Papers [V]:**
  1. Griesbach JK, Schulte FA, Schädli GN, Rubert M, Müller R. *Mechanoregulation analysis of bone formation in tissue engineered constructs requires a volumetric method using time-lapsed micro-computed tomography.* Acta Biomater 2024. doi:10.1016/j.actbio.2024.03.008
  2. Kendall JJ, …, Müller R. *Agent-based modelling of late-stage mechanical loading of femur defects in prematurely ageing PolgA mice.* Front Bioeng Biotechnol 2026. doi:10.3389/fbioe.2026.1879777
  3. Bouxsein ML, …, Müller R. JBMR 2010. doi:10.1002/jbmr.141
- **Relevance:** time-lapse micro-CT of scaffolds. Registration-based formation/resorption labelling is the conceptual basis of the pre-fill/post-fill truth design. Literature reference rather than a near-term contact.

### 3.7 Also useful as literature (not proposed contacts)

- Lima JR, …, Oliveira GJPL. *Effect of different thresholds on the accuracy of linear and volumetric analysis of native- and grafted-bone.* Braz Dent J 2022. doi:10.1590/0103-6440202204823 **[V]**. Directly relevant to threshold sensitivity.
- Lesage C, …, Mabilleau G. *Comprehensive Characterization of Tissue Mineralization in an Ex Vivo Model.* J Vis Exp 2024. doi:10.3791/67235 **[V]**
- Touré A, …, Weiss P. *BMP-2-Loaded Self-Crosslinking CaP/Hydrogel Composite Enables Complete Regeneration of Critical-Sized Segmental Bone Defects.* Bioengineering 2026. doi:10.3390/bioengineering13080888 **[V]**

---

## 4. Cross-cutting cautions

1. **IP and resources [V policy pointers; INF application].** UIUC policy (General Rules Art. III; Statutes Art. XII) makes OTM the body that determines ownership. Student IP made with University facilities, equipment or funds beyond those "usually and customarily provided" falls under standard University ownership rules. Get a written ownership determination **before** using a faculty sponsor's account, Beckman internal rates, ITG data storage, or lab data. See `IP_AND_OTM_QUESTIONS.md`.
2. **No confidential disclosure in first emails.** Keep the first contact non-confidential: describe what exists and what is asked, not novel methods.
3. **No overclaiming.** Say "research prototype" and "synthetic-phantom benchmark". Make no claims of validation, accuracy on real grafts, or customers.
4. **Data.** Do not request or accept lab data without a written data-use agreement routed through the institution.
