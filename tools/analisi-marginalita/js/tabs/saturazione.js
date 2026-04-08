// ═══════════════════════════════════════════════════════
// Tab 3: Risorse (Saturazione + Context Switching)
// ═══════════════════════════════════════════════════════

let risorseFilters = { companies: [], teamLeaders: [], persons: [], dateFrom: '', dateTo: '' };
let risorseFilterInstances = {};
let selectedPerson = null;

const MONTH_LABELS_IT = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];

function fmtMonthLabel(monthStr) {
  const d = new Date(monthStr);
  return `${MONTH_LABELS_IT[d.getMonth()]} '${String(d.getFullYear()).slice(2)}`;
}

function initSaturation() {
  const container = document.getElementById('risorse-filters');
  if (!container) return;

  // Collect unique values for filters
  const companies = new Set();
  const teamLeaders = new Set();
  const persons = new Set();

  DATA.employees.forEach(e => {
    if (!e.flg_operations) return;
    if (e.company) companies.add(e.company);
    if (e.team_leader) teamLeaders.add(e.team_leader);
    if (e.name) persons.add(e.name);
  });

  // Default date range: 6 months ago to today
  const today = new Date();
  const sixMonthsAgo = new Date(today);
  sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
  risorseFilters.dateFrom = sixMonthsAgo.toISOString().slice(0, 10);
  risorseFilters.dateTo = today.toISOString().slice(0, 10);

  container.innerHTML = '';

  // Company multi-select
  const companyGroup = document.createElement('div');
  companyGroup.className = 'filter-group';
  companyGroup.innerHTML = '<label>Company</label><div id="risorse-company-wrap"></div>';
  container.appendChild(companyGroup);

  risorseFilterInstances.company = createMultiSelect(document.getElementById('risorse-company-wrap'), {
    options: [...companies].sort().map(c => ({ value: c, label: c })),
    placeholder: 'Tutte',
    onChange: (vals) => { risorseFilters.companies = vals; renderSaturation(); }
  });

  // Team Leader multi-select
  const tlGroup = document.createElement('div');
  tlGroup.className = 'filter-group';
  tlGroup.innerHTML = '<label>TL</label><div id="risorse-tl-wrap"></div>';
  container.appendChild(tlGroup);

  risorseFilterInstances.teamLeader = createMultiSelect(document.getElementById('risorse-tl-wrap'), {
    options: [...teamLeaders].sort().map(t => ({ value: t, label: t })),
    placeholder: 'Tutti',
    onChange: (vals) => { risorseFilters.teamLeaders = vals; renderSaturation(); }
  });

  // Persona multi-select
  const personGroup = document.createElement('div');
  personGroup.className = 'filter-group';
  personGroup.innerHTML = '<label>Persona</label><div id="risorse-person-wrap"></div>';
  container.appendChild(personGroup);

  risorseFilterInstances.person = createMultiSelect(document.getElementById('risorse-person-wrap'), {
    options: [...persons].sort().map(p => ({ value: p, label: p })),
    placeholder: 'Tutte',
    onChange: (vals) => { risorseFilters.persons = vals; renderSaturation(); }
  });

  // Date from
  const fromGroup = document.createElement('div');
  fromGroup.className = 'filter-group';
  fromGroup.innerHTML = `<label>Da</label><input type="date" id="risorse-date-from" value="${risorseFilters.dateFrom}">`;
  container.appendChild(fromGroup);
  fromGroup.querySelector('input').addEventListener('change', (e) => {
    risorseFilters.dateFrom = e.target.value;
    renderSaturation();
  });

  // Date to
  const toGroup = document.createElement('div');
  toGroup.className = 'filter-group';
  toGroup.innerHTML = `<label>A</label><input type="date" id="risorse-date-to" value="${risorseFilters.dateTo}">`;
  container.appendChild(toGroup);
  toGroup.querySelector('input').addEventListener('change', (e) => {
    risorseFilters.dateTo = e.target.value;
    renderSaturation();
  });

  renderSaturation();
}

