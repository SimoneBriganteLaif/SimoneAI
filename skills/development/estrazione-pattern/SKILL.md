---
nome: "Estrazione Pattern"
descrizione: >
  A fine sprint o fine progetto, analizza feature-log.md e decisioni-tecniche.md
  di UN PROGETTO SPECIFICO per estrarre pattern riutilizzabili in patterns/ e
  aggiornare la knowledge cross-progetto in knowledge/.
  NON è un audit generale della KB (per quello usa audit-periodico).
fase: development
versione: "1.2"
stato: beta
legge:
  - projects/[nome]/development/feature-log.md
  - projects/[nome]/development/decisioni-tecniche.md
  - patterns/ (per verificare duplicati)
scrive:
  - patterns/[nuovo-pattern].md (nuovo o aggiornato)
  - patterns/README.md (indice)
  - knowledge/industrie/[settore].md (opzionale)
  - knowledge/problemi-tecnici/[problema].md (opzionale)
  - .tags/index.md
aggiornato: "2026-03-08"
---

# Skill: Estrazione Pattern

## Obiettivo

Trasforma l'esperienza accumulata su un progetto specifico in asset riutilizzabili per i progetti futuri.

---

## Perimetro

**Fa**: analizza UN progetto specifico ed estrae pattern e knowledge riutilizzabili.
**Non fa**: non audita l'intera KB (per quello usa `audit-periodico`).
**Non fa**: non gestisce changelog, idee o docs (per quello usa `gestione-kb`).

---

## Quando usarla

- A fine sprint
- A fine progetto
- Quando hai risolto un problema che non vuoi dover risolvere di nuovo
- Quando hai adattato un pattern da un progetto precedente

---

## Prerequisiti

- [ ] Accesso a `projects/[nome]/development/feature-log.md`
- [ ] Accesso a `projects/[nome]/development/decisioni-tecniche.md`

---

## Loop conversazionale

### Fase 1 — Ricognizione (automatica)

Leggi `feature-log.md` e `decisioni-tecniche.md`. Poi chiedi:

1. C'è qualcosa che hai risolto in questo progetto che pensi si ripresenterà su altri?
2. Hai usato o adattato pattern da altri progetti LAIF?

### Fase 2 — Valutazione candidati

Per ogni candidato, chiedi:
- Il problema è abbastanza generico per altri tipi di progetto? → `patterns/`
- È specifico del settore del cliente? → `knowledge/industrie/`
- Esiste già un pattern simile in `patterns/`? → aggiorna quello, non duplicare

### Fase 3 — Conferma

```
Candidati identificati:

NUOVI PATTERN:
  [Nome]: [problema che risolve] → patterns/[file].md

PATTERN DA AGGIORNARE:
  [Nome]: [cosa aggiungere] → patterns/[file].md (aggiungo esperienza)

KNOWLEDGE CROSS-PROGETTO:
  [Cosa]: knowledge/[sezione]/[file].md

Procedo?
```

Ad ogni step, se la skill è in stato **beta**, chiedi se il processo ha senso o se va modificato.

---

## Processo di produzione

**Pattern nuovo**: copia `patterns/_template.md`, compilalo completamente, aggiungi in "Esempi reali"
**Pattern esistente**: aggiungi il progetto in "Esempi reali", aggiungi varianti o miglioramenti se trovati
**Knowledge**: aggiorna il file appropriato in `knowledge/`

Dopo ogni modifica:
- Aggiorna `patterns/README.md` → indice
- Aggiorna `.tags/index.md`

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Estrazione Pattern

Estratto da: projects/[nome]
Periodo analizzato: [sprint/date]

Pattern nuovi creati: [N]
  → [lista nomi]

Pattern aggiornati: [N]
  → [lista nomi]

Knowledge aggiornata:
  → [lista file]

Prossimi passi:
  → Esegui skills/maintenance/audit-periodico/ a fine mese per audit completo
```

---

## Checklist qualità

- [ ] Ogni pattern nuovo usa il template completo
- [ ] Nessun dato sensibile del cliente nei pattern
- [ ] `patterns/README.md` aggiornato
- [ ] `.tags/index.md` aggiornato

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
