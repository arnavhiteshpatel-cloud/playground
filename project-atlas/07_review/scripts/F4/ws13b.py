from ws13 import *
print('-----')
b=mod(a,tech=8700,ins=1000)
C={'arpc_monthly':700,'proposal_to_win_pct':0.30}
R=show('CORR BASE2: ARPC 700, win .30, tech 8.7k, ins 1k',b,ov=C)
S=R['summary']; print({k:round(S[k]) for k in ['y1_op','y2_op','y3_op','y4_op','y5_op','breakeven_month','payback_month','min_cash_balance','lt_y10_cum_deployable','lt_y10_op','y3_revenue','first_month_op_10k']}, [sum(h[m] for h in R['headcount']) for m in (12,24,36,60)])
show(' + churn 6%',b,ov=dict(C,monthly_churn_pct=0.06))
show(' + hire threshold 25 (x1.25)',b,ov=dict(C,staff_threshold_multiplier=1.25))
show(' ARPC 650',b,ov=dict(C,arpc_monthly=650))
show(' ARPC 750',b,ov=dict(C,arpc_monthly=750))
show(' corrected conservative (orig cons + ins 1.4k)',mod(a,tech=8700,ins=1000),'conservative')
# founder-only capped approximation: steady state 20 accounts
for arpc in (550,600,675,750):
  for accts in (15,20):
    rev=accts*arpc*12; gp=rev*0.9-rev*0.05
    oh=(1000+900+300+200+400+633)*12+400*12
    cac=accts*0.05*12*250
    print(f'founder-only steady state accts={accts} ARPC={arpc}: rev={rev:,.0f} op={gp-oh-cac:,.0f}')
