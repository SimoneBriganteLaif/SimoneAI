---
progetto: "jubatus"
data-creazione: "2026-03-08"
ultimo-aggiornamento: "2026-03-09"
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
  - "#fase:dev"
  - "#stack:fastapi"
  - "#stack:nextjs"
  - "#stack:aws"
---

# Architettura — Jubatus Customer Care

---

## Overview

Piattaforma interna di customer care costruita su `laif-template` (v5.6.0). Il backend FastAPI gestisce l'integrazione email (Gmail, Microsoft, AWS SES) con sync periodico, stato ticket, assegnazione e categorizzazione. Il frontend Next.js offre più modalità di visualizzazione ticket (dashboard, command center, clean flow). Il deploy avviene sull'account AWS di Jubatus per accesso diretto a MySQL RDS e S3.

---

## Stack tecnologico

| Layer | Tecnologia | Versione | Motivo della scelta |
|-------|-----------|---------|-------------------|
| Frontend | Next.js + React + TypeScript | 16.1.1 / 19.2.3 / 5.9.3 | Standard laif-template, App Router, Turbopack |
| Design System | laif-ds + Tailwind CSS | 0.2.67 / 4.1.18 | Componenti condivisi LAIF |
| State Management | Redux Toolkit + TanStack Query | 2.11.2 / 5.90.12 | Redux per stato globale, TanStack per server state |
| Backend | FastAPI + Python | 0.128.0 / 3.12 | Preferenza Jubatus per nuovi servizi, async nativo |
| ORM | SQLAlchemy + Alembic | 2.0.45 / 1.17.2 | Standard laif-template |
| Database | PostgreSQL | 15 | Database applicativo (ticket, email, utenti) |
| Database cliente | MySQL RDS | — | Read-only, dati utenti/ordini/eventi Jubatus |
| Storage | AWS S3 | — | Foto, video, selfie (bucket Jubatus esistenti) |
| Auth | OAuth2 + JWT + RBAC | — | Standard laif-template |
| Email providers | Gmail API, Microsoft Graph, AWS SES | — | Multi-provider per flessibilità |
| CI/CD | GitHub Actions | — | Test + deploy automatizzato |
| Container | Docker + docker-compose | — | Dev locale multi-container |
| Task runner | Just | — | Comandi standardizzati |

---

## Diagramma architetturale

```
                         ┌─────────────────┐
                         │   Browser        │
                         │  (Operatori CS)  │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │   Next.js 16     │
                         │   (App Router)   │
                         │   Port 8080      │
                         └────────┬─────────┘
                                  │ HTTP/REST
                         ┌────────▼─────────┐
                         │   FastAPI        │
                         │   Port 8000      │
                         │                  │
                         │ ┌──────────────┐ │
                         │ │  Template    │ │  ← User mgmt, auth, chat,
                         │ │  modules    │ │    files, notifications
                         │ └──────────────┘ │
                         │ ┌──────────────┐ │
                         │ │  App modules │ │  ← Email, changelog
                         │ └──────────────┘ │
                         └───┬─────┬────┬───┘
                             │     │    │
              ┌──────────────┘     │    └──────────────┐
              │                    │                    │
     ┌────────▼────────┐  ┌───────▼───────┐  ┌────────▼────────┐
     │  PostgreSQL 15  │  │  MySQL RDS    │  │   AWS S3        │
     │  (applicativo)  │  │  (read-only)  │  │  (foto/video)   │
     │  Port 5432      │  │  Jubatus AWS  │  │  Jubatus AWS    │
     └─────────────────┘  └───────────────┘  └─────────────────┘

              ┌──────────────────────────────────────┐
              │          Email Providers              │
              │  ┌─────────┐ ┌──────┐ ┌───────────┐  │
              │  │  Gmail  │ │  MS  │ │  AWS SES  │  │
              │  │  OAuth  │ │Graph │ │  (invio)  │  │
              │  └─────────┘ └──────┘ └───────────┘  │
              └──────────────────────────────────────┘
```

---

## Componenti principali

### Email Module (`backend/src/app/email/`)

**Responsabilita**: Gestione completa del ciclo email — raccolta, sync, stato, invio.
**Struttura interna**:
- `controller.py` — 24 endpoint REST
- `providers/` — OAuth token management (Gmail, Microsoft)
- `senders/` — Invio email (Gmail, Microsoft, AWS SES)
- `services/` — 6 servizi: mailbox, message, send, sync, status, label
- `sync/engine.py` — Motore di sincronizzazione con cursor-based pagination
- `crypto.py` — Crittografia token OAuth
- `models.py` — 11 tabelle SQLAlchemy

**Interfacce**: REST API consumate dal frontend Next.js.

