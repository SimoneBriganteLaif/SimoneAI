# Loggare metriche database

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 159                |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | In analisi         |
| Priorita  | —                  |
| Effort    | 8h                 |

## Descrizione originale

> Sarebbe necessario loggare e raccogliere info su utilizzo db, su tempo di esecuzione delle query, su memoria occupata ecc. Così da debuggare meglio errori di timeout o cali di performance

## Piano di risoluzione

1. **Aggiungere event listener SQLAlchemy per il tempo di esecuzione delle query**
   - Registrare listener su `before_cursor_execute` e `after_cursor_execute`
   - Calcolare il tempo di esecuzione di ogni query
   - Loggare la query, i parametri (sanitizzati) e il tempo impiegato
   - Usare logging strutturato coerente con la strategia di logging del template

2. **Loggare le slow query sopra una soglia configurabile**
   - Soglia di default: 500ms (configurabile via variabile d'ambiente `DB_SLOW_QUERY_THRESHOLD_MS`)
   - Livello WARNING per query lente, livello DEBUG per le altre
   - Includere nel log: query SQL, tempo, tabelle coinvolte, caller (stack trace abbreviato)
   - In locale: evidenziare le slow query con colore diverso nel terminale

3. **Aggiungere metriche sul connection pool**
   - Monitorare: connessioni attive, idle, in overflow, checkout timeout
   - Registrare listener su `checkout`, `checkin`, `invalidate`, `soft_invalidate`
   - Esporre le metriche come log strutturato a intervalli regolari (ogni 60s)
   - Loggare warning se il pool si avvicina al limite (> 80% utilizzo)

4. **Integrare con CloudWatch custom metrics o log strutturati**
   - Opzione A: inviare metriche custom a CloudWatch via boto3 (costo aggiuntivo)
   - Opzione B: log strutturati JSON filtrabili con CloudWatch Insights (più economico)
   - Valutare il trade-off costi/usabilità — partire con Opzione B
   - Metriche chiave: query/s, avg response time, slow query count, pool utilization

5. **Aggiungere endpoint di health con statistiche del pool**
   - Endpoint `GET /health/db` con: stato connessione, pool stats, ultima slow query
   - Includere: `pool_size`, `checked_out`, `overflow`, `checked_in`
   - Proteggere l'endpoint (solo ad uso interno o con API key)

6. **Creare template dashboard CloudWatch per il monitoraggio DB**
   - Widget: query/minuto, tempo medio risposta, slow query count
   - Widget: utilizzo pool connessioni nel tempo
   - Widget: top 10 query più lente (ultime 24h)
   - Esportare come CloudFormation template riutilizzabile per ogni progetto

7. **Valutare il query profiling built-in di SQLAlchemy**
   - Testare `sqlalchemy.engine` con echo mode in ambiente di sviluppo
   - Considerare l'integrazione con `sqlalchemy-utils` per profiling avanzato
   - Documentare come attivare il profiling dettagliato per debug locale

## Note

Correlata alla issue #169 (Gestione Logging). Valutare se le due issue possono essere affrontate insieme per coerenza nella strategia di logging e formato dei log strutturati.

## Stima effort

- Event listener query execution: ~1.5h
- Slow query logging configurabile: ~1h
- Metriche connection pool: ~1.5h
- Integrazione CloudWatch: ~1.5h
- Endpoint health DB: ~1h
- Dashboard CloudWatch template: ~1h
- Documentazione e test: ~0.5h
- **Totale: ~8h**
