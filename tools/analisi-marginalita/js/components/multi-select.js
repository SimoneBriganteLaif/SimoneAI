// ═══════════════════════════════════════════════════════
// Componente Multi-Select con ricerca
// ═══════════════════════════════════════════════════════

/**
 * Crea un multi-select con ricerca.
 * @param {HTMLElement} container - dove inserire il componente
 * @param {Object} config
 * @param {Array<{value:string, label:string}>} config.options
 * @param {string} config.placeholder - testo quando nessuna selezione (default: 'Tutti')
 * @param {function(string[])} config.onChange - callback con valori selezionati
 * @returns {Object} - { getSelected(), setSelected(values), reset() }
 */
function createMultiSelect(container, config) {
  const { options, placeholder = 'Tutti', onChange } = config;

  const wrapper = document.createElement('div');
  wrapper.className = 'ms-wrapper';

  const toggle = document.createElement('div');
  toggle.className = 'ms-toggle';
  toggle.textContent = placeholder;
  toggle.tabIndex = 0;

  const dropdown = document.createElement('div');
  dropdown.className = 'ms-dropdown';

  const search = document.createElement('input');
  search.className = 'ms-search';
  search.type = 'text';
  search.placeholder = 'Cerca...';
  dropdown.appendChild(search);

  const optionEls = [];

  options.forEach(opt => {
    const el = document.createElement('label');
    el.className = 'ms-option';
    el.innerHTML = `<input type="checkbox" value="${opt.value}"> <span>${opt.label}</span>`;
    el.dataset.search = opt.label.toLowerCase();
    dropdown.appendChild(el);
    optionEls.push(el);
  });

  wrapper.appendChild(toggle);
  wrapper.appendChild(dropdown);
  container.appendChild(wrapper);

  // Logica
  function getSelected() {
    return optionEls
      .map(el => el.querySelector('input'))
      .filter(cb => cb.checked)
      .map(cb => cb.value);
  }

  function updateLabel() {
    const sel = getSelected();
    if (sel.length === 0) {
      toggle.textContent = placeholder;
    } else if (sel.length <= 2) {
      const labels = sel.map(v => {
        const opt = options.find(o => o.value === v);
        return opt ? opt.label : v;
      });
      toggle.textContent = labels.join(', ');
    } else {
      toggle.textContent = `${sel.length} selezionati`;
    }
  }

  // Toggle dropdown
  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    closeAllDropdowns(dropdown);
    dropdown.classList.toggle('open');
    toggle.classList.toggle('open');
    if (dropdown.classList.contains('open')) {
      search.value = '';
      filterOptions('');
      search.focus();
    }
  });

  // Ricerca
  search.addEventListener('input', () => filterOptions(search.value));
  search.addEventListener('click', (e) => e.stopPropagation());

  function filterOptions(query) {
    const q = query.toLowerCase();
    optionEls.forEach(el => {
      el.classList.toggle('hidden', q && !el.dataset.search.includes(q));
    });
  }

  // Checkbox change
  dropdown.addEventListener('change', () => {
    updateLabel();
    if (onChange) onChange(getSelected());
  });

  // Keyboard
  wrapper.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      dropdown.classList.remove('open');
      toggle.classList.remove('open');
    }
  });

  return {
    getSelected,
    setSelected(values) {
      optionEls.forEach(el => {
        const cb = el.querySelector('input');
        cb.checked = values.includes(cb.value);
      });
      updateLabel();
    },
    reset() {
      optionEls.forEach(el => { el.querySelector('input').checked = false; });
      updateLabel();
      if (onChange) onChange([]);
    },
    element: wrapper
  };
}

/**
 * Crea un single-select con ricerca (per drill-down progetto).
 * @param {HTMLElement} container
 * @param {Object} config
 * @param {Array<{value:string, label:string}>} config.options
 * @param {string} config.placeholder
 * @param {function(string)} config.onChange - callback con valore selezionato
 * @returns {Object} - { getSelected(), setSelected(value), reset() }
 */
function createSearchSelect(container, config) {
  const { options, placeholder = '\u2014 Seleziona \u2014', onChange } = config;

  const wrapper = document.createElement('div');
  wrapper.className = 'ms-wrapper';
  wrapper.style.minWidth = '300px';

  const toggle = document.createElement('div');
  toggle.className = 'ms-toggle';
  toggle.textContent = placeholder;
  toggle.tabIndex = 0;

  const dropdown = document.createElement('div');
  dropdown.className = 'ms-dropdown';

  const search = document.createElement('input');
  search.className = 'ms-search';
  search.type = 'text';
  search.placeholder = 'Cerca progetto...';
  dropdown.appendChild(search);

  const optionEls = [];
  let selectedValue = '';

  options.forEach(opt => {
    const el = document.createElement('div');
    el.className = 'ms-option';
    el.innerHTML = `<span>${opt.label}</span>`;
    el.dataset.value = opt.value;
    el.dataset.search = opt.label.toLowerCase();
    dropdown.appendChild(el);
    optionEls.push(el);

    el.addEventListener('click', (e) => {
      e.stopPropagation();
      selectedValue = opt.value;
      toggle.textContent = opt.label;
      optionEls.forEach(o => o.classList.remove('selected'));
      el.classList.add('selected');
      dropdown.classList.remove('open');
      toggle.classList.remove('open');
      if (onChange) onChange(opt.value);
    });
  });

  wrapper.appendChild(toggle);
  wrapper.appendChild(dropdown);
  container.appendChild(wrapper);

  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    closeAllDropdowns(dropdown);
    dropdown.classList.toggle('open');
    toggle.classList.toggle('open');
    if (dropdown.classList.contains('open')) {
      search.value = '';
      filterOpts('');
      search.focus();
    }
  });

  search.addEventListener('input', () => filterOpts(search.value));
  search.addEventListener('click', (e) => e.stopPropagation());

  function filterOpts(query) {
    const q = query.toLowerCase();
    optionEls.forEach(el => {
      el.classList.toggle('hidden', q && !el.dataset.search.includes(q));
    });
  }

  wrapper.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      dropdown.classList.remove('open');
      toggle.classList.remove('open');
    }
  });

  return {
    getSelected() { return selectedValue; },
    setSelected(value) {
      selectedValue = value;
      const opt = options.find(o => o.value === value);
      toggle.textContent = opt ? opt.label : placeholder;
      optionEls.forEach(o => o.classList.toggle('selected', o.dataset.value === value));
      if (onChange) onChange(value);
    },
    reset() {
      selectedValue = '';
      toggle.textContent = placeholder;
      optionEls.forEach(o => o.classList.remove('selected'));
    },
    element: wrapper
  };
}

// Chiudi tutti i dropdown tranne quello specificato
function closeAllDropdowns(except) {
  document.querySelectorAll('.ms-dropdown.open').forEach(d => {
    if (d !== except) {
      d.classList.remove('open');
      d.previousElementSibling?.classList.remove('open');
    }
  });
}

// Chiudi dropdown al click fuori
document.addEventListener('click', () => closeAllDropdowns(null));
