---
progetto: "laif-issue"
cliente: "LAIF (interno)"
industria: "internal-tooling"
stato: "in-sviluppo"
data-inizio: "2026-03-18"
data-fine: ""
stack: [notion, github]
tags:
  - "#progetto:laif-issue"
  - "#industria:operations-interne"
  - "#fase:dev"
---

# LAIF Issue — Gestione Issue Stack Interno

## Contesto

LAIF mantiene uno stack interno (template backend/frontend, design system, tooling) usato da tutti i progetti cliente. Un sottoinsieme del team ("team stack interno") si occupa dello sviluppo e della manutenzione di questo stack. Le issue vengono tracciate su Notion con un DB dedicato, ma manca un processo strutturato per gestirle efficacemente — sia nel day-to-day che durante le riunioni settimanali.

## Obiettivo del progetto

Creare un sistema strutturato per la gestione delle issue dello stack interno:
- **Dashboard Notion** con viste/filtri utili per diverse audience (team stack interno vs colleghi)
- **Processo chiaro** di gestione issue (offline e durante le call settimanali)
- **Skill interattive** in SimoneAI per assistere nella gestione issue via Notion MCP

## Team Stack Interno

Il team stack interno è un sottoinsieme degli sviluppatori LAIF che si occupa attivamente dello sviluppo e manutenzione dello stack. Gli "esterni" sono tutti gli altri colleghi LAIF che usano lo stack nei progetti cliente.

## Risorse Notion

| Risorsa | Tipo | ID |
|---------|------|----|
| Issues DB | Database | `21e90ad6-ee48-80ae-b0b3-000b7ba6ca13` |
| Release DB | Database | `32090ad6-ee48-80e0-9415-000b6984bd86` |
| Dashboard Issues | Pagina | `2f490ad6-ee48-8003-9408-ca0925e1cf8b` |
| Flusso Riunione | Pagina | `32790ad6-ee48-8045-8173-e95c180e9dd8` |
| Issues DOC & FAQs | Pagina | `2f890ad6-ee48-8072-b1e0-f1a19301736b` |
| Test Issues | Pagina | `31f90ad6-ee48-8086-b404-db2a85e4ec03` |
| GitHub PR DB | Database | `2f090ad6-ee48-806a-83a5-000b1b3b361f` |

## Struttura cartella

```
laif-issue/
├── README.md              <- questo file
├── processo-issue.md      <- ciclo di vita, RICE, release, regole
├── flusso-riunione.md     <- scaletta operativa riunione settimanale
├── dashboard-spec.md      <- specifiche riorganizzazione Dashboard Notion
├── stato-progetto.md      <- stato attuale e prossimi passi
└── decisioni.md           <- decisioni tecniche (ADR)
```

## Link utili

- **Dashboard Issues**: pagina Notion operativa del team
- **Issues DOC & FAQs**: documentazione lifecycle e FAQ per chi crea issue
- **Skill gestione-issue**: `skills/development/gestione-issue/SKILL.md`
