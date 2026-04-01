---
nome: "Gestione Issue"
descrizione: >
  Skill interattiva per gestire le issue dello stack interno LAIF via Notion MCP.
  Legge il DB Issues e Release, guida l'utente in triage, preparazione riunione,
  pianificazione release e health check del backlog. Scrive su Notion solo dopo
  approvazione esplicita.
fase: development
versione: "0.1"
stato: beta
legge:
  - projects/laif-issue/README.md
  - projects/laif-issue/processo-issue.md
  - projects/laif-issue/flusso-riunione.md
  - projects/laif-issue/stato-progetto.md
  - Notion Issues DB: 21e90ad6-ee48-80ae-b0b3-000b7ba6ca13 (via MCP)
  - Notion Release DB: 32090ad6-ee48-80e0-9415-000b6984bd86 (via MCP)
  - GitHub PR (sola lettura, per arricchire contesto)
scrive:
  - Notion Issues DB: 21e90ad6-ee48-80ae-b0b3-000b7ba6ca13 (via MCP, solo dopo conferma)
  - Notion Release DB: 32090ad6-ee48-80e0-9415-000b6984bd86 (via MCP, solo dopo conferma)
aggiornato: "2026-03-18"
---

# Skill: Gestione Issue

> **Stato beta**: all'inizio di ogni esecuzione avvisa l'utente che la skill e' in beta. Ad ogni step chiedi se il processo ha senso o se va modificato.

## Obiettivo

Assistere nella gestione interattiva delle issue dello stack interno LAIF. La skill legge il contesto dal DB Notion, propone azioni, e scrive solo dopo approvazione esplicita dell'utente.

## Perimetro

**Fa:**
- Legge issue per stato, tipo, stack, release, filone
- Propone RICE score con motivazione
- Assegna/sposta issue tra release
- Genera sommari (agenda riunione, stato release, anomalie backlog)
- Legge PR da GitHub (sola lettura) per arricchire il contesto
- Aggiorna stati, assegnazioni, RICE su Notion dopo conferma

**Non fa:**
- Non crea nuove issue (per quello: crearle direttamente su Notion o usare `crea-task-notion`)
- Non gestisce il codice o le PR (per quello: `feature-workflow`)
- Non modifica la struttura del DB o le viste Notion

## Quando usarla / Trigger

- Prima di una riunione settimanale stack interno
- Quando si vuole fare triage delle issue nuove
- Quando si pianifica una release
- Per un health check del backlog (issue stale, RICE mancante, anomalie)
- Quando si vuole capire lo stato complessivo delle issue

## Prerequisiti

- Notion MCP abilitato
- Progetto `projects/laif-issue/` presente nella KB

---

## Loop conversazionale

> **Regola fondamentale**: un step alla volta. Non anticipare. Non scrivere su Notion prima della conferma esplicita.

---

### Step 1 — Carica contesto

**Azione automatica** (nessuna domanda):
1. Leggi `projects/laif-issue/README.md` per gli ID Notion
2. Leggi `projects/laif-issue/processo-issue.md` per le regole di processo

Procedi automaticamente allo Step 2.

---

### Step 2 — Fetch dati Notion

**Azione automatica** (nessuna domanda):
1. Usa Notion MCP per leggere il DB Issues (query senza filtro, o con filtro per status attivi)
2. Usa Notion MCP per leggere il DB Release (ultime release + release future)
3. Prepara un sommario rapido:

```
Stato attuale DB Issues:
- Nuove: [N]
- In Analisi: [N]
- Da Iniziare: [N]
- In Corso: [N]
- Da Rilasciare: [N]
- Backlog: [N]
- Senza RICE completo: [N]

Prossime release: [lista con scope]
```

Procedi automaticamente allo Step 3.

---

### Step 3 — Chiedi cosa fare

**Chiedi**: "Cosa vuoi fare? Alcune opzioni:"

