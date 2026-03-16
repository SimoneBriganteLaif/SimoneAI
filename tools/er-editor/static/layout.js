// layout.js - Dagre auto-layout for JointJS ER diagram
// Exposes: window.ERLayout
(function() {
    'use strict';

    function autoLayout(graph) {
        var g = new dagre.graphlib.Graph();
        g.setGraph({
            rankdir: 'TB',      // Top to bottom (per user decision)
            nodesep: 60,        // Horizontal gap between siblings (from UI-SPEC)
            ranksep: 80,        // Vertical gap between ranks (from UI-SPEC)
            marginx: 40,
            marginy: 40
        });
        g.setDefaultEdgeLabel(function() { return {}; });

        // Add nodes with their current sizes
        graph.getElements().forEach(function(el) {
            var size = el.size();
            g.setNode(el.id, { width: size.width, height: size.height });
        });

        // Add edges from links
        graph.getLinks().forEach(function(link) {
            var srcId = link.source().id;
            var tgtId = link.target().id;
            if (srcId && tgtId) {
                g.setEdge(srcId, tgtId);
            }
        });

        // Compute layout
        dagre.layout(g);

        // Apply positions (dagre returns center coords, JointJS uses top-left)
        g.nodes().forEach(function(nodeId) {
            var node = g.node(nodeId);
            var el = graph.getCell(nodeId);
            if (el && node) {
                el.position(
                    Math.round((node.x - node.width / 2) / 20) * 20,   // Snap to 20px grid
                    Math.round((node.y - node.height / 2) / 20) * 20
                );
            }
        });
    }

    window.ERLayout = {
        autoLayout: autoLayout
    };
})();
