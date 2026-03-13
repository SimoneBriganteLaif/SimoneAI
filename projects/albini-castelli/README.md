---
progetto: "albini-castelli"
cliente: "Albini & Castelli"
industria: "Edilizia / Costruzioni"
stato: "manutenzione"
data-inizio: ""
data-fine: ""
stack:
  - FastAPI 0.128
  - Python 3.12
  - SQLAlchemy 2.0
  - PostgreSQL
  - Next.js 16
  - React 19
  - TypeScript
  - TailwindCSS 4
  - laif-ds 0.2.67
  - AWS (ECS + RDS + S3)
tags:
  - "#progetto:albini-castelli"
  - "#industria:edilizia"
  - "#fase:manutenzione"
---

# Albini & Castelli — Schede Cantiere

## Contesto

Albini & Castelli è un'impresa edile. Il progetto consiste in un'applicazione web per la gestione operativa ed economica dei cantieri: ogni cantiere ha una "scheda" con revisioni di budget, consuntivi, KPI e dati per anno.

## Obiettivo del progetto

Sistema di tracciamento delle schede cantiere: permette ai responsabili di gestire il ciclo di revisione budgettaria dei cantieri, monitorare i consuntivi e i KPI per fase e per anno, con import di dati storici e dashboard aggregata.

## Persone chiave

| Nome | Ruolo (lato cliente) | Contatto | Note |
|------|---------------------|---------|------|
| — | — | — | — |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| — | — | — |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Go-live | — | — |

## Link utili

- **Repository**: `/Users/simonebrigante/LAIF/repo/albini-castelli/`
- **Notion progetto**: https://www.notion.so/laifgroup/Albini-e-Castelli-Schede-Cantiere-21c90ad6ee48814daa90d04568118236
- **Staging**: —
- **Produzione**: —
- **AWS (dev)**: account `893990996376`, regione `eu-west-1`
- **AWS (prod)**: account `456128143654`, regione `eu-west-1`

## Struttura cartella

```
albini-castelli/
├── README.md              ← questo file
├── aws-config.yaml        ← configurazione AWS diagnostics
├── meeting/               ← note meeting
├── requisiti.md           ← requisiti (da compilare)
├── architettura.md        ← architettura del sistema
├── decisioni.md           ← decisioni tecniche (ADR)
├── feature-log.md         ← feature completate con note
├── stato-progetto.md      ← stato attuale e prossimi passi
├── allegato-tecnico.md    ← allegato contrattuale
├── mockup-brief.md        ← brief per mockup
├── manutenzione.md        ← note post go-live
└── reports/               ← report AWS generati
```

> La repository di codice vive in `/Users/simonebrigante/LAIF/repo/albini-castelli/`, separata dalla KB.

## Note

- Basato su **laif-template v5.0.1**
- Backend ha dipendenze opzionali attive per default: `pdf`, `docx`, `llm` (openai + pgvector), `xlsx`
- Il frontend usa **Turbopack** (`next dev --turbopack`)
- Testing e2e con **Playwright**, unit test backend con **pytest**
