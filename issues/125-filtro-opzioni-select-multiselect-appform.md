# Filtro opzioni select/multiselect in AppForm

| Campo      | Valore                |
|------------|-----------------------|
| **ID**     | 125                   |
| **Stack**  | laif-ds               |
| **Tipo**   | Bug                   |
| **Status** | Da iniziare           |
| **Priorità** | Media              |

## Descrizione originale

Ai campi select e multiselect di AppForm servirebbe la prop `searchable` come in AppSelect. Non vorrei sbagliarmi ma non mi pare di trovarla in `AppFormItems`.

## Piano di risoluzione

### 1. Analisi dello stato attuale

- Verificare il componente `AppSelect`: confermare che espone la prop `searchable` e come funziona (filtraggio locale delle opzioni tramite input di ricerca)
- Verificare il componente `AppFormItems`: controllare le definizioni dei tipi per le varianti `select` e `multiselect`
- Confermare che la prop `searchable` non viene effettivamente propagata da AppFormItems ad AppSelect

### 2. Mappatura del flusso delle prop

- Tracciare il percorso: `AppForm` -> `AppFormItems` -> `AppSelect`
- Identificare dove le prop vengono filtrate o destrutturate (probabile punto di perdita della prop)
- Controllare l'interfaccia/tipo TypeScript di `AppFormItems` per i campi select/multiselect

### 3. Implementare la propagazione

- Aggiungere `searchable?: boolean` all'interfaccia delle prop di AppFormItems per le varianti select e multiselect
- Propagare la prop `searchable` al componente `AppSelect` sottostante
- Assicurarsi che il valore di default sia `false` per mantenere la retrocompatibilita'
- Se esistono altre prop di AppSelect non esposte (es. `clearable`, `placeholder` per la ricerca), valutare se propagare anche quelle

### 4. Aggiornamento tipi

- Aggiornare i tipi TypeScript esportati dal pacchetto
- Assicurarsi che l'autocompletamento funzioni correttamente per chi usa il componente

### 5. Testing

- Testare in Storybook:
  - Select con `searchable={true}`: verificare che il filtro funzioni
  - Multiselect con `searchable={true}`: verificare che il filtro funzioni
  - Select/multiselect senza `searchable`: verificare che il comportamento di default non cambi
- Verificare che non ci siano regressioni sui form esistenti nei progetti che usano laif-ds

## Stima effort

**3 ore** — Propagazione prop + aggiornamento tipi + testing Storybook + verifica retrocompatibilita'
