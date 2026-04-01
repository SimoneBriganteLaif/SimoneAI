# Andriani Sequencing — Analisi Completa

## 1. Overview

**Applicazione**: Sistema di schedulazione e sequenziamento della produzione per un pastificio industriale.

**Cliente**: Andriani S.p.A. — azienda leader nella produzione di pasta a base di cereali e legumi (gluten-free, biologica). Sede a Gravina in Puglia.

**Industria**: Food Manufacturing / Produzione Alimentare Industriale.

**Cosa fa**: L'app ottimizza la pianificazione della produzione di pasta su più linee produttive. Gestisce l'intero ciclo: dagli ordini clienti, alla schedulazione della pastificazione, al confezionamento (packaging primario e secondario), fino all'export dei piani verso i sistemi aziendali. Utilizza **Google OR-Tools CP-SAT** per risolvere il problema di ottimizzazione combinatoria multi-obiettivo (minimizzare ritardi, setup, bilanciare carichi tra linee).

**Cod. Applicazione**: 2024054

---

## 2. Versioni

| Elemento | Versione |
|---|---|
| App (`version.txt`) | **4.7.42** |
| Template LAIF (`version.laif-template.txt`) | **5.6.7** |
| values.yaml version | 1.1.0 |
| Python | 3.12 |
| Node.js | >= 25.0.0 |
| PostgreSQL | 17.6 (con pgvector) |

---

## 3. Team (top contributors)

| # Commits | Contributor |
|---|---|
| 310 | mattiagualandi |
| 269 | Pinnuz |
| 199 | mlife |
| 186 | github-actions[bot] |
| 133 | Simone Brigante |
| 86 | bitbucket-pipelines |
| 85 | Marco Pinelli |
| 75 | neghilowio |
| 61 | cavenditti-laif |
| 58 | Matteo Scalabrini |
| 50 | Carlo A. Venditti |
| 49 | sadamicis |
| 48 | matteeeeeee |
| 38 | SimoneBriganteLaif |
| 33 | mattiagualandi01 |
| 32 | lorenzoTonetta |
| 28 | Daniele DN |
| 25 | cri-p |

Team molto numeroso (~20+ contributori), indicatore di un progetto ad alta priorita.

---

## 4. Stack e Dipendenze

### Backend (Python 3.12, FastAPI)

**Dipendenze standard template**: SQLAlchemy, Alembic, Pydantic v2, FastAPI, uvicorn, boto3, bcrypt/passlib, python-jose, httpx, requests.

**Dipendenze custom / non-standard**:

| Dipendenza | Uso |
|---|---|
| `ortools ~= 9.12` | **Solver OR-Tools CP-SAT** per schedulazione produzione (dependency group `etl`) |
| `pandas >= 2.2` | Elaborazione dati ETL e export Excel |
| `openpyxl >= 3.1` | Lettura file Excel input |
| `psutil >= 5.9` | Monitoraggio risorse durante ottimizzazione |
| `openai ~= 2.21` | Integrazione LLM (dependency group `llm`) |
| `pgvector ~= 0.4` | Embedding vettoriali per RAG/chat (dependency group `llm`) |
| `pymupdf ~= 1.27` | Parsing PDF (dependency group `pdf`) |
| `python-docx ~= 1.2` | Generazione documenti Word |
| `xlsxwriter ~= 3.2` | Generazione report Excel |
| `aiohttp ~= 3.13` | Client HTTP async |
| `click == 8.2` | CLI aggiuntiva |
| `dotenv >= 0.9` | Gestione env vars |

### Frontend (Next.js 16, React 19, TypeScript)

**Dipendenze custom / non-standard**:

| Dipendenza | Uso |
|---|---|
| `@amcharts/amcharts5` | Grafici KPI avanzati |
| `draft-js` + plugins (mention, export-html) | Rich text editing |
| `@hello-pangea/dnd` | Drag & drop |
| `react-dnd` | Drag & drop alternativo |
| `katex` + `rehype-katex` + `remark-math` | Rendering formule matematiche |
| `react-markdown` + `remark-gfm` | Rendering Markdown |
| `react-syntax-highlighter` | Evidenziazione codice |
| `@microsoft/fetch-event-source` | Server-Sent Events (streaming LLM) |
| `framer-motion` | Animazioni UI |
| `@ducanh2912/next-pwa` | Progressive Web App |
| `laif-ds` v0.2.73 | Design system LAIF |

