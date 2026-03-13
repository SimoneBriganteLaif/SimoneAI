---
progetto: "albini-castelli"
ultimo-aggiornamento: "2026-03-12"
tags:
  - "#progetto:albini-castelli"
  - "#fase:manutenzione"
---

# Manutenzione — Albini & Castelli

> Note post go-live: migrazione dati, incident, hotfix, deploy, monitoraggio.

---

## Fase attuale: Supporto migrazione (da 2026-03-12)

Il cliente deve migrare la propria gestione storica dei cantieri sull'applicazione. L'applicazione è in produzione e funzionante. Il lavoro riguarda:

1. **Import dati storici** — tramite modulo `import_storico` (backend) che usa openpyxl/xlsxwriter
2. **Validazione dati** — verifica che i dati importati siano coerenti con il modello dati dell'app
3. **Formazione utenti** — accompagnamento dei referenti cliente
4. **Monitoraggio** — health check AWS durante e dopo il caricamento dati

### Comandi utili per questa fase

```bash
# Health check infrastruttura AWS
# → usa skill aws-triage con projects/albini-castelli/aws-config.yaml

# Log applicativi post-import
# → usa skill aws-logs-diagnose

# Stato RDS (attenzione a storage dopo import massivo)
# → usa skill aws-rds-diagnose
```

### Risorse AWS

| Ambiente | Cluster ECS | RDS | S3 (dati) |
|----------|-------------|-----|-----------|
| dev | `dev-albini-castelli-cluster` | `dev-albini-castelli-db` | `dev-albini-castelli-data` |
| prod | `prod-albini-castelli-be-cluster` | `prod-albini-castelli-db` | `prod-albini-castelli-data-bucket` |

---

## Log interventi

*(aggiungi una sezione per ogni intervento: hotfix, deploy, incident, sessione migrazione)*

---

## Template sezione intervento

```markdown
### [YYYY-MM-DD] — [Tipo: Hotfix | Deploy | Migrazione | Incident | Formazione]

**Descrizione**: cosa è successo / cosa si è fatto
**Impatto**: nessuno | downtime N min | dati corrotti | performance
**Risoluzione**: come è stato risolto
**Note**: cosa tenere a mente per il futuro
```
