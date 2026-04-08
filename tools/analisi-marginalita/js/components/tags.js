// ═══════════════════════════════════════════════════════
// Tag System (sostituisce annotations.js)
// ═══════════════════════════════════════════════════════

const DEFAULT_TAG_DEFINITIONS = [
  // Negativi (rossi)
  { id: 'scope_creep', label: 'Scope Creep', color: 'red', builtin: true },
  { id: 'stima_errata', label: 'Stima Errata', color: 'red', builtin: true },
  { id: 'cliente_difficile', label: 'Cliente Difficile', color: 'red', builtin: true },
  { id: 'tech_debt', label: 'Tech Debt', color: 'red', builtin: true },
  { id: 'team_inadeguato', label: 'Team Inadeguato', color: 'red', builtin: true },
  { id: 'requisiti_cambiati', label: 'Requisiti Cambiati', color: 'red', builtin: true },
  { id: 'comunicazione_scarsa', label: 'Comunicazione Scarsa', color: 'red', builtin: true },
  // Positivi (verdi)
  { id: 'successo_tecnico', label: 'Successo Tecnico', color: 'green', builtin: true },
  { id: 'cliente_soddisfatto', label: 'Cliente Soddisfatto', color: 'green', builtin: true },
  { id: 'processo_efficiente', label: 'Processo Efficiente', color: 'green', builtin: true },
  // Tipologia (grigi)
  { id: 'tipo_gestionale', label: 'Gestionale', color: 'neutral', builtin: true },
  { id: 'tipo_chatbot', label: 'Chatbot', color: 'neutral', builtin: true },
  { id: 'tipo_genai', label: 'GenAI', color: 'neutral', builtin: true },
  { id: 'tipo_ottimizzatore', label: 'Ottimizzatore', color: 'neutral', builtin: true },
];

const LS_KEY = 'laif-margin-tags';
const OLD_LS_KEY = 'laif-margin-annotations';

let tagStore = { tagDefinitions: [...DEFAULT_TAG_DEFINITIONS], projectTags: {} };
let tagIndex = null; // { tagId: Set<saleId> }

function slugify(str) {
  return str.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
}

function loadTagStore() {
  // Try loading new format
  try {
    const stored = localStorage.getItem(LS_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      tagStore.tagDefinitions = parsed.tagDefinitions || [...DEFAULT_TAG_DEFINITIONS];
      tagStore.projectTags = parsed.projectTags || {};
    }
  } catch(e) { /* use defaults */ }

  // Migrate old annotations format
  try {
    const old = localStorage.getItem(OLD_LS_KEY);
    if (old) {
      const oldData = JSON.parse(old);
      const oldCatMap = {
        'scope_creep': 'scope_creep', 'stima_errata': 'stima_errata',
        'cliente_difficile': 'cliente_difficile', 'tech_debt': 'tech_debt',
        'team_inadeguato': 'team_inadeguato', 'requisiti_cambiati': 'requisiti_cambiati',
        'comunicazione': 'comunicazione_scarsa',
        'successo_tecnico': 'successo_tecnico', 'cliente_soddisfatto': 'cliente_soddisfatto',
        'processo_efficiente': 'processo_efficiente'
      };
      for (const [saleId, ann] of Object.entries(oldData)) {
        if (tagStore.projectTags[saleId]) continue;
        const tags = [];
        (ann.categories || []).forEach(c => {
          const mapped = oldCatMap[c] || c;
          if (getTagDef(mapped)) tags.push(mapped);
        });
        (ann.custom_categories || []).forEach(c => {
          const id = 'custom_' + slugify(c);
          if (!getTagDef(id)) {
            tagStore.tagDefinitions.push({ id, label: c, color: 'red', builtin: false });
          }
          tags.push(id);
        });
        tagStore.projectTags[saleId] = {
          tags: [...new Set(tags)],
          positive_notes: '',
          negative_notes: ann.notes || ''
        };
      }
      localStorage.removeItem(OLD_LS_KEY);
      saveTagStore();
    }
  } catch(e) { /* ignore migration errors */ }

  // Merge with data/annotations.json if loaded
  if (DATA.annotations) {
    for (const [saleId, ann] of Object.entries(DATA.annotations)) {
      if (!tagStore.projectTags[saleId]) {
        const tags = [...(ann.categories || []), ...(ann.custom_categories || [])];
        tagStore.projectTags[saleId] = {
          tags,
          positive_notes: '',
          negative_notes: ann.notes || ''
        };
      }
    }
  }

  // Ensure all default tags exist
  DEFAULT_TAG_DEFINITIONS.forEach(def => {
    if (!tagStore.tagDefinitions.find(t => t.id === def.id)) {
      tagStore.tagDefinitions.push(def);
    }
  });

  tagIndex = null;
}

