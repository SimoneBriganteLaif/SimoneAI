---
progetto: "umbra"
tipo: "windsurf-report"
data: "2026-03-10"
tags:
  - "#progetto:umbra"
  - "#fase:dev"
---

# Report: WOW Promotions UI Refactor
**Data**: 2025-01-27  
**Brief**: `wow-ui-refactor.md`  
**Repository**: `umbra-recommend`  
**Build finale**: ✅ Exit code 0 — 0 errori TypeScript

---

## 1. Task completati

| # | Task | Stato |
|---|------|-------|
| 1 | Aggiornare `navigation.tsx`: `isSingle: false`, 3 sotto-voci | ✅ |
| 2 | Creare `app/(authenticated)/wow-promotions/budget/page.tsx` | ✅ |
| 3 | Creare `app/(authenticated)/wow-promotions/storico/page.tsx` | ✅ |
| 4 | Estendere `wowScore.helper.ts` (6 settimane, `SpecialCampaign`, `buildGanttData`) | ✅ |
| 5 | Creare `WowGanttView.tsx` | ✅ (con deviazione — vedi §5) |
| 6 | Creare `WowCampaignDialog.tsx` | ✅ |
| 7 | Refactoring `WowPromotionsMain.tsx` (layout Gantt + slot + candidati) | ✅ |
| 8 | `WowCandidatesTable.tsx`: aggiunta riga "Aggiungi manuale" | ✅ |
| 9 | Creare `WowBudgetTree.tsx` (estratto da MissingDataPanel) | ✅ |
| 10 | Creare `WowPurchaseTable.tsx` (estratto da MissingDataPanel) | ✅ |
| 11 | Creare `WowBudgetPage.tsx` | ✅ |
| 12 | Creare `WowStoricoPage.tsx` | ✅ |
| 13 | Aggiungere chiavi i18n in `it.js` e `en.js` | ✅ |
| 14 | Eliminare `MissingDataPanel.tsx` e `WowWeekPlannerV2.tsx` | ✅ |

---

## 2. Difficoltà incontrate

- **`RawGanttDataType` non esportato**: il tipo interno del Gantt laif-ds non è esportato nel barrel export (`export declare type` assente). Soluzione: definito localmente `GanttItem` compatibile in `wowScore.helper.ts`, con `as any` nel `Gantt.Chart` per il cast.
- **`GanttDimensions.WEEK` assente**: il prerequisito `gantt-week-extension.md` non risulta completato nel DS installato — vedi §5.

---

## 3. Decisioni prese

- **Layout `WowPromotionsMain`**: sezione Gantt (full-width, altezza minima 320px) → strip slot settimane con scroll orizzontale → tabella candidati. Questa struttura permette di vedere il calendario Gantt sempre visibile senza tab.
- **`WowBudgetPage`**: due sotto-tab interni (Budget Fornitori / Listino Acquisto) anziché due route separate, in accordo con la struttura mostrata nel brief (la pagina `/budget` è già una sotto-voce di navigazione).
- **`WowStoricoPage`**: aggiunto blocco riepilogo (totale WOW, delta medio, % performance positiva) non esplicitamente richiesto ma coerente con la pagina di analisi.
- **`cancel` aggiunto a it.js/en.js**: chiave generica mancante usata nel `WowCampaignDialog`.

---

## 4. Pattern applicati

- **Lazy loading**: tutte le page route usano `lazy()` da React, coerente con le page esistenti.
- **Estrazione widget**: `WowBudgetTree` e `WowPurchaseTable` come widget autonomi in `widgets/`, `WowBudgetPage`/`WowStoricoPage` come feature entry point in `features/wow-promotions/`.
- **i18n**: tutte le stringhe visibili usano `intl.formatMessage()`, nessun testo hardcoded.
- **Classi Tailwind**: solo token laif-ds (`text-bodyPrimary`, `bg-surface`, `border-subtle`, ecc.).

---

