---
nome: "Feature Develop"
descrizione: >
  Implementa una feature seguendo il piano prodotto da feature-plan.
  Puo sviluppare direttamente (Claude Code) o produrre un brief dettagliato per Windsurf.
  NON testa e NON revisiona — si limita a implementare. Per test → feature-test. Per review → feature-review.
fase: development
versione: "1.1"
stato: beta
legge:
  - projects/[nome]/.feature-state.md (sezione Piano)
  - knowledge/azienda/processi.md
  - knowledge/azienda/stack.md
  - patterns/README.md (per brief Windsurf)
  - Codebase del progetto (repo Git)
scrive:
  - Codebase del progetto (codice)
  - projects/[nome]/.feature-state.md (sezione Sviluppo)
  - projects/[nome]/windsurf-briefs/[RF-XX]-[nome].md (modalita Windsurf)
aggiornato: "2026-03-10"
---

# Skill: Feature Develop

## Obiettivo

Implementa una feature seguendo il piano tecnico approvato. Opera in due modalita: sviluppo diretto (Claude Code) o produzione di un brief autocontenuto per Windsurf.

---

## Perimetro

**Fa**: implementazione codice, creazione file, seguire convenzioni LAIF, aggiornare lo stato di avanzamento, generare brief strutturati per Windsurf.

**NON fa**: test (→ `feature-test`), review codice (→ `feature-review`), pianificazione (→ `feature-plan`), processamento feedback Windsurf (→ `windsurf-feedback`).

**Puo essere invocata**: standalone (con piano gia scritto) o come parte di `feature-workflow`.

---

## Quando usarla

- Dopo che il piano e stato approvato (GATE 1 passato)
- Quando `.feature-state.md` contiene una sezione Piano completa
- Quando si deve implementare una feature gia pianificata

---

## Prerequisiti

- [ ] Piano approvato in `.feature-state.md` (sezione Piano)
- [ ] Accesso alla codebase del progetto (repo Git clonata)
- [ ] Convenzioni LAIF note (processi.md)

---

## Loop conversazionale

Fai le domande in questo ordine, **una alla volta**:

1. **(Solo se standalone, non invocata da feature-workflow)** Sviluppo diretto (Claude Code) o brief per Windsurf?
2. **(Solo se Windsurf)** Path della repo di destinazione?

Se invocata da `feature-workflow`, l'executor e gia definito nel campo `executor` di `.feature-state.md`.

---

## Processo di produzione — Modalita Claude Code

1. Leggi il piano dalla sezione `## Piano` di `.feature-state.md`
2. **Consulta `patterns/README.md`** e leggi i pattern referenziati nel piano. Applica le soluzioni e le checklist errori comuni di ogni pattern durante l'implementazione.
3. Implementa task per task seguendo l'ordine delle dipendenze definito nel piano
4. Per ogni task:
   - Implementa il codice seguendo le convenzioni LAIF (`processi.md`)
   - Verifica che compili / non ci siano errori sintattici
   - Passa al task successivo
5. Convenzioni da seguire:
   - **Backend**: RouterBuilder per endpoint, CRUDService per logica, modelli in `models.py`
   - **Frontend**: @laif/ds per componenti, soft-onion per architettura, no prop drilling
   - **Naming**: PascalCase componenti, camelCase hooks (.hook.ts), kebab-case cartelle
6. Aggiorna `.feature-state.md` sezione `## Sviluppo` con:
   - File creati (lista con path)
   - File modificati (lista con path e descrizione modifica)
   - Scelte implementative non ovvie (decisioni prese durante lo sviluppo)
7. **Tracking**: `echo "$(date +%Y-%m-%d\ %H:%M) | feature-develop | [progetto] | completata-cc" >> .claude/skill-usage.log`

## Processo di produzione — Modalita Windsurf Brief

1. Leggi il piano dalla sezione `## Piano` di `.feature-state.md`
2. Crea la directory `projects/[nome]/windsurf-briefs/` se non esiste
3. Produci un brief **autocontenuto** usando la struttura seguente e salvalo in `projects/[nome]/windsurf-briefs/[RF-XX]-[nome-feature].md`:

### Struttura del brief

