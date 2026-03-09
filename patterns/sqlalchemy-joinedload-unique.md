---
titolo: "SQLAlchemy joinedload richiede unique()"
categoria: "database"
complessità: "bassa"
usato-in:
  - jubatus
data-creazione: "2026-03-09"
ultimo-aggiornamento: "2026-03-09"
tags:
  - "#pattern:database"
  - "#stack:sqlalchemy"
  - "#stack:fastapi"
  - "#problema:serializzazione"
---

# Pattern: SQLAlchemy joinedload richiede unique()

## Problema

Quando usi `joinedload()` su relazioni one-to-many (collections), SQLAlchemy genera una JOIN che produce righe duplicate nel result set. Senza `.unique()`, ottieni l'errore:

```
InvalidRequestError: The unique() method must be invoked on this Result,
as it contains results that include joined eager loads against collections
```

**Segnali che questo pattern è quello giusto**:
- Stai usando `joinedload()` su una relazione con `relationship("Child", ...)`
- La relazione punta a una lista (one-to-many), non a un singolo oggetto (many-to-one)
- L'errore appare al momento di `.scalars().all()` o `.scalar_one_or_none()`

---

## Soluzione

Aggiungi `.unique()` prima di `.scalars()` o `.scalar_one_or_none()`.

### Implementazione

**Regola**: ogni volta che usi `joinedload()` su una collection, aggiungi `.unique()` al result.

### Codice di riferimento

```python
# SBAGLIATO - errore su collection joinedload
stmt = select(Thread).options(joinedload(Thread.messages))
result = db.execute(stmt)
threads = result.scalars().all()  # InvalidRequestError!

# CORRETTO
stmt = select(Thread).options(joinedload(Thread.messages))
result = db.execute(stmt)
threads = result.unique().scalars().all()  # OK

# Per scalar_one_or_none
result = db.execute(stmt)
thread = result.unique().scalar_one_or_none()  # OK
```

**Nota**: per relazioni many-to-one (singolo oggetto), `.unique()` non è necessario ma non causa problemi se presente. Nel dubbio, aggiungilo sempre con `joinedload`.

---

## Trade-off

**Vantaggi**:
- Soluzione semplice, una riga
- Nessun impatto sulle performance (il dedup avviene in-memory dopo la query)

**Svantaggi / costi**:
- Facile da dimenticare (l'errore appare solo a runtime)
- Il dedup in-memory può essere costoso su result set molto grandi

**Quando NON usare questo pattern**:
- Se usi `selectinload()` o `subqueryload()` al posto di `joinedload()` — queste strategie non producono righe duplicate
- Se la relazione è many-to-one (es. `message.thread`) — non serve ma non fa danni

---

## Varianti

### Variante: usare selectinload per evitare il problema

```python
from sqlalchemy.orm import selectinload

stmt = select(Thread).options(selectinload(Thread.messages))
result = db.execute(stmt)
threads = result.scalars().all()  # OK senza unique()
```

`selectinload` esegue una query separata per le relazioni, evitando JOIN e duplicati. Preferibile per collection grandi o query complesse.

---

## Esempi reali in LAIF

| Progetto | Come è stato usato | Note / deviazioni |
|---------|-------------------|------------------|
| Jubatus | `search_threads()` e `get_thread()` in email service | Aggiunto `.unique()` a tutte le query con `joinedload(Thread.messages)` |
| Jubatus | `get_message()` in email service | Aggiunto `.unique()` per joinedload su recipients, attachments, labels |

---

## Risorse esterne

- [SQLAlchemy 2.0 - Loading Relationships](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#joined-eager-loading)
- [SQLAlchemy FAQ - unique() requirement](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#the-importance-of-result-unique)
