---
nome: "Verifica Pre-Commit"
descrizione: >
  Skill autonoma di verifica della coerenza della KB prima di ogni commit.
  Esegue 5 check in parallelo (referenze cross-file, changelog, IDEAS, tag, struttura).
  Restituisce PASS o FAIL con issue specifiche da risolvere.
  NON ha loop conversazionale — progettata per girare come sub-agent.
  NON corregge: rileva e riporta. È il parent agent che corregge.
fase: meta
versione: "1.0"
stato: beta
legge:
  - CLAUDE.md
  - System.md
  - CHANGELOG-framework.md
  - CHANGELOG-contenuti.md
  - IDEAS.md
  - docs/struttura.md
  - docs/skills.md
  - docs/workflow.md
  - .tags/index.md
  - skills/ (frontmatter di tutti i SKILL.md)
scrive: []
aggiornato: "2026-03-08"
---

# Skill: Verifica Pre-Commit

## Obiettivo

Verificare in autonomia che la KB sia coerente prima di ogni commit. Nessuna conversazione, nessuna domanda: solo lettura, verifica e report.

## Perimetro

**Fa**: rileva inconsistenze, changelog mancanti, idee non aggiornate, tag assenti, drift struttura.
**NON fa**: correggere i problemi — li riporta al parent agent che li risolve.
**NON fa**: audit dei progetti o dei pattern (per quello: `audit-periodico`).
**NON fa**: sync interattivo della documentazione (per quello: `gestione-kb` modalità 3).

---

## Quando viene invocata

Questa skill viene invocata automaticamente dal parent agent (Claude Code) in questi momenti:

1. **Prima di ogni `git commit`** — BLOCCANTE: il commit non procede se il risultato è FAIL
2. **Al termine di qualsiasi sessione in cui sono stati modificati file della KB**
3. **Su richiesta esplicita dell'utente** per spot-check della coerenza

---

## Input

Il parent agent passa (in formato testo) la lista dei file modificati. Se non disponibile, esegui `git diff --name-only HEAD` per ricavarla.

```
File modificati:
- CLAUDE.md
- docs/skills.md
- skills/meta/verifica-pre-commit/SKILL.md
```

In alternativa, il parent può richiedere **full scan** (nessun file specifico): controlla tutto.

---

## Processo di verifica

Esegui i 5 check **in parallelo** (usa sub-agent separati se i file modificati sono più di 3).

---

### Check 1 — Coerenza referenze cross-file

**Mappa delle dipendenze da verificare:**

| Se è modificato... | Verifica anche... |
|---|---|
| Un file in `skills/[fase]/[nome]/` | `CLAUDE.md` (sezione workflow), `docs/skills.md` (tabella + sezione), `docs/workflow.md` (diagrammi Mermaid) |
| `skills/README.md` | `docs/skills.md` (deve essere allineato) |
| Una cartella aggiunta/rimossa in `skills/` | `CLAUDE.md`, `docs/struttura.md`, `docs/skills.md`, `System.md` |
| Una cartella aggiunta/rimossa in `projects/` o `knowledge/` | `CLAUDE.md`, `docs/struttura.md`, `System.md` |
| `CLAUDE.md` | `System.md` (struttura e skill citate), `docs/workflow.md` (flussi) |
| `docs/struttura.md` | Struttura cartelle reale (confronta albero documentato vs `ls`) |

**Come verificare:**
1. Per ogni file modificato, individua i file dipendenti dalla tabella sopra
2. Leggi i file dipendenti
3. Verifica che i nomi, percorsi e strutture citati siano ancora corretti
4. Segnala ogni discrepanza con: file sorgente → file dipendente → issue specifica

**Output check:**
```
Check 1 — Coerenza referenze: ✓ PASS | ✗ FAIL
  [Se FAIL — una riga per issue:]
  - docs/skills.md:31 → cita "verifica-commit" ma il percorso è "verifica-pre-commit"
```

---

### Check 2 — Changelog aggiornato

**Regola**: ogni commit deve avere almeno un'entry nel changelog appropriato.

**Come verificare:**
1. Leggi `CHANGELOG-framework.md` e `CHANGELOG-contenuti.md`
2. Controlla se esiste una sezione `## [Non rilasciato]` con entry recenti
3. Classifica le modifiche:
   - Modifiche a struttura, skill, template, processi → devono essere in `CHANGELOG-framework.md`
   - Modifiche a contenuti (progetti, pattern, knowledge aziendale) → in `CHANGELOG-contenuti.md`
4. Verifica che le modifiche nella lista di input siano tracciate nel changelog corretto

