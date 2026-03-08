# Stack Tecnologico LAIF

← [System.md](../../System.md) · [overview.md](overview.md) · [infrastruttura.md](infrastruttura.md) · [processi.md](processi.md)

#stack:nextjs #stack:fastapi #stack:postgresql #stack:aws

## Panoramica

Tutti i progetti LAIF partono da `laif-template` — un monorepo con backend Python e frontend Next.js.

---

## Backend

| Componente | Tecnologia | Versione |
|------------|-----------|----------|
| Framework | FastAPI | 0.131+ |
| Linguaggio | Python | 3.12+ |
| ORM | SQLAlchemy | 2.0 |
| Database | PostgreSQL | 15-17 |
| Validazione | Pydantic | 2.x |
| Autenticazione | JWT + API Key (HMAC-SHA256) | |
| Migrazione DB | Alembic | 1.18+ |
| File Storage | AWS S3 (boto3) | |
| Task runner | Justfile | |
| Linting | Ruff | |
| Test | pytest (asyncio) | |

### Pattern architetturali backend

- **RouterBuilder**: API fluente per definire endpoint REST (CRUD automatico)
- **CRUDService**: Classe base per business logic (create, read, update, delete, batch, file)
- **SecurityScope**: JWT + API Key con permessi `"risorsa:azione"` (es. `"users:read"`)
- **Modelli centralizzati**: TUTTI i modelli in `backend/src/template/models.py`

### Convenzioni naming colonne DB

| Prefisso | Significato | Esempio |
|----------|-------------|---------|
| `id_` | Primary/Foreign key | `id_user` |
| `cod_` | Codici/identificatori | `cod_order` |
| `des_` | Descrizioni | `des_product` |
| `dat_` | Date (YYYY-MM-DD) | `dat_birth` |
| `tms_` | Timestamp | `tms_created` |
| `val_` | Valori numerici | `val_quantity` |
| `amt_` | Importi monetari | `amt_total` |
| `flg_` | Boolean | `flg_active` |

---

## Frontend

| Componente | Tecnologia | Versione |
|------------|-----------|----------|
| Framework | Next.js (App Router) | 16.x |
| Linguaggio | TypeScript | 5.9+ |
| UI Components | `@laif/ds` (design system LAIF) + shadcn/ui | 0.2.74 |
| Styling | Tailwind CSS | 4.x |
| State management | Redux Toolkit | 2.x |
| API client | openapi-ts (auto-generato da OpenAPI spec) | |
| Data fetching | TanStack Query (React Query) | 5.x |
| Form | React Hook Form + Zod | |
| i18n | react-intl (EN + IT) | |
| Charts | amCharts 5 | |
| Test | Playwright (component + E2E) | |

### Architettura frontend — "Soft Onion"

```
src/
├── app/                     ← Next.js App Router (pagine)
│   └── (authenticated)/     ← Route protette
├── features/                ← Moduli feature (project-specific)
│   └── [feature-name]/
│       ├── types/
│       ├── services/        ← Hook custom (useCustomQuery, useCustomMutation)
│       ├── components/
│       ├── widgets/
│       ├── modals/
│       ├── store/           ← Redux slice (montata sullo store centrale)
│       └── [FeatureName]Main.tsx
├── components/              ← Componenti globali condivisi
│   └── ui/                  ← shadcn components
├── store/                   ← Redux store centralizzato
├── services/                ← Hook API globali
├── config/                  ← Navigation, tema
└── lib/                     ← Config librerie terze parti
```

### Convenzioni naming frontend

| Tipo | Formato | Esempio |
|------|---------|---------|
| Componenti React | PascalCase | `UserCard.tsx` |
| Hook | camelCase + `.hook.ts` | `useGetOrders.hook.ts` |
| Servizi | camelCase + `.service.ts` | `callExternalAPI.service.ts` |
| Helper | camelCase + `.helper.ts` | `formatDate.helper.ts` |
| Tipi | camelCase + `.types.ts` | `order.types.ts` |
| Redux slice | camelCase + `.slice.ts` | `navigation.slice.ts` |
| Cartelle | kebab-case | `user-management/` |

**Regola**: nomi di almeno 2-3 parole (evitare nomi generici come `card.tsx`, `list.tsx`).

---

## Design System (`@laif/ds`)

Pacchetto npm con **137+ componenti** organizzati in 3 livelli:

| Livello | Componenti | Esempi |
|---------|-----------|--------|
| **Atoms** (42) | Componenti base | Button, Input, Badge, Checkbox, Switch, Tooltip |
| **Molecules** (60) | Combinazioni | Card, Dialog, DataTable, Calendar, Select, Tabs |
| **Organisms** (35) | Componenti complessi | AppEditor (Lexical), AppKanban, Chat, Gantt, Sidebar |

### Regola fondamentale

> **Usare SEMPRE componenti `@laif/ds`.** Mai creare componenti da zero.
> Se un componente manca nel DS → aggiungerlo al DS, non crearlo nel progetto.

### Styling

- Solo **Tailwind CSS token** del DS (es. `text-d-foreground`, `bg-d-primary`)
- Mai classi Tailwind vanilla
- 4 temi disponibili: Light, Dark, Tangerine, Claymorphism
- Storybook su porta 6008 per preview componenti

---

## Workflow di sviluppo standard

1. Leggere `planning.md` per contesto architetturale
2. **Backend**: modello → schema → controller (RouterBuilder) → registra in main.py → migrazione
3. **Genera client API**: `just fe generate-client` (da OpenAPI spec)
4. **Frontend**: feature in `src/features/` → navigation config → componenti DS → hook → traduzioni
5. **Test**: backend `just run pytest`, frontend `npm run test`

---

## Configurazione progetto

Il file `values.yaml` nella root del progetto contiene i token di configurazione:

- `app_name` — nome progetto
- `cod_application` — codice applicazione
- `repo_name` — nome repository
- Account AWS (dev/prod) con ID e regioni
- Domini (es. `app-name.app.laifgroup.com`)

---

## Problemi noti

### Upstream da laif-template → conflitti merge

Quando `laif-template` viene aggiornato, propagare le modifiche ai progetti forkati genera **conflitti di merge** frequenti. Questo è un pain point riconosciuto.

Vedi IDEAS.md (IDEA-008) per il tracking di questa problematica.
