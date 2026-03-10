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
| Progetto | umbra-recommend |
| Requisito | Fasi 1-5 — Refactor UI WOW Promotions: Gantt + 3 pagine |
| Data brief | 2026-03-10 |
| Repository | `/Users/simonebrigante/LAIF/repo/umbra-recommend/` |
| Stack | Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS, laif-ds |

---

## 1. Obiettivo feature

Ristrutturare la sezione WOW Promotions da una singola pagina con 2 tab a **3 pagine separate**:

1. **Pianificazione** (`/wow-promotions/`) — Vista Gantt settimanale + pannello candidati sotto
2. **Budget & Vincoli** (`/wow-promotions/budget`) — Budget fornitori (tree espandibile) + listino acquisto CELIN
3. **Storico WOW** (`/wow-promotions/storico`) — Tabella storico promozioni passate con filtri

La pagina principale usa il componente **Gantt di laif-ds** (esteso con dimensione WEEK — vedi brief separato `gantt-week-extension.md`) per visualizzare e pianificare le promozioni su un orizzonte di 6+ settimane. Budget e Storico vengono estratti dall'attuale `MissingDataPanel.tsx` in pagine dedicate.

**PREREQUISITO**: il brief `gantt-week-extension.md` deve essere completato prima. Il Gantt laif-ds deve supportare `GanttDimensions.WEEK` e `DragStepSizes.ONE_WEEK`.

---

## 2. Contesto tecnico

### Architettura attuale

```
frontend/
├── app/(authenticated)/wow-promotions/
│   └── page.tsx                    # Lazy-loads WowPromotionsMain
├── src/features/wow-promotions/
│   ├── WowPromotionsMain.tsx       # Pagina singola con 2 tab (Planning + Missing Data)
│   ├── helpers/
│   │   └── wowScore.helper.ts     # Tipi, mock data, scoring (1415 righe)
│   └── widgets/
│       ├── WowCandidatesTable.tsx  # Tabella candidati con score, budget, azioni
│       ├── WowWeekPlannerV2.tsx    # Planner settimane verticale (da sostituire con Gantt)
│       ├── WowSuggestionCard.tsx   # Card suggerimento (non usata attualmente)
│       └── MissingDataPanel.tsx    # 3 sub-tab: Storico, Budget tree, Listino (845 righe)
├── src/config/navigation.tsx       # Sidebar navigation config
└── locale/project/it.js           # Traduzioni italiane
```

### Struttura target

```
frontend/
├── app/(authenticated)/wow-promotions/
│   ├── page.tsx                    # REFACTOR: Gantt + Candidati
│   ├── budget/
│   │   └── page.tsx                # NUOVO: Budget & Vincoli
│   └── storico/
│       └── page.tsx                # NUOVO: Storico WOW
├── src/features/wow-promotions/
│   ├── WowPromotionsMain.tsx       # REFACTOR: Gantt + Candidati (no tab)
│   ├── WowBudgetPage.tsx           # NUOVO: Budget + Listino
│   ├── WowStoricoPage.tsx          # NUOVO: Storico filtrato
│   ├── helpers/
│   │   └── wowScore.helper.ts     # MODIFICA: estendere settimane, tipo SpecialCampaign
│   └── widgets/
│       ├── WowGanttView.tsx        # NUOVO: wrapper Gantt laif-ds
│       ├── WowCandidatesTable.tsx  # MODIFICA: context-aware
│       ├── WowBudgetTree.tsx       # NUOVO: estratto da MissingDataPanel
│       ├── WowPurchaseTable.tsx    # NUOVO: estratto da MissingDataPanel (listino CELIN)
│       ├── WowCampaignDialog.tsx   # NUOVO: modal campagne speciali
│       └── MissingDataPanel.tsx    # DA ELIMINARE (contenuto distribuito)
```

### Codice esistente rilevante

**`WowPromotionsMain.tsx`** — Componente principale attuale. Stato da mantenere:
```typescript
const [selectedWeekIndex, setSelectedWeekIndex] = useState(0);
const [selectedLine, setSelectedLine] = useState<WowLine>("studio");
const [plannedWows, setPlannedWows] = useState<PlannedWow[]>([]);

// API call per dati marketing
const { data: marketingData, isLoading } = useCustomQuery({
  ...getMarketingItemsByColumnLatestModelResultMarketingAggregateByColumnGroupByPostOptions({
    path: { group_by: "des_fornitore|des_classe|des_sotto_classe" },
    body: {
      ...(selectedRole === "area-manager" && { cod_agente: allowedAgentCodes }),
      skip: 0, limit: 50,
      sort_by: "purchase_priority", sort_order: "desc",
    },
  }),
  placeholderData: keepPreviousData,
});

// Build candidati da dati API
const candidates = useMemo(
  () => buildWowCandidates(marketingData?.items ?? [], plannedWows),
  [marketingData, plannedWows],
);
```

