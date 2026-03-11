# MCP Server Wolico

Server MCP per interrogare Wolico (piattaforma interna LAIF).
Moduli: ferie/assenze, staffing settimanale, economics (fatturazione e revenue), dati dipendente.

## Tool disponibili

### Ferie e Assenze
| Tool | Descrizione |
|------|-------------|
| `get_ferie_team` | Tutte le assenze in un intervallo di date |
| `get_ferie_persona` | Assenze di un dipendente specifico (ricerca per nome) |
| `get_calendario_settimana` | Chi è assente in una settimana (default: corrente) |

### Staffing
| Tool | Descrizione |
|------|-------------|
| `get_staffing_team` | Allocazione settimanale di tutto il team (chi lavora su cosa) |
| `get_staffing_persona` | Staffing settimanale di un dipendente specifico |

### Economics
| Tool | Descrizione |
|------|-------------|
| `get_tranche_fatturazione` | Tranche di fatturazione da emettere (mese corrente e prossimi) |
| `get_revenues_overview` | Panoramica revenue annuale per mese (fatturato, forecast, starting, probabile) |

### Dipendenti
| Tool | Descrizione |
|------|-------------|
| `get_mio_stipendio` | Dati contratto e stipendio del dipendente corrente (permessi limitati) |

## Struttura progetto

```
wolico/
├── server.py          ← entry point MCP (stdio + HTTP)
├── api.py             ← auth JWT + HTTP helpers
├── helpers.py         ← utility condivise (date, filtri, error handling)
├── tools/
│   ├── __init__.py    ← registry di tutti i tool
│   ├── outages.py     ← 3 tool ferie/assenze
│   ├── staffing.py    ← 2 tool staffing settimanale
│   ├── economics.py   ← 2 tool fatturazione + revenue
│   └── employees.py   ← 1 tool dati dipendente
├── deploy/
│   ├── deploy.sh      ← deploy AWS Lambda (crea tutta l'infra)
│   ├── teardown.sh    ← elimina tutta l'infra AWS
│   └── Dockerfile.lambda  ← immagine Docker per Lambda
├── Dockerfile         ← immagine Docker per uso locale (stdio)
├── pyproject.toml
└── .env.example
```

## Setup locale

### Prerequisiti
- Docker Desktop **oppure** Python 3.10+
- Account Wolico con credenziali personali

### Opzione A — Docker (consigliata)

```bash
# 1. Clona o copia la cartella
cd ~/LAIF/Progetti/SimoneAI/mcp-servers/wolico

# 2. Build dell'immagine
docker build -t wolico-mcp .

# 3. Configura le TUE credenziali
cp .env.example .env
# Modifica .env con le tue credenziali Wolico

# 4. Registra in Claude Code
claude mcp add wolico -- docker run -i --rm \
  --env-file /percorso/completo/mcp-servers/wolico/.env \
  wolico-mcp

# 5. Riavvia Claude Code e testa
# "Chi è in ferie questa settimana?"
```

### Opzione B — Python diretto

```bash
# 1. Clona o copia la cartella
cd ~/LAIF/Progetti/SimoneAI/mcp-servers/wolico

# 2. Installa dipendenze
pip install mcp httpx python-dotenv

# 3. Configura le TUE credenziali
cp .env.example .env

# 4. Registra in Claude Code
claude mcp add wolico -- python3 /percorso/completo/mcp-servers/wolico/server.py

# 5. Riavvia Claude Code e testa
```

### Configurazione `.env`

```env
# Produzione (ogni collega usa le proprie credenziali)
WOLICO_BASE_URL=https://wolico.app.laifgroup.com/api/
WOLICO_EMAIL=nome.cognome@laifgroup.com
WOLICO_PASSWORD=la_tua_password_wolico
```

### Note importanti
- **Claude Code CLI**: i tool MCP configurati con `claude mcp add` sono visibili solo in Claude Code (la CLI), non nell'app Claude desktop/web
- **Riavvio**: dopo aver aggiunto/rimosso un MCP server, è necessario riavviare Claude Code per caricare i nuovi tool

---

## Deploy su AWS Lambda (~$0/mese)

Rende il server MCP accessibile a tutti i colleghi senza installazione locale.
Ogni utente si autentica con la propria email Wolico.

### Architettura

```
Colleghi (Claude Code / Notion AI)
    ↓ HTTPS POST (Streamable HTTP)
Lambda Function URL (RESPONSE_STREAM)
    ↓
Lambda Web Adapter → uvicorn (port 8080)
    ↓
MCP Server (server.py, transport HTTP)
    ↓                    ↓
Secrets Manager      Wolico API
(email→password)     (wolico.app.laifgroup.com)
```

### Prerequisiti

- AWS CLI v2
- Docker Desktop
- SSO configurato con profilo `LaifDev`

