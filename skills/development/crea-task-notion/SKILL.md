---
nome: "Crea Task Notion"
descrizione: >
  Genera task Notion strutturati per un progetto, usando KB come contesto di fondo e pagine Notion ad-hoc come input primario.
  Raggruppa i task sotto Feature esistenti o nuove (DB separato).
  Tutto interattivo in chat prima di creare qualsiasi cosa su Notion.
  Non è una skill di planning generale: si concentra sulla creazione operativa di task nel sistema Notion.
fase: development
versione: "0.1"
stato: beta
legge:
  - projects/[nome]/README.md
  - projects/[nome]/requisiti.md
  - projects/[nome]/stato-progetto.md
  - projects/[nome]/feature-log.md
  - Notion "Progetti" (via MCP, ricerca per nome progetto)
  - Notion "Note" (via MCP, ricerca per nome progetto)
  - Notion "Riunioni Private" (via MCP, ricerca per nome progetto)
  - Notion Feature DB: e9dcbcfeac9b43679c1cd58c07a989a2 (via MCP)
scrive:
  - Notion Task DB: a4394cc4dae34fe082803ea75e3fb164 (via MCP)
  - Notion Feature DB: e9dcbcfeac9b43679c1cd58c07a989a2 (via MCP, solo se nuove Feature)
aggiornato: "2026-03-12"
---

# Skill: Crea Task Notion

> **Stato beta**: all'inizio di ogni esecuzione avvisa l'utente che la skill è in beta. Ad ogni step chiedi se il processo ha senso o se va modificato.

## Obiettivo