### Servizi Docker

- **db**: PostgreSQL 17.6 con pgvector
- **backend**: FastAPI con supporto XLSX abilitato
- **etl**: Container separato per il solver OR-Tools (eseguito anche su **AWS ECS** in produzione con autoscaling)

---

## 5. Modello Dati Completo

### Schema `prs` (Presentation Layer) — 30+ tabelle

```mermaid
erDiagram
    %% === IMPIANTO ===
    Plant {
        int id PK
        str cod_plant UK
        str des_plant
    }

    ProductionLine {
        int id PK
        int id_plant FK
        str cod_production_line UK
        str des_production_line
        bool flg_parallel_packaging
    }

    Silo {
        int id PK
        int id_plant FK
        str cod_silo UK
        str des_silo
        int val_capacity
    }

    MicroSilo {
        int id PK
        int id_macro_silo FK
        str des_micro_silo
        bool flg_active
    }

    ProductionLineToSilo {
        int id PK
        int id_production_line FK
        int id_silo FK
        int id_macro_format FK
    }

    PackagingPrimaryLine {
        int id PK
        int id_plant FK
        str cod_packaging_primary_line UK
        str des_packaging_primary_line
        enum cod_packaging_primary_type
    }

    PackagingSecondaryLine {
        int id PK
        int id_plant FK
        str cod_packaging_secondary_line UK
        str des_packaging_secondary_line
    }

    PackagingPrimaryToSecondaryLine {
        int id PK
        int id_packaging_primary_line FK
        int id_packaging_secondary_line FK
    }

    ProductionToPackagingPrimaryLine {
        int id PK
        int id_production_line FK
        int id_packaging_primary_line FK
    }

    %% === FORMATO / TRAFILE ===
    MacroFormat {
        int id PK
        str cod_macro_format UK
        str des_macro_format
    }

    Format {
        int id PK
        int id_macro_format FK
        str cod_format UK
        str des_format
        float val_specific_weight
    }

    FormatToFormat {
        int id PK
        int id_format_from FK
        int id_format_to FK
        int val_change_time_minutes
    }

    Die {
        int id PK
        str cod_die UK
        str des_die
        int val_washing_time
    }

    FormatDie {
        int id PK
        int id_format FK
        int id_die FK
    }

    ProductionLineDie {
        int id PK
        int id_production_line FK
        int id_die FK
        bool flg_pastificabile
    }

    ProductionLineMacroFormat {
        int id PK
        int id_production_line FK
        int id_macro_format FK
        decimal num_pastification_to_package_hours_time
    }

    %% === RICETTE ===
    RecipeGroup {
        int id PK
        str cod_recipe_group UK
        str des_recipe_group
    }

    Recipe {
        int id PK
        int id_recipe_group FK
        str cod_recipe UK
        str des_recipe
        bool flg_biological
        enum cod_recipe_type
        bool flg_opportunity
    }

    RecipeToRecipe {
        int id PK
        int id_recipe_from FK
        int id_recipe_to FK
        int val_change_time_minutes
    }

    %% === PRODOTTI ===
    SemiFinishedProduct {
        int id PK
        int id_format FK
        int id_recipe FK
        str cod_semi_finished_product UK
        str des_semi_finished_product
    }

    ProductionLineSemiFinishedProduct {
        int id PK
        int id_production_line FK
        int id_semi_finished_product FK
        float val_kg_per_hour
        bool flg_active
    }

    Customer {
        int id PK
        str cod_customer UK
        str des_customer
    }

    Brand {
        int id PK
        str cod_brand UK
        str des_brand
    }

    Product {
        int id PK
        int id_semi_finished_product FK
        int id_brand FK
        int id_packaging_primary FK
        int id_packaging_secondary FK
        str cod_product
        str des_product
        decimal val_grams_per_piece
    }

    PackagingPrimary {
        int id PK
        str cod_packaging_primary UK
        str des_packaging_primary
        enum cod_packaging_primary_type
        float val_length
        float val_width
        float val_height
        float val_fronte_fascia
    }

    PackagingSecondary {
        int id PK
        str cod_packaging_secondary UK
        str des_packaging_secondary
        float val_length
        float val_width
        float val_height
    }

    PackagingPrimaryLineProduct {
        int id PK
        int id_packaging_primary_line FK
        int id_product FK
        int num_bpm
    }

    %% === ORDINI E SCHEDULING ===
    Orders {
        int id PK
        str cod_order UK "computed"
        str cod_original_order
        str cod_macro_order
        str cod_semi_finished_product FK
        str cod_order_type
        str cod_macro_order_status
        int id_line FK
        str cod_recipe FK
        str cod_format FK
        str cod_brand FK
        str cod_article "computed"
        str cod_week_slot
        int num_week_slot "computed"
        datetime tms_start
        datetime tms_end
        decimal val_kg
        decimal val_kg_with_extra
        bool flg_locked
    }

    LkpRuns {
        int id PK
        datetime tms_start
        datetime tms_end
        int id_user FK
        enum cod_customer_vs_efficency
        bool flg_active
        str des_run
        int num_week_horizon
        enum cod_run_type
        str ecs_task_id
        jsonb dict_params
        enum cod_run_status
        enum cod_run_error_type
        bool flg_exported
        jsonb run_steps
    }

    EtlErrors {
        int id PK
        int id_run FK
        enum cod_stage
        str cod_entity
        str cod_error
        str des_error
        jsonb dict_extra
    }

    SchedulingSolutions {
        int id_run PK_FK
        str cod_order PK
        int id_line FK
        datetime tms_start
        datetime tms_end
        decimal computed_kg_mix
        str cod_week_production
        decimal val_delay_hours
        jsonb dict_extra_info
        bool flg_locked
        str des_recipe
        str des_format
        jsonb packaging_primary
        jsonb packaging_secondary
    }

    PackagingSolutions {
        int id_run PK_FK
        str cod_order PK
        int id_production_line FK
        int id_packaging_line FK
        datetime tms_start_packaging
        datetime tms_end_packaging
    }

    WeeklyKpiResults {
        int id PK
        int id_run FK
        int id_line FK
        int num_year
        int num_week
        decimal val_kg
        decimal val_kg_mix
        decimal val_setup_hours
        int num_recipe_setups
        int num_format_setups
        int num_delays
        decimal val_delays_hours
    }

    PackagingKpis {
        int id PK
        int id_run FK
        int id_line FK
        int num_year
        int num_week
        int num_packed_orders
        int num_packing_time
        int num_stale_time
        int num_setup_time
        int num_short_setups
        int num_medium_setups
        int num_long_setups
    }

    %% === CONFIGURAZIONE E CALENDARIO ===
    Configuration {
        int id_configuration PK
        str cod_configuration UK
        decimal val_configuration
        str des_configuration
    }

    SchedulerConfig {
        int id PK
        jsonb dict_config
    }

    Closings {
        int id PK
        str des_name
        datetime tms_start
        datetime tms_end
    }

    Maintenances {
        int id PK
        int id_production_line FK
        int num_week_slot
        str des_maintenance
    }

    Unavailabilities {
        int id PK
        int id_production_line FK
        int id_packaging_primary_line FK
        str des_unavailability
        datetime tms_start
        datetime tms_end
    }

    %% === RELAZIONI ===
    Plant ||--o{ ProductionLine : "ha"
    Plant ||--o{ Silo : "ha"
    Plant ||--o{ PackagingPrimaryLine : "ha"
    Plant ||--o{ PackagingSecondaryLine : "ha"

    Silo ||--o{ MicroSilo : "contiene"
    ProductionLine ||--o{ ProductionLineToSilo : ""
    Silo ||--o{ ProductionLineToSilo : ""
    MacroFormat ||--o{ ProductionLineToSilo : ""

    ProductionLine ||--o{ ProductionToPackagingPrimaryLine : ""
    PackagingPrimaryLine ||--o{ ProductionToPackagingPrimaryLine : ""
    PackagingPrimaryLine ||--o{ PackagingPrimaryToSecondaryLine : ""
    PackagingSecondaryLine ||--o{ PackagingPrimaryToSecondaryLine : ""

    MacroFormat ||--o{ Format : "contiene"
    MacroFormat ||--o{ ProductionLineMacroFormat : ""
    ProductionLine ||--o{ ProductionLineMacroFormat : ""

    Format ||--o{ FormatDie : ""
    Die ||--o{ FormatDie : ""
    Die ||--o{ ProductionLineDie : ""
    ProductionLine ||--o{ ProductionLineDie : ""

    Format ||--o{ FormatToFormat : "from"
    Format ||--o{ FormatToFormat : "to"

    RecipeGroup ||--o{ Recipe : "raggruppa"
    Recipe ||--o{ RecipeToRecipe : "from"
    Recipe ||--o{ RecipeToRecipe : "to"

    Format ||--o{ SemiFinishedProduct : ""
    Recipe ||--o{ SemiFinishedProduct : ""
    SemiFinishedProduct ||--o{ ProductionLineSemiFinishedProduct : ""
    ProductionLine ||--o{ ProductionLineSemiFinishedProduct : ""

    SemiFinishedProduct ||--o{ Product : ""
    Brand ||--o{ Product : ""
    PackagingPrimary ||--o{ Product : ""
    PackagingSecondary ||--o{ Product : ""

    PackagingPrimaryLine ||--o{ PackagingPrimaryLineProduct : ""
    Product ||--o{ PackagingPrimaryLineProduct : ""

    ProductionLine ||--o{ Orders : ""
    Recipe ||--o{ Orders : ""
    Format ||--o{ Orders : ""
    Brand ||--o{ Orders : ""
    SemiFinishedProduct ||--o{ Orders : ""

    LkpRuns ||--o{ EtlErrors : ""
    LkpRuns ||--o{ SchedulingSolutions : ""
    LkpRuns ||--o{ WeeklyKpiResults : ""
    LkpRuns ||--o{ PackagingKpis : ""
    LkpRuns ||--o{ PackagingSolutions : ""

    ProductionLine ||--o{ SchedulingSolutions : ""
    ProductionLine ||--o{ PackagingSolutions : ""
    PackagingPrimaryLine ||--o{ PackagingSolutions : ""

    Maintenances }o--|| ProductionLine : ""
    Unavailabilities }o--o| ProductionLine : ""
    Unavailabilities }o--o| PackagingPrimaryLine : ""
```

