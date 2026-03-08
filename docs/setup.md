# Guida Setup Ambiente

← [System.md](../System.md) · [struttura.md](struttura.md) · [workflow.md](workflow.md)

**Ultimo aggiornamento**: 2026-03-08

Questa guida copre la configurazione completa dell'ambiente di lavoro: Knowledge Base, Claude Code, Windsurf, ambiente di sviluppo, e tool ausiliari.

---

## 1. Knowledge Base (SimoneAI)

### Prerequisiti

- Git installato
- Accesso al repository SimoneAI

### Setup

```bash
# Clona la KB
cd ~/LAIF/Progetti
git clone <url-repo> SimoneAI
cd SimoneAI

# Clona le repo core come contesto
mkdir -p core
cd core
git clone https://github.com/laif-group/laif-template.git laif-template
git clone https://github.com/laif-group/ds.git ds
git clone https://github.com/laif-group/laif-cdk.git laif-cdk
cd ..
```

Le repo core sono escluse dal git della KB (vedi `.gitignore`).

### Struttura

Vedi `docs/struttura.md` per la mappa completa delle cartelle.

### Primo utilizzo

1. Leggi `CLAUDE.md` — le istruzioni operative
2. Leggi `System.md` — panoramica del sistema
3. Consulta `knowledge/azienda/` — contesto aziendale LAIF
4. Guarda `skills/README.md` — elenco skill disponibili

---

## 2. Claude Code

### Installazione

```bash
# Installa Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

### Configurazione globale (`~/.claude/settings.json`)

Configurazione attuale:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "model": "sonnet",
  "enabledPlugins": {
    "frontend-design@claude-plugins-official": true,
    "github@claude-plugins-official": false,
    "Notion@claude-plugins-official": true,
    "claude-mem@thedotmack": true
  }
}
```

#### Note sulla configurazione

| Parametro | Valore | Note |
|-----------|--------|------|
| `model` | `sonnet` | Modello default. Per task complessi si può switchare a `opus` in sessione |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `1` | Abilita agent teams (sperimentale) |
| `frontend-design` | abilitato | Plugin per generare UI/frontend |
| `github` | **disabilitato** | Plugin GitHub (da valutare se riabilitare) |
| `Notion` | abilitato | Accesso a Notion via MCP |
| `claude-mem` | abilitato | Memoria persistente cross-sessione |

### Plugin installati

| Plugin | Scope | Scopo |
|--------|-------|-------|
| `frontend-design` | UI/Frontend | Genera interfacce frontend production-grade |
| `github` | GitHub | Integrazione GitHub (attualmente disabilitato) |
| `Notion` | MCP | Accesso a workspace Notion per leggere/scrivere pagine |
| `claude-mem` | MCP | Memoria semantica persistente tra sessioni |

### MCP Server

I plugin di Claude Code includono MCP server integrati. Attualmente:

- **Notion MCP**: lettura/scrittura pagine Notion (usato da `init-project`)
- **claude-mem**: ricerca semantica nella memoria cross-sessione
- **Context7**: documentazione librerie (disponibile via marketplace)

#### MCP da aggiungere (futuro)

| MCP | Scopo | Priorità |
|-----|-------|----------|
| Database locale | Connessione a PostgreSQL locale per ispezionare schema | alta |
| Database remoto | Connessione a RDS dev per debugging | media |
| GitHub MCP | Alternativa al plugin GitHub per operazioni avanzate | media |

### Uso con la KB

Aprire Claude Code dalla root della KB:

```bash
cd ~/LAIF/Progetti/SimoneAI
claude
```

Claude Code legge automaticamente `CLAUDE.md` e ha accesso a tutta la struttura.

### Uso su un progetto

```bash
cd ~/LAIF/repo/nome-progetto
claude
```

Il progetto deve avere il proprio `CLAUDE.md` (generato dalla skill `init-project`).

---

## 3. Windsurf

### Installazione

