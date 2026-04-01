# Raccomandazioni — Azioni Concrete dal Censimento

> Data analisi: 2026-03-21

## 1. Repos da Archiviare o Monitorare

| Repo | Azione | Motivazione |
|---|---|---|
| **sky-agent** | Archiviare o monitorare | Template vanilla senza alcun codice custom (fork 2026-03-18) |
| **retropricing** | Piano di migrazione urgente | Stack completamente obsoleto: Strapi v3 (EOL), Node 12 (EOL), React 16, CRA deprecato. Credenziali hardcoded. |

## 2. Aggiornamento Template

### Priorita ALTA (versioni <= 5.4.x)

| Repo | Versione attuale | Rischio |
|---|---|---|
| **crif** | 5.2.6 | FastAPI 0.105, Starlette 0.27.0, vecchie API template |
| **cae-genai** | 5.3.5 | Logica GenAI dentro `template/` invece di `app/` |
| **formart-marche** | 5.3.13 | |
| **creama** | 5.4.1 | FastAPI 0.105 |
| **preventivatore** | 5.4.0 | FastAPI 0.105 |
| **umbra-recommend** | 5.4.0 | |
| **coci** | 5.4.3 | FastAPI 0.105 |
| **experior** | 5.4.3 | |

### Priorita MEDIA (versioni 5.6.0-5.6.2)
I 15+ repos a 5.6.0 andrebbero aggiornati gradualmente a 5.7.0.

## 3. Pattern da Standardizzare

### ETL
- **Problema**: 8+ repos implementano ETL con approcci diversi (2-step, 3-step, 4-step, 6-step).
- **Raccomandazione**: Estrarre un **ETL framework** nel template con:
  - Base class per step (STG, TRN, PRS)
  - Run tracking con tabella `lkp_runs`
  - Error logging standardizzato
  - Supporto ECS Fargate out-of-the-box
  - Health check per container ETL
- **Repos di riferimento**: prima-power (6-step, piu maturo), andriani-sequencing (ben strutturato)

### Scheduling / Background Tasks
- **Problema**: approcci misti (`repeat_every`, APScheduler, `threading.Thread`, task commentati).
- **Raccomandazione**: Standardizzare su **APScheduler** (gia usato in bandi-platform, searchbridge) con configurazione dichiarativa.

### Materialized Views
- **Problema**: almeno 4 repos hanno implementazioni custom.
- **Raccomandazione**: Portare la `MaterializedView` base class di albini-castelli nel template.

### Chat AI / RAG
- **Problema**: Il provider OpenAI e stato esteso in modo diverso in ~10 repos. Alcuni usano il `CustomOpenAIProvider`, altri l'Agents SDK, altri Bedrock.
- **Raccomandazione**: Unificare il `gen_ai_provider` nel template con:
  - Supporto streaming SSE standard
  - Citation matching multi-strategia (gia implementato in 5+ repos)
  - System instructions da DB
  - Tag detection configurabile

### Forecasting / ML
- **Problema**: 4 repos con implementazioni indipendenti (nespak con 10 modelli statistici, sabart-demfor con PyTorch/CatBoost, umbra-recommend con CatBoost, coci con Polars).
- **Raccomandazione**: Valutare estrazione di un **forecasting toolkit** condiviso, partendo dal framework AHead di sabart-demfor.

## 4. Tech Debt Comune

### models.py troppo grande
**10+ repos** hanno `models.py` superiore a 1000 righe (max: studio-perri 2492, far-automation 2481, helia ~2400, preventivatore 2180). La convenzione interna e max 500 righe.

**Raccomandazione**: Split in moduli per dominio (es. `models/crm.py`, `models/etl.py`).

### Doppio HTTP client (httpx + requests)
**Tutti i repos** hanno il TODO `"maybe only use one?"` nel pyproject.toml. Entrambi httpx e requests sono nelle dipendenze.

**Raccomandazione**: Standardizzare su **httpx** (supporta sync e async) e rimuovere requests.

### CHANGELOG non mantenuto
**35+ repos** hanno il CHANGELOG.md fermo alla prima release `0.1`. Solo retropricing ha un changelog parzialmente aggiornato.

**Raccomandazione**: Automatizzare la generazione changelog da tag/release GitHub Actions.

### Task di esempio non rimosso
**30+ repos** hanno `events.py` con `_send_example_task` commentato (boilerplate template).

**Raccomandazione**: Rimuovere dal template scaffold o renderlo utile.

