---
progetto: "wolico"
data-go-live: ""
tags:
  - "#progetto:wolico"
  - "#fase:manutenzione"
---

# Note di Manutenzione — Wolico

---

## Informazioni accesso produzione

| Ambiente | URL | Accesso |
|---------|-----|--------|
| Produzione | https://wolico.app.laifgroup.com | Credenziali personali LAIF |
| Dev locale | http://localhost:8000 (BE) / http://localhost:3000 (FE) | `admin@laifgroup.local` / `passpartout` |

**Repository**: `/Users/simonebrigante/LAIF/repo/wolico/`
**Task runner**: `just` (vedere Justfile per comandi disponibili)
**API Docs**: `/docs` (Swagger, auto-login in dev)

---

## Procedure ricorrenti

### Avvio ambiente locale

```bash
just run default    # backend + DB (Docker)
just fe dev         # frontend dev server
```

### Deploy in produzione

*(da documentare)*

---

## Incidenti e risoluzione

*(nessun incidente documentato)*

---

## Aree critiche / attenzione

- **Integrazione Odoo**: sync dati contabili — verificare che il mapping sia corretto dopo aggiornamenti Odoo
- **MCP Server**: il server in `mcp-servers/wolico/` usa credenziali produzione — gestire con cura