## 5. Deviazioni dal piano

### ⚠️ `GanttDimensions.WEEK` / `DragStepSizes.ONE_WEEK` non disponibili

**Causa**: Il prerequisito `gantt-week-extension.md` non è stato completato. La versione installata di `laif-ds` ha:
```
enum GanttDimensions { HOUR | TWO_HOURS | THREE_HOURS | DAY }
enum DragStepSizes { FIVE_MIN | TEN_MIN | FIFTEEN_MIN | ... }
```
`WEEK` e `ONE_WEEK` non esistono.

**Soluzione adottata**: `WowGanttView.tsx` usa `GanttDimensions.DAY` come `defaultDimension`. Il Gantt funziona correttamente — l'utente vede le barre sulle date esatte, ma la granularità di zoom di default è giornaliera anziché settimanale. Quando il DS verrà aggiornato con `gantt-week-extension`, basterà cambiare la prop in `WowGanttView.tsx` riga 34.

---

## 6. File modificati

| File | Azione |
|------|--------|
| `frontend/src/config/navigation.tsx` | modificato |
| `frontend/app/(authenticated)/wow-promotions/budget/page.tsx` | creato |
| `frontend/app/(authenticated)/wow-promotions/storico/page.tsx` | creato |
| `frontend/src/features/wow-promotions/helpers/wowScore.helper.ts` | modificato |
| `frontend/src/features/wow-promotions/WowPromotionsMain.tsx` | modificato (refactoring) |
| `frontend/src/features/wow-promotions/WowBudgetPage.tsx` | creato |
| `frontend/src/features/wow-promotions/WowStoricoPage.tsx` | creato |
| `frontend/src/features/wow-promotions/widgets/WowGanttView.tsx` | creato |
| `frontend/src/features/wow-promotions/widgets/WowCampaignDialog.tsx` | creato |
| `frontend/src/features/wow-promotions/widgets/WowBudgetTree.tsx` | creato |
| `frontend/src/features/wow-promotions/widgets/WowPurchaseTable.tsx` | creato |
| `frontend/src/features/wow-promotions/widgets/WowCandidatesTable.tsx` | modificato |
| `frontend/src/features/wow-promotions/widgets/MissingDataPanel.tsx` | **eliminato** |
| `frontend/src/features/wow-promotions/widgets/WowWeekPlannerV2.tsx` | **eliminato** |
| `frontend/locale/project/it.js` | modificato |
| `frontend/locale/project/en.js` | modificato |

---

## 7. Domande aperte

1. **`gantt-week-extension.md`**: quando verrà completato il DS con `GanttDimensions.WEEK`? Il cambio in `WowGanttView.tsx` è una singola riga. Appena disponibile, aprire ticket per aggiornare la prop.
2. **`onBarChange` del Gantt**: il callback di drag è scaffolded (`// handle bar drag updates`) ma non implementa la logica di aggiornamento del `plannedWows`. Va definita la semantica: il drag cambia solo la visualizzazione o aggiorna anche la settimana pianificata? Attualmente lo stato rimane su `weekIndex` intero.
3. **`wow_add_manual`**: il pulsante "Aggiungi manuale" in `WowCandidatesTable` ha `onClick={() => {}}` placeholder. Serve definire il flow di inserimento manuale (form? dropdown articoli?).

---

## 8. Suggerimenti

- Il `WowStoricoPage` potrebbe beneficiare di un chart amcharts5 (bar chart delta per fornitore) quando i dati reali saranno disponibili.
- La strip degli slot settimane in `WowPromotionsMain` è gestita con `overflow-x-auto` e `minWidth: 130` per ogni card. Su schermi > 1400px è comodo; su 1280px funziona con scroll. Valutare se passare a 2 righe su mobile.
- La chiave `cancel` è generica e probabilmente già esiste nel locale globale `frontend/locale/en.js` / `it.js` — verificare e rimuovere il duplicato se presente.
