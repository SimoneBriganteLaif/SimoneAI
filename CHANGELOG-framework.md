# Changelog — Framework

Tutte le modifiche alla struttura del sistema: cartelle, skill, template, processi, documentazione.

Formato basato su [Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/).

---

## [Non rilasciato]

### Added

**Gestione repository progetti**
- `.gitignore` — aggiunta regola `projects/*/repo/` e `projects/*/repo-*/` per ignorare repo Git annidate nei progetti
- `projects/_archivio/` — creata directory per progetti archiviati

**Configurazione Obsidian**
- `.obsidian/app.json` — aggiunto filtro `projects/*/repo/` per escludere le repo dei progetti da explorer e ricerca
- `.obsidian/graph.json` — aggiunto `-path:repo` al filtro del grafo per escludere le repo dei progetti

### Changed

**Skill verifica-pre-commit v3.0 — ibrido script + semantica**
- `skills/meta/verifica-pre-commit/` — riscritta completamente:
  - 5 script Python deterministici: `run_all.py`, `check_refs.py`, `check_changelog.py`, `check_tags.py`, `check_struttura.py`
  - Check semantici documentati in SKILL.md (referenze non-link, contenuto changelog, IDEAS, skills/README.md)
  - `check_struttura.py` — check bidirezionale: reale→documentazione + documentazione→reale
  - `check_tags.py` — aggiunto check consistenza tag per progetto (#progetto: e #industria: uguali in tutti i file)
- `CLAUDE.md` — aggiornate regole autonome: rimossi sub-agent, aggiunto approccio ibrido script+semantica, aggiunta regola gestione idee/proposte

**Ristrutturazione template progetto**
- `projects/_template/` — struttura piatta per tipo di contenuto (era: presales/ → development/ → maintenance/)
  - Rimossi: `presales/`, `development/`, `maintenance/` (sotto-cartelle per fase)
  - File in root: `meeting/`, `requisiti.md`, `architettura.md`, `decisioni.md`, `feature-log.md`, `allegato-tecnico.md`, `mockup-brief.md`, `manutenzione.md`
  - Rinominati: `decisioni-tecniche.md` → `decisioni.md`, `requisiti-mockup.md` → `mockup-brief.md`, `note.md` → `manutenzione.md`, `note-meeting/` → `meeting/`
- `projects/jubatus/` — migrato alla nuova struttura piatta
- Aggiornati riferimenti alla vecchia struttura in: `CLAUDE.md`, `docs/struttura.md`, `docs/skills.md`, `docs/workflow.md`, `System.md`

---

## [v1.1] — 2026-03-08

### Added

**Navigazione Obsidian**
- `.obsidian/app.json` — configurato Obsidian: `userIgnoreFilters` per escludere `core/`, `.claude/`, `memory/` da explorer, ricerca e grafo
- `.obsidian/graph.json` — grafo configurato con 4 color group (arancio: docs/hub, verde: skills/, viola: knowledge/, grigio: projects/), search filter `-path:core`, `showArrow: true`, `nodeSizeMultiplier: 1.2`

**Link inter-file (connettività KB)**
- Tutti i 9 SKILL.md — aggiunto footer di navigazione `← [Catalogo skill] · [Workflow] · [System.md]`
- `knowledge/azienda/*.md` (4 file) — aggiunta breadcrumb cross-navigation tra i file della sezione

**Tag system**
- `.tags/index.md` — aggiunti: `#industria:software`, `#fase:contesto`, `#stack:fastapi`, `#stack:cdk`
- `knowledge/azienda/processi.md` — aggiunti tag inline `#industria:software #fase:contesto` (allineato con overview.md)

**Navigazione documentazione**
- `System.md` — aggiunta sezione "Navigazione documentazione" (tabella con link a tutti i doc) e sezione "Manutenzione del sistema stesso" riorganizzata come tabella con link diretti alle skill
- `docs/skills.md` — aggiunto nav breadcrumb (← System.md · workflow.md · struttura.md), TOC completo, mappa globale Mermaid di tutte le skill per fase con relazioni
- `docs/workflow.md` — aggiunto nav breadcrumb, TOC completo, diagramma Mermaid "Quale flusso usare?" come quick reference ad albero decisionale
- `docs/struttura.md` — aggiunto nav breadcrumb
- `docs/setup.md` — aggiunto nav breadcrumb

**Agenti autonomi**
- `skills/meta/verifica-pre-commit/` v1.0 — skill autonoma pre-commit: 5 check in parallelo (referenze cross-file, changelog, IDEAS.md, tag, struttura vs docs), output PASS/FAIL, nessun loop conversazionale, progettata per girare come sub-agent
- `CLAUDE.md` — aggiunta sezione "Agenti autonomi (comportamento obbligatorio)": 4 regole che specificano quando Claude Code deve invocare gli agenti senza essere chiesto (dopo ogni modifica, pre-commit bloccante, drift struttura, >3 file modificati)
- `docs/skills.md` — aggiunta `verifica-pre-commit` in tabella riepilogo, sezione Meta con diagramma Mermaid, e colonna nella tabella comparativa skill di manutenzione
- `docs/struttura.md` — aggiunto `verifica-pre-commit/` nella sezione skills/meta/

**Processo pre-commit**
- `CLAUDE.md` — aggiunta sezione "Processo pre-commit (OBBLIGATORIO)" con checklist coerenza (ora sostituita da riferimento alla skill autonoma)

**Idee**
- `IDEAS.md` — IDEA-010: definire processo branching/Git flow per il team
- `IDEAS.md` — IDEA-011: gestire iniziative interne come progetti con tag #tipo:interno

**Contesto aziendale**
- `knowledge/azienda/` — nuova sezione con 4 file:
  - `overview.md` — chi è LAIF, team, modello di lavoro
  - `stack.md` — stack tecnico, pattern architetturali, convenzioni naming
  - `infrastruttura.md` — architettura AWS, TemplateStack, configurazione, deploy
  - `processi.md` — flussi di lavoro, CI/CD, regole Windsurf

**Repository core**
- `core/` — cartella con repo LAIF clonate come contesto di riferimento
  - `core/laif-template/` — base per tutti i progetti
  - `core/ds/` — design system (@laif/ds, 137+ componenti)
  - `core/laif-cdk/` — infrastruttura AWS (CDK, TemplateStack)
- `core/README.md` — indice repo con link GitHub e descrizioni

### Fixed

**Coerenza documentazione** — 9 riferimenti a skill rinominate/rimosse corretti:
- `docs/workflow.md` — aggiornati 6 riferimenti: genera-documenti → genera-allegato-tecnico + genera-mockup-brief, aggiornamento-kb → estrazione-pattern, aggiornamento-periodico → audit-periodico
- `System.md` — corretto percorso skill maintenance + aggiunta knowledge/azienda/ nella struttura
- `.tags/index.md` — corretto riferimento skill di manutenzione
- `projects/_template/presales/allegato-tecnico.md` — corretto riferimento skill generazione
- `skills/development/estrazione-decisioni/SKILL.md` — corretto riferimento inline a estrazione-pattern
- `memory/MEMORY.md` — riscritto con struttura e nomi skill aggiornati
- `docs/setup.md` — aggiornata sezione Windsurf (regole globali espanse, flusso KB documentato)

### Changed

**Configurazione Windsurf**
- `~/.codeium/windsurf/memories/global_rules.md` — espansa con regole KB: file da leggere, pattern LAIF, come segnalare modifiche

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
- `docs/struttura.md` — albero cartelle riscritto come code block annotato (era Mermaid) + aggiunta core/ e knowledge/azienda/
- `docs/skills.md` — aggiornato con nomi, split, tabella confronto skill di manutenzione
- `CLAUDE.md` — aggiornati riferimenti a nuovi nomi skill + sezione beta + contesto aziendale + core/
- `skills/README.md` — aggiornato con colonne Stato/Legge/Scrive
- `knowledge/README.md` — aggiunta sezione Azienda con indice file
- `.gitignore` — aggiunte esclusioni per le tre repo core: laif-template, ds, laif-cdk

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
