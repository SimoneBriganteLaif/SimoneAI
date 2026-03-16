# Pitfalls Research

**Domain:** ER diagram editor with round-trip code generation (SQLAlchemy model.py)
**Researched:** 2026-03-16
**Confidence:** HIGH (libcst, JointJS well-documented; round-trip editing patterns well-known)

## Critical Pitfalls

### Pitfall 1: JointJS Open-Source Missing Essential Editor Features

**What goes wrong:**
JointJS open-source (MPL 2.0) lacks features that feel "basic" in a diagram editor but are only available in the commercial JointJS+ package. The following are **not included** in the open-source version:

- **CommandManager** (undo/redo) -- no history tracking at all
- **PaperScroller** (zoom/pan with inertia, auto-resize)
- **Keyboard plugin** (keyboard shortcuts)
- **Clipboard** (copy/paste)
- **Snaplines** (alignment guides)
- **Navigator** (minimap)
- **Selection/Halo** (multi-select with control panels)
- **Inspector** (property editor panel)
- **Stencil** (drag-from-palette)
- **ContextToolbar/Tooltip** components
- **Export** (PNG, SVG, print)

You start building, everything works for basic drag-and-drop, then realize Ctrl+Z does nothing, zoom requires custom code, and there is no property panel widget. Reimplementing these from scratch can take more time than the core diagram logic.

**Why it happens:**
JointJS markets the open-source version for "basic demo applications." The feature comparison page makes this clear, but developers often discover it too late after committing to the library.

**How to avoid:**
1. Accept upfront that you will build undo/redo, zoom/pan, and keyboard shortcuts yourself
2. Budget explicit development time for each missing feature
3. Implement undo/redo by listening to `graph` change events and maintaining a manual command stack (before/after JSON snapshots)
4. Implement zoom via `paper.scale()` and pan via `paper.translate()` with mouse wheel/drag handlers
5. Keep the scope minimal: only build what the ER editor actually needs (no minimap, no stencil -- tables are created via UI buttons, not drag-from-palette)

**Warning signs:**
- You find yourself searching "JointJS undo redo" and all results point to `CommandManager` docs under JointJS+
- Feature requests pile up that all map to JointJS+ components
- Users complain about missing standard editor interactions (Ctrl+Z, mouse wheel zoom)

**Phase to address:**
Phase 1 (core editor). Must decide upfront which JointJS+ features to reimplement and budget accordingly. Undo/redo and zoom/pan are MVP-critical.

---

### Pitfall 2: libcst original_node vs updated_node Confusion

**What goes wrong:**
In a `CSTTransformer`, the `leave_*` methods receive both `original_node` and `updated_node`. Returning modifications based on `original_node` silently **discards all changes made to child nodes** deeper in the tree. The code appears to work on simple cases but breaks when multiple nested transformations are needed.

Example: you modify a column annotation inside a class body. If the `leave_ClassDef` method returns a change based on `original_node` instead of `updated_node`, the column annotation change vanishes. No error is raised -- the output just has stale data.

**Why it happens:**
LibCST trees are immutable. By the time `leave_ClassDef` is called, `updated_node` already contains modifications from `leave_AnnAssign` (the column). Using `original_node` creates a fresh copy without those child modifications. The naming is counterintuitive: "original" sounds like "the real one" when it is actually "the stale one."

**How to avoid:**
1. **Rule: always modify `updated_node`, never `original_node`** in leave methods
2. Use `original_node` only for comparison (checking if something changed)
3. Write a test that modifies a column inside a class and verifies both changes appear in output
4. Add a code comment at the top of every Transformer: `# IMPORTANT: always use updated_node in leave_* methods`

**Warning signs:**
- Round-trip output is missing some changes but not others
- Changes work when applied individually but not together
- Deeper-nested modifications disappear while parent-level ones persist

**Phase to address:**
Phase 1 (parser/writer). This must be understood before writing any CSTTransformer code. Add a regression test in the first sprint.

---

### Pitfall 3: State Desynchronization Between Visual Model and Data Model

**What goes wrong:**
The diagram state (JointJS graph JSON) and the intermediate data model (parsed from model.py) drift apart. User drags a table, renames a column, deletes a relationship -- each operation updates one representation but not the other, or updates them inconsistently. Eventually the "Save" operation writes corrupted or incomplete model.py because the data model does not match what the user sees.

**Why it happens:**
Two sources of truth exist: the JointJS graph (visual) and the parsed SQLAlchemy model (semantic). Without a strict single-source-of-truth architecture, changes can be applied to one without propagating to the other. This is especially insidious with:
- Undo/redo (visual state reverts but data model does not)
- Relationship editing (link in JointJS vs ForeignKey + relationship() in data model)
- Batch operations (renaming a table must update all FK references)

