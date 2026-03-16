# Colori Toaster assenti senza richColors

| Campo      | Valore                |
|------------|-----------------------|
| **ID**     | 110                   |
| **Stack**  | laif-ds               |
| **Tipo**   | Bug                   |
| **Status** | Da iniziare           |
| **Priorità** | Alta                |

## Descrizione originale

E' necessario passare `richColors={false}` per visualizzare i colori degli status del Toaster. Evocare `toast.<status>()` dovrebbe mostrare testo e icona colorati del token dello status.

## Piano di risoluzione

### 1. Analisi del setup attuale del Toaster

- Individuare il componente Toaster nella codebase laif-ds (probabilmente un wrapper di `sonner`)
- Verificare come sono configurate le variabili CSS per i colori degli status (success, error, warning, info)
- Capire il comportamento attuale di `richColors`:
  - `richColors={true}` (default di sonner): applica sfondo colorato
  - `richColors={false}`: mostra testo e icona colorati ma sfondo neutro
  - Il comportamento desiderato e' che testo e icona siano sempre colorati, indipendentemente da `richColors`

### 2. Identificare il problema

- Probabile causa: i CSS custom del Toaster laif-ds sovrascrivono o non definiscono i colori per testo/icona nello stato default (senza `richColors`)
- Verificare se mancano le variabili CSS `--success-text`, `--error-text`, ecc. oppure se sono impostate su valori neutri

### 3. Implementare la fix

- Definire le variabili CSS corrette per i colori di testo e icona di ogni status:
  - `success`: colore token success
  - `error`: colore token error/destructive
  - `warning`: colore token warning
  - `info`: colore token info
- Assicurarsi che questi colori siano applicati di default, senza bisogno di prop aggiuntive
- La prop `richColors` deve controllare solo lo sfondo colorato, non il colore di testo e icona

### 4. Testing

- Testare ogni variante: `toast.success()`, `toast.error()`, `toast.warning()`, `toast.info()`
- Verificare che senza `richColors` si vedano testo e icona colorati su sfondo neutro
- Verificare che con `richColors={true}` lo sfondo diventi colorato
- Controllare sia in tema chiaro che scuro

## Stima effort

**1 ora** — Fix variabili CSS + testing dei 4 stati + verifica tema chiaro/scuro