**`wowScore.helper.ts`** — Tipi chiave:
```typescript
export type WowLine = "studio" | "laboratorio";
export type SelectionStatus = "selectable" | "at_limit" | "too_recent" | "already_planned";

export interface WowCandidate {
  id: string;
  des_articolo: string;
  des_fornitore: string;
  des_classe: string;
  des_sotto_classe?: string;
  pred_val_importo: number;
  purchase_priority: number;
  doos: number;
  pred_val_venduta: number;
  line: WowLine;
  wowScore: number;
  motivations: WowMotivation[];
  budgetTarget: number;
  budgetProgress: number;
  budgetImpact: number;
  lastWowDate: Date | null;
  daysSinceLastWow: number | null;
  wowCountThisYear: number;
  maxWowPerYear: number;
  minWowPerYear: number;
  hasTarget: boolean;
  selectionStatus: SelectionStatus;
  selectionBlockReason?: string;
}

export interface WowWeek {
  weekNumber: number;
  startDate: Date;
  endDate: Date;
  label: string;
  shortLabel: string;
}

export interface PlannedWow {
  weekIndex: number;
  line: WowLine;
  candidate: WowCandidate;
}

export interface WowHistoryItem {
  id: string;
  des_fornitore: string;
  des_classe: string;
  line: WowLine;
  startDate: Date;
  endDate: Date;
  budgetImpactActual: number;
  daysAgo: number;
}
```

`getWowWeeks()` attualmente genera **solo 3 settimane**. Va esteso a 6+.

**`navigation.tsx`** — Config sidebar attuale per WOW (da ristrutturare):
```typescript
{
  menuLabel: "wow_promotions",
  headerTitle: "wow_promotions_title",
  headerDescription: "wow_promotions_description",
  headerIcon: "Sparkles",
  private: true,
  menuActivation: "/wow-promotions/",
  permission: ["marketing:read"],
  href: "/wow-promotions/",
  hideTabs: true,
  isSingle: true,  // <-- da cambiare a false per sotto-pagine
  menuIcon: "Sparkles",
  items: [],       // <-- da popolare con 3 sotto-voci
  breadcrumbsArray: [{ label: "wow_promotions", href: "" }],
  tabsArray: [],
},
```

**Tipi navigazione** — da `template/types/navigation.ts`:
```typescript
export interface MenuBase {
  menuActivation?: string;
  menuLabel: string;
  href?: string;
  private: boolean;
  permission: string[];
  menuIcon?: IconName;
  headerIcon?: IconName;
  isHiddenFromMenu?: boolean;
  hideHeader?: boolean;
  hideTabs?: boolean;
  hideBreadcrumb?: boolean;
  breadcrumbsArray?: IBreadcrumb[];
  headerTitle: string;
  headerDescription?: string;
  tabsArray?: ITab[];
  headerCustomComponent?: string;
  hideSidebar?: boolean;
}

export interface MenuItem extends MenuBase {}

export interface MenuRoutesItem extends MenuBase {
  isSingle: boolean;
  items: MenuItem[];
  stickToBottom?: boolean;
}
```

**`page.tsx`** — Entry point attuale (lazy loading):
```typescript
"use client";
import { lazy } from "react";
const WowPromotionsMain = lazy(
  () => import("@/src/features/wow-promotions/WowPromotionsMain"),
);
export default function WowPromotionsPage() {
  return <WowPromotionsMain />;
}
```

**Gantt laif-ds API** (dopo estensione WEEK):
```tsx
import Gantt from "laif-ds/gantt"; // o dal path esportato dal DS
import { GanttDimensions, DragStepSizes } from "laif-ds";
import { RawGanttDataType } from "laif-ds/gantt/types";

<Gantt
  draggable={true}
  defaultDimension={GanttDimensions.WEEK}
  defaultDragStepSize={DragStepSizes.ONE_WEEK}
  treeTitle="Linee WOW"
>
  <Gantt.Controls />
  <Gantt.Chart
    data={ganttData}
    onBarDoubleClick={(bar) => { /* apri dettagli */ }}
    onBarChange={(bar) => { /* aggiorna date dopo drag */ }}
  />
</Gantt>

// Formato dati
const ganttData: RawGanttDataType[] = [
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
        leftRender: (barData) => <Icon name="Beaker" size="xs" />,
      },
    ],
  },
];
```

