# sabart-demfor

## Overview

**Applicazione**: Demand Forecasting per Sabart (probabilmente settore distribuzione/commercio articoli industriali)
**Cliente**: Sabart
**Settore**: Supply Chain / Demand Planning
**Stato**: Attivo, v5.7.0
**Repository**: `sabart-demfor`
**Codice applicazione**: 2024060
**Basato su laif-template**: Si (v5.6.1)

Sistema di previsione della domanda (demand forecasting) che combina modelli ML/AI con revisioni manuali da parte degli utenti. Il sistema gestisce un pipeline ETL completo: ingestione dati da S3, trasformazione, training modelli neurali, inferenza e presentazione risultati con possibilita di revisione umana.

## Versioni

| Componente | Versione |
|---|---|
| App | 5.7.0 |
| laif-template | 5.6.1 |
| Python | 3.12 |
| FastAPI | 0.128.0 |
| SQLAlchemy | 2.0.45 |
| Next.js | 16.1.1 |
| React | 19.2.3 |
| Node.js | >=24.0.0 |
| PyTorch (ETL) | 2.2.1 |

## Team

| Contributore | Commit |
|---|---|
| Pinnuz | 237 |
| mlife | 188 |
| github-actions[bot] | 106 |
| Simone Brigante | 95 |
| bitbucket-pipelines | 86 |
| Marco Pinelli | 85 |
| sadamicis | 49 |
| matteeeeeee | 47 |
| Matteo Scalabrini | 44 |
| cavenditti-laif | 42 |
| Daniele DN | 28 |
| Carlo A. Venditti | 25 |
| neghilowio | 25 |
| mlaif | 23 |
| SimoneBriganteLaif | 22 |
| angelolongano | 18 |
| Marco Vita | 17 |
| luca-stendardo | 13 |
| + altri minori | ~30 |

## Stack tecnico

### Backend
- **Framework**: FastAPI + Uvicorn
- **ORM**: SQLAlchemy 2.0 (sync)
- **DB**: PostgreSQL (Docker, porta 5432)
- **Migrazioni**: Alembic
- **Auth**: JWT (python-jose) + bcrypt/passlib
- **AWS**: boto3 (ECS, S3)
- **Export**: XlsxWriter + pandas
- **Package manager**: uv

### ETL (modulo separato)
- **ML Framework**: PyTorch 2.2.1
- **Scikit-learn**: 1.3.1
- **CatBoost**: >=1.2.8 (dependency group `train`)
- **Data processing**: Pandas 2.2.3, PyArrow
- **Explainability**: Captum 0.6.0
- **Serialization**: joblib
- **Container**: Docker separato, eseguito su ECS cluster AWS

### Frontend
- **Framework**: Next.js 16 + React 19 + TypeScript
- **State management**: Redux Toolkit + React Query (TanStack)
- **UI**: laif-ds 0.2.67, Tailwind CSS 4, Lucide React
- **Charts**: amCharts 5
- **Build**: Turbopack
- **Test**: Playwright

### Infrastruttura
- Docker Compose (backend + DB)
- AWS ECS (ETL cluster separato)
- AWS S3 (dati input, modelli, export)
- Region: eu-west-1

## Data model

Il database usa 3 schema: `stg` (staging), `prs` (presentation), `template` (laif-template).

### Schema `stg` — Staging Layer (dati grezzi da ERP)

| Tabella | Descrizione |
|---|---|
| `d_articoli` | Anagrafica articoli da ERP (cod_art, fornitore, classe materiale, linea, stato, prezzi, flag catalogo) |
| `d_articoli_univoci` | Articoli distinti (solo cod_art) |
| `d_calendar` | Calendario con flag weekend/festivi/estate |
| `d_clienti` | Anagrafica clienti (ragione sociale, indirizzo, agente, classificazione ABC) |
| `d_decodifiche` | Tabella di decodifica campi (nome_campo, codice, descrizione) |
| `f_ordini` | Fact table ordini (data, quantita, prezzi, sconti, stato) |
| `f_promozioni` | Promozioni per articolo (date inizio/fine, prezzo netto) |
| `f_sostituzioni` | Sostituzioni articoli (articolo originale -> sostituto, coefficiente) |
| `caps` | CAP italiani con provincia, regione, zona |

