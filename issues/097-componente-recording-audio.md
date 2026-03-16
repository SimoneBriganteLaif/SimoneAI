# Componente di recording audio

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 97              |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | Da iniziare     |
| **Priorità**| Bassa           |
| **Effort stimato** | 8h       |

## Descrizione originale

Componente di recording audio.

## Piano di risoluzione

### 1. Utilizzare la MediaRecorder Web API

Base tecnica del componente:

- Usare `navigator.mediaDevices.getUserMedia({ audio: true })` per accedere al microfono
- Creare un'istanza di `MediaRecorder` con il media stream ottenuto
- Raccogliere i chunk audio tramite l'evento `ondataavailable`
- Al termine della registrazione, combinare i chunk in un `Blob` (formato `audio/webm` o `audio/mp4` a seconda del browser)

### 2. Interfaccia utente

Progettare la UI del componente con i seguenti elementi:

- **Pulsante Record**: icona microfono, diventa rosso/pulsante durante la registrazione
- **Visualizzazione waveform**: barra o forma d'onda che mostra l'attività audio in tempo reale durante la registrazione (usando `AnalyserNode` della Web Audio API)
- **Pulsante Stop**: appare durante la registrazione, ferma e salva l'audio
- **Playback**: dopo la registrazione, mostrare un player audio con play/pause e barra di avanzamento
- **Pulsante Delete**: permette di cancellare la registrazione e ricominciare
- **Timer**: mostra la durata della registrazione in corso (formato `mm:ss`)

### 3. Output come Blob/File per upload

Al termine della registrazione:

- Esporre il risultato come `Blob` o `File` tramite una callback `onRecordingComplete`
- Fornire anche l'URL del blob (`URL.createObjectURL`) per il playback locale
- Supportare la prop `outputFormat` per specificare il formato preferito (se supportato dal browser)
- L'output deve essere pronto per l'upload tramite il media service esistente

### 4. Gestione permessi microfono

Gestire tutti gli stati dei permessi:

- **Prima richiesta**: mostrare un messaggio che spiega perché serve il microfono
- **Permesso concesso**: procedere con la registrazione
- **Permesso negato**: mostrare un messaggio di errore con istruzioni per abilitare il microfono nelle impostazioni del browser
- **Permesso revocato durante la registrazione**: interrompere gracefully e notificare l'utente
- Usare `navigator.permissions.query({ name: 'microphone' })` per verificare lo stato preventivamente (dove supportato)

### 5. Timer con durata della registrazione

Durante la registrazione:

- Mostrare un timer in tempo reale che conta i secondi dall'inizio
- Formato: `00:00` (minuti:secondi)
- Il timer si ferma quando l'utente preme Stop
- Il timer viene resettato quando l'utente cancella la registrazione

### 6. Supporto limite di durata massima

Aggiungere una prop `maxDuration` opzionale:

- Se specificata (in secondi), la registrazione si ferma automaticamente al raggiungimento del limite
- Mostrare un indicatore visuale del tempo rimanente (es. barra di progresso o cambio colore del timer)
- Notificare l'utente quando la registrazione viene fermata automaticamente

### 7. Fallback per browser non supportati

Gestire i browser che non supportano MediaRecorder:

- Verificare `typeof MediaRecorder !== 'undefined'` e `navigator.mediaDevices`
- Se non supportato: mostrare un messaggio esplicativo ("Il tuo browser non supporta la registrazione audio")
- Considerare la prop `fallback` per un componente alternativo (es. upload file audio)
- Documentare i browser supportati (Chrome 47+, Firefox 25+, Safari 14.1+, Edge 79+)

### 8. Storybook

Creare stories per tutti gli scenari:

- **Default**: componente pronto per registrare
- **Recording**: stato durante la registrazione con waveform e timer
- **Playback**: registrazione completata con player
- **Max Duration**: con limite di 30 secondi
- **Permission Denied**: stato di errore per permessi negati
- Documentare le prop e i pattern d'uso

## Stima effort

| Fase | Ore |
|------|-----|
| Setup MediaRecorder + stream audio | 1.5h |
| UI (pulsanti, timer, stati) | 2h |
| Waveform visualization | 1.5h |
| Gestione permessi | 0.5h |
| Max duration + fallback | 1h |
| Storybook | 1.5h |
| **Totale** | **8h** |
