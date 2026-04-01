# Arianna Care - Analisi Completa Repository

## 1. Overview

**Arianna Care** e' una piattaforma di assistenza sanitaria/sociale basata su AI, rivolta a **persone fragili** (pazienti/assistiti), **caregiver** e **operatori** del settore sanitario. Il cuore del sistema e' un chatbot AI ("Arianna") alimentato da OpenAI, che fornisce informazioni personalizzate su servizi sanitari, diritti, procedure e risorse disponibili sul territorio.

- **Cliente**: Arianna Care (progetto dedicato, non e' chiaro se il cliente finale sia una ASL, una cooperativa o un ente pubblico)
- **Industria**: Sanita' / Assistenza sociale / Caregiving
- **Cod. Applicazione**: 2025024
- **Repo name**: `arianna`
- **App name**: `ariannacare`

### Funzionalita' principali
- **Chatbot AI** con RAG (Retrieval-Augmented Generation): ricerca documenti da vector store OpenAI + web search con restrizioni di dominio
- **Chat operatore**: gli operatori possono chattare "per conto" di una persona assistita, usando il contesto della persona
- **Gestione persone**: registro anagrafico con ruoli (assistito, caregiver, operatore), relazioni caregiver-assistito
- **Gestione servizi territoriali**: catalogo servizi locali con geolocalizzazione, web scraping + generazione descrizioni AI
- **Knowledge base**: upload documenti per provincia, vector store OpenAI per ogni provincia
- **Survey system**: questionari di soddisfazione per caregiver e operatori con dashboard analytics
- **Risorse pubbliche**: news, video, documenti, glossario - tutto taggabile e filtrabile per regione
- **Sistema inviti**: operatori invitano caregiver/assistiti via email
- **Profiling utente**: onboarding che raccoglie condizione, provincia, genere
- **Prompt management**: gestione dinamica dei system prompt, summary prompt e operator prompt da DB
- **Sezione pubblica**: landing page, chi siamo, come funziona, contatti, privacy policy, risorse utili

## 2. Versioni

| Elemento | Versione |
|---|---|
| **App version** | `1.3.25` |
| **Laif Template** | `5.6.0` |
| **values.yaml version** | `1.1.0` |

## 3. Team (Contributors)

| Contributor | Commits |
|---|---|
| Pinnuz | 211 |
| Roberto (+ Roberto Zanolli) | 203 |
| mlife | 134 |
| Simone Brigante | 106 |
| bitbucket-pipelines / github-actions | 163 |
| Marco Pinelli | 85 |
| sadamicis / SaDamicis | 51 |
| luca-stendardo / Luca Stendardo | 47 |
| Daniele DN / Daniele Dalle Nogare | 36 |
| Matteo Scalabrini | 21 |
| angelolongano | 18 |
| Marco Vita | 17 |
| Carlo A. Venditti | 24 |
| altri | ~20 |

**Team numeroso** (~15 persone hanno contribuito), progetto maturo con 166+ PR.

## 4. Stack Tecnico e Deviazioni dal Template

### Backend (Python 3.12)
**Dipendenze standard template:**
- FastAPI ~0.128.0, SQLAlchemy ~2.0.45, Alembic ~1.17.2, Pydantic ~2.12.5
- PostgreSQL (asyncpg + psycopg2-binary)
- boto3 (AWS), bcrypt/passlib/python-jose (auth)
- uvicorn, starlette, httpx, requests

**Dipendenze NON standard (specifiche Arianna):**
| Dipendenza | Uso |
|---|---|
| `beautifulsoup4 + lxml` | Web scraping per generazione automatica descrizioni servizi |
| `aiohttp` | Client HTTP async (usato insieme a httpx) |
| **`openai ~=2.14.0`** | Integrazione OpenAI API (chat, vector stores, file search) |
| **`pgvector ~=0.4.2`** | Estensione PostgreSQL per vector embeddings |
| `PyMuPDF ~=1.26.7` | Parsing PDF |
| `python-docx ~=1.2.0` | Parsing DOCX |
| `xlsxwriter + pandas` | Generazione report XLSX |

### Frontend (Node >= 24)
**Dipendenze standard template:**
- Next.js 16.1.1, React 19.2.3, TypeScript 5.9.3
- Redux Toolkit, TanStack Query, Tailwind CSS 4.1.18
- laif-ds 0.2.67, react-intl, react-hook-form

**Dipendenze NON standard (specifiche Arianna):**
| Dipendenza | Uso |
|---|---|
| `@amcharts/amcharts5` | Grafici per survey dashboard |
| `draft-js + plugins` | Editor rich text (mention, export HTML) |
| `react-markdown + remark-gfm + remark-math + rehype-katex` | Rendering markdown con supporto math nelle risposte chatbot |
| `react-syntax-highlighter` | Syntax highlighting nelle risposte AI |
| `katex` | Rendering formule matematiche |
| `@microsoft/fetch-event-source` | Server-Sent Events per streaming chat |
| `maplibre-gl + react-map-gl` | Mappa interattiva per servizi territoriali |
| `@hello-pangea/dnd` | Drag and drop |
| `@microsoft/clarity` | Analytics Microsoft Clarity |
| `@mep-agency/next-iubenda` | Cookie/privacy compliance (Iubenda) |
| `framer-motion` | Animazioni |
| `next-pwa` | Progressive Web App |

### Docker Compose
- Setup standard: `db` (PostgreSQL) + `backend` (FastAPI)
- Arg build notevole: `ENABLE_XLSX: 1`
- Varianti: `docker-compose.wolico.yaml` (integrazione Wolico ticketing), `docker-compose.e2e.yaml`, `docker-compose.debug.yaml`
- **Nessun servizio extra** (no Redis, no Celery, no worker separato)

### Integrazioni esterne
| Servizio | Uso |
|---|---|
| **OpenAI API** (GPT-5.4, GPT-5.4-mini, GPT-5-nano) | Chat RAG, web search, file search, generazione riassunti, scraping AI |
| **OpenAI Vector Stores** | Storage documenti per retrieval (uno per provincia + uno generale) |
| **OpenAI Files API** | Upload documenti per vector store |
| **HERE Maps API** | Geocoding servizi (chiave API da AWS Parameter Store) |
| **AWS S3** | Storage file (documenti, immagini) |
| **AWS Parameter Store** | Secrets management |
| **Microsoft Clarity** | Analytics utente frontend |
| **Iubenda** | Cookie/privacy compliance |
| **Wolico** | Ticketing system (integrazione template) |

## 5. Modello Dati Completo

### Schema `prs` (dati applicativi)

```mermaid
erDiagram
    regions {
        str cod_region PK
        str des_name UK
        bool flg_active
    }

    provinces {
        str cod_province PK
        str des_name UK
        str cod_region FK
    }

    organizations {
        int id PK
        str des_name UK
        str cod_province FK
        str des_address
        str des_email UK
        str des_website
        datetime dat_created_at
        bool flg_active
        datetime dat_updated_at
        str des_description
    }

    facilities {
        int id PK
        str des_name UK
        str cod_province FK
        str des_address
        str des_email UK
        str des_website
        datetime dat_created_at
        bool flg_active
        datetime dat_updated_at
        str des_description
    }

    conditions {
        int id PK
        str des_name UK
        str des_description
        bool flg_exclude_general_vs
    }

    people {
        int id PK
        str cod_fiscal_code UK
        int id_user FK
        str des_name
        str des_surname
        datetime dat_birth
        enum cod_gender
        str cod_province FK
        int id_condition FK
        int id_organization FK
    }

    operators {
        int id PK
        int id_person FK_UK
        int id_organization FK
    }

    assisted {
        int id PK
        int id_person FK_UK
    }

    caregivers {
        int id PK
        int id_person FK_UK
    }

    caregiver_assisted {
        int id PK
        int caregiver_id FK
        int assisted_id FK
        datetime created_at
    }

    invitations {
        int id PK
        int id_inviter_operator FK
        str email
        str role
        str status
        int invited_person_id FK
        datetime created_at
        datetime expires_at
    }

    conversations {
        int id PK
        str des_name
        bool flg_favourite
        bool flg_operator
        bool flg_welcome_chat
        datetime dat_creation
        datetime dat_updated
        int id_person FK
        int id_behalf_person FK
    }

    chat_messages {
        int id PK
        int id_conversation FK
        bool flg_user
        str id_response
        int id_person FK
        json citations
        json web_citations
        str des_message
        datetime dat_sent
    }

    chat_message_feedbacks {
        int id PK
        int id_chat_message FK
        int id_person FK
        str des_message
        bool flg_positive
        int val_rating
        str des_comment
        str id_response_openai
        datetime dat_creation
    }

    files {
        int id PK
        str des_url
        str des_name
        str id_openai
        str cod_province FK
        bool flg_general
        enum des_status
        int id_condition FK
        int id_organization FK
        datetime dat_creation
        datetime dat_expiration
    }

    file_pages {
        int id PK
        int id_file FK
        str des_text
        int page_number
    }

    vector_stores {
        int id PK
        str id_openai UK
        str cod_province FK
        bool flg_general
        datetime dat_created_at
        datetime dat_updated_at
    }

    web_sources {
        int id PK
        str des_url
        str cod_province FK
        int id_condition FK
        bool flg_general
        int id_organization FK
        datetime dat_creation
        datetime dat_expiration
    }

    services {
        int id PK
        str des_name
        str des_address
        str cod_postal_code
        str cod_province FK
        str des_website
        str des_description_md
        str id_openai_file
        datetime dat_vector_sync
        float val_latitude
        float val_longitude
        datetime dat_created_at
        bool flg_active
        datetime dat_updated_at
    }

    service_tags {
        int id PK
        str des_name UK
        str des_description
    }

    service_tag_mappings {
        int id PK
        int id_service FK
        int id_tag FK
    }

    user_assistants {
        int id PK
        str des_condition FK
        str des_facility FK
        str id_vector_store UK
    }

    profiled_users {
        int id PK
        int id_user FK
        enum type
        enum gender
        str cod_province FK
        str des_condition FK
        str des_facility FK
    }

    user_interests {
        int id PK
        str des_email UK
        str des_type
        str des_interest
        str des_message
    }

    system_prompts {
        int id PK
        str des_prompt
        str des_name
        bool flg_active
        datetime dat_creation
        datetime dat_update
        int id_user_created FK
        int id_user_updated FK
    }

    summary_prompts {
        int id PK
        str des_prompt
        str des_name
        bool flg_active
        datetime dat_creation
        datetime dat_update
        int id_user_created FK
        int id_user_updated FK
    }

    operator_prompts {
        int id PK
        str des_prompt
        str des_name
        bool flg_active
        datetime dat_creation
        datetime dat_update
        int id_user_created FK
        int id_user_updated FK
    }

    caregiver_surveys {
        int id PK
        int id_person FK
        int val_1
        str des_1
        int val_2
        str des_2
        str des_3
        int val_4_1__val_4_5
        str des_4
        int val_5_1__val_5_3
        str des_5
        int val_6
        int val_7_1__val_7_2
        str des_8
    }

    operator_surveys {
        int id PK
        int id_person FK
        int val_1__val_11_2
        str des_1__des_12
    }

    resources_video {
        int id PK
        str iframe_url
        str des_title
        str des_preview_text
        str des_description
        bool flg_active
        int val_order
    }

    resources_document {
        int id PK
        str des_url
        str des_file_name
        str des_content_type
        int val_file_size
        str des_title
        str des_preview_text
        str des_description
        bool flg_active
        int val_order
    }

    resources_news {
        int id PK
        str des_title
        str des_preview_text
        str des_description
        bool flg_active
        datetime dat_news
        int val_order
        int id_preview_image FK
    }

    resources_news_preview_image {
        int id PK
        str des_url
        str des_name
        str des_content_type
        int val_file_size
    }

    resources_glossary_item {
        int id PK
        str des_term
        str des_definition_it
    }

    resources_tag {
        int id PK
        str des_name UK
        str des_description
        str des_intl_key
    }

    regions ||--o{ provinces : "cod_region"
    provinces ||--o{ people : "cod_province"
    provinces ||--o{ services : "cod_province"
    provinces ||--o{ vector_stores : "cod_province"
    provinces ||--o{ web_sources : "cod_province"
    provinces ||--o{ files : "cod_province"
    provinces ||--o{ organizations : "cod_province"
    provinces ||--o{ facilities : "cod_province"
    conditions ||--o{ people : "id_condition"
    conditions ||--o{ files : "id_condition"
    conditions ||--o{ web_sources : "id_condition"
    organizations ||--o{ people : "id_organization"
    organizations ||--o{ operators : "id_organization"
    organizations ||--o{ files : "id_organization"
    organizations ||--o{ web_sources : "id_organization"
    people ||--o| operators : "id_person"
    people ||--o| assisted : "id_person"
    people ||--o| caregivers : "id_person"
    caregivers ||--o{ caregiver_assisted : "caregiver_id"
    assisted ||--o{ caregiver_assisted : "assisted_id"
    people ||--o{ conversations : "id_person"
    people ||--o{ chat_messages : "id_person"
    conversations ||--o{ chat_messages : "id_conversation"
    chat_messages ||--o{ chat_message_feedbacks : "id_chat_message"
    files ||--o{ file_pages : "id_file"
    services ||--o{ service_tag_mappings : "id_service"
    service_tags ||--o{ service_tag_mappings : "id_tag"
    resources_tag }o--o{ resources_video : "video_tag_mapping"
    resources_tag }o--o{ resources_document : "document_tag_mapping"
    resources_tag }o--o{ resources_news : "news_tag_mapping"
    regions }o--o{ resources_video : "video_region_mapping"
    regions }o--o{ resources_document : "document_region_mapping"
    regions }o--o{ resources_news : "news_region_mapping"
    resources_news_preview_image ||--o{ resources_news : "id_preview_image"
    operators ||--o{ invitations : "id_inviter_operator"
    people ||--o{ invitations : "invited_person_id"
```

### Schema `template` (framework)
Tabelle standard laif-template: `users`, `roles`, `permissions`, `business`, `groups`, `user_role`, `user_permission`, `user_group`, `role_permission`, `group_permission`, `user_registrations`, `notifications`, `tickets`, `ticket_messages`, `ticket_attachments`, `ticket_updates`, `faq`, `faq_sections`, `runtasks`, `api_call_traces`.

### Schema `demo` (chat template)
Tabelle chat del template: `conversations`, `threads`, `collections`, `documents`, `document_pages`, `document_sections`, `feedbacks`, `system_instructions`.

**Nota importante**: Arianna ha il proprio sistema chat (schema `prs`) **separato** da quello del template (schema `demo`). Il template chat sembra non utilizzato attivamente.

## 6. API Routes (per risorsa)

### Chat & AI
| Route | Descrizione |
|---|---|
| `POST /chat/` | Chat streaming con SSE (Server-Sent Events) |
| `GET/POST /chat/conversations/` | CRUD conversazioni |
| `POST /chat/operator/` | Chat operatore per conto di persona |
| `POST /chat/welcome-chat/` | Crea welcome chat con riassunto |
| `POST /chat/summary/` | Genera riassunto conversazione AI |
| `POST /chat-message-feedback/` | CRUD feedback messaggi |

### Gestione Persone
| Route | Descrizione |
|---|---|
| `CRUD /people/` | Registro persone (anagrafica) |
| `CRUD /operators/` | Gestione operatori |
| `CRUD /assisted/` | Gestione assistiti |
| `CRUD /caregivers/` | Gestione caregiver |
| `CRUD /caregiver-assisted/` | Relazioni caregiver-assistito |
| `CRUD /invitations/` | Sistema inviti |
| `POST /signup/` | Registrazione utente |
| `CRUD /profiling/` | Profilazione utente (legacy) |

### Configurazione
| Route | Descrizione |
|---|---|
| `CRUD /conditions/` | Condizioni sanitarie |
| `CRUD /facilities/` | Strutture (legacy) |
| `CRUD /condition-facility/` | Mapping condizione-struttura |
| `CRUD /organizations/` | Organizzazioni |
| `CRUD /user-assistants/` | Assistenti AI per utente (legacy) |
| `CRUD /regions/` | Regioni |
| `CRUD /provinces/` | Province |

### Knowledge & AI
| Route | Descrizione |
|---|---|
| `CRUD /files/` | Gestione documenti knowledge base |
| `CRUD /vector-stores/` | Gestione vector store OpenAI |
| `CRUD /web-sources/` | Fonti web per domain-restricted search |
| `CRUD /user-interests/` | Interessi utente |

### Servizi Territoriali
| Route | Descrizione |
|---|---|
| `CRUD /services/` | Catalogo servizi locali |
| `POST /services/scrape/` | Web scraping + AI per generare descrizione servizio |
| `CRUD /service-tags/` | Tag per servizi |
| `CRUD /service-tag-mappings/` | Mapping servizio-tag |

### Prompt Management
| Route | Descrizione |
|---|---|
| `CRUD /system-prompts/` | System prompt chatbot |
| `CRUD /summary-prompts/` | Prompt per riassunti |
| `CRUD /operator-prompts/` | Prompt per modalita' operatore |

### Survey
| Route | Descrizione |
|---|---|
| `CRUD /caregiver-survey/` | Questionario caregiver |
| `CRUD /operator-survey/` | Questionario operatore |

### Risorse Pubbliche
| Route | Descrizione |
|---|---|
| `CRUD /resources-video/` | Video |
| `CRUD /resources-document/` | Documenti |
| `CRUD /resources-news/` | News |
| `CRUD /resources-news-preview-image/` | Immagini preview news |
| `CRUD /resources-glossary-item/` | Glossario |
| `CRUD /resources-tag/` | Tag risorse |
| `CRUD /resources-*-tag-mapping/` | Mapping risorse-tag |
| `CRUD /resources-*-region-mapping/` | Mapping risorse-regione |

### ETL & Utility
| Route | Descrizione |
|---|---|
| `POST /etl/` | Caricamento regioni e province da CSV |
| `CRUD /changelog/` | Lettura changelog app |

## 7. Business Logic

### Chatbot AI (cuore del sistema)
Il chatbot usa **OpenAI Responses API** con streaming (SSE), implementando un sistema RAG sofisticato:

1. **Context Resolution per Persona**: ogni persona ha una provincia, condizione e organizzazione. Il sistema risolve automaticamente:
   - Vector store della provincia (documenti locali)
   - Vector store generale (documenti nazionali)
   - Web sources permesse (filtrate per provincia + condizione)
2. **System Prompt Dinamico**: costruito combinando contesto persona + prompt attivo da DB + prompt operatore (se applicabile)
3. **File Search con Citations**: i risultati del file search vengono matchati alle pagine dei documenti con 4 strategie progressive (exact match, cross-boundary, token match, substring match)
4. **Web Search con Domain Restriction**: le ricerche web sono limitate ai domini configurati per la provincia/condizione della persona
5. **Deep Reasoning**: flag per usare modello piu' potente (gpt-5.4 vs gpt-5.4-mini)
6. **Generazione Riassunti**: usa gpt-5-nano con prompt dedicato per riassumere conversazioni

### Chat Operatore
Gli operatori possono:
- Selezionare una persona dal registro e chattare "per conto" di essa
- Il contesto AI (vector stores, web sources, system prompt) viene caricato dalla persona selezionata
- Possono generare un riassunto della conversazione e inviarlo come "Welcome Chat" alla persona assistita

### Vector Store Sync (Servizi)
Quando un servizio viene creato/aggiornato con una descrizione markdown:
1. La descrizione viene formattata in un documento markdown con metadati
2. Viene caricata come file su OpenAI
3. Il file viene collegato al vector store della provincia del servizio
4. In fase di chat, il servizio sara' trovabile via file_search

### Web Scraping + AI
Per i servizi, e' possibile:
1. Fornire un URL di una pagina web
2. Il sistema scrapa il contenuto (BeautifulSoup + lxml)
3. Lo passa a GPT-5.4 con prompt specifico per generare una descrizione markdown del servizio

### ETL
Caricamento CSV di regioni e province italiane con logica upsert.

### Background Tasks
Il file `events.py` contiene un **task di esempio** commentato (`repeat_every`). Non ci sono task background attivi.

## 8. Frontend - Albero Pagine

### Pagine Pubbliche (non autenticate)
```
/                          -> Home / Landing
/landing/                  -> Landing page
/chi-siamo/                -> Chi siamo
/come-funziona/            -> Come funziona
/contatti/                 -> Contatti
/values/                   -> Valori
/become-partner/           -> Diventa partner
/login/                    -> Login
/signup/                   -> Registrazione
/useful-resources/         -> Risorse utili (pubbliche)
/useful-resources/news/    -> Dettaglio news
/privacy-policy/           -> Privacy policy
/privacy-policy/operator/  -> Privacy policy operatore
/terms-of-use/             -> Termini di utilizzo
/logout/                   -> Logout
/registration/             -> Registrazione (template)
```

### Area Autenticata - App Custom
```
/chatbot/chat/             -> Chat con Arianna (chatbot AI)
/chatbot/operator/         -> Chat operatore (per conto di persona)
/chatbot/feedbacks/        -> Gestione feedback chat
/chatbot/knowledge/        -> Knowledge base (documenti per provincia)
/chatbot/knowledge/general/ -> Documenti generali

/my-assisted/              -> I miei assistiti (vista caregiver)
/my-caregivers/            -> I miei caregiver (vista assistito)
/my-profile/               -> Profilo personale

/manage-people/people-wizard/ -> Wizard creazione persona
/manage-people/assign-assisted/ -> Assegna assistiti a caregiver
/manage-people/register/   -> Registro persone
/manage-people/register/person-detail/ -> Dettaglio persona
/manage-people/register/person-relations/ -> Relazioni persona

/create-operators/         -> Crea operatori (admin)
/operator-welcome/         -> Welcome page operatore
/operator-prompts/         -> Gestione prompt operatore

/services/                 -> Catalogo servizi locali (con mappa)
/services-tags/            -> Gestione tag servizi

/vector-stores/            -> Gestione vector store OpenAI

/system-prompts/           -> Gestione system prompt
/summary-prompts/          -> Gestione summary prompt

/profiling/                -> Onboarding profilo utente

/config/organizations/     -> Gestione organizzazioni
/config/conditions/        -> Gestione condizioni
/config/facilities/        -> Gestione strutture (legacy)
/config/assistants/        -> Gestione assistenti (legacy)

/user-survey/              -> Hub questionari
/user-survey/caregiver/    -> Questionario caregiver
/user-survey/operator/     -> Questionario operatore
/survey-dashboard/         -> Dashboard risultati survey
/survey-dashboard/comments/ -> Commenti survey

/useful-resources-auth/    -> Risorse utili (area autenticata)
/resources-admin/          -> Admin risorse (video, documenti, news, glossario, tag)
/resources-admin/documents/
/resources-admin/news/
/resources-admin/glossary/
/resources-admin/tags/

/changelog-customer/       -> Changelog cliente
/changelog-technical/      -> Changelog tecnico
```

### Area Autenticata - Template
```
/conversation/chat/        -> Chat template (non usata attivamente)
/conversation/knowledge/   -> Knowledge template
/conversation/feedback/    -> Feedback template
/conversation/analytics/   -> Analytics template
/files/                    -> File template
/help/faq/                 -> FAQ
/help/ticket/              -> Ticketing
/profile/                  -> Profilo template
/user-management/          -> Gestione utenti/ruoli/permessi/gruppi
```

## 9. Deviazioni dal Laif Template

### Deviazioni significative

1. **Sistema chat completamente custom** (schema `prs`): Arianna non usa il sistema chat del template (schema `demo`), ma ha il proprio con modello `Conversation` + `ChatMessage` diverso da `TemplateConversation` + `TemplateThread`

2. **Integrazione OpenAI avanzata**: `CustomOpenAIProvider` estende `OpenAIProvider` del template con:
   - Streaming con web search domain-restricted
   - File search con citation matching multi-strategia
   - Vector store management per provincia
   - Generazione riassunti

3. **Modello dati domain-specific molto ricco**: ~35 tabelle custom nello schema `prs` (persone, operatori, caregiver, assistiti, servizi, condizioni, province, survey, risorse)

4. **Sezione pubblica** con landing page, chi-siamo, come-funziona, contatti, values, become-partner - non tipica del template

5. **HERE Maps integration** per geocoding servizi

6. **Microsoft Clarity** per analytics

7. **Iubenda** per compliance privacy

8. **PWA support** (next-pwa)

9. **amCharts** per grafici survey dashboard (invece di soluzioni piu' leggere)

10. **Draft.js** per rich text editing (libreria legacy, Facebook l'ha deprecata)

11. **Mapping risorse per regione**: sistema di tagging e regionalizzazione di video, documenti e news con tabelle many-to-many

12. **Prompt management da DB**: 3 tipi di prompt (system, summary, operator) gestibili da interfaccia, con flag `flg_active`

## 10. Pattern Notevoli

1. **RAG multi-source con context per persona**: il sistema risolve dinamicamente vector stores e web sources in base alla provincia e condizione della persona. E' un pattern RAG sofisticato.

2. **Citation matching multi-strategia**: 4 strategie progressive per matchare le citazioni OpenAI alle pagine dei documenti caricati (exact, cross-boundary, token-based, substring).

3. **Operator-on-behalf pattern**: gli operatori possono agire per conto di una persona, caricando il suo contesto nell'AI. Genera poi "welcome chat" che la persona ritrova nella sua area.

4. **Web scraping + AI per generazione contenuti**: i servizi possono essere arricchiti automaticamente facendo scraping di una pagina web e generando una descrizione con AI.

5. **Vector Store per provincia**: ogni provincia ha il proprio vector store OpenAI. Il sistema gestisce automaticamente upload/delete di file nei vector store corretti.

6. **Column properties estensive**: uso massiccio di `column_property` e `hybrid_property` in SQLAlchemy per campi calcolati (es. `current_roles` che calcola i ruoli di una persona con subquery).

## 11. Note e Tech Debt

### TODOs nel codice
- `models.py`: "TODO: language" su `ResourcesGlossaryItem` e `ResourcesNews` - supporto multilingua non implementato
- `chat/controller.py`: "TODO this can be simplified"

### Modelli deprecati
- `UserAssistant` e `ProfiledUser`: marcati con commento "DA NON USARE" nel codice. Il sistema di profilazione originale (condizione+struttura -> vector store dedicato) e' stato sostituito dal modello `People` con vector store per provincia.

### Potenziali problemi
1. **Draft.js e' deprecato** da Facebook - potrebbe causare problemi di compatibilita' futuri
2. **Due sistemi chat coesistono**: quello del template (schema `demo`) e quello custom (schema `prs`). Confusione potenziale.
3. **httpx + requests + aiohttp**: 3 client HTTP diversi nel backend. Il TODO nel pyproject.toml lo riconosce: "TODO maybe only use one?"
4. **Background tasks non implementati**: il file events.py ha solo un esempio commentato. Nessun task periodico attivo.
5. **Changelog vuoto**: il CHANGELOG.md non e' stato mantenuto oltre la prima release.
6. **Modelli OpenAI hardcoded**: i nomi dei modelli (gpt-5.4, gpt-5.4-mini, gpt-5-nano) sono hardcoded nel codice Python, non configurabili da env/DB.
7. **Survey con naming generico**: i campi survey usano nomi come `val_1`, `val_2`, `des_3` etc. che rendono il codice poco leggibile.
8. **Nessun test per la logica chat**: la logica di streaming e citation matching e' complessa ma non sembra avere test dedicati nel backend.
