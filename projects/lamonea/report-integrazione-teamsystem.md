---
progetto: "lamonea"
data: "2026-03-10"
tags:
  - "#progetto:lamonea"
  - "#fase:dev"
---

# Report: Integrazione TeamSystem per Lamonea — Preparazione Call Tecnica

Data: 2026-03-10
Call prevista: 2026-03-11

#progetto:lamonea #fase:presales #stack:teamsystem

---

## Contesto

Lamonea (3 aziende: SRL cod.49, Endosurgery cod.133, Medical cod.212) necessita di integrazione bidirezionale con TeamSystem Lynfa Azienda per sincronizzare anagrafiche, documenti e dati operativi con la nuova piattaforma cloud (FastAPI + Next.js). La call con il tecnico TeamSystem serve a definire concretamente come configurare le API per lettura/scrittura.

---

## 1. Anagrafiche TeamSystem rilevanti per Lamonea

### Anagrafiche Clienti/Fornitori (ANACF)
- **Archivio**: `ANACF` (anagrafica generale), `CLIGEST`/`FORGEST` (dati gestionali)
- **CodiceWS configurato**: 500001 (gia attivo per clienti/fornitori)
- **Dati chiave**:
  - Ragione sociale, P.IVA, Codice Fiscale, indirizzi
  - Contatti (telefono, email, PEC)
  - Condizioni pagamento (`CF-CODPAGAM`)
  - Fido (`CF-GESFIDO`: S=solo documenti, O=solo ordini, E=entrambi)
  - Vendite bloccate (`CF-VENDBLOC`: S/N/X)
  - Tipo soggetto fattura elettronica (`CF-STATO-PA`: B=privato SDI, A=PA, X=non attiva)
  - Categorie, sottocategorie, area, zona
  - Destinatari merce, annotazioni
- **Filtro C/F**: `VariazTipo` = "1" per clienti, "2" per fornitori
- **Variazioni supportate**: SI — file `ANACF` e `CFDATI`

### Anagrafica Articoli (MAGANA)
- **Archivio**: `MAGANA`, `MAGAGEST`, `MAGAGG`
- **CodiceWS da configurare**: 500027
- **Dati chiave**:
  - Codice articolo (`M-CODMAG`), descrizione, descrizione aggiuntiva
  - Famiglia, sottofamiglia, gruppo, sottogruppo
  - Aliquota IVA, prezzi (fino a 8 listini), costi
  - Tipo articolo (`M-TIPOART`: C=catalogo, V=non vendibile, B=bene usato)
  - Codici a barre, articoli fornitore
- **Vista relazionale**: articolo + attributi + famiglia + codici a barre + fornitori in unico schema
- **Variazioni supportate**: SI — file `MAGANA`
- **Volume stimato**: ~12.400 articoli totali, ~4.000-5.000 attivi

### Scadenze (EFFSCA)
- **Rilevanza**: dati finanziari read-only (situazione creditizia clienti)
- **Variazioni supportate**: SI

### Documenti di Vendita (MOVBOL)
- **CodiceWS da configurare**: 500011
- **Struttura**: Testata/Corpo — campo `B-TIPO` determina il tipo documento:
  - 1=Bolle vendita, 2=Fatture accompagnatorie, 3=Fatture immediate
  - 4=Note credito, 5=Ricevute fiscali, 10=Preventivi, 21=Bolle reso
- **Variazioni supportate**: NO (solo estrazione diretta)

### Ordini (MOVORD)
- **CodiceWS da configurare**: 500009 o 500028
- **Struttura**: Testata/Corpo — `OR-TIPO`: 1=clienti, 2=fornitori
- **Variazioni supportate**: SI

### Altre anagrafiche rilevanti
- **Totali Fatturazione (FOUTFAT)**: dati aggregati fatturato, variazioni SI
- **Giacenze/Progressivi (MAGPRO)**: disponibilita articoli, variazioni SI
- **Movimenti Magazzino (MOVMAG)**: variazioni SI
- **Tabelle di supporto**: famiglie, sottofamiglie, categorie, zone, causali, pagamenti, listini

---

## 2. Come creare API in lettura

### Architettura
- **Protocollo**: REST (solo REST, no SOAP), formato JSON
- **Autenticazione**: Bearer Token — `Authorization: Bearer PGAUTH-xxxxxxxx`
- **Endpoint sincrono**: `.../EVWSSYNC` (timeout 5s — attualmente rotto su Lamonea)
- **Endpoint asincrono**: `.../EVWSASYNC` (restituisce UUID, poi polling)

