// editor.js - Core editing infrastructure: schema state, save flow, toasts, popups, confirmations, keyboard shortcuts
// Exposes: window.EREditor
var EREditor = (function() {
    'use strict';

    // --- Schema State ---
    var _schema = { tables: [] };
    var _dirty = false;
    var _deletedClasses = [];
    var _activePopup = null;
    var _activeConfirmation = null;

    /**
     * Initialize editor with schema data from GET /api/schema.
     * Stores a deep copy and registers keyboard shortcuts.
     * @param {{ tables: Array }} schema
     */
    function init(schema) {
        _schema = JSON.parse(JSON.stringify(schema));
        _dirty = false;
        _deletedClasses = [];
        _setupKeyboardShortcuts();

        // Wire undo/redo stack change to toolbar button updates
        ERUndo.onChange(function() {
            _updateUndoRedoButtons();
            markDirty();
        });

        // Setup relationship drag-to-create and click handlers
        setupRelationshipDrag();
        _setupRelationshipClickHandlers();
    }

    /** @returns {{ tables: Array }} Current schema (mutable reference) */
    function getSchema() { return _schema; }

    /** @returns {boolean} Whether there are unsaved changes */
    function isDirty() { return _dirty; }

    /** Mark schema as having unsaved changes. Updates save button UI. */
    function markDirty() {
        _dirty = true;
        _updateSaveButton();
    }

    /** Mark schema as clean (after successful save). Updates save button UI. */
    function markClean() {
        _dirty = false;
        _updateSaveButton();
    }

    /**
     * Track a deleted class name for the next save payload.
     * @param {string} className
     */
    function trackDeletion(className) {
        if (_deletedClasses.indexOf(className) === -1) {
            _deletedClasses.push(className);
        }
    }

    /**
     * Remove a class name from the deletion list (called on undo of delete).
     * @param {string} className
     */
    function untrackDeletion(className) {
        var idx = _deletedClasses.indexOf(className);
        if (idx !== -1) _deletedClasses.splice(idx, 1);
    }

    // --- Save Flow ---

    /**
     * Save current schema to the backend via POST /api/schema.
     * Sends tables + deleted class list. On success: markClean, clear deletions, show toast.
     */
    async function save() {
        var saveBtn = document.getElementById('btn-save');
        if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.textContent = 'Saving...';
        }

        try {
            var res = await fetch('/api/schema', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tables: _schema.tables,
                    deleted: _deletedClasses
                })
            });

            if (!res.ok) {
                var errData = await res.json().catch(function() { return { detail: 'Unknown error' }; });
                throw new Error(errData.detail || 'Save failed');
            }

            markClean();
            _deletedClasses = [];
            showToast('Saved to model.py', 'success');
        } catch (err) {
            showToast('Save failed: ' + err.message, 'error');
        } finally {
            if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.innerHTML = 'Save Model<span class="dirty-dot"></span>';
                _updateSaveButton();
            }
        }
    }

    function _updateSaveButton() {
        var saveBtn = document.getElementById('btn-save');
        if (!saveBtn) return;
        if (_dirty) {
            saveBtn.classList.add('is-dirty');
            saveBtn.title = 'Save model to disk (Ctrl+S) - unsaved changes';
        } else {
            saveBtn.classList.remove('is-dirty');
            saveBtn.title = 'Save model to disk (Ctrl+S)';
        }
    }

    function _updateUndoRedoButtons() {
        var undoBtn = document.getElementById('btn-undo');
        var redoBtn = document.getElementById('btn-redo');
        if (undoBtn) undoBtn.disabled = !ERUndo.canUndo();
        if (redoBtn) redoBtn.disabled = !ERUndo.canRedo();
    }

    // --- Toast Notifications ---

    /**
     * Show a toast notification at bottom-center of the screen.
     * Auto-removes after 3 seconds with fade-out animation.
     * @param {string} message - Toast message text
     * @param {'success'|'error'} type - Toast type
     */
    function showToast(message, type) {
        var toast = document.createElement('div');
        toast.className = 'er-toast er-toast--' + type;

        // Icon SVG
        var iconSvg = '';
        if (type === 'success') {
            iconSvg = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none">' +
                '<path d="M3 8l3 3 7-7" stroke="#22c55e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' +
                '</svg>';
        } else {
            iconSvg = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none">' +
                '<path d="M4 4l8 8M12 4l-8 8" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round"/>' +
                '</svg>';
        }

        toast.innerHTML = iconSvg + '<span>' + _escapeHtml(message) + '</span>';
        document.body.appendChild(toast);

        // Auto-dismiss after 3 seconds
        setTimeout(function() {
            toast.classList.add('er-toast--fade-out');
            setTimeout(function() {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // --- Popup Management ---

    /**
     * Show a popup near an anchor element. Only one popup at a time.
     * @param {HTMLElement|{x:number,y:number}} anchor - Element or coordinates to anchor near
     * @param {string} contentHTML - Inner HTML for the popup
     * @param {Function} [onClose] - Callback when popup is closed
     * @returns {HTMLElement} The popup element
     */
    function showPopup(anchor, contentHTML, onClose) {
        closePopup();

        var popup = document.createElement('div');
        popup.className = 'er-popup';
        popup.innerHTML = contentHTML;

        document.body.appendChild(popup);

        // Position near anchor
        var rect;
        if (anchor && anchor.getBoundingClientRect) {
            rect = anchor.getBoundingClientRect();
        } else if (anchor && typeof anchor.x === 'number') {
            rect = { left: anchor.x, top: anchor.y, right: anchor.x, bottom: anchor.y, width: 0, height: 0 };
        } else {
            rect = { left: window.innerWidth / 2, top: window.innerHeight / 2, right: window.innerWidth / 2, bottom: window.innerHeight / 2, width: 0, height: 0 };
        }

        var popupRect = popup.getBoundingClientRect();
        var left = rect.left;
        var top = rect.bottom + 8;

        // Flip if near right edge
        if (left + popupRect.width > window.innerWidth - 16) {
            left = window.innerWidth - popupRect.width - 16;
        }
        // Flip if near bottom edge
        if (top + popupRect.height > window.innerHeight - 16) {
            top = rect.top - popupRect.height - 8;
        }
        // Clamp left
        if (left < 16) left = 16;

        popup.style.left = left + 'px';
        popup.style.top = top + 'px';

        _activePopup = {
            el: popup,
            onClose: onClose || null
        };

        return popup;
    }

    /** Close the active popup if any. */
    function closePopup() {
        if (_activePopup) {
            if (_activePopup.el && _activePopup.el.parentNode) {
                _activePopup.el.parentNode.removeChild(_activePopup.el);
            }
            if (_activePopup.onClose) _activePopup.onClose();
            _activePopup = null;
        }
    }

    /** @returns {HTMLElement|null} The active popup element, or null */
    function getActivePopup() {
        return _activePopup ? _activePopup.el : null;
    }

    // --- Inline Confirmation Banner ---

    /**
     * Show an inline confirmation banner inside a JointJS element's foreignObject body.
     * @param {joint.dia.Element} element - The table element
     * @param {string} message - Confirmation message
     * @param {Function} onConfirm - Called when user confirms
     * @param {Function} onCancel - Called when user cancels (or auto-cancel after 5s)
     */
    function showConfirmation(element, message, onConfirm, onCancel) {
        // Cancel any existing confirmation
        if (_activeConfirmation) {
            _cancelConfirmation();
        }

        var paper = ERCanvas.getPaper();
        var view = element.findView(paper);
        if (!view) return;

        var foreignObj = view.el.querySelector('foreignObject');
        if (!foreignObj) return;

        var bodyDiv = foreignObj.querySelector('.er-body');
        if (!bodyDiv) return;

        // Create banner
        var banner = document.createElement('div');
        banner.className = 'er-confirm-banner';
        banner.innerHTML = '<span>' + _escapeHtml(message) + '</span>' +
            '<button class="er-confirm-yes">Confirm</button>' +
            '<button class="er-confirm-no">Cancel</button>';

        // Insert at top of body
        bodyDiv.insertBefore(banner, bodyDiv.firstChild);

        var resolved = false;

        function resolve(confirmed) {
            if (resolved) return;
            resolved = true;
            if (banner.parentNode) banner.parentNode.removeChild(banner);
            clearTimeout(autoCancel);
            _activeConfirmation = null;
            if (confirmed) {
                onConfirm();
            } else {
                if (onCancel) onCancel();
            }
        }

        banner.querySelector('.er-confirm-yes').addEventListener('click', function(e) {
            e.stopPropagation();
            resolve(true);
        });
        banner.querySelector('.er-confirm-no').addEventListener('click', function(e) {
            e.stopPropagation();
            resolve(false);
        });

        // Auto-cancel after 5 seconds
        var autoCancel = setTimeout(function() {
            resolve(false);
        }, 5000);

        _activeConfirmation = {
            banner: banner,
            cancel: function() { resolve(false); }
        };
    }

    function _cancelConfirmation() {
        if (_activeConfirmation) {
            _activeConfirmation.cancel();
            _activeConfirmation = null;
        }
    }

    // --- Keyboard Shortcuts ---

    function _setupKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Don't intercept if user is typing in an input/textarea
            var tag = e.target.tagName;
            var isInput = (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT');

            // Escape always works (close popup, cancel edit)
            if (e.key === 'Escape') {
                closePopup();
                _cancelConfirmation();
                return;
            }

            // Ctrl+S / Cmd+S - Save
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                save();
                return;
            }

            // Skip other shortcuts when in an input field
            if (isInput) return;

            // Ctrl+Shift+Z / Cmd+Shift+Z - Redo (check before undo since it also has ctrlKey)
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'z' || e.key === 'Z')) {
                e.preventDefault();
                ERUndo.redo();
                return;
            }

            // Ctrl+Z / Cmd+Z - Undo
            if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z')) {
                e.preventDefault();
                ERUndo.undo();
                return;
            }

            // Delete / Backspace - delete selected (dispatches custom event for other modules)
            if (e.key === 'Delete' || e.key === 'Backspace') {
                var evt = new CustomEvent('er:delete-selected');
                document.dispatchEvent(evt);
                return;
            }
        });
    }

    // --- Utilities ---

    function _escapeHtml(text) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }

    function _escapeAttr(text) {
        return String(text || '')
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    /**
     * Simple pluralization: adds 's' or handles common patterns.
     * Used for auto-generating relationship names.
     * @param {string} name - camelCase or snake_case singular name
     * @returns {string} Pluralized name
     */
    function _toSnakeCasePlural(name) {
        // Convert camelCase to snake_case
        var snake = name.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase();
        // Simple pluralization
        if (snake.endsWith('s') || snake.endsWith('x') || snake.endsWith('z') ||
            snake.endsWith('sh') || snake.endsWith('ch')) {
            return snake + 'es';
        }
        if (snake.endsWith('y') && !/[aeiou]y$/.test(snake)) {
            return snake.slice(0, -1) + 'ies';
        }
        return snake + 's';
    }

    // --- Relationship CRUD ---

    /**
     * Setup drag-to-create relationship interaction.
     * Detects mousedown on table border (outer 8px), draws a dashed line,
     * highlights valid target tables, and opens creation popup on drop.
     */
    function setupRelationshipDrag() {
        var paper = ERCanvas.getPaper();
        var graph = ERCanvas.getGraph();
        var _dragging = false;
        var _dragLine = null;
        var _sourceElement = null;
        var _highlightedTarget = null;

        // Detect mousedown on table border area (outer 8px)
        paper.on('element:pointerdown', function(elementView, evt) {
            var el = elementView.model;
            if (el.get('type') !== 'er.Table') return;

            // Check if click is on the border area (outer 8px of element)
            var elRect = elementView.el.getBoundingClientRect();
            var margin = 8;
            var x = evt.clientX;
            var y = evt.clientY;

            var onBorder = (
                x < elRect.left + margin || x > elRect.right - margin ||
                y < elRect.top + margin || y > elRect.bottom - margin
            );

            // Only start drag if on border AND not on a sub-element (chevron, + icon, etc.)
            var target = evt.target;
            var isSubElement = target.getAttribute && (
                target.getAttribute('joint-selector') === 'chevronHit' ||
                target.getAttribute('joint-selector') === 'addColHit' ||
                target.closest('.er-body')
            );

            if (onBorder && !isSubElement) {
                _dragging = true;
                _sourceElement = el;

                // Create temporary dashed line
                var pos = el.position();
                var size = el.size();
                var startX = pos.x + size.width / 2;
                var startY = pos.y + size.height / 2;

                _dragLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                _dragLine.setAttribute('x1', startX);
                _dragLine.setAttribute('y1', startY);
                _dragLine.setAttribute('x2', startX);
                _dragLine.setAttribute('y2', startY);
                _dragLine.setAttribute('stroke', '#3b82f6');
                _dragLine.setAttribute('stroke-width', '2');
                _dragLine.setAttribute('stroke-dasharray', '6,4');
                _dragLine.setAttribute('pointer-events', 'none');
                paper.svg.appendChild(_dragLine);

                evt.stopPropagation();
            }
        });

        document.addEventListener('mousemove', function(evt) {
            if (!_dragging || !_dragLine) return;
            var p = ERCanvas.getPaper();
            var rect = p.el.getBoundingClientRect();
            var scale = p.scale().sx;
            var translate = p.translate();
            var x = (evt.clientX - rect.left - translate.tx) / scale;
            var y = (evt.clientY - rect.top - translate.ty) / scale;

            _dragLine.setAttribute('x2', x);
            _dragLine.setAttribute('y2', y);

            // Highlight valid target table
            var targetEl = _findElementAtPoint(graph, x, y);
            if (targetEl && targetEl.id !== _sourceElement.id && targetEl.get('type') === 'er.Table') {
                if (_highlightedTarget !== targetEl) {
                    _clearTargetHighlight();
                    _highlightedTarget = targetEl;
                    targetEl.attr('headerRect/stroke', '#3b82f6');
                    targetEl.attr('headerRect/strokeWidth', 3);
                    targetEl.attr('bodyRect/stroke', '#3b82f6');
                    targetEl.attr('bodyRect/strokeWidth', 3);
                }
            } else {
                _clearTargetHighlight();
            }
        });

        document.addEventListener('mouseup', function(evt) {
            if (!_dragging) return;
            _dragging = false;

            // Remove drag line
            if (_dragLine && _dragLine.parentNode) {
                _dragLine.parentNode.removeChild(_dragLine);
            }
            _dragLine = null;

            _clearTargetHighlight();

            // Check if dropped on a valid target
            var p = ERCanvas.getPaper();
            var rect = p.el.getBoundingClientRect();
            var scale = p.scale().sx;
            var translate = p.translate();
            var x = (evt.clientX - rect.left - translate.tx) / scale;
            var y = (evt.clientY - rect.top - translate.ty) / scale;

            var targetEl = _findElementAtPoint(graph, x, y);
            if (targetEl && _sourceElement && targetEl.id !== _sourceElement.id && targetEl.get('type') === 'er.Table') {
                showRelationshipCreationPopup(_sourceElement, targetEl);
            }

            _sourceElement = null;
            _highlightedTarget = null;
        });

        function _clearTargetHighlight() {
            if (_highlightedTarget) {
                _highlightedTarget.attr('headerRect/stroke', ERShapes.COLORS.border);
                _highlightedTarget.attr('headerRect/strokeWidth', 1);
                _highlightedTarget.attr('bodyRect/stroke', ERShapes.COLORS.border);
                _highlightedTarget.attr('bodyRect/strokeWidth', 1);
                _highlightedTarget = null;
            }
        }
    }

    function _findElementAtPoint(graph, x, y) {
        var elements = graph.getElements();
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            if (el.get('type') !== 'er.Table') continue;
            var pos = el.position();
            var size = el.size();
            if (x >= pos.x && x <= pos.x + size.width && y >= pos.y && y <= pos.y + size.height) {
                return el;
            }
        }
        return null;
    }

    /**
     * Show the relationship creation popup with all options.
     * @param {joint.dia.Element} sourceEl - Source (parent) element
     * @param {joint.dia.Element} targetEl - Target (child) element
     */
    function showRelationshipCreationPopup(sourceEl, targetEl) {
        var sourceData = sourceEl.get('tableData');
        var targetData = targetEl.get('tableData');
        var sourceName = sourceData.class_name;
        var targetName = targetData.class_name;

        // Auto-generate defaults
        var fkColName = targetName.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase() + '_id';
        var sourceRelName = targetName.charAt(0).toLowerCase() + targetName.slice(1);
        var targetRelName = _toSnakeCasePlural(sourceName.charAt(0).toLowerCase() + sourceName.slice(1));

        var html = '<h3>New Relationship</h3>';

        // Cardinality
        html += '<div class="er-popup-field">';
        html += '<label>Cardinality</label>';
        html += '<div style="display:flex;gap:12px;margin-top:4px;">';
        html += '<label style="font-weight:400;font-size:13px;"><input type="radio" name="popup-rel-card" value="1:1" /> 1:1</label>';
        html += '<label style="font-weight:400;font-size:13px;"><input type="radio" name="popup-rel-card" value="1:N" checked /> 1:N</label>';
        html += '<label style="font-weight:400;font-size:13px;"><input type="radio" name="popup-rel-card" value="N:M" /> N:M</label>';
        html += '</div></div>';

        // FK column name
        html += '<div class="er-popup-field" id="popup-rel-fk-group">';
        html += '<label>FK Column (on ' + _escapeHtml(targetName) + ')</label>';
        html += '<input type="text" id="popup-rel-fk" value="' + _escapeAttr(fkColName) + '" />';
        html += '</div>';

        // Relationship names
        html += '<div class="er-popup-field">';
        html += '<label>Relationship on ' + _escapeHtml(sourceName) + '</label>';
        html += '<input type="text" id="popup-rel-source-name" value="' + _escapeAttr(sourceRelName) + '" />';
        html += '</div>';

        html += '<div class="er-popup-field">';
        html += '<label>Relationship on ' + _escapeHtml(targetName) + '</label>';
        html += '<input type="text" id="popup-rel-target-name" value="' + _escapeAttr(targetRelName) + '" />';
        html += '</div>';

        // back_populates
        html += '<div class="er-popup-field er-popup-checkbox">';
        html += '<input type="checkbox" id="popup-rel-backpop" checked />';
        html += '<label for="popup-rel-backpop">back_populates</label>';
        html += '</div>';

        // cascade
        html += '<div class="er-popup-field">';
        html += '<label>Cascade</label>';
        html += '<select id="popup-rel-cascade">';
        html += '<option value="">none</option>';
        html += '<option value="all">all</option>';
        html += '<option value="all, delete-orphan" selected>all, delete-orphan</option>';
        html += '<option value="save-update, merge">save-update, merge</option>';
        html += '</select></div>';

        // lazy
        html += '<div class="er-popup-field">';
        html += '<label>Lazy</label>';
        html += '<select id="popup-rel-lazy">';
        html += '<option value="select" selected>select</option>';
        html += '<option value="joined">joined</option>';
        html += '<option value="subquery">subquery</option>';
        html += '<option value="dynamic">dynamic</option>';
        html += '<option value="selectin">selectin</option>';
        html += '</select></div>';

        // N:M secondary table (hidden by default)
        html += '<div class="er-popup-field" id="popup-rel-nm-group" style="display:none;">';
        html += '<label>Association Table</label>';
        html += '<select id="popup-rel-nm-table">';
        html += '<option value="__new__">Create new...</option>';
        var schema = EREditor.getSchema();
        schema.tables.forEach(function(t) {
            html += '<option value="' + _escapeAttr(t.class_name) + '">' + _escapeHtml(t.class_name) + ' (' + _escapeHtml(t.table_name) + ')</option>';
        });
        html += '</select></div>';

        // Actions
        html += '<div class="er-popup-actions">';
        html += '<button class="er-popup-btn er-popup-btn--secondary" id="popup-rel-cancel">Cancel</button>';
        html += '<button class="er-popup-btn er-popup-btn--primary" id="popup-rel-create">Create</button>';
        html += '</div>';

        // Show popup near the midpoint between source and target
        var srcPos = sourceEl.position();
        var tgtPos = targetEl.position();
        var paper = ERCanvas.getPaper();
        var rect = paper.el.getBoundingClientRect();
        var scale = paper.scale().sx;
        var translate = paper.translate();
        var midX = ((srcPos.x + tgtPos.x) / 2) * scale + translate.tx + rect.left;
        var midY = ((srcPos.y + tgtPos.y) / 2) * scale + translate.ty + rect.top;

        showPopup({ x: midX, y: midY }, html, null);

        // Wire cardinality toggle for N:M
        document.querySelectorAll('input[name="popup-rel-card"]').forEach(function(radio) {
            radio.addEventListener('change', function() {
                var nmGroup = document.getElementById('popup-rel-nm-group');
                var fkGroup = document.getElementById('popup-rel-fk-group');
                if (this.value === 'N:M') {
                    nmGroup.style.display = '';
                    fkGroup.style.display = 'none';
                } else {
                    nmGroup.style.display = 'none';
                    fkGroup.style.display = '';
                }
            });
        });

        // Wire buttons
        document.getElementById('popup-rel-cancel').addEventListener('click', function() {
            closePopup();
        });

        document.getElementById('popup-rel-create').addEventListener('click', function() {
            createRelationshipFromPopup(sourceEl, targetEl);
        });
    }

    /**
     * Create a relationship from the popup form values.
     * Builds compound undo commands for FK column + relationship attrs on both tables + JointJS link.
     * @param {joint.dia.Element} sourceEl - Source (parent) element
     * @param {joint.dia.Element} targetEl - Target (child) element
     */
    function createRelationshipFromPopup(sourceEl, targetEl) {
        var paper = ERCanvas.getPaper();
        var graph = ERCanvas.getGraph();
        var sourceData = sourceEl.get('tableData');
        var targetData = targetEl.get('tableData');

        // Read popup values
        var cardinality = document.querySelector('input[name="popup-rel-card"]:checked').value;
        var fkColName = document.getElementById('popup-rel-fk').value.trim();
        var sourceRelName = document.getElementById('popup-rel-source-name').value.trim();
        var targetRelName = document.getElementById('popup-rel-target-name').value.trim();
        var backPop = document.getElementById('popup-rel-backpop').checked;
        var cascade = document.getElementById('popup-rel-cascade').value || null;
        var lazy = document.getElementById('popup-rel-lazy').value || null;

        closePopup();

        var commands = [];

        if (cardinality === 'N:M') {
            // N:M: use or create association table
            var nmSelect = document.getElementById('popup-rel-nm-table');
            var nmValue = nmSelect ? nmSelect.value : '__new__';

            if (nmValue === '__new__') {
                var assocName = sourceData.class_name + targetData.class_name;
                var assocTableName = sourceData.table_name.replace(/s$/, '') + '_' + targetData.table_name.replace(/s$/, '');

                var assocTable = {
                    class_name: assocName,
                    table_name: assocTableName,
                    schema: sourceData.schema,
                    columns: [
                        { name: sourceData.class_name.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase() + '_id', type: 'Integer', nullable: false, primary_key: true, foreign_key: (sourceData.schema ? sourceData.schema + '.' : '') + sourceData.table_name + '.id', unique: false, index: false, default: null, server_default: null },
                        { name: targetData.class_name.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase() + '_id', type: 'Integer', nullable: false, primary_key: true, foreign_key: (targetData.schema ? targetData.schema + '.' : '') + targetData.table_name + '.id', unique: false, index: false, default: null, server_default: null }
                    ],
                    relationships: []
                };

                commands.push({
                    execute: function() {
                        EREditor.getSchema().tables.push(assocTable);
                        var pos = { x: (sourceEl.position().x + targetEl.position().x) / 2, y: Math.max(sourceEl.position().y, targetEl.position().y) + 200 };
                        var el = ERShapes.createTable(assocTable, pos, false);
                        graph.addCell(el);
                        if (window._elements) window._elements[assocName] = el;
                    },
                    undo: function() {
                        var tables = EREditor.getSchema().tables;
                        var idx = tables.indexOf(assocTable);
                        if (idx >= 0) tables.splice(idx, 1);
                        if (window._elements && window._elements[assocName]) {
                            graph.removeCells([window._elements[assocName]]);
                            delete window._elements[assocName];
                        }
                    }
                });
            }

            // Relationship on source side
            var sourceRelNM = { name: sourceRelName, target: targetData.class_name, back_populates: backPop ? targetRelName : null, cascade: cascade, lazy: lazy, uselist: true, order_by: null };
            var targetRelNM = { name: targetRelName, target: sourceData.class_name, back_populates: backPop ? sourceRelName : null, cascade: null, lazy: lazy, uselist: true, order_by: null };

            commands.push({
                execute: function() {
                    sourceData.relationships.push(sourceRelNM);
                    sourceEl.set('tableData', sourceData);
                    ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                },
                undo: function() {
                    var idx = sourceData.relationships.indexOf(sourceRelNM);
                    if (idx >= 0) sourceData.relationships.splice(idx, 1);
                    sourceEl.set('tableData', sourceData);
                    ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                }
            });

            commands.push({
                execute: function() {
                    targetData.relationships.push(targetRelNM);
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                },
                undo: function() {
                    var idx = targetData.relationships.indexOf(targetRelNM);
                    if (idx >= 0) targetData.relationships.splice(idx, 1);
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                }
            });

            // Create links for N:M (source -> assoc, assoc -> target)
            var linkKeyNM = sourceData.class_name + '->' + targetData.class_name;
            var linkNM = null;
            commands.push({
                execute: function() {
                    linkNM = ERShapes.createLink(sourceEl.id, targetEl.id, 'N', 'M');
                    graph.addCell(linkNM);
                    if (window._linkMap) window._linkMap[linkKeyNM] = linkNM;
                },
                undo: function() {
                    if (linkNM) graph.removeCells([linkNM]);
                    if (window._linkMap) delete window._linkMap[linkKeyNM];
                }
            });

        } else {
            // 1:1 or 1:N
            var sourceCard = '1';
            var targetCard = cardinality === '1:1' ? '1' : 'N';

            // FK column on target (child) table
            var fkCol = {
                name: fkColName,
                type: 'Integer',
                nullable: false,
                primary_key: false,
                foreign_key: (sourceData.schema ? sourceData.schema + '.' : '') + sourceData.table_name + '.id',
                unique: cardinality === '1:1',
                index: true,
                default: null,
                server_default: null
            };

            // Relationship on source (parent) side
            var sourceRel = {
                name: sourceRelName,
                target: targetData.class_name,
                back_populates: backPop ? targetRelName : null,
                cascade: cascade,
                lazy: lazy,
                uselist: cardinality !== '1:1',
                order_by: null
            };

            // Relationship on target (child) side
            var targetRel = {
                name: targetRelName,
                target: sourceData.class_name,
                back_populates: backPop ? sourceRelName : null,
                cascade: null,
                lazy: null,
                uselist: false,
                order_by: null
            };

            // Add FK column to target
            commands.push({
                execute: function() {
                    targetData.columns.push(fkCol);
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                },
                undo: function() {
                    var idx = targetData.columns.indexOf(fkCol);
                    if (idx >= 0) targetData.columns.splice(idx, 1);
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                }
            });

            // Add relationship on source
            commands.push({
                execute: function() {
                    sourceData.relationships.push(sourceRel);
                    sourceEl.set('tableData', sourceData);
                    ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                },
                undo: function() {
                    var idx = sourceData.relationships.indexOf(sourceRel);
                    if (idx >= 0) sourceData.relationships.splice(idx, 1);
                    sourceEl.set('tableData', sourceData);
                    ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                }
            });

            // Add relationship on target
            commands.push({
                execute: function() {
                    targetData.relationships.push(targetRel);
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                },
                undo: function() {
                    var idx = targetData.relationships.indexOf(targetRel);
                    if (idx >= 0) targetData.relationships.splice(idx, 1);
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                }
            });

            // Create JointJS link
            var linkKey = sourceData.class_name + '->' + targetData.class_name;
            var link = null;
            commands.push({
                execute: function() {
                    link = ERShapes.createLink(sourceEl.id, targetEl.id, sourceCard, targetCard);
                    graph.addCell(link);
                    if (window._linkMap) window._linkMap[linkKey] = link;
                },
                undo: function() {
                    if (link) graph.removeCells([link]);
                    if (window._linkMap) delete window._linkMap[linkKey];
                }
            });
        }

        // Dirty tracking + preview refresh
        commands.push({
            execute: function() { markDirty(); if (typeof ERPreview !== 'undefined') ERPreview.scheduleRefresh(); },
            undo: function() { markDirty(); if (typeof ERPreview !== 'undefined') ERPreview.scheduleRefresh(); }
        });

        ERUndo.execute(ERUndo.compound(commands));
    }

    /**
     * Show the relationship edit popup.
     * @param {joint.dia.Element} sourceEl - Source (parent) element
     * @param {joint.dia.Element} targetEl - Target (child) element
     * @param {Object|null} sourceRel - Relationship on source side
     * @param {Object|null} targetRel - Relationship on target side
     * @param {Object|null} fkCol - FK column on target table
     * @param {Object|null} link - JointJS link object
     * @param {HTMLElement|Object} anchorEl - Anchor for popup positioning
     */
    function showRelationshipEditPopup(sourceEl, targetEl, sourceRel, targetRel, fkCol, link, anchorEl) {
        var sourceData = sourceEl.get('tableData');
        var targetData = targetEl.get('tableData');

        var html = '<h3>Edit Relationship</h3>';

        // Source relationship name
        html += '<div class="er-popup-field">';
        html += '<label>' + _escapeHtml(sourceData.class_name) + '.' + _escapeHtml(sourceRel ? sourceRel.name : '?') + '</label>';
        html += '<input type="text" id="popup-redit-source-name" value="' + _escapeAttr(sourceRel ? sourceRel.name : '') + '" />';
        html += '</div>';

        // Target relationship name
        html += '<div class="er-popup-field">';
        html += '<label>' + _escapeHtml(targetData.class_name) + '.' + _escapeHtml(targetRel ? targetRel.name : '?') + '</label>';
        html += '<input type="text" id="popup-redit-target-name" value="' + _escapeAttr(targetRel ? targetRel.name : '') + '" />';
        html += '</div>';

        // back_populates
        html += '<div class="er-popup-field er-popup-checkbox">';
        html += '<input type="checkbox" id="popup-redit-backpop"' + (sourceRel && sourceRel.back_populates ? ' checked' : '') + ' />';
        html += '<label for="popup-redit-backpop">back_populates</label>';
        html += '</div>';

        // cascade
        html += '<div class="er-popup-field">';
        html += '<label>Cascade</label>';
        html += '<select id="popup-redit-cascade">';
        ['', 'all', 'all, delete-orphan', 'save-update, merge'].forEach(function(v) {
            var label = v || 'none';
            var selected = (sourceRel && sourceRel.cascade === (v || null)) ? ' selected' : '';
            html += '<option value="' + _escapeAttr(v) + '"' + selected + '>' + _escapeHtml(label) + '</option>';
        });
        html += '</select></div>';

        // lazy
        html += '<div class="er-popup-field">';
        html += '<label>Lazy</label>';
        html += '<select id="popup-redit-lazy">';
        ['select', 'joined', 'subquery', 'dynamic', 'selectin'].forEach(function(v) {
            var selected = (sourceRel && sourceRel.lazy === v) ? ' selected' : '';
            html += '<option value="' + v + '"' + selected + '>' + v + '</option>';
        });
        html += '</select></div>';

        // Actions
        html += '<div class="er-popup-actions">';
        html += '<button class="er-popup-btn er-popup-btn--secondary" id="popup-redit-delete" style="margin-right:auto;color:#ef4444;">Delete</button>';
        html += '<button class="er-popup-btn er-popup-btn--secondary" id="popup-redit-cancel">Cancel</button>';
        html += '<button class="er-popup-btn er-popup-btn--primary" id="popup-redit-apply">Apply</button>';
        html += '</div>';

        showPopup(anchorEl, html, null);

        document.getElementById('popup-redit-cancel').addEventListener('click', function() { closePopup(); });
        document.getElementById('popup-redit-apply').addEventListener('click', function() {
            applyRelationshipChanges(sourceEl, targetEl, sourceRel, targetRel);
        });
        document.getElementById('popup-redit-delete').addEventListener('click', function() {
            closePopup();
            deleteRelationship(sourceEl, targetEl, sourceRel, targetRel, fkCol, link);
        });
    }

    /**
     * Apply relationship edit changes from the edit popup.
     * Creates a single undo command to change names, back_populates, cascade, lazy.
     */
    function applyRelationshipChanges(sourceEl, targetEl, sourceRel, targetRel) {
        var paper = ERCanvas.getPaper();
        var sourceData = sourceEl.get('tableData');
        var targetData = targetEl.get('tableData');

        var newSourceName = document.getElementById('popup-redit-source-name').value.trim();
        var newTargetName = document.getElementById('popup-redit-target-name').value.trim();
        var backPop = document.getElementById('popup-redit-backpop').checked;
        var cascade = document.getElementById('popup-redit-cascade').value || null;
        var lazy = document.getElementById('popup-redit-lazy').value || null;

        var oldSource = sourceRel ? { name: sourceRel.name, back_populates: sourceRel.back_populates, cascade: sourceRel.cascade, lazy: sourceRel.lazy } : null;
        var oldTarget = targetRel ? { name: targetRel.name, back_populates: targetRel.back_populates } : null;

        var cmd = {
            execute: function() {
                if (sourceRel) {
                    sourceRel.name = newSourceName;
                    sourceRel.back_populates = backPop ? newTargetName : null;
                    sourceRel.cascade = cascade;
                    sourceRel.lazy = lazy;
                    sourceEl.set('tableData', sourceData);
                    ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                }
                if (targetRel) {
                    targetRel.name = newTargetName;
                    targetRel.back_populates = backPop ? newSourceName : null;
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                }
                markDirty();
                if (typeof ERPreview !== 'undefined') ERPreview.scheduleRefresh();
            },
            undo: function() {
                if (sourceRel && oldSource) {
                    sourceRel.name = oldSource.name;
                    sourceRel.back_populates = oldSource.back_populates;
                    sourceRel.cascade = oldSource.cascade;
                    sourceRel.lazy = oldSource.lazy;
                    sourceEl.set('tableData', sourceData);
                    ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                }
                if (targetRel && oldTarget) {
                    targetRel.name = oldTarget.name;
                    targetRel.back_populates = oldTarget.back_populates;
                    targetEl.set('tableData', targetData);
                    ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                }
                markDirty();
                if (typeof ERPreview !== 'undefined') ERPreview.scheduleRefresh();
            }
        };
        ERUndo.execute(cmd);
        closePopup();
    }

    /**
     * Delete a relationship with confirmation.
     * Compound undo: removes FK column, both relationship attrs, and the JointJS link.
     */
    function deleteRelationship(sourceEl, targetEl, sourceRel, targetRel, fkCol, link) {
        var sourceData = sourceEl.get('tableData');
        var targetData = targetEl.get('tableData');
        var fkName = fkCol ? fkCol.name : '?';
        var msg = 'Delete relationship? This removes the FK column "' + fkName + '" and relationship attributes from both "' + sourceData.class_name + '" and "' + targetData.class_name + '".';

        showConfirmation(sourceEl, msg, function() {
            var paper = ERCanvas.getPaper();
            var graph = ERCanvas.getGraph();
            var commands = [];
            var sourceRelIdx = sourceRel ? sourceData.relationships.indexOf(sourceRel) : -1;
            var targetRelIdx = targetRel ? targetData.relationships.indexOf(targetRel) : -1;
            var fkColIdx = fkCol ? targetData.columns.indexOf(fkCol) : -1;

            // Remove FK column from target
            if (fkCol && fkColIdx >= 0) {
                commands.push({
                    execute: function() {
                        var idx = targetData.columns.indexOf(fkCol);
                        if (idx >= 0) targetData.columns.splice(idx, 1);
                        targetEl.set('tableData', targetData);
                        ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                    },
                    undo: function() {
                        targetData.columns.splice(fkColIdx, 0, fkCol);
                        targetEl.set('tableData', targetData);
                        ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                    }
                });
            }

            // Remove relationship from source
            if (sourceRel && sourceRelIdx >= 0) {
                commands.push({
                    execute: function() {
                        var idx = sourceData.relationships.indexOf(sourceRel);
                        if (idx >= 0) sourceData.relationships.splice(idx, 1);
                        sourceEl.set('tableData', sourceData);
                        ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                    },
                    undo: function() {
                        sourceData.relationships.splice(sourceRelIdx, 0, sourceRel);
                        sourceEl.set('tableData', sourceData);
                        ERShapes.updateTable(sourceEl, paper, sourceEl.get('collapsed') || false);
                    }
                });
            }

            // Remove relationship from target
            if (targetRel && targetRelIdx >= 0) {
                commands.push({
                    execute: function() {
                        var idx = targetData.relationships.indexOf(targetRel);
                        if (idx >= 0) targetData.relationships.splice(idx, 1);
                        targetEl.set('tableData', targetData);
                        ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                    },
                    undo: function() {
                        targetData.relationships.splice(targetRelIdx, 0, targetRel);
                        targetEl.set('tableData', targetData);
                        ERShapes.updateTable(targetEl, paper, targetEl.get('collapsed') || false);
                    }
                });
            }

            // Remove link
            if (link) {
                var linkKey = sourceData.class_name + '->' + targetData.class_name;
                commands.push({
                    execute: function() { graph.removeCells([link]); if (window._linkMap) delete window._linkMap[linkKey]; },
                    undo: function() { graph.addCell(link); if (window._linkMap) window._linkMap[linkKey] = link; }
                });
            }

            commands.push({
                execute: function() { markDirty(); if (typeof ERPreview !== 'undefined') ERPreview.scheduleRefresh(); },
                undo: function() { markDirty(); if (typeof ERPreview !== 'undefined') ERPreview.scheduleRefresh(); }
            });

            ERUndo.execute(ERUndo.compound(commands));
        });
    }

    /**
     * Wire link click and relationship row click to open edit popup.
     * Called from init().
     */
    function _setupRelationshipClickHandlers() {
        var paper = ERCanvas.getPaper();
        var graph = ERCanvas.getGraph();

        // Link click -> relationship edit popup
        paper.on('link:pointerclick', function(linkView) {
            var link = linkView.model;
            var srcId = link.source().id;
            var tgtId = link.target().id;

            var srcEl = graph.getCell(srcId);
            var tgtEl = graph.getCell(tgtId);
            if (!srcEl || !tgtEl) return;

            var srcData = srcEl.get('tableData');
            var tgtData = tgtEl.get('tableData');
            if (!srcData || !tgtData) return;

            var srcRel = srcData.relationships.find(function(r) { return r.target === tgtData.class_name; });
            var tgtRel = tgtData.relationships.find(function(r) { return r.target === srcData.class_name; });
            var fkCol = tgtData.columns.find(function(c) { return c.foreign_key && c.foreign_key.indexOf(srcData.table_name) !== -1; });

            showRelationshipEditPopup(srcEl, tgtEl, srcRel, tgtRel, fkCol, link, linkView.el);
        });

        // Relationship row click -> same popup
        document.addEventListener('click', function(evt) {
            var row = evt.target.closest('.er-rel-row[data-rel-name]');
            if (!row) return;

            var relName = row.getAttribute('data-rel-name');
            if (!relName) return;

            var jointEl = row.closest('.joint-element');
            if (!jointEl) return;

            // Find JointJS model from DOM
            var elements = graph.getElements();
            var element = null;
            for (var i = 0; i < elements.length; i++) {
                var elView = elements[i].findView(paper);
                if (elView && elView.el === jointEl) {
                    element = elements[i];
                    break;
                }
            }
            if (!element) return;

            var tableData = element.get('tableData');
            if (!tableData) return;

            var rel = tableData.relationships.find(function(r) { return r.name === relName; });
            if (!rel) return;

            // Find counterpart table
            var targetClassName = rel.target;
            var targetEl = null;
            for (var j = 0; j < elements.length; j++) {
                var td = elements[j].get('tableData');
                if (td && td.class_name === targetClassName) {
                    targetEl = elements[j];
                    break;
                }
            }
            if (!targetEl) return;

            var targetData = targetEl.get('tableData');

            // Determine source/target pair (which side has the FK)
            var sourceEl, srcData, srcRel, tgtEl, tgtData, tgtRel, fkCol;
            var counterpartRel = targetData.relationships.find(function(r) { return r.target === tableData.class_name; });
            var hasFkToTarget = tableData.columns.find(function(c) { return c.foreign_key && c.foreign_key.indexOf(targetData.table_name) !== -1; });

            if (hasFkToTarget) {
                // Clicked table is child (has FK), target is parent
                sourceEl = targetEl; srcData = targetData;
                tgtEl = element; tgtData = tableData;
                srcRel = counterpartRel;
                tgtRel = rel;
                fkCol = hasFkToTarget;
            } else {
                // Clicked table is parent, target is child
                sourceEl = element; srcData = tableData;
                tgtEl = targetEl; tgtData = targetData;
                srcRel = rel;
                tgtRel = counterpartRel;
                fkCol = tgtData.columns.find(function(c) { return c.foreign_key && c.foreign_key.indexOf(srcData.table_name) !== -1; });
            }

            // Find JointJS link
            var linkKey = srcData.class_name + '->' + tgtData.class_name;
            var link = window._linkMap ? window._linkMap[linkKey] : null;

            showRelationshipEditPopup(sourceEl, tgtEl, srcRel, tgtRel, fkCol, link, row);
            evt.stopPropagation();
        }, true);
    }

    // --- Public API ---

    return {
        init: init,
        getSchema: getSchema,
        isDirty: isDirty,
        markDirty: markDirty,
        markClean: markClean,
        save: save,
        trackDeletion: trackDeletion,
        untrackDeletion: untrackDeletion,
        showToast: showToast,
        showPopup: showPopup,
        closePopup: closePopup,
        getActivePopup: getActivePopup,
        showConfirmation: showConfirmation,
        setupRelationshipDrag: setupRelationshipDrag
    };
})();
