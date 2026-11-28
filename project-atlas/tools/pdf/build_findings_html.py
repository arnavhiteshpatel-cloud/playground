import markdown, re, pathlib, html, json
A = pathlib.Path('/home/user/playground/project-atlas')
parts = [
 ("Executive Decision Memo", "10_deliverables/EXECUTIVE_DECISION_MEMO.md"),
 ("Master Research Report", "10_deliverables/MASTER_RESEARCH_REPORT.md"),
 ("Opportunity Landscape and Rejections (630 ideas)", "10_deliverables/sections/LANDSCAPE_AND_REJECTIONS.md"),
 ("Independent Review Report", "10_deliverables/INDEPENDENT_REVIEW_REPORT.md"),
 ("Capital Allocation Report", "10_deliverables/CAPITAL_ALLOCATION_REPORT.md"),
 ("Long-Term Wealth Creation Report", "10_deliverables/LONG_TERM_WEALTH_REPORT.md"),
 ("Cross-Finalist Model Audit", "07_review/CROSS_MODEL_AUDIT.md"),
 ("Playbook — Primary: Controls & Automation Engineering Recruiting Desk", "06_playbooks/WS12-014_playbook.md"),
 ("Adversarial Review — Recruiting Desk", "07_review/WS12-014_review.md"),
 ("Playbook — Alternative 1: Construction Subcontractor Back Office", "06_playbooks/SYN-006_playbook.md"),
 ("Adversarial Review — Construction Back Office", "07_review/SYN-006_review.md"),
 ("Playbook — Alternative 2: Large-Customer Energy Cost Management", "06_playbooks/SYN-004_playbook.md"),
 ("Adversarial Review — Energy Cost Management", "07_review/SYN-004_review.md"),
 ("Research Methodology, Scoring Framework and Evidence Standards", ["00_governance/METHODOLOGY.md","00_governance/SCORING_FRAMEWORK.md","00_governance/EVIDENCE_STANDARDS.md","00_governance/RESEARCH_LIMITATIONS.md"]),
]
fs = json.loads((A/'03_screening/final_status.json').read_text())
fin_rows = "".join(f"<tr><td>{k}</td><td><b>{html.escape(v['status'])}</b></td><td>{html.escape(v['concept'])}</td><td>{html.escape(v['post_review_y3_y5_op'])}</td><td>{html.escape(v['peak_funding'])}</td><td>{html.escape(v['decisive_test'])}</td></tr>" for k,v in fs.items())
md = markdown.Markdown(extensions=['tables','fenced_code','sane_lists'])
body=[]; toc=[]
for i,(title,src) in enumerate(parts,1):
    srcs = src if isinstance(src,list) else [src]
    text = "\n\n".join((A/s).read_text(encoding='utf-8') for s in srcs)
    out=[]; prev=''
    for line in text.split('\n'):
        m=re.match(r'^( *)([-*+]|\d+\.) ', line)
        if m:
            ind=len(m.group(1)); line=' '*(ind*2)+line.lstrip(' ')   # 2-space nesting -> 4-space
            pm=re.match(r'^( *)([-*+]|\d+\.) ', prev)
            if prev.strip() and not pm and not prev.lstrip().startswith('|'):
                out.append('')
        out.append(line); prev=line
    text='\n'.join(out)
    # break very long table-free lines? no. Convert
    h = md.reset().convert(text)
    h = re.sub(r'<h([1-6])>', lambda m: f'<h{min(6,int(m.group(1))+1)}>', h)
    h = re.sub(r'</h([1-6])>', lambda m: f'</h{min(6,int(m.group(1))+1)}>', h)
    toc.append(f'<li><a href="#part{i}">Part {i}. {html.escape(title)}</a></li>')
    body.append(f'<section class="part" id="part{i}"><div class="parthead">Part {i}</div><h1>{html.escape(title)}</h1>{h}</section>')
