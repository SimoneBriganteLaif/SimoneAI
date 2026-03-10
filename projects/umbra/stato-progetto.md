---
progetto: "umbra"
ultimo-aggiornamento: "2026-03-10"
tags:
  - "#progetto:umbra"
  - "#fase:dev"
---

# Stato Progetto — Umbra

> Punto di ingresso per riprendere lo sviluppo. Ultimo aggiornamento: 2026-03-10.

---

## Stato complessivo

Il progetto ha due moduli. Il modulo A (schedulazione settimanale) e in sviluppo: SFTP configurato, file settimanali depositati, parsing e riaggregazione in corso. Il modulo B (promozioni WOW) e in fase di analisi avanzata: requisiti raccolti in 3 meeting con il marketing, mockup interfaccia presentato il 3 marzo, validazione UI/UX pianificata per il 12 marzo.

---

## Mappa requisiti vs. implementazione

| ID | Requisito | Backend | Frontend | Stato |
|----|-----------|---------|----------|-------|
| RF-01 | Aggiornamento settimanale dati | Parziale | — | In sviluppo |
| RF-02 | Integrazione SFTP automatica | Parziale | — | In sviluppo |
| RF-03 | Formato output CSV | OK | — | Completato |
| RF-04 | Gestione varianti prodotto | Non iniziato | Non iniziato | Non iniziato |
| RF-05 | Modulo marketing WOW | Non iniziato | Non iniziato | In analisi |
| RF-06 | Vista Gantt pianificazione | Non iniziato | Non iniziato | In analisi |
| RF-07 | Suggerimenti AI prioritizzati | Non iniziato | Non iniziato | In analisi |
| RF-08 | Vincoli temporali per fornitore | Non iniziato | Non iniziato | In analisi |
| RF-09 | Conversione sell-out -> sell-in | Non iniziato | Non iniziato | In analisi |
| RF-10 | Tracciamento performance | Non iniziato | Non iniziato | In analisi |
| RF-11 | Campagne speciali | Non iniziato | Non iniziato | In analisi |

---

## Blocchi critici

### 1. Dati mancanti da Umbra

Diversi dataset necessari per il modulo WOW non sono ancora stati forniti:
- Storicita WOW completa
- Budget normalizzato per fornitore/classe/sottoclasse
- Listino CELIN (acquisto)
- Avanzamento fatturato per fornitore

Adriano sta sviluppando un'app sul gestionale per normalizzare il budget.

### 2. Certificato SFTP scaduto

Il certificato SFTP di Umbra e scaduto. Paolo (sistemista Umbra) deve risolverlo. Valutare uso wildcard Umbra o certificato LAIF.

### 3. Ponte S400-DMZ

Adriano deve configurare l'accesso diretto dall'S400 alla cartella SFTP in DMZ. Attualmente i file vengono depositati nella cartella condivisa, non ancora nell'SFTP diretto.

---

## Prossimi passi suggeriti

### Priorita 1 — Validazione UI modulo WOW (settimana 11)

1. **Follow-up 12 marzo ore 10-11**: validare grafica e flusso con Alessandra
2. **Sviluppare mockup funzionale** con dati finti per iterazione rapida

### Priorita 2 — Completare modulo A (settimane 11-12)

1. **Completare parsing file settimanali** da SFTP
2. **Implementare riaggregazione settimanale** dei dati
3. **Test end-to-end** del flusso settimanale

### Backlog

- Integrazione dati WOW quando Umbra li fornisce (storicita, budget, listino CELIN)
- Sviluppo algoritmo suggerimento WOW
- Frontend modulo marketing
- Tracciamento performance promozioni

---

## File di riferimento

| Documento | Contenuto |
|-----------|-----------|
| [README.md](README.md) | Overview progetto, team, timeline, link |
| [architettura.md](architettura.md) | Stack, diagrammi, componenti |
| [decisioni.md](decisioni.md) | Decisioni tecniche (ADR) |
| [requisiti.md](requisiti.md) | Requisiti funzionali e non funzionali |
| [feature-log.md](feature-log.md) | Feature implementate con note tecniche |
| [meeting/](meeting/) | Note meeting |

**Repository codice**: `/Users/simonebrigante/LAIF/repo/umbra-recommend/`
