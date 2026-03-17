# Requirements: ER Editor

**Defined:** 2026-03-16
**Core Value:** L'editing visuale del datamodel deve tradursi fedelmente in modifiche al model.py, preservando commenti, formattazione e struttura del file originale.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Parsing

- [x] **PARS-01**: User can load a SQLAlchemy 2.0 model.py file and see all tables extracted
- [x] **PARS-02**: Parser extracts columns with all properties (type, nullable, unique, index, PK, FK, default)
- [x] **PARS-03**: Parser extracts relationships with properties (target, back_populates, cascade, lazy, uselist)
- [x] **PARS-04**: App starts with `python server.py /path/to/model.py` and opens the browser

### Visualization

- [x] **VIS-01**: Tables render as boxes with header (table name) and typed column list with PK/FK/nullable/unique/index indicators
- [x] **VIS-02**: Relationship lines show between tables with crow's foot cardinality markers (1:1, 1:N, N:M)
- [x] **VIS-03**: User can drag tables freely on the canvas
- [x] **VIS-04**: User can pan and zoom the canvas with mouse/trackpad

### Editing

- [x] **EDIT-01**: User can add a new table with name and tablename
- [x] **EDIT-02**: User can rename an existing table (class name + tablename)
- [x] **EDIT-03**: User can delete a table (with confirmation)
- [ ] **EDIT-04**: User can add a column to a table with type selection
- [ ] **EDIT-05**: User can rename a column
- [ ] **EDIT-06**: User can delete a column (with confirmation)
- [ ] **EDIT-07**: User can modify column properties (type, nullable, unique, index, PK, default)

### Relationships

- [ ] **REL-01**: User can create a relationship between two tables (generates FK column + relationship on both sides)
- [ ] **REL-02**: User can modify relationship properties (back_populates, cascade, lazy)
- [ ] **REL-03**: User can delete a relationship (removes FK + relationship from both sides)

### Persistence

- [ ] **PERS-01**: Saving writes changes back to model.py preserving comments, whitespace and formatting
- [x] **PERS-02**: Table positions and groups are saved in a sidecar .er.json file
- [x] **PERS-03**: Reopening a model.py with an existing .er.json restores positions and groups

### UX

- [x] **UX-01**: User can create named, colored groups and drag tables into/out of them
- [ ] **UX-02**: Undo/redo for all editing operations (Ctrl+Z / Ctrl+Shift+Z)
- [x] **UX-03**: Auto-layout algorithm places tables when no .er.json exists
- [ ] **UX-04**: Real-time Python code preview panel showing the current model.py output

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Multi-file

- **MULTI-01**: Support importing multiple model.py files with cross-file relationships
- **MULTI-02**: Resolve Python imports to understand shared base classes

### Pydantic

- **PYD-01**: Parse and display Pydantic schema classes paired with ORM models
- **PYD-02**: Edit Pydantic schemas alongside ORM models

### Advanced

- **ADV-01**: Visual diff between model versions (comparing .er.json snapshots)
- **ADV-02**: Minimap for navigating large diagrams
- **ADV-03**: Keyboard shortcuts (vim-like navigation)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Generazione migrazioni Alembic | Scope creep. Richiede contesto dati, downgrade path. L'utente usa `alembic revision --autogenerate` |
| Pattern legacy SQLAlchemy (Column()) | Raddoppia complessita' parser per pattern deprecato. Solo Mapped[] |
| Connessione diretta al database | Il sorgente di verita' e' model.py, non il DB |
| Collaborazione real-time | Tool single-user locale. WebSocket + conflict resolution fuori scope |
| AI-powered schema generation | L'utente parte da model.py esistente, non genera da zero |
| Export PNG/PDF | v1: screenshot browser. v2: export SVG nativo JointJS |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| PARS-01 | Phase 1 | Complete |
| PARS-02 | Phase 1 | Complete |
| PARS-03 | Phase 1 | Complete |
| PARS-04 | Phase 1 | Complete |
| VIS-01 | Phase 1 | Complete |
| VIS-02 | Phase 1 | Complete |
| VIS-03 | Phase 1 | Complete |
| VIS-04 | Phase 1 | Complete |
| EDIT-01 | Phase 2 | Complete |
| EDIT-02 | Phase 2 | Complete |
| EDIT-03 | Phase 2 | Complete |
| EDIT-04 | Phase 2 | Pending |
| EDIT-05 | Phase 2 | Pending |
| EDIT-06 | Phase 2 | Pending |
| EDIT-07 | Phase 2 | Pending |
| REL-01 | Phase 2 | Pending |
| REL-02 | Phase 2 | Pending |
| REL-03 | Phase 2 | Pending |
| PERS-01 | Phase 2 | Pending |
| PERS-02 | Phase 1 | Complete |
| PERS-03 | Phase 1 | Complete |
| UX-01 | Phase 2 | Complete |
| UX-02 | Phase 2 | Pending |
| UX-03 | Phase 1 | Complete |
| UX-04 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 25 total
- Mapped to phases: 25
- Unmapped: 0

---
*Requirements defined: 2026-03-16*
*Last updated: 2026-03-16 after roadmap revision*
