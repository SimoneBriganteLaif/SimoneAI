---
progetto: "umbra"
tipo: "windsurf-brief"
data: "2026-03-10"
tags:
  - "#progetto:umbra"
  - "#fase:dev"
---

# Windsurf Development Brief

> Windsurf: questo file e il brief completo per lo sviluppo. Contiene tutto
> il contesto necessario. NON serve accesso ad altri file di documentazione.
> Alla fine trovi un template di report da compilare quando hai finito.

---

## Metadata

| Campo | Valore |
|-------|--------|
| Progetto | umbra (laif-ds — design system) |
| Requisito | Fase 0 — Estensione Gantt con dimensione WEEK |
| Data brief | 2026-03-10 |
| Repository | `/Users/simonebrigante/LAIF/repo/ds/` |
| Stack | React 19, TypeScript, Storybook, dayjs, react-window |

---

## 1. Obiettivo feature

Aggiungere la dimensione **WEEK** al componente Gantt di laif-ds, cosi che possa essere usato come vista settimanale per la pianificazione promozioni WOW del progetto Umbra. Attualmente il Gantt supporta zoom da 1 ora fino a 1 giorno — serve estenderlo per mostrare scale settimanali (header: "W11 — 10-16 mar", step: ogni giorno della settimana) e supportare drag a step di 1 settimana.

---

## 2. Contesto tecnico

### Architettura attuale

Il componente Gantt e in `src/components/ui/gantt/` ed e strutturato cosi:

```
gantt/
├── components/
│   ├── Gantt/          # Provider + container
│   │   ├── Gantt.tsx   # Root component (<Gantt>, <Gantt.Controls/>, <Gantt.Chart/>)
│   │   └── GanttContext.tsx
│   └── Chart/
│       ├── Scale/Scale.tsx    # Header della scala temporale (virtualizzato con react-window)
│       ├── Grid/              # Griglia delle righe
│       └── Bar/               # Barre draggabili
├── constants/
│   ├── GanttConsts.tsx         # ROW_HEIGHT, HEADER_HEIGHT, TREE_WIDTH, SECONDS_IN_HOUR, ecc.
│   ├── DimensionsSettings.tsx  # Config per ogni dimensione (px, step, secondsInPixel)
│   └── DragStepOptions.tsx     # Secondi per ogni DragStepSize
├── enums/
│   ├── GanttDimensions.tsx     # HOUR..DAY — da estendere con WEEK
│   ├── GanttUnitOfTimes.tsx    # DAY, MONTH — da estendere con WEEK
│   └── DragStepSizes.tsx       # FIVE_MIN..ONE_DAY — da estendere con ONE_WEEK
├── hooks/
│   └── useGanttCalculate.tsx   # Calcola griglia e scroll offset per una dimensione
├── utils/
│   ├── getScaleDates.tsx       # Genera array di date per la scala
│   ├── getScaleItems.tsx       # Genera label dei sotto-step della scala
│   └── getInitialScrollOffset.tsx  # Calcola scroll iniziale
└── types/
    └── GanttData.ts            # RawGanttDataType, GanttDataType
```

### Codice esistente rilevante

**`enums/GanttDimensions.tsx`** — Le dimensioni di zoom attualmente supportate:
```typescript
export enum GanttDimensions {
  HOUR = "hour",
  TWO_HOURS = "twoHours",
  THREE_HOURS = "threeHours",
  FOUR_HOURS = "fourHours",
  SIX_HOURS = "sixHours",
  EIGHT_HOURS = "eightHours",
  TWELVE_HOURS = "twelveHours",
  DAY = "day",
}
```

**`enums/GanttUnitOfTimes.tsx`** — Unita di tempo per la scala:
```typescript
export enum GanttUnitOfTimes {
  DAY = "day",
  MONTH = "month",
}
```

