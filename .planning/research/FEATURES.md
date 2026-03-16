# Feature Research

**Domain:** ER Diagram Editor with SQLAlchemy round-trip
**Researched:** 2026-03-16
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Visual table rendering (colonne, tipi, PK/FK indicators) | Every ER tool shows tables as rectangles with typed columns. pgModeler, DBeaver, dbdiagram.io all do this. Senza questo non e' un ER editor. | MEDIUM | JointJS shapes ER native (Entity) semplificano. Servono icone PK/FK, badge nullable/unique. |
| Relationship lines with cardinality | Linee tra tabelle con notazione crow's foot (1:1, 1:N, N:M). DBeaver usa solid/dashed per nullable FK. Standard visivo universale. | MEDIUM | JointJS ha link con markers. Servono custom markers crow's foot. |
| Drag & drop di tabelle sul canvas | Ogni tool permette di spostare tabelle. Pan e zoom sono il minimo per navigare diagrammi. | LOW | JointJS Paper ha pan/zoom built-in. |
| Zoom e pan del canvas | Navigazione base del diagramma. Tutti i tool lo hanno. | LOW | Wheel zoom + drag pan. JointJS supporta nativamente. |
| Import da sorgente esistente | dbdiagram.io importa SQL, DBeaver/DataGrip reverse-engineer da DB live, pgModeler importa da DB. Nel nostro caso: parsing di `model.py`. | HIGH | Core del progetto. libcst parsing di classi SQLAlchemy 2.0 Mapped[]. |
| Export/salvataggio verso sorgente | Round-trip: le modifiche visuali devono tradursi in codice. pgModeler genera DDL, MySQL Workbench fa forward engineering. Nel nostro caso: riscrittura model.py. | HIGH | libcst per preservare commenti e formattazione. Core value del progetto. |
| Aggiunta/rimozione tabelle | Operazione CRUD base. Tutti gli editor lo permettono. | MEDIUM | Creare nuova classe SQLAlchemy con struttura base. |
| Aggiunta/rimozione colonne | Operazione CRUD base. Tutti gli editor lo permettono. | MEDIUM | Aggiungere/rimuovere attributi Mapped[] dalla classe. |
| Editing proprieta' colonna (tipo, nullable, unique, index, default) | pgModeler e MySQL Workbench hanno form dettagliati per ogni colonna. Table stakes per un editor serio. | MEDIUM | Panel laterale o dialog con form per ogni proprieta'. |
| Creazione relazioni (FK + relationship) | Collegare tabelle visualmente per creare FK. pgModeler propaga colonne automaticamente. | HIGH | Deve creare sia la mapped_column FK che la relationship() su entrambi i lati. |
| Persistenza posizioni (layout state) | DBeaver salva layout nei suoi file .erd. Riaprire il diagramma deve mostrare le tabelle dove le hai lasciate. | LOW | File sidecar .er.json gia' previsto in PROJECT.md. |
| Undo/redo | ChartDB e tutti gli editor seri hanno undo/redo. Senza, ogni errore e' un disastro. | MEDIUM | Command pattern su stack di operazioni. |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Round-trip preservando commenti e formattazione | Nessun tool ER mainstream lavora su file ORM preservando il sorgente. dbdiagram.io genera SQL da zero, pgModeler genera DDL ex-novo. libcst permette editing byte-per-byte. Questo e' IL differenziatore. | HIGH | Gia' core del progetto. libcst e' la scelta giusta. |
| Lavora su file ORM (SQLAlchemy) anziche' SQL/DDL | Tutti i tool lavorano su SQL o su formato proprietario. Nessuno edita direttamente file Python ORM. Per team che usano SQLAlchemy, questo elimina il gap diagram-codice. | HIGH | Parser specifico per pattern Mapped[] / mapped_column(). |
| Raggruppamento visuale con colori | pgModeler ha "layers", ma la maggior parte dei tool non ha gruppi colorati. Per schemi con 10+ tabelle, i gruppi danno ordine cognitivo. | MEDIUM | JointJS embedding (group contiene tabelle). Colori + nomi custom. |
| Zero build step, portabilita' copia-e-incolla | Nessun tool competitor e' cosi' leggero. pgModeler richiede installazione Qt, dbdiagram.io e' SaaS, ChartDB richiede npm. `python server.py model.py` e basta. | LOW | Gia' constraint di progetto. Vanilla JS + CDN. |
| Sidecar file per metadati visuali (non inquina il sorgente) | Separare layout dal codice. Il model.py resta pulito, le posizioni vanno in .er.json. Versionabile opzionalmente. | LOW | Gia' previsto. JSON semplice. |
| Preview codice in tempo reale | Mostrare il codice Python che verra' generato mentre si edita il diagramma. Feedback loop immediato come dbdiagram.io (DBML -> diagram) ma invertito (diagram -> Python). | MEDIUM | Split panel con syntax highlighting (highlight.js da CDN). |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Generazione migrazioni Alembic | "Se modifico il modello, generami anche la migrazione" | Scope creep enorme. Le migrazioni richiedono contesto (dati esistenti, downgrade path, ordine). Mescolare editing visuale con migration generation crea rischio di data loss. | Il tool modifica model.py. L'utente genera la migrazione con `alembic revision --autogenerate` come workflow standard. |
| Supporto multi-file (import da piu' model.py) | "Il mio progetto ha modelli in file separati" | Complessita' di risoluzione import, base classes condivise, circular dependencies. v1 deve validare il concept su singolo file. | v1: singolo file. v2: eventuale supporto multi-file dopo validazione. |
| Supporto pattern legacy SQLAlchemy (Column(), declarative_base) | "Ho un progetto vecchio con Column()" | Raddoppia la complessita' del parser per un pattern in fase di deprecazione. I nuovi progetti LAIF usano tutti Mapped[]. | Solo Mapped[] / mapped_column(). Documentare che serve SQLAlchemy >= 2.0. |
| Collaborazione real-time | ChartDB e dbdiagram.io hanno editing collaborativo | Richiede backend con WebSocket, conflict resolution, autenticazione. Completamente fuori scope per un tool locale. | Tool single-user locale. Per condividere: versionare .er.json in git. |
| AI-powered schema generation | ChartDB e Eraser hanno AI per generare schemi | Dipendenza da API esterne, costi, complessita'. Il nostro utente ha gia' un modello, non ne genera uno da zero. | L'utente parte da model.py esistente. L'AI non serve. |
| Connessione diretta al database | DBeaver e DataGrip si connettono al DB live per reverse engineering | Il nostro tool lavora sul codice, non sul DB. Aggiungere connessioni DB porta dipendenze (driver), configurazione, e confonde lo scope. | Il sorgente di verita' e' model.py, non il DB. |
| Auto-layout automatico completo | dbdiagram.io ha auto-layout. Sembra comodo. | Per 5-10 tabelle il layout manuale e' migliore perche' riflette il modello mentale dello sviluppatore. L'auto-layout distrugge l'organizzazione semantica. | Opzionale "arrange" per primo import (suggerimento iniziale), poi l'utente organizza. Salvare in .er.json. |
| Export PNG/PDF del diagramma | pgModeler, DBeaver, DataGrip esportano immagini | Nice to have ma non core. Aggiunge complessita' (rendering SVG to raster). Non serve per il workflow primario. | v1: screenshot del browser. v2: eventuale export SVG (JointJS lo supporta nativamente). |

## Feature Dependencies

```
[Import model.py (parser libcst)]
    |
    +--requires--> [Rendering tabelle sul canvas]
    |                  |
    |                  +--requires--> [Rendering relazioni (linee)]
    |                  |
    |                  +--enables--> [Drag & drop tabelle]
    |                  |
    |                  +--enables--> [Zoom & pan]
    |
    +--enables--> [Editing colonne (CRUD)]
    |                  |
    |                  +--enables--> [Editing proprieta' colonna]
    |
    +--enables--> [Editing tabelle (CRUD)]
    |
    +--enables--> [Creazione relazioni]
    |
    +--feeds--> [Export model.py (writer libcst)]
                    |
                    +--requires--> [Tutte le operazioni di editing sopra]

[Persistenza posizioni (.er.json)]
    +--independent-- (puo' essere sviluppato in parallelo)

[Raggruppamento visuale]
    +--requires--> [Rendering tabelle]
    +--requires--> [Persistenza posizioni]

[Undo/redo]
    +--requires--> [Tutte le operazioni di editing]

[Preview codice real-time]
    +--requires--> [Export model.py (writer libcst)]
```

### Dependency Notes

- **Rendering tabelle requires Parser**: senza parsing del model.py non c'e' nulla da visualizzare
- **Editing requires sia Parser che Renderer**: l'utente edita sul canvas, i cambiamenti devono propagarsi al modello interno
- **Writer requires tutte le operazioni di editing**: il writer deve serializzare qualsiasi modifica fatta
- **Raggruppamento requires Persistenza**: i gruppi sono metadati visuali salvati in .er.json
- **Preview codice requires Writer**: deve invocare il writer per mostrare l'output in tempo reale

## MVP Definition

### Launch With (v1)

Minimum viable product -- validare che il round-trip SQLAlchemy funziona.

- [ ] Parser model.py (libcst) -- senza questo nulla funziona
- [ ] Rendering tabelle con colonne e tipi -- visualizzazione base
- [ ] Rendering relazioni con linee -- mostrare FK e relationships
- [ ] Drag & drop, pan, zoom -- navigazione minima
- [ ] Editing tabelle: aggiungere/rimuovere -- CRUD base
- [ ] Editing colonne: aggiungere/rimuovere/rinominare/modificare proprieta' -- CRUD base
- [ ] Creazione relazioni (FK + relationship) -- collegare tabelle
- [ ] Writer model.py con preservazione commenti -- il core value
- [ ] Persistenza posizioni in .er.json -- riaprire senza perdere il layout
- [ ] Server locale (`python server.py model.py`) -- portabilita'

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] Undo/redo -- dopo che il CRUD funziona, aggiungere command stack
- [ ] Raggruppamento visuale con colori -- per schemi con 10+ tabelle
- [ ] Preview codice in tempo reale -- split panel con output Python
- [ ] Export SVG del diagramma -- JointJS lo supporta, poco effort extra
- [ ] Layout suggerito per primo import -- auto-arrange iniziale

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] Supporto multi-file -- richiede risoluzione import Python
- [ ] Editing Pydantic schema (gia' in Out of Scope di PROJECT.md)
- [ ] Diff visuale tra versioni del modello -- confronto .er.json in git
- [ ] Minimap per navigazione diagrammi grandi
- [ ] Keyboard shortcuts avanzati (vim-like)

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Parser model.py | HIGH | HIGH | P1 |
| Rendering tabelle | HIGH | MEDIUM | P1 |
| Rendering relazioni | HIGH | MEDIUM | P1 |
| Drag & drop, pan, zoom | HIGH | LOW | P1 |
| Editing tabelle CRUD | HIGH | MEDIUM | P1 |
| Editing colonne CRUD | HIGH | MEDIUM | P1 |
| Creazione relazioni | HIGH | HIGH | P1 |
| Writer model.py preservante | HIGH | HIGH | P1 |
| Persistenza .er.json | MEDIUM | LOW | P1 |
| Server locale | MEDIUM | LOW | P1 |
| Undo/redo | MEDIUM | MEDIUM | P2 |
| Raggruppamento visuale | MEDIUM | MEDIUM | P2 |
| Preview codice real-time | MEDIUM | MEDIUM | P2 |
| Export SVG | LOW | LOW | P2 |
| Auto-arrange iniziale | LOW | MEDIUM | P2 |
| Multi-file support | MEDIUM | HIGH | P3 |
| Diff visuale | LOW | HIGH | P3 |
| Minimap | LOW | MEDIUM | P3 |

## Competitor Feature Analysis

| Feature | dbdiagram.io | pgModeler | DBeaver ERD | MySQL Workbench | DataGrip | ChartDB | **ER Editor (nostro)** |
|---------|-------------|-----------|-------------|-----------------|----------|---------|----------------------|
| Input format | DBML (DSL) | Formato proprietario | DB live | DB live / SQL | DB live | SQL query | **model.py SQLAlchemy** |
| Output format | SQL DDL | SQL DDL | SQL script | SQL DDL | -- | SQL DDL (AI) | **model.py preservato** |
| Round-trip | NO (genera da zero) | Parziale (sync DB) | Parziale (edit mode) | SI (forward/reverse) | NO (read-only) | NO | **SI (byte-per-byte)** |
| Preserva sorgente | NO | NO | N/A | NO | N/A | NO | **SI (commenti, formatting)** |
| Lavora su ORM | NO | NO | NO | NO | NO | NO | **SI (SQLAlchemy 2.0)** |
| Installazione | SaaS (browser) | Desktop (Qt) | Desktop (Java) | Desktop (C++) | Desktop (Java) | npm / Docker | **`pip install` + run** |
| Costo | Free/9$/mo | $40 una tantum | Free (Community) | Free | $229/anno | Free (OSS) | **Free (interno)** |
| Gruppi/layer | NO | SI (layers) | NO | SI (diagram tabs) | NO | NO | **SI (gruppi colorati)** |
| Undo/redo | SI | SI | SI | SI | NO | SI | **v1.x** |
| Auto-layout | SI | SI | SI | SI | SI | SI | **v1.x (opzionale)** |
| Collaborazione | SI (paid) | NO | NO | NO | NO | SI | **NO (tool locale)** |

## Sources

- [dbdiagram.io](https://dbdiagram.io/) -- DSL-first ER editor, reference per UX code-to-diagram
- [pgModeler](https://pgmodeler.io/) -- Desktop ER modeler per PostgreSQL, reference per feature set completo
- [DBeaver ERD docs](https://dbeaver.com/docs/dbeaver/ER-Diagrams/) -- ERD integrato in database IDE
- [MySQL Workbench forward/reverse engineering](https://dev.mysql.com/doc/workbench/en/wb-design-engineering.html) -- Reference per round-trip DB
- [DataGrip diagrams](https://www.jetbrains.com/help/datagrip/creating-diagrams.html) -- ERD in JetBrains IDE
- [ChartDB](https://github.com/chartdb/chartdb) -- OSS diagram editor con AI export
- [Top ER tools comparison (Holistics)](https://www.holistics.io/blog/top-5-free-database-diagram-design-tools/) -- Panoramica comparativa
- [ER tool trends 2025 (Liam ERD)](https://liambx.com/blog/er-diagram-tool-trends-2025) -- Trend del settore

---
*Feature research for: ER Diagram Editor with SQLAlchemy round-trip*
*Researched: 2026-03-16*
