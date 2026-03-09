---
nome: "Init Project"
descrizione: >
  Bootstrap completo di un nuovo progetto nella KB. Raccoglie info base,
  legge Notion via MCP, clona repo GitHub, analizza stack, popola i file
  di partenza e genera CLAUDE.md nella repo. Aggiorna projects/INDEX.md.
fase: presales
versione: "1.0"
stato: beta
legge:
  - Pagine Notion (via MCP)
  - Repository GitHub (clone + analisi)
scrive:
  - projects/[nome]/ (intera struttura da _template/)
  - projects/INDEX.md
aggiornato: "2026-03-08"
---

# Skill: Init Project

## Obiettivo

Crea la struttura completa di un progetto nella KB in un'unica operazione:
legge Notion, clona la repo, analizza il codice, popola i documenti di base.

---

## Loop conversazionale — Raccolta informazioni

Fai queste domande **in ordine**, **una alla volta**. Aspetta risposta prima di passare alla successiva.

### Domanda 1 — Nome progetto

```
Come si chiama questo progetto nella KB?
(suggerimento: usa kebab-case, es. "acme-ecommerce" o "mario-srl-gestionale")

Se esiste già una cartella con questo nome, aggiornerò solo i file mancanti.
```

### Domanda 2 — Repository GitHub

```
Qual è l'URL della repository GitHub principale?
(es. https://github.com/laif-dev/nome-repo)

Hai repository aggiuntive da collegare (es. infra, backend separato, mobile)?
Se sì, elencale pure tutte.
```

### Domanda 3 — Pagine Notion

```
Incolla i link alle pagine Notion con le note di meeting per questo progetto.
Puoi incollare più link, uno per riga.

(Le pagine verranno lette via MCP e salvate in meeting/ nella KB)
```

### Domanda 4 — Info cliente (solo se non emergono da Notion)

Se dopo aver letto Notion mancano queste informazioni, chiedile esplicitamente:
```
Alcune info necessarie per il README del progetto:
- Nome del cliente / azienda
- Settore / industria (es. retail, finance, saas, healthcare)
- Referente principale lato cliente (nome + ruolo)
```

---

## Processo di esecuzione

### Step 1 — Verifica progetto esistente

Controlla se `projects/[nome]/` esiste già:
- **Non esiste** → crea la struttura copiando `projects/_template/` (tutti i file)
- **Esiste già** → modalità merge: crea solo i file/cartelle mancanti, non toccare l'esistente

### Step 2 — Leggi le pagine Notion via MCP

Per ogni URL Notion fornito:
1. Leggi il contenuto della pagina tramite MCP
2. Estrai: titolo, data, partecipanti, contenuto completo
3. Salva in `projects/[nome]/meeting/[YYYY-MM-DD]-[titolo-slugificato].md`

Formato nota meeting:
```markdown
---
fonte: notion
url: [url originale]
data: YYYY-MM-DD
partecipanti: [lista se disponibile]
tipo: [kickoff | follow-up | review | commerciale]
---

# [Titolo pagina Notion]

[Contenuto completo della pagina]
```

### Step 3 — Analizza la repository

La repository vive in `/Users/simonebrigante/LAIF/repo/[nome]/` (non dentro la KB).

Leggi e analizza:
1. `/Users/simonebrigante/LAIF/repo/[nome]/README.md` — overview del progetto
2. `/Users/simonebrigante/LAIF/repo/[nome]/package.json` (o Gemfile, pyproject.toml, go.mod, ecc.) — stack e dipendenze
3. Struttura cartelle di primo e secondo livello (max 2 livelli di profondità)

Da questa analisi estrai:
- **Linguaggio/framework principale**
- **Dipendenze chiave** (solo quelle rilevanti, non l'elenco completo)
- **Struttura del progetto** (frontend, backend, shared, ecc.)
- **Comandi principali** (npm run dev, npm test, npm run build, ecc.)

### Step 4 — Popola README.md del progetto

Compila `projects/[nome]/README.md` con:
- Info cliente (da Notion o dalle risposte alle domande)
- Stack rilevato dalla repo
- Link alla repo GitHub
- Path locale della repo (`/Users/simonebrigante/LAIF/repo/[nome]/`)

### Step 5 — Genera bozza requisiti (condizionale)

Se le pagine Notion contengono note di meeting con requisiti identificabili:
- Crea una bozza di `projects/[nome]/requisiti.md`
- Segna ogni requisito come "Da validare" nel campo priorità
- Aggiungi una nota in testa: "Bozza generata automaticamente da init-project. Validare con la skill estrazione-requisiti."

Se il materiale Notion è troppo generico o insufficiente:
- Non creare requisiti.md (meglio vuoto che sbagliato)
- Segnalalo nell'output

### Step 6 — Aggiorna projects/INDEX.md

Aggiungi o aggiorna la riga del progetto in `projects/INDEX.md`.

---

## Output in chat (obbligatorio al termine)

```
✓ COMPLETATO — Init Project: [nome]

Struttura creata:
  projects/[nome]/                    [nuovo / aggiornato]

Repository analizzata:
  /Users/simonebrigante/LAIF/repo/[nome]/

Notion elaborato:
  [N] pagine lette
  [N] note meeting salvate:
    → [YYYY-MM-DD]-[titolo].md
    → ...

Stack rilevato: [framework] + [db] + [hosting]

File generati:
  ✓ projects/[nome]/README.md
  ✓ projects/[nome]/meeting/...
  [✓ projects/[nome]/requisiti.md (bozza)]
  ✓ projects/INDEX.md (aggiornato)

Prossimi passi:
  1. → Esegui skills/presales/estrazione-requisiti/ per strutturare i requisiti
       [le note meeting sono già disponibili come input]
  2. → Quando i requisiti sono pronti, esegui:
       skills/presales/genera-allegato-tecnico/
       skills/presales/genera-mockup-brief/
```

---

## Checklist qualità

- [ ] `projects/[nome]/README.md` ha cliente, industria, stack e link repo
- [ ] Tutte le pagine Notion sono state salvate in `meeting/`
- [ ] La repo è stata analizzata (in `/Users/simonebrigante/LAIF/repo/[nome]/`)
- [ ] `projects/INDEX.md` aggiornato
- [ ] Nessun file esistente è stato sovrascritto (modalità merge rispettata)

---

## Gestione errori

**Repo non accessibile (non trovata in /Users/simonebrigante/LAIF/repo/)**:
```
Non trovo la repo [nome] in /Users/simonebrigante/LAIF/repo/.
Assicurati che sia clonata localmente. Vuoi procedere senza analizzare la repo?
```

**Pagina Notion non leggibile**:
```
Non riesco a leggere [url]. Verifica che:
- Il link sia corretto e la pagina sia condivisa con l'integrazione Notion
Vuoi incollare il contenuto manualmente?
```

**Progetto già esistente con conflitti**:
```
La cartella projects/[nome]/ esiste già con questi file:
- [lista file esistenti]
Creerò solo i file mancanti. I file esistenti non verranno toccati.
Confermo?
```

---
← [Catalogo skill](../../../docs/skills.md) · [Workflow](../../../docs/workflow.md) · [System.md](../../../System.md)
