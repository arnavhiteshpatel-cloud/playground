#!/usr/bin/env python3
"""Create <ID>-REV_assumptions.json = Stage E assumptions + Stage F reviewer's corrected drivers.

Rules (applied identically to all four):
  BASE         = reviewer's corrected base exactly (reproduces the review's headline re-run).
  CONSERVATIVE = filed Stage E conservative, with the reviewer's conservative corrections layered on
                 only where they are LESS favourable than the filed value (never make a case rosier).
  OPTIMISTIC   = the reviewer's stated upside case where the review defines one (WS12-014: "Stage E base
                 becomes the optimistic case"; SYN-004: reviewer upside = base + 4 overrides), else the filed
                 optimistic with the reviewer's cost corrections layered on (SYN-006, WS04-014).
  start_capital_injection = REV base peak funding rounded up to $100 (Stage E standardization rule; it does
                 not change any operating, FCF or peak-funding metric).
Stage E files are only read, never written.
"""
import json, copy, math, sys, pathlib
ROOT = pathlib.Path("/home/user/playground/project-atlas")
sys.path.insert(0, str(ROOT / "tools"))
import fin_engine as E
FM = ROOT / "08_financial_models"
SCEN = ["conservative", "base", "optimistic"]


def load(i):
    return json.loads((FM / f"{i}_assumptions.json").read_text())


def as_dict(v):
    if isinstance(v, dict):
        return {s: v.get(s, v.get("base")) for s in SCEN}
    return {s: v for s in SCEN}


def setd(a, key, cons=None, base=None, opt=None, ev="E", src=""):
    cur = as_dict(a["drivers"].get(key, E.DEFAULTS[key]))
    for s, v in (("conservative", cons), ("base", base), ("optimistic", opt)):
        if v is not None:
            cur[s] = v
    a["drivers"][key] = cur
    a["drivers"][key + "__evidence"] = ev
    old = a["drivers"].get(key + "__source", "")
    a["drivers"][key + "__source"] = f"STAGE F CORRECTION: {src} | Stage E source: {old}"


def opt_equals_base(a):
    """Make every scenario-dependent value's optimistic column equal its base column."""
    for k, v in list(a["drivers"].items()):
        if isinstance(v, dict):
            v["optimistic"] = v.get("base")
    for grp, fld in (("staff", "monthly_cost"), ("staff", "capex_per_hire"), ("overhead", "monthly"), ("capex", "amount")):
        for it in a.get(grp, []):
            if isinstance(it.get(fld), dict):
                it[fld]["optimistic"] = it[fld].get("base")


def finish(a, oid, name, changes):
    a["id"] = oid + "-REV"
    a["name"] = name + " (post-review)"
    a["summary"] = ("POST-REVIEW MODEL. Stage E assumptions with the Stage F adversarial reviewer's corrected drivers applied. "
                    + " ".join(changes["summary"]) + " Original Stage E model: " + oid + "_assumptions.json (unchanged).")
    a["review_changes"] = changes["list"]
    a["evidence_notes"] = ["STAGE F CORRECTIONS (07_review/" + oid + "_review.md): " + "; ".join(changes["list"])] + a.get("evidence_notes", [])
    # start capital = base peak (rounded up to $100)
    pk = E.run(a, "base")["summary"]["peak_funding_need"]
    a["drivers"]["start_capital_injection"] = int(math.ceil(max(pk, 100) / 100.0) * 100)
    a["drivers"]["start_capital_injection__evidence"] = "E"
    a["drivers"]["start_capital_injection__source"] = ("Stage E standardization rule re-applied to the post-review base: smallest round "
                                                       "injection keeping base cash >= 0 (REV base peak funding rounded up to $100). Does not "
                                                       "change operating profit, FCF or peak funding.")
    out = FM / f"{oid}-REV_assumptions.json"
    out.write_text(json.dumps(a, indent=1, ensure_ascii=False))
    print("wrote", out.name)
    return a


R = lambda i: f"07_review/{i}_review.md"

