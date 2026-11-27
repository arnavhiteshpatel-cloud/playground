# Customer Discovery Interview Guide: OsteoQuant desktop application + analysis services

Version 0.2 (2026-11-27). It replaces v0.1 (DefectFill Report only). No interviews have been run yet. Every pain point and price in this guide is a hypothesis [HYP].

**What changed in v0.2**
- The product is now described as an **offline desktop application** plus optional services: paid pilot, non-GLP study analysis, material characterisation, academic licence, enterprise licence.
- New: segment-specific modules (§10). Questions on IT and installation (§7), the day-0 baseline scan (§4), and how people react to software that **abstains** (§9).
- Pricing now follows `PRICING_VALIDATION_PLAN.md`.
- New logging columns in `interview_log_template.csv`.

## Purpose
Find out whether the people who run or buy preclinical bone-graft studies have a costly, recurring problem with:

- placing the defect region of interest (ROI),
- separating new bone from residual graft and host bone,
- following the same defect over time, and
- producing a traceable report,

and whether they would rather **run software themselves** or **buy the analysis as a service**, and at what price. The goal is to learn. Do not pitch.

Segments (`prospect_segments.csv`; codes in `INTERVIEW_CODING_SCHEME.md` §1):
- orthobiologic and dental graft manufacturers (MFR-SME, MFR-ENT, OEM, TISSUE),
- preclinical CROs (CRO-DEV, CRO-ACAD, CRO-HISTO),
- academic labs (LAB),
- micro-CT core facilities (CORE).

## Ground rules
- 30–45 minutes, video or phone. Ask permission before recording. If refused, take notes only.
- Ask about **past behaviour** ("the last study you ran…"), not future intentions. Hold the concept until §9 and prices until §11.
- Do not ask for confidential study data, sponsor names or unpublished results. If they are volunteered, record them only in coded form and do not share them.
- Record role and organisation type. Never put personal contact details in shared files.
- Never imply that OsteoQuant is validated, GLP-compliant, Part 11-compliant, accepted by any regulator, or has customers. It is not, and it does not. It is a research prototype tested on synthetic data and a small amount of public real data.
- Do not disclose algorithm details (see `outreach/IP_AND_OTM_QUESTIONS.md`). Describe what it does, not how.

## 0. Opening (2 min)
"I'm researching how preclinical bone-graft and bone-defect studies are analysed, especially micro-CT. I'm not selling anything today. I'd like to understand how your team does it now and what is hard about it. Is it OK if I take notes or record? Nothing will be attributed to you or your organisation."

## 1. Context and role (3 min)
1. What is your role in preclinical bone studies: designer, analyst, approver or buyer? → `decision_role`
2. Which products or models do you work with? Probe: synthetic CaP, bioactive glass, calcium sulfate, DBM or allograft, xenograft, growth factor, cage plus graft; rat calvaria, rabbit femoral condyle, ovine, canine or minipig dental, spine fusion.

## 2. Study volume (5 min)
3. In the last 12 months, how many bone-defect or graft studies did your group run or analyse? How many were GLP? → `studies_per_year`, `glp_studies_per_year`. Ask: "Is that from records or an estimate?" and set `evidence_label` [V]/[RF].
4. Roughly how many animals and micro-CT scans per study, and how many time points? → `scans_per_study`, `timepoints_per_study`
5. Is volume rising, falling or flat? What drives it?

## 3. Current analysis workflow (7 min)
6. Walk me through the last study, from the reconstructed scan to the final report. Who did each step?
7. How do you define the defect ROI?
8. How do you separate new bone, residual graft and host bone? Single threshold, dual threshold, manual painting, histology only, or not at all? → `three_class_done`
9. Which parameters do you report? ASBMR nomenclature (Bouxsein et al. 2010)?
10. Which software and version? Any licence, seat or operating-system limits? → `software_used`
11. How do you check quality: second reader, agreement statistics, histology?

## 4. Longitudinal design and the day-0 scan (3 min)
12. Do you scan the same animal more than once (in vivo), or only at end-point (ex vivo)?
13. Is a scan **immediately after implantation (day 0)** feasible in your study designs? What would stop it: anaesthesia, scanner access, protocol approval, cost? → `day0_scan_feasible` (yes / sometimes / no / NA)
14. When graft and new bone look alike on micro-CT, what do you do today?

## 5. Analyst time and cost (5 min)
15. About how many analyst hours per scan and per study? Which step takes longest? → `analyst_hours_per_scan`, `analyst_hours_per_study`
16. What level of person does it? Ask for a loaded hourly rate range only if they are comfortable sharing.
17. Turnaround from last scan to final report? Has it ever delayed a submission or decision? → `turnaround_days`, `delay_incident`

## 6. Outsourcing (4 min)
18. Do you outsource any imaging analysis or histomorphometry? To which kind of provider? Why, or why not? → `outsources_analysis`, `outsource_provider_type`
19. Roughly what did the last analysis-only line item cost? Ask for a range only. → `outsource_cost_range_usd`
20. What would make you stop outsourcing, or start?

