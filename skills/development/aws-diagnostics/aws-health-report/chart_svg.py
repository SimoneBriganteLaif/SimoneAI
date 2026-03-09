"""
Generatore di grafici SVG inline per metriche CloudWatch.

Produce SVG self-contained da inserire direttamente nell'HTML.
"""

import html


def line_chart(values: list, timestamps: list, label: str,
               unit: str = "%", width: int = 700, height: int = 200,
               color: str = "#3b82f6",
               warn_threshold: float = None,
               fail_threshold: float = None) -> str:
    """
    Genera un grafico SVG a linea con area riempita.

    Features:
    - Polyline + area semi-trasparente
    - Asse Y con min/mid/max
    - Asse X con timestamp (ogni N-esimo)
    - Spike detection (>2x media → punto rosso)
    - Tooltip su hover
    - Linee soglia warn/fail
    - Barra statistiche sotto il grafico

    Returns:
        Stringa SVG completa.
    """
    if not values or not timestamps:
        return _no_data_svg(label, width, 80)

    n = len(values)
    clean = [v for v in values if v is not None]
    if not clean:
        return _no_data_svg(label, width, 80)

    min_v = min(clean)
    max_v = max(clean)
    avg_v = sum(clean) / len(clean)
    cur_v = clean[-1]

    # Padding
    pad_left = 60
    pad_right = 20
    pad_top = 30
    pad_bottom = 50
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    # Scala Y con margine
    y_min = min_v * 0.9 if min_v > 0 else min_v - abs(max_v - min_v) * 0.1
    y_max = max_v * 1.1 if max_v > 0 else max_v + abs(max_v - min_v) * 0.1
    if y_min == y_max:
        y_min -= 1
        y_max += 1
    y_span = y_max - y_min

    # Statistiche altezza totale
    stats_h = 30
    total_h = height + stats_h

    def x_pos(i):
        return pad_left + (i / max(n - 1, 1)) * chart_w

    def y_pos(v):
        if v is None:
            return pad_top + chart_h
        return pad_top + chart_h - ((v - y_min) / y_span) * chart_h

    # Build SVG
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" '
                 f'style="width:100%;max-width:{width}px;font-family:system-ui,sans-serif;font-size:11px">')

    # Background
    parts.append(f'<rect x="{pad_left}" y="{pad_top}" width="{chart_w}" height="{chart_h}" '
                 f'fill="#f8fafc" rx="4"/>')

    # Grid lines (4 horizontal)
    for i in range(5):
        gy = pad_top + (i / 4) * chart_h
        gv = y_max - (i / 4) * y_span
        parts.append(f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{pad_left + chart_w}" y2="{gy:.1f}" '
                     f'stroke="#e2e8f0" stroke-width="0.5"/>')
        parts.append(f'<text x="{pad_left - 5}" y="{gy + 3:.1f}" text-anchor="end" '
                     f'fill="#64748b" font-size="10">{gv:.1f}</text>')

    # Threshold lines
    if warn_threshold is not None and y_min <= warn_threshold <= y_max:
        wy = y_pos(warn_threshold)
        parts.append(f'<line x1="{pad_left}" y1="{wy:.1f}" x2="{pad_left + chart_w}" y2="{wy:.1f}" '
                     f'stroke="#f59e0b" stroke-width="1" stroke-dasharray="6,3"/>')
    if fail_threshold is not None and y_min <= fail_threshold <= y_max:
        fy = y_pos(fail_threshold)
        parts.append(f'<line x1="{pad_left}" y1="{fy:.1f}" x2="{pad_left + chart_w}" y2="{fy:.1f}" '
                     f'stroke="#ef4444" stroke-width="1" stroke-dasharray="6,3"/>')

    # Area fill
    area_points = []
    for i, v in enumerate(values):
        if v is not None:
            area_points.append(f"{x_pos(i):.1f},{y_pos(v):.1f}")
    if area_points:
        # Close the area path
        first_x = x_pos(0)
        last_x = x_pos(n - 1)
        bottom_y = pad_top + chart_h
        area_path = f"M{first_x:.1f},{bottom_y:.1f} L" + " L".join(area_points) + f" L{last_x:.1f},{bottom_y:.1f} Z"
        parts.append(f'<path d="{area_path}" fill="{color}" opacity="0.12"/>')

    # Line
    line_points = []
    for i, v in enumerate(values):
        if v is not None:
            line_points.append(f"{x_pos(i):.1f},{y_pos(v):.1f}")
    if line_points:
        parts.append(f'<polyline points="{" ".join(line_points)}" fill="none" '
                     f'stroke="{color}" stroke-width="2" stroke-linejoin="round"/>')

    # Data points + spike detection
    spike_threshold = avg_v * 2 if avg_v > 0 else max_v
    for i, v in enumerate(values):
        if v is None:
            continue
        cx = x_pos(i)
        cy = y_pos(v)
        ts = html.escape(timestamps[i] if i < len(timestamps) else "?")
        is_spike = v > spike_threshold and v > avg_v * 1.5

        # Invisible larger circle for hover
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="transparent" '
                     f'style="cursor:pointer">'
                     f'<title>{ts}\n{v:.2f}{unit}</title></circle>')

        # Visible point
        if is_spike:
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#ef4444" stroke="white" stroke-width="1"/>')
        else:
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="{color}" opacity="0.7"/>')

    # X-axis labels
    label_count = min(6, n)
    step = max(1, n // label_count)
    for i in range(0, n, step):
        lx = x_pos(i)
        ts = timestamps[i] if i < len(timestamps) else ""
        # Mostra solo ora:minuti se possibile
        short_ts = ts[-5:] if len(ts) >= 5 else ts
        parts.append(f'<text x="{lx:.1f}" y="{pad_top + chart_h + 15}" text-anchor="middle" '
                     f'fill="#64748b" font-size="9">{html.escape(short_ts)}</text>')

    # Label
    parts.append(f'<text x="{pad_left}" y="{pad_top - 10}" fill="#334155" '
                 f'font-size="13" font-weight="600">{html.escape(label)}</text>')

    # Unit label
    parts.append(f'<text x="{pad_left + chart_w}" y="{pad_top - 10}" text-anchor="end" '
                 f'fill="#94a3b8" font-size="10">{html.escape(unit)}</text>')

    # Stats bar
    stats_y = height + 5
    stats_items = [
        ("Attuale", cur_v, color),
        ("Media", avg_v, "#64748b"),
        ("Min", min_v, "#22c55e"),
        ("Max", max_v, "#ef4444"),
    ]
    sx = pad_left
    for stat_label, stat_val, stat_color in stats_items:
        parts.append(f'<text x="{sx}" y="{stats_y + 12}" fill="{stat_color}" font-size="11">'
                     f'{stat_label}: <tspan font-weight="600">{stat_val:.1f}{unit}</tspan></text>')
        sx += (chart_w) / 4

    parts.append('</svg>')
    return "\n".join(parts)


def _no_data_svg(label: str, width: int, height: int) -> str:
    """SVG placeholder per dati assenti."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'style="width:100%;max-width:{width}px;font-family:system-ui,sans-serif">'
        f'<rect width="{width}" height="{height}" fill="#f8fafc" rx="4"/>'
        f'<text x="{width // 2}" y="{height // 2}" text-anchor="middle" '
        f'fill="#94a3b8" font-size="13">{html.escape(label)}: nessun dato disponibile</text>'
        f'</svg>'
    )


def status_code_bar_chart(data: list, width: int = 400, height: int = 180) -> str:
    """
    Grafico a barre orizzontali per distribuzione status code.

    Args:
        data: [{"code": str, "count": int}] ordinato per count desc

    Returns:
        Stringa SVG.
    """
    if not data:
        return _no_data_svg("Status Codes", width, 60)

    pad_left = 60
    pad_right = 60
    pad_top = 10
    bar_h = 28
    gap = 6
    chart_w = width - pad_left - pad_right
    total_h = pad_top + len(data) * (bar_h + gap) + 10

    max_count = max(d["count"] for d in data)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" '
                 f'style="width:100%;max-width:{width}px;font-family:system-ui,sans-serif;font-size:12px">')

    for i, d in enumerate(data):
        code = str(d["code"])
        count = d["count"]
        y = pad_top + i * (bar_h + gap)
        bar_w = (count / max_count) * chart_w if max_count > 0 else 0

        # Color by status code range
        if code.startswith("5"):
            bar_color = "#ef4444"
        elif code.startswith("4"):
            bar_color = "#f59e0b"
        elif code.startswith("3"):
            bar_color = "#8b5cf6"
        elif code.startswith("2"):
            bar_color = "#22c55e"
        else:
            bar_color = "#64748b"

        # Label
        parts.append(f'<text x="{pad_left - 8}" y="{y + bar_h / 2 + 4}" text-anchor="end" '
                     f'fill="#334155" font-weight="600">{html.escape(code)}</text>')

        # Bar
        parts.append(f'<rect x="{pad_left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" '
                     f'fill="{bar_color}" rx="3" opacity="0.85">'
                     f'<title>{code}: {count} richieste</title></rect>')

        # Count label
        parts.append(f'<text x="{pad_left + bar_w + 6:.1f}" y="{y + bar_h / 2 + 4}" '
                     f'fill="#64748b">{count}</text>')

    parts.append('</svg>')
    return "\n".join(parts)
