---
tags: ["#stack:aws", "#stack:cloudwatch", "#fase:dev"]
---

# Query Templates — CloudWatch Logs Insights

Query pre-costruite per la diagnosi di applicazioni FastAPI su ECS.
Usate dalla skill `aws-logs-diagnose/`.

---

## errors — Errori ed eccezioni

```sql
fields @timestamp, @message, @logStream
| filter @message like /ERROR|Exception|Traceback|CRITICAL/
| sort @timestamp desc
| limit 100
```

**Quando usarla**: primo check per capire se ci sono errori applicativi.

---

## db-issues — Problemi connessione database

```sql
fields @timestamp, @message
| filter @message like /psycopg|connection refused|timeout|ConnectionError|OperationalError|too many connections|remaining connection slots/
| stats count(*) as occurrences by bin(5m)
| sort @timestamp desc
```

**Quando usarla**: sospetto di problemi di connessione al DB (troppi client, timeout, pool esaurito).

---

## slow-requests — Request lente (>1s)

```sql
fields @timestamp, @message
| filter @message like /took \d{4,}ms|duration.*[1-9]\d{3,}/
| sort @timestamp desc
| limit 50
```

**Quando usarla**: performance degradata, risposta lenta dell'API.

**Nota**: adattare il pattern se il formato dei log e' diverso. Se i log sono JSON strutturati con un campo `duration_ms`, usare:
```sql
fields @timestamp, @message, duration_ms
| filter duration_ms > 1000
| sort duration_ms desc
| limit 50
```

---

## status-codes — Distribuzione status code HTTP

```sql
fields @timestamp, @message
| filter @message like /HTTP\/\d|"status_code":\s*\d{3}/
| parse @message /"status_code":\s*(?<statusCode>\d{3})/
| stats count(*) as request_count by statusCode
| sort request_count desc
```

**Quando usarla**: visione d'insieme sulle risposte HTTP (quanti 4xx, 5xx, etc.).

**Nota**: il pattern `parse` dipende dal formato dei log. Adattare se necessario.

---

## recent — Ultimi log (tail)

```sql
fields @timestamp, @message
| sort @timestamp desc
| limit 50
```

**Quando usarla**: vedere cosa sta succedendo ora, log recenti senza filtri.

---

## memory — Problemi di memoria

```sql
fields @timestamp, @message
| filter @message like /MemoryError|OOM|OutOfMemory|memory|Cannot allocate/
| sort @timestamp desc
| limit 50
```

**Quando usarla**: task ECS che si fermano con exit code 137 (SIGKILL / OOM).

---

## Note sull'uso

### Finestre temporali consigliate

| Scenario | Finestra |
|----------|----------|
| Errore in corso | 15m |
| Problemi recenti | 1h |
| Analisi trend | 6h |
| Retrospettiva | 24h |

### Limiti CloudWatch Logs Insights

- Max 30 query concorrenti per account
- Query timeout dopo 60 minuti
- `limit` default 10000 risultati
- Campi auto-scoperti se i log sono JSON strutturati
