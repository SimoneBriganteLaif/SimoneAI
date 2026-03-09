"""
Formattazione output per skill diagnostiche AWS.

Produce tabelle markdown, semafori e report strutturati.
"""

from datetime import datetime


def semaphore(status: str) -> str:
    """Converte uno stato in emoji semaforo."""
    mapping = {
        "OK": "OK",
        "WARN": "WARN",
        "FAIL": "FAIL",
    }
    return mapping.get(status.upper(), status)


def format_table(headers: list, rows: list) -> str:
    """
    Formatta una tabella markdown.

    Args:
        headers: lista di stringhe per intestazioni
        rows: lista di liste di stringhe per righe

    Returns:
        Stringa con tabella markdown formattata.
    """
    if not headers or not rows:
        return "(nessun dato)"

    # Calcola larghezze colonne
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))

    # Header
    header_line = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    separator = "|-" + "-|-".join("-" * w for w in widths) + "-|"

    # Rows
    row_lines = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            w = widths[i] if i < len(widths) else len(str(cell))
            cells.append(str(cell).ljust(w))
        row_lines.append("| " + " | ".join(cells) + " |")

    return "\n".join([header_line, separator] + row_lines)


def format_report(title: str, env: str, sections: list) -> str:
    """
    Formatta un report diagnostico strutturato.

    Args:
        title: titolo del report (es. 'AWS TRIAGE')
        env: ambiente (es. 'dev', 'prod')
        sections: lista di dict con 'heading' e 'content'

    Returns:
        Report markdown formattato.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"## {title} ({env})",
        f"Data: {timestamp}",
        "",
    ]

    for section in sections:
        if "heading" in section:
            lines.append(f"### {section['heading']}")
        if "content" in section:
            lines.append(section["content"])
        lines.append("")

    return "\n".join(lines)


def verdict(statuses: list) -> str:
    """
    Calcola il verdetto complessivo da una lista di stati.

    Args:
        statuses: lista di stringhe ('OK', 'WARN', 'FAIL')

    Returns:
        'FAIL' se almeno uno e' FAIL, 'WARN' se almeno uno e' WARN, altrimenti 'OK'.
    """
    upper = [s.upper() for s in statuses]
    if "FAIL" in upper:
        return "FAIL"
    if "WARN" in upper:
        return "WARN"
    return "OK"


def format_error(message: str) -> str:
    """Formatta un messaggio di errore."""
    return f"ERRORE: {message}"


def sparkline(values: list, width: int = 40) -> str:
    """
    Genera una sparkline ASCII da una lista di valori numerici.

    Args:
        values: lista di float/int (None = dato mancante)
        width: larghezza target (resample se necessario)

    Returns:
        Stringa sparkline con blocchi Unicode.
    """
    BLOCKS = " ▁▂▃▄▅▆▇█"

    # Filtra None
    clean = [v for v in values if v is not None]
    if not clean:
        return "(nessun dato)"

    # Resample se troppi punti
    if len(values) > width:
        step = len(values) / width
        resampled = []
        for i in range(width):
            start = int(i * step)
            end = int((i + 1) * step)
            chunk = [v for v in values[start:end] if v is not None]
            resampled.append(sum(chunk) / len(chunk) if chunk else 0)
        values = resampled

    min_v = min(clean)
    max_v = max(clean)
    span = max_v - min_v if max_v != min_v else 1

    chars = []
    for v in values:
        if v is None:
            chars.append(" ")
        else:
            idx = int((v - min_v) / span * (len(BLOCKS) - 1))
            chars.append(BLOCKS[idx])

    return "".join(chars)


def format_metric_chart(label: str, values: list, timestamps: list,
                        unit: str = "%", show_stats: bool = True) -> str:
    """
    Formatta un grafico di metriche con sparkline, min/max/avg e timeline.

    Args:
        label: nome della metrica
        values: lista di valori numerici
        timestamps: lista di stringhe timestamp corrispondenti
        unit: unita' di misura
        show_stats: mostra min/max/avg

    Returns:
        Stringa multi-riga con grafico e statistiche.
    """
    clean = [v for v in values if v is not None]
    if not clean:
        return f"  {label}: (nessun dato)"

    chart = sparkline(values)
    lines = [f"  {label}: {chart}"]

    if show_stats:
        avg_v = sum(clean) / len(clean)
        min_v = min(clean)
        max_v = max(clean)
        cur_v = clean[-1] if clean else 0
        lines.append(f"    Attuale: {cur_v:.1f}{unit}  |  Media: {avg_v:.1f}{unit}  |  Min: {min_v:.1f}{unit}  |  Max: {max_v:.1f}{unit}")

    if timestamps and len(timestamps) >= 2:
        lines.append(f"    Da: {timestamps[0]}  →  A: {timestamps[-1]}")

    return "\n".join(lines)