**NOTA IMPORT**: verifica come laif-ds esporta il Gantt. Potrebbe essere `import { Gantt } from "laif-ds"` o `import Gantt from "laif-ds/components/ui/gantt/components/Gantt/Gantt"`. Controlla gli export del package.

---

## 3. Task list

Implementa in questo ordine (le dipendenze sono esplicite):

### Fase 1 — Routing e navigazione

| # | Task | Dipende da | File coinvolti | Tipo |
|---|------|------------|----------------|------|
| 1 | Aggiornare `navigation.tsx`: impostare `isSingle: false` per WOW Promotions, aggiungere 3 sotto-voci (Pianificazione, Budget, Storico) | - | `src/config/navigation.tsx` | modifica |
| 2 | Creare `app/(authenticated)/wow-promotions/budget/page.tsx` con lazy loading di `WowBudgetPage` | - | `app/(authenticated)/wow-promotions/budget/page.tsx` | nuovo |
| 3 | Creare `app/(authenticated)/wow-promotions/storico/page.tsx` con lazy loading di `WowStoricoPage` | - | `app/(authenticated)/wow-promotions/storico/page.tsx` | nuovo |

### Fase 2 — Gantt + Candidati (pagina principale)

| # | Task | Dipende da | File coinvolti | Tipo |
|---|------|------------|----------------|------|
| 4 | Estendere `wowScore.helper.ts`: `getWowWeeks()` → 6+ settimane; aggiungere tipo `SpecialCampaign`; aggiungere mock campagne speciali; aggiungere funzione `buildGanttData()` che converte `PlannedWow[]` + `SpecialCampaign[]` → `RawGanttDataType[]` | - | `src/features/wow-promotions/helpers/wowScore.helper.ts` | modifica |
| 5 | Creare `WowGanttView.tsx` — wrapper del Gantt laif-ds | #4 | `src/features/wow-promotions/widgets/WowGanttView.tsx` | nuovo |
| 6 | Creare `WowCampaignDialog.tsx` — dialog per aggiungere campagne speciali | - | `src/features/wow-promotions/widgets/WowCampaignDialog.tsx` | nuovo |
| 7 | Refactoring `WowPromotionsMain.tsx` — rimuovere tab, layout Gantt (60%) + Candidati (40%) | #4, #5 | `src/features/wow-promotions/WowPromotionsMain.tsx` | modifica |
| 8 | Aggiornare `WowCandidatesTable.tsx` — aggiungere pulsante "Aggiungi manuale" | - | `src/features/wow-promotions/widgets/WowCandidatesTable.tsx` | modifica |

### Fase 3 — Budget & Vincoli

| # | Task | Dipende da | File coinvolti | Tipo |
|---|------|------------|----------------|------|
| 9 | Creare `WowBudgetTree.tsx` — estrarre il tree espandibile budget da `MissingDataPanel.tsx` (sub-tab "Budget & Vincoli") | - | `src/features/wow-promotions/widgets/WowBudgetTree.tsx` | nuovo |
| 10 | Creare `WowPurchaseTable.tsx` — estrarre la tabella listino acquisto da `MissingDataPanel.tsx` (sub-tab "Listino Acquisto") | - | `src/features/wow-promotions/widgets/WowPurchaseTable.tsx` | nuovo |
| 11 | Creare `WowBudgetPage.tsx` — pagina con 2 tab interni (Budget Fornitori + Listino Acquisto) | #9, #10 | `src/features/wow-promotions/WowBudgetPage.tsx` | nuovo |

### Fase 4 — Storico WOW

| # | Task | Dipende da | File coinvolti | Tipo |
|---|------|------------|----------------|------|
| 12 | Creare `WowStoricoPage.tsx` — estrarre tabella storico da `MissingDataPanel.tsx`, aggiungere filtri e riepilogo | - | `src/features/wow-promotions/WowStoricoPage.tsx` | nuovo |

### Fase 5 — i18n, cleanup, polish

