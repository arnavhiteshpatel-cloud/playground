import sys, json
sys.path.insert(0, '/home/user/playground/project-atlas/tools')
import fin_engine as E
def load(i): return json.load(open(f'/home/user/playground/project-atlas/08_financial_models/{i}_assumptions.json'))
def show(tag, R):
    S=R['summary']
    print(f"{tag:55s} y1 {S['y1_op']:>10,.0f} y2 {S['y2_op']:>10,.0f} y3 {S['y3_op']:>10,.0f} y5 {S['y5_op']:>10,.0f} act5 {S['y5_active_end']:6.1f} peak {S['peak_funding_need']:>9,.0f} BE {S['breakeven_month']} PB {S['payback_month']}")
if __name__=='__main__':
    for i in ['SYN-004','SYN-001']:
        a=load(i)
        for s in ['conservative','base','optimistic']:
            show(f'{i} {s}', E.run(a,s))
