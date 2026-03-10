---
nome: "Windsurf Feedback"
descrizione: >
  Processa il report di feedback da Windsurf dopo lo sviluppo di una feature.
  Estrae difficolta, pattern, decisioni e arricchisce la KB.
  NON sviluppa e NON testa — solo processa feedback.
  Per lo sviluppo → feature-develop. Per i test → feature-test.
fase: development
versione: "1.0"
stato: beta
depends-on:
  - feature-develop (modalita Windsurf)
enables:
  - feature-test
  - feature-review
  - estrazione-pattern
  - estrazione-decisioni
legge:
  - projects/[nome]/windsurf-briefs/[RF-XX]-report.md (o input in chat)
  - projects/[nome]/.feature-state.md
  - patterns/README.md (per evitare duplicati)
  - knowledge/problemi-tecnici/ (per evitare duplicati)
scrive:
  - projects/[nome]/.feature-state.md (sezione Sviluppo)
  - projects/[nome]/decisioni.md (se decisioni rilevanti)
  - patterns/[nuovo].md (se pattern candidati approvati)
  - knowledge/problemi-tecnici/[nuovo].md (se problemi ricorrenti approvati)
aggiornato: "2026-03-10"
tags:
  - "#fase:development"
  - "#skill:windsurf-feedback"
---

# Skill: Windsurf Feedback

## Obiettivo

Processa il report strutturato che Windsurf produce dopo aver implementato una feature. Estrae le informazioni rilevanti e le smista nelle aree appropriate della KB.

---

## Perimetro

**Fa**: leggere il report Windsurf, estrarre difficolta/pattern/decisioni, proporre arricchimento KB, aggiornare `.feature-state.md`.

**NON fa**: sviluppo (→ `feature-develop`), test (→ `feature-test`), review (→ `feature-review`), pianificazione (→ `feature-plan`).

**Puo essere invocata**: da `feature-workflow` (dopo la fase Develop con executor=Windsurf) o standalone.

---

## Quando usarla

- Dopo che Windsurf ha completato lo sviluppo e l'utente fornisce il report
- Quando si vuole processare feedback da Windsurf fuori dal workflow orchestrato
- Quando si vuole arricchire la KB con le scoperte fatte durante lo sviluppo Windsurf

---

## Prerequisiti

- [ ] Report Windsurf disponibile (file o incollato in chat)
- [ ] Progetto inizializzato in `projects/[nome]/`

---

## Loop conversazionale

Fai le domande in questo ordine, **una alla volta**:

1. **Quale progetto?** (nome cartella in `projects/` — salta se gia noto dal contesto)
2. **Dove trovo il report?** (path al file, oppure "in chat" se incollato direttamente)

---

## Processo di produzione

### Step 1: Parse del report

Leggi il report e identifica le sezioni compilate. Se il report e incompleto o mal formattato, estrai comunque le informazioni disponibili e segnala le sezioni mancanti.

### Step 2: Riepilogo task

Mostra all'utente un riepilogo:

```
Report Windsurf — [RF-XX]
Task completati: [N/N]
Difficolta segnalate: [N]
Decisioni prese: [N]
Pattern individuati: [N]
Domande aperte: [N]
```

Chiedi: "Confermo il processamento del report?"

### Step 3: Aggiorna `.feature-state.md`

Aggiorna la sezione `## Sviluppo` con:
- File creati (dalla sezione 6 del report)
- File modificati (dalla sezione 6 del report)
- Scelte implementative (dalla sezione 3 del report)
- Deviazioni dal piano (dalla sezione 5 del report)
- Executor: Windsurf

### Step 4: Processa difficolta (sezione 2 del report)

Per ogni difficolta marcata come **ricorrente**:
1. Verifica che non esista gia in `knowledge/problemi-tecnici/`
2. Proponi all'utente: "Windsurf ha trovato questa difficolta ricorrente: [titolo]. Vuoi salvarla come problema tecnico nella KB?"
3. Se approvato: crea file in `knowledge/problemi-tecnici/` usando il template standard
4. Se non approvato: registra solo in `.feature-state.md`

### Step 5: Processa decisioni (sezione 3 del report)

Per ogni decisione non banale:
1. Proponi all'utente: "Windsurf ha preso questa decisione: [titolo]. Vuoi documentarla come ADR?"
2. Se approvato: aggiungi ADR in `projects/[nome]/decisioni.md` con il formato standard
3. Se non approvato: registra solo in `.feature-state.md`

### Step 6: Processa pattern (sezione 4 del report)

Per ogni pattern marcato come **riutilizzabile**:
1. Verifica che non esista gia in `patterns/` (leggi `patterns/README.md`)
2. Se esiste: proponi di aggiungere il progetto alla tabella "Esempi reali" del pattern esistente
3. Se non esiste: proponi all'utente: "Windsurf ha individuato questo pattern: [nome]. Vuoi estrarlo in patterns/?"
4. Se approvato: crea file in `patterns/` usando `patterns/_template.md`
5. Aggiorna `patterns/README.md` e `.tags/index.md`

### Step 7: Gestisci domande aperte (sezione 7 del report)

Se presenti:
1. Mostra le domande all'utente
2. Per ogni domanda: chiedi come risolverla
3. Le risposte possono influenzare la fase Test/Review successiva
4. Se una domanda richiede modifiche al codice: segnala che servira un fix brief

### Step 8: Registra suggerimenti (sezione 8 del report)

Se presenti suggerimenti interessanti:
1. Proponi all'utente: "Windsurf suggerisce: [suggerimento]. Lo registro in IDEAS.md?"
2. Se approvato: registra in `IDEAS.md` via `skills/meta/gestione-kb/` modalita 2

### Step 9: Tracking

```bash
echo "$(date +%Y-%m-%d\ %H:%M) | windsurf-feedback | [progetto] | completata" >> .claude/skill-usage.log
```

---

## Output in chat (obbligatorio al termine)

```
COMPLETATO — Windsurf Feedback

Feature: [RF-XX — titolo]
Report processato: [path o "in chat"]

KB arricchita:
  Problemi tecnici salvati: [N]
  ADR documentate: [N]
  Pattern estratti: [N]
  Suggerimenti in IDEAS.md: [N]
  Domande aperte risolte: [N/N]

Documenti aggiornati:
  projects/[nome]/.feature-state.md (sezione Sviluppo)
  [projects/[nome]/decisioni.md         ← solo se ADR creati]
  [patterns/[nome].md                   ← solo se pattern estratti]
  [knowledge/problemi-tecnici/[nome].md ← solo se problemi salvati]

Prossimi passi:
  → Conferma che lo sviluppo e completo (GATE 2)
  → Poi: skills/development/feature-test/ + feature-review/
```

---

## Checklist qualita

- [ ] Tutte le sezioni del report sono state processate
- [ ] Nessun duplicato creato in patterns/ o knowledge/
- [ ] `.feature-state.md` sezione Sviluppo e aggiornata
- [ ] Tag aggiunti per ogni nuovo file creato (`.tags/index.md`)
- [ ] Domande aperte gestite (risolte o segnalate)

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