**Output check:**
```
Check 2 — Changelog: ✓ PASS | ✗ FAIL
  [Se FAIL:]
  - skills/meta/verifica-pre-commit/SKILL.md aggiunta ma non tracciata in CHANGELOG-framework.md
```

---

### Check 3 — IDEAS.md aggiornato

**Regola**: se qualcosa di implementato corrisponde a un'idea in stato `proposta` o `approvata`, quella idea va marcata come `completata`.

**Come verificare:**
1. Leggi `IDEAS.md` — filtra idee con stato `proposta` o `approvata`
2. Per ciascuna, controlla se i file nella lista modificati le implementano (cerca match semantici: nomi file, concetti, percorsi citati nell'idea)
3. Segnala le idee che sembrano completate ma non sono marcate come tali

**Match rapidi da controllare sempre:**
- Nuova skill aggiunta → c'è un'idea per quella skill?
- Nuovo file in `docs/` → c'è un'idea per quella documentazione?
- Nuovo processo automatico → c'è un'idea per quell'automazione?

**Output check:**
```
Check 3 — IDEAS.md: ✓ PASS | ✗ FAIL
  [Se FAIL:]
  - IDEA-001 menziona "scheduled task pre-commit" — il nuovo skill verifica-pre-commit implementa parte di questo?
    → Valuta se aggiornare stato o aggiungere nota
```

---

### Check 4 — Tag frontmatter

**Regola**: ogni file .md nuovo o modificato che non è un file di sistema (CLAUDE.md, System.md, CHANGELOG*.md, IDEAS.md, README.md) deve avere tag nel frontmatter.

**Come verificare:**
1. Per ogni file .md nella lista modificati (esclusi file di sistema), leggi il frontmatter
2. Verifica presenza di almeno un tag riconosciuto (vedi tabella tag in CLAUDE.md)
3. Verifica che i tag usati siano registrati in `.tags/index.md`

**Output check:**
```
Check 4 — Tag: ✓ PASS | ✗ FAIL
  [Se FAIL:]
  - skills/meta/verifica-pre-commit/SKILL.md: tag mancanti nel frontmatter
  - knowledge/azienda/nuovo-file.md: tag #stack:laravel non in .tags/index.md
```

---

### Check 5 — Struttura vs documentazione

**Regola**: `docs/struttura.md` deve riflettere l'albero reale delle cartelle principali.

**Come verificare:**
1. Lista le cartelle di primo e secondo livello effettivamente esistenti:
   - `ls skills/` → confronta con skills documentate
   - `ls projects/` → confronta
   - `ls knowledge/` → confronta
   - `ls core/` → confronta
2. Leggi `docs/struttura.md` e confronta
3. Segnala: cartelle esistenti ma non documentate, cartelle documentate ma inesistenti

**Output check:**
```
Check 5 — Struttura: ✓ PASS | ✗ FAIL
  [Se FAIL:]
  - skills/meta/verifica-pre-commit/ esiste ma non è in docs/struttura.md
```

---

## Output finale (obbligatorio)

```
═══════════════════════════════════════
VERIFICA PRE-COMMIT — [PASS | FAIL]
File verificati: [N] | Issue trovate: [N]
═══════════════════════════════════════

Check 1 — Coerenza referenze:   [✓ PASS | ✗ FAIL (N issue)]
Check 2 — Changelog:            [✓ PASS | ✗ FAIL (N issue)]
Check 3 — IDEAS.md:             [✓ PASS | ✗ FAIL (N issue)]
Check 4 — Tag frontmatter:      [✓ PASS | ✗ FAIL (N issue)]
Check 5 — Struttura vs docs:    [✓ PASS | ✗ FAIL (N issue)]

[Se FAIL:]
────────────────────────────────────────
ACTION REQUIRED — risolvi prima del commit:

1. [Issue specifica con file:riga e descrizione]
2. [Issue specifica con file:riga e descrizione]
...

[Se PASS:]
────────────────────────────────────────
KB coerente — commit autorizzato.
```

---

## Comportamento del parent agent

Quando questo sub-agent restituisce **FAIL**:
1. Il parent agent **NON procede con il commit**
2. Il parent agent risolve **tutte** le issue in modo autonomo (senza chiedere all'utente, salvo ambiguità reali)
3. Il parent agent riesegue `verifica-pre-commit` finché non restituisce PASS
4. Solo a quel punto: esegue il commit

---

## Checklist qualità

- [ ] Tutti e 5 i check sono stati eseguiti (nessuno saltato)
- [ ] Ogni FAIL ha un'issue specifica con file e descrizione (non messaggi generici)
- [ ] Il risultato finale è PASS solo quando tutti e 5 i check sono PASS
- [ ] I sub-agent paralleli (se usati) hanno tutti completato prima del report finale

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
