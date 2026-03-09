---
problema: "Conflitti tra route statiche e parametriche"
categoria: "api"
frequenza: "media"
progetti-dove-si-e-presentato: [jubatus]
data-creazione: "2026-03-09"
tags:
  - "#problema:routing"
  - "#stack:fastapi"
---

# Problema Ricorrente: Conflitti tra route statiche e parametriche

## Descrizione del problema

In framework come FastAPI, le route vengono matchate nell'ordine di definizione. Se una route parametrica (`/items/{id}`) è definita prima di una statica (`/items/search`), la route statica viene catturata come parametro (id="search") e restituisce errori o dati sbagliati.

**Segnali che stai affrontando questo problema**:
- 404 o 422 su endpoint che dovrebbero funzionare
- Endpoint di ricerca/filtro che restituisce "not found" o errori di validazione
- Il path parameter riceve valori inattesi (es. "search" come UUID)

**Contesto tipico in cui si presenta**:
- API REST con endpoint CRUD + endpoint di utilità sullo stesso prefisso
- Router con molteplici route sullo stesso path prefix
- Aggiunta di nuovi endpoint a un router esistente

---

## Soluzioni adottate

### Soluzione A: Definire le route statiche PRIMA delle parametriche *(raccomandata)*

**Quando usarla**: sempre, come convenzione standard

**Come funziona**: in FastAPI l'ordine di definizione è l'ordine di matching. Le route statiche devono essere scritte prima nel codice.

**Riferimento al pattern**: [fastapi-route-order](../../patterns/fastapi-route-order.md)

---

## Prevenzione

- Stabilire come convenzione di team: route statiche sempre prima delle parametriche
- Durante la code review, verificare l'ordine delle route nei router
- In caso di dubbio, testare con curl/Swagger l'endpoint statico

---

## Esperienze nei progetti LAIF

| Progetto | Contesto | Soluzione usata | Risultato |
|---------|---------|----------------|----------|
| Jubatus | `/threads/search` vs `/threads/{id}` | Riordinamento route | Bug risolto immediatamente |
