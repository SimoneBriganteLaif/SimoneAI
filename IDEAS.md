# Backlog Idee e Miglioramenti

Raccolta strutturata di idee per evolvere il sistema. Le idee vengono valutate periodicamente tramite la skill `gestione-kb` (modalità 4 — review idee).

---

## Idee attive

| ID | Idea | Categoria | Effort | Priorità | Stato | Data | Note |
|----|------|-----------|--------|----------|-------|------|------|
| IDEA-001 | Scheduled task giornaliera: git diff → auto-changelog → commit/tag se modifiche + sync repo core (IDEA-008) | automazione | M | alta | proposta | 2026-03-08 | Usare scheduled tasks di Claude Code. "Staccare una versione" giornaliera solo se ci sono diff. Includere anche pull repo core + aggiornamento knowledge se cambiate |
| IDEA-002 | Definire skill operative per Windsurf (istruzioni per sviluppo codice) | skill | M | alta | proposta | 2026-03-08 | Complementare alle skill Claude Code — guida come Windsurf deve operare sui repo |
| IDEA-003 | Guida setup ambiente: installazione, configurazione, primo utilizzo | processo | S | media | completata | 2026-03-08 | Completata: vedi `docs/setup.md` |
| IDEA-004 | Valutare estensione multi-utente del sistema | processo | L | bassa | proposta | 2026-03-08 | Per ora uso personale. Valutare permessi, conflitti, workflow collaborativo |
| IDEA-005 | Sezione "Persone" per gestione team: one-to-one, obiettivi, crescita | struttura | M | bassa | proposta | 2026-03-08 | Tracciare esiti 1:1, obiettivi individuali, percorsi di crescita dei membri del team. Da valutare quando il sistema sarà più maturo |
| IDEA-006 | Sezione personale: task, organizzazione vita, obiettivi personali | struttura | L | bassa | proposta | 2026-03-08 | Integrare sfera personale nel sistema. Probabile refactor necessario per separare lavoro/vita. Visione: un unico sistema per gestire tutto |
| IDEA-007 | Migrazione knowledge su database (SQLite → eventuale web app) | integrazione | L | bassa | proposta | 2026-03-08 | File .md poco efficienti per ricerca e consumo token. SQLite locale come primo step, poi valutare web app. Obiettivo: accesso efficiente senza scansionare tutta la KB |
| IDEA-008 | Sync giornaliero repo core: pull laif-template e DS, diff, aggiorna knowledge | automazione | M | alta | proposta | 2026-03-08 | Da integrare nella scheduled task (IDEA-001). Le repo core vengono aggiornate spesso — la KB deve restare allineata. Pull → diff → aggiorna knowledge/azienda/ se necessario |
| IDEA-009 | Migliorare processo upstream laif-template → ridurre conflitti merge | processo | L | media | proposta | 2026-03-08 | Pain point riconosciuto: propagare aggiornamenti del template ai progetti forkati genera conflitti frequenti. Valutare strategie alternative (subtree, package, monorepo) |
| IDEA-010 | Definire processo di branching e Git flow per il team | processo | M | alta | proposta | 2026-03-08 | Attualmente non c'è un processo organizzato. Definire convenzioni branch, review, merge. Può diventare un pattern in knowledge/ |
| IDEA-011 | Gestire iniziative interne come progetti nella KB | struttura | S | media | proposta | 2026-03-08 | Iniziative tipo "ristrutturazione infra" o "processo Git" trattate come progetti in projects/ con tag #tipo:interno. Stesso template, diverso contesto |
| IDEA-012 | Modularizzare email reader come libreria interna riutilizzabile | integrazione | L | alta | proposta | 2026-03-09 | Il modulo lettura email (OAuth Gmail/Microsoft, sync, parsing) e presente in Jubatus e servira ad altri progetti. Obiettivo: estrarlo come pacchetto standalone. Per ora sviluppare in Jubatus con architettura incapsulata e interfacce pulite, pronto per estrazione futura. Valutare se collocarlo in laif-template o come pacchetto separato (npm/pypi interno) |
| IDEA-013 | Skill integrazione-email: guida setup OAuth per nuovi clienti | skill | M | media | proposta | 2026-03-09 | Il setup OAuth Gmail/Outlook + test connessione si ripete per ogni cliente. Creare una skill che guida nel setup Google Cloud Console / Azure AD, prepara .env, testa connessione con script standalone. Da creare quando IDEA-012 sara implementata |
| IDEA-014 | Brainstorming post-sviluppo come comportamento autonomo | processo | S | alta | completata | 2026-03-09 | Alla fine di ogni sessione, analizzare il lavoro svolto per estrarre pattern, skill, idee. Creata skill `brainstorming-post-sviluppo`. Valutare se aggiungere come Regola 5 in CLAUDE.md per esecuzione automatica |

---

## Categorie

| Categoria | Descrizione |
|-----------|-------------|
| `struttura` | Modifiche alla struttura cartelle, template, convenzioni |
| `skill` | Nuove skill o miglioramenti a skill esistenti |
| `processo` | Cambiamenti ai flussi di lavoro |
| `integrazione` | Integrazioni con strumenti esterni (Notion, GitHub, ecc.) |
| `automazione` | Automazioni, scheduled task, processi autonomi |

## Effort

| Valore | Significato |
|--------|-------------|
| `S` | Poche ore, modifiche localizzate |
| `M` | 1-2 sessioni di lavoro, più file coinvolti |
| `L` | Richiede progettazione, più sessioni, possibili dipendenze |

## Stati

| Stato | Significato |
|-------|-------------|
| `proposta` | Idea registrata, non ancora valutata |
| `approvata` | Valutata e approvata per implementazione |
| `in-corso` | Implementazione iniziata |
| `completata` | Implementata e verificata |
| `scartata` | Valutata e scartata (spostata nella sezione sotto) |

---

## Idee scartate

| ID | Idea | Motivo scarto | Data scarto |
|----|------|---------------|-------------|
| | _Nessuna idea scartata finora_ | | |
