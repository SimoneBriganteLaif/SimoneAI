---
nome: "Genera Documenti Presales"
descrizione: >
  A partire da requisiti.md validato, genera due documenti: l'allegato tecnico
  contrattuale (max 3 pagine, linguaggio non tecnico) e il brief mockup per Windsurf.
  Può produrre i due documenti insieme o separatamente.
fase: presales
versione: "1.1"
dipende-da: "projects/[nome]/presales/requisiti.md (completo e validato)"
output:
  - projects/[nome]/presales/allegato-tecnico.md
  - projects/[nome]/presales/requisiti-mockup.md
aggiornato: "2026-03-08"
---

# Skill: Genera Documenti Presales

## Obiettivo

Produce i due documenti presales finali a partire dai requisiti validati:
1. **Allegato tecnico** — per il contratto, linguaggio non tecnico, max 3 pagine
2. **Brief mockup** — per Windsurf, letto direttamente dal file nella KB

---

## Prerequisiti

- [ ] `projects/[nome]/presales/requisiti.md` completo (nessuna domanda aperta critica)
- [ ] `projects/[nome]/README.md` con info cliente compilate

Se mancano, blocca e indica cosa completare prima.

---

## Loop conversazionale — Allegato Tecnico

### Fase 1 — Calibrazione

1. Quali funzionalità sono escluse dall'ambito contrattuale ma rischiamo di non rendere esplicite?
2. Chi leggerà l'allegato? (CEO, ufficio legale, consulente esterno)
   → determina il livello di formalità e tecnicità del linguaggio

### Fase 2 — Struttura proposta

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

---

## Loop conversazionale — Brief Mockup

1. Quali sono le 3-5 schermate prioritarie da mockuppare?
2. Hai brand guidelines (colori, font, logo)?
3. Dispositivi prioritari: desktop, mobile, o entrambi?
4. Ci sono vincoli UI da rispettare (es. integrazione con sistema esistente)?

---

## Processo di produzione

### Allegato tecnico
1. Estrai le funzionalità da `requisiti.md`
2. Scrivi in linguaggio **non tecnico**: niente acronimi, niente stack, niente architettura
3. Test auto: "Un CEO capisce tutto senza chiedere?" — se no, riscrivi
4. Verifica: max 3 pagine (~1500 parole totali)
5. Salva in `projects/[nome]/presales/allegato-tecnico.md`

### Brief mockup
1. Per ogni schermata: scopo, elementi chiave, flusso di navigazione
2. Include struttura di navigazione testuale (ASCII tree)
3. Sezione "cosa NON mockuppare" — evita false aspettative
4. **Nota in testa al file**: "Windsurf: questo file è il brief completo per i mockup.
   Non richiede ulteriori chiarimenti per iniziare."
5. Salva in `projects/[nome]/presales/requisiti-mockup.md`

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Genera Documenti Presales

File prodotti:
  projects/[nome]/presales/allegato-tecnico.md  (~X pagine)
  projects/[nome]/presales/requisiti-mockup.md  (X schermate)

Allegato tecnico:
  Funzionalità incluse: [N]
  Funzionalità escluse: [N]
  Destinatario: [ruolo]

Brief mockup:
  Schermate da mockuppare: [lista titoli]
  Dispositivi: [desktop/mobile/entrambi]

Prossimi passi:
  → Allegato tecnico: converti in PDF/Word per il cliente
  → Brief mockup: il file è pronto in projects/[nome]/presales/requisiti-mockup.md
     Windsurf può leggerlo direttamente da quella path
```

---

## Checklist qualità

**Allegato tecnico**
- [ ] Nessun acronimo tecnico non spiegato
- [ ] Le esclusioni sono inequivocabili
- [ ] Max 3 pagine (~1500 parole)
- [ ] Le responsabilità del cliente sono chiare e numerabili
- [ ] Autonomo: si capisce senza aver letto i requisiti

**Brief mockup**
- [ ] Ogni schermata ha: scopo, elementi chiave, flusso
- [ ] Informazioni visive specificate (o indicato "nessuna preferenza")
- [ ] Sezione "cosa NON mockuppare" presente
- [ ] Header per Windsurf presente