### Schema `stg` (Staging Layer) — 3 tabelle

| Tabella | Descrizione |
|---|---|
| `stg.product` (StgProduct) | Anagrafica prodotti raw da CSV (51+ colonne, dati grezzi con commenti su edge case) |
| `stg.portate_orarie_linee` (StgPortateOrarieLinee) | Portate orarie per linea/formato/ricetta |
| `stg.macro_ordini` (StgMacroOrdini) | Macro ordini raw da CSV con dati denormalizzati |

---

## 6. API Routes

### App Routes (custom)

| Gruppo | Prefix | Operazioni |
|---|---|---|
| **Plant** | `/plant` | CRUD standard |
| **Production Line** | `/production-line` | CRUD standard |
| **Silo** | `/silo` | CRUD standard |
| **Packaging Primary Line** | `/packaging-primary-line` | CRUD + prodotti associati |
| **Packaging Secondary Line** | `/packaging-secondary-line` | CRUD standard |
| **Packaging Primary Line Product** | `/packaging-primary-line-product` | CRUD (BPM confezionamento) |
| **Production Line To Silo** | `/production-line-to-silo` | CRUD associazione |
| **Production To Packaging** | `/production-to-packaging-primary-line` | CRUD associazione |
| **Packaging Primary To Secondary** | `/packaging-primary-to-secondary-line` | CRUD associazione |
| **Production Line Semi Finished Product** | `/production-line-semi-finished-product` | CRUD (portate pastificazione) |
| **Die (Trafile)** | `/die` | CRUD standard |
| **Format** | `/format` | CRUD standard |
| **Macro Format** | `/macro-format` | CRUD standard |
| **Production Line Die** | `/production-line-die` | CRUD associazione |
| **Production Line Macro Format** | `/production-line-macro-format` | CRUD associazione |
| **Format To Format** | `/format-to-format` | CRUD (tempi cambio formato) |
| **Format Die** | `/format-die` | CRUD associazione |
| **Recipe** | `/recipe` | CRUD standard |
| **Recipe Group** | `/recipe-group` | CRUD standard |
| **Recipe To Recipe** | `/recipe-to-recipe` | CRUD (tempi cambio ricetta) |
| **Customer** | `/customer` | CRUD standard |
| **Brand** | `/brand` | CRUD standard |
| **Product** | `/product` | CRUD standard |
| **Packaging Primary** | `/packaging-primary` | CRUD standard |
| **Packaging Secondary** | `/packaging-secondary` | CRUD standard |
| **Semi Finished Product** | `/semi-finished-product` | CRUD standard |
| **Configuration** | `/configuration` | CRUD parametri schedulatore |
| **Orders** | `/orders` | CRUD ordini (con validazione errori) |
| **Runs** | `/runs` | CRUD + export Excel + download silos ZIP + export output S3 |
| **Scheduling Solutions** | `/scheduling-solutions` | CRUD soluzioni schedulazione |
| **Packaging Solution** | `/packaging-solution` | Soluzioni packaging |
| **Weekly KPI** | `/weekly-kpi` | KPI settimanali per run |
| **Changelog** | `/changelog` | Changelog applicativo |
| **ETL** | `/etl` | `POST /run` (lancio ETL locale o AWS), `POST /{id}/kill`, `GET /{id}/errors` |

