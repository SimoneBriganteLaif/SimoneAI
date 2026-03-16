# Modularizzazione dei Template

| Campo | Valore |
|---|---|
| **ID** | 74 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | Backlog |
| **Tag** | Breaking |

## Descrizione originale

Modularizzazione dei template.

## Piano di risoluzione

1. **Identificare i moduli impliciti attuali** — il template contiene già dei "moduli" non formalizzati. Censirli:
   - **Auth**: autenticazione, login, registrazione, JWT, OAuth2.
   - **Ticketing/Supporto**: sistema di ticket, gestione stati.
   - **User Management**: gestione utenti, ruoli, permessi.
   - **Media Service**: upload file, gestione media.
   - **AI Agent**: agente AI, chat, RAG (issue 163).
   - **Navigazione**: sidebar, header, routing.
   - **Core**: configurazione, API base, store Redux, layout.
2. **Definire l'interfaccia di un modulo** — stabilire il contratto che ogni modulo deve rispettare:
   - Cosa fornisce (route, componenti, API endpoints, modelli DB).
   - Cosa richiede (dipendenze da altri moduli, servizi core).
   - Come si registra nel sistema (auto-discovery o dichiarativo).
3. **Permettere opt-in/opt-out dei moduli al momento del fork** — al momento della creazione di un nuovo progetto, lo sviluppatore sceglie quali moduli includere. I moduli non selezionati non vengono copiati.
4. **Ogni modulo come directory o package separato** — strutturare il template con una convenzione chiara:
   - `modules/ticketing/` — backend + frontend + migrazioni.
   - `modules/auth/` — backend + frontend + migrazioni.
   - Ogni modulo è autocontenuto ma può dichiarare dipendenze.
5. **Risoluzione delle dipendenze tra moduli** — definire un grafo delle dipendenze (es. ticketing richiede auth + user-management). Validare le dipendenze al momento del fork.
6. **Dipendenza da Copier o tooling equivalente** — la modularizzazione ha senso solo se abbiamo un sistema di templating che supporta la generazione condizionale. Copier (issue 94) è il candidato principale (supporta condizionali Jinja2 nel `copier.yaml`).
7. **Approccio incrementale: partire dalla documentazione** — prima di ristrutturare il codice, documentare i moduli impliciti, le loro dipendenze e i loro confini. Questo è utile anche senza la modularizzazione formale.

### Issue correlate

- Issue 94 — Copier (abilita la modularizzazione)
- Issue 73 — Semplificare upstream (la modularizzazione semplifica gli aggiornamenti selettivi)
- Issue 141 — Config file e feature flag (i flag possono abilitare/disabilitare moduli)

## Stima effort

**Documentazione moduli: 8h. Implementazione completa: 40-60h.** Questa è la proposta più ambiziosa del template. Consigliato un approccio molto incrementale:
- Fase 1 (8h): documentazione dei moduli impliciti e delle dipendenze.
- Fase 2 (16h): ristrutturazione directory (senza cambiare funzionalità).
- Fase 3 (16h): integrazione con Copier per generazione condizionale.
- Fase 4 (16h): testing e migrazione progetti esistenti.
