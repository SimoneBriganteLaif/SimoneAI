---
titolo: "Integrazione API Async con Client + Poller + Processor Registry"
categoria: "integrazioni"
complessità: "media"
usato-in: ["lamonea"]
data-creazione: "2026-03-12"
ultimo-aggiornamento: "2026-03-12"
tags:
  - "#pattern:integrazione"
  - "#stack:fastapi"
  - "#stack:postgresql"
---

# Pattern: Integrazione API Async con Client + Poller + Processor Registry

## Problema

Devi integrare un sistema esterno che espone API asincrone basate su job: la chiamata non restituisce subito il risultato, ma un UUID che identifica il job. Il risultato va recuperato in polling dopo un certo tempo.

**Segnali che questo pattern è quello giusto**:
- L'API esterna restituisce un UUID/job ID invece del risultato diretto
- Il risultato va recuperato con chiamate separate di polling
- Devi integrare più entità dallo stesso sistema (es. articoli, clienti, fornitori)
- Vuoi poter triggerare le sync via API REST e monitorarne lo stato
- Il sistema esterno è un gestionale legacy (TeamSystem, SAP, ecc.) con API batch

---

## Soluzione

Separare le responsabilità in tre componenti distinti + una tabella DB per il tracking:

```
API Trigger
    ↓
TSClient (HTTP stateless)
    ↓ UUID
ts_sync_jobs (DB)
    ↑ polling ogni N secondi
TSPoller (asyncio background task)
    ↓ payload completato
Processor Registry
    ↓
ArticoliProcessor / ClientiProcessor / ...
    ↓
stg.* (staging RAW)
```

### Struttura

**TSClient** — solo HTTP, nessuna persistenza:
- `submit_request(...)` → UUID
- `get_status(uuid)` → stato job
- `get_response(uuid)` → payload completo

**TSPoller** — asyncio task nel lifespan FastAPI:
- Loop ogni N secondi (default 30)
- Legge dal DB i job in status `polling`
- Per ogni job: chiama `get_status`, se completato chiama `get_response` e dispatcha al processor
- Mantiene registry: `entity → callable`

**Processor** — uno per entità:
- Riceve il payload raw
- Fa mapping campi sorgente → schema staging
- Upsert in `stg.*`

**ts_sync_jobs** — tracking in DB:
- Colonne: `entity`, `ditta`, `mode` (full/incremental), `ts_job_uuid`, `status`, `created_at`, `completed_at`, `records_processed`, `error_message`

### Implementazione

**Passo 1** — Creare TSClient stateless:

```python
# backend/app/integrations/teamsystem/client.py
class TSClient:
    async def submit_request(self, codice_ws, ditta, operazione, tabella_campi,
                              variazioni=None, variaz_data=None, variaz_ora=None) -> str:
        body = {"CodiceWS": codice_ws, "Schema": "1", "Versione": "20250006",
                "Operazione": operazione, "Ditta": ditta, "TabellaCampi": tabella_campi}
        if variazioni:
            body |= {"Variazioni": variazioni, "VariazData": variaz_data, "VariazOra": variaz_ora}
        headers = {"Authorization": f"Bearer {settings.TS_BEARER_TOKEN}",
                   "Content-Type": "application/json"}  # obbligatorio anche senza body
        resp = await httpx_client.post(f"{settings.TS_BASE_URL}/EVWSASYNC", json=body, headers=headers)
        return resp.json()["uuid"]

    async def get_status(self, uuid: str) -> str: ...
    async def get_response(self, uuid: str) -> dict: ...
```

**Passo 2** — Creare tabella `ts_sync_jobs` (schema DB dove vivono gli altri dati):

```sql
CREATE TABLE prs.ts_sync_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity VARCHAR NOT NULL,
    codice_ws VARCHAR NOT NULL,
    ditta VARCHAR(3) NOT NULL,
    mode VARCHAR NOT NULL,           -- 'full' | 'incremental'
    ts_job_uuid VARCHAR UNIQUE,
    status VARCHAR NOT NULL DEFAULT 'queued',  -- queued|polling|completed|failed
    variaz_data VARCHAR(8),
    variaz_ora VARCHAR(6),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    last_polled_at TIMESTAMPTZ,
    records_processed INTEGER,
    error_message TEXT
);
```

**Passo 3** — Creare TSPoller con registry:

