# LAIF Repository Census — Indice Generale

> **Data analisi**: 2026-03-21
> **Repos analizzate**: 40
> **Template baseline**: laif-template v5.7.0

---

## Tabella Riepilogativa

| Repo | Cliente | Settore | Vers. Template | Top Contributor | Feature Chiave Custom | Integrazioni Esterne |
|---|---|---|---|---|---|---|
| advaisor | SaaS B2B | Insurtech | 4.4.6 | Marco Pinelli | Chat RAG polizze, document comparison | OpenAI, PDFRest, S3 |
| albini-castelli | Albini e Castelli | Edilizia | 5.6.0 | Marco Pinelli | Controllo gestione cantieri, materialized views, upload Excel | S3 |
| andriani-sequencing | Andriani S.p.A. | Food Manufacturing | 5.6.7 | Mattia Gualandi | OR-Tools scheduler produzione, ETL 3-layer, ECS Fargate | S3, ECS, OpenAI |
| argo | Amatori (Ancona) | Trasporto marittimo | 5.6.0 | Leonardo Carboni | Chatbot AI (Agents SDK), prenotazioni traghetti | Jadrolinija, OpenAI, SES |
| arianna | Arianna Care | Sanita / Caregiving | 5.6.0 | Roberto Zanolli | Chat RAG multi-provincia, web scraping servizi, survey | OpenAI, HERE Maps, Clarity |
| bandi-platform | Sinergia Srl | Finanza agevolata | 5.6.1 | Cristian P. | Crawler bandi (Playwright), YOLO PDF, matching AI | VTE CRM, Creatio, OpenAI, ECS |
| bonfiglioli-riduttori | Bonfiglioli | Meccanica industriale | 5.6.2 | Lorenzo T | Report analisi 3-livelli, chatbot RAG manuali | OpenAI, S3 |
| brain | SPH (Sport Padel Hub) | Sport / Padel | 5.6.0 | Angelo Longano | Gestione circoli padel (70+ tabelle), ETL Playtomic | Playtomic, S3 |
| cae-genai | CAE | GenAI | 5.3.5 | Marco Pinelli | Chat RAG streaming, knowledge base | OpenAI, PDFRest, Wolico |
| coci | Interno | Fintech / Crypto | 5.4.3 | Marco Vita | Backtesting DCA (Polars), materialized views, Binance | Binance, 3Commas, ECS |
| competitive-retail | Fiera Milano | Retail Intelligence | 5.6.0 | Alessandro Grotti | Interviste AI (Whisper), analisi geospaziale | OpenAI Whisper, Nominatim, D&B |
| creama | Creama | Condominiale | 5.4.1 | Carlo Venditti | Gestione condominiale completa, PDF bilanci | WeasyPrint, S3 |
| credit-assistant | Nivi S.p.A. | Credito autostradale | 5.6.7 | Federico Frasca | Email triage AI, classificazione automatica | MS Graph, OpenAI, S3 |
| crif | CRIF S.p.A. | Fintech / Document Mgmt | 5.2.6 | Daniele DN | Pipeline documentale 5-step via Lambda | Lambda, Cognito, S3 |
| experior | Experior | Assicurativo / Perizie | 5.4.3 | Roberto Zanolli | Completamento perizie AI, ETL MSSQL 3-layer | Sygest, OpenAI, MSSQL |
| far-automation | FAR S.r.l. | Manifatturiero | 5.7.0 | Michele Roberti | ETL Diapason (IBM i) + MasterFactory, verifica disponibilita | IBM i ODBC, MSSQL, ECS |
| formart-marche | Formart Marche | Formazione professionale | 5.3.13 | Cristian P. | Gestione bandi formativi, calendario auto, budget | OpenAI, WeasyPrint |
| fortlan-dibi | Fortlan-Dibi | Edilizia / Materiali | 5.6.0 | Luca Stendardo | Classificazione documenti AI, scraping Selenium | OpenAI, Selenium (Knauf, Ursa) |
| helia | Helia (LAIF) | AI / Voice / Customer Care | 5.6.7 | Leonardo Carboni | Voice agent AI, 8 CRM, outbound campaigns | ElevenLabs, Telnyx, Google Cal, 8 CRM |
| ids-georadar | IDS GeoRadar | Manifatturiero / Georadar | 5.6.0 | Lorenzo Monni Sau | Collaudi prodotto step-by-step, report PDF multi-brand | WeasyPrint, S3 |
| jubatus | Interno (?) | Customer Care / Eventi | standard | Michele Roberti | Email sync engine (Gmail + Microsoft), ticketing | Gmail API, MS Graph |
| lamonea | Lamonea Group | Dispositivi medici / ERP | 5.6.1 | Simone Brigante | Integrazione TeamSystem (passthrough), mockup CRM | TeamSystem |
| manfredi | Studio Manfredi | Progettazione tecnica | 5.6.4 | Michele Roberti | CRM + progetti, agente AI custom, audio trascrizione | OpenAI (Whisper, GPT-5), MapLibre |
| nespak | Nespak (Guillin) | Food Packaging | 5.6.7 | Lorenzo Monni Sau | Demand forecasting (10 modelli), ETL 3-schema | S3, ECS |
| nessy | People | Market Research / BI | 5.6.0 | Federico Frasca | Deep Search (o4-mini), In a Nutshell (Map-Reduce) | OpenAI (6 modelli), S3 |
| phoenix-assistant | Non specificato | Industriale | 5.6.7 | Tancredi Bosi | Agentic RAG (Bedrock KB), ingestion pipeline | AWS Bedrock, S3 Vectors, OpenRouter |
| preventivatore | Benozzi | Metalmeccanica | 5.4.0 | Simone Brigante | Motore calcolo costi industriali, ETL Galileo | Galileo ERP, S3 |
| prima-power | Prima Power | Machinery / After-Sales | 5.6.0 | Federico Frasca | ETL 6-step (4 DB MSSQL), pricing simulator | 4 DB MSSQL, ECS, S3 |
| ref-man | FIP | Sport / Basket | 5.6.0 | Roberto Zanolli | Algoritmo Elite (OR-Tools), ETL FOL (VPN + Protobuf) | FOL (VPN), OpenAI, S3 |
| retropricing | Tecnoform | Packaging industriale | N/A (Strapi) | Marco Pinelli | Preventivazione termoformatura, ETL bidirezionale | Gamma (MSSQL), Nicim (Oracle) |
| sabart-demfor | Sabart | Supply Chain | 5.6.1 | Matteo Scalabrini | Demand forecasting (PyTorch + CatBoost), ETL S3 | S3, ECS |
| scheduler-roloplast | Ferrari Rolo Plast | Plastica / Stampaggio | 5.6.1 | Luca Stendardo | OR-Tools scheduler, ETL 3 DB (Oracle + 2 MSSQL), magazzino | Nicim, Gamma, PowerMES, ECS |
| searchbridge | Searchbridge (SaaS) | Digital Marketing / ASO | 5.6.0 | Cristian P. | Multi-LLM analysis, knowledge graph, MCP server, geo audit | OpenRouter, OpenAI, Jina AI, pgvector |
| sebi-group | Sebi Group | Spedizioni internazionali | 5.7.0 | Carlo Venditti | Mockup inbox + quotazioni (presales) | Nessuna (pianificate: M365, Osma) |
| sireco | Sireco | Revisione contabile | 5.7.0 | Carlo Venditti | CRM revisori, analisi documenti AI, calcolo onorari | OpenAI, S3 |
| sky-agent | Sky (?) | Telecomunicazioni | 5.7.0 | - | Template vanilla, nessun custom | Nessuna |
| studio-perri | Studio Perri CdL | Consulenza del Lavoro | 5.6.7 | Mattia Gualandi | PayOps (60 tabelle), ETL Zucchetti SOAP, processi/adempimenti | Zucchetti (SOAP), S3 |
| supplynk | Supplynk S.r.l. | Horeca / Food B2B | 5.6.2 | Angelo Longano | Mockup marketplace B2B con agent AI | Nessuna (mockup) |
| umbra-recommend | Umbra Group | Odontoiatrico B2B | 5.4.0 | Simone Brigante | Raccomandazione prodotti (3 CatBoost), segmentazione RFM | FTPS, S3, ECS |
| wolico | LAIF (interno) | Software / Consulenza | 5.7.0 | Marco Vita | CRM, economics, monitoring app, ticketing hub, Odoo sync | Odoo, AWS (multi-org), GitHub |

