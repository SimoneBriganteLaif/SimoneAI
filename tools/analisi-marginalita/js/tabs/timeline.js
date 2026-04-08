// ═══════════════════════════════════════════════════════
// Tab: Timeline Gantt
// ═══════════════════════════════════════════════════════

let timelineFilters = { companies: [], teamLeaders: [], persons: [], clients: [], years: [], sort: 'Data inizio' };
let timelineFilterInstances = {};

const MONTH_PX = 80;
const ROW_HEIGHT = 32;
const BAR_HEIGHT = 20;
const PADDING_DAYS = 15;

function initTimeline() {
  const container = document.getElementById('timeline-filters');
  container.innerHTML = '';

  const companies = [...new Set(DATA.projects.map(p => p.company))].filter(Boolean).sort();
  const tls = [...new Set(DATA.projects.map(p => p.team_leader))].filter(Boolean).sort();
  const persons = [...new Set(DATA.projects.flatMap(p => (p.people_detail || []).map(pd => pd.employee)))].filter(Boolean).sort();
  const years = [...new Set(DATA.projects.map(p => p.dat_order ? getYear(p.dat_order) : null))].filter(Boolean).sort().reverse();

  // Company
  const companyGroup = document.createElement('div');
  companyGroup.className = 'filter-group';
  companyGroup.innerHTML = '<label>Company</label>';
  timelineFilterInstances.company = createMultiSelect(companyGroup, {
    options: companies.map(c => ({ value: c, label: c.toUpperCase() })),
    placeholder: 'Tutte',
    onChange: (vals) => { timelineFilters.companies = vals; renderTimeline(); }
  });
  container.appendChild(companyGroup);

  // Team Leader
  const tlGroup = document.createElement('div');
  tlGroup.className = 'filter-group';
  tlGroup.innerHTML = '<label>Team Leader</label>';
  timelineFilterInstances.tl = createMultiSelect(tlGroup, {
    options: tls.map(t => ({ value: t, label: t })),
    placeholder: 'Tutti',
    onChange: (vals) => { timelineFilters.teamLeaders = vals; renderTimeline(); }
  });
  container.appendChild(tlGroup);

  // Persona
  const personGroup = document.createElement('div');
  personGroup.className = 'filter-group';
  personGroup.innerHTML = '<label>Persona</label>';
  timelineFilterInstances.person = createMultiSelect(personGroup, {
    options: persons.map(pe => ({ value: pe, label: pe })),
    placeholder: 'Tutte',
    onChange: (vals) => { timelineFilters.persons = vals; renderTimeline(); }
  });
  container.appendChild(personGroup);

  // Cliente
  const clientsForTimeline = [...new Set(DATA.projects.map(p => p.client))].filter(Boolean).sort();
  const clientGroup = document.createElement('div');
  clientGroup.className = 'filter-group';
  clientGroup.innerHTML = '<label>Cliente</label>';
  timelineFilterInstances.client = createMultiSelect(clientGroup, {
    options: clientsForTimeline.map(c => ({ value: c, label: c })),
    placeholder: 'Tutti',
    onChange: (vals) => { timelineFilters.clients = vals; renderTimeline(); }
  });
  container.appendChild(clientGroup);

  // Anno
  const yearGroup = document.createElement('div');
  yearGroup.className = 'filter-group';
  yearGroup.innerHTML = '<label>Anno</label>';
  timelineFilterInstances.year = createMultiSelect(yearGroup, {
    options: years.map(y => ({ value: y, label: y })),
    placeholder: 'Tutti',
    onChange: (vals) => { timelineFilters.years = vals; renderTimeline(); }
  });
  container.appendChild(yearGroup);

  // Ordinamento (single-select)
  const sortGroup = document.createElement('div');
  sortGroup.className = 'filter-group';
  sortGroup.innerHTML = '<label>Ordinamento</label>';
  timelineFilterInstances.sort = createSearchSelect(sortGroup, {
    options: [
      { value: 'Data inizio', label: 'Data inizio' },
      { value: 'Margine%', label: 'Margine%' },
      { value: 'Durata', label: 'Durata' }
    ],
    placeholder: 'Data inizio',
    onChange: (val) => { timelineFilters.sort = val || 'Data inizio'; renderTimeline(); }
  });
  container.appendChild(sortGroup);

  // Fallback dates for projects missing first_day/last_day
  DATA.projects.forEach(p => {
    if (!p.first_day && p.dat_order) p.first_day = p.dat_order;
    if (!p.last_day && p.first_day) {
      const daysEstimate = Math.max((p.days_actual || 20) * 1.5, 30);
      const end = new Date(p.first_day);
      end.setDate(end.getDate() + Math.round(daysEstimate));
      p.last_day = end.toISOString().split('T')[0];
    }
  });
}

