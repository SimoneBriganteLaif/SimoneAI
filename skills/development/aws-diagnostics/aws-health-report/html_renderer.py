"""
Renderer HTML per AWS Health Report.

Genera un file HTML self-contained con CSS e JS inline.
"""

import html

from chart_svg import line_chart, status_code_bar_chart


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
:root {
  --ok: #22c55e; --ok-bg: #f0fdf4; --ok-border: #bbf7d0;
  --warn: #f59e0b; --warn-bg: #fffbeb; --warn-border: #fde68a;
  --fail: #ef4444; --fail-bg: #fef2f2; --fail-border: #fecaca;
  --bg: #f8fafc; --surface: #ffffff; --text: #1e293b; --muted: #64748b;
  --border: #e2e8f0; --accent: #3b82f6;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg);
       color: var(--text); line-height: 1.5; padding: 24px; max-width: 1000px; margin: 0 auto; }
h1 { font-size: 1.5rem; margin-bottom: 4px; }
h2 { font-size: 1.2rem; color: var(--text); margin: 0; display: inline; }
h3 { font-size: 1rem; color: var(--muted); margin: 16px 0 8px; }
.subtitle { color: var(--muted); font-size: 0.85rem; margin-bottom: 20px; }
header { margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }

/* Dashboard cards */
.dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
             gap: 12px; margin-bottom: 20px; }
.card { background: var(--surface); border-radius: 8px; padding: 16px;
        border: 1px solid var(--border); }
.card--ok { border-left: 4px solid var(--ok); }
.card--warn { border-left: 4px solid var(--warn); }
.card--fail { border-left: 4px solid var(--fail); }
.card h3 { margin: 0 0 8px; color: var(--text); font-size: 0.9rem; }
.card .detail { font-size: 0.85rem; color: var(--muted); }

.light { width: 10px; height: 10px; border-radius: 50%; display: inline-block;
         margin-right: 6px; vertical-align: middle; }
.light--ok { background: var(--ok); box-shadow: 0 0 6px var(--ok); }
.light--warn { background: var(--warn); box-shadow: 0 0 6px var(--warn); }
.light--fail { background: var(--fail); box-shadow: 0 0 6px var(--fail); }

.verdict { display: inline-block; padding: 4px 12px; border-radius: 4px;
           font-weight: 600; font-size: 0.9rem; }
