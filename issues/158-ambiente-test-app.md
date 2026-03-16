# Ambiente Test App

| Campo     | Valore           |
|-----------|------------------|
| ID        | 158              |
| Stack     | laif-infra       |
| Tipo      | Proposal         |
| Status    | Backlog          |
| Priorita  | —                |

## Descrizione originale

Oltre ad ambiente di DEV e PROD e necessaria possibilita di creare un ambiente di TEST dove poter ogni volta brasare e ricostruire da zero il database, eventualmente importando dati da database di DEV o PROD.

## Piano di risoluzione

1. **Clonare la stack CDK dell'ambiente DEV per TEST** — Creare una nuova stack CDK basata su quella DEV, parametrizzata per ambiente. L'ambiente TEST deve avere le stesse risorse (ECS, RDS, S3) ma con istanze piu piccole per contenere i costi.

2. **Automazione reset database** — Creare uno script (o comando `just`) per:
   - Drop completo dello schema applicativo
   - Ricreare lo schema da zero (migrazioni Alembic da zero)
   - Seed dei dati di base (utenti admin, configurazioni)
   - Deve essere eseguibile con un singolo comando, senza intervento manuale

3. **Import dati da DEV o PROD** — Script per importare dati reali (sanitizzati):
   - `pg_dump` dall'ambiente sorgente (DEV o PROD)
   - Sanitizzazione automatica: rimozione/offuscamento di dati sensibili (email, password, dati personali)
   - `pg_restore` sull'ambiente TEST
   - Comando `just`: es. `just test import-db dev` o `just test import-db prod`

4. **Ambiente effimero (creazione/distruzione on-demand)** — L'ambiente TEST non deve restare sempre acceso:
   - Script per `cdk deploy` e `cdk destroy` dell'intera stack TEST
   - Oppure: mantenere la stack ma spegnere ECS tasks e RDS (stop instance)
   - Trigger manuale o da CI/CD

5. **Ottimizzazione costi** — Minimizzare i costi quando l'ambiente non e in uso:
   - RDS: usare istanze `db.t3.micro` o Aurora Serverless v2 (scala a zero)
   - ECS: desired count = 0 quando non in uso
   - Auto-shutdown dopo N ore di inattivita (CloudWatch alarm + Lambda)
   - Budget alert specifico per l'ambiente TEST

6. **Integrazione con CI/CD** — Usare l'ambiente TEST per test automatizzati:
   - Pipeline GitHub Actions che deploya su TEST, esegue test E2E, poi resetta
   - Test suite dedicata per ambiente TEST (puo essere distruttiva)

7. **Comandi `just` per gestione ambiente TEST** — Aggiungere al justfile:
   - `just test up` — avvia l'ambiente TEST
   - `just test down` — spegni l'ambiente TEST
   - `just test reset-db` — reset database da zero
   - `just test import-db [source]` — importa dati da DEV/PROD
   - `just test deploy` — deploy dell'applicazione su TEST

## Stima effort

**24-32 ore** — Lavoro infrastrutturale significativo:
- Stack CDK per ambiente TEST (~8h)
- Script reset e import DB (~8h)
- Automazione on/off e ottimizzazione costi (~8h)
- Integrazione CI/CD e comandi just (~4-8h)
