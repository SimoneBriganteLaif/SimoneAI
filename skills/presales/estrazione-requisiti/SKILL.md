---
nome: "Estrazione Requisiti"
descrizione: >
  Trasforma note grezze di meeting, trascrizioni o documenti cliente in
  requisiti strutturati (RF + RNF) con priorità, criteri di accettazione
  e domande aperte. Produce requisiti.md nel formato LAIF.
fase: presales
versione: "1.1"
stato: beta
legge:
  - Materiale grezzo (testo incollato, file, pagine Notion)
  - projects/[nome]/ (se esiste)
scrive:
  - projects/[nome]/presales/requisiti.md
  - projects/[nome]/presales/note-meeting/[data]-[fonte].md
  - projects/INDEX.md (se progetto nuovo)
aggiornato: "2026-03-08"
---

# Skill: Estrazione Requisiti

## Obiettivo

Trasforma materiale grezzo (note meeting, trascrizioni, documenti cliente) in un documento
`requisiti.md` strutturato e validato, pronto per la fase contrattuale e di sviluppo.

---

## Prerequisiti

Verifica di avere almeno uno di:
- Trascrizione o note del meeting (testo incollato o file)
- Pagine Notion lette via MCP
- Documento di specifiche del cliente

Se non hai nulla, blocca e chiedi il materiale grezzo prima di procedere.

---

## Loop conversazionale

### Fase 1 — Orientamento (solo se il materiale è ambiguo)

Fai solo le domande necessarie, in questo ordine:

1. Chi era presente al meeting? (ruoli lato cliente e lato LAIF)
2. Qual è il contesto di business del cliente se non emerge dal materiale?
3. Esiste già una cartella in `projects/` per questo cliente?

### Fase 2 — Chiarimento requisiti

Dopo aver letto il materiale, identifica i punti ambigui e chiedi **una cosa alla volta**:

- Ambiguità su scope: "Si parla di X — è un requisito confermato o un'idea esplorativa?"
- Ambiguità su priorità: "RF-A e RF-B sembrano in conflitto. Qual è prioritario?"
- Ambiguità su attori: "Non è chiaro chi usa questa funzionalità. Puoi chiarire?"

**Regola**: non inventare requisiti. Se è ambiguo → "domanda aperta" nel documento.

### Fase 3 — Riepilogo prima di scrivere

```
Requisiti funzionali identificati:
- RF-01: [titolo] — Priorità Alta
- RF-02: [titolo] — Priorità Media
...

Requisiti non funzionali:
- Performance: [descrizione]
- Sicurezza: [descrizione]

Domande aperte da fare al cliente:
1. [domanda]

Esclusioni esplicite:
- [cosa non è incluso]

Confermo e scrivo il documento?
```

Attendi conferma prima di procedere.

---

## Processo di produzione

1. Se non esiste `projects/[nome]/`, creala copiando la struttura da `projects/_template/`
2. Salva il materiale grezzo in `projects/[nome]/presales/note-meeting/[YYYY-MM-DD]-[fonte].md`
3. Scrivi `projects/[nome]/presales/requisiti.md` seguendo il template
4. Aggiorna `projects/[nome]/README.md` con le informazioni base se mancanti
5. Aggiorna `projects/INDEX.md` se il progetto è nuovo

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Estrazione Requisiti

File prodotti:
  projects/[nome]/presales/requisiti.md
  projects/[nome]/presales/note-meeting/[data]-[fonte].md

Riepilogo:
  RF identificati: [N] (Alta: X, Media: Y, Bassa: Z)
  RNF identificati: [N]
  Domande aperte: [N]

Prossimi passi:
  → Condividi le domande aperte con il cliente
  → Quando requisiti validati, esegui:
     skills/presales/genera-allegato-tecnico/
     skills/presales/genera-mockup-brief/
```

---

## Checklist qualità

- [ ] Ogni RF ha criteri di accettazione misurabili
- [ ] Le ambiguità sono in "domande aperte", non nei requisiti
- [ ] Le esclusioni sono esplicite
- [ ] Il materiale grezzo è salvato in `note-meeting/`
- [ ] I tag nel frontmatter di `requisiti.md` sono corretti

---

## Note

- **Meeting in inglese**: scrivi i requisiti in italiano, conserva citazioni originali nelle note
- **Documento già strutturato del cliente**: non copiarlo — estrai e ristruttura nel formato LAIF
- **Requisiti contraddittori**: segnalali esplicitamente, non scegliere tu quale prevale
