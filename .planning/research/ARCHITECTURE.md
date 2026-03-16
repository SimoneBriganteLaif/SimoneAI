# Architecture Patterns

**Domain:** ER diagram editor (code-to-visual round-trip tool)
**Researched:** 2026-03-16

## Recommended Architecture

The system follows a **two-pipeline** architecture: a **read pipeline** (model.py to visual) and a **write pipeline** (visual edits back to model.py), connected through a shared intermediate representation (IR) in JSON. A sidecar `.er.json` file stores visual-only metadata (positions, groups, colors) that has no place in source code.

```
┌─────────────────────────────────────────────────────────────────┐
│                        BROWSER (Frontend)                       │
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────────────┐  │
│  │ Toolbar  │    │ Property     │    │ JointJS Canvas        │  │
│  │ & Actions│    │ Panel        │    │ (Paper + Graph)       │  │
│  └────┬─────┘    └──────┬───────┘    └───────────┬───────────┘  │
│       │                 │                         │              │
│       └─────────┬───────┘                         │              │
│                 │                                 │              │
│           ┌─────▼─────────────────────────────────▼──────┐      │
│           │          EditorState (JS singleton)          │      │
│           │  - schema: IR tables/columns/relations       │      │
│           │  - layout: positions, groups, colors         │      │
│           │  - dirty: change tracking                    │      │
│           └──────────────────┬───────────────────────────┘      │
│                              │ HTTP (JSON)                      │
└──────────────────────────────┼──────────────────────────────────┘
                               │
┌──────────────────────────────┼──────────────────────────────────┐
│                      PYTHON BACKEND                             │
│                              │                                  │
│           ┌──────────────────▼───────────────────┐              │
│           │         FastAPI Server               │              │
│           │  GET  /schema    → read pipeline     │              │
│           │  POST /schema    → write pipeline    │              │
│           │  GET  /layout    → read sidecar      │              │
│           │  POST /layout    → write sidecar     │              │
│           └──────┬───────────────────┬───────────┘              │
│                  │                   │                           │
│         ┌────────▼────────┐  ┌───────▼────────┐                 │
│         │  Parser         │  │  Writer        │                 │
│         │  (libcst visit) │  │  (libcst xform)│                 │
│         └────────┬────────┘  └───────┬────────┘                 │
│                  │                   │                           │
│         ┌────────▼───────────────────▼────────┐                 │
│         │         model.py (source of truth)  │                 │
│         │         .er.json (sidecar metadata) │                 │
│         └─────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| **Parser** (`parser.py`) | Reads `model.py` via libcst CSTVisitor, extracts classes/columns/relationships into IR dict | FastAPI server (returns IR JSON) |
| **Writer** (`writer.py`) | Receives IR diff, applies changes to `model.py` via libcst CSTTransformer, preserves formatting | FastAPI server (receives diff, reads/writes model.py) |
| **FastAPI Server** (`server.py`) | HTTP API: serves schema IR, accepts schema changes, serves/saves layout | Parser, Writer, filesystem (.er.json) |
| **EditorState** (JS) | In-memory state: current schema + layout. Tracks dirty state, produces diffs | All frontend components, backend via fetch |
| **JointJS Canvas** (JS) | Visual rendering: Graph model + Paper view. ER shapes, ports, links, embedding for groups | EditorState (reads schema, emits visual events) |
| **Property Panel** (JS) | Form UI for editing selected table/column properties | EditorState (reads selection, writes property changes) |
| **Toolbar** (JS) | Actions: add table, save, undo, zoom controls | EditorState (dispatches actions) |

---

## Data Flow

### Pipeline 1: Read (model.py to visual)

```
model.py
  │
  ▼ libcst.parse_module()
