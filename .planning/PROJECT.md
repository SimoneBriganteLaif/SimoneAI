# ER Editor

## What This Is

Un editor visuale di diagrammi ER che legge e scrive file `model.py` SQLAlchemy 2.0. Permette di visualizzare, organizzare in gruppi e modificare i modelli di dati delle app LAIF direttamente da un'interfaccia drag&drop nel browser, con round-trip completo verso il codice sorgente.

## Core Value

L'editing visuale del datamodel deve tradursi fedelmente in modifiche al `model.py`, preservando commenti, formattazione e struttura del file originale.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Importare un file `model.py` SQLAlchemy 2.0 e parsarlo in una struttura dati intermedia
- [ ] Visualizzare un diagramma ER interattivo con tabelle, colonne e relazioni
- [ ] Editing completo: aggiungere/rimuovere/rinominare tabelle e colonne
- [ ] Editing proprietà colonna: tipo, nullable, unique, index, primary key, foreign key, default
- [ ] Creare e modificare relazioni tra tabelle (relationship, back_populates, cascade, lazy)
- [ ] Raggruppare visualmente le tabelle in gruppi nominati con colori
- [ ] Drag&drop di tabelle e gruppi, pan/zoom del canvas
- [ ] Salvare le modifiche riscrivendo il `model.py` preservando commenti e formattazione
- [ ] Persistere posizioni e gruppi in un file sidecar `.er.json`
- [ ] App portabile: copiare la cartella, `pip install`, `python server.py model.py`

### Out of Scope

- Gestione schema Pydantic — evolutiva futura, non in v1
- Generazione migrazioni Alembic — il tool modifica solo `model.py`
- Supporto pattern legacy SQLAlchemy (`Column()`) — solo `Mapped[]` / `mapped_column()`
- Multi-file — v1 gestisce un singolo `model.py` alla volta
- Deploy/hosting — è un tool locale

## Context

- Tutte le app LAIF hanno il datamodel in `model.py` usando SQLAlchemy 2.0 con pattern `Mapped[]`
- I file vanno da 2 modelli semplici a 13+ modelli con 20+ relazioni (es. analyzer)
- Il tool sarà posizionato in `tools/er-editor/` nella KB SimoneAI
- Stack LAIF standard: FastAPI, PostgreSQL, SQLAlchemy 2.0

## Constraints

- **Portabilità**: deve funzionare copiando una cartella, senza build step frontend (no npm/webpack)
- **Dipendenze Python**: solo `fastapi`, `uvicorn`, `libcst` — minimali e standard
- **Frontend**: JointJS open-source da CDN, vanilla JS, nessun framework con build
- **Round-trip**: libcst per preservare byte-per-byte commenti, whitespace e formattazione
- **Licenza**: solo librerie open-source (JointJS MPL 2.0)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| JointJS open-source per diagrammi | CDN-ready, shape ER native, ports, embedding per gruppi, SVG. Alternative valutate: React Flow (no build = pain), Cytoscape (wrong abstraction), GoJS (commercial) | — Pending |
| libcst per parsing/writing | Round-trip byte-per-byte, preserva commenti. Alternative: ast (perde formattazione), redbaron (unmaintained), regex (fragile) | — Pending |
| File sidecar `.er.json` per metadati | Non inquina model.py con dati visuali, formato JSON estensibile, versionabile a scelta | — Pending |
| Solo pattern moderno `Mapped[]` | Semplifica il parser, i nuovi progetti LAIF usano tutti questo pattern | — Pending |

---
*Last updated: 2026-03-16 after initialization*
