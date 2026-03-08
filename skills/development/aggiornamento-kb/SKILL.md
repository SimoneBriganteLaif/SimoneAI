---
nome: "Aggiornamento Knowledge Base"
descrizione: >
  A fine sprint o fine progetto, analizza feature-log.md e decisioni-tecniche.md
  per estrarre pattern riutilizzabili e aggiornare la knowledge base cross-progetto.
fase: development
versione: "1.1"
output:
  - patterns/[nuovo-pattern].md (nuovo o aggiornato)
  - knowledge/industrie/[settore].md (aggiornamento opzionale)
  - knowledge/problemi-tecnici/[problema].md (aggiornamento opzionale)
aggiornato: "2026-03-08"
---

# Skill: Aggiornamento Knowledge Base

## Obiettivo

Trasforma l'esperienza accumulata su un progetto in asset riutilizzabili per i progetti futuri.

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
✓ COMPLETATO — Aggiornamento Knowledge Base

Estratto da: projects/[nome]
Periodo analizzato: [sprint/date]

Pattern nuovi creati: [N]
  → [lista nomi]

Pattern aggiornati: [N]
  → [lista nomi]

Knowledge aggiornata:
  → [lista file]

Prossimi passi:
  → Esegui skills/maintenance/aggiornamento-periodico/ a fine mese per pulizia completa
```

---

## Checklist qualità

- [ ] Ogni pattern nuovo usa il template completo
- [ ] Nessun dato sensibile del cliente nei pattern
- [ ] `patterns/README.md` aggiornato
- [ ] `.tags/index.md` aggiornato
