---
progetto: "jubatus"
data: "2026-04-10"
tags:
  - "#progetto:jubatus"
  - "#fase:dev"
  - "#infra"
---

# Log Setup Infrastruttura — 10 aprile 2026

> Registro di tutto ciò che è stato fatto durante la sessione di setup infra su AWS account Jubatus.

---

## Stato iniziale

- Account AWS: `776126712875`, regione `eu-central-1`, profilo `jubatus-dev`
- Stack `dev-jubatus-stack` in stato `UPDATE_ROLLBACK_COMPLETE` (broken)
- Backend non si avviava per errore `ResourceNotFoundException` sul segreto DB
- SSM Parameter Store `/dev/jubatus` creato in `eu-west-1` (regione sbagliata)
- App name: `jubatus` (il cliente non vuole questo nome nelle risorse)

---

## Bug trovati e fixati

### 1. Secret ARN senza suffisso random (CDK)

**File**: `laif-cdk/laif_cdk/stacks/template_stack.py:299`

Il CDK usava `self.db_secret.secret_arn` che restituisce un ARN senza il suffisso random di 6 caratteri (es. `-EJlkMY`). Secrets Manager richiede l'ARN completo oppure il nome friendly.

**Fix**: `self.db_secret_arn = self.db_secret_name` — passa il nome del segreto invece dell'ARN parziale.

### 2. Regione SSM hardcoded nel backend

**File**: `backend/src/template/common/utils/aws.py`

Le funzioni `get_parameter()`, `put_parameter()`, `delete_parameter()` avevano `region_name="eu-west-1"` hardcoded. Su Jubatus (eu-central-1) il parametro SSM non veniva trovato.

**Fix**: `region_name=os.getenv("AWS_DEFAULT_REGION", "eu-west-1")` — legge la regione dall'env var.

### 3. Regione hardcoded in utilities

**File**: `utilities/aws_commons.py`

La funzione `get_session()` aveva `region_name="eu-west-1"` hardcoded. Usata dalla pipeline CI per `store_parameters.py`.

**Fix**: `region_name=os.getenv("AWS_DEFAULT_REGION", "eu-west-1")` + aggiunto `import os`.

### 4. AWS_DEFAULT_REGION mancante nel container ECS

Il CDK non passava `AWS_DEFAULT_REGION` come variabile d'ambiente al container ECS. Anche col fix al codice, il default restava `eu-west-1`.

**Fix**: aggiunto `"AWS_DEFAULT_REGION": self.config.REGION` nel dict `infrastructure_environments` di `template_stack.py`.

---

## Rename app_name: jubatus → support

Il cliente non vuole "jubatus" nei nomi delle risorse AWS. Rinominato `app_name` da "jubatus" a "support".

**File modificati**:
- `jubatus/values.yaml` — `app_name: support`, `app_description: support`
- `jubatus-infra/dev.yaml` — `id: dev-support-stack`, `app_name: support`, `db_name: supportdb`
- `jubatus/docker-compose.yaml` — container names e APP_NAME

**Note**:
- `CUSTOMER_NAME` resta "jubatus" (usato per tag AWS e per il nome del DB/secret)
- Le repo GitHub restano `jubatus` e `jubatus-infra`
- Il DB si chiama `dev-jubatus-db` e il secret `dev-jubatus-db-sysuser-secrets` (usano CUSTOMER_NAME)

---

## Operazioni eseguite

### Distruzione risorse vecchie
1. Svuotati bucket S3: `dev-jubatus-fe-build`, `dev-jubatus-data-bucket`, logging bucket
2. Eliminato stack CloudFormation `dev-jubatus-stack` (con `--retain-resources` per risorse skipped)
3. Eliminato manualmente RDS `dev-jubatus-db` (`--skip-final-snapshot`)
4. Eliminato RDS subnet group orfano
5. Eliminato bucket logging CloudFront orfano
6. Eliminato SSM parameter `/dev/jubatus` da eu-west-1
7. Eliminati SSM parameters `/dev/jubatus/version`, `/dev/jubatus/laif_template_version`, `/dev/jubatus/tms_last_release` da eu-west-1

### Creazione nuove risorse
1. Creato SSM parameter `/dev/support` in eu-central-1 (manualmente via AWS CLI)
2. Aggiornate GitHub env vars (`APP_NAME`, `ECR_REPOSITORY`, `ECS_CLUSTER`, `ECS_SERVICE`, `FRONTEND_BUCKET`)
3. Reinstallato laif-cdk da locale nel venv di jubatus-infra (con i 2 fix)
4. Deploy CDK con `deploy_services: false` → stack `dev-support-stack` creato (50 risorse)
5. Deploy CDK con `deploy_services: true` → ALB, ECS service, listener creati
6. Aggiornato `DISTRIBUTION_ID` su GitHub (`E1IYBDCBKMPJE7`)
7. Registrata task definition v2 con `AWS_DEFAULT_REGION=eu-central-1` (manualmente via AWS CLI)
8. Aggiornata policy IAM `dev-jubatus-github-technical-user-policy` (v3) con nomi "support"

### Pipeline e deploy
1. Commit `3c57f0ad` — rename app configs
2. Commit `3a8e90da` — fix `aws_commons.py` region
3. Commit `a99f3981` (rebased) — fix `template/common/utils/aws.py` region
4. Pipeline GitHub Actions rilanciata → immagine Docker pushata su `dev/support/backend:latest`
5. ECS service raggiunge steady state ✅

---

## Stato finale delle risorse

| Risorsa | ID/Nome |
|---------|---------|
| CF Stack | `dev-support-stack` (CREATE_COMPLETE) |
| VPC | `vpc-0137e5201dcc8ed3d` (temporanea) |
| ALB | `dev-support-be-alb` (temporaneo) |
| ECS | `dev-support-be-cluster` / `dev-support-be-service` (1 task, steady state) |
| ECR | `dev/support/backend` |
| RDS | `dev-jubatus-db` (PostgreSQL 17.6, available) |
| S3 | `dev-support-fe-build`, `dev-support-data-bucket` |
| CloudFront | `E1IYBDCBKMPJE7` |
| ACM | `support-dev.mymemories.it` (PENDING_VALIDATION) |
| Secret | `dev-jubatus-db-sysuser-secrets` |
| SSM | `/dev/support` (eu-central-1) |

---

## Prossimi step

1. **Certificato** — Cliente deve aggiungere CNAME per validazione + CNAME per puntamento CloudFront
2. **Migrazione VPC** — Ricevere VPC ID e subnet dal cliente, aggiornare `dev.yaml` con `vpc_id`
3. **Migrazione ALB** — Ricevere ARN ALB dal cliente, aggiornare `dev.yaml` con `existing_alb`
4. **Fix policy CDK** — Correggere qualifier `cdk-None-*` → `cdk-hnb659fds-*` in `dev-cdk-technical-user-assume-cdk-roles`
5. **Restringere laif_admin** — Dopo migrazione VPC/ALB
6. **Propagare fix CDK** — Committare i fix di `template_stack.py` (secret_name + AWS_DEFAULT_REGION) nella repo laif-cdk

---

## Pagina Notion di riferimento

[Review Infra Jubatus](https://www.notion.so/laifgroup/Review-Infra-Jubatus-33c90ad6ee4880dabadfff781010c237) — contiene review policy IAM, piano migrazione VPC/ALB, e inventario risorse con link alla console AWS.
