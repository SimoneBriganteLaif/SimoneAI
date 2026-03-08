# Changelog — Framework

Tutte le modifiche alla struttura del sistema: cartelle, skill, template, processi, documentazione.

Formato basato su [Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/).

---

## [Non rilasciato]

### Changed

**Skill — Presales**
- `genera-documenti/` splittata in due skill separate:
  - `genera-allegato-tecnico/` — requisiti → allegato contrattuale (max 3 pagine)
  - `genera-mockup-brief/` — requisiti → brief mockup per Windsurf

**Skill — Development**
- `aggiornamento-kb/` rinominata in `estrazione-pattern/` — nome più chiaro sullo scope

**Skill — Maintenance**
- `aggiornamento-periodico/` rinominata in `audit-periodico/` — evita confusione con estrazione-pattern

**Tutte le skill**
- Aggiunto sistema `stato: beta | stable` nel frontmatter
- Aggiunto `legge:` e `scrive:` nel frontmatter per chiarire input/output
- Aggiunta sezione **Perimetro** (cosa fa / cosa NON fa / rimandi ad altre skill)
- Skill in beta: avviso all'inizio + review ad ogni step durante l'uso

**Documentazione**
- `docs/struttura.md` — albero cartelle riscritto come code block annotato (era Mermaid)
- `docs/skills.md` — aggiornato con nomi, split, tabella confronto skill di manutenzione
- `CLAUDE.md` — aggiornati riferimenti a nuovi nomi skill + sezione beta
- `skills/README.md` — aggiornato con colonne Stato/Legge/Scrive

### Removed
- `skills/presales/genera-documenti/` — sostituita da genera-allegato-tecnico + genera-mockup-brief

---

## [1.0.0] — 2026-03-08

Prima release della Knowledge Base.

### Added

**Struttura cartelle**
- `projects/` con `_template/` (README, presales/, development/, maintenance/)
- `projects/INDEX.md` — registro progetti
- `patterns/` con README e `_template.md`
- `knowledge/` con `industrie/` e `problemi-tecnici/` (entrambi con template)
- `.tags/index.md` — indice tag per ricerca rapida
- `skills/` con organizzazione per fase

**Skill — Presales**
- `skills/presales/init-project/` v1.0 — bootstrap completo progetto
- `skills/presales/estrazione-requisiti/` v1.1 — note meeting → requisiti strutturati
- `skills/presales/genera-documenti/` v1.1 — requisiti → allegato tecnico + brief mockup

**Skill — Development**
- `skills/development/estrazione-decisioni/` v1.1 — documentazione ADR
- `skills/development/aggiornamento-kb/` v1.1 — estrazione pattern a fine sprint

**Skill — Maintenance**
- `skills/maintenance/aggiornamento-periodico/` v1.1 — audit mensile KB

**Skill — Meta**
- `skills/meta/gestione-kb/` v1.0 — gestione changelog, idee, docs, review

**Documentazione**
- `docs/struttura.md` — mappa cartelle con diagramma Mermaid
- `docs/skills.md` — catalogo skill con flussi Mermaid
- `docs/workflow.md` — flussi di lavoro per fase + divisione Claude Code/Windsurf
- `CHANGELOG-framework.md` — questo file
- `CHANGELOG-contenuti.md` — changelog contenuti operativi
- `IDEAS.md` — backlog strutturato idee e miglioramenti

**File di sistema**
- `CLAUDE.md` — istruzioni operative per Claude Code
- `System.md` — panoramica del sistema

**Versioning**
- Inizializzazione repository Git
- `.gitignore` configurato
