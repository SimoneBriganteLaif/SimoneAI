// ═══════════════════════════════════════════════════════
// Tab 4: Accuratezza Stime (con filtri e KPI)
// ═══════════════════════════════════════════════════════

let stimeFilters = { companies: [], teamLeaders: [], years: [], statuses: [] };
let stimeFilterInstances = {};

function initStimeFilters() {
  const container = document.getElementById('stime-filters');
  container.innerHTML = '';

  const companies = [...new Set(DATA.projects.map(p => p.company))].filter(Boolean).sort();
  const tls = [...new Set(DATA.projects.map(p => p.team_leader))].filter(Boolean).sort();
  const years = [...new Set(DATA.projects.map(p => p.dat_order ? getYear(p.dat_order) : null))].filter(Boolean).sort().reverse();
  const statuses = [...new Set(DATA.projects.map(p => p.status))].filter(Boolean).sort();

  const companyGroup = document.createElement('div');
  companyGroup.className = 'filter-group';
  companyGroup.innerHTML = '<label>Company</label>';
  stimeFilterInstances.company = createMultiSelect(companyGroup, {
    options: companies.map(c => ({ value: c, label: c.toUpperCase() })),
    placeholder: 'Tutte',
    onChange: (vals) => { stimeFilters.companies = vals; renderStime(); }
  });
  container.appendChild(companyGroup);

  const tlGroup = document.createElement('div');
  tlGroup.className = 'filter-group';
  tlGroup.innerHTML = '<label>Team Leader</label>';
  stimeFilterInstances.tl = createMultiSelect(tlGroup, {
    options: tls.map(t => ({ value: t, label: t })),
    placeholder: 'Tutti',
    onChange: (vals) => { stimeFilters.teamLeaders = vals; renderStime(); }
  });
  container.appendChild(tlGroup);

  const yearGroup = document.createElement('div');
  yearGroup.className = 'filter-group';
  yearGroup.innerHTML = '<label>Anno</label>';
  stimeFilterInstances.year = createMultiSelect(yearGroup, {
    options: years.map(y => ({ value: y, label: y })),
    placeholder: 'Tutti',
    onChange: (vals) => { stimeFilters.years = vals; renderStime(); }
  });
  container.appendChild(yearGroup);

  const statusGroup = document.createElement('div');
  statusGroup.className = 'filter-group';
  statusGroup.innerHTML = '<label>Stato</label>';
  stimeFilterInstances.status = createMultiSelect(statusGroup, {
    options: statuses.map(s => ({ value: s, label: STATUS_LABELS[s] || s })),
    placeholder: 'Tutti',
    onChange: (vals) => { stimeFilters.statuses = vals; renderStime(); }
  });
  container.appendChild(statusGroup);

  const resetGroup = document.createElement('div');
  resetGroup.className = 'filter-group';
  resetGroup.style.justifyContent = 'flex-end';
  resetGroup.innerHTML = '<button class="btn btn-sm" onclick="resetStimeFilters()">Reset</button>';
  container.appendChild(resetGroup);
}

function resetStimeFilters() {
  stimeFilters = { companies: [], teamLeaders: [], years: [], statuses: [] };
  Object.values(stimeFilterInstances).forEach(inst => inst.reset());
  renderStime();
}

function getFilteredStimeProjects() {
  return DATA.projects.filter(p => {
    if (!p.total_hours || p.total_hours <= 0) return false;
    if (!p.days_target || p.days_target <= 0) return false;
    if (stimeFilters.companies.length && !stimeFilters.companies.includes(p.company)) return false;
    if (stimeFilters.teamLeaders.length && !stimeFilters.teamLeaders.includes(p.team_leader)) return false;
    if (stimeFilters.years.length && p.dat_order && !stimeFilters.years.includes(getYear(p.dat_order))) return false;
    if (stimeFilters.statuses.length && !stimeFilters.statuses.includes(p.status)) return false;
    return true;
  });
}

function renderStimeKPIs(data) {
  const kpiContainer = document.getElementById('stime-kpis');
  if (!data.length) {
    kpiContainer.innerHTML = '';
    return;
  }

  const ratios = data.map(p => p.days_actual / p.days_target);
  const avgRatio = ratios.reduce((s, r) => s + r, 0) / ratios.length;
  const worstRatio = Math.max(...ratios);
  const overrunCount = data.filter(p => (p.days_overrun || 0) > 0).length;
  const pctOverrun = (overrunCount / data.length) * 100;
  const overrunProjects = data.filter(p => (p.days_overrun || 0) > 0);
  const avgOverrun = overrunProjects.length ? overrunProjects.reduce((s, p) => s + p.days_overrun, 0) / overrunProjects.length : 0;

  const ratioColor = avgRatio > 2 ? 'var(--error)' : avgRatio > 1.3 ? 'var(--warning)' : 'var(--success)';
  const worstColor = worstRatio > 2 ? 'var(--error)' : worstRatio > 1.3 ? 'var(--warning)' : 'var(--success)';

  kpiContainer.innerHTML = `
    <div class="kpi-box"><div class="kpi-label">Media Ratio</div><div class="kpi-value" style="color:${ratioColor}">${fmtNum(avgRatio, 2)}x</div></div>
    <div class="kpi-box"><div class="kpi-label">Worst Ratio</div><div class="kpi-value" style="color:${worstColor}">${fmtNum(worstRatio, 2)}x</div></div>
    <div class="kpi-box"><div class="kpi-label">% in Sforamento</div><div class="kpi-value" style="color:${pctOverrun > 50 ? 'var(--error)' : 'var(--warning)'}">${fmtPct(pctOverrun)}</div></div>
    <div class="kpi-box"><div class="kpi-label">Sforamento Medio</div><div class="kpi-value" style="color:var(--error)">${avgOverrun > 0 ? '+' : ''}${fmtDays(avgOverrun)} GG</div></div>
  `;
}