function getTimelineProjects() {
  return DATA.projects.filter(p => {
    if (!p.first_day || !p.last_day) return false;
    if (timelineFilters.companies.length && !timelineFilters.companies.includes(p.company)) return false;
    if (timelineFilters.teamLeaders.length && !timelineFilters.teamLeaders.includes(p.team_leader)) return false;
    if (timelineFilters.persons.length && !(p.people_detail || []).some(pd => timelineFilters.persons.includes(pd.employee))) return false;
    if (timelineFilters.clients.length && !timelineFilters.clients.includes(p.client)) return false;
    if (timelineFilters.years.length && p.dat_order && !timelineFilters.years.includes(getYear(p.dat_order))) return false;
    return true;
  });
}

function sortTimelineProjects(projects) {
  const sorted = [...projects];
  switch (timelineFilters.sort) {
    case 'Margine%':
      sorted.sort((a, b) => (b.margin_pct || 0) - (a.margin_pct || 0));
      break;
    case 'Durata':
      sorted.sort((a, b) => {
        const durA = new Date(a.last_day) - new Date(a.first_day);
        const durB = new Date(b.last_day) - new Date(b.first_day);
        return durB - durA;
      });
      break;
    case 'Data inizio':
    default:
      sorted.sort((a, b) => new Date(a.first_day) - new Date(b.first_day));
      break;
  }
  return sorted;
}