| # | Task | Dipende da | File coinvolti | Tipo |
|---|------|------------|----------------|------|
| 13 | Aggiungere chiavi i18n mancanti in `locale/project/it.js` e `locale/project/en.js` | #1-#12 | `locale/project/it.js`, `locale/project/en.js` | modifica |
| 14 | Eliminare `MissingDataPanel.tsx` e `WowWeekPlannerV2.tsx` (codice ora distribuito) | #7, #11, #12 | widget files | elimina |
| 15 | Verificare responsive su 1280px+ e dark mode consistency | #1-#14 | tutti | verifica |

### Dettagli implementativi per i task chiave

#### Task 1 — Navigazione con sotto-voci

```typescript
{
  menuLabel: "wow_promotions",
  headerTitle: "wow_promotions_title",
  headerDescription: "wow_promotions_description",
  headerIcon: "Sparkles",
  private: true,
  menuActivation: "/wow-promotions",
  permission: ["marketing:read"],
  href: "/wow-promotions/",
  hideTabs: true,
  isSingle: false, // CAMBIATO da true
  menuIcon: "Sparkles",
  items: [
    {
      menuLabel: "wow_nav_planning",
      headerTitle: "wow_promotions_title",
      headerDescription: "wow_promotions_description",
      href: "/wow-promotions/",
      menuActivation: "/wow-promotions/",
      private: true,
      permission: ["marketing:read"],
      menuIcon: "CalendarDays",
      breadcrumbsArray: [
        { label: "wow_promotions", href: "/wow-promotions/" },
        { label: "wow_nav_planning", href: "" },
      ],
    },
    {
      menuLabel: "wow_nav_budget",
      headerTitle: "wow_budget_title",
      headerDescription: "wow_budget_description",
      href: "/wow-promotions/budget",
      menuActivation: "/wow-promotions/budget",
      private: true,
      permission: ["marketing:read"],
      menuIcon: "Wallet",
      breadcrumbsArray: [
        { label: "wow_promotions", href: "/wow-promotions/" },
        { label: "wow_nav_budget", href: "" },
      ],
    },
    {
      menuLabel: "wow_nav_storico",
      headerTitle: "wow_storico_title",
      headerDescription: "wow_storico_description",
      href: "/wow-promotions/storico",
      menuActivation: "/wow-promotions/storico",
      private: true,
      permission: ["marketing:read"],
      menuIcon: "History",
      breadcrumbsArray: [
        { label: "wow_promotions", href: "/wow-promotions/" },
        { label: "wow_nav_storico", href: "" },
      ],
    },
  ],
  breadcrumbsArray: [{ label: "wow_promotions", href: "" }],
  tabsArray: [],
},
```

#### Task 4 — Estensioni wowScore.helper.ts

Aggiungere:

```typescript
// Tipo campagna speciale
export interface SpecialCampaign {
  id: string;
  name: string;
  type: "si_parte" | "pasqua" | "summer" | "natale" | "custom";
  startDate: Date;
  endDate: Date;
  color?: string;
}

// Mock campagne speciali
export function getMockSpecialCampaigns(): SpecialCampaign[] {
  return [
    {
      id: "pasqua-2026",
      name: "Sorprese di Pasqua",
      type: "pasqua",
      startDate: new Date("2026-03-20"),
      endDate: new Date("2026-04-03"),
    },
  ];
}

// Convertire PlannedWow + SpecialCampaign in formato Gantt
export function buildGanttData(
  plannedWows: PlannedWow[],
  weeks: WowWeek[],
  specialCampaigns: SpecialCampaign[],
): RawGanttDataType[] {
  // Gruppo Studio: una barra per ogni WOW pianificata su linea studio
  // Gruppo Laboratorio: una barra per ogni WOW pianificata su linea laboratorio
  // Gruppo Campagne Speciali: una barra per ogni campagna
  // Settimane vuote: non generano barre (lo slot vuoto e implicito nel Gantt)
  return [
    {
      key: "studio",
      title: "Studio",
      children: plannedWows
        .filter((p) => p.line === "studio")
        .map((p) => ({
          key: `studio-w${p.weekIndex}`,
          title: `${p.candidate.des_fornitore} — ${p.candidate.des_articolo}`,
          data: {
            startDate: weeks[p.weekIndex].startDate.toISOString(),
            endDate: addDays(weeks[p.weekIndex].startDate, 14).toISOString(), // 15 giorni
          },
        })),
    },
    {
      key: "laboratorio",
      title: "Laboratorio",
      children: plannedWows
        .filter((p) => p.line === "laboratorio")
        .map((p) => ({
          key: `lab-w${p.weekIndex}`,
          title: `${p.candidate.des_fornitore} — ${p.candidate.des_articolo}`,
          data: {
            startDate: weeks[p.weekIndex].startDate.toISOString(),
            endDate: addDays(weeks[p.weekIndex].startDate, 14).toISOString(),
          },
        })),
    },
    {
      key: "speciali",
      title: "Campagne Speciali",
      children: specialCampaigns.map((c) => ({
        key: c.id,
        title: c.name,
        data: {
          startDate: c.startDate.toISOString(),
          endDate: c.endDate.toISOString(),
        },
      })),
    },
  ];
}
```

