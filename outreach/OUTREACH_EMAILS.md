# Outreach Email Drafts: NOT SENT

Drafted 2026-11-27. **Nothing here has been sent.** Read each draft, edit it, and send it yourself only after the pre-send checklist passes.

## Pre-send checklist (all must be true)

- [ ] You have talked to UIUC OTM (otm@illinois.edu) and/or the Landuyt Center, or at least read `IP_AND_OTM_QUESTIONS.md` and decided how to describe the project's independence.
- [ ] Every `[INSERT …]` placeholder is filled with a **real** number from your own synthetic-phantom Experiment B/C logs, or the sentence is deleted.
- [ ] No sentence claims validation, accuracy on real graft tissue, customers, pilots, partnerships, funding or incorporation.
- [ ] No novel algorithm details are disclosed. Describe *what it does*, not *how*.
- [ ] Contact address re-checked on the official page the same day you send (see `collaborators.csv`, column `contact_source_url`).
- [ ] Use your university email for UIUC recipients only if OTM has said that is fine for this project. Otherwise use a personal or project address and say you are a UIUC student.

Placeholders: `[Your Name]`, `[Year/Major]`, `[project email]`, `[link to 1-page summary]`.

**Standard IP paragraph.** Each draft carries a version of this:

> To be transparent: OsteoQuant is an independent project that I'm developing outside of any university lab, and I have not used university lab data or lab resources for it. I'd like to keep our first conversation non-confidential. If we decide to work together on anything, I'd want us to agree on terms in writing first (and route them through the appropriate university offices) before any data, code or unpublished ideas are exchanged.

---

## 1. Beckman Microscopy Suite: Versa 630 access (send FIRST)

**To:** itg-ms@beckman.illinois.edu
**Cc (optional):** josek1@illinois.edu, jcgibso2@illinois.edu
**Subject:** Versa 630 access question: ex vivo bone/graft phantom (independent project)

Hello Microscopy Suite team,

My name is [Your Name], and I'm a [Year/Major] student at Illinois. I'm planning a small ex vivo micro-CT phantom experiment and would like to understand whether, and how, I could use the ZEISS Xradia Versa 630.

The samples would be butcher-sourced bovine bone cores, roughly 25 mm in diameter by 15 mm tall, with small drilled defects. The defects would be filled with known masses of commercial bone-graft granules: hydroxyapatite, β-TCP, BCP, 45S5 bioactive glass and calcium sulfate. No live animals and no human tissue are involved. Samples would be sealed in polypropylene tubes and stored in 70% ethanol unless you advise otherwise. I'd expect roughly [35–90] instrument hours in total at 10, 20 and 40 µm voxel sizes, after a short pilot.

I have a few questions before I go further:

1. This is an independent, pre-incorporation software project (OsteoQuant), not part of a faculty lab. Which user and billing category would apply? The fees page lists internal, internal with F&A, external, and external with F&A ("businesses with a working contract"). Is there a route for a not-yet-incorporated student project, and does it require a CFOP or a contract?
2. Are the posted Versa 630 rates ($40.00 / $52.68 / $60.00 / $79.02 per hour, effective 1 Aug 2021) still current? How is training billed and how long does it usually take?
3. Do you have rules for animal-tissue samples: containment, the BL-2 room, fixative versus ethanol, and maximum sample size or weight?
4. Does the suite have an HA (hydroxyapatite) density calibration phantom users can scan, or should I bring my own?
5. Can scan data be written to user-owned storage? I understand the default is the ITG CTData drive.

To be transparent: this is independent work outside any university lab, and I am trying to set it up correctly from the start, including checking IP questions with OTM. I'm happy to come in for an orientation at whatever time suits you.

Thank you,
[Your Name]
[project email]

---

## 2. Prof. Mariana Kersh (MechSE / Beckman)

**To:** mkersh@illinois.edu
**Subject:** Seeking 20 minutes of advice: calibrated micro-CT phantom for bone vs graft separation

Dear Prof. Kersh,

I'm [Your Name], a [Year/Major] student with research experience in orthopedic imaging and fracture detection. I've followed your lab's work on CT-derived density and bone mechanics, including Moshage, McCoy & Kersh (J Biomech Eng 2023), and I saw that your group was an early user of the Beckman Versa 630.

I've been building OsteoQuant, an independent software project aimed at a narrow problem in preclinical micro-CT: separating new bone, residual graft and host bone in defect models, and producing morphometry reports with a full audit trail (calibration, parameters, QC flags, uncertainty). I have built a research prototype pipeline and a synthetic-phantom benchmark. [INSERT 1–2 sentence result summary from Experiment B/C.] I have not yet tested it on any physical scans. That is exactly the gap I want to close carefully.

My next step is an ex vivo phantom: bovine trabecular cores with drilled defects filled with weighed graft granules. Ground truth comes from construction, from a pre-fill scan registered to the post-fill scan, and from gravimetric mass. I would scan at 10, 20 and 40 µm with an HA calibration phantom and repeat scans. I've drafted a protocol, but several decisions should be made by someone with real micro-CT expertise rather than by me. These include the voxel sizes, the energy and filter choice, wet versus dry scanning, the calibration approach, and the acceptance criteria.

