# Skills del Sistema

Le skill sono istruzioni operative per Claude Code. Ogni skill è una **cartella** con dentro un file `SKILL.md` (e file aggiuntivi se necessario).

---

## Elenco skill

### Presales

| Skill | Trigger | Output |
|-------|---------|--------|
| `presales/init-project/` | Inizio nuovo progetto | struttura KB + note Notion + repo clonata + CLAUDE.md repo |
| `presales/estrazione-requisiti/` | Dopo un meeting cliente | `requisiti.md` |
| `presales/genera-documenti/` | Quando requisiti.md è validato | `allegato-tecnico.md` + `requisiti-mockup.md` |

### Development

| Skill | Trigger | Output |
|-------|---------|--------|
| `development/estrazione-decisioni/` | Dopo ogni decisione tecnica rilevante | aggiornamento `decisioni-tecniche.md` + `architettura.md` |
| `development/aggiornamento-kb/` | Fine sprint o fine progetto | pattern in `patterns/`, aggiornamento `knowledge/` |

### Maintenance

| Skill | Trigger | Output |
|-------|---------|--------|
| `maintenance/aggiornamento-periodico/` | Fine mese | report + aggiornamenti multipli KB |

### Meta

| Skill | Trigger | Output |
|-------|---------|--------|
| `meta/gestione-kb/` | Dopo modifiche KB, nuove idee, o periodicamente | aggiornamento changelog, IDEAS.md, docs/ |

---

## Formato standard SKILL.md

```markdown
---
nome: "Nome della skill"
descrizione: >
  Descrizione breve usata per capire quando invocarla.
fase: presales | development | maintenance
versione: "1.0"
output:
  - path/al/file/prodotto.md
aggiornato: "YYYY-MM-DD"
---

## Obiettivo
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
