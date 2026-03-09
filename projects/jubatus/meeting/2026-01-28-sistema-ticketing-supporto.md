---
fonte: notion
url: https://www.notion.so/2f690ad6ee4880709c36dcc84be184fb
data: 2026-01-28
partecipanti: [Team LAIF (Simone, Federico)]
tipo: follow-up
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
---

# Discussione Sistema di Ticketing e Supporto Clienti

## Panoramica

Incontro tecnico per discutere l'implementazione di un nuovo sistema di gestione ticket per il customer service, con focus sull'automazione dei processi attuali e integrazione di chatbot.

## Processo Attuale (AS IS)

- **Gestione centralizzata via email**: Tutte le segnalazioni clienti arrivano all'indirizzo info@ (non dedicato al supporto)
- **To-do list manuale**: Utilizzo di un foglio Google per tracciare tipo di problema, email cliente e stato di risoluzione
- **Team di supporto**: Tre persone gestiscono le email — Gionata, Lorenza e Logan
- **Dashboard Grafana interna**: Permette di interrogare il database inserendo l'email dell'utente per vedere tutti gli ordini, ricerche e contenuti
- **Escalation informale**: Problemi complessi vengono segnalati a Marco e altro membro del team, ma non esiste una gerarchia formale
- **Tempi di risoluzione**: Obiettivo massimo di due giorni, ma ritardi quando i referenti tecnici non sono disponibili

## Problemi Più Comuni

- Utenti che non trovano le foto (spesso dovuto a selfie di bassa qualità)
- Richieste di spiegazione del servizio
- Contenuti non ancora caricati dai fotografi
- La maggior parte dei problemi si risolve interrogando il database con l'email dell'utente

## Soluzioni Proposte

### Piattaforma di Ticketing Interna

- Centralizzare tutte le segnalazioni in un unico portale
- Raccolta automatica da email e potenzialmente da altri canali (Instagram, WhatsApp)
- Categorizzazione automatica dei ticket
- Integrazione diretta con database per mostrare informazioni utente (ordini, ricerche, link AWS, selfie) senza dover aprire pagine multiple
- Query SQL già esistenti possono essere riutilizzate dalla dashboard Grafana attuale
- Risposte automatiche per problemi standard/frequenti
- Sistema di analytics per identificare problemi ricorrenti ed eventi problematici

### Chatbot in Web App

- Integrazione di chatbot direttamente nella piattaforma (iframe in basso a destra)
- Gestione automatica di domande di primo livello
- Se il chatbot non riesce a risolvere, reindirizza a supporto email che finisce nella piattaforma di ticketing
- Aiuta a ridurre domande semplici e ripetitive
- Può utilizzare agente AI con prompt definito

### Approccio Incrementale

- Partire con piattaforma di base per raccolta e gestione ticket
- Aggiungere progressivamente automazioni e complessità
- Identificare quali risposte possono essere automatizzate

### Ispirazione da Progetti Esistenti

- Riutilizzare soluzioni sviluppate per Nevik (recupero crediti autostrade)
- Sistema che legge, categorizza, assegna e propone risposte automatiche
- Layout e funzionalità già testati possono essere adattati

## Dettagli Tecnici Database

- **Tipo**: MySQL su AWS RDS
- **Accesso**: Istanza privata con connessione SSH
- **Struttura dati**:
  - Ricerca per email utente
  - Associazione email → ricerche → eventi → contenuti
  - Link all'area personale utente
  - Link ai contenuti su AWS S3
  - Nome file selfie su S3

## Integrazione WhatsApp

### Stato Attuale
- Modulo separato su istanza AWS dedicata, collegato al database
- Flusso parallelo alla web app
- Ancora in fase di test locale, non in produzione

### Funzionamento
- Utente scannerizza QR code per iniziare conversazione
- Bot saluta in italiano e inglese, permette scelta lingua
- Identifica evento tramite domande (zona, data) o tag nel QR code
- Utente carica selfie → trigger ricerca foto su AWS
- Mostra prime 5 anteprime con filigrana
- Link univoco per vedere tutte le foto nella web app

### Pagamento
- Tutto gestito tramite web app (non direttamente da WhatsApp)
- Stesso link univoco usato anche dal supporto per verificare problemi

## Dashboard per Partner/Eventi

### Situazione Attuale
- Utilizzo di Grafana sia per dashboard interna che per clienti esterni
- Dashboard interna: tutti gli eventi + metriche tecniche aggiuntive
- Dashboard clienti: filtrate per mostrare solo eventi specifici dell'organizzatore

### Necessità di Miglioramento
- Grafana è principalmente uno strumento interno, poco adatto per condivisione esterna
- Serve soluzione più user-friendly per partner
- Sistema di permessi più sofisticato
- Dashboard personalizzata è elemento distintivo rispetto ai competitor

## Priorità di Sviluppo

1. **Prima priorità**: Piattaforma interna di ticketing
2. **Seconda priorità**: Chatbot in web app (riduce effort successivo)
3. **Terza priorità**: Dashboard migliorata per eventi/partner

## Prossimi Passi

- [ ] Team tecnico (Marco/Federico) fa check interno per raccogliere soluzioni da progetti simili (es. Nevik)
- [ ] Preparare mockup/presentazione della piattaforma di ticketing proposta
- [ ] Jonathan invia link demo e materiali per test (area demo, selfie di prova)
- [ ] Schedulare meeting di follow-up con mockup interattivi per raccogliere feedback

## Note Tecniche Aggiuntive

- Preferenza per FastAPI per nuovi servizi, ma disponibilità a lavorare su Node.js esistente se necessario
- Jonathan ha condiviso documento con screenshot della gestione attuale
- Area demo disponibile per testare il flusso completo (con carta test Stripe 4242...)
