# Laif Agent

| Campo | Valore |
|---|---|
| **ID** | 163 |
| **Stack** | laif-template |
| **Tipo** | Roadmap |
| **Status** | Nuova |
| **Target** | 23 Febbraio - 15 Aprile 2026 |

## Descrizione originale

Laif Agent — integrazione di un agente AI all'interno del template.

## Piano di risoluzione

1. **Definire l'architettura dell'agente** — progettare un'astrazione sul provider LLM che permetta di switchare tra provider (AWS Bedrock, OpenAI, Anthropic) senza modificare il codice applicativo. Definire le interfacce: `AgentProvider`, `AgentMessage`, `AgentTool`, `AgentConfig`.
2. **Backend: servizio agente con supporto streaming** — implementare un servizio FastAPI con:
   - Endpoint SSE (Server-Sent Events) per risposte in streaming.
   - Gestione della conversazione (history, context window).
   - Rate limiting e gestione costi.
   - Logging delle interazioni per debug e analisi.
3. **Frontend: componente chat UI** — sviluppare il componente di chat:
   - Coordinare con laif-ds issue 88 per il design del componente.
   - Supporto markdown nel rendering delle risposte.
   - Indicatore di streaming/typing.
   - History della conversazione con persistenza.
4. **Integrazione pipeline RAG** — implementare Retrieval-Augmented Generation:
   - Ingestion dei documenti (PDF, testo, pagine web).
   - Vector store (pgvector su PostgreSQL o servizio esterno).
   - Retrieval con ranking e context injection nel prompt.
5. **Supporto tool/function calling** — permettere all'agente di invocare funzioni definite dall'applicazione:
   - Registry dei tool disponibili.
   - Validazione input/output dei tool.
   - Gestione del loop agent → tool → agent.
6. **Sistema di configurazione dell'agente** — rendere l'agente configurabile per progetto:
   - System prompt personalizzabile.
   - Tool disponibili selezionabili.
   - Parametri LLM (temperatura, max tokens, modello).
   - Feature flag per abilitare/disabilitare l'agente (correlato a issue 141).
7. **AWS Bedrock come provider primario** — implementare l'integrazione con Bedrock:
   - Supporto modelli Claude (Anthropic via Bedrock).
   - Gestione credenziali AWS (IAM role, credentials chain).
   - Bedrock Knowledge Base per RAG managed (opzionale).
8. **Testing e documentazione** — test unitari per il servizio, test di integrazione per lo streaming, documentazione per l'integrazione nei progetti.

### Issue correlate

- Issue 72 — AI Stack (definizione dello stack AI del template)
- Issue 52 — MCP per produttività (MCP server per sviluppatori)
- Issue 88 (laif-ds) — Componente chat UI

## Stima effort

**Alto (40-60h)** — è una feature complessa e trasversale. Consigliato approccio incrementale:
- Fase 1 (16h): architettura + servizio backend con streaming + UI base.
- Fase 2 (16h): RAG pipeline + tool calling.
- Fase 3 (8h): configurazione avanzata + Bedrock integration.
- Fase 4 (8h): testing, documentazione, polish.
