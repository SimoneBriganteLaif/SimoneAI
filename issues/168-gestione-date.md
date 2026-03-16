# Gestione Date

| Campo | Valore |
|---|---|
| **ID** | 168 |
| **Stack** | laif-template |
| **Tipo** | Roadmap |
| **Status** | In analisi |
| **Effort** | 24h |
| **Target** | 6-10 Aprile 2026 |
| **Tag** | Filone Date |

## Descrizione originale

Gestione Date — miglioramento complessivo della gestione delle date in tutto il template, backend e frontend.

## Piano di risoluzione

1. **Audit della gestione date attuale** — censire come le date vengono gestite in tutto il codebase:
   - Backend: campi `datetime` nei modelli SQLAlchemy, serializzazione Pydantic, timezone awareness.
   - Frontend: librerie usate (moment, date-fns, dayjs, nativo), formattazione, parsing.
   - API: formato di scambio (ISO 8601? timestamp?), gestione timezone nell'header o nel body.
2. **Standardizzare: tutte le date come UTC nel DB e nelle API** — definire la convenzione:
   - DB: tutti i campi `TIMESTAMP WITH TIME ZONE`, salvati in UTC.
   - API: tutte le date in formato ISO 8601 con timezone (`2026-04-06T14:30:00Z`).
   - La conversione alla timezone dell'utente avviene solo nel frontend.
3. **Frontend: adottare una singola libreria per le date** — scegliere tra `date-fns` e `dayjs`:
   - `date-fns`: tree-shakeable, funzionale, più leggera se si usano poche funzioni.
   - `dayjs`: API simile a moment, plugin system, buona per manipolazione complessa.
   - Rimuovere tutte le altre librerie di date e i workaround manuali.
4. **Definire la strategia di serializzazione/deserializzazione** — risolvere il problema delle date nello store Redux (correlato a issue 80):
   - Le date nello store Redux devono essere stringhe ISO.
   - Deserializzare a oggetti `Date` solo nei componenti/selettori.
   - Configurare il middleware di serializzabilità di Redux Toolkit.
5. **Risolvere i problemi di timezone** — identificare e correggere tutti i casi in cui le date vengono mostrate con offset errato o senza considerare la timezone dell'utente.
6. **Aggiornare tutti i date picker e i componenti** — uniformare l'uso dei componenti di selezione data (da laif-ds o custom). Assicurarsi che tutti passino e ricevano date in formato standard.
7. **Backend: standardizzare i campi datetime nei modelli Pydantic** — definire un tipo custom `UTCDatetime` o usare i validator Pydantic per garantire che tutte le date in ingresso vengano convertite a UTC e che tutte le date in uscita siano in formato ISO 8601.
8. **Guida alla migrazione per i progetti esistenti** — documentare:
   - Come aggiornare i modelli DB (migrazione Alembic per aggiungere timezone ai campi esistenti).
   - Come aggiornare il frontend (sostituzione delle chiamate alla libreria precedente).
   - Checklist di verifica post-migrazione.

### Issue correlate

- Issue 80 — Redux: serializzare/deserializzare date (Filone Date)

## Stima effort

**24h** — effort significativo per la trasversalità del tema. L'audit iniziale (4h) è fondamentale per mappare tutti i punti di intervento. La standardizzazione backend (6h) e frontend (8h) richiedono modifiche diffuse. La guida alla migrazione (4h) è necessaria per i progetti derivati. Testing distribuito su tutto il template (2h).
