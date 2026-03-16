# Project Research Summary

**Project:** ER Diagram Editor (local Python tool with browser frontend)
**Domain:** Interactive ER diagram editor with SQLAlchemy round-trip code generation
**Researched:** 2026-03-16
**Confidence:** HIGH

## Executive Summary

This project is a local developer tool that visualizes SQLAlchemy 2.0 `model.py` files as interactive ER diagrams and writes changes back to the source file with byte-perfect round-trip fidelity. No competitor in the ER editor space (dbdiagram.io, pgModeler, DBeaver, ChartDB) works on ORM source files directly or preserves comments and formatting on write-back. That gap is the entire value proposition. The recommended approach is: FastAPI local server + libcst for Python CST parsing/writing + JointJS open-source (CDN, no build step) for the browser diagram canvas.

The core architectural insight from research is the two-pipeline pattern: a read pipeline (model.py -> libcst CST -> IR -> JointJS graph) and a write pipeline (user operations -> EditorState IR -> operation diff -> libcst CSTTransformer -> model.py). These pipelines share an intermediate representation (IR) in JSON, and a separate sidecar `.er.json` file holds visual-only metadata (positions, groups, colors) that must never pollute the Python source. The EditorState JS singleton is the single source of truth on the frontend; JointJS is a rendering layer only.

The top risks are: (1) libcst's `original_node` vs `updated_node` confusion in CSTTransformers that silently drops nested changes — this must be understood before writing any writer code; (2) state desynchronization between the JointJS visual model and the IR data model if semantic data leaks into JointJS cell attributes; (3) relationship modeling complexity explosion (FK column + relationship() on both sides + cascade + back_populates) which is far harder than it looks from the diagram side. All three risks are front-loaded into Phase 1 and must be resolved architecturally before editing features are built.

---

## Key Findings

### Recommended Stack

The stack is minimal and opinionated. The no-build constraint (portable folder, `pip install` + run) is non-negotiable and shapes every technology decision. JointJS open-source v4.2.4 is the only credible diagram library that ships as a UMD bundle via CDN, handles ER shapes natively (ports, embedding, links), and works without npm/webpack. libcst v1.8.6 is the only maintained Python CST library with round-trip preservation — `ast` and regex are disqualified because they lose comments and formatting. FastAPI is already in the LAIF stack and adds zero friction.

**Core technologies:**
- **@joint/core 4.2.4** (CDN UMD): diagram rendering, drag-and-drop, SVG canvas — dependency-free since v4.0, MPL 2.0 license, ports + embedding confirmed in open-source
- **libcst 1.8.6**: Python CST parsing and round-trip code generation — Meta-maintained, preserves comments/whitespace byte-for-byte, Visitor/Transformer pattern maps cleanly to parser/writer separation
- **FastAPI 0.135.1**: local HTTP server bridging frontend and backend — already in LAIF stack, auto-reload dev server (`fastapi dev server.py`), Python 3.10+ required (binding constraint)
- **pydantic 2.x**: IR type definitions and API serialization — comes with FastAPI, zero extra cost

What is NOT needed: npm, webpack, vite, jQuery, Backbone, any build pipeline. JointJS 4.x is self-contained. Frontend is vanilla JS loaded via `<script>` tags from jsDelivr CDN.

See `.planning/research/STACK.md` for full version compatibility matrix and CDN URLs.

### Expected Features

Research confirms that round-trip SQLAlchemy ORM editing is a genuine differentiator — no competitor does this. Every other ER tool generates SQL DDL from scratch (discarding source), works on live databases, or uses a proprietary DSL. The feature scope is therefore well-defined: everything that makes the round-trip work is P1; everything else is P2 or P3.

