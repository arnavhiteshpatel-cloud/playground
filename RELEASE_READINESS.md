# Release Readiness

Gates are cumulative. **Gate 3 is never self-declared by this project**: it requires real-world evidence and
external sign-off.

| Gate | Meaning | Criteria | Status |
|---|---|---|---|
| Gate 1 — Engineering preview | Installable build that a scientist can evaluate on their own data with no claims of accuracy on real grafts | Desktop app builds on all 3 OS in CI; Linux selftest passes; core workflows (import → QC → view → edit → analyse → report) work; tests ≥90% coverage; no open critical/high security issues; all outputs labelled with support status and evidence level | not met |
| Gate 2 — Pilot-ready research tool | Usable in a paid pilot under a written protocol that defines acceptance on the customer's data | Gate 1 + real-data validation for at least one task with specimen-level CIs; measurement-support logic validated against known-unsupported materials; three review cycles closed; documentation complete; pilot SOW/DPA templates reviewed by counsel (F) | not met |
| Gate 3 — Validated for a defined context of use | Evidence that measurements agree with reference methods on real graft materials | Physical phantom + histology-correlated data on real materials, independent analysts, pre-registered acceptance criteria; customer QA acceptance; (if GLP use) customer's computerised-system validation | not claimed |

## Checklist (updated 2026-11-28, Generation 2)
- [ ] Desktop build Linux (local): the only packaged build (27 Nov 2026) passed its packaged self-test and licence check at the time (`packaging/dist/build-info.json`), but it predates advisor 1.3.1–1.4.3 and the cycle-2/3 fixes, so it does not show the current code working. It must be rebuilt before any use or distribution (B-016); `build-info.json` should then record the commit and advisor version
- [ ] Desktop build Windows / macOS: never built; the `desktop-build` workflow has never run (manual dispatch is a founder distribution decision, B-013, decision #21)
- [x] CI green on Ubuntu, Windows and macOS × Python 3.12 / 3.13 for the library test suite, lint and dependency audit (first green run 2026-11-28, run 59; earlier runs failed: DF-022)
- [ ] Desktop tests in CI: run for the first time in run 59 (non-blocking step then). Since 2026-11-28 the full suite including desktop and licensing tests is a blocking CI step; whether CI passes under the new configuration is not yet recorded
- [ ] Coverage ≥95% critical / ≥90% overall: single source `docs/qa/test_summary.json` (597 passed, 1 skipped; 90.8% line+branch overall, desktop UI excluded; local full run at `4b5e84c`). CI gates are now ≥90% overall and ≥95% for morphometry, stats, metrics, I/O and audit; the per-module figures for the ≥95% target are not recorded in that file, so this item stays open
- [ ] Security: zero open critical/high — see docs/security/SECURITY_REVIEW_GEN2.md and the cycle-3 product review
- [x] Claims checker passes (`scripts/check_claims.py`)
- [ ] Benchmark scorecard targets met: B4, B10 met on synthetic data only; B1–B3 and B5–B8 not met or pending (BENCHMARK_SCORECARD.md)
- [ ] Review cycles: 2 completed / cycle 3 in progress (automated reviewer agents, not human experts)

**Gate status:** Gate 1 not met (Windows/macOS builds never run; the only Linux build predates the current code and
must be rebuilt; critical-module coverage and the security items unconfirmed). Gate 2 not met (no real-data
validation of the graft/new-bone task; no human expert review; pilot templates not reviewed by counsel). Gate 3 is
never claimed. No evaluation on customer data has been agreed, and the company is not incorporated.
