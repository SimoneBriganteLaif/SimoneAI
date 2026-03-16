# User Management — Form non gestiti correttamente

| Campo | Valore |
|---|---|
| **ID** | 76 |
| **Stack** | laif-template |
| **Tipo** | Bug |
| **Status** | To Review |
| **Effort** | 6h |

## Descrizione originale

In generale nelle varie tabs della sezione user-management, i form non sono sempre gestiti con React Hook Form e alcune validazioni oltre al submit "onEnter" non sono funzionanti.

## Piano di risoluzione

1. **Già in To Review.** Verificare eventuali PR o branch esistenti.
2. **Migrare tutti i form della sezione user-management a React Hook Form** — censire ogni tab (utenti, ruoli, permessi, ecc.) e identificare i form che usano ancora state locale o approcci misti. Convertirli tutti a React Hook Form con `useForm` e i componenti `AppForm` del design system.
3. **Correggere il submit con tasto Enter** — assicurarsi che:
   - Ogni form abbia un `<form>` wrapper con `onSubmit` collegato a `handleSubmit` di RHF.
   - Il bottone di submit sia di tipo `submit` dentro il `<form>`.
   - Non ci siano `event.preventDefault()` accidentali che bloccano il submit.
4. **Aggiungere validazione corretta su tutti i campi** — definire gli schema di validazione (Zod o Yup) per ogni form:
   - Campi obbligatori (email, nome, ruolo).
   - Formato (email valida, password con requisiti minimi).
   - Messaggi di errore in italiano.
   - Validazione inline (on blur) oltre che on submit.
5. **Garantire comportamento consistente su tutte le tab** — verificare che ogni tab segua lo stesso pattern:
   - Stessa struttura form (RHF + schema validation + AppForm).
   - Stessa gestione errori (toast per errori server, inline per errori di validazione).
   - Stessa UX per creazione, modifica, cancellazione.

## Stima effort

**6h** — lavoro prevalentemente di refactoring frontend. Il censimento dei form (1h) è il primo passo, poi migrazione e test tab per tab (4h), e verifica finale cross-tab (1h).
