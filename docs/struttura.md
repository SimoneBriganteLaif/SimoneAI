# Struttura della Knowledge Base

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
│   │   ├── presales/
│   │   │   ├── note-meeting/       ← Note grezze dai meeting (una per file, con data).
│   │   │   ├── requisiti.md        ← Requisiti strutturati: RF, RNF, domande aperte.
│   │   │   ├── requisiti-mockup.md ← Brief per Windsurf: schermate, flussi, brand.
│   │   │   └── allegato-tecnico.md ← Allegato contrattuale: max 3 pagine, non tecnico.
│   │   ├── development/
│   │   │   ├── architettura.md     ← Stack, componenti, diagrammi, debito tecnico.
│   │   │   ├── decisioni-tecniche.md ← Log ADR (Architecture Decision Record).
│   │   │   └── feature-log.md     ← Feature completate: cosa, come, problemi, PR.
│   │   └── maintenance/
│   │       └── note.md             ← Note post go-live.
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
│       └── gestione-kb/            ← Changelog, idee, sync docs, review idee.
│
├── knowledge/                      ← Conoscenza cross-progetto, non legata a un singolo progetto.
│   ├── README.md                   ← Overview della knowledge disponibile.
│   ├── industrie/                  ← Cosa sappiamo di settori specifici.
│   │   └── _template.md            │  (retail, finance, healthcare, saas...)
│   └── problemi-tecnici/           ← Soluzioni a problemi tecnici ricorrenti.
│       └── _template.md
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
