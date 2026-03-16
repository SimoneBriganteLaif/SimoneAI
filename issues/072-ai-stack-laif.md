# AI Stack LAIF

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 72                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | —                  |

## Descrizione originale

> Iniziare a strutturare l'AI Stack di Laif

## Piano di risoluzione

1. **Valutare l'utilizzo AI attuale nei progetti LAIF**
   - Mappare dove l'AI è già usata: Helia (assistente conversazionale), feature di agenti
   - Identificare i pattern comuni: chiamate LLM, embedding, ricerca semantica
   - Documentare i limiti dell'approccio attuale (se presente)

2. **Scegliere i provider LLM**
   - Valutare AWS Bedrock (già nell'infrastruttura LAIF) vs OpenAI vs Anthropic
   - Criteri: costi, latenza, qualità output, compliance dati (GDPR), supporto streaming
   - Considerare una strategia multi-provider per resilienza e ottimizzazione costi
   - Definire quale modello per quale use case (es. Claude per reasoning, GPT per generazione)

3. **Definire un layer di astrazione per le chiamate LLM**
   - Creare un modulo `ai/` nel template con interfaccia unificata
   - Supporto per: completion, chat, embedding, function calling
   - Configurazione provider via variabile d'ambiente (`AI_PROVIDER=bedrock|openai|anthropic`)
   - Retry, timeout, fallback su provider alternativo
   - Logging delle chiamate: prompt, tokens usati, latenza, costo stimato

4. **Definire la pipeline RAG standard**
   - Scelta vector DB: pgvector (già in PostgreSQL) vs servizio dedicato (OpenSearch, Pinecone)
   - Strategia di chunking dei documenti (dimensione, overlap, metadata)
   - Pipeline di indicizzazione: upload → chunk → embed → store
   - Pipeline di retrieval: query → embed → search → rerank → context
   - Aggiungere al template come modulo opzionale attivabile per progetto

5. **Sistema di gestione prompt**
   - Prompt versionati e configurabili (non hardcoded nel codice)
   - Storage: file YAML/JSON o tabella DB con versionamento
   - Supporto per template con variabili (`{user_name}`, `{context}`)
   - A/B testing di prompt diversi con tracking dei risultati

6. **Aggiungere utility AI al template**
   - Streaming delle risposte LLM via SSE (Server-Sent Events) al frontend
   - Conteggio token (pre-invio per rispettare i limiti del modello)
   - Rate limiting per utente sulle chiamate AI
   - Componente frontend per chat/conversazione riutilizzabile

7. **Coordinare con Laif Agent (issue #163)**
   - Verificare lo stato della issue #163 e le decisioni già prese
   - L'AI Stack deve supportare i casi d'uso dell'agent
   - Definire i confini: lo stack fornisce le primitive, l'agent le orchestra

## Note

Questa issue è strategica e trasversale. Si consiglia di procedere in modo incrementale: partire dal layer di astrazione LLM (step 3) e dalla pipeline RAG base (step 4), poi iterare.

## Stima effort

- Analisi utilizzo attuale: ~2h
- Valutazione provider e decisione: ~4h
- Layer astrazione LLM: ~8h
- Pipeline RAG standard: ~12h
- Sistema gestione prompt: ~6h
- Utility AI nel template: ~8h
- Documentazione e integrazione: ~4h
- **Totale: ~44h** (stima iniziale, da raffinare per fase)
