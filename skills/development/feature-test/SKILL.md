---
nome: "Feature Test"
descrizione: >
  Testa una feature in modo completo: scrive test mancanti, esegue la suite,
  verifica i criteri di accettazione, testa edge case e controlla regressioni.
  NON modifica il codice applicativo — solo test. Per fix → feature-develop.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/.feature-state.md (Piano + Sviluppo)
  - projects/[nome]/requisiti.md (criteri di accettazione)
  - Codebase del progetto (codice + test esistenti)
scrive:
  - Codebase del progetto (nuovi test)
  - projects/[nome]/.feature-state.md (sezione Test)
aggiornato: "2026-03-09"
---

# Skill: Feature Test

## Obiettivo

Verifica che una feature implementata funzioni correttamente: scrive test mancanti, esegue la suite completa, verifica i criteri di accettazione, testa edge case e controlla che non ci siano regressioni.

---

## Perimetro

**Fa**: scrive nuovi test, esegue test suite, verifica criteri di accettazione, identifica regressioni, testa edge case.

**NON fa**: modifica codice applicativo (→ `feature-develop`), review qualità codice (→ `feature-review`).

**Può essere invocata**: standalone o come parte di `feature-workflow` (in parallelo con `feature-review`).

---

## Quando usarla

- Dopo che lo sviluppo è completato (GATE 2 passato)
- Quando si vuole testare una feature specifica in modo approfondito
- Quando `.feature-state.md` contiene le sezioni Piano e Sviluppo

---

## Prerequisiti

- [ ] Feature implementata (codice presente nella codebase)
- [ ] `.feature-state.md` con sezione Piano (criteri) e Sviluppo (file modificati)
- [ ] Accesso alla codebase del progetto (repo Git)

---

## Loop conversazionale

Fai le domande in questo ordine, **una alla volta**:

1. **Ci sono scenari edge case specifici da testare?** (es. "testa con utente senza permessi", "testa con lista vuota")
2. **Il progetto ha una test suite esistente?** (framework usato, path dei test, comandi per eseguire)

---

## Processo di produzione

1. Leggi i criteri di accettazione da `requisiti.md` (RF-XX)
2. Leggi il piano e i file modificati da `.feature-state.md` (sezioni Piano + Sviluppo)
3. Analizza i test esistenti nella codebase per capire:
   - Framework di test usato (pytest, jest, vitest, ecc.)
   - Pattern di test seguiti (naming, struttura, fixture)
   - Coverage attuale
4. **Scrivi nuovi test**:
   - **Unit test** per ogni funzione/componente nuovo o significativamente modificato
   - **Integration test** per i flussi principali della feature
   - **Edge case** per ciascun endpoint/componente:
     - Input invalidi o mancanti
     - Valori limite (zero, stringhe vuote, liste lunghe)
     - Permessi e autorizzazioni
     - Scenari concorrenti (se applicabile)
5. **Esegui la suite completa** (non solo i nuovi test):
   - Comando di esecuzione test del progetto
   - Verifica che TUTTI i test passino (nuovi + esistenti)
6. **Verifica criteri di accettazione**:
   - Per ogni criterio di accettazione del requisito → identifica il test che lo copre
   - Se un criterio non ha test → scrivilo
   - Mappa: criterio → test → risultato (PASS/FAIL)
7. **Controlla regressioni**:
   - La suite pre-esistente passa ancora?
   - Funzionalità correlate non sono state rotte?
8. Aggiorna `.feature-state.md` sezione `## Test` con il report

### Formato report test

```markdown
## Test

### Test scritti
- `test_[nome].py` / `[nome].test.ts` — [cosa testa]
- ...

### Risultati esecuzione
- Suite completa: [N] test, [N] passati, [N] falliti
- Nuovi test: [N] scritti, [N] passati
- Regressioni: [nessuna / lista]

### Criteri di accettazione
| Criterio | Test | Risultato |
|----------|------|-----------|
| [criterio 1] | [test che lo copre] | PASS/FAIL |
| ... | ... | ... |

### Edge case testati
- [scenario] → [risultato]
- ...

### Verdetto: PASS / FAIL
[Se FAIL: lista dei problemi da risolvere]
```

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Feature Test

Feature testata: [RF-XX — titolo]
Test scritti: [N] nuovi test
Suite completa: [N] test totali, [N] passati, [N] falliti
Criteri di accettazione: [N/N] soddisfatti
Regressioni: [nessuna / N trovate]
Edge case: [N] testati

Verdetto: [PASS / FAIL]
[Se FAIL: lista problemi]

Documenti aggiornati:
  projects/[nome]/.feature-state.md (sezione Test)

Prossimi passi:
  [Se PASS] → Attendi risultato feature-review per GATE 3
  [Se FAIL] → Torna a feature-develop con fix list
```

---

## Checklist qualità

- [ ] Ogni criterio di accettazione ha almeno un test che lo copre
- [ ] Edge case testati (almeno 2 per endpoint/componente)
- [ ] Suite completa passa (nuovi + vecchi test)
- [ ] Nessuna regressione nella suite pre-esistente
- [ ] Coverage dei file modificati >= 80% (se misurabile)
- [ ] I test seguono i pattern e le convenzioni della suite esistente

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
