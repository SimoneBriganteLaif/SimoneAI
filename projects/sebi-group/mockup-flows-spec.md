---
progetto: "sebi-group"
data: "2026-03-18"
tipo: "Specifiche flussi e UI/UX per mockup"
scope: "Solo ciclo sales (non operativo)"
tags:
  - "#progetto:sebi-group"
  - "#fase:presales"
---

# Flussi e Specifiche UI/UX — SEBI Group Mockup

---

## A. Overview e Scope

### Obiettivo
Produrre un mockup interattivo della piattaforma SEBI Group che mostri al cliente come funzionerà il sistema nel flusso quotidiano degli operatori commerciali. Il mockup copre **solo il ciclo sales** (dalla ricezione email alla conferma/rifiuto quotazione), non la gestione operativa post-conferma.

### Utenti target
- **Operatori commerciali** (8-12): gestiscono email, prendono in carico richieste, inviano RDO ai fornitori, preparano quotazioni
- **Manager** (2-3): monitorano KPI, conversioni, margini
- **Admin** (1-2): configurano regole AI, template, stati

### Scope schermate
| Schermata | Livello dettaglio | Descrizione |
|-----------|------------------|-------------|
| Inbox Unificata | **Completa** | Vista email stile Outlook con categorizzazione AI |
| Dettaglio Pratica | **Completa** | Pagina dedicata con dati, timeline CRM, documenti, preventivi |
| Composizione Email | **Completa** | Template predefiniti, editor, contesto |
| Dashboard Operativa | Light | KPI e to-do operatore |
| Dashboard Management | Light | Conversioni e margini |
| Pannello Admin | Light | Configurazione regole e template |

### Stile UI
- **Enterprise Classico**: sidebar scura #1E293B, contenuto bianco #FFFFFF
- Badge colorati: Blu (info), Verde (conferma), Arancio (warning), Rosso (alert/urgente)
- Font Inter 13-14px, alta densità informativa
- Separatori netti tra sezioni
- Dati AI visivamente distinti (badge, confidence %, sfondo leggermente diverso)
- Ottimizzato 1920x1080
- Formattazione it-IT (dd/MM/yyyy, 1.250,00 EUR)

### Funzionalità demo mockup
Per rendere il mockup interattivo e convincente durante la demo:
- **Bottone "Simula risposta"**: bottone finto (visibile solo in demo mode) che simula l'arrivo di una risposta da cliente o fornitore, mostrando che la piattaforma intercetta la mail e la associa automaticamente alla pratica corretta. Serve a dimostrare il flusso end-to-end senza bisogno di inviare email reali.

---

## A-bis. Glossario terminologia logistica

Termini tecnici usati quotidianamente da SEBI e presenti nelle specifiche. Utile per chi costruisce il mockup.

