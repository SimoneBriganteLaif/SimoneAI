# ref-man - Analisi Completa

## 1. Overview

**Nome app**: ref-man (Referee Manager)
**Descrizione**: FIP Referee Manager Platform - piattaforma per la gestione degli arbitri e ufficiali di campo della **Federazione Italiana Pallacanestro (FIP)**. Gestisce designazioni arbitrali, pianificazione partite, controllo gestione economica (note spese, rimborsi), e include un algoritmo di ottimizzazione ("Elite") basato su OR-Tools per l'assegnazione automatica degli arbitri alle gare.
**Cliente**: FIP (Federazione Italiana Pallacanestro)
**Settore**: Sport / Federazioni sportive
**Infra repo**: `fip-infra`

## 2. Versioni

| Componente | Versione |
|---|---|
| App (`version.txt`) | **0.5.1** |
| laif-template (`version.laif-template.txt`) | **5.6.0** |
| `values.yaml` template version | 1.1.0 |
| laif-ds (frontend) | 0.2.67 |

## 3. Team (contributori principali)

| Contributore | Commit |
|---|---|
| Pinnuz | 291 |
| mlife | 272 |
| Roberto Zanolli | 155 |
| github-actions[bot] | 152 |
| Alessandro Grotti | 108 |
| Simone Brigante | 92 |
| Marco Pinelli | 85 |
| Carlo A. Venditti | 80 |
| neghilowio | 73 |
| cavenditti-laif | 51 |

Team molto ampio (~35 contributori totali), indica progetto maturo e attivo.

## 4. Stack e dipendenze

### Backend (Python 3.12)

**Dipendenze standard template**: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, Uvicorn, boto3, bcrypt/passlib, python-jose, httpx, requests

