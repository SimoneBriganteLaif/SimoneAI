# Improve Git Branches Workflow

| Campo     | Valore           |
|-----------|------------------|
| ID        | 136              |
| Stack     | (cross-stack)    |
| Tipo      | Proposal         |
| Status    | Backlog          |
| Priorita  | —                |
| Tag       | Filone Upstream  |

## Descrizione originale

Currently we have the 'release branch' (i.e. master) that's just used as a trigger for the release GitHub Action, we could do the same with just the tags.

## Piano di risoluzione

1. **Analisi dello stato attuale** — Attualmente il workflow prevede:
   - Branch `dev` per lo sviluppo
   - Branch `master` usato solo come trigger per la GitHub Action di release
   - Merge da `dev` a `master` per avviare il deploy
   - Il branch `master` non ha valore aggiuntivo rispetto a un tag

2. **Eliminare la necessita del branch di release** — Il branch `master` e ridondante se usato solo come trigger. I tag git sono lo strumento corretto per marcare le release.

3. **Aggiornare le GitHub Actions** — Modificare i workflow per triggerare su push di tag:
   ```yaml
   on:
     push:
       tags:
         - 'v*'  # Trigger su tag che iniziano con 'v'
   ```
   Invece dell'attuale trigger su push al branch master.

4. **Semplificare a: `dev` + tag** — Il nuovo workflow diventa:
   - `dev` e l'unico branch principale (sviluppo continuo)
   - Per rilasciare: creare un tag (`v1.2.3`) su `dev`
   - La GitHub Action si attiva sul tag e deploya
   - Feature branch da `dev`, merge back in `dev`

5. **Aggiornare documentazione e workflow del team** — Documentare il nuovo processo:
   - Come creare un tag di release (`git tag -a v1.2.3 -m "Release 1.2.3"`)
   - Convenzione di naming dei tag (semver)
   - Aggiornare i README dei progetti
   - Aggiornare eventuali script di release

6. **Considerare le implicazioni con issue 146** — L'issue 146 riguarda il fork del template da master. Se master viene eliminato come branch di release:
   - Verificare che il fork del template funzioni da `dev`
   - Oppure usare i tag come punto di fork
   - Coordinare le due modifiche

## Stima effort

**8-12 ore** — Principalmente lavoro di configurazione e coordinamento:
- Analisi e piano (~2h)
- Modifica GitHub Actions (~3h)
- Test del nuovo workflow (~2h)
- Aggiornamento documentazione (~2h)
- Coordinamento con issue 146 (~2h)
