// ═══════════════════════════════════════════════════════
// Tab 9: Impostazioni (Tag management, Import/Export, Stats)
// Card-based UI with per-group inline add
// ═══════════════════════════════════════════════════════

function renderImpostazioni() {
  const container = document.getElementById('impostazioni-content');

  const groups = [
    { color: 'red', label: 'Negativi', desc: 'Cause di problemi nei progetti' },
    { color: 'green', label: 'Positivi', desc: 'Fattori di successo' },
    { color: 'neutral', label: 'Tipologia', desc: 'Classificazione del progetto' }
  ];

  let html = '<h3 class="section-title">Gestione Tag</h3>';

  groups.forEach(g => {
    const c = TAG_COLORS[g.color];
    const tags = getTagDefinitions(g.color);
    html += `
      <div class="tag-group-card" style="border-left:4px solid ${c.bg};background:${c.bgLight};border-radius:6px;padding:14px;margin-bottom:12px">
        <div style="font-weight:600;font-size:0.85rem;margin-bottom:8px">${g.label} <span style="font-weight:400;font-size:0.75rem;color:var(--muted)">— ${g.desc}</span></div>
        <div class="settings-tag-list" data-color="${g.color}">
          ${tags.map(t => {
            return `<span class="tag-pill" style="background:${c.bg};color:${c.text}">${t.label} <span class="tag-remove" data-tag-id="${t.id}" title="Rimuovi">&times;</span></span>`;
          }).join(' ')}
        </div>
        <div style="display:flex;gap:6px;align-items:center;margin-top:8px">
          <input type="text" class="add-tag-input" data-color="${g.color}" placeholder="Nuovo tag ${g.label.toLowerCase()}..." style="padding:5px 8px;border:1px solid var(--border);border-radius:4px;font-size:0.8rem;flex:1;max-width:200px">
          <button class="btn btn-sm add-tag-btn" data-color="${g.color}">+</button>
        </div>
      </div>
    `;
  });

  // Import/Export
  html += `
    <h3 class="section-title" style="margin-top:20px">Import / Export</h3>
    <div style="display:flex;gap:10px;align-items:center;margin-bottom:20px">
      <button class="btn btn-sm" id="settings-export">Esporta dati</button>
      <label class="btn btn-sm" style="cursor:pointer">
        Importa dati
        <input type="file" accept=".json" id="settings-import" style="display:none">
      </label>
    </div>
  `;

  // Statistics
  html += `
    <h3 class="section-title">Statistiche Tag</h3>
    <div class="card"><div class="table-scroll"><table id="settings-stats-table"><thead><tr></tr></thead><tbody></tbody></table></div></div>
  `;

  container.innerHTML = html;

  // Wire remove buttons
  container.querySelectorAll('.tag-remove').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const tagId = btn.dataset.tagId;
      const def = getTagDef(tagId);
      if (def && confirm(`Rimuovere il tag "${def.label}"?`)) {
        removeTagDefinition(tagId);
        renderImpostazioni();
      }
    });
  });

  // Wire add buttons
  container.querySelectorAll('.add-tag-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const color = btn.dataset.color;
      const input = container.querySelector(`.add-tag-input[data-color="${color}"]`);
      const label = input.value.trim();
      if (!label) return;
      const result = addTagDefinition(label, color);
      if (!result) { alert('Tag già esistente'); return; }
      renderImpostazioni();
    });
  });

  // Wire Enter key on inputs
  container.querySelectorAll('.add-tag-input').forEach(input => {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        container.querySelector(`.add-tag-btn[data-color="${input.dataset.color}"]`).click();
      }
    });
  });

  // Export/Import
  document.getElementById('settings-export').addEventListener('click', exportTagStore);
  document.getElementById('settings-import').addEventListener('change', (e) => {
    importTagStore(e);
    setTimeout(renderImpostazioni, 500);
  });

  // Statistics table
  buildTagStatsTable();
}

function buildTagStatsTable() {
  const tagIdx = buildTagIndex();
  const statsData = [];
  getTagDefinitions().forEach(def => {
    const saleIds = tagIdx[def.id];
    if (!saleIds || !saleIds.size) return;
    const projects = DATA.projects.filter(p => saleIds.has(String(p.sale_id)));
    if (!projects.length) return;
    const avgMargin = projects.reduce((s, p) => s + (p.margin_pct || 0), 0) / projects.length;
    statsData.push({ tag: def, count: projects.length, avgMargin });
  });

  if (!statsData.length) return;

  buildSortableTable(document.getElementById('settings-stats-table'), [
    { label: 'Tag', render: d => {
      const c = TAG_COLORS[d.tag.color];
      return `<span class="tag-pill" style="background:${c.bg};color:${c.text}">${d.tag.label}</span>`;
    }, value: d => d.tag.label },
    { label: 'N. Progetti', numeric: true, value: d => d.count, render: d => d.count },
    { label: 'Margine% Medio', numeric: true, value: d => d.avgMargin, render: d => `<span class="${marginClass(d.avgMargin)}">${fmtPct(d.avgMargin)}</span>` }
  ], statsData, { defaultSort: 1, defaultAsc: false });
}

function initImpostazioni() {
  // Nothing to init, renderImpostazioni handles everything
}
