# Migrazione JWT da localStorage a HttpOnly Cookie

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 54                 |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | 8-16h (stimato)    |

## Descrizione originale

> Usare HttpOnly Cookie per salvare i JWT invece del localstorage.

Con diversi link di riferimento sulla sicurezza del salvataggio JWT in localStorage vs HttpOnly cookies.

## Piano di risoluzione

1. **Backend: modificare gli endpoint di autenticazione per impostare JWT in HttpOnly cookie**
   - Endpoint login: invece di restituire il token nel body, impostarlo come cookie
   - Flags del cookie: `HttpOnly=True`, `Secure=True`, `SameSite=Strict`
   - `Path=/api` per limitare l'invio del cookie solo alle chiamate API
   - Configurare `Max-Age` / `Expires` coerente con la durata del JWT

2. **Backend: aggiungere protezione CSRF**
   - Implementare il pattern double-submit cookie:
     - Generare un CSRF token e inviarlo come cookie non-HttpOnly
     - Il frontend lo legge e lo invia come header `X-CSRF-Token` ad ogni richiesta mutativa (POST, PUT, PATCH, DELETE)
     - Il backend verifica che header e cookie corrispondano
   - Alternativa: SameSite=Strict potrebbe essere sufficiente per la maggior parte dei casi, ma il CSRF token aggiunge un livello di sicurezza

3. **Frontend: rimuovere la gestione token da localStorage**
   - Eliminare tutte le chiamate `localStorage.setItem/getItem/removeItem` relative al token
   - Il browser inviera automaticamente il cookie con ogni richiesta (stesso dominio)
   - Rimuovere gli interceptor Axios/fetch che aggiungono l'header `Authorization: Bearer`

4. **Aggiornare il client API per includere le credenziali nelle richieste**
   - Configurare `credentials: 'include'` (fetch) o `withCredentials: true` (Axios)
   - Questo assicura che il browser invii i cookie anche per richieste cross-origin (se applicabile)
   - Aggiungere l'header CSRF token per le richieste mutative

5. **Gestire il token refresh tramite rotazione cookie**
   - Endpoint refresh: riceve il cookie corrente, valida, emette nuovo cookie
   - Implementare silent refresh: prima che il token scada, il frontend chiama l'endpoint refresh
   - Gestire il caso di cookie scaduto: redirect a login

6. **Aggiornare il logout per cancellare i cookie lato server**
   - Endpoint logout: impostare il cookie con `Max-Age=0` per cancellarlo
   - Non basta cancellarlo lato client (il cookie e' HttpOnly, il JS non puo toccarlo)

7. **Testare scenari cross-origin**
   - Verificare il funzionamento in dev locale (frontend su porta diversa dal backend)
   - Configurare `SameSite` e CORS appropriatamente per l'ambiente di sviluppo
   - Testare su staging con dominio reale

8. **Pianificare la migrazione come Breaking Change**
   - Questo e' un **breaking change** per tutti i progetti basati sul template
   - Scrivere una guida di migrazione per i progetti esistenti
   - Prevedere un periodo di transizione dove entrambi i metodi (cookie e Bearer header) sono accettati
   - Comunicare il cambio con anticipo al team

## Note

- Correlata alla issue #85 (OAuth2): la migrazione a cookie potrebbe essere fatta insieme all'eventuale adozione di OAuth2
- Valutare l'impatto su eventuali client mobile o API esterne che usano il Bearer token direttamente

## Stima effort

- Backend (cookie auth + CSRF): ~3-4h
- Frontend (rimozione localStorage + cookie handling): ~2-3h
- Token refresh e logout: ~1-2h
- Test cross-origin e scenari edge: ~1-2h
- Guida migrazione e comunicazione: ~1-2h
- **Totale: ~8-16h** (dipende dalla complessita dell'ecosistema di progetti da migrare)