### Template Routes (standard LAIF)
Auth, Users, Roles, Groups, Permissions, Business, Files, Chat/Conversation, Notifications, Health, Ticketing, FAQs, Analytics, Summary, Tasks, Loaders.

---

## 7. Business Logic

### ETL Pipeline (3 step)

Il cuore dell'applicazione e un pipeline ETL a 3 fasi (~23.000 righe di codice Python):

1. **STG (Staging)**: Legge CSV da **AWS S3** (`{mode}-sequencing-data-bucket`), li normalizza con Pandas e li carica nelle tabelle `stg.*`. File input: `AnagraficaItems.csv`, `PortateOrarieLinee.csv`, `ListaMacroOrdini.csv`, plus dati statici (trafile, pesi specifici, BPM confezionamento).

2. **PRS (Presentation)**: Trasforma i dati staging in entita normalizzate (prodotti, formati, ricette, semilavorati, ordini) con validazione e error tracking.

3. **MDL (Model)**: Il solver di ottimizzazione OR-Tools CP-SAT. Architettura modulare:
   - `SchedulerInstance`: carica dati e configurazione
   - `SchedulerConfig`: parametri solver (timeout, obiettivi, settimane, cluster size)
   - `ProductionScheduler`: orchestratore principale
   - `SchedulerVariableCreator`: creazione variabili CP-SAT
   - `SchedulerConstraints`: vincoli (2496 righe!) — assegnamento linee, setup ricetta/formato, silos, manutenzioni, chiusure, indisponibilita, packaging
   - `SchedulerObjectiveSetter`: funzioni obiettivo multi-obiettivo (minimizzare makespan, ritardi, setup, gap, efficienza)
   - `SolutionCallback` + `SolutionValidator`: monitoraggio e validazione soluzioni
   - `DatabaseSaver`: salvataggio soluzioni nel DB
   - `ReportGenerator` + `SystemMonitor`: report e monitoraggio risorse

