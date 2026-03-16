# Tipizzare la search (e tutto il CRUD service)

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 86                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Da iniziare        |
| Priorita  | —                  |
| Effort    | 8h                 |
| Tag       | Breaking, Filone CRUD Service |

## Descrizione originale

> Tipizzare la search (e tutto il crud service)

## Piano di risoluzione

1. **Audit del CRUD service attuale**
   - Mappare tutte le funzioni del CRUD service (create, read, update, delete, search)
   - Identificare i parametri di search non tipizzati (filtri, ordinamento, paginazione)
   - Catalogare i punti dove si usano `dict`, `Any` o parametri generici senza tipo

2. **Definire interfacce tipizzate per i filtri di ricerca (backend)**
   - Creare modelli Pydantic per i parametri di search: `SearchFilter`, `SearchOperator`, `SearchRequest`
   - Ogni filtro deve avere: nome campo (tipizzato sull'entità), operatore (enum), valore (tipizzato)
   - Operatori supportati: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `like`, `in`, `is_null`
   - Validazione automatica: i campi passati devono corrispondere allo schema dell'entità

3. **Aggiungere generics al CRUD service**
   - Rendere il CRUD service generico su `ModelType`, `CreateSchemaType`, `UpdateSchemaType`
   - I metodi di search devono accettare solo filtri validi per l'entità specifica
   - Usare `TypeVar` e `Generic` di Python per propagare i tipi

4. **Tipizzare i parametri di search end-to-end**
   - Campo: solo nomi di colonne validi per l'entità (derivati dal modello SQLAlchemy)
   - Operatore: enum con tutti gli operatori supportati
   - Valore: tipo coerente con il campo selezionato
   - Ordinamento: campo + direzione (`asc`/`desc`), tipizzato

5. **Generare il client OpenAPI per propagare i tipi al frontend**
   - Eseguire `just fe generate-client` dopo le modifiche backend
   - Verificare che le interfacce TypeScript generate riflettano i tipi Pydantic
   - Creare interfacce TS di supporto se il generatore non copre tutti i casi

6. **Gestire la breaking change**
   - Documentare tutte le modifiche alle API nella sezione changelog del template
   - Scrivere una guida di migrazione per i progetti esistenti (Jubatus, People, Nivi, ecc.)
   - Valutare se introdurre un periodo di compatibilità con i vecchi parametri non tipizzati
   - Comunicare la breaking change al team

7. **Aggiungere validazione schema-aware**
   - Validare a runtime che i campi di ricerca esistano nello schema dell'entità
   - Restituire errori chiari se un campo non esiste o l'operatore non è compatibile col tipo
   - Aggiungere test unitari per i casi di errore

## Stima effort

- Audit CRUD service attuale: ~1h
- Modelli Pydantic per search: ~2h
- Generics al CRUD service: ~1.5h
- Tipizzazione parametri e validazione: ~1.5h
- Generazione client e verifica frontend: ~0.5h
- Guida migrazione e gestione breaking change: ~1h
- Test: ~0.5h
- **Totale: ~8h**
