# LAIF-KB — Istruzioni per Claude Code

## Cos'e questo repo

Knowledge base condivisa di LAIF. Contiene convenzioni di codice, mappa dei processi aziendali e skill operative.

## Struttura

```
laif-kb/
├── convenzioni/              Regole naming DB, git flow, standard codice
├── processi/                 Mappa lifecycle con link a skill e conoscenze
└── skills/                   Skill autocontenute (SKILL.md + scripts/ + templates/)
    ├── analisi-repo/         Analisi complessita repository LAIF
    └── documenta-processo/   Documentazione processi guidata
```

## Regole

1. **Lingua**: italiano per tutti i contenuti
2. **Link relativi**: usa sempre link relativi tra documenti
3. **Skill autocontenute**: ogni skill ha dentro tutto cio che le serve (script, template, istruzioni)
4. **Template dentro le skill**: i template vivono in `skills/[nome]/templates/`, non in una cartella centralizzata

## Come usare le skill

1. Leggi il `SKILL.md` della skill desiderata
2. Segui il processo conversazionale (la skill fa domande prima di produrre output)
3. L'output viene generato usando il template interno della skill

## Convenzioni file

- Nomi file e cartelle: **kebab-case**, in italiano
- Formato date: **YYYY-MM-DD**
- Diagrammi: **Mermaid** (renderizzato da GitHub)
