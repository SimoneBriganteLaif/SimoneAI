# Cleanup technical debt template

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 164                |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | Nuova              |
| Priorita  | —                  |
| Effort    | 4-8h (stimato)     |

## Descrizione originale

> Nel template c'e' un po' di sporcizia data da vecchi approcci, come il file prettier, componenti di spinning pre laif-ds, e chiamate senza hook. Dopo il rilascio del nuovo ticketing si puo dedicare un piccolo momento ad un cleanup generale.

## Piano di risoluzione

1. **Rimuovere la configurazione Prettier (se ESLint gestisce il formatting)**
   - Verificare se `.prettierrc` / `prettier.config.js` e' ancora usato o se ESLint con plugin formatting lo ha sostituito
   - Se ridondante: rimuovere il file di configurazione, la dipendenza da `package.json`, e qualsiasi script npm legato a prettier
   - Se ancora necessario: mantenerlo ma documentare il motivo

2. **Sostituire i componenti spinner legacy con equivalenti laif-ds**
   - Cercare tutti i componenti di loading/spinner custom nel template
   - Sostituirli con il componente `Spinner` (o equivalente) di `laif-ds`
   - Verificare che gli import puntino a `laif-ds` e non a componenti locali
   - Rimuovere i file dei componenti legacy dopo la sostituzione

3. **Migrare le chiamate API dirette a hook (useQuery/useMutation)**
   - Identificare tutte le chiamate API fatte direttamente (es. `fetch`, `axios.get` dentro `useEffect`)
   - Migrare a `useQuery` per le letture e `useMutation` per le scritture
   - Questo porta benefici: caching, retry, loading/error states automatici, deduplicazione richieste
   - Priorita: partire dalle pagine piu usate

4. **Rimuovere import inutilizzati e codice morto**
   - Eseguire un'analisi statica per identificare import non usati
   - Rimuovere componenti, utility e file non referenziati
   - Verificare che non ci siano file orfani nella struttura del progetto

5. **Eseguire linter e correggere i warning residui**
   - Eseguire ESLint su tutto il progetto frontend
   - Correggere i warning (non solo gli errori)
   - Valutare se attivare regole piu strict per il futuro

6. **Attendere il completamento del Ticketing Refactor (issue #166)**
   - Come indicato nella descrizione, questo cleanup va fatto **dopo** il rilascio del nuovo ticketing
   - Il refactor del ticketing potrebbe introdurre nuovi componenti e pattern che influenzano il cleanup
   - Evitare di fare cleanup su codice che verra comunque riscritto

## Stima effort

- Rimozione Prettier: ~0.5h
- Sostituzione spinner legacy: ~1-2h
- Migrazione a hook: ~2-4h (dipende dal numero di chiamate dirette)
- Pulizia import e codice morto: ~0.5h
- Fix warning linter: ~0.5h
- **Totale: ~4-8h**
