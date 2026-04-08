// ═══════════════════════════════════════════════════════
// Tab 1: Classifica Progetti
// ═══════════════════════════════════════════════════════

let classificaFilters = { companies: [], teamLeaders: [], clients: [], years: [], statuses: [], persons: [], tags: [], projectType: [], marginMin: '', marginMax: '' };
let classificaFilterInstances = {};

let currentModalSaleId = null;

function openTagModal(project, event) {
  if (event) event.stopPropagation();
  currentModalSaleId = project.sale_id;
  const overlay = document.getElementById('tag-modal-overlay');
  const title = document.getElementById('tag-modal-title');
  title.textContent = `${project.project} — ${project.client}`;

  const pt = getProjectTags(project.sale_id);
  const selectedTags = new Set(pt.tags || []);

  // Populate tag pickers
  ['red', 'green', 'neutral'].forEach(color => {
    const container = document.getElementById(`modal-tags-${color}`);
    const defs = getTagDefinitions(color);
    container.innerHTML = defs.map(def => {
      const c = TAG_COLORS[def.color];
      const isSelected = selectedTags.has(def.id);
      const bgColor = isSelected ? c.bg : c.bgLight;
      const txtColor = isSelected ? c.text : (def.color === 'neutral' ? '#555' : c.bg);
      return `<span class="tag-pill${isSelected ? ' selected' : ''}" data-tag-id="${def.id}" style="background:${bgColor};color:${txtColor}">${def.label}</span>`;
    }).join(' ');

    container.querySelectorAll('.tag-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        pill.classList.toggle('selected');
        const def = getTagDef(pill.dataset.tagId);
        const c = TAG_COLORS[def.color];
        if (pill.classList.contains('selected')) {
          pill.style.background = c.bg;
          pill.style.color = c.text;
        } else {
          pill.style.background = c.bgLight;
          pill.style.color = def.color === 'neutral' ? '#555' : c.bg;
        }
      });
    });
  });

  document.getElementById('modal-positive-notes').value = pt.positive_notes || '';
  document.getElementById('modal-negative-notes').value = pt.negative_notes || '';
  overlay.style.display = 'flex';
}

function closeTagModal() {
  document.getElementById('tag-modal-overlay').style.display = 'none';
  currentModalSaleId = null;
}

function saveTagModal() {
  if (!currentModalSaleId) return;
  const tags = [];
  document.querySelectorAll('#tag-modal-overlay .tag-pill.selected').forEach(pill => {
    tags.push(pill.dataset.tagId);
  });
  setProjectTags(currentModalSaleId, {
    tags,
    positive_notes: document.getElementById('modal-positive-notes').value,
    negative_notes: document.getElementById('modal-negative-notes').value
  });
  closeTagModal();
  applyClassificaFilters(); // refresh table to show updated tags
}

// Wire modal buttons
document.getElementById('tag-modal-close')?.addEventListener('click', closeTagModal);
document.getElementById('tag-modal-cancel')?.addEventListener('click', closeTagModal);
document.getElementById('tag-modal-save')?.addEventListener('click', saveTagModal);
document.getElementById('tag-modal-overlay')?.addEventListener('click', (e) => {
  if (e.target === e.currentTarget) closeTagModal();
});