### Draft.js deprecato
**25+ repos** usano Draft.js nel frontend (Meta l'ha deprecato). Helia e sireco hanno gia iniziato la migrazione a TipTap.

**Raccomandazione**: Pianificare migrazione a **TipTap** (gia usato in helia, creama).

## 5. Problemi di Sicurezza

| Problema | Repos | Severita |
|---|---|---|
| **Credenziali hardcoded** | retropricing (DB Gamma/Nicim in codice), scheduler-roloplast (IP DB), helia (chiavi crittografia) | ALTA |
| **SQL injection potenziale** | umbra-recommend (f-string in query SQL), sabart-demfor (`eval()` nello staging) | ALTA |
| **SecurityScope commentate** | sireco (partner, uploads, economic data senza auth) | MEDIA |
| **`rejectUnauthorized: false`** | retropricing (connessione DB) | MEDIA |
| **API senza autenticazione** | lamonea (tutti endpoint TeamSystem), supplynk (zero backend) | MEDIA |
| **IP hardcoded** | scheduler-roloplast (88.214.45.175), ref-man (192.168.213.5) | BASSA |
| **Print statements di debug** | advaisor, argo, arianna, scheduler-roloplast, sireco | BASSA |
| **`datetime.utcnow()` deprecato** | argo | BASSA |

## 6. Test Mancanti

| Repo | Stato test |
|---|---|
| advaisor | Nessun test custom |
| albini-castelli | Nessun test custom |
| andriani-sequencing | Non menzionati test specifici |
| arianna | Nessun test chat/citazioni |
| bandi-platform | Non menzionati |
| cae-genai | Nessun test GenAI |
| crif | Credit Coach incompleto |
| experior | Directory test vuota |
| formart-marche | Nessun test custom |
| retropricing | Zero test (backend + frontend + ETL) |
| sabart-demfor | Non menzionati |
| umbra-recommend | Cartella test ETL vuota |

**Repos con test**: ids-georadar (32 backend, 11 frontend), jubatus (5 test custom), wolico (pytest + playwright)

## 7. Dipendenze da Allineare

| Dipendenza | Problema | Raccomandazione |
|---|---|---|
| **`python-binance`** | Presente in scheduler-roloplast e sabart-demfor senza motivo | Rimuovere |
| **`mechanicalsoup`** | In fortlan-dibi, probabilmente sostituito da Selenium | Rimuovere |
| **`pgvector`** | In 20+ repos come dipendenza default ma usato attivamente solo in ~5 | Spostare in gruppo opzionale |
| **`openai` + `pgvector`** | Abilitati di default in tutti i repos anche quando non servono (es. albini-castelli, far-automation) | Rendere opt-in, non opt-out |
| **`aiohttp`** | Presente in 20+ repos, spesso non chiaro il motivo (usato da SDK terze parti?) | Valutare rimozione dove non necessario |
| **`@amcharts/amcharts5` + `recharts`** | Helia usa entrambe le librerie grafici | Scegliere una sola |
| **`@hello-pangea/dnd` + `react-dnd`** | scheduler-roloplast usa entrambe | Scegliere una sola |

## 8. Feature da Estrarre nel Template

| Feature | Repos di origine | Motivazione |
|---|---|---|
| **MaterializedView base class** | albini-castelli | Pattern riusabile per tutti i progetti con analytics |
| **ETL framework** (STG->PRS) | andriani-sequencing, prima-power | 8+ repos lo reimplementano |
| **Citation matching multi-strategia** | nessy, cae-genai, arianna | 5+ repos hanno lo stesso codice |
| **Tag detection con LLM** | nessy, advaisor | Pattern comune per RAG con filtri |
| **Export Excel standardizzato** | 12+ repos | Tutti reimplementano xlsxwriter + pandas |
| **Changelog controller** | tutti | Gia di fatto standard, formalizzare |
| **ApplicationPermissions auto-setup** | competitive-retail | Pattern utile per permessi app-specifici |
| **column_property utilities** | ref-man, formart-marche | Helpers per le colonne calcolate piu comuni |

## 9. Repos con Stack Obsoleto

| Repo | Problema | Urgenza |
|---|---|---|
| **retropricing** | Strapi v3 EOL, Node 12 EOL, React 16, CRA deprecato | **CRITICA** — migrazione completa necessaria |
| **cae-genai** | Codice GenAI dentro `template/` invece di `app/` | ALTA — viola la convenzione |
| **creama** | FastAPI 0.105, Next.js 15 (non 16) | MEDIA |
| **preventivatore** | FastAPI 0.105, laif-ds 0.2.58 (molto vecchia) | MEDIA |

## 10. Osservazioni Strategiche

### Il template e il punto di forza (e il collo di bottiglia)
- 39 su 40 repos usano laif-template (l'unica eccezione e retropricing)
- Il template fornisce user management, ticketing, chat AI, file management, RBAC — riducendo il tempo di setup iniziale
- **MA** la divergenza tra versioni template (da 5.2.6 a 5.7.0) crea frammentazione e rende difficile backportare fix

### AI e il differenziatore principale
- 17 repos integrano OpenAI direttamente
- I progetti piu innovativi (helia, searchbridge, nessy) usano modelli recenti (GPT-5, o4-mini-deep-research, voice AI)
- Il RAG e il pattern AI piu comune (15+ repos), ma ogni repo lo reimplementa

### ETL e la competenza piu diffusa
- 24 repos hanno pipeline ETL di qualche tipo
- La complessita va dal semplice CSV import (sabart-demfor) al pipeline a 6 step con 4 DB source (prima-power)
- L'architettura a container separato su ECS e il pattern dominante per compute-intensive

### I mockup-first sono un anti-pattern da gestire
- 4 repos (sebi-group, supplynk, lamonea, + parzialmente sireco) hanno frontend completi con zero backend
- Questo crea debito tecnico al momento del collegamento backend
- **Raccomandazione**: definire un processo standard per transizione mockup -> backend
