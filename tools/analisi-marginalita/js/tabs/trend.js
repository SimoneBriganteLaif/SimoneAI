// ═══════════════════════════════════════════════════════
// Tab 7: Trend Temporale (con filtri, YoY, TL breakdown)
// ═══════════════════════════════════════════════════════

let trendFilters = { companies: [], teamLeaders: [], years: [] };
let trendFilterInstances = {};

function initTrendFilters() {
  const container = document.getElementById('trend-filters');
  if (!container) return;
  container.innerHTML = '';

  const companies = [...new Set(DATA.projects.map(p => p.company))].filter(Boolean).sort();
  const tls = [...new Set(DATA.projects.map(p => p.team_leader))].filter(Boolean).sort();
  const years = [...new Set(DATA.projects.map(p => p.dat_order ? getYear(p.dat_order) : null))].filter(Boolean).sort().reverse();

  const companyGroup = document.createElement('div');
  companyGroup.className = 'filter-group';
  companyGroup.innerHTML = '<label>Company</label>';
  trendFilterInstances.company = createMultiSelect(companyGroup, {
    options: companies.map(c => ({ value: c, label: c.toUpperCase() })),
    placeholder: 'Tutte',
    onChange: (vals) => { trendFilters.companies = vals; renderTrend(); }
  });
  container.appendChild(companyGroup);

  const tlGroup = document.createElement('div');
  tlGroup.className = 'filter-group';
  tlGroup.innerHTML = '<label>Team Leader</label>';
  trendFilterInstances.tl = createMultiSelect(tlGroup, {
    options: tls.map(t => ({ value: t, label: t })),
    placeholder: 'Tutti',
    onChange: (vals) => { trendFilters.teamLeaders = vals; renderTrend(); }
  });
  container.appendChild(tlGroup);

  const yearGroup = document.createElement('div');
  yearGroup.className = 'filter-group';
  yearGroup.innerHTML = '<label>Anno</label>';
  trendFilterInstances.year = createMultiSelect(yearGroup, {
    options: years.map(y => ({ value: y, label: y })),
    placeholder: 'Tutti',
    onChange: (vals) => { trendFilters.years = vals; renderTrend(); }
  });
  container.appendChild(yearGroup);

  const resetGroup = document.createElement('div');
  resetGroup.className = 'filter-group';
  resetGroup.style.justifyContent = 'flex-end';
  resetGroup.innerHTML = '<button class="btn btn-sm" onclick="resetTrendFilters()">Reset</button>';
  container.appendChild(resetGroup);
}

function resetTrendFilters() {
  trendFilters = { companies: [], teamLeaders: [], years: [] };
  Object.values(trendFilterInstances).forEach(inst => inst.reset());
  renderTrend();
}

function getFilteredTrendProjects() {
  return DATA.projects.filter(p => {
    if (!p.total_hours || !p.dat_order) return false;
    if (trendFilters.companies.length && !trendFilters.companies.includes(p.company)) return false;
    if (trendFilters.teamLeaders.length && !trendFilters.teamLeaders.includes(p.team_leader)) return false;
    if (trendFilters.years.length && !trendFilters.years.includes(getYear(p.dat_order))) return false;
    return true;
  });
}

