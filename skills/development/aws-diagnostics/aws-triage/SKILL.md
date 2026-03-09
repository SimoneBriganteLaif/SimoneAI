---
nome: "AWS Triage"
descrizione: >
  Controllo rapido dello stato di tutti i servizi AWS di un progetto LAIF.
  Verifica ECS (deployment, task running), RDS (stato), CloudWatch (errori recenti),
  S3 (accessibilita). Produce un report con semafori OK/WARN/FAIL.
  Per approfondimenti usa le skill dedicate: aws-ecs-diagnose, aws-logs-diagnose,
  aws-rds-diagnose, aws-s3-diagnose.
  Solo lettura — nessuna modifica alle risorse AWS.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/aws-config.yaml
scrive:
  - projects/[nome]/aws-config.yaml (solo se non esiste, prima esecuzione)
aggiornato: "2026-03-09"
---

# Skill: AWS Triage

## Obiettivo

Health check rapido (<2 minuti) di tutti i servizi AWS di un progetto LAIF. Produce un dashboard con semafori per identificare immediatamente quale servizio ha problemi, con rimandi alle skill di deep-dive.

---

## Perimetro

**Fa**: check superficiale di ECS, RDS, CloudWatch (errori), S3. Genera aws-config.yaml se non esiste.

**NON fa**: deep-dive su singoli servizi (per quello usa le skill dedicate), non esegue modifiche, non legge log completi.

**Rimandi**:
- Problemi ECS → `skills/development/aws-diagnostics/aws-ecs-diagnose/`
- Errori nei log → `skills/development/aws-diagnostics/aws-logs-diagnose/`
- Problemi DB → `skills/development/aws-diagnostics/aws-rds-diagnose/`
- Problemi storage → `skills/development/aws-diagnostics/aws-s3-diagnose/`

---

## Quando usarla

- Inizio sessione di debug su un ambiente AWS
- "Qualcosa non funziona" senza indicazioni specifiche
- Verifica rapida post-deploy
- Invocata da un agente come primo step di troubleshooting

---

## Prerequisiti

- [ ] AWS CLI installata e configurata
- [ ] Profilo AWS con permessi di lettura su ECS, RDS, CloudWatch, S3
- [ ] `projects/[nome]/aws-config.yaml` esistente (o generato al primo uso)

---

## Loop conversazionale

### Domanda 1 — Progetto

> Su quale progetto vuoi fare il triage?

(Elenca i progetti disponibili in `projects/`)

### Domanda 2 — Ambiente

> Quale ambiente? (`dev` o `prod`)

### Domanda 3 — Config (solo se aws-config.yaml non esiste)

> `aws-config.yaml` non trovato. Vuoi che lo generi ora?

(Se si: segui `_shared/config-discovery.md`)

---

## Script

```bash
python3 skills/development/aws-diagnostics/aws-triage/run.py \
  --project <nome> --env <dev|prod>
```

Lo script esegue 4 check in sequenza e produce il report.

---

## Processo di verifica

### Step 1 — Carica configurazione

Leggi `projects/[nome]/aws-config.yaml` per ottenere profilo, regione e nomi risorse.

### Step 2 — Check ECS

```bash
aws ecs describe-services --cluster {ecs_cluster} --services {ecs_service}
```
- OK: `runningCount == desiredCount`, deployment PRIMARY
- WARN: deployment in corso (PRIMARY + ACTIVE)
- FAIL: `runningCount < desiredCount` o servizio INACTIVE

### Step 3 — Check RDS

```bash
aws rds describe-db-instances --db-instance-identifier {rds_identifier}
```
- OK: status = `available`
- WARN: status = `backing-up`, `maintenance`
- FAIL: status = `stopped`, `failed`, `storage-full`

### Step 4 — Check errori recenti (CloudWatch)

```bash
# Query Logs Insights: errori nell'ultima ora
aws logs start-query ... → get-query-results
```
- OK: 0 errori
- WARN: 1-10 errori
- FAIL: >10 errori

### Step 5 — Check S3

```bash
aws s3api head-bucket --bucket {s3_data_bucket}
```
- OK: bucket accessibile
- FAIL: bucket non accessibile o non esistente

### Step 6 — Aggregazione

Calcola verdetto complessivo: FAIL se almeno uno FAIL, WARN se almeno uno WARN, altrimenti OK.

---

## Output in chat

```
AWS TRIAGE — {progetto} ({ambiente})
Data: {timestamp}

| Servizio   | Stato | Dettaglio                            |
|------------|-------|--------------------------------------|
| ECS        | OK    | 1/1 task running, PRIMARY stable     |
| RDS        | OK    | available, t4g.micro                 |
| CloudWatch | WARN  | 3 errori nell'ultima ora             |
| S3 Data    | OK    | accessibile                          |

Verdetto: WARN

Azione consigliata:
  → Logs: python3 .../aws-logs-diagnose/run.py --project {p} --env {e} --query-type errors
```

---

## Vincoli di sicurezza

- Solo comandi read-only (describe-*, head-*, start-query/get-query-results)
- Profilo AWS sempre esplicito (`--profile`)
- Timeout 30s per comando
- Nessuna credenziale nell'output

---

## Checklist qualita

- [ ] Tutti i 4 check eseguiti (ECS, RDS, CloudWatch, S3)
- [ ] Output con tabella formattata e verdetto
- [ ] Rimandi alle skill deep-dive per servizi con problemi
- [ ] Errori gestiti (risorsa non trovata, credenziali scadute, timeout)

#stack:aws #stack:ecs #stack:rds #stack:cloudwatch #fase:development
