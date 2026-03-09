---
nome: "AWS Logs Diagnose"
descrizione: >
  Interroga CloudWatch Logs Insights per un progetto LAIF.
  Offre query pre-costruite (errori, slow request, DB issues, status codes)
  e supporta query custom. Gestisce il polling asincrono dei risultati.
  Solo lettura.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/aws-config.yaml
  - skills/development/aws-diagnostics/_shared/query-templates.md
scrive:
  - (nessun file — skill di diagnosi)
aggiornato: "2026-03-09"
---

# Skill: AWS Logs Diagnose

## Obiettivo

Interrogare i log CloudWatch di un progetto LAIF usando query Logs Insights pre-costruite o custom, con gestione automatica del polling asincrono.

---

## Perimetro

**Fa**: esegue query Logs Insights, formatta risultati, gestisce polling.

**NON fa**: non modifica log group, non crea filtri o allarmi, non analizza metriche CloudWatch (solo log).

**Rimandi**:
- Template query → `_shared/query-templates.md`
- Triage rapido → `aws-triage/`
- Problemi specifici ECS → `aws-ecs-diagnose/`

---

## Quando usarla

- Cercare errori applicativi nei log
- Analizzare problemi di connessione al database
- Trovare request lente
- Verificare distribuzione status code HTTP
- Eseguire query custom sui log

---

## Prerequisiti

- [ ] `projects/[nome]/aws-config.yaml` configurato
- [ ] Profilo AWS con permessi su CloudWatch Logs

---

## Loop conversazionale

### Domanda 1 — Progetto e ambiente

> Quale progetto e ambiente?

### Domanda 2 — Tipo di query

> Che tipo di query?
> - `errors` — errori ed eccezioni
> - `db-issues` — problemi connessione database
> - `slow-requests` — request lente (>1s)
> - `status-codes` — distribuzione status code HTTP
> - `recent` — ultimi log (tail)
> - `memory` — problemi di memoria
> - `custom` — query Logs Insights libera

### Domanda 3 — Finestra temporale

> Finestra temporale? (default: 1h)
> - `15m`, `1h`, `6h`, `24h`

### Domanda 4 (solo per `custom`)

> Scrivi la query Logs Insights.

---

## Script

```bash
# Query pre-costruite
python3 skills/development/aws-diagnostics/aws-logs-diagnose/run.py \
  --project <nome> --env <dev|prod> \
  --query-type <errors|db-issues|slow-requests|status-codes|recent|memory> \
  --time-window <15m|1h|6h|24h>

# Query custom
python3 run.py --project jubatus --env dev \
  --query-type custom \
  --custom-query "fields @timestamp, @message | filter @message like /my-pattern/ | limit 20"
```

---

## Vincoli di sicurezza

- Solo comandi read-only: start-query, get-query-results, describe-log-groups
- Nessun put-log-events, delete-log-group, create-log-group
- Timeout 30s per il polling dei risultati
- Profilo AWS sempre esplicito

---

## Checklist qualita

- [ ] Query eseguita con risultati formattati
- [ ] Polling gestito correttamente (retry, timeout)
- [ ] Finestra temporale rispettata
- [ ] Errori gestiti (log group non trovato, query fallita)

#stack:aws #stack:cloudwatch #fase:development
