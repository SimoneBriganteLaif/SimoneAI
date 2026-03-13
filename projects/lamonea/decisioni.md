---
progetto: "lamonea"
tags:
  - "#progetto:lamonea"
  - "#fase:dev"
---

# Decisioni Tecniche — Lamonea

> **Formato ADR** (Architecture Decision Record).
> Ogni decisione rilevante viene documentata qui nel momento in cui viene presa.
> Aggiornato dalla skill `skills/development/estrazione-decisioni.md`.

---

## Come usare questo file

Aggiungi una sezione per ogni decisione tecnica significativa. Una decisione è "significativa" se:
- Cambia lo stack o introduce una nuova dipendenza
- Influenza come altri componenti vengono scritti
- Ha alternative valide che abbiamo scartato
- Potrebbe essere difficile da cambiare in futuro

---

## ADR-001: Architettura pipeline dati TeamSystem — STG / ETL / PRS

**Data**: 2026-03-12
**Stato**: Accettata
**Autore**: Simone Brigante

### Contesto

Dobbiamo integrare dati da TeamSystem Lynfa Azienda (articoli, clienti, fornitori, documenti) nella piattaforma Lamonea. I dati devono essere esposti al frontend tramite API FastAPI. TeamSystem ha 3 ditte separate (49, 133, 212) con gli stessi dati replicati, e le API sono asincrone (nessun risultato sincrono disponibile su istanza SaaS).

### Opzioni valutate

**Opzione A: Import diretto in tabelle applicative (prs)**
- Pro: meno layer, più semplice da implementare inizialmente
- Contro: dati TS arrivano in formato grezzo con campi non mappati, nomi non coerenti col modello applicativo; difficile fare rollback o debug; ogni cambio nel WS TS rompe il modello dati

**Opzione B: Staging RAW + ETL + Presentation (scelta)**
- Pro: staging isola il formato TS dal modello applicativo; debug facile (raw_payload JSONB); ETL separato e sostituibile; staging multi-ditta permette di vedere dati per singola ditta prima di unificarli
- Contro: più layer da mantenere, latenza maggiore tra sync TS e disponibilità dati in prs

### Decisione

Pipeline a tre layer:
1. **STG** (schema `stg`): dati RAW da TS, PK composta `(codice, ditta)`, campo `raw_payload JSONB` per debug, nessuna trasformazione
2. **ETL**: processo separato (background task o job schedulato) che trasforma stg → prs
3. **PRS** (schema `prs`): star schema per il frontend — dimensioni (articolo, cliente, fornitore, società) e fatti

Il Modulo Integrazione TS (TSClient + TSPoller + Processor) scrive solo in `stg`. Il frontend legge solo da `prs`. L'ETL è un componente separato e sostituibile.

Vedi pattern: `patterns/async-integration-client-poller.md`

### Conseguenze

**Positive**:
- Debugging semplice: `raw_payload` in stg contiene sempre il dato originale TS
- ETL modificabile senza toccare la logica di sync
- Staging multi-ditta permette analisi pre-ETL e riconciliazione

**Negative / trade-off accettati**:
- Due migrazioni da gestire (schema `stg` + schema `prs`)
- Latenza: un dato aggiornato in TS diventa visibile in frontend dopo sync + ETL
- Per ora l'ETL stg → prs non è ancora implementato (backlog)

**Azioni richieste**:
- Creare schema `stg` con tabelle per ogni entità TS integrata
- Implementare ETL stg → prs (sprint successivo)

---

## Indice decisioni

| ID | Titolo | Data | Stato |
|----|--------|------|-------|
| ADR-001 | Architettura pipeline dati TeamSystem — STG / ETL / PRS | 2026-03-12 | Accettata |
