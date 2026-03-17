---
phase: 02-full-editing
plan: 06
subsystem: ui, parser
tags: [column-crud, enum, sqlalchemy, jointjs, undo-redo, popup]

# Dependency graph
requires:
  - phase: 02-full-editing/02-02
    provides: "Undo/redo infrastructure (ERUndo.execute)"
  - phase: 02-full-editing/02-05
    provides: "data-col-name attributes on column rows"
provides:
  - "Column CRUD functions (add, rename, delete, property popup) in editor.js"
  - "ColumnIR.enum_values field for Enum column support"
  - "Python Enum class generation in writer.py (_build_enum_class)"
  - "Type selector with 12 SQLAlchemy type presets"
affects: [02-full-editing/02-07, 02-full-editing/02-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Column property popup with conditional type detail inputs"
    - "Enum class name derivation: {ClassName}{ColumnNameCapitalized}"
    - "Inline column name editing via overlay input on double-click"

key-files:
  created: []
  modified:
    - "tools/er-editor/static/editor.js"
    - "tools/er-editor/parser/ir.py"
    - "tools/er-editor/parser/writer.py"
    - "tools/er-editor/tests/test_writer.py"

key-decisions:
  - "Enum class naming convention: {ClassName}{ColumnNameCapitalized} (e.g., OrderStatus, TicketPriority)"
  - "Enum values stored as list[str] on ColumnIR, writer generates Python Enum class"
  - "Used existing _escapeAttr from relationship CRUD (reused, not duplicated)"

patterns-established:
  - "Column popup pattern: type dropdown with conditional detail fields (length, precision/scale, enum values, custom)"
  - "Inline edit pattern: fixed-position input overlay on cell, commit on Enter/blur, cancel on Escape"

requirements-completed: [EDIT-04, EDIT-05, EDIT-06, EDIT-07]

# Metrics
duration: 6min
completed: 2026-03-17
---

# Phase 02 Plan 06: Column CRUD with Enum Support Summary

**Column add/rename/delete with property popup, type selector (12 presets including Enum with inline value definition), and Python Enum class generation in writer.py**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-17T22:51:14Z
- **Completed:** 2026-03-17T22:57:12Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Full column CRUD: add via + icon, rename via double-click, delete with confirmation, property popup with all fields
- Type selector with 12 SQLAlchemy type presets including conditional detail inputs (String length, Numeric precision/scale, Enum values textarea, Custom type expression)
- End-to-end Enum support: ColumnIR.enum_values -> writer.py generates Python Enum class -> correct Mapped[] annotation and Enum() column type
- All column operations wrapped in undo/redo commands via ERUndo.execute()

## Task Commits

Each task was committed atomically:

1. **Task 1: Enum support -- ColumnIR + writer.py** - `9fe049c` (feat)
2. **Task 2: Column CRUD -- add, rename, delete, property popup** - `f600d8b` (feat)

## Files Created/Modified
- `tools/er-editor/parser/ir.py` - Added enum_values field to ColumnIR
- `tools/er-editor/parser/writer.py` - Added _build_enum_class, _resolve_enum_column, Enum class generation in CST round-trip and preview
- `tools/er-editor/tests/test_writer.py` - Added test_add_enum_column and test_preview_with_enum
- `tools/er-editor/static/editor.js` - Added column CRUD functions: addColumn, showColumnPopup, deleteColumn, applyColumnChanges, startColumnNameEdit, type helpers

## Decisions Made
- Enum class naming: {ClassName}{ColumnNameCapitalized} derives from table class name + column name (e.g., OrderStatus)
- Reused existing _escapeAttr utility already added by relationship CRUD plan
- Column click opens property popup; double-click on column name starts inline rename (different interaction patterns for different operations)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Column CRUD complete, ready for table CRUD (02-07) and polish plans
- Enum support end-to-end verified with tests

---
*Phase: 02-full-editing*
*Completed: 2026-03-17*
