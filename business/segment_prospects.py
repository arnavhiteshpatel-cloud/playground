"""Segment and prioritise the 103 organisations in business/prospects.csv for customer discovery.

Uses only fields already in prospects.csv (type, fit, latest_510k, public_contact_route, evidence, relevant_activity).
Writes business/prospect_segments.csv. The scoring rubric is documented in business/PROSPECT_SEGMENTATION.md.
No organisation has been contacted; a score is a guess about who is most likely to have the problem, not demand.

    python business/segment_prospects.py
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Explicit core-facility assignments: cores named in MARKET_MODEL_INPUTS.md §2 plus the local Beckman ITG and the HSS
# micro-CT core (fee schedule page fetched 2026-11-27: https://www.hss.edu/research/core-facilities/micro-computed-tomography-core)
CORE_IDS = {"P087", "P088", "P089", "P090", "P091", "P094", "P101"}
SEGMENT_INFO = {
    "ORTHO": ("Orthobiologic, spine-graft and tissue companies", "Non-GLP study analysis; material characterisation; paid pilot"),
    "DENTAL": ("Dental regenerative (graft / membrane) companies", "Non-GLP study analysis; material characterisation; paid pilot"),
    "CRO": ("Preclinical CROs", "Enterprise desktop licence; subcontracted study analysis"),
    "CORE": ("Academic micro-CT core facilities", "Academic desktop licence (core-wide); recharge-friendly terms"),
    "LAB": ("Academic and VA research labs", "Academic desktop licence"),
    "CHANNEL": ("Imaging / software vendors (channel or competitor, not buyers)", "Partnership only after validation; no sales pitch"),
}
UNVERIFIED_CONTACT = re.compile(r"not verified|blocked|503|unverified|domain error|URL not verified", re.I)


def segment(r):
    i = int(r["id"][1:])
    if r["id"] in CORE_IDS:
        return "CORE"
    if 1 <= i <= 51:
        return "ORTHO"
    if 52 <= i <= 69:
        return "DENTAL"
    if 70 <= i <= 81:
        return "CRO"
    if 82 <= i <= 86:
        return "CHANNEL"
    return "LAB"


def latest_year(r):
    years = [int(y) for y in re.findall(r"\b(20\d\d)-\d\d-\d\d\b", r["latest_510k"] + " " + r["relevant_activity"])]
    return max(years) if years else None


def score(r, seg):
    parts = []
    s = {"A": 3, "B": 2, "C": 0}[r["fit"]]
    parts.append(f"fit {r['fit']} (+{s})")
    if seg in ("ORTHO", "DENTAL"):
        y = latest_year(r)
        if y and y >= 2025:
            s += 2
            parts.append(f"regulatory activity {y} (+2)")
        elif y and y >= 2023:
            s += 1
            parts.append(f"regulatory activity {y} (+1)")
    route = r["public_contact_route"]
    if route and not UNVERIFIED_CONTACT.search(route) and "[UNR] contact" not in r["evidence"]:
        s += 1
        parts.append("company-level contact route verified (+1)")
    else:
        parts.append("contact route unverified (+0)")
    if re.search(r"\blarge\b", r["type"], re.I) or re.search(r"enterprise", r["fit_rationale"], re.I):
        s -= 1
        parts.append("enterprise procurement (-1)")
    if seg == "CRO" and "[V]" in r["evidence"] and re.search(r"orthop|bone|GLP", r["relevant_activity"], re.I):
        s += 1
        parts.append("bone/orthopaedic or GLP scope on a fetched page (+1)")
    if seg in ("CORE", "LAB") and re.search(r"NIH RePORTER", r["evidence"]):
        s += 1
        parts.append("NIH micro-CT bone project on record (+1)")
    if seg == "CHANNEL":
        s = 0
        parts = ["channel/competitor: excluded from buyer waves"]
    return s, "; ".join(parts)


# First 10 discovery conversations: a quota per segment, so that every pricing hypothesis meets its buyer early
# (study analysis and characterisation -> manufacturers; enterprise licence -> CROs; academic licence -> core + lab).
WAVE1_QUOTA = {"ORTHO": 4, "DENTAL": 2, "CRO": 2, "CORE": 1, "LAB": 1}


def prospects_md_rank():
    """Rank in the existing 'Top 15' table of PROSPECTS.md (used only to break score ties)."""
    ranks = {}
    for line in (HERE / "PROSPECTS.md").read_text().splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*(P\d{3})\s*\|", line)
        if m:
            ranks[m.group(2)] = int(m.group(1))
    return ranks


def assign_waves(out):
    ranks = prospects_md_rank()
    key = lambda d: (-d["priority_score"], ranks.get(d["id"], 99), d["id"])
    for seg, n in WAVE1_QUOTA.items():
        cands = sorted([d for d in out if d["segment"] == seg and d["fit"] != "C"], key=key)
        for d in cands[:n]:
            d["wave"] = "Wave 1"
    for d in out:
        if d.get("wave"):
            continue
        if d["segment"] == "CHANNEL":
            d["wave"] = "Hold (partner/competitor)"
        elif d["fit"] == "C":
            d["wave"] = "Hold"
        elif d["priority_score"] >= 4:
            d["wave"] = "Wave 2"
        else:
            d["wave"] = "Wave 3"


def main():
    rows = list(csv.DictReader(open(HERE / "prospects.csv", newline="")))
    out = []
    for r in rows:
        seg = segment(r)
        s, why = score(r, seg)
        out.append({"id": r["id"], "organization": r["organization"], "segment": seg,
                    "segment_name": SEGMENT_INFO[seg][0], "fit": r["fit"], "priority_score": s,
                    "wave": "", "score_rationale": why,
                    "first_offering_to_discuss": SEGMENT_INFO[seg][1],
                    "decision_maker_role": r["decision_maker_role"],
                    "public_contact_route": r["public_contact_route"], "evidence": r["evidence"]})
    assign_waves(out)
    order = {"Wave 1": 0, "Wave 2": 1, "Wave 3": 2, "Hold": 3, "Hold (partner/competitor)": 4}
    out.sort(key=lambda d: (order[d["wave"]], -d["priority_score"], d["id"]))
    with open(HERE / "prospect_segments.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    c = Counter((d["segment"], d["wave"]) for d in out)
    for seg in SEGMENT_INFO:
        print(seg, {k[1]: v for k, v in c.items() if k[0] == seg})
    print("Wave 1:", [(d["id"], d["organization"][:40], d["priority_score"]) for d in out if d["wave"] == "Wave 1"])


if __name__ == "__main__":
    main()
