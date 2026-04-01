---
progetto: "sebi-group"
data: "2026-03-29"
versione: "2.0"
stato: "bozza"
tags:
  - "#progetto:sebi-group"
  - "#fase:presales"
---

# Stima Modulare — Sebi Group

> Stime espresse in **€**.
> Le stime includono sviluppo, test e documentazione di base.
> Non includono: gestione progetto, meeting di allineamento, deploy infrastruttura.

---

## Riepilogo

| # | Modulo | € | Tipo |
|---|--------|---|------|
| — | Setup iniziale | 2.000 | ⭐ CORE |
| M1 | Email Intelligence | 14.000 | ⭐ CORE |
| M2 | Gestione Offerte | 18.000 | ⭐ CORE |
| M3 | Integrazione Gestionale | 5.000 | ⭐ CORE |
| | **TOTALE CORE** | **39.000** | |
| M4 | Dashboard e Analisi | 9.000 | Opzionale |
| M5 | Solleciti e Risposte Auto | 7.000 | Opzionale |
| | **TOTALE CORE + OPZIONALI** | **55.000** | |

---

## Setup iniziale (€2.000)

**Scope**: setup progetto, CI/CD, ambiente sviluppo/staging, autenticazione SSO M365, struttura database, design system UI, struttura ruoli e permessi (operatore, admin, management).

---

## M1 — Email Intelligence ⭐ CORE (€14.000)

**Scope**: connessione M365 Graph API, sincronizzazione email, classificatore AI, estrazione dati, vista unificata inbox.

**Dipendenze**: Setup iniziale, accesso admin M365

**Cosa include:**
- Sincronizzazione caselle email condivise (Export Sales, Import, China, Export, ecc.)
- Classificazione automatica per area (import/export), tipo richiesta, modalità trasporto, lingua
- Estrazione dati da email e allegati (origine, destinazione, peso, dimensioni, colli, resa, tipo merce) con indicatore di confidenza — sempre modificabili dall'operatore
- Inbox unificata con filtri, badge AI e segnalazione anomalie (cliente nuovo, fido esaurito, agente non verificato)

**Non include:** risposta automatica alle email, generazione risposta email, migrazione regole Outlook esistenti

---

## M2 — Gestione Offerte ⭐ CORE (€18.000)

**Scope**: ciclo completo dall'email alla quotazione cliente, per import e export. Flusso unificato con specificità dove i processi divergono.

**Dipendenze**: M1 (email), M3 (gestionale per import)

**Core (import + export):**
- Creazione pratica con codice univoco e timeline cronologica di tutti gli eventi
- Invio RDO ai fornitori selezionati dall'operatore, con template personalizzabili
- Raccolta e normalizzazione risposte fornitori in tabella comparativa (ogni fornitore risponde in formato diverso)
- Calcolo margine (percentuale o assoluto), generazione quotazione con alternative e versioni, PDF per il cliente
- Solleciti manuali a fornitori non rispondenti

**Specificità Export:**
- La piattaforma è il riferimento gestionale per l'export (nessun gestionale esterno)
- Gestione completa del ciclo offerta fino alla conferma cliente

**Specificità Import:**
- Inserimento dati pratica nel Gestionale via API
- L'operatore triggera l'invio massivo delle RDO dal Gestionale
- La piattaforma intercetta e normalizza le risposte dei fornitori
- Inserimento automatico dei costi fornitori nel Gestionale
- Il Gestionale applica il markup secondo le regole esistenti

**Non include:** invio automatico RDO senza selezione operatore, calcolo automatico del margine basato su regole, gestione operativa post-conferma, prepratica post-conferma

---

## M3 — Integrazione Gestionale ⭐ CORE (€5.000)

**Scope**: collegamento bidirezionale con il Gestionale esistente (area import).

**Dipendenze**: Meeting con fornitore gestionale, documentazione API

> **Dipendenza critica**: è necessario un **meeting tecnico con il fornitore del Gestionale** per validare la fattibilità dell'integrazione e affinare la stima. Senza questo confronto, ci posizioniamo verso il massimo del range.

