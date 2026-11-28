# Blind Re-Scoring Protocol (Stage B calibration)

Purpose: discovery authors may inflate scores for their own workstream or calibrate differently. You re-score
records **without seeing the author's scores, rationale, gates, verdict, or evidence rating**.

Read first: `00_governance/MANDATE_AND_FOUNDER_BRIEF.md`, `00_governance/SCORING_FRAMEWORK.md` (anchors are
binding), `00_governance/EVIDENCE_STANDARDS.md`.

Input: your packet `03_screening/blind_packets/packet_NN.jsonl` (one record per line).
Output: `03_screening/blind_scores/packet_NN.jsonl`, one line per record:
```json
{"id":"WS05-004","scores":{"fcf":4,"roic":6,"access":5,"scale":4,"resilience":7,"entry":5,"delegation":5,"cash":7,"feasibility":6,"ai":4},
 "evidence_confidence":"C","flags":["G2_LICENSE:WARN"],"rationale":"<=60 words: key reasons, esp. where the record's own text is weak or over-claims",
 "red_flags":["claims X without source", "..."]}
```
Rules
- Score for THIS founder from zero, against the anchors. Be skeptical of claims without sources (check the record's
  `source_ids`/`spending_evidence` text). If a record's numbers look implausible from your own knowledge, score
  what you believe is realistic and say why in `rationale`.
- `evidence_confidence` = your judgment of the evidence level supporting the record's ECONOMICS as written.
- `flags` = gate flags you believe apply (G1–G7 with :FAIL or :WARN).
- You may do a few quick web checks for records whose verdict hinges on one checkable fact (e.g., a license
  requirement), but the job is calibrated judgment across many records, not new research.
- Read-only: do not contact anyone or submit anything. Never fabricate.
- Write lines as you go; validate every line parses (`python3 -c "import json;[json.loads(l) for l in open(p)]"`).
- Final reply ≤120 words: count scored, the 5 records you think are most under-rated and 5 most over-rated
  (IDs only + 6 words each).

Scratch files: if you write helper scripts, put them in a subdirectory unique to your packet (e.g.
`/tmp/claude-0/atlas_scratch/<packet_name>/`) — other agents share the scratchpad.