```python
# backend/app/integrations/teamsystem/poller.py
class TSPoller:
    def __init__(self, db_factory, ts_client, poll_interval=30):
        self._registry: dict[str, callable] = {}
        self.is_running = False
        self.last_poll_at = None
        self.active_jobs_count = 0

    def register_processor(self, entity: str, callback: callable):
        self._registry[entity] = callback

    async def start(self):
        self.is_running = True
        asyncio.create_task(self._loop())

    async def _loop(self):
        while self.is_running:
            async with self._db_factory() as db:
                jobs = await db.query(TSyncJob).filter_by(status='polling').all()
                for job in jobs:
                    status = await self._client.get_status(job.ts_job_uuid)
                    if status == 'COMPLETED':
                        payload = await self._client.get_response(job.ts_job_uuid)
                        await self._registry[job.entity](job.ditta, payload)
                        job.status = 'completed'
                        job.completed_at = datetime.now(UTC)
                    elif status == 'ERROR':
                        job.status = 'failed'
                    job.last_polled_at = datetime.now(UTC)
            self.last_poll_at = datetime.now(UTC)
            await asyncio.sleep(self.poll_interval)
```

**Passo 4** — Collegare al lifespan FastAPI:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    ts_client = TSClient()
    poller = TSPoller(get_db, ts_client)
    poller.register_processor('articoli', ArticoliProcessor(ts_client).process_payload)
    app.state.ts_poller = poller
    app.state.ts_client = ts_client
    await poller.start()
    yield
    await poller.stop()

app = FastAPI(lifespan=lifespan)
```

**Passo 5** — Esporre API trigger:

```
POST /api/v1/integrations/{sistema}/sync
  body: {entity, ditta, mode}
  → inserisce ts_sync_jobs, chiama submit_request, aggiorna uuid e status='polling'

GET /api/v1/integrations/{sistema}/jobs
GET /api/v1/integrations/{sistema}/jobs/{job_id}
GET /api/v1/integrations/{sistema}/health   ← stato poller (running, last_poll_at, processors)
```

**Passo 6** — Implementare un Processor per entità:

```python
class ArticoliProcessor:
    async def process_payload(self, ditta: str, payload: dict):
        for record in payload["TabellaCampi"]:
            row = self._map(record)   # campi sorgente → schema stg
            await db.execute(
                insert(StgArticoli).values(row)
                .on_conflict_do_update(
                    index_elements=['codice_magazzino', 'ditta'],
                    set_={**row, 'synced_at': func.now()}
                )
            )
```

---

## Trade-off

**Vantaggi**:
- TSClient testabile in isolamento (nessuna dipendenza DB)
- Aggiungere una nuova entità = scrivere solo un nuovo Processor e registrarlo
- API trigger rende le sync osservabili e ripetibili senza accesso diretto al server
- Il polling ogni 30s è sufficiente per batch grandi; non serve websocket o push
- La tabella ts_sync_jobs fornisce storico completo di ogni sync

**Svantaggi / costi**:
- Il poller asyncio può crashare silenziosamente → serve endpoint `/health` diagnostico
- Se il backend si riavvia mentre un job è in `polling`, il job rimane stuck → serve logica di recovery all'avvio (query job in polling da > N minuti e riprende il polling)
- La latenza è almeno pari al poll_interval (30s) — non adatto per sync real-time

**Quando NON usare questo pattern**:
- L'API esterna è sincrona e risponde in < 5s → chiamata diretta, nessun poller
- Serve real-time (< 1s) → considera webhook/push se disponibile
- Un solo tipo di entità da integrare → il registry è over-engineering, un singolo processor basta

---

## Varianti

### Variante: sync incrementale via Variazioni

Aggiungere ai parametri della request: `Variazioni="S"`, `VariazData`, `VariazOra`.
Il `VariazData/Ora` si legge dall'ultima sync completata con successo dalla tabella `ts_sync_jobs`.
Utile per tenere lo staging allineato senza full load ogni volta.

### Variante: multi-ditta

Se il sistema esterno ha ditte/tenant separati (es. TeamSystem con ditte 49, 133, 212),
aggiungere `ditta` come parametro del job. Con `ditta='all'` il trigger API crea N job
separati (uno per ditta). Il Processor riceve `ditta` come parametro e la usa come parte
della PK nello staging.

---

## Esempi reali in LAIF

| Progetto | Come è stato usato | Note / deviazioni |
|---------|-------------------|------------------|
| Lamonea | Integrazione TeamSystem Lynfa Azienda — articoli, clienti, fornitori | Multi-ditta (49/133/212), solo endpoint async (sincrono rotto su SaaS) |

---

## Risorse esterne

- [FastAPI lifespan events](https://fastapi.tiangolo.com/advanced/events/)
- [asyncio.create_task](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task)
