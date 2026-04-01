---
tags:
  - "#progetto:laif-issue"
  - "#fase:dev"
aggiornato: "2026-03-18"
---

# Specifiche Dashboard Notion — Stack Interno

## Pagine da gestire

| Pagina | Audience | Scopo |
|--------|----------|-------|
| **Dashboard Issues** | Team stack interno | Operativa: gestione quotidiana e riunioni |
| **Stack Interno — Overview** | Colleghi LAIF | Informativa: stato release, roadmap, come segnalare |

---

## 1. Dashboard Issues (riorganizzazione)

**ID pagina**: `2f490ad6-ee48-8003-9408-ca0925e1cf8b`

### Layout proposto

```
┌─────────────────────────────────────────────────────┐
│ Callout (blu):                                      │
│   [Release DB] [Issues DOC & FAQs]                  │
│   [Flusso Riunione] [Processo Issue]                │
│   [-> Stack Interno — Overview]                     │
└─────────────────────────────────────────────────────┘

# In Corso
  → vista inline "In Corso" del DB Issues
    Filtro: Status = "In corso"
    Colonne: ID, Titolo, Status, Assegnato a, Stack, Tipo, Tag

# Prossime Release                              ← NUOVA
  → vista inline "Prossime Release" del DB Issues
    (vedi sezione Viste)

# Roadmap
  → vista inline "Timeline Roadmap" del DB Issues
    (gia' esistente, da promuovere in posizione visibile)

# PR Template
  → vista inline PR laif-template (esistente, invariata)

# PR laif-ds
  → vista inline PR laif-ds (esistente, invariata)
```

### Cosa rimuovere

Il contenuto non strutturato dal fondo della pagina attuale:
- **Sezione "Test + Lint"** (stato dell'arte, migliorie, obiettivo, linting, requisiti) -> spostare nel corpo della pagina **ISS-130** (Test improvements, ID: `30c90ad6-ee48-801a-96bd-c58a9c035ef4`)
- **Sezione "Test"** (BE unit/integration, FE unit, E2E) -> spostare in ISS-130
- **Lista numerata roadmap** (LAIF Agent, Upstream, Scalabilita', Logger, Date, Media, Monitoring, Sicurezza, Dev Experience) -> eliminare (tutti gia' coperti da issue Roadmap esistenti)
- **6 blocchi vuoti** -> eliminare

### Callout aggiornato

Il callout attuale ha Release DB e Issues DOC & FAQs. Aggiungere:
- Link a "Flusso Riunione" (pagina `32790ad6-ee48-8045-8173-e95c180e9dd8`)
- Link/menzione "Processo Issue" (riferimento a processo-issue.md in KB, o pagina Notion se si decide di duplicarlo)
- Link a "Stack Interno — Overview" (nuova pagina per colleghi)

---

## 2. Stack Interno — Overview (nuova pagina)

Pagina separata, semplificata, per i colleghi LAIF che non fanno parte del team stack interno.

### Layout

```
┌─────────────────────────────────────────────────────┐
│ Callout:                                            │
│   Questa pagina mostra lo stato dello stack LAIF.   │
│   Per il team operativo: [-> Dashboard Issues]      │
└─────────────────────────────────────────────────────┘

# Prossime Release
  → vista "Prossime Release" del DB Issues
    (stessa vista della Dashboard, o vista semplificata)

# Roadmap
  → vista "Timeline Roadmap" del DB Issues

# Come segnalare un problema o una richiesta
  Testo breve:
  "Se hai trovato un bug o vuoi proporre un miglioramento
   allo stack interno, crea una issue nel DB Issues."
  [Link a Issues DOC & FAQs]
  [Bottone: Crea Issue]
```

### Note

- Nessun dettaglio operativo (PR, backlog, RICE)
- Solo viste ad alto livello
- Il bottone "Crea Issue" punta al DB Issues con template pre-compilato (se Notion lo supporta)

---

## 3. Viste da creare

### Vista "Prossime Release"

| Proprieta' | Valore |
|------------|--------|
| **Sorgente** | DB Issues (`21e90ad6-ee48-80ae-b0b3-000b7ba6ca13`) |
| **Tipo** | Table |
| **Filtro** | Status IN ["Da iniziare", "In corso", "Da rilasciare"] |
| **Gruppo** | Release (ASC) |
| **Colonne** | ID, Titolo, Status, Assegnato a, Stack, Tipo |
| **Ordine** | Release ASC, Status DESC |

### Vista "Roadmap Overview"

| Proprieta' | Valore |
|------------|--------|
| **Sorgente** | DB Issues (`21e90ad6-ee48-80ae-b0b3-000b7ba6ca13`) |
| **Tipo** | Board |
| **Filtro** | Tipo = "Roadmap" |
| **Gruppo** | Tag (Filone) |
| **Card** | Titolo, Status, Assegnato a |

---

## 4. Pagina "Flusso Riunione"

**ID pagina**: `32790ad6-ee48-8045-8173-e95c180e9dd8`

Attualmente vuota. Popolare con il contenuto di `projects/laif-issue/flusso-riunione.md`.

---

## 5. Pagina "Test Issues"

**ID pagina**: `31f90ad6-ee48-8086-b404-db2a85e4ec03`

Spostare qui il contenuto strutturato dalla sezione "Test + Lint" rimossa dalla Dashboard:
- Stato dell'arte test e lint
- Migliorie proposte (docker compose, E2E non deterministici, pre-commit, unit test FE, coverage)
- Requisiti linting (configurazione, livelli, trigger)
- Struttura test (BE unit/integration, FE unit, E2E)

Organizzare come proposte per-tema con checkbox per tracciamento.
