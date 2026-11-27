// Orthogonal-slice viewer with correction tools. Coordinates: pos = [z, y, x] voxel indices.
const COLORS = { 1: [230, 159, 0], 2: [86, 180, 233], 3: [204, 121, 167], 255: [240, 228, 66] };
const PLANE = { 0: { r: 1, c: 2 }, 1: { r: 0, c: 2 }, 2: { r: 0, c: 1 } }; // which volume axes are rows/cols per view
const $ = (s) => document.querySelector(s);
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

async function decodePNG(blob) {
  const bmp = await createImageBitmap(blob);
  const c = new OffscreenCanvas(bmp.width, bmp.height); const g = c.getContext('2d');
  g.drawImage(bmp, 0, 0); const d = g.getImageData(0, 0, bmp.width, bmp.height).data;
  const out = new Uint8Array(bmp.width * bmp.height);
  for (let i = 0; i < out.length; i++) out[i] = d[i * 4];
  return { w: bmp.width, h: bmp.height, a: out };
}

export class Viewer {
  constructor(api) {
    this.api = api; this.tool = 'nav'; this.ops = []; this.measure = []; this.cache = {};
    this.views = [...document.querySelectorAll('.view[data-axis]')].map((el) => ({ el, axis: +el.dataset.axis, canvas: el.querySelector('canvas'), pos: el.querySelector('.vpos') }));
    this.views.forEach((v) => this.bindView(v));
    document.querySelectorAll('[data-tool]').forEach((b) => (b.onclick = () => { this.tool = b.dataset.tool; document.querySelectorAll('[data-tool]').forEach((x) => x.classList.toggle('active', x === b)); this.measure = []; }));
    ['#wl-lo', '#wl-hi', '#opacity', '#show-seg', '#show-unc', '#show-roi'].forEach((s) => ($(s).oninput = () => this.renderAll(s.startsWith('#wl'))));
    $('#seg-select').onchange = () => { this.ops = []; this.updatePending(); this.renderAll(); };
    $('#cmp-select').onchange = () => this.renderAll();
    document.querySelectorAll('[data-preset]').forEach((b) => (b.onclick = () => this.preset(b.dataset.preset)));
    $('#undo').onclick = () => { this.ops.pop(); this.cache = {}; this.updatePending(); this.renderAll(); };
    $('#save-edits').onclick = () => this.saveEdits();
    $('#rev-submit').onclick = () => this.sign();
    $('#mesh-btn').onclick = () => this.render3D();
    window.addEventListener('resize', () => this.renderAll(false));
  }

  async open(scanId) {
    this.scanId = scanId; this.cache = {}; this.ops = []; this.measure = [];
    const info = await this.api(`/api/scans/${scanId}`); this.info = info;
    this.shape = info.shape; this.sp = info.spacing_um;
    this.pos = this.shape.map((n) => Math.floor(n / 2));
    if (info.roi && info.roi.definition && info.roi.definition.params && info.roi.definition.params.center_um) {
      const c = info.roi.definition.params.center_um; const e = info.roi.definition.params.extent_um;
      this.pos = [Math.round(((e[0] + e[1]) / 2) / this.sp[0]), Math.round(c[1] / this.sp[1]), Math.round(c[2] / this.sp[2])].map((v, i) => Math.max(0, Math.min(this.shape[i] - 1, v)));
    }
    this.win = { min: info.window.min, max: info.window.max };
    this.preset('auto', false);
    $('#scan-title').textContent = `Scan ${scanId} — ${info.source_name}`;
    $('#scan-meta').textContent = `${info.shape.join('×')} voxels · ${info.spacing_um.map((v) => (+v).toFixed(2)).join('×')} µm · ${info.format} · SHA-256 ${String(info.file_sha256).slice(0, 12)}… · QC: ${info.qc ? info.qc.verdict : 'pending'}`;
    const segs = info.segmentations;
    const opts = segs.slice().reverse().map((s) => `<option value="${s.version}" data-key="${s.labels_key}">v${s.version} · ${s.kind} · ${esc(s.method)}${s.model_name ? ' · ' + esc(s.model_name) : ''}</option>`).join('');
    $('#seg-select').innerHTML = opts || '<option value="">(no segmentation — run analysis)</option>';
    $('#cmp-select').innerHTML = '<option value="">— (difference overlay off)</option>' + opts;
    this.renderHistory(); this.renderMetrics(); this.updatePending();
    this.renderAll();
  }

