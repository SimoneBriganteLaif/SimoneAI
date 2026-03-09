---
nome: "AWS Health Report"
descrizione: >
  Genera un report HTML interattivo e self-contained della salute
  dell'infrastruttura AWS di un progetto LAIF. Aggrega ECS, RDS,
  CloudWatch Logs e S3 in un singolo file con grafici SVG, semafori
  e tabelle filtrabili. Solo lettura — nessuna modifica alle risorse AWS.
fase: development
versione: "1.0"
stato: beta
legge:
  - "projects/[nome]/aws-config.yaml"
scrive:
  - "projects/[nome]/reports/aws-report-YYYY-MM-DD-HHMMSS.html"
tag:
  - "#stack:aws"
  - "#stack:ecs"
  - "#stack:rds"
  - "#stack:cloudwatch"
  - "#stack:s3"
  - "#fase:dev"
aggiornato: "2026-03-09"
---

# AWS Health Report

Genera un report HTML completo e interattivo dell'infrastruttura AWS
di un progetto LAIF. Il report include grafici delle metriche,
tabelle filtrabili e indicatori a semaforo.

## Perimetro

**Cosa fa:**
- Dashboard con semafori (ECS, RDS, CloudWatch, S3)
- Grafici SVG interattivi per metriche CloudWatch (CPU, memoria, connessioni, latenza)
- Spike detection automatica sui grafici (punti rossi)
- Tabelle log filtrabili e ordinabili
- Distribuzione status code HTTP con grafico a barre
- Report self-contained (un singolo file HTML, funziona offline)

**Cosa NON fa:**
- Non modifica alcuna risorsa AWS (solo read-only)
- Non installa dipendenze (usa solo Python stdlib + AWS CLI)
- Non sostituisce le skill di diagnosi singole (aws-ecs-diagnose, etc.)

**Rimandi:**
- Per diagnosi approfondita singola: usa le skill specifiche
- Per configurazione iniziale: `_shared/config-discovery.md`

## Prerequisiti

1. AWS CLI v2 installata e configurata
2. Profilo AWS con permessi di lettura
3. File `projects/{progetto}/aws-config.yaml` configurato

## Loop conversazionale

### 1. Progetto
> Quale progetto vuoi analizzare?

Verifica che esista `projects/{nome}/aws-config.yaml`.
Se non esiste, suggerisci di crearlo con `_shared/config-discovery.md`.

### 2. Ambiente
> Dev o prod?

### 3. Parametri (opzionali)
> Finestra metriche: ultime 24h (default) o altro?
> Finestra log: ultima 1h (default) o altro?

## Script

```bash
python3 skills/development/aws-diagnostics/aws-health-report/run.py \
  --project <nome> --env <dev|prod> \
  [--hours 24] [--log-window 1h] [--output path/custom.html]
```

**Argomenti:**
- `--project` (obbligatorio): nome progetto nella KB
- `--env` (obbligatorio): `dev` o `prod`
- `--hours` (default: 24): finestra metriche CloudWatch in ore
- `--log-window` (default: 1h): finestra query log (`15m`, `1h`, `6h`, `24h`)
- `--output` (opzionale): path output custom
- `--kb-root` (opzionale): path root KB

**Output:** `projects/{progetto}/reports/aws-report-YYYY-MM-DD-HHMMSS.html`

## Contenuto del report

1. **Dashboard** — Semafori per ECS, RDS, CloudWatch, S3 + verdetto
2. **ECS** — Deployment, EC2 instances, grafici CPU/Memory, task stoppati
3. **RDS** — Status, grafici CPU/RAM/Connessioni/Latenza R/W
4. **CloudWatch Logs** — Errori, errori HTTP, distribuzione status code
5. **S3** — Overview bucket (size, count)

## Output in chat

Dopo l'esecuzione, mostra:
- Path del file HTML generato
- Verdetto complessivo
- Eventuali problemi rilevati
