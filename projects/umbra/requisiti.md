---
progetto: "umbra"
versione: "1.0"
data: "2026-03-10"
fonte: "Meeting 2025-12-01, 2026-01-22, 2026-02-09, 2026-03-03 + Contratto 2025-11-19"
validato-da: "Simone"
tags:
  - "#progetto:umbra"
  - "#fase:dev"
---

# Requisiti — Umbra

> **Versione 1.0** — Validato con l'utente il 2026-03-10.
> Fonti: 4 meeting + contratto firmato (Allegato 1).

---

## Requisiti funzionali

### Modulo A — Improvement piattaforma recommender

---

### RF-01: Aggiornamento settimanale dei dati

**Priorita**: Alta
**Fonte**: Contratto (Allegato 1), Meeting 2025-12-01, Meeting 2026-01-22

**Descrizione**:
Il sistema deve passare dall'attuale aggiornamento mensile a un aggiornamento settimanale dei dati di vendita e previsioni. La logica dell'algoritmo resta invariata, cambia solo la frequenza di esecuzione. La previsione rimane mensile nonostante l'elaborazione settimanale.

**Criteri di accettazione**:
- [ ] L'ETL esegue staging e presentation settimanalmente
- [ ] I file settimanali sono piu contenuti rispetto ai mensili
- [ ] A fine mese vengono elaborate tutte le variazioni dell'intero portafoglio
- [ ] Le previsioni nel frontend si aggiornano entro 24h dal deposito file

