# Test nel pre-commit hook — Problema di performance

| Campo | Valore |
|---|---|
| **ID** | 92 |
| **Stack** | laif-template |
| **Tipo** | Bug |
| **Status** | In corso |

## Descrizione originale

Mettere dei test complessi che richiedono l'interazione con dei container e leggerne i log per capire gli errori nel pre-commit hook rallenta immensamente il processo di push e non dà alcuna visibilità sui risultati. Il linting può stare in un pre-commit hook, i test dovrebbero essere lanciati alla PR su dev.

## Piano di risoluzione

1. **Già in corso.** Verificare lo stato attuale e i branch aperti.
2. **Rimuovere i test di integrazione backend e i test E2E dal pre-commit hook** — eliminare gli step che avviano container Docker, eseguono test pytest con dipendenze esterne e test Playwright/Cypress dal file `.pre-commit-config.yaml` (o equivalente hook script).
3. **Mantenere solo il linting nel pre-commit hook**:
   - Backend: **Ruff** (lint + format check).
   - Frontend: **ESLint** + **Prettier** (o Biome, se adottato).
   - Type checking: opzionale, valutare se `tsc --noEmit` e `mypy` sono abbastanza veloci da restare nel hook.
4. **Spostare i test nella pipeline GitHub Actions sulla PR verso dev**:
   - Creare (o aggiornare) il workflow `.github/workflows/pr-tests.yml`.
   - Step 1: lint (stessa configurazione del pre-commit, per sicurezza).
   - Step 2: test backend (pytest con servizi Docker via `services:` in GitHub Actions).
   - Step 3: test E2E (se presenti).
   - Configurare come check bloccante sulla PR.
5. **Aggiungere i test come primo stage nella pipeline di deploy su dev** — in modo che un merge su dev che rompe i test blocchi il deploy prima che arrivi all'ambiente.
6. **Aggiornare i comandi `just`** — adeguare `just test`, `just lint`, `just pre-commit` per riflettere la nuova separazione. Documentare nel README del template.

### Issue correlate

- **Parent issue**: Test improvements (ID 130).

## Stima effort

**3-4h** — la rimozione dal hook è rapida, il grosso del lavoro è configurare correttamente la pipeline GitHub Actions con i servizi Docker e verificare che funzioni su tutti i progetti.
