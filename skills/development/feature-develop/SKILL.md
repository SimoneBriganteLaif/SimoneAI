---
nome: "Feature Develop"
descrizione: >
  Implementa una feature seguendo il piano prodotto da feature-plan.
  Può sviluppare direttamente (Claude Code) o produrre un brief dettagliato per Windsurf.
  NON testa e NON revisiona — si limita a implementare. Per test → feature-test. Per review → feature-review.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/.feature-state.md (sezione Piano)
  - knowledge/azienda/processi.md
  - knowledge/azienda/stack.md
  - Codebase del progetto (repo Git)
scrive:
  - Codebase del progetto (codice)
  - projects/[nome]/.feature-state.md (sezione Sviluppo)
aggiornato: "2026-03-09"
---

# Skill: Feature Develop

## Obiettivo

Implementa una feature seguendo il piano tecnico approvato. Opera in due modalità: sviluppo diretto (Claude Code) o produzione di un brief autocontenuto per Windsurf.

---

## Perimetro

**Fa**: implementazione codice, creazione file, seguire convenzioni LAIF, aggiornare lo stato di avanzamento.

**NON fa**: test (→ `feature-test`), review codice (→ `feature-review`), pianificazione (→ `feature-plan`).

**Può essere invocata**: standalone (con piano già scritto) o come parte di `feature-workflow`.

---

## Quando usarla

- Dopo che il piano è stato approvato (GATE 1 passato)
- Quando `.feature-state.md` contiene una sezione Piano completa
- Quando si deve implementare una feature già pianificata

---

## Prerequisiti

- [ ] Piano approvato in `.feature-state.md` (sezione Piano)
- [ ] Accesso alla codebase del progetto (repo Git clonata)
- [ ] Convenzioni LAIF note (processi.md)

---

## Loop conversazionale

Fai le domande in questo ordine, **una alla volta**:

1. **Sviluppo diretto (Claude Code) o brief per Windsurf?**
2. **(Solo se Windsurf)** Path della repo di destinazione?

---

## Processo di produzione — Modalità Claude Code

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

## Processo di produzione — Modalità Windsurf Brief

1. Leggi il piano dalla sezione `## Piano` di `.feature-state.md`
2. Produci un brief **autocontenuto** (Windsurf non ha accesso alla KB):
   - **Contesto progetto**: stack, architettura, obiettivo feature
   - **Task list**: dal piano, con ordine e dipendenze
   - **Convenzioni LAIF**: copiate integralmente da `processi.md` (non referenziate)
   - **Codice esistente**: snippet rilevanti dalla codebase attuale
   - **Criteri di accettazione**: dal piano
   - **File da creare/modificare**: lista completa con path
3. Mostra il brief all'utente per passaggio manuale a Windsurf
4. Aggiorna `.feature-state.md` sezione `## Sviluppo` con: "Brief Windsurf generato — in attesa di implementazione"
5. **Tracking**: `echo "$(date +%Y-%m-%d\ %H:%M) | feature-develop | [progetto] | completata-ws" >> .claude/skill-usage.log`

---

## Output in chat (obbligatorio al termine)

### Modalità Claude Code:
```
✓ COMPLETATO — Feature Develop (Claude Code)

Feature implementata: [RF-XX — titolo]
File creati: [N]
File modificati: [N]
Task completati: [N/N]

Documenti aggiornati:
  projects/[nome]/.feature-state.md (sezione Sviluppo)

Prossimi passi:
  → Conferma che lo sviluppo è completo (GATE 2)
  → Poi: skills/development/feature-test/ + feature-review/
```

### Modalità Windsurf:
```
✓ COMPLETATO — Feature Develop (Brief Windsurf)

Brief generato per: [RF-XX — titolo]
Task nel brief: [N]

Prossimi passi:
  → Passa il brief a Windsurf per l'implementazione
  → Dopo l'implementazione: aggiorna .feature-state.md e procedi con test/review
```

---

## Checklist qualità

- [ ] Tutti i task del piano sono stati implementati (o inclusi nel brief)
- [ ] Le convenzioni LAIF sono state seguite (RouterBuilder, CRUDService, @laif/ds, naming)
- [ ] Il codice compila senza errori (modalità Claude Code)
- [ ] Nessun file del piano è stato saltato
- [ ] La sezione Sviluppo di `.feature-state.md` è aggiornata

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
