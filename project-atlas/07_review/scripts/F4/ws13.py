from base import *
a=json.load(open(B+'WS13-014_assumptions.json'))
def mod(a,tech=None,ins=None):
    b=copy.deepcopy(a)
    for s in b['staff']:
        if s['role'].startswith('GPR') and tech: s['monthly_cost']={'conservative':tech+900,'base':tech,'optimistic':tech-600}
    for o in b['overhead']:
        if o['item'].startswith('Business insurance') and ins: o['monthly']={'conservative':ins+400,'base':ins,'optimistic':ins-200}
    return b
show('orig base',a)
for k,v in [('arpc_monthly',650),('arpc_monthly',700),('monthly_churn_pct',0.06),('proposal_to_win_pct',0.30),('founder_leads_per_month',18)]:
    show(f'{k}={v}',a,ov={k:v})
show('tech 8,700',mod(a,tech=8700))
show('insurance 1,000',mod(a,ins=1000))
b=mod(a,tech=8700,ins=1000)
C={'arpc_monthly':675,'monthly_churn_pct':0.06,'proposal_to_win_pct':0.30}
R=show('CORR BASE: ARPC 675, churn 6%, win .30, tech 8.7k, ins 1k',b,ov=C)
S=R['summary']; print({k:round(S[k]) for k in ['y1_op','y2_op','y3_op','y4_op','y5_op','breakeven_month','payback_month','min_cash_balance','lt_y10_cum_deployable','lt_y10_op','y3_revenue']}, [sum(h[m] for h in R['headcount']) for m in (12,24,36,60)])
show(' same, founder-only',b,ov=dict(C,staff_threshold_multiplier=100))
show(' same, hire gate at 25 accts / ARPC>=650 holds',b,ov=dict(C))
show(' ARPC 650',b,ov=dict(C,arpc_monthly=650))
show(' ARPC 750 (orig) with other corrections',b,ov=dict(C,arpc_monthly=750))
show(' ARPC 600 founder-only',b,ov=dict(C,arpc_monthly=600,staff_threshold_multiplier=100))
show('orig conservative',a,'conservative')
show('orig conservative founder-only',a,'conservative',ov={'staff_threshold_multiplier':100})
show('orig base founder-only',a,ov={'staff_threshold_multiplier':100})
