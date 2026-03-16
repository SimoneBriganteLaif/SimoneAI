# Async Confirmer — Gestione chiamate asincrone

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 42              |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | Backlog         |
| **Effort stimato** | 4h       |

## Descrizione originale

Migliorare la gestione di chiamate asincrone nell'action del Confirmer.

## Piano di risoluzione

### 1. Analisi dell'implementazione attuale del Confirmer

Esaminare il componente Confirmer esistente per capire:

- Come vengono gestite le action callback attuali (sync only?)
- Struttura del componente e delle prop
- Eventuali limitazioni note nella gestione degli eventi

### 2. Aggiungere stato di loading durante l'esecuzione dell'action asincrona

Quando la callback `onConfirm` ritorna una Promise:

- Rilevare automaticamente se il valore di ritorno è una Promise (duck typing con `.then`)
- Mostrare uno spinner/loading indicator sul pulsante di conferma
- Transizione visuale: il testo del pulsante viene sostituito o affiancato da uno spinner
- Lo stato di loading deve essere visibile e chiaro per l'utente

### 3. Disabilitare il pulsante di conferma durante il loading

Per prevenire il doppio click:

- Disabilitare il pulsante "Conferma" non appena viene cliccato e la Promise è in pending
- Disabilitare anche il pulsante "Annulla" durante il loading (opzionale, configurabile)
- Impedire la chiusura del dialog tramite click esterno o tasto Escape durante il loading
- Aggiungere `pointer-events: none` e stile visuale "disabled" al pulsante

### 4. Gestione errori graceful

Se la Promise viene rigettata (reject):

- **Non chiudere il dialog** — l'utente deve poter ritentare
- Mostrare un messaggio di errore (toast notification o inline nel dialog)
- Ripristinare lo stato del pulsante di conferma (riabilitarlo, rimuovere lo spinner)
- Supportare una prop `onError` opzionale per gestione custom degli errori
- Loggare l'errore in console per debug

### 5. Supporto a callback che ritornano Promise

Assicurarsi che l'API sia retrocompatibile:

- Se `onConfirm` ritorna `void` o `undefined`: comportamento attuale (chiudi subito)
- Se `onConfirm` ritorna una `Promise`: attendi risoluzione, poi chiudi
- Se la `Promise` viene rigettata: non chiudere (vedi step 4)
- Tipizzazione TypeScript: `onConfirm: () => void | Promise<void>`

### 6. Storybook — Esempi con scenari asincroni

Creare stories dedicate:

- **Async Success**: conferma con delay simulato (2s), mostra loading, poi chiude
- **Async Error**: conferma che fallisce, mostra errore, permette retry
- **Sync (backward compat)**: conferma sincrona, comportamento invariato
- Documentare il nuovo comportamento nella description del componente

## Stima effort

| Fase | Ore |
|------|-----|
| Analisi implementazione attuale | 0.5h |
| Stato loading + spinner | 1h |
| Disabilitazione pulsanti | 0.5h |
| Gestione errori | 1h |
| Storybook | 1h |
| **Totale** | **4h** |