function saveTagStore() {
  localStorage.setItem(LS_KEY, JSON.stringify(tagStore));
  tagIndex = null;
}

function getTagDefinitions(color) {
  if (color) return tagStore.tagDefinitions.filter(t => t.color === color);
  return tagStore.tagDefinitions;
}

function getTagDef(id) {
  return tagStore.tagDefinitions.find(t => t.id === id);
}

function addTagDefinition(label, color) {
  const id = 'custom_' + slugify(label);
  if (getTagDef(id)) return null;
  const def = { id, label, color, builtin: false };
  tagStore.tagDefinitions.push(def);
  saveTagStore();
  return def;
}

function removeTagDefinition(id) {
  const def = getTagDef(id);
  if (!def) return false;
  tagStore.tagDefinitions = tagStore.tagDefinitions.filter(t => t.id !== id);
  // Remove from all projects
  for (const pt of Object.values(tagStore.projectTags)) {
    pt.tags = pt.tags.filter(t => t !== id);
  }
  saveTagStore();
  return true;
}

function getProjectTags(saleId) {
  return tagStore.projectTags[String(saleId)] || { tags: [], positive_notes: '', negative_notes: '' };
}

function setProjectTags(saleId, data) {
  tagStore.projectTags[String(saleId)] = data;
  saveTagStore();
}

function buildTagIndex() {
  if (tagIndex) return tagIndex;
  tagIndex = {};
  for (const [saleId, pt] of Object.entries(tagStore.projectTags)) {
    (pt.tags || []).forEach(tagId => {
      if (!tagIndex[tagId]) tagIndex[tagId] = new Set();
      tagIndex[tagId].add(saleId);
    });
  }
  return tagIndex;
}

function renderTagBadges(saleId) {
  const pt = getProjectTags(saleId);
  if (!pt.tags.length) return '';
  return pt.tags.map(tagId => {
    const def = getTagDef(tagId);
    if (!def) return '';
    const c = TAG_COLORS[def.color] || TAG_COLORS.neutral;
    return `<span class="tag-pill" style="background:${c.bg};color:${c.text}">${def.label}</span>`;
  }).join(' ');
}

function exportTagStore() {
  const blob = new Blob([JSON.stringify(tagStore, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'marginalita-tags.json';
  a.click();
}

function importTagStore(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const imported = JSON.parse(e.target.result);
      // Merge tag definitions
      if (imported.tagDefinitions) {
        imported.tagDefinitions.forEach(def => {
          if (!getTagDef(def.id)) tagStore.tagDefinitions.push(def);
        });
      }
      // Merge project tags
      if (imported.projectTags) {
        for (const [saleId, pt] of Object.entries(imported.projectTags)) {
          if (!tagStore.projectTags[saleId]) {
            tagStore.projectTags[saleId] = pt;
          } else {
            const existing = tagStore.projectTags[saleId];
            existing.tags = [...new Set([...existing.tags, ...pt.tags])];
            if (pt.positive_notes && !existing.positive_notes) existing.positive_notes = pt.positive_notes;
            if (pt.negative_notes && !existing.negative_notes) existing.negative_notes = pt.negative_notes;
          }
        }
      }
      saveTagStore();
      alert('Dati importati con successo');
    } catch(err) {
      alert('Errore nel file JSON: ' + err.message);
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}
