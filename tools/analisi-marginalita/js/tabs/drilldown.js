// ═══════════════════════════════════════════════════════
// Tab 2: Drill-down Progetto (+ renderer condiviso)
// ═══════════════════════════════════════════════════════

let drilldownSelect = null;

function initDrilldownSelect() {
  const container = document.querySelector('#tab-drilldown .filters');
  container.innerHTML = '<div class="filter-group"><label>Progetto</label><div id="drilldown-select-wrap"></div></div>';

  const sorted = [...DATA.projects].sort((a, b) => a.project.localeCompare(b.project, 'it'));
  drilldownSelect = createSearchSelect(document.getElementById('drilldown-select-wrap'), {
    options: sorted.map(p => ({ value: String(p.sale_id), label: `${p.project} (${p.client})` })),
    placeholder: '\u2014 Seleziona progetto \u2014',
    onChange: (val) => renderDrilldown(val)
  });
}

function renderDrilldown(saleIdStr) {
  const container = document.getElementById('drilldown-content');
  const saleId = parseInt(saleIdStr || drilldownSelect?.getSelected());
  if (!saleId) {
    container.innerHTML = '<p class="text-muted" style="padding:40px;text-align:center">Seleziona un progetto per visualizzare il dettaglio</p>';
    return;
  }
  const project = DATA.projects.find(p => p.sale_id === saleId);
  if (!project) { container.innerHTML = '<p>Progetto non trovato</p>'; return; }
  container.innerHTML = '';
  renderDrilldownContent(project, container);
}

