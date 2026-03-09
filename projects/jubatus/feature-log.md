---
progetto: "jubatus"
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
  - "#fase:dev"
---

# Feature Log — Jubatus

> Registro delle feature completate con note tecniche rilevanti.

---

## [2026-03] — Email Body & Metadata nel Frontend

**Requisito di riferimento**: RF-02, RF-03
**Developer**: Team LAIF
**Sprint / periodo**: MVP

**Descrizione**:
Refactoring frontend per mostrare il corpo completo delle email (HTML sanitizzato), destinatari (To/Cc), mittente con email, e allegati con nome e dimensione. Pattern two-level detail: lista leggera + dettaglio on-demand.

**Implementazione**:
- Backend: `ThreadDetailResponse` con `MessageDetailResponse` (body_html, recipients, attachments) in `schema/email.py`
- Backend: eager loading completo in `get_thread()` (recipients, attachments, labels, category) in `message_service.py`
- Frontend: hook `useThreadDetail(threadId)` con fetch condizionale (`enabled: threadId !== null`)
- Frontend: `ConversationThread.tsx` renderizza HTML con DOMPurify, mostra recipients e allegati
- Frontend: utility condivisa `mapThreadDetailToMessages()` usata da `CommandCenterView` e `CleanFlowDetail`
- Dipendenza aggiunta: `dompurify` + `@types/dompurify`

**Problemi e soluzioni**:
- SQLAlchemy `joinedload` con stringa causava 500 → risolto con import `EmailMessageLabel` e attributo class-bound
- Hook `useThreadDetail` aggiunto solo in CleanFlowDetail ma non in CommandCenterView → risolto, aggiunto a entrambe le viste
- Mapping duplicato in 2 viste → estratto in `utils/mapThreadMessages.ts`

**Note per il futuro**:
- DOMPurify non è SSR-safe di default — se si passa a SSR, usare `isomorphic-dompurify`
- Allegati mostrano nome e dimensione ma il download non è ancora implementato

---

## [2026-03] — Modulo Email Backend

**Requisito di riferimento**: RF-01, RF-02, RF-03, RF-08
**Developer**: Team LAIF
**Sprint / periodo**: MVP

**Descrizione**:
Backend completo per gestione email: connessione mailbox OAuth (Gmail, Microsoft), sincronizzazione email con cursor-based pagination, gestione stati ticket, assegnazione operatori, invio risposte.

**Implementazione**:
- 24 endpoint REST in `backend/src/app/email/controller.py`
- Pattern strategy per provider (`providers/base.py` + Gmail/Microsoft) e sender (`senders/base.py` + Gmail/Microsoft/SES)
- Sync engine con deduplicazione (provider_message_id + internet_message_id) e risoluzione thread
- 11 tabelle SQLAlchemy: mailbox_connections, email_threads, email_messages, email_recipients, email_attachments, email_statuses, email_labels, email_categories, email_message_labels, email_message_state_history, email_send_logs
- Crittografia token OAuth a riposo (`crypto.py`)
- Audit trail su ogni cambio stato/assegnazione (state_history)

**Problemi e soluzioni**:
- Thread resolution complessa: risolto con fallback a 3 livelli (provider thread ID → message references → subject matching)
- Allegati grandi: body email > 1MB salvati su S3 invece che nel DB

**Note per il futuro**:
- Il sync e solo manuale (trigger via API), manca background job schedulato
- Token refresh non completamente testato per tutti i provider
- Max 5 errori consecutivi disabilita la mailbox automaticamente

---

## [2026-03] — UI Tickets Frontend (Mock Data)

**Requisito di riferimento**: RF-02, RF-03, RF-04, RF-09, RF-10
**Developer**: Team LAIF
**Sprint / periodo**: MVP

**Descrizione**:
Interfaccia completa per gestione ticket con 4 modalita di visualizzazione: Dashboard (analytics), Command Center (kanban), Clean Flow (lista), Detail (dettaglio conversazione).

**Implementazione**:
- Component principale: `frontend/src/features/tickets/TicketsMain.tsx`
- 4 view modes in `views/`: DashboardView, CommandCenterView, CleanFlowView, CleanFlowDetail
- Componenti riutilizzabili: TicketReply, ConversationThread, StatusBadge, CategoryBadge, SentimentIcon, AiSuggestion, CustomerContext
- Mock data realistici con 20+ ticket (`mock/data.ts`)
- TypeScript types: JubatusTicket, JubatusCustomer, JubatusMessage

**Problemi e soluzioni**:
- Complessita gestione stato tra view modes: gestita con state lifting nel componente TicketsMain

**Note per il futuro**:
- **Non collegato al backend** — usa interamente dati mock
- Da integrare con OpenAPI client generato (`frontend/client/`)
- Le view sono funzionanti ma i dati non persistono

---

## [2026-02] — Scaffolding pagine custom (Ordini, Clienti, Eventi)

**Requisito di riferimento**: RF-05, RF-06
**Developer**: Team LAIF
**Sprint / periodo**: MVP

**Descrizione**:
Pagine Next.js per ordini, clienti (lista + dettaglio), eventi e changelog. Struttura routing e navigazione.

**Implementazione**:
- `app/(authenticated)/(app)/ordini/page.tsx`
- `app/(authenticated)/(app)/clienti/page.tsx` + `[id]/page.tsx`
- `app/(authenticated)/(app)/eventi/page.tsx`
- `app/(authenticated)/(app)/changelog-customer/` e `changelog-technical/`
- Feature modules in `src/features/`: ordini, clienti, changelog, eventi
- Navigazione configurata in `src/config/navigation.tsx`

**Note per il futuro**:
- Pagine scaffoldate con implementazione minima
- Dipendono dall'integrazione con MySQL RDS per dati reali
- Da popolare quando l'accesso al DB Jubatus sara configurato

---

## [2026-01] — Setup progetto da laif-template

**Requisito di riferimento**: —
**Developer**: Simone
**Sprint / periodo**: Setup

**Descrizione**:
Fork da laif-template v5.6.0 con configurazione iniziale: Docker compose, CI/CD, pre-commit hooks, testing infrastructure.

**Implementazione**:
- Docker compose: PostgreSQL 15 + FastAPI + Next.js
- GitHub Actions: backend-tests.yaml (Ruff + Pytest), frontend-tests.yaml (ESLint + TSC + Playwright)
- Pre-commit: configurato con ruff
- Playwright: 4 test E2E (login, user management CRUD)
- Justfile: comandi standardizzati

**Note per il futuro**:
- `values.yaml` ancora con valori template (cod_application: "2024000", repo_name: "laif-template") — da aggiornare per deploy Jubatus
