# Struttura della Knowledge Base

← [System.md](../System.md) · [skills.md](skills.md) · [workflow.md](workflow.md)

**Ultimo aggiornamento**: 2026-04-08

---

## Albero delle cartelle

```
SimoneAI/
│
├── CLAUDE.md                       ← Istruzioni operative per Claude Code.
│                                     Letto automaticamente a ogni sessione.
│                                     Definisce regole, workflow per fase, tag standard.
│
├── System.md                       ← Panoramica del sistema: cos'è, perché esiste,
│                                     come funziona. Documento descrittivo per umani.
│
├── CHANGELOG.md                    ← Tutte le modifiche al sistema: struttura
│                                     (### Struttura) e contenuti (### Contenuti)
│                                     per ogni versione. Formato Keep a Changelog.
│
├── IDEAS.md                        ← Backlog strutturato di idee e miglioramenti.
│                                     Tabella con ID, categoria, effort, priorità, stato.
│                                     Gestito dalla skill gestione-kb (modalità 2 e 4).
│
├── .gitignore                      ← Esclude memory/, .claude/, file di sistema.
│
├── docs/                           ← Documentazione navigabile del sistema stesso.
│   │                                 Serve sia come riferimento per l'utente
│   │                                 sia come contesto per gli agenti AI.
│   ├── struttura.md                ← Questo file. Mappa delle cartelle e convenzioni.
│   ├── skills.md                   ← Catalogo completo delle skill con flussi Mermaid.
│   ├── workflow.md                 ← Flussi di lavoro per fase + divisione Claude Code/Windsurf.
│   └── setup.md                    ← Guida installazione: Claude Code, Windsurf, MCP, environment.
│
├── projects/                       ← Un progetto = una cartella.
│   │                                 Ogni cartella segue il template _template/.
│   ├── INDEX.md                    ← Registro di tutti i progetti: stato, stack, date.
│   │                                 Aggiornato automaticamente da init-project.
│   ├── _archivio/                  ← Progetti archiviati (chiusi o sospesi).
│   ├── _template/                  ← Template base — NON copiare manualmente,
│   │   │                             usa la skill init-project.
│   │   ├── README.md               ← Overview progetto: cliente, stack, link, timeline.
│   │   ├── meeting/               ← Note meeting (una per file, con data).
│   │   ├── requisiti.md           ← Requisiti strutturati: RF, RNF, domande aperte.
│   │   ├── architettura.md        ← Stack, componenti, diagrammi, debito tecnico.
│   │   ├── decisioni.md           ← Log ADR (Architecture Decision Record).
│   │   ├── feature-log.md         ← Feature completate: cosa, come, problemi, PR.
│   │   ├── stato-progetto.md     ← Stato attuale, blocchi critici, prossimi passi.
│   │   ├── allegato-tecnico.md    ← Allegato contrattuale: max 3 pagine, non tecnico.
│   │   ├── mockup-brief.md        ← Brief per Windsurf: schermate, flussi, brand.
│   │   ├── manutenzione.md        ← Note post go-live.
│   │   ├── aws-config.yaml        ← Config AWS: profili, regione, nomi risorse.
│   │   └── windsurf-briefs/       ← Brief di sviluppo per Windsurf + report feedback.
│   │       └── [RF-XX]-[nome].md  ← Brief autocontenuto generato da feature-develop.
│   └── [nome-progetto]/            ← Creato dalla skill init-project.
│
├── patterns/                       ← Pattern tecnici riutilizzabili estratti dai progetti.
│   │                                 Ogni pattern documenta: problema, soluzione,
│   │                                 trade-off, e in quali progetti è stato usato.
│   ├── README.md                   ← Indice dei pattern esistenti.
│   └── _template.md                ← Template per nuovi pattern.
│
├── skills/                         ← Istruzioni operative del sistema.
│   │                                 Ogni skill = cartella con SKILL.md dentro.
│   │                                 Organizzate per fase.
│   ├── README.md                   ← Indice delle skill con trigger e output.
│   ├── presales/                   ← Fase presales: dal primo contatto al contratto.
│   │   ├── init-project/           ← Bootstrap completo progetto nella KB.
│   │   ├── estrazione-requisiti/   ← Note meeting → requisiti strutturati.
│   │   ├── genera-allegato-tecnico/ ← Requisiti → allegato contrattuale.
│   │   └── genera-mockup-brief/    ← Requisiti → brief mockup per Windsurf.
│   ├── development/                ← Fase sviluppo: durante lo sprint.
│   │   ├── feature-workflow/       ← Orchestra ciclo completo feature (Plan→Dev→Test→Review).
│   │   ├── feature-plan/           ← Requisito → piano implementazione tecnico.
│   │   ├── feature-develop/        ← Piano → implementazione (Claude Code o Windsurf brief).
│   │   ├── feature-test/           ← Test completo: scrive, esegue, verifica criteri.
│   │   ├── feature-review/         ← Review: pattern LAIF, duplicazioni, qualità, KB.
│   │   ├── estrazione-decisioni/   ← Documenta decisioni tecniche in formato ADR.
│   │   ├── estrazione-pattern/     ← Fine sprint → estrae pattern riutilizzabili.
│   │   ├── setup-progetto-dev/     ← Verifica ambiente dev locale (Docker, servizi, auth).
│   │   ├── brainstorming-post-sviluppo/ ← Analisi fine sessione → pattern, skill, idee.
│   │   ├── crea-task-notion/      ← KB + Notion → task strutturati su Notion per Feature.
│   │   ├── windsurf-feedback/     ← Processa report feedback Windsurf → KB.
│   │   ├── db-transfer/          ← Trasferimento dati tra DB PostgreSQL con verifica schema.
│   │   ├── gestione-issue/       ← Gestione issue stack interno via Notion MCP.
│   │   └── aws-diagnostics/       ← Skill diagnostiche AWS read-only.
│   │       ├── README.md           ← Overview, flowchart selezione, naming convention.
│   │       ├── _shared/            ← Libreria Python + doc condivisi.
│   │       │   ├── config.py       ← Gestione aws-config.yaml.
│   │       │   ├── aws_runner.py   ← Wrapper AWS CLI (whitelist read-only).
│   │       │   ├── output.py       ← Formattazione tabelle e semafori.
│   │       │   ├── collectors.py   ← Layer raccolta dati (return dict, no print).
│   │       │   ├── config-discovery.md ← Procedura generazione config.
│   │       │   └── query-templates.md  ← Query CloudWatch Logs Insights.
│   │       ├── aws-health-report/  ← Report HTML completo con grafici SVG.
│   │       ├── aws-triage/         ← Health check rapido tutti i servizi.
│   │       ├── aws-ecs-diagnose/   ← Deep-dive ECS (deployment, task, capacity).
│   │       ├── aws-logs-diagnose/  ← Query CloudWatch Logs Insights.
│   │       ├── aws-rds-diagnose/   ← Stato RDS, connessioni, log PostgreSQL.
│   │       └── aws-s3-diagnose/    ← Inventario bucket, dimensioni, upload.
│   ├── maintenance/                ← Manutenzione periodica.
│   │   └── audit-periodico/        ← Audit mensile dell'intera KB.
│   └── meta/                       ← Gestione del sistema stesso.
│       ├── gestione-kb/            ← Changelog, idee, sync docs, review idee.
│       ├── contesto-progetto/      ← Script match.py: trova contesto rilevante per progetto.
│       └── verifica-pre-commit/    ← Verifica autonoma coerenza pre-commit (5 check paralleli).
│
├── knowledge/                      ← Conoscenza cross-progetto, non legata a un singolo progetto.
│   ├── README.md                   ← Overview della knowledge disponibile.
│   ├── azienda/                    ← Contesto aziendale LAIF.
│   │   ├── overview.md             ← Chi è LAIF, team, modello di lavoro.
│   │   ├── stack.md                ← Stack tecnico, pattern, convenzioni naming.
│   │   ├── infrastruttura.md       ← Architettura AWS, TemplateStack, deploy.
│   │   ├── processi.md             ← Flussi di lavoro, CI/CD, regole Windsurf.
│   │   ├── wolico-api.md           ← Riferimento API Wolico: auth, endpoint, pattern search.
│   │   └── laif-ds-local-link.md   ← Procedura link laif-ds locale nei progetti consumer.
│   ├── industrie/                  ← Cosa sappiamo di settori specifici.
│   │   ├── _template.md            ← Template per nuove industrie.
│   │   ├── entertainment.md        ← Entertainment/eventi (da Jubatus).
│   │   └── healthcare.md           ← Healthcare/medical devices (da Lamonea).
│   └── problemi-tecnici/           ← Soluzioni a problemi tecnici ricorrenti.
│       ├── _template.md            ← Template per nuovi problemi.
│       ├── query-n-plus-1.md       ← N+1 con ORM e relazioni.
│       ├── xss-contenuto-esterno.md ← XSS da HTML esterno.
│       └── routing-conflitti-parametrici.md ← Route statiche vs parametriche.
│
├── mcp-servers/                    ← MCP server locali per Claude Code.
│   └── wolico/                     ← MCP server Wolico: 25+ tool (CRM, HR, Economics,
│                                     Ticketing, Monitoring, Operations, Administration).
│
├── issues/                         ← Tracking issue interne cross-stack
│   │                                 (laif-template, laif-ds, laif-infra).
│   └── INDEX.md                    ← Dashboard con matrice priorità e statistiche.
│
├── tools/                          ← Strumenti standalone sviluppati per la KB.
│   ├── er-editor/                  ← Editor visuale schema ER (Flask, API, test).
│   ├── graph-api/                  ← Client CLI Microsoft Graph API (Device Code Flow, MSAL).
│   └── analisi-marginalita/        ← Dashboard web analisi marginalità (HTML/JS, 9 tab, extract.py).
│
├── LAIF-repo-analysis/             ← Censimento completo 40 repo LAIF in produzione.
│   ├── INDEX.md                    ← Indice generale analisi.
│   ├── repos/                      ← 40 analisi individuali (una per repo).
│   ├── cross-analysis/             ← Analisi trasversali: feature matrix, template drift, ecc.
│   └── laif-template-baseline.md   ← Documento baseline template v5.7.0.
│
├── laif-kb/                        ← KB condivisa LAIF (convenzioni, processi, skill operative).
│   ├── CLAUDE.md                   ← Istruzioni Claude Code per laif-kb.
│   ├── convenzioni/                ← Regole git flow, naming DB, standard codice.
│   ├── processi/                   ← Mappa ciclo di vita processi aziendali.
│   └── skills/                     ← Skill autocontenute (analisi-repo, documenta-processo).
│
├── .tags/                          ← Sistema di tag per navigazione cross-progetto.
│   ├── index.md                    ← Indice dei tag usati nella KB.
│   └── (nessun file runtime — solo indice)
│
└── .claude/
    ├── skills/                     ← Skill native Claude Code — trigger layer.
    │   │                             Ogni skill = directory con SKILL.md dentro.
    │   │                             Wrapper sottili che puntano alle skill KB
    │   │                             per auto-discovery e tracking nell'UI.
    │   └── [skill-name]/SKILL.md   ← 22 directory (gestione-kb, init-project, gestione-issue, db-transfer, ...)
    ├── hooks/                      ← Script automazione (attualmente vuota).
    ├── settings.json               ← Configurazione hook Claude Code.
    └── skill-usage.log             ← Log uso skill (gitignored, cresce runtime).
```

---

## Convenzioni di naming

| Tipo | Formato | Esempio |
|------|---------|---------|
| Cartelle progetto | kebab-case | `progetto-ecommerce` |
| File markdown | kebab-case | `allegato-tecnico.md` |
| Cartelle skill | kebab-case | `estrazione-requisiti/` |
| Tag | `#categoria:valore` | `#industria:retail` |
| ID requisiti | `RF-NN` / `RNF-NN` | `RF-01`, `RNF-03` |
| ID decisioni | `ADR-NNN` | `ADR-001` |
| ID idee | `IDEA-NNN` | `IDEA-001` |

---

## File nella root

| File | Scopo |
|------|-------|
| `CLAUDE.md` | Istruzioni operative per Claude Code — letto automaticamente a ogni sessione |
| `System.md` | Panoramica del sistema, motivazioni, struttura ad alto livello |
| `CHANGELOG.md` | Tutte le modifiche: struttura + contenuti per ogni versione |
| `IDEAS.md` | Backlog strutturato di idee e miglioramenti futuri |
