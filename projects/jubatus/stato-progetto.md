---
progetto: "jubatus"
ultimo-aggiornamento: "2026-04-10"
tags:
  - "#progetto:jubatus"
  - "#fase:dev"
---

# Stato Progetto — Jubatus

> Punto di ingresso per riprendere lo sviluppo. Ultimo aggiornamento: 2026-04-10.

---

## Stato complessivo: MVP in corso — Infra attiva

Il backend email e quasi completo (24 endpoint, sync engine, multi-provider). Il frontend ha un'interfaccia ticket ricca con 4 view modes, ma usa interamente dati mock. **Il gap principale e il collegamento frontend-backend e l'integrazione con MySQL RDS di Jubatus.**

### Infrastruttura AWS (aggiornato 2026-04-10)

**Stato**: Backend deployato e funzionante su AWS (`dev-support-be-service` steady state).

- `app_name` rinominato da "jubatus" a "support" (ADR-006)
- Stack `dev-support-stack` attivo in eu-central-1
- ECS service con 1 task running, ALB + CloudFront configurati
- DB PostgreSQL 17.6 (`dev-jubatus-db`) attivo
- Certificato SSL `support-dev.mymemories.it` in attesa validazione DNS dal cliente
- SSM Parameter Store in eu-central-1 (`/dev/support`)

**Prossimi step infra**: validazione certificato (cliente), migrazione VPC + ALB all'infra del cliente, restrizione policy IAM. Dettagli in [infra-setup-log.md](infra-setup-log.md) e nella [pagina Notion di review](https://www.notion.so/laifgroup/Review-Infra-Jubatus-33c90ad6ee4880dabadfff781010c237).

---

## Mappa requisiti vs. implementazione

| ID | Requisito | Backend | Frontend | Stato |
|----|-----------|---------|----------|-------|
| RF-01 | Raccolta automatica email | Sync engine completo | — | Backend OK, manca background job |
| RF-02 | Gestione stati ticket | API status + history | 4 view modes (mock) | Da collegare FE→BE |
| RF-03 | Assegnazione ticket | API assign + tracking | UI assegnazione (mock) | Da collegare FE→BE |
| RF-04 | Categorizzazione automatica | Labels + categories API | CategoryBadge (mock) | Manca logica auto-categorizzazione |
| RF-05 | Integrazione MySQL (read-only) | Non implementato | Non implementato | **Non iniziato** |
| RF-06 | Pagina utente integrata | Non implementato | CustomerContext (mock) | **Non iniziato** |
| RF-07 | Template risposte automatiche | Non implementato | AiSuggestion (mock) | **Non iniziato** |
| RF-08 | Risposta email dal ticket | Send API + 3 sender | TicketReply (mock) | Da collegare FE→BE |
| RF-09 | Prioritizzazione ticket | Non implementato | SentimentIcon (mock) | **Non iniziato** |
| RF-10 | Filtri e ricerca | Search API (threads/messages) | Non implementato | Parziale (solo BE) |
| RF-11 | Note e allegati | Non implementato | Non implementato | **Non iniziato** |

**Sintesi**: 4/11 requisiti con backend implementato, 0/11 con integrazione end-to-end completa.

---

## Blocchi critici

### 1. Frontend non collegato al backend
Il frontend usa `mock/data.ts` con 20+ ticket finti. L'OpenAPI client e configurato (`frontend/client/`) ma non integrato. Questo e il blocco piu grande: senza questa connessione, nessun test end-to-end e possibile.

### 2. Background sync email
Il sync email funziona solo via chiamata API manuale (`POST /email/sync/all`). Per un uso reale, serve un background job che giri ogni N minuti (configurato a 300s in `config.py` ma non implementato).

### 3. Accesso MySQL RDS Jubatus
RF-05 e RF-06 dipendono dall'accesso al database del cliente. Serve:
- Schema MySQL aggiornato da Jonathan (domanda aperta #1)
- Configurazione security group per accesso dal nostro servizio
- Modello read-only nel backend (nuovo modulo o estensione email)

### ~~4. values.yaml non aggiornato~~ ✅ Risolto (2026-04-10)
`values.yaml` aggiornato con `app_name: support`, `cod_application: "2025093"`, `repo_name: jubatus`. Deploy su AWS completato.

---

## Prossimi passi suggeriti

### Priorita 1 — Sbloccare l'end-to-end (settimane 1-2)

1. **Collegare frontend al backend**
   - Generare client OpenAPI aggiornato (`npm run generate-client`)
   - Sostituire mock data con chiamate API reali in TicketsMain.tsx
   - Testare flusso: login → lista ticket → dettaglio → risposta

2. **Implementare background sync**
   - Schedulare sync periodico (ogni 5 min) come background task
   - Gestire token refresh automatico per ogni mailbox
   - Aggiungere health check per lo stato sync

3. **Aggiornare values.yaml**
   - `app_name`, `cod_application`, `repo_name` → valori Jubatus
   - Verificare `aws_account_id` per dev e prod con il team Jubatus

### Priorita 2 — Funzionalita core mancanti (settimane 3-4)

4. **Integrazione MySQL RDS (RF-05, RF-06)**
   - Ottenere schema DB da Jonathan
   - Creare modulo read-only con query per: utenti, ordini, eventi, contenuti
   - Collegare CustomerContext alla pagina utente integrata

5. **Auto-categorizzazione (RF-04)**
   - Definire categorie con il team CS (Logan, Gionata, Lorenza)
   - Implementare logica rule-based o keyword-based
   - Opzionale: sentiment analysis con LLM

6. **Filtri e ricerca completi (RF-10)**
   - Estendere search API con filtri: evento, categoria, priorita, stato
   - Implementare UI filtri nel frontend

### Priorita 3 — Completamento MVP (settimane 5-6)

7. **Template risposte (RF-07)**
   - Creare sistema template per categoria
   - UI di selezione/personalizzazione template
   - Integrazione con invio email

8. **Note e allegati (RF-11)**
   - Aggiungere modello note interne al DB
   - UI per aggiungere/visualizzare note
   - Link a Google Drive

9. **Test e stabilizzazione**
   - Aumentare test coverage backend (target: endpoint email principali)
   - Test E2E Playwright per flusso ticket completo
   - Fix token refresh per tutti i provider

### Backlog

- Prioritizzazione ticket (RF-09) — rule-based + sentiment
- Export CSV per marketing (richiesto nel meeting 2026-02-13)
- WhatsApp chatbot (fase 2 — escluso da MVP)
- Dashboard partner/eventi (fase 3 — escluso da MVP)

---

## File di riferimento

| Documento | Contenuto |
|-----------|-----------|
| [README.md](README.md) | Overview progetto, team, timeline, link |
| [architettura.md](architettura.md) | Stack, diagrammi, componenti, debito tecnico |
| [decisioni.md](decisioni.md) | 5 ADR documentate (AWS, FastAPI, email, mock, template) |
| [requisiti.md](requisiti.md) | 11 RF + 3 RNF, 2 domande aperte |
| [feature-log.md](feature-log.md) | Feature implementate con note tecniche |
| [meeting/](meeting/) | 3 note meeting (kickoff, ticketing, CS) |

**Repository codice**: `/Users/simonebrigante/LAIF/repo/jubatus/`
