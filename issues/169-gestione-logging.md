# Gestione logging CloudWatch

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 169                |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | In analisi         |
| Priorita  | —                  |
| Effort    | 8h                 |

## Descrizione originale

> Per il logging su CloudWatch in modalita INFO mostriamo davvero un'esagerazione di dati (mi riferisco ai progetti People e Nivi) che rendono difficile capire cosa stia succedendo, mi piacerebbe avere su CloudWatch qualcosa di simile a quello che abbiamo in locale.

## Piano di risoluzione

1. **Analizzare la configurazione di logging attuale**
   - Mappare tutti i logger attivi: Python root logger, uvicorn, SQLAlchemy, boto3, httpx
   - Identificare quali moduli producono il volume maggiore di log in CloudWatch
   - Confrontare la configurazione locale con quella di produzione (ENV-based)

2. **Ridurre il rumore filtrando log non necessari**
   - Filtrare le richieste health check (`/health`, `/ping`) dai log di accesso
   - Filtrare le richieste a file statici
   - Escludere le query DB di routine (es. session check, heartbeat)
   - Configurare un filtro per richieste interne AWS (ALB health checks)

3. **Implementare logging strutturato JSON per CloudWatch**
   - Sostituire il formatter testuale con un JSON formatter in produzione
   - Campi standard: `timestamp`, `level`, `logger`, `message`, `request_id`, `user_id`
   - Mantenere il formato leggibile (colorato) in locale per non perdere la DX attuale

4. **Configurare il log level per modulo**
   - `SQLAlchemy.engine` → WARNING in produzione (elimina le query SQL verbose)
   - `uvicorn.access` → WARNING o filtrato (elimina ogni singola richiesta HTTP)
   - `boto3` / `botocore` → WARNING (elimina i dettagli delle chiamate AWS)
   - `httpx` → WARNING (elimina i log delle chiamate HTTP client)
   - Rendere i livelli configurabili via variabili d'ambiente (`LOG_LEVEL_SQLALCHEMY`, ecc.)

5. **Aggiungere correlation ID per richiesta**
   - Middleware che genera un UUID per ogni richiesta HTTP
   - Propagare il correlation ID in tutti i log emessi durante la richiesta
   - Includere il correlation ID nelle risposte HTTP (header `X-Request-ID`)
   - Questo permette di filtrare in CloudWatch tutti i log di una singola richiesta

6. **Creare query CloudWatch Insights predefinite**
   - Query per errori negli ultimi 30 minuti
   - Query per richieste lente (> 1s)
   - Query per tracciare una richiesta specifica via correlation ID
   - Query per conteggio errori per endpoint
   - Salvare le query come "saved queries" in CloudWatch

7. **Documentare la configurazione di logging nella documentazione del template**
   - Spiegare i livelli di log disponibili e come configurarli
   - Documentare le variabili d'ambiente per il tuning
   - Includere esempi di query CloudWatch Insights utili

## Note

Correlata alla issue #159 (DB metrics logging). Valutare se le due issue possono essere affrontate insieme per coerenza nella strategia di logging.

## Stima effort

- Analisi configurazione attuale: ~1h
- Filtri e riduzione rumore: ~1.5h
- Logging strutturato JSON: ~2h
- Configurazione per modulo: ~1h
- Correlation ID middleware: ~1.5h
- Query CloudWatch Insights: ~0.5h
- Documentazione: ~0.5h
- **Totale: ~8h**
