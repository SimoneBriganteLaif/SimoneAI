# Catalogo Integrazioni Esterne

> Data analisi: 2026-03-21

## 1. OpenAI

| Repo | Modelli | Feature |
|---|---|---|
| advaisor | GPT-4.1, GPT-4.1-mini, GPT-4.1-nano | Chat RAG streaming, tag detection, document comparison |
| argo | GPT-4.1-mini (Agents SDK) | Chatbot multi-tool, prenotazioni Jadrolinija |
| arianna | GPT-5.4, GPT-5.4-mini, GPT-5-nano | Chat RAG multi-source, web search, operator chat, service scraping |
| bandi-platform | GPT-5-nano, GPT-5-mini | Crawling + estrazione bandi, classificazione fatture, YOLO PDF |
| bonfiglioli-riduttori | GPT-5.4, GPT-5-nano | Chat RAG manuali tecnici |
| cae-genai | GPT-4.1, GPT-4.1-mini, GPT-5 | Chat RAG streaming, document upload |
| competitive-retail | GPT-4o, GPT-4o-mini, Whisper | Trascrizione interviste, analisi insight, web research |
| credit-assistant | GPT-5-mini | Classificazione email, generazione risposte, RAG knowledge base |
| experior | GPT-5.4 | Completamento perizie assicurative, estrazione titoletti da PDF |
| formart-marche | OpenAI (non specificato) | Generazione risposte formulari bandi, Vector Store per progetto |
| fortlan-dibi | GPT-5-nano | Classificazione documenti, estrazione dati (scadenza, prodotto) |
| helia | GPT-5-mini | AI daily digest (via OpenAI diretto) |
| manfredi | GPT-5, Whisper | Trascrizione audio, note strutturate, Vector Store RAG, agente AI custom |
| nessy | GPT-4.1, GPT-4.1-nano, GPT-5, GPT-5-mini, GPT-5-nano, o4-mini-deep-research | Chat, deep search, In a Nutshell (Map-Reduce), tag detection |
| phoenix-assistant | GPT-5-nano, GPT-5-mini (via OpenRouter) | Generazione titoli, chat (via OpenRouter) |
| searchbridge | GPT-5, GPT-5-mini (via OpenRouter) | KPI analysis, competitive tracking, geo audit, azioni AI |
| sireco | GPT-4o, GPT-4o-mini | Analisi documenti (visure, AIDA), summary economici |

**Totale repos con OpenAI: 17** (su 40)

## 2. Microsoft Graph / M365

| Repo | Uso |
|---|---|
| credit-assistant | Download email da shared mailbox Outlook (inbox + junk), OAuth2 con MSAL |
| jubatus | Sync email Microsoft Graph API, delta sync, invio risposte |

## 3. Google Calendar / Google API

| Repo | Uso |
|---|---|
| helia | OAuth2 Google Calendar, creazione eventi, disponibilita |
| jubatus | Gmail API (OAuth2), History API per delta sync |

## 4. Odoo (XML-RPC)

| Repo | Uso |
|---|---|
| wolico | Sync partner, fatture, ordini vendita, estratti conto, pagamenti. Lettura e scrittura. |

## 5. TeamSystem

| Repo | Uso |
|---|---|
| lamonea | API EVWSASYNC per import articoli (CodiceWS 500012), clienti/fornitori (CodiceWS 500011). 3 ditta (49, 133, 212). Import passthrough (non persistito). |

## 6. ERP Systems

| Sistema | Repo | Protocollo |
|---|---|---|
| **Diapason (IBM i / AS400)** | far-automation | ODBC con IBM i Access Driver |
| **Galileo** | preventivatore | REST API (httpx AsyncClient) |
| **Gamma (MSSQL)** | scheduler-roloplast, retropricing | pymssql |
| **Nicim (Oracle)** | scheduler-roloplast, retropricing | oracledb |
| **MasterFactory (SQL Server)** | far-automation | pymssql |
| **AX Reporting (MSSQL)** | prima-power | pymssql |
| **Dynamics DWH (MSSQL)** | prima-power | pymssql |
| **PST (Prima Service Tool)** | prima-power | pymssql (lettura + scrittura) |
| **PowerMES (MSSQL)** | scheduler-roloplast | pymssql |
| **Zucchetti HR** | studio-perri | SOAP/WSDL via zeep |