**How to avoid:**
1. **Single source of truth: the intermediate data model (IR)**. The JointJS graph is always a derived view
2. All user actions modify the IR first, then the JointJS graph is re-rendered/updated from the IR
3. Never let JointJS graph state be the authoritative source for semantic data (table names, column types, FK targets)
4. JointJS graph owns only visual-only properties: position, size, color, group membership
5. On save: serialize IR to model.py via libcst. The JointJS graph is never serialized to model.py
6. Keep a clear separation: `ir.tables[]` is the truth, `graph.getElements()` is the view

**Warning signs:**
- "What you see is not what you save" -- user renames a table but the saved file has the old name
- Deleting a table leaves orphaned foreign keys in the saved output
- Undo restores visual position but not the data change (or vice versa)

**Phase to address:**
Phase 1 (architecture). The IR-as-single-source pattern must be established before any editing features are built. Retrofitting this is a rewrite.

---

### Pitfall 4: libcst Statement Type Mismatches When Adding/Removing Nodes

**What goes wrong:**
In Python's grammar (as modeled by libcst), not all statements are interchangeable. A `SimpleStatementLine` wraps simple statements (assignments, imports, assert), while compound statements (class, if, for) are `BaseCompoundStatement`. If you try to replace one type with another, or insert a node at the wrong level, libcst raises a validation error -- but only at serialization time, not at tree construction time.

For the ER editor specifically: adding a new `class` definition to a module requires constructing a proper `ClassDef` wrapped in the correct parent containers. Adding a new `mapped_column()` assignment requires a `SimpleStatementLine` inside the class body. Getting the wrapping wrong produces cryptic errors.

**Why it happens:**
Libcst faithfully models Python's concrete syntax, including all the wrapper nodes that an AST would hide. Developers used to working with `ast` module expect a flat list of statements and are surprised by the nesting.

**How to avoid:**
1. Build helper functions: `make_class_def(name, bases, body)`, `make_column(name, type, ...)` that handle all the wrapping
2. Use `parse_statement()` to construct nodes from code strings rather than manual node construction -- libcst handles the wrapping automatically
3. Test every node construction helper with `module.code` roundtrip assertions
4. Study the CST structure using `libcst.parse_module(code)` and printing the tree before writing transformers

**Warning signs:**
- `ParserSyntaxError` or validation errors when calling `.code` on the modified tree
- Errors mentioning `SimpleStatementLine` or `IndentedBlock` that seem unrelated to your change
- Code that works for modifying existing nodes but fails when adding new ones

**Phase to address:**
Phase 1 (parser/writer). Build the helper functions as part of the IR-to-CST serialization layer. These are foundational utilities.

---

### Pitfall 5: Whitespace and Formatting Corruption During Round-Trip

**What goes wrong:**
Libcst preserves whitespace byte-for-byte on *unmodified* nodes, but newly constructed nodes get default whitespace. When you insert a new class between two existing classes, the spacing (blank lines between classes, indentation) may not match the file's conventions. Over multiple save cycles, formatting degrades: inconsistent blank lines, wrong indentation levels, trailing whitespace changes.

This is the "round-trip fidelity" promise breaking at the seams -- not on read-modify-write of existing code, but on *additions*.

**Why it happens:**
Libcst does not have a "match surrounding style" feature. New nodes use `MaybeSentinel.DEFAULT` or `SimpleWhitespace(" ")` defaults. The developer must explicitly set `leading_lines`, `lines_after_decorators`, `EmptyLine()` nodes, etc. to match the file's existing conventions.

**How to avoid:**
1. Analyze the existing file's whitespace conventions before inserting: count blank lines between classes, check indentation style
2. Build a `WhitespaceConvention` detector that runs once on parse and is passed to all node-construction helpers
3. For new class definitions: copy the `leading_lines` pattern from adjacent existing classes
4. Always diff the output file against the original to verify no unintended whitespace changes
5. Include a "formatting preservation" test: parse a file, modify it, save, and verify that unmodified sections are byte-identical

**Warning signs:**
- `git diff` shows whitespace-only changes in lines you did not edit
- New classes have different spacing than existing ones
- Blank lines accumulate or disappear after repeated save cycles

**Phase to address:**
Phase 2 (editing features). Once basic parse/write works, add whitespace convention detection before implementing "add table" feature.

---

### Pitfall 6: Relationship Modeling Complexity Explosion

