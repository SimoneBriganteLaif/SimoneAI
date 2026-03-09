---
nome: "AWS RDS Diagnose"
descrizione: >
  Diagnosi approfondita dell'istanza RDS PostgreSQL di un progetto LAIF.
  Verifica stato, storage, connessioni, parametri e log PostgreSQL.
  Solo lettura — nessuna modifica alle risorse AWS.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/aws-config.yaml
scrive:
  - (nessun file — skill di diagnosi)
aggiornato: "2026-03-09"
---

# Skill: AWS RDS Diagnose

## Obiettivo

Diagnosi approfondita dell'istanza RDS PostgreSQL: stato, storage, connessioni, parametri custom, log di errore.

---

## Perimetro

**Fa**: verifica stato istanza, controlla parametri DB, scarica log PostgreSQL, analizza configurazione.

**NON fa**: non modifica parametri, non fa restart, non cambia instance class. Non esegue query SQL (per quello usa MCP PostgreSQL).

**Rimandi**:
- Query SQL dirette → MCP PostgreSQL
- Triage rapido → `aws-triage/`
- Log applicativi → `aws-logs-diagnose/`

---

## Quando usarla

- Database non raggiungibile o lento
- Verifica parametri di configurazione (max_connections, shared_buffers)
- Analisi log PostgreSQL per errori
- Verifica storage disponibile
- Post-incidente: capire cosa e' successo al DB

---

## Prerequisiti

- [ ] `projects/[nome]/aws-config.yaml` configurato
- [ ] Profilo AWS con permessi di lettura su RDS

---

## Loop conversazionale

### Domanda 1 — Progetto e ambiente

> Quale progetto e ambiente?

### Domanda 2 — Cosa investigare

> Cosa stai investigando?
> - `status` — stato generale, endpoint, storage, classe istanza
> - `connections` — parametri connessione (max_connections, pool)
> - `logs` — log PostgreSQL recenti (errori, slow query)
> - `parameters` — parametri custom del parameter group
> - `all` — tutto

---

## Script

```bash
python3 skills/development/aws-diagnostics/aws-rds-diagnose/run.py \
  --project <nome> --env <dev|prod> --mode <status|connections|logs|parameters|all>
```

---

## Vincoli di sicurezza

- Solo comandi read-only: describe-db-instances, describe-db-log-files, download-db-log-file-portion, describe-db-parameters
- Nessun modify-db-instance, reboot-db-instance, delete-db-instance
- Endpoint DB mostrato ma credenziali mai esposte
- Profilo AWS sempre esplicito

---

## Checklist qualita

- [ ] Modalita' selezionata eseguita con output strutturato
- [ ] Storage e stato chiaramente riportati
- [ ] Log scaricati e filtrati per errori
- [ ] Errori gestiti (istanza non trovata, permessi insufficienti)

#stack:aws #stack:rds #fase:development
