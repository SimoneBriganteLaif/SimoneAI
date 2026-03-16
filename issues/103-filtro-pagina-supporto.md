# Filtro testo pagina Support non funzionante

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 103                |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | Da iniziare        |
| Priorita  | —                  |
| Effort    | 2-4h (stimato)     |

## Descrizione originale

> Non funziona il filtro "Search by text" nella pagina Support del template. Sembra non filtrare correttamente sul testo del ticket, sembra ricercare solo per una lettera.

## Piano di risoluzione

1. **Riprodurre il bug in locale**
   - Aprire la pagina Support con dei ticket di test
   - Digitare una parola nel campo "Search by text"
   - Verificare il comportamento: la ricerca parte ad ogni singolo carattere? Filtra solo sulla prima lettera? Il risultato cambia ad ogni keystroke?
   - Controllare la console browser per errori e la tab Network per le richieste inviate

2. **Verificare se la ricerca ha debounce o parte ad ogni keystroke**
   - Ispezionare il componente frontend del campo di ricerca
   - Se manca il debounce, ogni pressione di tasto invia una richiesta con un singolo carattere
   - Se c'e' debounce ma troppo corto, il problema potrebbe essere una race condition tra richieste

3. **Controllare l'endpoint di ricerca backend**
   - Verificare che l'endpoint riceva il parametro di ricerca corretto (stringa intera, non singolo carattere)
   - Controllare la query SQL: sta usando `LIKE '%testo%'` o `ILIKE`? Funziona correttamente?
   - Testare l'endpoint direttamente via Swagger con vari termini di ricerca

4. **Identificare la causa probabile**
   - Scenario A: manca debounce → la ricerca parte ad ogni carattere e l'ultima risposta (1 lettera) sovrascrive le precedenti
   - Scenario B: il parametro di ricerca viene troncato/sovrascritto prima dell'invio
   - Scenario C: il backend filtra solo sul primo carattere (bug nella query)

5. **Implementare la fix**
   - Aggiungere debounce all'input di ricerca (~300ms) se mancante
   - Assicurarsi che il termine di ricerca completo venga inviato all'API
   - Se il problema e' backend: correggere la query di filtro
   - Opzionale: aggiungere un numero minimo di caratteri (es. 2-3) prima di attivare la ricerca

6. **Test di verifica**
   - Testare con vari termini di ricerca (parole complete, parziali, con spazi)
   - Verificare che i risultati siano coerenti con il testo cercato
   - Verificare che non ci siano regressioni su altri filtri della pagina Support

## Stima effort

- Riproduzione e analisi: ~0.5h
- Identificazione causa e fix: ~1-2h
- Test e verifica: ~0.5h
- **Totale: ~2-4h**
