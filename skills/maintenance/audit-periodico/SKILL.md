---
nome: "Audit Periodico KB"
descrizione: >
  Audit mensile dell'INTERA Knowledge Base. Analizza tutti i progetti, verifica pattern,
  allinea tag, cerca domande aperte scadute, aggrega debito tecnico. Produce un report
  e applica gli aggiornamenti confermati.
  NON opera su un singolo progetto (per quello usa estrazione-pattern).
  NON gestisce meta-file come changelog/idee (per quello usa gestione-kb).
fase: maintenance
versione: "1.2"
stato: beta
frequenza-suggerita: "fine mese o fine sprint"
legge:
  - projects/INDEX.md + tutti i projects/[nome]/
  - patterns/ (tutti i pattern)
  - .tags/index.md
  - Tutti i requisiti.md (domande aperte)
  - Tutti i architettura.md (debito tecnico)
scrive:
  - knowledge/report-manutenzione-[YYYY-MM].md
  - patterns/ (aggiornamenti)
  - knowledge/ (aggiornamenti)
  - .tags/index.md
  - projects/INDEX.md
aggiornato: "2026-03-08"
---

# Skill: Audit Periodico KB

## Obiettivo

Mantiene la KB accurata e utile nel tempo. Previene il degrado progressivo della documentazione.

## Perimetro

**Fa**: audit dell'intera KB — progetti, pattern, tag, domande aperte, debito tecnico.
**Non fa**: non estrae pattern da un singolo progetto (per quello usa `estrazione-pattern`).
**Non fa**: non gestisce changelog, idee o docs (per quello usa `gestione-kb`).

---

## Processo (eseguibile senza input iniziale)

Esegui questi step in autonomia, poi presenta il report.

### Step 1 — Inventario progetti

Leggi `projects/INDEX.md` e ogni `projects/[nome]/README.md`. Classifica ogni progetto:

| Progetto | Stato attuale | Ultimo agg. KB | Azione |
|---------|--------------|---------------|--------|
| | | | Aggiorna / Archivia / Recupera / OK |

**Criteri**:
- **Aggiorna**: progetto attivo, documenti non aggiornati nell'ultimo mese
- **Archivia**: completato con documentazione completa → sposta in `projects/_archivio/`
- **Recupera**: completato ma documentazione lacunosa → chiedi se estrarre knowledge prima
- **OK**: tutto in ordine

### Step 2 — Verifica pattern

Per ogni file in `patterns/`:
- Usato in un progetto recente ma non aggiornato in "Esempi reali"?
- Contiene versioni o approcci obsoleti?
- Emerge un nuovo pattern dai feature-log che non è ancora documentato?

### Step 3 — Tag index

Confronta `.tags/index.md` con i tag effettivamente presenti nei file:
- Tag usati ma non nell'indice → aggiungi
- Tag nell'indice senza file → segna come inutilizzato

### Step 4 — Domande aperte scadute

Cerca in tutti i `requisiti.md` domande aperte con scadenza superata:
- Risposta trovata nel codice/meeting successivi → documenta
- Ancora aperta → segnala nel report

### Step 5 — Debito tecnico aggregato

Leggi le sezioni "Debito tecnico noto" in tutti gli `architettura.md` attivi.
Aggrega: cosa c'è, da quanto, impatto stimato.

---

## Loop conversazionale (post-analisi)

```
Analisi KB completata.

PROGETTI ATTIVI: [N]
  [Nome]: [stato] — [azione suggerita]

PROGETTI DA ARCHIVIARE: [N]
  [Nome]: [motivazione]

PATTERN:
  Da aggiornare: [N] — [lista]
  Mancanti suggeriti: [N] — [descrizione + progetto di origine]

DOMANDE APERTE SCADUTE: [N]
  [Domanda] in [progetto] — [stato]

DEBITO TECNICO ACCUMULATO:
  [Progetto]: [descrizione] (da [data])

Procedo con gli aggiornamenti, o ci sono priorità diverse?
```

---

## Esecuzione (dopo conferma)

In ordine:
1. Aggiornamenti pattern esistenti
2. Nuovi pattern da creare
3. Aggiornamenti knowledge cross-progetto
4. Archiviazione progetti completati
5. Aggiornamento `.tags/index.md`
6. Aggiornamento `projects/INDEX.md`

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Aggiornamento Periodico [YYYY-MM]

Azioni eseguite:
  Progetti aggiornati: [N]
  Progetti archiviati: [N]
  Pattern creati/aggiornati: [N]
  Knowledge aggiornata: [N file]
  Tag index allineato: sì/no

Rimasto aperto:
  [lista di cose non risolte e perché]

Report completo: knowledge/report-manutenzione-[YYYY-MM].md

Prossima manutenzione suggerita: [data]
```

---

## Checklist qualità

- [ ] Ogni progetto attivo ha documenti aggiornati nel mese corrente
- [ ] `.tags/index.md` allineato ai tag effettivi
- [ ] `projects/INDEX.md` aggiornato
- [ ] Report salvato in `knowledge/`
- [ ] Nessun pattern con "Esempi reali: vuoto" su pattern con più di 3 mesi

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
