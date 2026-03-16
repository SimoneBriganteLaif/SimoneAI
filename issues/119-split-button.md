# Nuovo componente SplitButton

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 119             |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | Backlog         |
| **Effort stimato** | 6h       |

## Descrizione originale

Uno split button è un pulsante con due componenti: un'etichetta e una freccia. Cliccando sull'etichetta si seleziona un'azione predefinita, mentre cliccando sulla freccia si apre un menu con altre azioni possibili.

## Piano di risoluzione

### 1. Progettare l'API del componente

Definire l'interfaccia pubblica del SplitButton:

```typescript
interface SplitButtonProps {
  label: string;                    // Testo dell'azione primaria
  onClick: () => void;              // Handler azione primaria
  items: SplitButtonItem[];         // Azioni secondarie nel dropdown
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
}

interface SplitButtonItem {
  label: string;
  onClick: () => void;
  icon?: ReactNode;
  disabled?: boolean;
  danger?: boolean;                 // Per azioni distruttive (es. "Elimina")
}
```

### 2. Implementare il componente con due zone cliccabili

Struttura DOM:

- Container wrapper con `display: flex`
- Zona sinistra: pulsante principale con label e stile di AppButton
- Separatore verticale visuale (border o divider)
- Zona destra: pulsante piccolo con icona freccia (chevron down)
- Le due zone condividono lo stesso stile di base ma sono elementi cliccabili separati

### 3. Riutilizzare gli stili di AppButton

Per coerenza con il design system:

- Applicare le stesse varianti di colore di AppButton (primary, secondary, outline)
- Stessi token per padding, border-radius, font
- Il border-radius si applica solo agli estremi esterni (sinistra per il pulsante, destra per la freccia)
- Hover e active state coerenti con AppButton

### 4. Dropdown con componenti esistenti

Per il menu dropdown:

- Riutilizzare il componente menu/popover esistente in laif-ds
- Il menu si apre al click sulla zona freccia
- Posizionamento: sotto il pulsante, allineato a destra
- Chiusura: click esterno, click su un item, tasto Escape

### 5. Supporto varianti

Implementare le varianti visive:

- **Primary**: sfondo pieno, colore primario
- **Secondary**: sfondo secondario, testo scuro
- **Outline**: bordo, sfondo trasparente
- Ogni variante deve funzionare correttamente su entrambe le zone (pulsante + freccia)

### 6. Navigazione da tastiera

Accessibilità e keyboard navigation:

- `Tab`: focus sul pulsante principale
- `Enter` / `Space` sul pulsante: esegue l'azione primaria
- `Tab` successivo (o `ArrowRight`): focus sulla freccia
- `Enter` / `Space` / `ArrowDown` sulla freccia: apre il menu dropdown
- `ArrowUp` / `ArrowDown` nel menu: navigazione tra gli item
- `Enter` su un item: esegue l'azione e chiude il menu
- `Escape`: chiude il menu
- Attributi ARIA: `aria-haspopup`, `aria-expanded`, ruoli appropriati

### 7. Integrazione con DataTable

Considerare l'uso del SplitButton nelle azioni delle righe della DataTable:

- Azione primaria visibile, azioni secondarie nel dropdown
- Verificare che le dimensioni siano adeguate per celle di tabella (size `sm`)
- Testare il posizionamento del dropdown quando il pulsante è vicino ai bordi della tabella

### 8. Documentazione Storybook

Creare stories complete:

- **Default**: split button con azione primaria e 3 azioni secondarie
- **Variants**: primary, secondary, outline a confronto
- **In DataTable**: esempio di integrazione in una riga di tabella
- **With Icons**: azioni secondarie con icone
- **Danger Action**: azione distruttiva nel dropdown
- Documentare tutte le prop e i pattern d'uso

## Stima effort

| Fase | Ore |
|------|-----|
| Design API | 0.5h |
| Implementazione componente base | 2h |
| Stili e varianti | 1h |
| Dropdown + menu | 1h |
| Keyboard navigation + a11y | 0.5h |
| Storybook | 1h |
| **Totale** | **6h** |
