# Visual feedback per upload file

| Campo      | Valore                |
|------------|-----------------------|
| **ID**     | 154                   |
| **Stack**  | laif-ds               |
| **Tipo**   | Bug                   |
| **Status** | Backlog               |
| **Priorità** | Media              |

## Descrizione originale

When uploading a file I'd expect to see a progress bar per-file of the upload progress (this could be even a very basic spinner changing to a check once done).

## Piano di risoluzione

### 1. Analisi del componente attuale

- Individuare il componente di upload file in laif-ds (es. `AppFileUpload`, `AppMediaUpload` o simile)
- Verificare lo stato attuale: come viene mostrato il progresso dell'upload (probabilmente nessun feedback visivo)
- Controllare se il componente gestisce upload singolo o multiplo
- Verificare come viene effettuata la chiamata di upload (fetch, axios, XMLHttpRequest)

### 2. Design del feedback visivo

Tre livelli di feedback, dal piu' semplice al piu' completo:

- **Livello base (MVP)**: spinner durante l'upload, icona check al completamento, icona errore se fallisce
- **Livello intermedio**: barra di progresso per-file con percentuale
- **Livello avanzato**: barra di progresso + velocita' upload + tempo stimato rimanente

Proposta: implementare il livello intermedio come default, con possibilita' di scegliere il livello base via prop.

### 3. Implementazione tracking progresso

- Se si usa `fetch`: non supporta nativamente il progress tracking per l'upload. Opzioni:
  - Usare `XMLHttpRequest` con listener `upload.onprogress`
  - Usare `ReadableStream` (supporto browser piu' recente)
- Se si usa `axios`: supporta `onUploadProgress` nativamente
- Esporre un callback `onProgress(file, percent)` dal componente per consentire ai consumatori di integrare con il proprio servizio di upload

### 4. Implementazione UI per-file

Per ogni file in coda di upload, mostrare:
- Nome del file (troncato con ellipsis se lungo)
- Dimensione del file
- Stato: `pending` | `uploading` | `completed` | `error`
- Indicatore visivo:
  - `pending`: icona file grigia
  - `uploading`: spinner o barra di progresso
  - `completed`: icona check verde
  - `error`: icona errore rossa con messaggio

### 5. Integrazione con i progetti esistenti

- Verificare come i progetti (es. Jubatus) usano il componente di upload
- Assicurarsi che il nuovo feedback visivo funzioni con il media service esistente
- Mantenere retrocompatibilita': il componente deve funzionare anche senza `onProgress`

### 6. Testing

- Testare upload singolo e multiplo
- Testare con file piccoli (feedback istantaneo) e grandi (progress visibile)
- Testare errori di rete durante l'upload
- Testare cancellazione upload in corso (se supportata)
- Verificare su mobile (spazio ridotto per la lista file)

## Stima effort

**6 ore** — Suddivise in:
- 1h analisi componente attuale e scelta approccio
- 3h implementazione UI progress + integrazione tracking
- 2h testing e rifinitura
