---
progetto: "sebi-group"
data: "2026-03-18"
destinatario: "Strumento mockup (generico)"
tags:
  - "#progetto:sebi-group"
  - "#fase:presales"
---

# Brief Mockup — Sebi Group

> **Uso**: questo documento viene passato allo strumento di mockup (codice, Figma, o altro) per la generazione delle schermate UI.
> Contiene tutto ciò che serve per produrre schermate fedeli alle aspettative del cliente.
> Per le specifiche dettagliate dei flussi e delle schermate, vedere `mockup-flows-spec.md`.

---

## Contesto prodotto

**Tipo di applicazione**: Web app (SaaS)
**Utenti principali**: 8-12 operatori commerciali (import/export), 2-3 manager. Profilo: non tecnico, età media 35-38 anni, abituati a Outlook e gestionale tradizionale.
**Dispositivi target**: Desktop (primario), responsive per tablet (secondario). No mobile.
**Lingua interfaccia**: Italiano (con supporto multilingua per email in uscita)

**Dominio**: Spedizioniere internazionale (import/export merci). Gli utenti ricevono 400-700 email/giorno su caselle condivise, gestiscono richieste di quotazione (RDO) da clienti e agenti esteri, contattano fornitori per preventivi, e preparano offerte. Terminologia di settore: Incoterms (FOB, CIF, EXW, DDP...), modalità trasporto (FCL, LCL, FTL, LTL, aereo), documenti (BL, AWB, CMR, Packing List), sovrapprezzi (THC, BAF, demurrage).

---

## Identità visiva

**Colori primari**: Enterprise Classico — sidebar scura #1E293B, contenuto bianco #FFFFFF
**Colori secondari**: Badge colorati Blu/Verde/Arancio/Rosso per stati e priorità. Grigio per testo secondario. Colori distinti per badge casella email di provenienza.
**Font**: Inter 13-14px, alta densità informativa
**Stile generale**: Enterprise Classico. Densità informativa alta ma organizzata. Separatori netti tra sezioni. Simile a strumenti come Front, Zendesk o HubSpot per l'email, non come Gmail.
**Logo disponibile**: no — usare placeholder "SEBI" in header
**Riferimenti UI che il cliente ama**: strumenti simili a quelli che già usano (gestionale tradizionale, Outlook) ma modernizzati. Layout familiare, non radicalmente diverso.
**AI data**: visivamente distinto dal resto — badge "Estratto da AI", confidence %, sfondo leggermente diverso

---

## Schermate da mockuppare

### Schermata 1: Inbox Unificata (completa)

**Scopo**: Vista principale dove l'operatore vede tutte le email delle caselle condivise, classificate e ordinate. Sostituisce completamente Outlook nel flusso quotidiano.

**Layout**: stile Outlook — lista email a tutta larghezza con anteprima espandibile. NON layout a 3 colonne compresse.

**Elementi chiave**:
- **Filtro visibilità**: "Le mie / Team / Tutte" — tutti vedono tutte le email, nessuna assegnazione automatica
- **Quick filters bar**: bottoni rapidi (Non lette, Export, Import, Mare, Aereo, Terra) + espandibile per filtri avanzati
- **Filtri avanzati**: casella, stato, categoria AI, data, cliente, destinazione, operatore, tipo trasporto (FCL/LCL/FTL/LTL/Aereo/Intermodale)
- **Lista email**: mittente, oggetto, anteprima, **badge casella di provenienza** (sales@, exportsales@, china@, project@), tag AI (tipo richiesta, area, modalità trasporto), badge pratica se associata, timestamp, warning icon per alert
- **Distinzione email nuove vs associate**: email senza pratica evidenziate con azione "Prendi in carico", email con pratica hanno badge codice cliccabile
- **Categorie AI**: tipo richiesta, area (import/export), modalità trasporto (mare/aereo/terra), lingua, destinazione, cliente nuovo/esistente, commodity type — con confidence %
- **Urgenza**: manuale (non AI) — l'operatore la imposta
- **Anteprima email**: pannello espandibile con corpo, allegati, banner alert contestuali
- **Azioni rapide**: Prendi in carico / Apri pratica, Rispondi, Inoltra, Imposta urgenza
- **Bottone demo "Simula risposta"**: visibile solo in demo, simula arrivo risposta fornitore/cliente

**Flusso**: landing page dopo login → filtra → click su email → anteprima → azione
**Note speciali**: la casella di provenienza è un badge/tag visibile nella lista. Le email già processate dall'AI al momento in cui l'utente le vede (processing in background).

---

### Schermata 2: Dettaglio Pratica / Quotazione (completa)

**Scopo**: Pagina dedicata (a tutta larghezza) di una pratica con tutto il contesto necessario.

**Layout**: pagina intera con sezioni/scroll, NON colonna compressa. Si esce dall'inbox per entrare qui.

