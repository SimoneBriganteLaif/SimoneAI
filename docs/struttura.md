# Struttura della Knowledge Base

← [System.md](../System.md) · [skills.md](skills.md) · [workflow.md](workflow.md)

**Ultimo aggiornamento**: 2026-03-08

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
├── CHANGELOG-framework.md          ← Traccia modifiche alla STRUTTURA del sistema:
│                                     cartelle, skill, template, processi, documentazione.
│                                     Formato Keep a Changelog.
│
├── CHANGELOG-contenuti.md          ← Traccia modifiche ai CONTENUTI operativi:
│                                     progetti, pattern, knowledge, decisioni tecniche.
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
│   └── workflow.md                 ← Flussi di lavoro per fase + divisione Claude Code/Windsurf.
│
├── projects/                       ← Un progetto = una cartella.
│   │                                 Ogni cartella segue il template _template/.
│   ├── INDEX.md                    ← Registro di tutti i progetti: stato, stack, date.
│   │                                 Aggiornato automaticamente da init-project.
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
│   │   └── manutenzione.md        ← Note post go-live.
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
│   │   ├── estrazione-decisioni/   ← Documenta decisioni tecniche in formato ADR.
│   │   └── estrazione-pattern/     ← Fine sprint → estrae pattern riutilizzabili.
│   ├── maintenance/                ← Manutenzione periodica.
│   │   └── audit-periodico/        ← Audit mensile dell'intera KB.
│   └── meta/                       ← Gestione del sistema stesso.
│       ├── gestione-kb/            ← Changelog, idee, sync docs, review idee.
│       └── verifica-pre-commit/    ← Verifica autonoma coerenza pre-commit (5 check paralleli).
│
├── knowledge/                      ← Conoscenza cross-progetto, non legata a un singolo progetto.
│   ├── README.md                   ← Overview della knowledge disponibile.
│   ├── azienda/                    ← Contesto aziendale LAIF.
│   │   ├── overview.md             ← Chi è LAIF, team, modello di lavoro.
│   │   ├── stack.md                ← Stack tecnico, pattern, convenzioni naming.
│   │   ├── infrastruttura.md       ← Architettura AWS, TemplateStack, deploy.
│   │   └── processi.md             ← Flussi di lavoro, CI/CD, regole Windsurf.
│   ├── industrie/                  ← Cosa sappiamo di settori specifici.
│   │   └── _template.md            │  (retail, finance, healthcare, saas...)
│   └── problemi-tecnici/           ← Soluzioni a problemi tecnici ricorrenti.
│       └── _template.md
│
├── core/                           ← Repository core LAIF clonate come riferimento.
│   │                                 NON modificare direttamente.
│   │                                 I riassunti sono in knowledge/azienda/.
│   ├── README.md                   ← Indice repo con link GitHub e descrizioni.
│   ├── laif-template/              ← Base per tutti i progetti (fork).
│   ├── ds/                         ← Design System condiviso (@laif/ds).
│   └── laif-cdk/                   ← Infrastruttura AWS via CDK.
│
└── .tags/                          ← Sistema di tag per navigazione cross-progetto.
    └── index.md                    ← Indice dei tag usati nella KB.
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
| `CHANGELOG-framework.md` | Traccia modifiche alla struttura: cartelle, skill, template, processi |
| `CHANGELOG-contenuti.md` | Traccia modifiche ai contenuti: progetti, pattern, knowledge, decisioni |
| `IDEAS.md` | Backlog strutturato di idee e miglioramenti futuri |
