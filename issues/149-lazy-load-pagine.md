# Lazy Load Pagine — Uniformare approccio

| Campo | Valore |
|---|---|
| **ID** | 149 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | Da rilasciare |
| **Effort** | 1h |

## Descrizione originale

Ora non tutte le pagine del template sono lazy loaded e soprattutto certe usano `lazy` di React e altre `dynamic` di Next, le uniformerei.

## Piano di risoluzione

1. **Pronto per il rilascio.** Tutte le pagine ora utilizzano un approccio di lazy loading consistente.
2. **Lavoro completato**: tutte le pagine sono state uniformate per usare lo stesso metodo di lazy loading, eliminando la coesistenza di `React.lazy` e `next/dynamic`.
3. **Nota importante**: questo approccio dovrà essere rivisto quando Next.js verrà sostituito da TanStack Router (issue 91). Con TanStack Router, il lazy loading sarà gestito nativamente tramite i file `.lazy.tsx` e il route splitting integrato, rendendo superfluo sia `React.lazy` che `next/dynamic`.

### Issue correlate

- Issue 91 — Dismettere Next.js per TanStack Router (impatterà il lazy loading)

## Stima effort

**1h** — completato, in attesa di rilascio. Verificare solo che non ci siano regressioni prima del merge.
