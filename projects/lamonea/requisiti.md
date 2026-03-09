---
progetto: "lamonea"
versione: "0.1"
data: "2026-02-25"
fonte: "Notion — Requisiti Fase 1"
validato-da: ""
tags:
  - "#progetto:lamonea"
  - "#fase:dev"
---

# Requisiti — Lamonea

> Generato automaticamente da init-project. Validare con skill `estrazione-requisiti`.

## Requisiti funzionali

### Catalogo Prodotti Digitale

| ID | Requisito | Priorità | Criterio di accettazione |
|----|-----------|----------|--------------------------|
| RF-CAT-01 | Vista catalogo tabellare con colonne configurabili, filtri, ordinamento, paginazione | Alta | L'utente può filtrare per categoria, stato, disponibilità, società, range prezzo, testo libero |
| RF-CAT-02 | Vista catalogo card ("Amazon-like") con griglia e toggle tra viste | Alta | L'utente può passare da vista tabellare a card e viceversa con stessi filtri |
| RF-CAT-03 | Dettaglio prodotto con gallery immagini, prezzi, disponibilità, documentazione tecnica | Alta | Pagina mostra gallery swipe, listino base + personalizzato, badge stock, file scaricabili |
| RF-CAT-04 | CRUD prodotto con upload multiplo immagini e documenti tecnici | Alta | Form con drag & drop, validazione codice univoco, campi obbligatori |
| RF-CAT-05 | Import massivo articoli da CSV/Excel con anteprima e report | Media | Anteprima pre-import con errori evidenziati, report post-import con righe importate/scartate |
| RF-CAT-06 | Listini personalizzati per cliente (prezzo o sconto %) con copia tra clienti | Alta | Da scheda cliente o dettaglio prodotto, vista riepilogativa per cliente |
| RF-CAT-07 | Filtro multi-società globale (Tutte / SRL / Endosurgery / Medical) | Alta | Toggle persistente in top bar, filtra tutti i dati in base alla società selezionata |
| RF-CAT-08 | Sincronizzazione TeamSystem (lettura iniziale, allineamento continuo, scrittura) | Alta | Import ~4.000-5.000 articoli movimentati, sync periodica, nuovo articolo scritto su 3 società TS |

### CRM

| ID | Requisito | Priorità | Criterio di accettazione |
|----|-----------|----------|--------------------------|
| RF-CRM-01 | Lista clienti con filtri, ordinamento, azione rapida nuovo cliente | Alta | Tabella con ragione sociale, tipologia, società, stato, agente, n° opportunità |
| RF-CRM-02 | Dossier cliente con tab (Anagrafica, Opportunità, Interazioni, Ordini, Listino, Finanze) | Alta | 6 tab navigabili, ordini e finanze read-only da TS |
| RF-CRM-03 | Pipeline opportunità Kanban (Lead → Qualificato → Proposta → Vinto → Perso) | Alta | Board drag & drop con filtri per società, agente, tipo, valore, date |
| RF-CRM-04 | Dettaglio opportunità con righe prodotto e interazioni | Alta | Header editabile, tabella righe con autocompletamento catalogo, timeline interazioni |
| RF-CRM-05 | Form creazione/modifica opportunità con centinaia di righe prodotto | Alta | Ricerca articolo da catalogo, prezzo precompilato da listino, virtualizzazione per grandi volumi |
| RF-CRM-06 | Interazioni con follow-up e reminder visivo in dashboard | Media | Form con tipo, rich text, follow-up opzionale; badge/notifica per follow-up in scadenza |
| RF-CRM-07 | Dashboard CRM con KPI, pipeline summary, attività recenti, follow-up | Media | KPI: n° opportunità, valore pipeline, tasso conversione; grafico barre; ultime 10 interazioni |
| RF-CRM-08 | Filtro multi-società globale (identico a RF-CAT-07) | Alta | Tutti i dati CRM si filtrano per società; ruolo manageriale vede tutte |
| RF-CRM-09 | Import dati iniziale (clienti, fornitori, note CRM, storico ordini) da TS | Alta | Mappatura per codice, report discrepanze, pulizia dati |
| RF-CRM-10 | Sincronizzazione TeamSystem continua | Alta | Lettura: clienti, ordini, finanze. Scrittura: nuovo cliente su 3 società. Schedule on-demand + notturna |

## Requisiti non funzionali

| ID | Requisito | Priorità | Note |
|----|-----------|----------|------|
| RNF-01 | Web App responsive (PWA) per desktop, tablet, smartphone | Alta | Commerciali usano l'app in mobilità |
| RNF-02 | Multisocietario nativo con separazione/condivisione governata da permessi | Alta | Vista aggregata di gruppo e per singola società |
| RNF-03 | Supporto a grandi volumi di dati (centinaia di righe per opportunità, ~14.000 articoli) | Alta | Virtualizzazione tabelle, paginazione |

## Integrazioni richieste

| Sistema | Tipo | Descrizione | Criticità |
|---------|------|-------------|-----------|
| TeamSystem (Lynfa Azienda) | Lettura + Scrittura | Sync clienti, fornitori, articoli, ordini, dati finanziari via Web Services JSON | Alta |
| TeamSystem — CodiceWS 500001 | Configurato | Clienti/Fornitori | — |
| TeamSystem — CodiceWS 500027 | Da configurare | Articoli | — |
| TeamSystem — CodiceWS 500011 | Da configurare | Documenti | — |
| TeamSystem — CodiceWS 500028 | Da configurare | Ordini | — |
| TeamSystem — CodiceWS 500009 | Da configurare | Movimenti | — |

## Esclusioni esplicite (Fase 1)

- Modulo Amazon (analisi futura)
- Logistica e spedizioni completa (DDT, tracking corrieri)
- Magazzino avanzato (lotti, scadenze, fabbisogni, pistole barcode)
- Preventivazione guidata e generazione PDF preventivi
- Portale B2B clienti
- Portale fornitori
- Recupero crediti / controllo
- Gare d'appalto a scalare (gestione quantitativi residui)

## Domande aperte

| # | Domanda | Stato |
|---|---------|-------|
| 1 | Articoli appartengono a una sola famiglia/sottofamiglia o a un solo gruppo/sottogruppo? | Da validare |
| 2 | Gestiremo famiglie e gruppi in app? | Da validare |
| 3 | Come funzionano i kit? | Da validare |
| 4 | Gestione prezzi: prezzo unico su articolo o solo tramite listini? | Da validare |
| 5 | I listini hanno periodi di durata? | Da validare |
| 6 | Opportunità e gare sono da gestire separatamente? | Da validare |
| 7 | Quanti magazzini? | Da validare |
| 8 | Configurazione WebService TS per articoli, documenti, ordini, movimenti | Bloccante per sync |

## Changelog

| Versione | Data | Autore | Descrizione |
|----------|------|--------|-------------|
| 0.1 | 2026-02-25 | init-project | Bozza iniziale da Notion |