.verdict--ok { background: var(--ok-bg); color: #166534; border: 1px solid var(--ok-border); }
.verdict--warn { background: var(--warn-bg); color: #92400e; border: 1px solid var(--warn-border); }
.verdict--fail { background: var(--fail-bg); color: #991b1b; border: 1px solid var(--fail-border); }

/* Collapsible sections */
details { background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
          margin-bottom: 16px; overflow: hidden; }
summary { padding: 14px 18px; cursor: pointer; background: var(--surface);
          user-select: none; list-style: none; display: flex; align-items: center; gap: 8px; }
summary::-webkit-details-marker { display: none; }
summary::before { content: "\\25B6"; font-size: 0.7rem; color: var(--muted);
                  transition: transform 0.2s; }
details[open] > summary::before { transform: rotate(90deg); }
details > .content { padding: 0 18px 18px; }

/* Tables */
table { width: 100%; border-collapse: collapse; font-size: 0.82rem; margin: 8px 0; }
th { background: #f1f5f9; padding: 8px 10px; text-align: left; font-weight: 600;
     border-bottom: 2px solid var(--border); cursor: pointer; user-select: none;
     white-space: nowrap; }
th:hover { background: #e2e8f0; }
th .sort-arrow { font-size: 0.65rem; margin-left: 4px; color: var(--muted); }
td { padding: 6px 10px; border-bottom: 1px solid #f1f5f9; word-break: break-all; }
tr:hover td { background: #f8fafc; }
tr.severity-critical td { background: #fef2f2; }
tr.severity-error td { background: #fff7ed; }
tr.severity-warn td { background: #fffbeb; }
tr.status-5xx td { background: #fef2f2; }
tr.status-4xx td { background: #fff7ed; }

/* Filter input */
.filter-box { width: 100%; padding: 8px 12px; border: 1px solid var(--border);
              border-radius: 6px; font-size: 0.85rem; margin-bottom: 8px; outline: none; }
.filter-box:focus { border-color: var(--accent); box-shadow: 0 0 0 2px #3b82f620; }

/* Charts */
.chart-container { margin: 12px 0; }

/* Misc */
.empty { color: var(--muted); font-style: italic; padding: 12px 0; }
.tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem;
       font-weight: 600; }
.tag--ok { background: var(--ok-bg); color: #166534; }
.tag--warn { background: var(--warn-bg); color: #92400e; }
.tag--fail { background: var(--fail-bg); color: #991b1b; }

footer { margin-top: 32px; padding-top: 16px; border-top: 1px solid var(--border);
         color: var(--muted); font-size: 0.8rem; text-align: center; }
"""

# ---------------------------------------------------------------------------
# JS (sorting + filtering)
# ---------------------------------------------------------------------------

JS = """
document.addEventListener('DOMContentLoaded', function() {
  // Table sorting
  document.querySelectorAll('th[data-sort]').forEach(function(th) {
    th.addEventListener('click', function() {
      var table = th.closest('table');
      var tbody = table.querySelector('tbody');
      var rows = Array.from(tbody.querySelectorAll('tr'));
      var col = parseInt(th.dataset.sort);
      var asc = th.dataset.dir !== 'asc';
      th.dataset.dir = asc ? 'asc' : 'desc';
      // Reset arrows
      table.querySelectorAll('th .sort-arrow').forEach(function(a) { a.textContent = ''; });
      th.querySelector('.sort-arrow').textContent = asc ? ' \\u25B2' : ' \\u25BC';
      rows.sort(function(a, b) {
        var av = a.cells[col].textContent.trim();
        var bv = b.cells[col].textContent.trim();
        var an = parseFloat(av), bn = parseFloat(bv);
        if (!isNaN(an) && !isNaN(bn)) return asc ? an - bn : bn - an;
        return asc ? av.localeCompare(bv) : bv.localeCompare(av);
      });
      rows.forEach(function(r) { tbody.appendChild(r); });
    });
  });
  // Table filtering
  document.querySelectorAll('.filter-box').forEach(function(input) {
    input.addEventListener('input', function() {
      var filter = input.value.toLowerCase();
      var table = input.nextElementSibling;
      if (!table || table.tagName !== 'TABLE') return;
      table.querySelectorAll('tbody tr').forEach(function(row) {
        row.style.display = row.textContent.toLowerCase().includes(filter) ? '' : 'none';
      });
    });
  });
});
"""


# ---------------------------------------------------------------------------
# Renderer principale
# ---------------------------------------------------------------------------

def render_report(data: dict) -> str:
    """
    Genera l'HTML completo del report.

    Args:
        data: {
            "project": str, "env": str, "timestamp": str,
            "profile": str, "region": str, "hours": int, "log_window": str,
            "triage": {...}, "ecs_deployment": {...}, "ecs_instances": {...},
            "ecs_metrics": {...}, "ecs_failures": {...},
            "rds_status": {...}, "rds_metrics": {...},
            "logs_errors": {...}, "logs_http_errors": {...}, "logs_status_codes": {...},
            "s3_data": {...}, "s3_frontend": {...}
        }
    """
    parts = []

    # Head
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="it">')
    parts.append('<head>')
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    title = f"AWS Health Report — {esc(data['project'])} ({esc(data['env'])})"
    parts.append(f'<title>{title}</title>')
    parts.append(f'<style>{CSS}</style>')
    parts.append('</head>')
    parts.append('<body>')

    # Header
    parts.append('<header>')
    parts.append(f'<h1>{title}</h1>')
    parts.append(f'<p class="subtitle">Generato: {esc(data["timestamp"])} '
                 f'| Profilo: {esc(data["profile"])} | Regione: {esc(data["region"])} '
                 f'| Metriche: ultime {data["hours"]}h | Log: ultimi {esc(data["log_window"])}</p>')
    parts.append('</header>')

    # Dashboard
    parts.append(_render_dashboard(data.get("triage", {})))

    # ECS Section
    parts.append(_render_ecs_section(data))

    # RDS Section
    parts.append(_render_rds_section(data))

    # Logs Section
    parts.append(_render_logs_section(data))

    # S3 Section
    parts.append(_render_s3_section(data))

    # Footer
    parts.append(f'<footer>LAIF aws-health-report v1.0 — {esc(data["timestamp"])}</footer>')

    # JS
    parts.append(f'<script>{JS}</script>')

    parts.append('</body>')
    parts.append('</html>')

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Sezioni
# ---------------------------------------------------------------------------

def _render_dashboard(triage: dict) -> str:
    if "error" in triage:
        return f'<div class="empty">Triage non disponibile: {esc(triage["error"])}</div>'

    checks = triage.get("checks", [])
    verdict = triage.get("verdict", "OK")

    parts = ['<div class="dashboard">']
    for c in checks:
        s = c["status"].lower()
        parts.append(
            f'<div class="card card--{s}">'
            f'<h3><span class="light light--{s}"></span>{esc(c["service"])}</h3>'
            f'<div class="detail">{esc(c["detail"])}</div>'
            f'</div>'
        )
    parts.append('</div>')

    v = verdict.lower()
    parts.append(f'<p>Verdetto: <span class="verdict verdict--{v}">{verdict}</span></p>')

    return "\n".join(parts)


def _render_ecs_section(data: dict) -> str:
    parts = ['<details open>', '<summary><h2>ECS — Elastic Container Service</h2></summary>',
             '<div class="content">']

    # Deployment
    dep = data.get("ecs_deployment", {})
    if "error" not in dep:
        deployments = dep.get("deployments", [])
        if deployments:
            parts.append('<h3>Deployment</h3>')
            parts.append(_table(
                ["Status", "Rollout", "Running/Desired", "Task Def", "Aggiornato"],
                [[d["status"], d["rollout"], f"{d['running']}/{d['desired']}",
                  d["task_def"], d["updated"]] for d in deployments],
            ))

        events = dep.get("events", [])
        if events:
            parts.append('<h3>Ultimi Eventi</h3>')
            parts.append(_table(
                ["Timestamp", "Messaggio"],
                [[e["timestamp"], e["message"][:120]] for e in events],
            ))

    # Instances
    inst = data.get("ecs_instances", {})
    if "error" not in inst:
        cis = inst.get("container_instances", [])
        ec2s = inst.get("ec2_details", [])
        if cis:
            parts.append('<h3>EC2 Container Instances</h3>')
            parts.append(_table(
                ["EC2 ID", "Stato", "Task", "CPU", "Memoria"],
                [[c["ec2_id"], c["status"], f"{c['running']} run / {c['pending']} pend",
                  f"{c['cpu_used']}/{c['cpu_total']} ({c['cpu_pct']:.0f}%)",
                  f"{c['mem_used_mb']}MB/{c['mem_total_mb']}MB ({c['mem_pct']:.0f}%)"]
                 for c in cis],
            ))
        if ec2s:
            parts.append(_table(
                ["Instance ID", "Tipo", "Stato", "AZ", "Avviata"],
                [[e["id"], e["type"], e["state"], e["az"], e["launch_time"]] for e in ec2s],
            ))

    # Metrics charts
    met = data.get("ecs_metrics", {})
    hours = met.get("hours", 24)
    cpu = met.get("cpu", {})
    mem = met.get("memory", {})

    if cpu.get("values") or mem.get("values"):
        parts.append(f'<h3>Metriche (ultime {hours}h)</h3>')

    if cpu.get("values"):
        parts.append('<div class="chart-container">')
        parts.append(line_chart(cpu["values"], cpu["timestamps"], "CPU Utilization",
                                unit="%", color="#3b82f6", warn_threshold=70, fail_threshold=90))
        parts.append('</div>')

    if mem.get("values"):
        parts.append('<div class="chart-container">')
        parts.append(line_chart(mem["values"], mem["timestamps"], "Memory Utilization",
                                unit="%", color="#8b5cf6", warn_threshold=70, fail_threshold=90))
        parts.append('</div>')

    # Task failures
    fail = data.get("ecs_failures", {})
    if "error" not in fail:
        tasks = fail.get("tasks", [])
        if tasks:
            parts.append('<h3>Task Stoppati</h3>')
            rows = []
            for t in tasks:
                row_class = ""
                if t["exit_code"] == "137":
                    row_class = ' class="severity-critical"'
                elif t["exit_code"] == "1":
                    row_class = ' class="severity-error"'
                rows.append((row_class, [t["id"], t["exit_code"], t["stop_code"],
                                         t["reason"], t["started"], t["stopped"]]))
            parts.append(_table_with_classes(
                ["Task ID", "Exit", "Stop Code", "Motivo", "Avviato", "Fermato"],
                rows,
            ))
        else:
            parts.append('<p class="empty">Nessun task stoppato recente.</p>')

    parts.append('</div></details>')
    return "\n".join(parts)


def _render_rds_section(data: dict) -> str:
    parts = ['<details>', '<summary><h2>RDS — Database PostgreSQL</h2></summary>',
             '<div class="content">']

    # Status
    st = data.get("rds_status", {})
    if "error" not in st:
        props = st.get("properties", [])
        if props:
            parts.append('<h3>Status</h3>')
            parts.append(_table(
                ["Proprieta", "Valore"],
                [[p["name"], p["value"]] for p in props],
            ))

    # Metrics charts
    met = data.get("rds_metrics", {})
    hours = met.get("hours", 24)
    has_metrics = any(met.get(k, {}).get("values") for k in
                      ["cpu", "freeable_memory", "connections", "read_latency", "write_latency"])

    if has_metrics:
        parts.append(f'<h3>Metriche (ultime {hours}h)</h3>')

        metrics_config = [
            ("cpu", "CPU Utilization", "%", "#3b82f6", 70, 90),
            ("freeable_memory", "RAM Libera", "MB", "#8b5cf6", None, None),
            ("connections", "Connessioni Database", "", "#f59e0b", None, None),
            ("read_latency", "Read Latency", "ms", "#06b6d4", None, None),
            ("write_latency", "Write Latency", "ms", "#ec4899", None, None),
        ]

        for key, label, unit, color, warn, fail in metrics_config:
            m = met.get(key, {})
            if m.get("values"):
                parts.append('<div class="chart-container">')
                parts.append(line_chart(m["values"], m["timestamps"], label,
                                        unit=unit, color=color,
                                        warn_threshold=warn, fail_threshold=fail))
                parts.append('</div>')

    parts.append('</div></details>')
    return "\n".join(parts)


def _render_logs_section(data: dict) -> str:
    parts = ['<details>', '<summary><h2>CloudWatch Logs</h2></summary>',
             '<div class="content">']

    # Errors
    errors = data.get("logs_errors", {})
    if "error" not in errors:
        count = errors.get("result_count", 0)
        parts.append(f'<h3>Errori ed Eccezioni ({count})</h3>')
        if count > 0:
            parts.append('<input type="text" class="filter-box" placeholder="Filtra errori...">')
            parts.append(_logs_table(errors))
        else:
            parts.append('<p class="empty">Nessun errore trovato.</p>')

    # HTTP errors
    http_errors = data.get("logs_http_errors", {})
    if "error" not in http_errors:
        count = http_errors.get("result_count", 0)
        parts.append(f'<h3>Errori HTTP 4xx/5xx ({count})</h3>')
        if count > 0:
            parts.append('<input type="text" class="filter-box" placeholder="Filtra errori HTTP...">')
            parts.append(_logs_table(http_errors, http_mode=True))
        else:
            parts.append('<p class="empty">Nessun errore HTTP trovato.</p>')

    # Status codes distribution
    sc = data.get("logs_status_codes", {})
    if "error" not in sc:
        parts.append('<h3>Distribuzione Status Code</h3>')
        results = sc.get("results", [])
        if results:
            # Parse status code data for chart
            sc_data = _parse_status_codes(results)
            if sc_data:
                parts.append('<div class="chart-container">')
                parts.append(status_code_bar_chart(sc_data))
                parts.append('</div>')
            # Also show table
            parts.append(_logs_table(sc))
        else:
            parts.append('<p class="empty">Nessun dato status code.</p>')

    # Statistics
    parts.append('<h3>Statistiche Query</h3>')
    stat_rows = []
    for key, label in [("logs_errors", "Errori"), ("logs_http_errors", "HTTP Errors"),
                       ("logs_status_codes", "Status Codes")]:
        d = data.get(key, {})
        if "error" not in d:
            stats = d.get("statistics", {})
            stat_rows.append([label,
                              str(int(stats.get("recordsMatched", 0))),
                              str(int(stats.get("recordsScanned", 0))),
                              f"{int(stats.get('bytesScanned', 0)) / 1024:.0f} KB"])
    if stat_rows:
        parts.append(_table(
            ["Query", "Trovati", "Scansionati", "Bytes"],
            stat_rows,
        ))

    parts.append('</div></details>')
    return "\n".join(parts)


def _render_s3_section(data: dict) -> str:
    parts = ['<details>', '<summary><h2>S3 — Storage</h2></summary>',
             '<div class="content">']

    for key, label in [("s3_data", "Data Bucket"), ("s3_frontend", "Frontend Bucket")]:
        s3 = data.get(key, {})
        if not s3:
            continue

        bucket = s3.get("bucket", "?")
        parts.append(f'<h3>{label}: {esc(bucket)}</h3>')

        if "error" in s3 and not s3.get("accessible", True):
            parts.append(f'<p class="empty">Non accessibile: {esc(s3["error"])}</p>')
            continue

        lines = s3.get("summary_lines", [])
        if lines:
            for line in lines:
                parts.append(f'<p>{esc(line)}</p>')
        else:
            parts.append('<p class="empty">Bucket vuoto o dati non disponibili.</p>')

    parts.append('</div></details>')
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc(text) -> str:
    """HTML escape."""
    return html.escape(str(text))


def _table(headers: list, rows: list) -> str:
    """Genera una tabella HTML con sorting."""
    parts = ['<table>']
    parts.append('<thead><tr>')
    for i, h in enumerate(headers):
        parts.append(f'<th data-sort="{i}">{esc(h)}<span class="sort-arrow"></span></th>')
    parts.append('</tr></thead>')
    parts.append('<tbody>')
    for row in rows:
        parts.append('<tr>')
        for cell in row:
            parts.append(f'<td>{esc(cell)}</td>')
        parts.append('</tr>')
    parts.append('</tbody></table>')
    return "\n".join(parts)


def _table_with_classes(headers: list, rows: list) -> str:
    """Tabella con classi CSS per riga. rows = [(class_str, [cells])]."""
    parts = ['<table>']
    parts.append('<thead><tr>')
    for i, h in enumerate(headers):
        parts.append(f'<th data-sort="{i}">{esc(h)}<span class="sort-arrow"></span></th>')
    parts.append('</tr></thead>')
    parts.append('<tbody>')
    for row_class, cells in rows:
        parts.append(f'<tr{row_class}>')
        for cell in cells:
            parts.append(f'<td>{esc(cell)}</td>')
        parts.append('</tr>')
    parts.append('</tbody></table>')
    return "\n".join(parts)


def _logs_table(log_data: dict, http_mode: bool = False) -> str:
    """Tabella per risultati Logs Insights con severity highlighting."""
    headers = log_data.get("headers", [])
    results = log_data.get("results", [])

    if not headers or not results:
        return '<p class="empty">Nessun risultato.</p>'

    parts = ['<table>']
    parts.append('<thead><tr>')
    for i, h in enumerate(headers):
        parts.append(f'<th data-sort="{i}">{esc(h)}<span class="sort-arrow"></span></th>')
    parts.append('</tr></thead>')
    parts.append('<tbody>')

    for result in results[:50]:
        # Build row values
        cells = {}
        for field in result:
            fname = field.get("field", "?")
            if fname != "@ptr":
                cells[fname] = field.get("value", "")

        # Determine row class
        row_class = ""
        msg = cells.get("@message", "")
        status_code = cells.get("statusCode", "")

        if http_mode and status_code:
            if status_code.startswith("5"):
                row_class = ' class="status-5xx"'
            elif status_code.startswith("4"):
                row_class = ' class="status-4xx"'
        elif "CRITICAL" in msg or "Traceback" in msg:
            row_class = ' class="severity-critical"'
        elif "ERROR" in msg:
            row_class = ' class="severity-error"'
        elif "WARN" in msg:
            row_class = ' class="severity-warn"'

        parts.append(f'<tr{row_class}>')
        for h in headers:
            val = cells.get(h, "")
            # Tronca messaggi lunghi
            if h == "@message" and len(val) > 150:
                val = val[:150] + "..."
            parts.append(f'<td>{esc(val)}</td>')
        parts.append('</tr>')

    parts.append('</tbody></table>')
    return "\n".join(parts)


def _parse_status_codes(results: list) -> list:
    """Parse risultati status-codes in formato per bar chart."""
    sc_data = []
    for result in results:
        code = ""
        count = 0
        for field in result:
            if field.get("field") == "statusCode":
                code = field.get("value", "")
            elif field.get("field") == "request_count":
                try:
                    count = int(float(field.get("value", 0)))
                except (ValueError, TypeError):
                    count = 0
        if code:
            sc_data.append({"code": code, "count": count})
    return sorted(sc_data, key=lambda x: x["count"], reverse=True)