  segKey(sel = '#seg-select') { const o = $(sel).selectedOptions[0]; return o && o.dataset.key ? o.dataset.key : null; }
  segVersion() { return +$('#seg-select').value; }

  preset(p, render = true) {
    const w = this.info.window; const span = this.win.max - this.win.min || 1;
    const to = (v) => Math.round(((v - this.win.min) / span) * 1000);
    if (p === 'auto') { $('#wl-lo').value = to(w.p1); $('#wl-hi').value = to(w.p99); }
    if (p === 'bone') { $('#wl-lo').value = to(w.p1 + 0.35 * (w.p99 - w.p1)); $('#wl-hi').value = to(w.p99); }
    if (p === 'full') { $('#wl-lo').value = 0; $('#wl-hi').value = 1000; }
    if (render) this.renderAll(true);
  }
  wl() { const span = this.win.max - this.win.min; return [this.win.min + (+$('#wl-lo').value / 1000) * span, this.win.min + (+$('#wl-hi').value / 1000) * span]; }

  async slice(axis, index, layer, imageKey = '') {
    const k = `${axis}/${index}/${layer}/${imageKey}`;
    if (this.cache[k]) return this.cache[k];
    let url = `/api/scans/${this.scanId}/slice?axis=${axis}&index=${index}&layer=${encodeURIComponent(layer)}`;
    if (layer === 'image') { const [lo, hi] = this.wl(); url += `&lo=${lo}&hi=${hi}`; }
    const r = await this.api(url); const d = await decodePNG(await r.blob());
    if (!layer.startsWith('labels/seg_') || layer !== `labels/${this.segKey()}`) { this.cache[k] = d; return d; }
    // apply pending local edits for display
    this.applyOpsLocal(d, axis, index); this.cache[k] = d; return d;
  }

  applyOpsLocal(d, axis, index) {
    for (const op of this.ops) {
      if (op.axis !== axis || op.index !== index) continue;
      if (op.op === 'brush') {
        for (let y = Math.max(0, Math.floor(op.cy - op.r)); y <= Math.min(d.h - 1, Math.ceil(op.cy + op.r)); y++)
          for (let x = Math.max(0, Math.floor(op.cx - op.r)); x <= Math.min(d.w - 1, Math.ceil(op.cx + op.r)); x++)
            if ((y - op.cy) ** 2 + (x - op.cx) ** 2 <= op.r ** 2) { const i = y * d.w + x; if (op.only_from === null || d.a[i] === op.only_from) d.a[i] = op.label; }
      } else if (op.op === 'fill_component') {
        const y0 = Math.round(op.cy), x0 = Math.round(op.cx); const src = d.a[y0 * d.w + x0]; const st = [[y0, x0]]; const seen = new Uint8Array(d.a.length);
        if (op.only_from !== null && src !== op.only_from) continue;
        while (st.length) { const [y, x] = st.pop(); if (y < 0 || x < 0 || y >= d.h || x >= d.w) continue; const i = y * d.w + x; if (seen[i] || d.a[i] !== src) continue; seen[i] = 1; d.a[i] = op.label; st.push([y + 1, x], [y - 1, x], [y, x + 1], [y, x - 1]); }
      }
    }
  }

  renderAll(imageChanged = false) {
    if (!this.info) return;
    if (imageChanged) for (const k of Object.keys(this.cache)) if (k.includes('/image/')) delete this.cache[k];
    this.views.forEach((v) => this.render(v));
  }

  geom(v, w, h) {
    const P = PLANE[v.axis]; const rs = this.sp[P.r], cs = this.sp[P.c];
    const physW = w * cs, physH = h * rs; const cw = v.canvas.clientWidth, ch = v.canvas.clientHeight;
    const scale = Math.min(cw / physW, ch / physH); const dw = physW * scale, dh = physH * scale;
    return { ox: (cw - dw) / 2, oy: (ch - dh) / 2, sx: dw / w, sy: dh / h, cw, ch, umPerPx: 1 / scale };
  }

