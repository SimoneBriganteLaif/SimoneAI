# Skills del Sistema

Le skill sono istruzioni operative per Claude Code. Ogni skill è una **cartella** con dentro un file `SKILL.md` (e file aggiuntivi se necessario).

---

## Elenco skill

### Presales

| Skill | Stato | Trigger | Legge | Scrive |
|-------|-------|---------|-------|--------|
| `presales/init-project/` | beta | Inizio nuovo progetto | Notion, GitHub | projects/[nome]/, INDEX.md |
| `presales/estrazione-requisiti/` | beta | Dopo un meeting cliente | Materiale grezzo | requisiti.md, meeting/ |
| `presales/genera-allegato-tecnico/` | beta | Requisiti validati, serve contratto | requisiti.md | allegato-tecnico.md |
| `presales/genera-mockup-brief/` | beta | Requisiti validati, servono mockup | requisiti.md | mockup-brief.md |

### Development

| Skill | Stato | Trigger | Legge | Scrive |
|-------|-------|---------|-------|--------|
| `development/feature-workflow/` | beta | Sviluppo feature end-to-end | requisiti.md, .feature-state.md | .feature-state.md, feature-log.md |
| `development/feature-plan/` | beta | Prima di sviluppare una feature | requisiti.md, architettura.md, patterns/ | .feature-state.md (Piano) |
| `development/feature-develop/` | beta | Piano approvato, da implementare | .feature-state.md (Piano), processi.md | Codebase, .feature-state.md (Sviluppo) |
| `development/feature-test/` | beta | Sviluppo completato, da testare | .feature-state.md, requisiti.md, codebase | Nuovi test, .feature-state.md (Test) |
| `development/feature-review/` | beta | Sviluppo completato, da revisionare | .feature-state.md, processi.md, patterns/ | .feature-state.md (Review) |
| `development/estrazione-decisioni/` | beta | Decisione tecnica non banale | decisioni.md | decisioni.md, architettura.md |
| `development/estrazione-pattern/` | beta | Fine sprint o fine progetto | feature-log, decisioni | patterns/, knowledge/ |

### Maintenance

| Skill | Stato | Trigger | Legge | Scrive |
|-------|-------|---------|-------|--------|
| `maintenance/audit-periodico/` | beta | Fine mese | Tutta la KB | Report + aggiornamenti distribuiti |

### Meta

| Skill | Stato | Trigger | Legge | Scrive |
|-------|-------|---------|-------|--------|
| `meta/gestione-kb/` | beta | Dopo modifiche KB, nuove idee, periodicamente | Meta-file | changelog, IDEAS.md, docs/ |
| `meta/verifica-pre-commit/` | stable | Prima di ogni commit | Tutti i file modificati | — (solo lettura) |

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
