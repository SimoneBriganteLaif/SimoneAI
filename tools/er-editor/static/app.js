// app.js - Main entry point for ER Editor
// Wires schema fetch, graph building, layout persistence, and collapse toggle
(function() {
    'use strict';

    // State
    var _elements = {};     // className -> JointJS element
    var _linkMap = {};      // "ParentClass->ChildClass" -> JointJS link

    // Expose for editor.js relationship CRUD
    window._elements = _elements;
    window._linkMap = _linkMap;
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

            // 12. Chevron click to toggle collapse + addCol icon click + preview wiring
            paper.on('element:pointerclick', function(elementView, evt) {
                var target = evt.target;
                // Check if click was on chevron hit area
                if (target.getAttribute && (
                    target.getAttribute('joint-selector') === 'chevronHit' ||
                    target.getAttribute('joint-selector') === 'chevronPath' ||
                    (target.parentNode && target.parentNode.getAttribute && target.parentNode.getAttribute('joint-selector') === 'chevronIcon')
                )) {
                    var el = elementView.model;
                    var currentCollapsed = el.get('collapsed') || false;
                    ERShapes.updateTable(el, paper, !currentCollapsed);
                    scheduleSave();
                    evt.stopPropagation();
                    return;
                }
                // Check if click was on addCol icon
                if (target.getAttribute && (
                    target.getAttribute('joint-selector') === 'addColHit' ||
                    target.getAttribute('joint-selector') === 'addColPath'
                )) {
                    if (EREditor && EREditor.addColumn) {
                        EREditor.addColumn(elementView.model);
                    }
                    evt.stopPropagation();
                    return;
                }
                // Wire selection to preview
                var tableData = elementView.model.get('tableData');
                if (tableData && tableData.class_name) {
                    ERPreview.setSelectedTable(tableData.class_name);
                }
            });

            // 13. Double-click for inline table rename
            paper.on('element:pointerdblclick', function(elementView, evt) {
                var el = elementView.model;
                if (el.get('type') === 'er.Group') return;
                startInlineRename(el, paper);
            });

            // 14. Blank click clears preview selection
            paper.on('blank:pointerclick', function() {
                ERPreview.clearSelectedTable();
            });

            // 15. Group right-click handler
            paper.on('element:contextmenu', function(elementView, evt) {
                if (elementView.model.get('type') === 'er.Group') {
                    evt.preventDefault();
                    ERGroups.showContextMenu(elementView.model, evt.clientX, evt.clientY);
                }
            });

            // 16. Initialize Phase 2 modules
            EREditor.init(schema);
            ERGroups.init(_elements, scheduleSave);
            ERPreview.init();

            // 17. Load groups from layout
            if (layout.groups && layout.groups.length > 0) {
                ERGroups.loadGroups(layout.groups, _elements);
            }

            // 18. Register delete handler
            document.addEventListener('er:delete-selected', function() {
                deleteSelectedTable();
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

    function startInlineRename(el, paper) {
        var tableData = el.get('tableData');
        var oldClassName = tableData.class_name;
        var oldTableName = tableData.table_name;
        var view = el.findView(paper);

        // Find the header rect to position over it
        var headerRect = view.el.querySelector('rect[joint-selector="headerRect"]');
        if (!headerRect) return;

        var hRect = headerRect.getBoundingClientRect();
        var input = document.createElement('input');
        input.type = 'text';
        input.className = 'er-inline-edit';
        input.value = oldClassName;
        input.style.position = 'fixed';
        input.style.left = (hRect.left + 28) + 'px';
        input.style.top = hRect.top + 'px';
        input.style.width = (hRect.width - 56) + 'px';
        input.style.height = hRect.height + 'px';
        input.style.textAlign = 'center';
        input.style.zIndex = '300';
        input.style.background = '#374151';
        input.style.color = '#ffffff';
        input.style.fontSize = '13px';
        input.style.fontWeight = '600';
        input.style.fontFamily = '"JetBrains Mono", "Fira Code", "SF Mono", "Consolas", monospace';
        input.style.border = 'none';
        input.style.outline = '2px solid #3b82f6';
        input.style.borderRadius = '4px 4px 0 0';
        input.style.padding = '0 4px';
        document.body.appendChild(input);
        input.select();

        var committed = false;

        function commit() {
            if (committed) return;
            committed = true;
            var newClassName = input.value.trim();
            if (!newClassName || newClassName === oldClassName) {
                input.remove();
                return;
            }
            // Auto-generate tablename
            var newTableName = ERToolbar.toSnakeCasePlural(newClassName);

            var cmd = {
                execute: function() {
                    tableData.class_name = newClassName;
                    tableData.table_name = newTableName;
                    // Update elements map
                    delete _elements[oldClassName];
                    _elements[newClassName] = el;
                    el.set('tableData', tableData);
                    // Update header text
                    var headerLabel = tableData.schema
                        ? newClassName + ' (' + tableData.schema + '.' + newTableName + ')'
                        : newClassName + ' (' + newTableName + ')';
                    el.attr('headerText/text', headerLabel);
                    EREditor.markDirty();
                    ERPreview.scheduleRefresh();
                },
                undo: function() {
                    tableData.class_name = oldClassName;
                    tableData.table_name = oldTableName;
                    delete _elements[newClassName];
                    _elements[oldClassName] = el;
                    el.set('tableData', tableData);
                    var headerLabel = tableData.schema
                        ? oldClassName + ' (' + tableData.schema + '.' + oldTableName + ')'
                        : oldClassName + ' (' + oldTableName + ')';
                    el.attr('headerText/text', headerLabel);
                    EREditor.markDirty();
                    ERPreview.scheduleRefresh();
                }
            };
            ERUndo.execute(cmd);
            input.remove();
        }

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); commit(); }
            if (e.key === 'Escape') { e.preventDefault(); input.remove(); committed = true; }
        });
        input.addEventListener('blur', commit);
    }

    function deleteSelectedTable() {
        var selected = ERCanvas.getSelectedElement();
        if (!selected || selected.get('type') !== 'er.Table') return;

        var tableData = selected.get('tableData');
        var className = tableData.class_name;
        var msg = 'Delete table "' + className + '"? This removes the class and all its columns and relationships.';

        EREditor.showConfirmation(selected, msg, function() {
            var el = selected;
            var pos = el.position();

            var cmd = {
                execute: function() {
                    ERCanvas.getGraph().removeCells([el]);
                    delete _elements[className];
                    EREditor.trackDeletion(className);
                    var tables = EREditor.getSchema().tables;
                    var idx = tables.findIndex(function(t) { return t.class_name === className; });
                    if (idx >= 0) tables.splice(idx, 1);
                    EREditor.markDirty();
                    ERPreview.scheduleRefresh();
                },
                undo: function() {
                    ERCanvas.getGraph().addCell(el);
                    el.position(pos.x, pos.y);
                    _elements[className] = el;
                    EREditor.untrackDeletion(className);
                    EREditor.getSchema().tables.push(tableData);
                    EREditor.markDirty();
                    ERPreview.scheduleRefresh();
                }
            };
            ERUndo.execute(cmd);
            ERCanvas.deselectAll();
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
        var groups = (typeof ERGroups !== 'undefined' && ERGroups.getGroupsData) ? ERGroups.getGroupsData() : [];

        try {
            await fetch('/api/layout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    positions: positions,
                    collapsed: collapsed,
                    viewport: viewport,
                    vertices: vertices,
                    groups: groups
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