  async render(v) {
    const axis = v.axis, idx = this.pos[axis];
    const token = (v.token = (v.token || 0) + 1);
    const img = await this.slice(axis, idx, 'image', $('#wl-lo').value + '_' + $('#wl-hi').value);
    const key = this.segKey(); const cmp = this.segKey('#cmp-select');
    const lab = key && $('#show-seg').checked ? await this.slice(axis, idx, `labels/${key}`) : null;
    const lab2 = cmp && lab ? await this.slice(axis, idx, `labels/${cmp}`) : null;
    const uncKey = key ? key.replace('seg_', 'unc_') : null;
    const unc = uncKey && $('#show-unc').checked && this.info.layers.includes(uncKey) ? await this.slice(axis, idx, `labels/${uncKey}`) : null;
    const roi = $('#show-roi').checked && this.info.layers.includes('roi_current') ? await this.slice(axis, idx, 'labels/roi_current') : null;
    if (token !== v.token) return;
    const { w, h } = img; const off = new OffscreenCanvas(w, h); const g = off.getContext('2d'); const id = g.createImageData(w, h);
    const al = +$('#opacity').value / 100;
    for (let i = 0; i < w * h; i++) {
      let r = img.a[i], gg = img.a[i], b = img.a[i];
      if (lab) { const L = lab.a[i]; const c = COLORS[L]; if (c) { r = (1 - al) * r + al * c[0]; gg = (1 - al) * gg + al * c[1]; b = (1 - al) * b + al * c[2]; } }
      if (lab2 && lab2.a[i] !== lab.a[i]) { r = 255; gg = 0; b = 255; }
      if (unc) { const u = unc.a[i] / 255; r = (1 - u) * r + u * 255; gg = (1 - u) * gg; b = (1 - u) * b; }
      if (roi && roi.a[i] && ((i % w > 0 && !roi.a[i - 1]) || (i % w < w - 1 && !roi.a[i + 1]) || (i >= w && !roi.a[i - w]) || (i < w * (h - 1) && !roi.a[i + w]))) { r = 255; gg = 255; b = 255; }
      const j = i * 4; id.data[j] = r; id.data[j + 1] = gg; id.data[j + 2] = b; id.data[j + 3] = 255;
    }
    g.putImageData(id, 0, 0);
    const c = v.canvas; const dpr = window.devicePixelRatio || 1;
    c.width = c.clientWidth * dpr; c.height = c.clientHeight * dpr;
    const ctx = c.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.imageSmoothingEnabled = false;
    ctx.fillStyle = '#0b0d10'; ctx.fillRect(0, 0, c.clientWidth, c.clientHeight);
    const G = this.geom(v, w, h); v.G = G; v.dim = { w, h };
    ctx.drawImage(off, G.ox, G.oy, w * G.sx, h * G.sy);
    // crosshair
    const P = PLANE[axis]; const cx = G.ox + (this.pos[P.c] + 0.5) * G.sx, cy = G.oy + (this.pos[P.r] + 0.5) * G.sy;
    ctx.strokeStyle = 'rgba(0,255,170,.55)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(cx, G.oy); ctx.lineTo(cx, G.oy + h * G.sy); ctx.moveTo(G.ox, cy); ctx.lineTo(G.ox + w * G.sx, cy); ctx.stroke();
    // scale bar
    const targetPx = 80; const um = G.umPerPx * targetPx; const nice = [50, 100, 200, 500, 1000, 2000, 5000, 10000].find((n) => n >= um * 0.5) || 10000;
    const px = nice / G.umPerPx; ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(12, G.ch - 22); ctx.lineTo(12 + px, G.ch - 22); ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = '11px sans-serif'; ctx.fillText(nice >= 1000 ? `${nice / 1000} mm` : `${nice} µm`, 12, G.ch - 28);
    // measurement
    if (this.measure.length && this.measure[0].axis === axis && this.measure[0].index === idx) {
      ctx.strokeStyle = '#ffd400'; ctx.lineWidth = 2; ctx.beginPath();
      this.measure.forEach((m, k) => { const X = G.ox + (m.c + 0.5) * G.sx, Y = G.oy + (m.r + 0.5) * G.sy; k ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y); ctx.fillRect(X - 2, Y - 2, 4, 4); });
      ctx.stroke();
    }
    v.pos.textContent = `slice ${idx + 1}/${this.shape[axis]} · (z,y,x)=(${this.pos.join(', ')})`;
  }

  toVoxel(v, ev) {
    const r = v.canvas.getBoundingClientRect(); const G = v.G; if (!G) return null;
    const c = (ev.clientX - r.left - G.ox) / G.sx - 0.5, rr = (ev.clientY - r.top - G.oy) / G.sy - 0.5;
    if (c < -0.5 || rr < -0.5 || c > v.dim.w - 0.5 || rr > v.dim.h - 0.5) return null;
    return { r: rr, c };
  }

  bindView(v) {
    let down = false;
    const act = (ev, first) => {
      const p = this.toVoxel(v, ev); if (!p) return;
      const P = PLANE[v.axis];
      if (this.tool === 'nav') { this.pos[P.r] = Math.round(p.r); this.pos[P.c] = Math.round(p.c); this.renderAll(); }
      else if (this.tool === 'brush' || (this.tool === 'fill' && first)) {
        if (!this.segKey()) return alert('No segmentation to edit — run analysis first.');
        const from = $('#paint-from').value;
        this.ops.push({ op: this.tool === 'brush' ? 'brush' : 'fill_component', axis: v.axis, index: this.pos[v.axis], cy: p.r, cx: p.c, r: +$('#brush-r').value, label: +$('#paint-label').value, only_from: from === '' ? null : +from });
        for (const k of Object.keys(this.cache)) if (k.includes('/labels/seg_')) delete this.cache[k];
        this.updatePending(); this.render(v);
      } else if (this.tool === 'measure' && first) {
        if (this.measure.length >= 2 || (this.measure[0] && this.measure[0].axis !== v.axis)) this.measure = [];
        this.measure.push({ axis: v.axis, index: this.pos[v.axis], r: p.r, c: p.c });
        if (this.measure.length === 2) {
          const [a, b] = this.measure; const d = Math.hypot((a.r - b.r) * this.sp[P.r], (a.c - b.c) * this.sp[P.c]);
          $('#measure-out').textContent = `Distance: ${(d / 1000).toFixed(3)} mm (${d.toFixed(0)} µm) in ${['axial', 'coronal', 'sagittal'][v.axis]} plane`;
        }
        this.render(v);
      }
    };
    v.canvas.addEventListener('pointerdown', (e) => { down = true; act(e, true); });
    v.canvas.addEventListener('pointermove', (e) => { if (down && (this.tool === 'nav' || this.tool === 'brush')) act(e, false); });
    window.addEventListener('pointerup', () => (down = false));
    v.canvas.addEventListener('wheel', (e) => { e.preventDefault(); this.pos[v.axis] = Math.max(0, Math.min(this.shape[v.axis] - 1, this.pos[v.axis] + Math.sign(e.deltaY))); this.renderAll(); }, { passive: false });
  }

  updatePending() { $('#pending').textContent = `${this.ops.length} pending edit${this.ops.length === 1 ? '' : 's'}`; }

  async saveEdits() {
    if (!this.ops.length) return alert('No pending edits');
    const reason = $('#edit-reason').value.trim(); if (reason.length < 3) return alert('Please give a reason for the correction (it is recorded in the audit trail).');
    try {
      const r = await this.api(`/api/scans/${this.scanId}/segmentations/edits`, { json: { base_version: this.segVersion(), ops: this.ops, reason } });
      alert(`Saved as version ${r.version}. Voxel changes: ${JSON.stringify(r.voxel_count_change)}`);
      await this.open(this.scanId);
    } catch (e) { alert('Save failed: ' + e.message); }
  }

  async sign() {
    const segs = this.info.segmentations; const s = segs.find((x) => x.version === this.segVersion()); if (!s) return;
    try {
      await this.api('/api/reviews', { json: { object_type: 'segmentation', object_id: s.id, decision: $('#rev-decision').value, meaning: $('#rev-meaning').value, password: $('#rev-pass').value } });
      $('#rev-pass').value = ''; alert('Signature recorded in audit trail.'); this.renderHistory();
    } catch (e) { alert('Signing failed: ' + e.message); }
  }

  async renderHistory() {
    const segs = this.info.segmentations; const rois = this.info.roi_history || [];
    $('#history').innerHTML = segs.slice().reverse().map((s) => `<div><b>seg v${s.version}</b> ${esc(s.kind)} · ${esc(s.created)}<br>${esc(s.method)} ${s.model_sha256 ? '· model ' + esc(s.model_sha256.slice(0, 10)) : ''}${s.edits && s.edits.reason ? '<br>reason: ' + esc(s.edits.reason) : ''}${s.edits && s.edits.voxel_count_change ? '<br>Δvoxels ' + esc(JSON.stringify(s.edits.voxel_count_change)) : ''}</div>`).join('') +
      rois.map((r) => `<div><b>ROI v${r.version}</b> ${esc(r.method)} · conf ${r.confidence == null ? '—' : (+r.confidence).toFixed(2)} · ${esc(r.created)}<br>${esc(r.reason || '')}</div>`).join('');
  }

  async renderMetrics() {
    const res = await this.api(`/api/studies/${this.info.study_id}/results`).catch(() => []);
    const r = res.find((x) => x.scan_id === this.scanId);
    const f = (v) => (v === undefined || v === null ? '—' : (+v).toFixed(4));
    $('#scan-metrics').innerHTML = r ? `<table><tr><td>TV</td><td>${f(r.TV_mm3)} mm³</td></tr><tr><td>New bone</td><td>${f(r.new_bone_volume_mm3)} mm³ (${f(r.new_bone_fraction)})</td></tr>
      <tr><td>Residual graft</td><td>${f(r.residual_graft_volume_mm3)} mm³ (${f(r.residual_graft_fraction)})</td></tr><tr><td>Uncertain</td><td>${f(r.uncertain_fraction)}</td></tr></table>
      <p class="muted">Latest measurement for segmentation ${r.segmentation_id}. Unreviewed until signed.</p>` : '<p class="muted">No analysis yet.</p>';
  }

  async render3D() {
    const key = this.segKey(); if (!key) return alert('No segmentation');
    const THREE = await import('./vendor/three.module.min.js'); const { OrbitControls } = await import('./vendor/OrbitControls.js');
    const L = +$('#mesh-label').value; const m = await this.api(`/api/scans/${this.scanId}/mesh?layer=labels/${key}&label=${L}&step=2`);
    const canvas = $('#c3d');
    if (!this.three) {
      const renderer = new THREE.WebGLRenderer({ canvas, antialias: true }); const scene = new THREE.Scene(); scene.background = new THREE.Color(0x0b0d10);
      const cam = new THREE.PerspectiveCamera(40, 1, 0.01, 1000); const ctl = new OrbitControls(cam, canvas);
      scene.add(new THREE.HemisphereLight(0xffffff, 0x333344, 1.1)); const dl = new THREE.DirectionalLight(0xffffff, 0.8); dl.position.set(1, 2, 3); scene.add(dl);
      this.three = { THREE, renderer, scene, cam, ctl, mesh: null };
      const loop = () => { const t = this.three; const w = canvas.clientWidth, h = canvas.clientHeight; if (canvas.width !== w || canvas.height !== h) { t.renderer.setSize(w, h, false); t.cam.aspect = w / h; t.cam.updateProjectionMatrix(); } t.ctl.update(); t.renderer.render(t.scene, t.cam); requestAnimationFrame(loop); };
      loop();
    }
    const t = this.three;
    if (t.mesh) { t.scene.remove(t.mesh); t.mesh.geometry.dispose(); }
    if (!m.vertices.length) return alert('No voxels of that class');
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(m.vertices, 3)); geo.setIndex(m.faces); geo.computeVertexNormals(); geo.center();
    const col = COLORS[L]; t.mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: new THREE.Color(col[0] / 255, col[1] / 255, col[2] / 255), roughness: 0.6, side: THREE.DoubleSide }));
    t.scene.add(t.mesh); geo.computeBoundingSphere(); const R = geo.boundingSphere.radius; t.cam.position.set(R * 1.8, R * 1.4, R * 2.2); t.ctl.target.set(0, 0, 0);
    let obj = '# OsteoQuant surface (mm)\n'; for (let i = 0; i < m.vertices.length; i += 3) obj += `v ${m.vertices[i]} ${m.vertices[i + 1]} ${m.vertices[i + 2]}\n`;
    for (let i = 0; i < m.faces.length; i += 3) obj += `f ${m.faces[i] + 1} ${m.faces[i + 1] + 1} ${m.faces[i + 2] + 1}\n`;
    $('#mesh-export').href = URL.createObjectURL(new Blob([obj], { type: 'text/plain' }));
  }
}