# ------------------------------------------------------------------ WS12-014
def ws12014():
    i = "WS12-014"; a = load(i); nm = a["name"]
    stageE = copy.deepcopy(a)
    opt_equals_base(a)          # optimistic := Stage E base (reviewer: "The Stage E base becomes the optimistic case")
    src = R(i)
    setd(a, "lead_to_proposal_pct", base=0.22, src=f"{src} §1 and §4 top-5 table: conversation -> signed agreement 30% -> 22% so that passing the playbook's own decisive gate (>=5 of 30 = 16.7%) is consistent with base; optimistic = Stage E base 30%; conservative unchanged (25%, offset by 7 conversations/month and an 18-month ramp)")
    setd(a, "proposal_to_win_pct", base=0.15, src=f"{src} §4: fill ratio 20% -> 15% (non-exclusive orders vs in-house TA with LinkedIn Hiring Assistant [B] and Actalent/Aerotek; PageGroup flags offer conversion as its top problem [B]); optimistic = Stage E base 20%")
    setd(a, "founder_ramp_months", base=15, src=f"{src} §4: ramp 12 -> 15 months (no agreed benchmark; in-firm ramps assume existing job orders [D]); optimistic = Stage E base 12")
    setd(a, "sales_cycle_months", base=5, src=f"{src} §4: sales cycle 4 -> 5 months; optimistic = Stage E base 4")
    setd(a, "arpc_monthly", base=520, src=f"{src} §4: repeat revenue $670 -> $520/month per active client (0.35 repeat placements/yr instead of 0.45; repeats consume desk time); optimistic = Stage E base $670")
    setd(a, "monthly_churn_pct", base=0.055, src=f"{src} §4: churn 5% -> 5.5%/month; optimistic = Stage E base 5%")
    setd(a, "ev_multiple", cons=1.0, base=1.5, opt=2.0, ev="D/E", src=f"{src} §3: 'Valuation 2.0x ... arguably generous for a single-producer desk where relationships leave with the producer. 1.0-1.5x is more defensible' -> base 1.5x (top of reviewer range), conservative 1.0x (unchanged), optimistic 2.0x (= Stage E base)")
    # make sure optimistic values that were scalars-at-base remain Stage E base (already done by opt_equals_base)
    ch = {"summary": ["Corrected base (review §1/§4): conversation->agreement 22%, fill 15%, ramp 15 mo, sales cycle 5 mo, repeat revenue $520/mo (0.35 repeats/yr), churn 5.5%/mo; EV 1.5x (review §3).",
                      "Optimistic = the Stage E base in every driver (review: 'The Stage E base becomes the optimistic case'), except EV 2.0x (also Stage E base). Conservative = Stage E conservative unchanged (review: 'Conservative (unchanged)')."],
          "list": ["lead_to_proposal_pct base 0.30->0.22", "proposal_to_win_pct base 0.20->0.15", "founder_ramp_months base 12->15",
                   "sales_cycle_months base 4->5", "arpc_monthly (repeat revenue) base 670->520", "monthly_churn_pct base 0.050->0.055",
                   "ev_multiple base 2.0->1.5 (opt 2.75->2.0)", "optimistic scenario := Stage E base (all drivers, staff, overhead)",
                   "conservative unchanged (note: its conversion 25% and repeat revenue $570 sit above the corrected base; offset by 7 conversations/mo, 18-mo ramp, 7% churn, $13.7k fee)"]}
    return finish(a, i, nm, ch)

