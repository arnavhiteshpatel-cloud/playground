// OsteoQuant Workbench — dependency-free SPA (ES modules). Talks only to the local API.
import { Viewer } from './viewer.js';

const S = { token: sessionStorage.getItem('oq_token'), me: null, study: null, viewer: null };
const $ = (s, r = document) => r.querySelector(s);
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export async function api(path, opts = {}) {
  const headers = Object.assign({}, opts.headers || {});
  if (S.token) headers['Authorization'] = 'Bearer ' + S.token;
  if (opts.json !== undefined) { headers['Content-Type'] = 'application/json'; opts.body = JSON.stringify(opts.json); }
  const r = await fetch(path, { method: opts.method || (opts.body ? 'POST' : 'GET'), headers, body: opts.body });
  if (r.status === 401 && !path.includes('/auth/')) { logout(); throw new Error('Session expired'); }
  if (!r.ok) { let d = r.statusText; try { d = (await r.json()).detail; } catch (e) {} throw new Error(typeof d === 'string' ? d : JSON.stringify(d)); }
  const ct = r.headers.get('content-type') || '';
  return ct.includes('json') ? r.json() : r;
}
window.oqApi = api;

function show(page) {
  document.querySelectorAll('.page').forEach((p) => (p.hidden = p.id !== page + '-view'));
  if (page === 'jobs') loadJobs();
  if (page === 'audit') loadAudit();
}

async function boot() {
  if (!S.token) { $('#login-view').hidden = false; $('#app').hidden = true; return; }
  try { S.me = await api('/api/me'); } catch (e) { return logout(); }
  $('#login-view').hidden = true; $('#app').hidden = false;
  $('#whoami').textContent = `${S.me.username} · ${S.me.role} · v${S.me.version}`;
  show('studies'); loadStudies();
}
function logout() { if (S.token) api('/api/auth/logout', { method: 'POST' }).catch(() => {}); S.token = null; sessionStorage.removeItem('oq_token'); location.reload(); }

$('#login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  try {
    const r = await api('/api/auth/login', { json: { username: $('#login-user').value, password: $('#login-pass').value } });
    S.token = r.token; sessionStorage.setItem('oq_token', r.token); boot();
  } catch (err) { $('#login-err').textContent = err.message; }
});
$('#logout').onclick = logout;
document.querySelectorAll('[data-nav]').forEach((b) => (b.onclick = () => show(b.dataset.nav)));

// ---------------------------------------------------------------- studies
async function loadStudies() {
  const [studies, projects] = await Promise.all([api('/api/studies'), api('/api/projects')]);
  $('#project-select').innerHTML = projects.map((p) => `<option value="${p.id}">${esc(p.name)}</option>`).join('');
  $('#study-list').innerHTML = studies.map((s) => `<li data-id="${s.id}" class="${S.study === s.id ? 'sel' : ''}">${esc(s.name)}<br><span class="muted">${esc(s.species)} · ${esc(s.defect_model)}${s.blinded ? ' · blinded' : ''}</span></li>`).join('') || '<li class="muted">No studies yet</li>';
  document.querySelectorAll('#study-list li[data-id]').forEach((li) => (li.onclick = () => openStudy(+li.dataset.id)));
  if (S.study) openStudy(S.study);
}
$('#new-project').addEventListener('submit', async (e) => { e.preventDefault(); await api('/api/projects', { json: { name: e.target.name.value } }); e.target.reset(); loadStudies(); });
$('#new-study').addEventListener('submit', async (e) => {
  e.preventDefault(); const f = e.target;
  await api('/api/studies', { json: { project_id: +f.project_id.value, name: f.name.value, species: f.species.value, defect_model: f.defect_model.value, graft_materials: f.graft_materials.value, blinded: f.blinded.checked } });
  f.reset(); loadStudies();
});