function getFilteredEmployees() {
  return DATA.employees.filter(e => {
    if (!e.flg_operations) return false;
    if (risorseFilters.companies.length && !risorseFilters.companies.includes(e.company)) return false;
    if (risorseFilters.teamLeaders.length && !risorseFilters.teamLeaders.includes(e.team_leader)) return false;
    if (risorseFilters.persons.length && !risorseFilters.persons.includes(e.name)) return false;
    return true;
  });
}

function isMonthInRange(monthStr) {
  if (!monthStr) return false;
  const m = monthStr.slice(0, 7); // YYYY-MM
  const from = risorseFilters.dateFrom ? risorseFilters.dateFrom.slice(0, 7) : '';
  const to = risorseFilters.dateTo ? risorseFilters.dateTo.slice(0, 7) : '';
  if (from && m < from) return false;
  if (to && m > to) return false;
  return true;
}

function renderSaturation() {
  const employees = getFilteredEmployees();

  renderKPIs(employees);
  renderRisorseHeatmap(employees);

  if (selectedPerson) {
    const emp = employees.find(e => e.name === selectedPerson);
    if (emp) {
      renderPersonDetail(emp);
    } else {
      document.getElementById('risorse-person-detail').style.display = 'none';
      selectedPerson = null;
    }
  }
}

// ── Section A: KPIs ──
function renderKPIs(employees) {
  const container = document.getElementById('risorse-kpis');
  if (!container) return;

  let totalUtil = 0, utilCount = 0;
  let totalHoursSold = 0, totalHoursWorked = 0, totalHoursAbsence = 0;
  let weeklyProjectsSum = 0, weeklyProjectsCount = 0;

  employees.forEach(emp => {
    (emp.monthly_saturation || []).forEach(ms => {
      if (!isMonthInRange(ms.month)) return;
      totalUtil += ms.utilization_pct;
      utilCount++;
      totalHoursSold += ms.hours_sold || 0;
      totalHoursWorked += ms.hours_worked || 0;
      totalHoursAbsence += ms.hours_absence || 0;
    });

    (emp.weekly_context_switching || []).forEach(ws => {
      if (!isMonthInRange(ws.month)) return;
      weeklyProjectsSum += ws.num_projects || 0;
      weeklyProjectsCount++;
    });
  });

  const avgUtil = utilCount ? totalUtil / utilCount : 0;
  const absencePct = (totalHoursWorked + totalHoursAbsence) > 0
    ? (totalHoursAbsence / (totalHoursWorked + totalHoursAbsence)) * 100
    : 0;
  const avgProjects = weeklyProjectsCount ? weeklyProjectsSum / weeklyProjectsCount : 0;

  container.innerHTML = `
    <div class="kpi-box">
      <div class="kpi-label">Utilizzo medio</div>
      <div class="kpi-value" style="color:${avgUtil >= 70 ? 'var(--success-dark)' : 'var(--warning)'}">${fmtPct(avgUtil)}</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-label">Ore vendute / totali</div>
      <div class="kpi-value">${fmtHours(totalHoursSold)} / ${fmtHours(totalHoursWorked)}</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-label">% Assenze</div>
      <div class="kpi-value">${fmtPct(absencePct)}</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-label">Media progetti/sett</div>
      <div class="kpi-value" style="color:${avgProjects >= 4 ? 'var(--error)' : avgProjects >= 3 ? 'var(--warning)' : 'var(--primary-dark)'}">${fmtNum(avgProjects, 1)}</div>
    </div>
  `;
}