css = """
@page { size: Letter; margin: 0.75in 0.7in 0.8in 0.7in; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 9.6pt; line-height: 1.42; color:#1a1a1a; }
h1 { font-size: 20pt; color:#1F3864; margin: 4pt 0 14pt; border-bottom: 2px solid #1F3864; padding-bottom:6pt;}
h2 { font-size: 14.5pt; color:#1F3864; margin-top:18pt; } h3 { font-size: 12pt; color:#2E4A7D; margin-top:14pt;}
h4,h5,h6 { font-size: 10.5pt; color:#333; }
h2,h3,h4 { page-break-after: avoid; }
.part { page-break-before: always; } .parthead { color:#888; font-size:10pt; letter-spacing:2px; text-transform:uppercase; margin-top:0;}
table { border-collapse: collapse; width:100%; margin: 8pt 0; font-size: 8pt; page-break-inside:auto;}
tr { page-break-inside: avoid; }
table.score { table-layout: fixed; } table.score td { overflow-wrap: normal; word-break: normal; }
th { background:#1F3864; color:#fff; text-align:left; padding:3pt 4pt; }
td:first-child { min-width: 58px; } table { table-layout:auto; } td, th { overflow-wrap:anywhere; }
td { border:1px solid #ccc; padding:3pt 4pt; vertical-align:top; word-break: break-word;}
tr:nth-child(even) td { background:#f5f7fb; }
code { font-size: 8.3pt; background:#f1f1f1; padding:0 2px; word-break: break-all;}
pre { background:#f4f4f4; padding:6pt; font-size:7.8pt; white-space:pre-wrap; }
blockquote { border-left:3px solid #1F3864; margin-left:0; padding-left:10pt; color:#444;}
.cover { height: 9in; display:flex; flex-direction:column; justify-content:center; }
.cover h1 { font-size: 34pt; border:none; } .cover .sub { font-size:14pt; color:#444; }
.box { border:2px solid #1F3864; padding:10pt 14pt; margin:14pt 0; background:#f5f7fb;}
.toc li { margin: 4pt 0; font-size: 11pt; } a { color:#1F3864; text-decoration:none; }
"""
cover = f"""<div class="cover"><div class="parthead">Project Atlas</div><h1>Project Atlas<br>Findings and Recommendation</h1>
<div class="sub">Evidence-driven search for the strongest from-scratch first operating company<br>Illinois · 28 November 2026</div>
<div class="box"><b>Recommendation.</b> Start an employer-paid contingency recruiting desk placing controls, automation and I&amp;C engineers with
Illinois integrators, plants and engineering firms — run as a 2–3-year cash engine with a month-24 boutique-or-harvest decision — but only after a
60-day, ≈$600 test: ≥5 of 30 hiring managers sign an 18–20% fee agreement.<br><br>
<b>Alternatives.</b> (1) Construction subcontractor back office (surety-grade WIP bookkeeping + Illinois certified payroll) — the durable-asset choice.
(2) Energy cost management for &gt;1,500 kW Illinois commercial users (statutory broker-licence exemption) — the high-upside choice.<br><br>
<b>Headline.</b> No from-scratch option shows credible evidence of $500k–$1M/yr owner cash within five years; the wealth path is a sequence —
cheap cash engine → deployable capital → durable, delegable assets. Most of the $100k backing should stay uncommitted.</div>
<p style="color:#666;font-size:9pt">Desk research only: no supplier or customer has been contacted, nothing has been purchased or submitted. Evidence levels:
A direct · B strong documentation · C industry · D proxy · E assumption. Source IDs in brackets refer to the project's evidence database
(1,618 sources). Editable models, databases and all 630 records are in the <code>project-atlas</code> folder.</p></div>"""
summary = f"""<section class="part"><div class="parthead">At a glance</div><h1>Contents and finalist scorecard</h1>
<ol class="toc">{''.join(toc)}</ol>
<h2>Research funnel</h2><p>18 discovery workstreams → 630 opportunity records (all blind re-scored) → 74 industry investigations → 25 commercial deep dives with
named Illinois prospects, suppliers and verified financial models → 11 finalist playbooks → 6 independent adversarial reviews + cross-model audit → 1 primary, 2 alternatives, 1 reserve.</p>
<h2>Final status of the 11 finalists (post-review)</h2>
<table class="score"><colgroup><col style="width:9%"><col style="width:13%"><col style="width:24%"><col style="width:12%"><col style="width:11%"><col style="width:31%"></colgroup><tr><th>ID</th><th>Status</th><th>Concept</th><th>Base Y3 / Y5 operating profit</th><th>Peak funding</th><th>Decisive validation test</th></tr>{fin_rows}</table>
<p style="font-size:8.5pt;color:#555">Operating profit is before owner compensation; peak funding includes a standardized $4,000/month owner draw from month 13 unless noted.</p></section>"""
doc = f"<!doctype html><html><head><meta charset='utf-8'><title>Project Atlas — Findings</title><style>{css}</style></head><body>{cover}{summary}{''.join(body)}</body></html>"
pathlib.Path('/tmp/claude-0/pdfbuild/atlas.html').write_text(doc, encoding='utf-8')
print(len(doc))