async function openStudy(id) {
  S.study = id;
  const d = await api(`/api/studies/${id}`);
  const st = d.study;
  const grp = Object.fromEntries(d.groups.map((g) => [g.id, g.name]));
  const spc = Object.fromEntries(d.specimens.map((s) => [s.id, s]));
  const tp = Object.fromEntries(d.timepoints.map((t) => [t.id, t.label]));
  const results = await api(`/api/studies/${id}/results`).catch(() => []);
  const res = Object.fromEntries(results.map((r) => [r.scan_id, r]));
  const f = (v) => (v === undefined || v === null || Number.isNaN(v) ? '—' : (+v).toFixed(3));
  $('#study-detail').innerHTML = `
    <h2>${esc(st.name)}</h2>
    <p class="muted">${esc(st.species)} · ${esc(st.defect_model)} · graft: ${esc(st.graft_materials)} ${st.blinded ? '· <b>blinded</b> (group names hidden for analysts)' : ''}</p>
    <div class="cols">
      <div class="panel wide"><h3>Groups</h3>${d.groups.map((g) => `<span class="badge">${esc(g.name)}</span>`).join(' ') || '<span class="muted">none</span>'}
        <form id="f-group" class="row"><input name="name" placeholder="Group name" required><button class="small">Add</button></form></div>
      <div class="panel wide"><h3>Timepoints</h3>${d.timepoints.map((t) => `<span class="badge">${esc(t.label)}</span>`).join(' ') || '<span class="muted">none</span>'}
        <form id="f-tp" class="row"><input name="label" placeholder="e.g. week 8" required><input name="days" type="number" placeholder="days"><button class="small">Add</button></form></div>
      <div class="panel wide"><h3>Specimens</h3>${d.specimens.map((s) => `<span class="badge">${esc(s.animal_id)} (${esc(s.group_name || '—')})</span>`).join(' ') || '<span class="muted">none</span>'}
        <form id="f-spec" class="row"><input name="animal_id" placeholder="Animal ID" required><select name="group_id"><option value="">group…</option>${d.groups.map((g) => `<option value="${g.id}">${esc(g.name)}</option>`).join('')}</select><button class="small">Add</button></form></div>
    </div>
    <div class="panel"><h3>Upload reconstructed scan</h3>
      <form id="f-upload" class="row">
        <input type="file" name="file" required style="width:auto">
        <select name="specimen_id"><option value="">specimen…</option>${d.specimens.map((s) => `<option value="${s.id}">${esc(s.animal_id)}</option>`).join('')}</select>
        <select name="timepoint_id"><option value="">timepoint…</option>${d.timepoints.map((t) => `<option value="${t.id}">${esc(t.label)}</option>`).join('')}</select>
        <input name="spacing_um" type="number" step="any" placeholder="voxel µm (if not in file)" style="width:170px">
        <button>Upload &amp; QC</button><span id="up-status" class="muted"></span>
      </form>
      <p class="muted">Accepted: NIfTI, NRRD, (OME-)TIFF, Zeiss TXM, Zarr, or ZIP of a TIFF/DICOM slice folder. Files are hashed (SHA-256); duplicates are rejected.</p>
    </div>
    <div class="panel"><h3>Scans</h3>
      <div class="row">Segmentation: <select id="seg-method" style="width:auto"><option value="multiotsu">multi-Otsu (classical)</option><option value="unet:unet_ctx_s0">U-Net ctx (SYNTHETIC-TRAINED)</option></select>
        Defect model: <select id="defect-model" style="width:auto"><option>condyle</option><option>calvarial</option><option>segmental</option></select>
        Nominal Ø µm <input id="nom-d" type="number" style="width:110px">
        <button id="analyze-all" class="small">Analyze all</button>
        <button id="make-report" class="small">Generate DefectFill report</button><span id="rep-status" class="muted"></span></div>
      <table><tr><th>Scan</th><th>Specimen</th><th>Group</th><th>TP</th><th>Voxel µm</th><th>Status</th><th>New bone BV/TV</th><th>Graft frac</th><th>Uncertain</th><th></th></tr>
      ${d.scans.map((s) => { const r = res[s.id] || {}; const sp = spc[s.specimen_id] || {}; return `<tr>
        <td>${s.id} <span class="muted">${esc(s.source_name)}</span></td><td>${esc(sp.animal_id || '—')}</td><td>${esc(sp.group_name || '—')}</td><td>${esc(tp[s.timepoint_id] || '—')}</td>
        <td>${s.spacing_um.map((v) => (+v).toFixed(1)).join('×')}</td><td><span class="badge ${/fail|unsuitable/.test(s.status) ? 'fail' : /review/.test(s.status) ? 'warn' : /analyzed|suitable/.test(s.status) ? 'ok' : ''}">${esc(s.status)}</span></td>
        <td>${f(r.new_bone_fraction)}</td><td>${f(r.residual_graft_fraction)}</td><td>${f(r.uncertain_fraction)}</td>
        <td><button class="small" data-open="${s.id}">Open viewer</button> <button class="small ghost" data-an="${s.id}">Analyze</button></td></tr>`; }).join('')}
      </table></div>`;
  const post = (url, form, cast = {}) => async (e) => { e.preventDefault(); const o = {}; new FormData(e.target).forEach((v, k) => { if (v !== '') o[k] = cast[k] ? cast[k](v) : v; }); await api(url, { json: o }); openStudy(id); };
  $('#f-group').onsubmit = post(`/api/studies/${id}/groups`, null);
  $('#f-tp').onsubmit = post(`/api/studies/${id}/timepoints`, null, { days: Number });
  $('#f-spec').onsubmit = post(`/api/studies/${id}/specimens`, null, { group_id: Number });
  $('#f-upload').onsubmit = async (e) => {
    e.preventDefault(); const fd = new FormData(e.target); for (const k of [...fd.keys()]) if (fd.get(k) === '') fd.delete(k);
    $('#up-status').textContent = 'uploading…';
    try { const r = await api(`/api/studies/${id}/scans`, { method: 'POST', body: fd }); $('#up-status').textContent = `scan ${r.scan_id} imported; QC job ${r.qc_job}. ${r.warnings.join(' ')}`; await waitJob(r.qc_job); openStudy(id); }
    catch (err) { $('#up-status').textContent = 'Error: ' + err.message; }
  };
  const cfg = () => ({ segmentation: $('#seg-method').value, defect_model: $('#defect-model').value, nominal_diameter_um: +$('#nom-d').value || null });
  document.querySelectorAll('[data-open]').forEach((b) => (b.onclick = () => openViewer(+b.dataset.open)));
  document.querySelectorAll('[data-an]').forEach((b) => (b.onclick = async () => { b.textContent = '…'; const j = await api(`/api/scans/${b.dataset.an}/analyze`, { json: { config: cfg() } }); await waitJob(j.job_id); openStudy(id); }));
  $('#analyze-all').onclick = async () => { for (const s of d.scans) { const j = await api(`/api/scans/${s.id}/analyze`, { json: { config: cfg() } }); await waitJob(j.job_id); } openStudy(id); };
  $('#make-report').onclick = async () => {
    $('#rep-status').textContent = 'building…';
    const j = await api(`/api/studies/${id}/report`, { method: 'POST' }); const res = await waitJob(j.job_id);
    if (res.status === 'done') $('#rep-status').innerHTML = ` <a href="#" id="dl-pdf">PDF</a> · <a href="#" id="dl-csv">CSV</a>`;
    else $('#rep-status').textContent = 'failed: ' + res.message;
    const dl = async (kind) => { const r = await api(`/api/reports/${res.result.report_id}/${kind}`); const b = await r.blob(); const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = `defectfill_${res.result.report_id}.${kind}`; a.click(); };
    if ($('#dl-pdf')) { $('#dl-pdf').onclick = (e) => { e.preventDefault(); dl('pdf'); }; $('#dl-csv').onclick = (e) => { e.preventDefault(); dl('csv'); }; }
  };
  document.querySelectorAll('#study-list li').forEach((li) => li.classList.toggle('sel', +li.dataset.id === id));
}

