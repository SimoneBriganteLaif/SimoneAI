---
progetto: "sebi-group"
data: "2026-03-18"
tipo: "Backlog evolutive"
tags:
  - "#progetto:sebi-group"
  - "#fase:presales"
---

# Evolutive Backlog — SEBI Group

> Funzionalità discusse durante la fase di analisi, rimandate a moduli futuri.
> Non incluse nel mockup attuale (scope: solo ciclo sales).

---

## 1. Feedback AI automatico su correzione categorizzazione

**Descrizione**: Quando un operatore corregge manualmente una categorizzazione AI (es. cambia "Export" in "Import"), il sistema usa questa correzione come feedback per migliorare le categorizzazioni future.

**Priorità**: Alta — richiesta esplicita da Simone. È il meccanismo base per rendere l'AI sempre più precisa nel tempo.

**Versione mockup**: Nel mockup i tag AI sono editabili dall'operatore, ma senza feedback loop visibile. Il feedback avviene in background.

**Note implementazione**: Richiede logging delle correzioni + pipeline di retraining/fine-tuning periodico.

---

## 2. Urgenza AI-driven

**Descrizione**: Categorizzazione automatica dell'urgenza basata su keyword, deadline menzionate, tono dell'email, storico cliente.

**Priorità**: Media — al momento l'urgenza è troppo soggettiva per affidarla all'AI. Nella v1 resta manuale.

**Versione mockup**: Urgenza è un badge impostato manualmente dall'operatore.

**Note implementazione**: Richiede training specifico su email reali di SEBI per capire cosa è "urgente" nel loro contesto. Potrebbe essere un buon candidato per feedback loop (punto 1).

---

## 3. Invio automatico email per info mancanti

**Descrizione**: Quando l'AI rileva dati mancanti in una richiesta, il sistema invia automaticamente un'email al cliente per richiedere le informazioni, senza intervento dell'operatore.

**Priorità**: Media — utile per velocizzare il ciclo, ma richiede alta fiducia nell'AI.

**Versione mockup**: Nel mockup c'è il bottone manuale "Richiedi info mancanti" che l'operatore clicca. L'automazione completa è l'evolutiva.

**Note implementazione**: Richiede soglia di confidence configurabile per decidere quando inviare automaticamente vs chiedere conferma all'operatore.

---

## 4. Gestione operativa post-conferma

**Descrizione**: Modulo separato per la gestione delle operazioni dopo che una quotazione è stata confermata dal cliente (booking, tracking, documentazione, fatturazione).

**Priorità**: Alta — ma è un modulo completamente separato dal ciclo sales.

**Versione mockup**: Fuori scope. Il mockup si ferma a "Confermata/Rifiutata".

**Note implementazione**: Da definire in una fase successiva con il team operativo. Probabile integrazione più profonda con l'ERP.

---

## 5. Assegnazione automatica operatori

**Descrizione**: Il sistema assegna automaticamente le email/pratiche agli operatori basandosi su criteri configurabili (area geografica, tipo trasporto, carico di lavoro, competenze).

**Priorità**: Bassa — il cliente attualmente non ne sente il bisogno. Gli operatori preferiscono scegliere autonomamente cosa prendere in carico.

**Versione mockup**: Non presente. L'operatore filtra e prende in carico manualmente.

**Note implementazione**: Se implementata, richiede pannello admin per configurare i criteri di assegnazione + override manuale sempre disponibile.

---

## 6. Riconoscimento avanzato thread email senza codice nell'oggetto

**Descrizione**: Capacità dell'AI di associare email a pratiche esistenti anche quando il codice pratica non è presente nell'oggetto (es. analizzando contenuto, mittente, contesto, allegati).

**Priorità**: Media — il codice nell'oggetto copre la maggior parte dei casi, ma ci sono situazioni (email da nuovi indirizzi del cliente, forward senza oggetto originale) dove serve un matching più intelligente.

**Versione mockup**: Solo matching per codice nell'oggetto. Le email senza codice vengono trattate come nuove.

**Note implementazione**: ML su contenuto + mittente + grafo relazioni per suggerire associazione. Potrebbe essere un "suggerimento" con conferma operatore.

---

## 7. Integrazione WebCargo

**Descrizione**: Integrazione con la piattaforma WebCargo per ottenere tariffe aeree in tempo reale, riducendo la necessità di inviare RDO manuali per il trasporto aereo.

**Priorità**: Media — da valutare costi API e copertura tratte.

**Versione mockup**: Non presente.

---

## 8. Documenti doganali

**Descrizione**: Modulo per la gestione dei documenti doganali (fatture commerciali, packing list, certificati di origine, BL, AWB, ecc.) con validazione automatica completezza.

**Priorità**: Bassa — fuori scope sales, più rilevante per il modulo operativo.

---

## 9. App mobile/tablet

**Descrizione**: Versione responsive o app nativa per accesso da dispositivi mobili.

**Priorità**: Bassa — gli operatori lavorano quasi esclusivamente da desktop.
