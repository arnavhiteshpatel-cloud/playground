import sys, json
sys.path.insert(0,'/tmp/claude-0/atlas_scratch/F2')
from rerun import load, show, E
a=load('SYN-001')
def attach(age_m, path):
    return path[min(age_m//12, len(path)-1)]
def corrected(scen='base', ov=None, ins_per_insured=360.0, path=(0.05,0.14,0.21,0.25,0.28), comp=287.5, label=''):
    ov=ov or {}
    R=E.run(a,scen,ov); d=R['drivers']; c=d['monthly_churn_pct']*d['churn_multiplier']
    M=60; new=R['new']; cohorts=[0.0]*(M+1)
    rev_corr=[0.0]*(M+1); ins_share=[0.0]*(M+1)
    for m in range(1,M+1):
        yr=(m-1)//12+1
        for j in range(1,m): cohorts[j]*= (1-c)
        cohorts[m]=new[m]
        act=sum(cohorts[1:m+1])
        ins=sum(cohorts[j]*attach(m-j,path) for j in range(1,m+1))
        ins_share[m]=ins/act if act else 0
        rev_corr[m]=act*comp*1.03**(yr-1) + ins*ins_per_insured*1.03**(yr-1)
    # delta on recurring revenue; insurance margin ~ (0.97 - var opex)
    gm_ins=0.97-d['variable_opex_pct_revenue']
    out={}
    for y in range(1,6):
        rm=sum(R['rev_rec'][(y-1)*12+1:y*12+1]); rc=sum(rev_corr[(y-1)*12+1:y*12+1])
        dop=(rc-rm)*gm_ins
        out[y]=dict(model_rec=rm, corr_rec=rc, model_op=R['summary'][f'y{y}_op'], corr_op=R['summary'][f'y{y}_op']+dop,
                    attach_end=ins_share[y*12], active_end=R['summary'][f'y{y}_active_end'])
    # corrected peak funding: recompute cumulative retained with delta op (ignoring tax effects; conservative small)
    cum=0; peak=0; cumtax=0
    for m in range(1,M+1):
        dop=(rev_corr[m]-R['rev_rec'][m])*gm_ins
        cum+=R['retained'][m]+dop
        peak=min(peak,cum)
    print(f"{label:48s}", ' '.join(f"y{y}: op {out[y]['corr_op']:>9,.0f} (model {out[y]['model_op']:>9,.0f}) att {out[y]['attach_end']:.2f}" for y in (1,3,5)), f"peak~{-peak:,.0f} act5 {out[5]['active_end']:.0f}")
    return out, -peak
res={}
res['base_cohort']=corrected(label='Base, cohort-correct attach')
res['base_cohort_split40']=corrected(ins_per_insured=288, label='Base, cohort attach + 40% split')
res['base_cohort_split40_lowattach']=corrected(ins_per_insured=288, path=(0.03,0.09,0.14,0.17,0.19), label='+ attach path 2/3 of filed')
res['rev_base']=corrected(ov={'founder_leads_per_month':15,'proposal_to_win_pct':0.22,'monthly_churn_pct':0.018}, ins_per_insured=288, path=(0.03,0.09,0.14,0.17,0.19), label='REVIEWER BASE (leads15 win.22 churn1.8%)')
res['rev_cons']=corrected(ov={'founder_leads_per_month':12,'proposal_to_win_pct':0.18,'monthly_churn_pct':0.022}, ins_per_insured=288, path=(0.02,0.06,0.09,0.11,0.12), label='REVIEWER CONS')
json.dump({k:{'years':v[0],'peak':v[1]} for k,v in res.items()}, open('syn001_cohort_results.json','w'), indent=1, default=float)

print('--- no-draw peaks')
a['drivers']['founder_draw_per_month']=0
corrected(ins_per_insured=288, label='NO DRAW: cohort + 40% split')
corrected(label='NO DRAW: cohort only')
