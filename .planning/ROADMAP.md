# Roadmap: ER Editor

## Overview

Transform a SQLAlchemy 2.0 model.py file into an interactive ER diagram that supports full visual editing with byte-perfect round-trip back to source. Two phases: first build the foundation (parser + visual canvas) with parallel tracks for Python and JS, then deliver all editing capabilities with maximum parallelization across independent feature tracks.

## Phases

**Phase Numbering:**
- Integer phases (1, 2): Planned milestone work
- Decimal phases (1.1, 1.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Parser and Visual Canvas** - Parse model.py into an interactive ER diagram with navigation and layout persistence
- [ ] **Phase 2: Full Editing** - Complete CRUD for tables, columns, relationships with round-trip write-back, undo/redo, grouping, and live code preview

## Phase Details

### Phase 1: Parser and Visual Canvas
**Goal**: User can open any LAIF model.py and see a complete, navigable ER diagram with tables, columns, relationships, and persistent layout
**Depends on**: Nothing (first phase)
**Requirements**: PARS-01, PARS-02, PARS-03, PARS-04, VIS-01, VIS-02, VIS-03, VIS-04, PERS-02, PERS-03, UX-03
**Success Criteria** (what must be TRUE):
  1. User runs `python server.py /path/to/model.py` and the browser opens showing all tables from the file as ER boxes with typed columns and PK/FK/nullable/unique/index indicators
  2. Relationship lines with crow's foot cardinality markers connect related tables accurately reflecting the model's foreign keys and relationships
  3. User can drag tables, pan the canvas, and zoom in/out with mouse/trackpad
  4. Table positions persist across browser reloads via .er.json sidecar file
  5. Opening a model.py for the first time auto-arranges tables in a readable layout
**Plans:** 5 plans

**Parallelization opportunities:**
- Python parser (PARS-01..04) and JointJS shapes/canvas (VIS-01..04) are independent -- build simultaneously
- Server API and frontend app shell are independent
- Layout persistence (PERS-02, PERS-03, UX-03) can start once IR format is defined

Plans:
- [ ] 01-01-PLAN.md — Python IR dataclasses + libcst parser with TDD
- [x] 01-02-PLAN.md — FastAPI server, API routes, HTML shell, persistence tests
- [ ] 01-03-PLAN.md — JointJS custom shapes (ERTable, ERLink) + canvas setup (pan/zoom/grid/interactions)
- [ ] 01-04-PLAN.md — Integration: dagre auto-layout, toolbar, app.js wiring
- [ ] 01-05-PLAN.md — Human visual/functional verification checkpoint

### Phase 2: Full Editing
**Goal**: User can visually add, modify, and delete tables, columns, and relationships, save changes back to model.py with comments and formatting preserved, undo/redo any operation, organize tables into groups, and preview generated code in real-time
**Depends on**: Phase 1
**Requirements**: EDIT-01, EDIT-02, EDIT-03, EDIT-04, EDIT-05, EDIT-06, EDIT-07, REL-01, REL-02, REL-03, PERS-01, UX-01, UX-02, UX-04
**Success Criteria** (what must be TRUE):
  1. User can add a new table, rename or delete existing tables, and the changes appear immediately on the canvas
  2. User can add, rename, delete columns and modify their properties (type, nullable, unique, index, PK, default) via a property panel
  3. User can create a relationship between two tables (auto-generates FK column + relationship on both sides) and modify or delete existing relationships
  4. Saving writes all changes back to model.py preserving every comment, blank line, and formatting from the original file
  5. Destructive operations (delete table, delete column, delete relationship) require confirmation before executing
  6. User can undo and redo any editing operation with Ctrl+Z / Ctrl+Shift+Z
  7. User can create named, colored groups and drag tables into and out of them to organize the diagram
  8. A real-time code preview panel shows the current model.py output, updating as the user makes changes
**Plans**: TBD

**Parallelization opportunities:**
- Table CRUD (EDIT-01..07) and relationship CRUD (REL-01..03) share the IR but have independent UI -- build in parallel
- Undo/redo (UX-02) is an IR-level concern, independent from any specific editing UI
- Groups (UX-01) are a canvas-level feature, independent from schema editing
- Code preview (UX-04) reads the IR and generates Python -- independent from editing UI
- Round-trip writer (PERS-01) is a pure Python concern, independent from all frontend work

Plans:
- [ ] 02-01: TBD
- [ ] 02-02: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Parser and Visual Canvas | 1/5 | In progress | - |
| 2. Full Editing | 0/? | Not started | - |
