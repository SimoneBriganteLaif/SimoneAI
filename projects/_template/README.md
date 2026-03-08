---
progetto: "[NOME PROGETTO]"
cliente: "[NOME CLIENTE]"
industria: "[SETTORE]"
stato: "presales | in-sviluppo | completato | manutenzione"
data-inizio: "YYYY-MM-DD"
data-fine: ""
stack: []
tags:
  - "#progetto:[nome]"
  - "#industria:[settore]"
  - "#fase:presales"
---

# [Nome Progetto] — [Nome Cliente]

## Contesto

<!-- Descrizione del cliente e del contesto di business in 3-5 righe.
     Chi sono? Cosa fanno? Qual è il problema che vogliono risolvere? -->

## Obiettivo del progetto

<!-- Cosa deve fare il sistema che stiamo costruendo?
     Evita tecnicismi, descrivi in termini di valore per il cliente. -->

## Persone chiave

| Nome | Ruolo (lato cliente) | Contatto | Note |
|------|---------------------|---------|------|
| | | | |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| | | |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Kick-off | | |
| Consegna mockup | | |
| Inizio sviluppo | | |
| Go-live | | |

## Link utili

- **Repository**: (link al repo)
- **Staging**:
- **Produzione**:
- **Documenti contrattuali**:

## Struttura cartella

```
[nome-progetto]/
├── README.md                  ← questo file
├── presales/
│   ├── note-meeting/          ← trascrizioni e note grezze dei meeting
│   ├── requisiti.md           ← requisiti estratti e validati
│   ├── allegato-tecnico.md    ← allegato contrattuale (max 3 pag, non tecnico)
│   └── requisiti-mockup.md    ← brief per mockup in Windsurf
├── development/
│   ├── architettura.md        ← decisioni architetturali
│   ├── decisioni-tecniche.md  ← log delle decisioni tecniche (ADR)
│   └── feature-log.md         ← feature completate con note
└── maintenance/
    └── note.md                ← note post go-live
```

## Note

<!-- Qualsiasi cosa utile che non rientra nelle categorie sopra -->