## 7. CRM Systems

| CRM | Repo | Protocollo |
|---|---|---|
| **VTE CRM** | bandi-platform | REST API, Basic Auth |
| **Creatio** | bandi-platform | OData + OAuth |
| **HubSpot** | helia | OAuth2 |
| **Salesforce** | helia | OAuth2 |
| **Zendesk** | helia | API |
| **Zoho Desk** | helia | OAuth2 |
| **Freshdesk** | helia | OAuth2 |
| **Intercom** | helia | OAuth2 |
| **Jira Service Management** | helia | OAuth2 |
| **Deepser** | helia | API |

## 8. AWS Services (oltre standard S3/SSM)

| Servizio | Repos |
|---|---|
| **ECS (task ETL/compute)** | andriani-sequencing, coci, bandi-platform, far-automation, prima-power, scheduler-roloplast, sabart-demfor, umbra-recommend, nespak |
| **ASG (autoscaling)** | andriani-sequencing, scheduler-roloplast, umbra-recommend |
| **Cognito** | crif (auth utenti + client credentials per lambda) |
| **Lambda** | crif (pipeline documenti 5 step) |
| **Secrets Manager** | crif, prima-power, scheduler-roloplast, coci |
| **Bedrock KB** | phoenix-assistant (Knowledge Base, embeddings Titan v2) |
| **S3 Vectors** | phoenix-assistant (vector store) |
| **Cost Explorer** | wolico (costi cloud multi-org) |
| **Organizations** | wolico (lista account e OU) |
| **Budgets** | wolico (budget per account) |
| **RDS** | wolico (start/stop istanze) |

## 9. Voice / SIP / Telephony

| Servizio | Repo | Uso |
|---|---|---|
| **ElevenLabs** | helia | Voice AI core (agenti vocali, streaming, knowledge base, 885 righe di integrazione) |
| **Telnyx** | helia | SIP proxy, call control, warm/conference/refer transfer, bridge ElevenLabs-PSTN |

## 10. Altre Integrazioni Specifiche

| Servizio | Repo | Uso |
|---|---|---|
| **Jadrolinija API** | argo | Prenotazioni traghetti, porti, tratte, date |
| **Binance API** | coci | Portafoglio crypto, dati storici da data.binance.vision |
| **3Commas API** | coci | Drawdown deals (HMAC-SHA256 auth) |
| **Playtomic** | brain | ETL prenotazioni, giocatori, tornei padel |
| **Sygest API** | experior | Callback risultati perizie, autenticazione basic |
| **D&B (Dun & Bradstreet)** | competitive-retail | Dati competitor importati via CSV |
| **ISTAT** | competitive-retail | Dati redditi e demografici via CSV |
| **Nominatim (OpenStreetMap)** | competitive-retail | Geocoding indirizzi |
| **HERE Maps** | arianna | Geocoding servizi territoriali |
| **PDFRest** | advaisor, cae-genai | Conversione DOCX/PPTX in PDF |
| **WebScrapingAPI** | bandi-platform | Fallback scraping quando Playwright bloccato |
| **Jina AI** | searchbridge | Fallback rendering pagine JS-heavy |
| **OpenRouter** | phoenix-assistant, searchbridge | Proxy multi-LLM |
| **Microsoft Clarity** | arianna | Analytics utente |
| **Iubenda** | arianna | Cookie/privacy compliance |
| **Hotjar** | retropricing | Analytics UX |
| **Notion API** | helia | Landing form -> Notion database |
| **GitHub API** | wolico | Lettura file YAML da repo infra (GitHub App JWT) |
| **Wolico (cross-app)** | tutti i progetti laif-template | Ticketing centralizzato, error sync |
