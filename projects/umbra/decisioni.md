---
progetto: "umbra"
tags:
  - "#progetto:umbra"
  - "#fase:dev"
---

# Decisioni Tecniche — Umbra

> **Formato ADR** (Architecture Decision Record).
> Ogni decisione rilevante viene documentata qui nel momento in cui viene presa.
> Aggiornato dalla skill `skills/development/estrazione-decisioni.md`.

---

## Come usare questo file

Aggiungi una sezione per ogni decisione tecnica significativa. Una decisione e "significativa" se:
- Cambia lo stack o introduce una nuova dipendenza
- Influenza come altri componenti vengono scritti
- Ha alternative valide che abbiamo scartato
- Potrebbe essere difficile da cambiare in futuro

---

## Indice decisioni

| ID | Titolo | Data | Stato |
|----|--------|------|-------|
| ADR-001 | GanttUnitOfTimes.WEEK = "isoWeek" | 2026-03-10 | accettata |
| ADR-002 | Layout WowPromotionsMain: Gantt → strip settimane → candidati | 2026-03-10 | accettata |
| ADR-003 | WowBudgetPage con tab interni invece di route separate | 2026-03-10 | accettata |
| ADR-004 | Colori barre Gantt: Tailwind hardcoded invece di token semantici | 2026-03-13 | accettata |
| ADR-005 | Date handling nel Gantt: componenti locali invece di toISOString() | 2026-03-13 | accettata |

---

## ADR-004: Colori barre Gantt — Tailwind hardcoded invece di token semantici

**Data**: 2026-03-13
**Stato**: accettata

**Contesto**: Le barre del Gantt (Studio e Laboratorio) usavano i token semantici laif-ds `bg-info/80` e `bg-success/80`. In light theme questi token mappano su colori molto tenui (quasi trasparenti), rendendo le barre invisibili.

**Decisione**: usare colori Tailwind hardcoded: `bg-blue-500` (Studio) e `bg-emerald-600` (Laboratorio).

**Alternative scartate**:
- Continuare con `bg-info`/`bg-success` senza opacità: il problema persiste perché il token in light mode è già un colore chiaro.
- Usare CSS variables con override per tema: più complesso e accoppiato al design system.

**Trade-off accettato**: i colori non seguono automaticamente eventuali future ribranding del design system. Accettabile perché Studio/Laboratorio hanno identità visiva stabile (blu = Studio, verde = Laboratorio).

---

## ADR-005: Date handling nel Gantt — componenti locali invece di toISOString()

**Data**: 2026-03-13
**Stato**: accettata

**Contesto**: `toDateStr()` in `WowAddPromotionDialog.tsx` usava `d.toISOString().slice(0,10)` per convertire una `Date` in stringa `YYYY-MM-DD`. In timezone UTC+1, la mezzanotte locale è le 23:00 UTC del giorno precedente → la stringa risultante era sempre 1 giorno indietro. Effetto: promozioni create da clic su cella del Gantt iniziavano il giorno prima, e la durata apparente era 13 giorni invece di 14.

**Decisione**: usare `getFullYear()`/`getMonth()`/`getDate()` (componenti locali) per costruire la stringa:
```ts
function toDateStr(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}
```

**Regola generale**: nel Gantt WOW tutte le date sono "date locali senza ora". Non usare mai `toISOString()` per serializzarle — usare sempre i componenti locali.

---

## ADR-001: GanttUnitOfTimes.WEEK = "isoWeek"

**Data**: 2026-03-10
**Stato**: accettata
**Contesto**: Aggiungendo la dimensione WEEK al Gantt di laif-ds, serviva scegliere il valore dell'enum `GanttUnitOfTimes.WEEK`.

**Decisione**: Usare `"isoWeek"` (non `"week"`) come valore enum.

**Alternative considerate**:
- `"week"` — piu semplice, ma `dayjs.startOf("week")` inizia da domenica (locale US di default)
- `"isoWeek"` — esplicito: inizia da lunedi (ISO 8601), coerente con il calendario europeo usato dai clienti LAIF

**Conseguenze**:
- Richiede il plugin `isoWeek` di dayjs
- Necessario mapping `"isoWeek" → "week"` per `ManipulateType` (vedi pattern `dayjs-isoweek-manipulate-mapping`)
- Garantisce coerenza con il calendario italiano/europeo senza dipendere dal locale

---

## ADR-002: Layout WowPromotionsMain: Gantt → strip settimane → candidati

**Data**: 2026-03-10
**Stato**: accettata
**Contesto**: La pagina principale promozioni WOW doveva combinare la vista Gantt con la selezione settimanale e la tabella candidati.

**Decisione**: Layout verticale in 3 sezioni: Gantt full-width in alto, strip slot settimane centrale, tabella candidati in basso.

**Alternative considerate**:
- Tutto in un'unica pagina scrollabile con tutte le sezioni (budget, storico inclusi) — troppo denso
- Gantt e candidati side-by-side — lo spazio orizzontale non basta per il Gantt
- Solo Gantt con drill-down sui singoli slot — troppi click per il workflow quotidiano

**Conseguenze**:
- Budget e Storico separati come pagine (vedi ADR-003)
- La strip slot settimane fa da "ponte" tra vista macro (Gantt) e dettaglio (candidati)
- L'utente puo selezionare una settimana nella strip e vedere i candidati filtrati

---

## ADR-003: WowBudgetPage con tab interni invece di route separate

**Data**: 2026-03-10
**Stato**: accettata
**Contesto**: La pagina Budget doveva mostrare sia il budget gerarchico per fornitore sia il listino acquisti CELIN.

**Decisione**: Una singola route `/wow-promotions/budget` con 2 tab interni: "Budget Fornitori" e "Listino Acquisti".

**Alternative considerate**:
- Due route separate (`/budget/fornitori` e `/budget/listino`) — navigazione piu frammentata, dati correlati separati
- Una pagina unica senza tab — troppo lunga, contesti diversi mescolati

**Conseguenze**:
- Navigazione sidebar piu pulita (un solo item "Budget")
- L'utente puo passare rapidamente tra budget e listino senza cambiare pagina
- Lo stato della pagina (filtri, selezioni) si mantiene cambiando tab
