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
│   └── azienda/            ← contesto aziendale LAIF (stack, infra, processi)
├── core/                   ← repo core LAIF clonate (contesto, non modificare)
│   ├── laif-template/      ← base per tutti i progetti (fork)
│   ├── ds/                 ← design system (@laif/ds)
│   └── laif-cdk/           ← infrastruttura AWS (CDK)
└── .tags/                  ← indice dei tag per ricerca rapida
```

Per la documentazione completa della struttura vedi `docs/struttura.md`.

## Regole fondamentali

1. **Tutta la documentazione è in italiano**
2. **Claude Code gestisce questa cartella.** Windsurf agisce solo sulle repository di codice.
3. **Ogni skill ha un loop conversazionale**: chiedi sempre chiarimenti prima di produrre output.
4. **Aggiorna la KB dopo ogni decisione rilevante** (non a fine progetto).
5. **Taglia il tag corretto** su ogni file che crei o aggiorni (vedi `.tags/index.md`).

---

## Comportamenti autonomi (obbligatori)

Claude Code deve seguire queste regole **in autonomia, senza aspettare che l'utente le chieda**.

### Regola 1 — Prima di ogni `git commit` (BLOCCANTE)

Il commit **non può procedere** finché la verifica non passa:

1. Esegui `python3 skills/meta/verifica-pre-commit/run_all.py`
2. Completa i check semantici descritti in `skills/meta/verifica-pre-commit/SKILL.md`
3. Se **FAIL**: risolvi tutto, poi riesegui
4. Solo con **PASS completo** (script + semantica): procedi con il commit

### Regola 2 — Quando percepisci drift documentazione

Se durante il lavoro noti che la struttura reale non corrisponde a quella documentata (es. una cartella esiste ma non è in `docs/struttura.md`):

1. Esegui `skills/meta/gestione-kb/` modalità 3 (sync) in autonomia
2. Registra il sync nel changelog

### Regola 3 — Gestione idee e proposte

Quando durante la conversazione emergono idee o proposte di miglioramento al framework (dall'utente o da te):

1. **Non svilupparle subito** (a meno che l'utente non lo chieda esplicitamente)
2. Chiedi all'utente: *"Vuoi che lo implementi ora o lo segno in IDEAS.md?"*
3. Se l'utente sceglie di segnarlo: registra in `IDEAS.md` via `skills/meta/gestione-kb/` modalità 2
4. Se l'utente sceglie di farlo subito: procedi con l'implementazione

Questa regola vale per qualsiasi proposta che richieda modifiche non banali al framework.

---

## Come usare le skill

Le skill sono in `skills/`. Ogni skill è una **cartella** con un `SKILL.md` dentro.
Per invocarla: leggi il `SKILL.md` e segui il processo conversazionale.

Ogni skill ha:
- **Frontmatter YAML**: metadati (nome, fase, stato beta/stable, legge, scrive)
- **Perimetro**: cosa fa, cosa NON fa, rimandi ad altre skill
- **Loop conversazionale**: domande da fare prima di produrre output
- **Processo di produzione**: passi da eseguire
- **Output in chat**: riepilogo obbligatorio al termine

**Skill in beta**: all'inizio avvisa che è in beta. Durante l'uso, ad ogni step chiede se il processo ha senso o se va modificato.

## Workflow per fase

### Presales
1. **Nuovo progetto** → `skills/presales/init-project/`
   Chiede: nome progetto, URL GitHub, link Notion. Fa tutto in autonomia.
2. **Struttura requisiti** → `skills/presales/estrazione-requisiti/`
   Input: note Notion già salvate. Output: `requisiti.md`
3. **Allegato contrattuale** → `skills/presales/genera-allegato-tecnico/`
   Input: `requisiti.md` validato. Output: allegato tecnico (max 3 pagine)
4. **Brief mockup** → `skills/presales/genera-mockup-brief/`
   Input: `requisiti.md` validato. Output: brief per Windsurf

### Development
1. Decisione tecnica → `skills/development/estrazione-decisioni/`
2. Feature completata → aggiorna `projects/[nome]/feature-log.md` direttamente
3. Fine sprint → `skills/development/estrazione-pattern/`

### Maintenance / Consulta
1. Ricerca per tag → `.tags/index.md`
2. Pattern riutilizzabili → `patterns/`
3. Audit mensile → `skills/maintenance/audit-periodico/`

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

## Contesto aziendale

Il contesto su LAIF (stack, infrastruttura, processi) è in `knowledge/azienda/`.
Le repo core sono clonate in `core/` come riferimento — vedi `core/README.md`.

Per lo stack tecnico dettagliato: `knowledge/azienda/stack.md`
Per le convenzioni di sviluppo e regole Windsurf: `knowledge/azienda/processi.md`

## Processo pre-commit

La verifica pre-commit è **ibrida**: 4 check automatizzati (script Python) + check semantici (eseguiti dal parent agent). Vedi sezione "Comportamenti autonomi" sopra.

```bash
python3 skills/meta/verifica-pre-commit/run_all.py
```

Dettagli completi: `skills/meta/verifica-pre-commit/SKILL.md`

## Tag standard

| Tag | Quando usarlo |
|-----|--------------|
| `#progetto:[nome]` | Su tutti i file di un progetto |
| `#industria:[settore]` | Settore del cliente (es. `#industria:retail`) |
| `#pattern:[tipo]` | Pattern tecnico (es. `#pattern:autenticazione`) |
| `#fase:[presales\|dev\|manutenzione]` | Fase del ciclo di vita |
| `#problema:[tipo]` | Problema ricorrente (es. `#problema:performance`) |
| `#stack:[tecnologia]` | Tecnologia usata (es. `#stack:nextjs`) |