Would you be willing to meet for 20 minutes to look at the design and tell me what's wrong with it? I'm not asking for lab resources or data.

To be transparent: OsteoQuant is an independent project developed outside any university lab, and I haven't used university lab data or resources for it. I'd like to keep this first conversation non-confidential. If anything beyond advice made sense later, I'd want us to agree on terms in writing first, through OTM, before any data, code or unpublished ideas are exchanged.

Thank you for considering it,
[Your Name]
[project email] · [link to 1-page summary]

---

## 3. Prof. Amy Wagoner Johnson (MechSE)

**To:** ajwj@illinois.edu
**Subject:** Question about bone vs calcium-phosphate segmentation (building on Polak et al. 2012)

Dear Prof. Wagoner Johnson,

I'm [Your Name], a [Year/Major] student at Illinois. I've been reading Polak, Candido, Levengood & Johnson, "Automated segmentation of micro-CT images of bone formation in calcium phosphate scaffolds" (Comput Med Imaging Graph 2012), because it addresses the problem I'm working on: separating bone from calcium-phosphate graft when their attenuations overlap.

I'm developing OsteoQuant, an independent software project focused on audited separation of new bone, residual graft and host bone in preclinical micro-CT. I have built a research prototype pipeline and a synthetic-phantom benchmark. [INSERT 1–2 sentence result summary from Experiment B/C.] There are no real-scan results yet.

I'm now designing a physical ex vivo phantom with HA, β-TCP and BCP granules in bovine bone defects, with ground truth from weighed graft mass and pre-fill/post-fill registered scans. One thing worries me in particular: granule **microporosity below the voxel size**, which will bias both gray values and volumes. I'd value 15–20 minutes of your perspective on:

- whether the gravimetric "truth" approach is sound for microporous BCP;
- which granule characteristics I should measure or request from suppliers, such as skeletal density and porosity; and
- anything Polak et al. learned that I shouldn't relearn the hard way.

To be transparent: this is independent work outside any university lab, with no use of university lab data or resources. I'd like to keep our conversation non-confidential. If anything further made sense, I'd want to agree on terms in writing first, via OTM.

With thanks,
[Your Name]
[project email]

---

## 4. Prof. Brendan Harley (ChBE / BIOE)

**To:** bharley@illinois.edu
**Subject:** Scientific feedback request: micro-CT separation of residual mineralized scaffold vs new bone

Dear Prof. Harley,

I'm [Your Name], a [Year/Major] student at Illinois with research experience in orthopedic imaging and regenerative medicine. I read the 2026 Current Protocols paper by Kang et al., which you co-authored with Dr. Justine Lee's group, on evaluating mineral deposition in collagen scaffolds with high-resolution micro-CT and 3D segmentation. It describes very clearly the problem I'm focused on.

I'm developing OsteoQuant, an independent software project that aims to separate new bone, residual graft or scaffold, and host bone in preclinical micro-CT, and to produce audited morphometry reports. I have built a research prototype pipeline and a synthetic-phantom benchmark. [INSERT 1–2 sentence result summary from Experiment B/C.] I haven't analyzed any real graft or scaffold scans yet, and I'm next building a physical ex vivo phantom with known graft placement.

I'd be grateful for 15–20 minutes of your scientific perspective. In particular: in mineralized collagen scaffolds, which features would make residual scaffold mineral hardest to distinguish from early new bone on micro-CT? And what would a convincing validation look like to someone in your field?

To be clear, I'm not asking for lab data or resources. OsteoQuant is an independent project developed outside any university lab, and I haven't used university lab data or resources for it. I'd like to keep this conversation non-confidential. If a collaboration ever made sense, I'd want terms agreed in writing first, through OTM, before any data, code or unpublished ideas are exchanged.

Thank you for your time,
[Your Name]
[project email]

---

## 5. Prof. Justine C. Lee (UCLA)

**To:** justinelee@mednet.ucla.edu
**Subject:** Your 2026 Current Protocols micro-CT segmentation method: question from an independent developer

Dear Dr. Lee,

I'm [Your Name], an undergraduate at the University of Illinois with research experience in orthopedic imaging. I read Kang et al., "Evaluating Mineral Deposition in Bone-Regenerative Collagen-Based Scaffolds Using High-Resolution microCT and 3D Computational Segmentation" (Curr Protoc 2026), and found it very useful.

I'm developing OsteoQuant, an independent software project for audited separation of new bone, residual graft and host bone in preclinical micro-CT. I have built a research prototype pipeline and a synthetic-phantom benchmark. [INSERT 1–2 sentence result summary from Experiment B/C.] I have no results on real scans yet. My next step is an ex vivo phantom where graft location and mass are known by construction.

Two questions, if you have a moment:

1. In your experience, where does threshold- or segmentation-based separation of scaffold mineral and new bone fail most often in calvarial defects? For example: early woven bone, thin residual scaffold, or partial-volume edges.
2. Would your group be open to a future, properly papered comparison, in which both methods are run on the same phantom and agreement is reported? I would only use data your group chose to share under a written agreement.

To be transparent: OsteoQuant is independent work, not part of any university lab, and I'd like to keep this first exchange non-confidential. Any collaboration would start with written terms agreed by both institutions.

Thank you,
[Your Name]
[project email]

---

## 6. Dr. Kirk McGilvray (Colorado State University, OBRL)

**To:** kirk.mcgilvray@colostate.edu
**Subject:** 20-minute question about how your team separates graft from new bone in micro-CT

Dear Dr. McGilvray,

I'm [Your Name], an undergraduate at the University of Illinois with research experience in orthopedic imaging. I'm developing OsteoQuant, an independent software project for preclinical micro-CT. It aims to separate new bone, residual graft and host bone in defect models, and to produce morphometry reports with a complete audit trail: calibration, parameters, QC flags and uncertainty.

I have built a research prototype pipeline and a synthetic-phantom benchmark. [INSERT 1–2 sentence result summary from Experiment B/C.] It has not been validated on real graft data. I'm preparing a physical ex vivo phantom experiment as the next step.

Before I go further, I'd like to learn from groups that run large-animal orthopaedic studies, such as your work with Drs. Puttlitz and Easley at OBRL/PSRL. Would you have 20 minutes for a short conversation?

- How does your team currently quantify new bone versus residual graft in micro-CT? Thresholds, manual contours, histology correlation?
- What would a sponsor or a GLP reviewer need to see in an analysis report for it to be trusted?
- Where does the current workflow cost the most time or cause the most disagreement?

I'm not selling anything and I'm not asking for data. To be transparent, OsteoQuant is an independent, pre-incorporation project. I'd like to keep this conversation non-confidential, and any future work together would start with written terms.

Many thanks,
[Your Name]
[project email]

---

## 7. Dr. Andrew H. Lee (Midwestern University): BONe

**To:** alee712@gmail.com *(the corresponding-author address printed in Front Bioinform 2026; no institutional page was found, so check the latest paper or the Midwestern directory before sending)*
**Subject:** BONe as a comparator for bone vs graft segmentation: question about use

Dear Dr. Lee,

I'm [Your Name], an undergraduate at the University of Illinois. I read your paper "Deep learning software and revised 2D model to segment bone in micro-CT scans" (Front Bioinform, 2026), and I appreciate that the models and code are available on Dryad.

I'm developing OsteoQuant, an independent project focused on a related but different problem: separating new bone, residual **graft** material and host bone in preclinical defect models. I have built a research prototype pipeline and a synthetic-phantom benchmark. [INSERT 1–2 sentence result summary from Experiment B/C.] There are no real-scan results yet.

I'd like to include BONe as an external comparator in my benchmark, cited properly. Generic bone segmenters are a natural baseline for showing how often dense graft granules get labelled as bone. Could you confirm:

1. the license terms for the BP-2D-03 model files on Dryad, including whether they cover use in a benchmark by a project that may later become commercial; and
2. whether you would be interested in a joint, co-authored technical comparison on a shared phantom dataset?

To be transparent: OsteoQuant is independent work outside any university lab and is pre-incorporation. I'd like to keep this exchange non-confidential, and anything joint would start with written terms.

Thank you,
[Your Name]
[project email]

---

## 8. Prof. Mark Anastasio (Washington University in St. Louis)

**To:** anastasio@wustl.edu
**Subject:** Seeking methodological critique: synthetic phantom benchmark for bone vs graft segmentation

Dear Prof. Anastasio,

I'm [Your Name], an undergraduate at the University of Illinois with research experience in orthopedic imaging. Your recent work on task-based image quality and machine hallucination in radiology (Brooks & Anastasio, Radiol Artif Intell 2026; Lu et al., IEEE TMI 2026) shaped how I think about evaluating segmentation.

I'm developing OsteoQuant, an independent software project that separates new bone, residual graft and host bone in preclinical micro-CT and produces audited morphometry reports. I have built a research prototype pipeline and a synthetic-phantom benchmark, which is essentially a small virtual imaging study. [INSERT 1–2 sentence result summary from Experiment B/C.] I have not validated it on real scans.

The question I'd most like expert critique on: how do I make sure my synthetic phantoms don't flatter the method? I mean forward-model realism (beam hardening, partial volume, noise texture), the choice of task-based metrics, and explicit tests for a segmenter "hallucinating" bone inside graft. If you or someone in your group had 20 minutes, I'd be very grateful.

To be transparent: OsteoQuant is independent work outside any university lab and is pre-incorporation. I'd like to keep this conversation non-confidential, and anything beyond advice would start with written terms.

With thanks,
[Your Name]
[project email]

---

## Follow-up etiquette

- If there is no reply after about 10 business days, send one short follow-up. If there is still no reply, stop.
- Log every send and reply in `collaborators.csv`. A `last_contacted` column can be added.
- If someone offers data or lab resources, **pause** and go to OTM before accepting.