export async function waitJob(jid) {
  for (;;) { const j = await api(`/api/jobs/${jid}`); if (['done', 'failed', 'cancelled'].includes(j.status)) return j; await new Promise((r) => setTimeout(r, 700)); }
}

// ---------------------------------------------------------------- viewer
async function openViewer(scanId) {
  show('viewer');
  if (!S.viewer) S.viewer = new Viewer(api);
  await S.viewer.open(scanId);
}
$('#back-to-study').onclick = () => { show('studies'); if (S.study) openStudy(S.study); };

// ---------------------------------------------------------------- jobs / audit
async function loadJobs() {
  const jobs = await api('/api/jobs');
  $('#jobs-table').innerHTML = '<tr><th>ID</th><th>Kind</th><th>Status</th><th>Progress</th><th>Message</th><th>Created</th><th></th></tr>' +
    jobs.map((j) => `<tr><td>${j.id}</td><td>${esc(j.kind)}</td><td>${esc(j.status)}</td><td>${Math.round((j.progress || 0) * 100)}%</td><td>${esc(j.message || '')}</td><td>${esc(j.created)}</td><td>${['queued', 'running'].includes(j.status) ? `<button class="small" data-cancel="${j.id}">Cancel</button>` : ''}</td></tr>`).join('');
  document.querySelectorAll('[data-cancel]').forEach((b) => (b.onclick = async () => { await api(`/api/jobs/${b.dataset.cancel}/cancel`, { method: 'POST' }); loadJobs(); }));
}
async function loadAudit() {
  try {
    const ev = await api('/api/audit');
    $('#audit-table').innerHTML = '<tr><th>#</th><th>Time (UTC)</th><th>User</th><th>Action</th><th>Object</th><th>Details</th><th>Hash</th></tr>' +
      ev.map((e) => `<tr><td>${e.seq}</td><td>${esc(e.ts.slice(0, 19))}</td><td>${esc(e.user_id ?? '')}</td><td>${esc(e.action)}</td><td>${esc((e.object_type || '') + ':' + (e.object_id || ''))}</td><td><code>${esc(JSON.stringify(e.details)).slice(0, 160)}</code></td><td><code>${e.row_hash.slice(0, 10)}</code></td></tr>`).join('');
  } catch (e) { $('#audit-table').innerHTML = `<tr><td>${esc(e.message)}</td></tr>`; }
}
$('#verify-chain').onclick = async () => { const r = await api('/api/audit/verify'); $('#chain-status').innerHTML = r.ok ? `<span class="badge ok">intact · ${r.n} events</span>` : `<span class="badge fail">BROKEN at #${r.first_bad_seq}: ${esc(r.reason)}</span>`; };

boot();