function renderDrilldownContent(project, container) {
  const p = project;
  const totalCost = (p.internal_cost || 0) + (p.external_cost || 0);

  container.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <h3 style="font-size:1.05rem">${p.project} <span class="text-muted" style="font-weight:400;font-size:0.85rem">\u2014 ${p.client}</span></h3>
      <button class="btn btn-sm go-to-drilldown">Apri in Drill-down completo</button>
    </div>
    <div class="kpi-row">
      <div class="kpi-box"><div class="kpi-label">Revenue</div><div class="kpi-value">${fmtEur(p.revenue)}</div></div>
      <div class="kpi-box"><div class="kpi-label">Costo Totale</div><div class="kpi-value">${fmtEur(totalCost)}</div></div>
      <div class="kpi-box"><div class="kpi-label">Margine</div><div class="kpi-value" style="color:${marginColor(p.margin_pct)}">${fmtEur(p.margin)}</div></div>
      <div class="kpi-box"><div class="kpi-label">Margine%</div><div class="kpi-value" style="color:${marginColor(p.margin_pct)}">${fmtPct(p.margin_pct)}</div></div>
      <div class="kpi-box"><div class="kpi-label">GG Target</div><div class="kpi-value">${fmtDays(p.days_target)}</div></div>
      <div class="kpi-box"><div class="kpi-label">GG Effettivi</div><div class="kpi-value">${fmtDays(p.days_actual)}</div></div>
      <div class="kpi-box"><div class="kpi-label">Periodo</div><div class="kpi-value" style="font-size:0.8rem">${p.first_day || '?'} \u2014 ${p.last_day || '?'}</div></div>
    </div>

    <h4 class="section-title">Struttura Costi & Team</h4>
    <div class="drill-cost-layout">
      <div class="waterfall-side">
        <div class="waterfall-container"></div>
      </div>
      <div class="team-side">
        <div class="table-scroll">
          <table class="drill-people-table">
            <thead><tr>
              <th>Persona</th><th>Ruolo</th><th style="text-align:right">Ore</th><th style="text-align:right">GG</th><th style="text-align:right">Costo</th><th style="text-align:right">% sul totale</th>
            </tr></thead>
            <tbody>
              ${(p.people_detail || []).map(pd => {
                const days = pd.hours / 8;
                const pctTotal = totalCost > 0 ? (pd.cost / totalCost * 100) : 0;
                return `<tr>
                  <td>${pd.employee}</td><td>${pd.role}</td>
                  <td class="num">${fmtHours(pd.hours)}</td><td class="num">${fmtDays(days)}</td>
                  <td class="num">${fmtEur(pd.cost)}</td><td class="num">${fmtPct(pctTotal)}</td>
                </tr>`;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <h4 class="section-title">Curva GG cumulativi vs Target</h4>
    <div class="cumulative-container"></div>

    <h4 class="section-title">Heatmap Settimanale (ore per persona)</h4>
    <div class="heatmap-container"></div>

    <div class="tag-section">
      <h4 class="section-title">Tag & Note</h4>
      <div class="tag-group-header">Negativi</div>
      <div class="tag-picker tag-picker-red"></div>
      <div class="tag-group-header">Positivi</div>
      <div class="tag-picker tag-picker-green"></div>
      <div class="tag-group-header">Tipologia</div>
      <div class="tag-picker tag-picker-neutral"></div>
      <div class="notes-split">
        <div><label>Note positive</label><textarea class="positive-notes" placeholder="Cosa è andato bene..."></textarea></div>
        <div><label>Note negative</label><textarea class="negative-notes" placeholder="Cosa è andato male..."></textarea></div>
      </div>
      <div class="mt-8"><button class="btn btn-primary btn-sm save-tags-btn">Salva</button></div>
    </div>
  `;

  // Go-to-drilldown button
  container.querySelector('.go-to-drilldown')?.addEventListener('click', () => {
    if (drilldownSelect) drilldownSelect.setSelected(String(p.sale_id));
    switchToTab('tab-drilldown');
    renderDrilldown(String(p.sale_id));
  });

  try { renderWaterfallChart(p, container.querySelector('.waterfall-container')); } catch(e) { console.error('Waterfall error:', e); }
  try { renderCumulativeChart(p, container.querySelector('.cumulative-container')); } catch(e) { console.error('Cumulative error:', e); }
  try { renderHeatmap(p, container.querySelector('.heatmap-container')); } catch(e) { console.error('Heatmap error:', e); }
  try { renderTagSection(p, container); } catch(e) { console.error('TagSection error:', e); }
}

function renderCumulativeChart(project, container) {
  const ts = DATA.timesheet.filter(t => t.id_sale === project.sale_id);
  if (!ts.length) {
    container.innerHTML = '<p class="text-muted">Nessun dato timesheet disponibile</p>';
    return;
  }

  const people = [...new Set(ts.map(t => t.employee))].sort();

  container.innerHTML = `
    <div class="chart-controls">
      <div class="filter-group">
        <label>Granularità</label>
        <div class="granularity-toggle">
          <button class="active" data-gran="week">Settimana</button>
          <button data-gran="month">Mese</button>
        </div>
      </div>
      <div class="filter-group">
        <label>Persone</label>
        <div class="cum-person-filter"></div>
      </div>
      <div class="filter-group">
        <label>Da</label>
        <input type="date" class="cum-date-from">
      </div>
      <div class="filter-group">
        <label>A</label>
        <input type="date" class="cum-date-to">
      </div>
    </div>
    <canvas class="cumulative-canvas" style="max-height:300px"></canvas>
  `;

  let currentGran = 'week';
  let selectedPeople = [];

  // Person multi-select
  createMultiSelect(container.querySelector('.cum-person-filter'), {
    options: people.map(p => ({ value: p, label: p })),
    placeholder: 'Tutte',
    onChange: (vals) => { selectedPeople = vals; rebuild(); }
  });

  // Granularity toggle
  container.querySelectorAll('.granularity-toggle button').forEach(btn => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('.granularity-toggle button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentGran = btn.dataset.gran;
      rebuild();
    });
  });

  // Date filters
  const dateFrom = container.querySelector('.cum-date-from');
  const dateTo = container.querySelector('.cum-date-to');
  dateFrom.addEventListener('change', rebuild);
  dateTo.addEventListener('change', rebuild);

  function rebuild() {
    // Destroy old chart
    if (container._cumulativeChart) {
      container._cumulativeChart.destroy();
      container._cumulativeChart = null;
    }

    // Filter data
    let filtered = ts;
    if (selectedPeople.length > 0) {
      filtered = filtered.filter(t => selectedPeople.includes(t.employee));
    }
    if (dateFrom.value) {
      filtered = filtered.filter(t => {
        const ref = currentGran === 'week' ? t.week_start : t.dat_month;
        return ref >= dateFrom.value;
      });
    }
    if (dateTo.value) {
      filtered = filtered.filter(t => {
        const ref = currentGran === 'week' ? t.week_start : t.dat_month;
        return ref <= dateTo.value;
      });
    }

    if (!filtered.length) return;

    // Group by period
    const periodMap = {};
    const personPeriodMap = {};
    const activePeople = [...new Set(filtered.map(t => t.employee))].sort();

    filtered.forEach(t => {
      const key = currentGran === 'week'
        ? `${t.dat_month}_w${t.num_week}`
        : t.dat_month;
      if (!periodMap[key]) periodMap[key] = { key, month: t.dat_month, week: t.num_week, hours: 0 };
      periodMap[key].hours += t.hours;

      const pk = `${t.employee}|${key}`;
      personPeriodMap[pk] = (personPeriodMap[pk] || 0) + t.hours;
    });

    const periods = Object.values(periodMap).sort((a, b) => {
      if (a.month !== b.month) return a.month.localeCompare(b.month);
      return (a.week || 0) - (b.week || 0);
    });

    // Labels
    const labels = periods.map(p => {
      if (currentGran === 'week') return `${p.month.substring(0,7)} W${p.week}`;
      return p.month;
    });

    // Cumulative line data
    let cum = 0;
    const cumData = periods.map(p => {
      cum += p.hours / 8;
      return Math.round(cum * 10) / 10;
    });

    const targetLine = Array(periods.length).fill(project.days_target);

    // Bar datasets per person
    const barDatasets = activePeople.map((person, i) => ({
      label: person,
      data: periods.map(p => {
        const h = personPeriodMap[`${person}|${p.key}`] || 0;
        return Math.round((h / 8) * 10) / 10;
      }),
      backgroundColor: (PERSON_PALETTE[i % PERSON_PALETTE.length]) + '80',
      borderColor: PERSON_PALETTE[i % PERSON_PALETTE.length],
      borderWidth: 1,
      type: 'bar',
      yAxisID: 'y1',
      stack: 'people'
    }));

    // Line datasets
    const lineDatasets = [
      { label: 'GG Cumulativi', data: cumData, borderColor: '#64c2d1', backgroundColor: 'rgba(100,194,209,0.1)', fill: true, tension: 0.3, pointRadius: 2, type: 'line', yAxisID: 'y' },
      { label: 'GG Target', data: targetLine, borderColor: '#f2493a', borderDash: [6, 4], pointRadius: 0, fill: false, type: 'line', yAxisID: 'y' }
    ];

    const canvas = container.querySelector('.cumulative-canvas');
    container._cumulativeChart = new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels,
        datasets: [...lineDatasets, ...barDatasets]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'top' } },
        scales: {
          y: { beginAtZero: true, title: { display: true, text: 'GG Cumulativi' }, position: 'left' },
          y1: { beginAtZero: true, title: { display: true, text: 'GG per Periodo' }, position: 'right', grid: { drawOnChartArea: false }, stacked: true },
          x: { ticks: { maxRotation: 45, font: { size: 10 } }, stacked: true }
        }
      }
    });
  }

  rebuild();
}

function renderHeatmap(project, container) {
  const ts = DATA.timesheet.filter(t => t.id_sale === project.sale_id);
  if (!ts.length) { container.innerHTML = '<p class="text-muted">Nessun dato timesheet disponibile</p>'; return; }

  const MONTH_SHORT_IT = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
  let currentGran = 'week';

  container.innerHTML = `
    <div class="heatmap-controls">
      <div class="granularity-toggle">
        <button class="active" data-hm-gran="week">Settimana</button>
        <button data-hm-gran="month">Mese</button>
      </div>
    </div>
    <div class="heatmap-wrapper"><div class="heatmap-table-wrap"></div></div>
  `;

  container.querySelectorAll('.heatmap-controls .granularity-toggle button').forEach(btn => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('.heatmap-controls .granularity-toggle button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentGran = btn.dataset.hmGran;
      buildTable();
    });
  });

  function buildTable() {
    const people = [...new Set(ts.map(t => t.employee))].sort();

    let periodKeys;
    if (currentGran === 'week') {
      periodKeys = [...new Set(ts.map(t => `${t.dat_month}_w${t.num_week}`))];
      periodKeys.sort((a, b) => {
        const [am, aw] = a.split('_w');
        const [bm, bw] = b.split('_w');
        if (am !== bm) return am.localeCompare(bm);
        return parseInt(aw) - parseInt(bw);
      });
    } else {
      periodKeys = [...new Set(ts.map(t => t.dat_month))].sort();
    }

    // Build matrix
    const matrix = {};
    let maxHours = 0;
    ts.forEach(t => {
      const pk = currentGran === 'week' ? `${t.dat_month}_w${t.num_week}` : t.dat_month;
      const key = `${t.employee}|${pk}`;
      matrix[key] = (matrix[key] || 0) + t.hours;
      if (matrix[key] > maxHours) maxHours = matrix[key];
    });

    // Labels
    const periodLabels = periodKeys.map(k => {
      if (currentGran === 'week') {
        const [m, w] = k.split('_w');
        return `${m.substring(5,7)}/${m.substring(2,4)} W${w}`;
      } else {
        // k is like "2025-03" or "2025-03-01"
        const parts = k.split('-');
        const monthIdx = parseInt(parts[1], 10) - 1;
        const yearShort = parts[0].substring(2);
        return `${MONTH_SHORT_IT[monthIdx]} '${yearShort}`;
      }
    });

    // Row totals and column totals
    const colTotals = periodKeys.map(() => 0);
    let grandTotal = 0;

    // Pre-calculate person totals
    const personTotals = {};
    people.forEach(person => {
      let total = 0;
      periodKeys.forEach(pk => { total += matrix[`${person}|${pk}`] || 0; });
      personTotals[person] = total;
    });

    let html = '<table class="heatmap-table"><thead><tr><th class="sticky-left">Persona</th>';
    html += '<th class="sticky-left" style="left:130px;background:#f0f0f0">Totale</th>';
    periodLabels.forEach(l => { html += `<th>${l}</th>`; });
    html += '</tr></thead><tbody>';

    people.forEach(person => {
      html += `<tr><th class="sticky-left" style="text-align:left;white-space:nowrap">${person}</th>`;
      html += `<td class="sticky-left num" style="left:130px;background:#f0f0f0;font-weight:700">${personTotals[person]}</td>`;
      periodKeys.forEach((pk, ci) => {
        const hours = matrix[`${person}|${pk}`] || 0;
        colTotals[ci] += hours;
        const intensity = maxHours > 0 ? hours / maxHours : 0;
        const bg = hours > 0 ? `rgba(100,194,209,${0.1 + intensity * 0.7})` : 'transparent';
        html += `<td class="hm-cell" style="background:${bg}" title="${person}: ${hours}h">${hours > 0 ? hours : ''}</td>`;
      });
      grandTotal += personTotals[person];
      html += '</tr>';
    });

    // Totals row
    html += '<tr class="totals-row"><th class="sticky-left" style="text-align:left;white-space:nowrap"><strong>Totale</strong></th>';
    html += `<td class="sticky-left num" style="left:130px;background:#f0f0f0"><strong>${grandTotal}</strong></td>`;
    colTotals.forEach(ct => {
      html += `<td class="num">${ct > 0 ? ct : ''}</td>`;
    });
    html += '</tr>';

    html += '</tbody></table>';
    container.querySelector('.heatmap-table-wrap').innerHTML = html;
  }

  buildTable();
}

