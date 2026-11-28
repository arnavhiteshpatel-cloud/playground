# Cycle 3 — Business, regulatory and IP review response (REVIEW_BUSINESS_REG.md)

Status: **fixed** (file changed; the claims checker passes where it applies), **partly fixed** (residual stated),
**founder** (a decision only the founder can take; recorded in `FOUNDER_DECISIONS.md`), **open** (planned; reason
given). Nothing in this response is legal advice; every IP and privacy point needs counsel.

## New findings

| ID | Sev | Status | Response / evidence |
|---|---|---|---|
| C3-BIZ-01 | High | fixed | The per-material table is generated from the full per-scan decision on synthetic phantoms (`scripts/material_support_table.py`, default mode) and shows new bone as not supported for every material, as in S1H3; website, user documents and the deck slide use it (C3-SCI-12). |
| C3-BIZ-02 | High | fixed | "Total mineral is still reported" is withdrawn everywhere it was a promise; `docs/user/MATERIALS_AND_SUPPORT.md` says it is not a guaranteed fallback. `business/REVENUE_MODEL.md` §2a-bis states the risk of refused or undeliverable studies, which the model does not price; `business/templates/PILOT_PROPOSAL.md` states the coverage and selection effect. Positioning after S1H3 is founder decision #20. |
| C3-BIZ-03 | High | fixed | API and CLI default to `advisor_threshold`; the six customer documents name it as the default and say that every other method has no measurement support (C3-PRD-13). |
| C3-BIZ-04 | High | fixed | `investor/ONE_PAGE_OVERVIEW.md` rewritten: advisor 1.4.3, S1H3 in the standard phrase with a plain-language reading, the stale bundle stated, the hard-coded test count removed, Cozad dates corrected. |
| C3-BIZ-05 | High | fixed | Documents no longer say the Linux bundle ships a given advisor version: it is dated 27 Nov and predates advisor 1.3.1–1.4.3 (`docs/desktop/PACKAGING.md`, `FOUNDER_HANDOFF.md`). `packaging/build.py` now writes `git_commit`, `osteoquant_dirty` and `advisor_version` into `build-info.json` (commit `5d517cd`). Rebuilt on 28 Nov from a clean tree at `1f568f4` with advisor 1.4.3, both recorded in `build-info.json`; packaged self-test PASS, licence check exit 0. Windows/macOS builds remain founder decision #21 (B-013). |
| C3-BIZ-06 | High | fixed / founder | Free evaluations on customer scans are withdrawn from the website, services page, outreach drafts and decks; the site says pilots and evaluations are planned only after incorporation, a DPA and Gate 1. Whether to offer any before M0 is founder decision #18. |
| C3-BIZ-07 | High | founder / fixed (record) | `docs/ip/INVENTION_REGISTER.md` records the public disclosures of 27 and 28 Nov (advisor 1.4.0–1.4.3 mechanisms, external anchors, fail-closed registration QC) with commit dates. Pushing continues under the founder's 27 Nov instruction ("push everything", `docs/ip/IP_STRATEGY.md`); whether new inventive work keeps going to the public repository is founder decision #17, with #2 still open. |
| C3-BIZ-08 | Medium | fixed (wording) / founder | `docs/ip/IP_STRATEGY.md` corrected: grace-period jurisdictions and their deadlines (2027-11-27 / 2027-11-28) are named instead of "foreign rights are lost"; counsel must confirm each point. Non-US filings are founder decision #19. |
| C3-BIZ-09 | Medium | fixed | Cozad: 2 Feb 2027 is the registration deadline and finals are in April (date not confirmed) in `FOUNDER_DECISIONS.md`, the executive summary, the one-pager and deck. The single pricing gate is split into two evaluable gates (`business/PRICING_VALIDATION_PLAN.md`); M0 and Gate 2 references aligned. |
| C3-BIZ-10 | Medium | partly fixed | One test summary file (`docs/qa/test_summary.json`) is read by the decks, the Gen-2 report builder and the founder documents; `QA_REPORT.md` explains that the 91% "final" figure is the 27 Nov run. Open: CI writing the file itself (it is written by a local script after a full run), and renaming the dossier to "verification" (kept: the mandate names it). |
| C3-BIZ-11 | Medium | fixed (builder, index) / open (PDF) | `scripts/build_gen2_report.py` lists held-out validations first, labels S1/S1b/S1c as in-sample development runs, prints structure-level bounds and reads metrics from files; `deliverables/README.md` lists the Gen-2 report as deliverable 1 and marks the Gen-1 report superseded. The PDF is rebuilt at the end of Generation 2, after S1H4 and the ML results are recorded. |
| C3-BIZ-12 | Medium | fixed | `web/landing/index.html` is marked SUPERSEDED (do not publish), its pilot invitation and day-0 claims removed. Manuscript 1's conclusion now cites L3 (day-0 helps only without granule motion). The registry header says "internal automated reviews". The checker's outward-facing scope now includes `validation/`, `FOUNDER_HANDOFF.md` and the root ledgers the website links to (run-count bans are lifted for the ledgers, which hold the raw counts by design). |
| C3-BIZ-13 | Medium | fixed | `business/INTERVIEW_GUIDE.md` §9 no longer claims day-0 registration; it states how often measurements are refused. |
| C3-BIZ-14 | Medium | fixed | Every price on a pricing card lies inside a hypothesis range H1–H5; cards without a hypothesis show no figure (`business/PRICING_EXPERIMENT.md`). No offer is made before incorporation (C3-BIZ-06). |
| C3-BIZ-15 | Medium | partly fixed / founder | The generated notice no longer says "we will provide"; it names the licensor in the end-user licence agreement, once incorporated (`packaging/bundle_inventory.py`). `docs/desktop/PACKAGING.md` lists the missing ICU source and the offeror gap; who makes the offer, or whether source archives ship with each build, is founder decision #22. No distribution happens before that. |
| C3-BIZ-16 | Medium | fixed | Sample reports are generated through the desktop path from committed code only (the generator refuses a dirty tree), record the commit, and are watermarked "SAMPLE - SYNTHETIC DATA - NOT FOR STUDY DECISIONS" (commits `969d9a5`, `ab617ea`). Gen-1 SAMPLE1–3 moved to `reports_samples/superseded/` with a README. |
| C3-BIZ-17 | Medium | partly fixed | The checker reads decks and PDFs, binds the structure-level and row-level S1H3 bounds, the structure count and the no-endpoint share, rejects a non-zero quantity quoted as zero, bans "proven safe" phrasing and covers publications, the landing page, outreach, founder files, validation pages and ledgers. Open: UI strings, and the Gen-2 report builder's own literals (checked through the built PDF). |
| C3-BIZ-18 | Medium | fixed | Refusal reasons no longer advise a day-0 scan (advisor 1.4.3; commit `969d9a5`). |
| C3-BIZ-19 | Low | fixed | Quick Start and FAQ list bone-derived grafts as refused by every mechanism, with or without a day-0 scan, and say the desktop application has no day-0 workflow. |
| C3-BIZ-20 | Low | partly fixed | The website scorecard and validation programme stage A are regenerated from `BENCHMARK_SCORECARD.md` and the registry (S1H3 as the exit criterion; in-sample runs are development checks); the about page no longer lists a day-0 study design as a focus. Open: the report-preview screenshot (`website/assets/img/08_report_preview.png`) is regenerated with the final deliverables. |
| C3-BIZ-21 | Low | fixed | The registry gives the actual state per experiment (S2 part b running since 00:34, part c, S3, U1 and O2 queued). |
| C3-BIZ-22 | Low | fixed | The NSF pitch uses the competitor matrix's wording: deep learning is available from others; graft-aware abstention was not found in the sources reviewed. |
| C3-BIZ-23 | Low | partly fixed / founder | Decision #3 now names `outreach/collaborators.csv` and `outreach/OUTREACH_EMAILS.md`; the CSV is re-quoted (23 fields per row); one personal email address was removed from the current tree and runtime logs are no longer tracked. History is unchanged: rewriting it is part of decision #3. |

