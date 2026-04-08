# LAIF Knowledge Base

La knowledge base condivisa di LAIF. Conoscenza aziendale, processi, convenzioni e skill operative — tutto in un posto solo.

## Navigazione

| Sezione | Cosa trovi | Per chi |
|---------|-----------|--------|
| [convenzioni/](convenzioni/) | Regole di naming, git flow, standard di codice | Sviluppatori |
| [processi/](processi/) | Mappa del ciclo di vita di un progetto LAIF | Tutti |
| [skills/](skills/) | Skill automatizzate (analisi repo, documentazione processi) | Utenti Claude Code |

## Come contribuire

- **Nuovo contenuto**: apri una Pull Request
- **Fix typo o link rotto**: push diretto su `main`
- **Nuova skill o modifica strutturale**: PR + discussione

Se usi Claude Code, le [skill](skills/) ti guidano nella creazione di contenuti con il formato corretto.

## Struttura

```
laif-kb/
├── convenzioni/          Regole di codice e naming
├── processi/             Mappa lifecycle → skill
└── skills/               Skill con script e template interni
    ├── analisi-repo/     Analisi complessita repository
    └── documenta-processo/  Documentazione processi guidata
```
