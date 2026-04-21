---
data: "2026-04-10"
tipo: "call pre-kickoff"
partecipanti: ["Antonio Scagliuso", "Andrea Mordenti", "Simone Brigante"]
tags:
  - "#progetto:bonfiglioli-consulting"
  - "#meeting"
---

# Call Pre-Kickoff — Bonfiglioli Consulting — 10 Aprile 2026

## Obiettivo della call

Allineamento pre-kickoff: chiarire punti aperti, raccogliere informazioni mancanti, assegnare compiti preparatori al cliente in vista del kickoff in presenza a Lecco.

---

## Domande da fare

### A. Accesso dati e integrazione (Andrea IT)

- [ ] **Stato Tailscale**: l'accesso VPN è già configurato? Account SQL read-only creato?
- [ ] **Schema DWH**: esiste documentazione delle tabelle/viste disponibili? Possiamo avere un export dello schema (tabelle, colonne, relazioni)?
- [ ] **Frequenza refresh DWH**: conferma che i dati si aggiornano ogni 2 ore?
- [ ] **CRM**: che tecnologia usa il CRM? I dati CRM passano nel DWH o servono accessi separati?
- [ ] **Dati Orchestra nel DWH**: la pianificazione settimanale di Orchestra confluisce nel DWH? Con che frequenza?
- [ ] **System integrator DWH**: hanno già contattato il loro fornitore per predisporre gli accessi?

### B. Logiche di business (Antonio)

- [ ] **Formula TAKT**: come si calcola esattamente? Varia per ruolo, seniority o service line?
- [ ] **Formula OME**: (Giornate fatturate + LFS) / Giornate disponibili — conferma? Cos'è LFS nel dettaglio?
- [ ] **Target saturazione**: qual è il target per risorsa? Uguale per tutti o differenziato?
- [ ] **Distribuzione temporale**: quando una commessa ha 100 giornate, come si distribuiscono nel tempo? Ci sono regole (es. max 3gg/sett per commessa) o è libero?
- [ ] **Risorse esterne**: quante sono? Come funziona il budget per le esterne? Vincoli specifici?
- [ ] **Proiezione 9 mesi**: la logica è proiettare il mix % di effort degli ultimi mesi? O c'è un modello diverso?
- [ ] **Numeri**: quante risorse operative totali? Quanti progetti attivi contemporaneamente? Quante service line e sotto-competenze?
- [ ] **Scala competenze**: la scala 1-5 esiste già o va definita da zero? Chi la compila?

### C. Processi operativi (Antonio / Direzione)

- [ ] **Meeting DICAP** (1° e 3° lunedi): che decisioni vengono prese? Che materiale preparano oggi? Che output serve dalla piattaforma?
- [ ] **S&OP mensile**: partecipanti, tipo di decisioni, dati necessari?
- [ ] **Chi pianifica oggi**: solo i Principal? O anche i responsabili di team?
- [ ] **Conflitti allocazione**: come si risolvono oggi? Chi decide in caso di contesa su una risorsa?
- [ ] **Flusso nuova commessa**: dal CRM alla pianificazione su Orchestra, quanti passaggi e quanto tempo passa?
- [ ] **Report scostamenti**: ce ne possono mandare uno di esempio (Power BI export)?

### D. CRM e pipeline (Marica)

- [ ] **Codifica competenze nel CRM**: e' gia' partita? Se no, quando pensano di iniziare?
- [ ] **Struttura offerta CRM**: che campi ci sono per opportunita'? (importo, probabilita', durata, competenze richieste?)
- [ ] **Volumi pipeline**: quante opportunita' attive tipicamente? Tasso di conversione medio?
- [ ] **Filtro >60%**: confermato come soglia per includere nella simulazione?

### E. Aspetti organizzativi / Kickoff

- [ ] **Data kickoff in presenza**: conferma settimana prossima a Lecco?
- [ ] **Partecipanti kickoff**: chi deve esserci? (Antonio + Andrea IT + Marica + Georgia + Direzione?)
- [ ] **Tranche fatturazione**: hanno preferenze? Proposta LAIF: 40% avvio, 30% M2, 30% go-live?
- [ ] **Prototipo**: hanno visto il prototipo su bonfiglioli-consulting.laifgroup.com? Feedback?
- [ ] **Priorita' moduli**: se dovessero scegliere, quale modulo vorrebbero vedere per primo in demo?

---

## Compiti per casa — Da comunicare al cliente

Attivita' che il cliente deve completare **prima del kickoff in presenza**:

| # | Compito | Owner | Deadline | Note |
|---|---------|-------|----------|------|
| 1 | **Accesso DWH**: configurare Tailscale VPN + account SQL read-only per team LAIF | Andrea IT | Prima del kickoff | Coinvolgere il system integrator se necessario |
| 2 | **Schema DWH**: inviare documentazione tabelle/viste disponibili (o export schema) | Andrea IT | Prima del kickoff | Anche un semplice elenco tabelle con descrizione |
| 3 | **Anagrafica consulenti** (Excel): nome, codice, ruolo, service line, provincia, competenze con livello 1-5, TAKT target, flag interno/esterno | Antonio | Prima del kickoff | Puo' essere il file Excel che usano oggi, arricchito |
| 4 | **Formula TAKT e OME**: documentare le formule esatte con 2-3 esempi di calcolo | Antonio | Prima del kickoff | Anche scritto a mano va bene |
| 5 | **Regole allocazione**: documentare vincoli risorse esterne, regole di priorita', logiche di distribuzione temporale | Antonio | Prima del kickoff | |
| 6 | **Lista utenti piattaforma**: chi usera' il sistema, con quale profilo (Principal / Team Lead / Direzione) | Antonio | Prima del kickoff | |
| 7 | **Report esempio**: export di un report scostamenti settimanale attuale da Power BI | Antonio | Prima del kickoff | Per capire cosa replicare/migliorare |
| 8 | **Tabella trascodifica** fatturabile/non fatturabile in NAV | Georgia | Entro Mese 1 | Puo' partire dopo il kickoff |
| 9 | **Codifica competenze** richieste per opportunita' nel CRM | Marica | Entro Mese 1 | Definire struttura insieme al kickoff |

---

## Note dalla call

<!-- Compilare durante la call -->



---

## Decisioni prese

<!-- Compilare dopo la call -->



---

## Prossimi passi

<!-- Compilare dopo la call -->


