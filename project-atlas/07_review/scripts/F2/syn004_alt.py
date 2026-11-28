import sys, json
sys.path.insert(0,'/tmp/claude-0/atlas_scratch/F2')
from rerun import load, show, E
a=load('SYN-004')
show('base (as filed)', E.run(a,'base'))
runs = {
 'sales_cycle 10 (expiry wait)': {'sales_cycle_months':10},
 'sales_cycle 8': {'sales_cycle_months':8},
 'leads 7': {'founder_leads_per_month':7},
 'win 0.18': {'proposal_to_win_pct':0.18},
 'arpc 800 (DR share ~0, true-ups)': {'arpc_monthly':800},
 'REVIEWER BASE: cycle10 leads7 win.20 arpc800': {'sales_cycle_months':10,'founder_leads_per_month':7,'proposal_to_win_pct':0.20,'arpc_monthly':800},
 'REVIEWER CONS: cycle12 leads5 win.15 arpc650 churn.018': {'sales_cycle_months':12,'founder_leads_per_month':5,'proposal_to_win_pct':0.15,'arpc_monthly':650,'monthly_churn_pct':0.018},
 'REVIEWER UPSIDE: cycle8 leads9 win.22 arpc900': {'sales_cycle_months':8,'founder_leads_per_month':9,'proposal_to_win_pct':0.22,'arpc_monthly':900},
}
out={}
for k,v in runs.items():
    R=E.run(a,'base',v); show(k,R); out[k]={kk:R['summary'][kk] for kk in ['y1_op','y2_op','y3_op','y4_op','y5_op','y3_revenue','y5_active_end','y3_active_end','peak_funding_need','breakeven_month','payback_month']}
    R0=E.run(a,'base',{**v,'founder_draw_per_month':0}); out[k]['peak_no_draw']=R0['summary']['peak_funding_need']
json.dump(out,open('syn004_alt_results.json','w'),indent=1)
for k in out: print(k, 'peak no draw', round(out[k]['peak_no_draw']))