**Must have (table stakes — v1):**
- Parser: model.py (libcst) to IR — nothing works without this
- Rendering: tables with columns, types, PK/FK indicators on JointJS canvas
- Rendering: relationship lines with cardinality markers (crow's foot notation)
- Navigation: drag-and-drop tables, zoom (mouse wheel), pan (drag blank area)
- CRUD: add/remove/rename tables
- CRUD: add/remove/rename/modify columns (type, nullable, unique, index, default)
- Relationship creation: creates FK column + relationship() on both sides
- Writer: model.py with comment and formatting preservation (the core value)
- Persistence: table positions in `.er.json` sidecar
- Server: `python server.py model.py` portable entry point

**Should have (competitive differentiators — v1.x after validation):**
- Undo/redo via command stack
- Visual grouping of tables with colors (JointJS embedding)
- Real-time code preview (split panel showing generated Python)
- Auto-arrange for first import (optional, non-destructive)
- Export SVG (JointJS supports this natively, low effort)

**Defer (v2+):**
- Multi-file support (requires Python import resolution — complexity not justified for v1)
- Many-to-many with association tables (start with one-to-many only)
- Pydantic schema editing (explicitly out of scope in PROJECT.md)
- Visual diff between model versions
- Minimap

**Anti-features (explicitly excluded):**
- Alembic migration generation (scope creep, risk of data loss)
- Real-time collaboration (out of scope for local tool)
- AI schema generation (not needed — user has existing model.py)
- Direct DB connection (wrong source of truth for this tool)

See `.planning/research/FEATURES.md` for full dependency graph and competitor analysis.

### Architecture Approach

The system uses a stateless Python backend (re-parses model.py on each save) and a stateful JavaScript frontend (EditorState singleton as canonical data store). Two pipelines connect them: GET /schema returns IR from libcst parsing; POST /schema accepts discrete operation objects (`add_column`, `rename_table`, etc.) each mapped to a dedicated CSTTransformer. Layout data flows separately via GET/POST /layout to/from `.er.json`. JointJS is a pure rendering layer — it never owns semantic data.

**Major components:**
1. **Parser** (`parser.py`) — libcst CSTVisitor reads model.py, extracts tables/columns/relationships into IR dict; no dependencies, testable in isolation
2. **Writer** (`writer.py`) — one CSTTransformer class per operation type; applies surgical changes to existing CST tree; never regenerates the file from scratch
3. **FastAPI Server** (`server.py`) — HTTP API: serves IR, accepts operation diffs, reads/writes `.er.json`; stateless, re-parses on each request
4. **EditorState** (JS singleton) — in-memory IR + layout + dirty tracking + operations queue; single source of truth for all frontend components
5. **JointJS Canvas** (`canvas.js`) — renders EditorState to Graph+Paper; emits events translated back to EditorState operations; never read back for schema data
6. **Property Panel** (`panel.js`) — form UI for editing selected table/column; reads from EditorState, writes via `applyChange()`
7. **Sidecar** (`sidecar.py`) — `.er.json` read/write; only stores positions, group membership, group colors/names; schema data never lives here

**Key architectural decisions:**
- Operation-based diffs (not full IR replace): keeps each CSTTransformer small and testable, enables undo/redo log
- Schema (model.py) and layout (.er.json) are separate concerns: model.py stays clean, layout is optionally versionable
- JointJS as view layer only: prevents the fragile pattern of reading schema back from visual attributes

See `.planning/research/ARCHITECTURE.md` for full data flow diagrams and component deep dives.

### Critical Pitfalls

1. **libcst `original_node` vs `updated_node` in CSTTransformers** — always modify `updated_node` (which contains child modifications), never `original_node` (stale copy). Silently drops nested changes with no error. Must be understood before writing any writer code. Add regression test in first sprint: modify column inside class, verify both changes appear in output.

2. **State desynchronization (visual vs data model)** — JointJS graph state and IR drift apart if semantic data (column types, nullable, FK targets) leaks into JointJS cell attributes. IR must be the single source of truth; JointJS owns only position/size/color. Retrofitting this pattern after the fact is a rewrite.

3. **Relationship modeling complexity explosion** — a simple FK line hides: FK column on child, `relationship()` on parent, optional `back_populates` on child, cascade config. Renaming a table must update all `ForeignKey("table.col")` string references across the file. Model relationships as first-class IR entities. Start with one-to-many only; add many-to-many as a separate feature in v1.x.

4. **libcst statement type mismatches when adding nodes** — `SimpleStatementLine` vs `BaseCompoundStatement` wrapping requirements cause cryptic serialization errors when inserting new nodes. Use `libcst.parse_statement()` to construct new nodes from code strings rather than building CST nodes manually. Build helper functions for all node types before writing transformers.

5. **JointJS open-source missing undo/redo and zoom/pan** — these are not included in the free version (JointJS+ only). Budget explicit dev time: undo/redo via manual command stack (before/after JSON snapshots on `graph` change events); zoom via `paper.scale()` with mouse wheel handler; pan via `paper.translate()` with drag handler (~20 lines of JS each, but must be planned upfront).

---

## Implications for Roadmap

The architecture research defines a strict dependency chain that maps directly to phases. The write pipeline can be developed in parallel with the frontend rendering once the parser is working, which enables the main risk items (libcst round-trip) to be validated independently before the full UI integration.

### Phase 1: Foundations — Parser, IR, and Backend API

**Rationale:** Nothing in the system works without the parser. The IR data structure is the contract between all other components. This phase validates the core technical premise (libcst round-trip fidelity) before any UI work begins. All three architectural pitfalls (original_node confusion, state desync, relationship modeling) must be resolved here at the design level.

**Delivers:** Working `parser.py` + `ir.py` + FastAPI endpoints (`GET /schema`, `GET /layout`, `POST /layout`) + `.er.json` sidecar. Tests proving round-trip fidelity on real LAIF model files.

**Implements:** Parser component, IR type definitions, sidecar component, FastAPI server skeleton

**Addresses from FEATURES.md:** Parser model.py (P1), server entry point (P1), persistence sidecar (P1)

**Must avoid:** Using `ast` module instead of libcst, storing any schema data in `.er.json`, building a monolithic CSTTransformer

### Phase 2: Canvas Rendering — Visual Layer

**Rationale:** Once the backend serves a stable IR, the frontend can populate JointJS from it. This phase has no write-back complexity — it is read-only rendering. It validates that JointJS custom shapes work for the ER use case and that zoom/pan/drag work correctly without JointJS+.

**Delivers:** Single-page browser app that loads model.py, renders tables as ER shapes with columns and FK relationships as links, supports drag-and-drop repositioning, zoom, pan, and saves positions to `.er.json`.

**Implements:** JointJS canvas setup, custom table shape definition, EditorState singleton (read path), layout auto-save

**Addresses from FEATURES.md:** Rendering tables (P1), rendering relationships (P1), drag/drop + zoom/pan (P1), persistence positions (P1)

**Must avoid:** Storing schema data in JointJS cell attributes, reading schema back from JointJS elements

### Phase 3: Schema Editing — Write Pipeline

**Rationale:** With rendering working and the IR validated, this phase adds the write pipeline. Each editing operation is implemented as a discrete CSTTransformer. The `original_node` vs `updated_node` pitfall must be addressed with regression tests before any transformer is considered done.

**Delivers:** Property panel for editing selected table/column, POST /schema endpoint accepting operation diffs, Writer with CSTTransformers for all P1 table/column operations, backup file (`.model.py.bak`) before each save, "unsaved changes" indicator in UI.

**Implements:** Writer component (table and column operation types), Property Panel, Toolbar actions, EditorState write path

**Addresses from FEATURES.md:** Editing tables CRUD (P1), editing columns CRUD (P1), writer with preservation (P1)

**Must avoid:** Full file regeneration (always use surgical CSTTransformer), whitespace corruption on new node insertion (use `parse_statement()` helpers)

### Phase 4: Relationship Editing

**Rationale:** Relationship editing is isolated into its own phase because it is the most complex operation in the system. It touches both models: visually a link between two shapes, semantically a FK column on the child table, a `relationship()` declaration on both sides, and `back_populates` pairing. Keeping it separate prevents relationship complexity from blocking column/table editing in Phase 3.

**Delivers:** Visual relationship creation (drag from port to port), relationship property editing, FK column auto-creation on child table, table rename propagating all FK string references, delete relationship cleaning up both sides. One-to-many only for v1.

**Implements:** Relationship CSTTransformers (add/remove/modify/rename-cascade), relationships as first-class IR entities

**Addresses from FEATURES.md:** Creazione relazioni (P1), rendering relazioni (P1)

**Must avoid:** Hardcoding FK string references without rename-aware propagation, skipping back_populates pairing, implementing many-to-many before one-to-many is stable

**Research flag:** SQLAlchemy relationship permutations (uselist, lazy, secondary, viewonly, cascade combinations) likely need targeted research to determine which subset to model in v1 IR.

### Phase 5: Editor Polish — Undo/Redo and UX

**Rationale:** Undo/redo and UX polish features are deferred to avoid scope creep in Phases 3-4. Undo/redo requires the full operation log from Phases 3-4 to be stable before a reliable command stack can be built.

**Delivers:** Undo/redo via command stack (before/after IR snapshots), keyboard shortcuts (Delete to remove, Ctrl+S to save, Escape to deselect), visual grouping of tables with colors, real-time code preview panel, `beforeunload` warning for unsaved changes, viewport state persistence in `.er.json`.

**Implements:** Command stack on EditorState, visual group elements (JointJS embedding), split panel with syntax-highlighted code preview

**Addresses from FEATURES.md:** Undo/redo (P2), raggruppamento visuale (P2), preview codice real-time (P2)

---

### Phase Ordering Rationale

- Parser before canvas: JointJS canvas needs data to render. Without a working parser the frontend is empty.
- Canvas before editing: The property panel and write pipeline are meaningless without something to select and display.
- Columns and tables before relationships: Relationship editing has combinatorial complexity. Base CRUD must be stable first. The IR data structure must accommodate relationships from Phase 1 even if editing comes in Phase 4.
- Polish last: Undo/redo requires a complete operation log. Adding it early means it would cover an incomplete set of operations.
- Writer can parallel canvas: The write pipeline (writer.py CSTTransformers) can be built and unit-tested in parallel with canvas rendering since it only needs the parser and test fixtures. A small team could overlap Phase 3 writer work with Phase 2 canvas work.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 4 (Relationship Editing):** SQLAlchemy relationship permutations (uselist, lazy, secondary, viewonly, cascade combinations) may require research into which subset to support in v1 and how to represent them in the IR.

Phases with well-documented patterns (research-phase not needed):
- **Phase 1 (Parser):** libcst CSTVisitor pattern is well-documented with Meta production use cases. SQLAlchemy 2.0 Mapped[] syntax is stable and documented.
- **Phase 2 (Canvas):** JointJS shape definition, ports, and embedding are documented in official guides. Pan/zoom without JointJS+ is a known solved pattern (~20 lines per PITFALLS.md).
- **Phase 3 (Schema Editing):** CSTTransformer pattern is well-established. The `parse_statement()` helper approach avoids manual node construction complexity.
- **Phase 5 (Polish):** Undo/redo via command stack with JSON snapshots is a standard pattern. JointJS embedding for groups is confirmed in open-source feature set.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All technologies verified on official sources (jsDelivr CDN, PyPI, FastAPI docs). JointJS 4.x CDN usage confirmed. libcst Meta-maintained with active releases. |
| Features | HIGH | Competitor analysis covers all major ER tools. Feature dependencies mapped clearly. MVP scope is conservative and well-reasoned. |
| Architecture | HIGH | Two-pipeline pattern is standard for code-to-visual tools. libcst Transformer pattern verified against real-world use cases (Meta, SeatGeek, Instawork). Key decisions are well-motivated. |
| Pitfalls | HIGH | All pitfalls sourced from real libcst GitHub issues, production use case writeups, and JointJS official comparison page. No speculative pitfalls. |

**Overall confidence: HIGH**

### Gaps to Address

- **SQLAlchemy relationship permutations for IR modeling:** Which combination of `relationship()` kwargs (lazy, uselist, secondary, viewonly, cascade, overlaps) need to be represented in v1 IR vs deferred? Needs a decision before Phase 4 IR design.
- **Whitespace convention for LAIF model files:** Are all LAIF `model.py` files formatted consistently (consistent blank lines between classes, indentation style)? If yes, whitespace conventions can be hardcoded in the writer (acceptable technical debt per PITFALLS.md). If no, a `WhitespaceConvention` detector is needed before Phase 3.
- **Initial auto-layout algorithm:** The specific algorithm for first-import positioning (force-directed, grid, hierarchical by FK) was not researched. Needs a decision before Phase 2 sidecar integration.

---

## Sources

### Primary (HIGH confidence)
- [JointJS official comparison page](https://www.jointjs.com/comparison) — open-source vs JointJS+ feature breakdown
- [JointJS v4.0 release blog](https://www.jointjs.com/blog/introducing-version-4) — dependency-free announcement
- [JointJS docs: Containers and Grouping](https://docs.jointjs.com/learn/features/containers-and-grouping/) — embedding/nesting in open-source
- [@joint/core on jsDelivr](https://www.jsdelivr.com/package/npm/@joint/core) — CDN availability v4.2.4
- [libcst on PyPI](https://pypi.org/project/libcst/) — v1.8.6, Python 3.9+
- [libcst on GitHub](https://github.com/Instagram/LibCST) — Meta/Instagram maintained, best practices docs
- [LibCST Visitors Documentation](https://libcst.readthedocs.io/en/latest/visitors.html) — CSTTransformer and CSTVisitor patterns
- [FastAPI on PyPI](https://pypi.org/project/fastapi/) — v0.135.1, Python 3.10+

### Secondary (MEDIUM confidence)
- [Refactoring with LibCST (SeatGeek)](https://chairnerd.seatgeek.com/refactoring-python-with-libcst/) — practical transformer pitfalls
- [Refactoring with LibCST (Instawork)](https://engineering.instawork.com/refactoring-a-python-codebase-with-libcst-fc645ecc1f09) — real-world experience
- [LibCST whitespace issue #1118](https://github.com/Instagram/LibCST/issues/1118) — whitespace validation gotchas
- [Top ER tools comparison (Holistics)](https://www.holistics.io/blog/top-5-free-database-diagram-design-tools/) — competitor landscape
- [ER tool trends 2025 (Liam ERD)](https://liambx.com/blog/er-diagram-tool-trends-2025) — trend context

### Tertiary (for background)
- [dbdiagram.io](https://dbdiagram.io/) — DSL-first ER editor, UX reference
- [pgModeler](https://pgmodeler.io/) — desktop ER modeler, full feature set reference
- [ChartDB](https://github.com/chartdb/chartdb) — OSS competitor

---
*Research completed: 2026-03-16*
*Ready for roadmap: yes*
