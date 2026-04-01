---
progetto: "sebi-group"
cliente: "Sebi Group"
data: "2026-03-17"
versione: "1.0"
stato: "bozza"
max-pagine: 3
tags:
  - "#progetto:sebi-group"
  - "#fase:presales"
---

# Allegato Tecnico — Piattaforma Gestione Email e Quotazioni

**Cliente**: Sebi Group S.r.l.
**Data**: 17 marzo 2026
**Versione**: 1.0

---

## 1. Oggetto della fornitura

LAIF realizzerà per Sebi Group una piattaforma web che centralizza la gestione delle email commerciali e automatizza il processo di quotazione per i reparti import ed export. La piattaforma leggerà le email dalle caselle condivise, le classificherà automaticamente, le assegnerà agli operatori, e guiderà il processo dalla richiesta del cliente alla quotazione finale — riducendo il tempo dedicato ad attività manuali a basso valore aggiunto e fornendo visibilità completa su ogni pratica.

---

## 2. Funzionalità incluse

Le seguenti funzionalità sono incluse nell'ambito contrattuale, organizzate in moduli:

| # | Modulo | Descrizione sintetica |
|---|--------|----------------------|
| 1 | **Email Intelligence** | Connessione alle caselle email Outlook 365, classificazione automatica delle email in arrivo (tipo, area, cliente, urgenza), assegnazione all'operatore competente, vista unificata senza bisogno di aprire Outlook |
| 2 | **Gestione Offerte Export** | Ciclo completo dalla richiesta alla quotazione: creazione richieste ai fornitori, raccolta e confronto preventivi, calcolo prezzo con margine, generazione documento per il cliente. Ogni richiesta ha un codice univoco |
| 3 | **Gestione Offerte Import** | Integrazione con il gestionale per apertura quotazioni, invio richieste ai fornitori, lettura automatica delle risposte, inserimento costi, selezione migliore offerta con markup |
| 4 | **Integrazione Gestionale** | Collegamento con il software gestionale esistente: lettura anagrafiche clienti e fornitori, verifica fido e credito, lettura tariffari, creazione quotazioni |
| 5 | **Dashboard Operativa** | Vista personalizzata per operatore con attività da svolgere, stato delle pratiche, solleciti attivi, tempi di risposta |
| 6 | **Automazioni Assistite** | Solleciti automatici ai fornitori che non rispondono, richiesta dati mancanti al cliente, bozze email assistite — sempre con approvazione umana prima dell'invio |

**Fasi successive** (non incluse nel presente contratto, quotabili separatamente):
- Dashboard management con KPI avanzati (conversioni, margini, performance)
- Integrazione WebCargo per quotazioni aeree automatizzate
- Verifica automatica appartenenza agenti ai network

---

## 3. Funzionalità escluse

Le seguenti funzionalità **non sono incluse** nel presente contratto:

- Gestione operativa post-conferma (sdoganamento, tracking spedizione, consegna)
- Contabilità, fatturazione e gestione amministrativa
- Sostituzione del software gestionale esistente (la piattaforma lo affianca)
- Invio automatico di email senza revisione e approvazione dell'operatore
- Gestione documentazione doganale
- Applicazione mobile nativa (la piattaforma è accessibile da browser)

---

## 4. Modalità di consegna

**Consegna**: applicazione web accessibile da browser (Chrome, Edge, Firefox) senza installazione.

**Ambienti**:
- Ambiente di test: disponibile durante lo sviluppo per validazione progressiva
- Ambiente di produzione: attivato al go-live dopo approvazione del cliente

**Accesso**: tramite credenziali aziendali (Single Sign-On con Microsoft 365).

**Rilascio**: incrementale per moduli, con validazione del cliente ad ogni rilascio.

---

## 5. Responsabilità del cliente

Per consentire la realizzazione del progetto nei tempi previsti, il cliente si impegna a:

- Designare un **referente tecnico** (interno o IT) disponibile per incontri di allineamento bisettimanali
- Fornire **accesso amministrativo** alle caselle email Microsoft 365 coinvolte
- Coordinare il **meeting con il fornitore del gestionale** per definire le modalità di integrazione (API, credenziali, ambiente di test)
- Fornire **esempi reali** di email e flussi operativi per configurare la classificazione AI
- Fornire le **regole di markup e margine** da applicare nelle quotazioni
- Validare i deliverable (mockup, funzionalità rilasciate) entro **5 giorni lavorativi** dalla consegna

---

## 6. Manutenzione e supporto post go-live

Al completamento del progetto è previsto un periodo di **garanzia di 30 giorni** per la correzione di difetti. Eventuali servizi di manutenzione continuativa, evoluzione funzionale e supporto tecnico saranno oggetto di un contratto separato.

---

## 7. Proprietà intellettuale

Il codice sorgente sviluppato specificamente per Sebi Group è di proprietà del cliente al completamento del pagamento. LAIF mantiene il diritto di riutilizzare componenti generici, librerie e framework non specifici al progetto del cliente.

---

*Documento redatto da LAIF — 17 marzo 2026 — Versione 1.0*
