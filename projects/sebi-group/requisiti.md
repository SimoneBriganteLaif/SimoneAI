---
progetto: "sebi-group"
versione: "1.0"
data: "2026-03-17"
fonte: "Kickoff 2026-02-17 | On-site 2026-03-16 (2 sessioni)"
validato-da: ""
tags:
  - "#progetto:sebi-group"
  - "#fase:presales"
---

# Requisiti — Sebi Group

---

## Requisiti funzionali

### RF-01: Connessione e sincronizzazione email

**Priorità**: Alta
**Fonte**: Kickoff (Feb 17), On-site sessione 1 e 2

**Descrizione**:
Il sistema deve connettersi alle caselle email condivise Outlook 365 (10-15 caselle) tramite Microsoft Graph API, sincronizzare le email in ingresso in tempo reale e renderle disponibili in una vista unificata. L'operatore non dovrà più aprire Outlook.

**Criteri di accettazione**:
- [ ] Connessione a tutte le caselle email M365 identificate (Export Sales, Intertrapporto, China, Project, Export, Import, e altre)
- [ ] Sincronizzazione in tempo reale (latenza <1 minuto)
- [ ] Gestione allegati (PDF, Excel, immagini) con anteprima
- [ ] Storico email preservato e ricercabile

**Note / vincoli**:
- Volume: 400-700 email/giorno
- Piano M365 da verificare per confermare disponibilità Graph API

---

### RF-02: Classificazione automatica email (AI)

**Priorità**: Alta
**Fonte**: Kickoff (Feb 17), On-site sessione 1 e 2

**Descrizione**:
Il sistema deve classificare automaticamente le email in arrivo utilizzando AI generativa, estraendo: tipo richiesta (quotazione, conferma, operativo, informativo), area (import/export), cliente, destinazione/origine, lingua, urgenza stimata. Attualmente metà delle email vengono smistate manualmente (~1h/giorno).

**Criteri di accettazione**:
- [ ] Classificazione automatica su dimensioni: tipo, area, cliente, geografia, lingua, urgenza
- [ ] Accuratezza ≥85% sulla classificazione primaria (tipo + area)
- [ ] Gestione mail inviate a casella sbagliata con suggerimento riassegnazione
- [ ] Riconoscimento pattern specifici del settore (es. "piedi" = mare)
- [ ] Regole e categorie configurabili dall'utente senza codice

**Note / vincoli**:
- Basata su AI generativa con guard rail, non ML tradizionale
- Complementare alle regole Outlook esistenti (dominio + parole chiave)
- Necessari pochi esempi ben fatti per il fine-tuning iniziale

---

### RF-03: Assegnazione automatica a operatore

**Priorità**: Alta
**Fonte**: Kickoff (Feb 17), On-site sessione 1 e 2

**Descrizione**:
Il sistema deve assegnare automaticamente le email classificate all'operatore più adatto, basandosi su: linee/destinazioni assegnate, carico di lavoro corrente, storico competenze, disponibilità (assenze, part-time). Deve supportare redistribuzione automatica in caso di assenze.

**Criteri di accettazione**:
- [ ] Assegnazione automatica basata su regole configurabili
- [ ] Bilanciamento carico di lavoro tra operatori
- [ ] Gestione assenze con redistribuzione automatica
- [ ] Possibilità di riassegnazione manuale
- [ ] Preservazione della sigla operatore (3 lettere) come identificativo

**Note / vincoli**:
- Attualmente la sigla nell'oggetto email è l'unico identificativo di presa in carico

---

### RF-04: Estrazione automatica dati da email e allegati

**Priorità**: Alta
**Fonte**: On-site sessione 2

**Descrizione**:
Il sistema deve estrarre automaticamente i dati strutturati dalle email e dagli allegati (PDF, Excel): origine, destinazione, peso, dimensioni, colli, resa merce, tipo merce, e pre-popolare le maschere di quotazione. L'operatore verifica e conferma.

**Criteri di accettazione**:
- [ ] Estrazione da corpo email in formato testo
- [ ] Estrazione da allegati PDF e Excel
- [ ] Pre-popolamento maschera quotazione con dati estratti
- [ ] Evidenziazione dati mancanti rispetto al set minimo richiesto
- [ ] Confidence score visibile per ogni campo estratto

