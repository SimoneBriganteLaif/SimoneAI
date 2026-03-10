# Indice Tag

Tutti i tag usati nella knowledge base. Aggiornato dalla skill `maintenance/audit-periodico/SKILL.md`.

---

## Come cercare

1. Trova il tag nella categoria rilevante
2. Clicca sui file elencati per quel tag
3. Oppure usa grep: `grep -r "#tag:valore" /path/to/KnowledgeBase`

---

## Tag per Progetto (`#progetto:`)

| Tag | File che lo usano |
|-----|-----------------|
| `#progetto:jubatus` | projects/jubatus/README.md, projects/jubatus/requisiti.md, projects/jubatus/architettura.md, projects/jubatus/decisioni.md, projects/jubatus/feature-log.md, projects/jubatus/stato-progetto.md, projects/jubatus/permessi-aws.md, projects/jubatus/meeting/*.md |
| `#progetto:lamonea` | projects/lamonea/README.md, projects/lamonea/requisiti.md, projects/lamonea/architettura.md, projects/lamonea/decisioni.md, projects/lamonea/feature-log.md, projects/lamonea/stato-progetto.md, projects/lamonea/allegato-tecnico.md, projects/lamonea/mockup-brief.md, projects/lamonea/manutenzione.md, projects/lamonea/aws-config.yaml, projects/lamonea/meeting/*.md |
| `#progetto:umbra` | projects/umbra/README.md, projects/umbra/requisiti.md, projects/umbra/architettura.md, projects/umbra/decisioni.md, projects/umbra/feature-log.md, projects/umbra/stato-progetto.md, projects/umbra/allegato-tecnico.md, projects/umbra/mockup-brief.md, projects/umbra/manutenzione.md, projects/umbra/aws-config.yaml, projects/umbra/meeting/*.md, projects/umbra/windsurf-briefs/*.md |

---

## Tag per Industria (`#industria:`)

| Tag | File che lo usano |
|-----|-----------------|
| `#industria:retail` | |
| `#industria:finance` | |
| `#industria:healthcare` | projects/lamonea/, knowledge/industrie/healthcare.md |
| `#industria:saas` | |
| `#industria:marketplace` | |
| `#industria:enterprise` | |
| `#industria:software` | knowledge/azienda/ |
| `#industria:entertainment` | projects/jubatus/, knowledge/industrie/entertainment.md |
| *(aggiungi nuove industrie qui)* | |

---

## Tag per Fase (`#fase:`)

| Tag | Descrizione |
|-----|------------|
| `#fase:presales` | Documenti di presales (requisiti, allegati, mockup) |
| `#fase:dev` | Documenti di sviluppo (ADR, feature log, architettura) |
| `#fase:manutenzione` | Note post go-live |
| `#fase:contesto` | Conoscenza aziendale/contestuale (knowledge/azienda/) |
| `#fase:development` | Skill di sviluppo (feature-workflow, windsurf-feedback, ecc.) |

---

## Tag per Pattern (`#pattern:`)

| Tag | File pattern |
|-----|------------|
| `#pattern:orm` | patterns/sqlalchemy-joinedload-unique.md |
| `#pattern:api` | patterns/fastapi-route-order.md |
| `#pattern:workflow` | patterns/fullstack-dev-preview-loop.md |
| `#pattern:database` | patterns/sqlalchemy-joinedload-unique.md |
| `#pattern:performance` | patterns/list-detail-lazy-loading.md |
| `#pattern:sicurezza` | patterns/html-sanitization-dompurify.md |
| `#pattern:integrazione` | patterns/dayjs-isoweek-manipulate-mapping.md |

---

## Tag per Problema (`#problema:`)

| Tag | File |
|-----|------|
| `#problema:serializzazione` | patterns/sqlalchemy-joinedload-unique.md, knowledge/problemi-tecnici/query-n-plus-1.md |
| `#problema:integrazione` | patterns/fullstack-dev-preview-loop.md |
| `#problema:routing` | patterns/fastapi-route-order.md, knowledge/problemi-tecnici/routing-conflitti-parametrici.md |
| `#problema:performance` | patterns/list-detail-lazy-loading.md, knowledge/problemi-tecnici/query-n-plus-1.md |
| `#problema:xss` | patterns/html-sanitization-dompurify.md, knowledge/problemi-tecnici/xss-contenuto-esterno.md |
| `#problema:sicurezza` | knowledge/problemi-tecnici/xss-contenuto-esterno.md |
| `#problema:integrazione` | knowledge/problemi-tecnici/laif-ds-type-export.md |
| `#knowledge:azienda` | knowledge/azienda/laif-ds-local-link.md |

---

## Tag per Stack (`#stack:`)

| Tag | File che lo usano |
|-----|-----------------|
| `#stack:nextjs` | patterns/fullstack-dev-preview-loop.md, knowledge/problemi-tecnici/xss-contenuto-esterno.md |
| `#stack:react` | patterns/list-detail-lazy-loading.md, patterns/html-sanitization-dompurify.md, knowledge/problemi-tecnici/xss-contenuto-esterno.md |
| `#stack:nodejs` | |
| `#stack:typescript` | |
| `#stack:postgresql` | |
| `#stack:supabase` | |
| `#stack:vercel` | |
| `#stack:aws` | skills/development/aws-diagnostics/ |
| `#stack:fastapi` | knowledge/azienda/stack.md, patterns/fastapi-route-order.md, patterns/fullstack-dev-preview-loop.md, patterns/list-detail-lazy-loading.md, knowledge/problemi-tecnici/query-n-plus-1.md, knowledge/problemi-tecnici/routing-conflitti-parametrici.md |
| `#stack:sqlalchemy` | patterns/sqlalchemy-joinedload-unique.md, knowledge/problemi-tecnici/query-n-plus-1.md |
| `#stack:dayjs` | patterns/dayjs-isoweek-manipulate-mapping.md |
| `#stack:laif-ds` | knowledge/azienda/laif-ds-local-link.md, knowledge/problemi-tecnici/laif-ds-type-export.md, patterns/dayjs-isoweek-manipulate-mapping.md |
| `#stack:npm` | knowledge/azienda/laif-ds-local-link.md |
| `#stack:cdk` | knowledge/azienda/infrastruttura.md, projects/jubatus/permessi-aws.md |
| `#stack:ecs` | skills/development/aws-diagnostics/aws-ecs-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| `#stack:rds` | skills/development/aws-diagnostics/aws-rds-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| `#stack:cloudwatch` | skills/development/aws-diagnostics/aws-logs-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| `#stack:s3` | skills/development/aws-diagnostics/aws-s3-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| *(aggiungi nuovi stack qui)* | |

---

*Ultimo aggiornamento: 2026-03-10*
