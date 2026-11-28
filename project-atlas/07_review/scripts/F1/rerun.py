import sys, json, copy
sys.path.insert(0, '/home/user/playground/project-atlas/tools')
import fin_engine as E
B='/home/user/playground/project-atlas/08_financial_models/'
def show(tag, a, scen='base', ov=None):
    R=E.run(a, scen, ov or {}); S=R['summary']
    print(f"{tag:55s} y3op={S['y3_op']:>10,.0f} y5op={S['y5_op']:>10,.0f} y3rev={S['y3_revenue']:>10,.0f} y3cust={S['y3_active_end']:6.1f} y5cust={S['y5_active_end']:6.1f} peak={S['peak_funding_need']:>10,.0f} peak_nodraw={-min(0,min([x for x in E.run(a,scen,dict(ov or {},founder_draw_per_month=0))['cum_retained'][1:]])):>9,.0f}")
    return S
# ---- SYN-006
a=json.load(open(B+'SYN-006_assumptions.json'))
print("SYN-006")
show('original base',a)
show('original conservative',a,'conservative')
show('ARPC 900',a,ov={'arpc_monthly':900})
show('ARPC 800',a,ov={'arpc_monthly':800})
b=copy.deepcopy(a)
for s in b['staff']:
    if s['role'].startswith('Construction bookkeeper'):
        s['per']=12; s['monthly_cost']={'conservative':7200,'base':6500,'optimistic':6000}
    if s['role'].startswith('External'):
        s['monthly_cost']={'conservative':1500,'base':1000,'optimistic':700}
show('bookkeeper 12 clients @ $6.5k, reviewer $1k',b)
show('  + ARPC 900',b,ov={'arpc_monthly':900})
show('  + ARPC 900, win 0.25',b,ov={'arpc_monthly':900,'proposal_to_win_pct':0.25})
show('  + ARPC 900, win 0.25, churn 2%',b,ov={'arpc_monthly':900,'proposal_to_win_pct':0.25,'monthly_churn_pct':0.02})
show('  + ARPC 1000 (keep price), win .25',b,ov={'proposal_to_win_pct':0.25})
show('corrected-conservative: ARPC 800, win .2, churn 2.5%',b,'conservative')
# ---- WS16-006
w=json.load(open(B+'WS16-006_assumptions.json'))
print("\nWS16-006")
show('original base',w)
show('original conservative',w,'conservative')
show('GM 26/24',w,ov={'gross_margin_pct':0.26,'onetime_gross_margin_pct':0.24})
show('GM 26/24, churn 3%',w,ov={'gross_margin_pct':0.26,'onetime_gross_margin_pct':0.24,'monthly_churn_pct':0.03})
show('GM 26/24, churn 3%, DSO 45',w,ov={'gross_margin_pct':0.26,'onetime_gross_margin_pct':0.24,'monthly_churn_pct':0.03,'dso_days':45})
show('GM 26/24, churn 3%, DSO 45, ARPC 550',w,ov={'gross_margin_pct':0.26,'onetime_gross_margin_pct':0.24,'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':550})
show('GM 28/26, churn 3%, DSO 45, ARPC 550',w,ov={'gross_margin_pct':0.28,'onetime_gross_margin_pct':0.26,'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':550})
show('GM 30/28 (orig) + churn 3%, DSO45, ARPC 550',w,ov={'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':550})
show('corrected + win 0.2',w,ov={'gross_margin_pct':0.26,'onetime_gross_margin_pct':0.24,'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':550,'proposal_to_win_pct':0.2})
show('GM 22/20 conservative-like on base volume',w,ov={'gross_margin_pct':0.22,'onetime_gross_margin_pct':0.20,'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':550})
