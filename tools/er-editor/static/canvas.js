// canvas.js - JointJS Paper setup with pan/zoom, grid, selection, interactions
// Exposes: window.ERCanvas
(function() {
    'use strict';

    var MIN_SCALE = 0.2;
    var MAX_SCALE = 4.0;
    var ZOOM_STEP = 0.1;
    var GRID_SIZE = 20;

    var _paper = null;
    var _graph = null;
    var _selectedElement = null;
    var _zoomLevelEl = null;

    /**
     * Initialize the canvas with a JointJS Graph and Paper.
     * @param {HTMLElement} paperEl - Container element for the paper
     * @returns {{ graph: joint.dia.Graph, paper: joint.dia.Paper }}
     */
    function init(paperEl) {
        _graph = new joint.dia.Graph();
        _paper = new joint.dia.Paper({
            el: paperEl,
            model: _graph,
            width: '100%',
            height: '100%',
            gridSize: GRID_SIZE,
            drawGrid: {
                name: 'dot',
                args: { color: '#e5e7eb', thickness: 2 }
            },
            background: { color: '#f9fafb' },
            interactive: { elementMove: true },
            embeddingMode: true,
            validateEmbedding: function(childView, parentView) {
                return parentView.model.get('type') === 'er.Group';
            },
            snapLinks: false,
            linkPinning: false,
            defaultConnector: { name: 'rounded', args: { radius: 5 } },
            defaultRouter: { name: 'manhattan', args: { padding: 20 } },
            defaultAnchor: { name: 'center' },
            defaultConnectionPoint: { name: 'bbox' },
            async: true
        });

        _zoomLevelEl = document.getElementById('zoom-level');

        setupPanZoom();
        setupSelection();
        setupLinkHover();
        setupSnapToGrid();

        return { graph: _graph, paper: _paper };
    }

    // --- Pan & Zoom ---

    /**
     * Scale the paper to a given level, centered on a specific point.
     * Uses the matrix approach from JointJS community pattern.
     * @param {number} nextScale - Target zoom level
     * @param {number} x - X coordinate of zoom center (in paper local coords)
     * @param {number} y - Y coordinate of zoom center (in paper local coords)
     */
    function scaleToPoint(nextScale, x, y) {
        if (nextScale < MIN_SCALE || nextScale > MAX_SCALE) return;
        var currentScale = _paper.scale().sx;
        var beta = currentScale / nextScale;
        var ax = x - (x * beta);
        var ay = y - (y * beta);
        var translate = _paper.translate();
        var nextTx = translate.tx - ax * nextScale;
        var nextTy = translate.ty - ay * nextScale;
        _paper.translate(nextTx, nextTy);
        var ctm = _paper.matrix();
        ctm.a = nextScale;
        ctm.d = nextScale;
        _paper.matrix(ctm);
        updateZoomDisplay();
    }

    function setupPanZoom() {
        // Zoom on mouse wheel over blank area
        _paper.on('blank:mousewheel', function(evt, x, y, delta) {
            evt.preventDefault();
            var oldScale = _paper.scale().sx;
            scaleToPoint(oldScale + delta * ZOOM_STEP, x, y);
        });

        // Zoom on mouse wheel over elements
        _paper.on('cell:mousewheel', function(_, evt, x, y, delta) {
            evt.preventDefault();
            var oldScale = _paper.scale().sx;
            scaleToPoint(oldScale + delta * ZOOM_STEP, x, y);
        });

        // Pan on blank area drag
        var panning = false;
        var panStart = {};

        _paper.on('blank:pointerdown', function(evt) {
            panning = true;
            panStart = {
                x: evt.clientX,
                y: evt.clientY,
                tx: _paper.translate().tx,
                ty: _paper.translate().ty
            };
        });

        document.addEventListener('mousemove', function(evt) {
            if (!panning) return;
            _paper.translate(
                panStart.tx + evt.clientX - panStart.x,
                panStart.ty + evt.clientY - panStart.y
            );
        });

        document.addEventListener('mouseup', function() {
            panning = false;
        });
    }

    function updateZoomDisplay() {
        if (_zoomLevelEl) {
            var pct = Math.round(_paper.scale().sx * 100);
            _zoomLevelEl.textContent = pct + '%';
        }
    }

    // --- Selection & Highlighting ---

    function setupSelection() {
        // Click element: select it, highlight connected, dim others
        _paper.on('element:pointerclick', function(elementView) {
            selectElement(elementView.model);
        });

        // Click blank: deselect all
        _paper.on('blank:pointerclick', function() {
            deselectAll();
        });
    }

    /**
     * Select a table element: highlight it and connected tables/links,
     * dim unrelated elements to 0.3 opacity.
     * @param {joint.dia.Element} element - Element to select
     */
    function selectElement(element) {
        deselectAll();
        _selectedElement = element;

        // Highlight selected element with blue border
        element.attr('headerRect/stroke', ERShapes.COLORS.borderSelected);
        element.attr('headerRect/strokeWidth', 2);
        element.attr('bodyRect/stroke', ERShapes.COLORS.borderSelected);
        element.attr('bodyRect/strokeWidth', 2);

        // Find connected elements via links
        var connectedIds = {};
        _graph.getLinks().forEach(function(link) {
            var srcId = link.source().id;
            var tgtId = link.target().id;
            if (srcId === element.id) {
                connectedIds[tgtId] = true;
                link.attr('line/stroke', ERShapes.COLORS.borderSelected);
            } else if (tgtId === element.id) {
                connectedIds[srcId] = true;
                link.attr('line/stroke', ERShapes.COLORS.borderSelected);
            }
        });

        // Highlight connected elements, dim unrelated
        _graph.getElements().forEach(function(el) {
            if (el.id === element.id) return;
            if (connectedIds[el.id]) {
                // Connected: dashed blue border
                el.attr('headerRect/stroke', ERShapes.COLORS.borderSelected);
                el.attr('headerRect/strokeDasharray', '4,2');
                el.attr('bodyRect/stroke', ERShapes.COLORS.borderSelected);
                el.attr('bodyRect/strokeDasharray', '4,2');
            } else {
                // Unrelated: dim to 0.3 opacity
                var view = el.findView(_paper);
                if (view) view.el.style.opacity = '0.3';
            }
        });

        // Dim unconnected links
        _graph.getLinks().forEach(function(link) {
            var srcId = link.source().id;
            var tgtId = link.target().id;
            if (srcId !== element.id && tgtId !== element.id) {
                var view = link.findView(_paper);
                if (view) view.el.style.opacity = '0.3';
            }
        });
    }

    /**
     * Deselect all elements: restore all to default appearance.
     */
    function deselectAll() {
        _selectedElement = null;

        // Restore all elements
        _graph.getElements().forEach(function(el) {
            el.attr('headerRect/stroke', ERShapes.COLORS.border);
            el.attr('headerRect/strokeWidth', 1);
            el.attr('headerRect/strokeDasharray', '');
            el.attr('bodyRect/stroke', ERShapes.COLORS.border);
            el.attr('bodyRect/strokeWidth', 1);
            el.attr('bodyRect/strokeDasharray', '');
            var view = el.findView(_paper);
            if (view) view.el.style.opacity = '1';
        });

        // Restore all links
        _graph.getLinks().forEach(function(link) {
            link.attr('line/stroke', ERShapes.COLORS.relLine);
            var view = link.findView(_paper);
            if (view) view.el.style.opacity = '1';
        });
    }

    // --- Link Hover ---

    function setupLinkHover() {
        _paper.on('link:mouseenter', function(linkView) {
            // Don't override selection highlighting
            if (_selectedElement) return;

            var link = linkView.model;
            link.attr('line/stroke', ERShapes.COLORS.relLineHover);

            var srcId = link.source().id;
            var tgtId = link.target().id;

            _graph.getElements().forEach(function(el) {
                if (el.id === srcId || el.id === tgtId) {
                    // Connected: dashed blue border
                    el.attr('headerRect/stroke', ERShapes.COLORS.borderSelected);
                    el.attr('headerRect/strokeDasharray', '4,2');
                    el.attr('bodyRect/stroke', ERShapes.COLORS.borderSelected);
                    el.attr('bodyRect/strokeDasharray', '4,2');
                } else {
                    // Unrelated: dim
                    var view = el.findView(_paper);
                    if (view) view.el.style.opacity = '0.3';
                }
            });

            // Dim other links
            _graph.getLinks().forEach(function(l) {
                if (l.id !== link.id) {
                    var v = l.findView(_paper);
                    if (v) v.el.style.opacity = '0.3';
                }
            });
        });

        _paper.on('link:mouseleave', function() {
            if (_selectedElement) {
                // Restore selection highlighting
                selectElement(_selectedElement);
            } else {
                deselectAll();
            }
        });
    }

    // --- Snap to Grid ---

    function setupSnapToGrid() {
        // Alt key overrides snap-to-grid for free drag
        _paper.on('element:pointermove', function(elementView, evt) {
            if (evt.altKey) {
                _paper.options.gridSize = 1;
            } else {
                _paper.options.gridSize = GRID_SIZE;
            }
        });

        _paper.on('element:pointerup', function() {
            _paper.options.gridSize = GRID_SIZE;
        });
    }

    // --- Public API ---

    /**
     * Zoom and pan to fit all elements in the viewport.
     */
    function fitAll() {
        _paper.scaleContentToFit({
            padding: 40,
            minScale: MIN_SCALE,
            maxScale: MAX_SCALE
        });
        updateZoomDisplay();
    }

    /**
     * Zoom in by one step, centered on the paper center.
     */
    function zoomIn() {
        var center = _paper.getComputedSize();
        var oldScale = _paper.scale().sx;
        scaleToPoint(oldScale + ZOOM_STEP, center.width / 2, center.height / 2);
    }

    /**
     * Zoom out by one step, centered on the paper center.
     */
    function zoomOut() {
        var center = _paper.getComputedSize();
        var oldScale = _paper.scale().sx;
        scaleToPoint(oldScale - ZOOM_STEP, center.width / 2, center.height / 2);
    }

    /**
     * Apply a saved viewport (zoom + pan) from .er.json layout data.
     * @param {{ zoom: number, panX: number, panY: number }} viewport
     */
    function applyViewport(viewport) {
        if (!viewport) return;
        if (viewport.zoom) {
            var ctm = _paper.matrix();
            ctm.a = viewport.zoom;
            ctm.d = viewport.zoom;
            _paper.matrix(ctm);
        }
        if (viewport.panX !== undefined && viewport.panY !== undefined) {
            _paper.translate(viewport.panX, viewport.panY);
        }
        updateZoomDisplay();
    }

    /**
     * Get the current viewport state for saving.
     * @returns {{ zoom: number, panX: number, panY: number }}
     */
    function getViewport() {
        var scale = _paper.scale();
        var translate = _paper.translate();
        return {
            zoom: scale.sx,
            panX: translate.tx,
            panY: translate.ty
        };
    }

    window.ERCanvas = {
        init: init,
        fitAll: fitAll,
        zoomIn: zoomIn,
        zoomOut: zoomOut,
        selectElement: selectElement,
        deselectAll: deselectAll,
        applyViewport: applyViewport,
        getViewport: getViewport,
        getGraph: function() { return _graph; },
        getPaper: function() { return _paper; },
        getSelectedElement: function() { return _selectedElement; },
        GRID_SIZE: GRID_SIZE
    };
})();
