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

**Numeri chiave**: 400-700 email/giorno, ~20.000 quotazioni/anno (export), tasso conversione 18%, 30% fatturato potenziale perso per mancanza tempo/risorse.

## Obiettivo del progetto

Sviluppare una piattaforma AI-powered che:
1. **Centralizzi e categorizzi automaticamente** le email (10-15 caselle condivise M365)
2. **Tracci il ciclo completo dell'offerta**: richiesta cliente → RDO fornitori → preventivi → pricing → risposta
3. **Automatizzi** assegnazione mail, solleciti, risposte semi-automatiche, caricamento preventivi nel gestionale
4. **Fornisca dashboard/KPI** per il management (quotazioni, performance, margini, tempi di risposta)

Approccio graduale con man-in-the-loop. Il gestionale (Osma per import) non viene sostituito ma affiancato.

## Moduli identificati

| # | Modulo | Descrizione |
|---|--------|-------------|
| M1 | Email Intelligence | Connessione M365, classificatore AI, assegnazione automatica, inbox unificata |
| M2 | Gestione Offerte Export | Ciclo RDO→preventivi→quotazione, ID univoco, WebCargo, prepratiche |
| M3 | Gestione Offerte Import | Autocotazione, gestionale Osma, invio massivo, parsing risposte |
| M4 | Integrazione Gestionale | API bidirezionale Osma, anagrafiche, fido/credito, tariffari |
| M5 | Dashboard & Analytics | KPI operativi e management, conversioni, tempi, margini |
| M6 | Alerting Intelligente | Alert fido, mail non lavorati, solleciti, agenti non in network |

**Stima totale**: 93-142 giorni/uomo (dettaglio in `stima-modulare.md`)

## Persone chiave

| Nome | Ruolo (lato cliente) | Contatto | Note |
|------|---------------------|---------|------|
| Michele Bonicalzi | Referente principale | michele.bonicalzi@sebigroup.com | Decision maker |
| Stefano | Operativo export | | Presente on-site |
| Gabriella | Operativo import | | Presente on-site |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| Simone | Lead progetto, raccolta requisiti | |
| Federico | Raccolta requisiti, design soluzione | Presentato al kickoff |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Kick-off (call) | 2026-02-17 | completato |
| Raccolta requisiti on-site | 2026-03-16 | completato |
| Estrazione requisiti + stima modulare | 2026-03-17 | completato |
| Punto situazione con cliente | 2026-03-23 | pianificato |
| Meeting fornitore gestionale (Osma) | TBD (dopo punto situazione) | da pianificare |
| Consegna mockup | TBD | da pianificare |
| Presentazione proposta commerciale | TBD | da pianificare |

## Link utili

- **Notion Lead**: https://www.notion.so/20d90ad6ee4881cea697f7631d2c9490
- **Notion Kickoff**: https://www.notion.so/30a90ad6ee48803dae48fccafc85d890
- **Notion On-site**: https://www.notion.so/32590ad6ee4880b2b7f2e189f3b64029
- **Codice progetto**: 2026012
- **Fonte lead**: LandingPage
- **Repository codice**: `/Users/simonebrigante/LAIF/repo/sebi-group/`

## Struttura cartella

```
sebi-group/
├── README.md                  ← questo file
├── meeting/                   ← note meeting (una per file)
│   ├── 2025-12-18-primo-incontro.md
│   ├── 2026-02-17-kickoff.md
│   ├── 2026-03-16-prep-on-site.md
│   └── 2026-03-16-on-site.md
├── requisiti.md               ← requisiti estratti e validati (17 RF + 5 RNF)
├── allegato-tecnico.md        ← allegato contrattuale (max 3 pag)
├── stima-modulare.md          ← stima giorni/uomo per modulo
├── mockup-brief.md            ← brief per mockup Windsurf
├── architettura.md            ← architettura del sistema (TBD)
├── decisioni.md               ← decisioni tecniche (ADR)
├── feature-log.md             ← feature completate con note
├── stato-progetto.md          ← stato attuale, blocchi e prossimi passi
└── manutenzione.md            ← note post go-live
```

## Note

- Il fornitore del gestionale import (Osma) è disponibile per integrazione via API — ambiente test disponibile
- La software house attuale (gestionale) è molto lenta — il cliente vuole velocità
- Import ed Export hanno dinamiche molto diverse: Export è più destrutturato e con più volume mail
- Il 90% delle quotazioni subisce revisioni per cambi dimensioni/pesi
- Solo 3-4 preventivi su 10 vengono effettivamente inseriti nel gestionale
- Il cliente vuole approccio graduale con man-in-the-loop (NO automazioni senza supervisione umana)
- Target utenti: 35-38 anni, non tecnici
- WebCargo usato per export aereo — API disponibili, da verificare scope