## 7. Data handling, IT and quality requirements (5 min)
21. **Where may study data go?** Can scans leave your network? Are cloud tools allowed? Would software that runs entirely on your own computer, with no upload, change that? → `desktop_it_constraints`
22. Can you install software yourselves? Which operating system? Is there a GPU on the analysis workstation? Who approves installation (IT, QA)?
23. For GLP studies, what do you require of analysis software: validation, audit trail, e-signatures, version locking? Who would do that validation, you or the vendor? Record the requirement **without** suggesting OsteoQuant meets it. → `glp_software_requirements`, `part11_required`
24. Has an auditor or reviewer ever questioned your micro-CT analysis? What happened? → `audit_finding_history`

## 8. Pain and satisfaction (4 min)
25. What is the most frustrating part of quantifying graft-filled defects today? → `biggest_pain_verbatim`, `pain_codes`
26. On a scale of 1–10, how satisfied are you with your current approach? What would move it up 2 points? → `satisfaction_1to10`
27. Have you tried to fix it (bought software, built scripts, hired someone)? What happened? Past attempts are the strongest evidence of real pain. → `prior_fix_attempts`

## 9. Concept reaction (5 min)
Read this description verbatim, then show a **mock** report page labelled "illustrative, not validated":

> "OsteoQuant is a desktop application under development. It runs on your own computer, so scans do not leave your network. For each scan it proposes the defect region and labels new bone, residual graft and host bone for an analyst to review and correct. It can register later scans to a day-0 scan, reports standard morphometry, and keeps an audit trail of every change. When it cannot support a measurement, for example because the graft and new bone are not distinguishable at that resolution, it says so and does not report a number. It has been tested on simulated data and a small amount of public micro-CT data. It has not been validated on any commercial graft material, and it is not GLP-validated. Alongside the software we would offer analysis as a service."

28. First reaction? What is missing? What would you not trust? → `concept_reaction_code`, `trust_requirements`
29. **Abstention:** how would you feel about software that declines to report a value instead of giving a number with a warning? Helpful, frustrating, or a deal-breaker? → `abstention_reaction`
30. What would you need to see before using it on a real study: agreement with your own analysts, comparison with histology, a validation report?
31. **Pilot willingness:** would you share 10–20 retrospective, de-identified scans with your existing analysis so we can compare blind? What would block that? → `pilot_willing`, `pilot_blockers`

## 10. Segment modules (pick one; 4 min)
**Manufacturers (MFR / OEM / TISSUE)**
- M1. Before a study, how do you decide scanner settings and whether micro-CT can see your material? Has a study ever ended with "we couldn't tell graft from bone"? (tests material characterisation, H3)
- M2. For which studies would you buy analysis as a service, and which would you keep in-house?

**CROs**
- C1. How many bone-healing studies per year need graft versus new-bone quantification? From records or an estimate? (≥10 is the enterprise threshold [AE])
- C2. When you add analysis software, is it an organisation-wide licence, per seat, or per study passed through to the sponsor?
- C3. Would you rather license software for your analysts or subcontract the analysis? Would a sponsor accept either?

**Academic labs**
- L1. Which grant pays for analysis software or core time? Is software an allowable direct cost on your current award?
- L2. Do free tools (BoneJ, Dragonfly academic) do what you need? Where do they fall short?

**Core facilities**
- K1. How do you charge users for analysis: hourly recharge, per sample, or included? Would a core-wide licence fit your recharge model?
- K2. How many user groups run bone-defect or graft studies on your scanners each year?

## 11. Pricing (6 min). All figures are [HYP]
Run only after §§2–9, following `PRICING_VALIDATION_PLAN.md` §4:
1. Current cost (§4a of the plan), if not already captured.
2. Van Westendorp's four questions on the **primary card** for the segment: manufacturers S, CROs E, labs and cores A. → `vw_offering`, `vw_*`
3. Gabor–Granger ladder on the same card, starting point chosen by coin flip. → `gg_offering`, `ladder_start_anchor_usd`, `ladder_max_yes_usd`
4. If time allows, a second ladder: manufacturers card M or P, CROs card S, cores card P only if they serve industry. → `gg_secondary_offering`, `gg_secondary_max_yes_usd`
5. Model and unit preference: card sort M1–M8 plus "service or software?". → `model_rank_1`, `model_rank_last`, `price_unit_preferred`
6. Reference-price reaction, using the published HSS figure only, and only now. → `anchor_shown`, `reference_price_reaction`

## 12. Purchasing and close (3 min)
32. Who decides on buying a service or software? What is the approval threshold? Is it budgeted per study or per year? → `approval_chain`, `approval_threshold_usd`, `budget_source`
33. What does vendor qualification involve, and how long does it usually take? → `vendor_qualification_weeks`
34. Who else should I talk to? Ask for an introduction, not contact details. → `referrals_offered`
35. Can I send a short summary of what I learned? → `follow_up_agreed`

Thank them. Promise nothing beyond the summary.

## After the interview
- Fill in one row of `interview_log_template.csv` within 24 h, including `segment` and `prospect_wave` from `prospect_segments.csv`.
- Code the notes with `INTERVIEW_CODING_SCHEME.md`.
- After every 5 interviews, run the synthesis (`INTERVIEW_CODING_SCHEME.md` §9) and the price summary (`PRICING_VALIDATION_PLAN.md` §8).
- Store recordings encrypted, delete them after transcription and coding (target ≤90 days), and keep the consent record.
