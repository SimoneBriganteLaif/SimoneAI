---
nome: "db-transfer"
descrizione: >
  Trasferimento dati tra database PostgreSQL con verifica schema, selezione tabelle
  interattiva e ordinamento automatico per foreign key. Supporta AWS Secrets Manager,
  URL diretti e file .env.
fase: development
versione: "1.1"
stato: beta
legge:
  - projects/[nome]/aws-config.yaml
  - .env files del progetto
scrive:
  - (nessun file KB — opera direttamente sui database)
aggiornato: "2026-04-21"
---

# db-transfer — Trasferimento dati tra database PostgreSQL

## Obiettivo

Copiare dati da un database PostgreSQL a un altro in modo sicuro, con verifica
preventiva degli schema e selezione interattiva delle tabelle.

## Perimetro

**Cosa fa:**
- Identifica source e destination (ARN, URL, .env)
- Confronta gli schema dei due database e segnala discrepanze
- Mostra le tabelle disponibili con row count e dimensione stimata
- Permette di selezionare quali tabelle trasferire (con wildcard)
- Ordina le tabelle per rispettare le foreign key (gestisce anche cicli FK)
- Esegue il trasferimento con `pg_dump | psql`, disabilitando temporaneamente i FK constraint (`session_replication_role = replica`) per supportare cicli e ordinamenti non perfetti

**Cosa NON fa:**
- Migrazioni di schema (usa Alembic per quello)
- Trasferimento tra DBMS diversi (solo PostgreSQL ↔ PostgreSQL)
- Backup completi (usa `pg_dump` direttamente per quello)

## Quando usarla / Trigger

- L'utente dice "copia i dati", "transfer data", "sync database"
- L'utente vuole allineare il DB locale con dev/staging/prod
- L'utente vuole popolare un ambiente con dati reali

## Prerequisiti

- `psql` e `pg_dump` installati e raggiungibili da PATH
- `python3` con `psycopg2`, `boto3`, `rich`, `click` disponibili
- Se source/dest è un ARN: AWS CLI configurata con profilo corretto
- Connettività di rete verso entrambi i database

## Loop conversazionale

### Step 1 — Source e Destination

Chiedi all'utente:
- **Da dove** vuoi copiare i dati? (source)
- **Verso dove** vuoi copiarli? (destination)

**Auto-discovery**: se il progetto ha `aws-config.yaml` nella KB (`projects/[nome]/`),
proponi le opzioni disponibili:
- `prod → locale` (ARN prod → .env locale)
- `dev → locale` (ARN dev → .env locale)
- `prod → dev` (ARN → ARN)

Formati accettati per source e destination:
| Formato | Esempio |
|---|---|
| ARN AWS Secrets Manager | `arn:aws:secretsmanager:eu-west-1:...` |
| URL PostgreSQL diretto | `postgresql://user:pass@host:5432/db` |
| File .env | `backend/envs/dev.env` |
| Shortcut progetto | `prod`, `dev`, `locale` (risolti da aws-config.yaml) |

Per ogni shortcut, risolvi usando `aws-config.yaml`:
- `prod` → usa l'ARN dal blocco `prod` (formato: `arn:aws:secretsmanager:{region}:{account_id}:secret:{app_name}-prod-db`)
- `dev` → usa l'ARN dal blocco `dev`
- `locale` → usa il file `.env` locale del progetto o URL `postgresql://app:app@localhost:5432/app`

### Step 2 — Verifica connessione e confronto schema

Esegui `compare_schemas.py` (nella cartella della skill):

```bash
python3 skills/development/db-transfer/compare_schemas.py \
  --source "<SOURCE>" --destination "<DESTINATION>" \
  [--src-profile "<PROFILE>"] [--dest-profile "<PROFILE>"]
```