function renderWaterfallChart(project, container) {
  const p = project;
  const revenue = p.revenue || 0;
  const internal_cost = p.internal_cost || 0;
  const external_cost = p.external_cost || 0;
  const margin = p.margin || 0;

  container.innerHTML = `<canvas class="waterfall-canvas" style="max-height:220px"></canvas>`;

  const canvas = container.querySelector('.waterfall-canvas');

  const waterfallChart = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: ['Revenue', 'Costo Interno', 'Costo Esterno', 'Margine'],
      datasets: [{
        data: [
          [0, revenue],
          [revenue - internal_cost, revenue],
          [margin, revenue - internal_cost],
          margin >= 0 ? [0, margin] : [margin, 0]
        ],
        backgroundColor: [
          'rgba(47,218,115,0.6)',
          'rgba(242,73,58,0.6)',
          'rgba(255,165,0,0.6)',
          margin >= 0 ? 'rgba(47,218,115,0.6)' : 'rgba(242,73,58,0.6)'
        ],
        borderColor: [
          '#2fda73',
          '#f2493a',
          '#ffa500',
          margin >= 0 ? '#2fda73' : '#f2493a'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const raw = ctx.raw;
              const val = Math.abs(raw[1] - raw[0]);
              return fmtEur(val);
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: (v) => fmtEur(v) }
        }
      }
    }
  });

  if (charts) charts['waterfall_' + p.sale_id] = waterfallChart;
}

