---
tags: [convenzioni, git, laif-kb]
---

# Convenzioni Git Flow

Come gestiamo branch, commit e PR nei progetti LAIF.

## Branch

| Branch | Scopo | Chi pusha |
|--------|-------|-----------|
| `main` | Codice in produzione | Solo via PR (o CI) |
| `feature/[nome]` | Nuova feature | Sviluppatore assegnato |
| `fix/[nome]` | Bug fix | Sviluppatore assegnato |
| `hotfix/[nome]` | Fix urgente in prod | Tech lead |

Formato nome: `feature/RF-XX-breve-descrizione` (es. `feature/RF-12-email-templates`).

## Commit message

Formato: `tipo(scope): descrizione breve`

| Tipo | Quando |
|------|--------|
| `feat` | Nuova funzionalita |
| `fix` | Bug fix |
| `refactor` | Refactoring senza cambio comportamento |
| `docs` | Solo documentazione |
| `chore` | Manutenzione, dipendenze, config |
| `test` | Aggiunta o modifica test |

Esempi:
- `feat(orders): add export to CSV`
- `fix(auth): handle expired refresh token`
- `chore(deps): update fastapi to 0.131`

## Pull Request

- **Titolo**: stesso formato dei commit (`feat(scope): descrizione`)
- **Descrizione**: cosa cambia, perche, come testare
- **Review**: almeno 1 approvazione richiesta
- **Merge**: squash merge su `main`

## Upstream da laif-template

Quando `laif-template` viene aggiornato:

1. Aggiungere remote upstream (se non presente):
   ```bash
   git remote add upstream [url-laif-template]
   ```
2. Fetch e merge:
   ```bash
   git fetch upstream
   git merge upstream/main
   ```
3. Risolvere conflitti — frequenti su file condivisi tra template e progetto
4. Testare tutto prima di pushare

**Nota**: la cartella `template/` nel progetto dovrebbe essere read-only rispetto al template base. I conflitti nascono quando il progetto modifica file che anche il template aggiorna.
