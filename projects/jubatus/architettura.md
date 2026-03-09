---
progetto: "jubatus"
data-creazione: "2026-03-08"
ultimo-aggiornamento: "2026-03-08"
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
  - "#fase:dev"
  - "#stack:fastapi"
  - "#stack:nextjs"
  - "#stack:aws"
---

# Architettura — [Nome Progetto]

> **Istruzioni**: questo documento descrive l'architettura del sistema.
> Aggiornarlo ogni volta che l'architettura cambia significativamente.
> Aggiornato dalla skill `skills/development/estrazione-decisioni.md`.

---

## Overview

[Descrizione in 3-5 righe dell'architettura generale. Chi legge deve capire la struttura senza leggere il resto.]

---

## Stack tecnologico

| Layer | Tecnologia | Versione | Motivo della scelta |
|-------|-----------|---------|-------------------|
| Frontend | | | |
| Backend | | | |
| Database | | | |
| Hosting | | | |
| CI/CD | | | |
| Auth | | | |

---

## Diagramma architetturale

```
[Diagramma testuale o link a diagramma esterno]

Esempio:
[Browser] → [CDN/Vercel] → [Next.js App]
                                ↓
                         [API Routes]
                                ↓
                    [PostgreSQL su Supabase]
```

---

## Componenti principali

### [Nome Componente]

**Responsabilità**: [cosa fa]
**Tecnologia**: [cosa usa]
**Interfacce**: [come comunica con altri componenti]
**Note**: [decisioni importanti, vincoli]

---

## Flussi principali

### Flusso: [Nome]

```
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]
```

---

## Dipendenze esterne

| Servizio | Scopo | Criticità | Alternativa se cade |
|---------|-------|----------|-------------------|
| | | Alta/Media/Bassa | |

---

## Considerazioni di sicurezza

- **Autenticazione**: [come]
- **Autorizzazione**: [come]
- **Dati sensibili**: [come gestiti]
- **Backup**: [strategia]

---

## Considerazioni di scalabilità

[Come regge la crescita? Dove sono i colli di bottiglia previsti?]

---

## Debito tecnico noto

| # | Descrizione | Impatto | Priorità |
|---|------------|--------|---------|
| 1 | | | |
