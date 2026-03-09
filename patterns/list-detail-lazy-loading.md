---
titolo: "List-Detail Lazy Loading"
categoria: "performance"
complessità: "media"
usato-in: [jubatus]
data-creazione: "2026-03-09"
ultimo-aggiornamento: "2026-03-09"
tags:
  - "#pattern:performance"
  - "#stack:react"
  - "#stack:fastapi"
---

# Pattern: List-Detail Lazy Loading

## Problema

Hai una UI lista/dettaglio dove ogni elemento ha dati pesanti (body HTML, file, relazioni profonde) ma la lista deve restare veloce. Caricare tutto nella lista è uno spreco: l'utente vede un elemento alla volta.

**Segnali che questo pattern è quello giusto**:
- La lista carica 50+ elementi ma mostra solo titolo/metadata
- Il dettaglio include campi pesanti (HTML body, allegati, relazioni N+1)
- L'endpoint della lista è lento perché eager-load troppi dati
- Vuoi che la lista risponda in <200ms anche con molti elementi

---

## Soluzione

Separare in due livelli: **lista leggera** (solo metadata) + **dettaglio completo** (on-demand quando l'utente seleziona).

### Struttura

```
Backend:
  ListResponse     → campi leggeri (id, title, date, status, sender)
  DetailResponse   → campi completi (body_html, body_text, recipients, attachments)

  POST /items/search  → ListResponse[]     (lista)
  GET  /items/{id}    → DetailResponse      (dettaglio singolo)

Frontend:
  useItemsList()    → chiama POST /search, mappa a tipo leggero
  useItemDetail(id) → chiama GET /{id}, enabled solo quando id != null
  enrichedData      → useMemo che merge dettaglio nel tipo lista
```

### Implementazione

**Passo 1**: Backend — Definire due response schema separati

```python
# Schema leggero per la lista
class ItemListResponse(BaseModel):
    id: int
    title: str
    date: datetime
    status: str

# Schema completo per il dettaglio
class ItemDetailResponse(BaseModel):
    id: int
    title: str
    date: datetime
    status: str
    body_html: str | None
    body_text: str | None
    recipients: list[RecipientResponse]
    attachments: list[AttachmentResponse]
```

**Passo 2**: Backend — Endpoint dettaglio con eager loading

```python
@router.get("/items/{item_id}", response_model=ItemDetailResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Item)
        .where(Item.id == item_id)
        .options(
            joinedload(Item.recipients),
            joinedload(Item.attachments),
        )
    )
    result = db.execute(stmt)
    return result.unique().scalar_one_or_none()  # .unique() obbligatorio con joinedload
```

**Passo 3**: Frontend — Hook dettaglio con `enabled` condizionale

```typescript
export function useItemDetail(itemId: number | null) {
  return useQuery({
    queryKey: ["item-detail", itemId],
    queryFn: async () => {
      const response = await getItemById({ path: { item_id: itemId! } });
      return response.data;
    },
    enabled: itemId !== null,  // fetch solo quando serve
  });
}
```

**Passo 4**: Frontend — Merge dettaglio nella vista con `useMemo`

```typescript
const { data: detail, isLoading } = useItemDetail(selectedItem?.id ?? null);

const enrichedData = useMemo(() => {
  if (!selectedItem) return null;
  if (!detail) return selectedItem;  // fallback sui dati lista
  return mapDetailToViewModel(detail, selectedItem.id);
}, [detail, selectedItem]);
```

### Codice di riferimento

Il mapping da DTO backend a tipo frontend va estratto in una utility condivisa per evitare duplicazione tra viste diverse (vedi sezione "Quando NON usare"):

```typescript
// utils/mapItemDetail.ts
export function mapDetailToViewModel(detail: ItemDetailResponse, parentId: number): ItemViewModel {
  return {
    id: detail.id,
    parentId,
    content: detail.body_html ?? detail.body_text ?? "",
    // ... mapping completo
  };
}
```

---

## Trade-off

**Vantaggi**:
- Lista veloce: nessun eager loading pesante sulla query di lista
- Dettaglio completo: carica tutto solo quando serve
- Cache TanStack Query: il dettaglio resta in cache, riselezionare è istantaneo
- Fallback naturale: mostra dati lista mentre il dettaglio carica

**Svantaggi / costi**:
- Due endpoint da mantenere (lista + dettaglio)
- Breve flash di contenuto leggero prima che il dettaglio carichi
- Se l'utente naviga rapidamente tra elementi, genera molte chiamate API

**Quando NON usare questo pattern**:
- La lista ha pochi elementi (<20) e i dati non sono pesanti → carica tutto nella lista
- L'utente deve vedere il dettaglio di TUTTI gli elementi contemporaneamente (es. tabella con colonne espandibili)
- I dati pesanti servono anche per filtrare/cercare nella lista

---

## Varianti

### Variante: Prefetch on hover

Avviare il fetch del dettaglio quando l'utente passa il mouse sull'elemento della lista (prima del click). Riduce il tempo percepito.

```typescript
const prefetch = useQueryClient();
const handleHover = (id: number) => {
  prefetch.prefetchQuery({
    queryKey: ["item-detail", id],
    queryFn: () => fetchItemDetail(id),
    staleTime: 30_000,
  });
};
```

### Variante: Dettaglio inline nella lista

Invece di un pannello separato, espandere l'elemento della lista per mostrare il dettaglio. Il pattern resta identico (fetch on-demand), cambia solo la UI.

---

## Esempi reali in LAIF

| Progetto | Come è stato usato | Note / deviazioni |
|---------|-------------------|------------------|
| Jubatus | Email threads: `POST /email/threads/search` (lista) + `GET /email/threads/{id}` (dettaglio con body HTML, recipients, attachments) | Mapping duplicato in 2 viste — da estrarre in utility condivisa |

---

## Risorse esterne

- [TanStack Query — Dependent Queries](https://tanstack.com/query/latest/docs/framework/react/guides/dependent-queries)
- [SQLAlchemy — joinedload + unique()](sqlalchemy-joinedload-unique.md) (pattern correlato)
