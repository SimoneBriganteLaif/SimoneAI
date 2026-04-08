// ═══════════════════════════════════════════════════════
// App: Data loading, tab navigation, init
// ═══════════════════════════════════════════════════════

let DATA = { projects: [], timesheet: [], employees: [], clients: [], annotations: {} };
let charts = {};

// Tab navigation
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
    const tab = btn.dataset.tab;
    if (tab === 'tab-drilldown') renderDrilldown();
    if (tab === 'tab-saturazione') renderSaturation();
    if (tab === 'tab-stime') renderStime();
    if (tab === 'tab-concentrazione') renderConcentrazione();
    if (tab === 'tab-trend') renderTrend();
    if (tab === 'tab-timeline') renderTimeline();
    if (tab === 'tab-impostazioni') renderImpostazioni();
  });
});

function switchToTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.toggle('active', c.id === tabId));
}

// Data loading
async function loadData() {
  try {
    const [projects, timesheet, employees, clients, annotationsFile] = await Promise.all([
      fetch('data/projects.json').then(r => r.json()),
      fetch('data/timesheet.json').then(r => r.json()),
      fetch('data/employees.json').then(r => r.json()),
      fetch('data/clients.json').then(r => r.json()),
      fetch('data/annotations.json').then(r => r.json()).catch(() => ({})),
    ]);
    DATA = { projects, timesheet, employees, clients, annotations: annotationsFile };
    loadTagStore();
    init();
  } catch (e) {
    console.error('Errore caricamento dati:', e);
    document.getElementById('fetch-warning').style.display = 'block';
    document.getElementById('loading-overlay').innerHTML = `
      <div style="text-align:center">
        <div style="margin-bottom:12px;color:var(--error)">Impossibile caricare i dati</div>
        <div style="font-size:0.85rem;color:var(--muted)">Avvia con: <code>python3 -m http.server 8888</code></div>
      </div>
    `;
  }
}

function init() {
  document.getElementById('loading-overlay').style.display = 'none';
  initClassificaFilters();
  renderClassifica();
  initDrilldownSelect();
  initSaturation();
  initTimeline();
  initStimeFilters();
  initTrendFilters();
}

loadData();
