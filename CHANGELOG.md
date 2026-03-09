# Changelog

Tutte le modifiche al sistema SimoneAI: struttura (cartelle, skill, template, processi) e contenuti (progetti, pattern, knowledge).

Formato basato su [Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/).

---

## [Non rilasciato]

### Struttura

#### Added

**v1.7 — Miglioramenti gestione skill e knowledge**
- `CHANGELOG.md` — changelog unificato (merge di CHANGELOG-framework.md + CHANGELOG-contenuti.md), sezioni `### Struttura` e `### Contenuti` per versione
- `skills/meta/contesto-progetto/match.py` — script deterministico: dato un progetto, trova pattern/knowledge/industrie rilevanti per tag matching
- `.claude/hooks/skill-logger.sh` — hook PostToolUse per tracking automatico invocazioni skill native
- `.claude/settings.json` — registrazione hook PostToolUse con matcher "Skill"
- `knowledge/industrie/entertainment.md` — conoscenza settore entertainment/eventi (da esperienza Jubatus)
- `knowledge/industrie/healthcare.md` — conoscenza settore healthcare/medical devices (da esperienza Lamonea)
- `knowledge/problemi-tecnici/query-n-plus-1.md` — problema N+1 con ORM, cross-link a pattern
- `knowledge/problemi-tecnici/xss-contenuto-esterno.md` — XSS da HTML esterno, cross-link a pattern
- `knowledge/problemi-tecnici/routing-conflitti-parametrici.md` — route statiche vs parametriche, cross-link a pattern
- `.tags/index.md` — registrato tag `#progetto:lamonea` e aggiornato `#industria:healthcare`
- `.claude/skills/` — ristrutturate da file piatti (`.md`) a directory con `SKILL.md` dentro (17 skill) per corretta auto-discovery dal Skill tool
- `.claude/skill-usage.log` — spostato da `.tags/` a `.claude/` (gitignored, file runtime che cresce)

#### Changed

