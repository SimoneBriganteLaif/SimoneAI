---
phase: 01-parser-and-visual-canvas
plan: 03
subsystem: ui
tags: [jointjs, svg, canvas, pan-zoom, er-diagram, javascript]

# Dependency graph
requires:
  - phase: none
    provides: standalone shapes and canvas (no API dependency)
provides:
  - ERShapes.createTable() factory for JointJS ER table elements with foreignObject HTML body
  - ERShapes.createLink() factory for manhattan-routed relationship lines with cardinality labels
  - ERShapes.updateTable() for collapse/expand with dynamic size recalculation
  - ERCanvas.init() for paper setup with dot grid, pan/zoom, selection, link hover
  - ERCanvas public API (fitAll, zoomIn, zoomOut, applyViewport, getViewport)
  - CSS styles for table content (columns, badges, relationships, dividers)
affects: [01-04-integration, 01-05-verification]

# Tech tracking
tech-stack:
  added: [JointJS 4.x custom shapes, foreignObject HTML-in-SVG]
  patterns: [IIFE namespace pattern (ERShapes, ERCanvas), factory function for dynamic JointJS elements, matrix-based zoom-to-point]

key-files:
  created:
    - tools/er-editor/static/shapes.js
    - tools/er-editor/static/canvas.js
    - tools/er-editor/static/style.css

key-decisions:
  - "Used foreignObject with HTML content inside JointJS SVG elements for table body rendering - much simpler than pure SVG for dynamic column/relationship rows with badges"
  - "Used object hash instead of Set for connected ID tracking (broader browser compatibility)"

patterns-established:
  - "ERShapes factory pattern: createTable() returns configured joint.dia.Element with stored tableData for later reference"
  - "Canvas interaction layering: selection overrides hover state, link:mouseleave restores selection if active"

requirements-completed: [VIS-01, VIS-02, VIS-03, VIS-04]

# Metrics
duration: 3min
completed: 2026-03-16
---

# Phase 01 Plan 03: JointJS Custom Shapes and Canvas Summary

**ERTable/ERLink shape factories with foreignObject HTML body, manhattan routing, and canvas with dot grid pan/zoom/selection/hover interactions**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-16T22:04:27Z
- **Completed:** 2026-03-16T22:07:50Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- ERShapes namespace with createTable, createLink, updateTable covering all UI-SPEC visual requirements
- ERCanvas namespace with full interactive canvas: dot grid, pan/zoom, selection highlighting, link hover, snap-to-grid
- Complete CSS styling for toolbar, table foreignObject content, loading/empty states

## Task Commits

Each task was committed atomically:

1. **Task 1: Create custom JointJS ERTable and ERLink shapes** - `de06e2c` (feat)
2. **Task 2: Create canvas setup with pan/zoom, grid, selection, interactions** - `14c8915` (feat)

## Files Created/Modified
- `tools/er-editor/static/shapes.js` - ERShapes namespace: createTable (foreignObject HTML body with PK/FK icons, NN/UQ/IDX badges, relationship section), createLink (manhattan routing, cardinality labels), updateTable (collapse/expand)
- `tools/er-editor/static/canvas.js` - ERCanvas namespace: init (JointJS Paper with dot grid), pan/zoom, selection highlighting, link hover, snap-to-grid, fitAll/zoomIn/zoomOut/applyViewport/getViewport
- `tools/er-editor/static/style.css` - CSS for toolbar, foreignObject table content (.er-col-row, .er-badge, .er-divider, .er-rel-row), JointJS element transitions, loading/empty states

## Decisions Made
- Used foreignObject with HTML div inside SVG for table body content (per plan recommendation) - much easier for multi-column layout with badges than pure SVG text elements
- Used plain object hash instead of ES6 Set for connected element ID tracking (broader browser compatibility without polyfills)
- Added escapeHtml() utility for XSS safety when rendering table/column names

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added HTML escaping for user-provided text**
- **Found during:** Task 1 (shapes.js)
- **Issue:** Column names, table names, and types from the parsed model are rendered as HTML inside foreignObject - potential XSS if model contains special characters
- **Fix:** Added escapeHtml() function using DOM text node creation, applied to all user-provided text in buildColumnHTML and buildRelHTML
- **Files modified:** tools/er-editor/static/shapes.js
- **Verification:** Function present, applied to all user text
- **Committed in:** de06e2c (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** Essential security fix for HTML injection. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- shapes.js and canvas.js are standalone modules ready for integration in Plan 04
- Plan 04 will wire these to API data via app.js, add dagre auto-layout, and connect toolbar controls
- The ERShapes/ERCanvas API surface matches the interfaces documented in PLAN.md

---
*Phase: 01-parser-and-visual-canvas*
*Completed: 2026-03-16*

## Self-Check: PASSED
- All 3 files exist (shapes.js 315 lines, canvas.js 363 lines, style.css)
- Both task commits verified (de06e2c, 14c8915)
- Both files exceed 150-line minimum requirement
