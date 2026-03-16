# Backend Upload

| Campo     | Valore              |
|-----------|---------------------|
| ID        | 134                 |
| Stack     | laif-template       |
| Tipo      | Proposal            |
| Status    | Nuova               |
| Priorita  | —                   |
| Parent    | 133 (Miglioramenti Media Service) |

## Descrizione originale

Backend upload — sotto-item dei miglioramenti al Media Service.

## Piano di risoluzione

1. **Migliorare l'endpoint di file upload** — Implementare chunked upload per file di grandi dimensioni:
   - Endpoint per iniziare un upload multipart (restituisce upload ID)
   - Endpoint per caricare singoli chunk (con numero di sequenza)
   - Endpoint per completare l'upload (assembla i chunk)
   - Gestione timeout e retry per chunk singoli
   - Limite dimensione chunk configurabile (es. 5MB)

2. **Validazione tipo file (approccio whitelist)** — Sicurezza lato server:
   - Verificare il MIME type reale del file (non fidarsi dell'header `Content-Type`)
   - Usare `python-magic` per detection basata su magic bytes
   - Whitelist per contesto: immagini profilo (jpg, png, webp), documenti (pdf, docx, xlsx), allegati generici
   - Rifiutare eseguibili e file potenzialmente pericolosi

3. **Integrazione virus scanning (opzionale)** — Per ambienti che lo richiedono:
   - ClamAV come sidecar container o servizio separato
   - Scan asincrono: file in quarantena fino a scan completato
   - Alternativa AWS: S3 Object Lambda con scanning

4. **Upload diretto su S3 per file grandi** — Per file sopra una soglia (es. 10MB):
   - Generare pre-signed URL per upload diretto dal frontend a S3
   - Il backend genera l'URL, il frontend carica direttamente
   - Callback o polling per confermare il completamento
   - Evita di far passare file grandi attraverso il backend

5. **API di tracking progresso** — Per dare feedback al frontend:
   - Endpoint per verificare lo stato di un upload in corso
   - Percentuale di completamento (basata su chunk ricevuti)
   - Integrazione con i media service hooks (issue 135)

## Stima effort

**12-16 ore**:
- Chunked upload endpoint (~4h)
- Validazione tipo file (~3h)
- Upload diretto S3 (~4h)
- Progress tracking API (~2h)
- Test e documentazione (~2h)
