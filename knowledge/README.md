# Knowledge Cross-Progetto

Conoscenza accumulata che non appartiene a un singolo progetto ma è riutilizzabile trasversalmente.

---

## Struttura

```
knowledge/
├── README.md                    ← questo file
├── industrie/                   ← cosa sappiamo dei vari settori
│   └── _template.md
├── problemi-tecnici/            ← soluzioni a problemi ricorrenti
│   └── _template.md
└── report-manutenzione-*.md    ← report mensili del sub-agente
```

---

## Industrie documentate

| Industria | File | Aggiornato |
|-----------|------|-----------|
| *(nessuna ancora)* | | |

---

## Problemi tecnici documentati

| Problema | File | Aggiornato |
|---------|------|-----------|
| *(nessuno ancora)* | | |

---

## Come aggiungere knowledge

### Per un'industria nuova
1. Copia `industrie/_template.md`
2. Rinomina con il nome del settore (es. `retail.md`, `finance.md`)
3. Compila le sezioni
4. Aggiorna l'indice sopra

### Per un problema tecnico
1. Copia `problemi-tecnici/_template.md`
2. Rinomina con il tipo di problema (es. `performance-query.md`)
3. Compila le sezioni
4. Aggiorna l'indice sopra

### Differenza con `patterns/`
- **`patterns/`**: soluzione tecnica implementativa (codice, architettura)
- **`knowledge/`**: contesto, business logic, comportamenti attesi di un settore o tipo di problema

Spesso si usano insieme: il pattern tecnico + la knowledge di business che spiega perché quella soluzione è la giusta per quel settore.
