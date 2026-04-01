# Phoenix Assistant — Analisi Repository

## 1. Overview

**Cosa fa**: Assistente conversazionale AI con RAG (Retrieval-Augmented Generation) basato su AWS Bedrock Knowledge Base. L'utente carica documenti, li classifica per dipartimento/processo/macchina/applicazione, e poi interroga l'assistente AI che recupera informazioni dalla knowledge base per generare risposte contestuali con citazioni.

**Cliente**: Non specificato nel codice (nome generico "Phoenix-Genai")
**Settore**: Industriale/manifatturiero (entita: macchine, famiglie macchine, processi, applicazioni, dipartimenti)
**Stato**: Attivo, v1.1.4
**Repository**: phoenix-assistant

## 2. Versioni

| Componente | Versione |
|---|---|
| App | 1.1.4 |
| laif-template | 5.6.7 |

## 3. Team

| Contributore | Commit |
|---|---|
| Pinnuz | 263 |
| mlife | 193 |
| github-actions[bot] | 112 |
| Simone Brigante | 92 |
| bitbucket-pipelines | 86 |
| Marco Pinelli | 85 |
| neghilowio | 65 |
| cavenditti-laif | 49 |
| sadamicis | 49 |
| Carlo A. Venditti | 31 |
| Daniele DN | 28 |
| lorenzoTonetta | 23 |
| Matteo Scalabrini | 21 |
| tancredibosi | 21 |
| SimoneBriganteLaif | 20 |
| mlaif | 19 |
| TancrediBosi | 18 |
| angelolongano | 18 |
| Marco Vita | 17 |
| Daniele DalleN | 14 |
| + altri minori | ~50 |

## 4. Modello dati CUSTOM

Tutte le tabelle sono nello schema `prs`. Il modello e fortemente orientato alla gestione di una knowledge base documentale con classificazione multi-dimensionale.

```mermaid
erDiagram
    LlmModel {
        int id PK
        string des_name
        string cod_model
        string des_provider
        bool flg_active
        bool flg_default
        int id_business FK
    }

    RetrievalConfig {
        int id PK
        int id_business FK
        int val_max_results
        float val_min_score_threshold
    }

    SystemPrompt {
        int id PK
        string des_name
        string des_prompt
        bool flg_active
        int id_business FK
    }

    Conversation {
        int id PK
        string des_name
        int id_user FK
        int id_department FK
        int id_process FK
        int id_machine_family FK
        int id_application FK
        int id_system_prompt FK
        int id_model FK
    }

    Thread {
        int id PK
        enum des_sender
        string des_message
        int id_conversation FK
        string id_response
        int id_user FK
        json citations
    }

    ThreadAttachment {
        int id PK
        int id_thread FK
        string des_filename
        string des_s3_key
        string des_content_type
        int num_file_size
    }

    Feedback {
        int id PK
        int id_thread FK
        int id_user FK
        bool flg_positive
        enum des_status
        string des_question
        string des_answer
        string des_solution
        bool issue_resolved
        int response_accuracy
    }

    Document {
        int id PK
        string des_name
        int id_user FK
        enum des_status
        bool flg_chat
        bool flg_all_departments
        bool flg_all_processes
        bool flg_all_machine_families
        bool flg_all_applications
        string des_s3_key
        int id_data_source FK
        bool flg_knowledge_available
    }

    Department {
        int id PK
        string des_name
        string des_description
    }

    Process {
        int id PK
        string des_name
        string des_description
    }

    MachineFamily {
        int id PK
        string des_name
        string des_description
    }

    Machine {
        int id PK
        string des_code
        int id_machine_family FK
    }

    Application {
        int id PK
        string des_name
        string des_description
    }

    VectorBucket {
        int id PK
        string des_name
        string des_arn
        int id_business FK
    }

    VectorIndex {
        int id PK
        string des_name
        string des_arn
        int id_vector_bucket FK
    }

    KnowledgeBase {
        int id PK
        string des_name
        string cod_knowledge_base_id
        string des_role_arn
        int id_vector_index FK
        enum cod_status
    }

    DataSource {
        int id PK
        string des_name
        string cod_data_source_id
        int id_knowledge_base FK
        string des_bucket_name
        string des_bucket_prefix
        enum cod_status
        enum cod_type
        bool flg_ingestion_pending
    }

    IngestionJob {
        int id PK
        string cod_job_id
        int id_data_source FK
        enum cod_status
        int val_documents_scanned
        int val_documents_indexed
        int val_documents_failed
        datetime tms_started
        datetime tms_completed
    }

    Conversation ||--o{ Thread : has
    Thread ||--o{ ThreadAttachment : has
    Thread ||--o| Feedback : has
    Conversation }o--|| Department : "filtro"
    Conversation }o--|| Process : "filtro"
    Conversation }o--|| MachineFamily : "filtro"
    Conversation }o--|| Application : "filtro"
    Conversation }o--|| SystemPrompt : uses
    Conversation }o--|| LlmModel : uses
    Document }o--o{ Department : "M2M"
    Document }o--o{ Process : "M2M"
    Document }o--o{ MachineFamily : "M2M"
    Document }o--o{ Application : "M2M"
    Document }o--|| DataSource : belongs_to
    MachineFamily ||--o{ Machine : has
    VectorBucket ||--o{ VectorIndex : has
    VectorIndex ||--o{ KnowledgeBase : has
    KnowledgeBase ||--o{ DataSource : has
    DataSource ||--o{ IngestionJob : has
    DataSource ||--o{ Document : has
```