### Obiettivi di ottimizzazione

- `MINIMIZE_MAKESPANS` — bilanciare carico tra linee
- `MINIMIZE_DELAY` — minimizzare ritardi consegna
- `MINIMIZE_SETUPS` — minimizzare cambi ricetta/formato
- `MINIMIZE_GAP` — minimizzare gap temporali
- `WEIGHTED_MULTI_OBJECTIVE` — combinazione pesata (default)
- `MAXIMIZE_EFFICIENCY` — massimizzare efficienza

### Background Tasks

- **ETL schedulato**: `repeat_every(60min)` controlla se e ora 2:00 e `flg_etl_enabled` e true, poi lancia STG+PRS (attualmente **commentato** per evitare sovrascritture durante run lunghe notturne).
- **ETL on-demand**: via API `/etl/run` come FastAPI `BackgroundTask` (locale) o come **AWS ECS Task** (produzione) con autoscaling ASG.

### Esecuzione su AWS ECS

Il solver gira su un cluster ECS dedicato (`{mode}-sequencing-etl-cluster`) con:
- Capacity provider con ASG (scale a 0 dopo completamento)
- Task definition separata per ETL
- Kill automatico del task ECS al termine del run
- Deploy separato via GitHub Actions (`build-and-deploy-etl.dev.yml`)

