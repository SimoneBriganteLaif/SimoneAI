# KnowledgeBase — Istruzioni per Claude Code

Questo file definisce come Claude Code interagisce con la knowledge base di LAIF.

## Struttura del sistema

```
KnowledgeBase/
├── CLAUDE.md               ← sei qui
├── System.md               ← panoramica del sistema
├── CHANGELOG-framework.md  ← modifiche alla struttura del sistema
├── CHANGELOG-contenuti.md  ← modifiche ai contenuti operativi
├── IDEAS.md                ← backlog idee e miglioramenti
├── docs/                   ← documentazione navigabile (struttura, skill, workflow)
├── projects/               ← un progetto per cartella
│   └── _template/          ← template base per nuovi progetti
├── patterns/               ← pattern tecnici riutilizzabili cross-progetto
├── skills/                 ← skill e sub-agenti del sistema
│   └── meta/               ← skill di gestione del sistema stesso
├── knowledge/              ← conoscenza cross-progetto (industrie, problemi ricorrenti)
└── .tags/                  ← indice dei tag per ricerca rapida
```

Per la documentazione completa della struttura vedi `docs/struttura.md`.

## Regole fondamentali

1. **Tutta la documentazione è in italiano**
2. **Claude Code gestisce questa cartella.** Windsurf agisce solo sulle repository di codice.
3. **Ogni skill ha un loop conversazionale**: chiedi sempre chiarimenti prima di produrre output.
4. **Aggiorna la KB dopo ogni decisione rilevante** (non a fine progetto).
5. **Taglia il tag corretto** su ogni file che crei o aggiorni (vedi `.tags/index.md`).

## Come usare le skill

Le skill sono in `skills/`. Ogni skill è una **cartella** con un `SKILL.md` dentro.
Per invocarla: leggi il `SKILL.md` e segui il processo conversazionale.

Ogni skill ha:
- **Frontmatter YAML**: metadati (nome, fase, output)
- **Loop conversazionale**: domande da fare prima di produrre output
- **Processo di produzione**: passi da eseguire
- **Output in chat**: riepilogo obbligatorio al termine

## Workflow per fase

### Presales
1. **Nuovo progetto** → `skills/presales/init-project/`
   Chiede: nome progetto, URL GitHub, link Notion. Fa tutto in autonomia.
2. **Struttura requisiti** → `skills/presales/estrazione-requisiti/`
   Input: note Notion già salvate. Output: `requisiti.md`
3. **Documenti per cliente** → `skills/presales/genera-documenti/`
   Input: `requisiti.md` validato. Output: allegato tecnico + brief Windsurf

### Development
1. Decisione tecnica → `skills/development/estrazione-decisioni/`
2. Feature completata → aggiorna `projects/[nome]/development/feature-log.md` direttamente
3. Fine sprint → `skills/development/aggiornamento-kb/`

### Maintenance / Consulta
1. Ricerca per tag → `.tags/index.md`
2. Pattern riutilizzabili → `patterns/`
3. Manutenzione mensile → `skills/maintenance/aggiornamento-periodico/`

### Meta / Gestione KB
1. Registra modifica → `skills/meta/gestione-kb/` (modalità 1)
2. Nuova idea → `skills/meta/gestione-kb/` (modalità 2)
3. Sync documentazione → `skills/meta/gestione-kb/` (modalità 3)
4. Review idee periodica → `skills/meta/gestione-kb/` (modalità 4)

## Divisione strumenti

- **Claude Code**: gestione KB, review codice, esecuzione test, aggiornamento KB post-sviluppo
- **Windsurf**: scrittura codice, implementazione feature, debug, refactoring

Claude Code opera con parsimonia (costi). Windsurf gestisce lo sviluppo intensivo.
Per i flussi di lavoro completi vedi `docs/workflow.md`.

## Creare un nuovo progetto

**Non duplicare `_template/` manualmente.** Usa la skill:
```
Leggi e segui: skills/presales/init-project/SKILL.md
```
La skill gestisce creazione struttura, clonazione repo e lettura Notion in autonomia.

## Tag standard

| Tag | Quando usarlo |
|-----|--------------|
| `#progetto:[nome]` | Su tutti i file di un progetto |
| `#industria:[settore]` | Settore del cliente (es. `#industria:retail`) |
| `#pattern:[tipo]` | Pattern tecnico (es. `#pattern:autenticazione`) |
| `#fase:[presales\|dev\|manutenzione]` | Fase del ciclo di vita |
| `#problema:[tipo]` | Problema ricorrente (es. `#problema:performance`) |
| `#stack:[tecnologia]` | Tecnologia usata (es. `#stack:nextjs`) |
