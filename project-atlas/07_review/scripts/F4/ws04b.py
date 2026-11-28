from base import *
a=json.load(open(B+'WS04-014_assumptions.json'))
def tech(a,cost,thr=14,per=28):
    b=copy.deepcopy(a)
    for s in b['staff']:
        if s['role'].startswith('Field'): s['monthly_cost']={'conservative':cost+500,'base':cost,'optimistic':cost-400}; s['threshold']=thr; s['per']=per
    return b
C={'arpc_monthly':650,'onetime_revenue_per_new_customer':500}
b=tech(a,7500)
R=show('CORR BASE: tech 7500, ARPC 650, onb 500',b,ov=C)
S=R['summary']; print({k:round(S[k]) for k in ['y1_op','y2_op','y3_op','y4_op','y5_op','breakeven_month','payback_month','first_month_op_5k','first_month_op_10k','min_cash_balance','lt_y10_cum_deployable','lt_y10_op']})
show(' + win 0.20',b,ov=dict(C,proposal_to_win_pct=0.2))
show(' + win 0.20 + leads 10',b,ov=dict(C,proposal_to_win_pct=0.2,founder_leads_per_month=10))
b8=tech(a,7500,thr=11,per=21)
show(' 8 h/practice (founder 11, tech 21)',b8,ov=C)
show(' ARPC 690 retained',b,ov=dict(C,arpc_monthly=690))
show(' ARPC 600',b,ov=dict(C,arpc_monthly=600))
show(' hire at 18 not 14',tech(a,7500,thr=18),ov=C)
R=show(' hire at 18, per 28, ARPC 650',tech(a,7500,thr=18),ov=C); S=R['summary']; print({k:round(S[k]) for k in ['y3_op','y4_op','y5_op','min_cash_balance']})
bc=tech(a,7500)
show('CORR CONS: orig cons + tech 8000',bc,'conservative')
show('CORR CONS founder-only (never hires)',bc,'conservative',ov={'staff_threshold_multiplier':100})
show('orig base, founder only',a,ov={'staff_threshold_multiplier':100})
