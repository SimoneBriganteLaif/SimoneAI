---
nome: "Genera Allegato Tecnico"
descrizione: >
  A partire da requisiti.md validato, genera l'allegato tecnico contrattuale.
  Max 3 pagine, linguaggio non tecnico, comprensibile da un CEO senza contesto.
fase: presales
versione: "1.0"
stato: beta
dipende-da: "projects/[nome]/presales/requisiti.md (completo e validato)"
legge:
  - projects/[nome]/presales/requisiti.md
  - projects/[nome]/README.md
scrive:
  - projects/[nome]/presales/allegato-tecnico.md
aggiornato: "2026-03-08"
---

# Skill: Genera Allegato Tecnico

## Obiettivo

Produce l'allegato tecnico per il contratto: documento non tecnico (max 3 pagine) che descrive cosa viene fornito, cosa è escluso, e le responsabilità del cliente.

---

## Perimetro

**Fa**: genera l'allegato contrattuale a partire dai requisiti validati.
**Non fa**: non genera il brief mockup (usa `genera-mockup-brief` per quello).
**Non fa**: non struttura i requisiti (usa `estrazione-requisiti` prima).

---

## Prerequisiti

- [ ] `projects/[nome]/presales/requisiti.md` completo (nessuna domanda aperta critica)
- [ ] `projects/[nome]/README.md` con info cliente compilate

Se mancano, blocca e indica cosa completare prima.

---

## Loop conversazionale

### Domanda 1 — Esclusioni

Quali funzionalità sono escluse dall'ambito contrattuale ma rischiamo di non rendere esplicite?
(Questo è il punto più critico: le esclusioni vaghe generano contenziosi.)

### Domanda 2 — Destinatario

Chi leggerà l'allegato? (CEO, ufficio legale, consulente esterno?)
→ Determina il livello di formalità e tecnicità del linguaggio.

### Domanda 3 — Struttura proposta

Presenta la struttura prima di scrivere:

```
Struttura allegato tecnico proposta:
1. Oggetto della fornitura
2. Funzionalità incluse ([N] voci da RF)
3. Funzionalità escluse
4. Modalità di consegna
5. Responsabilità del cliente
6. Manutenzione post go-live
7. Proprietà intellettuale

Stima: ~[N] pagine. Modifico la struttura?
```

Ad ogni step, se la skill è in stato **beta**, chiedi se il processo ha senso o se va modificato.

---

## Processo di produzione

1. Estrai le funzionalità da `requisiti.md`
2. Scrivi in linguaggio **non tecnico**: niente acronimi, niente stack, niente architettura
3. Test auto: "Un CEO capisce tutto senza chiedere?" — se no, riscrivi
4. Verifica: max 3 pagine (~1500 parole totali)
5. Salva in `projects/[nome]/presales/allegato-tecnico.md`

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Genera Allegato Tecnico

File prodotto:
  projects/[nome]/presales/allegato-tecnico.md  (~X pagine)

Riepilogo:
  Funzionalità incluse: [N]
  Funzionalità escluse: [N]
  Destinatario: [ruolo]

Prossimi passi:
  → Converti in PDF/Word per il cliente
  → Se servono mockup, esegui: skills/presales/genera-mockup-brief/
```

---

## Checklist qualità

- [ ] Nessun acronimo tecnico non spiegato
- [ ] Le esclusioni sono inequivocabili
- [ ] Max 3 pagine (~1500 parole)
- [ ] Le responsabilità del cliente sono chiare e numerabili
- [ ] Autonomo: si capisce senza aver letto i requisiti