## Cycle-2 dispositions the review disputed

| ID | Response |
|---|---|
| C2-BIZ-01 | Agreed; the one-pager residual is C3-BIZ-04 (fixed). |
| C2-BIZ-02 | Agreed; the Gen-2 report's in-sample "validation" row is C3-BIZ-11 (builder fixed; PDF rebuilt at the end of Generation 2). |
| C2-BIZ-07 | Agreed; the old samples are moved to `reports_samples/superseded/` and the current ones are watermarked (C3-BIZ-16). |
| C2-BIZ-11 | Agreed the one-pager had gone stale again; rewritten (C3-BIZ-04). |
| C2-BIZ-13 | Agreed; interview script fixed (C3-BIZ-13). |
| C2-BIZ-14 | Agreed; scope widened and the files cited corrected (C3-BIZ-12, C3-BIZ-17). |
| C2-BIZ-18 | Agreed; Quick Start and FAQ fixed (C3-BIZ-19). |
| C2-BIZ-20 | Agreed; decks and PDFs are now checked (C3-BIZ-17). |
| C2-BIZ-22, IP-06 | Agreed; the 28 Nov disclosures are recorded and pushing is founder decision #17 (C3-BIZ-07). There is still no `LICENSE` file: choosing one is part of founder decision #2. |
| C2-BIZ-24, IP-12 | Agreed: free evaluations kept the risks. Withdrawn; founder decision #18 (C3-BIZ-06). |

## Founder decisions added (review section c)

`FOUNDER_DECISIONS.md` #17–#25: pushing new inventive work (#17), evaluations before M0 and Gate 1 (#18), non-US
grace-period filings (#19), positioning after S1H3 (#20), running the desktop-build workflow (#21), the LGPL written
source offer (#22), manuscripts and AI-assistance disclosure (#23), budget for human expert reviewers (#24), release and
version policy (#25).
