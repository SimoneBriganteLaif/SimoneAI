// app.js - Main entry point for ER Editor
// Wires schema fetch, graph building, layout persistence, and collapse toggle
(function() {
    'use strict';

    // State
    var _elements = {};     // className -> JointJS element
    var _linkMap = {};      // "ParentClass->ChildClass" -> JointJS link
    var _saveTimeout = null;
    var SAVE_DEBOUNCE = 1000;

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

            document.title = 'ER Editor - ' + (schema.file || 'model.py');

            if (!schema.tables || schema.tables.length === 0) {
                hideLoading();
                showEmpty();
                return;
            }

            // 2. Fetch saved layout
            var layoutRes = await fetch('/api/layout');
            var layout = layoutRes.ok ? await layoutRes.json() : { positions: {}, collapsed: {}, viewport: {}, vertices: {} };

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
            var tableByTableName = {};
            schema.tables.forEach(function(t) {
                var fullName = t.schema ? t.schema + '.' + t.table_name : t.table_name;
                tableByTableName[fullName] = t.class_name;
                tableByTableName[t.table_name] = t.class_name;
            });

            var linksCreated = {};
            // Build a map from element ID to class name for reverse lookup
            var idToClass = {};
            Object.keys(_elements).forEach(function(className) {
                idToClass[_elements[className].id] = className;
            });

            schema.tables.forEach(function(tableData) {
                tableData.columns.forEach(function(col) {
                    if (col.foreign_key) {
                        var parts = col.foreign_key.split('.');
                        var refTableKey;
                        if (parts.length === 3) {
                            refTableKey = parts[0] + '.' + parts[1];
                        } else if (parts.length === 2) {
                            refTableKey = parts[0];
                        }
                        var refClassName = tableByTableName[refTableKey];
                        if (refClassName && _elements[refClassName] && _elements[tableData.class_name]) {
                            var linkKey = refClassName + '->' + tableData.class_name;
                            var reverseLinkKey = tableData.class_name + '->' + refClassName;
                            if (!linksCreated[linkKey] && !linksCreated[reverseLinkKey]) {
                                var sourceId = _elements[refClassName].id;
                                var targetId = _elements[tableData.class_name].id;

                                // Restore saved vertices if any
                                var savedVerts = (layout.vertices && layout.vertices[linkKey]) || null;

                                var link = ERShapes.createLink(sourceId, targetId, '1', 'N', savedVerts);
                                graph.addCell(link);
                                _linkMap[linkKey] = link;
                                linksCreated[linkKey] = true;
                            }
                        }
                    }
                });
            });

            // 6. Apply layout
            if (!hasPositions) {
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

            // 10. Link tools on hover — allow dragging vertices
            setupLinkTools(paper);

            // 11. Auto-save on changes
            graph.on('change:position', function() {
                scheduleSave();
            });
            graph.on('change:vertices', function() {
                scheduleSave();
            });

            // 12. Double-click to toggle collapse
            paper.on('element:pointerdblclick', function(elementView) {
                var el = elementView.model;
                var currentCollapsed = el.get('collapsed') || false;
                ERShapes.updateTable(el, paper, !currentCollapsed);
                scheduleSave();
            });

        } catch (err) {
            console.error('ER Editor init error:', err);
            if (err instanceof TypeError && err.message.includes('fetch')) {
                showError('Cannot reach the server. Make sure server.py is running.');
            } else {
                showError('Initialization error: ' + err.message);
            }
        }
    }

    /**
     * Show link editing tools (vertex handles) on hover.
     * Users can click to add vertices and drag them for manual routing.
     */
    function setupLinkTools(paper) {
        paper.on('link:mouseenter', function(linkView) {
            if (linkView._hasTools) return;
            var tools = new joint.dia.ToolsView({
                tools: [
                    new joint.linkTools.Vertices(),
                    new joint.linkTools.Segments()
                ]
            });
            linkView.addTools(tools);
            linkView._hasTools = true;
        });

        paper.on('link:mouseleave', function(linkView) {
            linkView.removeTools();
            linkView._hasTools = false;
        });
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

        // Save link vertices
        var vertices = {};
        Object.entries(_linkMap).forEach(function(entry) {
            var key = entry[0];
            var link = entry[1];
            var verts = link.vertices();
            if (verts && verts.length > 0) {
                vertices[key] = verts;
            }
        });

        var viewport = ERCanvas.getViewport();

        try {
            await fetch('/api/layout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    positions: positions,
                    collapsed: collapsed,
                    viewport: viewport,
                    vertices: vertices
                })
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

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', main);
    } else {
        main();
    }
})();
