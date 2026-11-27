# Interview Coding Scheme

Purpose: turn discovery-interview notes into comparable codes so that patterns across segments can be counted, not guessed. These codes are applied to `interview_log_template.csv` (`pain_codes`, `concept_reaction_code`, `evidence_label`, `notes_coded`) and to transcript excerpts.

## 1. Segment codes (`org_type`)
| Code | Segment |
|---|---|
| MFR-SME | Orthobiologic / dental graft manufacturer, <500 staff |
| MFR-ENT | Enterprise medtech / dental (≥500 staff) |
| OEM | Contract developer/manufacturer of biomaterials |
| TISSUE | Tissue bank / HCT/P allograft |
| CRO-DEV | Medical-device preclinical CRO |
| CRO-ACAD | Academic CRO / university preclinical lab offering fee-for-service |
| CRO-HISTO | Histology / pathology / imaging specialist CRO |
| CORE | Academic micro-CT core |
| LAB | Academic PI lab |
| SBIR | Grant-funded startup |
| VEND | Imaging hardware/software vendor |

## 2. Workflow codes
- **ROI-MAN** manual contour; **ROI-GEOM** fixed geometric (cylinder/sphere); **ROI-TPL** template/registration; **ROI-NONE** whole-specimen
- **SEG-1T** single global threshold; **SEG-2T** dual threshold (graft vs bone); **SEG-MAN** manual painting; **SEG-ML** ML/AI tool; **SEG-HISTO** histology only; **SEG-NONE** no graft/bone separation
- **SW-SCANCO / SW-CTAN / SW-DRAGONFLY / SW-AMIRA / SW-VIVOQ / SW-IMAGEJ / SW-INHOUSE / SW-OTHER**
- **QC-2READ** second reader; **QC-ICC** formal agreement statistics; **QC-HISTO** histology correlation; **QC-NONE**

## 3. Pain codes (`pain_codes`, several allowed). Every pain code is [HYP] until it has been coded in ≥3 interviews in a segment.
| Code | Definition | Example signal |
|---|---|---|
| P-TIME | Analyst time per scan/study is burdensome | "Takes a week per study" |
| P-TAT | Turnaround delays decisions or submissions | "Report held up the 510(k)" |
| P-GRAFT | Cannot reliably separate residual graft from new bone | "Granules and bone overlap in density" |
| P-ROI | Defect boundary or ROI placement is inconsistent | "Everyone draws the defect differently" |
| P-REPRO | Inter- or intra-observer variability | "Two analysts got different BV/TV" |
| P-AUDIT | GLP, audit trail or Part 11 gaps | "QA flagged our spreadsheets" |
| P-SKILL | Scarce expertise / key-person risk | "Only one person knows the scripts" |
| P-COST | Direct cost of software, seats or outsourcing | "CTAn seat licences limit us" |
| P-REPORT | Report formatting and assembly effort | "Copying numbers into Word" |
| P-HISTO | Misalignment between micro-CT and histology | |
| P-NONE | No meaningful pain expressed | |

**Severity (`pain_severity_1to5`):** 1 = mentioned only when prompted; 2 = a minor annoyance; 3 = costs measurable time or money; 4 = has caused a delay, rework or an audit finding; 5 = they have actively spent money or effort trying to fix it.

## 4. Purchasing codes
- **DM-YES** interviewee can approve a pilot/purchase; **DM-INF** influencer; **DM-NO** no role
- **BUD-STUDY / BUD-ANNUAL / BUD-GRANT / BUD-RECHARGE / BUD-UNK**
- **QUAL-LIGHT** (<4 weeks, no audit); **QUAL-AUDIT** (supplier audit + quality agreement); **QUAL-UNK**

## 5. Concept-reaction codes (`concept_reaction_code`)
- **C-PULL** asks unprompted about the pilot, price or timing
- **C-POS** positive but passive
- **C-COND** positive conditional on validation/GLP/feature X (record X in `trust_requirements`)
- **C-NEUT** indifferent
- **C-NEG** sees no value or has a better solution (record what it is)
- **C-COMP** names a competitor/in-house tool that already solves it

## 6. Pilot codes (`pilot_willing`)
**PW-YES** (will share 20–30 retrospective scans), **PW-COND** (needs NDA, sponsor consent or a DPA), **PW-NO**, **PW-NA** (has no data). Blockers go in `pilot_blockers` as **B-CONF** (confidentiality), **B-SPONSOR**, **B-LEGAL**, **B-IT** (data-transfer/security), **B-TIME**, **B-VALID** (wants validation first).

## 7. Evidence labels on coded statements
Each coded statement gets an evidence label:
- **[V]** — the interviewee gave a direct number from their own records ("we ran 14 studies last year").
- **[RF]** — the interviewee reported it without records ("probably around a dozen").
- **[INF]** — the interviewer's inference.
- **[HYP]** — still untested.

Never upgrade a code to [V] on the basis of enthusiasm.

## 8. Decision thresholds for synthesis [HYP]
Proceed with a segment when, out of ≥8 interviews in that segment:

- ≥50% code P-GRAFT or P-TIME at severity ≥3,
- ≥30% are C-PULL or C-COND with satisfiable conditions,
- ≥2 are PW-YES or PW-COND, and
- the Van Westendorp acceptable-price range overlaps the cost-to-serve floor (see `PRICING_EXPERIMENT.md`).

Deprioritize the segment if ≥50% are P-NONE or C-COMP.

## 9. Process
1. Two coders (where possible) code the first 5 interviews independently and compute Cohen's κ on the pain codes. Target κ ≥ 0.6; refine the definitions if it falls short.
2. Keep a codebook change log at the bottom of this file.
3. Run the synthesis after every 5 interviews: count codes by segment and capture representative verbatims, anonymized and with no company names.

## Codebook change log
- 2026-11-27 v0.1 created (no interviews yet).