**Elementi chiave**:
- **Header**: codice piattaforma (SEBI-2026-001) + codice ERP (solo import, solo dopo push al gestionale), cliente, tipo, modalità trasporto, stato, urgenza, operatore
- **Sezione Dati Spedizione**: tabella "Richiesta cliente" con dati AI (origine, dest, peso, dimensioni, pezzi, commodity, HS Code, Incoterms, modalità trasporto) + confidence %. Dati mancanti in rosso con bottone **"Richiedi info mancanti"**. Info cliente (fido, credito, storico).
- **Sezione Storico Interazioni (CRM)**: timeline cronologica di TUTTI gli eventi — email ricevute/inviate, cambi stato, creazione pratica, preventivi ricevuti, push a ERP, solleciti, note operatore. Ogni email espandibile.
- **Sezione Documenti**: tutti gli allegati estratti dalle email della pratica, con tag tipo documento (Packing List, Invoice, Preventivo, BL, AWB...)
- **Sezione Preventivi**: tabella comparativa fornitori (prezzo, transit, tipo, note, stato) + per import: vista parsing AI "prima/dopo" + calcolo margine (% o valore assoluto) + alternative multiple + genera quotazione
- **Solo Import — Modulo ERP**: sezione isolata per interazione gestionale (push dati, ricevi codice ERP, log)

**Transizioni stato configurabili**: Nuova → In quotazione → Inviata → Confermata / Rifiutata
**Alert inline**: banner colorati per credito, fornitori non rispondenti, deadline

---

### Schermata 3: Composizione Email (completa)

**Scopo**: Modale o pannello per comporre email con template predefiniti.

**Elementi chiave**:
- **No AI generativa** — solo template predefiniti
- **Template**: "Presa in carico", "Richiesta informazioni extra", "RDO Fornitore", "Sollecito Fornitore", "Quotazione Cliente"
- **A / CC / BCC**: autocomplete da rubrica. Per RDO: **selezione multipla fornitori** con filtri (tratta, tipo trasporto, zona) — invio massivo facile
- **Oggetto**: pre-compilato con codice pratica
- **Corpo email**: editor rich-text con template + variabili pratica
- **Allegati**: drag & drop, suggerimento allegati dalla pratica
- **Info contestuali**: sidebar con dati pratica
- **Azioni**: Invia (con conferma + indicazione N destinatari), Salva bozza, Annulla

---

### Schermata 4: Dashboard Operativa (light)

**Scopo**: Colpo d'occhio sul carico di lavoro dell'operatore.

**Elementi chiave**:
- **Card KPI**: email non lette, pratiche da lavorare oggi, solleciti da inviare, deadline prossime
- **Lista to-do prioritizzata**: azioni cliccabili (naviga a pratica)
- **Tabella pratiche attive**: ID, cliente, tipo, modalità trasporto, stato, ultimo aggiornamento

---

### Schermata 5: Dashboard Management (light)

**Scopo**: KPI aggregati. Focus su conversione e margini.

**Elementi chiave**:
- **KPI cards**: tasso conversione, margine medio, quotazioni inviate, valore pipeline
- **Grafico trend**: quotazioni inviate vs confermate
- **Filtri**: periodo, area (import/export), modalità trasporto

---

### Schermata 6: Pannello Configurazione — Admin (light)

**Scopo**: Configurazione regole sistema senza sviluppatori.

**Elementi chiave**:
- **Tab "Categorizzazione"**: gestione descrizioni AI per le categorie (tipo, area, modalità trasporto, lingua). Urgenza NON inclusa (è manuale).
- **Tab "Template Email"**: lista template modificabili con variabili
- **Tab "Stati Pratica"**: configurazione stati e transizioni
- **Tab "Caselle Email"**: stato connessione, frequenza polling, errori

---

## Navigazione e struttura

```
├── Inbox (vista email unificata) ← pagina principale
├── Lista Pratiche (con filtri stato, tipo, operatore, destinazione, trasporto)
│   └── Dettaglio pratica (pagina dedicata)
├── Dashboard
│   ├── Dashboard Operativa (per operatore)
│   └── Dashboard Management (solo manager)
├── Configurazione (solo admin)
│   ├── Categorizzazione
│   ├── Template Email
│   ├── Stati Pratica
│   └── Caselle Email
└── Profilo utente
```

Sidebar fissa a sinistra con icone + label. Header con nome utente, notifiche (campanella con contatore), ricerca globale.
"Lista Pratiche" è una voce a sé nella navigazione.

---

## Vincoli tecnici da rispettare nel mockup

- Layout ottimizzato per monitor 1920x1080 (desktop primario)
- Inbox: stile Outlook (lista + anteprima), NON 3 colonne compresse
- Dettaglio Pratica: pagina dedicata a tutta larghezza
- Stile Enterprise Classico: sidebar #1E293B, content #FFFFFF
- Font Inter 13-14px, alta densità
- I dati AI sono visivamente distinti (badge, confidence %, sfondo diverso)
- Urgenza: solo manuale, non AI
- Casella di provenienza: badge/tag visibile nella lista email
- Distinzione chiara email nuove vs associate a pratica
- Le azioni principali raggiungibili in max 2 click
- Lingua interfaccia: italiano, formattazione it-IT
- Bottone "Simula risposta" per demo

---

## Cosa NON mockuppare

- Login page (SSO)
- Gestione utenti e permessi
- Pagine di errore
- Versione mobile/tablet
- Integrazione WebCargo (fase successiva)
- Vista documenti doganali (fuori scope)
- **Gestione operativa post-conferma** (fuori scope — solo ciclo sales)
- **Assegnazione automatica operatori** (non prevista)
- **Urgenza automatica AI** (è manuale nel mockup)
