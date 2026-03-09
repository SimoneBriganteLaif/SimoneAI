# Pattern Tecnici Cross-Progetto

Pattern riutilizzabili estratti dall'esperienza su progetti reali.
Ogni pattern è stato usato almeno una volta in produzione.

---

## Come leggere un pattern

Ogni file pattern contiene:
- **Problema**: quando usare questo pattern
- **Soluzione**: come implementarlo
- **Trade-off**: cosa perdi e cosa guadagni
- **Esempi reali**: in quali progetti LAIF è stato usato
- **Codice di riferimento**: snippet o link al repo

## Come aggiungere un pattern

1. Copia `_template.md`
2. Rinomina con un nome descrittivo (kebab-case)
3. Compila tutte le sezioni
4. Aggiungi il tag `#pattern:[tipo]` nel frontmatter
5. Aggiorna l'indice qui sotto
6. Aggiorna `.tags/index.md`

---

## Indice pattern

| Pattern | Categoria | Usato in | Ultimo aggiornamento |
|---------|----------|---------|---------------------|
| [sqlalchemy-joinedload-unique](sqlalchemy-joinedload-unique.md) | orm | jubatus | 2026-03-09 |
| [fastapi-route-order](fastapi-route-order.md) | api | jubatus | 2026-03-09 |
| [fullstack-dev-preview-loop](fullstack-dev-preview-loop.md) | workflow | jubatus | 2026-03-09 |

---

## Categorie

- **autenticazione** — login, SSO, gestione sessioni
- **autorizzazione** — ruoli, permessi, multi-tenant
- **pagamenti** — integrazione stripe, fatturazione
- **notifiche** — email, push, in-app
- **file-upload** — upload, storage, ottimizzazione
- **ricerca** — full-text, filtri, facets
- **performance** — caching, lazy loading, ottimizzazione query
- **testing** — strategie di test, mock, CI
- **deploy** — CI/CD, infrastruttura, rollback
- **api** — design REST/GraphQL, versioning, rate limiting
- **orm** — query, relazioni, serializzazione ORM
- **workflow** — flussi di lavoro e cicli di sviluppo