**What goes wrong:**
SQLAlchemy relationships involve multiple interconnected pieces: `ForeignKey` on the child column, `relationship()` on the parent (and optionally child via `back_populates`), cascade options, lazy loading strategy, and potentially association tables for many-to-many. The ER editor must keep all of these in sync. Deleting a relationship means removing the FK column, both relationship() declarations, and possibly an association table. Renaming a table means updating every `ForeignKey("old_table.id")` string reference.

Developers underestimate this because a simple FK looks easy, but the full matrix of operations (add/remove/rename table, add/remove/rename FK column, add/remove relationship with back_populates) creates combinatorial complexity.

**Why it happens:**
In code, these are just strings and function calls scattered across multiple classes. The visual representation (a line between two boxes) hides the underlying complexity. The IR must model all the interconnections, and every mutation must cascade correctly.

**How to avoid:**
1. Model relationships as first-class entities in the IR, not as properties of tables
2. Each relationship in the IR holds references to: source table, target table, FK column, relationship() on both sides, cascade config
3. All mutations go through relationship-aware methods: `ir.rename_table(old, new)` automatically updates all FK string references
4. Build a validation pass that runs before serialization: check that every FK references an existing table/column, every back_populates has a matching counterpart
5. Start with one-to-many only. Add many-to-many (association tables) as a separate feature

**Warning signs:**
- Renaming a table breaks FK references in other tables
- Deleting a table leaves orphaned relationship() declarations
- back_populates references become stale after renames

**Phase to address:**
Phase 2-3 (relationship editing). One-to-many in Phase 2, many-to-many deferred. The IR data structure must support relationships from Phase 1 even if editing comes later.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Store semantic data in JointJS cell attributes | Quick to implement, one data store | Couples view to model, makes headless testing impossible, sync bugs | Never -- always use separate IR |
| Use regex instead of libcst for simple extractions | Faster to write for known patterns | Breaks on edge cases (multiline, comments, decorators), cannot round-trip | Never for write operations; acceptable for initial file detection/validation only |
| Skip undo/redo in MVP | Saves significant development time | Users will lose work, fundamental UX expectation for any editor | Acceptable for internal alpha only, must add before any external use |
| Serialize entire model.py on every change | Simple save logic | Slow on large files (13+ models), risk of data loss on concurrent edits | Acceptable for v1 (single user, local tool) |
| Hardcode whitespace conventions | Avoids building detection logic | Breaks on files with different formatting styles | Acceptable for v1 if all LAIF files follow same conventions |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| libcst parse | Parsing file with syntax errors crashes with unhelpful error | Wrap in try/except, show user-friendly error with line number. Validate file parses before opening editor |
| libcst write | Calling `.code` on tree with invalid structure gives cryptic error | Build nodes using `parse_statement()` helpers, validate tree before serialization |
| JointJS links + ports | Creating links without ports makes reconnection unreliable | Define ports on every table element (in-port, out-port per FK column), use port-based links |
| JointJS embedded elements | Moving parent does not always correctly reposition embedded children when custom shapes are used | Test embedding with actual custom shapes early, not just with built-in shapes |
| Sidecar .er.json | Saving positions but not validating against current model.py | On load, validate that every table in .er.json exists in model.py. Ignore stale entries, use default positions for new tables |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Re-rendering entire JointJS graph on every IR change | Visible flicker, slow response to edits | Use targeted cell updates (`cell.set()`, `cell.remove()`) not full graph rebuild | >20 tables with relationships |
| Parsing model.py on every save | Noticeable delay (100ms+) on large files | Parse once on load, maintain IR in memory, serialize only on explicit save | >500 lines / 13+ models |
| SVG DOM bloat from complex table shapes | Scroll/zoom becomes jerky | Keep table SVG markup minimal, avoid nested foreignObject HTML | >30 tables rendered simultaneously |
| Unthrottled graph change events | Multiple rapid updates cause cascading re-renders | Debounce change handlers (50-100ms), use batch operations | Any interactive drag/resize operation |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Executing parsed Python code from model.py | Arbitrary code execution if model.py contains malicious code | libcst is parse-only, never use `exec()` or `eval()`. This is inherently safe with CST approach |
| Serving the editor on 0.0.0.0 | Network-accessible file editor | Default to 127.0.0.1 (localhost only). Document this clearly in setup instructions |
| No file backup before overwrite | User loses original model.py on buggy save | Write to `.model.py.bak` before overwriting. Atomic write (write to temp, then rename) |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No visual feedback on unsaved changes | User closes browser, loses all edits | Show "unsaved changes" indicator, warn on page close via `beforeunload` |
| Tiny click targets for relationship lines | Impossible to select/delete relationships on complex diagrams | Add invisible wider hit area on links (12px stroke-width transparent overlay), or use vertex markers |
| No way to see the generated code before saving | User fears the tool will corrupt their file | Add a "Preview changes" diff view showing before/after |
| Cramped table display with many columns | Tables become unreadably tall, overlap each other | Collapsible column sections, show only name + type by default, expand on click |
| Pan/zoom resets on page reload | User loses their carefully arranged viewport | Persist viewport state in .er.json alongside table positions |
| No keyboard navigation | Power users (developers) expect keyboard shortcuts | At minimum: Delete key to remove selected, Escape to deselect, Ctrl+S to save |
| Relationship cardinality unclear | User cannot tell if a relationship is one-to-many or many-to-many | Show crow's foot notation or 1..* labels on link endpoints |

