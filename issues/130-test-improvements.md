# Test Improvements

| Campo     | Valore           |
|-----------|------------------|
| ID        | 130              |
| Stack     | (cross-stack)    |
| Tipo      | Proposal         |
| Status    | In corso         |
| Priorita  | —                |
| Tag       | Filone Test      |

## Descrizione originale

Test improvements — issue ombrello con sotto-item.

### Sotto-issue

- **ID 92** — Test pre-commit hook (In corso)
- Linting pipeline
- Test pipeline

## Piano di risoluzione

Questa e una issue ombrello. Il lavoro e gia in corso e si articola nei seguenti step:

1. **Fix pre-commit hooks (issue 92 — in corso)** — Risolvere i problemi con i pre-commit hook per i test. L'hook deve:
   - Eseguire i test rilevanti prima di ogni commit
   - Non bloccare per test lenti (solo test unitari rapidi)
   - Dare feedback chiaro in caso di fallimento

2. **Setup GitHub Actions per test su PR** — Configurare una pipeline CI che:
   - Si attiva su ogni pull request
   - Esegue l'intera test suite (unit + integration)
   - Blocca il merge se i test falliscono
   - Report dei risultati visibile nella PR

3. **Aggiungere linting alla pipeline CI** — Integrare linting automatico:
   - Backend: `ruff` (o `flake8`) + `black` per Python
   - Frontend: `eslint` + `prettier`
   - Check nella pipeline CI, non solo in pre-commit

4. **Migliorare determinismo test E2E** — I test E2E tendono a essere flaky:
   - Identificare e fixare test non deterministici
   - Aggiungere retry per test noti come instabili (temporaneo)
   - Migliorare setup/teardown dei dati di test

5. **Aggiungere test suite frontend** — Attualmente la copertura frontend e limitata:
   - Setup Vitest (o Jest) per unit test React
   - Test per hook custom e utility
   - Test per componenti critici (form, tabelle, navigation)

6. **Definire target di code coverage** — Stabilire obiettivi realistici:
   - Backend: target iniziale 60%, obiettivo 80%
   - Frontend: target iniziale 40%, obiettivo 60%
   - Tracking progressivo, non bloccante inizialmente

### Sotto-issue correlate

Le singole sotto-issue tracciano il lavoro specifico. Questa issue si chiude quando tutte le sotto-issue sono completate.

## Stima effort

**Effort distribuito nel tempo** — Questa e una issue di lungo periodo:
- Pre-commit hooks (issue 92): ~4h (in corso)
- Pipeline CI test: ~8h
- Pipeline CI linting: ~4h
- Test E2E determinism: ~8h (ongoing)
- Frontend test suite: ~16h
- Coverage targets e tracking: ~4h
