# Repository Core LAIF

Repository di riferimento clonate per contesto. **Non modificare direttamente** — servono come fonte di informazioni per la KB.

---

## Indice

| Repo | URL | Scopo |
|------|-----|-------|
| `laif-template/` | https://github.com/laif-group/laif-template | Base per tutti i progetti LAIF (fork). Monorepo con FastAPI backend + Next.js frontend. |
| `ds/` | https://github.com/laif-group/ds | Design System condiviso. Pacchetto npm `@laif/ds` con 137+ componenti React. |
| `laif-cdk/` | https://github.com/laif-group/laif-cdk | Infrastruttura AWS via CDK. Il TemplateStack è lo stack usato per tutti i progetti. |

---

## Uso

Queste repo vengono consultate per:
- Comprendere lo stack e le convenzioni prima di iniziare un progetto
- Verificare componenti disponibili nel DS
- Capire l'infrastruttura disponibile

I riassunti strutturati sono in `knowledge/azienda/`:
- `overview.md` — chi è LAIF, team, modello di lavoro
- `stack.md` — tecnologie, pattern, convenzioni di codice
- `infrastruttura.md` — architettura AWS, configurazione, deploy
- `processi.md` — flussi di lavoro, CI/CD, regole Windsurf

---

## Aggiornamento

Le repo vengono aggiornate periodicamente (pull) per restare allineate.
Se ci sono modifiche rilevanti, aggiornare i file in `knowledge/azienda/`.
