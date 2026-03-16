# Nuova gestione permessi centralizzata

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 70                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | —                  |
| Tag       | Filone Sicurezza   |

## Descrizione originale

> Per ora usiamo solo i permessi nel frontend. Il db gestisce le pagine e i permessi, gli accessi alle api, e le feature flag. Centralizzare i permessi in un punto unico.

## Piano di risoluzione

1. **Progettare lo schema permessi centralizzato**
   - Definire un modello unico che copra: permessi pagine, permessi API, feature flag
   - Schema proposto: `Permission(resource, action, role, enabled)`
   - Risorse: pagine (`page:dashboard`), endpoint API (`api:users:create`), feature (`feature:export-csv`)
   - Azioni: `view`, `create`, `edit`, `delete`, `execute`
   - Creare un ADR per documentare la decisione architetturale

2. **Backend: middleware di autorizzazione basato su DB**
   - Creare un middleware FastAPI che intercetta ogni richiesta
   - Lookup in DB: dato il ruolo dell'utente e l'endpoint richiesto, verificare il permesso
   - Cache dei permessi in memoria (invalidata su modifica) per evitare query ad ogni richiesta
   - Decoratore `@require_permission("resource", "action")` per endpoint specifici
   - Risposta 403 con messaggio chiaro se il permesso manca

3. **Frontend: fetch permessi al login e store in context**
   - Endpoint `GET /api/permissions/me` che restituisce tutti i permessi dell'utente corrente
   - Salvare i permessi in un React Context (`PermissionsProvider`)
   - Hook `usePermission("resource", "action")` → `boolean`
   - Componente `<IfPermitted resource="..." action="...">` per rendering condizionale
   - Refresh automatico dei permessi quando cambiano (via WebSocket o polling)

4. **Admin UI per gestione permessi per ruolo**
   - Pagina di amministrazione con matrice ruolo × risorsa
   - Checkbox per abilitare/disabilitare ogni combinazione
   - Raggruppamento per tipo di risorsa (pagine, API, feature flag)
   - Possibilità di creare nuovi ruoli e clonare permessi da un ruolo esistente
   - Log delle modifiche ai permessi (audit trail)

5. **Rimuovere i check hardcoded dal codice backend**
   - Cercare tutti i punti dove i ruoli sono controllati con `if user.role == "admin"`
   - Sostituire con il decoratore `@require_permission` o il middleware
   - Assicurarsi che nessun endpoint resti senza protezione (audit completo)

6. **Implementare il sistema di feature flag**
   - Feature flag: abilitare/disabilitare funzionalità per progetto, ruolo o utente
   - Tabella `feature_flags(name, enabled, roles, description)`
   - Endpoint per gestire i flag dall'admin UI
   - Frontend: hook `useFeatureFlag("nome-feature")` → `boolean`
   - Utile per rilasci graduali e A/B testing

7. **Definire il percorso di migrazione per i progetti esistenti**
   - Script di migrazione che popola la tabella permessi a partire dalla configurazione attuale
   - Periodo di transizione: il vecchio sistema e il nuovo coesistono (doppio check)
   - Documentazione per ogni progetto su come migrare
   - Test automatizzati per verificare che la migrazione non cambi i permessi effettivi

8. **Creare ADR e documentazione**
   - ADR con: contesto, decisione, alternative valutate, conseguenze
   - Documentazione per sviluppatori: come aggiungere un nuovo permesso
   - Documentazione per admin: come gestire i permessi dalla UI

## Note

Questa è una modifica architetturale maggiore che impatta tutti i progetti basati su laif-template. Richiede un ADR e un piano di rollout coordinato.

## Stima effort

- Design schema e ADR: ~4h
- Middleware backend: ~6h
- Context e hook frontend: ~4h
- Admin UI permessi: ~8h
- Rimozione check hardcoded: ~4h
- Sistema feature flag: ~4h
- Migrazione progetti esistenti: ~6h
- Documentazione e test: ~4h
- **Totale: ~40h** (stima iniziale, da raffinare dopo l'analisi)