### Incoterms (i più comuni)
| Codice | Significato | Chi gestisce il trasporto principale |
|--------|------------|--------------------------------------|
| **EXW** | Ex Works | Compratore (massimo onere per l'importatore) |
| **FOB** | Free on Board | Venditore fino a carico su nave, poi compratore |
| **CIF** | Cost, Insurance & Freight | Venditore fino a porto destinazione |
| **DAP** | Delivered at Place | Venditore fino a luogo concordato (no sdoganamento) |
| **DDP** | Delivered Duty Paid | Venditore (massimo onere per l'esportatore) |

L'Incoterm determina **chi paga cosa** e quindi quale parte del trasporto è gestita da SEBI per conto del cliente.

### Modalità di trasporto
| Sigla | Tipo | Descrizione |
|-------|------|-------------|
| **FCL** | Mare | Full Container Load — container intero |
| **LCL** | Mare | Less than Container Load — groupage mare |
| **20GP / 40GP / 40HC** | Mare | Tipi container (20 piedi, 40 piedi, 40 high cube) |
| **FTL** | Terra | Full Truck Load — camion completo |
| **LTL** | Terra | Less than Truck Load — groupage strada |
| **Aereo** | Aereo | Spedizione aerea (si misura in kg tassabili) |
| **Intermodale** | Misto | Combinazione di più modalità sotto un unico contratto |

### Documenti chiave
| Sigla | Documento | Quando serve |
|-------|-----------|-------------|
| **BL / B/L** | Bill of Lading (Polizza di Carico) | Trasporto marittimo — documento di titolo |
| **AWB** | Air Waybill | Trasporto aereo |
| **CMR** | Lettera di vettura | Trasporto stradale internazionale |
| **Packing List** | Lista colli | Sempre — dettaglio peso/dimensioni per collo |
| **Commercial Invoice** | Fattura commerciale | Sempre — serve per dogana |
| **C/O** | Certificato di Origine | Per dazi preferenziali |

### Sovrapprezzi e costi ricorrenti
| Sigla | Significato |
|-------|------------|
| **THC** | Terminal Handling Charge — costo movimentazione al porto |
| **BAF** | Bunker Adjustment Factor — sovrattassa carburante |
| **Demurrage** | Sovrattassa per ritardo ritiro container al porto |
| **Detention** | Sovrattassa per ritardo restituzione container vuoto |
| **Transit Time** | Giorni di transito porto-porto o door-door |

### Sigle operative
| Sigla | Significato |
|-------|------------|
| **RDO** | Richiesta di Offerta (Request for Quote) |
| **ETD / ETA** | Estimated Time of Departure / Arrival |
| **POL / POD** | Port of Loading / Port of Discharge |
| **Nolo** | Costo del trasporto marittimo principale |
| **All-in** | Tariffa tutto compreso (nolo + surcharge) |
| **HS Code** | Codice doganale merce (Harmonized System) |

---

## B. Flussi principali

### B0. Pipeline di processing (cosa succede prima che l'utente veda le email)

```
Sistema esegue polling caselle email ogni N minuti
    │  (sales@, exportsales@, china@, project@)
    │
    ▼
Nuove email importate nel sistema
    │
    ▼
Per ogni email, il sistema verifica:
    │
    ├── Codice pratica presente nell'oggetto? (es. SEBI-2026-001 o 2026-12345678)
    │   │
    │   ├── SÌ → email associata automaticamente alla pratica esistente
    │   │        (appare nella timeline della pratica + nell'inbox con badge pratica)
    │   │
    │   └── NO → email classificata come "nuova" (potenziale nuova richiesta)
    │
    ▼
AI processa TUTTE le email (nuove e associate):
    │  • estrazione dati (origine, dest, peso, commodity, Incoterms, modalità trasporto...)
    │  • categorizzazione automatica:
    │     - tipo richiesta (quotazione, conferma, info, operativo, sollecito...)
    │     - area (import / export)
    │     - modalità trasporto (mare FCL/LCL, aereo, terra FTL/LTL, intermodale)
    │     - lingua
    │     - destinazione / origine
    │     - cliente (nuovo / esistente)
    │     - commodity type
    │     - confidence % per ogni campo
    │  • urgenza: NON categorizzata da AI — impostata manualmente dall'operatore
    │
    ▼
Email appaiono nell'Inbox pronte per essere lavorate
    │  con tutti i tag AI, dati estratti, e associazione pratica (se applicabile)
```

**Principio chiave**: quando l'utente apre l'app, le email sono già processate. L'AI lavora in background, non in tempo reale davanti all'utente.

**Riconoscimento email nuove vs esistenti**: il codice pratica nell'oggetto è il meccanismo principale. Questo è fondamentale per associare le risposte dei fornitori e dei clienti alla pratica corretta. Le email senza codice nell'oggetto sono trattate come potenziali nuove richieste.

---

### B1. Flusso Email → Inbox

```
Email già processate dall'AI (→ B0)
    │
    ▼
Operatore apre l'Inbox
    │  vede lista email stile Outlook
    │  ogni email ha tag AI + badge casella di provenienza
    │
    ▼
Operatore filtra per categorie preferite
    │  (nessuna assegnazione automatica)
    │  filtro: "Le mie / Team / Tutte"
    │
    ▼
Quick filters: Non lette, Export, Import, Mare, Aereo, Terra
    + filtri avanzati espandibili
    │
    ▼
Distinzione visiva chiara:
    ├── Email NUOVE (senza pratica): evidenziate, azione "Prendi in carico"
    └── Email ASSOCIATE a pratica: badge con codice pratica, azione "Apri pratica"
```

**Caselle monitorate**: sales@, exportsales@, china@, project@ @sebigroup.com

**Principio chiave**: tutti vedono tutte le email. L'operatore filtra e sceglie cosa prendere in carico. Non c'è assegnazione automatica.

---

### B2. Flusso Presa in Carico

```
Operatore seleziona email NUOVA dall'Inbox
    │
    ▼
Click "Prendi in carico"
    │
    ▼
Sistema genera codice pratica piattaforma
    │  es. SEBI-2026-001
    │  (il codice ERP per import NON esiste ancora a questo punto)
    │
    ▼
Codice inserito nell'oggetto email (per aggregare thread futuri)
    │
    ▼
Vista dati estratti da AI nella pagina Dettaglio Pratica
    │  origine, destinazione, peso, dimensioni, pezzi,
    │  commodity, Incoterms, modalità trasporto
    │  ogni campo con confidence %
    │
    ├── Dati completi → procede con flusso quotazione
    │
    └── Dati mancanti evidenziati in rosso
         │
         ▼
        Bottone "Richiedi info mancanti"
         │  → genera email al cliente (template "Richiesta informazioni extra")
         │
         ▼
        In attesa risposta cliente
         │  (quando il cliente risponde, la risposta viene associata
         │   alla pratica tramite codice nell'oggetto → appare nella timeline)
```

---

### B3. Flusso Export (senza ERP)

```
Email cliente ricevuta e processata
    │
    ▼
Presa in carico (→ B2)
    │  Codice: SEBI-2026-XXX
    │
    ▼
Dati estratti da AI → tabella "Richiesta cliente"
    │  (origine, destinazione, peso, dimensioni, pezzi,
    │   commodity, Incoterms, modalità trasporto, note)
    │
    ▼
Operatore seleziona fornitori da rubrica
    │  filtri: tratta, tipo trasporto (FCL/LCL/aereo/terra), zona
    │  ⚡ selezione multipla per invio massivo
    │
    ▼
Invia RDO a N fornitori dalla piattaforma
    │  template: "RDO Fornitore"
    │  → un'email per fornitore, tutte con codice pratica nell'oggetto
    │  → deve essere FACILE e VELOCE mandare tante RDO
    │
    ▼
Fornitori rispondono via email
    │  piattaforma intercetta e associa alla pratica (codice nell'oggetto)
    │  AI estrae dati dalla risposta → compila tabella preventivi
    │
    ▼
Nella pratica ci sono ORA DUE TABELLE:
    │
    │  TABELLA 1 — "Richiesta cliente" (dati estratti dalla mail originale)
    │  ┌─────────────┬──────────────┬────────┬──────────┬──────────┐
    │  │ Origine     │ Destinazione │ Peso   │ Commodity │ Incoterm │
    │  │ Shanghai,CN │ Milano,IT    │ 2.450kg│ Elettron. │ FOB      │
    │  └─────────────┴──────────────┴────────┴──────────┴──────────┘
    │
    │  TABELLA 2 — "Preventivi fornitori" (confronto)
    │  ┌───────────┬──────────┬─────────┬───────┬──────────────────┐
    │  │ Fornitore │ Prezzo   │ Transit │ Note  │ Stato            │
    │  │ MSC       │ 1.250EUR │ 32gg    │ Suez  │ ✉ Risposta       │
    │  │ Maersk    │ 1.180EUR │ 35gg    │ —     │ ✉ Risposta       │
    │  │ CMA CGM   │ —        │ —       │ —     │ ⏳ In attesa      │
    │  └───────────┴──────────┴─────────┴───────┴──────────────────┘
    │
    ▼
Operatore seleziona fornitore/i + applica margine
    │  margine: % o valore assoluto (campo editabile, switch %)
    │  prezzo fornitore + ricarico = prezzo cliente
    │  può selezionare più fornitori per alternative
    │
    ▼
Genera quotazione cliente (solo fornitori selezionati)
    │  template: "Quotazione Cliente"
    │  1 o più alternative (più veloce, più economico)
    │
    ▼
Invia al cliente
    │
    ├── Confermata → pratica chiusa (lato sales)
    ├── Rifiutata → pratica chiusa
    └── Revisione richiesta (~90% dei casi: cambio peso/dimensioni)
         │
         ▼
        Ciclo riparte da RDO fornitori
```

---

### B4. Flusso Import (con ERP)

```
Email cliente ricevuta e processata
    │
    ▼
Presa in carico (→ B2)
    │  Codice piattaforma: SEBI-2026-XXX
    │  (codice ERP NON ancora assegnato)
    │
    ▼
Dati estratti da AI → tabella "Richiesta cliente"
    │
    ▼
Bottone "Inserisci nel gestionale"
    │  → push dati via API all'ERP
    │  → ERP risponde con il codice numerico (es. 2026-12345678)
    │  → codice ERP associato alla pratica da QUESTO momento
    │  → la pratica mostra ora DOPPIO codice: SEBI-2026-XXX + 2026-12345678
    │
    ▼
ERP manda N email automatiche ai fornitori
    │  (con codice ERP nell'oggetto)
    │
    ▼
Fornitori rispondono alla casella
    │  piattaforma intercetta risposte
    │  associa alla pratica tramite codice ERP nell'oggetto
    │
    ▼
AI parsing: normalizza formati diversi fornitori
    │  → tabella comparativa uniforme (stessa struttura di Export)
    │  → vista "prima/dopo" (email originale → dati strutturati)
    │     importante perché i fornitori rispondono con formati molto diversi
    │
    ▼
Due tabelle nella pratica (come Export):
    │  TABELLA 1 — "Richiesta cliente"
    │  TABELLA 2 — "Preventivi fornitori" (con dati normalizzati dall'AI)
    │
    ▼
Gestione mail aggiuntive con cliente/fornitori
    │
    ▼
Quotazione al cliente con 1+ alternative + margine (% o assoluto)
    │
    ▼
Invia al cliente
    │
    ├── Confermata → chiusa lato sales
    └── Rifiutata → chiusa lato sales
```

**Differenze chiave rispetto a Export**:
- Il codice ERP viene assegnato **solo dopo** il push al gestionale, non alla presa in carico
- L'ERP invia le RDO ai fornitori (non la piattaforma direttamente)
- L'AI parsing è più rilevante perché i fornitori rispondono in formati molto diversi
- L'interazione con l'ERP è un **modulo ben definito** (API push dati → ricevi codice → intercetta risposte)

---

## C. Schermate — Specifiche dettagliate

### C1. Inbox Unificata (completa)

#### Layout
**Stile Outlook**: lista email a tutta larghezza (non 3 colonne compresse). Anteprima email in pannello espandibile o pannello laterale attivabile.

La pratica ha la sua **pagina dedicata** separata — non è compressa in una colonna dell'inbox.

#### Barra superiore
- Toggle **"Le mie / Team / Tutte"**
- Ricerca full-text
- Quick filters: Non lette, Export, Import, Mare, Aereo, Terra
- Bottone "Filtri avanzati" → espande pannello

#### Filtri avanzati (espandibili)
- Casella email di provenienza
- Stato pratica
- Categoria AI (tipo richiesta, area, modalità trasporto)
- Data (range)
- Cliente
- Destinazione / Origine
- Operatore assegnato
- Tipo trasporto (FCL, LCL, FTL, LTL, Aereo, Intermodale)

#### Lista email
Ogni riga mostra:
- Checkbox (per azioni bulk)
- Mittente (nome o email)
- Oggetto (troncato)
- Preview testo (1 riga)
- **Badge casella**: tag colorato che indica da quale casella è arrivata (es. "sales@" verde, "china@" rosso, "export@" blu)
- **Tag AI**: tipo richiesta, area (import/export), modalità trasporto — con colori
- **Badge pratica** (se associata): codice pratica cliccabile (es. "SEBI-2026-015")
- **Indicatore "Nuova"**: evidenziazione per email senza pratica associata
- Timestamp (relativo: "2h fa", "ieri")
- Warning icon se ci sono alert attivi (fido, credito, etc.)
- Urgenza: badge manuale se impostata dall'operatore (non AI)

Ordinamento default: per data (più recenti in alto).

#### Anteprima email
Pannello attivabile (click su email o split-view tipo Outlook):
- Header: mittente, destinatari, data, oggetto
- Corpo email completo
- Lista allegati (con dimensione e tipo)
- Banner alert contestuali in alto:
  - "Cliente con fido esaurito" (rosso)
  - "Agente non verificato in network" (arancio)
  - "Cliente nuovo — nessuno storico" (blu info)
- Azioni rapide (bottoni):
  - **Prendi in carico** (se email nuova, senza pratica)
  - **Apri pratica** (se email già associata)
  - Rispondi
  - Inoltra
  - Imposta urgenza (manuale)

#### Bottone demo "Simula risposta"
Visibile solo in modalità demo. Click → simula l'arrivo di una risposta fornitore/cliente che si associa automaticamente alla pratica, mostrando il meccanismo in azione.

---

### C2. Dettaglio Pratica (completa) — Pagina dedicata

**Layout**: pagina intera, NON colonna compressa. Organizzata in sezioni/tab con scroll verticale.

#### Header pratica
- Codice pratica piattaforma: **SEBI-2026-001** (sempre visibile)
- Codice ERP (solo import, solo dopo push al gestionale): **2026-12345678** (con label "Cod. Gestionale")
- Nome cliente (link a anagrafica)
- Tipo: badge "Import" o "Export"
- Modalità trasporto: badge (es. "FCL Mare", "Aereo", "FTL Terra")
- Stato: badge colorato (es. "In quotazione" arancio)
- Urgenza: badge manuale (se impostata)
- Date: creazione, ultimo aggiornamento
- Operatore assegnato
- Bottone "Torna a Inbox"

#### Sezione 1 — Dati spedizione (richiesta cliente)

**Tabella "Richiesta cliente"** — dati estratti dall'AI con confidence:

| Campo | Valore | Confidence | Fonte |
|-------|--------|------------|-------|
| Origine | Shanghai, CN | 95% ✓ | AI |
| Destinazione | Milano, IT | 98% ✓ | AI |
| Peso | 2.450 kg | 87% ⚠ | AI |
| Dimensioni | 120x80x100 cm | — (mancante) | — |
| Pezzi | 15 | 92% ✓ | AI |
| Commodity | Componenti elettronici | 78% ⚠ | AI |
| HS Code | 8542.31 | 65% ⚠ | AI |
| Incoterms | FOB | 95% ✓ | AI |
| Modalità trasporto | FCL Mare | 90% ✓ | AI |
| Tipo container | 40HC | — (mancante) | — |

- Ogni campo editabile dall'operatore
- Badge "Estratto da AI" con icona
- Confidence: ✓ verde (>90%), ⚠ arancio (70-90%), ✗ rosso (<70%)
- Campi mancanti: riga evidenziata in rosso con "—"
- Bottone **"Richiedi info mancanti"**: genera email al cliente con i campi mancanti elencati

**Info cliente** (pannello laterale o sezione collassabile):
- Ragione sociale
- Fido disponibile / Fido totale (barra grafica)
- Stato credito: badge (Regolare / In ritardo / Bloccato)
- Storico: N quotazioni, tasso conferma %, ultimo ordine

#### Sezione 2 — Storico interazioni (stile CRM)

Cronologia verticale completa (più recente in alto) di **tutti gli eventi** della pratica, non solo le email:

| Tipo evento | Icona | Esempio |
|-------------|-------|---------|
| Email ricevuta | ✉ | "Email ricevuta da cliente@rossi.it — Richiesta quotazione FCL Shanghai" |
| Email inviata | ➤ | "RDO inviata a MSC, Maersk, CMA CGM (3 fornitori)" |
| Cambio stato | 🔄 | "Stato cambiato: Nuova → In quotazione" |
| Pratica creata | ➕ | "Pratica SEBI-2026-001 creata — operatore: M. Rossi" |
| Preventivo ricevuto | 📊 | "Preventivo ricevuto da MSC — 1.250 EUR, 32gg transit" |
| Push a ERP | 🔗 | "Dati inviati al gestionale — Cod. ERP: 2026-12345678" |
| Sollecito inviato | ⏰ | "Sollecito inviato a CMA CGM (in attesa da 3gg)" |
| Quotazione inviata | 📤 | "Quotazione v1 inviata al cliente — 1.357,00 EUR" |
| Nota operatore | 📝 | "Cliente chiede consegna entro fine mese" |
| Urgenza impostata | 🔴 | "Urgenza impostata: Alta — da M. Rossi" |

Ogni email nella timeline è espandibile per leggere il testo completo.

Azioni inline:
- "Sollecita fornitore" (su RDO senza risposta)
- "Rispondi" (su email ricevuta)
- "Aggiungi nota"

#### Sezione 3 — Documenti allegati

Raccolta di **tutti i documenti/allegati** estratti dalle email della pratica:

| Documento | Tipo | Fonte | Data | Dimensione |
|-----------|------|-------|------|------------|
| Packing_list_Shanghai.pdf | Packing List | Email cliente 14/03 | 14/03/2026 | 245 KB |
| Commercial_Invoice_2026.pdf | Fattura commerciale | Email cliente 14/03 | 14/03/2026 | 180 KB |
| MSC_quotation.pdf | Preventivo fornitore | Email MSC 16/03 | 16/03/2026 | 95 KB |
| Maersk_rate_FCL.xlsx | Preventivo fornitore | Email Maersk 16/03 | 16/03/2026 | 42 KB |

- Click → preview/download
- Possibilità di allegare documenti manualmente
- Tag tipo documento (Packing List, Invoice, Preventivo, BL, AWB, Certificato, Altro)

#### Sezione 4 — Preventivi fornitori e quotazione

**Tabella preventivi fornitori** (popolata da AI parsing delle risposte)

| Fornitore | Prezzo | Transit | Tipo | Note | Stato |
|-----------|--------|---------|------|------|-------|
| MSC | 1.250 EUR | 32 gg | FCL 40HC | Via Suez | ✉ Risposta ricevuta |
| Maersk | 1.180 EUR | 35 gg | FCL 40HC | — | ✉ Risposta ricevuta |
| CMA CGM | — | — | — | — | ⏳ In attesa |
| Evergreen | 1.320 EUR | 30 gg | FCL 40HC | Via Suez, fast | ✉ Risposta ricevuta |

- Ordinabile per prezzo, transit time
- Stato: "Inviata RDO" / "Risposta ricevuta" / "Sollecitato" / "Scaduto"
- Checkbox per selezionare i fornitori da includere nella quotazione al cliente

**Vista parsing AI "prima/dopo" (soprattutto per import)**
- Pannello espandibile per ogni fornitore che mostra:
  - **Prima**: testo originale dell'email del fornitore (formati diversi, lingue diverse)
  - **Dopo**: dati normalizzati nella riga della tabella
- Utile per verificare che il parsing sia corretto

**Sezione calcolo quotazione**
- Fornitore/i selezionati (checkbox nella tabella)
- Per ogni fornitore selezionato:
  - Prezzo fornitore: 1.180,00 EUR
  - Tipo margine: **switch % / valore assoluto**
  - Ricarico: +15% oppure +200,00 EUR
  - **Prezzo cliente: 1.357,00 EUR** (calcolato in automatico)
- Possibilità di aggiungere alternative:
  - Alternativa 1: "Economica" — Maersk, 35gg, 1.357,00 EUR
  - Alternativa 2: "Veloce" — Evergreen, 30gg, 1.518,00 EUR

Bottone **"Genera quotazione"** → apre composizione email con template "Quotazione Cliente" pre-compilato con le alternative selezionate

**Storico revisioni**
- v1 — 14/03/2026 — 1.357,00 EUR — Inviata
- v2 — 16/03/2026 — 1.320,00 EUR (revisione peso) — Inviata
- v3 — 17/03/2026 — 1.320,00 EUR — Confermata ✓

#### Sezione 5 — Solo Import: Modulo ERP

Per le pratiche import, sezione dedicata all'interazione con il gestionale:

- **Stato integrazione**: "Non inviato" / "Inviato al gestionale" / "Codice ERP ricevuto"
- Bottone **"Inserisci nel gestionale"** → push dati via API
- Dopo il push: mostra codice ERP ricevuto (es. 2026-12345678)
- Log delle interazioni con l'ERP (data push, risposta, errori)

Questo è un **modulo ben definito e isolato** — l'interfaccia con il gestionale SEBI è confinata in questa sezione.

#### Transizioni stato
Configurabili dall'admin. Set base:

```
Nuova → In quotazione → Inviata → Confermata
                                  → Rifiutata
```

- Il cambio stato può essere manuale o automatico (es. "Inviata" quando si invia la quotazione)
- Gli stati sono configurabili nel pannello Admin (tab "Stati Pratica")

#### Alert inline
Banner colorati nella parte alta della pratica:
- "Fido cliente esaurito — contattare amministrazione" (rosso)
- "MSC non ha risposto da 3 giorni — sollecitare?" (arancio)
- "Deadline quotazione: domani 18:00" (giallo)

---

### C3. Composizione Email (completa)

#### Apertura
Modale o pannello laterale. Si apre dal dettaglio pratica o dall'inbox.

#### Template selector
Dropdown in alto con template predefiniti:
1. **"Presa in carico"** — conferma al cliente che la richiesta è in lavorazione
2. **"Richiesta informazioni extra"** — richiede dati mancanti al cliente
3. **"RDO Fornitore"** — richiesta di quotazione al fornitore
4. **"Sollecito Fornitore"** — reminder a fornitore che non ha risposto
5. **"Quotazione Cliente"** — invio offerta al cliente con dettagli e alternative

Selezionando un template, il corpo email si popola con il testo predefinito + variabili della pratica (codice, dati spedizione, prezzi).

**Nessuna AI generativa**: il testo viene solo dal template. L'operatore modifica manualmente.

#### Campi email
- **A**: autocomplete da rubrica (clienti e fornitori). Per RDO: **selezione multipla fornitori** dalla rubrica con filtri (tratta, tipo trasporto FCL/LCL/aereo/terra, zona) — deve essere facile selezionare tanti fornitori e inviare in blocco
- **CC / BCC**: autocomplete
- **Oggetto**: pre-compilato con codice pratica (es. "SEBI-2026-001 — RDO FCL Shanghai-Milano")
- **Corpo**: editor rich-text con formattazione base (grassetto, elenchi, tabelle)
- **Allegati**: drag & drop + bottone upload. Suggerimento allegati dalla pratica (packing list, invoice).

#### Sidebar contestuale
Pannello a destra (o in basso) con:
- Dati pratica sintetici (origine, destinazione, peso, commodity, Incoterm, modalità trasporto)
- Nome e dati cliente
- Storico email della pratica (per contesto)

#### Azioni
- **Invia** (con dialog di conferma "Sei sicuro?" + indicazione N destinatari se invio multiplo)
- **Salva bozza**
- **Annulla** (chiude senza salvare, con conferma se ci sono modifiche)

---

### C4. Dashboard Operativa (light)

#### KPI cards (riga in alto)
4 card con icona, numero, label:
1. **Email non lette**: contatore totale caselle monitorate
2. **Pratiche da lavorare oggi**: pratiche con azioni pendenti
3. **Solleciti da inviare**: fornitori che non hanno risposto in tempo
4. **Deadline prossime**: pratiche con deadline entro 48h

#### Lista to-do prioritizzata
Tabella ordinata per priorità:
| Priorità | Azione | Pratica | Cliente | Scadenza |
|----------|--------|---------|---------|----------|
| Alta | Sollecitare MSC | SEBI-2026-015 | Rossi SpA | Oggi |
| Media | Inviare quotazione | SEBI-2026-022 | Bianchi Srl | Domani |
| Bassa | Verificare risposta | SEBI-2026-018 | Chen Ltd | 20/03 |

Click su riga → naviga al dettaglio pratica.

#### Tabella pratiche attive
| ID | Cliente | Tipo | Trasporto | Stato | Ultimo agg. |
|----|---------|------|-----------|-------|-------------|
| SEBI-2026-015 | Rossi SpA | Export | FCL Mare | In quotazione | 2h fa |
| SEBI-2026-022 | Bianchi Srl | Import | Aereo | Inviata | Ieri |

---

### C5. Dashboard Management (light)

#### KPI cards
1. **Tasso conversione**: % quotazioni confermate / inviate (benchmark 18%)
2. **Margine medio**: margine % medio sulle quotazioni confermate
3. **Quotazioni inviate** (mese corrente)
4. **Valore pipeline**: somma quotazioni in attesa di conferma

#### Grafico trend
Grafico a linee: quotazioni inviate vs confermate, ultimi 6 mesi.
Asse X: mesi. Asse Y: numero quotazioni. Due linee con area fill.

#### Filtri
- Periodo: mese, trimestre, anno, custom
- Area: Import / Export / Tutte
- Modalità trasporto: Mare / Aereo / Terra / Tutte

---

### C6. Pannello Admin (light)

#### Tab "Categorizzazione"
Tabella editabile delle regole AI:
| Categoria | Valori possibili | Descrizione per AI | Attiva |
|-----------|-----------------|-------------------|--------|
| Tipo richiesta | Quotazione, Conferma, Info, Operativo, Sollecito | Descrizione testuale | ✓ |
| Area | Import / Export | Basata su contesto email | ✓ |
| Modalità trasporto | Mare FCL, Mare LCL, Aereo, Terra FTL, Terra LTL, Intermodale | Riconoscimento da keyword + contesto | ✓ |
| Lingua | IT, EN, ZH, DE, FR... | Rilevamento automatico | ✓ |

**Nota**: l'urgenza NON è nella tabella AI — è sempre manuale.

L'admin modifica le **descrizioni** che l'AI usa per categorizzare (non regole if/then, ma descrizioni testuali che guidano il modello).

#### Tab "Template Email"
| Nome template | Lingua | Ultima modifica |
|---------------|--------|-----------------|
| Presa in carico | IT | 10/03/2026 |
| RDO Fornitore | IT/EN | 08/03/2026 |
| Sollecito Fornitore | IT/EN | 08/03/2026 |
| Richiesta info extra | IT | 11/03/2026 |
| Quotazione Cliente | IT | 12/03/2026 |

Click → editor inline con anteprima. Variabili disponibili: {{codice_pratica}}, {{cliente}}, {{origine}}, {{destinazione}}, {{peso}}, {{commodity}}, {{incoterm}}, {{modalita_trasporto}}, etc.

#### Tab "Stati Pratica"
Configurazione degli stati e transizioni:
| Stato | Colore | Transizioni consentite | Ordine |
|-------|--------|----------------------|--------|
| Nuova | Blu | → In quotazione | 1 |
| In quotazione | Arancio | → Inviata | 2 |
| Inviata | Giallo | → Confermata, → Rifiutata | 3 |
| Confermata | Verde | (finale) | 4 |
| Rifiutata | Rosso | (finale) | 5 |

Admin può aggiungere, rimuovere, riordinare stati e definire le transizioni consentite.

#### Tab "Caselle Email"
| Casella | Stato | Ultima sync | Frequenza polling | Errori |
|---------|-------|-------------|-------------------|--------|
| sales@sebigroup.com | Connessa | 2 min fa | ogni 5 min | — |
| exportsales@sebigroup.com | Connessa | 2 min fa | ogni 5 min | — |
| china@sebigroup.com | Connessa | 5 min fa | ogni 5 min | — |
| project@sebigroup.com | Errore | 1h fa | ogni 5 min | Auth scaduta |

---

## D. Decisioni UI/UX

### Layout generale
- **Inbox**: stile Outlook — lista email a tutta larghezza con anteprima espandibile. NON layout a 3 colonne compresse.
- **Dettaglio Pratica**: pagina dedicata a tutta larghezza, organizzata in sezioni con scroll. Si esce dall'inbox per entrare nella pratica.
- Questo evita la compressione eccessiva di un layout a 3 colonne e dà spazio a tutte le informazioni.

### Stile visivo
- **Sidebar navigazione**: #1E293B (scuro), testo bianco, icone + label
- **Content area**: #FFFFFF, testo #1E293B
- **Badge stati**: Blu (Nuova), Arancio (In quotazione), Giallo (Inviata), Verde (Confermata), Rosso (Rifiutata)
- **Badge casella**: colori distinti per casella email di provenienza
- **Badge modalità trasporto**: icona + testo (nave, aereo, camion)
- **Font**: Inter, 13-14px per body, 11-12px per metadata
- **Alta densità**: molte informazioni per schermata, ben separate da bordi e spacing

### Dati AI
- Ogni dato estratto da AI ha badge "Estratto da AI" e confidence %
- Sfondo leggermente diverso (es. #F8FAFC) per distinguere da dati manuali
- Confidence: colore icona proporzionale al valore

### Urgenza
- **Manuale**, non AI. L'operatore la imposta esplicitamente.
- Motivo: l'urgenza è difficile da determinare automaticamente in modo affidabile nel contesto logistico.
- Badge: Rosso (Alta), Arancio (Media), nessun badge (Bassa/non impostata).

### Email nuove vs associate
- Le email **nuove** (senza pratica) hanno evidenziazione visiva distinta e azione primaria "Prendi in carico"
- Le email **associate a pratica** mostrano il badge codice pratica e azione "Apri pratica"
- Il meccanismo di associazione è il **codice pratica nell'oggetto email**. Questo è il punto fondamentale del sistema.

### Alert e warning
- Nella **lista email** (Inbox): warning icon accanto alla riga
- Nel **dettaglio pratica**: banner colorato in alto con testo esplicito e azione suggerita
- Colori alert: rosso (bloccante), arancio (attenzione), giallo (informativo)

### Filtri
- Quick filters sempre visibili (bottoni rapidi)
- Filtri avanzati espandibili (collassati di default)
- I filtri attivi mostrano badge contatore

### Formattazione
- Date: dd/MM/yyyy (es. 18/03/2026)
- Valute: 1.250,00 EUR (formato italiano)
- Percentuali: 18,5%
- Pesi: 2.450 kg
- Lingua interfaccia: italiano

### Ottimizzazione
- Target: 1920x1080
- Scrolling verticale per liste lunghe, paginazione classica
- Dettaglio pratica: sezioni collassabili per gestire la densità

---

## E. Evolutive (fuori scope mockup)

Le seguenti funzionalità sono state discusse e pianificate come moduli futuri. Non vanno incluse nel mockup ma sono documentate separatamente in `evolutive-backlog.md`.

- Feedback AI automatico su correzione categorizzazione
- Urgenza AI-driven (attualmente manuale)
- Invio automatico email per info mancanti (senza click operatore)
- Gestione operativa post-conferma (modulo separato)
- Assegnazione automatica operatori
- Riconoscimento avanzato thread email senza codice nell'oggetto (ML su contenuto)
- Integrazione WebCargo
- Documenti doganali
- App mobile/tablet
