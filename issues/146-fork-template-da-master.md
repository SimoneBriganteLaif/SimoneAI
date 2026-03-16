# Fork template da master invece di dev

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 146                |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | —                  |

## Descrizione originale

> Al momento i nostri fork partono da dev. Questo puo generare app che sono ad una versione maggiore del template, con cose magari non del tutto testate.

## Piano di risoluzione

1. **Aggiornare la documentazione per specificare il fork da master**
   - Modificare il README del template e qualsiasi guida di setup progetto
   - Specificare chiaramente: "I nuovi progetti devono fare fork da `master` (o `main`), non da `dev`"
   - Spiegare la motivazione: `dev` contiene feature non testate/rilasciate, `master` e' stabile

2. **Aggiornare automazioni e script di creazione fork**
   - Verificare se esistono script o automazioni che creano fork automaticamente
   - Se si: modificare il branch sorgente da `dev` a `master`/`main`
   - Se si usa copier (issue #94): configurare il branch sorgente nel template copier

3. **Assicurarsi che master contenga sempre l'ultima release stabile**
   - Verificare il flusso di rilascio attuale: `dev` → `staging` → `master`?
   - Assicurarsi che i merge in master avvengano regolarmente dopo il testing
   - Eventualmente automatizzare il merge in master dopo una release validata

4. **Valutare impatto sulle issue correlate**
   - Issue #94 (copier): se si adotta copier per la creazione progetti, configurare il branch sorgente correttamente
   - Issue #73 (semplificazione upstream): il cambio di branch sorgente potrebbe semplificare il processo di upstream
   - Issue #74 (modularizzazione): una base stabile (master) rende la modularizzazione piu prevedibile

5. **Comunicare il cambiamento a tutti gli sviluppatori**
   - Notifica al team del cambio di procedura
   - Verificare che i progetti in corso non siano impattati
   - Per i progetti gia forkati da dev: nessun intervento necessario (sono gia avviati)

## Stima effort

- Aggiornamento documentazione: ~0.5h
- Aggiornamento script/automazioni: ~1h
- Verifica flusso di rilascio: ~0.5h
- Comunicazione al team: ~0.5h
- **Totale: ~2-3h**