Genera task Notion strutturati a partire dal contesto del progetto (KB + pagine Notion selezionate dall'utente). Raggruppa i task sotto **Feature** (entità di primo livello nel DB Notion dedicato). Nulla viene creato su Notion finché l'utente non conferma esplicitamente.

## Perimetro

**Fa:**
- Legge KB del progetto (README, requisiti, stato, feature-log)
- Cerca e legge pagine Notion rilevanti per il progetto
- Propone raggruppamento task per Feature (esistenti o nuove)
- Mostra bozza completa dei task in chat prima di creare
- Crea Feature e Task su Notion solo dopo conferma

**Non fa:**
- Non pianifica feature (per quello: `feature-workflow`)
- Non scrive su file KB (solo task su Notion)
- Non valuta la qualità tecnica dei task (per quello: `feature-review`)

## Quando usarla / Trigger

- L'utente vuole popolare il Notion con task per un progetto
- Dopo un meeting, un brainstorming, o una revisione di requisiti
- Prima di uno sprint o di una sessione di sviluppo

## Prerequisiti

- Notion MCP abilitato (plugin `Notion@claude-plugins-official`)
- Il progetto deve avere almeno `README.md` o `stato-progetto.md` in `projects/[nome]/`

---

## Loop conversazionale

> **Regola fondamentale**: un step alla volta. Non anticipare. Non creare nulla su Notion prima dello Step 7.

---

### Step 1 — Q: Progetto

**Chiedi**: "Per quale progetto stai creando task?"

**Azione automatica dopo la risposta:**
1. Leggi `projects/[nome]/README.md`, `requisiti.md`, `stato-progetto.md`, `feature-log.md`
2. Mostra un brief riepilogo (max 5 righe):
   ```
   Contesto [NomeProgetto]:
   - Stato: [fase attuale da stato-progetto.md]
   - Prossimi passi noti: [elenco breve]
   - RF chiave: [2-3 requisiti più rilevanti da requisiti.md]
   - Completato di recente: [ultimo entry feature-log.md]
   ```
3. Procedi automaticamente allo Step 2

---

### Step 2 — Fetch proattivo Notion (automatico, nessuna domanda)

**Azione automatica** (non chiedere, fai direttamente):
1. Usa il MCP Notion per cercare pagine contenenti il nome del progetto nei 3 contesti:
   - "Progetti"
   - "Note"
   - "Riunioni Private"
2. Mostra le pagine trovate:
   ```
   Pagine Notion trovate per [NomeProgetto]:
   [1] Titolo pagina (Riunioni Private, 2026-03-10)
   [2] Titolo pagina (Progetti)
   [3] Titolo pagina (Note, 2026-03-08)
   ...
   ```
   Se nessuna trovata: "Nessuna pagina Notion trovata. Procedo con solo KB."

**Chiedi**: "Quali includere come contesto? (numeri separati da virgola, 'tutte', 'nessuna')"

**Azione dopo la risposta**: Leggi le pagine selezionate via MCP.

---

### Step 3 — Q: Focus

**Chiedi**: "Su cosa vuoi concentrarti? (es. prossimo sprint, backlog feature X, blocchi attuali, onboarding utenti, ...)"

Risposta libera. Usala per filtrare il contesto KB e Notion nelle fasi successive.

---

### Step 4 — Feature: cerca esistenti + propone raggruppamento

**Azione automatica**:
1. Leggi il Feature DB Notion (`e9dcbcfeac9b43679c1cd58c07a989a2`) e filtra per progetto
2. Analizza KB + pagine Notion selezionate tenendo conto del focus dichiarato
3. Proponi una logica di raggruppamento per modulo/area/tema

**Mostra proposta**:
```
Raggruppamento proposto:

- Feature A "[nome Feature esistente]" (esistente, ID: xxx)
  → task candidati: descrizione breve T1, T2, T3

- Feature B "[nome proposto]" (nuova)
  → task candidati: descrizione breve T4, T5
```

**Chiedi**: "Va bene questo raggruppamento? (modifica la struttura Feature o scrivi 'ok')"

Loop finché l'utente non approva.

---

### Step 5 — Proposta task in chat

**Mostra proposta completa** (tutto interattivo, nulla creato ancora):
```
Task proposti (N totali):

━━━ Feature: [nome Feature A] (esistente) ━━━
  1. [Titolo — verbo + oggetto, es. "Implementare validazione email signup"]
     Priorità: Alta | Stima: M
     Note: [contesto breve, 1 riga max]

  2. [Titolo]
     Priorità: Media | Stima: S
     Note: ...

━━━ Feature: [nome Feature B] (nuova) ━━━
  3. [Titolo]
     Priorità: Alta | Stima: L
     Note: ...
```

**Chiedi**: "Modifiche? Esempi: '3 rimuovi', '1 titolo: Nuovo titolo', '1 priorità: Bassa', 'aggiungi a Feature A: Titolo task', 'ok'"

Loop di editing finché l'utente non scrive 'ok'.

**Logica di priorità per proporre task:**
- `stato-progetto.md` → priorità massima (prossimi passi, blocchi aperti)
- `requisiti.md` → validazione che i task linkino a un RF
- `feature-log.md` → evita duplicati (non proporre task per feature già completate)
- `README.md` / pagine Notion → nomenclatura coerente con stack e terminologia del progetto

**Logica titoli task**: sempre nella forma `Verbo + oggetto` (es. "Aggiungere filtro data", "Correggere bug timeout", "Migrare schema tabella utenti"). Mai titoli vaghi come "Bug fix" o "Miglioramenti".

---

### Step 6 — Conferma finale

**Mostra riepilogo pre-creazione:**
```
Riepilogo:
- Progetto: [nome]
- Feature nuove da creare: [N] → [lista nomi]
- Feature esistenti con task: [N] → [lista nomi]
- Task totali da creare: [N]

Creo tutto su Notion. Procedo?
```

Aspetta conferma esplicita ("sì", "procedi", "ok"). Se l'utente dice "no" o chiede modifiche, torna allo Step 5.

---

### Step 7 — Creazione + Riepilogo

**Esecuzione** (in ordine):
1. Crea le Feature nuove nel DB `e9dcbcfeac9b43679c1cd58c07a989a2`
2. Crea tutti i task nel Task DB `a4394cc4dae34fe082803ea75e3fb164`, con riferimento alla Feature
3. Gestisci errori: se una creazione fallisce, mostra l'errore e chiedi come procedere

**Mostra riepilogo finale:**
```
✓ COMPLETATO — Crea Task Notion

Progetto: [nome]
Feature create: [N] | Feature esistenti usate: [N]
Task creati: [N]

Task per Feature:
  [Feature A]: T1, T2, T3
  [Feature B]: T4, T5
```

---

## Checklist qualità

Prima di procedere con Step 7, verifica mentalmente:

- [ ] Nessun task duplica una feature già completata in `feature-log.md`
- [ ] Ogni task ha un titolo nella forma `Verbo + oggetto`
- [ ] Ogni task è assegnato a una Feature (mai task orfani)
- [ ] Le Feature nuove hanno nomi coerenti con la nomenclatura del progetto
- [ ] L'utente ha confermato esplicitamente la lista in Step 5 e la creazione in Step 6