## Feature Matrix Sintetica

| Repo | BG Tasks | ETL | AI/ML | API Esterne | File Proc. | Email | Scheduling | OR-Tools | Multi-tenant | Scraping |
|---|---|---|---|---|---|---|---|---|---|---|
| advaisor | X | | X | X | X | | | | | |
| albini-castelli | | | | | X | | | | | |
| andriani-sequencing | X | X | | | | | X | X | | |
| argo | | | X | X | | | | | | |
| arianna | | | X | X | X | | | | | X |
| bandi-platform | X | X | X | X | X | | X | | X | X |
| bonfiglioli-riduttori | | | X | | X | | | | | |
| brain | | X | | X | | | | | | |
| cae-genai | | | X | X | X | | | | | |
| coci | X | X | | X | | | | | | |
| competitive-retail | X | | X | X | | | | | | |
| creama | | | | | X | | | | | |
| credit-assistant | X | | X | X | X | X | | | | |
| crif | | X | | X | X | | | | X | |
| experior | X | X | X | X | | | X | | | |
| far-automation | X | X | | X | X | X | | | | |
| formart-marche | | | X | | X | | | | | |
| fortlan-dibi | X | | X | | X | | X | | | X |
| helia | X | | X | X | X | | | | X | |
| ids-georadar | | | | | X | | | | | |
| jubatus | X | | | X | | X | | | | |
| lamonea | | | | X | | | | | | |
| manfredi | X | | X | | X | X | | | | |
| nespak | | X | X | | X | | | | | |
| nessy | X | | X | | X | | | | | |
| phoenix-assistant | X | | X | X | X | | | | | |
| preventivatore | X | X | | X | | | X | | | |
| prima-power | | X | | X | X | | | | | |
| ref-man | X | X | X | X | X | | | X | | |
| retropricing | | X | | X | X | X | | | | |
| sabart-demfor | | X | X | | X | | | | | |
| scheduler-roloplast | X | X | | X | | | X | X | | |
| searchbridge | X | | X | X | | | X | | X | X |
| sebi-group | | | | | | | | | | |
| sireco | X | | X | | X | | | | | |
| sky-agent | | | | | | | | | | |
| studio-perri | X | X | | X | X | | | | | |
| supplynk | | | | | | | | | | |
| umbra-recommend | | X | X | X | X | | X | | | |
| wolico | X | X | | X | X | X | | | | |