**Tabelle associative M2M**: `document_departments`, `document_processes`, `document_machine_families`, `document_applications`, `business_knowledge_bases`

## 5. API Routes CUSTOM

| Prefisso | Descrizione |
|---|---|
| `/app_conversations` | Chat conversazionale con streaming SSE |
| `/app_documents` | Upload/gestione documenti con presigned URL S3 |
| `/app_feedbacks` | Feedback utenti sulle risposte AI |
| `/knowledge-bases` | CRUD Knowledge Base Bedrock |
| `/vector-buckets` | Gestione S3 Vector Buckets |
| `/vector-indexes` | Gestione Vector Indexes |
| `/data-sources` | Gestione Data Sources Bedrock |
| `/ingestion-jobs` | Monitoraggio job di indicizzazione |
| `/departments` | Anagrafica dipartimenti |
| `/processes` | Anagrafica processi |
| `/machines` | Anagrafica macchine |
| `/machine_families` | Anagrafica famiglie macchine |
| `/applications` | Anagrafica applicazioni |
| `/system-prompts` | Gestione system prompt per business |
| `/llm-models` | Configurazione modelli LLM per business |
| `/retrieval-configs` | Configurazione parametri di retrieval |
| `/changelog` | Changelog applicativo |

## 6. Business Logic CUSTOM

### RAG Orchestrator (Agentic Tool-Call Pattern)
Componente centrale che coordina il pipeline RAG:
- L'LLM riceve un tool `search_knowledge_base` e decide autonomamente quando e quante volte interrogare la KB (max 3 round)
- Supporto multimodale: immagini estratte dai chunk, PDF e immagini allegati dall'utente
- Citazioni con riferimento ai documenti sorgente e pagine
- Streaming SSE con status updates (generating_title, processing_attachments, retrieving_context, preparing_response)

### Ingestion Pipeline (Background)
- Upload documenti su S3 con metadati Bedrock
- Job di indicizzazione con polling asincrono (background task o thread daemon)
- Sistema di chaining: se arriva una richiesta durante un job attivo, viene flaggata come pending e concatenata automaticamente
- Riconciliazione periodica ogni 180 secondi per recuperare job orfani/bloccati
- Riconciliazione `flg_knowledge_available` tramite confronto con documenti indicizzati su Bedrock

### Filtri dimensionali
I documenti sono classificati su 4 dimensioni (dipartimento, processo, famiglia macchine, applicazione) con flag `flg_all_*` per applicabilita globale. La conversazione filtra i documenti recuperati dalla KB in base alle dimensioni selezionate.

### Generazione titolo conversazione
Usa GPT-5-nano per generare automaticamente un titolo di max 30 caratteri dalla prima domanda.

## 7. Integrazioni esterne

