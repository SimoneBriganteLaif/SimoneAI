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
        showConfirmation: showConfirmation
    };
})();
