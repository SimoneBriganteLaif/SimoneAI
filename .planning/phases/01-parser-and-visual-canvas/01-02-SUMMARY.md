---
phase: 01-parser-and-visual-canvas
plan: 02
subsystem: api
tags: [fastapi, uvicorn, html, css, jointjs, dagre, persistence, sidecar]

# Dependency graph
requires:
  - phase: 01-parser-and-visual-canvas (plan 01)
    provides: "parser IR dataclasses and extract_model() function"
provides:
  - "FastAPI server entry point (server.py) with CLI and browser open"
  - "API routes: GET /api/schema, GET /api/layout, POST /api/layout"
  - "HTML shell with toolbar, canvas container, loading/empty/error states"
  - "Full CSS per UI-SPEC (toolbar, overlays, spinner, ER table styles)"
  - ".er.json sidecar persistence (read/write)"
affects: [01-03, 01-04, 01-05]

# Tech tracking
tech-stack:
  added: [fastapi, uvicorn, httpx]
  patterns: [sidecar-json-persistence, fastapi-static-spa, module-global-state]

key-files:
  created:
    - tools/er-editor/server.py
    - tools/er-editor/api/__init__.py
    - tools/er-editor/api/routes.py
    - tools/er-editor/static/index.html
    - tools/er-editor/tests/test_server.py
    - tools/er-editor/tests/test_persistence.py
  modified:
    - tools/er-editor/static/style.css
    - tools/er-editor/parser/ir.py
    - tools/er-editor/requirements.txt

key-decisions:
  - "Added from __future__ import annotations to ir.py for Python 3.9 compat"
  - "Merged style.css with existing ER table styles from Plan 03 parallel execution"
  - "httpx added as test dependency for FastAPI TestClient"

patterns-established:
  - "Sidecar persistence: .er.json next to model.py for layout state"
  - "Module-global state: set_model_path() configures routes before uvicorn starts"

requirements-completed: [PARS-04, PERS-02, PERS-03]

# Metrics
duration: 7min
completed: 2026-03-16
---

# Phase 1 Plan 02: Server, API Routes, HTML Shell Summary

**FastAPI server with schema/layout API, HTML shell with toolbar + JointJS/dagre CDN, and .er.json sidecar persistence with 10 passing tests**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-16T22:04:19Z
- **Completed:** 2026-03-16T22:11:19Z
- **Tasks:** 2
- **Files modified:** 9

## Accomplishments
- FastAPI server.py that accepts model.py path from CLI, starts uvicorn, opens browser
- API routes serving parsed schema (GET /api/schema) and layout persistence (GET/POST /api/layout)
- HTML shell with full toolbar (search, collapse/expand, re-layout, fit-all, zoom) and canvas container with loading/empty/error states
- CSS implementing UI-SPEC values (toolbar, overlays, spinner, ER table foreignObject styles)
- 10 passing tests covering server startup, schema endpoint, layout read/write/overwrite

## Task Commits

Each task was committed atomically:

1. **Task 1: Create FastAPI server entry point and API routes** - `14c8915` (feat)
2. **Task 2: Create HTML shell, tests for server and persistence** - `df9531e` (feat)

## Files Created/Modified
- `tools/er-editor/server.py` - FastAPI app entry point with uvicorn + browser open
- `tools/er-editor/api/__init__.py` - Empty package init
- `tools/er-editor/api/routes.py` - API routes: GET /api/schema, GET /api/layout, POST /api/layout
- `tools/er-editor/static/index.html` - SPA shell with toolbar, canvas, CDN scripts
- `tools/er-editor/static/style.css` - Full UI-SPEC CSS (merged with existing ER table styles)
- `tools/er-editor/tests/test_server.py` - 5 server smoke tests
- `tools/er-editor/tests/test_persistence.py` - 5 persistence unit tests
- `tools/er-editor/parser/ir.py` - Added future annotations for Python 3.9 compat
- `tools/er-editor/requirements.txt` - Added httpx dependency

## Decisions Made
- Added `from __future__ import annotations` to `ir.py` because Python 3.9 does not support `str | None` and `list[...]` syntax at runtime without it
- Merged Plan 02 CSS with existing ER table styles that Plan 03 had already created in `style.css` (parallel execution overlap)
- Added httpx to requirements.txt as it is needed by FastAPI TestClient

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Python 3.9 type annotation compatibility**
- **Found during:** Task 1 (server entry point creation)
- **Issue:** parser/ir.py used `str | None` and `list[ColumnIR]` syntax which requires Python 3.10+. System Python is 3.9.6.
- **Fix:** Added `from __future__ import annotations` to ir.py and all new files
- **Files modified:** tools/er-editor/parser/ir.py
- **Verification:** `from parser.ir import TableIR` succeeds on Python 3.9
- **Committed in:** 14c8915 (Task 1 commit)

**2. [Rule 3 - Blocking] Merged style.css with parallel Plan 03 work**
- **Found during:** Task 2 (HTML shell creation)
- **Issue:** Plan 03 had already created style.css with ER table foreignObject styles. Plan 02 needed to add toolbar, canvas, overlay styles without losing Plan 03's work.
- **Fix:** Rewrote style.css preserving all existing ER table CSS classes while adding Plan 02 toolbar/overlay/spinner styles
- **Files modified:** tools/er-editor/static/style.css
- **Verification:** All acceptance criteria for CSS met; no ER table styles lost
- **Committed in:** df9531e (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Both auto-fixes necessary for correct operation on target Python version and parallel plan coordination. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Server, API, and HTML shell ready for Plans 03 (JointJS shapes/canvas) and 04 (integration/toolbar wiring)
- Parser is fully implemented (Plan 01 completed) and returns real data for the 3 sample tables
- All 10 tests green, providing regression safety for future work

## Self-Check: PASSED

- All 7 created/modified files verified on disk
- Commit 0961fe7 (Task 1) found in git log
- Commit df9531e (Task 2) found in git log
- 10/10 tests passing

---
*Phase: 01-parser-and-visual-canvas*
*Completed: 2026-03-16*