| Servizio | Utilizzo |
|---|---|
| **AWS Bedrock** | Knowledge Base: creazione KB, data source, ingestion, retrieve. Embedding con Titan Embed Text v2 |
| **AWS S3** | Storage documenti, metadati (.metadata.json), allegati chat. Presigned URL per upload/download |
| **AWS S3 Vectors** | Vector store per embeddings (alternativa a OpenSearch) |
| **AWS IAM** | Creazione automatica ruoli e policy per KB Bedrock |
| **OpenRouter** | Proxy LLM per streaming risposte (OpenAI Responses API). Default: `openai/gpt-5-mini`. Web search nativa |
| **OpenAI (via OpenRouter)** | Embeddings (`text-embedding-3-small`), generazione titoli (`gpt-5-nano`) |

## 8. Pagine frontend CUSTOM

| Pagina | Descrizione |
|---|---|
| `/assistant/` | Chat AI principale (home page default, tema dark) |
| `/assistant-config/` | Configurazione assistente (system prompt, modello LLM, retrieval config) |
| `/documents/` | Gestione documenti con upload e classificazione |
| `/feedbacks/` | Dashboard feedback utenti sulle risposte AI |
| `/knowledge-base/*` | Monitoring KB con 5 tab: vector buckets, vector indexes, knowledge bases, data sources, ingestion jobs |
| `/entity-management/*` | Gestione anagrafiche con 5 tab: dipartimenti, processi, macchine, famiglie macchine, applicazioni |

## 9. Deviazioni dallo stack

| Aspetto | Standard template | Questo progetto |
|---|---|---|
| LLM Provider | OpenAI diretto | **OpenRouter** come proxy (supporto multi-modello) |
| Vector Store | Non presente | **AWS S3 Vectors** (non OpenSearch/Pinecone) |
| Knowledge Base | Chat AI semplice del template | **AWS Bedrock Knowledge Base** completa |
| Background tasks | Template base | **Polling ingestion con chaining** + riconciliazione periodica (`repeat_every`) |
| Streaming | Non presente | **SSE con status pipeline** e agentic tool-call loop |
| Ruolo custom | - | `manager` (oltre ai template roles) |

**Dipendenze aggiuntive rispetto al template**:
- `boto3` (AWS SDK, piu pesante del solito con bedrock, s3vectors, iam, bedrock-agent, bedrock-agent-runtime)
- `openai` (via OpenRouter)
- `pgvector` (presente nelle deps ma non usato attivamente - rimpiazzato da S3 Vectors)
- `pymupdf` (estrazione PDF)
- `python-docx` (documenti Word)
- `xlsxwriter` + `pandas` (export Excel)

## 10. Pattern notevoli

- **Agentic RAG**: l'LLM decide autonomamente quando cercare nella KB tramite tool calling, non e un semplice retrieve-then-generate
- **Ingestion chaining con SELECT FOR UPDATE**: previene race condition su job concorrenti, garantisce che ogni modifica venga indicizzata
- **Riconciliazione periodica**: task ogni 3 minuti che recupera job orfani (crashed poller) e flag pending dimenticati
- **Metadata Bedrock**: sistema sofisticato di metadati `.metadata.json` con tipi nativi (STRING_LIST, BOOLEAN) per filtraggio dimensionale
- **Multi-tenant KB**: una KB puo essere associata a piu business tramite tabella `business_knowledge_bases` con flag attivazione
- **Presigned URL pattern**: sia per upload documenti (PUT) che per download allegati chat e immagini KB (GET)

## 11. Tech debt e note

- **`pgvector` nelle dipendenze ma non usato**: la migrazione a S3 Vectors ha reso pgvector superfluo, ma resta come dipendenza
- **`blocking_function` di esempio in events.py**: codice di test lasciato nel modulo eventi (commentato ma presente)
- **CHANGELOG non aggiornato**: fermo a "0.1 2026-01-02 - First release", nonostante la app sia a v1.1.4
- **`time.sleep(15)` in BedrockProvider**: attesa fissa per propagazione IAM, potrebbe essere ottimizzata con retry/backoff
- **Async/sync mixing**: `RAGOrchestrator.run_stream()` crea un nuovo event loop (`asyncio.new_event_loop()`) per bridgare async->sync, pattern fragile
- **`_pending_document_uploads` in-memory dict**: nel service documenti c'e un dict globale per tracking upload pendenti che non sopravvive a restart