**Note / vincoli**:
- Set dati minimi: origine, destinazione, peso, dimensioni, colli, resa merce, tipo merce
- I formati variano enormemente tra fornitori e clienti
- Decodifica sigle e terminologia tecnica del settore

---

### RF-05: Richiesta automatica dati mancanti

**Priorità**: Media
**Fonte**: On-site sessione 2

**Descrizione**:
Il sistema deve rilevare quando una richiesta è incompleta (dati mancanti rispetto al set minimo) e generare automaticamente una bozza di email al cliente per richiedere le informazioni mancanti. Per mail notturne, la richiesta può essere inviata automaticamente.

**Criteri di accettazione**:
- [ ] Rilevamento automatico dati mancanti vs. set minimo
- [ ] Generazione bozza email di richiesta dati con template configurabili
- [ ] Invio automatico per mail notturne (fuori orario) se configurato
- [ ] Man-in-the-loop per invii in orario lavorativo

**Note / vincoli**:
- Template multilingua (clienti internazionali)

---

### RF-06: Gestione ciclo offerta export

**Priorità**: Alta
**Fonte**: Kickoff (Feb 17), On-site sessione 1 e 2

**Descrizione**:
Il sistema deve gestire il ciclo completo dell'offerta export: dalla richiesta del cliente alla generazione della quotazione. Include: creazione RDO, invio a 2-3 fornitori selezionati, raccolta risposte, comparazione, applicazione margine, generazione PDF quotazione. Ogni richiesta deve avere un **ID univoco** che la segue in tutta la corrispondenza.

**Criteri di accettazione**:
- [ ] ID univoco per pratica che persiste in tutta la corrispondenza
- [ ] Creazione RDO con selezione fornitori assistita (suggerimento basato su storico)
- [ ] Tracking risposte fornitori con timer e scadenze
- [ ] Tabella comparativa offerte ricevute
- [ ] Calcolo prezzo rivendita con margine configurabile (esposto o nascosto)
- [ ] Generazione PDF quotazione per il cliente
- [ ] Gestione revisioni multiple (90% dei casi)
- [ ] Timeline visiva di tutta la corrispondenza legata alla pratica

**Note / vincoli**:
- Margine tipico: 5c/kg con minimo 20-30€ (varia per cliente/destinazione)
- 2025: ~20.000 quotazioni, tasso conversione 18%
- Da una richiesta possono partire 7+ email a fornitori diversi
- Una spedizione "semplice" genera 9+ scambi email
- 80% spedizioni standard, 20% speciali (merci pericolose, animali vivi, oversize)

---

### RF-07: Gestione ciclo offerta import

**Priorità**: Alta
**Fonte**: On-site sessione 1 e 2

**Descrizione**:
Il sistema deve gestire il ciclo offerta import, integrandosi con il sistema di autocotazione esistente e il gestionale Osma. Include: apertura quotazione con dati estratti, invio massivo a fornitori (es. 9 agenti per Shanghai), ricezione e decodifica risposte in formati eterogenei, inserimento automatico nel gestionale, selezione migliore offerta con markup.

**Criteri di accettazione**:
- [ ] Integrazione con sistema autocotazione esistente
- [ ] Invio massivo RDO a fornitori selezionati con template
- [ ] ID quotazione (formato gestionale, es. 2026-6-01) nell'oggetto email
- [ ] Parsing automatico risposte fornitori (formati eterogenei)
- [ ] Inserimento automatico costi nel gestionale Osma
- [ ] Confronto offerte con ordinamento per criteri configurabili
- [ ] Generazione offerta cliente con markup applicato

**Note / vincoli**:
- Il gestionale Osma ha già funzionalità di invio massivo (da integrare, non duplicare)
- Ogni fornitore risponde con formato diverso; lo stesso fornitore può variare

---

### RF-08: Solleciti automatici

**Priorità**: Media
**Fonte**: Kickoff (Feb 17), On-site sessione 2

**Descrizione**:
Il sistema deve inviare solleciti automatici: (a) ai fornitori che non rispondono entro il tempo configurato, (b) ai clienti per quotazioni in attesa di conferma. I solleciti sono bozze con approvazione umana, salvo configurazione diversa.

**Criteri di accettazione**:
- [ ] Solleciti fornitori dopo N ore/giorni configurabili
- [ ] Solleciti clienti per quotazioni non confermate
- [ ] Template solleciti personalizzabili per lingua e contesto
- [ ] Dashboard solleciti attivi con possibilità di annullamento
- [ ] Man-in-the-loop di default, auto-send configurabile

