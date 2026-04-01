# Sistema Knowledge Base — LAIF

**Versione**: 1.14
**Creato**: 2026-03-08
**Team**: ~20 sviluppatori

---

## Navigazione documentazione

| Documento | Contenuto |
|-----------|-----------|
| [CLAUDE.md](CLAUDE.md) | Istruzioni operative per Claude Code — regole, workflow per fase, agenti autonomi |
| [docs/struttura.md](docs/struttura.md) | Albero cartelle, convenzioni naming, file nella root |
| [docs/skills.md](docs/skills.md) | Catalogo skill: mappa globale, flowchart per skill, input/output |
| [docs/workflow.md](docs/workflow.md) | Flussi per fase: quale skill usare quando, sequence diagrams |
| [docs/setup.md](docs/setup.md) | Guida installazione: Claude Code, Windsurf, MCP, environment |
| [knowledge/azienda/overview.md](knowledge/azienda/overview.md) | Chi è LAIF: team, clienti, modello di lavoro |
| [knowledge/azienda/stack.md](knowledge/azienda/stack.md) | Stack tecnico, pattern architetturali, RouterBuilder |
| [knowledge/azienda/infrastruttura.md](knowledge/azienda/infrastruttura.md) | AWS, ECS, TemplateStack, deploy pipeline |
| [knowledge/azienda/processi.md](knowledge/azienda/processi.md) | Dev workflow, CI/CD, regole Windsurf, pain point upstream |
| [IDEAS.md](IDEAS.md) | Backlog idee e miglioramenti futuri con stato |
| [CHANGELOG.md](CHANGELOG.md) | Tutte le modifiche al sistema (struttura + contenuti) |

---

## Cos'è questo sistema

Una knowledge base vivente per il team di LAIF. Non è una wiki statica: è un sistema che si aggiorna automaticamente durante il lavoro, cattura le decisioni mentre vengono prese, e rende riutilizzabile l'esperienza accumulata su ogni progetto.

**Gestito da**: Claude Code
**Usato per**: presales, sviluppo, consulta futura
**Lingua**: italiano

---

## Perché esiste

Senza un sistema, il knowledge generato su ogni progetto rimane nella testa delle persone o si disperde su Slack, Notion, email. Questo sistema serve a:

1. **Non perdere decisioni tecniche**: ogni scelta architetturale viene documentata mentre si fa
2. **Velocizzare i presales**: template e pattern già pronti per contratti e requisiti
3. **Riutilizzare pattern**: ciò che funziona su un progetto diventa un asset per il prossimo
4. **Onboarding rapido**: un nuovo sviluppatore trova il contesto di ogni progetto in un posto solo

---

## Come funziona

```
Input (meeting, codice, decisioni)
        ↓
   Skill Claude Code
        ↓
Documenti strutturati nella KB
        ↓
Tag → ricercabile
        ↓
Riutilizzo su progetti futuri
```

### Le skill sono il motore

Ogni operazione ha una skill dedicata. Le skill guidano Claude Code con un loop conversazionale: prima di produrre output, l'agente raccoglie le informazioni necessarie tramite domande mirate.

### I tag sono il motore di ricerca

Ogni documento ha tag nel frontmatter YAML. L'indice in `.tags/index.md` permette di trovare rapidamente pattern, decisioni e soluzioni per industria, tecnologia o problema.

---

## Struttura in dettaglio

### `projects/`
Un progetto = una cartella. Ogni cartella segue il template in `_template/` e contiene:
- **meeting/**: note meeting (una per file)
- File di progetto in root: requisiti, architettura, decisioni (ADR), feature-log, allegato-tecnico, mockup-brief, manutenzione

> Le repository di codice vivono in `/Users/simonebrigante/LAIF/repo/[nome]/`, separate dalla KB.

### `patterns/`
Pattern tecnici riutilizzabili estratti dai progetti. Esempi: architettura multi-tenant, integrazione pagamenti, autenticazione con provider esterni. Ogni pattern include contesto, soluzione, trade-off e link ai progetti dove è stato usato.

### `skills/`
I "programmi" del sistema. Ogni skill è un file markdown che Claude Code legge e segue. Contiene trigger, loop conversazionale, formato output.

### `knowledge/`
Conoscenza cross-progetto non legata a un singolo progetto. Include:
- **azienda/**: contesto aziendale LAIF (team, stack, infrastruttura, processi)
- **industrie/**: cosa sappiamo di retail, finance, healthcare, ecc.
- **problemi-tecnici/**: soluzioni a problemi ricorrenti

### `.tags/`
Indice dei tag. Permette di navigare la KB senza conoscere la struttura delle cartelle.

---

## Migrazione futura

Il sistema è progettato per migrare su Notion tramite MCP quando il team cresce. La struttura markdown è compatibile con import Notion. I tag diventeranno proprietà del database.

---

## Manutenzione del sistema stesso

| Quando | Skill | Cosa fa |
|--------|-------|---------|
| Ad ogni modifica + pre-commit | [verifica-pre-commit](skills/meta/verifica-pre-commit/SKILL.md) | 5 check automatici, blocca commit incoerenti |
| Dopo ogni modifica al framework | [gestione-kb](skills/meta/gestione-kb/SKILL.md) mod. 1 | Aggiorna changelog + docs/ |
| Fine sprint / fine mese | [audit-periodico](skills/maintenance/audit-periodico/SKILL.md) | Audit intera KB: obsolescenze, gap, tag |
| Fine sprint / fine progetto | [estrazione-pattern](skills/development/estrazione-pattern/SKILL.md) | Estrae pattern riutilizzabili |
| Periodicamente | [gestione-kb](skills/meta/gestione-kb/SKILL.md) mod. 4 | Review idee backlog |
