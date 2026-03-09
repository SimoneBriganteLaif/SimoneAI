---
progetto: "jubatus"
cliente: "Jubatus"
industria: "entertainment"
stato: "in-sviluppo"
data-inizio: "2026-01-23"
data-fine: ""
stack: [python, fastapi, nextjs, typescript, postgresql, docker, aws]
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
  - "#fase:dev"
  - "#stack:fastapi"
  - "#stack:nextjs"
  - "#stack:aws"
---

# Jubatus — Customer Care Platform

## Contesto

Jubatus è un'azienda nel settore entertainment/eventi musicali che offre servizi di foto e video ai partecipanti di concerti e festival. Gli utenti scansionano un QR code all'evento, caricano un selfie, e ricevono le foto in cui sono stati riconosciuti tramite face recognition. L'azienda è in forte crescita (obiettivo 4x fatturato 2026) con focus su festival ed eventi musicali (es. Rocky 1000, Monsterland).

## Obiettivo del progetto

Costruire una piattaforma interna di customer care per centralizzare la gestione delle segnalazioni clienti, attualmente gestite manualmente via email e fogli Excel. Il sistema deve raccogliere automaticamente i ticket da email, categorizzarli, integrarsi con il database esistente (MySQL/AWS RDS) per mostrare dati utente, e proporre risposte automatiche per i problemi più comuni (90% delle richieste sono semplici).

### Priorità di sviluppo

1. **Piattaforma interna di ticketing** — centralizzare segnalazioni email, categorizzazione automatica, integrazione DB
2. **Chatbot in web app** — gestione domande di primo livello, escalation a ticketing
3. **Dashboard migliorata per eventi/partner** — sostituzione Grafana con soluzione user-friendly

## Persone chiave

| Nome | Ruolo (lato cliente) | Contatto | Note |
|------|---------------------|---------|------|
| Jonathan | Tech Lead | | Referente tecnico principale, gestisce architettura |
| Marco | Tech/Management | | Co-referente tecnico |
| Logan | Supporto clienti | | Gestisce email customer care |
| Gionata | Supporto clienti | | Gestisce email customer care |
| Lorenza | Supporto clienti | | Gestisce email customer care |

## Team LAIF

| Nome | Ruolo | Note |
|------|-------|------|
| Simone | Infrastruttura cloud | Owner progetto |
| Federico | Frontend/Backend | Mockup e sviluppo applicativo |
| Lorenzo | Frontend/Backend | Sviluppo applicativo |

## Timeline

| Milestone | Data | Stato |
|-----------|------|-------|
| Kick-off | 2026-01-23 | Completato |
| Analisi requisiti | 2026-01-28 | Completato |
| Demo mockup customer care | 2026-02-13 | Completato |
| MVP ticketing | | In corso |
| Go-live | | Da definire |

## Decisioni chiave

- **Hosting**: Deploy sull'account AWS di Jubatus (non su account LAIF separato) — semplifica accesso a MySQL RDS e bucket S3
- **Approccio iterativo**: Validare mockup con dati finti prima di collegare dati reali
- **Focus iniziale**: Gestione segnalazioni email con categorizzazione e ticket management
- **Stack backend**: FastAPI (preferenza per nuovi servizi)

## Link utili

- **Repository**: https://github.com/laif-group/jubatus.git
- **Staging**: —
- **Produzione**: —
- **Notion progetto**: https://www.notion.so/laifgroup/Jubatus-2f190ad6ee4880a7af50fcc88ad15873

## Architettura esistente cliente

- **Database**: MySQL su AWS RDS (istanza privata, accesso SSH)
- **Storage**: S3 buckets per foto e video
- **Dashboard**: Grafana (interna + condivisa con partner)
- **WhatsApp bot**: Node.js, istanza AWS dedicata, in fase di test
- **Web app**: Gestita da software house esterna (non LAIF)

## Struttura cartella

```
jubatus/
├── README.md              ← questo file
├── meeting/               ← note meeting (una per file)
├── requisiti.md           ← requisiti estratti e validati
├── architettura.md        ← architettura del sistema
├── decisioni.md           ← decisioni tecniche (ADR)
├── feature-log.md         ← feature completate con note
├── stato-progetto.md      ← stato attuale e prossimi passi
└── manutenzione.md        ← note post go-live
```

> Repository codice: `/Users/simonebrigante/LAIF/repo/jubatus/`

## Note

- Il progetto è basato su `laif-template` (fork da upstream)
- La web app principale di Jubatus è gestita da una software house esterna — LAIF lavora solo sulla piattaforma di customer care
- L'integrazione con il DB MySQL esistente è un requisito chiave (read-only per ora)
