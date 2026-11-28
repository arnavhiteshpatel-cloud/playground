import sys, json, copy
sys.path.insert(0, '/home/user/playground/project-atlas/tools')
import fin_engine as E
B='/home/user/playground/project-atlas/08_financial_models/'
def show(tag, a, scen='base', ov=None):
    R=E.run(a, scen, ov or {}); S=R['summary']
    nd=E.run(a,scen,dict(ov or {},founder_draw_per_month=0))
    print(f"{tag:58s} y3op={S['y3_op']:>9,.0f} y5op={S['y5_op']:>9,.0f} y3cust={S['y3_active_end']:5.1f} y5cust={S['y5_active_end']:5.1f} peak={S['peak_funding_need']:>9,.0f} nodraw={-min(0,min(nd['cum_retained'][1:])):>8,.0f}")
    return R
if __name__=='__main__':
    for i in ['WS04-014','WS13-014']:
        a=json.load(open(B+i+'_assumptions.json'))
        for s in ['conservative','base','optimistic']: show(i+' '+s,a,s)
