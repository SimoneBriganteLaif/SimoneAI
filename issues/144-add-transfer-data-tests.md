# Add Transfer Data Tests

| Campo     | Valore           |
|-----------|------------------|
| ID        | 144              |
| Stack     | (cross-stack)    |
| Tipo      | Proposal         |
| Status    | Backlog          |
| Priorita  | —                |
| Tag       | Filone Test      |

## Descrizione originale

Add transfer_data tests.

## Piano di risoluzione

1. **Scrivere unit test per il modulo transfer_data** — Coprire le funzionalita principali:
   - Trasferimento completo (full sync)
   - Trasferimento incrementale (solo dati nuovi/modificati)
   - Gestione degli errori (connessione fallita, dati corrotti, timeout)
   - Mapping dei dati tra schema sorgente e destinazione
   - Validazione dei dati prima del trasferimento

2. **Test scenari di trasferimento** — Verificare i casi d'uso reali:
   - Sync da DB vuoto
   - Sync con dati gia presenti (upsert vs insert)
   - Sync con conflitti (dati modificati sia nella sorgente che nella destinazione)
   - Sync parziale (interruzione e ripresa)
   - Grandi volumi di dati (performance)

3. **Mock delle connessioni DB esterne** — Per i test unitari:
   - Usare `pytest` fixtures con mock delle connessioni
   - Simulare risposte del DB sorgente
   - Verificare le query generate senza eseguirle realmente
   - Usare SQLite in-memory o testcontainers per test rapidi

4. **Test di integrazione con DB reale** — Per la pipeline CI:
   - Usare Docker Compose per avviare DB PostgreSQL di test
   - Popolare il DB sorgente con dati di test noti
   - Eseguire il trasferimento e verificare il risultato
   - Cleanup automatico dopo ogni test

5. **Correlazione con issue 130 (Test Improvements)** — Questa issue fa parte del filone Test. I test scritti qui devono:
   - Seguire le convenzioni stabilite nella issue 130
   - Essere integrati nella pipeline CI
   - Contribuire al target di code coverage

## Stima effort

**8-12 ore**:
- Unit test con mock (~4h)
- Test di integrazione con DB reale (~4h)
- Integrazione nella pipeline CI (~2h)
- Documentazione test (~1h)
