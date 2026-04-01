# Pattern Matrix — Pattern Tecnici per Repository

> Data analisi: 2026-03-21

## Legenda
- **X** = presente e usato attivamente
- **D** = dipendenza presente ma non usata attivamente
- **(C)** = commentato/disabilitato

## Matrice Pattern

| Pattern | Repos |
|---|---|
| **ETL multi-layer (STG/TRN/PRS)** | andriani-sequencing, far-automation, nespak, prima-power, scheduler-roloplast, sabart-demfor, experior, umbra-recommend |
| **OR-Tools CP-SAT Solver** | andriani-sequencing, scheduler-roloplast, ref-man |
| **Materialized Views** | albini-castelli, coci, sabart-demfor, searchbridge (overview) |
| **Background tasks / repeat_every** | credit-assistant, fortlan-dibi, scheduler-roloplast, helia, wolico, coci, nessy, brain, far-automation, studio-perri, umbra-recommend |
| **RAG con OpenAI (Vector Store)** | advaisor, argo, arianna, bonfiglioli-riduttori, cae-genai, formart-marche, manfredi, nessy, searchbridge, fortlan-dibi, credit-assistant |
| **RAG con AWS Bedrock** | phoenix-assistant |
| **FTPS/SFTP integration** | umbra-recommend |
| **Strategy pattern** | jubatus (email provider Gmail/Microsoft), far-automation (disponibilita per famiglia prodotto) |
| **Web scraping (Selenium)** | fortlan-dibi (Knauf, Ursa) |
| **Web scraping (Playwright)** | bandi-platform |
| **Web scraping (BeautifulSoup)** | arianna |
| **Web crawler (httpx/lxml)** | searchbridge (geo audit) |
| **PDF generation (WeasyPrint)** | albini-castelli (implico), creama, far-automation, formart-marche, ids-georadar, manfredi |
| **PDF generation (react-pdf)** | brain, scheduler-roloplast, studio-perri, bandi-platform |
| **PDF generation (html-pdf/EJS)** | retropricing |
| **Excel import/export** | albini-castelli, andriani-sequencing, far-automation, nespak, prima-power, preventivatore, competitive-retail, credit-assistant, studio-perri, umbra-recommend, wolico, sabart-demfor |
| **Multi-schema PostgreSQL** | andriani-sequencing (stg/prs), far-automation (stg/prs), nespak (stg/prs/anls), prima-power (lnd/stg/trn/prs/static), scheduler-roloplast (stg/trn/mdl/prs), sabart-demfor (stg/prs), experior (lnd/stg/prs), umbra-recommend (stg/trn/infer/prs), preventivatore (stg/prs), crif (prs + multi-tenant) |
| **column_property denormalization** | bandi-platform, formart-marche, fortlan-dibi, ref-man, scheduler-roloplast, studio-perri, wolico, ids-georadar, arianna, searchbridge |
| **MCP Server** | searchbridge |
| **OpenAI Agents SDK** | argo |
| **OpenAI Structured Output** | credit-assistant, experior, nessy, bandi-platform, searchbridge |
| **OpenAI Whisper (trascrizione)** | competitive-retail, manfredi |
| **Protobuf** | ref-man |
| **ECS Fargate tasks** | andriani-sequencing, coci, bandi-platform, far-automation, prima-power, scheduler-roloplast, sabart-demfor, umbra-recommend |
| **APScheduler** | bandi-platform, searchbridge |
| **Polars (non Pandas)** | coci |
| **Multi-tenant DB separati** | crif (3 database) |
| **CatBoost ML** | sabart-demfor, umbra-recommend |
| **PyTorch Neural Networks** | sabart-demfor (AHead framework) |
| **YOLO Computer Vision** | bandi-platform (FFDNet per PDF field detection) |
| **SOAP/WSDL integration** | studio-perri (Zucchetti) |
| **Knowledge Graph** | searchbridge |
| **pgvector embedding** | bandi-platform, searchbridge, arianna |
| **Subscription/Billing system** | helia (minuti), searchbridge (piani SaaS) |
| **OpenRouter (multi-LLM proxy)** | phoenix-assistant, searchbridge |
| **ElevenLabs Voice AI** | helia |
| **Telnyx SIP telephony** | helia |
| **CRM integrations (multi-provider)** | helia (8 provider CRM: HubSpot, Salesforce, Zendesk, Zoho, Freshdesk, Intercom, Jira, Deepser) |
| **Google Calendar OAuth** | helia, jubatus |
| **Microsoft Graph API** | credit-assistant, jubatus |
| **Binance API** | coci |
| **Odoo XML-RPC** | wolico |
| **VPN containerizzata** | ref-man (FOL) |
| **DB esterni MSSQL** | far-automation (Diapason), prima-power (AX/Dynamics/PST), scheduler-roloplast (Gamma/PowerMES), retropricing (Gamma), experior (Sygest) |
| **DB esterni Oracle** | scheduler-roloplast (Nicim), retropricing (Nicim), helia (DB consulting) |
| **DB esterni IBM i (AS400/ODBC)** | far-automation (Diapason) |
| **Versioning anagrafiche (snapshot)** | formart-marche (Companies/Participants/Staff versions) |
| **Dual data model con migrazione** | preventivatore (legacy -> AllArticle) |
| **Assembly/BOM ricorsivo** | preventivatore (quotation-quotation), scheduler-roloplast (networkx per BOM) |
| **Geolocalizzazione/mappe** | arianna (MapLibre + HERE Maps), competitive-retail (Leaflet + Nominatim), manfredi (MapLibre), brain (coordinate club) |
| **PWA (Progressive Web App)** | argo, arianna, bonfiglioli-riduttori, helia, manfredi, nessy, wolico |
| **Mockup-first development** | sebi-group, supplynk, lamonea |
| **Email provider multi-provider** | jubatus (Gmail + Microsoft), credit-assistant (Microsoft Graph) |
| **Encrypted credentials (Fernet)** | jubatus, helia |