function renderStime() {
  const data = getFilteredStimeProjects();
  renderStimeKPIs(data);

  // Project detail table
  const columns = [
    { label: 'Progetto', key: 'project' },
    { label: 'Cliente', key: 'client' },
    { label: 'TL', key: 'team_leader', render: p => p.team_leader || '\u2014' },
    { label: 'GG Target', numeric: true, value: p => p.days_target, render: p => fmtDays(p.days_target) },
    { label: 'GG Effettivi', numeric: true, value: p => p.days_actual, render: p => fmtDays(p.days_actual) },
    { label: 'Ratio', numeric: true, value: p => p.days_actual / p.days_target, render: p => {
      const r = p.days_actual / p.days_target;
      const color = r > 2 ? 'var(--error)' : r > 1.3 ? 'var(--warning)' : r > 1 ? '#c0a000' : 'var(--success)';
      return `<span style="color:${color};font-weight:600">${fmtNum(r, 2)}x</span>`;
    }},
    { label: 'Sforamento', numeric: true, value: p => p.days_overrun, render: p => {
      const v = p.days_overrun;
      if (v == null) return '\u2014';
      const color = v > 0 ? 'var(--error)' : 'var(--success)';
      return `<span style="color:${color}">${v > 0 ? '+' : ''}${fmtDays(v)} GG</span>`;
    }}
  ];

  buildSortableTable(document.getElementById('stime-table'), columns, data, {
    defaultSort: 5, defaultAsc: false
  });

  // TL aggregation
  const tlMap = {};
  data.forEach(p => {
    const tl = p.team_leader || 'N/A';
    if (!tlMap[tl]) tlMap[tl] = { tl, projects: [], totalTarget: 0, totalActual: 0 };
    tlMap[tl].projects.push(p);
    tlMap[tl].totalTarget += p.days_target;
    tlMap[tl].totalActual += p.days_actual;
  });
  const tlData = Object.values(tlMap).map(t => ({
    ...t,
    avgRatio: t.totalActual / t.totalTarget,
    worst: Math.max(...t.projects.map(p => p.days_actual / p.days_target))
  }));

  buildSortableTable(document.getElementById('stime-tl-table'), [
    { label: 'Team Leader', value: t => t.tl, render: t => t.tl },
    { label: 'N. Progetti', numeric: true, value: t => t.projects.length, render: t => t.projects.length },
    { label: 'Ratio Medio', numeric: true, value: t => t.avgRatio, render: t => {
      const color = t.avgRatio > 2 ? 'var(--error)' : t.avgRatio > 1.3 ? 'var(--warning)' : 'var(--success)';
      return `<span style="color:${color};font-weight:600">${fmtNum(t.avgRatio, 2)}x</span>`;
    }},
    { label: 'Worst', numeric: true, value: t => t.worst, render: t => {
      const color = t.worst > 2 ? 'var(--error)' : t.worst > 1.3 ? 'var(--warning)' : 'var(--success)';
      return `<span style="color:${color}">${fmtNum(t.worst, 2)}x</span>`;
    }}
  ], tlData, { defaultSort: 2, defaultAsc: false });

  // Client aggregation
  const clMap = {};
  data.forEach(p => {
    const cl = p.client || 'N/A';
    if (!clMap[cl]) clMap[cl] = { client: cl, projects: [], totalTarget: 0, totalActual: 0 };
    clMap[cl].projects.push(p);
    clMap[cl].totalTarget += p.days_target;
    clMap[cl].totalActual += p.days_actual;
  });
  const clData = Object.values(clMap).map(c => ({
    ...c,
    avgRatio: c.totalActual / c.totalTarget
  }));

  buildSortableTable(document.getElementById('stime-client-table'), [
    { label: 'Cliente', value: c => c.client, render: c => c.client },
    { label: 'N. Progetti', numeric: true, value: c => c.projects.length, render: c => c.projects.length },
    { label: 'Ratio Medio', numeric: true, value: c => c.avgRatio, render: c => {
      const color = c.avgRatio > 2 ? 'var(--error)' : c.avgRatio > 1.3 ? 'var(--warning)' : 'var(--success)';
      return `<span style="color:${color};font-weight:600">${fmtNum(c.avgRatio, 2)}x</span>`;
    }}
  ], clData, { defaultSort: 2, defaultAsc: false });
}
