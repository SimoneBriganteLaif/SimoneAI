---
nome: "Brainstorming Post-Sviluppo"
descrizione: >
  Alla fine di una sessione di sviluppo, analizza il lavoro svolto per
  identificare pattern riutilizzabili, skill da creare, workflow da
  migliorare e idee da registrare. Alimenta il ciclo di miglioramento
  continuo di SimoneAI.
fase: development
versione: "1.0"
stato: beta
legge:
  - (contesto della sessione corrente)
  - patterns/ (per evitare duplicati)
  - skills/ (per evitare duplicati)
  - IDEAS.md (per evitare duplicati)
scrive:
  - patterns/[nuovo].md (se individuato)
  - skills/[fase]/[nuova]/SKILL.md (se individuata)
  - IDEAS.md (nuove idee)
  - CHANGELOG-contenuti.md
aggiornato: "2026-03-09"
---

# Skill: Brainstorming Post-Sviluppo

## Obiettivo

Trasformare l'esperienza della sessione di sviluppo appena conclusa in asset riutilizzabili per SimoneAI. Ogni sessione produce conoscenza — questa skill la cattura sistematicamente.

---

## Perimetro

**Fa**: analizza la sessione corrente ed estrae pattern, skill, workflow, idee.

**NON fa**: non implementa le skill/workflow identificati (a meno che l'utente non lo chieda). Li registra e propone.

**Rimandi**:
- Per estrarre pattern da un progetto completo → `skills/development/estrazione-pattern/`
- Per registrare idee → `skills/meta/gestione-kb/` modalità 2

---

## Quando usarla

**Sempre**, alla fine di ogni sessione di sviluppo significativa. Idealmente diventa un'abitudine automatica.

Trigger:
- L'utente dice "abbiamo finito" o simili
- Si è completato un obiettivo di sviluppo
- Sono stati risolti bug non banali
- Si sono fatte scelte architetturali

---

## Loop conversazionale

### Step 1 — Recap del lavoro

Presenta un riepilogo strutturato della sessione:

> **Lavoro svolto in questa sessione:**
> 1. [cosa è stato fatto]
> 2. [cosa è stato fatto]
> ...
>
> **Bug risolti:** [lista]
> **Decisioni prese:** [lista]
> **Errori commessi e corretti:** [lista]

### Step 2 — Identificazione asset

Analizza il recap e proponi asset suddivisi in categorie:

#### Pattern tecnici (→ `patterns/`)
Soluzioni a problemi che si ripresenteranno. Criteri:
- Il problema non è specifico di un singolo progetto
- La soluzione è generalizzabile
- È un "gotcha" facile da dimenticare

#### Skill (→ `skills/`)
Processi ripetibili che seguono un loop conversazionale. Criteri:
- Il processo ha più step
- Richiede input dall'utente
- Si ripeterà in futuro su altri progetti

#### Workflow / Miglioramenti a skill esistenti
Modifiche a skill o workflow già esistenti. Criteri:
- Una skill esistente non copre un caso emerso
- Un processo manuale potrebbe essere automatizzato
- Un gate di qualità mancante ha causato un errore

#### Idee (→ `IDEAS.md`)
Tutto ciò che non rientra nelle categorie sopra ma vale la pena ricordare.

### Step 3 — Validazione con l'utente

> Ho identificato questi asset dalla sessione:
>
> **Pattern**: [lista]
> **Skill**: [lista]
> **Workflow**: [lista]
> **Idee**: [lista]
>
> Quali vuoi che sviluppi ora? Quali segno in IDEAS.md?

### Step 4 — Esecuzione

Per ogni asset approvato:
- **Pattern**: crea il file in `patterns/` seguendo `_template.md`
- **Skill**: crea la cartella e `SKILL.md` in `skills/[fase]/`
- **Idee**: registra in `IDEAS.md` via `skills/meta/gestione-kb/` modalità 2
- **Workflow**: modifica la skill esistente o crea la nuova

### Step 5 — Aggiornamento KB

1. Aggiorna `CHANGELOG-contenuti.md` con gli asset creati
2. Aggiorna `.tags/index.md` se necessario
3. Aggiorna `patterns/README.md` se nuovi pattern

---

## Output in chat

```
Brainstorming completato:
- [N] pattern creati/aggiornati
- [N] skill create
- [N] idee registrate in IDEAS.md
- [N] miglioramenti a skill esistenti

Dettaglio: [lista dei file creati/modificati]
```

---

## Note

Questa skill migliora SimoneAI in modo incrementale. Ogni sessione di sviluppo diventa un'opportunità di apprendimento per il sistema. L'accumulo nel tempo crea un vantaggio competitivo significativo: meno errori ripetuti, più automazione, processi più raffinati.
