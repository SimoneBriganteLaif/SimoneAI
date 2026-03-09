---
fonte: notion
url: https://www.notion.so/30690ad6ee4880a8b590c575621a78be
data: 2026-02-13
partecipanti: [Team LAIF (Simone, Lorenzo)]
tipo: review
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
---

# Riunione Sviluppo Applicativo Customer Care

## Processo Attuale di Customer Care

- Tutte le richieste arrivano via email a info@
- Per eventi complessi viene creato un file Excel condiviso manualmente con: email utente, ID ordine, motivo segnalazione, stato, note, link documenti, conferma invio email chiusura
- Distinzione eventi: oggetto email o ricerca su dashboard tramite email utente per trovare event ID
- 2-4 persone massimo lavorano contemporaneamente sui ticket nei picchi
- Alcune modifiche richiedono intervento manuale su video/foto

## Dashboard e Strumenti Attuali

- Dashboard Grafana usata per ricerche: inserendo email si vedono ordini, event ID, items ricevuti (foto/video)
- Controllo proattivo utenti con pochi ordini per verificare se selfie è corretto
- Accesso diretto database MySQL su RDS per modifiche tecniche
- Percorsi S3 per video/foto accessibili da ordini

## Richieste Frequenti

- Utenti non trovano foto o area personale: risolto inviando link MyMemories con verifica e hash ID
- Confusione tra email preview e area personale completa
- Problemi accesso gestiti da HCD
- Selfie sbagliati o inadeguati per riconoscimento facciale

## Architettura Tecnica

- Database: MySQL su RDS
- Storage: S3 buckets per foto e video
- Tutto hostato su AWS account Jubatus
- Se deploy su account Jubatus: accesso semplificato tramite security group
- Se deploy su account separato: necessario SSH per connessione database
- Preferenza iniziale: deploy su account Jubatus per semplicità gestione

## Funzionalità Desiderate per Nuovo Applicativo

### Gestione ticket
- Visualizzazione mail con corpo messaggio e possibilità risposta
- Stati: nuovo, work in progress, stand-by, in attesa cliente, fatto
- Assegnazione ticket a specifici utenti/team
- Note e link a Google Drive per documenti

### Categorizzazione e priorità
- Categorie automatiche basate su contenuto email
- Tag multipli: errore foto, intervento database, intervento S3, video editing
- Template risposte automatiche per categoria
- Priorità basata su categoria e data arrivo
- Sentiment analysis per urgenza

### Pagina utente integrata
- Clic su utente mostra: eventi partecipati, ordini effettuati, contenuti acquistati
- Visualizzazione diretta selfie da S3 (non più manuale)
- Link automatici a MyMemories invece di copia manuale hash ID

### Funzionalità aggiuntive
- Sezione gestione evento: controllo preordini, statistiche
- Export CSV utenti senza acquisti per campagne marketing
- Dashboard metriche evento (numero acquisti, trend)
- Gestione thread e follow-up email

## Canali Supporto

- Principale: email (da prioritizzare)
- Nice to have: DM Instagram, WhatsApp (da valutare in futuro)
- Per social: reindirizzamento a email tramite risposta automatica

## Demo Mostrata

- Applicativo esempio con inbox mail, categorizzazione, possibilità risposta
- Filtri per evento, categoria, priorità
- Obiettivo: ridurre numero di clic necessari per risolvere ticket

## Prossimi Passi

- [ ] Jonathan: condividere schema database aggiornato
- [ ] Jonathan: verificare con Marco e Simone preferenze per deploy AWS (account Jubatus vs separato)
- [ ] Federico: preparare mockup e flussi schermata principale
- [ ] Team: creare data model dell'applicazione (mail, utenti, tag, categorie, risposte)
- [ ] Team: validare iterazioni frontend prima di collegare dati reali

## Decisioni

- **Hosting**: Deployare sull'account AWS di Jubatus per semplificare accesso al database MySQL RDS e bucket S3
- **Approccio iterativo**: Prima validare mockup e flussi utente con dati finti, successivamente collegare i dati reali
- **Priorità**: Focus iniziale sulla gestione segnalazioni email con categorizzazione e ticket management
