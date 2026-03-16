# Censimento compatibilita' componenti Firefox

| Campo      | Valore                |
|------------|-----------------------|
| **ID**     | 126                   |
| **Stack**  | laif-ds               |
| **Tipo**   | Bug                   |
| **Status** | Backlog               |
| **Priorità** | Media              |

## Descrizione originale

Alcuni componenti come l'input di tipo month perdono funzionalita' su Firefox.

## Piano di risoluzione

### 1. Preparazione matrice di test

- Elencare tutti i componenti laif-ds che hanno interazione utente (form controls, pickers, selects, ecc.)
- Creare una matrice di test con le colonne: componente, funzionalita', Chrome, Firefox, stato
- Componenti prioritari da verificare:
  - Input `type="month"` (segnalato come problematico)
  - Input `type="date"` e `type="datetime-local"`
  - Input `type="time"`
  - Input `type="color"`
  - AppSelect / Multiselect
  - AppDatePicker / AppDateRangePicker
  - File upload / drag-and-drop
  - AppSlider
  - Tutti i componenti che usano API CSS/JS non universali

### 2. Esecuzione test su Firefox

- Usare l'ultima versione stabile di Firefox
- Per ogni componente:
  - Verificare il rendering visivo (layout, dimensioni, stili)
  - Verificare la funzionalita' interattiva (click, input, selezione, validazione)
  - Documentare eventuali differenze o malfunzionamenti rispetto a Chrome
  - Screenshot se utile per documentare il problema

### 3. Classificazione dei problemi trovati

Per ogni problema identificato, classificare per:
- **Gravita'**: bloccante (componente inutilizzabile), degradato (funziona ma con limitazioni), cosmetico (solo visivo)
- **Frequenza d'uso**: quanto spesso il componente viene usato nei progetti LAIF
- **Priorita' fix**: alta (bloccante + uso frequente), media, bassa

### 4. Proposte di risoluzione per componente

Per ciascun componente problematico:
- **Input `type="month"`**: Firefox non supporta nativamente il picker month. Soluzione: sostituire con un custom date picker limitato a mese/anno, oppure usare un select con mesi + anno
- **Input `type="date"`** (se problematico): verificare se il date picker custom di laif-ds e' gia' usato come fallback
- **Altri componenti**: per ciascuno, proporre polyfill, custom implementation o CSS fix

### 5. Implementazione fix

- Procedere per priorita' (alta prima)
- Per ogni fix:
  - Implementare la soluzione
  - Testare su Firefox E su Chrome (no regressioni)
  - Aggiornare Storybook con note di compatibilita' se necessario

### 6. Deliverable

- Report di compatibilita' Firefox (tabella markdown)
- PR separate per ogni fix (raggruppate per componente)
- Eventuale aggiornamento della documentazione laif-ds con note browser support

## Stima effort

**16 ore (2 giorni)** — Suddivise in:
- 4h per censimento e test sistematico
- 8h per implementazione fix dei componenti problematici
- 2h per testing regressioni cross-browser
- 2h per documentazione e report finale