- `CLAUDE.md` — snellito da ~210 a ~105 righe: estratte sezioni "Workflow per fase", "Tag standard", "Sistema ibrido skill" verso docs/. Aggiunta Regola 4.2 (contesto proattivo via match.py) e Regola 5.4 (verifica problemi tecnici)
- `docs/skills.md` — aggiunta sezione "Ciclo di vita delle skill" con criteri graduazione beta→stable; aggiunta sezione "Dipendenze tra skill" con diagramma Mermaid; aggiunta tabella disambiguazione "Quando NON usare una skill"; aggiornato formato SKILL.md con depends-on/enables
- `docs/struttura.md` — aggiornato albero con: CHANGELOG.md unificato, contesto-progetto/, industrie popolate, problemi-tecnici popolati, .claude/hooks/, .claude/settings.json
- `skills/README.md` — aggiornati stati skill promosse (estrazione-requisiti, estrazione-decisioni, estrazione-pattern → stable); aggiunto contesto-progetto
- `skills/meta/gestione-kb/SKILL.md` — v1.1: riferimenti aggiornati a CHANGELOG.md unificato
- `skills/meta/verifica-pre-commit/check_changelog.py` — riscritto per changelog unificato (cerca ### Struttura e ### Contenuti dentro [Non rilasciato])
- `skills/maintenance/audit-periodico/SKILL.md` — aggiunto Step 6 "Skill health report" (frequenza uso, candidate promozione, skill inutilizzate)
- `skills/development/brainstorming-post-sviluppo/SKILL.md` — riferimento aggiornato a CHANGELOG.md
- `System.md` — versione 1.7, link a CHANGELOG.md unificato
- `.gitignore` — aggiunto `!.claude/hooks/` e `!.claude/settings.json` per versionare hook e config
- `.tags/index.md` — aggiunti file knowledge a tag #problema:*, #stack:*, #industria:*

**Promozione skill a stable**
- `skills/presales/estrazione-requisiti/SKILL.md` — stato: beta → stable, versione 1.1, aggiunti depends-on/enables
- `skills/development/estrazione-decisioni/SKILL.md` — stato: beta → stable
- `skills/development/estrazione-pattern/SKILL.md` — stato: beta → stable, aggiunti enables

#### Removed

- `CHANGELOG-framework.md` — sostituito da CHANGELOG.md unificato
- `CHANGELOG-contenuti.md` — sostituito da CHANGELOG.md unificato

### Contenuti

#### Progetti

- `projects/lamonea/` — nuovo progetto inizializzato (Lamonea S.R.L., healthcare/medical devices)
  - README.md compilato con contesto cliente, team, timeline, link
  - 5 meeting notes da Notion (kickoff interno, kickoff cliente, requisiti fase 1, dubbi TS, domande 5/3)
  - requisiti.md bozza con RF-CAT-01→08 e RF-CRM-01→10 da Notion
  - aws-config.yaml compilato (dev: 809472478744, prod: 889486284368)
  - INDEX.md aggiornato (3 progetti totali)

#### Knowledge

- `knowledge/industrie/entertainment.md` — nuovo: settore entertainment/eventi musicali, pain point, regolamentazioni, integrazioni tipiche
- `knowledge/industrie/healthcare.md` — nuovo: settore healthcare/medical devices, regolamentazioni MDR/UDI, integrazioni ERP
- `knowledge/problemi-tecnici/query-n-plus-1.md` — nuovo: problema N+1 con ORM e relazioni, soluzioni, cross-link pattern
- `knowledge/problemi-tecnici/xss-contenuto-esterno.md` — nuovo: XSS da HTML esterno, DOMPurify, cross-link pattern
- `knowledge/problemi-tecnici/routing-conflitti-parametrici.md` — nuovo: conflitti route statiche vs parametriche, cross-link pattern

---

## [v1.6] — 2026-03-09

### Struttura

#### Added

**Sistema ibrido skill — trigger layer nativo**
- `.claude/skills/` — 17 file skill native Claude Code (auto-discovery, UI, tracking automatico)
  - Presales: `init-project`, `estrazione-requisiti`, `genera-allegato-tecnico`, `genera-mockup-brief`
  - Development: `feature-workflow`, `estrazione-decisioni`, `estrazione-pattern`, `setup-progetto-dev`, `brainstorming-post-sviluppo`
  - AWS: `aws-triage`, `aws-ecs-diagnose`, `aws-logs-diagnose`, `aws-rds-diagnose`, `aws-s3-diagnose`, `aws-health-report`
  - Maintenance: `audit-periodico`
  - Meta: `gestione-kb`
- `.tags/skill-usage.log` — log uso skill KB-only (tracking automatico per skill senza wrapper nativo)

**AWS Diagnostics — pacchetto skill read-only**
- `skills/development/aws-diagnostics/` — 5 skill con script Python per diagnosi ambienti AWS LAIF
  - `aws-triage/` — health check rapido su tutti i servizi (ECS, RDS, Logs, S3)
  - `aws-ecs-diagnose/` — deep-dive ECS (deployment, task failure, capacity, config)
  - `aws-logs-diagnose/` — query CloudWatch Logs Insights (6 template + custom)
  - `aws-rds-diagnose/` — stato RDS, connessioni, log PostgreSQL, parametri
  - `aws-s3-diagnose/` — inventario bucket, dimensioni, upload recenti
  - `_shared/` — libreria Python condivisa (config, aws_runner, output) + documentazione
- `projects/_template/aws-config.yaml` — template configurazione risorse AWS per nuovi progetti

#### Changed

- `CLAUDE.md` — aggiunta sezione "Sistema ibrido skill" con spiegazione formato duale native/KB e tracking
- `docs/struttura.md` — aggiunta `.claude/skills/` e `.tags/skill-usage.log` all'albero
- `skills/README.md` — aggiunta colonna "Nativa" nella tabella skill
- `docs/skills.md` — aggiunta colonna "Nativa" nel Riepilogo, aggiunte 5 skill AWS diagnostics con diagrammi Mermaid
- `skills/development/feature-plan/SKILL.md` — aggiunta riga tracking uso
- `skills/development/feature-develop/SKILL.md` — aggiunta riga tracking uso (entrambe le modalità)
- `skills/development/feature-test/SKILL.md` — aggiunta riga tracking uso
- `skills/development/feature-review/SKILL.md` — aggiunta riga tracking uso
- `skills/meta/verifica-pre-commit/SKILL.md` — aggiunta riga tracking uso
- `docs/struttura.md` — aggiornato albero con aws-diagnostics/ e aws-config.yaml nel template progetto
- `skills/README.md` — aggiunte 5 skill AWS diagnostics alla tabella Development
- `.tags/index.md` — aggiunti tag `#stack:ecs`, `#stack:rds`, `#stack:cloudwatch`, `#stack:s3`
- `.gitignore` — `.claude/` → `.claude/*` + `!.claude/skills/` per versionare skill native; aggiunto `*.code-workspace`
- `System.md` — aggiornata versione a 1.6

### Contenuti

#### Progetti

- `projects/albini-castelli/` — registrato in INDEX.md (esisteva su disco con aws-config.yaml, non era tracciato)

#### Skill

- Aggiunte righe di tracking uso (`.tags/skill-usage.log`) a 5 skill KB-only: feature-plan, feature-develop, feature-test, feature-review, verifica-pre-commit

---

## [v1.5] — 2026-03-09

### Contenuti

#### Pattern

- `patterns/list-detail-lazy-loading.md` — nuovo: lista leggera + dettaglio on-demand per UI con dati pesanti (body HTML, allegati)
- `patterns/html-sanitization-dompurify.md` — nuovo: sanitizzazione XSS con DOMPurify per HTML da fonti esterne (email, CMS)

#### Knowledge

- `knowledge/azienda/processi.md` — aggiunta checklist refactoring: verifica multi-vista, utility condivise, sanitizzazione HTML

---

## [v1.4] — 2026-03-09

### Struttura

#### Added

- `skills/development/setup-progetto-dev/` v1.0 beta — verifica ambiente dev locale (Docker, servizi, auth, migrazioni DB)
- `skills/development/brainstorming-post-sviluppo/` v1.0 beta — analisi fine sessione per estrarre pattern, skill, idee per SimoneAI

#### Changed

- `CLAUDE.md` — aggiunta Regola 5 (comportamento autonomo): brainstorming post-sviluppo alla fine di ogni sessione significativa
- `docs/skills.md` — aggiunte 2 nuove skill development con diagrammi Mermaid, aggiornato diagramma globale
- `docs/struttura.md` — aggiornato albero con le 2 nuove skill

### Contenuti

#### Pattern

- `patterns/sqlalchemy-joinedload-unique.md` — nuovo: `.unique()` obbligatorio con `joinedload()` su collections in SQLAlchemy
- `patterns/fastapi-route-order.md` — nuovo: route statiche prima di parametriche in FastAPI
- `patterns/fullstack-dev-preview-loop.md` — nuovo: ciclo iterativo Backend Fix → Frontend Adapt → Preview Verify

#### Skill

- `skills/development/setup-progetto-dev/SKILL.md` — nuovo: verifica ambiente dev locale (Docker, servizi, auth, migrazioni)
- `skills/development/brainstorming-post-sviluppo/SKILL.md` — nuovo: analisi fine sessione per estrarre pattern, skill, idee

#### Idee

- `IDEAS.md` — aggiunta IDEA-013 (skill integrazione-email per setup OAuth)
- `IDEAS.md` — aggiunta IDEA-014 (brainstorming post-sviluppo come comportamento autonomo, completata)

---

## [v1.3] — 2026-03-09

### Struttura

#### Added

**Workflow multi-agente per feature development**
- `skills/development/feature-workflow/` v1.0 beta — orchestratore ciclo completo feature (Plan → Develop → Test + Review → Exit) con 3 gate di qualità
- `skills/development/feature-plan/` v1.0 beta — analizza requisito → piano implementazione tecnico
- `skills/development/feature-develop/` v1.0 beta — piano → implementazione (Claude Code diretto o brief Windsurf)
- `skills/development/feature-test/` v1.0 beta — scrive test, esegue suite, verifica criteri, edge case, regressioni
- `skills/development/feature-review/` v1.0 beta — review codice per qualità, aderenza pattern LAIF, duplicazioni
- `.feature-state.md` — nuovo file temporaneo di stato condiviso tra le fasi del workflow

**Template progetto**
- `projects/_template/stato-progetto.md` — mappa requisiti vs implementazione, blocchi critici, prossimi passi

#### Changed

- `docs/skills.md` — aggiunte 5 nuove skill development con diagrammi Mermaid e tabella comparativa aggiornata
- `docs/workflow.md` — aggiornato flusso Development con il nuovo workflow multi-agente
- `skills/README.md` — aggiunte 5 nuove skill al catalogo Development

**Convenzione repository progetti**
- Le repository di codice non vivono più dentro `projects/[nome]/repo/` ma in `/Users/simonebrigante/LAIF/repo/[nome]/`
- Rimossa copia residua `projects/jubatus/repo/`
- Aggiornati: `docs/struttura.md`, `System.md`, `projects/_template/README.md`, `projects/jubatus/README.md`
- `skills/presales/init-project/SKILL.md` — riscritta: rimosso clone repo, analisi da path esterno

#### Fixed

**Allineamento documentazione post-review v1.3**
- `docs/struttura.md` — aggiunto `projects/_archivio/` e `docs/setup.md` nell'albero
- `docs/skills.md` — `verifica-pre-commit`: corretto stato da "beta" a "stable", aggiornata descrizione e diagramma Mermaid
- `System.md` — aggiornata versione da 1.0 a 1.3
- `.tags/index.md` — aggiornato tag `#progetto:jubatus` con i nuovi file

### Contenuti

#### Progetti

**Jubatus — Documentazione progetto compilata**
- `projects/jubatus/architettura.md` — stack, diagramma, componenti, flussi, dipendenze, debito tecnico
- `projects/jubatus/decisioni.md` — 5 ADR documentate (AWS deploy, FastAPI, multi-provider email, mock data, template separation)
- `projects/jubatus/feature-log.md` — 4 feature registrate (email backend, tickets UI, scaffolding pagine, setup template)
- `projects/jubatus/requisiti.md` — aggiornato a v0.2: 3 domande aperte risolte
- `projects/jubatus/stato-progetto.md` — nuovo: mappa requisiti vs implementazione, blocchi critici, prossimi passi

---

## [v1.2] — 2026-03-09

### Struttura

#### Added

- `.gitignore` — aggiunta regola `projects/*/repo/` e `projects/*/repo-*/`
- `projects/_archivio/` — directory per progetti archiviati
- `.obsidian/app.json` — filtro `projects/*/repo/` per Obsidian
- `.obsidian/graph.json` — `-path:repo` per escludere repo dal grafo

#### Changed

**Skill verifica-pre-commit v3.0 — ibrido script + semantica**
- `skills/meta/verifica-pre-commit/` — riscritta: 5 script Python + check semantici in SKILL.md
- `CLAUDE.md` — aggiornate regole autonome: approccio ibrido script+semantica, regola gestione idee

**Ristrutturazione template progetto**
- `projects/_template/` — struttura piatta per tipo di contenuto (era per fase)
- `projects/jubatus/` — migrato alla nuova struttura piatta

### Contenuti

#### Progetti

- `projects/jubatus/` — nuovo progetto: piattaforma customer care (entertainment/eventi musicali)
- `projects/jubatus/meeting/` — 3 note meeting importate da Notion
- `projects/jubatus/requisiti.md` — bozza v0.1 con 11 RF estratti

---

## [v1.1] — 2026-03-08

### Struttura

#### Added

- `.obsidian/` — configurazione Obsidian con color-coded graph
- Link inter-file su tutti i 9 SKILL.md (footer navigazione)
- `knowledge/azienda/` breadcrumb cross-navigation
- `.tags/index.md` — aggiunti tag `#industria:software`, `#fase:contesto`, `#stack:fastapi`, `#stack:cdk`
- `System.md` — sezione "Navigazione documentazione" e "Manutenzione del sistema"
- `docs/skills.md` — nav breadcrumb, TOC, mappa globale Mermaid
- `docs/workflow.md` — nav breadcrumb, TOC, diagramma "Quale flusso usare?"
- `skills/meta/verifica-pre-commit/` v1.0 — skill autonoma pre-commit (5 check paralleli)
- `CLAUDE.md` — regole agenti autonomi (4 comportamenti obbligatori)
- `knowledge/azienda/` — 4 file: overview, stack, infrastruttura, processi
- `core/` — repo LAIF clonate (laif-template, ds, laif-cdk) con README

#### Changed

- `genera-documenti/` splittata in `genera-allegato-tecnico/` + `genera-mockup-brief/`
- `aggiornamento-kb/` rinominata in `estrazione-pattern/`
- `aggiornamento-periodico/` rinominata in `audit-periodico/`
- Tutte le skill: aggiunto stato beta/stable, legge/scrive nel frontmatter, sezione Perimetro

#### Fixed

- 9 riferimenti a skill rinominate corretti in docs, System.md, tags, skill SKILL.md

#### Removed

- `skills/presales/genera-documenti/` — sostituita da 2 skill separate

---

## [1.0.0] — 2026-03-08

Prima release della Knowledge Base.

### Struttura

#### Added

- Struttura cartelle: `projects/`, `patterns/`, `knowledge/`, `.tags/`, `skills/`
- 7 skill iniziali: init-project, estrazione-requisiti, genera-documenti, estrazione-decisioni, aggiornamento-kb, aggiornamento-periodico, gestione-kb
- Documentazione: `docs/struttura.md`, `docs/skills.md`, `docs/workflow.md`
- File di sistema: `CLAUDE.md`, `System.md`, `IDEAS.md`
- Inizializzazione repository Git
