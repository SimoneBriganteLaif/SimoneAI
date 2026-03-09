---
nome: "Feature Review"
descrizione: >
  Revisiona il codice di una feature per qualità, aderenza ai pattern LAIF,
  duplicazioni e code smell. Confronta con patterns/ nella KB e suggerisce
  nuovi pattern estraibili. NON modifica il codice — produce solo il report.
  Per fix → feature-develop. Per estrarre pattern → estrazione-pattern.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/.feature-state.md (Piano + Sviluppo)
  - knowledge/azienda/processi.md
  - knowledge/azienda/stack.md
  - patterns/
  - patterns/_template.md
  - Codebase del progetto (codice modificato)
scrive:
  - projects/[nome]/.feature-state.md (sezione Review)
aggiornato: "2026-03-09"
---

# Skill: Feature Review

## Obiettivo

Revisiona il codice prodotto per una feature, verificando aderenza ai pattern LAIF, assenza di duplicazioni, qualità del codice e opportunità di arricchire la KB con nuovi pattern.

---

## Perimetro

**Fa**: review codice, check convenzioni LAIF, check duplicazioni, check qualità e sicurezza, confronto con patterns/ nella KB, identificazione pattern estraibili.

**NON fa**: modifica codice (→ `feature-develop`), test (→ `feature-test`), estrazione pattern (→ `estrazione-pattern`).

**Può essere invocata**: standalone o come parte di `feature-workflow` (in parallelo con `feature-test`).

---

## Quando usarla

- Dopo che lo sviluppo è completato (GATE 2 passato)
- Quando si vuole verificare la qualità del codice di una feature
- Quando `.feature-state.md` contiene le sezioni Piano e Sviluppo

---

## Prerequisiti

- [ ] Feature implementata (codice presente nella codebase)
- [ ] `.feature-state.md` con sezione Piano e Sviluppo (lista file modificati)
- [ ] Accesso alla codebase del progetto (repo Git)

---

## Loop conversazionale

**Nessuno** — questa skill opera autonomamente sulla base del piano e del codice. Non richiede input aggiuntivo dall'utente.

---

## Processo di produzione

1. Leggi la lista dei file creati/modificati dalla sezione `## Sviluppo` di `.feature-state.md`
2. Per ogni file, esegui i seguenti check:

### Check 1: Aderenza pattern LAIF

Verifica rispetto a `knowledge/azienda/processi.md`:

**Backend**:
- Usa `RouterBuilder` per gli endpoint? (non route manuali)
- Usa `CRUDService` per la logica? (non `RoleBasedCRUDService` che è deprecato)
- Modelli aggiunti in `backend/src/template/models.py`?
- Naming colonne DB rispetta le convenzioni?
- Migrazione creata dopo schema change?

**Frontend**:
- Usa componenti `@laif/ds`? (non shadcn/ui raw o componenti custom quando esiste l'equivalente in DS)
- Segue architettura soft-onion? (`features/[nome]/` con types, services, components, store)
- No prop drilling? (usa Redux o Context dove necessario)
- Design responsive?
- Tailwind usa solo token DS? (non classi vanilla)

**Naming**:
- Componenti: `PascalCase` (es. `UserCard.tsx`)
- Hook: `camelCase.hook.ts` (es. `useGetOrders.hook.ts`)
- Servizi: `camelCase.service.ts`
- Cartelle: `kebab-case`

### Check 2: Duplicazioni

- Codice duplicato tra file della stessa feature
- Codice duplicato con componenti/funzioni esistenti nel progetto
- Logica che potrebbe essere estratta in utility o hook condiviso
- Componenti UI che replicano componenti già presenti in @laif/ds

### Check 3: Qualità codice

- Code smell: funzioni > 50 righe, nesting > 3 livelli, parametri > 4
- Gestione errori: presente dove necessaria (boundary di sistema, API call, input utente)
- Sicurezza: no SQL injection, no XSS, input validation ai boundary
- Performance: no N+1 query, no rendering inutili, no import pesanti non necessari

### Check 4: Confronto con KB

- Cerca in `patterns/` pattern che la feature avrebbe dovuto applicare e non ha applicato
- Identifica soluzioni nella feature che potrebbero diventare **nuovi pattern riutilizzabili**
- Per ogni pattern candidato: segnala con descrizione e riferimento al template `patterns/_template.md`

### Classificazione issue

| Livello | Criteri | Effetto |
|---------|---------|---------|
| **Critica** | Viola convenzioni LAIF, introduce bug, duplicazione significativa, problema sicurezza | Blocca GATE 3 |
| **Minore** | Naming non ottimale, codice migliorabile, suggerimenti stilistici | Non blocca GATE 3 |

3. **Tracking**: `echo "$(date +%Y-%m-%d\ %H:%M) | feature-review | [progetto] | [PASS/FAIL]" >> .tags/skill-usage.log`

### Formato report review

```markdown
## Review

### Issue critiche (bloccanti)
- [C1] [file:riga] — [descrizione] — [convenzione/regola violata]
- ...

### Issue minori (suggerimenti)
- [M1] [file:riga] — [descrizione] — [suggerimento]
- ...

### Pattern LAIF
- Rispettati: [lista]
- Violati: [lista con riferimento a processi.md]

### Pattern KB
- Pattern esistenti applicabili non usati: [lista con riferimento a patterns/]
- Pattern candidati per estrazione: [lista con breve descrizione]

### Verdetto: PASS / FAIL
[PASS se zero issue critiche, FAIL altrimenti]
[Se FAIL: lista fix necessari]
```

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Feature Review

Feature revisionata: [RF-XX — titolo]
File analizzati: [N]
Issue critiche: [N] (bloccanti)
Issue minori: [N] (suggerimenti)
Pattern LAIF violati: [N]
Pattern KB candidati: [N]

Verdetto: [PASS / FAIL]
[Se FAIL: lista issue critiche]

Documenti aggiornati:
  projects/[nome]/.feature-state.md (sezione Review)

Prossimi passi:
  [Se PASS] → Attendi risultato feature-test per GATE 3
  [Se FAIL] → Torna a feature-develop con fix list
  [Se pattern candidati] → Considera estrazione-pattern dopo il merge
```

---

## Checklist qualità

- [ ] Tutti i file creati/modificati sono stati revisionati
- [ ] Convenzioni LAIF verificate contro `processi.md`
- [ ] Check duplicazioni eseguito (intra-feature e cross-progetto)
- [ ] Check qualità e sicurezza completato
- [ ] Confronto con `patterns/` completato
- [ ] Issue classificate correttamente (critica vs minore)

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
