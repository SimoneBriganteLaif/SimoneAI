---
titolo: "FastAPI: route statiche prima di parametriche"
categoria: "api"
complessità: "bassa"
usato-in:
  - jubatus
data-creazione: "2026-03-09"
ultimo-aggiornamento: "2026-03-09"
tags:
  - "#pattern:api"
  - "#stack:fastapi"
  - "#problema:routing"
---

# Pattern: FastAPI — route statiche prima di parametriche

## Problema

FastAPI (e Starlette) valuta le route nell'ordine in cui sono definite. Se definisci una route parametrica prima di una statica con lo stesso prefisso, la parametrica "cattura" anche i valori statici.

```
POST /sync/{mailbox_id}   ← definita prima
POST /sync/all             ← mai raggiunta! "all" viene matchato come mailbox_id
```

L'errore risultante è un `422 Unprocessable Entity` (o `int_parsing` error se il parametro è int).

**Segnali che questo pattern è quello giusto**:
- Errore `422` su un endpoint che dovrebbe funzionare
- Errore "unable to parse string as an integer" su un path parameter
- Un endpoint "scompare" dopo averne aggiunto un altro sullo stesso prefisso

---

## Soluzione

Definisci sempre le route **statiche** PRIMA delle route **parametriche** sullo stesso prefisso.

### Implementazione

**Regola**: nell'ordine di definizione nel controller, le route senza parametri (o con parametri più specifici) vanno prima di quelle con path parameter generici.

### Codice di riferimento

```python
router = APIRouter(prefix="/sync")

# SBAGLIATO: la parametrica cattura tutto
@router.post("/{mailbox_id}")
async def sync_mailbox(mailbox_id: int): ...

@router.post("/all")
async def sync_all(): ...  # Mai raggiunta! "all" → mailbox_id

# CORRETTO: statica prima di parametrica
@router.post("/all")
async def sync_all(): ...

@router.post("/{mailbox_id}")
async def sync_mailbox(mailbox_id: int): ...
```

---

## Trade-off

**Vantaggi**:
- Zero overhead, solo ordine di definizione
- Soluzione definitiva, nessun workaround necessario

**Svantaggi / costi**:
- Richiede attenzione manuale all'ordine delle route
- Facile da rompere con un refactoring che riordina le funzioni

**Quando NON usare questo pattern**:
- Se i path sono completamente diversi (es. `/sync` e `/mailboxes/{id}`) — nessun conflitto
- Se usi `Depends()` con type checking avanzato che disambigua (raro in FastAPI)

---

## Esempi reali in LAIF

| Progetto | Come è stato usato | Note / deviazioni |
|---------|-------------------|------------------|
| Jubatus | `/email/sync/all` vs `/email/sync/{mailbox_id}` | Route swap nel controller email — `sync_all` spostato prima di `sync_mailbox` |

---

## Risorse esterne

- [FastAPI Docs - Path Operation Order](https://fastapi.tiangolo.com/tutorial/path-params/#order-matters)
- [Starlette Routing](https://www.starlette.io/routing/)
