---
nome: "Aggiornamento Periodico KB"
descrizione: >
  Sub-agente di manutenzione mensile. Analizza l'intera KB, identifica documenti obsoleti,
  gap di documentazione e pattern non ancora estratti. Produce un report e applica gli
  aggiornamenti confermati dall'utente.
fase: maintenance
versione: "1.1"
frequenza-suggerita: "fine mese o fine sprint"
output:
  - knowledge/report-manutenzione-[YYYY-MM].md
  - aggiornamenti distribuiti nella KB
aggiornato: "2026-03-08"
---

# Skill: Aggiornamento Periodico KB

## Obiettivo

Mantiene la KB accurata e utile nel tempo. Previene il degrado progressivo della documentazione.

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
