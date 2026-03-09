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
| `#progetto:jubatus` | projects/jubatus/README.md, projects/jubatus/requisiti.md, projects/jubatus/architettura.md, projects/jubatus/decisioni.md, projects/jubatus/feature-log.md, projects/jubatus/stato-progetto.md, projects/jubatus/meeting/*.md |
| `#progetto:lamonea` | projects/lamonea/README.md, projects/lamonea/requisiti.md, projects/lamonea/architettura.md, projects/lamonea/decisioni.md, projects/lamonea/feature-log.md, projects/lamonea/stato-progetto.md, projects/lamonea/allegato-tecnico.md, projects/lamonea/mockup-brief.md, projects/lamonea/manutenzione.md, projects/lamonea/aws-config.yaml, projects/lamonea/meeting/*.md |

---

## Tag per Industria (`#industria:`)

| Tag | File che lo usano |
|-----|-----------------|
| `#industria:retail` | |
| `#industria:finance` | |
| `#industria:healthcare` | projects/lamonea/ |
| `#industria:saas` | |
| `#industria:marketplace` | |
| `#industria:enterprise` | |
| `#industria:software` | knowledge/azienda/ |
| `#industria:entertainment` | projects/jubatus/ |
| *(aggiungi nuove industrie qui)* | |

---

## Tag per Fase (`#fase:`)

| Tag | Descrizione |
|-----|------------|
| `#fase:presales` | Documenti di presales (requisiti, allegati, mockup) |
| `#fase:dev` | Documenti di sviluppo (ADR, feature log, architettura) |
| `#fase:manutenzione` | Note post go-live |
| `#fase:contesto` | Conoscenza aziendale/contestuale (knowledge/azienda/) |

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

---

## Tag per Problema (`#problema:`)

| Tag | File |
|-----|------|
| `#problema:serializzazione` | patterns/sqlalchemy-joinedload-unique.md |
| `#problema:integrazione` | patterns/fullstack-dev-preview-loop.md |
| `#problema:routing` | patterns/fastapi-route-order.md |
| `#problema:performance` | patterns/list-detail-lazy-loading.md |
| `#problema:xss` | patterns/html-sanitization-dompurify.md |

---

## Tag per Stack (`#stack:`)

| Tag | File che lo usano |
|-----|-----------------|
| `#stack:nextjs` | patterns/fullstack-dev-preview-loop.md |
| `#stack:react` | patterns/list-detail-lazy-loading.md, patterns/html-sanitization-dompurify.md |
| `#stack:nodejs` | |
| `#stack:typescript` | |
| `#stack:postgresql` | |
| `#stack:supabase` | |
| `#stack:vercel` | |
| `#stack:aws` | skills/development/aws-diagnostics/ |
| `#stack:fastapi` | knowledge/azienda/stack.md, patterns/fastapi-route-order.md, patterns/fullstack-dev-preview-loop.md, patterns/list-detail-lazy-loading.md |
| `#stack:sqlalchemy` | patterns/sqlalchemy-joinedload-unique.md |
| `#stack:cdk` | knowledge/azienda/infrastruttura.md |
| `#stack:ecs` | skills/development/aws-diagnostics/aws-ecs-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| `#stack:rds` | skills/development/aws-diagnostics/aws-rds-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| `#stack:cloudwatch` | skills/development/aws-diagnostics/aws-logs-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| `#stack:s3` | skills/development/aws-diagnostics/aws-s3-diagnose/, skills/development/aws-diagnostics/aws-triage/ |
| *(aggiungi nuovi stack qui)* | |

---

*Ultimo aggiornamento: 2026-03-09*
