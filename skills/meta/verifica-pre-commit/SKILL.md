---
nome: "Verifica Pre-Commit"
descrizione: >
  Verifica ibrida della coerenza della KB: script Python per i check
  meccanici + check semantici eseguiti dal parent agent.
  FONDAMENTALE: il commit non può procedere senza PASS completo.
fase: meta
versione: "3.0"
stato: stable
legge:
  - CHANGELOG.md
  - IDEAS.md
  - docs/struttura.md
  - .tags/index.md
  - skills/README.md
  - frontmatter dei file modificati
scrive: []
aggiornato: "2026-03-09"
---

# Skill: Verifica Pre-Commit

## Obiettivo

Verificare in modo completo che la KB sia coerente prima di un commit.
La verifica è **ibrida**: check meccanici automatizzati (script Python) + check semantici (parent agent).
Il commit è bloccato finché tutti i check — sia script che semantici — non passano.

## Perimetro

**Fa**: rileva inconsistenze di ogni tipo — referenze rotte, changelog incompleti, tag mancanti o inconsistenti, struttura disallineata, idee non aggiornate, skills/README.md fuori sync.
**NON fa**: correggere i problemi — li riporta al parent agent che li risolve.
**NON fa**: audit completo dei progetti (per quello: `audit-periodico`).

---

## Esecuzione

### Fase 1 — Script automatici

```bash
python3 skills/meta/verifica-pre-commit/run_all.py
```

Esegue 4 check meccanici. Se non si passano file, li ricava da `git diff`.

### Fase 2 — Check semantici (obbligatori)

Il parent agent esegue i check semantici **dopo** gli script. Sono elencati sotto in ogni sezione di check.

### Risultato finale

**PASS** solo quando: tutti gli script passano **E** tutti i check semantici passano.

---

## I 5 check — dettaglio completo

---

### Check 1 — Referenze cross-file

**Script**: `check_refs.py file1.md [file2.md ...]`
Estrae i link markdown `[testo](target)`, risolve i percorsi relativi, verifica che il target esista. Ignora URL esterni, ancore, blocchi di codice e inline code.

**Check semantico 1a — Referenze non-link**:
Percorsi citati come testo libero (es. `vedi projects/jubatus/requisiti.md` senza sintassi `[]()`) non sono catturati dallo script. Il parent agent deve:
1. Scorrere i file modificati cercando percorsi interni citati fuori da link markdown
2. Verificare che esistano

**Check semantico 1b — Coerenza skills/README.md**:
Se sono state modificate skill (aggiunte, rimosse, rinominate):
1. Leggere `skills/README.md`
2. Verificare che la tabella riepilogo sia allineata con le skill reali (nomi, fase, stato, legge/scrive)

---

### Check 2 — Changelog aggiornato

**Script**: `check_changelog.py file1 [file2 ...]`
Classifica i file in "framework" o "contenuti" e verifica che la sezione `[Non rilasciato]` del changelog corrispondente non sia vuota.

**Check semantico 2a — Contenuto del changelog**:
Lo script verifica solo che il changelog non sia vuoto. Il parent agent deve:
1. Leggere la sezione `[Non rilasciato]` del changelog appropriato
2. Verificare che le entry descrivano effettivamente le modifiche fatte
3. Verificare che non manchino modifiche significative
4. Verificare che le entry siano nel changelog giusto (framework vs contenuti)

---

### Check 3 — IDEAS.md

**Nessuno script** — check interamente semantico.

**Check semantico 3a — Idee completate**:
1. Leggere `IDEAS.md`, filtrare idee con stato `proposta` o `approvata`
2. Confrontare con i file modificati (match per keyword, concetti, percorsi)
3. Segnalare idee che sembrano completate ma non sono marcate come tali

**Check semantico 3b — Nuove idee emerse**:
1. Se durante la sessione sono emerse idee o proposte non ancora registrate
2. Verificare che siano state registrate in IDEAS.md o esplicitamente rifiutate dall'utente

---

### Check 4 — Tag frontmatter

**Script**: `check_tags.py file1.md [file2.md ...]`
Per ogni file .md (esclusi file di sistema e directory `docs/`, `.tags/`, `core/`):
- Verifica frontmatter presente
- Verifica almeno un tag `#categoria:valore`
- Verifica tag registrati in `.tags/index.md`
- **Verifica consistenza progetto**: tutti i file di un progetto devono usare gli stessi `#progetto:` e `#industria:`

Nessun check semantico aggiuntivo — lo script copre tutti i casi.

---

### Check 5 — Struttura vs documentazione

**Script**: `check_struttura.py` (nessun input)
Check **bidirezionale**:
- **Diretto**: directory reali (skills, projects, knowledge, core) devono essere in `docs/struttura.md` e `projects/INDEX.md`
- **Inverso**: directory documentate in `docs/struttura.md` devono esistere su disco

Nessun check semantico aggiuntivo — lo script copre tutti i casi.

---

## Script disponibili

| Script | Check | Input | Cosa fa |
|--------|-------|-------|---------|
| `run_all.py` | tutti | file (o auto da git) | Runner: esegue check 1,2,4,5 |
| `check_refs.py` | 1 | file .md | Link markdown → file esistenti |
| `check_changelog.py` | 2 | file | Changelog non vuoto per tipo modifica |
| `check_tags.py` | 4 | file .md | Tag presenti, registrati e consistenti per progetto |
| `check_struttura.py` | 5 | nessuno | Struttura reale ↔ documentazione (bidirezionale) |

Tutti: exit 0 = PASS, exit 1 = FAIL con dettaglio issue su stdout.

---

## Checklist semantica per il parent agent

Dopo aver eseguito `run_all.py`, verifica:

- [ ] **1a**: Percorsi interni citati come testo libero (non link) puntano a file esistenti?
- [ ] **1b**: Se skill modificate → `skills/README.md` è allineato?
- [ ] **2a**: Le entry nel changelog descrivono accuratamente le modifiche fatte?
- [ ] **3a**: Idee in IDEAS.md con stato `proposta`/`approvata` sono state implementate dai file modificati?
- [ ] **3b**: Nuove idee emerse in sessione sono state registrate o rifiutate?

---

## Comportamento del parent agent

- **FAIL** → risolvi le issue autonomamente, riesegui, ripeti finché PASS
- **PASS completo** (script + checklist semantica) → commit autorizzato
- **Tracking**: `echo "$(date +%Y-%m-%d\ %H:%M) | verifica-pre-commit | [progetto] | [PASS/FAIL]" >> .claude/skill-usage.log`

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
