from base import *
a=json.load(open(B+'WS04-014_assumptions.json'))
def tech(a,cost):
    b=copy.deepcopy(a)
    for s in b['staff']:
        if s['role'].startswith('Field'): s['monthly_cost']={'conservative':cost+500,'base':cost,'optimistic':cost-400}
    return b
show('orig base',a)
show('ARPC 625',a,ov={'arpc_monthly':625})
show('onboard 500',a,ov={'onetime_revenue_per_new_customer':500})
show('win 0.20',a,ov={'proposal_to_win_pct':0.20})
show('churn 1.25%',a,ov={'monthly_churn_pct':0.0125})
b=tech(a,7900); show('tech $7,900',b)
show('tech 7900 + ARPC 625',b,ov={'arpc_monthly':625})
show('tech 7900 + ARPC 625 + onboard 500',b,ov={'arpc_monthly':625,'onetime_revenue_per_new_customer':500})
C={'arpc_monthly':625,'onetime_revenue_per_new_customer':500,'proposal_to_win_pct':0.20,'monthly_churn_pct':0.0125}
R=show('CORRECTED BASE (tech 7900, ARPC 625, onb 500, win .20, churn 1.25%)',b,ov=C)
S=R['summary']; print({k:round(S[k]) for k in ['y1_op','y2_op','y3_op','y4_op','y5_op','breakeven_month','payback_month','first_month_op_5k','first_month_op_10k','min_cash_balance','lt_cum_deployable' if 'lt_cum_deployable' in S else 'y5_fcf']})
print([k for k in S if k.startswith('lt_')])
show('corrected + insurance 700 (ovh x1.1)',b,ov=dict(C,overhead_multiplier=1.1))
show('corrected, ARPC 690 (keep price)',b,ov=dict(C,arpc_monthly=690))
show('corrected, win .25',b,ov=dict(C,proposal_to_win_pct=0.25))
show('corrected, hours 8 -> per 21 practices',b,ov=dict(C,staff_threshold_multiplier=0.75))
show('corrected, founder never hires (threshold x100)',b,ov=dict(C,staff_threshold_multiplier=100))
show('corrected conservative (orig cons + tech 8400)',b,'conservative')
show('corrected conservative founder-only',b,'conservative',ov={'staff_threshold_multiplier':100})