### Request di Lettura
```json
{
  "CodiceWS": "500001",
  "Schema": "1",
  "Versione": "20250006",
  "Operazione": "read",
  "Ditta": "49",
  "TabellaCampi": [
    {"CF-TIPO": "1", "CF-CODICE": "0", "operatore": "<>"}
  ]
}
```

### Lettura dalle Variazioni (sync incrementale)
```json
{
  "CodiceWS": "500001",
  "Schema": "1",
  "Versione": "20250006",
  "Operazione": "read",
  "Ditta": "49",
  "Variazioni": "S",
  "VariazData": "20260309",
  "VariazOra": "080000",
  "VariazTipo": "1",
  "TabellaCampi": []
}
```

**File che supportano variazioni**: ANACF, CFDATI, EFFSCA, FOUTFAT, MAGANA, MAGPRO, MOVMAG, MOVORD

### Operatori di filtro
| Operatore | Significato |
|-----------|-------------|
| `=` | Uguale (default) |
| `>` / `<` | Maggiore / Minore |
| `>=` | A partire da |
| `<>` | Diverso |
| `cm` | Compreso (due righe: inizio e fine) |
| `il` / `nl` | In lista / Non in lista |
| `ct` | Contiene (ricerca parziale) |

### Configurazione in CONFWS
Ogni WS va configurato in `CONFWS` (Procedure Gestionali > Amministrazione > AcuRcl > CONFWS):
1. **Scheda Parametri**: attivazione, versione, tipo log
2. **Scheda Gestione Campi**: tipo (Tabellare vs Vista), archivio master, permessi R/W/Delete
3. **Scheda Request**: campi filtro, nomi chiave, trascodifiche
4. **Scheda Response**: campi da restituire, nomi chiave, formati date

**Importante**: WS standard (codici < 500000) NON si modificano. Si duplicano con codici >= 500001.

### Sincrono vs Asincrono
- **Sincrono** (`EVWSSYNC`): timeout 5s. **Su Lamonea restituisce SEMPRE WORKER_TIMEOUT — inutilizzabile.**
- **Asincrono** (`EVWSASYNC`): restituisce UUID, poi polling su `batch/status/{uuid}` e `batch/response/{uuid}`

---

## 3. Come creare API in scrittura

### Scrittura tabellare (anagrafiche, articoli)
```json
{
  "CodiceWS": "500027",
  "Schema": "1",
  "Versione": "20250006",
  "Operazione": "update",
  "Ditta": "49",
  "TabellaCampi": [
    {
      "M-CODMAG": "ART001",
      "M-DESCRIZIONE": "Articolo nuovo",
      "M-DESCRAGG": "Descrizione aggiuntiva"
    }
  ]
}
```

### Scrittura testata-corpo (documenti, ordini)
```json
{
  "CodiceWS": "500011",
  "Schema": "1",
  "Versione": "20250006",
  "Operazione": "update",
  "Ditta": "49",
  "TabellaCampi": [
    {
      "Testata": {
        "B-TIPO": "3",
        "B-CODCLI": "100",
        "B-DATABOLLA2": "20260315",
        "B-DEP": "1"
      },
      "Corpo": [
        {
          "B-CODMAG4": "ART001",
          "B-QUANTITA": "10",
          "B-IVA": "22",
          "B-PREZZO": "15.50",
          "B-IMPORTO": "155"
        }
      ]
    }
  ]
}
```

### Parametri importanti per scrittura in CONFWS

**Anagrafiche**: aggiornamento automatico/non aggiorna, associazione (per P.IVA, per codice, per email)

**Articoli**: creazione inesistente si/no, aggiornamento tutto/solo prezzi, codici a barre auto

**Documenti/Ordini**: numerazione auto/da tracciato, documenti esistenti non aggiorna/aggiorna/accoda, eccezioni (fatture SDI, bolle fatturate, ordini evasi)

### Vista vs Tabellare
- **Tabellare**: singola tabella, validazione minima
- **Vista**: alto livello, validazione automatica, dati relazionati. **Consigliato per Lamonea.**

---

## 4. Gestione File/Documenti

### La documentazione NON copre
- Download/upload di PDF fatture
- Gestione allegati ai documenti
- Accesso al DMS (Document Management System)
- Download di fatture elettroniche XML/P7M dallo SDI

### Cosa sappiamo
- I tag SDI della fattura elettronica sono gestibili tramite il ramo "Dati fat. elet." in CONFWS
- Questo e il punto **piu critico** da chiarire nella call

