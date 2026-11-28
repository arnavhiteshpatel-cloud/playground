# Decision Log

Each entry: date · decision · rationale · evidence · reversibility.

- **2026-11-28 · Workspace location.** Project Atlas lives in `project-atlas/` inside the `playground` repository on
  branch `claude/confident-newton-ql284g`, because that is the session's working repository and pushing it is the
  only way to persist work beyond this ephemeral container. It is fully self-contained and unrelated to the
  OsteoQuant files in the same repository; it can be moved to a dedicated repository at any time. Reversible.
- **2026-11-28 · Scoring weights.** Adopted the founder's provisional weights unchanged as v1.0. Added evidence
  shrinkage (k by evidence level) so weakly evidenced ideas cannot outrank well-evidenced ones on modeled upside.
  Any weight revision will be logged here with original scores retained. Reversible.
- **2026-11-28 · Gates.** G1 (>$100k before first revenue), G2 (unobtainable license), G3 (predatory/illegal),
  G6 (acquisition-only) are FAIL gates; G4, G5, G7 are warnings. Reason: founder's hard constraints.
- **2026-11-28 · Taxonomy.** 18 discovery workstreams (founder's sector list + mechanism-first, regulation-driven,
  quiet-money niches, specialty distribution, automotive/fleet, local/consumer services) to avoid anchoring on the
  founder's examples.
- **2026-11-28 · Stage A complete.** 18 workstreams → 630 records, 630 sources, all validated (0 errors).
- **2026-11-28 · De-duplication.** 32 cross-workstream clusters reviewed manually from the full title list plus
  Jaccard similarity; in each, the record with the strongest evidence (then most sources) is kept and the others
  linked via `duplicate_of` (`03_screening/dedupe_decisions.json`). Duplicates are excluded from ranking, but
  Stage C investigators read them. Result: 37 records linked as duplicates; 593 distinct opportunities. Reversible.
- **2026-11-28 · Stage B complete.** All 630 records blind re-scored (13 packets, 12 independent scorers). Authors
  inflated their own composite by +0.17 to +0.70 points (WS02 highest); current Stage-B scores = mean(author,
  blind). See `03_screening/calibration.md`. Dispositions for every record: `03_screening/screening_dispositions.csv`
  (74 Stage C, 59 Stage B only, 444 deprioritized with score, 23 gate failures, 37 merged duplicates).
- **2026-11-28 · Stage C selection.** 52 top evidence-adjusted records (≤7 per workstream) + 7 synthesized
  cross-stream bundles + 6 wildcards (highest raw score, weak evidence) + 9 mechanism-coverage judgment picks
  (`03_screening/judgment_picks.json`). Reason for judgment picks: composite scores are tightly bunched (core cut
  ≈5.40 on a 1–10 scale), so each value-capture family (freight, customs, contingency audit, government, GPO,
  recruiting, sourcing brokerage, code-driven trades) gets its best representative tested rather than being
  excluded by sub-0.2-point noise. Organized into 9 themed batches (`03_screening/stage_C_batches.json`).
- **2026-11-28 · Stage C complete.** 74 investigations (9 batches, ~280 new sources). Almost every opportunity's
  evidence-adjusted score fell (median ≈ −0.3) once real prices were found; most realistic new-entrant year-3
  operating-profit ranges sit at ~$25–250k. Bundles: SYN-001 (insurance-led carrier hub) and SYN-006 (construction
  back office, narrowed) survived; SYN-002/003/005/007 dropped (bundles mixed buyers, licenses or delivery systems).
- **2026-11-28 · Stage D selection (25 concepts).** All Stage C "advance" verdicts plus "hold" records with
  adj ≥ 5.25 that were not absorbed into another concept, plus masonry (5.23, C-level permit data). Overlapping
  survivors are merged into one concept (e.g., WS02-028 + WS15-023 → SYN-006; WS02-001 + WS17-001 → SYN-001;
  WS18-007 → WS05-007). Batches in `03_screening/stage_D_batches.json`. Chicago open data (food inspections, permits)
  and the DOT FMCSA census API are reachable and will be used for lawful, business-level prospect lists.
- **2026-11-28 · Stage D results (22 of 25 concepts; DG batch pending).** Finalist verdicts: SYN-006, SYN-004,
  WS05-007, WS04-014, SYN-001 (conditional). Strongest reserves: WS18-003 (B evidence), WS18-035, WS13-014, WS16-006.
  Dropped: WS04-010, WS07-023, WS11-017, WS13-028, WS03-012, WS10-010. All 16 models built by then verified
  (960/960 Summary values match after LibreOffice recalculation).
- **2026-11-28 · Stage E finalists (first 9).** SYN-006, SYN-004, WS05-007, WS04-014, WS18-003, WS18-035, SYN-001,
  WS13-014, WS16-006 (`03_screening/stage_E_finalists.json`). Rule: every Stage D finalist plus reserves with
  base-case year-3 operating profit ≥ ~$40k AND either peak funding (no draw) ≤ $90k or B-level evidence, except
  WS13-014 (peak $161k) kept because it is the best founder fit with A/B price anchors and a cheap rented-kit pilot.
  Excluded reserves: WS11-021 (G4 ceiling, 10-yr deployable ~$47k; kept as SYN-006 adjacency), WS05-026 (margin
  fragility), WS05-001 (kept as WS05-007 second license), WS18-004/WS13-016 (low year-3, high funding), WS18-002 (peak
  funding > $100k), WS17-004 (peak funding ~$433k). Models standardized for comparability (owner draw $4k/mo from
  month 13; tax 30%).
