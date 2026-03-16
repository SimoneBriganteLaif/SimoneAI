# AppDialog mobile — Drawer bottom-up

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 89              |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | Backlog         |
| **Effort stimato** | 6h       |

## Descrizione originale

AppDialog mobile → Usare componente Drawer (bottom-up).

## Piano di risoluzione

### 1. Creare o integrare un componente Drawer (bottom-up sheet)

Verificare se esiste già un componente Drawer in laif-ds. Se non esiste:

- Creare un componente `AppDrawer` con animazione bottom-up (slide dal basso verso l'alto)
- Il Drawer deve supportare: apertura/chiusura animata, overlay/backdrop, altezza variabile (snap points opzionali)
- Struttura: header con handle di trascinamento, body scrollabile, footer opzionale
- Utilizzare CSS transitions o `framer-motion` (se già in uso nel progetto) per le animazioni

### 2. Aggiungere comportamento responsive a AppDialog

Modificare AppDialog per rilevare la viewport:

- Utilizzare un media query o un hook `useMediaQuery` per rilevare la larghezza dello schermo
- Sotto il breakpoint (es. `768px` o il breakpoint `md` del design system), renderizzare come Drawer
- Sopra il breakpoint: mantenere il comportamento attuale (modal centrato)
- Il breakpoint deve essere configurabile tramite prop opzionale `mobileBreakpoint`

### 3. Rendering condizionale sotto breakpoint

Quando la viewport è sotto il breakpoint:

- Il contenuto del dialog viene renderizzato dentro il componente Drawer
- L'animazione cambia da fade-in/scale a slide-up dal basso
- Il dialog occupa la larghezza completa dello schermo
- L'altezza si adatta al contenuto (con un massimo dell'85-90% della viewport height)
- Il border-radius si applica solo agli angoli superiori

### 4. Mantenere la stessa API per gli sviluppatori

L'interfaccia pubblica di AppDialog non deve cambiare:

- Stesse prop (`open`, `onClose`, `title`, `children`, ecc.)
- Stesso comportamento logico (apertura, chiusura, callback)
- Il cambio di rendering è trasparente per chi usa il componente
- Aggiungere prop opzionale `disableMobileDrawer` per chi vuole forzare il modal anche su mobile

### 5. Gesture touch (swipe down to close)

Sul Drawer mobile:

- Implementare il gesto "swipe down" per chiudere il drawer
- Rilevare il touch start, touch move, touch end sull'handle o sull'header
- Se il drag verso il basso supera una soglia (es. 100px o 30% dell'altezza), chiudere il drawer
- Animazione fluida durante il trascinamento (il drawer segue il dito)
- Supportare anche il tap sull'overlay per chiudere

### 6. Test su dispositivi mobili reali

Verificare il comportamento su:

- iOS Safari (iPhone)
- Android Chrome
- Tablet (verifica del breakpoint)
- Testare con contenuti di diverse altezze (form brevi, form lunghi con scroll)
- Verificare che la tastiera virtuale non causi problemi di layout
- Testare le gesture touch su diversi dispositivi

## Stima effort

| Fase | Ore |
|------|-----|
| Componente Drawer base | 2h |
| Comportamento responsive AppDialog | 1h |
| Rendering condizionale | 1h |
| Gesture touch | 1h |
| Test dispositivi + Storybook | 1h |
| **Totale** | **6h** |