**`enums/DragStepSizes.tsx`** — Step di snap per il drag:
```typescript
export enum DragStepSizes {
  FIVE_MIN = "FIVE_MIN",
  TEN_MIN = "TEN_MIN",
  FIFTEEN_MIN = "FIFTEEN_MIN",
  TWENTY_MIN = "TWENTY_MIN",
  THIRTY_MIN = "THIRTY_MIN",
  ONE_HOUR = "ONE_HOUR",
  EIGHT_HOURS = "EIGHT_HOURS",
  TWELVE_HOURS = "TWELVE_HOURS",
  ONE_DAY = "ONE_DAY",
}
```

**`constants/DimensionsSettings.tsx`** — Config per dimensione. Esempio DAY (l'ultimo attualmente):
```typescript
[GanttDimensions.DAY]: {
  value: 7,
  hours: 24,
  label: "1 day",
  unitOfTime: GanttUnitOfTimes.MONTH,
  itemsCount: 11,
  stepWidth: GanttConsts.SCALE_STEP_DEFAULT_WIDTH,
  scaleStepItems: GanttConsts.HOURS_IN_DAY / 24,
  secondsInPixel:
    (GanttConsts.SECONDS_IN_HOUR * 24) / GanttConsts.SCALE_STEP_DEFAULT_WIDTH,
},
```

**`constants/GanttConsts.tsx`**:
```typescript
export const GanttConsts = {
  ROW_HEIGHT: 40,
  HEADER_HEIGHT: 50,
  TREE_WIDTH: 300,
  LEAF_TITLE_PADDING_LEFT: 50,
  LEAF_CHILDREN_PADDING_LEFT: 5,
  SCALE_STEP_DEFAULT_WIDTH: 50,
  SECONDS_IN_HOUR: 3600,
  SECONDS_IN_DAY: 86400,
  HOURS_IN_DAY: 24,
  MIN_SCROLL_OFFSET: 2400,
  SCALE_STEP_RATIO: 1.6,
};
```

**`constants/DragStepOptions.tsx`** — Secondi per step. Ultimo entry:
```typescript
[DragStepSizes.ONE_DAY]: {
  seconds: 24 * 60 * 60,
  label: "1 day",
},
```

**`utils/getScaleDates.tsx`** — Genera le date della scala. Usa `dayjs.startOf(unitOfTime)`:
```typescript
export const getScaleDates = (
  startDate = dayjs().unix(),
  count = 99,
  unitOfTime: dayjs.ManipulateType = GanttUnitOfTimes.DAY,
) => {
  const data: number[] = [];
  for (let i = 0; i < count; i++) {
    data.push(
      dayjs
        .unix(startDate)
        .startOf(unitOfTime)
        .subtract(Math.floor(count / 2) - i, unitOfTime)
        .unix(),
    );
  }
  return data;
};
```

**NOTA**: `dayjs.startOf("week")` e `dayjs.add(N, "week")` sono supportati nativamente da dayjs (con plugin `weekOfYear` se serve `dayjs().week()`). Assicurarsi che il plugin `isoWeek` sia importato per avere lunedi come primo giorno della settimana.

**`utils/getScaleItems.tsx`** — Genera le label dei sotto-step. Attualmente gestisce solo `DAY` e `MONTH`:
```typescript
export const getScaleItems = (dimension: GanttDimensions, date: number) => {
  const period = GanttDimensionsSettings[dimension].unitOfTime;
  switch (period) {
    case GanttUnitOfTimes.DAY: {
      // genera ore ("00", "01"..."23" o range "00-06", "06-12"...)
    }
    case GanttUnitOfTimes.MONTH: {
      // genera giorni del mese ("01", "02"..."28/30/31")
    }
    default:
      return [];
  }
};
```

**`utils/getInitialScrollOffset.tsx`** — Calcola lo scroll iniziale per centrare la data corrente:
```typescript
export const getInitialScrollOffset = (
  dimension: GanttDimensions,
  scaleDates: number[],
  currentDate?: number,
) => {
  const { secondsInPixel, unitOfTime } = GanttDimensionsSettings[dimension];
  const secondsBeforeCurrentDate =
    (currentDate || dayjs().unix()) -
    dayjs.unix(scaleDates[0]).startOf(unitOfTime).unix();
  return (
    Math.round(secondsBeforeCurrentDate / secondsInPixel) -
    GanttConsts.TREE_WIDTH
  );
};
```

**`components/Chart/Scale/Scale.tsx`** — Render della scala. I punti chiave:

1. `getItemSize` — calcola la larghezza di ogni item della scala:
```typescript
if (settings.dimension === GanttDimensions.DAY) {
  const days = date.daysInMonth();
  return days * settings.stepWidth;
}
return settings.scaleStepItems * settings.stepWidth;
```

2. Formato label — attualmente:
```typescript
dayjs.unix(data[index]).format(
  settings.dimension === GanttDimensions.DAY
    ? "MMMM, YYYY"
    : "ddd, D MMMM, YY",
)
```

3. `onScroll` — gestione infinite scroll (aggiunge date ai bordi):
```typescript
if (settings.dimension === GanttDimensions.DAY) {
  const days = newDate.daysInMonth();
  newItemWidth = days * settings.stepWidth;
}
```

**`hooks/useGanttCalculate.tsx`** — Ricalcola tutto quando cambia dimensione:
```typescript
const calculate = useCallback(
  (dimension: GanttDimensions) => {
    const { stepWidth, itemsCount, scaleStepItems, secondsInPixel, unitOfTime } =
      GanttDimensionsSettings[dimension];
    const newScaleDates = getScaleDates(currentDate, itemsCount, unitOfTime);
    const initialScrollOffset = getInitialScrollOffset(dimension, newScaleDates, currentDate);
    const gridSize = DragStepOptions[settings.dragStepSize].seconds / secondsInPixel;
    setSettings({ stepWidth, initialScrollOffset, scaleStepItems, secondsInPixel, dimension, ... });
    setScaleDates(newScaleDates);
    wrapRef.current?.scrollTo({ left: initialScrollOffset });
  },
  [currentDate, setScaleDates, setSettings, settings.dragStepSize, wrapRef],
);
```

**Storybook — API d'uso**:
```tsx
// Default
<Gantt><Gantt.Controls /><Gantt.Chart data={sampleData} /></Gantt>

// Con defaults personalizzati
<Gantt draggable={true} defaultDimension={GanttDimensions.DAY} defaultDragStepSize={DragStepSizes.ONE_DAY}>
  <Gantt.Controls />
  <Gantt.Chart data={sampleData} />
</Gantt>

// Data format
const sampleData: RawGanttDataType[] = [
  {
    key: "task-1",
    title: "Ricerca e pianificazione",
    data: {
      startDate: "2025-04-01T08:00:00.000Z",
      endDate: "2025-04-05T18:00:00.000Z",
    },
    leftRender: (barData) => <span>...</span>, // opzionale
  },
];
```

---

## 3. Task list

Implementa in questo ordine (le dipendenze sono esplicite):

| # | Task | Dipende da | File coinvolti | Tipo |
|---|------|------------|----------------|------|
| 1 | Aggiungere `WEEK = "week"` all'enum `GanttDimensions` | - | `src/components/ui/gantt/enums/GanttDimensions.tsx` | modifica |
| 2 | Aggiungere `WEEK = "week"` all'enum `GanttUnitOfTimes` | - | `src/components/ui/gantt/enums/GanttUnitOfTimes.tsx` | modifica |
| 3 | Aggiungere `ONE_WEEK = "ONE_WEEK"` all'enum `DragStepSizes` | - | `src/components/ui/gantt/enums/DragStepSizes.tsx` | modifica |
| 4 | Aggiungere `SECONDS_IN_WEEK: 604800` e `DAYS_IN_WEEK: 7` a `GanttConsts` | - | `src/components/ui/gantt/constants/GanttConsts.tsx` | modifica |
| 5 | Aggiungere entry `ONE_WEEK` in `DragStepOptions` con `seconds: 7 * 24 * 60 * 60` | #3 | `src/components/ui/gantt/constants/DragStepOptions.tsx` | modifica |
| 6 | Aggiungere entry `WEEK` in `GanttDimensionsSettings` | #1, #2, #4 | `src/components/ui/gantt/constants/DimensionsSettings.tsx` | modifica |
| 7 | Aggiornare `getScaleDates` per gestire `unitOfTime: "week"` | #2 | `src/components/ui/gantt/utils/getScaleDates.tsx` | modifica |
| 8 | Aggiungere case `WEEK` in `getScaleItems` — generare 7 label giornaliere (lun, mar, ..., dom) | #1, #2 | `src/components/ui/gantt/utils/getScaleItems.tsx` | modifica |
| 9 | Aggiornare `getInitialScrollOffset` per gestire la dimensione WEEK | #1, #6 | `src/components/ui/gantt/utils/getInitialScrollOffset.tsx` | modifica |
| 10 | Aggiornare `Scale.tsx` per gestire la dimensione WEEK (getItemSize, label format, onScroll) | #1, #6, #8 | `src/components/ui/gantt/components/Chart/Scale/Scale.tsx` | modifica |
| 11 | Aggiornare `useGanttCalculate.tsx` — nessuna modifica logica necessaria se i settings sono corretti, ma verificare che funzioni con WEEK | #6 | `src/components/ui/gantt/hooks/useGanttCalculate.tsx` | verifica |
| 12 | Importare plugin dayjs `isoWeek` (se non gia presente) per `startOf("isoWeek")` con lunedi come primo giorno | - | File di setup dayjs o direttamente nei file che usano dayjs | modifica |
| 13 | Creare story Storybook `gantt-chart-weekly.stories.tsx` con dati mock settimanali | #1-#10 | `src/components/stories/gantt-chart-weekly.stories.tsx` | nuovo |

### Dettagli implementativi per i task chiave:

#### Task 6 — DimensionsSettings per WEEK

La logica segue il pattern di DAY. DAY usa `unitOfTime: MONTH` (la scala mostra mesi, con giorni come step). Analogamente, WEEK usa `unitOfTime: WEEK` (la scala mostra settimane, con giorni come step):

```typescript
[GanttDimensions.WEEK]: {
  value: 8, // successivo a DAY (7)
  hours: 24 * 7, // 168 ore
  label: "1 week",
  unitOfTime: GanttUnitOfTimes.WEEK,
  itemsCount: 11,
  stepWidth: GanttConsts.SCALE_STEP_DEFAULT_WIDTH,
  scaleStepItems: GanttConsts.DAYS_IN_WEEK, // 7 step (giorni) per ogni settimana
  secondsInPixel:
    GanttConsts.SECONDS_IN_WEEK / (GanttConsts.DAYS_IN_WEEK * GanttConsts.SCALE_STEP_DEFAULT_WIDTH),
},
```

**Nota**: `secondsInPixel` = secondi_in_settimana / (7_giorni * 50px_per_giorno) = 604800 / 350 ≈ 1728 secondi/px. Questo da una settimana larga 350px (7 × 50px), ragionevole per la visualizzazione.

#### Task 7 — getScaleDates per WEEK

dayjs supporta `"week"` come ManipulateType. Per avere lunedi come primo giorno, usa `startOf("isoWeek")` (richiede plugin `isoWeek`):

```typescript
// Il codice esistente gia funziona con "week" perche usa dayjs genericamente:
// dayjs.unix(startDate).startOf(unitOfTime).subtract(...)
// MA: per garantire che la settimana inizi di lunedi, serve che:
// - Il plugin isoWeek sia caricato
// - Si usi "isoWeek" invece di "week" come unitOfTime
```

**Opzione raccomandata**: usare `"isoWeek"` come valore in GanttUnitOfTimes (o fare un mapping interno), cosi che `startOf("isoWeek")` parta da lunedi. Alternativamente, configurare dayjs locale con lunedi come primo giorno.

#### Task 8 — getScaleItems per WEEK

```typescript
case GanttUnitOfTimes.WEEK: {
  // 7 giorni, label = abbreviazione giorno (Lun, Mar, Mer...)
  return new Array(7).fill(0).map((_item, index) => {
    return dayjs.unix(date).startOf("isoWeek").add(index, "day").format("dd"); // "Lu", "Ma", "Me"...
  });
}
```

#### Task 10 — Scale.tsx per WEEK

In `getItemSize`:
```typescript
if (settings.dimension === GanttDimensions.WEEK) {
  return GanttConsts.DAYS_IN_WEEK * settings.stepWidth; // 7 * 50 = 350px
}
```

In render label:
```typescript
// Formato: "W12 — 16-22 mar 2026"
if (settings.dimension === GanttDimensions.WEEK) {
  const weekStart = dayjs.unix(data[index]);
  const weekEnd = weekStart.add(6, "day");
  const weekNum = weekStart.isoWeek();
  return `W${weekNum} — ${weekStart.format("D")}-${weekEnd.format("D MMM")}`;
}
```

In `onScroll` (gestione infinite scroll):
```typescript
if (settings.dimension === GanttDimensions.WEEK) {
  newItemWidth = GanttConsts.DAYS_IN_WEEK * settings.stepWidth;
}
```

#### Task 12 — Plugin dayjs isoWeek

Verificare se dayjs gia importa il plugin `isoWeek`. Se no, aggiungerlo dove dayjs viene configurato:

```typescript
import dayjs from "dayjs";
import isoWeek from "dayjs/plugin/isoWeek";
dayjs.extend(isoWeek);
```

#### Task 13 — Story settimanale

```tsx
const weeklyData: RawGanttDataType[] = [
  {
    key: "studio",
    title: "Studio",
    children: [
      {
        key: "studio-w12",
        title: "KERR — OptiBond FL",
        data: {
          startDate: "2026-03-16T00:00:00.000Z",
          endDate: "2026-03-29T23:59:59.000Z",
        },
      },
      {
        key: "studio-w14",
        title: "IVOCLAR — IPS Empress A2",
        data: {
          startDate: "2026-03-30T00:00:00.000Z",
          endDate: "2026-04-13T23:59:59.000Z",
        },
      },
    ],
  },
  {
    key: "laboratorio",
    title: "Laboratorio",
    children: [
      {
        key: "lab-w12",
        title: "IVOCLAR — IPS e.max",
        data: {
          startDate: "2026-03-16T00:00:00.000Z",
          endDate: "2026-03-29T23:59:59.000Z",
        },
      },
    ],
  },
  {
    key: "speciali",
    title: "Campagne Speciali",
    children: [
      {
        key: "pasqua",
        title: "Sorprese di Pasqua",
        data: {
          startDate: "2026-03-20T00:00:00.000Z",
          endDate: "2026-04-03T23:59:59.000Z",
        },
      },
    ],
  },
];

export const Weekly: Story = {
  render: () => (
    <div className="h-[500px]">
      <Gantt
        draggable={true}
        defaultDimension={GanttDimensions.WEEK}
        defaultDragStepSize={DragStepSizes.ONE_WEEK}
        treeTitle="Linee WOW"
      >
        <Gantt.Controls />
        <Gantt.Chart data={weeklyData} />
      </Gantt>
    </div>
  ),
};
```

---

## 4. Convenzioni LAIF (obbligatorie)

### Frontend

- Usare SOLO token Tailwind del DS (mai classi vanilla)
- Preferire componenti `@laif/ds` su shadcn/ui raw
- Hook custom per logica riutilizzabile
- No prop drilling (usare Redux o Context)
- Naming: PascalCase componenti, camelCase hooks (.hook.ts), kebab-case cartelle

### Per questo progetto specifico (laif-ds)

- Seguire le convenzioni Storybook esistenti (Meta, StoryObj, tags: ["autodocs"])
- Non modificare l'API pubblica del componente se non strettamente necessario
- Le nuove enum values devono seguire il pattern esistente (SCREAMING_SNAKE per DragStepSizes, camelCase per GanttDimensions, lowercase per GanttUnitOfTimes)
- Verificare che la build (`npm run build` o equivalente) compili senza errori

---

## 5. Pattern da applicare

Non ci sono pattern specifici dalla KB applicabili a questa estensione. Seguire i pattern gia presenti nel codice del Gantt:

- **Pattern DimensionsSettings**: ogni nuova dimensione segue la struttura `{ value, hours, label, unitOfTime, itemsCount, stepWidth, scaleStepItems, secondsInPixel }`
- **Pattern Scale rendering**: DAY e l'unico case speciale per `getItemSize` e label format; WEEK diventa il secondo case speciale
- **Pattern dayjs**: tutto il date handling usa dayjs con timestamp unix — mantenere lo stesso pattern

---

## 6. Criteri di accettazione

- [ ] `GanttDimensions.WEEK` esiste e funziona come dimensione di zoom
- [ ] Lo zoom WEEK mostra header settimanali con formato "W12 — 16-22 mar"
- [ ] Ogni settimana ha 7 sotto-step (uno per giorno, label abbreviata)
- [ ] Le settimane iniziano di lunedi (ISO week)
- [ ] `DragStepSizes.ONE_WEEK` funziona: le barre snappano a settimane intere
- [ ] Lo scroll infinito (aggiunta settimane ai bordi) funziona come per DAY/MONTH
- [ ] La story Storybook `Weekly` mostra 3 gruppi (Studio, Laboratorio, Campagne Speciali) con barre di durata 2 settimane
- [ ] Tutte le stories esistenti continuano a funzionare (nessuna regressione)
- [ ] Il build del progetto compila senza errori
- [ ] I controlli zoom nel componente `Gantt.Controls` includono l'opzione WEEK

---

## 7. Rischi e note

- **dayjs `startOf("week")`** parte da domenica di default. Serve `isoWeek` per partire da lunedi. Verifica che il plugin sia esteso globalmente, altrimenti il calcolo delle date sara sbagliato.
- **Larghezza settimana**: 7 × 50px = 350px per settimana. Se risulta troppo largo o stretto, regola `stepWidth` nel settings. Potresti dover usare `SCALE_STEP_DEFAULT_WIDTH * ratio` come fanno le altre dimensioni.
- **`getScaleDates` con "week"**: dayjs accetta "week" come `ManipulateType`, ma `startOf("week")` e sensibile al locale. Preferisci `startOf("isoWeek")` che e sempre lunedi. Questo potrebbe richiedere un mapping interno in `getScaleDates`: se `unitOfTime === "week"` usa `"isoWeek"` per `startOf`.
- **Controls**: il componente `Gantt.Controls` probabilmente genera le opzioni zoom dall'enum `GanttDimensions` o da `GanttDimensionsSettings`. Verifica che WEEK appaia automaticamente nel selector. Se le opzioni sono hardcoded, aggiungila.
- **Value ordering**: `GanttDimensions.WEEK.value = 8` (successivo a DAY = 7). Verifica che i controls usino `value` per l'ordinamento zoom.

---

## 8. File da creare / modificare (riepilogo)

### Nuovi file
- `src/components/stories/gantt-chart-weekly.stories.tsx` — Story Storybook per vista settimanale

### File da modificare
- `src/components/ui/gantt/enums/GanttDimensions.tsx` — Aggiungere WEEK
- `src/components/ui/gantt/enums/GanttUnitOfTimes.tsx` — Aggiungere WEEK
- `src/components/ui/gantt/enums/DragStepSizes.tsx` — Aggiungere ONE_WEEK
- `src/components/ui/gantt/constants/GanttConsts.tsx` — Aggiungere SECONDS_IN_WEEK, DAYS_IN_WEEK
- `src/components/ui/gantt/constants/DimensionsSettings.tsx` — Aggiungere entry WEEK
- `src/components/ui/gantt/constants/DragStepOptions.tsx` — Aggiungere entry ONE_WEEK
- `src/components/ui/gantt/utils/getScaleDates.tsx` — Gestire "week" / "isoWeek"
- `src/components/ui/gantt/utils/getScaleItems.tsx` — Aggiungere case WEEK (7 giorni)
- `src/components/ui/gantt/utils/getInitialScrollOffset.tsx` — Gestire dimensione WEEK
- `src/components/ui/gantt/components/Chart/Scale/Scale.tsx` — Gestire WEEK (getItemSize, label format, onScroll)
- File setup dayjs (se non gia presente) — Aggiungere plugin `isoWeek`

---

## 9. Template Report Feedback

> Quando hai finito, compila questo template e passalo a Claude Code.
> Puoi salvarlo come `gantt-week-extension-report.md` nella stessa cartella del brief
> oppure copiarlo direttamente in chat a Claude Code.

### Windsurf Report — Fase 0 — Estensione Gantt con dimensione WEEK

#### Metadata

| Campo | Valore |
|-------|--------|
| Data completamento | [YYYY-MM-DD] |
| Tempo stimato | [ore] |
| Completamento task | [N/13 completati] |

#### 1. Task completati

| # | Task | Stato | Note |
|---|------|-------|------|
| 1 | Aggiungere WEEK a GanttDimensions | completato / parziale / saltato | [note] |
| 2 | Aggiungere WEEK a GanttUnitOfTimes | completato / parziale / saltato | [note] |
| 3 | Aggiungere ONE_WEEK a DragStepSizes | completato / parziale / saltato | [note] |
| 4 | Aggiungere costanti SECONDS_IN_WEEK, DAYS_IN_WEEK | completato / parziale / saltato | [note] |
| 5 | Aggiungere ONE_WEEK a DragStepOptions | completato / parziale / saltato | [note] |
| 6 | Aggiungere WEEK a DimensionsSettings | completato / parziale / saltato | [note] |
| 7 | Aggiornare getScaleDates per WEEK | completato / parziale / saltato | [note] |
| 8 | Aggiungere case WEEK in getScaleItems | completato / parziale / saltato | [note] |
| 9 | Aggiornare getInitialScrollOffset per WEEK | completato / parziale / saltato | [note] |
| 10 | Aggiornare Scale.tsx per WEEK | completato / parziale / saltato | [note] |
| 11 | Verificare useGanttCalculate per WEEK | completato / parziale / saltato | [note] |
| 12 | Importare plugin dayjs isoWeek | completato / parziale / saltato | [note] |
| 13 | Creare story Storybook Weekly | completato / parziale / saltato | [note] |

#### 2. Difficolta incontrate

Per ogni difficolta significativa:

**Difficolta: [titolo]**
- **Problema**: [cosa non funzionava]
- **Causa**: [perche]
- **Soluzione adottata**: [come hai risolto]
- **Tempo perso**: [stima]
- **Ricorrente?**: [si/no — potrebbe ripresentarsi in altri progetti?]

#### 3. Decisioni prese

Per ogni decisione tecnica non prevista dal piano:

**Decisione: [titolo]**
- **Contesto**: [perche serviva decidere]
- **Alternativa scelta**: [cosa hai scelto]
- **Alternative scartate**: [cosa hai considerato]
- **Motivazione**: [perche questa scelta]

#### 4. Pattern individuati

Per ogni soluzione che potrebbe essere riutilizzabile:

**Pattern: [nome suggerito]**
- **Problema che risolve**: [descrizione]
- **Soluzione**: [come funziona]
- **Riutilizzabile?**: [si — in quali contesti]

#### 5. Deviazioni dal piano

- [file/componente]: [cosa e cambiato rispetto al piano e perche]

#### 6. File creati e modificati

**Nuovi file:**
- `path/file.ext` — [scopo]

**File modificati:**
- `path/file.ext` — [cosa e cambiato]

#### 7. Domande aperte

- [ ] [domanda irrisolta che richiede una decisione]

#### 8. Suggerimenti

- [suggerimento per migliorare codice, processo o architettura]
