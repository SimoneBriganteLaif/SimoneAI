---
progetto: "bonfiglioli-consulting"
cliente: "Bonfiglioli Consulting"
industria: "consulenza-direzionale"
stato: "presales"
data-inizio: "2026-04-10"
data-fine: ""
stack: ["python", "fastapi", "react", "postgresql", "aws"]
tags:
  - "#progetto:bonfiglioli-consulting"
  - "#industria:consulenza"
  - "#fase:presales"
---

# Piattaforma di Pianificazione Risorse — Bonfiglioli Consulting

## Contesto

Bonfiglioli Consulting è una società di consulenza direzionale specializzata in Operations Excellence, con sede a Lecco. Il team di consulenti (~decine di risorse) è distribuito sul territorio nazionale e opera presso le sedi dei clienti, gestendo contemporaneamente numerose commesse attive articolate in task, organizzate in 4 service line.

Oggi la pianificazione avviene su **Orchestra** (sistema custom mantenuto da un unico sviluppatore esterno — single point of failure), integrato con **Business Central** (ERP) e **Power BI** (reporting su DWH). Non esiste capacità di simulazione what-if, l'anagrafica risorse è su Excel, e non c'è incrocio domanda/offerta competenze.

## Obiettivo del progetto

Piattaforma web SaaS (Opzione 2 — affiancamento a Orchestra) con 5 moduli:
1. **Progetti** — Vista consolidata commesse (ERP) + opportunità CRM (>60%)
2. **Analytics** — Dashboard TAKT, scostamenti, trend, vista costi riservata alla direzione
3. **Capacity & What-If** — Simulazione scenari, proiezione 12 mesi, skills gap analysis
4. **Anagrafiche** — Risorse, competenze (matrice 2 livelli, scala 1-5), storico modifiche
5. **Pianificazione (Run Allocazione)** — Suggerimento allocazione automatica su capacità residua

Integrazione in **sola lettura** con DWH del cliente (SQL Server via Tailscale VPN). Nessuna scrittura verso sistemi esistenti.

## Persone chiave

| Nome | Ruolo (lato cliente) | Note |
|------|---------------------|------|
| Antonio Scagliuso | Referente di progetto | Interlocutore principale, validazione requisiti |
| Umberto / Roberto | Direzione / Decisori | Vista costi riservata, approvazione strategica |
| Andrea (IT) | Referente tecnico | Accesso DWH, Tailscale VPN, account SQL |
| Marica | Referente CRM | Codifica competenze richieste per opportunità |
| Georgia | Referente NAV | Integrazione BC, tabella trascodifica |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| Andrea Mordenti | PM / Referente commerciale | |
| Da assegnare | UX/UI Designer | |
| Da assegnare | Backend Developer | |
| Da assegnare | Frontend Developer | |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Call pre-kickoff | 2026-04-10 | In corso |
| Kick-off in presenza (Lecco) | ~settimana prossima | Da confermare |
| M1: Requisiti validati, design approvato | Fine Mese 1 | |
| M2: Pipeline + Progetti + Anagrafiche in staging | Fine Mese 2 | |
| M3: Tutti i moduli in staging, demo completa | Fine Mese 3 | |
| M4: UAT ok, rilascio produzione, onboarding | Fine Mese 4 | |
| Target completamento | Estate 2026 | |

## Budget

| Voce | Importo |
|------|---------|
| Setup (una tantum) | 25.000 EUR |
| Canone annuale | 5.000 EUR/anno |
| Costi cloud stimati | ~2.500 EUR/anno (inclusi nel canone) |

## Ecosistema cliente

- **Business Central (NAV)** — ERP: commesse, task, fatturazione
- **Orchestra** — Pianificazione settimanale/mensile, agenda (mezza giornata atomica). Sync con BC ogni 15 min
- **CRM** — Offerte e opportunità. Dati spesso incompleti
- **Rydoo** — Note spese, km. Sync con BC ogni notte
- **Power BI + DWH** — Reportistica, DWH Microsoft cloud. Refresh ogni 2h
- **Sistema paghe Raidou** — Dati stipendi/costi nel DWH

## Link utili

- **Lead Notion**: [Bonfiglioli Consulting - Pianificazione carico team](https://www.notion.so/laifgroup/Bonfiglioli-Consulting-Pianificazione-carico-team-2bc90ad6ee4880518643f90a387d007f)
- **Project Card**: [Project Card Notion](https://www.notion.so/laifgroup/Project-Card-Bonfiglioli-Consulting-Piattaforma-di-Pianificazione-Risorse-63346b35cb9e4c8fa7b61654b0ec0ce3)
- **Prototipo**: [bonfiglioli-consulting.laifgroup.com](http://bonfiglioli-consulting.laifgroup.com)
- **Repository**: Da creare
- **Staging**: Da configurare
- **Produzione**: Da configurare

## Struttura cartella

```
bonfiglioli-consulting/
├── README.md              <- questo file
├── meeting/               <- note meeting
├── requisiti.md           <- requisiti estratti e validati
├── architettura.md        <- architettura del sistema
├── decisioni.md           <- decisioni tecniche (ADR)
├── feature-log.md         <- feature completate con note
├── stato-progetto.md      <- stato attuale, blocchi e prossimi passi
├── allegato-tecnico.md    <- allegato contrattuale
├── mockup-brief.md        <- brief per mockup
└── windsurf-briefs/       <- brief per Windsurf
```
