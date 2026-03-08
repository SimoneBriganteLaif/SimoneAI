# Infrastruttura AWS — LAIF

← [System.md](../../System.md) · [overview.md](overview.md) · [stack.md](stack.md) · [processi.md](processi.md)

#stack:aws #stack:cdk

## Panoramica

Tutta l'infrastruttura è gestita via **AWS CDK v2** (Python) dal repository `laif-cdk`.

Ogni cliente ha **2 account AWS separati**: dev e prod.

---

## Template Stack — Architettura standard

Ogni progetto viene deployato con il **TemplateStack**, che crea:

```
CloudFront (CDN)
    ↓ (/api/* → Lambda@Edge URL rewriting)
ALB (Application Load Balancer)
    ↓
ECS Cluster (EC2-based, NO Fargate)
├── EC2 Auto Scaling Group (Capacity Provider)
│   └── Backend container (Docker, FastAPI)
├── RDS PostgreSQL (15-17)
├── S3 Data Bucket (file storage)
└── S3 Frontend Bucket (static assets)
```

### Risorse create

| Componente | Risorsa AWS | Note |
|------------|-------------|------|
| Networking | VPC 10.0.0.0/16, multi-AZ | Subnet pubbliche/private |
| Compute | ECS Cluster + EC2 ASG | Default: t4g.small, max 2 istanze |
| Database | RDS PostgreSQL | Default: t4g.micro, 20 GB |
| Storage | 2 bucket S3 | Data (privato) + Frontend |
| CDN | CloudFront | Con Lambda@Edge per URL rewriting |
| Load Balancer | ALB | Health check su backend |
| Registry | ECR | Max 5 immagini (lifecycle policy) |
| Sicurezza | Security Groups, IAM Roles | Permessi fine-grained |
| Segreti | AWS Secrets Manager | Credenziali DB |
| DNS | Route 53 | Opzionale |
| WAF | AWS WAFv2 | Opzionale, rate limiting |

### Scaling

- **Capacity Provider** con EC2 Auto Scaling Group
- **No scaling orizzontale**: le applicazioni servono pochi utenti (PMI, uso interno)
- Managed scaling abilitato ma capacità limitata (max 2 istanze)
- **Auto-turnoff** disponibile: spegne ECS e RDS fuori orario (per dev)

---

## Configurazione per ambiente

Ogni progetto ha due file YAML:

```yaml
# dev.yaml
CUSTOMER_NAME: "nome-cliente"
ACCOUNT_ID: "111111111111"
REGION: eu-west-1
default_stack:
  id: dev-nome-app-stack
  app_name: nome-app
  domain: nome-app.app.laifgroup.com
  db_name: nome_db
  deploy_services: true
  auto_turnoff: true          # ← solo dev

# prod.yaml
ACCOUNT_ID: "222222222222"
REGION: eu-west-1
default_stack:
  id: prod-nome-app-stack
  deploy_services: true
  auto_turnoff: false         # ← mai in prod
```

### Deploy

```bash
# Dev
cdk deploy --all -c env=dev --profile cliente-dev

# Prod
cdk deploy --all -c env=prod --profile cliente-prod
```

---

## Stack opzionali

| Stack | Scopo | Stato |
|-------|-------|-------|
| WAF Stack | Rate limiting, IP whitelist | Usato occasionalmente |
| ETL Stack | Pipeline ETL su Fargate | Disponibile |
| Queue Stack | Code SQS | Disponibile |
| Remote Stack | Bastion host per accesso DB | Disponibile |
| AutoTurnOff | Spegnimento notturno risorse | Usato per dev |

---

## Progetto futuro

Simone vuole ricreare l'infrastruttura da zero usando **CDK v3**, mantenendo lo stesso pattern ma con codice più pulito e meglio documentato. Progetto già avviato ma non completato.

---

## Convenzioni naming risorse AWS

```
Stack:    {env}-{app_name}-{component}-{type}
Risorse:  {env}-{app_name}-{component}-{resource}
Esempio:  dev-myapp-be-cluster, prod-myapp-rds-db
```