### Possibilita da esplorare
- Modulo DMS separato con API proprie
- File XML FE accessibili via file system
- Servizio specifico non documentato nel manuale MATRIX
- Accesso ODBC diretto (in dismissione)

---

## 5. Risultati Test API Live (2026-03-09)

### Ambiente confermato
| Parametro | Valore |
|-----------|--------|
| URL | `https://lamonea.teamsystem.io` |
| Token | `PGAUTH-1465308c...` (utente: `commerciale2`) |
| Scadenza token | 2027/02/06 |
| SSL | Certificato valido Amazon RSA |
| Protocollo | HTTP/2 su TLS 1.3 |

### Risultati per endpoint

| Test | Risultato |
|------|-----------|
| **Sincrono (EVWSSYNC)** | SEMPRE `WORKER_TIMEOUT` — inutilizzabile |
| **Asincrono (EVWSASYNC)** | Funzionante |
| **WS 500001 Clienti (ditta 49)** | OK — **3.168** clienti |
| **WS 500001 Clienti (ditta 133)** | OK — **246** clienti |
| **WS 500001 Clienti (ditta 212)** | OK — **249** clienti |
| **WS 500001 Fornitori (ditta 49)** | OK — **1.840** fornitori |
| **WS 500001 Fornitori (ditta 133)** | OK — **322** fornitori |
| **WS 500001 Fornitori (ditta 212)** | OK — **111** fornitori |
| **WS 500027 Articoli (tutte le ditte)** | `ID_CODE_ERR` — **NON configurato in CONFWS** |
| **WS 500009 Ordini (tutte le ditte)** | `ID_CODE_ERR` — **NON configurato in CONFWS** |
| **WS 500011 Documenti (tutte le ditte)** | `ID_CODE_ERR` — **NON configurato in CONFWS** |
| **WS 500020 Movimenti (tutte le ditte)** | `ID_CODE_ERR` — **NON configurato in CONFWS** |
| **CodiceWS 1 Tabelle** | `ERR_PARAM_REQUEST` — formato request errato |
| **Variazioni (WS 500001)** | `ERR_PARAM_REQUEST` — da chiarire formato |

### Campi confermati nel WS 500001

| Campo TS | Descrizione |
|----------|-------------|
| `ANRASO\|100008\|` | Ragione Sociale |
| `ANPIVA\|100008\|` | Partita IVA |
| `ANCOFI\|100008\|` | Codice Fiscale |
| `CFCODPAG\|100094\|` | Codice Pagamento |
| `CF-TIPO` | 1=Cliente, 2=Fornitore |
| `CF-CODICE` | Codice numerico |
| `ANIND\|100008\|` | Indirizzo |
| `ANCAP\|100008\|` | CAP |
| `ANCITTA\|100008\|` | Citta |
| `ANPROV\|100008\|` | Provincia |
| `CF-PRLIST` | Listino |
| `CF-TIPOIVA` | Tipo IVA |
| `ANTELEFONO\|100008\|` | Telefono |
| `ANEMAIL\|100008\|` | Email |

### Scoperte chiave
1. **Il sincrono e rotto** — restituisce SEMPRE `WORKER_TIMEOUT`, da chiedere al tecnico
2. **WS 500001 funziona su tutte e 3 le ditte** — clienti e fornitori estratti con successo
3. **Articoli, ordini, documenti, movimenti**: confermato `ID_CODE_ERR` — **serve il tecnico TS per configurarli in CONFWS**
4. **L'async accetta tutto** — scheduling non implica WS configurato, errore appare solo nella response
5. **Batch job persistono a lungo** — i job della sessione precedente erano ancora disponibili dopo ~12 ore
6. **Content-Type obbligatorio** — tutte le chiamate API (anche GET senza body) richiedono `Content-Type: application/json`

---

## 6. Ricerca online — stato dell'arte

**Non esiste nessun esempio pubblico** di integrazione con i Web Service MATRIX di TeamSystem Lynfa Azienda (cercato su Google, GitHub, StackOverflow).

- TSE Cloud (prodotto diverso) ha docs pubbliche su `tse.docs.teamsystem.cloud`
- bindCommerce si integra con Lynfa ma non pubblica dettagli tecnici
- Nessun forum o community discussion sui WS MATRIX

**Implicazione**: siamo completamente dipendenti dalla documentazione PDF e dal supporto tecnico del consulente.

---

## 7. Domande per la call con il tecnico TS

