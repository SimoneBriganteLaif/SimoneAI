// ═══════════════════════════════════════════════════════
// Tab 6: Concentrazione Clienti
// ═══════════════════════════════════════════════════════

function renderConcentrazione() {
  const clients = [...DATA.clients].sort((a, b) => b.total_revenue - a.total_revenue);

  buildSortableTable(document.getElementById('concentrazione-table'), [
    { label: 'Cliente', key: 'client' },
    { label: 'N. Progetti', numeric: true, value: c => c.num_projects, render: c => c.num_projects },
    { label: 'Revenue', numeric: true, value: c => c.total_revenue, render: c => fmtEur(c.total_revenue) },
    { label: 'Costo', numeric: true, value: c => c.total_cost, render: c => fmtEur(c.total_cost) },
    { label: 'Margine', numeric: true, value: c => c.total_margin, render: c => fmtEur(c.total_margin) },
    { label: 'Margine%', numeric: true, value: c => c.avg_margin_pct, render: c => `<span class="${marginClass(c.avg_margin_pct)}">${fmtPct(c.avg_margin_pct)}</span>` },
  ], clients, { defaultSort: 2, defaultAsc: false });

  const totalRev = clients.reduce((s, c) => s + c.total_revenue, 0);
  const top5Rev = clients.slice(0, 5).reduce((s, c) => s + c.total_revenue, 0);
  const top10Rev = clients.slice(0, 10).reduce((s, c) => s + c.total_revenue, 0);

  document.getElementById('concentrazione-summary').innerHTML = `
    <div class="stat">Top 5 clienti: <span class="stat-value">${fmtPct(totalRev ? top5Rev/totalRev*100 : 0)}</span> del revenue</div>
    <div class="stat">Top 10 clienti: <span class="stat-value">${fmtPct(totalRev ? top10Rev/totalRev*100 : 0)}</span> del revenue</div>
    <div class="stat">Totale clienti: <span class="stat-value">${clients.length}</span></div>
  `;

  renderParetoChart(clients, totalRev);
}

function renderParetoChart(clients, totalRev) {
  if (charts.paretoChart) charts.paretoChart.destroy();
  const top = clients.slice(0, 20);
  let cumPct = 0;
  const cumData = top.map(c => { cumPct += c.total_revenue / totalRev * 100; return cumPct; });

  charts.paretoChart = new Chart(document.getElementById('pareto-chart').getContext('2d'), {
    type: 'bar',
    data: {
      labels: top.map(c => c.client.length > 25 ? c.client.substring(0, 25) + '...' : c.client),
      datasets: [
        { type: 'bar', label: 'Revenue', data: top.map(c => c.total_revenue), backgroundColor: 'rgba(100,194,209,0.6)', yAxisID: 'y' },
        { type: 'line', label: '% Cumulativa', data: cumData, borderColor: '#f2493a', backgroundColor: 'transparent', pointRadius: 3, tension: 0.2, yAxisID: 'y1' }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: { beginAtZero: true, position: 'left', title: { display: true, text: 'Revenue (\u20ac)' }, ticks: { callback: v => fmtEur(v) } },
        y1: { beginAtZero: true, max: 100, position: 'right', title: { display: true, text: '% Cumulativa' }, grid: { drawOnChartArea: false }, ticks: { callback: v => v + '%' } },
        x: { ticks: { maxRotation: 45, font: { size: 10 } } }
      }
    }
  });
}
