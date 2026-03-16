# Horizontal Scaling

| Campo     | Valore           |
|-----------|------------------|
| ID        | 167              |
| Stack     | laif-infra       |
| Tipo      | Roadmap          |
| Status    | Nuova            |
| Priorita  | —                |
| Target    | 20-24 Apr 2026   |

## Descrizione originale

Horizontal Scaling

## Piano di risoluzione

1. **Audit componenti stateful** — Analizzare l'architettura attuale per identificare tutto cio che impedisce lo scaling orizzontale:
   - Sessioni in memoria (JWT va bene, session server-side no)
   - Upload file su filesystem locale
   - Cache in-memory (es. dizionari Python)
   - Scheduled task / cron che non devono duplicarsi
   - WebSocket connections (se presenti)

2. **Esternalizzare le sessioni** — Se ci sono sessioni server-side, spostarle su Redis (ElastiCache) o DynamoDB. Se si usa solo JWT stateless, verificare che non ci siano dati di sessione salvati in memoria.

3. **Configurare ECS auto-scaling** — Aggiungere scaling policy al servizio ECS:
   - Target tracking su CPU (es. target 60%)
   - Target tracking su memoria (es. target 70%)
   - Min capacity: 1, max capacity: da definire per progetto
   - Cooldown period per evitare flapping

4. **Application Load Balancer con health checks** — Verificare/configurare:
   - Health check endpoint dedicato (`/health` o `/api/health`)
   - Deregistration delay appropriato
   - Sticky sessions solo se strettamente necessario (preferibilmente no)

5. **Connection pooling database** — Con piu istanze, le connessioni DB si moltiplicano. Soluzioni:
   - **RDS Proxy**: gestione automatica del pool lato AWS
   - **PgBouncer**: sidecar container o servizio dedicato
   - Verificare i limiti di connessione di RDS per il tier in uso

6. **File upload via S3** — Spostare tutti gli upload su S3 (non filesystem locale):
   - Pre-signed URL per upload diretto dal frontend
   - Oppure upload tramite backend con stream verso S3
   - Verificare che il media service gia gestisca S3 (correlato a issue 133)

7. **Considerazioni ETL e job asincroni** — Per task long-running:
   - Usare SQS + worker separato (non inline nel web server)
   - Evitare duplicazione di job schedulati (leader election o SQS FIFO)

8. **Load testing** — Prima e dopo lo scaling:
   - Tool: k6, Locust o Artillery
   - Scenario: carico progressivo fino a N utenti concorrenti
   - Misurare: latenza p50/p95/p99, error rate, tempo di scale-out

9. **Cost modeling** — Stimare i costi per i diversi scenari di scaling:
   - Baseline (1 istanza) vs picco (N istanze)
   - Costo RDS Proxy o ElastiCache aggiuntivo
   - Confronto Fargate vs EC2 per workload scaled

## Stima effort

**Effort significativo, da suddividere in sprint** — Stima complessiva: 40-60 ore
- Audit e piano dettagliato (~4h)
- Esternalizzazione sessioni/cache (~8h)
- Configurazione ECS auto-scaling (~8h)
- Connection pooling DB (~8h)
- Migrazione file upload a S3 (~8h, dipende da stato attuale)
- Load testing e tuning (~8h)
- Cost modeling e documentazione (~4h)