### A. Problemi infrastrutturali
1. **WORKER_TIMEOUT sincrono**: `EVWSSYNC` restituisce SEMPRE timeout. Problema di configurazione? Sincrono non supportato su istanza SaaS?
2. **ACLAPG**: l'utente `commerciale2` ha visibilita completa su tutti i dati di tutte le ditte?

### B. Web Service NON configurati (PRIORITA MASSIMA)
3. **Articoli (500027), Ordini (500009), Documenti (500011), Movimenti (500020)**: restituiscono `ID_CODE_ERR`. Sono NON configurati in CONFWS? **Chi li deve configurare?**
4. **Tabelle di supporto (CodiceWS 1)**: restituisce `ERR_PARAM_REQUEST`. Quali parametri servono?
5. **Scadenze (EFFSCA)**: esiste un WS configurato?

### C. Clienti/Fornitori (funzionante)
6. **Multi-ditta**: WS 500001 attivo anche per ditte 133 e 212? Stessi codici anagrafica su tutte le ditte?
7. **Campi mancanti**: destinatari merce, annotazioni, PEC, codice SDI, fido — configurabili nella response?
8. **Listini**: quanti attivi? Come estrarre la tabella listini completa?

### D. Documenti e Ordini
9. **Tipi documento**: quali `B-TIPO` usa Lamonea?
10. **Ordini**: solo clienti (tipo=1) o anche fornitori? CodiceWS 500009 o 500028?
11. **Storico**: BOLSTO/ORDSTO accessibili con lo stesso WS?

### E. Scrittura
12. **Multi-ditta**: nuovo cliente/articolo va scritto su tutte e 3 le ditte?
13. **Codifica automatica**: TS assegna codici progressivi?
14. **Validazioni Vista**: cosa viene rifiutato in scrittura?
15. **Conflitti**: timestamp di ultima modifica nei record?

### F. File/Documenti (CRITICO)
16. **PDF Fatture**: come accedere ai PDF? API o file system?
17. **Fatture elettroniche XML**: dove salvati i file XML/P7M SDI?
18. **DMS**: TeamSystem ha DMS con API?
19. **Allegati**: possibile associare file a documenti via API?
20. **Schede tecniche**: certificati CE/MDR gestiti in TS?

### G. Sync e Operativita
21. **Variazioni**: conferma funzionamento, granularita (record intero o campo?)
22. **Rate limiting**: limite chiamate API?
23. **Webhook/Push**: notifiche push o solo polling?
24. **Ambiente test**: staging separato o produzione?

---

## 8. Riepilogo priorita

### Gia risolto
| Argomento | Risultato |
|-----------|-----------|
| URL + SSL | `https://lamonea.teamsystem.io`, SSL valido (Amazon RSA) |
| Token | Attivo, utente `commerciale2`, scade 2027/02/06 |
| WS 500001 **tutte le ditte** | d.49: 3.168 cli + 1.840 for / d.133: 246 cli + 322 for / d.212: 249 cli + 111 for |
| Sincrono vs Asincrono | Sincrono rotto (WORKER_TIMEOUT), usare SEMPRE async |
| Batch API | Funzionanti (Content-Type obbligatorio) |
| WS 500027/500009/500011/500020 | Confermato NON configurati (`ID_CODE_ERR`) — serve tecnico TS |

### Da risolvere nella call
| Priorita | Argomento | Domande |
|----------|-----------|---------|
| **P0** | Configurazione WS articoli/ordini/documenti/movimenti | #3 |
| **P0** | Accesso PDF fatture e XML FE | #16-17 |
| **P0** | WORKER_TIMEOUT sincrono | #1 |
| **P1** | WS 500001 per ditte 133 e 212 | #6 |
| **P1** | Tabelle di supporto | #4 |
| **P1** | Campi mancanti response clienti | #7 |
| **P1** | Strategia multi-ditta | #6, #12 |
| **P2** | Scrittura e codifica automatica | #12-15 |
| **P2** | Variazioni e sync incrementale | #21 |
| **P2** | DMS e allegati | #18-19 |
| **P2** | Rate limiting e ambiente test | #22-24 |

---

## 9. Script di test

Lo script `test_teamsystem_api.py` e stato creato in:
`/Users/simonebrigante/LAIF/Progetti/Lamonea/CollectionTeamSystem/DocumentazioneTS/test_teamsystem_api.py`

Testa sistematicamente tutti i WS su tutte le ditte via endpoint asincrono e produce un report dettagliato con risultati, errori, numero record e campi disponibili.