### Schema `prs` — Presentation Layer (dati elaborati)

| Tabella | Descrizione |
|---|---|
| `articles` | Articoli con FK a supplier, line, classe_mat, tipo_web_art |
| `suppliers` | Fornitori |
| `lines` | Linee prodotto |
| `classe_mat` | Classi materiale |
| `tipo_web_art` | Tipo web articolo |
| `ordini_cons` | Ordini consolidati per data/articolo (qty, prezzo, flag promo) |
| `demand_forecast` | Previsioni domanda per run/modello/data (partitioned by id_run) |
| `demand_review` | Revisioni manuali domanda per articolo/anno/mese |
| `lkp_runs` | Lookup run ETL (id_run, data inferenza) |
| `runtasks` | Stato task ETL (step, status, parametri JSON, ECS task id) |
| `new_articles` | Nuovi articoli da gestire (flag processed/to_handle) |
| `article_link` | Legami tra articoli (sostituzione con coefficienti) |
| `promo` | Promozioni data entry (date, nome) |
| `general_review` | Revisioni generali per dimensione (supplier/line/classe_mat/tipo_web_art, percentuale) |

### Materialized Views (schema `prs`)

| View | Descrizione |
|---|---|
| `lkp_month` | Calendario mesi con numero settimane |
| `monthly_orders` | Ordini mensili aggregati per articolo |
| `monthly_orders_py` | Ordini mensili anno precedente |
| `monthly_demand_forecast` | Forecast mensile aggregato per articolo |
| `adhoc_demand_review` | Vista combinata forecast + ordini + revisioni per review ad hoc |
| `weekly_demand_review` | Revisioni settimanali (qty e prezzo divisi per settimane del mese) |

### Diagramma ER (tabelle principali prs)

```mermaid
erDiagram
    Supplier {
        string cod_supplier PK
        string des_supplier
    }
    Line {
        string cod_line PK
        string des_line
    }
    ClasseMat {
        string cod_classe_mat PK
        string des_classe_mat
    }
    TipoWebArt {
        string cod_tipo_web_art PK
        string des_tipo_web_art
    }
    Article {
        string cod_art PK
        string des_art
        string cod_supplier FK
        string cod_line FK
        string cod_classe_mat FK
        string cod_tipo_web_art FK
        decimal val_price
    }
    LkpRun {
        int id_run PK
        date dat_inference
    }
    OrdiniCons {
        date dat_order PK
        string cod_art PK_FK
        int num_year
        int num_month
        decimal val_order_qty
        decimal val_order_price
        bool flg_promo
    }
    DemandForecast {
        int id_run PK_FK
        string cod_art PK_FK
        date dat_prediction PK
        string cod_model_type
        int num_year
        int num_month
        decimal val_prediction_qty
        decimal val_prediction_price
        bool flg_promo
    }
    DemandReview {
        string cod_art PK_FK
        int num_year PK
        int num_month PK
        decimal val_qty
    }
    NewArticle {
        int id PK
        string cod_art FK
        datetime tms_update
        bool flg_to_handle
        bool flg_processed
        int cod_stato_art
    }
    ArticleLink {
        int id PK
        string cod_art FK
        string cod_art_sost FK
        decimal val_coeff_art
        decimal val_coeff_art_sost
        bool flg_processed
    }
    Promo {
        int id PK
        string cod_art PK_FK
        date dat_start_promo
        date dat_end_promo
        string des_name
    }
    GeneralReview {
        int id PK
        string cod_type
        string cod_col
        date dat_start
        date dat_end
        decimal val_perc
        int id_user FK
    }
    RunTask {
        int uid PK
        string kind
        string step
        string status
        int model_id
        string description
        json dict_params
        datetime tms_start
        datetime tms_end
        string ecs_task_id
    }

    Supplier ||--o{ Article : "has"
    Line ||--o{ Article : "has"
    ClasseMat ||--o{ Article : "has"
    TipoWebArt ||--o{ Article : "has"
    Article ||--o{ OrdiniCons : "has orders"
    Article ||--o{ DemandForecast : "has forecasts"
    Article ||--o| NewArticle : "new article"
    Article ||--o{ ArticleLink : "linked to"
    Article ||--o{ Promo : "has promos"
    Article ||--o{ DemandReview : "has reviews"
    LkpRun ||--o{ DemandForecast : "run"
```

