# Font Sizes in rem

| Campo | Valore |
|---|---|
| **ID** | 147 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | Da rilasciare |
| **Effort** | 2h |

## Descrizione originale

Con l'introduzione dell'input per personalizzare la grandezza dei font, sarebbe utile migliorare la gestione usando unità di misura per le font sizes relative (rem).

## Piano di risoluzione

1. **Pronto per il rilascio.** Le font sizes ora utilizzano unità rem con baseline configurabile.
2. **Lavoro completato**: tutte le dimensioni dei font sono state convertite da `px` a `rem`. Il selettore di dimensione font modifica il `font-size` del root (`<html>`), e tutte le dimensioni scalano proporzionalmente grazie all'uso di `rem`.
3. **Verifica pre-rilascio**: controllare che la scala dei font funzioni correttamente su tutti i breakpoint e che il selettore di personalizzazione produca risultati visivamente coerenti.

### Issue correlate

- Issue 91 — Dismettere Next.js per TanStack Router (verificare compatibilità con il nuovo sistema di font)
- Issue 129 — Ristrutturare colori Tailwind (allineamento token design system)

## Stima effort

**2h** — completato, in attesa di rilascio. Effort residuo per testing finale e merge.
