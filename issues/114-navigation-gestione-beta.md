# Navigation — Gestione Beta

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 114             |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | Da iniziare     |
| **Priorità**| Bassa           |
| **Effort stimato** | 4h       |

## Descrizione originale

Navigation - Gestione Beta.

## Piano di risoluzione

### 1. Aggiungere la prop `badge` agli item di navigazione

Estendere l'interfaccia dei navigation item con una prop opzionale per mostrare un badge:

- Aggiungere `badge?: string` (es. `"Beta"`, `"New"`, `"Alpha"`) all'interfaccia dell'item
- Oppure, in alternativa, una prop booleana `beta?: boolean` se si vuole un approccio più semplice
- La soluzione con stringa è preferibile perché più flessibile (permette testi diversi come "Beta", "New", "Alpha", "Soon")

### 2. Rendering del badge accanto alla label

Quando `badge` è valorizzato:

- Mostrare un badge inline accanto al testo dell'item di navigazione
- Posizionamento: a destra della label, con un piccolo margine
- Il badge deve essere visibile sia nella navigazione espansa che in quella compressa (tooltip o overlay)

### 3. Stile del badge con token del tema

Definire lo stile del badge utilizzando i design token esistenti:

- Background: usare un colore che si distingua ma non sia troppo aggressivo (es. `--color-info-light` o un token dedicato)
- Testo: piccolo, uppercase o capitalized, font-weight medium
- Border-radius arrotondato (pill shape)
- Dimensioni compatte per non sbilanciare il layout della navigazione

### 4. Personalizzazione del badge

Permettere la customizzazione del badge:

- Prop `badgeVariant` opzionale per varianti di colore (info, warning, success)
- Oppure supporto a classi CSS custom tramite `badgeClassName`
- Default: variante "info" (blu/azzurro) per il caso "Beta"

### 5. Aggiornare Storybook

- Aggiungere esempi con item di navigazione che mostrano badge "Beta", "New", "Alpha"
- Mostrare le diverse varianti di colore disponibili
- Documentare la nuova prop nell'interfaccia del componente

## Stima effort

| Fase | Ore |
|------|-----|
| Implementazione prop e rendering | 1.5h |
| Stile e token | 1h |
| Personalizzazione varianti | 0.5h |
| Storybook | 1h |
| **Totale** | **4h** |