function renderTrend() {
  const data = getFilteredTrendProjects();

  // Group by quarter
  const qMap = {};
  data.forEach(p => {
    const q = getQuarter(p.dat_order);
    if (!qMap[q]) qMap[q] = [];
    qMap[q].push(p);
  });
  const quarters = Object.keys(qMap).sort();
  const qData = quarters.map(q => {
    const ps = qMap[q];
    return {
      quarter: q,
      count: ps.length,
      avgRevenue: ps.reduce((s, p) => s + p.revenue, 0) / ps.length,
      avgMargin: ps.reduce((s, p) => s + (p.margin_pct || 0), 0) / ps.length,
      avgOverrun: ps.reduce((s, p) => s + (p.days_overrun || 0), 0) / ps.length,
      avgRevenuePerDay: ps.reduce((s, p) => s + (p.days_target > 0 ? p.revenue / p.days_target : 0), 0) / ps.length,
      avgRatio: (() => { const v = ps.filter(p => p.days_target > 0 && p.days_actual > 0); return v.length ? v.reduce((s, p) => s + p.days_actual / p.days_target, 0) / v.length : null; })(),
      pctHealthy: Math.round(ps.filter(p => (p.margin_pct || 0) >= 70).length / ps.length * 100)
    };
  });

  // Margin trend chart
  if (charts.trendMargin) charts.trendMargin.destroy();
  const marginCtx = document.getElementById('trend-margin-chart');
  if (marginCtx) {
    charts.trendMargin = new Chart(marginCtx.getContext('2d'), {
      type: 'line',
      data: {
        labels: qData.map(d => d.quarter),
        datasets: [{
          label: 'Margine% Medio',
          data: qData.map(d => Math.round(d.avgMargin * 10) / 10),
          borderColor: '#64c2d1',
          backgroundColor: 'rgba(100,194,209,0.15)',
          fill: true,
          tension: 0.3,
          pointRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: { title: { display: true, text: 'Margine% Medio per Trimestre' } },
        scales: { y: { ticks: { callback: v => v + '%' } } }
      }
    });
  }

  // Overrun trend chart
  if (charts.trendOverrun) charts.trendOverrun.destroy();
  const overrunCtx = document.getElementById('trend-overrun-chart');
  if (overrunCtx) {
    charts.trendOverrun = new Chart(overrunCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: qData.map(d => d.quarter),
        datasets: [{
          label: 'Sforamento Medio GG',
          data: qData.map(d => Math.round(d.avgOverrun * 10) / 10),
          backgroundColor: qData.map(d => d.avgOverrun > 0 ? 'rgba(242,73,58,0.5)' : 'rgba(47,218,115,0.5)'),
          borderColor: qData.map(d => d.avgOverrun > 0 ? '#f2493a' : '#2fda73'),
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: { title: { display: true, text: 'Sforamento Medio per Trimestre' } },
        scales: { y: { title: { display: true, text: 'GG' } } }
      }
    });
  }

  // Deal Quality Chart
  if (charts.trendDealQuality) charts.trendDealQuality.destroy();
  const dealCtx = document.getElementById('trend-deal-chart');
  if (dealCtx && qData.length) {
    charts.trendDealQuality = new Chart(dealCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: qData.map(d => d.quarter),
        datasets: [{
          label: '\u20ac/GG Target Medio',
          data: qData.map(d => Math.round(d.avgRevenuePerDay)),
          backgroundColor: 'rgba(100,194,209,0.5)',
          borderColor: '#64c2d1',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: { title: { display: true, text: 'Qualit\u00e0 Deal: Revenue Medio per GG Target' } },
        scales: { y: { beginAtZero: true, ticks: { callback: v => '\u20ac' + v } } }
      }
    });
  }

  // Estimate Accuracy Chart
  if (charts.trendEstimate) charts.trendEstimate.destroy();
  const estCtx = document.getElementById('trend-estimate-chart');
  if (estCtx && qData.length) {
    charts.trendEstimate = new Chart(estCtx.getContext('2d'), {
      type: 'line',
      data: {
        labels: qData.map(d => d.quarter),
        datasets: [
          {
            label: 'Ratio Medio (Effettivo/Target)',
            data: qData.map(d => d.avgRatio ? Math.round(d.avgRatio * 100) / 100 : null),
            borderColor: '#f2493a', backgroundColor: 'rgba(242,73,58,0.1)',
            fill: true, tension: 0.3, pointRadius: 4, yAxisID: 'y', spanGaps: true
          },
          {
            label: '% Progetti Sani (margine \u226570%)',
            data: qData.map(d => d.pctHealthy),
            borderColor: '#2fda73', backgroundColor: 'rgba(47,218,115,0.1)',
            fill: true, tension: 0.3, pointRadius: 4, yAxisID: 'y1', spanGaps: true
          }
        ]
      },
      options: {
        responsive: true,
        plugins: { title: { display: true, text: 'Accuratezza Stime & Salute Progetti' } },
        scales: {
          y: { position: 'left', title: { display: true, text: 'Ratio' }, min: 0 },
          y1: { position: 'right', title: { display: true, text: '% Sani' }, min: 0, max: 100, grid: { drawOnChartArea: false }, ticks: { callback: v => v + '%' } }
        }
      }
    });
  }

  // YoY Comparison Chart
  renderYoYChart(data);

  // TL Breakdown Chart
  renderTLBreakdownChart(data);

  // Quarterly table
  buildSortableTable(document.getElementById('trend-table'), [
    { label: 'Trimestre', key: 'quarter' },
    { label: 'N. Progetti', numeric: true, value: d => d.count, render: d => d.count },
    { label: 'Revenue Medio', numeric: true, value: d => d.avgRevenue, render: d => fmtEur(d.avgRevenue) },
    { label: 'Margine% Medio', numeric: true, value: d => d.avgMargin, render: d => `<span class="${marginClass(d.avgMargin)}">${fmtPct(d.avgMargin)}</span>` },
    { label: 'Sforamento Medio', numeric: true, value: d => d.avgOverrun, render: d => {
      const color = d.avgOverrun > 0 ? 'var(--error)' : 'var(--success)';
      return `<span style="color:${color}">${d.avgOverrun > 0 ? '+' : ''}${fmtDays(d.avgOverrun)} GG</span>`;
    }},
    { label: '\u20ac/GG', numeric: true, value: d => d.avgRevenuePerDay, render: d => fmtEur(d.avgRevenuePerDay) },
    { label: 'Ratio', numeric: true, value: d => d.avgRatio, render: d => {
      if (!d.avgRatio) return '\u2014';
      const color = d.avgRatio > 2 ? 'var(--error)' : d.avgRatio > 1.3 ? 'var(--warning)' : 'var(--success)';
      return `<span style="color:${color};font-weight:600">${fmtNum(d.avgRatio, 2)}x</span>`;
    }},
    { label: '% Sani', numeric: true, value: d => d.pctHealthy, render: d => {
      const color = d.pctHealthy >= 70 ? 'var(--success)' : d.pctHealthy >= 50 ? 'var(--warning)' : 'var(--error)';
      return `<span style="color:${color}">${d.pctHealthy}%</span>`;
    }}
  ], qData, { defaultSort: 0, defaultAsc: true });

  // Tag analytics
  renderTagAnalytics();
}

function renderYoYChart(data) {
  if (charts.trendYoY) charts.trendYoY.destroy();
  const canvas = document.getElementById('trend-yoy-chart');
  if (!canvas) return;

  // Find the two most recent years
  const yearSet = [...new Set(data.map(p => new Date(p.dat_order).getFullYear()))].sort();
  if (yearSet.length < 2) {
    canvas.parentElement.innerHTML = '<p class="text-muted" style="text-align:center;padding:20px">Servono almeno 2 anni di dati per il confronto YoY</p><canvas id="trend-yoy-chart" style="display:none"></canvas>';
    return;
  }
  const currentYear = yearSet[yearSet.length - 1];
  const prevYear = yearSet[yearSet.length - 2];

  const getQuarterData = (year) => {
    const qMap = {};
    data.filter(p => new Date(p.dat_order).getFullYear() === year).forEach(p => {
      const q = Math.ceil((new Date(p.dat_order).getMonth() + 1) / 3);
      if (!qMap[q]) qMap[q] = [];
      qMap[q].push(p);
    });
    return [1, 2, 3, 4].map(q => {
      const ps = qMap[q];
      if (!ps || !ps.length) return null;
      return ps.reduce((s, p) => s + (p.margin_pct || 0), 0) / ps.length;
    });
  };

  const currentData = getQuarterData(currentYear);
  const prevData = getQuarterData(prevYear);

  charts.trendYoY = new Chart(canvas.getContext('2d'), {
    type: 'line',
    data: {
      labels: ['Q1', 'Q2', 'Q3', 'Q4'],
      datasets: [
        {
          label: String(currentYear),
          data: currentData,
          borderColor: '#64c2d1',
          backgroundColor: 'rgba(100,194,209,0.1)',
          fill: true,
          tension: 0.3,
          pointRadius: 5,
          borderWidth: 2,
          spanGaps: true
        },
        {
          label: String(prevYear),
          data: prevData,
          borderColor: '#9b59b6',
          borderDash: [6, 4],
          backgroundColor: 'rgba(155,89,182,0.05)',
          fill: true,
          tension: 0.3,
          pointRadius: 5,
          borderWidth: 2,
          spanGaps: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { title: { display: true, text: `Confronto Margine%: ${currentYear} vs ${prevYear}` } },
      scales: { y: { ticks: { callback: v => v + '%' } } }
    }
  });
}

function renderTLBreakdownChart(data) {
  if (charts.trendTL) charts.trendTL.destroy();
  const canvas = document.getElementById('trend-tl-chart');
  if (!canvas) return;

  // Group by quarter + TL
  const qMap = {};
  const tlSet = new Set();
  data.forEach(p => {
    const q = getQuarter(p.dat_order);
    const tl = p.team_leader || 'N/A';
    tlSet.add(tl);
    if (!qMap[q]) qMap[q] = {};
    if (!qMap[q][tl]) qMap[q][tl] = [];
    qMap[q][tl].push(p);
  });

  const quarters = Object.keys(qMap).sort();
  const tls = [...tlSet].sort();

  const datasets = tls.map((tl, i) => ({
    label: tl,
    data: quarters.map(q => {
      const ps = (qMap[q] || {})[tl];
      if (!ps || !ps.length) return null;
      return Math.round(ps.reduce((s, p) => s + (p.margin_pct || 0), 0) / ps.length * 10) / 10;
    }),
    backgroundColor: PERSON_PALETTE[i % PERSON_PALETTE.length] + '99',
    borderColor: PERSON_PALETTE[i % PERSON_PALETTE.length],
    borderWidth: 1
  }));

  charts.trendTL = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: { labels: quarters, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { title: { display: true, text: 'Margine% per Team Leader per Trimestre' } },
      scales: {
        y: { ticks: { callback: v => v + '%' } },
        x: { ticks: { font: { size: 10 } } }
      }
    }
  });
}

function renderTagAnalytics() {
  const tabEl = document.getElementById('tab-trend');
  let tagSection = tabEl.querySelector('.tag-analytics-section');
  if (!tagSection) {
    tagSection = document.createElement('div');
    tagSection.className = 'tag-analytics-section';
    tabEl.appendChild(tagSection);
  }

  const tagIdx = buildTagIndex();
  const tagAnalytics = [];
  getTagDefinitions().forEach(def => {
    const saleIds = tagIdx[def.id];
    if (!saleIds || !saleIds.size) return;
    const projects = DATA.projects.filter(p => saleIds.has(String(p.sale_id)));
    if (!projects.length) return;
    const n = projects.length;
    tagAnalytics.push({
      tag: def,
      numProjects: n,
      avgMargin: projects.reduce((s, p) => s + (p.margin_pct || 0), 0) / n,
      avgOverrun: projects.reduce((s, p) => s + (p.days_overrun || 0), 0) / n,
      avgRevenue: projects.reduce((s, p) => s + p.revenue, 0) / n,
    });
  });

  if (!tagAnalytics.length) {
    tagSection.innerHTML = '';
    return;
  }

  tagSection.innerHTML = `
    <h3 class="section-title" style="margin-top:20px">Analisi per Tag</h3>
    <div class="card">
      <div class="grid-2">
        <div class="chart-container"><canvas id="tag-margin-chart"></canvas></div>
        <div class="chart-container"><canvas id="tag-overrun-chart"></canvas></div>
      </div>
      <div class="table-scroll" style="margin-top:12px"><table id="tag-analytics-table"><thead><tr></tr></thead><tbody></tbody></table></div>
    </div>
  `;

  // Margin chart
  const sortedByMargin = [...tagAnalytics].sort((a, b) => a.avgMargin - b.avgMargin);
  if (charts.tagMargin) charts.tagMargin.destroy();
  charts.tagMargin = new Chart(document.getElementById('tag-margin-chart').getContext('2d'), {
    type: 'bar',
    data: {
      labels: sortedByMargin.map(d => d.tag.label),
      datasets: [{
        label: 'Margine% Medio',
        data: sortedByMargin.map(d => Math.round(d.avgMargin * 10) / 10),
        backgroundColor: sortedByMargin.map(d => TAG_COLORS[d.tag.color].bg + '99'),
        borderColor: sortedByMargin.map(d => TAG_COLORS[d.tag.color].bg),
        borderWidth: 1
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: { title: { display: true, text: 'Margine% Medio per Tag' }, legend: { display: false } },
      scales: { x: { ticks: { callback: v => v + '%' } } }
    }
  });

  // Overrun chart
  const sortedByOverrun = [...tagAnalytics].sort((a, b) => b.avgOverrun - a.avgOverrun);
  if (charts.tagOverrun) charts.tagOverrun.destroy();
  charts.tagOverrun = new Chart(document.getElementById('tag-overrun-chart').getContext('2d'), {
    type: 'bar',
    data: {
      labels: sortedByOverrun.map(d => d.tag.label),
      datasets: [{
        label: 'Sforamento Medio GG',
        data: sortedByOverrun.map(d => Math.round(d.avgOverrun * 10) / 10),
        backgroundColor: sortedByOverrun.map(d => d.avgOverrun > 0 ? 'rgba(242,73,58,0.5)' : 'rgba(47,218,115,0.5)'),
        borderColor: sortedByOverrun.map(d => d.avgOverrun > 0 ? '#f2493a' : '#2fda73'),
        borderWidth: 1
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: { title: { display: true, text: 'Sforamento Medio GG per Tag' }, legend: { display: false } },
      scales: { x: { title: { display: true, text: 'GG' } } }
    }
  });

  // Tag table
  buildSortableTable(document.getElementById('tag-analytics-table'), [
    { label: 'Tag', render: d => {
      const c = TAG_COLORS[d.tag.color];
      return `<span class="tag-pill" style="background:${c.bg};color:${c.text}">${d.tag.label}</span>`;
    }, value: d => d.tag.label },
    { label: 'N. Progetti', numeric: true, value: d => d.numProjects, render: d => d.numProjects },
    { label: 'Margine% Medio', numeric: true, value: d => d.avgMargin, render: d => `<span class="${marginClass(d.avgMargin)}">${fmtPct(d.avgMargin)}</span>` },
    { label: 'Sforamento Medio', numeric: true, value: d => d.avgOverrun, render: d => {
      const color = d.avgOverrun > 0 ? 'var(--error)' : 'var(--success)';
      return `<span style="color:${color}">${d.avgOverrun > 0 ? '+' : ''}${fmtDays(d.avgOverrun)} GG</span>`;
    }},
    { label: 'Revenue Medio', numeric: true, value: d => d.avgRevenue, render: d => fmtEur(d.avgRevenue) }
  ], tagAnalytics, { defaultSort: 2, defaultAsc: true });
}