function initClassificaFilters() {
  const container = document.getElementById('classifica-filters');
  const companies = [...new Set(DATA.projects.map(p => p.company))].filter(Boolean).sort();
  const tls = [...new Set(DATA.projects.map(p => p.team_leader))].filter(Boolean).sort();
  const clients = [...new Set(DATA.projects.map(p => p.client))].filter(Boolean).sort();
  const years = [...new Set(DATA.projects.map(p => p.dat_order ? getYear(p.dat_order) : null))].filter(Boolean).sort().reverse();

  container.innerHTML = '';

  // Company multi-select
  const companyGroup = document.createElement('div');
  companyGroup.className = 'filter-group';
  companyGroup.innerHTML = '<label>Company</label>';
  classificaFilterInstances.company = createMultiSelect(companyGroup, {
    options: companies.map(c => ({ value: c, label: c.toUpperCase() })),
    placeholder: 'Tutte',
    onChange: (vals) => { classificaFilters.companies = vals; applyClassificaFilters(); }
  });
  container.appendChild(companyGroup);

  // Team Leader multi-select
  const tlGroup = document.createElement('div');
  tlGroup.className = 'filter-group';
  tlGroup.innerHTML = '<label>Team Leader</label>';
  classificaFilterInstances.tl = createMultiSelect(tlGroup, {
    options: tls.map(t => ({ value: t, label: t })),
    placeholder: 'Tutti',
    onChange: (vals) => { classificaFilters.teamLeaders = vals; applyClassificaFilters(); }
  });
  container.appendChild(tlGroup);

  // Cliente multi-select
  const clientGroup = document.createElement('div');
  clientGroup.className = 'filter-group';
  clientGroup.innerHTML = '<label>Cliente</label>';
  classificaFilterInstances.client = createMultiSelect(clientGroup, {
    options: clients.map(c => ({ value: c, label: c })),
    placeholder: 'Tutti',
    onChange: (vals) => { classificaFilters.clients = vals; applyClassificaFilters(); }
  });
  container.appendChild(clientGroup);

  // Anno multi-select
  const yearGroup = document.createElement('div');
  yearGroup.className = 'filter-group';
  yearGroup.innerHTML = '<label>Anno</label>';
  classificaFilterInstances.year = createMultiSelect(yearGroup, {
    options: years.map(y => ({ value: y, label: y })),
    placeholder: 'Tutti',
    onChange: (vals) => { classificaFilters.years = vals; applyClassificaFilters(); }
  });
  container.appendChild(yearGroup);

  // Persona multi-select
  const persons = [...new Set(DATA.projects.flatMap(p => (p.people_detail || []).map(pd => pd.employee)))].filter(Boolean).sort();
  const personGroup = document.createElement('div');
  personGroup.className = 'filter-group';
  personGroup.innerHTML = '<label>Persona</label>';
  classificaFilterInstances.person = createMultiSelect(personGroup, {
    options: persons.map(pe => ({ value: pe, label: pe })),
    placeholder: 'Tutte',
    onChange: (vals) => { classificaFilters.persons = vals; applyClassificaFilters(); }
  });
  container.appendChild(personGroup);

  // Stato multi-select
  const statuses = [...new Set(DATA.projects.map(p => p.status))].filter(Boolean).sort();
  const statusGroup = document.createElement('div');
  statusGroup.className = 'filter-group';
  statusGroup.innerHTML = '<label>Stato</label>';
  classificaFilterInstances.status = createMultiSelect(statusGroup, {
    options: statuses.map(s => ({ value: s, label: STATUS_LABELS[s] || s })),
    placeholder: 'Tutti',
    onChange: (vals) => { classificaFilters.statuses = vals; applyClassificaFilters(); }
  });
  container.appendChild(statusGroup);

  // Tipo progetto multi-select
  const typeGroup = document.createElement('div');
  typeGroup.className = 'filter-group';
  typeGroup.innerHTML = '<label>Tipo</label>';
  classificaFilterInstances.type = createMultiSelect(typeGroup, {
    options: [
      { value: 'progetto', label: 'Progetto' },
      { value: 'ricorrente', label: 'Canone/Manut.' }
    ],
    placeholder: 'Tutti',
    onChange: (vals) => { classificaFilters.projectType = vals; applyClassificaFilters(); }
  });
  container.appendChild(typeGroup);

  // Tag multi-select
  const tagDefs = getTagDefinitions();
  const tagGroup = document.createElement('div');
  tagGroup.className = 'filter-group';
  tagGroup.innerHTML = '<label>Tag</label>';
  classificaFilterInstances.tag = createMultiSelect(tagGroup, {
    options: tagDefs.map(t => ({ value: t.id, label: t.label })),
    placeholder: 'Tutti',
    onChange: (vals) => { classificaFilters.tags = vals; applyClassificaFilters(); }
  });
  container.appendChild(tagGroup);

  // Margine% Min
  const minGroup = document.createElement('div');
  minGroup.className = 'filter-group';
  minGroup.innerHTML = '<label>Margine% Min</label><input type="number" id="filter-margin-min" placeholder="0" step="1">';
  container.appendChild(minGroup);

  // Margine% Max
  const maxGroup = document.createElement('div');
  maxGroup.className = 'filter-group';
  maxGroup.innerHTML = '<label>Margine% Max</label><input type="number" id="filter-margin-max" placeholder="100" step="1">';
  container.appendChild(maxGroup);

  // Reset
  const resetGroup = document.createElement('div');
  resetGroup.className = 'filter-group';
  resetGroup.style.justifyContent = 'flex-end';
  resetGroup.innerHTML = '<button class="btn btn-sm" onclick="resetClassificaFilters()">Reset</button>';
  container.appendChild(resetGroup);

  document.getElementById('filter-margin-min').addEventListener('input', (e) => { classificaFilters.marginMin = e.target.value; applyClassificaFilters(); });
  document.getElementById('filter-margin-max').addEventListener('input', (e) => { classificaFilters.marginMax = e.target.value; applyClassificaFilters(); });
}

