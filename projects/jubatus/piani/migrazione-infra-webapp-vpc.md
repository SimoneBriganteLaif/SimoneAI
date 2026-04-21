---
progetto: "jubatus"
data: "2026-04-14"
tags:
  - "#progetto:jubatus"
  - "#fase:dev"
  - "#infra"
  - "#migrazione"
---

# Piano Migrazione Infra — webapp_vpc

> Dalla call "Jubatus - Update Infra #2" del 14/04/2026.
> Deadline: martedì 22/04/2026.

## Obiettivo

Migrare l'infrastruttura Jubatus (support) dalla VPC CDK-created alla VPC condivisa `webapp_vpc`, condividendo l'ALB con photo-uploader, mettendo RDS in subnet private e configurando SSL con dominio custom.

## Stato attuale → desiderato

| Risorsa | Attuale | Desiderato |
|---------|---------|------------|
| VPC | `vpc-0137e5201dcc8ed3d` (3 subnet pubbliche) | `vpc-0d40b276a0ce7d4e3` (2 pub + 2 private) |
| RDS | PubliclyAccessible=YES, subnet pubbliche | Subnet **private**, non accessibile pubblicamente |
| ALB | `dev-support-be-alb` dedicato, HTTP:80 | ALB condiviso `alb-photo-uploader-218746`, porta **8088** |
| CloudFront | No dominio custom, origin porta 80 | `support-dev.mymemories.it`, cert SSL, origin porta **8088** |
| Tags | Solo Environment + Customer | + `CostCenter=support` |

## Valori AWS

- Certificato: `arn:aws:acm:us-east-1:776126712875:certificate/470f4195-2d55-4f47-aeca-42eb25bab273`
- ALB ARN: `arn:aws:elasticloadbalancing:eu-central-1:776126712875:loadbalancer/app/alb-photo-uploader-218746/bd32e812903e9789`
- ALB DNS: `alb-photo-uploader-218746-2052265039.eu-central-1.elb.amazonaws.com`
- ALB SG: `sg-0cc8a72edb5e351b4`

## Problemi identificati

1. **CRITICO**: subnet pubbliche di webapp_vpc hanno `MapPublicIpOnLaunch=false` → EC2 senza internet. Fix: abilitare auto-assign IP prima del deploy.
2. Subnet private senza NAT → CDK le classifica come `PRIVATE_ISOLATED` (non `PRIVATE_WITH_EGRESS`).
3. CloudFront `LoadBalancerV2Origin` non supportava porta custom → aggiunto `http_port` a laif-cdk.

## Modifiche effettuate

### laif-cdk
- `template_stack.py`: aggiunto parametro `rds_subnet_type` per placement RDS indipendente
- `cloudfront.py`: aggiunto `http_port` a `LoadBalancerV2Origin` per porta custom
- `template_stack.py`: passaggio `listener_port` come `origin_http_port` a CloudFront

### jubatus-infra
- `dev.yaml`: configurato `vpc_id`, `existing_alb`, `listener_port: 8088`, `certificate_arn`, `rds_subnet_type: PRIVATE_ISOLATED`
- `app.py`: passato `rds_subnet_type` a TemplateStack, aggiunto tag `CostCenter=support`

## Passi pre-deploy

1. Abilitare `MapPublicIpOnLaunch` sulle subnet pubbliche di webapp_vpc
2. `cdk context --clear` per pulire cache lookup VPC
3. `cdk diff` per verificare i cambiamenti

## Passi post-deploy

1. Aggiornare DNS CNAME `support-dev.mymemories.it`
2. Verificare ECS, RDS, ALB:8088, CloudFront, photo-uploader (regression)
3. Cleanup vecchia VPC e risorse orfane