Lo script:
1. Si connette a entrambi i database
2. Elenca schema e tabelle di entrambi
3. Per ogni tabella presente in entrambi: confronta colonne, tipi, nullable
4. Produce un report con:
   - Tabelle solo nel source
   - Tabelle solo nella destination
   - Tabelle con differenze di schema (colonne mancanti, tipi diversi)

**Se ci sono discrepanze**:
- Mostra il report all'utente
- Chiedi se vuole procedere comunque (le tabelle con schema diverso potrebbero fallire)
- Suggerisci di allineare gli schema prima (migrazioni Alembic)

**Se non ci sono discrepanze**: conferma che gli schema sono allineati e procedi.

### Step 3 — Selezione tabelle

Mostra all'utente la lista delle tabelle disponibili nel source, raggruppate per schema,
con per ognuna:
- **Row count** (numero di righe)
- **Dimensione stimata** (da `pg_total_relation_size`)

Formato:
```
Schema: template (5 tabelle, ~12.340 righe totali)
  template.users          1.234 righe    ~2.1 MB
  template.roles             12 righe    ~16 KB
  ...

Schema: prs (8 tabelle, ~456.789 righe totali)
  prs.predictions       234.567 righe   ~45.2 MB
  ...
```

Chiedi: *"Quali tabelle vuoi trasferire? Puoi specificare:"*
- *Schema intero: `template.*`, `prs.*`*
- *Tabelle singole: `template.users`, `prs.predictions`*
- *Mix: `template.*`, `prs.predictions`, `prs.suggestions_*`*
- *Tutte: `*.*`*

### Step 4 — Conferma piano di esecuzione

Mostra il riepilogo prima di eseguire:

```
Piano di trasferimento:
  Source:      postgresql://...@prod:5432/app (via ARN)
  Destination: postgresql://app:***@localhost:5432/app

  Tabelle selezionate: 15
  Righe stimate:       ~45.000
  Dimensione stimata:  ~120 MB

  Ordine (per FK):
    1. template.roles
    2. template.permissions
    3. template.users
    ...

  Opzioni:
    Truncate destination: Sì/No
    Replace DB host:      Sì (db → localhost)
```

Chiedi:
- *"Vuoi fare truncate delle tabelle destination prima della copia?"*
  (consigliato se si vuole un allineamento pulito)
- *"Confermi l'esecuzione?"*

### Step 5 — Esecuzione

Esegui `transfer_data.py` (nella cartella della skill):

```bash
python3 skills/development/db-transfer/transfer_data.py \
  "<SOURCE>" "<DESTINATION>" \
  -t "pattern1" -t "pattern2" \
  [--truncate] \
  [--src-profile-name "<PROFILE>"] \
  [--dest-profile-name "<PROFILE>"] \
  [--no-replace-db-host] \
  --print-src-tables \
  -y
```

**Nota**: passa `-y` per conferma automatica (l'utente ha già confermato nello step 4).

Monitora l'output e riporta all'utente:
- Progresso tabella per tabella
- Eventuali errori
- Row count finale source vs destination

### Step 6 — Verifica post-trasferimento

Dopo l'esecuzione, mostra un riepilogo:

```
Risultato trasferimento:
  ✅ 14/15 tabelle copiate con successo
  ❌ 1 errore: template.ticket_attachments (FK violation)

  Confronto row count:
    Tabella                    Source    Dest    Match
    template.users              1.234   1.234   ✅
    template.roles                 12      12   ✅
    prs.predictions           234.567 234.567   ✅
    ...
```

Se ci sono errori, suggerisci possibili soluzioni (es. truncate + retry, verificare FK).

## Checklist qualità

- [ ] Source e destination verificati (connessione OK)
- [ ] Schema confrontati e discrepanze segnalate
- [ ] Tabelle selezionate dall'utente (non default hardcoded)
- [ ] Ordine FK calcolato (non ordine alfabetico)
- [ ] Conferma esplicita prima di qualsiasi operazione distruttiva
- [ ] Row count verificato post-trasferimento
