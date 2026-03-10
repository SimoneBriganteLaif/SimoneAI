---
problema: "RawGanttDataType non esportato da laif-ds"
categoria: "integrazione"
frequenza: "media"
progetti-dove-si-e-presentato: ["umbra"]
data-creazione: "2026-03-10"
tags:
  - "#problema:integrazione"
  - "#stack:laif-ds"
  - "#stack:typescript"
---

# Problema Ricorrente: RawGanttDataType non esportato da laif-ds

## Descrizione del problema

Il tipo `RawGanttDataType` (struttura dati richiesta dal componente `<Gantt.Chart data={...} />`) non e incluso nel barrel export di laif-ds (`src/index.ts`). I progetti consumer non possono importare il tipo e devono usare workaround.

**Segnali che stai affrontando questo problema**:
- Errore TypeScript quando provi a tipizzare i dati per `Gantt.Chart`
- Il tipo `RawGanttDataType` non e tra gli export di `laif-ds`
- Devi definire un tipo locale compatibile con la struttura Gantt

**Contesto tipico in cui si presenta**:
- Progetti che usano il componente Gantt di laif-ds
- Quando vuoi tipizzare correttamente l'helper che costruisce i dati Gantt

---

## Soluzioni adottate

### Soluzione A: Tipo locale + cast `as any` *(workaround attuale)*

**Quando usarla**: Subito, per non bloccare lo sviluppo.

**Come funziona**: Definire un tipo locale `GanttItem` che replica la struttura attesa da `RawGanttDataType`, e castare con `as any` nel passaggio a `<Gantt.Chart>`.

```typescript
// Tipo locale compatibile
export interface GanttItem {
  key: string;
  title: string;
  data: {
    startDate: string;
    endDate: string;
    color?: string;
  };
  children?: GanttItem[];
}

// Uso nel JSX
<Gantt.Chart data={ganttData as any} />
```

**Risultati ottenuti in LAIF**: Funziona ma perde type safety. Eventuali breaking change nel tipo interno non vengono catturate a compile time.

---

### Soluzione B: PR verso laif-ds per esportare il tipo *(raccomandata)*

**Quando usarla**: Appena possibile, come fix permanente.

**Come funziona**: Aggiungere `RawGanttDataType` (e altri tipi Gantt utili) al barrel export in `src/index.ts` di laif-ds.

**Perché è seconda scelta**: Richiede una PR, review, e nuova release di laif-ds. Non e un fix immediato.

---

## Soluzioni che NON hanno funzionato

- **Importare direttamente dal path interno**: `import { RawGanttDataType } from "laif-ds/src/components/ui/gantt/types"` — non funziona perche il build produce solo `dist/` e i path interni non sono esposti.

---

## Prevenzione

- Quando si aggiunge un componente pubblico a laif-ds, esportare anche tutti i tipi necessari ai consumer
- Verificare che il barrel export includa i tipi delle props e dei dati di ogni componente

---

## Esperienze nei progetti LAIF

| Progetto | Contesto | Soluzione usata | Risultato |
|---------|---------|----------------|----------|
| umbra | WowGanttView.tsx — dati Gantt per promozioni WOW | Tipo locale `GanttItem` + cast `as any` | Funzionante, da risolvere con PR |
