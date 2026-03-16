# Chat refactor — Necessita' e problemi UI

| Campo      | Valore                |
|------------|-----------------------|
| **ID**     | 88                    |
| **Stack**  | laif-ds               |
| **Tipo**   | Bug                   |
| **Status** | In corso              |
| **Priorità** | Alta                |

## Descrizione originale

Alcuni appunti raccolti durante l'implementazione dell'agent - Chat refactor | Necessita' e problemi UI.

## Piano di risoluzione

### 1. Raccolta e revisione degli appunti esistenti

- Recuperare tutti gli appunti raccolti durante l'implementazione dell'agent
- Categorizzare i problemi per area:
  - **Layout**: problemi di struttura del componente chat (dimensioni, scrolling, responsiveness)
  - **Rendering messaggi**: formattazione, markdown, code blocks, media allegati
  - **Area di input**: composizione messaggio, toolbar azioni, invio
  - **UX generica**: feedback visivi, stati di caricamento, errori

### 2. Analisi del componente Chat attuale

- Mappare l'architettura del componente Chat in laif-ds
- Identificare i sotto-componenti: `ChatMessage`, `ChatInput`, `ChatList`, `ChatBubble`, ecc.
- Capire i limiti attuali che hanno generato le segnalazioni durante lo sviluppo dell'agent

### 3. Problemi noti da affrontare (da confermare con gli appunti)

- **Scroll automatico**: il chat deve scrollare automaticamente ai nuovi messaggi, ma permettere di risalire nella conversazione senza jump forzati
- **Streaming messaggi**: supporto per messaggi che arrivano in streaming (tipico di agent/AI), con rendering progressivo
- **Tipologie di messaggi**: supporto per messaggi di sistema, tool calls, thinking indicators oltre ai classici user/assistant
- **Layout responsivo**: il componente deve funzionare bene sia in sidebar stretta che in vista full-width
- **Performance**: rendering efficiente di conversazioni lunghe (virtualizzazione lista se necessario)

### 4. Refactor incrementale

Data la complessita' (12h stimate, gia' in corso), procedere per step:

1. **Step 1 — Fix critici**: risolvere i bug bloccanti che impattano l'uso dell'agent
2. **Step 2 — Struttura componente**: refactor dell'architettura interna per renderla piu' flessibile
3. **Step 3 — Nuove funzionalita'**: aggiungere supporto per i casi d'uso agent (streaming, tool calls, thinking)
4. **Step 4 — Polish**: animazioni, transizioni, micro-interazioni

### 5. Coordinamento

- Sincronizzarsi con chi sta implementando la feature agent per capire le priorita'
- Assicurarsi che il refactor non rompa le chat esistenti (es. customer care in Jubatus)
- Definire un'interfaccia stabile per il componente Chat che copra sia il caso "chat umana" che "chat con agent"

### 6. Testing

- Testare con conversazioni lunghe (100+ messaggi)
- Testare streaming di messaggi in tempo reale
- Testare su mobile e desktop
- Verificare accessibilita' (keyboard navigation, screen reader)
- Testare con contenuti misti: testo, codice, immagini, link

## Stima effort

**12 ore (1.5 giorni)** — Suddivise in:
- 2h raccolta requisiti e revisione appunti
- 4h refactor architettura componente
- 4h implementazione fix e nuove funzionalita'
- 2h testing e verifica regressioni
