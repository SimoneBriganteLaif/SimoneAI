# Processi di Lavoro — LAIF

← [System.md](../../System.md) · [overview.md](overview.md) · [stack.md](stack.md) · [infrastruttura.md](infrastruttura.md)

#industria:software #fase:contesto

## Come nasce un progetto

1. **Fork** da `laif-template` → nuovo repository
2. Configurare `values.yaml` con nome app, account AWS, domini
3. Creare infrastruttura con `laif-cdk` (TemplateStack)
4. Sviluppare feature specifiche del progetto
5. Deploy via CI/CD (GitHub Actions in `.github/`)

---

## Flusso di sviluppo giornaliero

### Backend

1. Definire/aggiornare modello in `backend/src/template/models.py`
2. Creare schema Pydantic in `backend/src/app/schema/`
3. Implementare controller con `RouterBuilder`
4. Registrare router in `main.py`
5. Creare migrazione: `just migrate create`
6. Applicare migrazione: `just migrate upgrade`

### Frontend

1. Generare client API: `just fe generate-client` (da OpenAPI spec)
2. Creare feature in `src/features/[feature-name]/`
3. Usare componenti `@laif/ds` — **mai** creare da zero
4. Aggiornare `src/config/navigation.tsx`
5. Aggiungere traduzioni in `locale/project/`

### Ambiente locale

- Backend: `just run default` (Docker Compose: PostgreSQL + FastAPI con hot-reload)
- Frontend: `npm run dev` (Turbopack)
- Tutto insieme: `just run all`

---

## Processo upstream (laif-template → progetti)

Quando `laif-template` viene aggiornato con fix o nuove feature:

1. Nel progetto forkato, aggiungere `laif-template` come remote upstream
2. `git fetch upstream`
3. `git merge upstream/main`
4. Risolvere conflitti (frequenti, specialmente su file condivisi)

**Problema noto**: i conflitti merge sono un pain point significativo. La cartella `template/` nel progetto dovrebbe essere read-only, ma le modifiche al template base toccano file che i progetti hanno personalizzato.

---

## Windsurf — Regole per lo sviluppo

Il progetto include regole Windsurf in `.windsurf/rules/` che guidano l'AI durante lo sviluppo:

### Backend rules

- **Sempre** usare `RouterBuilder` per endpoint
- **Sempre** usare `CRUDService` per business logic
- **Mai** usare `RoleBasedCRUDService` (deprecato)
- Aggiungere modelli SOLO in `template/models.py`
- Rispettare convenzioni naming colonne DB
- Dopo modifica schema → `just migrate create`
- Dopo modifica route → `just fe generate-client`

### Frontend rules

- Usare SOLO token Tailwind del DS (mai classi vanilla)
- Preferire componenti `@laif/ds` su shadcn/ui raw
- Architettura feature-based (soft onion)
- Redux solo per stato globale
- Hook custom per API call (TanStack Query wrapper)
- No prop drilling (usare Redux o Context)
- Design responsive obbligatorio

### Checklist refactoring

- Quando modifichi un hook, un tipo, o cambi la shape dei dati: **verifica TUTTE le viste** che consumano quei dati. Cerca con grep i file che importano quel hook/tipo.
- Quando estrai logica condivisa (mapping, utility): verifica che ogni consumatore usi la versione condivisa e non una copia locale.
- HTML da fonti esterne (email, CMS): sanitizzare con DOMPurify (vedi pattern `html-sanitization-dompurify`).

---

## CI/CD

Pipeline GitHub Actions in `.github/workflows/`:
- Build e test automatici su push/PR
- Deploy via CDK su ambiente target
- Rebuild condizionale dipendenze

---

## Template vs. Codice progetto

| Dove | Cosa contiene | Modificabile? |
|------|--------------|---------------|
| `backend/src/template/` | Moduli core, pattern, esempi | Solo come riferimento |
| `backend/src/app/` | Logica specifica del progetto | Si |
| `frontend/template/` | Componenti e layout template | Solo come riferimento |
| `frontend/src/` | Feature, pagine, componenti del progetto | Si |