function renderTagSection(project, container) {
  const pt = getProjectTags(project.sale_id);
  const selectedTags = new Set(pt.tags || []);

  // Populate each color group
  ['red', 'green', 'neutral'].forEach(color => {
    const picker = container.querySelector(`.tag-picker-${color}`);
    if (!picker) return;
    const defs = getTagDefinitions(color);
    picker.innerHTML = defs.map(def => {
      const c = TAG_COLORS[def.color];
      const isSelected = selectedTags.has(def.id);
      const bgColor = isSelected ? c.bg : c.bgLight;
      const txtColor = isSelected ? c.text : (def.color === 'neutral' ? '#555' : c.bg);
      return `<span class="tag-pill${isSelected ? ' selected' : ''}" data-tag-id="${def.id}" style="background:${bgColor};color:${txtColor}">${def.label}</span>`;
    }).join(' ');
  });

  // Toggle selection on click
  container.querySelectorAll('.tag-picker .tag-pill').forEach(pill => {
    pill.addEventListener('click', () => pill.classList.toggle('selected'));
  });

  // Fill notes
  const posNotes = container.querySelector('.positive-notes');
  const negNotes = container.querySelector('.negative-notes');
  if (posNotes) posNotes.value = pt.positive_notes || '';
  if (negNotes) negNotes.value = pt.negative_notes || '';

  // Save
  container.querySelector('.save-tags-btn').addEventListener('click', () => {
    const tags = [];
    container.querySelectorAll('.tag-picker .tag-pill.selected').forEach(pill => {
      tags.push(pill.dataset.tagId);
    });
    setProjectTags(project.sale_id, {
      tags,
      positive_notes: posNotes ? posNotes.value : '',
      negative_notes: negNotes ? negNotes.value : ''
    });
    const btn = container.querySelector('.save-tags-btn');
    btn.textContent = 'Salvato!';
    btn.style.background = 'var(--success)';
    setTimeout(() => { btn.textContent = 'Salva'; btn.style.background = ''; }, 1500);
  });
}
