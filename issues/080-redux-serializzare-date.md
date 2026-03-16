# Store Redux: Serializzare/Deserializzare Date

| Campo | Valore |
|---|---|
| **ID** | 80 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | To Review |
| **Effort** | 12h |
| **Tag** | Breaking, Filone Date |

## Descrizione originale

Store Redux: serializzare - deserializzare date e altri tipi problematici. Possibile documentazione: https://redux-toolkit.js.org/api/serializabilityMiddleware

## Piano di risoluzione

1. **Già in To Review.** Verificare eventuali PR o branch esistenti.
2. **Configurare il middleware di serializzabilità di Redux Toolkit** — abilitare `serializableCheck` nello store con configurazione personalizzata:
   - Definire quali path ignorare (se necessario durante la migrazione).
   - Attivare i warning in development per identificare tutti i valori non serializzabili.
3. **Definire serializzatori custom per gli oggetti Date** — stabilire la convenzione:
   - **Nello store**: le date sono sempre stringhe ISO 8601 (`"2026-04-06T14:30:00Z"`).
   - **Nei componenti**: deserializzare a `Date` solo quando serve (nei selettori o direttamente nel componente).
   - Creare utility helper: `toStoreDate(date: Date): string` e `fromStoreDate(iso: string): Date`.
4. **Salvare le date come stringhe ISO nello store, deserializzare in lettura** — aggiornare tutti i reducer che attualmente salvano oggetti `Date` nello store:
   - Nei `createSlice`: convertire le date a stringa ISO prima di salvarle.
   - Nei `createAsyncThunk`: le risposte API arrivano già come stringhe, non convertirle a `Date`.
   - Nei selettori: se serve un oggetto `Date`, convertire lì.
5. **Aggiornare tutti i reducer e i selettori che gestiscono date** — censire tutti i punti dove le date transitano nello store e applicare il pattern di serializzazione. Questo è il passo più impattante e richiede attenzione per non introdurre regressioni.

### Issue correlate

- Issue 168 — Gestione Date (parent issue del Filone Date)

## Stima effort

**12h** — il setup del middleware è rapido (1h), ma l'aggiornamento di tutti i reducer e selettori richiede un censimento accurato e modifiche diffuse nel codebase. Consigliato procedere slice per slice, con test dopo ogni modifica. Breaking change: i progetti derivati dovranno adeguare i propri slice custom.
