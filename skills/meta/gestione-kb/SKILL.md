---
nome: "Gestione Knowledge Base"
descrizione: >
  Gestisce i meta-file del sistema: changelog (framework e contenuti),
  backlog idee, documentazione, e review periodica delle idee.
  Opera in 4 modalità selezionabili.
fase: meta
versione: "1.0"
output:
  - CHANGELOG-framework.md
  - CHANGELOG-contenuti.md
  - IDEAS.md
  - docs/struttura.md
  - docs/skills.md
  - docs/workflow.md
aggiornato: "2026-03-08"
---

## Obiettivo

Mantenere aggiornati e coerenti i meta-file del sistema: changelog, backlog idee, e documentazione. Questa skill è il punto unico per tutte le operazioni di "manutenzione del framework".

## Quando usarla / Trigger

- **Dopo ogni modifica alla struttura della KB** (nuove cartelle, skill, template, processi)
- **Dopo ogni modifica ai contenuti** (nuovi progetti, pattern, knowledge)
- **Quando viene un'idea** per migliorare il sistema
- **Periodicamente** per sincronizzare la documentazione e fare review delle idee

## Prerequisiti

Nessuno. Questa skill è sempre invocabile.

---

## Loop conversazionale

### Domanda iniziale

> In che modalità vuoi operare?
> 1. **Registra modifica** — aggiorna il changelog appropriato
> 2. **Aggiungi idea** — inserisci una nuova idea nel backlog
> 3. **Sync documentazione** — verifica e aggiorna docs/ rispetto alla struttura reale
> 4. **Review idee** — rivedi le idee pendenti e decidi cosa farne

---

## Modalità 1 — Registra modifica

### Loop

1. **Cosa è cambiato?** Descrivi brevemente la modifica.
2. **È una modifica al framework o ai contenuti?**
   - **Framework**: struttura cartelle, skill, template, processi, documentazione del sistema
   - **Contenuti**: progetti, pattern, knowledge, decisioni tecniche
3. **Categoria?**
   - Framework: `Added` | `Changed` | `Removed` | `Fixed`
   - Contenuti: `Progetti` | `Pattern` | `Knowledge` | `Decisioni`

### Processo

1. Apri il changelog corretto (`CHANGELOG-framework.md` o `CHANGELOG-contenuti.md`)
2. Se non esiste una sezione `[Non rilasciato]`, creala in cima
3. Aggiungi l'entry sotto la categoria corretta con la data
4. Se la modifica è al framework e impatta `docs/`, aggiorna anche i file di documentazione:
   - Nuova cartella → aggiorna `docs/struttura.md`
   - Nuova/modificata skill → aggiorna `docs/skills.md`
   - Nuovo/modificato flusso → aggiorna `docs/workflow.md`

### Output in chat

```
✓ Changelog aggiornato: [framework|contenuti]
  Categoria: [categoria]
  Entry: [descrizione breve]
  Docs aggiornati: [sì/no — quali file]
```

---

## Modalità 2 — Aggiungi idea

### Loop

1. **Descrivi l'idea.** Anche in forma grezza, la strutturiamo insieme.
2. **In quale categoria rientra?** `struttura` | `skill` | `processo` | `integrazione` | `automazione`
3. **Effort stimato?** `S` (poche ore) | `M` (1-2 sessioni) | `L` (progettazione + più sessioni)
4. **Priorità suggerita?** `alta` | `media` | `bassa` (o lascia che la valuti io)
5. **Note aggiuntive?** Contesto, dipendenze, link rilevanti (opzionale)

### Processo

1. Apri `IDEAS.md`
2. Trova l'ultimo IDEA-NNN e incrementa
3. Aggiungi la riga nella tabella "Idee attive" con:
   - ID: `IDEA-[NNN+1]`
   - Stato: `proposta`
   - Data: data odierna
4. Se l'idea ha dipendenze da altre idee, annotalo nelle note

### Output in chat

```
✓ Idea registrata: IDEA-[NNN]
  Titolo: [titolo breve]
  Categoria: [categoria] | Effort: [S/M/L] | Priorità: [alta/media/bassa]
```

---

## Modalità 3 — Sync documentazione

### Loop

Nessuna domanda iniziale. Processo autonomo con conferma prima di scrivere.

### Processo

1. **Scansiona la struttura reale** delle cartelle della KB
2. **Leggi i file di documentazione** attuali:
   - `docs/struttura.md` — confronta albero documentato vs reale
   - `docs/skills.md` — confronta elenco skill documentate vs cartelle in `skills/`
   - `docs/workflow.md` — verifica coerenza con skill esistenti
3. **Identifica differenze**:
   - Cartelle esistenti ma non documentate
   - Cartelle documentate ma inesistenti
   - Skill aggiunte/rimosse/modificate
   - Diagrammi Mermaid non aggiornati
4. **Mostra le differenze** all'utente prima di procedere
5. **Aggiorna** i file di documentazione solo dopo conferma
6. Se ci sono state modifiche, registrale nel `CHANGELOG-framework.md` (usa modalità 1 internamente)

### Output in chat

```
✓ Sync documentazione completata
  File verificati: [N]
  Differenze trovate: [N]
  File aggiornati: [lista o "nessuno — tutto allineato"]
```

---

## Modalità 4 — Review idee

### Loop

Nessuna domanda iniziale. Processo guidato per ogni idea pendente.

### Processo

1. **Leggi `IDEAS.md`** e filtra le idee con stato `proposta` o `approvata`
2. **Per ogni idea**, mostra:
   - ID, titolo, categoria, effort, priorità, data, note
   - Tempo trascorso dalla proposta
3. **Chiedi per ciascuna** (una alla volta):
   - **Implementare ora** → stato diventa `in-corso`, discutiamo i prossimi passi
   - **Approvare per dopo** → stato diventa `approvata`
   - **Rimandare** → resta `proposta`, aggiorna note se necessario
   - **Scartare** → sposta nella sezione "Idee scartate" con motivo
4. **Aggiorna `IDEAS.md`** con le decisioni prese
5. Se un'idea viene completata, registra in `CHANGELOG-framework.md` o `CHANGELOG-contenuti.md`

### Output in chat

```
✓ Review idee completata
  Idee revisionate: [N]
  → In corso: [N] ([lista ID])
  → Approvate: [N] ([lista ID])
  → Rimandate: [N]
  → Scartate: [N] ([lista ID])
```

---

## Checklist qualità

- [ ] Ogni entry di changelog ha la data corretta
- [ ] Gli ID delle idee sono progressivi e senza buchi
- [ ] I diagrammi Mermaid sono sintatticamente corretti (dopo sync)
- [ ] I link interni tra file sono validi
- [ ] Le idee scartate hanno sempre un motivo documentato
- [ ] Nessun duplicato tra idee attive e scartate