## Statistiche Aggregate

| Metrica | Valore |
|---|---|
| **Repos totali analizzate** | 40 |
| **Repos basate su laif-template** | 39 (97.5%) |
| **Repos con stack non-template** | 1 (retropricing — Strapi v3) |
| **Repos template vanilla (zero custom)** | 1 (sky-agent) |
| **Repos solo mockup (zero backend)** | 3 (sebi-group, supplynk, lamonea) |
| **Integrazioni OpenAI** | 17 repos |
| **Integrazioni ERP/DB esterni** | 12 repos |
| **Pipeline ETL** | 24 repos |
| **OR-Tools solver** | 3 repos |
| **ML/Forecasting** | 4 repos |
| **Voice AI** | 1 repo (helia) |
| **Tabelle custom totali stimate** | ~750+ |
| **Integrazioni esterne uniche** | ~45 servizi diversi |
| **Versione template piu vecchia** | 5.2.6 (crif) |
| **Versione template piu recente** | 5.7.0 (5 repos) |
| **Repos con >50 tabelle custom** | 3 (brain ~70, studio-perri ~60, prima-power ~50) |
| **Settori industriali coperti** | 25+ |
| **Contributori unici stimati** | ~45 persone |

## Link Cross-Analysis

| Documento | Descrizione |
|---|---|
| [pattern-matrix.md](cross-analysis/pattern-matrix.md) | Mappa pattern tecnici per repository |
| [integration-catalog.md](cross-analysis/integration-catalog.md) | Catalogo completo integrazioni esterne |
| [feature-matrix.md](cross-analysis/feature-matrix.md) | Categorizzazione funzionale dettagliata |
| [template-drift.md](cross-analysis/template-drift.md) | Analisi scostamento dal template 5.7.0 |
| [team-map.md](cross-analysis/team-map.md) | Mappa persone, competenze, cross-pollination |
| [raccomandazioni.md](cross-analysis/raccomandazioni.md) | Raccomandazioni concrete (archivio, aggiornamenti, sicurezza, standardizzazione) |

## Link Analisi Singole

Tutte le 40 analisi dettagliate sono in [repos/](repos/):

advaisor, albini-castelli, andriani-sequencing, argo, arianna, bandi-platform, bonfiglioli-riduttori, brain, cae-genai, coci, competitive-retail, creama, credit-assistant, crif, experior, far-automation, formart-marche, fortlan-dibi, helia, ids-georadar, jubatus, lamonea, manfredi, nespak, nessy, phoenix-assistant, preventivatore, prima-power, ref-man, retropricing, sabart-demfor, scheduler-roloplast, searchbridge, sebi-group, sireco, sky-agent, studio-perri, supplynk, umbra-recommend, wolico.

## Baseline Template

La baseline del template v5.7.0 e documentata in [laif-template-baseline.md](laif-template-baseline.md).
