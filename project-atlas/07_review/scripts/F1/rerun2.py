import sys, json, copy
sys.path.insert(0, '/home/user/playground/project-atlas/tools'); sys.path.insert(0,'/tmp/claude-0/atlas_scratch/F1')
import fin_engine as E
B='/home/user/playground/project-atlas/08_financial_models/'
def run(tag,a,scen='base',ov=None):
    R=E.run(a,scen,ov or {}); S=R['summary']
    R0=E.run(a,scen,dict(ov or {},founder_draw_per_month=0))
    pk0=-min(0,min(R0['cum_retained'][1:]))
    ms=[m for m in range(1,61) if R['op'][m]>=10000]
    print(f"{tag:48s} y3op={S['y3_op']:>9,.0f} y4op={S['y4_op']:>9,.0f} y5op={S['y5_op']:>9,.0f} y5fcf={S['y5_fcf']:>9,.0f} y3cust={S['y3_active_end']:5.1f} peak={S['peak_funding_need']:>9,.0f} peak0={pk0:>8,.0f} 10k/mo@{ms[0] if ms else None}")
    return S
a=json.load(open(B+'SYN-006_assumptions.json'))
def syn(per,cost,rev):
    b=copy.deepcopy(a)
    for s in b['staff']:
        if s['role'].startswith('Construction bookkeeper'):
            s['per']=per; s['monthly_cost']=cost
        if s['role'].startswith('External'):
            s['monthly_cost']=rev
    return b
print('SYN-006')
c=syn(13,{'conservative':7000,'base':6200,'optimistic':5800},{'conservative':1500,'base':1000,'optimistic':700})
for arpc in [1000,950,900]:
    run(f'per13 $6.2k rev$1k ARPC {arpc}',c,ov={'arpc_monthly':arpc})
run('per13 $6.2k ARPC 950 win .25',c,ov={'arpc_monthly':950,'proposal_to_win_pct':0.25})
run('per13 $6.2k corrected conservative',c,'conservative')
run('per13 $6.2k optimistic',c,'optimistic')
run('labour x1.2 on original',a,ov={'labor_cost_multiplier':1.2})
w=json.load(open(B+'WS16-006_assumptions.json'))
print('WS16-006')
cb={'gross_margin_pct':0.27,'onetime_gross_margin_pct':0.25,'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':600}
run('corrected base GM27/25 churn3 DSO45 ARPC600',w,ov=cb)
run('  same, win .2',w,ov=dict(cb,proposal_to_win_pct=0.2))
run('  same, GM 30/28 (if V1 passes)',w,ov=dict(cb,gross_margin_pct=0.30,onetime_gross_margin_pct=0.28))
run('corrected cons GM23/21 churn4 DSO55 ARPC450',w,'conservative',{'gross_margin_pct':0.23,'onetime_gross_margin_pct':0.21,'monthly_churn_pct':0.04,'dso_days':55,'arpc_monthly':450})
