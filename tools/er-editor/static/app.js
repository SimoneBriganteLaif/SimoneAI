// app.js - Main entry point for ER Editor
// Wires schema fetch, graph building, layout persistence, and collapse toggle
(function() {
    'use strict';

    // State
    var _elements = {};     // className -> JointJS element
    var _saveTimeout = null;
    var SAVE_DEBOUNCE = 1000; // 1 second debounce for auto-save

    async function main() {
        try {
            // 1. Fetch schema from API
            var schemaRes = await fetch('/api/schema');
            if (!schemaRes.ok) {
                var err = await schemaRes.json().catch(function() { return { detail: 'Unknown error' }; });
                showError(err.detail || 'Failed to parse model file.');
                return;
            }
            var schema = await schemaRes.json();

            // Set browser tab title
            document.title = 'ER Editor - ' + (schema.file || 'model.py');

            // Check empty state
            if (!schema.tables || schema.tables.length === 0) {
                hideLoading();
                showEmpty();
                return;
            }

            // 2. Fetch saved layout
            var layoutRes = await fetch('/api/layout');
            var layout = layoutRes.ok ? await layoutRes.json() : { positions: {}, collapsed: {}, viewport: {} };

            // 3. Initialize canvas
            var paperEl = document.getElementById('paper');
            var canvas = ERCanvas.init(paperEl);
            var graph = canvas.graph;
            var paper = canvas.paper;

            // 4. Build JointJS elements from schema
            var hasPositions = layout.positions && Object.keys(layout.positions).length > 0;

            schema.tables.forEach(function(tableData) {
                var savedPos = hasPositions && layout.positions[tableData.class_name]
                    ? layout.positions[tableData.class_name]
                    : { x: 0, y: 0 };
                var collapsed = layout.collapsed && layout.collapsed[tableData.class_name] === true;

                var el = ERShapes.createTable(tableData, savedPos, collapsed);
                _elements[tableData.class_name] = el;
                graph.addCell(el);
            });

            // 5. Build relationship links
            // Build FK map: for each table, find columns with foreign_key pointing to another table
            var tableByTableName = {};
            schema.tables.forEach(function(t) {
                var fullName = t.schema ? t.schema + '.' + t.table_name : t.table_name;
                tableByTableName[fullName] = t.class_name;
                // Also register without schema for simpler FK references
                tableByTableName[t.table_name] = t.class_name;
            });

            var linksCreated = {}; // track "srcClass->tgtClass" to avoid duplicates

            schema.tables.forEach(function(tableData) {
                tableData.columns.forEach(function(col) {
                    if (col.foreign_key) {
                        // FK format: "schema.table.column" or "table.column"
                        var parts = col.foreign_key.split('.');
                        var refTableKey;
                        if (parts.length === 3) {
                            // schema.table.column
                            refTableKey = parts[0] + '.' + parts[1];
                        } else if (parts.length === 2) {
                            // table.column
                            refTableKey = parts[0];
                        }
                        var refClassName = tableByTableName[refTableKey];
                        if (refClassName && _elements[refClassName] && _elements[tableData.class_name]) {
                            var linkKey = refClassName + '->' + tableData.class_name;
                            var reverseLinkKey = tableData.class_name + '->' + refClassName;
                            if (!linksCreated[linkKey] && !linksCreated[reverseLinkKey]) {
                                // Determine cardinality:
                                // The FK side is "N" (many), the referenced side is "1"
                                var sourceId = _elements[refClassName].id;  // Referenced (parent) = "1"
                                var targetId = _elements[tableData.class_name].id;  // FK holder (child) = "N"

                                var link = ERShapes.createLink(sourceId, targetId, '1', 'N');
                                graph.addCell(link);
                                linksCreated[linkKey] = true;
                            }
                        }
                    }
                });
            });

            // 6. Apply layout
            if (!hasPositions) {
                // No saved positions: run auto-layout
                ERLayout.autoLayout(graph);
            }

            // 7. Hide loading, show canvas
            hideLoading();

            // 8. Apply saved viewport or fit-all
            if (hasPositions && layout.viewport && layout.viewport.zoom) {
                ERCanvas.applyViewport(layout.viewport);
            } else {
                ERCanvas.fitAll();
            }

            // 9. Initialize toolbar
            ERToolbar.init(_elements, scheduleSave);

            // 10. Set up auto-save on position changes
            graph.on('change:position', function() {
                scheduleSave();
            });

            // 11. Set up double-click to toggle collapse
            paper.on('element:pointerdblclick', function(elementView) {
                var el = elementView.model;
                var currentCollapsed = el.get('collapsed') || false;
                ERShapes.updateTable(el, paper, !currentCollapsed);
                scheduleSave();
            });

        } catch (err) {
            console.error('ER Editor init error:', err);
            showError('Cannot reach the server. Make sure server.py is running.');
        }
    }

    function scheduleSave() {
        clearTimeout(_saveTimeout);
        _saveTimeout = setTimeout(saveLayout, SAVE_DEBOUNCE);
    }

    async function saveLayout() {
        var positions = {};
        var collapsed = {};
        Object.entries(_elements).forEach(function(entry) {
            var className = entry[0];
            var el = entry[1];
            var pos = el.position();
            positions[className] = { x: pos.x, y: pos.y };
            if (el.get('collapsed')) {
                collapsed[className] = true;
            }
        });
        var viewport = ERCanvas.getViewport();

        try {
            await fetch('/api/layout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ positions: positions, collapsed: collapsed, viewport: viewport })
            });
        } catch (err) {
            console.warn('Failed to save layout:', err);
        }
    }

    function hideLoading() {
        var el = document.getElementById('loading-state');
        if (el) el.style.display = 'none';
    }

    function showEmpty() {
        var el = document.getElementById('empty-state');
        if (el) el.style.display = 'flex';
    }

    function showError(message) {
        hideLoading();
        var el = document.getElementById('error-state');
        var msgEl = document.getElementById('error-message');
        if (el) el.style.display = 'flex';
        if (msgEl) msgEl.textContent = message;
    }

    // Start on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', main);
    } else {
        main();
    }
})();