Modificare `getWowWeeks()` per generare **6 settimane** (invece di 3):
```typescript
// Cambiare il count da 3 a 6
const WEEK_COUNT = 6;
```

#### Task 5 — WowGanttView.tsx

```typescript
import { useMemo } from "react";
import { Gantt } from "laif-ds"; // VERIFICA l'import corretto
import { GanttDimensions, DragStepSizes } from "laif-ds";
import { buildGanttData, PlannedWow, SpecialCampaign, WowLine, WowWeek } from "../helpers/wowScore.helper";

interface WowGanttViewProps {
  weeks: WowWeek[];
  plannedWows: PlannedWow[];
  specialCampaigns: SpecialCampaign[];
  onSlotClick?: (weekIndex: number, line: WowLine) => void;
  onBarChange?: (barKey: string, startDate: Date, endDate: Date) => void;
}

export default function WowGanttView({
  weeks, plannedWows, specialCampaigns, onSlotClick, onBarChange,
}: WowGanttViewProps) {
  const ganttData = useMemo(
    () => buildGanttData(plannedWows, weeks, specialCampaigns),
    [plannedWows, weeks, specialCampaigns],
  );

  return (
    <div className="h-full min-h-[300px]">
      <Gantt
        draggable={true}
        defaultDimension={GanttDimensions.WEEK}
        defaultDragStepSize={DragStepSizes.ONE_WEEK}
        treeTitle="Linee"
      >
        <Gantt.Controls />
        <Gantt.Chart
          data={ganttData}
          onBarDoubleClick={(bar) => {
            // Apri dettaglio o permetti modifica
          }}
          onBarChange={(bar) => {
            if (onBarChange) {
              onBarChange(bar.key, new Date(bar.data.startDate), new Date(bar.data.endDate));
            }
          }}
        />
      </Gantt>
    </div>
  );
}
```

**NOTA**: l'API esatta del Gantt (callback `onBarDoubleClick`, `onBarChange`, ecc.) va verificata sulla codebase laif-ds. Controlla `Gantt.tsx` e `Chart.tsx` per i prop disponibili.

#### Task 6 — WowCampaignDialog.tsx

Dialog modale per aggiungere campagne speciali. Usa componenti laif-ds (`Dialog`, `Select`, `DatePicker`, `Button`):

- Campo tipo: Select con opzioni Si Parte, Pasqua, Summer, Natale, Custom
- Campo nome: TextField (precompilato dal tipo)
- Campo date inizio/fine: DatePicker
- Durata automatica: 2-8 settimane (calcolata da date)
- Pulsante conferma → aggiunge la campagna al Gantt

#### Task 7 — Refactoring WowPromotionsMain.tsx

Il componente va semplificato rimuovendo:
- La struttura `<Tabs>` con tab Planning e Missing Data
- Il planner orizzontale inline (ora sostituito da `WowGanttView`)

Layout target:

```
┌─────────────────────────────────────┐
│ Header: titolo, contatori, [+ Camp] │
├─────────────────────────────────────┤
│ GANTT (flex-1, min 300px)           │
│ WowGanttView                        │
├─────────────────────────────────────┤
│ CANDIDATI (flex-1, min 200px)       │
│ "Suggerimenti per W12 — Studio"     │
│ WowCandidatesTable                  │
└─────────────────────────────────────┘
```

Mantenere:
- Lo state management (`selectedWeekIndex`, `selectedLine`, `plannedWows`)
- La query API per marketing data
- Il build dei candidati (`buildWowCandidates`)
- I handler `handleSelect`, `handleDeselect`, `handleRemovePlanned`

