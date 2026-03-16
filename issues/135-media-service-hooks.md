# Media Service Hooks

| Campo     | Valore              |
|-----------|---------------------|
| ID        | 135                 |
| Stack     | laif-template       |
| Tipo      | Proposal            |
| Status    | Nuova               |
| Priorita  | —                   |
| Parent    | 133 (Miglioramenti Media Service) |

## Descrizione originale

Media service hooks — sotto-item dei miglioramenti al Media Service.

## Piano di risoluzione

1. **Creare hook React per il media service** — Set di hook riutilizzabili:
   - `useUpload()` — gestisce l'upload di uno o piu file, espone stato e progresso
   - `useMedia(mediaId)` — recupera metadati e URL di un media
   - `usePreview(mediaId)` — genera/recupera URL di anteprima
   - `useMediaList(filters)` — lista media con paginazione e filtri

2. **Gestione stato upload** — Ogni upload deve esporre:
   - `isLoading` — upload in corso
   - `progress` — percentuale di completamento (0-100)
   - `error` — errore se presente (tipo file non valido, dimensione eccessiva, errore di rete)
   - `isSuccess` — upload completato con successo
   - `data` — metadata del file caricato (URL, dimensione, tipo)
   - `cancel()` — funzione per annullare un upload in corso

3. **Integrazione con componenti laif-ds** — Gli hook devono funzionare con:
   - Componente file upload della design system
   - Drag & drop area
   - Image preview component
   - Correlazione con issue 154 (visual feedback upload in DS)

4. **Strategia di cache e invalidazione** — Per performance:
   - Cache delle URL media con React Query (TanStack Query)
   - Invalidazione automatica dopo upload/delete
   - Prefetch per media probabilmente necessari (es. lista allegati)
   - Stale-while-revalidate per anteprime

5. **Supporto upload multiplo** — Gestione upload di piu file contemporaneamente:
   - Queue di upload con limite di concorrenza (es. max 3 simultanei)
   - Stato aggregato (totale file, file completati, file in errore)
   - Possibilita di rimuovere file dalla coda
   - Retry automatico per errori transitori (errori di rete)

## Stima effort

**12-16 ore**:
- Hook useUpload con stato e progresso (~4h)
- Hook useMedia e usePreview (~3h)
- Integrazione con laif-ds (~3h)
- Cache e invalidazione (~2h)
- Upload multiplo e queue (~3h)
- Test e documentazione (~2h)
