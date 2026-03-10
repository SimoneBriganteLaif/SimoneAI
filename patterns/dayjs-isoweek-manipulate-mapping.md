---
titolo: "dayjs isoWeek ManipulateType mapping"
categoria: "integrazione"
complessità: "bassa"
usato-in: ["umbra"]
data-creazione: "2026-03-10"
ultimo-aggiornamento: "2026-03-10"
tags:
  - "#pattern:integrazione"
  - "#stack:dayjs"
  - "#stack:typescript"
---

# Pattern: dayjs isoWeek ManipulateType mapping

## Problema

Quando usi il plugin `isoWeek` di dayjs, il tipo `ManipulateType` non include `"isoWeek"` come valore valido. Questo causa errori TypeScript quando provi a passare un'unita di tempo dinamica (es. da un enum) a metodi come `.add()`, `.subtract()`, `.startOf()`.

**Segnali che questo pattern è quello giusto**:
- Usi dayjs con il plugin `isoWeek`
- Hai un enum o costante con valore `"isoWeek"` che passi a metodi dayjs
- TypeScript segnala che `"isoWeek"` non e assegnabile a `ManipulateType`

---

## Soluzione

Mappare esplicitamente `"isoWeek"` a `"week"` prima di passare il valore ai metodi dayjs che accettano `ManipulateType`. Per `startOf()` e `endOf()`, castare a `OpUnitType` (che include `"isoWeek"`).

### Struttura

```
enum → mapping → metodo dayjs
  "isoWeek" → "week" per .add() / .subtract()
  "isoWeek" → cast OpUnitType per .startOf() / .endOf()
```

### Implementazione

**Passo 1**: Definire il mapping inline dove serve:

```typescript
const manipulateUnit = (
  unitOfTime === "isoWeek" ? "week" : unitOfTime
) as dayjs.ManipulateType;
```

**Passo 2**: Usare `manipulateUnit` per `.add()` e `.subtract()`:

```typescript
const newDate = dayjs().subtract(1, manipulateUnit);
```

**Passo 3**: Per `.startOf()` e `.endOf()`, castare direttamente:

```typescript
dayjs().startOf(unitOfTime as dayjs.OpUnitType);
```

### Codice di riferimento

```typescript
import dayjs from "dayjs";
import isoWeek from "dayjs/plugin/isoWeek";

dayjs.extend(isoWeek);

// Enum con valore "isoWeek"
enum UnitOfTimes {
  WEEK = "isoWeek",
  MONTH = "month",
}

// Per .add() / .subtract() — mappare a "week"
const unit = UnitOfTimes.WEEK;
const manipulateUnit = (
  unit === "isoWeek" ? "week" : unit
) as dayjs.ManipulateType;

dayjs().add(1, manipulateUnit);     // OK
dayjs().subtract(1, manipulateUnit); // OK

// Per .startOf() / .endOf() — cast a OpUnitType
dayjs().startOf(unit as dayjs.OpUnitType); // OK — usa isoWeek (lunedi)
```

---

## Trade-off

**Vantaggi**:
- Risolve l'incompatibilita di tipo senza perdere la semantica ISO 8601
- `.startOf("isoWeek")` inizia da lunedi (corretto per calendario europeo)
- Pattern semplice, nessuna dipendenza aggiuntiva

**Svantaggi / costi**:
- Il mapping e duplicato ogni volta che serve (inline)
- Se dayjs aggiornasse i tipi, il mapping diventerebbe superfluo

**Quando NON usare questo pattern**:
- Se non usi il plugin `isoWeek` (usa direttamente `"week"`)
- Se lavori solo con `.startOf()` / `.endOf()` (basta il cast a `OpUnitType`)

---

## Varianti

### Variante: Helper centralizzato

Se il mapping si ripete in molti punti, estrarre una funzione helper:

```typescript
export const toManipulateUnit = (
  unit: string,
): dayjs.ManipulateType =>
  (unit === "isoWeek" ? "week" : unit) as dayjs.ManipulateType;
```

Preferirla quando il mapping appare in 3+ file diversi.

---

## Esempi reali in LAIF

| Progetto | Come è stato usato | Note / deviazioni |
|---------|-------------------|------------------|
| umbra (laif-ds) | Gantt WEEK dimension: mapping in `getScaleDates.tsx`, `Scale.tsx` | Mapping inline, 3 occorrenze nel componente Gantt |

---

## Risorse esterne

- [dayjs isoWeek plugin](https://day.js.org/docs/en/plugin/iso-week)
- [dayjs ManipulateType](https://day.js.org/docs/en/manipulate/add)
