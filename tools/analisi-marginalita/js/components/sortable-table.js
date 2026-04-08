// ═══════════════════════════════════════════════════════
// Factory tabella sortabile
// ═══════════════════════════════════════════════════════

function buildSortableTable(tableEl, columns, data, opts = {}) {
  const thead = tableEl.querySelector('thead tr');
  const tbody = tableEl.querySelector('tbody');
  let sortCol = opts.defaultSort || 0;
  let sortAsc = opts.defaultAsc !== undefined ? opts.defaultAsc : true;

  function render() {
    const sorted = [...data].sort((a, b) => {
      const col = columns[sortCol];
      let va = col.value ? col.value(a) : a[col.key];
      let vb = col.value ? col.value(b) : b[col.key];
      if (va == null) va = col.numeric ? -Infinity : '';
      if (vb == null) vb = col.numeric ? -Infinity : '';
      if (col.numeric) return sortAsc ? va - vb : vb - va;
      return sortAsc ? String(va).localeCompare(String(vb), 'it') : String(vb).localeCompare(String(va), 'it');
    });

    thead.innerHTML = columns.map((c, i) => {
      const arrow = i === sortCol ? (sortAsc ? ' \u25B2' : ' \u25BC') : '';
      const cls = i === sortCol ? ' class="sorted"' : '';
      const align = c.numeric ? ' style="text-align:right"' : '';
      return `<th${cls}${align} data-idx="${i}">${c.label}<span class="sort-arrow">${arrow}</span></th>`;
    }).join('');

    tbody.innerHTML = sorted.map((row, ri) => {
      const rowClass = opts.rowClass ? opts.rowClass(row) : '';
      const clickable = opts.onRowClick ? ' class="clickable ' + rowClass + '"' : (rowClass ? ` class="${rowClass}"` : '');
      const cells = columns.map(c => {
        const val = c.render ? c.render(row) : (c.value ? c.value(row) : row[c.key]);
        const cls = c.numeric ? ' class="num"' : (c.cellClass ? ` class="${c.cellClass(row)}"` : '');
        return `<td${cls}>${val ?? '\u2014'}</td>`;
      }).join('');
      return `<tr${clickable} data-idx="${ri}">${cells}</tr>`;
    }).join('');

    thead.querySelectorAll('th').forEach(th => {
      th.addEventListener('click', () => {
        const idx = parseInt(th.dataset.idx);
        if (idx === sortCol) { sortAsc = !sortAsc; }
        else { sortCol = idx; sortAsc = columns[idx].numeric ? false : true; }
        render();
      });
    });

    if (opts.onRowClick) {
      tbody.querySelectorAll('tr').forEach(tr => {
        tr.addEventListener('click', () => {
          opts.onRowClick(sorted[parseInt(tr.dataset.idx)], tr);
        });
      });
    }
  }

  tableEl._render = render;
  tableEl._updateData = (newData) => { data = newData; render(); };
  render();
}