CST tree (immutable, preserves all formatting)
  │
  ▼ CSTVisitor traversal
  │   visit_ClassDef → extract table name, base classes
  │   visit_AnnAssign → extract Mapped[] columns, types, constraints
  │   visit_SimpleStatementLine → extract relationship() calls
  │
  ▼ Intermediate Representation (IR)
{
  "tables": [{
    "name": "User",
    "columns": [
      {"name": "id", "type": "int", "primary_key": true, ...},
      {"name": "email", "type": "str", "nullable": false, "unique": true, ...}
    ],
    "relationships": [
      {"name": "orders", "target": "Order", "back_populates": "user", ...}
    ]
  }]
}
  │
  ▼ GET /schema → JSON response
  │
  ▼ EditorState stores IR
  │
  ▼ JointJS Graph population
      For each table → joint.shapes.standard.HeaderedRectangle (or custom ER shape)
      For each column → port on the element
      For each relationship → joint.dia.Link between ports
      For each group → parent element with embed()
```

### Pipeline 2: Write (visual edits to model.py)

```
User interaction (rename column, add table, change type, etc.)
  │
  ▼ Property Panel / Canvas event
  │
  ▼ EditorState.applyChange(change)
  │   Updates local IR
  │   Pushes change to dirty queue
  │   Re-renders affected JointJS elements
  │
  ▼ User clicks "Save"
  │
  ▼ POST /schema with change operations
{
  "operations": [
    {"op": "add_column", "table": "User", "column": {"name": "phone", "type": "str", ...}},
    {"op": "rename_table", "old_name": "Order", "new_name": "Purchase"},
    {"op": "remove_column", "table": "User", "column": "legacy_field"}
  ]
}
  │
  ▼ Writer receives operations
  │   For each operation:
  │     1. Parse current model.py with libcst.parse_module()
  │     2. Apply CSTTransformer for that operation type
  │     3. Serialize back with module.code (byte-perfect round-trip)
  │
  ▼ Updated model.py on disk
```

### Pipeline 3: Layout (sidecar metadata)

```
Layout changes (drag table, create group, change color)
  │
  ▼ EditorState.updateLayout(change)
  │   Updates positions/groups in memory
  │
  ▼ Auto-save or explicit save
  │
  ▼ POST /layout
{
  "positions": {
    "User": {"x": 100, "y": 200},
    "Order": {"x": 400, "y": 200}
  },
  "groups": [
    {"name": "Core", "color": "#E3F2FD", "tables": ["User", "Role"]},
    {"name": "Commerce", "color": "#FFF3E0", "tables": ["Order", "Product"]}
  ]
}
  │
  ▼ Written to .er.json alongside model.py
