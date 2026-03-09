---
progetto: "lamonea"
cliente: "Lamonea S.R.L. Unipersonale"
industria: "Healthcare / Medical Devices"
stato: "in-sviluppo"
data-inizio: "2026-02-20"
data-fine: ""
stack: [FastAPI, Next.js 16, PostgreSQL, Docker, AWS]
tags:
  - "#progetto:lamonea"
  - "#industria:healthcare"
  - "#fase:dev"
  - "#stack:fastapi"
  - "#stack:nextjs"
  - "#stack:postgresql"
---

# Lamonea — Lamonea S.R.L.

## Contesto

Lamonea S.R.L. Unipersonale (P.IVA 01201040423, Ancona) è un distributore di materiale medico-chirurgico composto da tre società: **Lamonea SRL** (importazione diretta, gare grandi, Amazon), **Lamonea Endosurgery** (clienti privati: cliniche, laboratori) e **Lamonea Medical** (gare d'appalto PA). Attualmente i processi sono molto artigianali (Excel, cartaceo, TeamSystem con interfaccia obsoleta) e le tre società operano come silos separati.

## Obiettivo del progetto

Realizzare una piattaforma gestionale cloud unica e **multisocietaria** che diventi il punto centrale di lavoro per commerciale/CRM, gare, ordini, magazzino, logistica e controllo. L'obiettivo immediato (Fase 1) è il **Catalogo Prodotti Digitale** e il **CRM** con gestione opportunità/gare, integrati con TeamSystem come sistema contabile di riferimento.

## Persone chiave

| Nome | Ruolo (lato cliente) | Note |
|------|---------------------|------|
| Mathias Lamonea | CEO | Supervisione generale, delega molto |
| Andrea Spilli | Responsabile acquisti/import | Preciso, esigente, crea nuovi prodotti a marchio Lamonea |
| Matteo Farinelli | Responsabile commerciale | Sponsor progetto, interfaccia con TeamSystem |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| Marco Vita | Ha portato il cliente | Amico del cliente |
| Simone Brigante | Team Leader | Requisiti, prototipi, modello dati |
| Luca | Fullstack Developer | Focus frontend |
| Daniele | Fullstack Developer | Data, flussi dati |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Kick-off interno | 2026-02-20 | completato |
| Kick-off con cliente | 2026-02-23 | completato |
| Mockup frontend | 2026-02-25 | completato |
| Requisiti Fase 1 | 2026-02-25 | completato |
| Fine sviluppo (stimata) | 2026-06 | — |

## Link utili

- **Repository**: [GitHub](https://github.com/laif-group/lamonea.git)
- **Repo locale**: `/Users/simonebrigante/LAIF/repo/lamonea/`
- **Notion**: [Progetto Lamonea](https://www.notion.so/30d90ad6ee4880ff823bf5f19f380679)
- **Documentazione locale**: `/Users/simonebrigante/LAIF/Progetti/Lamonea`
- **Staging**: —
- **Produzione**: —

## Struttura cartella

```
lamonea/
├── README.md              ← questo file
├── meeting/               ← note meeting (una per file)
├── requisiti.md           ← requisiti estratti e validati
├── architettura.md        ← architettura del sistema
├── decisioni.md           ← decisioni tecniche (ADR)
├── feature-log.md         ← feature completate con note
├── stato-progetto.md      ← stato attuale, blocchi e prossimi passi
├── allegato-tecnico.md    ← allegato contrattuale (max 3 pag)
├── mockup-brief.md        ← brief per mockup Windsurf
├── aws-config.yaml        ← configurazione risorse AWS
└── manutenzione.md        ← note post go-live
```

> La repository di codice vive in `/Users/simonebrigante/LAIF/repo/lamonea/`, separata dalla KB.

## Note

- Investimento concordato: 35.000€ + canone ricorrente annuale, 4 tranche fino a fine giugno
- Integrazione bidirezionale con TeamSystem (Lynfa Azienda) via Web Services JSON
- TeamSystem ha 3 ditte separate (49, 133, 212) — la piattaforma le unifica
- Solo CodiceWS 500001 (clienti/fornitori) attualmente configurato su TS; articoli, documenti, ordini, movimenti da configurare
- ~3.300 clienti, ~1.900 fornitori, ~12.400 articoli (di cui ~4.000-5.000 movimentati ultimi 3 anni)
- Documentazione API TeamSystem completa in `/Users/simonebrigante/LAIF/Progetti/Lamonea/CollectionTeamSystem/`
