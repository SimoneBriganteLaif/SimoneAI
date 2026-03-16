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

        // Enable toolbar buttons (they start disabled during loading)
        document.querySelectorAll('.toolbar-btn').forEach(function(btn) {
            btn.removeAttribute('disabled');
        });
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
        init: init
    };
})();
