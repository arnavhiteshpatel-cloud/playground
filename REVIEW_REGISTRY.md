# Review Registry

Twelve review perspectives, at least three review → remediation cycles. **Disclosure:** reviews in this registry are
performed by *automated reviewer agents* (AI models given only the repository and a perspective brief, separate from
the agent that wrote the code). They are useful for finding defects but are **not** reviews by qualified human experts
and must not be described as such to customers, investors or grant reviewers. Human expert review (imaging scientist,
bone biologist, biostatistician, regulatory/quality professional, counsel) remains an open founder action. Findings are
recorded with IDs and closed only with evidence (commit, test, or document change).

| # | Perspective | Cycle 1 | Cycle 2 | Cycle 3 |
|---|---|---|---|---|
| 1 | Bone biologist / histomorphometrist | 2026-11-27: 16 findings (BIO) — `docs/reviews/cycle1/REVIEW_BIO_CRO_QUALITY.md`; response `RESPONSE_PART2.md` | 2026-11-28: with #2–#4 — `docs/reviews/cycle2/REVIEW_SCIENCE.md` (C2-SCI, 23 findings; 1 critical); response `RESPONSE_SCIENCE.md` | 2026-11-28: with #2–#4 — `docs/reviews/cycle3/REVIEW_SCIENCE.md` (C3-SCI, 18 findings: 2 critical, 4 high); response `RESPONSE_SCIENCE.md` |
| 2 | Micro-CT imaging scientist | 2026-11-27: 16 findings (IMG-01…16; 1 critical, 6 high) — `docs/reviews/cycle1/REVIEW_IMAGING_STATS.md`; response `docs/reviews/cycle1/RESPONSE.md` | 2026-11-28: C2-SCI (with #1) — imaging physics, registration QC aperture problem, blur | 2026-11-28: C3-SCI (with #1) — fail-open registration QC on the tube axis (fixed: fails closed, Exp. L5) |
| 3 | ML / computer vision scientist | 2026-11-27: 16 findings (ML-01…16; 7 high) — `docs/reviews/cycle1/REVIEW_ML_ARCH.md` | 2026-11-28: C2-SCI (with #1) — method binding of support (critical, fixed) | 2026-11-28: C3-SCI (with #1) — validation-record binding, measured references (fixed, advisor 1.4.3) |
| 4 | Biostatistician | 2026-11-27: 16 findings (STAT-01…16; 1 critical, 7 high) — with #2 | 2026-11-28: C2-SCI (with #1) — pseudoreplication, acceptance rule, group statistics | 2026-11-28: C3-SCI (with #1) — S1H3 bound with structures as the unit: 0.34, not 0.045 (corrected) |
| 5 | Software architect | 2026-11-27: 12 findings (ARC-01…12; 1 critical, 5 high) — with #3 | 2026-11-27: with #6, #7, #9 — `docs/reviews/cycle2/REVIEW_PRODUCT.md` (C2-PRD, 21 findings); response in file (18 fixed, 3 low open) | 2026-11-28: with #6, #7, #9 — `docs/reviews/cycle3/REVIEW_PRODUCT.md` (C3-PRD, 22 findings: 3 high); response `RESPONSE_PRODUCT.md` |
| 6 | Security engineer | Gen-1 review (S-01…S-21) | 2026-11-27: C2-PRD (with #5) | 2026-11-28: C3-PRD (with #5) — appended audit events, unsigned validation records (fixed / mitigated) |
| 7 | QA / test engineer | — | 2026-11-27: C2-PRD (with #5) — first QA/test-engineer review | 2026-11-28: C3-PRD (with #5) — CI never blocked desktop/licensing tests (fixed; 90% gate) |
| 8 | Quality / regulatory (GLP, Part 11 awareness) | 2026-11-27: 16 findings (QA-REG; 1 critical) — with #1 | 2026-11-27: with #10–#12 — `docs/reviews/cycle2/REVIEW_BUSINESS_REG.md` (C2-BIZ, 24 findings); response in file (founder decisions in `FOUNDER_DECISIONS.md`) | 2026-11-28: with #10–#12 — `docs/reviews/cycle3/REVIEW_BUSINESS_REG.md` (C3-BIZ, 23 findings: 7 high); response `RESPONSE_BUSINESS_REG.md` |
| 9 | UX / desktop usability (study director, analyst) | 2026-11-27: 40 findings (UX-01…40; 10 high) — `docs/reviews/cycle1/REVIEW_UX.md`; remediation in progress | 2026-11-27: C2-PRD (with #5), headless desktop run with screenshots | 2026-11-28: C3-PRD (with #5), headless run with screenshots — dialog overstated validation (fixed) |
| 10 | CRO operations buyer | 2026-11-27: 13 findings (CRO; 1 critical) — with #1 | 2026-11-27: C2-BIZ (with #8) | 2026-11-28: C3-BIZ (with #8) — free evaluations before incorporation (suspended; founder decision) |
| 11 | Investor / commercial due diligence | 2026-11-27: 13 findings (INV; 1 critical) — `docs/reviews/cycle1/REVIEW_INVESTOR_IP.md` | 2026-11-27: C2-BIZ (with #8) | 2026-11-28: C3-BIZ (with #8) — per-material table oversold new bone; stale one-pager (fixed) |
| 12 | IP / licensing counsel perspective (non-legal) | 2026-11-27: 16 findings (IP; 2 critical) — with #11 | 2026-11-27: C2-BIZ (with #8) | 2026-11-28: C3-BIZ (with #8) — 28 Nov disclosures recorded; grace-period wording (not legal advice) |

Generation-1 reviews: scientific review Q-01…Q-14 (`docs/security/SCIENTIFIC_REVIEW.md`), security review
S-01…S-21 (`docs/security/SECURITY_REVIEW.md`), responses in `docs/security/REVIEW_RESPONSE.md`.

## Cycle 1 outcome (science core)
60 findings; all 3 critical and all 23 high-severity findings fixed or (STAT-04) accepted with documented
limitation; remediation verified by tests and re-runs (`docs/reviews/cycle1/RESPONSE.md`). Notable consequences:
reports now suppress unsupported endpoints; the advisor gained graft-share robustness, metal refusal, computed day-0
inputs and (from the S1b re-run) a partial-volume rule for new bone vs soft tissue; the pre-registration claim for
S1/S1b was withdrawn.

## Cycle 2 outcome
68 findings across the twelve perspectives (C2-SCI 23, C2-PRD 21, C2-BIZ 24). The critical science finding
(C2-SCI-02: support decisions applied to segmentation methods they were not validated for) was fixed by binding
support to `advisor_threshold` in the pipeline. Two pre-registered held-out validations followed (S1H2, S1H3).
Open items are listed with dispositions in the three response sections; founder-only items in `FOUNDER_DECISIONS.md`.

## Cycle 3 outcome
63 findings (C3-SCI 18, C3-PRD 22, C3-BIZ 23). Both critical findings (C3-SCI-01: total mineral wrongly supported with the
material unspecified; C3-SCI-02: API edits printed refused values) and all high findings are fixed or mitigated, with
tests that fail on the old code where stated. Science claims were restated (S1H3 bound 0.34 with structures as the unit;
precision criterion not demonstrated). Advisor 1.4.3 followed; any further claim about it needs a new pre-registered
held-out test. Open items are listed in the three response files. These are automated reviews; human expert review is
an open founder action.
