---
nome: "AWS ECS Diagnose"
descrizione: >
  Diagnosi approfondita del cluster ECS di un progetto LAIF.
  Analizza servizi, deployment, task stoppati, exit code, capacity provider,
  e configurazione task definition (CPU, memoria, env vars).
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

# Skill: AWS ECS Diagnose

## Obiettivo

Diagnosi approfondita di problemi ECS: deployment bloccati, task che crashano, capacity insufficiente, configurazione errata.

---

## Perimetro

**Fa**: analisi dettagliata di servizi, deployment, task (running e stopped), cluster capacity, task definition.

**NON fa**: non modifica servizi, non fa restart, non aggiorna task definition. Non legge log applicativi (per quello usa `aws-logs-diagnose`).

**Rimandi**:
- Log applicativi → `aws-logs-diagnose/`
- Triage rapido → `aws-triage/`

---

## Quando usarla

- Deploy bloccato o in rollback
- Task che si fermano ripetutamente (restart loop)
- Container con exit code non-zero
- Capacity cluster insufficiente
- Verifica configurazione task definition (CPU, memoria, env vars)

---

## Prerequisiti

- [ ] `projects/[nome]/aws-config.yaml` configurato
- [ ] Profilo AWS con permessi di lettura su ECS

---

## Loop conversazionale

### Domanda 1 — Progetto e ambiente

> Quale progetto e ambiente? (es. `jubatus dev`)

### Domanda 2 — Cosa investigare

> Cosa stai investigando?
> - `deployment` — problemi di deploy, rollout, rollback
> - `task-failure` — task che si fermano, exit code, motivi di stop
> - `capacity` — cluster capacity, scaling, container instances
> - `config` — task definition, CPU, memoria, env vars
> - `all` — tutto

---

## Script

```bash
# Modalita' specifiche
python3 skills/development/aws-diagnostics/aws-ecs-diagnose/run.py \
  --project <nome> --env <dev|prod> --mode <deployment|task-failure|capacity|config|all>

# Esempi
python3 run.py --project jubatus --env dev --mode task-failure
python3 run.py --project jubatus --env prod --mode deployment
```

---

## Vincoli di sicurezza

- Solo comandi read-only: describe-services, describe-tasks, describe-clusters, describe-task-definition, list-tasks
- Nessun execute-command, update-service, stop-task
- Profilo AWS sempre esplicito

---

## Checklist qualita

- [ ] Modalita' selezionata eseguita con output strutturato
- [ ] Exit code e stoppedReason riportati per task failure
- [ ] Deployment events mostrati per problemi di deploy
- [ ] Errori gestiti (servizio non trovato, permessi insufficienti)

#stack:aws #stack:ecs #fase:development
