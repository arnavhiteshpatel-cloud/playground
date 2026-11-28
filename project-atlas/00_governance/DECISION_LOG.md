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