```

---

## Key Architecture Decisions

### 1. Operation-Based Diffs (Not Full IR Replace)

**Decision:** The frontend sends discrete operations (`add_column`, `rename_table`, etc.) instead of sending the entire modified IR and diffing server-side.

**Rationale:**
- Each operation maps to a specific libcst CSTTransformer, keeping transformers small and testable
- Avoids the complexity of diffing two full IR trees and figuring out what CST changes to make
- Operations are sequential and composable -- apply one transformer per operation
- Enables future undo/redo by storing an operation log

**Operation types needed for v1:**
- `add_table`, `remove_table`, `rename_table`
- `add_column`, `remove_column`, `rename_column`, `modify_column`
- `add_relationship`, `remove_relationship`, `modify_relationship`

### 2. Schema and Layout Are Separate Concerns

**Decision:** Schema (tables, columns, relationships) lives in `model.py`. Layout (positions, groups, colors) lives in `.er.json`.

**Rationale:**
- model.py is the source of truth for data structure -- adding visual metadata would pollute it
- .er.json is optional -- if missing, the editor auto-layouts tables and creates it on first save
- .er.json is versionable (commit it) or gitignore-able (treat as personal preference)
- Different developers can have different layouts for the same model

### 3. Stateless Backend, Stateful Frontend

**Decision:** The backend is stateless -- each request re-parses model.py. The frontend holds all state in an EditorState singleton.

**Rationale:**
- No server-side session state simplifies the architecture
- Re-parsing model.py on each save ensures we never drift from disk reality
- libcst parsing is fast (< 50ms for files with 13+ models)
- The frontend state is the "working copy" -- disk is the "committed" version

### 4. JointJS Graph as View Layer Only

**Decision:** JointJS Graph/Paper is a rendering layer. It reads from EditorState and emits events back to it. It does NOT own the schema data.

**Rationale:**
- JointJS graph model stores shapes/links/positions, not domain concepts like "nullable" or "cascade"
- Keeping domain state in EditorState means the property panel and canvas always read from the same source
- Rebuilding JointJS elements from IR is straightforward; the reverse (extracting schema from JointJS shapes) would be fragile

---

## Component Deep Dives

### Parser (libcst CSTVisitor)

The parser uses libcst's `CSTVisitor` pattern (read-only traversal, no modification).

**Key visitor methods:**
- `visit_ClassDef` / `leave_ClassDef` -- detect SQLAlchemy model classes (inheriting from `Base`)
- `visit_AnnAssign` -- detect `column_name: Mapped[type] = mapped_column(...)` patterns
- `visit_SimpleStatementLine` -- detect `relationship()` assignments

**Parsing challenges for SQLAlchemy 2.0 Mapped[] pattern:**
- Type extraction from `Mapped[Optional[str]]`, `Mapped[int]`, `Mapped[list["Order"]]`
- mapped_column() kwargs: `primary_key`, `nullable`, `unique`, `index`, `default`, `server_default`
- ForeignKey extraction from `mapped_column(ForeignKey("table.column"))`
- relationship() kwargs: `back_populates`, `cascade`, `lazy`, `uselist`

**Output:** Python dict matching the IR schema, serialized to JSON by FastAPI.

### Writer (libcst CSTTransformer)

One transformer class per operation type. Each transformer:

1. Receives the operation parameters
2. Overrides `leave_ClassDef` (or `leave_AnnAssign`, etc.) to find the target node
3. Returns modified node via `updated_node.with_changes(...)` or `RemovalSentinel.REMOVE`
4. For additions: injects new CST nodes built with `libcst.parse_statement()`

**Critical pattern -- using `parse_statement()` for additions:**
Instead of manually constructing CST nodes (verbose and error-prone), generate the Python code string and parse it:
```python
new_line = libcst.parse_statement("    phone: Mapped[Optional[str]] = mapped_column(nullable=True)\n")
```
This inherits sensible default whitespace and is much simpler than building `AnnAssign(target=Name(...), annotation=Annotation(...), ...)` by hand.

**Critical pattern -- preserving formatting:**
libcst preserves all whitespace, comments, and formatting by default. The writer does NOT need to handle formatting -- it comes for free as long as modifications use `with_changes()` on existing nodes.

### EditorState (JavaScript Singleton)

```javascript
const EditorState = {
    schema: null,          // IR from backend: {tables: [...]}
    layout: null,          // From .er.json: {positions: {}, groups: []}
    dirty: false,          // Has unsaved schema changes
    layoutDirty: false,    // Has unsaved layout changes
    operations: [],        // Pending operations queue
    selection: null,       // Currently selected table/column/link

    // Methods
    async loadFromServer(),     // GET /schema + GET /layout
    applyChange(operation),     // Mutate local IR + queue operation
    async save(),               // POST /schema with operations, then POST /layout
    getTableIR(tableName),      // Read access for property panel
    getColumnsForTable(name),   // Read access for rendering
    syncToGraph(graph),         // Push IR changes to JointJS Graph
};
```

### JointJS Canvas Integration

**Graph model** (`joint.dia.Graph`): holds shapes (table elements), links (relationships), and embedding hierarchy (groups contain tables).

**Paper view** (`joint.dia.Paper`): renders the graph, handles user interaction (drag, click, zoom).

**Table element shape:** Custom shape extending `joint.shapes.standard.HeaderedRectangle`:
- Header: table name (bold)
- Body: column list with icons for PK/FK/nullable
- Ports: one port per column (left and right) for link attachment

**Group element shape:** Simple rectangle with colored background, label. Uses JointJS embedding:
- `groupElement.embed(tableElement)` -- table becomes child
- Moving group moves all embedded tables
- `embeddingMode: true` on Paper for drag-to-group
- `validateEmbedding` callback to restrict: only group elements can be parents

**Link shape:** Standard link connecting FK column port to PK column port:
- Label shows relationship name
- Arrow indicates direction (one-to-many, etc.)
- Router: `manhattan` for orthogonal lines

---

## Patterns to Follow

### Pattern 1: Command Pattern for Operations

**What:** Each user edit becomes an operation object with type and parameters.
**When:** Any schema modification (not layout changes).
**Why:** Enables undo/redo, batch saves, and maps cleanly to CSTTransformers.

```javascript
// Frontend operation
{ op: "add_column", table: "User", column: { name: "phone", type: "str", nullable: true } }

