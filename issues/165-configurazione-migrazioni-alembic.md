# Configurazione migrazioni Alembic

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 165                |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | In corso           |
| Priorita  | —                  |
| Effort    | 4h                 |

## Descrizione originale

> Proposta di configurazione migrazioni Alembic.

## Piano di risoluzione

1. **Standardizzare la naming convention delle migrazioni**
   - Definire un formato coerente per i nomi delle migrazioni (es. `YYYY_MM_DD_HHMM_descrizione_breve`)
   - Configurare il template di Alembic per generare nomi secondo la convenzione
   - Documentare la convenzione per gli sviluppatori

2. **Configurare le impostazioni di auto-generazione**
   - Verificare e ottimizzare `env.py` per l'auto-detect delle modifiche ai modelli
   - Configurare `compare_type=True` per rilevare cambi di tipo colonna
   - Configurare `compare_server_default=True` se necessario per rilevare cambi ai default
   - Gestire le esclusioni: tabelle da ignorare, schemi specifici

3. **Supporto multi-schema (prs vs template)**
   - Configurare Alembic per gestire correttamente lo schema `prs` (dati applicativi) e lo schema `template` (dati framework)
   - Assicurarsi che le migrazioni specifichino sempre lo schema target
   - Valutare se servono branch Alembic separati per i due schemi o se un unico flusso e' sufficiente

4. **Definire un approccio per il testing delle migrazioni**
   - Implementare test che verificano che le migrazioni siano reversibili (upgrade + downgrade)
   - Verificare che la catena di migrazioni sia integra (no branch orfani, no gap)
   - Opzionale: test che verifica che i modelli SQLAlchemy siano allineati con lo stato del DB dopo le migrazioni

5. **Aggiornare la configurazione nel template**
   - Aggiornare `alembic.ini` e `env.py` con le best practice definite
   - Assicurarsi che la configurazione funzioni sia in locale (Docker) che in produzione (AWS)
   - Documentare eventuali variabili d'ambiente necessarie

## Note

Questa issue e' gia **in corso**. Il piano sopra serve come riferimento per gli step rimanenti o come checklist di verifica.

## Stima effort

- Naming convention e template: ~0.5h
- Auto-generazione settings: ~1h
- Multi-schema: ~1.5h
- Testing migrazioni: ~0.5h
- Aggiornamento template e docs: ~0.5h
- **Totale: ~4h**
