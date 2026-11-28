#!/usr/bin/env python3
"""Validate a discovery workstream's JSONL outputs.

Usage: python3 tools/validate_discovery.py WS03        (validates 02_discovery/WS03_*.jsonl)
       python3 tools/validate_discovery.py --all
Exit code 0 = valid. Prints every problem found.
"""
import json, sys, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DISC = ROOT / "02_discovery"

REQUIRED = ["id","title","workstream","industry","subindustry","naics","mechanisms","product_service",
 "target_customer","purchase_motivation","spending_evidence","representative_operators","revenue_mechanism",
 "typical_transaction_value","gross_margin_pct_low","gross_margin_pct_high","direct_costs",
 "contribution_profit_note","validation_cost_usd","launch_capital_usd_low","launch_capital_usd_high",
 "working_capital_note","time_to_first_revenue_months","time_to_profitability_months","sales_cycle",
 "repeat_purchase","acquisition_channels","customer_accessibility","supplier_accessibility",
 "competitive_intensity","entry_strategy","licenses","regulatory_barriers","operational_risks",
 "financial_risks","geographic_constraints","founder_expertise","staffing","automation_potential",
 "delegation_potential","scalability","expansion","yr3_operating_profit_usd_low",
 "yr3_operating_profit_usd_high","plausible_milestone_ceiling","roic_note","evidence_confidence",
 "source_ids","critical_assumptions","unanswered_questions","failure_modes","scores","score_rationale",
 "gates","preliminary_verdict"]
NUMERIC = ["gross_margin_pct_low","gross_margin_pct_high","validation_cost_usd","launch_capital_usd_low",
 "launch_capital_usd_high","time_to_first_revenue_months","time_to_profitability_months",
 "yr3_operating_profit_usd_low","yr3_operating_profit_usd_high"]
LISTS = ["mechanisms","representative_operators","acquisition_channels","source_ids","critical_assumptions",
 "unanswered_questions","failure_modes","gates"]
SCORE_KEYS = ["fcf","roic","access","scale","resilience","entry","delegation","cash","feasibility","ai"]
SRC_REQUIRED = ["source_id","url","organization","title","publication_date","access_date","claim",
 "evidence_level","excerpt","limitations","opportunity_ids"]
LEVELS = set("ABCDE")


def load_jsonl(path, errors):
    rows = []
    if not path.exists():
        errors.append(f"missing file {path.name}")
        return rows
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as e:
            errors.append(f"{path.name}:{i} JSON parse error: {e}")
    return rows


def validate(ws):
    errors, warnings = [], []
    opps = load_jsonl(DISC / f"{ws}_opportunities.jsonl", errors)
    srcs = load_jsonl(DISC / f"{ws}_sources.jsonl", errors)
    src_ids = set()
    for s in srcs:
        for k in SRC_REQUIRED:
            if k not in s:
                errors.append(f"source {s.get('source_id','?')}: missing key {k}")
        if s.get("evidence_level") not in LEVELS:
            errors.append(f"source {s.get('source_id','?')}: bad evidence_level {s.get('evidence_level')}")
        sid = s.get("source_id")
        if sid in src_ids:
            errors.append(f"duplicate source_id {sid}")
        src_ids.add(sid)
        if not str(s.get("url","")).startswith("http"):
            warnings.append(f"source {sid}: url not http(s)")
    ids = set()
    for o in opps:
        oid = o.get("id", "?")
        for k in REQUIRED:
            if k not in o:
                errors.append(f"{oid}: missing key {k}")
        if oid in ids:
            errors.append(f"duplicate id {oid}")
        ids.add(oid)
        if not re.match(rf"^{ws}-\d{{3}}$", str(oid)):
            errors.append(f"{oid}: id must look like {ws}-001")
        for k in NUMERIC:
            v = o.get(k)
            if v is not None and not isinstance(v, (int, float)):
                errors.append(f"{oid}: {k} must be number or null (got {v!r})")
        for k in LISTS:
            if k in o and not isinstance(o[k], list):
                errors.append(f"{oid}: {k} must be a list")
        sc = o.get("scores", {})
        if not isinstance(sc, dict):
            errors.append(f"{oid}: scores must be an object")
        else:
            for k in SCORE_KEYS:
                v = sc.get(k)
                if not isinstance(v, int) or not 1 <= v <= 10:
                    errors.append(f"{oid}: scores.{k} must be int 1-10 (got {v!r})")
        if o.get("evidence_confidence") not in LEVELS:
            errors.append(f"{oid}: evidence_confidence must be one of A-E")
        for sid in o.get("source_ids", []) or []:
            if sid not in src_ids:
                warnings.append(f"{oid}: source_id {sid} not found in sources file")
        lo, hi = o.get("yr3_operating_profit_usd_low"), o.get("yr3_operating_profit_usd_high")
        if isinstance(lo, (int, float)) and isinstance(hi, (int, float)) and lo > hi:
            errors.append(f"{oid}: yr3 profit low > high")
        if o.get("evidence_confidence") in ("A", "B") and not o.get("source_ids"):
            errors.append(f"{oid}: evidence A/B claimed but no source_ids")
    summary = DISC / f"{ws}_summary.md"
    if not summary.exists():
        warnings.append(f"missing {summary.name}")
    print(f"[{ws}] opportunities={len(opps)} sources={len(srcs)} errors={len(errors)} warnings={len(warnings)}")
    for e in errors:
        print("  ERROR", e)
    for w in warnings[:40]:
        print("  warn ", w)
    return not errors


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "--all":
        wss = sorted({p.name.split("_")[0] for p in DISC.glob("WS*_opportunities.jsonl")})
    else:
        wss = args
    ok = all([validate(w) for w in wss])
    sys.exit(0 if ok else 1)