// ── Section B: Heatmap Persone × Mesi ──
function renderRisorseHeatmap(employees) {
  const container = document.getElementById('risorse-heatmap');
  if (!container) return;

  // Collect all months in range
  const monthSet = new Set();
  employees.forEach(emp => {
    (emp.monthly_saturation || []).forEach(ms => {
      if (isMonthInRange(ms.month)) monthSet.add(ms.month.slice(0, 7));
    });
  });
  const months = [...monthSet].sort();

  if (!months.length || !employees.length) {
    container.innerHTML = '<div style="color:var(--muted);font-size:0.85rem;padding:12px">Nessun dato nel periodo selezionato</div>';
    return;
  }

  // Build employee data
  const empData = [];
  employees.forEach(emp => {
    const satByMonth = {};
    (emp.monthly_saturation || []).forEach(ms => {
      const mk = ms.month.slice(0, 7);
      if (isMonthInRange(ms.month)) satByMonth[mk] = ms;
    });

    // Aggregate weekly context switching to monthly
    const csByMonth = {};
    (emp.weekly_context_switching || []).forEach(ws => {
      const mk = ws.month ? ws.month.slice(0, 7) : null;
      if (!mk || !isMonthInRange(ws.month)) return;
      if (!csByMonth[mk]) csByMonth[mk] = { sum: 0, count: 0 };
      csByMonth[mk].sum += ws.num_projects || 0;
      csByMonth[mk].count++;
    });

    // Check if employee has any data in range
    const hasData = months.some(m => satByMonth[m]);
    if (!hasData) return;

    const row = { name: emp.name, satByMonth, csByMonth, months: {} };
    let totalUtil = 0, totalCount = 0;
    months.forEach(m => {
      const sat = satByMonth[m];
      const cs = csByMonth[m];
      const util = sat ? sat.utilization_pct : null;
      const numProj = cs ? (cs.sum / cs.count) : null;
      row.months[m] = { util, numProj };
      if (util != null) { totalUtil += util; totalCount++; }
    });
    row.avgUtil = totalCount ? totalUtil / totalCount : null;
    empData.push(row);
  });

  // Sort by name
  empData.sort((a, b) => a.name.localeCompare(b.name));

  // Compute column totals
  const colTotals = {};
  months.forEach(m => {
    let sum = 0, count = 0;
    empData.forEach(e => {
      if (e.months[m] && e.months[m].util != null) { sum += e.months[m].util; count++; }
    });
    colTotals[m] = count ? sum / count : null;
  });

  // Legend
  let html = `<div class="note-box" style="margin-bottom:12px;font-size:0.8rem">
    <strong>Come leggere questa vista:</strong> Ogni cella mostra la % di utilizzo e il numero di progetti attivi nel mese.
    Clicca sul nome di una persona per vedere il suo andamento dettagliato e i progetti su cui ha lavorato.<br>
    <span style="display:inline-flex;gap:12px;margin-top:6px;flex-wrap:wrap">
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:2px;background:rgba(242,73,58,0.25);vertical-align:middle"></span> &gt;90% (sovraccarico)</span>
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:2px;background:rgba(47,218,115,0.2);vertical-align:middle"></span> 70-90% (ottimale)</span>
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:2px;background:rgba(255,165,0,0.2);vertical-align:middle"></span> 60-70% (sotto target)</span>
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:2px;background:rgba(122,122,122,0.1);vertical-align:middle"></span> &lt;60% (sottoutilizzato)</span>
    </span>
  </div>`;

  // Build table HTML
  html += '<table class="heatmap-table"><thead><tr>';
  html += '<th class="sticky-left" style="left:0;min-width:140px">Persona</th>';
  html += '<th class="sticky-left" style="left:140px;min-width:60px">Totale</th>';
  months.forEach(m => {
    html += `<th>${fmtMonthLabel(m + '-01')}</th>`;
  });
  html += '</tr></thead><tbody>';

  empData.forEach(row => {
    const isSelected = selectedPerson === row.name;
    html += `<tr class="risorse-hm-row${isSelected ? ' selected' : ''}" data-person="${row.name}" style="cursor:pointer${isSelected ? ';outline:2px solid var(--primary)' : ''}">`;
    html += `<td class="sticky-left" style="left:0;font-weight:500;font-size:0.75rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:140px" title="${row.name}">${row.name}</td>`;
    // Totale column
    const avgBg = row.avgUtil != null ? satBgColor(row.avgUtil) : 'transparent';
    html += `<td class="hm-cell sticky-left" style="left:140px;background:${avgBg};font-weight:600">${row.avgUtil != null ? Math.round(row.avgUtil) + '%' : '\u2014'}</td>`;
    months.forEach(m => {
      const cell = row.months[m];
      if (cell && cell.util != null) {
        const bg = satBgColor(cell.util);
        const projLabel = cell.numProj != null ? ` <span style="font-size:0.58rem;color:var(--muted)">${cell.numProj.toFixed(1)}p</span>` : '';
        html += `<td class="hm-cell" style="background:${bg}">${Math.round(cell.util)}%${projLabel}</td>`;
      } else {
        html += '<td class="hm-cell">\u2014</td>';
      }
    });
    html += '</tr>';
  });

  // Totals row
  html += '<tr class="totals-row"><th class="sticky-left" style="left:0">Media</th>';
  const overallTotal = empData.reduce((s, e) => s + (e.avgUtil || 0), 0) / (empData.filter(e => e.avgUtil != null).length || 1);
  html += `<td class="hm-cell sticky-left" style="left:140px;font-weight:700">${Math.round(overallTotal)}%</td>`;
  months.forEach(m => {
    const val = colTotals[m];
    html += `<td class="hm-cell" style="font-weight:700">${val != null ? Math.round(val) + '%' : '\u2014'}</td>`;
  });
  html += '</tr>';

  html += '</tbody></table>';
  container.innerHTML = html;

  // Click handlers
  container.querySelectorAll('.risorse-hm-row').forEach(tr => {
    tr.addEventListener('click', () => {
      const name = tr.dataset.person;
      selectedPerson = name;
      const emp = employees.find(e => e.name === name);
      if (emp) {
        renderRisorseHeatmap(employees); // re-render to update highlight
        renderPersonDetail(emp);
      }
    });
  });
}