// Backend transformer
class AddColumnTransformer(cst.CSTTransformer):
    def __init__(self, table_name, column_def):
        self.table_name = table_name
        self.column_def = column_def

    def leave_ClassDef(self, original_node, updated_node):
        if self._get_class_name(updated_node) == self.table_name:
            new_stmt = cst.parse_statement(self._build_column_code())
            new_body = updated_node.body.with_changes(
                body=[*updated_node.body.body, new_stmt]
            )
            return updated_node.with_changes(body=new_body)
        return updated_node
```

### Pattern 2: IR as Single Source of Truth

**What:** EditorState.schema is the canonical data. JointJS Graph and Property Panel derive from it.
**When:** Always. Never read schema data from JointJS elements.
**Why:** Prevents divergence between what you see and what gets saved.

```
EditorState.schema ──┬──► JointJS Graph (visual)
                     └──► Property Panel (form fields)

User edits ──► EditorState.applyChange() ──► re-render both
```

### Pattern 3: Lazy Sidecar Creation

**What:** If `.er.json` does not exist, the editor works anyway with auto-layout, and creates it on first layout save.
**When:** First time opening a model.py that has never been used with the editor.
**Why:** Zero setup friction. The tool works immediately on any model.py.

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Bidirectional Sync Between JointJS and State

**What:** Reading data back from JointJS elements to reconstruct schema state.
**Why bad:** JointJS stores visual attributes (position, size, color), not domain data (nullable, cascade). Mixing these creates fragile coupling.
**Instead:** JointJS is write-only from EditorState's perspective. Events from JointJS (click, drag) are translated into EditorState operations, never into direct state reads.

### Anti-Pattern 2: Full File Replacement on Save

**What:** Generating model.py from scratch based on IR, discarding the original file.
**Why bad:** Loses comments, custom formatting, import ordering, module-level code that the parser does not understand.
**Instead:** Apply surgical CSTTransformer operations to the existing CST tree.

### Anti-Pattern 3: Storing Schema in the Sidecar

**What:** Duplicating column types, constraints, or relationship data in .er.json.
**Why bad:** Creates two sources of truth. They will diverge.
**Instead:** .er.json stores ONLY visual metadata: positions, group membership, group colors, group names. Schema data lives exclusively in model.py.

### Anti-Pattern 4: One Giant CSTTransformer

**What:** A single transformer class that handles all operation types via if/elif chains.
**Why bad:** Hard to test, hard to debug, operation interactions become implicit.
**Instead:** One transformer per operation type. Apply them sequentially: `parse -> transform1 -> transform2 -> serialize`.

---

## Build Order (Dependencies)

The build order follows a strict dependency chain. Each phase requires the previous one.

```
Phase 1: Parser (model.py → IR)
   │      No dependencies. Can be built and tested in isolation.
   │      Test: parse real model.py files, assert IR structure.
   │
Phase 2: Backend API + Sidecar
   │      Depends on: Parser
   │      FastAPI endpoints that serve IR and manage .er.json
   │      Test: HTTP requests return correct JSON.
   │
Phase 3: Canvas Rendering (IR → visual)
   │      Depends on: Backend API
   │      JointJS graph population from IR JSON.
   │      Table shapes, column ports, relationship links.
   │      Test: Load IR, verify shapes render.
   │
