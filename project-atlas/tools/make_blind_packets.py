#!/usr/bin/env python3
"""Create blinded scoring packets: records with author scores, rationale, gates and verdict removed.

Usage: python3 tools/make_blind_packets.py [n_packets]
Writes 03_screening/blind_packets/packet_NN.jsonl (records interleaved across workstreams so no packet is
dominated by one author) and prints packet sizes.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB, SCR = ROOT / "09_databases", ROOT / "03_screening"
HIDE = {"scores", "score_rationale", "gates", "preliminary_verdict", "original_scores", "blind_scores",
        "current_scores", "current_score_basis", "latest_verdict", "stage_history", "blind_rationale",
        "blind_flags", "original_evidence_confidence", "blind_evidence_confidence", "max_stage"}
KEEP_PREFIX_DROP = ("current_",)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    opps = [json.loads(l) for l in (DB / "opportunities.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    opps = [o for o in opps if not o.get("duplicate_of")]
    # interleave by workstream
    by = {}
    for o in opps:
        by.setdefault(o.get("workstream"), []).append(o)
    order = []
    while any(by.values()):
        for ws in sorted(by):
            if by[ws]:
                order.append(by[ws].pop(0))
    out = SCR / "blind_packets"; out.mkdir(parents=True, exist_ok=True)
    for p in out.glob("packet_*.jsonl"):
        p.unlink()
    packets = [[] for _ in range(n)]
    for i, o in enumerate(order):
        packets[i % n].append({k: v for k, v in o.items() if k not in HIDE and not k.startswith(KEEP_PREFIX_DROP)
                               and k != "evidence_confidence"})
    for i, pk in enumerate(packets, 1):
        with (out / f"packet_{i:02d}.jsonl").open("w", encoding="utf-8") as f:
            for r in pk:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"packet_{i:02d}: {len(pk)} records")


if __name__ == "__main__":
    main()
