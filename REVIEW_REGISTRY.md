# Review Registry

Twelve review perspectives, at least three review → remediation cycles. **Disclosure:** reviews in this registry are
performed by *automated reviewer agents* (AI models given only the repository and a perspective brief, separate from
the agent that wrote the code). They are useful for finding defects but are **not** reviews by qualified human experts
and must not be described as such to customers, investors or grant reviewers. Human expert review (imaging scientist,
bone biologist, biostatistician, regulatory/quality professional, counsel) remains an open founder action. Findings are
recorded with IDs and closed only with evidence (commit, test, or document change).

| # | Perspective | Cycle 1 | Cycle 2 | Cycle 3 |
|---|---|---|---|---|
| 1 | Bone biologist / histomorphometrist | — | — | — |
| 2 | Micro-CT imaging scientist | 2026-11-27: 16 findings (IMG-01…16; 1 critical, 6 high) — `docs/reviews/cycle1/REVIEW_IMAGING_STATS.md`; response `docs/reviews/cycle1/RESPONSE.md` | — | — |
| 3 | ML / computer vision scientist | 2026-11-27: 16 findings (ML-01…16; 7 high) — `docs/reviews/cycle1/REVIEW_ML_ARCH.md` | — | — |
| 4 | Biostatistician | 2026-11-27: 16 findings (STAT-01…16; 1 critical, 7 high) — with #2 | — | — |
| 5 | Software architect | 2026-11-27: 12 findings (ARC-01…12; 1 critical, 5 high) — with #3 | — | — |
| 6 | Security engineer | Gen-1 review (S-01…S-21) | — | — |
| 7 | QA / test engineer | — | — | — |
| 8 | Quality / regulatory (GLP, Part 11 awareness) | — | — | — |
| 9 | UX / desktop usability (study director, analyst) | — | — | — |
| 10 | CRO operations buyer | — | — | — |
| 11 | Investor / commercial due diligence | — | — | — |
| 12 | IP / licensing counsel perspective (non-legal) | — | — | — |

Generation-1 reviews: scientific review Q-01…Q-14 (`docs/security/SCIENTIFIC_REVIEW.md`), security review
S-01…S-21 (`docs/security/SECURITY_REVIEW.md`), responses in `docs/security/REVIEW_RESPONSE.md`.

## Cycle 1 outcome (science core)
60 findings; all 3 critical and all 23 high-severity findings fixed or (STAT-04) accepted with documented
limitation; remediation verified by tests and re-runs (`docs/reviews/cycle1/RESPONSE.md`). Notable consequences:
reports now suppress unsupported endpoints; the advisor gained graft-share robustness, metal refusal, computed day-0
inputs and (from the S1b re-run) a partial-volume rule for new bone vs soft tissue; the pre-registration claim for
S1/S1b was withdrawn.