Scaricare Windsurf da [windsurf.com](https://windsurf.com) e installare.

### Percorsi configurazione

| Percorso | Contenuto |
|----------|-----------|
| `~/.windsurf/` | Configurazione editor (argv.json, estensioni, plans) |
| `~/.codeium/windsurf/` | Configurazione AI (skill, memorie, MCP, regole globali) |

### Skill Windsurf esistenti

Windsurf ha già 8 skill operative in `~/.codeium/windsurf/skills/`:

| Skill | Scopo |
|-------|-------|
| `full-feature` | Orchestratore end-to-end: plan → backend → frontend → test → docs |
| `plan-feature` | Analisi AS-IS/TO-BE, genera specifica feature |
| `backend-api` | Modello → Schema → Service → Controller → Migrazione |
| `backend-test` | Genera test pytest + comandi curl |
| `frontend-page` | Pagina → Feature module → Navigation → i18n |
| `frontend-test` | Test Playwright component + E2E |
| `test` | Esecuzione test generica |
| `update-docs` | Aggiorna changelog e documentazione progetto |

Queste skill guidano Windsurf nella scrittura del codice seguendo i pattern LAIF.

### Regole globali Windsurf

File: `~/.codeium/windsurf/memories/global_rules.md`

Contiene regole su:
- Lingua e comunicazione (italiano)
- Riferimenti alla KB LAIF: quali file leggere prima di sviluppare
- Regole di sviluppo LAIF: DS obbligatorio, pattern backend/frontend, naming conventions
- Come segnalare le modifiche: aggiornare CHANGELOG, feature spec, PROJECT_CONTEXT nel progetto
- Cosa NON fare: non modificare direttamente la KB, non ignorare i pattern documentati

### MCP Server Windsurf

File: `~/.codeium/windsurf/mcp_config.json`

| Server | Stato | Scopo |
|--------|-------|-------|
| `postgresql` | **abilitato** | Connessione a PostgreSQL locale (`host.docker.internal:5432`) |
| `github-mcp-server` | disabilitato | Operazioni GitHub via Docker |
| `memory` | disabilitato | Server memoria MCP |
| `notion-mcp-server` | disabilitato | Accesso Notion |

### Regole per progetto

Le regole Windsurf specifiche per progetto vivono in `.windsurf/rules/` **dentro ogni progetto** (incluse in `laif-template`).

Guidano Windsurf su:
- Come usare RouterBuilder (backend)
- Come usare componenti DS (frontend)
- Convenzioni naming
- Architettura soft onion

### Flusso KB con Windsurf

Windsurf **legge** la KB per contesto (stack, pattern, processi) ma **non la modifica** direttamente.
Dopo ogni sessione di sviluppo, Windsurf aggiorna i file del progetto (`CHANGELOG.md`, feature spec, `PROJECT_CONTEXT.md`).
Claude Code sincronizza poi queste informazioni nella KB.

Le regole globali da estendere andrebbero in `~/.codeium/windsurf/memories/global_rules.md`.

---

## 4. Ambiente di sviluppo

### Prerequisiti

| Tool | Versione | Installazione |
|------|----------|--------------|
| Docker Desktop | Latest | [docker.com](https://docker.com) |
| Node.js | 25+ | `nvm install 25` o download diretto |
| Python | 3.12+ | `pyenv install 3.12` o download diretto |
| Just | Latest | `brew install just` |
| Git | Latest | `brew install git` |
| GitHub CLI | Latest | `brew install gh` |
| AWS CLI | v2 | `brew install awscli` |

### Docker

Docker Desktop deve essere in esecuzione per lo sviluppo locale (backend usa PostgreSQL in container).

### Just (task runner)

`laif-template` usa Just al posto di Make. Comandi principali:

```bash
just run default    # Avvia ambiente dev (backend + DB)
just run all        # Avvia backend + frontend
just run pytest     # Esegui test backend
just migrate create # Crea migrazione DB
just migrate upgrade # Applica migrazioni
just fe generate-client  # Genera client API da OpenAPI spec
```

### AWS

```bash
# Configura profili AWS per ogni cliente
aws configure --profile cliente-dev
aws configure --profile cliente-prod

# Verifica
aws sts get-caller-identity --profile cliente-dev
```

Ogni cliente ha 2 account AWS separati (dev/prod). I profili devono corrispondere a quelli in `dev.yaml`/`prod.yaml` del progetto CDK.

### GitHub CLI

```bash
# Autenticazione
gh auth login

# Verifica accesso ai repo LAIF
gh repo list laif-group
```

---

## 5. Workflow tipico: nuovo progetto

1. **KB**: esegui `skills/presales/init-project/` per creare struttura progetto
2. **GitHub**: fork `laif-template` → nuovo repo
3. **Locale**: `git clone` del nuovo repo
4. **CDK**: configura `dev.yaml`/`prod.yaml`, deploy infrastruttura
5. **Dev**: `just run all`, inizia sviluppo con Windsurf
6. **KB**: documenta decisioni con `skills/development/estrazione-decisioni/`

---

## 6. Tool ausiliari

### Tool attualmente in uso

| Tool | Scopo | Config |
|------|-------|--------|
| Docker Desktop | Container per sviluppo locale | Sempre in esecuzione |
| AWS CLI v2 | Deploy infrastruttura, accesso servizi | Profili per cliente |
| GitHub CLI (`gh`) | Gestione repo, PR, issues | `gh auth login` |
| Notion | Documentazione cliente, info progetto | Via MCP in Claude Code |

### Tool da configurare (futuro)

| Tool | Scopo | Note |
|------|-------|------|
| MCP Database locale | Ispezionare schema PostgreSQL da Claude Code | Connessione a Docker locale |
| MCP Database remoto | Debugging su RDS dev | Richiede tunnel/bastion |
| MCP GitHub | Operazioni GitHub avanzate da Claude Code | Alternativa al plugin |

---

## Checklist setup completo

- [ ] Git configurato con chiave SSH per GitHub
- [ ] SimoneAI clonato con repo core in `core/`
- [ ] Claude Code installato e configurato (`settings.json`)
- [ ] Plugin Claude Code attivi (Notion, claude-mem, frontend-design)
- [ ] Windsurf installato
- [ ] Docker Desktop installato e in esecuzione
- [ ] Node.js 25+ installato
- [ ] Python 3.12+ installato
- [ ] Just installato (`brew install just`)
- [ ] AWS CLI configurato con profili per ogni cliente
- [ ] GitHub CLI autenticato (`gh auth login`)