```bash
# Login SSO (una tantum, scade dopo ~8h)
aws sso login --profile LaifDev
```

### Deploy

```bash
cd ~/LAIF/Progetti/SimoneAI/mcp-servers/wolico

# Deploy completo (crea ECR + IAM + Lambda + Secrets Manager + Function URL)
./deploy/deploy.sh

# Output: URL MCP del tipo https://xxx.lambda-url.eu-west-1.on.aws/mcp
```

### Aggiungere utenti

Le password Wolico sono salvate in AWS Secrets Manager (criptato KMS).
Il client invia solo l'email via header HTTPS — la password non esce mai da AWS.

```bash
# Aggiungi un collega
./deploy/deploy.sh add-user simone.brigante@laifgroup.com 'password_wolico'
./deploy/deploy.sh add-user marco.pinelli@laifgroup.com 'password_wolico'
```

### Configurazione colleghi (Claude Code)

Ogni collega esegue:

```bash
claude mcp add wolico \
  --transport streamablehttp \
  --header "X-Wolico-Email:nome.cognome@laifgroup.com" \
  https://xxx.lambda-url.eu-west-1.on.aws/mcp
```

### Aggiornare il server

Dopo modifiche al codice:

```bash
./deploy/deploy.sh update
```

### Eliminare tutta l'infrastruttura

```bash
./deploy/teardown.sh
```

Rimuove: Lambda, Function URL, IAM role, ECR repository, Secrets Manager.

### Costi stimati

| Risorsa | Costo |
|---------|-------|
| Lambda (256MB ARM64, free tier) | ~$0/mese |
| ECR (immagine ~100MB) | ~$0.01/mese |
| Secrets Manager (1 secret) | ~$0.40/mese |
| **Totale** | **~$0.50/mese** |

---

## Notion AI — Custom Agent

Notion AI supporta MCP server esterni tramite Custom Agents.

### Prerequisiti
- Server MCP deployato su Lambda (sezione precedente)
- Workspace admin Notion (per abilitare la feature)

### 1. Abilitare MCP server custom (admin workspace)

1. **Settings & members** → **Notion AI**
2. Sotto **AI connectors**, abilita **Custom MCP servers**
3. Questo permette a tutti gli utenti del workspace di collegare MCP esterni

### 2. Creare un Custom Agent (ogni utente)

1. Apri **Notion AI** → **Custom Agents** → **New Agent**
2. **Nome**: `Wolico` (o a piacere)
3. **Descrizione**: `Accesso a ferie, staffing, fatturazione e dati Wolico`
4. Sezione **MCP connections** → **Add connection** → **Custom server**
5. **URL**: `https://xxx.lambda-url.eu-west-1.on.aws/mcp` (l'URL dal deploy)
6. **Headers personalizzati**: `X-Wolico-Email: tua.email@laifgroup.com`

### 3. Configurare i permessi tool

Notion mostra la lista degli 8 tool. Per ciascuno scegliere:
- **Auto-run** — esegui automaticamente (consigliato per lettura)
- **Confirm before running** — chiedi conferma

### 4. Testare

Nella chat con il Custom Agent, scrivere:
- *"Chi è in ferie questa settimana?"*
- *"Qual è lo staffing del team?"*
- *"Mostrami le tranche di fatturazione"*

### Note Notion AI
- Ogni connessione MCP è specifica per un singolo Custom Agent
- I Custom Agents usano Notion Credits (~$10 per 1,000 credits)
- L'autenticazione Wolico usa l'email configurata nell'header dell'agente

---

## Come funziona

1. All'avvio (prima chiamata) il server fa login su `POST /auth/login` e salva il JWT in memoria
2. Ogni tool esegue chiamate autenticate alle API Wolico
3. In caso di 401 (token scaduto) rinnova automaticamente il token
4. Transport locale: `stdio` — Claude Code lo lancia automaticamente
5. Transport remoto: `Streamable HTTP` — Lambda Function URL

## Esempi di utilizzo

- *"Chi è in ferie questa settimana?"*
- *"Mostrami le assenze di Marco a marzo 2026"*
- *"Qual è lo staffing di Simone questa settimana?"*
- *"Mostrami lo staffing del team"*
- *"Quali sono le tranche di fatturazione da emettere?"*
- *"Dammi una panoramica delle revenue 2026"*
- *"Mostrami i miei dati contrattuali"*

## API Wolico utilizzate

| Endpoint | Metodo | Modulo |
|----------|--------|--------|
| `/auth/login` | POST | Auth |
| `/outages/search` | POST | Ferie |
| `/staffing/search` | POST | Staffing |
| `/economics/revenues/to-issue/{company}` | GET | Economics |
| `/economics/revenues/chart-data/{company}/{year}` | GET | Economics |
| `/employees/myself` | GET | Dipendenti |
