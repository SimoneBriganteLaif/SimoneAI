# Changelog — Contenuti

Tutte le modifiche ai contenuti operativi: progetti, pattern, knowledge, decisioni tecniche.

Formato basato su [Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/).

Categorie usate:
- **Progetti** — nuovi progetti, cambi di stato, aggiornamenti
- **Pattern** — nuovi pattern, aggiornamenti a pattern esistenti
- **Knowledge** — nuove knowledge di industria o problemi tecnici
- **Decisioni** — ADR rilevanti cross-progetto

---

## [Non rilasciato]

### Progetti

- `projects/albini-castelli/` — registrato in INDEX.md (esisteva su disco con aws-config.yaml, non era tracciato)

### Skill

- Aggiunte righe di tracking uso (`.tags/skill-usage.log`) a 5 skill KB-only: feature-plan, feature-develop, feature-test, feature-review, verifica-pre-commit

---

## [v1.5] — 2026-03-09

### Pattern

- `patterns/list-detail-lazy-loading.md` — nuovo: lista leggera + dettaglio on-demand per UI con dati pesanti (body HTML, allegati)
- `patterns/html-sanitization-dompurify.md` — nuovo: sanitizzazione XSS con DOMPurify per HTML da fonti esterne (email, CMS)

### Knowledge

- `knowledge/azienda/processi.md` — aggiunta checklist refactoring: verifica multi-vista, utility condivise, sanitizzazione HTML

---

## [v1.4] — 2026-03-09

### Pattern

- `patterns/sqlalchemy-joinedload-unique.md` — nuovo: `.unique()` obbligatorio con `joinedload()` su collections in SQLAlchemy
- `patterns/fastapi-route-order.md` — nuovo: route statiche prima di parametriche in FastAPI
- `patterns/fullstack-dev-preview-loop.md` — nuovo: ciclo iterativo Backend Fix → Frontend Adapt → Preview Verify

### Skill

- `skills/development/setup-progetto-dev/SKILL.md` — nuovo: verifica ambiente dev locale (Docker, servizi, auth, migrazioni)
- `skills/development/brainstorming-post-sviluppo/SKILL.md` — nuovo: analisi fine sessione per estrarre pattern, skill, idee

### Idee

- `IDEAS.md` — aggiunta IDEA-013 (skill integrazione-email per setup OAuth)
- `IDEAS.md` — aggiunta IDEA-014 (brainstorming post-sviluppo come comportamento autonomo, completata)

---

## [v1.3] — 2026-03-09

### Progetti

**Jubatus — Documentazione progetto compilata**
- `projects/jubatus/architettura.md` — compilata: stack, diagramma, componenti, flussi, dipendenze, debito tecnico
- `projects/jubatus/decisioni.md` — 5 ADR documentate (AWS deploy, FastAPI, multi-provider email, mock data, template separation)
- `projects/jubatus/feature-log.md` — 4 feature registrate (email backend, tickets UI, scaffolding pagine, setup template)
- `projects/jubatus/requisiti.md` — aggiornato a v0.2: 3 domande aperte risolte (#2, #4, #5)
- `projects/jubatus/stato-progetto.md` — nuovo: mappa requisiti vs implementazione, blocchi critici, prossimi passi

---

## [v1.2] — 2026-03-09

### Progetti

**Jubatus — Inizializzazione**
- `projects/jubatus/` — nuovo progetto: piattaforma customer care per Jubatus (entertainment/eventi musicali)
- `projects/jubatus/meeting/` — 3 note meeting importate da Notion (kickoff 2026-01-23, ticketing 2026-01-28, customer care 2026-02-13)
- `projects/jubatus/requisiti.md` — bozza v0.1 con 11 RF estratti dalle note meeting (tutti da validare)
- Repository codice: `/Users/simonebrigante/LAIF/repo/jubatus/`
