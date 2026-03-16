# Aggiornamento stato ticket lato LAIF

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 65                 |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | In pausa           |
| Priorita  | —                  |
| Effort    | 4h                 |

## Descrizione originale

> A volte nei ticket sbaglio e metto marca come risolto invece di trattasi di nuova features. Possiamo introdurre un edit di stato lato nostro?

## Piano di risoluzione

1. **Aggiungere azione di modifica stato nella UI ticketing (Support)**
   - Nella vista dettaglio ticket, aggiungere un pulsante/icona di edit accanto allo stato corrente
   - L'azione deve essere visibile solo agli utenti LAIF (non al cliente finale)

2. **Backend: creare endpoint PATCH per aggiornamento stato ticket**
   - Endpoint: `PATCH /api/v1/tickets/{ticket_id}/status`
   - Body: `{ "status": "<nuovo_stato>" }`
   - Validare che lo stato sia tra quelli ammessi
   - Proteggere con permessi admin/LAIF

3. **Frontend: aggiungere selettore di stato nella vista dettaglio ticket**
   - Dropdown con gli stati disponibili (es. Aperto, In lavorazione, Risolto, Nuova feature, Chiuso)
   - Mostrare lo stato corrente come valore selezionato
   - Disabilitare lo stato corrente nella lista opzioni

4. **Aggiungere dialog di conferma prima del cambio stato**
   - Mostrare stato attuale e nuovo stato selezionato
   - Richiedere conferma esplicita per evitare cambi accidentali (che e' proprio il problema originale)

5. **Registrare i cambi di stato per audit trail**
   - Loggare ogni cambio stato con: utente, timestamp, stato precedente, nuovo stato
   - Eventualmente mostrare lo storico cambi nella vista dettaglio ticket

## Note

Questa issue e' attualmente **in pausa**, probabilmente in attesa del completamento del Ticketing Refactor (issue #166). Valutare se implementare come parte del refactor o come intervento separato.

## Stima effort

- Backend (endpoint + validazione + audit log): ~1.5h
- Frontend (dropdown + dialog conferma): ~2h
- Test e verifica: ~0.5h
- **Totale: ~4h**
