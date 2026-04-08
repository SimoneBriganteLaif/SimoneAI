// ═══════════════════════════════════════════════════════
// Tab 5: Context Switching
// ═══════════════════════════════════════════════════════

function renderSwitching() {
  const rows = [];
  const personStats = {};

  DATA.employees.forEach(emp => {
    if (!emp.weekly_context_switching || !emp.weekly_context_switching.length) return;
    emp.weekly_context_switching.forEach(cs => {
      if (cs.num_projects === 0) return;
      const tsForWeek = DATA.timesheet.filter(t =>
        t.employee === emp.name && t.dat_month === cs.month && t.num_week === cs.week
      );
      const projectNames = [...new Set(tsForWeek.map(t => t.project))].sort();

      rows.push({
        name: emp.name, month: cs.month, week: cs.week,
        numProjects: cs.num_projects, projects: projectNames.join(', ') || '\u2014',
      });

      if (!personStats[emp.name]) personStats[emp.name] = { totalProjects: 0, weeks: 0, highWeeks: 0 };
      personStats[emp.name].totalProjects += cs.num_projects;
      personStats[emp.name].weeks++;
      if (cs.num_projects >= 3) personStats[emp.name].highWeeks++;
    });
  });

  const totalWeeks = rows.length;
  const highWeeks = rows.filter(r => r.numProjects >= 3).length;
  const avgProjects = totalWeeks ? rows.reduce((s, r) => s + r.numProjects, 0) / totalWeeks : 0;

  document.getElementById('switching-summary').innerHTML = `
    <div class="stat">Settimane totali: <span class="stat-value">${totalWeeks}</span></div>
    <div class="stat">Media progetti/settimana: <span class="stat-value">${fmtNum(avgProjects, 1)}</span></div>
    <div class="stat">Settimane con 3+ progetti: <span class="stat-value" style="color:var(--error)">${highWeeks} (${fmtPct(totalWeeks ? highWeeks/totalWeeks*100 : 0)})</span></div>
  `;

  buildSortableTable(document.getElementById('switching-table'), [
    { label: 'Persona', key: 'name' },
    { label: 'Mese', key: 'month', render: r => new Date(r.month).toLocaleDateString('it-IT', { month: 'short', year: 'numeric' }) },
    { label: 'Settimana', numeric: true, value: r => r.week, render: r => `W${r.week}` },
    { label: 'N. Progetti', numeric: true, value: r => r.numProjects, render: r => {
      const color = r.numProjects >= 3 ? 'var(--error)' : 'inherit';
      return `<span style="color:${color};font-weight:${r.numProjects >= 3 ? '700' : '400'}">${r.numProjects}</span>`;
    }},
    { label: 'Progetti', key: 'projects', render: r => `<span style="font-size:0.78rem">${r.projects}</span>` },
  ], rows, { defaultSort: 3, defaultAsc: false, rowClass: r => r.numProjects >= 3 ? 'cs-high' : '' });

  renderSwitchingChart(personStats);
}

function renderSwitchingChart(personStats) {
  if (charts.switchingChart) charts.switchingChart.destroy();
  const entries = Object.entries(personStats).sort((a, b) => (b[1].totalProjects / b[1].weeks) - (a[1].totalProjects / a[1].weeks));

  charts.switchingChart = new Chart(document.getElementById('switching-chart').getContext('2d'), {
    type: 'bar',
    data: {
      labels: entries.map(e => e[0]),
      datasets: [
        {
          label: 'Media progetti/settimana',
          data: entries.map(e => Math.round(e[1].totalProjects / e[1].weeks * 10) / 10),
          backgroundColor: entries.map(e => {
            const avg = e[1].totalProjects / e[1].weeks;
            return avg >= 3 ? 'rgba(242,73,58,0.6)' : avg >= 2 ? 'rgba(255,165,0,0.6)' : 'rgba(100,194,209,0.6)';
          }),
        },
        {
          label: '% settimane con 3+ progetti',
          data: entries.map(e => Math.round(e[1].highWeeks / e[1].weeks * 100)),
          backgroundColor: 'rgba(242,73,58,0.2)',
          borderColor: 'rgba(242,73,58,0.6)',
          borderWidth: 1,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: { beginAtZero: true },
        x: { ticks: { maxRotation: 45, font: { size: 11 } } }
      }
    }
  });
}
