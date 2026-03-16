# Navigazione stile mobile — bottom nav bar

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 71                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | In pausa           |
| Priorita  | Media              |
| Effort    | 16h                |

## Descrizione originale

> E' possibile implementare un menù che per schermi pc e ipad è la solita sidebar, mentre da mobile è un menù fisso in basso.

## Piano di risoluzione

1. **Progettare la bottom navigation bar**
   - Seguire le linee guida Material Design: massimo 5 elementi nella bottom nav
   - Definire le icone e le label per ogni voce
   - Prevedere uno stato attivo visivamente distinto (colore, peso icona)
   - Mockup rapido per validazione con il team

2. **Implementare lo switch sidebar/bottom nav con CSS media queries**
   - Breakpoint: sidebar per desktop e tablet (>= 768px), bottom nav per mobile (< 768px)
   - La sidebar si nasconde completamente su mobile (non collassa, sparisce)
   - La bottom nav si nasconde completamente su desktop/tablet
   - Usare `position: fixed` + `bottom: 0` per la bottom nav, con `z-index` adeguato

3. **Selezionare le voci per la bottom nav**
   - Identificare le 4-5 pagine più utilizzate nei progetti attuali
   - La selezione deve essere configurabile per progetto (non hardcoded)
   - Esempio default: Home, [Entità principale], Notifiche, Profilo

4. **Aggiungere un menu "Altro" per le voci rimanenti**
   - Ultima voce della bottom nav: icona "..." o "Altro"
   - Al tap: apre un drawer o un bottom sheet con tutte le altre voci di navigazione
   - Il drawer contiene le stesse voci della sidebar desktop
   - Animazione di apertura fluida (slide up)

5. **Integrare con il componente di navigazione di laif-ds**
   - Verificare se il componente `AppSidebar` di laif-ds supporta già la trasformazione
   - Se no: estendere il componente per accettare una prop `mode: 'sidebar' | 'bottom-nav'`
   - Mantenere la stessa struttura dati di navigazione per entrambe le modalità
   - Gestire i sotto-menu: su mobile, il tap su una voce con figli apre una sotto-navigazione

6. **Coordinare con il Refactor Navigazione (issue #111)**
   - Questa issue dipende dal refactor della navigazione
   - Verificare lo stato della issue #111 prima di procedere
   - Se #111 non è completata: implementare sulla struttura attuale con attenzione a non creare debito tecnico
   - Idealmente: attendere il refactor per evitare doppio lavoro

7. **Test su dispositivi reali**
   - Testare su iOS Safari e Android Chrome
   - Verificare il comportamento con la tastiera aperta (la bottom nav non deve sovrapporsi)
   - Gestire il "safe area" per dispositivi con notch/home indicator
   - Testare la transizione sidebar/bottom nav in landscape su tablet

## Stima effort

- Design bottom nav e mockup: ~2h
- Implementazione CSS responsive switch: ~3h
- Selezione voci e configurazione: ~2h
- Menu "Altro" con drawer: ~3h
- Integrazione con laif-ds: ~3h
- Test dispositivi e fix: ~2h
- Documentazione: ~1h
- **Totale: ~16h**
