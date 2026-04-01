# Argo — Analisi Completa Repository

## 1. Overview

**Argo** e' la piattaforma customer-facing dell'agenzia marittima **Amatori**, che opera dal porto di Ancona. L'app consente ai clienti di:

- Registrarsi e gestire il proprio profilo viaggiatore
- Consultare e salvare le proprie prenotazioni di traghetti (integrate con l'API Jadrolinija)
- Interagire con un **chatbot AI** (OpenAI GPT-4.1-mini) per assistenza su prenotazioni, rotte, porti e consigli di viaggio
- Gestire una knowledge base documentale per il chatbot (RAG con OpenAI Vector Stores)
- Visualizzare i propri biglietti con dettagli su passeggeri, veicoli, cabine, cani, assicurazione

**Cliente**: Amatori (agente marittimo, Ancona)
**Industria**: Trasporto marittimo / Turismo
**Cod. Applicazione**: 2025013

---

## 2. Versioni

| Elemento | Versione |
|---|---|
| App (`version.txt`) | **1.1.1** |
| laif-template (`version.laif-template.txt`) | **5.6.0** |
| `values.yaml` version | 1.1.0 |

---

## 3. Team (top contributors)

| Contributor | Commits |
|---|---|
| Pinnuz | 269 |
| mlife | 223 |
| github-actions[bot] | 121 |
| Simone Brigante | 92 |
| bitbucket-pipelines | 86 |
| Marco Pinelli | 85 |
| neghilowio | 75 |
| Leonardo Carboni | 73 |
| cavenditti-laif | 50 |
| sadamicis | 49 |

Totale commit: **~1451** (695 dal 2025 in poi)

---

## 4. Stack e dipendenze non-standard

### Backend (Python 3.12)

**Dipendenze standard template**: FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, asyncpg, psycopg2-binary, uvicorn, boto3, bcrypt/passlib, python-jose, httpx, requests, typer, jinja2

**Dipendenze NON standard (specifiche di Argo)**:
| Dipendenza | Scopo |
|---|---|
| `openai-agents==0.0.15` | **OpenAI Agents SDK** per il chatbot AI multi-tool |
| `aiohttp~=3.13.0` | HTTP async (usata probabilmente dall'agents SDK) |
| `openai~=2.14.0` (gruppo llm) | Client OpenAI per RAG e completions |
| `pgvector~=0.4.2` (gruppo llm) | Supporto vector embeddings PostgreSQL |
| `PyMuPDF~=1.26.7` (gruppo pdf) | Parsing PDF |
| `python-docx~=1.2.0` (gruppo docx) | Parsing DOCX |
| `xlsxwriter~=3.2.2` (gruppo xlsx) | Generazione file Excel |
| `pandas~=2.3.3` (gruppo xlsx) | Manipolazione dati per export |

### Frontend (Node >=24, Next.js 16)

**Dipendenze NON standard (oltre template base)**:
| Dipendenza | Scopo |
|---|---|
| `@amcharts/amcharts5` | Grafici avanzati |
| `@draft-js-plugins/editor` + `@draft-js-plugins/mention` | Editor rich-text con menzioni |
| `@hello-pangea/dnd` | Drag and drop |
| `@microsoft/fetch-event-source` | SSE per streaming chat AI |
| `draft-js` + `draft-js-export-html` | Editor rich-text |
| `katex` + `rehype-katex` + `remark-math` | Rendering formule matematiche |
| `react-markdown` + `remark-gfm` | Rendering markdown (risposte chat) |
| `react-syntax-highlighter` | Syntax highlighting nel chat |
| `react-hot-toast` | Notifiche toast |
| `tailwind-merge` | Utility per merge classi Tailwind |
| `next-pwa` | Progressive Web App |

### Docker Compose

Servizi standard: `db` (PostgreSQL), `backend` (FastAPI). XLSX abilitato via build arg `ENABLE_XLSX: 1`.
Config extra: `docker-compose.wolico.yaml` per test con rete condivisa Wolico.

---

## 5. Modello dati completo

### Tabelle custom (schema `prs`)

#### `argo_users`
| Colonna | Tipo | Note |
|---|---|---|
| `id` | int (PK, FK -> template.users.id) | One-to-one con User template |
| `flg_privacy` | bool | Consenso privacy |
| `flg_marketing` | bool | Consenso marketing |
| `preferences` | JSONB (nullable) | Profili viaggio + booking_status |
| `birth_date` | datetime (nullable) | Data di nascita |
| `saved_reservations` | JSONB (nullable) | **Array di oggetti prenotazione completi** (dati da API Jadro) |

#### `documents`
| Colonna | Tipo | Note |
|---|---|---|
| `id` | int (PK) | |
| `name` | str | Nome documento |
| `url` | str (nullable) | URL S3 |
| `openai_vectorstore_id` | str (nullable) | ID file su OpenAI |
| `created_at` | datetime | server_default now() |
| `id_user` | int (FK -> template.users.id) | Utente che ha caricato |

#### `conversations`
| Colonna | Tipo | Note |
|---|---|---|
| `id` | int (PK) | |
| `name` | str | Titolo conversazione (auto-generato da AI) |
| `created_at` | datetime | server_default now() |
| `id_user` | int (FK -> template.users.id) | |

#### `threads`
| Colonna | Tipo | Note |
|---|---|---|
| `id` | int (PK) | |
| `sender` | SenderType (enum: user/bot) | |
| `message` | str | Contenuto messaggio |
| `sent_at` | datetime | server_default now() |
| `id_conversation` | int (FK -> prs.conversations.id, CASCADE) | |
| `id_user` | int (FK -> template.users.id) | |
| `citations` | JSON (nullable) | Citazioni RAG |

#### `vector_stores`
| Colonna | Tipo | Note |
|---|---|---|
| `id` | int (PK) | |
| `name` | str | |
| `openai_vector_store_id` | str | ID OpenAI Vector Store |
| `is_active` | bool (default True) | |
| `created_at` | datetime | |
| `updated_at` | datetime | |

### Diagramma ER (Mermaid)

```mermaid
erDiagram
    USERS ||--o| ARGO_USERS : "1:1 (id)"
    USERS ||--o{ DOCUMENTS : "id_user"
    USERS ||--o{ CONVERSATIONS : "id_user"
    USERS ||--o{ THREADS : "id_user"
    CONVERSATIONS ||--o{ THREADS : "id_conversation"

    USERS {
        int id PK
        string email
        string name
        string surname
        string password
        int id_business FK
        bool flg_valid
    }

    ARGO_USERS {
        int id PK_FK
        bool flg_privacy
        bool flg_marketing
        jsonb preferences
        datetime birth_date
        jsonb saved_reservations
    }

    DOCUMENTS {
        int id PK
        string name
        string url
        string openai_vectorstore_id
        datetime created_at
        int id_user FK
    }

    CONVERSATIONS {
        int id PK
        string name
        datetime created_at
        int id_user FK
    }

    THREADS {
        int id PK
        enum sender
        string message
        datetime sent_at
        int id_conversation FK
        int id_user FK
        json citations
    }

    VECTOR_STORES {
        int id PK
        string name
        string openai_vector_store_id
        bool is_active
        datetime created_at
        datetime updated_at
    }
```

---

## 6. API Routes

### `/argo-users` (argo_users controller)
| Metodo | Path | Descrizione |
|---|---|---|
| POST | `/signup` | Registrazione utente (crea User + ArgoUsers + invia email verifica) |
| GET | `/verify-signup/{token}` | Verifica email con token |
| POST | `/preferences` | Aggiorna preferenze viaggiatore (profili + booking_status) |
| GET | `/preferences` | Legge preferenze utente |

### `/reservation` (reservation controller)
| Metodo | Path | Descrizione |
|---|---|---|
| POST | `/add` | Aggiunge prenotazione all'utente (fetch da API Jadro + salva in DB) |
| POST | `/remove` | Rimuove prenotazione dalla lista salvata |
| GET | `/my-reservations` | Elenco prenotazioni salvate (solo DB, no API) |
| POST | `/refresh` | Aggiorna dati prenotazione da API esterna |
| POST | `/check-email` | Cerca prenotazioni per email (via API Jadro) |
| GET | `/health` | Health check connettivita' API Jadro |

### `/argo_conversations` (chat controller - RouterBuilder CRUD + custom)
| Metodo | Path | Descrizione |
|---|---|---|
| GET | `/{id}` | Dettaglio conversazione con threads |
| GET | `/search` | Lista conversazioni |
| POST | `/` | Crea conversazione |
| PUT | `/{id}` | Aggiorna conversazione |
| DELETE | `/{id}` | Elimina conversazione |
| POST | `/{id_conversation}/stream` | **Endpoint chat streaming** (SSE) - invia domanda all'agente AI |

### `/argo_documents` (documents controller - RouterBuilder CRUD + file)
| Metodo | Path | Descrizione |
|---|---|---|
| GET | `/search` | Lista documenti |
| POST | `/` | Crea documento |
| PUT | `/{id}` | Aggiorna documento |
| DELETE | `/{id}` | Elimina documento (+ file S3 + file OpenAI) |
| POST | `/{id}/upload` | Upload file (S3 + OpenAI Vector Store) |
| GET | `/{id}/download` | Download file da S3 |

### `/changelog` (changelog controller)
Controller per changelog customer e tecnico.

---

## 7. Business Logic

### Chatbot AI con OpenAI Agents SDK

Il cuore dell'applicazione. Architettura:

1. **AgentProvider** (`agents_provider.py`): wrapper attorno a `openai-agents` SDK
   - Crea agenti con modello `gpt-4.1-mini`
   - Streaming SSE delle risposte verso il frontend
   - Salva automaticamente i messaggi bot in DB

2. **Agent Tools** (5 tool funzionali):
   - `get_reservation_details` - Recupera dettagli prenotazione da API Jadro
   - `request_human_assistance` - Inoltra conversazione via email al team supporto
   - `get_all_ports` - Lista porti disponibili da API Jadro
   - `get_routes_from_port` - Tratte da un porto specifico
   - `get_route_dates` - Date disponibili per una tratta

3. **FileSearchTool** (OpenAI): RAG sulla knowledge base documentale (Vector Stores)

4. **Prompt dinamico** (`prompt.md`): il prompt dell'agente viene popolato con:
   - Data/ora corrente
   - Prenotazioni prossime e passate dell'utente
   - Preferenze di viaggio dell'utente (12 profili viaggiatore)
   - Guardrail: rifiuta domande non pertinenti al marittimo

### Gestione Prenotazioni

- Le prenotazioni NON sono tabelle DB dedicate: sono salvate come **array JSON** nel campo `saved_reservations` di `argo_users`
- I dati vengono fetchati dall'API esterna Jadro e convertiti in formato frontend-friendly
- Validazione contatto (telefono/email) per aggiungere una prenotazione
- Supporto per passeggeri (adulti/bambini/neonati), veicoli con dimensioni, cabine/ponti/poltrone, cani, assicurazione

### Registrazione utenti

Self-signup con:
1. Creazione utente in `template.users` (flg_valid=False)
2. Creazione record `argo_users`
3. Assegnazione ruolo "user"
4. Invio email verifica con token
5. Validazione token e attivazione account

### Knowledge Base / RAG

- Upload documenti su S3 + OpenAI Files API
- Attach automatico a Vector Store attivo
- Eliminazione gestita sia lato S3 che OpenAI
- Il chatbot usa `FileSearchTool` per cercare nei documenti

### Background Tasks

`events.py` contiene un esempio di task periodico (con `repeat_every`), ma e' **commentato/disabilitato**.

---

## 8. Integrazioni Esterne

### Jadrolinija API (Jadro)
- **Base URL**: `http://api2.amatori.com:5980/jadroservices/api`
- **Timeout**: 30s
- **Client**: `JadroAPIClient` (singleton `jadro_client`)
- **Endpoint utilizzati**:
  - `GET /booking/getBookingDetail/{book_number}` - Dettaglio prenotazione
  - `GET /booking/GetRouteList/Ports` - Lista porti
  - `GET /booking/GetRouteList/{port_code}` - Tratte da un porto
  - `GET /booking/GetRouteDates/{from}/{to}` - Date per tratta
  - `GET /booking/GetBookingListByMail/{email}` - Prenotazioni per email
- Parsing complesso della risposta API in schema Pydantic (passeggeri, veicoli, cabine, servizi)
- Paesi supportati: Italia, Croazia, Montenegro, Albania, Grecia, Bosnia

### OpenAI
- **Modello chat**: `gpt-4.1-mini` (via Agents SDK)
- **Modello titoli**: OpenAI chat completion (via `template.chat.gen_ai_provider`)
- **Vector Stores**: per RAG documentale
- **Files API**: upload/delete documenti
- Tracing abilitato (`set_tracing_export_api_key`)

### AWS
- **S3**: storage documenti
- **SSM Parameter Store**: configurazione (da template)

### Email (SES via template)
- Template: `signup.html` (verifica account), `support_assistance.html` (richiesta assistenza)
- Email di supporto: `marco.vita@laifgroup.com`
- Branding: colore `#004B93` (blu Amatori)

---

## 9. Frontend — Albero Pagine

```
app/
├── login/                              → Pagina login custom
├── signup/                             → Pagina registrazione + verifica token
├── (not-auth-template)/
│   ├── logout/                         → Logout
│   └── registration/                   → Registrazione (template)
├── (authenticated)/
│   ├── chat/                           → Chat AI principale
│   ├── knowledge/                      → Gestione knowledge base documenti
│   ├── profiling/                      → Selezione profilo viaggiatore + booking status
│   ├── viaggi/                         → Storico viaggi / biglietti salvati
│   ├── (app)/
│   │   ├── changelog-customer/         → Changelog per clienti
│   │   └── changelog-technical/        → Changelog tecnico
│   └── (template)/
│       ├── conversation/
│       │   ├── chat/                   → Chat (template)
│       │   ├── analytics/              → Analytics conversazioni
│       │   ├── feedback/               → Feedback
│       │   └── knowledge/              → Knowledge base (template)
│       │       └── detail/
│       ├── files/                      → Gestione file
│       ├── help/
│       │   ├── faq/                    → FAQ
│       │   └── ticket/                 → Ticket supporto
│       ├── profile/                    → Profilo utente
│       └── user-management/            → Gestione utenti (admin)
│           ├── business/
│           ├── group/
│           │   └── detail/
│           ├── permission/
│           ├── role/
│           └── user/
│               ├── create/
│               └── detail/
│                   ├── groups/
│                   ├── info/
│                   └── roles/
```

### Features frontend principali

| Feature | File principali | Descrizione |
|---|---|---|
| **Chat AI** | `ChatMain.tsx`, `InputChat.tsx`, `messages.tsx`, `markdownComponents.tsx` | Chat con streaming SSE, rendering markdown/LaTeX/syntax highlight |
| **Viaggi** | `TravelHistoryMain.tsx`, `TicketDetail.tsx`, `AddTicketModal.tsx` | Visualizzazione biglietti, aggiunta/rimozione prenotazioni |
| **Profiling** | `ProfilingPage.tsx`, `ReservationSelectionModal.tsx` | Selezione profilo viaggiatore (12 tipi), booking status |
| **Knowledge** | `KnowledgeMain.tsx`, `ManageAttachments.tsx`, `uploadDocument.tsx` | Upload/gestione documenti per RAG |
| **Signup** | `SignupMain.tsx` | Registrazione self-service |
| **Login** | `LoginPage.tsx`, `ForgotPasswordModal.tsx` | Login custom con reset password |
| **Changelog** | `ChangelogCustomerMain.tsx`, `ChangelogTechnicalMain.tsx` | Changelog dual-target |
| **Landing** | `LandingMain.tsx` | Pagina landing |

---

## 10. Deviazioni dal laif-template

### Moduli custom backend (`backend/src/app/`)
- `agents/` - OpenAI Agents SDK integration (provider, tools, prompt)
- `argo_users/` - Registrazione self-service e preferenze utente
- `chat/` - Controller conversazioni con streaming AI
- `documents/` - Gestione documenti con sync OpenAI Vector Stores
- `reservation/` - Integrazione API Jadrolinija
- `common/email/templates/` - Template email custom (signup, support_assistance)

### Pagine frontend custom
- `app/(authenticated)/chat/` - Chat AI dedicata
- `app/(authenticated)/knowledge/` - Knowledge base
- `app/(authenticated)/profiling/` - Profiling viaggiatore
- `app/(authenticated)/viaggi/` - Storico viaggi
- `app/signup/` - Self-signup
- `app/login/` - Login custom

### File/cartelle non standard
- `docker-compose.wolico.yaml` - Testing con rete Wolico
- `docs/amatori/JADRO_API_CLIENT.md` - Documentazione API Jadro
- `docs/troisi/custom_email_style.md` - Stile email custom
- `AGENTS.md` - Documentazione agenti AI
- 34 migrazioni Alembic (molte di template + custom)

---

## 11. Pattern notevoli

### Prenotazioni come JSON document store
Le prenotazioni non sono in tabelle relazionali ma salvate come **array JSONB** nel campo `saved_reservations` di `argo_users`. Questo evita la complessita' di un modello relazionale per dati che arrivano da API esterna con struttura complessa e variabile (passeggeri, veicoli, cabine, servizi). Tradeoff: nessun indice o query SQL sulle prenotazioni individuali.

### OpenAI Agents SDK con streaming
Uso del nuovo `openai-agents` SDK (v0.0.15) con `Runner.run_streamed()` per risposte in streaming. L'agente ha 5 function tools + FileSearchTool per RAG. Il prompt e' dinamico e viene popolato con contesto utente ad ogni richiesta.

### Dual email template system
Template email custom (`signup`, `support_assistance`) con branding Amatori (colore `#004B93`). L'assistenza umana inoltra l'intera conversazione via email con contesto prenotazioni.

### Phone normalization robusto
Utility `phone_utils.py` con normalizzazione telefoni italiani e internazionali (gestione prefissi `0039`, `+39`, confronto per suffisso). Usato per validare che chi aggiunge una prenotazione sia il titolare.

### Profiling viaggiatore
12 profili viaggiatore predefiniti (solo_explorer, family_traveler, luxury_lover, ecc.) che influenzano il comportamento del chatbot. Il prompt dell'agente viene adattato in base al profilo selezionato.

---

## 12. Note e tech debt

### Tech debt identificato
- **TODO nel codice**: `# TODO: Remove` sulla relazione `conversation` in `Thread` model
- **TODO**: `# TODO maybe only use one?` su httpx + requests (duplicazione client HTTP)
- **TODO**: `# TODO: move this to a config file ???` per ruolo e business default in `argo_users/service.py`
- **TODO**: `# TODO: check` gestione fallimento ruolo default non trovato
- **Changelog applicativo non aggiornato**: solo entry `0.1 2025-04-26`, nessun changelog per le release successive (1.0.x, 1.1.x)
- **`events.py` con task di esempio**: contiene un task periodico `_send_example_task` commentato, residuo del template
- **`datetime.utcnow()` deprecato**: usato in `argo_users/service.py` per token expiration
- **Password in `AgencyInfoSchema`**: lo schema include `user` e `password` dell'agenzia (dati dalla API Jadro) - potenziale rischio sicurezza se esposto
- **Debug print statements**: molti `print(f"DEBUG: ...")` e `print(f"Error...")` sparsi nel codice invece di usare il logger

### Peculiarita'
- L'API Jadro e' su porta custom (`5980`) e protocollo HTTP (non HTTPS)
- La sanitizzazione email per l'API Jadro **rimuove il TLD** dal dominio (es. `user@gmail` invece di `user@gmail.com`) - sembra un workaround per un bug dell'API esterna
- Il `values.yaml` ha un campo `infra_repo_name: amatori-infra` (repo infrastruttura separata)
- Il ruolo custom aggiunto e' solo `MANAGER` (oltre ai template roles)
- Supporto PWA abilitato (`next-pwa` nelle dipendenze)
- Supporto LaTeX nel chat (katex + rehype-katex) - insolito per un'app di prenotazioni marittime
