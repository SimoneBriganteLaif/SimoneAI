# Stack Research

**Domain:** Interactive ER diagram editor with Python backend and browser frontend
**Researched:** 2026-03-16
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| **@joint/core** (JointJS open-source) | 4.2.4 | Diagram rendering, drag&drop, SVG canvas | Dependency-free since v4.0 (no jQuery/Backbone/Lodash). CDN-ready via jsDelivr. Native support for ports, embedding/grouping, custom shapes. MPL 2.0 license. Only credible option that works without build tools AND handles ER diagrams natively. |
| **libcst** | 1.8.6 | Python CST parsing and round-trip code generation | The only maintained Python CST library that preserves comments, whitespace, and formatting byte-for-byte. Used by Instagram/Meta at scale. Supports Python 3.0-3.14. Visitor/Transformer pattern makes SQLAlchemy model extraction clean. |
| **FastAPI** | 0.135.1 | Local HTTP server for API between frontend and backend | Already in LAIF stack. Lightweight, async, auto-generates OpenAPI docs. Perfect for local tool: `fastapi dev server.py` with auto-reload. Requires Python 3.10+. |
| **uvicorn** | 0.34.x | ASGI server for FastAPI | Standard FastAPI server. Included with `pip install fastapi[standard]`. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **pydantic** | 2.x | Data models for API request/response and intermediate representation | Comes with FastAPI. Use for the IR (intermediate representation) between parsed CST and frontend JSON. Type-safe serialization of table/column/relationship structures. |
| **python-multipart** | 0.x | File upload handling | For the `model.py` file upload endpoint. Included in `fastapi[standard]`. |

### Frontend (CDN, no build)

| Library | CDN URL | Purpose | Notes |
|---------|---------|---------|-------|
| **@joint/core** | `https://cdn.jsdelivr.net/npm/@joint/core@4.2.4/dist/joint.min.js` | Diagram engine | UMD bundle, access via `joint` global. ~400KB minified. |
| **@joint/core CSS** | `https://cdn.jsdelivr.net/npm/@joint/core@4.2.4/dist/joint.min.css` | JointJS styles | Required for proper rendering. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **fastapi dev** | Auto-reload dev server | `fastapi dev server.py` -- watches for changes, reloads automatically |
| **Browser DevTools** | Frontend debugging | No special tooling needed -- vanilla JS is directly debuggable |

## Installation

```bash
# Python dependencies (entire backend)
pip install fastapi[standard] libcst

# That's it. No npm, no build step.
# Frontend loads from CDN via script tags in HTML.
```

### Minimal `requirements.txt`

```
fastapi[standard]>=0.135.0,<1.0
libcst>=1.8.0,<2.0
```

### Frontend HTML includes

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@joint/core@4.2.4/dist/joint.min.css">
<script src="https://cdn.jsdelivr.net/npm/@joint/core@4.2.4/dist/joint.min.js"></script>
```

## Key Technical Details

### JointJS Open-Source: What's Included vs What's Not

**Included in open-source (sufficient for this project):**
- Custom shape definitions (we define our own ER table shape)
- Ports (connection points on shapes -- used for FK relationships)
- Embedding / nested elements (parent-child hierarchy -- used for table groups)
- Drag & drop of elements on canvas
- Link routing (connections between ports)
- JSON serialization/deserialization of graph state
- Event system (click, double-click, hover on elements)
- SVG-based rendering with full CSS styling control
- foreignObject support (embed HTML inside SVG elements -- useful for edit forms)
- 70+ code examples

**NOT included (JointJS+ only, but we DON'T need these):**
- Stencil palette widget (we build our own simple toolbar)
- Inspector panel (we build a custom property editor)
- Navigator minimap (nice-to-have, not essential for v1)
- Undo/redo CommandManager (we implement undo via re-parse from saved state)
- Export to PNG/SVG/PDF (not needed -- we export to code)
- Auto-layout algorithms (we save positions in `.er.json` sidecar)
- Snaplines, alignment guides (nice UX but not critical)
- Validation engine (we validate in Python backend)

**Assessment:** The open-source version covers all functional requirements. The missing JointJS+ features are UX polish that can be built manually or deferred.

### libcst: Key Patterns for This Project

```python
# Parse preserving everything
import libcst as cst
tree = cst.parse_module(source_code)

# Visit to extract model info (read-only)
class ModelExtractor(cst.CSTVisitor):
    def visit_ClassDef(self, node): ...

# Transform to modify (preserves formatting)
class AddColumn(cst.CSTTransformer):
    def leave_ClassDef(self, original, updated): ...

