---
nome: "Genera Mockup Brief"
descrizione: >
  A partire da requisiti.md validato, genera il brief per i mockup destinato a Windsurf.
  Descrive schermate prioritarie, flussi di navigazione, brand guidelines e vincoli UI.
fase: presales
versione: "1.0"
stato: beta
dipende-da: "projects/[nome]/requisiti.md (completo e validato)"
legge:
  - projects/[nome]/requisiti.md
  - projects/[nome]/README.md
scrive:
  - projects/[nome]/mockup-brief.md
aggiornato: "2026-03-08"
---

# Skill: Genera Mockup Brief

## Obiettivo

Produce il brief per i mockup: documento operativo per Windsurf che descrive le schermate da progettare, i flussi di navigazione, e i vincoli visivi.

---

## Perimetro

**Fa**: genera il brief mockup per Windsurf a partire dai requisiti validati.
**Non fa**: non genera l'allegato contrattuale (usa `genera-allegato-tecnico` per quello).
**Non fa**: non struttura i requisiti (usa `estrazione-requisiti` prima).

---

## Prerequisiti

- [ ] `projects/[nome]/requisiti.md` completo (nessuna domanda aperta critica)
- [ ] `projects/[nome]/README.md` con info cliente compilate

Se mancano, blocca e indica cosa completare prima.

---

## Loop conversazionale

### Domanda 1 — Schermate prioritarie

Quali sono le 3-5 schermate prioritarie da mockuppare?
(Se non sei sicuro, ti propongo quelle che emergono dai requisiti.)

### Domanda 2 — Brand guidelines

Hai brand guidelines del cliente? (colori, font, logo)
Se no, usiamo un design neutro che Windsurf potrà personalizzare.

### Domanda 3 — Dispositivi

Dispositivi prioritari: desktop, mobile, o entrambi?
Se entrambi, quale ha la priorità?

### Domanda 4 — Vincoli UI

Ci sono vincoli UI da rispettare? (es. integrazione con sistema esistente, componenti da riutilizzare, framework CSS specifico)

Ad ogni step, se la skill è in stato **beta**, chiedi se il processo ha senso o se va modificato.

---

## Processo di produzione

1. Per ogni schermata: scopo, elementi chiave, flusso di navigazione
2. Includi struttura di navigazione testuale (ASCII tree)
3. Sezione "cosa NON mockuppare" — evita false aspettative
4. Aggiungi header per Windsurf:
   "Windsurf: questo file è il brief completo per i mockup. Non richiede ulteriori chiarimenti per iniziare."
5. Salva in `projects/[nome]/mockup-brief.md`

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Genera Mockup Brief

File prodotto:
  projects/[nome]/mockup-brief.md  (X schermate)

Riepilogo:
  Schermate da mockuppare: [lista titoli]
  Dispositivi: [desktop/mobile/entrambi]

Prossimi passi:
  → Il file è pronto in projects/[nome]/mockup-brief.md
    Windsurf può leggerlo direttamente da quella path
```

---

## Checklist qualità

- [ ] Ogni schermata ha: scopo, elementi chiave, flusso
- [ ] Informazioni visive specificate (o indicato "nessuna preferenza")
- [ ] Sezione "cosa NON mockuppare" presente
- [ ] Header per Windsurf presente

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
