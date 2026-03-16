# n8n per workflow e pipeline ETL

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 51                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | —                  |

## Descrizione originale

> n8n per i workflow: testare in locale, monitorare ETL in produzione, stack ETL pipeline ci-cd, integrazioni, grafica per gestire i workflow

## Piano di risoluzione

1. **PoC: deploy n8n in locale via Docker**
   - Aggiungere n8n al `docker-compose.yml` del template come servizio opzionale (profilo `etl`)
   - Configurare il volume per persistenza dei workflow
   - Configurare le credenziali di base (DB, API interne)
   - Comando: `just run etl` per avviare n8n in locale sulla porta 5678

2. **Testare l'integrazione con il template LAIF**
   - Connettere n8n al database PostgreSQL del progetto
   - Creare un workflow di esempio: trigger API → trasformazione dati → scrittura DB
   - Testare i trigger: webhook (chiamata dal backend), cron (schedulato), evento DB
   - Verificare l'autenticazione: n8n deve poter chiamare le API del backend con token valido

3. **Valutare n8n per i casi d'uso ETL attuali**
   - Confrontare con l'approccio attuale (script Python, async-integration-client-poller)
   - Casi d'uso: sincronizzazione dati da sistemi esterni, import/export CSV, pipeline di trasformazione
   - Pro: interfaccia grafica, monitoring built-in, retry automatici, log esecuzioni
   - Contro: dipendenza aggiuntiva, curva di apprendimento, overhead di gestione

4. **Definire la strategia di deploy su AWS**
   - Opzione A: container ECS dedicato per n8n (costo fisso, sempre attivo)
   - Opzione B: ECS Fargate on-demand (si accende quando serve)
   - Storage workflow: volume EFS o database PostgreSQL dedicato
   - Networking: n8n nella stessa VPC del backend per accesso diretto al DB
   - Stimare i costi mensili per le due opzioni

5. **Pipeline CI/CD per i workflow n8n**
   - I workflow n8n possono essere esportati come JSON
   - Versionare i workflow JSON nella repository del progetto (`workflows/n8n/`)
   - GitHub Action: al push su main, importare automaticamente i workflow aggiornati in n8n
   - Separare i workflow per ambiente (dev, staging, prod) con variabili d'ambiente

6. **Analisi costi**
   - Costo infrastruttura: ECS/Fargate + storage + networking
   - Costo manutenzione: aggiornamenti n8n, gestione credenziali, monitoring
   - Confrontare con il costo dello sviluppo custom equivalente (script Python + cron)
   - Break-even point: da quanti workflow in su n8n conviene rispetto allo sviluppo custom

7. **Decisione: adottare, rimandare o alternativa**
   - Se PoC positivo e costi accettabili → adottare come componente opzionale del template
   - Se troppo costoso o complesso → rimandare e rivalutare tra 6 mesi
   - Alternative da considerare: Apache Airflow (più maturo per ETL), Prefect, Temporal
   - Documentare la decisione in un ADR

## Stima effort

- PoC locale con Docker: ~3h
- Test integrazione con template: ~4h
- Valutazione casi d'uso ETL: ~2h
- Strategia deploy AWS: ~3h
- Pipeline CI/CD workflow: ~4h
- Analisi costi: ~2h
- ADR e documentazione decisione: ~2h
- **Totale: ~20h** (PoC completo con decisione finale)