**Dipendenze NON standard (app-specific)**:
| Pacchetto | Uso |
|---|---|
| `protobuf>=7.0.0` | Deserializzazione dati da API FIP/FOL (gare, note spese, correzioni NSD) |
| `aiohttp~=3.13.0` | HTTP client asincrono |
| `openpyxl>=3.1.2` | Lettura/scrittura Excel |
| `pillow>=9.5.0` | Gestione immagini (foto tesserati) |
| `ortools>=9.6.2534` | Algoritmo di ottimizzazione combinatoria (designazione arbitri) - dependency group `ds` |
| `openai~=2.14.0` | LLM integration - dependency group `llm` |
| `pgvector~=0.4.2` | Vector embeddings per RAG/chat - dependency group `llm` |
| `PyMuPDF~=1.26.7` | Parsing PDF - dependency group `pdf` |
| `python-docx~=1.2.0` | Generazione DOCX - dependency group `docx` |
| `xlsxwriter~=3.2.2` | Generazione Excel - dependency group `xlsx` |
| `pandas~=2.3.3` | Analisi dati (usato nell'algoritmo elite) - dependency group `xlsx` |

**Default groups attivi**: pdf, docx, llm, xlsx, ds

### Frontend (Node >= 24)

**Dipendenze standard template**: Next.js 16.1.1, React 19.2.3, TailwindCSS 4, react-hook-form, react-intl, react-redux, @tanstack/react-query, axios, laif-ds

**Dipendenze NON standard**:
| Pacchetto | Uso |
|---|---|
| `@amcharts/amcharts5` + `amcharts5-geodata` | Grafici avanzati e mappe geografiche (dashboard economics/analytics) |
| `@draft-js-plugins/editor` + `@draft-js-plugins/mention` | Rich text editor con menzioni |
| `draft-js` + `draft-js-export-html` | Gestione contenuti rich text |
| `@hello-pangea/dnd` | Drag and drop |
| `@microsoft/fetch-event-source` | Server-Sent Events (chat/streaming) |
| `katex` + `rehype-katex` + `remark-math` | Rendering formule matematiche |
| `react-markdown` + `remark-gfm` | Rendering markdown |
| `react-syntax-highlighter` | Evidenziazione sintassi codice |
| `framer-motion` | Animazioni UI |

### Docker Compose

**Servizi standard**: `db` (PostgreSQL), `backend` (FastAPI)

**Servizi extra (non-template)**:
- `docker-compose.etl.yaml`: VPN container + ETL container. La VPN e' necessaria per raggiungere FOL (Fip On Line) su rete privata `192.168.213.5`. Il container ETL gira sulla rete della VPN (`network_mode: "service:vpn"`)
- `docker-compose.wolico.yaml`: Configurazione per test locali con rete condivisa Wolico (`wolico_shared_network`)
- Build arg `ENABLE_XLSX: 1` nel docker-compose base

## 5. Modello Dati Completo

### Schema `prs` (dati applicativi)

```mermaid
erDiagram
    regioni {
        string cod_regione PK
        string cod_istat_regione UK
        string des_regione
        string des_area
    }

    province {
        string cod_provincia PK
        string cod_istat_provincia UK
        string des_provincia
        string cod_regione FK
    }

    comuni {
        string cod_comune PK
        string des_comune
        string cod_regione FK
        string cod_provincia FK
        string cod_istat_regione FK
        string cod_istat_provincia FK
    }

    comitati {
        string cod_comitato PK
        string des_comitato
    }

    tesserati {
        int id PK
        string cf
        int id_user FK
        enum figura
        string cognome
        string nome
        date dat_nascita
        date dat_primo_tesseramento
        date dat_scadenza_certificato
        string cellulare
        string mail
        string des_cap
        string cod_comune FK
        int num_partite_acc
        int num_partite_rif
        int num_presenze
        int med_num_errori
        bool flg_immagine
        bool flg_alone
        int num_gare
        int id_categoria FK
    }

    tessere {
        string cod_tessera PK
        int id_tesserato FK
        string cod_qualifica FK
        string cod_inquadramento FK
        enum stato_rinnovo
        bool flg_valido
    }

    qualifiche {
        string cod_qualifica PK
        string des_qualifica
    }

    inquadramenti {
        string cod_inquadramento PK
        enum figura
        string des_categoria
        string des_specifica
        int num_livello
    }

    incarichi {
        string cod_incarico PK
        string des_incarico
    }

    incaricati {
        int id_tesserato PK_FK
        string cod_incarico PK_FK
        date dat_inizio
    }

    campionati {
        string cod_campionato PK
        string des_campionato
        int num_order
        bool flg_refman
    }

    campionati_comitati {
        string cod_comitato PK_FK
        string cod_campionato PK_FK
        int num_min_arb
        int num_max_arb
        int num_min_udc
        int num_max_udc
        int num_livello_arb
        int num_livello_udc
        string elite_group
    }

    squadre {
        string cod_squadra PK
        string cod_comitato FK
        string cod_campionato FK
        string cod_societa
        string des_squadra
    }

    campi {
        string cod_campo PK
        string cod_regione FK
        string cod_comune FK
        string des_campo
        string des_indirizzo
        string des_cap
    }

    stati {
        int cod_stato PK
        string des_stato
        int num_livello
        enum stato_designazione
    }

    gare {
        string cod_comitato PK_FK
        int num_gara PK
        string cod_campionato FK
        string cod_comitato_designatore_arb FK
        string cod_comitato_designatore_udc FK
        string cod_comitato_designatore_oss FK
        date dat_gara
        time ora_gara
        string des_fase
        string des_tipo_fase
        string des_girone
        int num_giornata
        string des_tipo_giornata
        string cod_campo FK
        string cod_squadra_a FK
        string cod_squadra_b FK
        string des_squadra_a_placeholder
        string des_squadra_b_placeholder
        int num_versione
        float amt_tassa_gara
        int cod_elite_round
        string des_elite_round
    }

    designazioni {
        string cod_comitato_designatore FK
        string cod_comitato PK
        string cod_campionato FK
        int num_gara PK
        string cod_tessera PK_FK
        string cod_ruolo PK_FK
        int cod_stato FK
        date dat_ultima_modifica
    }

    ruoli {
        string cod_ruolo PK
        string des_ruolo
    }

    derogati {
        string cod_comitato_designatore FK
        string cod_comitato PK
        string cod_campionato PK
        int id_tesserato PK_FK
        enum tipo_deroga
    }

    extraterritorialita {
        string cod_comitato_designatore FK
        string cod_comitato PK
        int num_gara PK
        enum figura PK
        string cod_regione PK_FK
        string cod_campionato
    }

    note_spese {
        string cod_comitato PK_FK
        int num_gara PK
        int id_tesserato PK_FK
        string cod_campionato FK
        float km_solitaria
        float km_colleghi
        float km_noleggio
        float importo_solitaria
        float importo_colleghi
        float importo_noleggio
        float pedaggio
        float altro
        float parcheggio
        float importo_pernottamenti
        float importo_pasti
        float gettone
        float gettone_extra
        float totale_da_nota_spese
        float totale_da_pianificazione
        date dat_convalida
        enum figura
        float amt_aereo
        float amt_treno
        float amt_noleggio
    }

    tasse_gara {
        string cod_comitato PK_FK
        string cod_campionato PK_FK
        string des_fase PK
        float importo_tassa
        float num_target_budget
    }

    ragioni_indisponibilita {
        int id PK
        string des_tipo_ragione
        bool flg_public
    }

    indisponibilita {
        int id PK
        int id_tipo_ragione FK
        date dat_inizio
        date dat_fine
        string time_from
        string time_to
        string des_motivo
        bool flg_di_gruppo
        bool flg_ricorrente
        string giorni_settimana
    }

    indisponibilita_tesserati {
        int id PK
        int id_indisponibilita FK
        int id_tesserato FK
        datetime dat_ultima_modifica
    }

    tesserati_giocatori {
        int id PK
        int id_tesserato FK
        string cod_squadra FK
    }

    tesserati_fuori_sede {
        int id PK
        int id_tesserato FK
        string cod_comune FK
        date dat_inizio
        date dat_fine
        string giorni_settimana
    }

    assegnazioni_possibili {
        string cod_comitato_designatore FK
        string cod_comitato PK
        int num_gara PK
        int id_tesserato PK_FK
        string cod_campionato
        enum figura
        int num_nominations_a
        int num_nominations_b
        date dat_last_game_a
        date dat_last_game_b
        jsonb other_games
        array admitted_roles
    }

    distanze {
        string cod_comune_a PK_FK
        string cod_comune_b PK_FK
        int num_km
        float amt_pedaggio
    }

    categorie {
        int id PK
        enum figura
        string cod_categoria
        string cod_sub_categoria
        int sub_cat_order
        string des_categoria
        string des_sub_categoria
    }

    tesserati_campionati {
        int id PK
        int id_tesserato FK
        string cod_campionato FK
    }

    rimborso_km {
        date dat_inizio_validita PK
        date dat_fine_validita
        float amt_tariffa_km
        float amt_quinto
        float amt_settimo
        float amt_decimo
    }

    tariffe_cia {
        string cod_comitato PK_FK
        string cod_campionato PK_FK
        enum figura PK
        float amt_gettone
        float amt_pasto
        float amt_pernotto
        float amt_extragettone_100km
        float amt_extragettone_singolo
        float amt_extragettone_singolo_100km
        float amt_extragettone_singolo_300km
        float num_fraz_benzina_singolo
        float num_fraz_benzina_colleghi
        float num_fraz_benzina_noleggio
    }

    gruppi_comitati {
        int id_gruppo PK_FK
        string cod_comitato PK_FK
    }

    gruppi_inquadramenti {
        int id_gruppo PK_FK
        string cod_inquadramento PK_FK
    }

    tesserati_comitati {
        int id_tesserato PK_FK
        string cod_comitato PK_FK
    }

    elite_algorithm_runs {
        int id PK
        string cod_comitato FK
        string cod_elite_group
        int cod_elite_round
        enum cod_status
        datetime tms_started_at
        datetime tms_finished_at
        string des_error_message
    }

    elite_algorithm_general_results {
        int id_run PK_FK
        float amt_costi_totale
        float num_easiness
        float num_gare_passate
        float num_squadre_passate
        float num_coppie_passate
    }

    elite_algorithm_gara_results {
        int id_run PK_FK
        string cod_comitato PK
        int num_gara PK
        float amt_compensi
        float amt_tasse_gara
        float amt_compensi_extra
        float amt_spese_trasferta
    }

    elite_algorithm_gara_ruolo_results {
        int id_run PK_FK
        string cod_comitato PK
        int num_gara PK
        string cod_ruolo PK_FK
        int id_tesserato FK
    }

    elite_algorithm_general_params {
        int id_run PK_FK
        bool flg_no_stessa_citta
        bool flg_no_stessa_citta_trasferta
    }

    elite_algorithm_tesserati_da_designare_generali_params {
        int id_run PK_FK
        int id_tesserato PK_FK
    }

    elite_algorithm_tesserati_da_designare_gare_params {
        int id_run PK_FK
        int num_gara PK
        int id_tesserato PK_FK
        string cod_comitato
    }

    elite_algorithm_tesserati_vietati_generali_params {
        int id_run PK_FK
        int id_tesserato PK_FK
    }

    elite_algorithm_tesserati_vietati_gare_params {
        int id_run PK_FK
        int num_gara PK
        int id_tesserato PK_FK
        string cod_comitato
    }

    elite_algorithm_tesserati_coppie_vietate_params {
        int id_run PK_FK
        int id_tesserato_1 PK_FK
        int id_tesserato_2 PK_FK
    }

    elite_algorithm_gara_ruoli_params {
        int id_run PK_FK
        int num_gara PK
        string cod_ruolo PK_FK
        string cod_comitato
        int id_tesserato FK
    }

    regioni ||--o{ province : "ha"
    regioni ||--o{ comuni : "contiene"
    province ||--o{ comuni : "contiene"
    comuni ||--o{ tesserati : "residenza"
    comuni ||--o{ campi : "localizzazione"
    tesserati ||--o{ tessere : "possiede"
    qualifiche ||--o{ tessere : "tipo"
    inquadramenti ||--o{ tessere : "livello"
    tesserati ||--o{ designazioni : "designato_via_tessera"
    gare ||--o{ designazioni : "per_gara"
    ruoli ||--o{ designazioni : "ruolo"
    stati ||--o{ designazioni : "stato"
    campionati ||--o{ campionati_comitati : "in_comitato"
    comitati ||--o{ campionati_comitati : "organizza"
    campionati_comitati ||--o{ gare : "programma"
    campionati_comitati ||--o{ squadre : "partecipa"
    gare ||--o{ note_spese : "genera"
    tesserati ||--o{ note_spese : "riceve"
    tesserati ||--o{ indisponibilita_tesserati : "dichiara"
    indisponibilita ||--o{ indisponibilita_tesserati : "dettaglio"
    tesserati ||--o{ tesserati_fuori_sede : "sedi_extra"
    tesserati ||--o{ tesserati_giocatori : "giocatore_associato"
    tesserati ||--o{ assegnazioni_possibili : "candidato"
    gare ||--o{ assegnazioni_possibili : "per_gara"
    elite_algorithm_runs ||--o{ elite_algorithm_general_results : "risultati"
    elite_algorithm_runs ||--o{ elite_algorithm_gara_results : "risultati_gara"
    elite_algorithm_runs ||--o{ elite_algorithm_gara_ruolo_results : "assegnazioni"
```

### Schema `stg` (staging ETL)

- **`stg.note_spese`** (`TempNoteSpese`): tabella di staging per upsert note spese dal proto NSD. ~30+ colonne di dettaglio voci di spesa
- **`stg.dati_agenzia`** (`TempDatiAgenzia`): dati prenotazioni agenzia viaggi (passeggero, servizio, vettore, importi)

### Enum applicativi

- `Figura`: ARB, UDC, OSS_ARB, OSS_UDC (tipi di ufficiale di gara)
- `StatoRinnovo`: rinnovato, da_rinnovare, in_corso
- `StatoDesignazione`: accettata, rifiutata, temporanea, trasmessa, revoca
- `TipoDeroga`: extraterritorialita, abilitazione
- `StatoNotaSpesa`: liquidata, in_liquidazione, in_attesa
- `StatoAlgoritmo`: ACCEPTED, RUNNING, ERROR, END

**Totale tabelle**: ~35 tabelle nello schema `prs` + 2 tabelle staging in `stg`

## 6. API Routes

### Risorse con RouterBuilder (CRUD standard template)

| Prefisso | Operazioni | Note |
|---|---|---|
| `/tesserati` | search, export, get_by_id, upload, update | Upload foto, update dati, stats endpoint custom |
| `/gare` | search, export | + endpoint custom `/elite-rounds` |
| `/designazioni` | search | |
| `/campionati` | search | + endpoint custom `/elite-groups/{cod_comitato}` |
| `/categorie` | search | |
| `/comitati` | search | |
| `/comuni` | search | |
| `/province` | search | |
| `/regioni` | search | |
| `/inquadramenti` | search | |
| `/squadre` | search, get_by_id | |
| `/indisponibilita` | search, delete, create | |
| `/indisponibilita_tesserati` | search, delete, create | |
| `/tipo-indisponibilita` | search | |
| `/tesserati_fuori_sede` | search, update, delete, create | |
| `/tesserati_giocatori` | search, delete, create | |
| `/tesserati_campionati` | search, get_by_id, upload, batch_create, batch_delete, delete, create | |
| `/tasse_gara` | search, custom PUT update | |
| `/controllo-gestione` | search | + endpoint custom `/statistics-economics` |
| `/assegnazioni_possibili` | search | + endpoint custom `/generali` |

### Controller custom (non RouterBuilder)

| Prefisso | Endpoint | Metodo |
|---|---|---|
| `/etl` | `/execute` | GET - Lancia ETL in background (Thread) |
| `/algorithms` | `/run-elite-algorithm` | POST - Esegue algoritmo elite in BackgroundTasks |
| `/algorithms` | `/elite/constraints` | POST - Salva vincoli algoritmo elite |
| `/algorithms` | `/elite/info` | POST - Info run + risultati |
| `/algorithms` | `/elite/status` | GET - Stato esecuzione |
| `/analytics` | `/home/tesserati` | POST - Dashboard tesserati |
| `/analytics` | `/home/designazioni` | POST - Dashboard designazioni |
| `/analytics` | `/home/gare` | POST - Dashboard gare |
| `/calendario` | `` | POST - Calendario con filtri e paginazione |
| `/changelog` | `/` | GET - Changelog tech/customer |

## 7. Business Logic

### Algoritmo Elite (OR-Tools CP-SAT Solver)

Componente piu' complesso dell'app. Usa Google OR-Tools (constraint programming) per ottimizzare le designazioni arbitrali:

- **InputManager** (`algorithms/elite/input_manager.py`): prepara i dati dal DB (giocatori, gare, distanze, tariffe, indisponibilita')
- **Designator** (`algorithms/elite/designator.py`): modello CP con:
  - Variabili booleane `X[member, role, game]` per ogni assegnazione possibile
  - Vincoli: non sovrapposizione, livelli inquadramento, extraterritorialita', coppie vietate, stessa citta'
  - Funzione obiettivo: minimizzazione costi (trasferta, compensi) con bilanciamento equita'
- **Esecuzione asincrona**: lanciato via `BackgroundTasks` di FastAPI, stato tracciato in DB (`EliteAlgorithmRuns`)
- **Fallback**: se il modello risulta INFEASIBLE, ritenta con vincoli rilassati
- **Post-processing**: salva risultati in DB e crea designazioni automatiche

### ETL (Extract-Transform-Load)

Pipeline ETL complessa per sincronizzare dati da FOL (Fip On Line):

- **Connessione VPN**: container Docker OpenVPN dedicato per raggiungere FOL su rete privata (`192.168.213.5`)
- **API FOL**: REST + Protobuf. Usa header custom `x-des-fip-it` per autenticazione
- **API FIP**: endpoint separato per controllo gestione (`x-api-key`)
- **Protobuf**: definizioni `.proto` per gare, note spese (NSD), correzioni NSD
- **Entita' sincronizzate**: tesserati, campionati, campionati_comitati, squadre, campi, derogati, gare, designazioni, extraterritorialita', rimborso_km, note_spese
- **Post-processing SQL**: query per populate_rounds, assegnazioni_possibili, tesserati_comitati
- **Doppia modalita'**: ETL standalone (`main.py` via docker-compose) oppure on-demand via API (`/etl/execute`)

### Controllo Gestione (Economics)

- Statistiche economiche aggregate per comitato con filtri temporali/geografici
- Dettaglio gare con note spese associate
- Budget target per campionato/fase (tasse gara)

### Sistema Permessi

Permessi basati su comitati e inquadramenti tramite tabelle ponte `gruppi_comitati` e `gruppi_inquadramenti`. Ogni utente vede solo i dati dei comitati/inquadramenti associati ai suoi gruppi.

### Task Periodici

- `repeat_every` configurato (esempio placeholder da template, non attivo in produzione)
- L'ETL puo' essere schedulato come job separato

## 8. Integrazioni Esterne

| Sistema | Protocollo | Dettaglio |
|---|---|---|
| **FOL (Fip On Line)** | REST JSON via VPN | API designazioni: tesserati, campionati, squadre, gare, designazioni, derogati, campi. URL: `192.168.213.5/fol/apiDesignazioni` |
| **FIP Controllo Gestione** | REST + Protobuf via VPN | Gare (protobuf), note spese (protobuf NSD), correzioni NSD. URL: `192.168.213.5/fip/services/cia/controllo_gestione` |
| **AWS S3** | boto3 | Storage note spese protobuf, immagini tesserati |
| **OpenAI** | openai SDK | Integrazione LLM (area formazione/chat) |
| **pgvector** | PostgreSQL extension | Vector store per RAG nella knowledge base formazione |
| **Wolico** | rete Docker condivisa | Integrazione testing locale con piattaforma Wolico |

## 9. Albero Pagine Frontend

```
/(authenticated)
├── /home/                                    -- Dashboard con analytics tesserati/designazioni/gare
├── /economics/
│   ├── /riepilogo/                          -- Riepilogo controllo gestione
│   └── /dettaglio-gare/                     -- Dettaglio gare con note spese
├── /tesserati/
│   ├── / (lista)                            -- Elenco tesserati con filtro per figura
│   └── /detail/                             -- Dettaglio tesserato (info, foto, tessere)
├── /gare/                                    -- Elenco gare
├── /designazioni/
│   ├── /algoritmi/                          -- Configurazione ed esecuzione algoritmo Elite
│   ├── /schede-attivita/                    -- Schede attivita' designazioni
│   └── /parametri-tesserati/                -- Parametri tesserati per campionato
├── /pianificazione/
│   ├── /calendario/                         -- Calendario gare con filtri
│   ├── /indisponibilita/
│   │   ├── /singole/                        -- Indisponibilita' singole
│   │   └── /gruppo/                         -- Indisponibilita' di gruppo
│   ├── /giocatori/                          -- Associazione giocatori-squadre
│   └── /fuori-sede/                         -- Gestione sedi temporanee
├── /valutazioni/                             -- Valutazioni arbitrali
├── /riunioni/                                -- Attivita' tecnica / riunioni
├── /comunicazioni/                           -- Sistema comunicazioni
├── /formazione/
│   ├── /chat/                               -- Chat AI (OpenAI + RAG)
│   ├── /knowledge/                          -- Knowledge base documentale
│   └── /quiz/                               -- Quiz formativi
├── /prenotazioni-agenzia/
│   ├── /inserimento/                        -- Inserimento prenotazioni viaggio
│   └── /rendicontazione/                    -- Rendicontazione spese viaggio
├── /impostazioni/
│   └── /budget/                             -- Impostazioni budget per comitato
├── /sal/
│   ├── /controllo-gestione/                 -- SAL controllo gestione
│   └── /test-algoritmo/                     -- SAL test algoritmo
├── (template)
│   ├── /conversation/ (analytics, chat, feedback, knowledge)
│   ├── /files/
│   ├── /help/ (faq, ticket)
│   ├── /profile/
│   └── /user-management/ (user, group, role, permission, business)
├── /changelog-customer/
└── /changelog-technical/
```

**Permessi principali**: economics:read, planning:read, calendar:read, outages:read, players:read, locations:read, scoring:read, meetings:read, communications:read, training:read, quiz:read, chat:read, knowledge:read, travel-agency:read, settings:read

## 10. Deviazioni dal laif-template

### Cartelle/file NON standard

| Path | Descrizione |
|---|---|
| `backend/src/app/algorithms/` | Intero modulo algoritmo di ottimizzazione OR-Tools (designator, input_manager, solver_utils, schema) |
| `backend/src/app/algorithms/elite/` | Implementazione specifica algoritmo Elite |
| `backend/src/app/algorithms/old_schema/` | Schema vecchio algoritmo (legacy) |
| `backend/src/app/etl/` | Pipeline ETL completa con VPN container |
| `backend/src/app/etl/vpn/` | Container Docker OpenVPN con healthcheck |
| `backend/src/app/etl/proto/` | Definizioni Protobuf + generated bindings |
| `backend/src/app/etl/entities/` | 15+ moduli per trasformazione entita' da FOL |
| `backend/src/app/etl/queries/` | Query SQL raw per post-processing ETL |
| `backend/src/app/etl/data/` | Dati statici (regioni) |
| `backend/src/app/schema/generated/` | Schema Pydantic generati |
| `backend/src/app/utils/permission_service.py` | Sistema permessi custom basato su comitati/inquadramenti |
| `docker-compose.etl.yaml` | Docker compose per ETL con VPN |
| `docker-compose.wolico.yaml` | Docker compose per integrazione Wolico |
| `docs/troisi/` | Documentazione specifica (custom email style) |

### Moduli dominio (tutti custom, ~20 moduli)

Ogni modulo in `backend/src/app/` con controller.py + service.py: `regioni`, `province`, `comuni`, `comitati`, `tesserati`, `tessere`, `inquadramenti`, `campionati`, `squadre`, `gare`, `designazioni`, `indisponibilita`, `indisponibilita_tesserati`, `tipo_indisponibilita`, `tesserati_fuori_sede`, `tesserati_giocatori`, `tesserati_campionati`, `assegnazioni_possibili`, `tasse_gara`, `controllo_gestione`, `analytics`, `calendario`, `esecuzione_algoritmi`, `categorie`, `changelog`

## 11. Pattern Notabili

### Algoritmo di ottimizzazione con CP-SAT
Pattern unico nel portfolio LAIF: uso di Google OR-Tools per risolvere un problema di assegnamento combinatorio. Il modello include variabili booleane per ogni tripla (membro, ruolo, gara), vincoli complessi e funzione obiettivo multi-criterio. Include fallback automatico con rilassamento vincoli.

### ETL con VPN containerizzata
Architettura elegante: container VPN dedicato che crea un tunnel verso la rete privata FIP, e il container ETL usa `network_mode: "service:vpn"` per condividere la rete. Healthcheck sulla VPN prima di procedere.

### Protobuf per dati strutturati
Unico progetto LAIF che usa Protocol Buffers per deserializzare dati da API esterne. Definizioni `.proto` per gare, note spese, correzioni.

### Tabelle ponte permessi
Sistema permessi granulare basato su `gruppi_comitati` e `gruppi_inquadramenti` per filtrare i dati per utente in base al comitato di appartenenza.

### column_property estensivo
Uso molto intenso di `column_property` di SQLAlchemy per derivare campi da subquery correlate (es. nome completo del tesserato, regione della gara tramite il campo, codici comitato aggregati).

### Nomenclatura italiana coerente con FOL
Scelta deliberata di mantenere la nomenclatura italiana sia nel codice che nel DB per coerenza con il sistema sorgente FOL.

## 12. Note e Tech Debt

### TODO/FIXME significativi

- **Designazioni**: filtro permessi incompleto - il presidente delle Marche dovrebbe vedere tutte le designazioni dei propri arbitri anche fuori regione
- **Gare controller**: schema risposta include note spese dove non dovrebbe (FIXME)
- **Export gare**: manca l'export delle designazioni associate
- **Assegnazioni possibili**: supporta solo ARB, manca UDC
- **Algoritmo Elite**: tariffe km hardcodate a 0.24 invece di usare tabella `rimborso_km`, gestione pasti/pernotti mancante, ranking squadre non implementato, gare regionali non gestite
- **ETL**: gestione cambio stagione da implementare, correzioni NSD non importate, logica conguagli da chiarire

### Codice legacy
- `algorithms/old_schema/` contiene schema precedente dell'algoritmo (non piu' in uso ma non rimosso)
- Molto codice commentato in `service_elite.py` (vecchia logica email, vecchi task handler)

### Dipendenze duplicate
- Sia `httpx` che `requests` come HTTP client (TODO nel pyproject.toml: "maybe only use one?")

### Eventi placeholder
- `events.py` contiene un task periodico di esempio non attivato (`_send_example_task`)

### Modello dati monolitico
- Tutte le ~35 tabelle in un singolo file `models.py` di 1127 righe (supera il limite di 500 righe indicato nelle convenzioni)
