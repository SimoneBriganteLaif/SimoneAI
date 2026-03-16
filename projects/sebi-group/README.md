---
progetto: "sebi-group"
cliente: "Sebi Group"
industria: "Logistica / Spedizioni internazionali"
stato: "presales"
data-inizio: "2026-02-17"
data-fine: ""
stack: []
tags:
  - "#progetto:sebi-group"
  - "#industria:logistica"
  - "#fase:presales"
---

# Sebi Group — Gestione Email & Quotazioni AI-powered

## Contesto

Sebi Group è uno spedizioniere internazionale (51-200 dipendenti) che gestisce import/export di merci.
Il problema centrale: la gestione di offerte e comunicazioni è completamente manuale, dispersa tra mail,
gestionale e fogli Excel. Le mail si perdono, i preventivi non vengono tracciati, e non c'è supporto
decisionale per pricing e priorità.

## Obiettivo del progetto

Sviluppare una soluzione AI-powered che:
1. **Centralizzi e categorizzi automaticamente** le email (10-15 caselle condivise)
2. **Tracci il ciclo completo dell'offerta**: richiesta cliente → RDO agenti → preventivi → pricing → risposta
3. **Automatizzi** assegnazione mail, solleciti, risposte semi-automatiche, caricamento preventivi nel gestionale
4. **Fornisca dashboard/KPI** per il management (quotazioni, performance, margini, tempi di risposta)

Due fasi: Fase 1 operativa (categorizzazione, tracciamento, automazione), Fase 2 analytics/dashboard.

## Persone chiave

| Nome | Ruolo (lato cliente) | Contatto | Note |
|------|---------------------|---------|------|
| Michele Bonicalzi | Referente principale | michele.bonicalzi@sebigroup.com | Ha chiesto feedback su fattibilità |
| Stefano | Operativo | | Presente alle sessioni on-site |
| Gabriella | Operativo | | Presente alle sessioni on-site |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| Simone | Lead progetto, raccolta requisiti | |
| Federico | Raccolta requisiti, design soluzione | Presentato al kickoff |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Kick-off (call) | 2026-02-17 | completato |
| Raccolta requisiti on-site | 2026-03-16 | pianificato |
| Meeting fornitore gestionale | TBD (dopo on-site) | da pianificare |
| Consegna stima + mockup | TBD | da pianificare |

## Link utili

- **Notion Lead**: https://www.notion.so/20d90ad6ee4881cea697f7631d2c9490
- **Notion Kickoff**: https://www.notion.so/30a90ad6ee48803dae48fccafc85d890
- **Codice progetto**: 2026012
- **Fonte lead**: LandingPage

## Struttura cartella

```
sebi-group/
├── README.md              ← questo file
├── meeting/               ← note meeting (una per file)
├── requisiti.md           ← requisiti estratti e validati
├── architettura.md        ← architettura del sistema
├── decisioni.md           ← decisioni tecniche (ADR)
├── feature-log.md         ← feature completate con note
├── stato-progetto.md      ← stato attuale, blocchi e prossimi passi
├── allegato-tecnico.md    ← allegato contrattuale (max 3 pag)
├── mockup-brief.md        ← brief per mockup Windsurf
└── manutenzione.md        ← note post go-live
```

## Note

- Il fornitore del gestionale è disponibile per integrazione via API/passaggio parametri
- La software house attuale è molto lenta — il cliente vuole velocità
- Import ed Export hanno dinamiche molto diverse: Export è più destrutturato e con più volume mail
- Il 90% delle quotazioni subisce revisioni per cambi dimensioni/pesi
- Solo 3-4 preventivi su 10 vengono effettivamente inseriti nel gestionale (mancanza tempo)