Phase 4: Layout & Groups
   │      Depends on: Canvas Rendering
   │      Drag-to-reposition, group creation, embedding.
   │      .er.json save/load cycle.
   │      Test: Drag tables, create groups, reload page.
   │
Phase 5: Property Editing
   │      Depends on: Canvas Rendering + Backend API
   │      Property panel for editing selected element.
   │      Generates operations, sends to backend.
   │      Test: Edit column properties, verify model.py changes.
   │
Phase 6: Writer (operations → model.py)
   │      Depends on: Parser (to verify round-trip)
   │      CSTTransformers for each operation type.
   │      Test: Apply operation, re-parse, verify IR matches expected.
   │
Phase 7: Integration & Polish
          Wire property editing to writer.
          Undo/redo. Error handling. Edge cases.
```

**Critical dependency:** Phase 6 (Writer) can be developed in parallel with Phases 3-5, since it only needs the Parser and test model files. The frontend and backend write pipelines converge in Phase 7.

---

## File Structure

```
tools/er-editor/
├── server.py              # FastAPI app, CLI entry point
├── parser.py              # libcst CSTVisitor → IR extraction
├── writer.py              # libcst CSTTransformers → code modification
├── ir.py                  # IR type definitions (TypedDict / dataclass)
├── sidecar.py             # .er.json read/write logic
├── requirements.txt       # fastapi, uvicorn, libcst
├── static/
│   ├── index.html         # Single page, loads JS/CSS from CDN + local
│   ├── app.js             # Entry point, initializes editor
│   ├── state.js           # EditorState singleton
│   ├── canvas.js          # JointJS graph/paper setup, shape definitions
│   ├── shapes.js          # Custom ER table shape definition
│   ├── panel.js           # Property panel rendering and events
│   ├── toolbar.js         # Toolbar actions
│   └── style.css          # Layout, panel styling
└── tests/
    ├── test_parser.py     # Parser unit tests with real model.py snippets
    ├── test_writer.py     # Writer round-trip tests
    ├── fixtures/
    │   ├── simple.py      # 2-table model for basic tests
    │   └── complex.py     # 13+ table model matching LAIF complexity
    └── test_sidecar.py    # .er.json read/write tests
```

---

## Scalability Considerations

| Concern | 2-3 tables | 13+ tables (LAIF max) | 50+ tables (future) |
|---------|------------|----------------------|---------------------|
| Parse time | < 10ms | < 50ms | < 200ms, still fine |
| Canvas render | Trivial | Fine with JointJS | May need virtualization (not in v1) |
| Save operations | Instant | Sequential transforms, < 100ms | Batch transforms, still fine |
| Layout file | Tiny JSON | Small JSON | Manageable |

The v1 scope (single model.py, max ~20 tables in LAIF projects) is well within comfortable limits for all components. No performance optimizations needed at this scale.

---

## Sources

- [LibCST GitHub - Instagram/LibCST](https://github.com/Instagram/LibCST) -- CST parser documentation and capabilities (HIGH confidence)
- [LibCST Visitors Documentation](https://libcst.readthedocs.io/en/latest/visitors.html) -- CSTTransformer and CSTVisitor patterns (HIGH confidence)
- [LibCST Nodes Documentation](https://libcst.readthedocs.io/en/latest/nodes.html) -- Node types and with_changes API (HIGH confidence)
- [JointJS Containers & Grouping](https://docs.jointjs.com/learn/features/containers-and-grouping/) -- Embedding and group behavior (HIGH confidence)
- [JointJS Paper API](https://docs.jointjs.com/api/dia/Paper/) -- Paper view, events, embedding mode (HIGH confidence)
- [JointJS Ready-to-use Shapes](https://docs.jointjs.com/learn/features/ready-to-use-shapes/) -- Shape types including ER (HIGH confidence)
- [JointJS Links Overview](https://docs.jointjs.com/learn/features/shapes/links/) -- Link configuration and routing (HIGH confidence)
