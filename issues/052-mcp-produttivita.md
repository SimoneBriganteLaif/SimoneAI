# MCP per Produttività

| Campo | Valore |
|---|---|
| **ID** | 52 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | In corso |

## Descrizione originale

MCP per produttività: chiamate a DB locale, documentazione, design system e progetti, cos'è successo in prod nell'ultima ora?, l'IDE diventa il pannello di controllo dello sviluppatore in locale.

## Piano di risoluzione

1. **Già in corso.** Verificare lo stato attuale dell'implementazione e i server MCP già creati.
2. **Creare MCP server per query al DB locale** — permettere allo sviluppatore di eseguire query SQL direttamente dall'IDE tramite MCP:
   - Connessione al database PostgreSQL locale (Docker).
   - Query in sola lettura (sicurezza).
   - Formattazione risultati leggibile.
   - Già parzialmente implementato (vedi server MCP PostgreSQL esistente).
3. **Creare MCP server per visualizzazione log di produzione** — rispondere alla domanda "cos'è successo in prod nell'ultima ora?":
   - Integrazione con CloudWatch Logs (AWS).
   - Filtro per servizio, livello di log, timerange.
   - Aggregazione errori e anomalie.
4. **Creare MCP server per ricerca nella documentazione** — permettere di cercare nella KB, nella documentazione dei progetti e nel design system:
   - Indicizzazione dei file markdown della KB.
   - Ricerca nei componenti laif-ds.
   - Contesto del progetto corrente.
5. **Integrazione con gli IDE** — assicurarsi che i server MCP siano compatibili con:
   - Windsurf (già supportato nativamente).
   - VS Code (tramite estensioni MCP).
   - Claude Code (già supportato).
6. **Dashboard di monitoring nell'IDE** — permettere allo sviluppatore di avere una visione d'insieme:
   - Stato dei servizi (Docker container attivi).
   - Ultime migrazioni applicate.
   - Errori recenti in produzione.
   - Metriche di base (response time, error rate).

### Issue correlate

- Issue 163 — Laif Agent (l'agent può usare i server MCP come tool)

## Stima effort

**Medio-alto (20-30h)** — ogni server MCP richiede 4-8h. Approccio incrementale consigliato:
- Fase 1 (8h): server DB locale + documentazione (maggiore impatto immediato).
- Fase 2 (8h): server log produzione (richiede integrazione AWS).
- Fase 3 (8h): dashboard e polish.
