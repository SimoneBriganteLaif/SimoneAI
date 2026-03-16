---
phase: 01-parser-and-visual-canvas
plan: 01
subsystem: parser
tags: [libcst, sqlalchemy, dataclasses, cst-visitor, python]

# Dependency graph
requires: []
provides:
  - "IR dataclasses (TableIR, ColumnIR, RelationshipIR) for all downstream consumers"
  - "extract_model() function: source string -> list[TableIR]"
  - "Test fixtures: realistic 3-table LAIF model (Mailbox, EmailTicket, EmailMessage)"
  - "11 unit tests validating parser correctness"
affects: [01-02, 01-03, 01-04, 02-01]

# Tech tracking
tech-stack:
  added: [libcst, pytest]
  patterns: [CSTVisitor for AST extraction, TDD red-green]

key-files:
  created:
    - tools/er-editor/parser/ir.py
    - tools/er-editor/parser/extractor.py
    - tools/er-editor/tests/test_parser.py
    - tools/er-editor/tests/fixtures/sample_model.py
    - tools/er-editor/tests/conftest.py
    - tools/er-editor/requirements.txt
  modified: []

key-decisions:
  - "ORM detection by __tablename__ presence, not base class name -- handles all LAIF patterns"
  - "Column type extracted from mapped_column() first positional arg, annotation as fallback"
  - "Nullable inference: PK always False, explicit nullable= overrides, annotation Mapped[X | None] as default"
  - "uselist inference: list[] in Mapped annotation -> True, bare type -> False, explicit uselist= overrides"

patterns-established:
  - "CSTVisitor pattern: visit_ClassDef opens table context, leave_ClassDef closes and conditionally appends"
  - "visit_SimpleStatementLine dispatches to typed handlers (_handle_assign, _handle_ann_assign)"

requirements-completed: [PARS-01, PARS-02, PARS-03]

# Metrics
duration: 6min
completed: 2026-03-16
---

# Phase 1 Plan 01: Parser Summary

**libcst CSTVisitor parser extracting SQLAlchemy 2.0 tables, columns (type/PK/FK/nullable/unique/index/default), and relationships (target/back_populates/cascade/uselist) into JSON-serializable IR dataclasses**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-16T22:03:57Z
- **Completed:** 2026-03-16T22:10:26Z
- **Tasks:** 2
- **Files modified:** 8

## Accomplishments
- IR dataclasses (ColumnIR, RelationshipIR, TableIR) with all fields needed by downstream plans
- libcst ModelExtractor CSTVisitor that correctly parses realistic LAIF models
- 11 unit tests covering all extraction behaviors: tables, columns, FK, nullable, defaults, relationships, uselist, schema, ORM detection, index, JSON serialization
- All tests green, JSON round-trip verified

## Task Commits

Each task was committed atomically:

1. **Task 1: Create IR dataclasses, test fixtures, and test scaffold** - `66b0335` (test)
2. **Task 2: Implement libcst ModelExtractor (GREEN phase)** - `df7fee5` (feat)

_TDD flow: Task 1 = RED (failing tests), Task 2 = GREEN (implementation passes all tests)_

## Files Created/Modified
- `tools/er-editor/parser/ir.py` - IR dataclasses: ColumnIR, RelationshipIR, TableIR
- `tools/er-editor/parser/extractor.py` - libcst CSTVisitor + extract_model() function
- `tools/er-editor/parser/__init__.py` - Package init
- `tools/er-editor/tests/test_parser.py` - 11 unit tests for parser extraction
- `tools/er-editor/tests/conftest.py` - Shared fixtures (sample_model_path, sample_model_source, parsed_tables)
- `tools/er-editor/tests/fixtures/sample_model.py` - Realistic LAIF 3-table model fixture
- `tools/er-editor/tests/__init__.py` - Package init
- `tools/er-editor/requirements.txt` - Python dependencies (fastapi, uvicorn, libcst, pytest)

## Decisions Made
- ORM detection by `__tablename__` presence (not base class name) -- handles all LAIF inheritance patterns
- Column type from `mapped_column()` first positional arg, Mapped[] annotation as fallback -- avoids showing raw Python types like `str | None`
- Nullable logic: PK -> always False, explicit `nullable=` overrides, Mapped annotation as default
- uselist from `list[]` annotation -> True, bare type -> False, explicit `uselist=` keyword overrides

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed Python 3.9 type annotation compatibility**
- **Found during:** Task 1 (IR dataclasses)
- **Issue:** `str | None` syntax in dataclass fields not supported at runtime in Python 3.9
- **Fix:** Added `from __future__ import annotations` to ir.py and extractor.py (linter auto-applied on ir.py)
- **Files modified:** tools/er-editor/parser/ir.py, tools/er-editor/parser/extractor.py
- **Verification:** All imports and tests work on Python 3.9.6
- **Committed in:** 66b0335 (Task 1 commit)

**2. [Rule 3 - Blocking] Fixed libcst Module.walk() API for CSTVisitor**
- **Found during:** Task 2 (extractor implementation)
- **Issue:** libcst Module has no `.walk()` method for CSTVisitor -- requires MetadataWrapper
- **Fix:** Changed `tree.walk(extractor)` to `cst.metadata.MetadataWrapper(tree).visit(extractor)`
- **Files modified:** tools/er-editor/parser/extractor.py
- **Verification:** All 11 tests pass
- **Committed in:** df7fee5 (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Both fixes necessary to run on system Python 3.9 and use correct libcst API. No scope creep.

## Issues Encountered
None beyond the auto-fixed deviations above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- IR format stable, ready for Plan 02 (FastAPI server + API routes)
- extract_model() function ready for integration in API routes
- Test fixtures available for Plan 02 server testing

## Self-Check: PASSED

- All 8 created files verified present on disk
- Commit 66b0335 (Task 1 RED) verified in git log
- Commit df7fee5 (Task 2 GREEN) verified in git log
- 11/11 tests passing confirmed

---
*Phase: 01-parser-and-visual-canvas*
*Completed: 2026-03-16*
