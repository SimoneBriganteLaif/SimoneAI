# LAIF — Overview Aziendale

#industria:software #fase:contesto

## Chi è LAIF

LAIF è un'azienda di sviluppo software con circa **20 sviluppatori** organizzati in **3 team**.

Sviluppa **web application per PMI** — applicazioni ad uso interno con pochi utenti (non consumer-facing, non ad alto traffico).

---

## Team di Simone

| Membro | Ruolo |
|--------|-------|
| Simone | Team Lead |
| Luca | Sviluppatore |
| Carlo | Sviluppatore |
| Daniele | Sviluppatore |
| Tancredi | Sviluppatore |
| Federico | Sviluppatore |

---

## Modello di lavoro

- **Ogni progetto** parte come fork di `laif-template` (vedi `knowledge/azienda/stack.md`)
- **Due ambienti** per cliente: dev e prod (account AWS separati)
- **Design system condiviso** (`@laif/ds`): tutti i progetti usano gli stessi componenti UI
- **Infrastruttura standardizzata** via CDK (vedi `knowledge/azienda/infrastruttura.md`)

---

## Divisione strumenti AI

| Strumento | Cosa fa |
|-----------|---------|
| **Claude Code** | Gestione KB, review codice, esecuzione test, aggiornamento KB post-sviluppo |
| **Windsurf** | Scrittura codice, implementazione feature, debug, refactoring |

Claude Code opera con parsimonia (costi). Windsurf gestisce lo sviluppo intensivo.

---

## Repository core

Vedi `core/README.md` per l'indice completo delle repo con link e descrizioni.

| Repo | Scopo |
|------|-------|
| `laif-template` | Base per tutti i progetti (fork) |
| `ds` | Design System condiviso (pacchetto npm `@laif/ds`) |
| `laif-cdk` | Infrastruttura AWS via CDK |
