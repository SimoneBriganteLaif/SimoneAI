// groups.js - Visual grouping system with draw-to-create, JointJS embedding, context menu
// Exposes: window.ERGroups
var ERGroups = (function() {
    'use strict';

    var GROUP_COLORS = {
        Blue:   { bg: '#dbeafe', border: '#93c5fd', label: '#1e40af' },
        Green:  { bg: '#dcfce7', border: '#86efac', label: '#166534' },
        Purple: { bg: '#f3e8ff', border: '#c4b5fd', label: '#6b21a8' },
        Orange: { bg: '#ffedd5', border: '#fdba74', label: '#9a3412' },
        Pink:   { bg: '#fce7f3', border: '#f9a8d4', label: '#9d174d' },
        Teal:   { bg: '#ccfbf1', border: '#5eead4', label: '#115e59' },
        Gray:   { bg: '#f3f4f6', border: '#d1d5db', label: '#374151' },
        Yellow: { bg: '#fef9c3', border: '#fde047', label: '#854d0e' }
    };
    var COLOR_NAMES = Object.keys(GROUP_COLORS);

    var _groups = {};       // groupId -> { element, name, color }
    var _drawingGroup = false;
    var _rubberBand = null;
    var _startPoint = null;
    var _idCounter = 0;
    var _onLayoutChange = null;
    var _elements = {};     // className -> JointJS element (from app.js)

    function init(elements, onLayoutChange) {
        _elements = elements;
        _onLayoutChange = onLayoutChange;
    }

    // --- Group Element Creation ---

    function createGroupElement(name, colorName, bounds) {
        var color = GROUP_COLORS[colorName] || GROUP_COLORS.Blue;
        var id = 'group-' + (++_idCounter);

        var el = new joint.dia.Element({
            type: 'er.Group',
            id: id,
            position: { x: bounds.x, y: bounds.y },
            size: { width: Math.max(200, bounds.width), height: Math.max(120, bounds.height) },
            z: -1, // Below table elements
            attrs: {
                body: {
                    width: 'calc(w)',
                    height: 'calc(h)',
                    fill: color.bg,
                    stroke: color.border,
                    strokeWidth: 2,
                    rx: 8,
                    ry: 8
                },
                label: {
                    x: 12,
                    y: 4,
                    text: name,
                    fill: color.label,
                    fontSize: 12,
                    fontWeight: 600,
                    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif',
                    textVerticalAnchor: 'top'
                }
            },
            markup: [
                { tagName: 'rect', selector: 'body' },
                { tagName: 'text', selector: 'label' }
            ],
            groupData: { name: name, color: colorName }
        });

        return { id: id, element: el };
    }

    // --- Draw-to-Create Interaction ---

    function startDraw() {
        _drawingGroup = true;
        var paper = ERCanvas.getPaper();
        paper.el.style.cursor = 'crosshair';

        // Store handlers to remove later
        var handlers = {};

        handlers.onDown = function(evt, x, y) {
            if (!_drawingGroup) return;
            _startPoint = { x: x, y: y };
            // Create rubber band SVG rect
            _rubberBand = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            _rubberBand.setAttribute('fill', 'rgba(59, 130, 246, 0.05)');
            _rubberBand.setAttribute('stroke', '#3b82f6');
            _rubberBand.setAttribute('stroke-dasharray', '4,4');
            _rubberBand.setAttribute('stroke-width', '1');
            paper.svg.appendChild(_rubberBand);
        };

        // Use document mousemove for smooth tracking
        handlers.onMove = function(evt) {
            if (!_drawingGroup || !_startPoint || !_rubberBand) return;
            var rect = paper.el.getBoundingClientRect();
            var scale = paper.scale().sx;
            var translate = paper.translate();
            var x = (evt.clientX - rect.left - translate.tx) / scale;
            var y = (evt.clientY - rect.top - translate.ty) / scale;

            var rx = Math.min(_startPoint.x, x);
            var ry = Math.min(_startPoint.y, y);
            var rw = Math.abs(x - _startPoint.x);
            var rh = Math.abs(y - _startPoint.y);

            _rubberBand.setAttribute('x', rx);
            _rubberBand.setAttribute('y', ry);
            _rubberBand.setAttribute('width', rw);
            _rubberBand.setAttribute('height', rh);
        };

        handlers.onUp = function(evt) {
            if (!_drawingGroup || !_startPoint) return;

            var rect = paper.el.getBoundingClientRect();
            var scale = paper.scale().sx;
            var translate = paper.translate();
            var endX = (evt.clientX - rect.left - translate.tx) / scale;
            var endY = (evt.clientY - rect.top - translate.ty) / scale;

            var bounds = {
                x: Math.min(_startPoint.x, endX),
                y: Math.min(_startPoint.y, endY),
                width: Math.abs(endX - _startPoint.x),
                height: Math.abs(endY - _startPoint.y)
            };

            // Remove rubber band
            if (_rubberBand && _rubberBand.parentNode) {
                _rubberBand.parentNode.removeChild(_rubberBand);
            }
            _rubberBand = null;
            _startPoint = null;

            // Only create if area is meaningful (> 50x50)
            if (bounds.width > 50 && bounds.height > 50) {
                finishDraw(bounds);
            }

            cancelDraw(handlers);
        };

        paper.on('blank:pointerdown', handlers.onDown);
        document.addEventListener('mousemove', handlers.onMove);
        document.addEventListener('mouseup', handlers.onUp);

        // Store handlers on _drawingGroup for cleanup
        _drawingGroup = handlers;
    }

    function cancelDraw(handlers) {
        var paper = ERCanvas.getPaper();
        paper.el.style.cursor = '';
        _drawingGroup = false;

        if (handlers) {
            paper.off('blank:pointerdown', handlers.onDown);
            document.removeEventListener('mousemove', handlers.onMove);
            document.removeEventListener('mouseup', handlers.onUp);
        }

        if (_rubberBand && _rubberBand.parentNode) {
            _rubberBand.parentNode.removeChild(_rubberBand);
        }
        _rubberBand = null;
        _startPoint = null;
    }

    function finishDraw(bounds) {
        var graph = ERCanvas.getGraph();
        var result = createGroupElement('New Group', 'Blue', bounds);
        var groupEl = result.element;
        var groupId = result.id;

        graph.addCell(groupEl);

        // Auto-embed tables whose center falls inside the group bounds
        var embedded = [];
        Object.keys(_elements).forEach(function(className) {
            var tableEl = _elements[className];
            var pos = tableEl.position();
            var size = tableEl.size();
            var centerX = pos.x + size.width / 2;
            var centerY = pos.y + size.height / 2;

            if (centerX >= bounds.x && centerX <= bounds.x + bounds.width &&
                centerY >= bounds.y && centerY <= bounds.y + bounds.height) {
                groupEl.embed(tableEl);
                embedded.push(className);
            }
        });

        _groups[groupId] = { element: groupEl, name: 'New Group', color: 'Blue', members: embedded };

        // Make label editable immediately
        startLabelEdit(groupEl);

        if (_onLayoutChange) _onLayoutChange();
    }

    // --- Label Editing ---

    function startLabelEdit(groupEl) {
        var paper = ERCanvas.getPaper();
        var view = groupEl.findView(paper);
        if (!view) return;

        var textEl = view.el.querySelector('text[joint-selector="label"]');
        if (!textEl) return;

        // Create input overlay
        var bbox = textEl.getBBox();
        var ctm = textEl.getScreenCTM();
        var input = document.createElement('input');
        input.type = 'text';
        input.className = 'er-group-label-input';
        input.value = groupEl.get('groupData').name;
        input.style.position = 'fixed';
        input.style.left = (ctm.e) + 'px';
        input.style.top = (ctm.f) + 'px';
        input.style.width = '120px';
        input.style.zIndex = '300';
        document.body.appendChild(input);
        input.select();

        function commit() {
            var name = input.value.trim() || 'New Group';
            groupEl.attr('label/text', name);
            var data = groupEl.get('groupData');
            data.name = name;
            groupEl.set('groupData', data);
            var groupId = groupEl.id;
            if (_groups[groupId]) _groups[groupId].name = name;
            input.remove();
            if (_onLayoutChange) _onLayoutChange();
        }

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); commit(); }
            if (e.key === 'Escape') { e.preventDefault(); input.remove(); }
        });
        input.addEventListener('blur', commit);
    }

    // --- Color Picker (inline after label) ---

    function showColorPicker(groupEl) {
        var paper = ERCanvas.getPaper();
        var view = groupEl.findView(paper);
        var rect = view.el.getBoundingClientRect();

        var picker = document.createElement('div');
        picker.className = 'er-group-colors';
        picker.style.position = 'fixed';
        picker.style.left = (rect.left + 12) + 'px';
        picker.style.top = (rect.top + 24) + 'px';
        picker.style.zIndex = '300';
        picker.style.background = '#ffffff';
        picker.style.padding = '4px';
        picker.style.borderRadius = '6px';
        picker.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';

        var currentColor = groupEl.get('groupData').color;

        COLOR_NAMES.forEach(function(name) {
            var swatch = document.createElement('div');
            swatch.className = 'er-group-color-swatch';
            if (name === currentColor) swatch.classList.add('is-selected');
            swatch.style.background = GROUP_COLORS[name].bg;
            swatch.style.borderColor = name === currentColor ? '#374151' : GROUP_COLORS[name].border;
            swatch.addEventListener('click', function() {
                applyColor(groupEl, name);
                picker.remove();
            });
            picker.appendChild(swatch);
        });

        document.body.appendChild(picker);

        // Close on click outside
        function closePicker(e) {
            if (!picker.contains(e.target)) {
                picker.remove();
                document.removeEventListener('click', closePicker, true);
            }
        }
        setTimeout(function() { document.addEventListener('click', closePicker, true); }, 0);
    }

    function applyColor(groupEl, colorName) {
        var color = GROUP_COLORS[colorName];
        groupEl.attr('body/fill', color.bg);
        groupEl.attr('body/stroke', color.border);
        groupEl.attr('label/fill', color.label);
        var data = groupEl.get('groupData');
        data.color = colorName;
        groupEl.set('groupData', data);
        if (_groups[groupEl.id]) _groups[groupEl.id].color = colorName;
        if (_onLayoutChange) _onLayoutChange();
    }

    // --- Context Menu ---

    function showContextMenu(groupEl, x, y) {
        // Remove any existing context menu
        var existing = document.querySelector('.er-group-context-menu');
        if (existing) existing.remove();

        var menu = document.createElement('div');
        menu.className = 'er-group-context-menu';
        menu.style.left = x + 'px';
        menu.style.top = y + 'px';

        var btnRename = document.createElement('button');
        btnRename.textContent = 'Rename';
        btnRename.addEventListener('click', function() { menu.remove(); startLabelEdit(groupEl); });

        var btnColor = document.createElement('button');
        btnColor.textContent = 'Change Color';
        btnColor.addEventListener('click', function() { menu.remove(); showColorPicker(groupEl); });

        var btnDelete = document.createElement('button');
        btnDelete.textContent = 'Delete Group';
        btnDelete.addEventListener('click', function() {
            menu.remove();
            deleteGroup(groupEl);
        });

        menu.appendChild(btnRename);
        menu.appendChild(btnColor);
        menu.appendChild(btnDelete);
        document.body.appendChild(menu);

        // Close on click outside
        function closeMenu(e) {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', closeMenu, true);
            }
        }
        setTimeout(function() { document.addEventListener('click', closeMenu, true); }, 0);
    }

    function deleteGroup(groupEl) {
        var graph = ERCanvas.getGraph();
        // Unembed all children first (tables stay on canvas)
        var children = groupEl.getEmbeddedCells();
        children.forEach(function(child) { groupEl.unembed(child); });
        graph.removeCells([groupEl]);
        delete _groups[groupEl.id];
        if (_onLayoutChange) _onLayoutChange();
    }

    // --- Persistence ---

    function getGroupsData() {
        var result = [];
        Object.keys(_groups).forEach(function(id) {
            var g = _groups[id];
            var el = g.element;
            var pos = el.position();
            var size = el.size();
            var members = el.getEmbeddedCells().map(function(child) {
                return child.get('tableData') ? child.get('tableData').class_name : null;
            }).filter(Boolean);

            result.push({
                id: id,
                name: g.name,
                color: g.color,
                bounds: { x: pos.x, y: pos.y, width: size.width, height: size.height },
                members: members
            });
        });
        return result;
    }

    function loadGroups(groupsData, elements) {
        if (!groupsData || !Array.isArray(groupsData)) return;
        var graph = ERCanvas.getGraph();

        groupsData.forEach(function(gd) {
            var result = createGroupElement(gd.name, gd.color, gd.bounds);
            var groupEl = result.element;
            graph.addCell(groupEl);

            // Embed member tables
            var members = [];
            (gd.members || []).forEach(function(className) {
                if (elements[className]) {
                    groupEl.embed(elements[className]);
                    members.push(className);
                }
            });

            _groups[result.id] = { element: groupEl, name: gd.name, color: gd.color, members: members };
        });
    }

    function isDrawing() {
        return _drawingGroup !== false;
    }

    return {
        init: init,
        startDraw: startDraw,
        cancelDraw: cancelDraw,
        getGroupsData: getGroupsData,
        loadGroups: loadGroups,
        showContextMenu: showContextMenu,
        isDrawing: isDrawing,
        GROUP_COLORS: GROUP_COLORS
    };
})();
