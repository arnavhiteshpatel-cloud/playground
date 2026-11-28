#!/usr/bin/env python3
"""Create blinded scoring packets: records with author scores, rationale, gates and verdict removed.

Usage: python3 tools/make_blind_packets.py [n_packets] [--ws WS02,WS03] [--prefix A]
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
    args = sys.argv[1:]
    n = int(args[0]) if args and args[0].isdigit() else 8
    wsf = args[args.index("--ws") + 1].split(",") if "--ws" in args else None
    prefix = args[args.index("--prefix") + 1] if "--prefix" in args else ""
    opps = [json.loads(l) for l in (DB / "opportunities.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    opps = [o for o in opps if not o.get("duplicate_of") and (wsf is None or o.get("workstream") in wsf)]
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
    for p in out.glob(f"packet_{prefix}*.jsonl"):
        p.unlink()
    packets = [[] for _ in range(n)]
    for i, o in enumerate(order):
        packets[i % n].append({k: v for k, v in o.items() if k not in HIDE and not k.startswith(KEEP_PREFIX_DROP)
                               and k != "evidence_confidence"})
    for i, pk in enumerate(packets, 1):
        with (out / f"packet_{prefix}{i:02d}.jsonl").open("w", encoding="utf-8") as f:
            for r in pk:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"packet_{prefix}{i:02d}: {len(pk)} records")


if __name__ == "__main__":
    main()
