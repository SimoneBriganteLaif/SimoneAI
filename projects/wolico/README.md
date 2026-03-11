---
progetto: "wolico"
cliente: "LAIF (interno)"
industria: "operations-interne"
stato: "in-sviluppo"
data-inizio: ""
data-fine: ""
stack:
  - FastAPI 0.131
  - Next.js 16
  - PostgreSQL
  - SQLAlchemy 2
  - Alembic
  - Redux Toolkit
  - React Query
  - laif-ds
  - amCharts 5
  - AWS (S3, CloudWatch)
  - OpenAI + pgvector
tags:
  - "#progetto:wolico"
  - "#tipo:interno"
  - "#industria:operations-interne"
  - "#fase:dev"
  - "#stack:fastapi"
  - "#stack:nextjs"
  - "#stack:postgresql"
  - "#stack:sqlalchemy"
  - "#stack:aws"
---

# Wolico — LAIF (interno)

## Contesto

Wolico è la piattaforma gestionale interna di LAIF. Centralizza tutte le operazioni aziendali: CRM, ticketing delle app clienti, contabilità, rendicontazione ore, gestione HR, monitoring applicazioni e integrazione con Odoo ERP. È il punto di riferimento per le attività operative quotidiane del team.

## Obiettivo del progetto

Fornire al team LAIF un unico strumento per gestire l'intero ciclo operativo: dall'acquisizione lead alla fatturazione, dal supporto clienti al monitoring delle app in produzione. In futuro: aggiungere nuovi moduli per coprire ulteriori esigenze interne.

## Moduli attivi

| Modulo | Descrizione |
|--------|-------------|
| **CRM** | Leads, sales, partners, contacts, notes, tag, tranche fatture |
| **Ticketing** | Ticket per app clienti con messaggi, allegati, aggiornamenti |
| **HR / Employees** | Anagrafiche dipendenti, contratti |
| **Calendar** | Giorni lavorativi, ferie, festivi, weekend |
| **Economics** | Cash flow, balance, marginalità, ricavi |
| **Operations** | Costi cloud, staffing, outages, reporting ore |
| **Administration** | Spese, voci spesa, recap mensili |
| **Monitoring** | Tracking errori backend e frontend delle app |
| **Changelog** | Audit log di sistema |
| **Odoo** | Integrazione ERP (fatture, pagamenti) |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| Simone Brigante | Sviluppo + gestione | — |

## Link utili

- **Repository**: `/Users/simonebrigante/LAIF/repo/wolico/`
- **Produzione**: `https://wolico.app.laifgroup.com`
- **MCP Server**: `mcp-servers/wolico/` (3 tool: ferie team, ferie persona, calendario settimana)

## Note tecniche

- Basato su **LAIF Template** (architettura standard LAIF)
- Frontend usa **laif-ds** (design system LAIF) + **amCharts 5** per grafici
- Integrazione **OpenAI + pgvector** per funzionalità AI/embeddings
- Integrazione **Odoo** per dati contabili e fatturazione
- Schema DB: `prs` (dati app), `template` (dati laif-template)
- 28 migrazioni Alembic attive

## Struttura cartella

```
wolico/
├── README.md              ← questo file
├── meeting/               ← note meeting
├── requisiti.md           ← requisiti per nuovi moduli
├── architettura.md        ← architettura del sistema
├── decisioni.md           ← decisioni tecniche (ADR)
├── feature-log.md         ← feature completate con note
├── stato-progetto.md      ← stato attuale dei moduli
├── manutenzione.md        ← note operative e accessi
└── windsurf-briefs/       ← brief per sviluppo Windsurf
```

> La repository di codice vive in `/Users/simonebrigante/LAIF/repo/wolico/`, separata dalla KB.