**Cosa include:**
- Sincronizzazione anagrafiche clienti e fornitori
- Verifica fido/credito in tempo reale (fido disponibile, totale, stato credito)
- Accesso tariffari per suggerire prezzi di riferimento
- Push dati bidirezionale: quotazioni → Gestionale, conferme/codici pratica ← Gestionale

**Non include:** modifica struttura o logica del Gestionale, migrazione dati storici, funzionalità non esposte da API

**Rischio**: la stima dipende fortemente dalla qualità e completezza delle API del gestionale. Se le API sono limitate o la documentazione carente, il costo può crescere.

---

## M4 — Dashboard e Analisi (€9.000)

> Modulo da approfondire in un secondo sviluppo. Il tipo di analisi e i KPI prioritari vanno definiti con il cliente.

**Scope**: dashboard operativa per operatore, dashboard management con KPI, analisi clienti e agenti.

**Dipendenze**: M1-M3 (dati da tutti i moduli core)

**Cosa include:**
- **Dashboard operativa**: email non lette, pratiche da lavorare, deadline, solleciti pendenti, lista prioritizzata
- **Dashboard management**: tasso di conversione, margine medio, valore pipeline, trend temporali
- **Analisi Clienti e Agenti**: sezione dedicata per ogni cliente/agente con frequenza richieste, tasso di accettazione (quotazioni confermate / richieste), storico ordini e volumi, scoring e ranking per prioritizzare i clienti più profittevoli
- **Filtri**: per periodo, area (import/export), modalità di trasporto, operatore
- **Export dati** per analisi esterne

---

## M5 — Solleciti e Risposte Automatiche (€7.000)

> Sistema di automazione email con regole configurabili e guard-rail per evitare invii indesiderati.

**Scope**: solleciti automatici, risposte automatiche, presa in carico email ricorrenti.

**Dipendenze**: M1 (email), M2 (pratiche)

**Cosa include:**
- Solleciti automatici a fornitori non rispondenti (dopo X ore/giorni, configurabile)
- Risposte automatiche per richiesta dati mancanti (es. fuori orario lavorativo)
- Presa in carico automatica email ricorrenti
- Ogni automazione disattivabile singolarmente, con log di tutti gli invii

> Questo modulo richiede la definizione di regole molto specifiche insieme agli operatori per evitare errori. L'approccio sarà graduale: si parte con poche regole semplici e si estende progressivamente.

**Non include:** invio autonomo di quotazioni o RDO senza supervisione

---

## Note sulla stima

### Fattori che possono aumentare la stima
- **API gestionale**: documentazione carente, limiti non noti, necessità di reverse engineering
- **Varietà formati fornitori**: se i formati sono molto più eterogenei del previsto, il parsing AI richiederà più tuning
- **Requisiti aggiuntivi**: funzionalità emerse durante lo sviluppo non previste nei requisiti attuali

### Fattori che possono ridurre la stima
- **API gestionale ben documentate** e complete → M3 verso il minimo
- **Riuso componenti LAIF template** → setup e UI base più rapidi
- **Esempi email di qualità** forniti rapidamente → tuning AI più veloce

### Ordine di sviluppo suggerito
1. **Setup + M1 (Email Intelligence)** — fondamento per tutto
2. **M2 Core + Export** — gestione offerte, prima area più autonoma
3. **M2 Import + M3 (Integrazione Gestionale)** — richiede meeting con fornitore
4. **M4 (Dashboard e Analisi)** — quando ci sono dati sufficienti
5. **M5 (Solleciti e Risposte Auto)** — dopo stabilizzazione flussi core

### Moduli indipendenti
Ogni modulo è stimato per essere **acquistabile separatamente**. Il cliente può scegliere di partire con un sottoinsieme (es. solo Setup + M1 + M2 + M3 per il core) e aggiungere M4 e M5 successivamente.

Il **MVP minimo** consigliato è: Setup + M1 + M2 + M3 = **€39.000**.
