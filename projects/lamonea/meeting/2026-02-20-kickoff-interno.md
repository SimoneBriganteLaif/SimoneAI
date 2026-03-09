---
fonte: notion
url: https://www.notion.so/30d90ad6ee4880989611dd3d0ab8c14c
data: 2026-02-20
partecipanti: [Simone Brigante]
tipo: kickoff
tags:
  - "#progetto:lamonea"
---

# Kickoff interno

Meeting interno per il kickoff del progetto Lamonea S.R.L., piattaforma gestionale per distribuzione materiale medico.

## Panoramica Progetto

- Investimento: 35.000€ + canone ricorrente annuale, 4 tranche fino a fine giugno
- Cliente ha valutato competitor (~50K€ una tantum, no canone) ma ha scelto LAIF
- Livello di digitalizzazione molto basso — processi artigianali, Excel, cartaceo

## Contesto Cliente

- **3 società**: SRL (import, gare grandi, Amazon), Endosurgery (privati), Medical (gare PA)
- Attualmente usano TeamSystem con tre silos separati, vogliono vista unificata
- Fondatore ancora in azienda, gestione passata a Mathias (CEO)

### Persone chiave
- **Mathias Lamonea**: CEO, persona tranquilla, delega molto
- **Andrea Spilli**: responsabile acquisti/logistica, molto preciso ma esigente
- **Matteo Farinelli**: responsabile commerciale, sponsor del progetto

### Modello di business
- Acquisto materiale medico da Est/Cina con lead time lunghi (anche 3 mesi via nave)
- Rivendita a privati e PA tramite gare d'appalto
- Magazzini propri per gestione stock

## Scope tecnico

### Priorità sviluppo
1. Catalogo digitale prodotti (base di tutto)
2. CRM con gestione clienti/opportunità/ordini
3. Portale cliente
4. Modulo gare d'appalto
5. Logistica e magazzino (fase 2)

### Moduli principali
- **CRM**: gestione clienti, prospect, opportunità, ordini (nessun CRM attuale)
- **Gare d'appalto**: trattamento speciale, gara vinta genera ordini progressivi nel tempo
- **Catalogo digitale**: anagrafica articoli, listini, immagini, import massivo
- **Ordini**: multi-canale (email, telefono, NSO per PA), commerciali da mobile
- **Portale B2B**: accesso clienti selezionati, catalogo personalizzato, riordino
- **Portale fornitori**: upload certificati, multilingua
- **Magazzino**: giacenze da TS, lotti/scadenze, alert sottoscorta, fabbisogni da gare vinte
- **Logistica**: DDT, tracking spedizioni, pistole barcode via TS

## Integrazioni
- **TeamSystem**: API testate e funzionanti, lettura/scrittura, sync notturna per BI + on-demand per operativo
- **NSO**: ordini PA arrivano su TS, da sincronizzare in lettura
- **Amazon**: evolutiva futura, monitoraggio vendite/KPI (fuori scope iniziale)

## Approccio
- Partire dal basso, portare valore rapidamente, poi iterare
- Evitare scope creep con analisi requisiti strutturata
- Guidare il cliente verso soluzioni semplici ed efficaci
- Web app responsive (PWA) per desktop, tablet, mobile

## Action Items
- Marco Vita: creare infrastruttura e account
- Meeting con cliente lunedì mattina per allineamento
- Simone: supporto analisi requisiti
- 2-3 meeting interni per divisione task