// ── Section C: Person Timeline Chart ──
function renderPersonDetail(emp) {
  const detailEl = document.getElementById('risorse-person-detail');
  detailEl.style.display = 'block';
  document.getElementById('risorse-person-title').textContent = `Timeline — ${emp.name}`;

  renderPersonChart(emp);
  renderPersonGantt(emp);
}

function renderPersonChart(emp) {
  if (charts.risorsePerson) charts.risorsePerson.destroy();

  const satData = (emp.monthly_saturation || [])
    .filter(ms => isMonthInRange(ms.month))
    .sort((a, b) => a.month.localeCompare(b.month));

  // Aggregate weekly CS to monthly
  const csByMonth = {};
  (emp.weekly_context_switching || []).forEach(ws => {
    const mk = ws.month ? ws.month.slice(0, 7) : null;
    if (!mk || !isMonthInRange(ws.month)) return;
    if (!csByMonth[mk]) csByMonth[mk] = { sum: 0, count: 0 };
    csByMonth[mk].sum += ws.num_projects || 0;
    csByMonth[mk].count++;
  });

  const labels = satData.map(ms => fmtMonthLabel(ms.month));
  const utilData = satData.map(ms => ms.utilization_pct);
  const projData = satData.map(ms => {
    const mk = ms.month.slice(0, 7);
    const cs = csByMonth[mk];
    return cs ? cs.sum / cs.count : 0;
  });
  const barColors = projData.map(v => v >= 4 ? 'rgba(242,73,58,0.7)' : v >= 3 ? 'rgba(255,165,0,0.7)' : 'rgba(100,194,209,0.7)');

  const ctx = document.getElementById('risorse-person-chart').getContext('2d');
  charts.risorsePerson = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          type: 'line',
          label: 'Utilizzo %',
          data: utilData,
          borderColor: 'var(--primary-dark)',
          backgroundColor: 'rgba(100,194,209,0.1)',
          borderWidth: 2,
          pointRadius: 3,
          tension: 0.3,
          yAxisID: 'y',
          order: 1
        },
        {
          type: 'bar',
          label: 'Progetti/sett (media)',
          data: projData,
          backgroundColor: barColors,
          borderRadius: 3,
          yAxisID: 'y1',
          order: 2
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'top', labels: { font: { size: 11 } } }
      },
      scales: {
        y: {
          type: 'linear',
          position: 'left',
          title: { display: true, text: 'Utilizzo %', font: { size: 11 } },
          min: 0,
          max: 120,
          ticks: { callback: v => v + '%' }
        },
        y1: {
          type: 'linear',
          position: 'right',
          title: { display: true, text: 'Progetti/sett', font: { size: 11 } },
          min: 0,
          grid: { drawOnChartArea: false },
          ticks: { stepSize: 1 }
        }
      }
    }
  });
}

