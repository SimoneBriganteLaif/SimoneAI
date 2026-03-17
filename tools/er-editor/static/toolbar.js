// toolbar.js - Toolbar event handlers for ER Editor
// Exposes: window.ERToolbar
(function() {
    'use strict';

    var _elements = {};  // className -> JointJS element mapping
    var _onLayoutChange = null;  // callback for persistence

    function init(elements, onLayoutChange) {
        _elements = elements;
        _onLayoutChange = onLayoutChange;

        // Fit All
        document.getElementById('btn-fit-all').addEventListener('click', function() {
            ERCanvas.fitAll();
        });

        // Re-layout
        document.getElementById('btn-relayout').addEventListener('click', function() {
            ERLayout.autoLayout(ERCanvas.getGraph());
            ERCanvas.fitAll();
            if (_onLayoutChange) _onLayoutChange();
        });

        // Zoom In / Out
        document.getElementById('btn-zoom-in').addEventListener('click', function() {
            ERCanvas.zoomIn();
        });
        document.getElementById('btn-zoom-out').addEventListener('click', function() {
            ERCanvas.zoomOut();
        });

        // Collapse All
        document.getElementById('btn-collapse-all').addEventListener('click', function() {
            var paper = ERCanvas.getPaper();
            Object.values(_elements).forEach(function(el) {
                if (!el.get('collapsed')) {
                    ERShapes.updateTable(el, paper, true);
                }
            });
            if (_onLayoutChange) _onLayoutChange();
        });

        // Expand All
        document.getElementById('btn-expand-all').addEventListener('click', function() {
            var paper = ERCanvas.getPaper();
            Object.values(_elements).forEach(function(el) {
                if (el.get('collapsed')) {
                    ERShapes.updateTable(el, paper, false);
                }
            });
            if (_onLayoutChange) _onLayoutChange();
        });

        // Search
        var searchTimeout = null;
        var searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                handleSearch(searchInput.value.trim());
            }, 200);  // 200ms debounce per UI-SPEC
        });

        // --- Phase 2: + Table ---
        document.getElementById('btn-add-table').addEventListener('click', function() {
            addTable();
        });

        // --- Phase 2: + Group ---
        document.getElementById('btn-add-group').addEventListener('click', function() {
            ERGroups.startDraw();
        });

        // --- Phase 2: Save ---
        document.getElementById('btn-save').addEventListener('click', function() {
            EREditor.save();
        });

        // --- Phase 2: Undo/Redo ---
        var undoBtn = document.getElementById('btn-undo');
        var redoBtn = document.getElementById('btn-redo');
        undoBtn.addEventListener('click', function() { ERUndo.undo(); });
        redoBtn.addEventListener('click', function() { ERUndo.redo(); });

        // Update undo/redo button state on stack change
        ERUndo.onChange(function() {
            undoBtn.disabled = !ERUndo.canUndo();
            redoBtn.disabled = !ERUndo.canRedo();
        });

        // --- Phase 2: Code Preview toggle ---
        document.getElementById('btn-preview').addEventListener('click', function() {
            ERPreview.toggle();
        });

        // Enable toolbar buttons (they start disabled during loading)
        document.querySelectorAll('.toolbar-btn').forEach(function(btn) {
            btn.removeAttribute('disabled');
        });
        // Re-disable undo/redo if stacks empty
        undoBtn.disabled = !ERUndo.canUndo();
        redoBtn.disabled = !ERUndo.canRedo();
    }

    function toSnakeCasePlural(name) {
        // CamelCase -> snake_case: split on uppercase boundaries
        var snake = name.replace(/([a-z0-9])([A-Z])/g, '$1_$2')
                        .replace(/([A-Z])([A-Z][a-z])/g, '$1_$2')
                        .toLowerCase();
        // Simple pluralize: add 's', handle 'y' -> 'ies', 's' -> 'ses'
        if (snake.endsWith('y') && !snake.endsWith('ay') && !snake.endsWith('ey') && !snake.endsWith('oy') && !snake.endsWith('uy')) {
            return snake.slice(0, -1) + 'ies';
        }
        if (snake.endsWith('s') || snake.endsWith('x') || snake.endsWith('z') || snake.endsWith('ch') || snake.endsWith('sh')) {
            return snake + 'es';
        }
        return snake + 's';
    }

    function addTable() {
        var paper = ERCanvas.getPaper();
        var graph = ERCanvas.getGraph();

        // Default table at center of viewport
        var paperSize = paper.getComputedSize();
        var scale = paper.scale().sx;
        var translate = paper.translate();
        var centerX = (paperSize.width / 2 - translate.tx) / scale;
        var centerY = (paperSize.height / 2 - translate.ty) / scale;

        // Generate unique name
        var baseName = 'NewTable';
        var counter = 1;
        var className = baseName;
        while (_elements[className]) {
            className = baseName + counter;
            counter++;
        }

        var tableName = toSnakeCasePlural(className);

        var tableData = {
            class_name: className,
            table_name: tableName,
            schema: null,
            columns: [
                { name: 'id', type: 'Integer', nullable: false, primary_key: true, foreign_key: null, unique: false, index: false, default: null, server_default: null }
            ],
            relationships: []
        };

        var el = ERShapes.createTable(tableData, { x: centerX - 120, y: centerY - 50 }, false);

        // Wrap in undo command
        var cmd = {
            execute: function() {
                graph.addCell(el);
                _elements[className] = el;
                EREditor.getSchema().tables.push(tableData);
                EREditor.markDirty();
                ERPreview.scheduleRefresh();
            },
            undo: function() {
                graph.removeCells([el]);
                delete _elements[className];
                var tables = EREditor.getSchema().tables;
                var idx = tables.findIndex(function(t) { return t.class_name === className; });
                if (idx >= 0) tables.splice(idx, 1);
                EREditor.markDirty();
                ERPreview.scheduleRefresh();
            }
        };
        ERUndo.execute(cmd);
        if (_onLayoutChange) _onLayoutChange();
    }

    function handleSearch(query) {
        ERCanvas.deselectAll();
        var noResultsEl = document.getElementById('search-no-results');

        if (!query) {
            // Empty search: restore all
            if (noResultsEl) noResultsEl.style.display = 'none';
            return;
        }

        var lowerQuery = query.toLowerCase();
        var found = null;

        // Search by class_name or table_name
        Object.entries(_elements).forEach(function(entry) {
            var className = entry[0];
            var el = entry[1];
            var tableData = el.get('tableData');
            var matches = className.toLowerCase().includes(lowerQuery) ||
                            tableData.table_name.toLowerCase().includes(lowerQuery);
            if (matches && !found) {
                found = el;
            }
        });

        if (found) {
            if (noResultsEl) noResultsEl.style.display = 'none';
            // Highlight matching table
            ERCanvas.selectElement(found);
            // Pan to center it
            var paper = ERCanvas.getPaper();
            var pos = found.position();
            var size = found.size();
            var paperSize = paper.getComputedSize();
            var scale = paper.scale().sx;
            var centerX = pos.x + size.width / 2;
            var centerY = pos.y + size.height / 2;
            paper.translate(
                paperSize.width / 2 - centerX * scale,
                paperSize.height / 2 - centerY * scale
            );
        } else {
            // No match
            if (noResultsEl) {
                noResultsEl.textContent = 'No tables match "' + query + '"';
                noResultsEl.style.display = 'block';
            }
            // Dim all tables
            var paper = ERCanvas.getPaper();
            ERCanvas.getGraph().getElements().forEach(function(el) {
                var view = el.findView(paper);
                if (view) view.el.style.opacity = '0.3';
            });
        }
    }

    window.ERToolbar = {
        init: init,
        toSnakeCasePlural: toSnakeCasePlural,
        addTable: addTable
    };
})();
