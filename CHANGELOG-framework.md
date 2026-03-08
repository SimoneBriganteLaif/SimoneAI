# Changelog — Framework

Tutte le modifiche alla struttura del sistema: cartelle, skill, template, processi, documentazione.

Formato basato su [Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/).

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
