// shapes.js - ERTable and ERLink factories for JointJS ER diagram
// Exposes: window.ERShapes
(function() {
    'use strict';

    var COLORS = {
        headerBg: '#374151',
        headerText: '#ffffff',
        bodyBg: '#ffffff',
        bodyText: '#1f2937',
        border: '#d1d5db',
        borderSelected: '#3b82f6',
        pkIcon: '#d97706',
        fkIcon: '#2563eb',
        badgeBg: '#f3f4f6',
        badgeText: '#6b7280',
        relLine: '#6b7280',
        relLineHover: '#3b82f6',
        divider: '#e5e7eb',
        cardinalityText: '#374151'
    };

    var DIMS = {
        headerH: 32,
        rowH: 22,
        bodyPadV: 8,
        bodyPadH: 16,
        dividerMargin: 4,
        minW: 240,
        maxW: 500,
        charW: 7.2
    };

    // PK icon SVG (key shape, 14x14)
    var PK_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">' +
        '<circle cx="5" cy="5" r="3" fill="none" stroke="' + COLORS.pkIcon + '" stroke-width="1.5"/>' +
        '<line x1="8" y1="5" x2="13" y2="5" stroke="' + COLORS.pkIcon + '" stroke-width="1.5"/>' +
        '<line x1="11" y1="5" x2="11" y2="8" stroke="' + COLORS.pkIcon + '" stroke-width="1.5"/>' +
        '</svg>';

    // FK icon SVG (link shape, 14x14)
    var FK_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">' +
        '<path d="M3 4 A3 3 0 0 1 3 10 M11 4 A3 3 0 0 0 11 10 M5 7 L9 7" ' +
        'fill="none" stroke="' + COLORS.fkIcon + '" stroke-width="1.5" stroke-linecap="round"/>' +
        '</svg>';

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }

    function buildColumnRow(col) {
        var html = '<tr class="er-col-row">';
        // Icon cell
        html += '<td class="er-col-icon">';
        if (col.primary_key) {
            html += PK_ICON;
        } else if (col.foreign_key) {
            html += FK_ICON;
        }
        html += '</td>';
        // Name cell
        html += '<td class="er-col-name">' + escapeHtml(col.name) + '</td>';
        // Type cell
        html += '<td class="er-col-type">' + escapeHtml(col.type) + '</td>';
        // Badges cell
        html += '<td class="er-col-badges">';
        if (col.nullable === false) {
            html += '<span class="er-badge">NN</span>';
        }
        if (col.unique) {
            html += '<span class="er-badge">UQ</span>';
        }
        if (col.index) {
            html += '<span class="er-badge">IDX</span>';
        }
        html += '</td>';
        html += '</tr>';
        return html;
    }

    function buildRelHTML(rel) {
        var targetDisplay = rel.uselist ? escapeHtml(rel.target) + '[]' : escapeHtml(rel.target);
        return '<div class="er-rel-row">' +
            '<span class="er-rel-arrow">&harr;</span> ' +
            '<span class="er-rel-name">' + escapeHtml(rel.name) + '</span>' +
            ' <span class="er-rel-target">&rarr; ' + targetDisplay + '</span>' +
            '</div>';
    }

    function computeTableSize(tableData, collapsed) {
        var visibleCols = collapsed
            ? tableData.columns.filter(function(c) { return c.primary_key || c.foreign_key; })
            : tableData.columns;
        var hiddenCount = tableData.columns.length - visibleCols.length;
        var rels = tableData.relationships || [];

        // Width calculation: icon(24) + name + type + badges(80) + padding
        var headerLabel = tableData.schema
            ? tableData.class_name + ' (' + tableData.schema + '.' + tableData.table_name + ')'
            : tableData.class_name + ' (' + tableData.table_name + ')';
        var maxNameW = 0;
        var maxTypeW = 0;
        visibleCols.forEach(function(c) {
            maxNameW = Math.max(maxNameW, c.name.length * DIMS.charW);
            maxTypeW = Math.max(maxTypeW, c.type.length * DIMS.charW);
        });
        var tableContentW = 24 + 12 + maxNameW + 8 + maxTypeW + 80; // icon + pad + name + gap + type + badges
        var headerW = headerLabel.length * 8;
        rels.forEach(function(r) {
            var relText = '<-> ' + r.name + ' -> ' + r.target + (r.uselist ? '[]' : '');
            tableContentW = Math.max(tableContentW, relText.length * DIMS.charW + 16);
        });
        var width = Math.min(DIMS.maxW, Math.max(DIMS.minW, Math.max(tableContentW, headerW + 16)));

        // Height calculation
        var colsH = visibleCols.length * DIMS.rowH;
        var collapsedH = (collapsed && hiddenCount > 0) ? DIMS.rowH : 0;
        var hasDivider = rels.length > 0;
        var dividerH = hasDivider ? (DIMS.dividerMargin + 1 + DIMS.dividerMargin) : 0;
        var relsH = rels.length * DIMS.rowH;
        var height = DIMS.headerH + DIMS.bodyPadV + colsH + collapsedH + dividerH + relsH + DIMS.bodyPadV;

        return {
            width: width,
            height: height,
            visibleCols: visibleCols,
            hiddenCount: hiddenCount,
            rels: rels
        };
    }

    function buildBodyHTML(visibleCols, hiddenCount, rels, collapsed) {
        var html = '<div class="er-body" style="padding: ' + DIMS.bodyPadV + 'px 0;">';
        // Columns table
        html += '<table class="er-col-table"><tbody>';
        visibleCols.forEach(function(c) {
            html += buildColumnRow(c);
        });
        if (collapsed && hiddenCount > 0) {
            html += '<tr><td colspan="4" class="er-collapsed-indicator">\u25B6 ' + hiddenCount + ' more columns</td></tr>';
        }
        html += '</tbody></table>';
        // Relationships
        if (rels.length > 0) {
            html += '<div class="er-divider"></div>';
            rels.forEach(function(r) {
                html += buildRelHTML(r);
            });
        }
        html += '</div>';
        return html;
    }

    function buildHeaderLabel(tableData) {
        return tableData.schema
            ? tableData.class_name + ' (' + tableData.schema + '.' + tableData.table_name + ')'
            : tableData.class_name + ' (' + tableData.table_name + ')';
    }

    window.ERShapes = {
        COLORS: COLORS,
        DIMS: DIMS,

        /**
         * Create a JointJS element representing an ER table.
         * @param {Object} tableData - {class_name, table_name, schema, columns, relationships}
         * @param {Object} position - {x, y}
         * @param {boolean} collapsed - Whether to show only PK/FK columns
         * @returns {joint.dia.Element} JointJS element instance
         */
        createTable: function(tableData, position, collapsed) {
            collapsed = collapsed || false;
            var computed = computeTableSize(tableData, collapsed);
            var bodyHTML = buildBodyHTML(computed.visibleCols, computed.hiddenCount, computed.rels, collapsed);
            var headerLabel = buildHeaderLabel(tableData);

            var el = new joint.dia.Element({
                type: 'er.Table',
                size: { width: computed.width, height: computed.height },
                position: position || { x: 0, y: 0 },
                attrs: {
                    root: {
                        cursor: 'move'
                    },
                    headerRect: {
                        width: 'calc(w)',
                        height: DIMS.headerH,
                        fill: COLORS.headerBg,
                        stroke: COLORS.border,
                        strokeWidth: 1,
                        rx: 4,
                        ry: 4
                    },
                    headerText: {
                        x: 'calc(0.5*w)',
                        y: DIMS.headerH / 2,
                        textAnchor: 'middle',
                        textVerticalAnchor: 'middle',
                        fill: COLORS.headerText,
                        fontSize: 13,
                        fontWeight: 600,
                        fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", "Consolas", monospace',
                        text: headerLabel
                    },
                    bodyRect: {
                        width: 'calc(w)',
                        height: 'calc(h - ' + DIMS.headerH + ')',
                        y: DIMS.headerH,
                        fill: COLORS.bodyBg,
                        stroke: COLORS.border,
                        strokeWidth: 1
                    },
                    bodyContent: {
                        refX: 0,
                        refY: DIMS.headerH,
                        width: 'calc(w)',
                        height: 'calc(h - ' + DIMS.headerH + ')',
                        html: bodyHTML
                    }
                },
                markup: [
                    { tagName: 'rect', selector: 'headerRect' },
                    { tagName: 'text', selector: 'headerText' },
                    { tagName: 'rect', selector: 'bodyRect' },
                    { tagName: 'foreignObject', selector: 'bodyContent', attributes: { overflow: 'hidden' } }
                ],
                // Store table data for later reference (collapse/expand, search)
                tableData: tableData,
                collapsed: collapsed
            });

            return el;
        },

        /**
         * Update an existing ERTable element when collapse state changes.
         * Recalculates size and rebuilds body HTML.
         * @param {joint.dia.Element} element - The ERTable element
         * @param {joint.dia.Paper} paper - The paper instance
         * @param {boolean} collapsed - New collapse state
         */
        updateTable: function(element, paper, collapsed) {
            var tableData = element.get('tableData');
            var computed = computeTableSize(tableData, collapsed);
            var bodyHTML = buildBodyHTML(computed.visibleCols, computed.hiddenCount, computed.rels, collapsed);

            element.set('collapsed', collapsed);
            element.resize(computed.width, computed.height);
            element.attr('bodyContent/html', bodyHTML);
            element.attr('bodyContent/height', 'calc(h - ' + DIMS.headerH + ')');
            element.attr('bodyRect/height', 'calc(h - ' + DIMS.headerH + ')');
        },

        /**
         * Create a JointJS link representing a relationship between tables.
         * Uses manhattan (orthogonal) routing with rounded connectors.
         * @param {string} sourceId - Source element ID
         * @param {string} targetId - Target element ID
         * @param {string} sourceCardinality - "1", "N", or "M"
         * @param {string} targetCardinality - "1", "N", or "M"
         * @returns {joint.shapes.standard.Link} JointJS link instance
         */
        createLink: function(sourceId, targetId, sourceCardinality, targetCardinality, savedVertices) {
            var config = {
                source: { id: sourceId },
                target: { id: targetId },
                router: {
                    name: 'manhattan',
                    args: {
                        padding: 30,
                        step: 10,
                        maximumLoops: 5000
                    }
                },
                connector: {
                    name: 'rounded',
                    args: { radius: 8 }
                },
                attrs: {
                    line: {
                        stroke: COLORS.relLine,
                        strokeWidth: 1.5,
                        targetMarker: {
                            type: 'path',
                            d: 'M 10 -5 0 0 10 5 z',
                            fill: COLORS.relLine
                        }
                    }
                },
                labels: [
                    {
                        position: { distance: 24, offset: -14, args: { absoluteDistance: true } },
                        attrs: {
                            text: {
                                text: sourceCardinality || '1',
                                fontSize: 11,
                                fontWeight: 600,
                                fontFamily: '"JetBrains Mono", monospace',
                                fill: COLORS.cardinalityText
                            },
                            rect: { fill: 'white', rx: 2, ry: 2 }
                        }
                    },
                    {
                        position: { distance: -24, offset: -14, args: { absoluteDistance: true } },
                        attrs: {
                            text: {
                                text: targetCardinality || 'N',
                                fontSize: 11,
                                fontWeight: 600,
                                fontFamily: '"JetBrains Mono", monospace',
                                fill: COLORS.cardinalityText
                            },
                            rect: { fill: 'white', rx: 2, ry: 2 }
                        }
                    }
                ]
            };

            // Restore saved vertices (manual routing by user)
            if (savedVertices && savedVertices.length > 0) {
                config.vertices = savedVertices;
            }

            var link = new joint.shapes.standard.Link(config);
            return link;
        }
    };
})();