# ------------------------------------------------------------------ SYN-006
def syn006():
    i = "SYN-006"; a = load(i); nm = a["name"]; src = R(i)
    setd(a, "arpc_monthly", base=950, ev="D/E", src=f"{src} §4 top-5 table: ARPC $1,000 -> $950 base / $800 conservative (already filed). Newcomer sells against Wishup's dedicated construction-trained bookkeeper from $999/month that lists WIP preparation [D, C5-S035]; vendor bands are the vendor's own pricing [D, C5-S009]. Optimistic $1,200 unchanged (not reviewer-endorsed)")
    for s in a["staff"]:
        if s["role"].startswith("Construction bookkeeper"):
            s["per"] = 13
            s["monthly_cost"] = {"conservative": 7000, "base": 6200, "optimistic": 5800}
            s["notes"] = ("STAGE F CORRECTION (" + src + " §4): 15 -> 13 clients per bookkeeper (reviewer base 13 / conservative 11; the engine's 'per' is not scenario-specific, so 13 is used in all scenarios as in the reviewer's own corrected-conservative run); loaded cost $5,800 -> $6,200 base / $7,000 conservative / $5,800 optimistic: Chicago metro bookkeeping clerk mean $53,560 [C, F1-S001], business & financial ops mean $46.54/h [C, F1-S002]; a full-charge construction bookkeeper sits between. | Stage E: " + s["notes"])
        if s["role"].startswith("External"):
            s["monthly_cost"] = {"conservative": 1500, "base": 1000, "optimistic": 700}
            s["notes"] = ("STAGE F CORRECTION (" + src + " §4): reviewer $600 -> $1,000 base / $1,500 conservative / $700 optimistic; an experienced construction controller/CPA is unlikely to bill under $150/h (E; rate MISSING). | Stage E: " + s["notes"])
    ch = {"summary": ["Corrected base (review §4, 'all four'): ARPC $950, 13 clients per bookkeeper, bookkeeper $6,200/mo loaded, external construction reviewer $1,000/mo.",
                      "Conservative = Stage E conservative + bookkeeper $7,000 and reviewer $1,500 (review 'corrected conservative'). Optimistic = Stage E optimistic + bookkeeper $5,800 / reviewer $700 / 13 per bookkeeper; NOT reviewer-endorsed (review ceiling ~$150k/yr)."],
          "list": ["arpc_monthly base 1000->950", "bookkeeper clients-per-head 15->13 (all scenarios; reviewer cons 11 not representable)",
                   "bookkeeper loaded cost 5800/5800/5500 -> 7000/6200/5800 (cons/base/opt)", "external reviewer 1200/600/400 -> 1500/1000/700",
                   "not modelled (reviewer 'missing line'): clean-up overruns/write-offs ~1-2% of revenue (E)"]}
    return finish(a, i, nm, ch)

# ------------------------------------------------------------------ SYN-004
def syn004():
    i = "SYN-004"; a = load(i); nm = a["name"]; src = R(i)
    filed_cons = {k: as_dict(a["drivers"][k])["conservative"] for k in ["sales_cycle_months", "founder_leads_per_month", "proposal_to_win_pct", "arpc_monthly", "monthly_churn_pct"]}
    opt_equals_base(a)   # optimistic := reviewer upside = base + 4 overrides (review §4 combined runs)
    setd(a, "sales_cycle_months", cons=max(12, filed_cons["sales_cycle_months"]), base=10, opt=8,
         src=f"{src} §2 F5 and §4: fee starts only when the new supply contract flows at the customer's current expiry (ENGIE pays nothing until a Customer Agreement is executed and the customer pays [B, F2-S005]); ~3 months selling + ~9-month average expiry wait -> 10 base / 12 conservative / 8 upside (E). Biggest error in the Stage E model")
    setd(a, "founder_leads_per_month", cons=min(5, filed_cons["founder_leads_per_month"]), base=7, opt=9,
         src=f"{src} §4: courted, already-brokered exempt pool (93% of >1 MW ComEd usage on ARES [A, F2-S008]); must screen kW before pitching; no track record (E): 10 -> 7 base / 5 conservative / 9 upside")
    setd(a, "proposal_to_win_pct", cons=min(0.15, filed_cons["proposal_to_win_pct"]), base=0.20, opt=0.22,
         src=f"{src} §4: every win displaces an incumbent broker; customer designates between brokers [B, F2-S005] (E): 22% -> 20% base / 15% conservative / 22% upside")
    setd(a, "arpc_monthly", cons=min(650, filed_cons["arpc_monthly"]), base=800, opt=900, ev="D/E",
         src=f"{src} §3/§4: DR partner share ~0 (CSPs advertise 100% pass-through [D, F2-S010]) and true-ups [B]: $850 -> $800 base / upside $900; conservative keeps the filed $460 (harsher than the reviewer's $650)")
    setd(a, "monthly_churn_pct", cons=max(0.018, filed_cons["monthly_churn_pct"]), src=f"{src} §4: churn 1.2% kept as reasonable; reviewer conservative 1.8% is milder than filed 2.0%, so filed 2.0% kept")
    ch = {"summary": ["Corrected base (review §1/§4 'Reviewer base'): sales cycle 10 months (contract-expiry wait), 7 qualified exempt-size conversations/month, 20% proposal->win, ARPC $800 (DR share ~0).",
                      "Optimistic = reviewer upside exactly (cycle 8, 9 leads, 22% win, ARPC $900, all other drivers at base). Conservative = Stage E conservative with reviewer's cycle 12 and 5 leads layered on (reviewer's ARPC $650 and churn 1.8% are milder than filed, so filed $460 / 2.0% kept)."],
          "list": ["sales_cycle_months 6/4/3 -> 12/10/8", "founder_leads_per_month 6/10/12 -> 5/7/9", "proposal_to_win_pct 0.15/0.22/0.28 -> 0.15/0.20/0.22",
                   "arpc_monthly 460/850/1380 -> 460/800/900", "optimistic scenario := reviewer upside (other drivers at base)",
                   "reviewer's own conservative (base drivers + cycle 12, leads 5, win 15%, ARPC 650, churn 1.8%) reported separately: Y3 -$2.7k, Y5 $30.4k, peak $212.6k"]}
    return finish(a, i, nm, ch)