---

## 8. Integrazioni Esterne

| Integrazione | Dettaglio |
|---|---|
| **AWS S3** | Bucket dati (`{mode}-sequencing-data-bucket`) per input CSV, output CSV, file silos flow |
| **AWS ECS** | Esecuzione solver su cluster dedicato con autoscaling |
| **AWS ASG** | Autoscaling group per capacity provider ECS (scale down a 0 dopo run) |
| **OpenAI** | Integrazione LLM (dependency group, probabilmente per chat template) |
| **pgvector** | Embedding vettoriali PostgreSQL (RAG/knowledge base template) |

---

## 9. Albero Pagine Frontend

### Pagine App (custom)

```
/ (authenticated)
├── /schedule                        — Dashboard schedulazione (Gantt chart, KPI)
│   └── /schedule/create             — Creazione nuovo run (parametri solver)
├── /orders                          — Gestione ordini (tabella, errori, filtri)
├── /configurations/
│   ├── /production-lines/lines      — Linee di produzione
│   ├── /production-lines/bpm        — Portate pastificazione (kg/h per linea/semilavorato)
│   ├── /packaging-lines/primary-lines    — Linee confezionamento primario
│   ├── /packaging-lines/secondary-lines  — Linee confezionamento secondario
│   ├── /packaging-lines/bpm         — BPM confezionamento
│   ├── /formats/list                — Formati pasta
│   ├── /formats/timings             — Tempi cambio formato
│   ├── /dies                        — Trafile
│   ├── /recipes/list                — Ricette
│   ├── /recipes/groups              — Gruppi ricette
│   ├── /recipes/timings             — Tempi cambio ricetta
│   ├── /packaging                   — Packaging primario/secondario
│   ├── /closings                    — Chiusure stabilimento
│   ├── /maintenances                — Manutenzioni programmate
│   └── /unavailabilities            — Indisponibilita linee
├── /archive                         — Archivio run precedenti
├── /changelog-customer              — Changelog cliente
└── /changelog-technical             — Changelog tecnico
```

### Pagine Template (standard LAIF)
Login, Logout, Registration, Profile, User Management (users/roles/groups/permissions/business), Files, Help (FAQ/Ticket), Conversation (chat/feedback/knowledge/analytics).

### Widget custom notabili
- **Gantt Chart**: Widget custom completo per la visualizzazione del piano di produzione, con task card, popover dettaglio, controlli vista, preview block. Implementato da zero (non libreria esterna).
- **Grafici**: Widget grafici con amCharts5 per KPI settimanali.

---

## 10. Deviazioni dal Template LAIF

### Struttura extra

| File/Cartella | Descrizione |
|---|---|
| `backend/src/app/etl/` | Intero modulo ETL con solver OR-Tools (~23.000 righe) |
| `backend/src/app/generic.py` | Base classes custom (`ExtendedBase` con schema `prs`, `ExtendedStgBase` con schema `stg`) |
| `backend/src/app/enums.py` | Enum di dominio molto ricchi (15+ enum) |
| `backend/src/app/events.py` | Background task schedulato ETL |
| `backend/src/app/config.py` | Settings custom (ETL flags) |
| `docker-compose.yaml` service `etl` | Container ETL separato con dipendenze OR-Tools |
| `docker-compose.wolico.yaml` | Compose per ambiente Wolico (condivisione infra?) |
| `.github/workflows/build-and-deploy-etl.dev.yml` | CI/CD separata per container ETL |
| `frontend/src/widgets/gantt/` | Widget Gantt chart custom |
| `frontend/src/widgets/graphs/` | Widget grafici custom |
| `frontend/src/features/schedule/` | Feature complessa con store, hooks, dashboard, create |
| `frontend/src/features/orders/` | Feature ordini con dashboard e tabelle |
| `frontend/src/features/formats/` | Gestione formati con tabs |
| `frontend/src/features/recipes/` | Gestione ricette con tabs |
| `frontend/src/features/changelog/` | Changelog custom |
| `frontend/src/archive/` | Archivio run |
| `db/Dockerfile` | PostgreSQL custom con pgvector |
| `docs/` | Documentazione estesa (backend, frontend, tooling) |

### Dependency groups nel pyproject.toml

