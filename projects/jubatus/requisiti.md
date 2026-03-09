---
progetto: "jubatus"
versione: "0.1"
data: "2026-03-08"
fonte: "Meeting 2026-01-23 | Meeting 2026-01-28 | Meeting 2026-02-13"
validato-da: ""
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
  - "#fase:dev"
---

# Requisiti — Jubatus Customer Care

> **Nota**: Bozza generata automaticamente da init-project. Validare con la skill estrazione-requisiti.
> Ogni requisito è segnato come "Da validare".

---

## Requisiti funzionali

### RF-01: Raccolta automatica email

**Priorità**: Da validare
**Fonte**: Meeting 2026-01-28, Meeting 2026-02-13

**Descrizione**:
Il sistema deve raccogliere automaticamente le email inviate all'indirizzo di supporto (info@) e creare un ticket per ogni segnalazione ricevuta.

**Criteri di accettazione**:
- [ ] Email ricevute vengono trasformate in ticket automaticamente
- [ ] Il corpo del messaggio e i metadati (mittente, data, oggetto) sono salvati
- [ ] Thread email successivi vengono associati al ticket originale

**Note / vincoli**:
Attualmente tutte le segnalazioni arrivano a info@ (non un indirizzo dedicato al supporto). Da valutare se creare un indirizzo dedicato.

---

### RF-02: Gestione stati ticket

**Priorità**: Da validare
**Fonte**: Meeting 2026-02-13

**Descrizione**:
Il sistema deve permettere di gestire il ciclo di vita dei ticket con stati definiti.

**Criteri di accettazione**:
- [ ] Stati disponibili: nuovo, work in progress, stand-by, in attesa cliente, fatto
- [ ] Transizioni di stato tracciate con timestamp e autore
- [ ] Visualizzazione chiara dello stato corrente nella lista ticket

---

### RF-03: Assegnazione ticket

**Priorità**: Da validare
**Fonte**: Meeting 2026-02-13

**Descrizione**:
Il sistema deve permettere di assegnare ticket a specifici utenti o team di supporto.

**Criteri di accettazione**:
- [ ] Assegnazione manuale a un utente specifico
- [ ] Possibilità di riassegnare un ticket
- [ ] Visualizzazione dei ticket assegnati per ogni operatore

---

### RF-04: Categorizzazione automatica

**Priorità**: Da validare
**Fonte**: Meeting 2026-01-28, Meeting 2026-02-13

**Descrizione**:
Il sistema deve categorizzare automaticamente i ticket in base al contenuto dell'email.

**Criteri di accettazione**:
- [ ] Categorie predefinite identificate (errore foto, intervento database, intervento S3, video editing, etc.)
- [ ] Tag multipli per ticket
- [ ] Possibilità di modificare manualmente la categorizzazione

---

### RF-05: Integrazione database cliente (read-only)

**Priorità**: Da validare
**Fonte**: Meeting 2026-01-28, Meeting 2026-02-13

**Descrizione**:
Il sistema deve integrarsi con il database MySQL esistente di Jubatus (AWS RDS) per mostrare le informazioni dell'utente segnalante senza dover aprire pagine multiple.

**Criteri di accettazione**:
- [ ] Ricerca utente per email
- [ ] Visualizzazione ordini, eventi partecipati, contenuti acquistati
- [ ] Link diretti a risorse S3 (foto, video, selfie)
- [ ] Link automatico a pagina MyMemories dell'utente

**Note / vincoli**:
Query SQL già esistenti nella dashboard Grafana attuale possono essere riutilizzate. Accesso read-only al database MySQL RDS (connessione via security group se deploy su stesso account AWS).

---

### RF-06: Pagina utente integrata

**Priorità**: Da validare
**Fonte**: Meeting 2026-02-13

**Descrizione**:
Cliccando su un utente nel ticket, il sistema deve mostrare una vista aggregata con tutti i dati rilevanti.

**Criteri di accettazione**:
- [ ] Eventi partecipati
- [ ] Ordini effettuati
- [ ] Contenuti acquistati
- [ ] Visualizzazione diretta selfie da S3
- [ ] Link automatici a MyMemories

---

### RF-07: Template risposte automatiche

**Priorità**: Da validare
**Fonte**: Meeting 2026-01-28, Meeting 2026-02-13

**Descrizione**:
Il sistema deve proporre risposte automatiche per i problemi più comuni, basate sulla categoria del ticket.