### Template Modules (`backend/src/template/`)

**Responsabilita**: Funzionalita condivise cross-progetto LAIF (NON modificare).
**Moduli**: user_management, chat, ticketing, notifications, files, conversations, tasks, health.
**Note**: Gestiti da laif-template upstream. Aggiornamenti via merge dal template.

### Frontend Tickets (`frontend/src/features/tickets/`)

**Responsabilita**: UI principale per la gestione ticket.
**Modalita di visualizzazione**:
- Dashboard — metriche e analytics
- Command Center — vista kanban
- Clean Flow — lista + dettaglio
**Stato attuale**: Usa dati mock, non ancora collegato al backend.

### Frontend Template (`frontend/template/`)

**Responsabilita**: UI condivise (user management, chat, profilo, file, help).
**Note**: Da laif-template, non modificare direttamente.

---

## Flussi principali

### Flusso: Sincronizzazione email

```
1. Trigger sync (manuale o schedulato)
2. Per ogni mailbox connessa:
   a. Refresh token OAuth via provider (Gmail/Microsoft)
   b. Fetch nuovi messaggi con cursor (paginazione)
   c. Per ogni messaggio:
      - Deduplicazione (provider_message_id + internet_message_id)
      - Risoluzione thread (provider thread ID, references, subject)
      - Import messaggio + destinatari + allegati
   d. Aggiornamento cursor per sync successivo
3. Max 5 errori consecutivi → disabilita mailbox
```

### Flusso: Gestione ticket

```
1. Email arriva → sync engine crea/aggiorna thread
2. Operatore vede thread nella vista ticket
3. Operatore assegna stato (nuovo → WIP → fatto)
4. Ogni cambio stato/assegnazione → registrato in state_history
5. Operatore risponde → email inviata via provider/SES
6. Risposta tracciata in email_send_logs
```

### Flusso: Autenticazione

```
1. Login con username/password → JWT token
2. Token include ruoli e permessi (RBAC)
3. Ogni request verificata via middleware
4. Dev mode: auto-login middleware per testing
```

---

## Dipendenze esterne

| Servizio | Scopo | Criticita | Alternativa se cade |
|---------|-------|----------|-------------------|
| Gmail API | Ricezione/invio email | Alta | Microsoft Graph / AWS SES |
| Microsoft Graph | Ricezione/invio email | Media | Gmail API / AWS SES |
| AWS SES | Invio email (fallback) | Bassa | Gmail/Microsoft sender |
| MySQL RDS Jubatus | Dati utenti/ordini/eventi | Alta | Nessuna (read-only, dati proprietari) |
| AWS S3 Jubatus | Foto, video, selfie | Alta | Nessuna (storage proprietario) |
| PostgreSQL | Database applicativo | Alta | Nessuna (core data) |

---

## Considerazioni di sicurezza

- **Autenticazione**: OAuth2 + JWT via laif-template. Token con scadenza.
- **Autorizzazione**: RBAC con permessi granulari per ruolo.
- **Token OAuth email**: Crittografati a riposo (`crypto.py`), storage in PostgreSQL.
- **MySQL**: Accesso esclusivamente read-only. Connessione via security group AWS.
- **Dati sensibili**: Email body > 1MB salvate su S3 (non in DB). Allegati max 25MB.
- **CORS**: Limitato a localhost in dev. Da configurare per produzione.

---

## Considerazioni di scalabilita

- **Utenti concorrenti**: 2-4 operatori CS — carico minimo, non un collo di bottiglia.
- **Volume email**: Dipende dal volume segnalazioni. Sync con cursor evita re-fetch.
- **Storage**: Email body grandi su S3 per non appesantire PostgreSQL.
- **Background sync**: Non ancora implementato come job schedulato — attualmente solo manuale.

---

## Debito tecnico noto

| # | Descrizione | Impatto | Priorita |
|---|------------|--------|---------|
| 1 | Frontend usa dati mock, non collegato al backend | Alto — blocca validazione end-to-end | Alta |
| 2 | Sync email solo manuale, no background jobs | Medio — operatori devono triggerare sync | Alta |
| 3 | Token refresh incompleto | Medio — token scaduti bloccano sync | Alta |
| 4 | Feature ordini/clienti/eventi solo scaffoldate | Basso — dipende da integrazione MySQL | Media |
| 5 | Test coverage limitata (16 backend, 4 frontend) | Medio — rischio regressioni | Media |
| 6 | Nessun rate limiting sugli endpoint API | Basso — uso interno, pochi utenti | Bassa |
| 7 | values.yaml ancora con valori laif-template (cod_application, repo_name) | Basso — da allineare per deploy Jubatus | Media |
