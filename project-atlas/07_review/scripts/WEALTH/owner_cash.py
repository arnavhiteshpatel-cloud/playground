import json,sys
sys.path.insert(0,'/home/user/playground/project-atlas/tools'); import fin_engine as E
src=open('/home/user/playground/project-atlas/07_review/cross_model_audit.py').read().split("if __name__")[0]
cma={}; exec(compile(src,'cma','exec'),cma)
FM='/home/user/playground/project-atlas/08_financial_models/'
FDC={"WS12-014":6900,"SYN-006":6200,"SYN-004":6000,"WS04-014":7500}
res={}
for i in FDC:
    a=json.load(open(FM+i+'-REV_assumptions.json'))
    rows={}
    for tag,(s,ov) in {"cons":("conservative",{}),"base":("base",{}),"opt":("optimistic",{}),"harm":("base",cma["harmonized_overrides"](i,a))}.items():
        S=E.run(a,s,ov)["summary"]; lt=S["lt_table"]
        oc=[r["distributable"]+r["owner_comp"] for r in lt]
        f=[12*FDC[i]*1.03**(y) for y in range(10)]
        cum=lambda n: sum(oc[:n]); cumf=lambda n: sum(oc[:n])-sum(f[:n])*(1-0.3)  # FDC after 30% tax shield approx
        rows[tag]=dict(op3=lt[2]["op"],op5=lt[4]["op"],op10=lt[9]["op"],oc3=cum(3),oc5=cum(5),oc10=cum(10),
                       y5_oc=oc[4],y10_oc=oc[9],dep3=lt[2]["cum_deployable_positive"],dep5=lt[4]["cum_deployable_positive"],dep10=lt[9]["cum_deployable_positive"],
                       ev3=lt[2]["ev"],ev5=lt[4]["ev"],ev10=lt[9]["ev"],fdc3=lt[2]["op"]-f[2],fdc5=lt[4]["op"]-f[4],fdc10=lt[9]["op"]-f[9],
                       peak=S["peak_funding_need"])
        r=rows[tag]
        print(f"{i:9s} {tag:4s} op3/5/10 {r['op3']/1e3:7.1f} {r['op5']/1e3:7.1f} {r['op10']/1e3:7.1f} | ownercash cum3/5/10 {r['oc3']/1e3:7.1f} {r['oc5']/1e3:7.1f} {r['oc10']/1e3:8.1f} | y5/y10 per-yr {r['y5_oc']/1e3:6.1f} {r['y10_oc']/1e3:6.1f} | dep3/5/10 {r['dep3']/1e3:6.1f} {r['dep5']/1e3:6.1f} {r['dep10']/1e3:7.1f} | EV3/5/10 {r['ev3']/1e3:6.1f} {r['ev5']/1e3:6.1f} {r['ev10']/1e3:7.1f} | afterFDC op3/5/10 {r['fdc3']/1e3:6.1f} {r['fdc5']/1e3:6.1f} {r['fdc10']/1e3:6.1f}")
    res[i]=rows
json.dump(res,open('owner_cash.json','w'),indent=1)