function renderTimeline() {
  const projects = sortTimelineProjects(getTimelineProjects());
  const summaryEl = document.getElementById('timeline-summary');
  const containerEl = document.getElementById('timeline-gantt');
  const tooltip = document.getElementById('timeline-tooltip');

  // Summary bar
  if (projects.length === 0) {
    summaryEl.innerHTML = '<div class="stat">Nessun progetto con date disponibili</div>';
    containerEl.innerHTML = '<div style="padding:2rem;color:var(--text-secondary)">Nessun progetto corrispondente ai filtri selezionati.</div>';
    return;
  }

  const avgMargin = projects.reduce((s, p) => s + (p.margin_pct || 0), 0) / projects.length;
  const avgDurationMonths = projects.reduce((s, p) => {
    const days = (new Date(p.last_day) - new Date(p.first_day)) / (1000 * 60 * 60 * 24);
    return s + days / 30;
  }, 0) / projects.length;

  summaryEl.innerHTML = `
    <div class="stat"><span>${projects.length}</span> <span class="stat-value">progetti</span></div>
    <div class="stat">Durata media: <span class="stat-value">${fmtNum(avgDurationMonths, 1)} mesi</span></div>
    <div class="stat">Margine medio: <span class="stat-value">${fmtPct(avgMargin)}</span></div>
  `;

  // Compute time range
  const dates = projects.flatMap(p => [new Date(p.first_day), new Date(p.last_day)]);
  const minDate = new Date(Math.min(...dates));
  const maxDate = new Date(Math.max(...dates));
  minDate.setDate(minDate.getDate() - PADDING_DAYS);
  maxDate.setDate(maxDate.getDate() + PADDING_DAYS);

  const totalDays = (maxDate - minDate) / (1000 * 60 * 60 * 24);

  // Build month columns
  const months = [];
  const cursor = new Date(minDate.getFullYear(), minDate.getMonth(), 1);
  while (cursor <= maxDate) {
    const monthStart = new Date(cursor);
    cursor.setMonth(cursor.getMonth() + 1);
    const monthEnd = new Date(cursor);
    // Clamp to range
    const visStart = Math.max(monthStart.getTime(), minDate.getTime());
    const visEnd = Math.min(monthEnd.getTime(), maxDate.getTime());
    const fraction = (visEnd - visStart) / (1000 * 60 * 60 * 24) / 30.44; // approximate month fraction
    months.push({
      label: monthStart.toLocaleDateString('it-IT', { month: 'short', year: '2-digit' }),
      widthPx: Math.max(fraction * MONTH_PX, 20),
      offsetPct: ((visStart - minDate.getTime()) / (1000 * 60 * 60 * 24)) / totalDays * 100
    });
  }

  const totalWidth = months.reduce((s, m) => s + m.widthPx, 0);

  // Build left labels
  const leftLabelsHtml = `
    <div class="timeline-project-label" style="height:${ROW_HEIGHT}px">&nbsp;</div>
    ${projects.map((p, i) => `<div class="timeline-project-label" title="${p.project} — ${p.client || ''}">${p.project} <span style="color:var(--muted);font-size:0.7rem">— ${p.client || ''}</span></div>`).join('')}
  `;

  // Build month header
  const monthHeaderHtml = months.map(m =>
    `<div class="timeline-month-cell" style="width:${m.widthPx}px">${m.label}</div>`
  ).join('');

  // Build bar rows
  const barRowsHtml = projects.map((p, i) => {
    const start = new Date(p.first_day);
    const end = new Date(p.last_day);
    const leftPct = ((start - minDate) / (1000 * 60 * 60 * 24)) / totalDays * 100;
    const widthPct = ((end - start) / (1000 * 60 * 60 * 24)) / totalDays * 100;
    const color = marginColor(p.margin_pct || 0);
    return `<div class="timeline-bar-row">
      <div class="timeline-bar"
           style="left:${leftPct}%;width:${Math.max(widthPct, 0.3)}%;background:${color}"
           data-project-idx="${i}"></div>
    </div>`;
  }).join('');

  // Build month vertical lines
  let cumulativePx = 0;
  const monthLinesHtml = months.map(m => {
    const pct = (cumulativePx / totalWidth) * 100;
    cumulativePx += m.widthPx;
    return `<div class="timeline-month-line" style="left:${pct}%"></div>`;
  }).join('');

  containerEl.innerHTML = `
    <div class="timeline-container">
      <div class="timeline-left">${leftLabelsHtml}</div>
      <div class="timeline-right" style="width:${totalWidth}px">
        <div class="timeline-header-row">${monthHeaderHtml}</div>
        ${barRowsHtml}
        ${monthLinesHtml}
      </div>
    </div>
  `;

  // Sync vertical scroll between left and right panels
  const leftPanel = containerEl.querySelector('.timeline-left');
  const rightPanel = containerEl.querySelector('.timeline-right');
  let syncing = false;
  if (leftPanel && rightPanel) {
    rightPanel.addEventListener('scroll', () => {
      if (syncing) return;
      syncing = true;
      leftPanel.scrollTop = rightPanel.scrollTop;
      syncing = false;
    });
    leftPanel.addEventListener('scroll', () => {
      if (syncing) return;
      syncing = true;
      rightPanel.scrollTop = leftPanel.scrollTop;
      syncing = false;
    });
  }

  // Tooltip handling
  containerEl.querySelectorAll('.timeline-bar').forEach(bar => {
    bar.addEventListener('mouseover', (e) => {
      const idx = parseInt(bar.dataset.projectIdx);
      const p = projects[idx];
      if (!p) return;
      const teamCount = (p.people_detail || []).length;
      tooltip.innerHTML = `
        <strong>${p.project}</strong><br>
        Cliente: ${p.client || '—'}<br>
        Margine: ${fmtPct(p.margin_pct)}<br>
        GG Target: ${fmtDays(p.days_target)} | Effettivi: ${fmtDays(p.days_actual)}<br>
        Periodo: ${p.first_day} — ${p.last_day}<br>
        Team: ${teamCount} persone
      `;
      tooltip.classList.add('visible');
    });

    bar.addEventListener('mousemove', (e) => {
      tooltip.style.left = (e.clientX + 10) + 'px';
      tooltip.style.top = (e.clientY + 10) + 'px';
    });

    bar.addEventListener('mouseout', () => {
      tooltip.classList.remove('visible');
    });
  });
}