**Note / vincoli**:
- Tempistiche risposta tipiche fornitori: 1-2 giorni (aereo)

---

### RF-09: Integrazione gestionale Osma (import)

**Priorità**: Alta
**Fonte**: On-site sessione 2

**Descrizione**:
Il sistema deve integrarsi bidirezionalmente con il gestionale Osma (import) via API: lettura anagrafiche clienti/agenti/fornitori, lettura/scrittura quotazioni, verifica fido/credito, apertura pratiche, sync dati.

**Criteri di accettazione**:
- [ ] Lettura anagrafiche clienti, agenti (con filiali e codici multipli), fornitori
- [ ] Creazione quotazioni e inserimento costi fornitori
- [ ] Verifica fido/credito in tempo reale
- [ ] Codice extra-contabile per nuovi clienti/case spedizione
- [ ] Collegamento quotazione confermata → pratica operativa
- [ ] Lettura tariffari pre-caricati per trasportatori abituali

**Note / vincoli**:
- Software Osma con API disponibili
- Ambiente di test appena arrivato
- Stanno già implementando collegamento quotazione→pratica
- Agenti hanno anagrafica separata con possibili più filiali/codici

---

### RF-10: Integrazione WebCargo (export aereo)

**Priorità**: Media
**Fonte**: On-site sessione 2

**Descrizione**:
Il sistema deve integrarsi con WebCargo per le quotazioni export aeree: interrogare tariffe in tempo reale delle compagnie aeree, importare rate, e possibilmente automatizzare l'inserimento dati dalla piattaforma.

**Criteri di accettazione**:
- [ ] Interrogazione tariffe WebCargo da dentro la piattaforma
- [ ] Import automatico rate aeree nella quotazione
- [ ] Gestione scadenza tariffe (quotazioni "da riconfermare")

**Note / vincoli**:
- WebCargo ha API disponibili — da verificare scope e costi
- Tariffe real-time: cambiano frequentemente
- Già richieste specifiche per copia-incolla automatico mail

---

### RF-11: Verifica appartenenza network agenti

**Priorità**: Media
**Fonte**: On-site sessione 1

**Descrizione**:
Il sistema deve verificare automaticamente se un agente estero è membro di uno dei 5-6 network di cui Sebi fa parte, tramite API dei network o scraping dei siti.

**Criteri di accettazione**:
- [ ] Verifica automatica appartenenza network (per i network che offrono API)
- [ ] Alert per agenti non verificati
- [ ] Cache risultati con aggiornamento periodico

**Note / vincoli**:
- Attualmente verifica manuale sui singoli siti web dei network
- Disponibilità API network da verificare caso per caso

---

### RF-12: Alert intelligenti e proattivi

**Priorità**: Media
**Fonte**: Kickoff (Feb 17), On-site sessione 1 e 2

**Descrizione**:
Il sistema deve mostrare alert proattivi contestuali durante il lavoro dell'operatore: clienti con fido esaurito/scaduto, clienti bloccati, nuovi agenti non verificati, destinazioni non competitive, fornitori non rispondenti, quotazioni in scadenza.