Uso sofisticato di dependency groups (`pdf`, `docx`, `llm`, `xlsx`, `etl`, `debugger`, `pycharm-debugger`) per caricare solo le dipendenze necessarie per ogni container (backend vs etl).

---

## 11. Pattern Notabili

### Architettura Solver
Il solver e strutturato secondo il **CP-SAT primer** di Google con separazione netta tra:
- Dati/configurazione (`SchedulerInstance` + `SchedulerConfig`)
- Creazione variabili (`SchedulerVariableCreator`)
- Vincoli (`SchedulerConstraints`)
- Obiettivi (`SchedulerObjectiveSetter`)
- Monitoring (`SolutionCallback`, `SystemMonitor`, `SolutionValidator`)

Pattern molto maturo e ben organizzato per un solver di ~5000+ righe.

### Setup Matrix
Matrice dei tempi di cambio tra ricette e formati, elemento chiave dell'ottimizzazione. Modellata come grafo diretto con pesi (tempi in minuti) nelle tabelle `recipe_to_recipe` e `format_to_format`.

### Computed Columns PostgreSQL
Uso estensivo di `Computed()` per colonne derivate (durata ordini, cod_order composto, cod_article normalizzato, cod_year_week).

### Hybrid Properties complesse
Logica di validazione ordini (`lst_errors`, `has_errors`) implementata come hybrid property con doppia implementazione Python + SQL expression per supporto sia in-memory che query.

### Denormalizzazione strategica
`SchedulingSolutions` denormalizza intenzionalmente dati da ordini (ricetta, formato, packaging) per evitare join e garantire consistenza storica.

### ETL a 3 livelli (STG/PRS/MDL)
Pattern data warehouse classico adattato: staging grezzo da CSV S3, presentazione normalizzata, modello di ottimizzazione.

### ECS Task con ASG scale-to-zero
Pattern cost-effective per workload compute-intensive: l'ASG scala a 0 dopo il completamento del task, evitando costi idle.

---

## 12. Note e Tech Debt

### Tech Debt

1. **ETL notturno commentato**: Il background task `run_etl` e commentato da settembre 2025 per evitare sovrascritture durante run lunghe. Potrebbe servire un meccanismo di lock piu robusto.

2. **MINUTES_PER_HOUR = 50**: Costante che definisce 50 minuti per "ora produttiva" (probabilmente per pause/setup). Potrebbe confondere chi non conosce il dominio.

3. **TODO in pyproject.toml**: `# TODO maybe only use one?` per httpx vs requests — doppia dipendenza HTTP client.

4. **BUG noto in docker-compose**: `# BUG: currently if profiles is set, env_file is not loaded` per il container ETL.

5. **CHANGELOG non aggiornato**: Contiene solo la release iniziale `0.1` del 2025-02-04, nonostante la versione sia 4.7.42.

6. **Linee mappate hardcoded**: `LINE_MAPPING` e `CONF_MAPPING` hardcodano i nomi delle linee di Andriani (LINEA 1-7, Conf 1-12). Fragile se cambiano.

7. **PAST_TO_PACK_OFFSET_MINUTES hardcodato**: Tempi di essicazione per macro formato hardcodati nel codice.

### Peculiarita

- **Dominio molto specifico**: L'app modella fedelmente il processo produttivo di un pastificio (trafile, essiccazione, silos, confezionamento primario/secondario).
- **Scala computazionale**: Il solver CP-SAT ha timeout fino a 10 ore (36000s) e supporta clustering di settimane per problemi grandi.
- **Errori ETL tipizzati**: 12+ tipi di errore MDL specifici del dominio (ordine troppo piccolo, linea non compatibile, ceci mancanti, ecc.).
- **RunCodErrorType.CHICKPEAS_MISSING**: Errore specifico per ceci mancanti — indica vincoli di produzione molto specifici.
- **Export output verso cartella condivisa**: Il sistema esporta `OutputSchedulatore.csv` verso una cartella S3 `input-data/Output/` per l'accesso da parte di altri sistemi aziendali.
- **Supporto packaging-only**: Possibilita di rieseguire solo la fase di packaging senza ricalcolare la pastificazione.
- **docker-compose.wolico.yaml**: Presenza di un compose Wolico suggerisce condivisione infrastruttura o testing cross-progetto.