```
1. Preparare la riunione settimanale (genera agenda con anomalie e proposte)
2. Triage issue nuove (revisiona issue in stato "Nuova")
3. Pianificare release (assegnare issue a una release, verificare scope)
4. Health check backlog (issue stale, RICE mancante, anomalie)
5. Stato release [versione] (dettaglio su una release specifica)
6. Altro (descrivi cosa ti serve)
```

L'utente sceglie. La skill guida interattivamente in base alla scelta.

---

### Step 4 — Esecuzione guidata

In base alla scelta dell'utente, la skill:

#### Opzione 1: Preparare la riunione

1. Genera l'agenda seguendo `flusso-riunione.md`:
   - Issue in corso con eventuali anomalie (bloccate da troppo tempo, senza assegnazione)
   - PR aperte da revieware
   - Scope prossima release
   - Top 5 backlog per RICE score
   - Issue senza RICE da stimare
2. Mostra l'agenda e chiedi: *"Vuoi modificare qualcosa o la usiamo cosi'?"*

#### Opzione 2: Triage issue nuove

1. Mostra le issue in stato "Nuova", una alla volta
2. Per ciascuna proponi: *"Suggerisco [stato]: [motivazione]. Va bene?"*
   - Se necessita RICE, proponi i valori con motivazione
3. Dopo conferma, aggiorna su Notion

#### Opzione 3: Pianificare release

1. Mostra le issue "Da Rilasciare" e "In Corso" quasi completate
2. Proponi scope release: *"Per la [versione], suggerisco queste issue: [lista]. Confermi?"*
3. Dopo conferma, assegna le issue alla release su Notion

#### Opzione 4: Health check backlog

1. Analizza il backlog e segnala:
   - Issue senza RICE completo (con suggerimento valori)
   - Issue "In Corso" da piu' di 2 settimane senza aggiornamenti
   - Issue "Da Iniziare" non assegnate
   - Issue "Backlog" con RICE alto (candidati a promozione)
   - Filoni senza owner
2. Mostra il report e chiedi: *"Vuoi agire su qualcuna di queste?"*

#### Opzione 5: Stato release

1. Mostra dettaglio della release richiesta: issue associate, stato, assegnazione
2. Evidenzia rischi (issue bloccate, RICE non compilato)

#### Opzione 6: Altro

Ascolta la richiesta e guida in modo flessibile, sempre con conferma prima di ogni scrittura.

---

### Step 5 — Conferma scritture

**Prima di ogni scrittura su Notion**, mostra un riepilogo:

```
Modifiche da applicare su Notion:
- [Issue X]: Status da "Nuova" a "Da Iniziare"
- [Issue Y]: RICE aggiornato (Reach: 8, Impatto: 2, Effort: 16, Confidence: 0.8)
- [Issue Z]: Assegnata a Release 5.7.2

Procedo?
```

Solo dopo conferma esplicita ("si'", "ok", "procedi"), esegui le scritture.

---

### Step 6 — Riepilogo e prossime azioni

Dopo le scritture, mostra:

```
Completato:
- [N] issue aggiornate
- [lista modifiche applicate]

Suggerimenti per dopo:
- [eventuali azioni rimandate o da fare offline]
```

**Chiedi**: *"Vuoi fare altro o chiudiamo?"*

Se l'utente vuole continuare, torna allo Step 3.

---

## Evoluzione futura (non implementare ora)

- Modalita' specializzate con flow dedicati e meno domande
- Automazioni (reminder settimanale pre-riunione)
- Metriche (cycle time, throughput, lead time per filone)
- Integrazione bidirezionale GitHub (leggere stato PR, associare automaticamente)
- Report periodico per stakeholder

## Checklist qualita'

Prima di ogni scrittura su Notion, verifica mentalmente:

- [ ] L'utente ha confermato esplicitamente ogni modifica
- [ ] Gli stati rispettano il lifecycle definito in `processo-issue.md`
- [ ] I valori RICE sono coerenti con la guida in `processo-issue.md`
- [ ] Le assegnazioni release hanno senso (non assegnare a release passate)
