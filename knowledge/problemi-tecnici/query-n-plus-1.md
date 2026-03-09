---
problema: "Query N+1 con ORM e relazioni"
categoria: "performance"
frequenza: "alta"
progetti-dove-si-e-presentato: [jubatus]
data-creazione: "2026-03-09"
tags:
  - "#problema:performance"
  - "#problema:serializzazione"
  - "#stack:sqlalchemy"
  - "#stack:fastapi"
---

# Problema Ricorrente: Query N+1 con ORM e relazioni

## Descrizione del problema

Quando si usano ORM come SQLAlchemy con relazioni (one-to-many, many-to-many), il caricamento lazy di default genera N+1 query: 1 per la lista principale + 1 per ogni elemento per caricare la relazione. Su liste con molti elementi, le performance crollano.

**Segnali che stai affrontando questo problema**:
- Endpoint lento su liste con relazioni (>500ms per 50 elementi)
- Molte query identiche nel log SQL
- `InvalidRequestError` dopo aver aggiunto `joinedload()`

**Contesto tipico in cui si presenta**:
- API REST che ritorna liste di oggetti con relazioni annidate
- SQLAlchemy 2.0 con modelli che hanno relazioni `relationship()`
- Endpoint di tipo "lista con dettaglio" (es. thread con messaggi, ordini con righe)

---

## Soluzioni adottate

### Soluzione A: `joinedload()` + `.unique()` *(raccomandata)*

**Quando usarla**: relazioni one-to-many dove servono i dati correlati nella risposta

**Come funziona**: `joinedload()` genera un JOIN SQL che carica tutto in una query. Ma il JOIN produce righe duplicate — serve `.unique()` prima di `.scalars()` per deduplicare.

**Riferimento al pattern**: [sqlalchemy-joinedload-unique](../../patterns/sqlalchemy-joinedload-unique.md)

**Risultati ottenuti in LAIF**: da N+1 query a 1 query, tempo risposta da ~800ms a ~50ms su 100 elementi (Jubatus)

---

### Soluzione B: `selectinload()`

**Quando usarla**: relazioni many-to-many o quando il JOIN produce troppe righe duplicate

**Come funziona**: genera 2 query separate (1 per la lista + 1 IN query per le relazioni). Non richiede `.unique()`.

**Perché è seconda scelta**: leggermente più lento di joinedload per relazioni semplici, ma migliore per relazioni complesse o nested

---

## Soluzioni che NON hanno funzionato

- **`lazy="joined"` nel modello**: funziona ma carica sempre la relazione anche quando non serve, impattando tutte le query
- **Paginare senza risolvere N+1**: riduce il numero di query ma non il problema — 20 query per pagina è comunque troppo

---

## Prevenzione

- Usare `joinedload()` o `selectinload()` fin dall'inizio sugli endpoint di tipo lista
- Abilitare SQL echo in sviluppo per individuare N+1 subito
- Pattern list-detail: caricare solo dati leggeri nella lista, dettagli on-demand

---

## Esperienze nei progetti LAIF

| Progetto | Contesto | Soluzione usata | Risultato |
|---------|---------|----------------|----------|
| Jubatus | Thread con messaggi email | joinedload + unique | 800ms → 50ms |