Aggiungere:
- State per `specialCampaigns`
- `handleSelectWeek` collegato al click su slot vuoto nel Gantt
- Pulsante "+ Campagna speciale" nell'header che apre `WowCampaignDialog`

#### Task 9 — WowBudgetTree.tsx (estrazione da MissingDataPanel)

In `MissingDataPanel.tsx` c'e un sub-tab "Budget & Vincoli" che contiene un tree espandibile con i dati mock dei fornitori. Il codice e nelle righe relative al budget tree. Estrarlo in un componente standalone che:

- Mostra il tree espandibile: Fornitore → Classe → Sottoclasse
- Ogni riga ha: nome, budget annuo, progress bar avanzamento, gap EUR, WOW effettuate/max
- Aggiungere filtro per fornitore in cima

Usare i dati mock gia presenti in `wowScore.helper.ts` (funzione `buildBudgetTree` o dati inline nel MissingDataPanel).

#### Task 10 — WowPurchaseTable.tsx (estrazione da MissingDataPanel)

Estrarre il sub-tab "Listino Acquisto" con la tabella CELIN. Colonne: codice articolo, descrizione, fornitore, costo acquisto.

#### Task 12 — WowStoricoPage.tsx

Estrarre il sub-tab "Storico WOW" da `MissingDataPanel.tsx`. Aggiungere:

- **Filtri in cima**: fornitore (Select), classe (Select), linea (Select), periodo da/a (DatePicker), pulsante Reset
- **Tabella**: fornitore, classe, articolo, linea, date, score al momento della pianificazione, venduto previsto, venduto effettivo, delta (colorato verde/rosso)
- **Riepilogo in fondo**: totale WOW, delta medio EUR, % performance positiva

#### Task 13 — Chiavi i18n da aggiungere

```javascript
// Navigazione
wow_nav_planning: "Pianificazione",
wow_nav_budget: "Budget & Vincoli",
wow_nav_storico: "Storico",

// Pagina budget
wow_budget_title: "Budget & Vincoli Fornitori",
wow_budget_description: "Monitoraggio budget fornitori e vincoli contrattuali",
wow_budget_tab_suppliers: "Budget Fornitori",
wow_budget_tab_purchase: "Listino Acquisto",
wow_budget_filter_supplier: "Filtra per fornitore",

// Pagina storico
wow_storico_title: "Storico Promozioni WOW",
wow_storico_description: "Analisi performance promozioni passate",
wow_storico_filter_reset: "Reset filtri",
wow_storico_summary_total: "Totale WOW",
wow_storico_summary_avg_delta: "Delta medio",
wow_storico_summary_positive: "Performance positiva",

// Gantt
wow_gantt_add_campaign: "Aggiungi campagna speciale",
wow_gantt_campaign_type: "Tipo campagna",
wow_gantt_campaign_name: "Nome campagna",
wow_gantt_campaign_dates: "Periodo",
wow_gantt_campaign_si_parte: "WOW Si Parte",
wow_gantt_campaign_pasqua: "Sorprese di Pasqua",
wow_gantt_campaign_summer: "Umbra Summer",
wow_gantt_campaign_natale: "Aspettando il Natale",
wow_gantt_campaign_custom: "Personalizzata",

// Candidati
wow_add_manual: "Aggiungi manuale",
wow_candidates_context: "Candidati per {week} — {line}",
```

---

## 4. Convenzioni LAIF (obbligatorie)

### Frontend

- Usare SOLO token Tailwind del DS (mai classi vanilla type)
- Preferire componenti `laif-ds` su shadcn/ui raw (`Badge`, `Icon`, `Skeleton`, `Tabs`, `TabsContent`, `TabsList`, `TabsTrigger`, `Dialog`, `Select`, `Button`, ecc.)
- Architettura feature-based (soft onion): widget in `widgets/`, helper in `helpers/`, pagina-container al root
- Redux solo per stato globale; stato locale con `useState`/`useMemo`
- Hook custom per API call (TanStack Query wrapper via `useCustomQuery`)
- No prop drilling (usare Redux o Context se servono dati cross-componente)
- Design responsive obbligatorio (1280px+)
- Naming: PascalCase componenti, camelCase hooks, kebab-case cartelle
- Traduzioni via `react-intl` (`useIntl()`, `intl.formatMessage({ id: "chiave" })`)

### Per questo progetto specifico

