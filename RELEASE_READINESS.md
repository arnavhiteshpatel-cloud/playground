# Release Readiness

Gates are cumulative. **Gate 3 is never self-declared by this project**: it requires real-world evidence and
external sign-off.

| Gate | Meaning | Criteria | Status |
|---|---|---|---|
| Gate 1 — Engineering preview | Installable build that a scientist can evaluate on their own data with no claims of accuracy on real grafts | Desktop app builds on all 3 OS in CI; Linux selftest passes; core workflows (import → QC → view → edit → analyse → report) work; tests ≥90% coverage; no open critical/high security issues; all outputs labelled with support status and evidence level | not met |
| Gate 2 — Pilot-ready research tool | Usable in a paid pilot under a written protocol that defines acceptance on the customer's data | Gate 1 + real-data validation for at least one task with specimen-level CIs; measurement-support logic validated against known-unsupported materials; three review cycles closed; documentation complete; pilot SOW/DPA templates reviewed by counsel (F) | not met |
| Gate 3 — Validated for a defined context of use | Evidence that measurements agree with reference methods on real graft materials | Physical phantom + histology-correlated data on real materials, independent analysts, pre-registered acceptance criteria; customer QA acceptance; (if GLP use) customer's computerised-system validation | not claimed |

## Checklist (updated each generation)
- [ ] Desktop build Linux (local) · [ ] Windows (CI) · [ ] macOS arm64 (CI)
- [ ] Coverage ≥95% critical / ≥90% overall
- [ ] Security: zero open critical/high
- [ ] Claims checker passes
- [ ] Benchmark scorecard targets met (BENCHMARK_SCORECARD.md)
- [ ] Review cycles: 0 / 3