**Criteri di accettazione**:
- [ ] Alert fido/credito in fase quotazione (non solo all'apertura pratica)
- [ ] Alert clienti bloccati, scaduti, morosi
- [ ] Alert agenti non in network
- [ ] Alert fornitori non rispondenti oltre soglia
- [ ] Alert quotazioni prossime a scadenza
- [ ] Distinzione livelli visibilità: info per tutti vs. info solo per commerciali senior
- [ ] Canali: in-app (sempre), email digest giornaliero (configurabile)

**Note / vincoli**:
- Info fido/credito attualmente visibile solo aprendo pratica → troppo tardi
- Recupero dati da gestionale basato su ragione sociale o dominio email

---

### RF-13: Prioritizzazione intelligente

**Priorità**: Media
**Fonte**: On-site sessione 1 e 2

**Descrizione**:
Il sistema deve calcolare una priorità per ogni richiesta basata su: completezza dati, fatturato storico cliente, tasso conferma cliente, margine atteso, urgenza (fuso orario/deadline), e presentare le richieste ordinate per priorità.

**Criteri di accettazione**:
- [ ] Score di priorità calcolato automaticamente
- [ ] Peso dei fattori configurabile
- [ ] Vista coda ordinata per priorità per ogni operatore
- [ ] Evidenziazione richieste sotto soglia (destinazioni non competitive, clienti a bassa conversione)
- [ ] Quotazioni con tutti i dati = priorità 1; dati mancanti + cliente non collaborativo = priorità inferiore

**Note / vincoli**:
- Attualmente nessun metodo strutturato — basato su intuizione
- Clienti che chiedono molto e confermano poco devono essere identificabili

---

### RF-14: Dashboard operativa

**Priorità**: Alta
**Fonte**: Kickoff (Feb 17), On-site sessione 2

**Descrizione**:
Il sistema deve fornire una dashboard personalizzata per operatore con: attività da fare ordinate per priorità, stato pratiche in corso, solleciti attivi, email non lavorati, statistiche giornaliere.

**Criteri di accettazione**:
- [ ] Vista personalizzata per operatore
- [ ] Coda attività ordinate per priorità
- [ ] Stato pratiche in corso con timeline
- [ ] Contatore email non lavorati per casella
- [ ] Indicatori tempo medio risposta

**Note / vincoli**:
- Layout semplice, minimo numero di schermate ma con tutte le info
- Target utenti: 35-38 anni

---

### RF-15: Dashboard management e KPI

**Priorità**: Media (Fase 2)
**Fonte**: Kickoff (Feb 17), On-site sessione 2

**Descrizione**:
Il sistema deve fornire dashboard per il management con KPI: tasso conversione quotazioni→conferme, tempi medi risposta, margini per cliente/destinazione, performance per operatore, trend temporali.

**Criteri di accettazione**:
- [ ] Tasso conversione quotazioni (attualmente 18% export)
- [ ] Tempi risposta (arrivo mail → invio quotazione)
- [ ] Margini per cliente, destinazione, operatore
- [ ] Identificazione clienti ad alto volume/bassa conversione
- [ ] Numero scambi email per pratica
- [ ] Trend temporali e comparazione periodi
- [ ] Export dati

**Note / vincoli**:
- KPI specifici da definire, ma infrastruttura dati deve essere pronta da Fase 1
- 30% fatturato potenziale perso → metrica chiave da tracciare

---

### RF-16: Generazione bozze email assistita

**Priorità**: Media
**Fonte**: On-site sessione 2

**Descrizione**:
Il sistema deve generare bozze di email per l'operatore: risposte ai clienti, richieste ai fornitori, solleciti. L'operatore rivede, modifica se necessario, e invia. Template configurabili per lingua e contesto.

**Criteri di accettazione**:
- [ ] Generazione bozze contestuali (basate su pratica in corso)
- [ ] Template multilingua configurabili
- [ ] Editor email con anteprima
- [ ] Invio da piattaforma (non serve tornare su Outlook)
- [ ] Man-in-the-loop obbligatorio (nessun invio senza approvazione umana in orario lavorativo)

**Note / vincoli**:
- Il cliente è chiaro: NO risposte completamente automatiche in orario lavorativo
- Template devono riflettere il tono professionale del settore

---

### RF-17: Gestione prepratiche (export)

**Priorità**: Bassa
**Fonte**: On-site sessione 2

**Descrizione**:
Il sistema deve supportare la creazione e gestione delle prepratiche export: raccolta documenti, bollettino ritiro, entrata magazzino, note. Supporto per situazioni multi-mittente/multi-ritiro per una destinazione.

**Criteri di accettazione**:
- [ ] Creazione prepratica da quotazione confermata
- [ ] Raccolta documenti con checklist
- [ ] Gestione multi-mittente e multi-ritiro
- [ ] Collegamento a pratica definitiva nel gestionale

**Note / vincoli**:
- Creata indifferentemente da commerciale o operativo (chi ha tempo)

---

## Requisiti non funzionali

### RNF-01: Performance

**Descrizione**: Il sistema deve gestire il volume di 400-700 email/giorno con classificazione in tempo reale e risposta sub-secondo per l'interfaccia utente.
**Criteri misurabili**:
- Classificazione email: <30 secondi dall'arrivo
- Caricamento pagine UI: <2 secondi
- Estrazione dati da allegati: <60 secondi

### RNF-02: Sicurezza

**Descrizione**: Il sistema deve proteggere i dati commerciali sensibili (prezzi, margini, fido clienti) con controllo accessi differenziato e comunicazioni cifrate.
**Criteri misurabili**:
- Autenticazione SSO con Active Directory/M365
- Ruoli differenziati: operatore, commerciale senior, management
- Info fido/margini visibili solo ai ruoli autorizzati
- HTTPS/TLS per tutte le comunicazioni
- GDPR compliance per dati personali

### RNF-03: Usabilità

**Descrizione**: L'interfaccia deve essere semplice e familiare per utenti non tecnici (35-38 anni), riducendo il numero di click e schermate necessarie.
**Criteri misurabili**:
- Onboarding: operatore produttivo entro 1 giorno
- Max 3 click per completare un'azione primaria
- Zero necessità di aprire Outlook durante il lavoro quotidiano

### RNF-04: Configurabilità

**Descrizione**: Regole di classificazione, template email, categorie, soglie alert e criteri di priorità devono essere configurabili dall'utente senza intervento tecnico.
**Criteri misurabili**:
- Pannello admin per configurazione regole
- Nessun parametro hardcoded per logiche di business

### RNF-05: Disponibilità

**Descrizione**: Il sistema deve essere disponibile durante l'orario lavorativo (8:00-19:00 CET, lun-ven) e gestire richieste notturne in coda.
**Criteri misurabili**:
- Uptime 99.5% in orario lavorativo
- Email notturne processate e in coda entro le 8:00

---

## Integrazioni richieste

| Sistema esterno | Tipo integrazione | Dati scambiati | Note |
|----------------|------------------|----------------|------|
| Microsoft 365 (Outlook) | Microsoft Graph API | Email (lettura + invio), allegati, contatti | 10-15 caselle condivise |
| Gestionale Osma (import) | API bidirezionale | Anagrafiche, quotazioni, fido/credito, tariffari, pratiche | Ambiente test disponibile |
| WebCargo | API (da verificare) | Tariffe aeree real-time, prenotazioni | Verifica scope API in corso |
| Network agenti (5-6 siti) | API o scraping | Verifica appartenenza agente | Disponibilità API da verificare |
| Gestionale export | Da definire | Prepratiche, pratiche definitive, tariffari trasportatori | Meeting con fornitore da pianificare |

---

## Esclusioni esplicite

- **Gestione operativa post-conferma**: sdoganamento, consegna, tracking spedizione — restano sul gestionale attuale
- **Contabilità e fatturazione**: non incluse, restano sul gestionale
- **Sostituzione gestionale**: il sistema si affianca al gestionale, non lo sostituisce
- **Invio automatico email senza approvazione umana** (in orario lavorativo): escluso per scelta del cliente
- **Gestione documenti doganali**: resta al reparto dogana
- **App mobile nativa**: solo web app responsive

---

## Domande aperte

| # | Domanda | Responsabile | Scadenza | Stato |
|---|---------|-------------|---------|-------|
| 1 | Dettaglio API gestionale Osma: endpoint disponibili, autenticazione, limiti | Fornitore Osma | Meeting da pianificare | Aperta |
| 2 | Piano M365: conferma disponibilità Graph API con piano attuale | IT Sebi | 2026-03-23 | Aperta |
| 3 | WebCargo: scope API, costi licenza API, limiti rate | WebCargo | 2026-03-23 | Aperta |
| 4 | Nome e contatto fornitore gestionale export (se diverso da Osma) | Michele Bonicalzi | 2026-03-23 | Aperta |
| 5 | Regole markup definite: formula per calcolo margine automatico per import | Stefano/Gabriella | 2026-03-23 | Aperta |
| 6 | Network agenti: elenco completo 5-6 network con siti/contatti | Michele Bonicalzi | 2026-03-30 | Aperta |
| 7 | Esempi email thread completi con screenshot gestionale (export + import) | Stefano/Gabriella | 2026-03-23 | Aperta |
| 8 | Gestionale export: è lo stesso Osma o diverso? API disponibili? | Michele Bonicalzi | Meeting fornitore | Aperta |

---

## Changelog

| Data | Versione | Modifica | Autore |
|------|---------|---------|--------|
| 2026-03-17 | 1.0 | Prima stesura completa — da kickoff (Feb 17) e on-site (Mar 16) | Simone |
