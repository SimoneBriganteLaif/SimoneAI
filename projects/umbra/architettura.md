---
progetto: "umbra"
data-creazione: "2026-03-10"
ultimo-aggiornamento: "2026-03-10"
tags:
  - "#progetto:umbra"
  - "#fase:dev"
  - "#stack:fastapi"
  - "#stack:nextjs"
  - "#stack:postgresql"
---

# Architettura — Umbra

> Rilevata automaticamente da init-project tramite analisi della repository.

---

## Overview

Piattaforma full-stack di recommendation e business intelligence per distribuzione B2B. Composta da un backend FastAPI, un frontend Next.js 15, un database PostgreSQL con pgvector, e una pipeline ETL standalone per l'addestramento e l'inferenza di modelli CatBoost. Basata su LaifTemplate.

---

## Stack tecnologico

| Layer | Tecnologia | Versione | Motivo della scelta |
|-------|-----------|---------|-------------------|
| Frontend | Next.js + React | 15.3.3 / 19.1.0 | Turbopack, SSR, App Router |
| UI Library | laif-ds | 0.2.58 | Design system interno LAIF |
| State | Redux Toolkit + React Query | 2.0.1 / 5.80.7 | State globale + data fetching |
| Charts | amcharts5 | 5.13.3 | Grafici interattivi dashboard |
| Backend | FastAPI | 0.105 | API REST async, auto-docs |
| ORM | SQLAlchemy | 2.0.43 | Async, multi-schema |
| ML | CatBoost | — | Modelli predittivi riordini |
| Embeddings | pgvector + OpenAI | 0.3.3 / 1.107.0 | RAG e ricerca semantica |
| Database | PostgreSQL | 17.6 | Multi-schema (template, demo, prs) |
| Package Manager | uv (backend) / npm (frontend) | — | Lockfile, velocita |
| Hosting | AWS ECS + S3 | — | Container + static files |
| Data Transfer | SFTP | — | Scambio file con cliente (AS400) |
| ETL | Python standalone | 3.12 | Pipeline 6-step con CatBoost |

---

## Diagramma architetturale

```
[Utenti Umbra] --> [CloudFront/S3] --> [Next.js 15 Frontend]
                                            |
                                     [API REST - FastAPI]
                                            |
                                    [PostgreSQL 17 + pgvector]
                                     /      |       \
                              [schema    [schema   [schema
                              template]   demo]     prs]
                                                     ^
                                                     |
                                              [ETL Pipeline]
                                                     ^
                                                     |
                                            [S3 Data Bucket]
                                                     ^
                                                     |
                                         [SFTP - File da Umbra]
                                                     ^
                                                     |
                                              [AS400 Umbra]
```

---

## Componenti principali

### Backend API (FastAPI)

**Responsabilita**: Servire le previsioni ML, gestire dati agenti e clienti, esporre endpoint per il frontend
**Tecnologia**: FastAPI 0.105 + SQLAlchemy async
**Interfacce**: REST API con Swagger, OpenAPI client auto-generato
**Note**: Schema `prs` per dati business, `template` per sistema base, `demo` per RAG/AI

### Frontend Dashboard (Next.js 15)

**Responsabilita**: Visualizzazione previsioni, segmentazione clienti, dashboard agenti, modulo marketing
**Tecnologia**: Next.js 15 + Turbopack, React 19, laif-ds
**Interfacce**: Consuma API backend via client OpenAPI generato
**Note**: Feature modulari in `/frontend/src/features/`

### ETL Pipeline

**Responsabilita**: Ingestion dati, training modelli CatBoost, inferenza, segmentazione RFM, preparazione dati frontend
**Tecnologia**: Python 3.12 standalone con Docker
**Interfacce**: Legge da S3/SFTP, scrive su PostgreSQL (schema prs)
**Note**: 6 step sequenziali: STG -> TRN -> Training -> INFER -> Segmentation -> PRS. Full run ~1-1.5 ore. Aggiornamenti settimanali per staging + presentation.

### Database PostgreSQL

**Responsabilita**: Persistenza dati, vettori per RAG, risultati ML
**Tecnologia**: PostgreSQL 17.6 + pgvector
**Interfacce**: SQLAlchemy async dal backend, connessione diretta da ETL
**Note**: 3 schemi separati. 23 migrazioni Alembic applicate.

---

## Flussi principali

### Flusso: Aggiornamento settimanale dati

```
1. Umbra AS400 esporta file CSV nella cartella SFTP (elaborazioni_settimanali)
2. ETL legge i file da SFTP e li carica su S3
3. ETL esegue staging (STG) e presentation (PRS) — solo settimanale
4. Frontend mostra dati aggiornati
```

### Flusso: Training mensile completo

```
1. ETL esegue tutti i 6 step: STG -> TRN -> Training -> INFER -> Segmentation -> PRS
2. Modelli CatBoost riaddestrati con dati aggiornati
3. Nuove previsioni generate e caricate in schema prs
4. Dashboard aggiornata con nuove previsioni e segmentazione
```

---

## Dipendenze esterne

| Servizio | Scopo | Criticita | Alternativa se cade |
|---------|-------|----------|-------------------|
| SFTP Umbra | Ricezione file dati | Alta | Upload manuale su S3 |
| AWS S3 | Storage file dati e frontend | Alta | — |
| AWS ECS | Hosting backend | Alta | — |
| OpenAI API | Embeddings per RAG | Bassa | Funzionalita RAG degradata |

---

## Considerazioni di sicurezza

- **Autenticazione**: LaifTemplate (JWT + login middleware)
- **Autorizzazione**: Role-based (template schema)
- **Dati sensibili**: Dati vendita B2B, non PII. File transitano via SFTP con IP whitelist
- **Backup**: RDS automated backup (AWS)

---

## Debito tecnico noto

| # | Descrizione | Impatto | Priorita |
|---|------------|--------|---------|
| 1 | FastAPI pinned a 0.105 per bug file upload | Impossibile aggiornare | Bassa |
| 2 | Certificato SFTP scaduto | Blocca automazione | Alta |
| 3 | Ponte S400-DMZ non configurato | File depositati manualmente | Media |
