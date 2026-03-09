---
nome: "Setup Progetto Dev"
descrizione: >
  Verifica e prepara l'ambiente di sviluppo locale per un progetto LAIF.
  Controlla Docker, servizi, connettività, autenticazione e permessi.
  Da usare a inizio sessione di sviluppo o dopo un onboarding.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/architettura.md
  - projects/[nome]/stato-progetto.md
  - knowledge/azienda/stack.md
  - .claude/projects/*/memory/MEMORY.md
scrive:
  - (nessun file — skill di verifica e diagnosi)
aggiornato: "2026-03-09"
---

# Skill: Setup Progetto Dev

## Obiettivo

Verificare che l'ambiente di sviluppo locale sia operativo per un progetto LAIF specifico. Al termine, tutti i servizi devono essere raggiungibili e l'autenticazione funzionante.

---

## Perimetro

**Fa**: verifica infrastruttura Docker, connettività servizi, autenticazione API, permessi utente, stato migrazioni DB.

**NON fa**: non installa dipendenze da zero, non configura infrastruttura cloud, non crea account.

**Rimandi**: per la creazione del progetto nella KB usa `skills/presales/init-project/`.

---

## Quando usarla

- Inizio di una sessione di sviluppo su un progetto
- Dopo un cambio di branch significativo
- Dopo un onboarding su un nuovo progetto
- Quando qualcosa "non funziona" senza errore chiaro

---

## Prerequisiti

- [ ] Progetto presente in `projects/[nome]/`
- [ ] Repository clonata localmente
- [ ] Docker Desktop attivo

---

## Loop conversazionale

### Domanda 1 — Progetto

> Su quale progetto vuoi lavorare?

(Leggi `projects/` per elencare i progetti disponibili)

### Domanda 2 — Servizi attesi

> Confermo i servizi da verificare: [lista da architettura.md]. Corretto?

---

## Processo di verifica

### Step 1 — Consulta la KB

1. Leggi `projects/[nome]/architettura.md` per capire i servizi coinvolti
2. Leggi `MEMORY.md` per credenziali, porte, comandi salvati
3. Leggi `knowledge/azienda/stack.md` per convenzioni generali

### Step 2 — Verifica Docker

1. Controlla che Docker sia attivo: `docker info`
2. Verifica i container del progetto: `docker compose ps` (dalla root del progetto)
3. Se i container non sono attivi: `just run default` (o il comando specifico da MEMORY.md)
4. Attendi avvio e verifica log: `docker compose logs --tail=20`

### Step 3 — Verifica connettività servizi

Per ogni servizio (backend, DB, frontend):

1. **Backend API**: `curl -s http://localhost:[port]/docs` → atteso 200
2. **Database**: verifica connessione via MCP PostgreSQL o `just migrate upgrade`
3. **Frontend**: `curl -s -o /dev/null -w "%{http_code}" http://localhost:[port]/` → atteso 200

### Step 4 — Verifica autenticazione

1. Login con credenziali standard: `POST /auth/login` con le credenziali da MEMORY.md
2. Verifica JWT valido
3. Testa un endpoint protetto con il token

### Step 5 — Verifica migrazioni DB

1. Controlla stato migrazioni: tabelle attese presenti nello schema corretto
2. Se necessario: `just migrate upgrade`

### Step 6 — Riepilogo

Riporta lo stato di ogni check:

| Check | Stato | Note |
|-------|-------|------|
| Docker attivo | ... | ... |
| Backend raggiungibile | ... | ... |
| DB raggiungibile | ... | ... |
| Frontend raggiungibile | ... | ... |
| Autenticazione | ... | ... |
| Migrazioni | ... | ... |

---

## Output in chat

```
Setup completato per [progetto]:
- Backend: [url] [status]
- Frontend: [url] [status]
- DB: [host:port] [status]
- Auth: [ok/errore]
- Migrazioni: [ok/da applicare]

[Eventuali problemi riscontrati e suggerimenti]
```
