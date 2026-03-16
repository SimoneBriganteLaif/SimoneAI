# Ticketing Refactor

| Campo | Valore |
|---|---|
| **ID** | 166 |
| **Stack** | laif-template |
| **Tipo** | Roadmap |
| **Status** | In corso |
| **Effort** | 8h |
| **Target** | 2-20 Marzo 2026 |

## Descrizione originale

Ticketing Refactor — refactoring completo del sistema di ticketing/supporto nel template.

## Piano di risoluzione

1. **Già in corso con PR aperte.** Verificare lo stato delle PR e i branch attivi prima di procedere.
2. **Refactoring del sistema di ticketing/supporto nel template** — rivedere l'architettura del modulo: modelli, API, componenti frontend. Allineare alla struttura standard del template.
3. **Migliorare la gestione degli stati del ticket** — implementare una macchina a stati chiara per i ticket (aperto → in lavorazione → risolto → chiuso). Includere la possibilità di editing degli stati (sub-issue dedicata). Correlato a issue 65 (aggiornamento stato ticket).
4. **Migliorare la funzionalità di ricerca e filtro** — implementare filtri per stato, data, assegnatario, priorità. Aggiungere ricerca full-text sui ticket. Risolve issue 103 (filtro pagina supporto).
5. **UI moderna con componenti laif-ds** — sostituire i componenti legacy con quelli del design system. Usare `AppTable`, `AppDialog`, `AppForm` e gli altri componenti standard.
6. **Sub-issue: capacità di editing dello stato del ticket** — permettere agli utenti autorizzati di modificare lo stato di un ticket direttamente dalla lista o dal dettaglio, con validazione delle transizioni ammesse.
7. **Dopo il completamento: pulizia componenti legacy** — rimuovere i vecchi componenti del ticketing non più utilizzati (issue 164).

### Issue correlate

- Issue 65 — Aggiornamento stato ticket
- Issue 103 — Filtro pagina supporto
- Issue 164 — Pulizia componenti legacy post-refactor

## Stima effort

**8h** — il refactoring è ben definito e le PR sono già in corso. Il grosso del lavoro è nell'allineamento dei componenti al design system e nel testing delle transizioni di stato.
