# Docker Compose — shutdown e switch progetto migliorati

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 151                |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | 4h                 |
| Tag       | Filone Dev Experience AI |

## Descrizione originale

> Sarebbe carino non dover fare docker compose down tutte le volte quando voglio tirare giù un be e tirarne su un altro

## Piano di risoluzione

1. **Analizzare il flusso attuale di stop/start dei container**
   - Capire perché serve `docker compose down` invece di un semplice Ctrl+C
   - Verificare se i container rimangono in stato zombie dopo Ctrl+C
   - Controllare la configurazione `stop_signal` e `stop_grace_period` nel docker-compose

2. **Aggiungere un comando `just` con gestione corretta dei segnali**
   - Creare `just run dev` (o equivalente) che wrappa `docker compose up` con trap su SIGINT/SIGTERM
   - Al Ctrl+C: eseguire `docker compose stop` (non `down`) per fermare i container senza rimuoverli
   - Restart più veloce: i container stoppati si riavviano istantaneamente con `docker compose start`

3. **Usare Docker Compose profiles per servizi opzionali**
   - Separare i servizi in profili: `backend`, `db`, `frontend`, `monitoring`
   - Permettere di avviare solo ciò che serve: `just run backend` avvia solo BE + DB
   - Il DB può restare attivo anche quando si switcha progetto (se usano porte diverse)

4. **Creare un comando `just switch <progetto>`**
   - Stoppa i container del progetto corrente (`docker compose stop`)
   - Avvia i container del nuovo progetto
   - Gestire i conflitti di porta (stessa porta 8000 per backend diversi)
   - Opzionale: mantenere il DB attivo se il nuovo progetto usa un DB diverso

5. **Assicurare la propagazione corretta di SIGTERM ai container**
   - Verificare che ogni Dockerfile usi `exec` form per CMD (non shell form)
   - Aggiungere `tini` come init system se necessario per la corretta propagazione dei segnali
   - Testare che il backend FastAPI si spenga correttamente (graceful shutdown delle connessioni)

## Stima effort

- Analisi flusso attuale: ~0.5h
- Comando just con signal handling: ~1h
- Docker Compose profiles: ~1h
- Comando just switch: ~1h
- Test propagazione segnali e fix: ~0.5h
- **Totale: ~4h**
