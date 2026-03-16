# Focus modale — Disabilitare autofocus in modalità edit

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 104             |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | Backlog         |
| **Effort stimato** | 2h       |

## Descrizione originale

Molto utile avere il focus in fase di create appena si apre un modale. A mio avviso non è utile in caso di edit, magari ho un form pieno di dati, lo apro per modificarne uno, trovo evidenziato il primo input testuale.

## Piano di risoluzione

### 1. Aggiungere la prop `autoFocus` al componente modale

Estendere l'interfaccia del componente dialog/modal:

- Aggiungere `autoFocus?: boolean` con default `true` per garantire retrocompatibilità
- Quando `autoFocus={true}`: comportamento attuale (focus sul primo campo input all'apertura)
- Quando `autoFocus={false}`: il modale si apre senza spostare il focus su nessun campo del form

### 2. Valutare l'aggiunta di una prop `mode`

Come alternativa o complemento a `autoFocus`, considerare una prop `mode`:

- `mode?: 'create' | 'edit'`
- In modalità `create`: autofocus attivo (l'utente sta per compilare un form vuoto)
- In modalità `edit`: autofocus disabilitato (l'utente vuole prima osservare i dati esistenti)
- Questa prop potrebbe controllare automaticamente il focus senza che lo sviluppatore debba gestire `autoFocus` manualmente
- Se si implementa `mode`, il `autoFocus` esplicito dovrebbe avere priorità su `mode`

### 3. Implementazione del controllo focus

Modificare la logica di apertura del modale:

- Intercettare il momento in cui il modale diventa visibile (es. `useEffect` con dipendenza su `open`)
- Se `autoFocus` è `true` (o `mode` è `create`): cercare il primo elemento focusable e applicare `.focus()`
- Se `autoFocus` è `false` (o `mode` è `edit`): non applicare focus automatico su campi del form, ma mantenere il focus trap del modale per accessibilità (focus sul container del modale o sul pulsante di chiusura)

### 4. Documentare il comportamento

- Aggiornare la documentazione Storybook con esempi per entrambi i casi
- Story "Create Mode": modale con autofocus sul primo campo
- Story "Edit Mode": modale con dati precompilati, senza autofocus
- Documentare nella description della prop la motivazione UX della distinzione

## Stima effort

| Fase | Ore |
|------|-----|
| Implementazione prop `autoFocus` | 0.5h |
| Valutazione e implementazione prop `mode` | 0.5h |
| Logica controllo focus | 0.5h |
| Storybook + documentazione | 0.5h |
| **Totale** | **2h** |