## API Routes

### Custom (non template)

| Metodo | Path | Descrizione |
|---|---|---|
| GET | `/etl/execute` | Avvia pipeline ETL su ECS (con parametri data, run, inference flag) |
| GET | `/etl/{id_run}/complete` | Completa un run ETL (refresh MV, kill task ECS) |
| GET | `/etl/{id_run}/kill` | Ferma un task ECS |
| GET | `/demand-forecast/run` | Lista tutti i run |
| POST | `/demand-forecast/{id_run}` | Dati chart forecast con filtri (dimensione, gruppo, articoli, fornitori, linee) |
| GET | `/demand-forecast/{id_run}/monthly-report` | Export XLSX report mensile |
| GET | `/demand-forecast/{id_run}/monthly-report-s3` | Export report mensile su S3 |
| GET/POST | `/adhoc-review/search` | Ricerca revisioni ad hoc |
| PUT | `/adhoc-review` | Aggiorna revisioni demand |
| DELETE | `/adhoc-review` | Elimina revisione per cod_art |
| GET | `/adhoc-review/export` | Export revisioni |
| CRUD | `/general-review/*` | CRUD completo revisioni generali (per dimensione) + export |
| CRUD | `/link/*` | CRUD legami articoli (search, create, update, delete) |
| CRUD | `/new-articles/*` | Search, update, export nuovi articoli |
| CRUD | `/promo/*` | Search, update, delete, export promozioni + upload CSV |
| GET | `/article/search` | Ricerca articoli |
| GET | `/supplier/search` | Ricerca fornitori |
| GET | `/line/search` | Ricerca linee |
| GET | `/classe_mat/search` | Ricerca classi materiale |
| GET | `/tipo_web_art/search` | Ricerca tipo web articolo |
| GET | `/changelog/` | Contenuto changelog (tech/customer, template/app) |

## Business logic

### Pipeline ETL (modulo `etl/`)

Pipeline multi-step eseguito su **AWS ECS** (cluster dedicato `sabart-etl-cluster`):

1. **Staging** (`tasks/staging/`): Scarica CSV da S3, li processa (cast tipi, trasformazioni custom, gestione booleani), li carica nel DB schema `stg` con upsert o truncate+insert a batch
2. **Transformation** (`tasks/transformation/`): Trasforma dati staging in formato intermedio (schema `trn`), gestisce sostituzioni articoli
3. **Inference** (`tasks/inference/`): Esegue inferenza con modello neurale (AHead client), include:
   - Download modello da S3 (zip)
   - Scaling dati con `ZeroQuantileScaler` (quantile-based con outlier detection IQR/Z-score/MAD)
   - Split articoli: modello ML vs baseline (media ultimi N step)
   - Inferenza neurale via AHead framework proprietario
   - Unscaling risultati
   - Gestione sostituzioni articoli (coefficienti)
   - Filtro articoli attivi
4. **Training** (`tasks/train/`): Preprocessing + training modello neurale con AHead framework, usa CatBoost per gradient boosting
5. **Presentation** (`tasks/presentation/`): Costruisce tabelle presentation layer, merge risultati

### AHead Framework (ML proprietario)
- Framework interno LAIF per time series forecasting
- Supporta modelli **neural network** (PyTorch) e **ML classico** (scikit-learn, CatBoost)
- Pipeline: preprocessing -> training -> inference
- Configurazione via YAML
- Feature: baseline prediction, anomaly detection, variable importance (Captum)

### Materialized Views
- 6 materialized view per aggregazioni pre-calcolate
- Refresh automatico al completamento di ogni run ETL
- Vista `adhoc_demand_review` combina forecast + ordini + ordini anno precedente + revisioni manuali

### Revisioni domanda
- **Ad hoc review**: revisione per singolo articolo/mese
- **General review**: revisione percentuale per dimensione (fornitore, linea, classe materiale, tipo web art)
- Le revisioni vengono applicate come moltiplicatori sul forecast nel calcolo del valore "reviewed"

