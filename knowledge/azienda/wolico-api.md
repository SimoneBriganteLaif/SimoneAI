---
tags: ["#progetto:wolico", "#knowledge:azienda", "#mcp:server", "#stack:fastapi"]
---

# API Wolico — Riferimento

> tags: #progetto:wolico #knowledge:azienda #mcp:server #stack:fastapi

## Base URL

- **Produzione**: `https://wolico.app.laifgroup.com/api/`
- **Dev locale**: `http://localhost:8000`

## Autenticazione

- **Endpoint**: `POST /auth/login`
- **Content-Type**: `application/x-www-form-urlencoded` (OAuth2PasswordRequestForm)
- **Payload**: `username=email&password=password`
- **Risposta**: `{"access_token": "jwt_token_here"}`
- **Uso**: `Authorization: Bearer {token}` su ogni richiesta
- **Attenzione**: la libreria `httpx` con `data={}` fa URL-encoding automatico dei valori. Se la password contiene `%`, viene correttamente inviata come `%25` nel form-urlencoded.

## Pattern di ricerca (search)

Wolico usa un pattern di ricerca comune su tutti gli endpoint `/search`. Il payload è:

```json
{
  "search": {
    "campo": {"operator": "operatore", "value": "valore"}
  },
  "limit": 200,
  "offset": 0,
  "sort_by": "campo",
  "sort_order": "desc"
}
```

**Risposta standard**: `{"total": N, "items": [...]}`

### Operatori disponibili (22)

| Operatore | Descrizione |
|-----------|-------------|
| `eq` | Uguale |
| `ne` | Diverso |
| `lt`, `le`, `gt`, `ge` | Confronto numerico |
| `like` | Contiene stringa (case-insensitive) — **preferito per ricerca testuale** |
| `n_like` | Non contiene |
| `starts_with`, `ends_with` | Inizia/finisce con |
| `in`, `nin` | In lista / non in lista |
| `between` | Tra due valori |
| `date_before`, `date_after` | Prima/dopo una data |
| `date_time_before`, `date_time_after` | Prima/dopo un datetime |
| `array_overlap`, `n_array_overlap` | Intersezione/non intersezione array |
| `array_contains` | Array contiene |
| `eq_null`, `n_eq_null` | È null / non è null |
| `checked`, `unchecked` | Boolean true/false |

### Combinatori logici

```json
{"_and": [{"campo1": {...}}, {"campo2": {...}}]}
{"_or": [{"campo1": {...}}, {"campo2": {...}}]}
```

### Campi nested (dot notation)

Funziona su molti endpoint (non tutti):
- `application.app_name` — nome app nel ticket
- `partner.name` — nome partner in lead/contatti
- `user.flg_valid` — utente attivo per dipendenti

**Attenzione**: la dot notation NON funziona per `owner.des_name` e `owner.des_surname` nei ticket. Usare `search_concat` come fallback.

### Campi computed

- `search_concat` (ticket): concatena titolo, messaggi, nomi utente, business
- `search_concat` (ordini/sales): concatena lead, partner, progetto

### Paginazione

Il campo `total` nella risposta indica il numero totale. Usare `offset` per scorrere:
```json
{"limit": 200, "offset": 0}
{"limit": 200, "offset": 200}
```

## Endpoint principali

### Ferie e Assenze
- `POST /outages/search` — cerca assenze
  - Campi search: `dat_from`, `dat_to`, `employee.des_name`
  - Item: `employee`, `dat_from`, `dat_to`, `am_pm`, `des_note`, `tms_approval`, `flg_declined`

### Staffing
- `POST /staffing/search` — cerca allocazioni
  - Campo chiave: `dat_week` (sempre lunedì, YYYY-MM-DD), operatore `eq`
  - Item: `employee`, `category`, `sub_category`, `sale.lead.name` (progetto), `num_hours`, `dat_week`

### Presenze
- `POST /presences/search` — chi è in ufficio
  - Campi: `calendar.dat_calendar` con `date_after`/`date_before`
  - Item: `employee`, `calendar`, `cod_probability`

### Rendicontazione
- `POST /reporting/search` — ore rendicontate
  - Campi: `dat_month` con `date_after`/`date_before`
  - Item: `employee`, `category`, `sub_category`, `sale.lead.name`, `num_hours`, `dat_day`

