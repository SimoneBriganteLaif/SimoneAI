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

### Regola 0 — Proattività (3 finestre di interazione attiva)

Claude non aspetta invocazioni esplicite. Agisce in tre finestre temporali precise.

**Finestra 1 — Inizio task** (prima di iniziare qualsiasi lavoro su un progetto):
1. Esegui `python3 skills/meta/contesto-progetto/match.py [nome-progetto]` e leggi i file suggeriti
2. In un **unico messaggio** segnala (se rilevanti):
   - Pattern applicabili dalla KB (`patterns/`)
   - Decisioni simili prese in passato (`projects/[nome]/decisioni.md`)
   - Problemi tecnici noti correlati (`knowledge/problemi-tecnici/`)
   - La skill più adatta se ne esiste una per il task descritto
3. Non inviare messaggi multipli — tutto in un blocco iniziale

**Finestra 2 — Durante implementazione** (accumulo batch, no interrupt):
1. Accumula osservazioni, dubbi, idee senza interrompere il flusso
2. Quando hai ≥3 elementi accumulati → presentali in un unico batch
3. Formato batch: *"Ho alcune osservazioni: [lista puntata]"*
4. Non interrompere per ogni singola osservazione — aspetta di averne abbastanza

**Finestra 3 — Fine task** (prima di chiudere la sessione):
1. Proponi aggiornamento KB se hai:
   - Risolto un problema che ha richiesto tempo/ricerca
   - Preso una decisione architetturale
   - Trovato un pattern riutilizzabile non ancora documentato
   - Incontrato un comportamento inatteso (bug, quirk, edge case)
2. Chiedi: *"Vuoi che aggiunga questo a patterns/ / knowledge/ / decisioni.md?"*
3. L'utente decide — non creare mai asset KB senza approvazione esplicita

---

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

### Regola 6 — Selezione executor prima dello sviluppo

Prima di ogni task di sviluppo (non solo quelli orchestrati da feature-workflow):

1. Chiedi all'utente: *"Vuoi sviluppare con Claude Code o Windsurf?"*
2. Se **Claude Code**: procedi con lo sviluppo diretto
3. Se **Windsurf**: genera il brief autocontenuto con `feature-develop` modalità Windsurf, salvalo in `projects/[nome]/windsurf-briefs/`
4. Dopo il ritorno da Windsurf: processa il report con `windsurf-feedback`
5. In ogni caso: **test e review restano responsabilità di Claude Code**

**Non è bloccante per task banali**: per fix di una riga o modifiche ovvie, non chiedere.

### Politica di crescita KB

> Claude **propone sempre** quando qualcosa merita di essere aggiunto alla KB.
> L'utente decide. **Non creare mai nuovi asset KB senza approvazione esplicita.**

Principio operativo: inizia semplice, arricchisci gradualmente.
- Ogni problema risolto con tempo/ricerca → proponi `knowledge/problemi-tecnici/`
- Ogni pattern riutilizzabile scoperto → proponi `patterns/`
- Ogni decisione architetturale → proponi `projects/[nome]/decisioni.md`
- Ogni idea di miglioramento al framework → proponi `IDEAS.md`

---

## Trigger proattivi — Pattern → Skill mapping

Claude riconosce questi contesti e **suggerisce la skill pertinente** senza aspettare invocazione esplicita:

| Contesto rilevato | Skill da suggerire |
|---|---|
| L'utente descrive requisiti da meeting notes o documenti cliente | `estrazione-requisiti` |
| L'utente vuole iniziare una nuova feature end-to-end | `feature-workflow` |
| Il task stimato è > 1h o complesso | Chiedere: *"Claude Code o Windsurf?"* (Regola 6) |
| La sessione di sviluppo si sta concludendo | `brainstorming-post-sviluppo` (Regola 5) |
| L'utente ha ricevuto un report da Windsurf | `windsurf-feedback` |
| Si è presa una decisione tecnica non banale | `estrazione-decisioni` |
| Fine sprint o mese | `audit-periodico` |
| L'utente vuole un documento tecnico per il cliente | `genera-allegato-tecnico` |
| Si sta avviando un nuovo progetto cliente | `init-project` |
| Ambiente locale non funziona o primo avvio | `setup-progetto-dev` |
| Problemi AWS (deploy, log, DB, performance) | `aws-triage` → skill specifica |
| Fine fase o sprint, pattern da estrarre | `estrazione-pattern` |
| L'utente vuole creare task Notion per un progetto | `crea-task-notion` |
| L'utente vuole copiare/sincronizzare dati tra database | `db-transfer` |

**Come suggerire**: in modo breve e non invasivo, es.:
*"Noto che stai descrivendo requisiti da note — suggerisco di usare la skill `estrazione-requisiti`. Vuoi procedere così?"*

---

## Come usare le skill

Le skill sono in `skills/`. Ogni skill è una **cartella** con un `SKILL.md` dentro.
Per invocarla: leggi il `SKILL.md` e segui il processo conversazionale.

Per il catalogo completo, i flussi Mermaid, il ciclo di vita e le dipendenze: vedi `docs/skills.md`.
Per i workflow per fase (presales, development, maintenance, meta): vedi `docs/workflow.md`.

**Skill in beta**: all'inizio avvisa che è in beta. Durante l'uso, ad ogni step chiede se il processo ha senso o se va modificato.

## Divisione strumenti

- **Claude Code**: gestione KB, pianificazione feature, generazione brief per Windsurf, review codice, esecuzione test, processamento feedback Windsurf, aggiornamento KB post-sviluppo
- **Windsurf**: scrittura codice, implementazione feature, debug, refactoring, compilazione report feedback. Guidato dalla skill globale `claude-brief` (`~/.codeium/windsurf/skills/claude-brief/SKILL.md`)

Claude Code opera con parsimonia (costi). Windsurf gestisce lo sviluppo intensivo.

### Ciclo Windsurf (quando l'utente sceglie Windsurf come executor)

1. Claude Code pianifica e genera un brief autocontenuto (`windsurf-briefs/`)
2. L'utente passa il brief a Windsurf
3. Windsurf sviluppa e compila il report di feedback (template incluso nel brief)
4. L'utente passa il report a Claude Code
5. Claude Code processa il feedback (`windsurf-feedback`), arricchisce la KB, ed esegue test + review

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
