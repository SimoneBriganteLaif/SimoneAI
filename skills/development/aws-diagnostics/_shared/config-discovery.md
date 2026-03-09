---
tags: ["#stack:aws", "#fase:dev"]
---

# Procedura: Generazione aws-config.yaml

Questa procedura genera il file `projects/[nome]/aws-config.yaml` per un progetto LAIF, derivando i nomi delle risorse AWS dalle convenzioni CDK.

---

## Quando eseguirla

- La prima volta che si usa una skill `aws-diagnostics/` su un progetto
- Se i nomi delle risorse cambiano (es. dopo un re-deploy con nuovi parametri CDK)

---

## Prerequisiti

- [ ] Il progetto esiste in `projects/[nome]/`
- [ ] La repository del progetto e' clonata localmente
- [ ] AWS CLI configurata con i profili necessari

---

## Procedura

### Step 1 — Trova il path della repository

Leggi `projects/[nome]/README.md` e cerca il campo "Repository codice" o "repo_path".
Se non indicato, chiedi all'utente.

### Step 2 — Leggi i file CDK config

Cerca nella root della repository:
- `dev.yaml` — configurazione ambiente dev
- `prod.yaml` — configurazione ambiente prod

Ogni file contiene:
```yaml
CUSTOMER_NAME: "nome-cliente"
ACCOUNT_ID: "111111111111"
REGION: eu-west-1
default_stack:
  app_name: nome-app
  # ... altri parametri
```

### Step 3 — Estrai i parametri chiave

Da ogni file CDK config estrai:
- `CUSTOMER_NAME` — nome del cliente
- `ACCOUNT_ID` — ID account AWS
- `REGION` — regione (es. `eu-west-1`)
- `default_stack.app_name` — nome applicazione

### Step 4 — Deriva i nomi risorse

Applica le convenzioni di naming dal CDK LAIF:

| Risorsa | Pattern | Note |
|---------|---------|------|
| ECS Cluster | `{env}-{app_name}-cluster` | |
| ECS Service | `{env}-{app_name}-be-service` | |
| ECS Task Family | `{env}-{app_name}-be-task` | |
| Log Group | `{env}-{app_name}-be-task-log-group` | |
| RDS Identifier | `{env}-{customer_name}-db` | Usa `customer_name`, NON `app_name` |
| S3 Data Bucket | `{env}-{app_name}-data` | Nome bucket root "data" |
| S3 Frontend | `{env}-{app_name}-fe-frontend` | Nome bucket root "frontend" |
| ALB | `{env}-{app_name}-be-alb` | |

### Step 5 — Chiedi i profili AWS

I profili AWS CLI sono configurazioni locali, non derivabili dal CDK.
Chiedi all'utente:
- Profilo per l'ambiente dev (es. `cliente-dev`)
- Profilo per l'ambiente prod (es. `cliente-prod`)

### Step 6 — Genera il file

Scrivi `projects/[nome]/aws-config.yaml`:

```yaml
# AWS Config per [nome progetto]
# Generato da: skills/development/aws-diagnostics/_shared/config-discovery.md
# Nomi risorse derivati dalle convenzioni CDK LAIF.
# Modificabile manualmente se le risorse hanno nomi custom.

environments:
  dev:
    aws_profile: "cliente-dev"
    region: "eu-west-1"
    account_id: "111111111111"
    app_name: "nome-app"
    customer_name: "nome-cliente"
    resources:
      ecs_cluster: "dev-nome-app-cluster"
      ecs_service: "dev-nome-app-be-service"
      ecs_task_family: "dev-nome-app-be-task"
      log_group: "dev-nome-app-be-task-log-group"
      rds_identifier: "dev-nome-cliente-db"
      s3_data_bucket: "dev-nome-app-data"
      s3_frontend_bucket: "dev-nome-app-fe-frontend"
      alb_name: "dev-nome-app-be-alb"
  prod:
    aws_profile: "cliente-prod"
    region: "eu-west-1"
    account_id: "222222222222"
    app_name: "nome-app"
    customer_name: "nome-cliente"
    resources:
      ecs_cluster: "prod-nome-app-cluster"
      ecs_service: "prod-nome-app-be-service"
      ecs_task_family: "prod-nome-app-be-task"
      log_group: "prod-nome-app-be-task-log-group"
      rds_identifier: "prod-nome-cliente-db"
      s3_data_bucket: "prod-nome-app-data"
      s3_frontend_bucket: "prod-nome-app-fe-frontend"
      alb_name: "prod-nome-app-be-alb"
```

### Step 7 — Conferma con l'utente

Mostra il file generato e chiedi conferma prima di salvare.
Se il progetto ha risorse con nomi custom (es. RDS con identificatore diverso), l'utente puo' modificare manualmente.

---

## Casi speciali

### Progetto con worker (BackendWithWorkersV1)

Se il progetto usa worker Celery, aggiungi:
```yaml
resources:
  # ... risorse standard ...
  worker_service: "{env}-{app_name}-worker-service"
  worker_log_group: "{env}-{app_name}-worker-task-log-group"
  scheduler_service: "{env}-{app_name}-scheduler-service"
```

### RDS con identificatore custom

Se il CDK config ha `rds_identifier` custom:
```yaml
default_stack:
  rds_identifier: "custom-name"
```
Allora: `{env}-{customer_name}-{rds_identifier}-db`

### Multipli bucket S3

Se il progetto ha bucket aggiuntivi oltre data e frontend, aggiungerli manualmente.