# Write back -- identical formatting where unchanged
modified_code = tree.code
```

**Critical capability:** `CSTTransformer.leave_*` methods return modified nodes while preserving all whitespace and comments on unchanged nodes. This is what makes round-trip editing work.

### Pan/Zoom Without JointJS+

JointJS open-source provides basic `Paper` scrolling. For pan/zoom:
- **Zoom:** `paper.scale(sx, sy)` with mouse wheel event
- **Pan:** `paper.translate(tx, ty)` with mouse drag on blank area
- These are ~20 lines of vanilla JS event handlers, no plugin needed.

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **JointJS** | **React Flow** | If you already have a React build pipeline. React Flow has better DX for React apps but requires npm/webpack/vite. Incompatible with our no-build constraint. |
| **JointJS** | **Cytoscape.js** | If building a network graph (nodes + edges without ports/shapes). Cytoscape excels at graph analysis and force-directed layouts. Wrong abstraction for structured ER shapes with columns. |
| **JointJS** | **D3.js** | If building custom data visualizations from scratch. D3 is too low-level for diagramming -- you'd rebuild what JointJS gives you. |
| **JointJS** | **GoJS** | If budget allows commercial licensing. GoJS has richer built-in ER support but requires a commercial license ($4k+). |
| **libcst** | **ast module** | Never for this project. `ast` discards comments and formatting -- we'd lose the round-trip guarantee. |
| **libcst** | **RedBaron** | Never. Unmaintained since 2019. libcst is its spiritual successor. |
| **libcst** | **parso** | If you only need parsing without transformation. parso (used by jedi) is read-only focused. libcst's Transformer pattern is essential for our write-back requirement. |
| **FastAPI** | **Flask** | If you want synchronous simplicity. Flask works fine for a local tool but FastAPI gives auto-OpenAPI docs, type validation, and async support at zero extra cost. LAIF already standardizes on FastAPI. |
| **FastAPI** | **http.server** | If you want zero dependencies. stdlib http.server works for serving static files but building a REST API on it is painful. FastAPI is worth the dependency. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **`jointjs` npm package** | Deprecated legacy name (stuck at v3.7.7). The project moved to `@joint/core` | `@joint/core` via CDN |
| **jQuery / Backbone / Lodash** | JointJS 4.0 removed all external dependencies. Loading these is dead weight. | Nothing -- JointJS 4.x is self-contained |
| **Any JS build tool** (webpack, vite, rollup) | Project constraint: portable folder, no build step. CDN + vanilla JS is the correct approach. | `<script>` tags from jsDelivr CDN |
| **ast module** for code manipulation | Loses all comments and formatting. Violates the core round-trip requirement. | libcst |
| **Regular expressions** for Python parsing | Fragile, breaks on edge cases (multiline strings, decorators, nested classes). | libcst |
| **mxGraph** | Predecessor of draw.io, technically deprecated in favor of maxGraph. Community fragmented. | JointJS |
| **jsPlumb** | Good for flow connectors but weak on structured shapes (table-like elements with columns). No built-in embedding/grouping. | JointJS |

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| @joint/core 4.2.4 | Any modern browser (ES2015+) | No external dependencies since 4.0 |
| libcst 1.8.6 | Python 3.9+ | Parses Python 3.0-3.14 syntax |
| FastAPI 0.135.1 | Python 3.10+ | FastAPI requires 3.10+, this is the binding constraint |
| uvicorn 0.34.x | Python 3.10+ | Included with fastapi[standard] |

**Python version constraint:** Use Python 3.10+ (FastAPI requirement). libcst supports 3.9+ so no conflict.

## Confidence Assessment

| Technology | Confidence | Reason |
|------------|------------|--------|
| JointJS open-source | HIGH | Verified: v4.2.4 on jsDelivr, dependency-free, ports + embedding confirmed in official docs. CDN usage documented. |
| libcst | HIGH | Verified: v1.8.6 on PyPI, actively maintained by Meta, round-trip preservation is its core design goal. |
| FastAPI | HIGH | Verified: v0.135.1, already in LAIF stack, well-understood. |
| No-build frontend approach | HIGH | Verified: JointJS 4.x officially supports UMD via CDN with `joint` global variable. |

## Sources

- [JointJS official comparison page](https://www.jointjs.com/comparison) -- open-source vs JointJS+ feature breakdown
- [JointJS v4.0 release blog](https://www.jointjs.com/blog/introducing-version-4) -- dependency-free announcement
- [JointJS docs: Containers & Grouping](https://docs.jointjs.com/learn/features/containers-and-grouping/) -- embedding/nesting in open-source
- [JointJS docs: Element API](https://docs.jointjs.com/api/dia/Element/) -- ports, embeds, parent properties
- [JointJS docs: JavaScript integration](https://docs.jointjs.com/learn/integration/javascript/) -- CDN script tag usage
- [@joint/core on jsDelivr](https://www.jsdelivr.com/package/npm/@joint/core) -- CDN availability, v4.2.4
- [@joint/core on npm](https://www.npmjs.com/package/@joint/core) -- v4.2.4, latest release
- [libcst on PyPI](https://pypi.org/project/libcst/) -- v1.8.6, Python 3.9+
- [libcst on GitHub](https://github.com/Instagram/LibCST) -- Meta/Instagram maintained
- [libcst documentation](https://libcst.readthedocs.io/) -- Visitor/Transformer patterns
- [FastAPI on PyPI](https://pypi.org/project/fastapi/) -- v0.135.1, Python 3.10+
- [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/) -- current features

---
*Stack research for: ER diagram editor (local Python tool with browser frontend)*
*Researched: 2026-03-16*
