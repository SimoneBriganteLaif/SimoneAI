// ═══════════════════════════════════════════════════════
// Costanti e Formatters
// ═══════════════════════════════════════════════════════

const TAG_COLORS = {
  red:     { bg: '#f2493a', text: '#fff', bgLight: 'rgba(242,73,58,0.12)' },
  green:   { bg: '#2fda73', text: '#fff', bgLight: 'rgba(47,218,115,0.12)' },
  neutral: { bg: '#e0e0e0', text: '#333', bgLight: 'rgba(0,0,0,0.05)' }
};

const PERSON_PALETTE = [
  '#64c2d1', '#f2493a', '#2fda73', '#ffa500', '#9b59b6',
  '#e67e22', '#1abc9c', '#e74c3c', '#3498db', '#f39c12'
];

const fmtEur = (v) => {
  if (v == null || isNaN(v)) return '\u2014';
  return '\u20ac ' + Number(v).toLocaleString('it-IT', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
};
const fmtPct = (v) => {
  if (v == null || isNaN(v)) return '\u2014';
  return Number(v).toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
};
const fmtDays = (v) => {
  if (v == null || isNaN(v)) return '\u2014';
  return Number(v).toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
};
const fmtHours = (v) => {
  if (v == null || isNaN(v)) return '\u2014';
  return Number(v).toLocaleString('it-IT', { minimumFractionDigits: 0, maximumFractionDigits: 1 });
};
const fmtNum = (v, d = 0) => {
  if (v == null || isNaN(v)) return '\u2014';
  return Number(v).toLocaleString('it-IT', { minimumFractionDigits: d, maximumFractionDigits: d });
};

// Soglie margine: <0% rosso (perdita), <45% rosso (sotto target), 45-70% giallo, >=70% verde
function marginClass(pct) {
  if (pct < 45) return 'margin-red';
  if (pct < 70) return 'margin-yellow';
  return 'margin-green';
}
function marginRowClass(pct) {
  if (pct < 45) return 'row-margin-red';
  if (pct < 70) return 'row-margin-yellow';
  return 'row-margin-green';
}
function marginColor(pct) {
  if (pct < 45) return '#f2493a';
  if (pct < 70) return '#e6c200';
  return '#2fda73';
}

function getQuarter(dateStr) {
  const d = new Date(dateStr);
  const q = Math.ceil((d.getMonth() + 1) / 3);
  return `${d.getFullYear()}-Q${q}`;
}
function getYear(dateStr) {
  return new Date(dateStr).getFullYear().toString();
}

function isRecurring(p) {
  return /canone|manutenzione/i.test(p.project);
}

function satColor(pct) {
  if (pct > 90) return 'var(--error)';
  if (pct >= 70) return 'var(--success)';
  if (pct >= 60) return 'var(--warning)';
  return 'var(--muted)';
}

function satBgColor(pct) {
  if (pct > 90) return 'rgba(242,73,58,0.25)';
  if (pct >= 70) return 'rgba(47,218,115,0.2)';
  if (pct >= 60) return 'rgba(255,165,0,0.2)';
  return 'rgba(122,122,122,0.1)';
}

const STATUS_LABELS = {
  'invoiced_and_paid': 'Fatturato e pagato',
  'totally_invoiced': 'Fatturato',
  'partially_invoiced': 'Parzialmente fatturato',
  'invoiced_and_partially_paid': 'Fatt. parz. pagato',
  'to_be_invoiced': 'Da fatturare',
  'undefined_tranches': 'Tranche indefinite'
};
