# Decisions Required Before Protocol OQ-P1 Can Start

**For:** a qualified imaging scientist or lab supervisor (proposed: an advisor such as a micro-CT-experienced faculty member or Beckman Suite staff, as appropriate).
**From:** OsteoQuant founder. Drafted 2026-11-27.

Each decision lists the options, the founder's **default proposal** (marked *Proposed*), why it matters, and a sign-off line. The founder does not have the expertise to make these alone. Proposals are [INF] or [HYP] unless noted.

---

### D1. Access and billing pathway
- **Options:**
  - (a) faculty-sponsored internal rate ($40/h [V, 2021 rates])
  - (b) external rate ($60/h) or external with F&A ($79.02/h) via a contract after incorporation
  - (c) another facility or a CRO
- **Why it matters:** cost (about 2× difference) **and** IP ownership. Using a University account or equipment may trigger University ownership rules (see `../outreach/IP_AND_OTM_QUESTIONS.md`).
- *Proposed:* do not book until OTM answers A5–A8. Prefer (b) or a written sponsored-access agreement that preserves ownership.
- Decision: ______________________ Signed/date: __________

### D2. Voxel sizes and field-of-view strategy
- **Options:**
  - Whole-core 40 and 20 µm, plus 10 µm **ROI (interior) tomography** on one Ø6 defect per core.
  - Or cut smaller sub-cores for true whole-sample 10 µm.
  - Which objective or flat panel to use at each size.
- **Why it matters:** interior tomography introduces truncation artifacts that may bias 10 µm results. Scan time drives cost.
- *Proposed:* 40/20 µm whole-core; 10 µm ROI on 6 cores; pilot both options in Phase 0.
- Decision: ______________________ Signed/date: __________

### D3. Energy, filter, exposure, projections, reconstruction
- **Questions:**
  - Which kV and filter maximize HA/β-TCP/BCP/45S5/CaSO4 vs bone contrast while controlling beam hardening in a ~25 mm bone core?
  - What number of projections and exposure are needed for an adequate SNR?
  - Which reconstruction settings? **Must AI/deep-learning reconstruction options be disabled** for truth scans?
- *Proposed:* one fixed kV/filter for all main scans, chosen in Phase 0 from 2–3 candidates using phantom contrast-to-noise ratio. Standard FDK reconstruction with a fixed beam-hardening constant. **No DL reconstruction** for truth scans. If DL reconstruction is available, run a separate exploratory sub-study.
- Decision: ______________________ Signed/date: __________

### D4. Density calibration phantom
- **Options:**
  - (a) the facility's HA phantom, if one exists
  - (b) Bruker BMD phantom set, 0.3/1.25 g/cm³ CaHA, $2,296.16 [V]
  - (c) QRM micro-CT HA phantom (quote [UNR])
  - (d) DIY K2HPO4 solutions (drift QC only)
- **Also decide:** rod diameter matching the sample size, and whether to scan the phantom alongside each specimen or separately.
- *Proposed:* (a) if available, else (b) with medium rods. Separate phantom scans each session plus one full calibration per setting.
- Decision: ______________________ Signed/date: __________

### D5. Host material and core geometry
- **Questions:** Is bovine distal-femoral trabecular bone appropriate, or would porcine be better? Is a Ø25 × 15 mm core with 4 defects (Ø6/Ø4 × 8 mm) appropriate? Is the bone bridge thick enough (about 4 mm)? Should marrow be removed from the whole core (cleaner registration) or kept (more realistic)?
- *Proposed:* bovine, as specified. Remove marrow only by drilling and flushing defects, and keep the rest.
- Decision: ______________________ Signed/date: __________

### D6. Storage, fixative and scan medium
- **Options:**
  - 70% ethanol storage then humid-sealed scanning (default)
  - 10% NBF fixation
  - Scanning immersed in liquid
  - Scanning dry
- **Constraints [INF]:**
  - 45S5 glass and CaSO4 react with or dissolve in water, and 70% ethanol contains 30% water.
  - Formalin adds a carcinogen hazard and a waste stream.
  - Drying changes bone attenuation and may crack specimens.
