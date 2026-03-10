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

Il progetto ha due moduli. Il modulo A (schedulazione settimanale) e in sviluppo: SFTP configurato, file settimanali depositati, parsing e riaggregazione in corso. Il modulo B (promozioni WOW) ha completato il primo ciclo di sviluppo UI: Windsurf ha implementato sia l'estensione Gantt WEEK in laif-ds (13/13 task) sia il refactor UI WOW in 3 pagine (14/14 task). Le modifiche sono linkate localmente via `npm link` e pronte per review visuale. Validazione UI/UX pianificata per il 12 marzo.

---

## Mappa requisiti vs. implementazione

| ID | Requisito | Backend | Frontend | Stato |
|----|-----------|---------|----------|-------|
| RF-01 | Aggiornamento settimanale dati | Parziale | — | In sviluppo |
| RF-02 | Integrazione SFTP automatica | Parziale | — | In sviluppo |
| RF-03 | Formato output CSV | OK | — | Completato |
| RF-04 | Gestione varianti prodotto | Non iniziato | Non iniziato | Non iniziato |
| RF-05 | Modulo marketing WOW | Non iniziato | Scaffold UI (3 pagine) | In sviluppo |
| RF-06 | Vista Gantt pianificazione | Non iniziato | Gantt WEEK + wrapper | In review |
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

### Priorita 1 — Review e test modulo WOW (settimana 11)

1. **Sviluppo Windsurf completato** (10 marzo):
   - Gantt WEEK extension in laif-ds: 13/13 task completati (report: `windsurf-briefs/2026-03-10T1524-gantt-week-extension-report.md`)
   - UI refactor WOW in 3 pagine: 14/14 task completati (report: `windsurf-briefs/2026-03-10T1509-wow-ui-refactor-report.md`)
2. **Integrazione locale**: laif-ds linkata via `npm link`, `WowGanttView.tsx` aggiornato a `GanttDimensions.WEEK`
3. **Da fare**: review visuale, test navigazione 3 pagine, verificare rendering Gantt settimanale
4. **Decisioni documentate**: 3 ADR in `decisioni.md` (isoWeek, layout main, tab budget)
5. **Follow-up 12 marzo ore 10-11**: validare grafica e flusso con Alessandra

### Priorita 2 — Completare modulo A (settimane 11-12)

1. **Completare parsing file settimanali** da SFTP
2. **Implementare riaggregazione settimanale** dei dati
3. **Test end-to-end** del flusso settimanale

### Backlog

- Integrazione dati WOW quando Umbra li fornisce (storicita, budget, listino CELIN)
- Sviluppo algoritmo suggerimento WOW
- Frontend modulo marketing
- Tracciamento performance promozioni
- Helper `toManipulateUnit()` in laif-ds — estrarre mapping `"isoWeek" → "week"` duplicato in 3+ punti del Gantt (vedi pattern `dayjs-isoweek-manipulate-mapping`)
- Grafico amcharts5 in WowStoricoPage — delta performance per fornitore nel tempo (amcharts5 già in uso)
- PR laif-ds: esportare `RawGanttDataType` nel barrel export (vedi `knowledge/problemi-tecnici/laif-ds-type-export.md`)

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