### Export
- Report mensile XLSX con pivot per mese (nomi mesi in italiano)
- Export su S3
- Ordinamento mesi a partire dal mese corrente

## Integrazioni esterne

| Servizio | Uso |
|---|---|
| **AWS ECS** | Esecuzione task ETL su cluster dedicato (`sabart-etl-cluster`) |
| **AWS S3** | Storage dati input (CSV), modelli ML (zip), export report |
| **AWS Parameter Store** | Configurazione (implicito da template) |

## Frontend — Pagine custom

| Route | Descrizione |
|---|---|
| `/demand-forecast` | Dashboard previsioni domanda con grafici amCharts (chart + tabella, filtri per dimensione/gruppo/fornitore/linea/articolo) |
| `/adhoc-review` | Tabella revisioni ad hoc (forecast vs ordini vs anno precedente vs revisione) |
| `/general-review` | Tabella revisioni generali per dimensione con percentuali |
| `/new-articles` | Gestione nuovi articoli + tabella legami |
| `/promo` | Gestione promozioni (CRUD + upload CSV) |
| `/changelog-customer` | Changelog per il cliente |
| `/changelog-technical` | Changelog tecnico |

Componenti frontend custom:
- `demand-forecast-chart`: grafico amCharts per forecast
- `demand-forecast-table`: tabella dati forecast
- `adhoc-review-table`: tabella revisioni
- `general-review-table`: tabella revisioni generali
- `new-articles-table` + `links-table`: gestione articoli e legami
- `promo-table`: gestione promozioni

## Pattern notevoli

1. **Materialized View pattern**: classe base `MaterializedView` con metodi `create`, `refresh`, `drop`, `recreate` — le view sono definite come modelli SQLAlchemy con statement SQL come proprietà di classe
2. **RouterBuilder pattern**: uso del builder pattern del template per costruire controller CRUD in modo dichiarativo
3. **ZeroQuantileScaler**: scaler custom per normalizzazione time series con gestione zeri, outlier detection multipla (IQR, Z-score, MAD), e compressione non-lineare (power transform)
4. **Aliased GeneralReview**: uso di `aliased()` per joinare la stessa tabella `GeneralReview` 4 volte (una per ogni dimensione) nella stessa query
5. **Partitioned table**: `demand_forecast` partizionata per `id_run` (LIST partition PostgreSQL)
6. **Hybrid properties**: `flg_processed` su Article come hybrid property che fa subquery su NewArticle
7. **ETL su ECS separato**: il backend invoca task ECS con `run_task`, passa parametri come environment variables, e il task richiama il backend al completamento

## Tech debt e note

1. **`eval()` nel staging**: `service.py` del staging usa `eval(f"{transformation_name}(df=df, kwargs={kwargs})")` per eseguire trasformazioni custom — rischio sicurezza
2. **Pydantic v1 nell'ETL**: il modulo ETL usa ancora Pydantic 1.10.16 mentre il backend usa v2 — disallineamento
3. **SQLAlchemy 2.0.0 nell'ETL**: versione minima, mentre il backend usa 2.0.45
4. **Dipendenza `python-binance`**: presente nel pyproject.toml dell'ETL ma sembra non utilizzata (probabilmente residuo)
5. **CHANGELOG non aggiornato**: fermo alla v0.1 del 2024-12-24, ma l'app è alla v5.7.0
6. **Duplicazione logica export**: `export_monthly_report_xlsx` e `export_monthly_report_s3` hanno query quasi identiche duplicate
7. **Schema `mdl`**: referenziato nell'ETL (tabella `model_ids`) ma non definito nei modelli backend — gestito solo via SQL diretto
8. **Schema `trn`**: referenziato nell'ETL (tabella `trn.f_ordini`) ma non modellato in SQLAlchemy
9. **Task ETL via GET**: gli endpoint `/etl/execute` e `/etl/{id_run}/kill` usano GET per operazioni con side-effect — dovrebbero essere POST/DELETE
10. **Gestione errori basica nell'ETL**: catch generico `Exception` in molti punti
