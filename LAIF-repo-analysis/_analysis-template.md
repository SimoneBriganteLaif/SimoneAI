# {Nome Repo} — Analisi Repository

> Censimento LAIF — Data analisi: 2026-03-21

## Overview

- **Cosa fa**: [descrizione 1-3 frasi]
- **Cliente**: [nome cliente]
- **Settore**: [industria/dominio]
- **Stato**: attivo / manutenzione / archiviato
- **Branch analizzato**: master / develop
- **Ultima attivita**: [data ultimo commit]

## Versioni

| Componente | Versione |
|---|---|
| App | [da values.yaml o package.json] |
| laif-template | [versione base del fork] |
| Python | |
| FastAPI | |
| Next.js | |
| PostgreSQL | |

## Team

| Contributor | Commit |
|---|---|
| ... | ... |

## Stack e Deviazioni dal Template

### Dipendenze Backend Non-Standard

| Package | Scopo |
|---|---|
| ... | ... |

### Dipendenze Frontend Non-Standard

| Package | Scopo |
|---|---|
| ... | ... |

### Servizi Docker Extra

| Servizio | Immagine | Scopo |
|---|---|---|
| ... | ... | ... |

## Modello Dati Completo

### Tabelle

| Tabella | Schema | Colonne Principali | Relazioni |
|---|---|---|---|
| ... | prs | ... | FK -> ... |

### Diagramma ER

```mermaid
erDiagram
    ...
```

## API Routes

| Prefisso | Risorsa | Metodi | Note |
|---|---|---|---|
| /api/v1/... | ... | CRUD | ... |

### Route Non-Standard

[Route custom fuori dal pattern RouterBuilder]

## Logica di Business

### Background Tasks
[Celery, asyncio, BackgroundTasks, APScheduler]

### ETL / Data Processing
[Import/export, trasformazioni, pipeline]

### AI / ML
[Modelli, inference, embeddings, LLM]

### Scheduler / Automazioni
[Job schedulati, workflow automatici]

## Integrazioni Esterne

| Servizio | Tipo | Scopo | Pattern Usato |
|---|---|---|---|
| ... | ... | ... | ... |

## Albero Pagine Frontend

```
frontend/src/app/
├── (auth)/
│   └── ...
├── (protected)/
│   └── ...
└── ...
```

### Componenti Complessi
[Widget, editor, kanban, chart non-standard]

### Deviazioni UI
[Componenti custom non da @laif/ds]

## Deviazioni da laif-template

### File/Cartelle Aggiunti
- ...

### Modifiche Strutturali
- ...

### File Template Rimossi/Modificati
- ...

## Pattern Notevoli
[Soluzioni innovative, approcci diversi, workaround]

## Note
[Tech debt, TODO, peculiarita, osservazioni]
