# KPI fiducia cliente nell'applicativo

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 150                |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | —                  |
| Tag       | Filone Monitoring  |

## Descrizione originale

> Studiamo una serie di KPI per tracciare lo stato di fiducia del cliente nei confronti dell'applicativo

## Piano di risoluzione

1. **Definire i KPI di fiducia/soddisfazione**
   - **Durata sessione media**: sessioni più lunghe indicano engagement (ma attenzione: potrebbe indicare anche difficoltà)
   - **Frequenza di utilizzo feature**: quali funzionalità vengono usate e quanto spesso
   - **Tasso di errori incontrati**: quanti errori vede l'utente per sessione
   - **Frequenza ticket di supporto**: trend nel tempo, correlato alla fiducia
   - **Task completion rate**: percentuale di azioni iniziate e completate con successo
   - **Bounce rate**: utenti che accedono e escono subito senza interagire
   - **Feature adoption rate**: percentuale di utenti che usano una nuova funzionalità dopo il rilascio

2. **Aggiungere tracking eventi frontend (anonimo, GDPR-compliant)**
   - Creare un modulo di tracking leggero nel frontend del template
   - Eventi da tracciare: page view, click su feature, inizio/completamento task, errori visualizzati
   - Nessun dato personale: solo ID sessione anonimo, timestamp, tipo evento, metadata
   - Consenso: informare l'utente e rispettare le preferenze cookie/privacy
   - Storage: invio eventi al backend via batch (non uno per uno, per performance)

3. **Backend: endpoint di aggregazione analytics**
   - Endpoint `POST /api/analytics/events` per ricevere i batch di eventi dal frontend
   - Tabella `analytics_events(id, session_id, event_type, metadata, timestamp)`
   - Endpoint `GET /api/analytics/kpi` per i KPI aggregati (protetto, solo admin)
   - Aggregazioni: per giorno, settimana, mese — con confronto periodo precedente
   - Job schedulato per pre-calcolare le aggregazioni (evitare query pesanti on-demand)

4. **Dashboard di visualizzazione KPI**
   - Pagina admin dedicata con grafici dei KPI nel tempo
   - Grafici: linee per trend temporali, barre per confronti, numeri per KPI puntuali
   - Filtri: periodo temporale, ruolo utente, feature specifica
   - Indicatori visivi: freccia verde/rossa per trend positivo/negativo rispetto al periodo precedente
   - Usare una libreria charts (es. Recharts o Chart.js) già compatibile con laif-ds

5. **Configurare soglie di allarme per metriche in calo**
   - Definire soglie per ogni KPI (es. session duration -20% = warning)
   - Notifica via email o Teams quando una soglia viene superata
   - Configurabile per progetto dall'admin UI
   - Utile per intercettare cali di fiducia prima che diventino critici

6. **Partire con metriche base, iterare**
   - Fase 1: solo page view, session duration, error rate (le più semplici da implementare)
   - Fase 2: feature usage, task completion rate
   - Fase 3: dashboard completa, soglie di allarme, correlazioni
   - Raccogliere feedback dal team su quali KPI sono davvero utili prima di investire sulle fasi avanzate

## Stima effort

- Definizione KPI e design: ~2h
- Tracking eventi frontend: ~6h
- Backend aggregazione: ~6h
- Dashboard visualizzazione: ~8h
- Soglie di allarme: ~4h
- Test e documentazione: ~2h
- **Totale: ~28h** (stima per tutte le fasi; fase 1 sola ~10h)