### Ticket
- `POST /application_ticket/search` — ticket applicazioni
  - Campi search: `cod_status`, `cod_gravity`, `cod_category`, `application.app_name`, `search_concat`
  - Sort consigliato: `dat_creation desc`
  - **Nota**: `owner.des_name` NON funziona. Usare `search_concat` per cercare per owner.
- `GET /application_ticket/{id}` — dettaglio ticket

### Applicazioni
- `POST /applications/search` — lista applicazioni
  - Campi search: `app_name`, `project_status`, `env`
  - Item: `app_name`, `env`, `project_status`, `partner`, `health` (dict), `summary` (dict con versions), `application_maintainers`
  - **Nota**: `health` e `summary` sono dict, non stringhe

### Errori Applicazioni
- `POST /application/errors/backend/search` — errori backend
- `POST /application/errors/frontend/search` — errori frontend
  - Campi: `application.app_name`, `des_status`
  - Sort consigliato: `dat_last_occurrence desc`

### CRM — Opportunità
- `POST /leads/search` — lead/opportunità
  - Campi: `partner.name` (like), `cod_status` (eq)
  - Sort consigliato: `dat_creation desc`

### CRM — Ordini
- `POST /sales/search` — ordini/vendite
  - Campi: `search_concat` (like), `cod_sales_status` (eq), `dat_creation` (date_after per anno)
  - Sort consigliato: `dat_creation desc`

### CRM — Clienti
- `POST /partners/search` — clienti/partner
  - Campi: `name` (like), `cod_sector` (eq)

### CRM — Contatti
- `POST /contacts/search` — contatti persone
  - Campi: `des_name`, `des_surname` (like, usare `_or`), `partner.name` (like)

### Dipendenti
- `GET /employees/myself` — dati del dipendente corrente
  - I campi stipendio NON sono restituiti senza permessi avanzati
- `POST /employees/search` — richiede permesso `employees:read` (non disponibile per utenti normali)

### Economics
- `GET /economics/revenues/to-issue/{company}` — tranche da emettere (lista diretta)
- `GET /economics/revenues/chart-data/{company}/{year}` — revenue mensili
- `GET /economics/revenues/expiring-recurring/{company}` — ricorrenti in scadenza
  - Risposta: lista con `partner_name`, `lead_name`, `amt_lead`, `dat_expiration`, `flg_renew`, `tl_name`, `tl_surname`
- `GET /reporting/employee-working-hours/{year}/{company}` — ore lavorate per dipendente/mese
  - Risposta: lista piatta con `des_name`, `des_surname`, `dat_month`, `total_work_hours`, `num_working_days`

## Valori Enum

| Campo | Valori |
|-------|--------|
| Ticket Status | open, work_in_progress, feature, waiting_customer, solved, closed |
| Ticket Gravity | low, medium, high |
| Ticket Category | data_not_updated, incorrect_data, incorrect_behavior, visibility_issue |
| Error Status | unassigned, assigned, in_progress, fixed, to_ignore |
| Project Status | development, maintenance, retired |
| Lead Status | new, qualified, proposition, won, freezed, lost |
| Sales Status | undefined_tranches, to_be_invoiced, partially_invoiced, totally_invoiced, invoiced_and_paid, invoiced_and_partially_paid |
| Partner Sector | manufacturing, financial_services, technology_software, healthcare, energy, retail, public_sector, logistics, food, other |
| Companies | laif, helia |

## Permessi

L'API usa un sistema di permessi role-based. Un utente normale (es. Technical Project Manager) può:
- Leggere ferie, staffing, presenze, rendicontazione di tutto il team
- Leggere i propri dati dipendente (senza stipendio)
- Leggere economics (tranche, revenue, ricorrenti)
- Leggere ticket, applicazioni, errori, CRM

Non può:
- Vedere dati retributivi (amt_ral, ecc.)
- Cercare altri dipendenti via `/employees/search`

## MCP Server

Il server MCP Wolico è in `mcp-servers/wolico/`.

**Architettura**: `server.py` → `tools/*.py` (23 tool) + 4 MCP Resources

**Tool**: tutti read-only con `ToolAnnotations`. Usano `paginated_search()` per paginazione automatica, `build_search()` per costruire filtri, `safe_call()` per error handling.

**Resources**: `wolico://dipendenti`, `wolico://applicazioni`, `wolico://clienti`, `wolico://enum` — dati semi-statici con cache TTL 5 min.

**Transport**: stdio (locale), Streamable HTTP (Lambda/remoto).
