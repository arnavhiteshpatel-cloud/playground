const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file:///tmp/claude-0/pdfbuild/atlas.html', {waitUntil:'load'});
  await p.pdf({ path: '/home/user/playground/project-atlas/10_deliverables/Project_Atlas_Findings.pdf', format: 'Letter', printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<div style="font-size:7px;color:#999;width:100%;text-align:right;padding-right:0.7in">Project Atlas — Findings and Recommendation</div>',
    footerTemplate: '<div style="font-size:8px;color:#777;width:100%;text-align:center"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: {top:'0.75in', bottom:'0.8in', left:'0.7in', right:'0.7in'} });
  await b.close();
})();
