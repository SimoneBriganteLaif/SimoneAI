---
progetto: "umbra"
cliente: "Umbra S.p.a."
industria: "Distribuzione prodotti dentali"
stato: "in-sviluppo"
data-inizio: "2025-11-20"
data-fine: ""
stack:
  - FastAPI
  - Next.js 15
  - PostgreSQL 17
  - pgvector
  - CatBoost ML
  - ETL Python
  - AWS (S3, ECS)
  - SFTP
tags:
  - "#progetto:umbra"
  - "#industria:healthcare"
  - "#fase:dev"
---

# Umbra — Umbra S.p.a.

## Contesto

Umbra S.p.a. e un distributore B2B di prodotti dentali (linee Studio e Laboratorio) con sede in Italia. LAIF ha gia sviluppato una piattaforma "recommender" basata su modelli CatBoost per prevedere riordini e segmentare clienti. Il progetto attuale (codice 2025079, contratto EUR 31.000) prevede il miglioramento della piattaforma esistente e lo sviluppo di un nuovo modulo marketing per la pianificazione delle promozioni WOW.

## Obiettivo del progetto

Due moduli principali:

1. **Improvement piattaforma recommender** (EUR 13.000): passaggio da aggiornamento mensile a settimanale dei dati, automazione dello scambio file via SFTP (sostituzione FileZilla manuale), gestione varianti prodotto con aggregazione per modello.

2. **Pianificatore promozioni WOW** (EUR 18.000): modulo marketing che suggerisce le promozioni WOW piu efficaci per ogni periodo, basandosi su budget fornitori, storicita, vincoli temporali, stagionalita e performance attese. Supporto decisionale per la responsabile marketing, non sostitutivo.

## Persone chiave

| Nome | Ruolo (lato cliente) | Contatto | Note |
|------|---------------------|---------|------|
| Gianni Fagnioli | Legale rappresentante | | Firmatario contratto |
| Adriano Bezzi | IT / Sistemi | | Gestisce AS400, estrazioni dati, SFTP |
| Alessandra Olivanti | Responsabile Marketing | | Utente principale modulo WOW |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| Simone | Lead / PM | |
| Tancredi | Developer | Backend + ETL |
| Daniele | Developer | Frontend + integrazioni |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Kick-off | 2025-12-01 | Completato |
| Allineamento tecnico SFTP | 2026-01-22 | Completato |
| Requisiti WOW con marketing | 2026-02-09 | Completato |
| Mockup interfaccia WOW | 2026-03-03 | In corso |
| Validazione UI/UX | 2026-03-12 | Pianificato |
| Go-live | — | Da definire |

## Link utili

- **Repository**: `/Users/simonebrigante/LAIF/repo/umbra-recommend/`
- **Notion progetto**: [Umbra - Improvement recommender](https://www.notion.so/2b190ad6ee488159960cf541149b511f)
- **Contratto**: `/Users/simonebrigante/LAIF/Progetti/Umbra/2025-11-19 Sviluppi Recommender e Pianificatore promozioni_signedLAIF.pdf`
- **Staging**: —
- **Produzione**: —

## Struttura cartella

```
umbra/
├── README.md              <- questo file
├── meeting/               <- note meeting (una per file)
├── requisiti.md           <- requisiti estratti e validati
├── architettura.md        <- architettura del sistema
├── decisioni.md           <- decisioni tecniche (ADR)
├── feature-log.md         <- feature completate con note
├── stato-progetto.md      <- stato attuale, blocchi e prossimi passi
├── allegato-tecnico.md    <- allegato contrattuale (max 3 pag)
├── mockup-brief.md        <- brief per mockup Windsurf
├── aws-config.yaml        <- config risorse AWS
└── manutenzione.md        <- note post go-live
```

> La repository di codice vive in `/Users/simonebrigante/LAIF/repo/umbra-recommend/`, separata dalla KB.

## Note

- Codice progetto Notion: 2025079
- App name AWS: `umbra-recommend`
- AWS Dev Account: `053612131633` (eu-west-1)
- AWS Prod Account: `386318839910`
- Il cliente NON riceve scritture sui propri sistemi — solo lettura dati via SFTP