# ------------------------------------------------------------------ WS04-014
def ws04014():
    i = "WS04-014"; a = load(i); nm = a["name"]; src = R(i)
    setd(a, "arpc_monthly", base=650, ev="B/D/E",
         src=f"{src} §2 F2-F3, §4: Siotek is active in Chicago (landing page, coordinated on-site technicians [D, F4-S002]) at $399 + add-ons with free onboarding incl. risk assessment [B, F4-S003]; $690 -> $650 base; conservative $540 unchanged; optimistic $860 unchanged (not reviewer-endorsed)")
    setd(a, "onetime_revenue_per_new_customer", cons=300, base=500, ev="B/E",
         src=f"{src} §4: Siotek charges $0 onboarding [B, F4-S003]: $1,000 -> $500 base / $500 -> $300 conservative; optimistic unchanged")
    for s in a["staff"]:
        if s["role"].startswith("Field"):
            s["monthly_cost"] = {"conservative": 8000, "base": 7500, "optimistic": 7100}
            s["notes"] = ("STAGE F CORRECTION (" + src + " §2 F1, §4): the role is a solo field engineer, so the comparable occupation is Chicago computer network support specialist, median $73,340 (75th pct $88,550) [C, F4-S004], not help-desk $59,860: loaded $6,500 -> $7,500 base / $8,000 conservative / $7,100 optimistic (reviewer script: base - $400). Hire trigger kept at 14 practices (reviewer recommends 18 as an operating rule; reported as a variant, not built in). | Stage E: " + s["notes"])
    ch = {"summary": ["Corrected base (review §1/§4): technician $7,500/mo loaded, ARPC $650, onboarding $500; every funnel rate as filed; first technician still triggered at 14 practices.",
                      "Conservative = Stage E conservative + technician $8,000 + onboarding $300. Optimistic = Stage E optimistic + technician $7,100; NOT reviewer-endorsed. Reviewer's recommended hire-at-18 rule is reported as a variant."],
          "list": ["arpc_monthly base 690->650", "onetime_revenue_per_new_customer cons/base 500/1000 -> 300/500",
                   "field technician loaded cost 7000/6500/6200 -> 8000/7500/7100", "hire trigger 14 kept (variant at 18 reported separately)"]}
    return finish(a, i, nm, ch)


if __name__ == "__main__":
    for f in (ws12014, syn006, syn004, ws04014):
        f()
