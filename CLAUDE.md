# KnowledgeBase — Istruzioni per Claude Code

Questo file definisce come Claude Code interagisce con la knowledge base di LAIF.

## Struttura del sistema

```
KnowledgeBase/
├── CLAUDE.md               ← sei qui
├── System.md               ← panoramica del sistema
├── CHANGELOG.md             ← tutte le modifiche (struttura + contenuti)
├── IDEAS.md                ← backlog idee e miglioramenti
├── docs/                   ← documentazione navigabile (struttura, skill, workflow)
├── projects/               ← un progetto per cartella
├── patterns/               ← pattern tecnici riutilizzabili cross-progetto
├── skills/                 ← skill e sub-agenti del sistema
├── knowledge/              ← conoscenza cross-progetto (industrie, problemi ricorrenti)
├── core/                   ← repo core LAIF clonate (contesto, non modificare)
├── .tags/                  ← indice tag per ricerca rapida
└── .claude/
    ├── skills/             ← trigger layer skill native Claude Code
    └── hooks/              ← script automazione (tracking skill)
```

Per dettagli completi: `docs/struttura.md`. Per tag: `.tags/index.md`.

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

Se durante il lavoro noti che la struttura reale non corrisponde a quella documentata:

1. Esegui `skills/meta/gestione-kb/` modalità 3 (sync) in autonomia
2. Registra il sync nel changelog

### Regola 3 — Gestione idee e proposte

Quando emergono idee o proposte di miglioramento al framework:

1. **Non svilupparle subito** (a meno che l'utente non lo chieda esplicitamente)
2. Chiedi all'utente: *"Vuoi che lo implementi ora o lo segno in IDEAS.md?"*
3. Se segnare: registra in `IDEAS.md` via `skills/meta/gestione-kb/` modalità 2
4. Se fare subito: procedi con l'implementazione

### Regola 4 — Operazioni su repository di progetto (BLOCCANTE)

Quando operi su una repository di progetto (non sulla KB):

1. **Consulta prima la KB**: leggi `projects/[nome]/` per contesto, decisioni, convenzioni
2. **Consulta contesto rilevante**: esegui `python3 skills/meta/contesto-progetto/match.py [nome-progetto]` e leggi i file suggeriti (pattern, problemi tecnici, knowledge di settore)
3. **Usa SEMPRE `just`** per qualsiasi operazione (migrazioni, build, test, server). Mai comandi diretti (`alembic`, `npm`, `docker compose`, ecc.)
4. **Non prendere iniziative su operazioni irreversibili** (migrazioni DB, eliminazione file, modifiche schema): chiedi prima schema, conferma, contesto
5. **Se non conosci una convenzione** (es. quale schema DB usare), chiedi — non assumere

### Regola 5 — Brainstorming post-sviluppo

Alla fine di ogni sessione di sviluppo significativa (non per fix banali o solo consultazione KB):

1. Analizza il lavoro svolto nella sessione
2. Proponi all'utente un brainstorming seguendo `skills/development/brainstorming-post-sviluppo/SKILL.md`
3. Presenta le idee emerse (pattern, skill, workflow, miglioramenti)
4. **Verifica problemi tecnici**: se hai incontrato problemi risolvibili, proponi di salvarli in `knowledge/problemi-tecnici/`
5. Se l'utente approva: sviluppa gli asset approvati e aggiorna la KB
6. Se l'utente declina: registra le idee più rilevanti in `IDEAS.md`

**Non è bloccante**: se l'utente chiude la sessione senza brainstorming, non insistere.

---

## Come usare le skill

Le skill sono in `skills/`. Ogni skill è una **cartella** con un `SKILL.md` dentro.
Per invocarla: leggi il `SKILL.md` e segui il processo conversazionale.

Per il catalogo completo, i flussi Mermaid, il ciclo di vita e le dipendenze: vedi `docs/skills.md`.
Per i workflow per fase (presales, development, maintenance, meta): vedi `docs/workflow.md`.

**Skill in beta**: all'inizio avvisa che è in beta. Durante l'uso, ad ogni step chiede se il processo ha senso o se va modificato.

## Divisione strumenti

- **Claude Code**: gestione KB, review codice, esecuzione test, aggiornamento KB post-sviluppo
- **Windsurf**: scrittura codice, implementazione feature, debug, refactoring

Claude Code opera con parsimonia (costi). Windsurf gestisce lo sviluppo intensivo.

## Creare un nuovo progetto

**Non duplicare `_template/` manualmente.** Usa la skill:
```
Leggi e segui: skills/presales/init-project/SKILL.md
```

## Contesto aziendale

Il contesto su LAIF (stack, infrastruttura, processi) è in `knowledge/azienda/`.
Le repo core sono clonate in `core/` come riferimento — vedi `core/README.md`.

## Processo pre-commit

La verifica pre-commit è **ibrida**: 4 check automatizzati (script Python) + check semantici (eseguiti dal parent agent). Vedi Regola 1 sopra.

```bash
python3 skills/meta/verifica-pre-commit/run_all.py
```

Dettagli completi: `skills/meta/verifica-pre-commit/SKILL.md`
