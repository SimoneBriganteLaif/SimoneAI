# Visualizzazione orari WeeklyCalendar per eventi brevi

| Campo      | Valore                |
|------------|-----------------------|
| **ID**     | 160                   |
| **Stack**  | laif-ds               |
| **Tipo**   | Bug                   |
| **Status** | Backlog               |
| **Priorità** | Media              |

## Descrizione originale

Nella visualizzazione del WeeklyCalendar del ds, quando gli eventi sono più brevi di 45 minuti, l'orario dell'evento, che si vede sotto al titolo, esce dallo spazio dell'evento stesso.

## Piano di risoluzione

### 1. Analisi del componente WeeklyCalendar

- Individuare il componente `WeeklyCalendar` nella codebase laif-ds
- Trovare la logica di rendering degli eventi (slot temporali, calcolo altezza)
- Capire come vengono calcolate le dimensioni del blocco evento in base alla durata

### 2. Identificare la causa dell'overflow

- Il blocco evento ha un'altezza calcolata proporzionale alla durata
- Per eventi < 45 min l'altezza risultante non contiene titolo + orario
- L'orario (label secondaria sotto il titolo) trabocca fuori dal contenitore

### 3. Implementare la fix

- **Opzione A — Nascondere l'orario sotto una soglia**: se l'altezza calcolata dell'evento e' inferiore a una soglia (es. corrispondente a ~45 min), nascondere la riga dell'orario con `overflow: hidden` e mostrare solo il titolo
- **Opzione B — Testo inline**: per eventi brevi, mostrare titolo e orario sulla stessa riga con `text-overflow: ellipsis` e `white-space: nowrap`
- **Opzione C — Tooltip**: per eventi molto corti (< 30 min), mostrare solo il titolo troncato e spostare i dettagli in un tooltip al hover
- Valutare quale opzione offre la migliore UX; probabilmente una combinazione: inline per 30-45 min, solo titolo + tooltip per < 30 min

### 4. Aggiungere min-height e overflow safety

- Impostare un `min-height` ragionevole sul blocco evento (es. equivalente a 15 min) per evitare che eventi brevissimi diventino invisibili
- Aggiungere `overflow: hidden` come rete di sicurezza sul contenitore evento

### 5. Testing

- Testare con eventi di durate diverse: 15 min, 30 min, 45 min, 1h, 2h
- Verificare che il titolo resti sempre leggibile
- Verificare che l'orario non trabocchi in nessun caso
- Controllare in Storybook e su viewport diversi (desktop e tablet)

## Stima effort

**2 ore** — Fix CSS/logica condizionale + testing su durate diverse
