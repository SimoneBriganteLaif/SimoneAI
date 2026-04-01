---
tags: ["#progetto:jubatus", "#fase:dev"]
---

# Piano di azione — Setup infrastruttura Jubatus

**Creato**: 20/03/2026
**Stato**: In preparazione
**Obiettivo**: Deploy dell'applicazione Jubatus sull'account AWS del cliente

---

## Fase 1 — Raccolta informazioni dal cliente

Prima della sessione operativa, servono dal cliente:

| Info | Necessaria per | Stato |
|------|---------------|-------|
| VPC ID | Import VPC nel CDK | Da richiedere |
| Lista subnet (public/private) + AZ | Piazzamento risorse | Da richiedere |
| Conferma Internet Gateway | ALB internet-facing | Da richiedere |
| ARN/nome ALB esistente | Riutilizzo load balancer | Da richiedere |
| Credenziali utenza tecnica AWS | Deploy CDK | Da richiedere |
| Dominio email supporto | Configurazione SES | Da richiedere |

---

## Fase 2 — Modifica CDK: supporto ALB esistente

**Problema**: il CDK LAIF crea sempre un nuovo ALB. Il cliente vuole riutilizzare l'ALB esistente.

**File da modificare**: `core/laif-cdk/laif_cdk/constructs/ecs.py`

**Modifiche necessarie**:

1. Aggiungere parametro opzionale `existing_alb` a `add_application_load_balanced_service()` (linea 545)
2. Se `existing_alb` è fornito:
   - Importare ALB con `elb.ApplicationLoadBalancer.from_lookup()` o passare direttamente l'oggetto
   - Saltare la creazione di ALB e security group dedicato
   - Creare solo un nuovo listener + target group sull'ALB importato
3. Se `existing_alb` non è fornito: comportamento attuale (crea nuovo ALB)

**File collegati da aggiornare**:
- `stacks/template_stack.py`: passare parametro `existing_alb` se configurato
- `app.py` (jubatus-infra): configurare l'ARN dell'ALB nel setup

**Note**:
- Verificare che il listener port non sia già occupato sull'ALB esistente
- Il security group dell'ALB esistente deve permettere traffico da CloudFront
- Potrebbe servire aggiungere una regola ingress al SG dell'ALB per il prefix list CloudFront

---

## Fase 3 — Creazione repo `jubatus-infra`

Basata su `voltan-infra` come riferimento.

### `dev.yaml`

```yaml
CUSTOMER_NAME: jubatus
ACCOUNT_ID: <da-richiedere>
PROFILE_NAME: jubatus-dev
REGION: eu-west-1  # da confermare con cliente

default_stack:
  id: dev-jubatus-stack
  app_name: jubatus
  certificate_arn: <da-creare-o-richiedere>
  domain: <da-definire>
  deploy_services: true
  backend_cluster_instance_type: t4g.small
  rds_instance_type: t4g.micro
  db_name: jubatusdb
  auto_turnoff: true  # per ambiente dev
  # VPC del cliente
  vpc_id: <da-richiedere>
  # ALB del cliente
  existing_alb_arn: <da-richiedere>
```

### `prod.yaml`

Come dev ma con:
- `auto_turnoff: false`
- Istanze più grandi (t4g.small → t4g.medium per backend, t4g.micro → t4g.small per RDS)
- WAF abilitato

---

## Fase 4 — Lista permessi AWS

Permessi necessari per l'utenza tecnica, raggruppati per servizio:

### Permessi completi (CRUD)

| Servizio | Motivo |
|----------|--------|
| CloudFormation | CDK crea/aggiorna stack |
| ECS | Cluster, servizi, task definitions |
| ECR | Push immagini Docker |
| RDS | Creazione istanza PostgreSQL |
| S3 | Bucket frontend + data |
| CloudFront | Distribuzione CDN |
| IAM | Ruoli per ECS, Lambda |
| Lambda | Funzioni edge + auto-turnoff |
| Secrets Manager | Credenziali DB |
| SSM Parameter Store | Configurazione cross-stack |
| CloudWatch | Logs e metriche |
| SES | Invio email |
| ACM | Certificati SSL |

### Permessi in lettura

| Servizio | Motivo |
|----------|--------|
| EC2 (VPC, subnet, SG) | Lookup VPC esistente |
| ELB (ALB) | Import ALB esistente |
| Route53 | Se dominio gestito su AWS |

### Approccio consigliato

1. **Setup iniziale**: policy `AdministratorAccess` o policy custom ampia
2. **Post-setup**: analisi CloudTrail per identificare permessi effettivamente usati
3. **Produzione**: policy restrittiva basata su least-privilege

---

## Fase 5 — Setup SES

1. **Verifica dominio**: aggiungere record DNS (DKIM, SPF) per il dominio del cliente
2. **Uscita dalla sandbox SES**: richiedere production access se l'account è nuovo
3. **Casella ricezione**: il cliente crea casella dedicata (es. `supporto-cc@jubatus.it`)
4. **Configurazione invio**: IAM policy per il backend ECS per inviare come `supporto@jubatus.it`
5. **Inoltro test**: configurare inoltro automatico dalla casella del cliente alla nostra per testing

---

## Fase 6 — Sessione operativa (prossima settimana)

Agenda proposta:

1. **Verifica accessi**: test utenza tecnica + console
2. **Ispezione VPC**: conferma subnet, Internet Gateway, routing tables
3. **Ispezione ALB**: conferma ARN, listener disponibili, security group
4. **Bootstrap CDK**: `cdk bootstrap` sull'account del cliente
5. **Primo deploy**: stack dev su ambiente di test
6. **Verifica**: frontend raggiungibile, backend healthcheck OK, DB connesso
7. **SES**: inizio configurazione email

---

## Checklist pre-sessione

- [ ] Ricevute credenziali AWS dal cliente
- [ ] Ricevuto VPC ID e info subnet
- [ ] Ricevuto ARN ALB esistente
- [ ] Modifica CDK per ALB esistente completata e testata
- [ ] Repo `jubatus-infra` creata con config base
- [ ] Lista permessi inviata al cliente
- [ ] Sessione operativa fissata
