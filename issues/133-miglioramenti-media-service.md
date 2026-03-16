# Miglioramenti Media Service

| Campo     | Valore              |
|-----------|---------------------|
| ID        | 133                 |
| Stack     | laif-template       |
| Tipo      | Proposal            |
| Status    | In corso            |
| Priorita  | —                   |
| Tag       | Filone Gestione File|

## Descrizione originale

Miglioramenti Media Service — issue ombrello.

### Sotto-issue

- **ID 134** — Backend upload
- **ID 135** — Media service hooks

## Piano di risoluzione

Questa e una issue ombrello. Il lavoro e gia in corso e si articola nei seguenti step:

1. **Migliorare la gestione upload backend (issue 134)** — Rendere l'upload piu robusto e scalabile:
   - Supporto chunked upload per file di grandi dimensioni
   - Validazione tipo file lato server
   - Upload diretto su S3 per file grandi
   - Vedi dettagli in `issues/134-backend-upload.md`

2. **Creare hook React per il media service (issue 135)** — Fornire al frontend un'interfaccia pulita:
   - Hook `useUpload`, `useMedia`, `usePreview`
   - Gestione stato (loading, progress, error, success)
   - Integrazione con componenti laif-ds
   - Vedi dettagli in `issues/135-media-service-hooks.md`

3. **Migliorare la validazione dei tipi di file** — Approccio whitelist:
   - Definire lista di tipi MIME accettati per contesto (immagini profilo, documenti, allegati)
   - Validazione sia frontend che backend
   - Messaggio di errore chiaro per tipi non supportati

4. **Supporto preview per tipi file comuni** — Generare anteprime:
   - Immagini: thumbnail automatico
   - PDF: prima pagina come immagine
   - Documenti Office: icona per tipo
   - Video: frame di anteprima (opzionale, piu complesso)

5. **Correlazione con issue 154 (visual feedback upload in DS)** — Il feedback visuale durante l'upload nella design system e correlato. Coordinare le modifiche per garantire coerenza tra media service e componenti DS.

### Sotto-issue correlate

- Issue 134: Backend upload
- Issue 135: Media service hooks
- Issue 154: Visual feedback file uploads (DS)

## Stima effort

**Effort totale stimato: 24-32 ore** (somma delle sotto-issue):
- Backend upload (issue 134): ~12-16h
- Media service hooks (issue 135): ~12-16h
- Le sotto-issue possono procedere in parallelo