function resetClassificaFilters() {
  classificaFilters = { companies: [], teamLeaders: [], clients: [], years: [], statuses: [], persons: [], tags: [], projectType: [], marginMin: '', marginMax: '' };
  Object.values(classificaFilterInstances).forEach(inst => inst.reset());
  document.getElementById('filter-margin-min').value = '';
  document.getElementById('filter-margin-max').value = '';
  applyClassificaFilters();
}

function getFilteredProjects() {
  return DATA.projects.filter(p => {
    if (classificaFilters.companies.length && !classificaFilters.companies.includes(p.company)) return false;
    if (classificaFilters.teamLeaders.length && !classificaFilters.teamLeaders.includes(p.team_leader)) return false;
    if (classificaFilters.clients.length && !classificaFilters.clients.includes(p.client)) return false;
    if (classificaFilters.years.length && p.dat_order && !classificaFilters.years.includes(getYear(p.dat_order))) return false;
    if (classificaFilters.statuses.length && !classificaFilters.statuses.includes(p.status)) return false;
    if (classificaFilters.persons.length && !(p.people_detail || []).some(pd => classificaFilters.persons.includes(pd.employee))) return false;
    if (classificaFilters.tags.length) {
      const pt = getProjectTags(p.sale_id).tags;
      if (!classificaFilters.tags.some(t => pt.includes(t))) return false;
    }
    if (classificaFilters.projectType.length) {
      const recurring = isRecurring(p);
      const matches = classificaFilters.projectType.some(t =>
        (t === 'ricorrente' && recurring) || (t === 'progetto' && !recurring)
      );
      if (!matches) return false;
    }
    if (classificaFilters.marginMin !== '' && p.margin_pct < parseFloat(classificaFilters.marginMin)) return false;
    if (classificaFilters.marginMax !== '' && p.margin_pct > parseFloat(classificaFilters.marginMax)) return false;
    return true;
  });
}

function applyClassificaFilters() {
  const filtered = getFilteredProjects();
  updateClassificaSummary(filtered);
  document.getElementById('classifica-table')._updateData(filtered);
}

function updateClassificaSummary(data) {
  const totalRev = data.reduce((s, p) => s + (p.revenue || 0), 0);
  const totalMargin = data.reduce((s, p) => s + (p.margin || 0), 0);
  const avgMargin = data.length ? data.reduce((s, p) => s + (p.margin_pct || 0), 0) / data.length : 0;
  document.getElementById('classifica-summary').innerHTML = `
    <div class="stat"><span>${data.length}</span> <span class="stat-value">progetti</span></div>
    <div class="stat">Revenue totale: <span class="stat-value">${fmtEur(totalRev)}</span></div>
    <div class="stat">Margine totale: <span class="stat-value">${fmtEur(totalMargin)}</span></div>
    <div class="stat">Margine medio: <span class="stat-value ${marginClass(avgMargin)}">${fmtPct(avgMargin)}</span></div>
  `;
}

