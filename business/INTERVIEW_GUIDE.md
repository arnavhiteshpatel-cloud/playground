# Customer Discovery Interview Guide: DefectFill Report

Version 0.1 (2026-11-27). No interviews have been run yet. Every pain point and price in this guide is a hypothesis [HYP].

## Purpose
Find out whether preclinical bone-defect sponsors and service providers (orthobiologic and dental manufacturers, preclinical CROs, academic micro-CT cores) have a costly, recurring problem with:

- placing the defect ROI,
- separating new bone from residual graft and host bone, and
- producing an audit-ready morphometry report,

and whether they would pay to have it solved. The goal is to learn. Do not pitch.

## Ground rules
- 30–45 minutes, video or phone. Ask permission before recording. If refused, take notes only.
- Ask about past behaviour ("the last study you ran…"), not future intentions ("would you…"). Hold any product description until section 9.
- Do not ask for confidential study data, sponsor names or unpublished results. If the interviewee volunteers them, record them only in coded form (see the coding scheme) and do not share them.
- Do not quote prices first. The price questions (section 10) come only after the pain questions.
- Record the interviewee's role and organization type. Never put personal contact details into shared files.
- Never imply that OsteoQuant is validated, GLP-compliant or has customers. It is not, and it does not.

## 0. Opening (2 min)
"I'm researching how preclinical bone-defect studies are analysed, especially micro-CT of graft-filled defects. I'm not selling anything today. I'd like to learn how your team does it now and what's hard about it. Is it OK if I take notes or record? Nothing will be attributed to you or your company."

## 1. Context and role (3 min)
1. What is your role, and how are you involved in preclinical bone studies? (designer / analyst / approver / buyer)
2. What kinds of products or models does your group work with? Probe: synthetic CaP, bioactive glass, DBM/allograft, xenograft, growth factor, cage plus graft; rat calvaria, rabbit femoral condyle, ovine, canine/minipig dental, spine fusion.

## 2. Study volume (5 min)
3. In the last 12 months, roughly how many bone-defect or graft studies did your group run or analyse? How many were GLP?
4. Roughly how many animals and micro-CT scans per study? How many time points?
5. Is volume rising, falling or flat? What drives it (new 510(k)s, label expansions, grants, sponsor demand)?

## 3. Current analysis workflow (8 min)
6. Walk me through the last study, from the reconstructed scan to the final report. Who did each step?
7. How do you define the defect ROI: manual contour, cylinder, template, by slice?
8. How do you separate new bone, residual graft and host bone? Single threshold, dual threshold, manual painting, histology only, or not at all?
9. Which morphometric parameters do you report (BV/TV, Tb.Th, graft volume fraction, etc.)? Do you follow ASBMR nomenclature (Bouxsein et al. 2010)?
10. Which software? (Scanco IPL, Bruker CTAn, Dragonfly, Amira/Avizo, VivoQuant, ImageJ/BoneJ, in-house scripts, other.) Any licence or seat limits?
11. How do you check quality? Second reader, inter-observer agreement, comparison with histology?

## 4. Analyst time and cost (5 min)
12. About how many analyst hours per scan, and per study? Which step takes longest?
13. What level of person does it (technician, PhD scientist, pathologist)? (Ask for a loaded hourly rate range only if they are comfortable sharing.)
14. How long is the turnaround from last scan to final report? Has it ever delayed a submission or decision?

## 5. Outsourcing (4 min)
15. Do you outsource any imaging analysis or histomorphometry? To whom (type, not name, if they prefer)? Why or why not?
16. If you outsource, roughly what did the last analysis-only or imaging line item cost? Ask for a range only, and don't push.
17. What would make you stop outsourcing, or start?

## 6. Regulatory, GLP and data integrity (5 min)
18. For GLP studies, what do you require of analysis software: validation, audit trail, Part 11 e-signatures, version locking, raw-data definitions?
19. Has an auditor or FDA reviewer ever questioned your micro-CT analysis (thresholds, ROI, reproducibility)? What happened?
20. Who signs off on new analysis software or vendors: QA, the study director, IT, procurement?

## 7. Pain points and satisfaction (5 min)
21. What is the most frustrating part of quantifying graft-filled defects today?
22. On a 1–10 scale, how satisfied are you with your current approach? What would move it up 2 points?
23. Have you tried to fix it (bought software, built scripts, hired someone)? What happened? (Past attempts are strong evidence of real pain.)
24. If the problem disappeared tomorrow, what would change: time, cost, data quality, faster submission?

## 8. Purchasing authority (3 min)
25. Who decides on buying an analysis service or software at your organization? What is the approval threshold before procurement or a committee gets involved?
26. Is the money budgeted per study or per year? Which budget line (R&D, study budget, core recharge, grant)?
27. What does vendor qualification involve (supplier audit, quality agreement, security questionnaire)? How long does it usually take?

## 9. Concept reaction (5 min)
Show a one-paragraph description and a **mock** report page clearly labelled "illustrative, not validated". Then ask:

28. What is your first reaction? What is missing? What would you not trust?
29. What would you need to see before using it on a real study (validation evidence, ICC against your analysts, comparison with histology)?
30. **Pilot willingness:** Would you be willing to share 20–30 retrospective, de-identified scans with existing manual analysis so we can compare? What would block that (confidentiality, sponsor consent, data transfer)?

## 10. Pricing (5 min). All figures are [HYP]
Run these only after sections 2–8.

**Van Westendorp (unit = one complete non-GLP study report, ~20–40 scans):**
- At what price would it be so expensive you wouldn't consider it?
- At what price would it be expensive, but you'd still consider it?
- At what price would it be a bargain?
- At what price would it be so cheap you'd doubt the quality?

Repeat for one GLP study only if time allows.

**Price ladder (Gabor–Granger), with one randomized starting anchor per interview:**
"If a validated, audit-trailed report for one non-GLP study cost $X, how likely would you be to buy it for your next study (1–5)?" Ladder: $3K → $6K → $12K → $18K → $25K. Go down after a "no" and up after a "yes". Randomize whether you start at $6K or $18K, and log the starting point.

**Model preference:** Show the cards in `PRICING_EXPERIMENT.md` §2 (per-scan, per-study, annual subscription, CRO enterprise licence, full analysis service, vendor-bundled, algorithm licence). Ask them to rank the cards and explain the top and bottom choices.

## 11. Close (2 min)
31. Who else should I talk to, inside or outside your organization? (Ask for an introduction; do not request contact details.)
32. Can I follow up with a short summary of what I learned?

Thank them. Promise nothing beyond the summary.

## After the interview
- Fill in one row of `interview_log_template.csv` within 24 h.
- Code the notes with `INTERVIEW_CODING_SCHEME.md`.
- Store recordings encrypted, delete them after transcription and coding (target ≤90 days), and keep the consent record.
