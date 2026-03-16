# Dashboard standard per il template

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 56                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | —                  |

## Descrizione originale

> Dashboard standard (stile Notion) da mettere nel template (al posto del conversazion o profile)

## Piano di risoluzione

1. **Progettare il layout della dashboard a widget**
   - Layout basato su griglia (CSS Grid), stile Notion/dashboard moderna
   - Widget di dimensioni diverse: small (1 colonna), medium (2 colonne), large (full width)
   - Responsive: su mobile i widget si impilano in colonna singola
   - Mockup della disposizione di default per validazione con il team

2. **Implementare i widget standard**
   - **KPI cards**: numeri chiave con trend (es. +12% rispetto a ieri), icona e colore configurabili
   - **Attività recenti**: lista cronologica delle ultime azioni (creazione, modifica, eliminazione)
   - **Grafici**: barre, linee, torta — wrapper su libreria charts (Recharts o Chart.js)
   - **Quick actions**: pulsanti per le azioni più frequenti (crea nuovo X, vai a Y)
   - **Tabella riassuntiva**: top N elementi per una metrica (es. ticket aperti per priorità)

3. **Rendere i widget configurabili per progetto**
   - File di configurazione (JSON o DB) che definisce quali widget mostrare e in che ordine
   - Ogni widget ha: tipo, titolo, dimensione, endpoint dati, parametri specifici
   - Configurazione di default nel template, sovrascrivibile per progetto
   - Possibilità futura: drag & drop per riordinare (non in v1)

4. **Usare CSS Grid per il layout responsive**
   - Desktop: griglia a 4 colonne
   - Tablet: griglia a 2 colonne
   - Mobile: colonna singola
   - Gap e padding consistenti con il design system laif-ds
   - Skeleton loading per ogni widget durante il caricamento dati

5. **Backend: endpoint di aggregazione per i widget**
   - Endpoint generico `GET /api/dashboard/widgets/{widget_id}` che restituisce i dati per un widget
   - Ogni tipo di widget ha il suo handler backend registrato in un registry
   - Cache dei dati aggregati (TTL configurabile per tipo di widget)
   - Il progetto registra i propri widget handler con i dati specifici dell'applicazione

6. **Aggiungere al template come landing page di default**
   - Sostituire la pagina corrente (conversazione o profilo) con la dashboard
   - Mantenere la pagina precedente accessibile come route separata
   - La dashboard è la prima cosa che l'utente vede dopo il login
   - Configurabile: il progetto può scegliere una landing page diversa

## Stima effort

- Design layout e mockup: ~3h
- Widget standard (KPI, attività, grafici, quick actions): ~10h
- Sistema configurazione widget: ~4h
- Layout CSS Grid responsive: ~3h
- Backend endpoint aggregazione: ~6h
- Integrazione nel template come landing page: ~2h
- Test e documentazione: ~2h
- **Totale: ~30h** (stima iniziale, da raffinare)