- *Proposed:* ethanol storage before filling. After filling, humid-sealed and not immersed. Scan within 48 h. Identical conditioning pre and post. No formalin.
- Decision: ______________________ Signed/date: __________

### D7. Graft characterization and truth densities
- **Questions:**
  - Which skeletal density do we use: the supplier CoA, helium pycnometry (facility [UNR]), or textbook values [RF]?
  - Do we need porosity or BET data for microporous BCP, phase confirmation by XRD (e.g. for CaSO4 dihydrate), or SEM of granule microstructure?
  - Which granule size classes?
- *Proposed:* CoA values plus pycnometry if an accessible facility exists. A single size class (0.5–2 mm) for the main study; 0.5–1 vs 1–2 mm HA as an optional arm.
- Decision: ______________________ Signed/date: __________

### D8. Packing standardization
- **Question:** how to tamp reproducibly (number of taps, a fixed weight, or vibration).
- **Why it matters:** packing density changes the voxel-scale mixture of graft, void and partial volume.
- *Proposed:* matched PTFE rod with a fixed 200 g weight for 5 s, repeated 3× [HYP]. Record the fill height.
- Decision: ______________________ Signed/date: __________

### D9. Balance requirement
- **Options:** 1 mg readability (≈$150–400 [INF]) vs 0.1 mg (≈$900–2,500 [INF]), or access to a balance at a permitted location.
- *Proposed:* 1 mg is adequate. The expected fill masses are about 100–300 mg, so the error is ≲1% [INF]. Calibrate daily with a check weight.
- Decision: ______________________ Signed/date: __________

### D10. Acceptance criteria and QC thresholds (fix BEFORE unblinding)
Fill in values:

| Criterion | Value |
|---|---|
| Graft volume bias at 20 µm vs T2 | within ±___ % |
| Graft volume 95% LoA | within ±___ % |
| Peri-defect host BV/TV equivalence margin | ±___ percentage points |
| Peri-defect ring definition | ___–___ mm from defect wall |
| Per-material Dice (graft) at 20 µm | ≥ ___ |
| Scan–rescan ICC(2,1) | ≥ ___ |
| QC: cupping ≤ ___ %; phantom drift ≤ ___ %; calibration R² ≥ ___; TRE ≤ ___ voxels; displacement ≤ ___ voxels | n/a |

Signed/date: __________

### D11. Optional "woven-bone surrogate" (partially demineralized bone chips)
- **Question:** include it or not? If included: which agent (EDTA or dilute HCl), concentration, time points, and how to measure the resulting mineral fraction (ash or mass loss on sister chips).
- *Proposed:* exclude from Tier A. Pilot in Tier B only if the advisor considers it meaningful.
- Decision: ______________________ Signed/date: __________

### D12. Blinding custodian and pre-registration venue
- **Questions:** who holds the fill map? Where is pre-registration recorded (OSF, or a hash emailed to the advisor)?
- Decision: ______________________ Signed/date: __________

### D13. Biosafety and containment
- **Questions:** is BL-2 room handling required at the Suite? Is double containment in the scanner acceptable? Does DRS registration apply to food-source tissue?
- *Proposed:* ask the Suite and DRS. Default to sealed double containment and no open tissue in the scanner room.
- Decision: ______________________ Signed/date: __________

### D14. Location for specimen preparation
- **Question:** where can drilling and filling happen without using University resources, pending OTM? Options: a founder-owned home/garage bench, a makerspace with a membership, or a permitted campus space after OTM approval.
- **Constraint:** the Beckman Low Speed Bone Saw ($12.68/h internal [V]) is University equipment, so the IP question applies.
- Decision: ______________________ Signed/date: __________

---

**Go/No-go:** Protocol OQ-P1 may proceed when D1–D10, D12, D13 and D14 are signed. D11 is optional.

Reviewer name/role: ____________________ Signature: ____________ Date: ________
