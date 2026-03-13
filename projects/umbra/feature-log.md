---
progetto: "umbra"
tags:
  - "#progetto:umbra"
  - "#fase:dev"
---

# Feature Log — Umbra

> Registro delle feature completate con note tecniche rilevanti.
> Non e un changelog per il cliente — e un documento interno per il team.
> Aggiornare a ogni feature completata o ogni fine sprint.

---

## Come aggiungere una feature

Aggiungi in cima (ordine cronologico inverso). Includi:
- **Cosa fa** la feature (una riga)
- **Come e implementata** (scelte non ovvie)
- **Problemi incontrati** e come risolti
- **Link al codice** se utile per riferimento futuro

---

## 2026-03-13 — Bug fix e UX Gantt WOW

**Cosa fa**: corregge 3 bug sul Gantt promozioni WOW e migliora la UX generale della pagina.

**Bug risolti**:

1. **Durata promozione 13 giorni invece di 14** — `toDateStr()` in `WowAddPromotionDialog.tsx` usava `toISOString().slice(0,10)` che converte la data locale in UTC, spostando la mezzanotte di un giorno indietro in UTC+1. Fix: usare `getFullYear/getMonth/getDate()` (componenti locali) per costruire la stringa `YYYY-MM-DD`.

2. **Modal pre-selezionato sulla linea sbagliata** — `useState(defaultLine ?? "studio")` inizializza solo al primo mount. Riaprendo il dialog con un `defaultLine` diverso lo stato non si aggiornava. Fix: `useEffect(() => { if (open) { /* reset state */ } }, [open])` che re-sincronizza tutto lo stato ogni volta che il dialog si apre.

3. **Bottone "Oggi" intercettato dalle barre Gantt** — le barre con `z-index: 10` (position: relative) potevano sovrapporsi alla navigation bar. Fix: `isolation: isolate` sul container del grid (crea stacking context isolato) + `z-index: 10` esplicito sulla nav bar.

**Miglioramenti UX**:

- **Barre Gantt invisibili in light theme**: i token semantici `bg-info/80` e `bg-success/80` in light mode mappano su colori molto tenui. Sostituiti con `bg-blue-500` / `bg-emerald-600` (Tailwind hardcoded) che hanno saturazione garantita in entrambi i temi.
- **Celle vuote non sembrano cliccabili**: aggiunto `title="Clicca per pianificare WOW"` + `hover:ring-1 hover:ring-accentPrimary/20` per feedback visivo al hover.
- **Alternanza celle poco visibile in light**: `bg-surfaceSecondary/30` → `/50` per maggiore contrasto.
- **Badge "mock" visibili in produzione**: rimossi i due badge arancioni "mock" da intestazione colonna e cella "ultima WOW" in `WowCandidatesTable`.

**File modificati**:
- `src/features/wow-promotions/widgets/WowAddPromotionDialog.tsx`
- `src/features/wow-promotions/widgets/WowGanttView.tsx`
- `src/features/wow-promotions/widgets/gantt/GanttGrid.tsx`
- `src/features/wow-promotions/widgets/gantt/GanttBar.tsx`
- `src/features/wow-promotions/widgets/WowCandidatesTable.tsx`

---

## 2026-03-13 — UX pagina Budget dettaglio fornitore

**Cosa fa**: aumenta le dimensioni di tutti gli elementi UI e riorganizza la sezione "Totale classi".

**Implementazione**:
- Tutti i testi scala da `text-[10px]`/`text-[11px]` → `text-xs`/`text-sm`
- Input normali: `h-7 w-32` → `h-9 w-36`; input piccoli: `h-6 w-20` → `h-7 w-24`
- "Totale classi" spostato da fondo pagina a sezione dedicata subito dopo "Budget annuo fornitore" (logica: il totale è il confronto diretto col budget fornitore, non una nota a piè di pagina)

**File modificati**:
- `src/features/wow-promotions/WowBudgetDetailPage.tsx`