**Note / vincoli**:
- File settimanali in formato CSV (non piu Excel)
- Il sistema deve ricavare la settimana dal file (vale sempre l'ultimo file)

---

### RF-02: Integrazione SFTP automatica

**Priorita**: Alta
**Fonte**: Meeting 2026-01-22, Meeting 2026-02-09

**Descrizione**:
Il sistema deve leggere automaticamente i file di dati dalla cartella SFTP condivisa con Umbra, sostituendo il processo manuale via FileZilla. Struttura cartelle IN/OUT, accesso programmatico filtrato per IP.

**Criteri di accettazione**:
- [ ] Connessione SFTP programmatica funzionante (AWS Transfer)
- [ ] Lettura automatica dalla cartella `elaborazioni_settimanali`
- [ ] Parsing corretto dei file CSV settimanali (ordini e sconti)
- [ ] Gestione errori e notifica in caso di file mancanti o malformati

**Note / vincoli**:
- IP autorizzati: 18.267.69 e 54.246.152.243
- Certificato SFTP da rinnovare (blocco attuale — responsabile: Paolo)
- Ponte S400-DMZ da configurare lato Umbra
- Il contratto menziona opzione tunnel ipsec (da validare)

---

### RF-03: Formato output CSV

**Priorita**: Completato
**Fonte**: Meeting 2026-01-22

**Descrizione**:
I file di output dell'algoritmo devono essere prodotti in formato CSV invece di Excel, per permettere l'automazione completa del processo di lettura e import.

**Criteri di accettazione**:
- [x] Output ETL in formato CSV
- [x] Encoding e separatore corretti per lettura automatica

---

### RF-04: Gestione varianti prodotto

**Priorita**: Bassa (Nice to Have)
**Fonte**: Contratto (Allegato 1), Meeting 2025-12-01

**Descrizione**:
Il sistema dovrebbe gestire prodotti con varianti e articoli sostitutivi, aggregando le previsioni a livello di modello invece che di singola variante, per mantenere continuita storica.

**Criteri di accettazione**:
- [ ] Previsioni aggregate per modello (non per singola variante/taglia)
- [ ] Tabella associazione modello-prodotti integrata (fornita da Adriano)
- [ ] Coerenza con la segmentazione B2B del cliente

**Note / vincoli**:
- Gerarchia prodotti: classe > sottoclasse > capitolo > modello > prodotto (variante)
- Non ancora discusso approfonditamente col cliente
- Complesso da implementare, da valutare in futuro
- Valutare se usare tabella Adriano vs algoritmo semantico attuale

---

### Modulo B — Pianificatore promozioni WOW

> **Nota architetturale**: il modulo WOW non contiene un algoritmo predittivo proprio.
> Riutilizza l'output del recommender gia in produzione (Pagina operativa Marketing)
> e vi applica **regole deterministiche** di selezione e prioritizzazione con vincoli
> specifici WOW (budget, temporali, stagionalita).

---

### RF-05: Modulo marketing — pianificatore promozioni WOW

**Priorita**: Alta
**Fonte**: Contratto (Allegato 1), Meeting 2026-02-09, Meeting 2026-03-03

**Descrizione**:
Il sistema deve fornire un modulo dedicato marketing dove vengono proposte, per ciascun periodo, le promozioni WOW piu efficaci. Il modulo riutilizza le previsioni dell'algoritmo recommender gia in produzione (Pagina operativa Marketing) e vi applica regole di selezione. L'utente principale e Alessandra (responsabile marketing). Il sistema fornisce supporto decisionale, non sostituisce il giudizio umano.

**Criteri di accettazione**:
- [ ] Sezione dedicata nel frontend accessibile dal marketing
- [ ] Lettura automatizzata in background dei dati WOW storiche e future
- [ ] Lista suggerimenti ordinata per priorita (basata su regole, non AI)
- [ ] Possibilita di scelta sottoinsieme prodotti in una shortlist (max 10 prodotti)

**Note / vincoli**:
- 2 WOW a settimana: 1 Studio + 1 Laboratorio
- Ogni WOW dura 15 giorni (si sovrappongono)
- Pianificazione con almeno 15 giorni di anticipo
- Il modulo non ha un algoritmo predittivo proprio

---

### RF-06: Vista Gantt pianificazione + slot campagne

**Priorita**: Alta
**Fonte**: Meeting 2026-03-03, chiarimento utente 2026-03-10

**Descrizione**:
Il sistema deve visualizzare una vista Gantt con slot temporali per le promozioni future. Ogni slot rappresenta una campagna WOW con configurazione flessibile. Gli slot sono la feature base delle campagne WOW: di default durano 2 settimane e contengono 1 prodotto Studio + 1 Laboratorio, ma l'utente puo modificare date, durata e prodotti.

**Criteri di accettazione**:
- [ ] Vista Gantt con almeno 4 settimane visibili
- [ ] Slot di default: 2 settimane, 1 prodotto Studio + 1 Laboratorio
- [ ] Date di inizio/fine dello slot modificabili
- [ ] Durata dello slot variabile (da 2 fino a 8 settimane per campagne speciali)
- [ ] Possibilita di aggiungere piu prodotti per slot
- [ ] Possibilita di aggiungere manualmente prodotti non suggeriti dal sistema
- [ ] Override dei suggerimenti per accordi specifici con fornitori
- [ ] Supporto campagne speciali come slot con durate diverse:
  - WOW Si Parte (gennaio, 3+ settimane)
  - Sorprese di Pasqua (2-3 settimane, 8-9 promozioni)
  - Umbra Summer (luglio-agosto)
  - Aspettando il Natale (1-24 dicembre)
- [ ] Slot multipli in periodi speciali

**Note / vincoli**:
- Le campagne speciali non sono un modulo a parte: sono slot piu lunghi nella stessa Gantt
- Agosto: niente WOW settimanali standard (gestito come campagna speciale "Summer")

---

### RF-07: Suggerimenti basati su regole

**Priorita**: Alta
**Fonte**: Contratto (Allegato 1 punti 1-9), Meeting 2026-02-09, Meeting 2026-03-03, chiarimento utente 2026-03-10

**Descrizione**:
Il sistema deve generare suggerimenti di prodotti da mettere in promozione WOW, basandosi sull'output del recommender esistente (Pagina operativa Marketing) e applicando regole deterministiche di prioritizzazione. Non utilizza un algoritmo AI dedicato — il ranking e calcolato tramite regole configurabili.

**Criteri di accettazione**:
- [ ] ~5 suggerimenti per Studio e ~5 per Laboratorio per settimana target
- [ ] Ranking basato su regole deterministiche, NON su algoritmo AI dedicato
- [ ] Criteri di prioritizzazione (dal recommender + regole WOW):
  - Gap budget fornitore (quanto manca al target)
  - Importo previsto valorizzato al sell-in (listino CELIN)
  - Priorita di acquisto (indicatore OOS dal recommender)
  - Giorni all'out of stock (dal recommender)
  - Storicita WOW (quando e stata fatta l'ultima WOW su quella classe/sottoclasse)
  - Vincoli temporali per fornitore (min/max WOW/anno)
  - Lead time specifici dei fornitori (contratto punto 5)
  - Sovrapposizioni con campagne canvas in corso (contratto punto 7)
- [ ] Motivazione esplicita per ogni suggerimento (perche questo prodotto e prioritario)
- [ ] Aggiornamento quindicinale delle proposte
- [ ] Perimetro di pianificazione: 3 settimane avanti con 2 settimane di anticipo

**Note / vincoli**:
- L'output proviene dalla Pagina operativa Marketing (verificare campi disponibili)
- Le WOW sono fatte su classi o sottoclassi, non su singoli articoli

---

### RF-08: Vincoli temporali per fornitore

**Priorita**: Alta
**Fonte**: Meeting 2026-02-09, Meeting 2026-03-03, Contratto punto 5

**Descrizione**:
Il sistema deve rispettare vincoli temporali specifici per ogni fornitore nel proporre le promozioni WOW, inclusi i lead time di fornitura.

**Criteri di accettazione**:
- [ ] Fornitori con target (~8-9): min 2 / max 5 WOW/anno
- [ ] Altri fornitori: max 2 WOW/anno
- [ ] Non riproporre stessa classe/sottoclasse se fatta di recente (finestra minima configurabile)
- [ ] Esclusione WOW settimanali standard in agosto
- [ ] Lead time specifici dei fornitori considerati nella pianificazione

---

### RF-09: Conversione sell-out → sell-in per confronto budget

**Priorita**: Alta
**Fonte**: Meeting 2026-02-09, Meeting 2026-03-03

**Descrizione**:
Il sistema deve convertire le previsioni di vendita (sell-out) al costo di acquisto (sell-in) usando il listino CELIN, per confrontare con il budget fornitore e calcolare lo scostamento.

**Criteri di accettazione**:
- [ ] Previsioni valorizzate al sell-in tramite listino CELIN
- [ ] Avanzamento budget per fornitore/classe/sottoclasse visualizzato (budget totale vs venduto)
- [ ] Calcolo scostamento budget con prioritizzazione fornitori che scostano di piu

---

### RF-10: Tracciamento performance promozioni

**Priorita**: Bassa
**Fonte**: Meeting 2026-03-03

**Descrizione**:
Il sistema deve permettere l'analisi a posteriori delle promozioni WOW, confrontando previsioni con vendite effettive.

**Criteri di accettazione**:
- [ ] Confronto previsione vs vendite effettive per ogni WOW
- [ ] Calcolo avanzamento budget dopo ogni promozione
- [ ] Storico WOW con dati previsti vs effettivi
- [ ] Valorizzazione sia sell-out che CELIN

**Note / vincoli**:
- Meno prioritario per l'utente. Da sviluppare dopo il core del modulo WOW.

---

## Requisiti non funzionali

### RNF-01: Performance

**Descrizione**: L'aggiornamento settimanale (staging + presentation) deve completarsi in tempi ragionevoli.
**Criteri misurabili**: ETL settimanale completato entro 30 minuti.

### RNF-02: Sicurezza

**Descrizione**: Lo scambio dati via SFTP deve essere sicuro e limitato per IP.
**Criteri misurabili**: Accesso SFTP solo da IP whitelist, nessuna VPN richiesta.

### RNF-03: Usabilita

**Descrizione**: L'interfaccia del modulo marketing deve essere fruibile dalla responsabile marketing (Alessandra) senza formazione tecnica specifica.
**Criteri misurabili**: L'utente marketing riesce a pianificare una WOW completa senza assistenza tecnica.

---

## Integrazioni richieste

| Sistema esterno | Tipo integrazione | Dati scambiati | Note |
|----------------|------------------|----------------|------|
| SFTP Umbra (AS400) | File CSV settimanali | Ordini, sconti, anagrafica | Cartella `elaborazioni_settimanali` |
| Listino CELIN | Import una tantum + aggiornamenti | Costi acquisto prodotti | Da integrare in anagrafica |
| Budget fornitori | Import periodico | Budget per fornitore/classe/sottoclasse | Adriano sviluppa app gestionale per normalizzazione |
| Storicita WOW | Import una tantum + aggiornamenti | Date, fornitore, linea, classe, sottoclasse | Da Alessandra + Adriano |
| Avanzamento fatturato | Settimanale | Fatturato per fornitore/classe/sottoclasse (sell-in) | Da integrare nell'ETL |
| Pagina operativa Marketing | Interno (stesso DB) | Output recommender: probabilita acquisto, OOS, importi previsti | Gia in produzione |

---

## Esclusioni esplicite

- Il sistema NON scrive dati sui sistemi del cliente (gestionale/AS400)
- L'inserimento effettivo della WOW nel gestionale resta manuale (lato Umbra)
- Il modulo non sostituisce il giudizio della responsabile marketing
- NON e previsto un algoritmo AI/ML dedicato per il modulo WOW (si usano regole deterministiche)
- Helia (use cases AI) e gestito in un progetto/tavolo separato
- RF-04 (gestione varianti) e Nice to Have, non incluso nello scope primario

---

## Domande aperte

| # | Domanda | Responsabile risposta | Scadenza | Stato |
|---|---------|----------------------|---------|-------|
| 1 | Struttura esatta file budget normalizzato | Adriano Bezzi | — | Aperta |
| 2 | Formato tracciato storicita WOW | Adriano / Alessandra | — | Aperta |
| 3 | Conferma vincoli temporali per ogni fornitore (tabella completa) | Alessandra Olivanti | — | Aperta |
| 4 | Certificato SFTP rinnovato? | Paolo (sistemista) | — | Aperta |
| 5 | Ponte S400-DMZ configurato? | Adriano Bezzi | — | Aperta |
| 6 | Quali campi esatti della Pagina operativa Marketing servono al modulo WOW? | LAIF (Simone/Tancredi) | — | Aperta |
| 7 | Mockup UI abbozzato disponibile? Dove? | Simone | — | Aperta |

---

## Changelog

| Data | Versione | Modifica | Autore |
|------|---------|---------|--------|
| 2026-03-10 | 0.1 | Bozza generata da init-project (4 meeting + contratto) | Claude Code |
| 2026-03-10 | 1.0 | Validato con l'utente. RF-07 → regole (no AI). RF-04 → Nice to Have. RF-11 integrato in RF-06. RF-10 → Bassa. Aggiunto RNF-03. Nota architetturale su riuso recommender. | Claude Code |
