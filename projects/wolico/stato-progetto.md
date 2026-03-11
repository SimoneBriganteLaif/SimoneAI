---
progetto: "wolico"
ultimo-aggiornamento: "2026-03-10"
tags:
  - "#progetto:wolico"
  - "#fase:dev"
---

# Stato Progetto — Wolico

> Punto di ingresso per riprendere lo sviluppo. Ultimo aggiornamento: 2026-03-10.

---

## Stato complessivo

Wolico è operativo in produzione con tutti i moduli core funzionanti. La piattaforma copre CRM, ticketing, HR, contabilità, operations e monitoring. Lo sviluppo futuro si concentra sull'aggiunta di nuovi moduli e sul miglioramento di quelli esistenti.

---

## Mappa moduli

| Modulo | Backend | Frontend | Stato | Note |
|--------|---------|----------|-------|------|
| CRM | Completo | Completo | Operativo | Leads, sales, partners, contacts, tranche |
| Ticketing | Completo | Completo | Operativo | Messaggi, allegati, aggiornamenti |
| HR / Employees | Completo | Completo | Operativo | Anagrafiche, contratti |
| Calendar | Completo | Completo | Operativo | Ferie, festivi, giorni lavorativi |
| Economics | Completo | Completo | Operativo | Cash flow, balance, marginalità, ricavi |
| Operations | Completo | Completo | Operativo | Cloud costs, staffing, outages, reporting |
| Administration | Completo | Completo | Operativo | Spese, recap mensili |
| Monitoring | Completo | Completo | Operativo | Errori BE/FE delle app |
| Changelog | Completo | Completo | Operativo | Audit log |
| Odoo | Completo | — | Operativo | Integrazione ERP (solo backend) |

---

## MCP Server

Attivo in `mcp-servers/wolico/` con 3 tool:
- `get_ferie_team` — assenze team per intervallo date
- `get_ferie_persona` — assenze per dipendente
- `get_calendario_settimana` — vista settimanale assenze

---

## Blocchi critici

Nessun blocco critico attivo. La piattaforma è stabile e operativa.

---

## Prossimi passi suggeriti

### Backlog

- Pianificazione nuovi moduli (da definire con il team)
- Estensione MCP Server con tool aggiuntivi (ticketing, reporting)
- Documentazione moduli esistenti nella KB man mano che si lavora su Wolico

---

## File di riferimento

| Documento | Contenuto |
|-----------|-----------|
| [README.md](README.md) | Overview progetto, moduli, link |
| [architettura.md](architettura.md) | Stack, diagrammi, componenti |
| [decisioni.md](decisioni.md) | Decisioni tecniche (ADR) |
| [requisiti.md](requisiti.md) | Requisiti per nuovi moduli |
| [feature-log.md](feature-log.md) | Feature implementate |
| [manutenzione.md](manutenzione.md) | Accessi e procedure operative |

**Repository codice**: `/Users/simonebrigante/LAIF/repo/wolico/`