**Criteri di accettazione**:
- [ ] Template risposte predefiniti per categoria
- [ ] Possibilità di personalizzare prima dell'invio
- [ ] Invio risposta direttamente dalla piattaforma

---

### RF-08: Risposta email dal ticket

**Priorità**: Da validare
**Fonte**: Meeting 2026-02-13

**Descrizione**:
Il sistema deve permettere di rispondere alle email direttamente dall'interfaccia del ticket.

**Criteri di accettazione**:
- [ ] Visualizzazione corpo messaggio nel ticket
- [ ] Composizione e invio risposta dalla piattaforma
- [ ] Storico conversazione visibile

---

### RF-09: Prioritizzazione ticket

**Priorità**: Da validare
**Fonte**: Meeting 2026-02-13

**Descrizione**:
Il sistema deve assegnare priorità ai ticket basandosi su categoria, data arrivo e potenzialmente sentiment analysis.

**Criteri di accettazione**:
- [ ] Priorità basata su categoria e data arrivo
- [ ] Sentiment analysis per urgenza (opzionale)
- [ ] Ordinamento ticket per priorità

---

### RF-10: Filtri e ricerca

**Priorità**: Da validare
**Fonte**: Meeting 2026-02-13

**Descrizione**:
Il sistema deve permettere di filtrare e cercare ticket.

**Criteri di accettazione**:
- [ ] Filtro per evento
- [ ] Filtro per categoria
- [ ] Filtro per priorità
- [ ] Filtro per stato
- [ ] Ricerca per email utente

---

### RF-11: Note e allegati

**Priorità**: Da validare
**Fonte**: Meeting 2026-02-13

**Descrizione**:
Il sistema deve permettere di aggiungere note interne ai ticket e link a documenti.

**Criteri di accettazione**:
- [ ] Note interne (non visibili al cliente)
- [ ] Link a Google Drive per documenti
- [ ] Storico note con timestamp e autore

---

## Requisiti non funzionali

### RNF-01: Performance

**Descrizione**: Il sistema deve rispondere in modo rapido per non rallentare il lavoro degli operatori (2-4 persone in contemporanea nei picchi).
**Criteri misurabili**: Tempo di risposta < 2 secondi per le query principali.

### RNF-02: Sicurezza

**Descrizione**: Il sistema deve accedere ai dati del database MySQL solo in read-only. Autenticazione per gli operatori.
**Criteri misurabili**: Nessuna operazione di scrittura sul database MySQL del cliente.

### RNF-03: Hosting

**Descrizione**: Deploy sull'account AWS di Jubatus per semplificare accesso al database e storage.
**Criteri misurabili**: Infrastruttura deployata su account AWS Jubatus con accesso via security group.

---

## Integrazioni richieste

| Sistema esterno | Tipo integrazione | Dati scambiati | Note |
|----------------|------------------|----------------|------|
| MySQL RDS (Jubatus) | Read-only query | Utenti, ordini, eventi, contenuti | Via security group su stesso account AWS |
| AWS S3 (Jubatus) | Read | Foto, video, selfie | Link diretti ai bucket esistenti |
| Email (info@) | Inbound | Segnalazioni clienti | Da definire protocollo (IMAP/webhook) |
| Grafana | Riferimento | Query SQL esistenti | Riutilizzo query, non integrazione diretta |

---

## Esclusioni esplicite

- Gestione web app principale di Jubatus (responsabilità altra software house)
- Chatbot WhatsApp (fase successiva)
- Dashboard partner/eventi (fase successiva)
- DM Instagram e altri canali social (nice to have futuro)
- Modifica dati nel database MySQL (solo lettura)

---

## Domande aperte

| # | Domanda | Responsabile risposta | Scadenza | Stato |
|---|---------|----------------------|---------|-------|
| 1 | Schema database MySQL aggiornato | Jonathan | — | Aperta |
| 2 | Conferma deploy su account AWS Jubatus | Jonathan/Marco/Simone | — | Aperta |
| 3 | Creare indirizzo email dedicato al supporto? | Team | — | Aperta |
| 4 | Protocollo ricezione email (IMAP, webhook, altro)? | Team tecnico | — | Aperta |
| 5 | Data model applicazione (mail, utenti, tag, categorie, risposte) | Team | — | Aperta |

---

## Changelog

| Data | Versione | Modifica | Autore |
|------|---------|---------|--------|
| 2026-03-08 | 0.1 | Bozza generata da init-project (da 3 note meeting Notion) | Claude Code |