## "Looks Done But Isn't" Checklist

- [ ] **Table rename:** Often missing FK string reference updates in other tables -- verify all `ForeignKey("table.col")` strings are updated
- [ ] **Column delete:** Often missing relationship() cleanup -- verify relationship declarations referencing deleted column are removed
- [ ] **Relationship display:** Often missing back_populates pairing -- verify both sides of relationship are shown and editable
- [ ] **File save:** Often missing comment preservation -- verify comments above/inline with modified code survive the round-trip
- [ ] **Import parsing:** Often missing `from typing import Optional` and similar imports -- verify type annotations in Mapped[] are correctly parsed
- [ ] **Group persistence:** Often missing group membership save -- verify groups survive page reload via .er.json
- [ ] **Empty file handling:** Often missing edge case for model.py with no classes -- verify editor loads empty state gracefully
- [ ] **Decorator preservation:** Often missing @declared_attr or custom decorators -- verify decorators are preserved on round-trip

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| State desync (visual vs data) | MEDIUM | Force full re-render from IR; add IR-to-graph consistency check |
| Whitespace corruption | LOW | Re-format file with black/ruff; fix convention detector |
| Lost undo history | LOW | Undo history is in-memory only; acceptable to lose on page reload |
| Corrupted model.py save | LOW | Restore from .model.py.bak backup file |
| JointJS+ feature needed | HIGH | Reimplement from scratch or purchase license (~$2,930). Evaluate early |
| Relationship data inconsistency | MEDIUM | Run validation pass on IR, auto-fix orphaned references, show warnings to user |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| JointJS missing features (undo, zoom, keyboard) | Phase 1 - Core editor | Manual test: Ctrl+Z works, mouse wheel zooms, Delete removes selected |
| original_node vs updated_node | Phase 1 - Parser/writer | Unit test: modify column inside class, verify both changes in output |
| State desynchronization | Phase 1 - Architecture | Integration test: modify via UI, save, reload, verify consistency |
| Statement type mismatches | Phase 1 - Parser helpers | Unit test: add new class to module, add new column to class, roundtrip |
| Whitespace corruption | Phase 2 - Editing features | Diff test: modify file, verify unmodified sections are byte-identical |
| Relationship complexity | Phase 2-3 - Relationship editing | Integration test: rename table, verify all FK references updated |
| UX pitfalls (unsaved indicator, click targets) | Phase 2 - Editor UX polish | Manual QA checklist |
| File backup on save | Phase 1 - Save logic | Verify .bak file exists after save |

## Sources

- [JointJS vs JointJS+ comparison](https://www.jointjs.com/comparison) -- definitive feature split between open-source and commercial
- [JointJS embedding/hierarchy docs](https://resources.jointjs.com/tutorial/hierarchy) -- embedding behavior and limitations
- [JointJS nested elements issue #427](https://github.com/clientIO/joint/issues/427) -- link routing with nested elements
- [LibCST best practices](https://github.com/Instagram/LibCST/blob/main/docs/source/best_practices.rst) -- original_node vs updated_node, matchers
- [LibCST tutorial](https://libcst.readthedocs.io/en/latest/tutorial.html) -- CST traversal and modification
- [LibCST whitespace issue #1118](https://github.com/Instagram/LibCST/issues/1118) -- whitespace validation gotchas
- [Preserving comments in round-trip editing](https://jayconrod.com/posts/129/preserving-comments-when-parsing-and-formatting-code) -- general round-trip challenges
- [Refactoring with LibCST (SeatGeek)](https://chairnerd.seatgeek.com/refactoring-python-with-libcst/) -- practical transformer pitfalls
- [Refactoring with LibCST (Instawork)](https://engineering.instawork.com/refactoring-a-python-codebase-with-libcst-fc645ecc1f09) -- real-world experience

---
*Pitfalls research for: ER diagram editor with round-trip SQLAlchemy code generation*
*Researched: 2026-03-16*
