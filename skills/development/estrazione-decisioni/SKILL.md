---
nome: "Estrazione Decisioni Tecniche"
descrizione: >
  Cattura una decisione tecnica non banale in formato ADR (Architecture Decision Record).
  Documenta contesto, alternative valutate, trade-off e impatto architetturale.
  NON per decisioni ovvie — solo per scelte che qualcuno potrebbe mettere in discussione.
fase: development
versione: "1.1"
stato: beta
legge:
  - projects/[nome]/development/decisioni-tecniche.md (per numero ADR)
  - projects/[nome]/development/architettura.md (per valutare impatto)
scrive:
  - projects/[nome]/development/decisioni-tecniche.md (nuovo ADR)
  - projects/[nome]/development/architettura.md (se impatto architetturale)
aggiornato: "2026-03-08"
---

# Skill: Estrazione Decisioni Tecniche

## Obiettivo

Cattura le decisioni tecniche mentre vengono prese, nel formato ADR.
Una decisione non documentata è una decisione che si ripete.

---

## Quando usarla

Usa questa skill quando:
- Scegli una tecnologia o libreria nuova
- Decidi un'architettura o pattern non banale
- Scarti un'opzione valida in favore di un'altra
- Risolvi un problema complesso in modo non ovvio
- Il codice fa qualcosa che sorprenderà chi lo legge la prima volta

**Non usarla per**: decisioni banali o ovvie (es. "usiamo React perché è già nel progetto").

---

## Prerequisiti

Uno o più di:
- [ ] Descrizione della decisione presa
- [ ] Codice o snippet rilevante
- [ ] Link a PR/commit
- [ ] Discussione (Slack, email) in cui è stata presa la decisione

---

## Loop conversazionale

Fai le domande in questo ordine, **una alla volta**:

1. **Cosa è stato deciso?** (una riga, chiara senza contesto)
2. **Perché era necessaria una decisione?** (qual era il problema o il bivio)
3. **Quali alternative sono state valutate?** (anche brevemente)
4. **Perché questa opzione e non le altre?** (i motivi reali)
5. **Ci sono trade-off o limitazioni accettate?**
6. **Questa decisione impatta l'architettura generale?** (sì/no → se sì, aggiorno anche architettura.md)
7. **La decisione è reversibile?** Se no, perché.

### Riepilogo prima di scrivere

```
ADR da aggiungere:

Titolo: [titolo]
Stato: Accettata
Contesto: [2-3 righe]
Decisione: [la scelta]
Alternative scartate: [lista]
Trade-off: [cosa perdiamo]
Impatto su architettura: sì / no

Scrivo?
```

---

## Processo di produzione

1. Leggi `decisioni-tecniche.md` per determinare il prossimo numero ADR
2. Aggiungi la nuova sezione ADR in **cima** al documento (ordine cronologico inverso)
3. Aggiorna l'indice in fondo al documento
4. Se la decisione impatta l'architettura: aggiorna le sezioni rilevanti di `architettura.md`
5. Valuta: è un **pattern riutilizzabile**? → se sì, segnalalo nell'output

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Estrazione Decisione Tecnica

ADR aggiunto: [ADR-NNN] — [titolo]
Documenti aggiornati:
  projects/[nome]/development/decisioni-tecniche.md
  [projects/[nome]/development/architettura.md  ← solo se impatta arch]

Pattern riutilizzabile rilevato: [sì/no]
  → [Se sì: considera di estrarlo in patterns/ con la skill aggiornamento-kb]

Prossimi passi:
  → Condividi l'ADR con il team se la decisione li impatta
  [→ Esegui skills/development/estrazione-pattern/ se vuoi estrarre il pattern ora]
```

---

## Checklist qualità

- [ ] Il titolo dell'ADR spiega la decisione in modo autonomo (senza leggere il corpo)
- [ ] Le alternative scartate sono documentate con motivazione
- [ ] I trade-off sono onesti — nessuna decisione è perfetta
- [ ] Le conseguenze per gli altri dev sono chiare
- [ ] L'indice in fondo a `decisioni-tecniche.md` è aggiornato
