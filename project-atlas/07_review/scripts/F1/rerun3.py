import sys, json, copy
sys.path.insert(0, '/home/user/playground/project-atlas/tools')
import fin_engine as E
B='/home/user/playground/project-atlas/08_financial_models/'
a=json.load(open(B+'SYN-006_assumptions.json'))
def syn(per=15,cost=5800,rev=600):
    b=copy.deepcopy(a)
    for s in b['staff']:
        if s['role'].startswith('Construction bookkeeper'): s['per']=per; s['monthly_cost']={'base':cost,'conservative':cost,'optimistic':cost}
        if s['role'].startswith('External'): s['monthly_cost']={'base':rev,'conservative':rev,'optimistic':rev}
    return b
for tag,b,ov in [('ARPC 950 only',syn(),{'arpc_monthly':950}),('reviewer $1k only',syn(rev=1000),{}),('per 13 only',syn(per=13),{}),('$6.2k only',syn(cost=6200),{}),('all four',syn(13,6200,1000),{'arpc_monthly':950})]:
    S=E.run(b,'base',ov)['summary']; print(f"{tag:22s} y3={S['y3_op']:>9,.0f} y5={S['y5_op']:>9,.0f}")
R=E.run(a,'base'); 
for y in (3,5):
    m=y*12; print('orig yr',y,'clients',round(R['active'][m],1),'headcount by role',[h[m] for h in R['headcount']], 'rev/head incl founder', round(R['summary'][f'y{y}_revenue']/(1+sum(h[m] for h in R['headcount'])))) 
w=json.load(open(B+'WS16-006_assumptions.json'))
for tag,ov in [('WS16 bad debt +1% (var opex 4.5%)',{'variable_opex_pct_revenue':0.045}),('WS16 corrected + bad debt',{'gross_margin_pct':0.27,'onetime_gross_margin_pct':0.25,'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':600,'variable_opex_pct_revenue':0.04})]:
    S=E.run(w,'base',ov)['summary']; print(f"{tag:40s} y3={S['y3_op']:>9,.0f} y5={S['y5_op']:>9,.0f} peak={S['peak_funding_need']:>9,.0f}")
R=E.run(w,'base',{'gross_margin_pct':0.27,'onetime_gross_margin_pct':0.25,'monthly_churn_pct':0.03,'dso_days':45,'arpc_monthly':600})
print('WS16 corrected y3 ending AR', round(R['ar'][36]), 'nwc', round(R['nwc'][36]), 'monthly COGS y3 end', round(R['cogs'][36]), 'retained y1-5',[round(R['summary'][f'y{y}_retained']) for y in range(1,6)])
