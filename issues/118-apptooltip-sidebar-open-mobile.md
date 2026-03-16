# AppTooltip nella sidebar inizializzato a open su mobile

| Campo      | Valore                |
|------------|-----------------------|
| **ID**     | 118                   |
| **Stack**  | laif-ds               |
| **Tipo**   | Bug                   |
| **Status** | Backlog               |
| **Priorità** | Bassa               |

## Descrizione originale

AppTooltip nella sidebar inizializzato a open su mobile - da testare.

## Piano di risoluzione

### 1. Riproduzione del bug

- Aprire l'app con la sidebar su viewport mobile (< 768px) o su dispositivo touch reale
- Verificare se l'AppTooltip appare gia' aperto al mount del componente
- Identificare quale tooltip specifico nella sidebar presenta il problema (probabilmente i tooltip sulle icone di navigazione quando la sidebar e' collassata)

### 2. Analisi della causa

- Controllare il componente `AppTooltip` nella codebase laif-ds
- Verificare come viene gestito lo stato `open`:
  - Se usa `defaultOpen` impostato a `true`
  - Se lo stato iniziale dipende da un evento hover/focus che su mobile si attiva al primo tap
  - Se c'e' un listener `mouseenter` che su touch devices viene triggerato al mount
- Controllare se il componente distingue tra dispositivi touch e non-touch

### 3. Implementare la fix

- **Rilevamento touch device**: usare `window.matchMedia('(hover: none)')` o `'ontouchstart' in window` per determinare se il dispositivo e' touch
- **Su dispositivi touch**:
  - Non impostare `open` a `true` al mount
  - Gestire l'apertura del tooltip tramite tap esplicito (non hover)
  - Chiudere il tooltip al tap fuori dall'elemento
- **Su desktop**: mantenere il comportamento attuale (hover per aprire)
- Alternativa: usare `delayDuration` per evitare aperture accidentali e assicurarsi che `defaultOpen` sia sempre `false`

### 4. Considerazioni sulla sidebar

- Quando la sidebar e' collassata su mobile, i tooltip sono necessari per mostrare il nome delle voci di navigazione
- Valutare se su mobile convenga usare un approccio diverso (es. long-press per tooltip, oppure label compatte al posto dei tooltip)

### 5. Testing

- Testare su Chrome DevTools in modalita' responsive (vari viewport mobile)
- Testare su dispositivo fisico iOS (Safari) e Android (Chrome)
- Verificare che il tooltip non appaia al mount
- Verificare che si apra correttamente al tap e si chiuda al tap esterno
- Verificare che su desktop il comportamento hover resti invariato

## Stima effort

**4 ore** — Analisi + fix event handling touch/hover + testing cross-device