```markdown
# Windsurf Development Brief

> Windsurf: questo file e il brief completo per lo sviluppo. Contiene tutto
> il contesto necessario. NON serve accesso ad altri file di documentazione.
> Alla fine trovi un template di report da compilare quando hai finito.

---

## Metadata

| Campo | Valore |
|-------|--------|
| Progetto | [nome-progetto] |
| Requisito | [RF-XX — titolo] |
| Data brief | [YYYY-MM-DD] |
| Repository | [path assoluto della repo] |
| Stack | [backend: FastAPI/Python, frontend: Next.js/TypeScript, DB: PostgreSQL] |

---

## 1. Obiettivo feature

[Descrizione chiara della feature in 2-3 frasi. Cosa deve fare, per chi, perche.]

---

## 2. Contesto tecnico

### Architettura attuale
[Descrizione dei componenti coinvolti, schema se utile]

### Codice esistente rilevante
[Snippet di codice dalla codebase attuale che Windsurf deve conoscere.
Includere path dei file con snippet rappresentativi.]

---

## 3. Task list

Implementa in questo ordine (le dipendenze sono esplicite):

| # | Task | Dipende da | File coinvolti | Tipo |
|---|------|------------|----------------|------|
| 1 | [descrizione task] | - | [path/file] | nuovo / modifica |
| 2 | [descrizione task] | #1 | [path/file] | nuovo / modifica |

---

## 4. Convenzioni LAIF (obbligatorie)

[Copiare integralmente le convenzioni da knowledge/azienda/processi.md.
NON referenziare — copiare il testo completo delle sezioni backend e frontend.]

---

## 5. Pattern da applicare

[Per ogni pattern rilevante da patterns/, copiare:
- Nome e descrizione del problema
- Soluzione
- Checklist errori comuni
NON referenziare il file nella KB — copiare il contenuto.]

---

## 6. Criteri di accettazione

- [ ] [criterio 1 — misurabile]
- [ ] [criterio 2 — misurabile]

---

## 7. Rischi e note

- [rischio o nota utile per l'implementazione]

---

## 8. File da creare / modificare (riepilogo)

### Nuovi file
- `path/nuovo/file.ext` — [scopo]

### File da modificare
- `path/esistente/file.ext` — [cosa cambiare]

---

## 9. Template Report Feedback

> Quando hai finito, compila questo template e passalo a Claude Code.
> Puoi salvarlo come `[RF-XX]-report.md` nella stessa cartella del brief
> oppure copiarlo direttamente in chat a Claude Code.

### Windsurf Report — [RF-XX — titolo feature]

#### Metadata

| Campo | Valore |
|-------|--------|
| Data completamento | [YYYY-MM-DD] |
| Tempo stimato | [ore] |
| Completamento task | [N/N completati] |

#### 1. Task completati

| # | Task | Stato | Note |
|---|------|-------|------|
| 1 | [dal brief] | completato / parziale / saltato | [note] |

#### 2. Difficolta incontrate

Per ogni difficolta significativa:

**Difficolta: [titolo]**
- **Problema**: [cosa non funzionava]
- **Causa**: [perche]
- **Soluzione adottata**: [come hai risolto]
- **Tempo perso**: [stima]
- **Ricorrente?**: [si/no — potrebbe ripresentarsi in altri progetti?]

#### 3. Decisioni prese

Per ogni decisione tecnica non prevista dal piano:

**Decisione: [titolo]**
- **Contesto**: [perche serviva decidere]
- **Alternativa scelta**: [cosa hai scelto]
- **Alternative scartate**: [cosa hai considerato]
- **Motivazione**: [perche questa scelta]

#### 4. Pattern individuati

Per ogni soluzione che potrebbe essere riutilizzabile:

**Pattern: [nome suggerito]**
- **Problema che risolve**: [descrizione]
- **Soluzione**: [come funziona]
- **Riutilizzabile?**: [si — in quali contesti]

#### 5. Deviazioni dal piano

- [file/componente]: [cosa e cambiato rispetto al piano e perche]

#### 6. File creati e modificati

**Nuovi file:**
- `path/file.ext` — [scopo]

**File modificati:**
- `path/file.ext` — [cosa e cambiato]

#### 7. Domande aperte

- [ ] [domanda irrisolta che richiede una decisione]

#### 8. Suggerimenti

- [suggerimento per migliorare codice, processo o architettura]
```

4. Mostra all'utente il path del brief salvato
5. Aggiorna `.feature-state.md` sezione `## Sviluppo` con:
   ```
   Brief Windsurf generato: projects/[nome]/windsurf-briefs/[RF-XX]-[nome-feature].md
   Report atteso: projects/[nome]/windsurf-briefs/[RF-XX]-report.md
   ```
6. **Tracking**: `echo "$(date +%Y-%m-%d\ %H:%M) | feature-develop | [progetto] | completata-ws" >> .claude/skill-usage.log`

---

## Output in chat (obbligatorio al termine)

### Modalita Claude Code:
```
COMPLETATO — Feature Develop (Claude Code)

Feature implementata: [RF-XX — titolo]
File creati: [N]
File modificati: [N]
Task completati: [N/N]

Documenti aggiornati:
  projects/[nome]/.feature-state.md (sezione Sviluppo)

Prossimi passi:
  → Conferma che lo sviluppo e completo (GATE 2)
  → Poi: skills/development/feature-test/ + feature-review/
```

### Modalita Windsurf:
```
COMPLETATO — Feature Develop (Brief Windsurf)

Brief salvato: projects/[nome]/windsurf-briefs/[RF-XX]-[nome-feature].md
Task nel brief: [N]

Prossimi passi:
  → Passa il brief a Windsurf per l'implementazione
  → Windsurf compila il report (sezione 9 del brief)
  → Torna con il report per processarlo con windsurf-feedback
```

---

## Checklist qualita

- [ ] Tutti i task del piano sono stati implementati (o inclusi nel brief)
- [ ] Le convenzioni LAIF sono state seguite (RouterBuilder, CRUDService, @laif/ds, naming)
- [ ] Il codice compila senza errori (modalita Claude Code)
- [ ] Nessun file del piano e stato saltato
- [ ] La sezione Sviluppo di `.feature-state.md` e aggiornata
- [ ] (Windsurf) Il brief e autocontenuto — nessun riferimento a file KB
- [ ] (Windsurf) Il template report feedback e incluso nel brief (sezione 9)
- [ ] (Windsurf) Il brief e salvato come file in `windsurf-briefs/`

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
