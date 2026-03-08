# Knowledge Cross-Progetto

Conoscenza accumulata che non appartiene a un singolo progetto ma è riutilizzabile trasversalmente.

---

## Struttura

```
knowledge/
├── README.md                    ← questo file
├── azienda/                     ← contesto aziendale LAIF
│   ├── overview.md              ← chi è LAIF, team, modello di lavoro
│   ├── stack.md                 ← tecnologie, pattern, convenzioni
│   ├── infrastruttura.md        ← architettura AWS, deploy
│   └── processi.md              ← flussi di lavoro, CI/CD, regole Windsurf
├── industrie/                   ← cosa sappiamo dei vari settori
│   └── _template.md
├── problemi-tecnici/            ← soluzioni a problemi ricorrenti
│   └── _template.md
└── report-manutenzione-*.md    ← report mensili del sub-agente
```

---

## Azienda

Contesto fondamentale su LAIF: struttura, stack, infrastruttura, processi.

| File | Contenuto | Aggiornato |
|------|-----------|-----------|
| `azienda/overview.md` | Chi è LAIF, team di Simone, modello di lavoro | 2026-03-08 |
| `azienda/stack.md` | Stack tecnico, pattern architetturali, convenzioni naming | 2026-03-08 |
| `azienda/infrastruttura.md` | AWS: TemplateStack, risorse, configurazione, deploy | 2026-03-08 |
| `azienda/processi.md` | Flusso sviluppo, upstream, Windsurf rules, CI/CD | 2026-03-08 |

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
