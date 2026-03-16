# Skills del Sistema

Le skill sono istruzioni operative per Claude Code. Ogni skill è una **cartella** con dentro un file `SKILL.md` (e file aggiuntivi se necessario).

---

## Elenco skill

### Presales

| Skill | Stato | Nativa | Trigger | Legge | Scrive |
|-------|-------|--------|---------|-------|--------|
| `presales/init-project/` | beta | si | Inizio nuovo progetto | Notion, GitHub | projects/[nome]/, INDEX.md |
| `presales/estrazione-requisiti/` | stable | si | Dopo un meeting cliente | Materiale grezzo | requisiti.md, meeting/ |
| `presales/genera-allegato-tecnico/` | beta | si | Requisiti validati, serve contratto | requisiti.md | allegato-tecnico.md |
| `presales/genera-mockup-brief/` | beta | si | Requisiti validati, servono mockup | requisiti.md | mockup-brief.md |

### Development

| Skill | Stato | Nativa | Trigger | Legge | Scrive |
|-------|-------|--------|---------|-------|--------|
| `development/feature-workflow/` | beta | si | Sviluppo feature end-to-end | requisiti.md, .feature-state.md | .feature-state.md, feature-log.md |
| `development/feature-plan/` | beta | — | Prima di sviluppare una feature | requisiti.md, architettura.md, patterns/ | .feature-state.md (Piano) |
| `development/feature-develop/` | beta | — | Piano approvato, da implementare | .feature-state.md (Piano), processi.md | Codebase, .feature-state.md (Sviluppo) |
| `development/feature-test/` | beta | — | Sviluppo completato, da testare | .feature-state.md, requisiti.md, codebase | Nuovi test, .feature-state.md (Test) |
| `development/feature-review/` | beta | — | Sviluppo completato, da revisionare | .feature-state.md, processi.md, patterns/ | .feature-state.md (Review) |
| `development/estrazione-decisioni/` | stable | si | Decisione tecnica non banale | decisioni.md | decisioni.md, architettura.md |
| `development/estrazione-pattern/` | stable | si | Fine sprint o fine progetto | feature-log, decisioni | patterns/, knowledge/ |
| `development/setup-progetto-dev/` | beta | si | Inizio sessione dev | architettura.md, MEMORY.md, stack.md | nessuno (solo report) |
| `development/brainstorming-post-sviluppo/` | beta | si | Fine sessione dev | Lavoro svolto nella sessione | patterns/, skills/, IDEAS.md |
| `development/windsurf-feedback/` | beta | si | Report feedback da Windsurf | Report .md da Windsurf | knowledge/, patterns/, decisioni.md |
| `development/aws-diagnostics/aws-health-report/` | beta | si | Report HTML completo infrastruttura | aws-config.yaml | reports/aws-report-*.html |
| `development/aws-diagnostics/aws-triage/` | beta | si | Debug AWS, primo check | aws-config.yaml | — (diagnosi) |
| `development/aws-diagnostics/aws-ecs-diagnose/` | beta | si | Problemi ECS (deploy, task, capacity) | aws-config.yaml | — (diagnosi) |
| `development/aws-diagnostics/aws-logs-diagnose/` | beta | si | Errori nei log, query CloudWatch | aws-config.yaml | — (diagnosi) |
| `development/aws-diagnostics/aws-rds-diagnose/` | beta | si | Problemi database RDS | aws-config.yaml | — (diagnosi) |
| `development/aws-diagnostics/aws-s3-diagnose/` | beta | si | Inventario bucket S3 | aws-config.yaml | — (diagnosi) |
| `development/crea-task-notion/` | beta | si | Creare task Notion per progetto | KB progetto, pagine Notion | Task su Notion |
| `development/db-transfer/` | beta | si | Copiare/sincronizzare dati tra DB | aws-config.yaml, .env | — (opera sui DB) |

### Maintenance

| Skill | Stato | Nativa | Trigger | Legge | Scrive |
|-------|-------|--------|---------|-------|--------|
| `maintenance/audit-periodico/` | beta | si | Fine mese | Tutta la KB | Report + aggiornamenti distribuiti |

### Meta

| Skill | Stato | Nativa | Trigger | Legge | Scrive |
|-------|-------|--------|---------|-------|--------|
| `meta/gestione-kb/` | beta | si | Dopo modifiche KB, nuove idee, periodicamente | Meta-file | changelog, IDEAS.md, docs/ |
| `meta/contesto-progetto/` | stable | — | Prima di lavorare su un progetto | README progetto, patterns/, knowledge/ | — (lista file rilevanti) |
| `meta/verifica-pre-commit/` | stable | — | Prima di ogni commit | Tutti i file modificati | — (solo lettura) |

---

## Formato standard SKILL.md

```markdown
---
nome: "Nome della skill"
descrizione: >
  Descrizione con scope chiaro: cosa fa, cosa NON fa, rimandi ad altre skill.
fase: presales | development | maintenance | meta
versione: "1.0"
stato: beta | stable
legge:
  - file/cartelle letti come input
scrive:
  - file/cartelle prodotti o aggiornati
aggiornato: "YYYY-MM-DD"
---

## Obiettivo
## Perimetro          ← cosa fa / cosa NON fa
## Quando usarla / Trigger
## Prerequisiti
## Loop conversazionale    ← domande prima di agire
## Processo di produzione  ← passi da eseguire
## Output in chat          ← riepilogo obbligatorio al termine
## Checklist qualità
```

---

## Principio fondamentale

**Mai produrre output senza prima raccogliere le informazioni necessarie.**

Il loop conversazionale non è opzionale: è la parte più importante di ogni skill.
Chiedi una cosa alla volta. Aspetta risposta. Poi agisci.

**Skill in beta**: all'inizio avvisa l'utente che è in beta. Durante l'uso, ad ogni step chiede se il processo ha senso o se va modificato.