- **Lazy loading pagine**: ogni `page.tsx` in `app/(authenticated)/` usa `lazy()` per caricare il componente feature
- **Generazione client API**: dopo modifica route backend → `just fe generate-client`
- **Stile componenti**: usare `clsx` per classi condizionali (gia in uso)
- **Colori linee**: Studio = `info` (blu), Laboratorio = `success` (verde), Campagne Speciali = `warning` (ambra)
- **Icone linee**: Studio = `Beaker`, Laboratorio = `Microscope`

---

## 5. Pattern da applicare

### Pattern: fullstack-dev-preview-loop

Ciclo iterativo per sviluppo full-stack con preview:

1. **Backend Fix** → Modifica backend se serve
2. **Frontend Adapt** → Adatta frontend al cambiamento
3. **Preview Verify** → Verifica con preview (screenshot, console, network)
4. **Ripeti** se ci sono errori

Per questo brief il backend non cambia, quindi il ciclo e:
1. Frontend Edit → 2. Verify (dev server `just fe dev`) → 3. Ripeti

### Pattern: list-detail-lazy-loading

Per tabelle con molti dati, usare lazy loading via TanStack Query con `keepPreviousData`. Gia implementato nella query marketing; mantenere lo stesso pattern per Budget e Storico se passano a dati reali.

---

## 6. Criteri di accettazione

### Navigazione
- [ ] La sidebar mostra "Promozioni WOW" con 3 sotto-voci: Pianificazione, Budget, Storico
- [ ] Click su ogni sotto-voce naviga alla pagina corretta
- [ ] Breadcrumb corrette su ogni pagina

### Pagina Gantt + Candidati (`/wow-promotions/`)
- [ ] Il Gantt mostra 3 righe/gruppi: Studio, Laboratorio, Campagne Speciali
- [ ] L'orizzonte e di almeno 6 settimane
- [ ] Click su uno slot vuoto nel Gantt aggiorna i candidati sotto
- [ ] Selezionare un candidato dalla tabella crea una barra nel Gantt
- [ ] Le barre sono draggabili e ridimensionabili (snap a 1 settimana)
- [ ] Le campagne speciali sono visibili come barre distinte (colore diverso)
- [ ] Il pulsante "+ Campagna speciale" apre il dialog e aggiunge al Gantt
- [ ] Il contatore "N/M pianificati" si aggiorna correttamente
- [ ] La tabella candidati mostra "Aggiungi manuale" in fondo

### Pagina Budget (`/wow-promotions/budget`)
- [ ] Tab "Budget Fornitori" mostra tree espandibile con progress bar
- [ ] Tab "Listino Acquisto" mostra tabella CELIN
- [ ] Filtro per fornitore funziona
- [ ] Dati mock consistenti con quelli della pagina principale

### Pagina Storico (`/wow-promotions/storico`)
- [ ] Tabella mostra WOW passate con tutte le colonne
- [ ] Filtri (fornitore, classe, linea, periodo) funzionano
- [ ] Riepilogo aggregato visibile in fondo
- [ ] Delta colorato (verde positivo, rosso negativo)

### Generale
- [ ] `MissingDataPanel.tsx` e `WowWeekPlannerV2.tsx` eliminati
- [ ] Nessun import rotto (tutti i riferimenti aggiornati)
- [ ] Build compila senza errori (`just fe build` o equivalente)
- [ ] Responsive su 1280px+
- [ ] Chiavi i18n aggiunte in `it.js` e `en.js`

---

## 7. Rischi e note

- **Import Gantt da laif-ds**: verifica come il Gantt e esportato dal package. Se non e nel barrel export (`index.ts`), potrebbe servire un import diretto. Controlla `src/index.ts` o `src/components/ui/gantt/index.ts`.
- **Gantt WEEK prerequisito**: se la dimensione WEEK non e ancora implementata, il Gantt fallira. Questo brief dipende dal completamento di `gantt-week-extension.md`.
- **Dati mock**: tutto e attualmente mock. Non serve collegare API reali — la struttura dati e gia predisposta per il passaggio futuro.
- **MissingDataPanel split**: il componente ha 845 righe. Estrarre con attenzione separando stato locale e dati mock condivisi. Se ci sono funzioni di utility usate da piu sub-tab, spostarle in `wowScore.helper.ts`.
- **Gantt click su slot vuoto**: il Gantt laif-ds potrebbe non avere un callback per click su aree vuote. Se non c'e, si puo gestire con un click listener sul container o usando le date della scala per determinare quale settimana e stata cliccata. In alternativa, mantenere un selector esterno al Gantt (dropdown settimana + linea) che aggiorna i candidati.
- **Tree espandibile Budget**: gia implementato con componenti custom in MissingDataPanel. Quando lo estrai, mantieni lo stesso stile visuale.

