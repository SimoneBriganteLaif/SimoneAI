---
fonte: notion
url: https://www.notion.so/31290ad6ee4880418bcefbad73999099
data: 2026-02-25
partecipanti: [Simone Brigante]
tipo: review
tags:
  - "#progetto:lamonea"
---

# Requisiti Fase 1 — Catalogo Prodotti Digitale & CRM

Documento requisiti funzionali dei moduli Catalogo Prodotti Digitale e CRM con livello di dettaglio sufficiente a generare mockup UI.

## 1. Contesto generale

### Struttura del gruppo
| Società | Focus | Canali vendita |
|---------|-------|----------------|
| Lamonea SRL | Importazione diretta, gare grandi | B2B, Amazon, futuro B2C |
| Lamonea Endosurgery | Clienti privati (cliniche, laboratori) | B2B |
| Lamonea Medical | Gare d'appalto pubbliche | PA |

### Principi di prodotto
- Multisocietario nativo: anagrafica unica condivisa
- TeamSystem come sistema contabile (master contabilità/fatturazione)
- Web App (PWA): desktop, tablet, smartphone
- Ruoli e permessi: manageriale (multi-società) vs operativo (filtrato)

## 2. Modulo Catalogo Prodotti Digitale

### Data Model: Prodotto (Articolo)
Campi principali: codice articolo (unique, stesso su 3 società TS), nome/descrizione, categoria (gerarchia), immagini (gallery), documentazione tecnica (CE/MDR, conformità, IFU), listino base, unità di misura, disponibilità a stock (da TS), lead time, stato (attivo/obsoleto/dismesso), società di appartenenza (multi-select), fornitore/i.

### Data Model: Listino personalizzato
Per cliente: articolo, prezzo personalizzato o sconto %, validità opzionale.

### Data Model: Kit multiprodotto
Nome, articoli componenti con quantità, prezzo kit.

### Requisiti funzionali Catalogo
- **REQ-CAT-01**: Vista catalogo tabellare con colonne configurabili, filtri, ordinamento, paginazione
- **REQ-CAT-02**: Vista catalogo card ("Amazon-like") con griglia, toggle tra viste
- **REQ-CAT-03**: Dettaglio prodotto (gallery, prezzi, disponibilità, documentazione, info)
- **REQ-CAT-04**: CRUD prodotto con upload multiplo immagini/documenti, validazione
- **REQ-CAT-05**: Import massivo CSV/Excel con anteprima e report
- **REQ-CAT-06**: Listini personalizzati per cliente (prezzo/sconto, copia tra clienti)
- **REQ-CAT-07**: Filtro multi-società globale (Tutte | SRL | Endosurgery | Medical)
- **REQ-CAT-08**: Sync TeamSystem (lettura import iniziale, allineamento continuo, scrittura nuovo articolo su 3 società)

## 3. Modulo CRM

### Data Model: Cliente
Campi: ragione sociale, P.IVA/CF, tipologia (Privato/PA/Clinica mista), società servite, indirizzi (fatturazione + spedizione multipli), agente assegnato, stato, portale B2B abilitato.

### Data Model: Contatto
Per cliente: nome, ruolo, email, telefono, note.

### Data Model: Opportunità
Titolo, cliente, tipo (Commerciale/Gara d'appalto), stato pipeline (Lead → Qualificato → Proposta → Vinto → Perso), valore stimato, società, commerciale, date apertura/chiusura, motivazione chiusura, righe prodotto (articolo + quantità + prezzo).

### Data Model: Interazione
Tipo (Nota/Chiamata/Email/Appuntamento/Sollecito), descrizione (rich text), data, cliente, opportunità (opzionale), autore, follow-up previsto.

### Requisiti funzionali CRM
- **REQ-CRM-01**: Lista clienti con filtri, ordinamento, azione rapida nuovo cliente
- **REQ-CRM-02**: Dossier cliente con tab (Anagrafica, Opportunità, Interazioni, Ordini read-only da TS, Listino personalizzato, Dati finanziari read-only da TS)
- **REQ-CRM-03**: Pipeline Kanban (board drag & drop: Lead → Qualificato → Proposta → Vinto → Perso)
- **REQ-CRM-04**: Dettaglio opportunità (header, righe prodotto, interazioni, bottone "Genera Preventivo")
- **REQ-CRM-05**: Form opportunità con righe prodotto (supporto centinaia di righe, virtualizzazione)
- **REQ-CRM-06**: Interazioni con follow-up e reminder visivo in dashboard
- **REQ-CRM-07**: Dashboard CRM (KPI, pipeline summary, attività recenti, follow-up in scadenza)
- **REQ-CRM-08**: Filtro multi-società globale
- **REQ-CRM-09**: Import dati iniziale (clienti, fornitori, note CRM, storico ordini da TS)
- **REQ-CRM-10**: Sync TeamSystem continua (lettura aggiornamenti, scrittura nuovi clienti, schedule on-demand/notturna)

## 4. Navigazione e layout UI

### Struttura navigazione
- Dashboard (KPI CRM + alert)
- Catalogo (vista tabellare / card)
- CRM: Clienti, Opportunità (Kanban), Interazioni (timeline)
- Impostazioni (utenti, ruoli, listini)

### Elementi globali
- Selector società in top bar (persistente)
- Barra ricerca globale (prodotti, clienti, opportunità)
- Avatar utente + ruolo
- Layout responsive desktop → tablet → mobile

### Schermate da mockuppare (priorità)
1. Catalogo vista card
2. Catalogo vista tabellare
3. Dettaglio prodotto
4. Lista clienti
5. Dossier cliente (tab)
6. Pipeline Kanban
7. Dettaglio opportunità
8. Form nuova interazione
9. Dashboard CRM
10. Import massivo
