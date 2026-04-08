---
nome: "Analisi Repository"
descrizione: >
  Analizza i repository LAIF e produce report strutturati con metriche di complessita,
  confrontando con il baseline del template v5.7.0. Output: JSON + SQLite + Excel + Markdown.
  Suite modulare di script Python: un check per area, componibili.
fase: development
versione: "1.0"
stato: beta
legge:
  - repos.yaml (configurazione repo)
  - scripts/baseline.json (manifesto template)
  - Repository target (clonati localmente)
scrive:
  - output/*.json (dati per repo)
  - output/cross_analysis.json (metriche aggregate)
  - output/analysis.db (SQLite)
  - output/analysis.xlsx (Excel multi-foglio)
aggiornato: "2026-04-07"
---

# Skill: Analisi Repository

## Obiettivo

Analizzare automaticamente i repository LAIF e produrre report con metriche custom (filtrate dal template baseline), dati tabulari in SQLite/Excel, e un report aggregato cross-progetto.

## Perimetro

**Fa:**
- Clona/aggiorna repo da config (`repos.yaml`)
- Per ogni repo: conta pagine, modali, tabelle DB, endpoint API, componenti DS, dipendenze extra, background task, contributor
- Tutte le metriche sono "custom = totale - template baseline"
- Genera data model Mermaid ER per le tabelle custom
- Produce output JSON, SQLite, Excel, Markdown
- Analisi cross-progetto: matrice impatto DS, librerie diffuse, drift ranking

**Non fa:**
- Non analizza qualita del codice (lint, complessita ciclomatica)
- Non si collega ai database (solo analisi statica)
- Non modifica i repository analizzati

## Quando usarla

- Esecuzione settimanale per monitoraggio stato repository
- Prima di iniziare lavoro su un progetto (capire dimensione e complessita)
- Per censimenti e confronti cross-progetto

## Prerequisiti

- Python 3.12+
- `openpyxl` e `pyyaml` (`pip install -r scripts/requirements.txt`)
- Accesso SSH ai repository GitHub LAIF
- `repos.yaml` configurato con la lista repo

## Struttura file

```
skills/analisi-repo/
├── SKILL.md                        # Questo file
├── repos.yaml                      # Lista repo da analizzare
├── scripts/
│   ├── sync_repos.py               # Clone/pull da repos.yaml
│   ├── analyze.py                  # Orchestratore singolo repo
│   ├── checks/                     # Un modulo per area (A-H)
│   │   ├── versioning.py           # A: versione template, drift
│   │   ├── datamodel.py            # B: tabelle, MV, diagramma ER
│   │   ├── frontend_pages.py       # C: pagine, modali
│   │   ├── frontend_components.py  # D: componenti DS, custom
│   │   ├── api_routes.py           # E: endpoint, RouterBuilder
│   │   ├── dependencies.py         # F: dipendenze extra
│   │   ├── background_tasks.py     # G: ETL, task, ECS
│   │   └── git_stats.py            # H: contributor
│   ├── cross_analysis.py           # I: analisi cross-progetto
│   ├── export.py                   # JSON → SQLite + Excel
│   ├── baseline.json               # Manifesto template v5.7.0
│   └── requirements.txt
├── templates/
│   └── report.md
└── output/                         # Report generati (gitignored)
```

## Uso

### Analisi singolo repo
```bash
python3 scripts/analyze.py --path /path/to/repo
python3 scripts/analyze.py --path /path/to/repo --output output/ --quiet
```

### Sync + analisi batch
```bash
python3 scripts/sync_repos.py --config repos.yaml
python3 scripts/analyze.py --path /tmp/laif-repos/albini-castelli --output output/
# Ripetere per ogni repo, oppure scriptare un loop
python3 scripts/cross_analysis.py --input output/
python3 scripts/export.py --input output/
```

### Dry run sync
```bash
python3 scripts/sync_repos.py --config repos.yaml --dry-run
```

## Metriche (28 totali, 8 sezioni per repo + 1 cross-progetto)

### A. Versioning e template drift
- Versione template dell'app (parse `version.laif-template.txt`)
- Delta versione rispetto al baseline
- File nelle cartelle `*/template/` (per rilevare modifiche)
- File template rimossi dal progetto

### B. Data model
- Tabelle custom (parse `__tablename__` in tutti i .py, filtrate vs baseline 32 tabelle)
- Materialized views (classi con pattern `MaterializedView`)
- Bozza data model: diagramma Mermaid ER con entita custom e relazioni FK

### C. Frontend — pagine e navigazione
- Pagine custom (page.tsx filtrate vs baseline 27 route)
- Alberatura sito delle sole route custom
- Modali custom (file Modal/Dialog o in cartella `modals/`, esclusi `template/`)

### D. Frontend — componenti
- Componenti laif-ds usati: lista con conteggio utilizzi per componente
- Componenti laif-ds non usati (richiede lista completa DS)
- Componenti custom: file .tsx in `src/features/` e `src/components/`

### E. Backend — API
- Endpoint custom (solo in `app/`, non in `template/`), breakdown per metodo HTTP
- Endpoint per controller
- RouterBuilder vs decoratori manuali

### F. Dipendenze
- Librerie extra backend (diff `pyproject.toml` vs baseline)
- Librerie extra frontend (diff `package.json` vs baseline)

### G. ETL e background task
- Background task (repeat_every, BackgroundTask, asyncio.create_task)
- ETL pipeline: directory esplicite (etl/, import_storico/) + driver DB esterni
- Job ECS/Fargate: Dockerfile extra, entry point CLI alternativi

### H. Git
- Contributor con conteggio commit (esclusi commit template via `upstream/master` o `upstream/main`)
- Ultimo commit: data, autore, messaggio

### I. Cross-progetto (in cross_analysis.py)
- Matrice impatto DS: componente × progetto
- Componenti custom ricorrenti in 2+ progetti (candidati DS)
- Librerie non-template piu diffuse (candidati per template)
- Mappa integrazioni esterne ricorrenti
- Drift ranking: classifica progetti per urgenza aggiornamento

## Output

| File | Formato | Contenuto |
|------|---------|-----------|
| `output/{repo}.json` | JSON | Tutte le metriche per singolo repo |
| `output/cross_analysis.json` | JSON | Metriche aggregate cross-progetto |
| `output/analysis.db` | SQLite | Tabelle queryabili (repos, custom_tables, ds_components_usage, ...) |
| `output/analysis.xlsx` | Excel | Fogli: Repos, DS Components, Extra Deps, Custom Tables |

## Tabelle SQLite

| Tabella | Contenuto |
|---------|-----------|
| `repos` | Nome, versione, delta, pagine, modali, tabelle, endpoint, componenti |
| `custom_tables` | Repo, tabella, classe, file |
| `custom_endpoints` | Repo, metodo, path, tipo (RouterBuilder/manual), file |
| `custom_pages` | Repo, route, profondita |
| `ds_components_usage` | Repo, componente, conteggio utilizzi |
| `custom_components` | Repo, file |
| `extra_deps_backend` | Repo, pacchetto, versione |
| `extra_deps_frontend` | Repo, pacchetto, versione |
| `contributors` | Repo, nome, numero commit |
| `background_tasks` | Repo, tipo, file |

## Note implementative

- Il baseline (`baseline.json`) contiene 32 tabelle, 27 route frontend, 24 modali template, e tutte le dipendenze del template v5.7.0
- I modali sono rilevati per nome file (`*Modal.tsx`, `*Dialog.tsx`) o per directory (`modals/`), escludendo sotto-componenti in directory con "modal" nel nome
- Per il git, lo script prova `upstream/main`, `upstream/master`, `upstream/develop` in ordine come ref di esclusione
- L'ETL viene rilevato solo per indicatori forti (directory `etl/`, `import_storico/`, driver DB esterni), non per parole generiche come "load" o "transform"
- I componenti DS vengono estratti da import `from "laif-ds"` e `from 'laif-ds'` (entrambi i formati)

## Checklist qualita

- [ ] baseline.json aggiornato quando il template viene rilasciato
- [ ] repos.yaml aggiornato con nuovi progetti
- [ ] I conteggi custom matchano l'analisi manuale per almeno 2 repo di riferimento
- [ ] L'output SQLite e queryabile senza errori
- [ ] L'Excel e apribile e filtrabile