---

## 8. File da creare / modificare (riepilogo)

### Nuovi file
- `app/(authenticated)/wow-promotions/budget/page.tsx` — Entry point pagina Budget
- `app/(authenticated)/wow-promotions/storico/page.tsx` — Entry point pagina Storico
- `src/features/wow-promotions/WowBudgetPage.tsx` — Componente pagina Budget
- `src/features/wow-promotions/WowStoricoPage.tsx` — Componente pagina Storico
- `src/features/wow-promotions/widgets/WowGanttView.tsx` — Wrapper Gantt laif-ds
- `src/features/wow-promotions/widgets/WowCampaignDialog.tsx` — Dialog campagne speciali
- `src/features/wow-promotions/widgets/WowBudgetTree.tsx` — Tree budget fornitori (da MissingDataPanel)
- `src/features/wow-promotions/widgets/WowPurchaseTable.tsx` — Tabella listino acquisto (da MissingDataPanel)

### File da modificare
- `src/config/navigation.tsx` — Da `isSingle: true` a `false` con 3 sotto-voci
- `src/features/wow-promotions/WowPromotionsMain.tsx` — Refactor completo: Gantt + Candidati
- `src/features/wow-promotions/helpers/wowScore.helper.ts` — 6+ settimane, SpecialCampaign, buildGanttData
- `src/features/wow-promotions/widgets/WowCandidatesTable.tsx` — Aggiungere "Aggiungi manuale"
- `locale/project/it.js` — Nuove chiavi i18n
- `locale/project/en.js` — Nuove chiavi i18n (tradotte in inglese)

### File da eliminare
- `src/features/wow-promotions/widgets/MissingDataPanel.tsx` — Contenuto distribuito nelle nuove pagine
- `src/features/wow-promotions/widgets/WowWeekPlannerV2.tsx` — Sostituito da WowGanttView

---

## 9. Template Report Feedback

> Quando hai finito, compila questo template e passalo a Claude Code.
> Puoi salvarlo come `wow-ui-refactor-report.md` nella stessa cartella del brief
> oppure copiarlo direttamente in chat a Claude Code.

### Windsurf Report — Fasi 1-5 — Refactor UI WOW Promotions

#### Metadata

| Campo | Valore |
|-------|--------|
| Data completamento | [YYYY-MM-DD] |
| Tempo stimato | [ore] |
| Completamento task | [N/15 completati] |

#### 1. Task completati

| # | Task | Stato | Note |
|---|------|-------|------|
| 1 | Aggiornare navigation.tsx con 3 sotto-voci | completato / parziale / saltato | [note] |
| 2 | Creare page budget | completato / parziale / saltato | [note] |
| 3 | Creare page storico | completato / parziale / saltato | [note] |
| 4 | Estendere wowScore.helper.ts | completato / parziale / saltato | [note] |
| 5 | Creare WowGanttView.tsx | completato / parziale / saltato | [note] |
| 6 | Creare WowCampaignDialog.tsx | completato / parziale / saltato | [note] |
| 7 | Refactoring WowPromotionsMain.tsx | completato / parziale / saltato | [note] |
| 8 | Aggiornare WowCandidatesTable.tsx | completato / parziale / saltato | [note] |
| 9 | Creare WowBudgetTree.tsx | completato / parziale / saltato | [note] |
| 10 | Creare WowPurchaseTable.tsx | completato / parziale / saltato | [note] |
| 11 | Creare WowBudgetPage.tsx | completato / parziale / saltato | [note] |
| 12 | Creare WowStoricoPage.tsx | completato / parziale / saltato | [note] |
| 13 | Aggiungere chiavi i18n | completato / parziale / saltato | [note] |
| 14 | Eliminare MissingDataPanel e WowWeekPlannerV2 | completato / parziale / saltato | [note] |
| 15 | Verificare responsive e dark mode | completato / parziale / saltato | [note] |

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

**File eliminati:**
- `path/file.ext` — [motivo]

#### 7. Domande aperte

- [ ] [domanda irrisolta che richiede una decisione]

#### 8. Suggerimenti

- [suggerimento per migliorare codice, processo o architettura]
