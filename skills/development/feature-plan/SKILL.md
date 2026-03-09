---
nome: "Feature Plan"
descrizione: >
  Analizza un requisito e produce un piano di implementazione tecnico.
  Identifica file da modificare, componenti coinvolti, dipendenze e rischi.
  NON implementa — produce solo il piano. Per l'implementazione → feature-develop.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/requisiti.md
  - projects/[nome]/architettura.md
  - projects/[nome]/decisioni.md
  - knowledge/azienda/processi.md
  - knowledge/azienda/stack.md
  - patterns/
scrive:
  - projects/[nome]/.feature-state.md (sezione Piano)
aggiornato: "2026-03-09"
---

# Skill: Feature Plan

## Obiettivo

Trasforma un requisito (RF-XX o descrizione libera) in un piano di implementazione tecnico dettagliato, pronto per essere eseguito da un developer (Claude Code o Windsurf).

---

## Perimetro

**Fa**: analisi tecnica, scomposizione in task, identificazione file coinvolti, mappatura dipendenze, ricerca pattern riutilizzabili.

**NON fa**: implementazione codice, test, review. Per queste → `feature-develop`, `feature-test`, `feature-review`.

**Può essere invocata**: standalone o come parte di `feature-workflow`.

---

## Quando usarla

- Prima di iniziare lo sviluppo di una feature
- Quando un requisito è stato validato e serve un piano tecnico
- Quando si vuole stimare la complessità di un requisito

---

## Prerequisiti

- [ ] Progetto inizializzato in `projects/[nome]/`
- [ ] Requisito identificato (RF-XX in `requisiti.md` o descrizione libera)
- [ ] Accesso alla codebase del progetto (repo Git)

---

## Loop conversazionale

Fai le domande in questo ordine, **una alla volta**:

1. **Qual è il requisito?** (RF-XX da requisiti.md, oppure descrizione libera se non esiste ancora)
2. **Ci sono vincoli tecnici noti?** (es. "deve usare la libreria X", "non toccare il modulo Y", "il cliente vuole Z")
3. **Ci sono pattern già esistenti in `patterns/` da riutilizzare?** (se non lo sai, cercherò io)
4. **Backend, frontend, o fullstack?**
5. **Stima di complessità percepita?** (piccola = poche ore / media = 1-2 giorni / grande = più giorni)

### Riepilogo prima di scrivere

```
Piano feature proposto:

Requisito: [RF-XX — titolo]
Complessità: [piccola / media / grande]
Scope: [backend / frontend / fullstack]

Task (N totali):
  1. [task] → [file coinvolti]
  2. [task] → [file coinvolti]
  ...

Criteri di accettazione: [N criteri]
Rischi identificati: [N rischi]
Pattern da applicare: [lista o "nessuno"]

Procedo con la scrittura del piano?
```

---

## Processo di produzione

1. Leggi `requisiti.md` per il requisito specifico (RF-XX con criteri di accettazione)
2. Leggi `architettura.md` per capire i componenti coinvolti
3. Leggi `knowledge/azienda/processi.md` per le convenzioni LAIF
4. **Consulta `patterns/README.md`** per identificare pattern applicabili alla feature. Per ogni pattern rilevante, leggi il file completo per ottenere soluzione, codice di riferimento e checklist errori comuni. Integra i pattern nel piano come vincoli tecnici.
5. Leggi `decisioni.md` per decisioni pregresse che impattano la feature
6. Produci il piano con queste sezioni:
   - **Task list**: lista ordinata di micro-task, ciascuno atomico e verificabile
   - **File coinvolti**: lista dei file da creare/modificare con indicazione (nuovo/modifica)
   - **Dipendenze**: ordine di implementazione (es. "model prima di controller prima di route")
   - **Criteri di accettazione**: ripresi dal requisito + eventuali criteri tecnici aggiuntivi
   - **Rischi**: cosa potrebbe andare storto e come mitigare
   - **Pattern da applicare**: riferimenti a `patterns/` o convenzioni LAIF specifiche
7. Scrivi il piano nella sezione `## Piano` di `.feature-state.md`
8. **Tracking**: `echo "$(date +%Y-%m-%d\ %H:%M) | feature-plan | [progetto] | completata" >> .claude/skill-usage.log`

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Feature Plan

Piano creato per: [RF-XX — titolo]
Task: [N] task identificati
File coinvolti: [N] file ([N] nuovi, [N] modifiche)
Complessità stimata: [piccola / media / grande]

Documenti aggiornati:
  projects/[nome]/.feature-state.md (sezione Piano)

Prossimi passi:
  → Approvazione del piano (GATE 1)
  → Poi: skills/development/feature-develop/ per implementare
```

---

## Checklist qualità

- [ ] Ogni task è atomico e verificabile (non "implementa la feature")
- [ ] I criteri di accettazione sono misurabili (non "funziona bene")
- [ ] Le convenzioni LAIF sono rispettate nel piano (RouterBuilder, CRUDService, @laif/ds, soft-onion)
- [ ] I pattern riutilizzabili sono stati cercati in `patterns/` e referenziati
- [ ] L'ordine delle dipendenze è esplicito (cosa va fatto prima di cosa)
- [ ] I rischi sono concreti (non generici "potrebbe non funzionare")

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
