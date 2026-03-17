// preview.js - Code preview panel with live Python output, syntax highlighting, auto-scroll
// Exposes: window.ERPreview
var ERPreview = (function() {
    'use strict';

    var DEBOUNCE_MS = 500;
    var _panel = null;
    var _codeEl = null;
    var _loadingBar = null;
    var _previewBtn = null;
    var _previewTab = null;
    var _isOpen = false;
    var _debounceTimer = null;
    var _resizing = false;
    var _selectedClassName = null;

    function init() {
        _panel = document.getElementById('preview-panel');
        _codeEl = _panel.querySelector('code.language-python');
        _loadingBar = _panel.querySelector('.preview-loading');
        _previewBtn = document.getElementById('btn-preview');
        _previewTab = document.getElementById('preview-tab');

        // Close button
        _panel.querySelector('.preview-close').addEventListener('click', close);

        // Reopen tab
        _previewTab.addEventListener('click', open);

        // Resize handle
        setupResize();
    }

    function open() {
        _isOpen = true;
        _panel.classList.add('is-open');
        _previewTab.classList.remove('is-visible');
        _previewBtn.style.background = '#e5e7eb'; // pressed state
        document.body.classList.add('preview-open');
        refresh(); // Fetch immediately on open
    }

    function close() {
        _isOpen = false;
        _panel.classList.remove('is-open');
        _previewTab.classList.add('is-visible');
        _previewBtn.style.background = ''; // reset
        document.body.classList.remove('preview-open');
    }

    function toggle() {
        if (_isOpen) close(); else open();
    }

    function isOpen() { return _isOpen; }

    // Called by editor after any schema mutation
    function scheduleRefresh() {
        if (!_isOpen) return;
        clearTimeout(_debounceTimer);
        _debounceTimer = setTimeout(refresh, DEBOUNCE_MS);
    }

    async function refresh() {
        if (!_isOpen) return;
        var schema = EREditor.getSchema();
        if (!schema || !schema.tables) return;

        // Show loading bar
        _loadingBar.classList.add('is-loading');

        try {
            var res = await fetch('/api/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tables: schema.tables })
            });
            if (!res.ok) throw new Error('Preview failed');
            var data = await res.json();
            renderCode(data.code);
        } catch (err) {
            _codeEl.textContent = '# Could not generate preview. ' + err.message;
        } finally {
            _loadingBar.classList.remove('is-loading');
        }
    }

    function renderCode(code) {
        _codeEl.textContent = code;
        // Apply syntax highlighting
        if (window.hljs) {
            hljs.highlightElement(_codeEl);
        }
        // Auto-scroll to selected table
        if (_selectedClassName) {
            scrollToClass(_selectedClassName);
        }
    }

    function scrollToClass(className) {
        _selectedClassName = className;
        if (!_isOpen || !_codeEl.textContent) return;

        // Remove previous highlights
        var existingHighlights = _panel.querySelectorAll('.preview-highlight');
        existingHighlights.forEach(function(el) { el.remove(); });

        // Find the class definition line in the code
        var lines = _codeEl.textContent.split('\n');
        var classPattern = 'class ' + className + '(';
        var startLine = -1;
        var endLine = -1;

        for (var i = 0; i < lines.length; i++) {
            if (lines[i].indexOf(classPattern) !== -1) {
                startLine = i;
            }
            // Find end of class (next class or end of file)
            if (startLine >= 0 && i > startLine) {
                if (lines[i].match(/^class /) || (i === lines.length - 1)) {
                    endLine = lines[i].match(/^class /) ? i - 1 : i;
                    break;
                }
            }
        }

        if (startLine >= 0) {
            // Scroll to the class definition
            var lineHeight = 18; // 12px * 1.5 line-height
            var scrollContainer = _panel.querySelector('.preview-code');
            var targetScroll = startLine * lineHeight - scrollContainer.clientHeight / 3;
            scrollContainer.scrollTo({ top: Math.max(0, targetScroll), behavior: 'smooth' });
        }
    }

    function setupResize() {
        var handle = _panel.querySelector('.resize-handle');
        var startX, startWidth;

        handle.addEventListener('mousedown', function(e) {
            _resizing = true;
            startX = e.clientX;
            startWidth = _panel.offsetWidth;
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        });

        document.addEventListener('mousemove', function(e) {
            if (!_resizing) return;
            var delta = startX - e.clientX; // moving left = wider panel
            var newWidth = Math.max(280, Math.min(window.innerWidth * 0.5, startWidth + delta));
            _panel.style.width = newWidth + 'px';
            document.querySelector('#canvas-container').style.right = newWidth + 'px';
        });

        document.addEventListener('mouseup', function() {
            if (_resizing) {
                _resizing = false;
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }
        });
    }

    // Called when canvas selection changes
    function setSelectedTable(className) {
        _selectedClassName = className;
        if (_isOpen) {
            scrollToClass(className);
        }
    }

    function clearSelectedTable() {
        _selectedClassName = null;
    }

    return {
        init: init,
        open: open,
        close: close,
        toggle: toggle,
        isOpen: isOpen,
        scheduleRefresh: scheduleRefresh,
        refresh: refresh,
        setSelectedTable: setSelectedTable,
        clearSelectedTable: clearSelectedTable
    };
})();