function renderClassifica() {
  const columns = [
    { label: 'Progetto', key: 'project', render: (p) => {
      const icon = isRecurring(p) ? '<span title="Canone/Manutenzione" style="margin-right:4px">🔄</span>' : '';
      const badge = p.flg_active ? ' <span class="badge badge-active">IN CORSO</span>' : '';
      return icon + p.project + badge;
    }},
    { label: 'Cliente', key: 'client' },
    { label: 'TL', key: 'team_leader', render: p => p.team_leader || '\u2014' },
    { label: 'Revenue', numeric: true, value: p => p.revenue, render: p => fmtEur(p.revenue) },
    { label: 'Costo Tot.', numeric: true, value: p => (p.internal_cost||0)+(p.external_cost||0), render: p => fmtEur((p.internal_cost||0)+(p.external_cost||0)) },
    { label: 'Margine', numeric: true, value: p => p.margin, render: p => fmtEur(p.margin) },
    { label: 'Margine%', numeric: true, value: p => p.margin_pct, render: p => `<span class="${marginClass(p.margin_pct)}">${fmtPct(p.margin_pct)}</span>` },
    { label: 'GG Target', numeric: true, value: p => p.days_target, render: p => fmtDays(p.days_target) },
    { label: 'GG Effettivi', numeric: true, value: p => p.days_actual, render: p => fmtDays(p.days_actual) },
    { label: 'Sforamento', numeric: true, value: p => p.days_overrun, render: p => {
      const v = p.days_overrun;
      if (v == null || isNaN(v)) return '\u2014';
      const color = v > 0 ? 'var(--error)' : (v < 0 ? 'var(--success-dark)' : 'inherit');
      return `<span style="color:${color}">${v > 0 ? '+' : ''}${fmtDays(v)}</span>`;
    }},
    { label: 'Persone', numeric: true, value: p => p.num_people, render: p => p.num_people },
    { label: 'Stato', key: 'status', render: p => STATUS_LABELS[p.status] || p.status || '\u2014' },
    { label: 'Tag', render: p => renderTagBadges(p.sale_id) },
    { label: 'Note +', render: (p) => {
      const pt = getProjectTags(p.sale_id);
      const note = pt.positive_notes || '';
      if (!note) return '';
      const short = note.length > 30 ? note.substring(0, 30) + '\u2026' : note;
      return `<span title="${note.replace(/"/g, '&quot;')}" style="font-size:0.72rem;color:#18b356;max-width:120px;display:inline-block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${short}</span>`;
    }},
    { label: 'Note \u2212', render: (p) => {
      const pt = getProjectTags(p.sale_id);
      const note = pt.negative_notes || '';
      if (!note) return '';
      const short = note.length > 30 ? note.substring(0, 30) + '\u2026' : note;
      return `<span title="${note.replace(/"/g, '&quot;')}" style="font-size:0.72rem;color:var(--error);max-width:120px;display:inline-block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${short}</span>`;
    }},
    { label: '', render: (p) => `<button class="btn-icon tag-modal-btn" title="Assegna tag" onclick="openTagModal(DATA.projects.find(pr=>pr.sale_id===${p.sale_id}), event)">🏷</button>` }
  ];

  const data = getFilteredProjects();
  updateClassificaSummary(data);

  buildSortableTable(document.getElementById('classifica-table'), columns, data, {
    defaultSort: 6,
    defaultAsc: true,
    rowClass: (p) => marginRowClass(p.margin_pct),
    onRowClick: (p) => openClassificaDrill(p)
  });
}

function openClassificaDrill(project) {
  const panel = document.getElementById('classifica-drill');
  panel.classList.add('open');
  renderDrilldownContent(project, panel);
  panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
