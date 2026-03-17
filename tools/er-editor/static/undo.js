// undo.js - Command pattern undo/redo stack
// Exposes: window.ERUndo
var ERUndo = (function() {
    'use strict';

    var undoStack = [];
    var redoStack = [];
    var MAX_STACK = 100;
    var _onChangeCallback = null;

    /**
     * Execute a command and push it onto the undo stack.
     * Clears the redo stack (forward history is lost on new action).
     * @param {{ execute: Function, undo: Function }} command
     */
    function execute(command) {
        command.execute();
        undoStack.push(command);
        if (undoStack.length > MAX_STACK) undoStack.shift();
        redoStack = [];
        if (_onChangeCallback) _onChangeCallback();
    }

    /**
     * Undo the last command. Moves it to the redo stack.
     */
    function undo() {
        if (undoStack.length === 0) return;
        var cmd = undoStack.pop();
        cmd.undo();
        redoStack.push(cmd);
        if (_onChangeCallback) _onChangeCallback();
    }

    /**
     * Redo the last undone command. Moves it back to the undo stack.
     */
    function redo() {
        if (redoStack.length === 0) return;
        var cmd = redoStack.pop();
        cmd.execute();
        undoStack.push(cmd);
        if (_onChangeCallback) _onChangeCallback();
    }

    /** @returns {boolean} Whether there are commands to undo */
    function canUndo() { return undoStack.length > 0; }

    /** @returns {boolean} Whether there are commands to redo */
    function canRedo() { return redoStack.length > 0; }

    /** Clear both stacks (e.g., after save or load) */
    function clear() {
        undoStack = [];
        redoStack = [];
        if (_onChangeCallback) _onChangeCallback();
    }

    /**
     * Register a callback fired whenever stacks change.
     * Used to update toolbar button states.
     * @param {Function} cb
     */
    function onChange(cb) { _onChangeCallback = cb; }

    /**
     * Create a compound command from multiple sub-commands.
     * Executes all in order, undoes all in reverse order.
     * @param {Array<{ execute: Function, undo: Function }>} commands
     * @returns {{ execute: Function, undo: Function }}
     */
    function compound(commands) {
        return {
            execute: function() {
                commands.forEach(function(c) { c.execute(); });
            },
            undo: function() {
                for (var i = commands.length - 1; i >= 0; i--) {
                    commands[i].undo();
                }
            }
        };
    }

    return {
        execute: execute,
        undo: undo,
        redo: redo,
        canUndo: canUndo,
        canRedo: canRedo,
        clear: clear,
        onChange: onChange,
        compound: compound
    };
})();