// ── Section D: Project Load Mini-Gantt ──
function renderPersonGantt(emp) {
  const container = document.getElementById('risorse-person-gantt');
  if (!container) return;

  // Find all timesheet entries for this person
  const tsEntries = DATA.timesheet.filter(t => t.employee === emp.name || t.id_employee === emp.id);

  // Group by project
  const projectMap = {};
  tsEntries.forEach(t => {
    const key = t.id_sale || t.project;
    if (!projectMap[key]) projectMap[key] = { name: t.project, id_sale: t.id_sale, hours: 0, dates: [] };
    projectMap[key].hours += t.hours || 0;
    const dateStr = t.week_start || t.dat_month;
    if (dateStr) projectMap[key].dates.push(dateStr);
  });

  let projects = Object.values(projectMap).filter(p => p.hours > 0);

  // Compute min/max dates per project and filter by date range
  projects.forEach(p => {
    const sorted = p.dates.sort();
    p.startDate = sorted[0];
    p.endDate = sorted[sorted.length - 1];
    // Look up margin
    const proj = DATA.projects.find(dp => dp.sale_id === p.id_sale || dp.project === p.name);
    p.margin_pct = proj ? proj.margin_pct : null;
  });

  // Filter projects with dates in range
  projects = projects.filter(p => {
    if (!p.startDate) return false;
    const from = risorseFilters.dateFrom || '';
    const to = risorseFilters.dateTo || '';
    if (to && p.startDate > to) return false;
    if (from && p.endDate < from) return false;
    return true;
  });

  // Sort by start date
  projects.sort((a, b) => a.startDate.localeCompare(b.startDate));

  if (!projects.length) {
    container.innerHTML = '<div style="color:var(--muted);font-size:0.82rem;padding:8px">Nessun progetto nel periodo</div>';
    return;
  }

  // Compute global date range for positioning
  const rangeStart = risorseFilters.dateFrom || projects[0].startDate;
  const rangeEnd = risorseFilters.dateTo || projects[projects.length - 1].endDate;
  const rangeStartMs = new Date(rangeStart).getTime();
  const rangeEndMs = new Date(rangeEnd).getTime();
  const rangeDuration = Math.max(rangeEndMs - rangeStartMs, 1);

  let html = '';
  projects.forEach(p => {
    const startMs = Math.max(new Date(p.startDate).getTime(), rangeStartMs);
    const endMs = Math.min(new Date(p.endDate).getTime(), rangeEndMs);
    const leftPct = ((startMs - rangeStartMs) / rangeDuration * 100).toFixed(1);
    const widthPct = Math.max(((endMs - startMs) / rangeDuration * 100), 1).toFixed(1);
    const color = p.margin_pct != null ? marginColor(p.margin_pct) : 'var(--primary)';
    const days = p.hours / 8;
    const marginLabel = p.margin_pct != null ? ` | Margine: ${fmtPct(p.margin_pct)}` : '';

    const projData = DATA.projects.find(pr => pr.sale_id === p.id_sale);
    const clientName = projData ? projData.client : '';
    const displayName = clientName ? `${p.name} (${clientName})` : p.name;

    html += `<div style="display:flex;align-items:center;height:28px;margin-bottom:4px">`;
    html += `<div style="width:260px;flex-shrink:0;font-size:0.78rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="${displayName}">${displayName}</div>`;
    html += `<div style="flex:1;position:relative;height:20px;background:#f5f5f5;border-radius:3px">`;
    html += `<div style="position:absolute;left:${leftPct}%;width:${widthPct}%;height:100%;background:${color};border-radius:3px;opacity:0.8" title="${fmtDays(days)} GG${marginLabel}"></div>`;
    html += `</div>`;
    html += `<div style="width:60px;text-align:right;font-size:0.75rem;font-family:'JetBrains Mono',monospace">${fmtDays(days)} GG</div>`;
    html += `</div>`;
  });

  container.innerHTML = html;
}
