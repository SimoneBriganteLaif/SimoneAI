---
nome: "Sistema Riunioni Notion"
descrizione: >
  Pulizia e arricchimento della tabella Notion "Riunioni Private" (LAIF - Private).
  Aggiorna icone, Tag, relation Progetto, Partecipanti Interni e titoli placeholder
  di pagine meeting. Inferisce i valori mancanti da titolo + riassunto, rispetta i
  valori già popolati, chiede conferma sui casi ambigui.
  Usa in autonomia il piano: scan → inferenza → conferma → batch update.
fase: maintenance
versione: "0.1"
stato: beta
frequenza-suggerita: "mensile o on-demand quando la tabella non è più aggiornata"
legge:
  - Notion DB "Riunioni Private": 2ee90ad6ee48805daafde5c0d4849337 (via MCP)
  - Notion DB "Progetti": collection://f3e5280e-5025-4470-848c-df5f240773e0 (via MCP)
  - Notion workspace users (via MCP get-users)
scrive:
  - Notion DB "Riunioni Private" (via MCP update-page): icon, Name, Tag, Progetto, Partecipanti Interni
aggiornato: "2026-04-22"
tags:
  - "#fase:manutenzione"
  - "#skill:sistema-riunioni-notion"
---

# Skill: Sistema Riunioni Notion

> **Stato beta**: all'inizio avvisa che è in beta. Ad ogni step chiedi se il processo ha senso o se va modificato.

## Obiettivo

Mantenere la tabella "Riunioni Private" consistente e navigabile: ogni riunione deve avere icona coerente al Tag, Tag valido, relation Progetto dove applicabile, Partecipanti Interni veri (Simone escluso), titolo descrittivo.

## Perimetro

**Fa**:
- Query + fetch delle pagine del DB (con paginazione se necessario)
- Inferisce Tag / Progetto / Partecipanti / Titolo dal contesto (titolo + riassunto)
- Applica icone da mapping fisso
- Riscrive titoli placeholder (es. "‣", "Untitled", "@<date>...") con titolo breve descrittivo
- Chiede conferma all'utente per casi ambigui con `AskUserQuestion`

**Non fa**:
- Non crea mai nuove pagine/riunioni
- Non modifica il **Riassunto** (è generato altrove)
- Non tocca i campi readonly (`Orario`, `Week`, `Created time`)
- Non popola Progetto se l'ID del progetto non è noto (meglio vuoto che sbagliato)
- Non aggiunge mai **Simone Brigante** ai Partecipanti Interni

## Quando usarla / Trigger

- L'utente dice "sistema le riunioni", "fixa la tabella delle call", "aggiorna le call su Notion"
- La tabella mostra molte pagine con titolo "‣", icone mancanti, Tag vuoti
- Vuoi una passata di manutenzione dopo un periodo intenso di meeting

## Prerequisiti

- Notion MCP abilitato (tool `mcp__notion__notion-*` o equivalente `mcp__38fee*__notion-*`)
- Accesso in scrittura alla pagina "LAIF - Private"
- Tool disponibili: `AskUserQuestion`, `TodoWrite`

---

## Configurazione (costanti)

### ID Notion fissi

| Entità | ID |
|---|---|
| DB Riunioni Private (page) | `2ee90ad6ee48805daafde5c0d4849337` |
| DB Riunioni Private (collection) | `2ee90ad6-ee48-80e0-bcbc-000b5dbc5d71` |
| Default view "Tabella" | `2ee90ad6-ee48-806e-b915-000cf08a2003` |
| DB Progetti (collection) | `f3e5280e-5025-4470-848c-df5f240773e0` |

### Schema rilevante del DB

| Property | Tipo | Note |
|---|---|---|
| `Name` | title | Titolo della riunione |
| `Tag` | select | Opzioni sotto |
| `Progetto` | relation (limit 1) | Verso DB Progetti |
| `Partecipanti Interni` | person (array) | **Simone escluso** |
| `Lead` | relation (limit 1) | Verso DB Persone, NON toccare |
| `Accesso` | person | NON toccare |
| `Riassunto` | text | Generato altrove, NON toccare |

### Valori Tag ammessi

```
Progetto - Interna · Progetto - Cliente · LAIF - 1:1 · LAIF - AI in LAIF
LAIF - Fatturazioni · LAIF - Pianificazione · LAIF - Team Delivery
LAIF - Team Stack Interno · LAIF - Staffing · LAIF - Status Stack Interno
Solitario · Notion · Personale · Altro
```

### Mapping emoji Tag → icona (stabile, approvato 2026-04-22)

| Tag | Emoji |
|---|---|
| Progetto - Cliente | 🤝 |
| Progetto - Interna | 🛠️ |
| LAIF - 1:1 | 👤 |
| LAIF - AI in LAIF | 🤖 |
| LAIF - Fatturazioni | 💰 |
| LAIF - Pianificazione | 🗓️ |
| LAIF - Team Delivery | 🚚 |
| LAIF - Team Stack Interno | 🧩 |
| LAIF - Staffing | 👥 |
| LAIF - Status Stack Interno | 📊 |
| Solitario | 🧘 |
| Notion | 📝 |
| Personale | 🌱 |
| Altro | 📌 |
| *(fallback: Tag non inferibile)* | 📌 |

### Progetti con ID noto (per relation `Progetto`)

Aggiorna questa tabella man mano che scopri nuovi ID (via `notion-search` nel DB Progetti).

| Progetto | Page ID Notion |
|---|---|
| Jubatus | `2f190ad6-ee48-80a7-af50-fcc88ad15873` |
| Lamonea | `30d90ad6-ee48-80ff-823b-f5f19f380679` |
| Nivi | `21490ad6-ee48-800d-bd92-c5200b4a8372` |
| Albini&Castelli (A&C) | `21c90ad6-ee48-814d-aa90-d04568118236` |
| SEBI (Sebi Group) | `2f590ad6-ee48-81bf-bc9a-fb1dc5fa6d60` |
| Creama | `1c090ad6-ee48-80d2-84f7-f6dd71827a2b` |

Progetti presenti nella KB ma con ID Notion **da scoprire** al bisogno: Bonfiglioli Consulting, Umbra, Wolico, LAIF Issue. Per altri clienti (CRIF, Phoenix, ValueTarget, Publicis, Elia, Nespaq, Kreef, Andriani, Sireco) l'ID non è noto: lascia `Progetto` vuoto e segnalalo.

### Utenti Notion (nome → user_id)

Snapshot al 2026-04-22. Per refresh chiama `notion-get-users`. Usare sempre questa mappa per il campo `Partecipanti Interni`.

```
Alessandro Grotti   198d872b-594c-8127-a50c-0002b0e2ca7a
Andrea Mordenti     c3529cc1-194f-4e22-ad85-cbb3ca3d2b15
Andrea Fruttidoro   348d872b-594c-8140-b792-00025c7d8ae5
Angelo Longano      c09c511e-60be-4315-b733-ba4837ef9763
Carlo Venditti      115d872b-594c-81e3-b9fd-0002d759d53e
Cristiano Piscioneri 1b9d872b-594c-8140-a740-00020f324d2c
Daniele DN (Dani)   a454c868-e7a9-4903-90e1-19e74f6a7dc2
Davide Leonescu     349d872b-594c-81e4-9a11-000254e8a89c
Davide Miani (Dave) 317d872b-594c-817f-985b-00020b78843b
Dmitry Babich       305d872b-594c-816c-9736-000281776e2d
Federico Frascà     1e3d872b-594c-81c4-87cf-00022565f5c1
Francesco Barbanti  21bd872b-594c-8100-aa65-00021a755dbb
Gabriele Fogu       11bd872b-594c-8118-9d52-00020ec6b08f
Leonardo Carboni    224d872b-594c-81a7-8883-0002ef4f8e3e
Letizia Maccariello 2e2d872b-594c-810c-b2cd-0002b45b05b5
Lorenzo Monni Sau   2ccd872b-594c-8125-9840-000249ceeffa
Lorenzo Tonetta     172d872b-594c-8109-9262-0002f3e83634
Luca Stendardo      173d872b-594c-8175-9db7-000248c61a9d
Luca Torresan       229d872b-594c-8145-b413-0002425e3d42
Marco Pinelli (Pinnuz) edc1cade-6412-46f9-b42d-53697c6d7ccf
Marco Vita          af96b8d6-aca7-4cc1-b264-595ddc356d3c
Matteo Betti        2e2d872b-594c-81ca-b700-0002dd67dbb8
Matteo Scalabrini   111d872b-594c-817c-b485-000265bdd836
Mattia Gualandi     1f4d872b-594c-81e4-965a-000235364360
Mattia Palmucci     349d872b-594c-8188-bd6f-0002f1c70089
Michele Roberti     279d872b-594c-81bd-a0f7-0002852534a2
Roberto Bonetti     181d872b-594c-81f6-b942-00021472554a
Roberto Zanolli     199d872b-594c-8189-9a2d-0002224caae6
Simone Antimiani    1aad872b-594c-81ad-a7a4-00026f8ae35c
Simone Brigante     e980af16-6ba9-416c-a722-0438176fed93   ← NON inserire mai
Tancredi Bosi       18fd872b-594c-813d-95ef-00020e3d17b4
```

---

## Regole fondamentali (NON derogabili)

1. **Simone Brigante non va mai in Partecipanti Interni**. Se Simone era l'unico partecipante inferito, il campo deve rimanere vuoto (`"[]"`).
2. **Mai sovrascrivere un valore già popolato**, a meno che non sia evidentemente errato e l'utente lo confermi via `AskUserQuestion`.
3. **Su ogni dubbio (Tag / Progetto / identità di un partecipante)**: usa `AskUserQuestion`. Quando chiedi, specifica sempre **data della riunione** e **argomenti principali** (2–3 bullet dal Riassunto).
4. **Progetto relation**: popola solo se l'ID del progetto è nella tabella "Progetti con ID noto". Altrimenti lascia vuoto.
5. **Titoli**: brevi (3–6 parole, ≤45 char), in italiano, nominali, senza data, coerenti con lo stile esistente (es. "SAL Lamonea", "1:1 Daniele", "Update w/ Tancre", "Jubatus - Setup Infra #1", "Analisi Marginalità").
6. **Nessuna iniziativa irreversibile senza conferma**: cambi massivi (>10 pagine) solo dopo approvazione del mapping emoji + regole di inferenza.

---

## Regole di inferenza Tag

Applicale in ordine. La prima che matcha vince.

1. Titolo contiene "Staffing" → `LAIF - Staffing`
2. Titolo contiene "Team Delivery" o "Team Blue" → `LAIF - Team Delivery`
3. Titolo contiene "Team Stack Interno" o "Stack Interno" (NO "Status") → `LAIF - Team Stack Interno`
4. Titolo contiene "Status Stack Interno" → `LAIF - Status Stack Interno`
5. Titolo contiene "1:1" → `LAIF - 1:1`
6. Titolo contiene "AI in LAIF" → `LAIF - AI in LAIF`
7. Titolo contiene "Fatturazion" → `LAIF - Fatturazioni`
8. Titolo è tipo "#NN" / "S #NN" → `Personale`
9. Titolo tipo "[Cliente] - SAL / Update / Setup / Infra / Revisione Mockup / Dashboard" con cliente esterno → `Progetto - Cliente`
10. Titolo tipo "[Cliente] - Update Interno / Allineamento Interno / Brief Interno / Task e Mockup / w/ [interno]" → `Progetto - Interna`
11. Titolo tipo "Update w/ [nome interno]", "Allineamento [nome]", "Pipeline X", "Contratto X", "LAIF-KB", "Analisi Marginalità", "Accessi X", "Claude Code - ..." → `LAIF - Pianificazione`
12. Titolo placeholder ("‣", vuoto, "@<date>..."): **leggi il Riassunto completo** → inferisci. Se riassunto è generico su pianificazione LAIF → `LAIF - Pianificazione`. Se riguarda un progetto specifico → `Progetto - Interna` o `Progetto - Cliente` a seconda del contesto.
13. Se Tag è già presente, NON toccarlo.

**Errori ricorrenti da evitare**:
- Una riunione con nome progetto ma contenuto di "pianificazione risorse interna" va `Progetto - Interna`, non `LAIF - Pianificazione`.
- "Feedback [persona]" spesso è un `LAIF - 1:1`, non `Progetto - Interna`.
- "Pianificazione Settimanale" / "Retro Team" è `LAIF - Team Delivery`, non `Progetto - Interna`.
- "Bug SSO", "Release X.Y", "CLI" → tipicamente `LAIF - Team Stack Interno` o `LAIF - Status Stack Interno`, non `LAIF - Pianificazione`.

Quando non sei sicuro al 100% → `AskUserQuestion`.

---

## Processo (loop conversazionale)

### Step 0 — Apri la sessione

Avvisa che la skill è in beta. Chiedi lo **scope**:
- tutte le pagine oppure solo ultimo mese / ultime N settimane
- solo arricchimento (icona/Tag/Progetto/Partecipanti) oppure anche riscrittura titoli placeholder

### Step 1 — Recupera dati

1. `notion-fetch` sul DB per schema attuale (verifica mapping Tag non sia cambiato).
2. `notion-query-database-view` sulla view "Tabella". **Attenzione**: l'output è ~90k caratteri → delegare la lettura a un subagent con istruzioni di sliceing `python3 -c "print(open('...').read()[A:B])"` a fette di 80k.
3. `notion-get-users` per aggiornare la mappa utenti.
4. Se servono pagine più vecchie di 100 righe: `notion-search` con `data_source_url` + filtri `created_date_range.end_date`, iterando con query keyword diverse ("update", "meeting", "riunione", ecc.).

### Step 2 — Diagnostico

Il subagent produce tabella per pagina (page_id, titolo, tag, progetto, icona, partecipanti_count, riassunto_preview) e sommario (senza tag, senza progetto, placeholder "‣", distribuzione Tag).

Mostra all'utente:
- totale pagine, quante con anomalie, distribuzione Tag.
- proposta di mapping emoji (se prima esecuzione).
- lista dei casi da chiedere (casi ambigui).

### Step 3 — Conferma mapping e regole

La prima volta (o se le regole sono cambiate): mostra il mapping emoji e le regole di inferenza. `AskUserQuestion` con opzione "ok / modifica".

### Step 4 — Costruisci piano update (JSON)

Delega a subagent la creazione di `/tmp/meeting_update_plan.json` con record `{page_id, title_preview, icon, set_tag, set_progetto_id, set_partecipanti_ids, reasoning}`. Regole:
- includi tutte le pagine (anche no-op per applicare solo l'icona)
- `set_partecipanti_ids`: **mai** Simone. Solo se campo era vuoto + identità chiara dal riassunto.
- `set_progetto_id`: solo da mappa ID noti.

### Step 5 — Chiedi sui casi ambigui

Per ogni pagina con Tag inferito dubbio (titolo generico, contenuto misto, placeholder "‣"):
```
AskUserQuestion({
  question: "\"<titolo>\" (<data>). Argomenti: <bullet 2-3 dal Riassunto>. Che Tag preferisci?",
  options: [consigliato, alternativa1, alternativa2]
})
```
Massimo 4 domande per turno (limite tool).

### Step 6 — Batch update

Applica gli update a blocchi di ~20 chiamate parallele `notion-update-page`:

```
{
  page_id: "<id>",
  command: "update_properties",
  icon: "🤝",
  properties: {
    "Name": "...",                                // opzionale
    "Tag": "Progetto - Cliente",                  // opzionale
    "Progetto": "[\"https://www.notion.so/<id>\"]", // relation: JSON string
    "Partecipanti Interni": "[\"<uid>\", ...]"    // persone: JSON array
  },
  content_updates: []
}
```

**Nota formato**:
- `Partecipanti Interni` accetta `"[]"` per svuotare, `"[\"<uid>\"]"` per 1 persona.
- `Progetto` relation singola: `"[\"https://www.notion.so/<id-senza-trattini>\"]"`.
- `properties: {}` con solo `icon` funziona per settare solo l'icona.

### Step 7 — Riscrittura titoli placeholder (opzionale)

Se scope include titoli:
1. Subagent legge Riassunto completo delle pagine con titolo "‣" / vuoto / "@date..."
2. Genera titoli brevi stile esistente → `/tmp/meeting_titles.json`
3. Applica via `notion-update-page` con `properties.Name`.

### Step 8 — Report finale

Tabella delle modifiche fatte, categorizzate: icone, Tag inferiti, Progetto popolato, Partecipanti, titoli riscritti. Segnala:
- pagine con progetti senza ID noto (da aggiungere in futuro)
- pagine lasciate con tag `Solitario` o `📌` (fallback)
- eventuali pagine non raggiunte dalla paginazione

---

## Errori noti / gotcha

- **MCP Notion disconnette a metà sessione**: esiste un secondo MCP con prefisso diverso. Carica gli schemi con `ToolSearch select:mcp__notion__notion-update-page,...` e riprendi.
- **Output `query-database-view` oltre 90k caratteri**: NON leggerlo inline → sempre subagent con slicing.
- **"Solitario" può essere intenzionale**: non cambiarlo senza conferma (è il tag per focus time).
- **Partecipanti già presenti prima della skill**: non sovrascrivere. Se devi aggiungere, usa l'unione, non la sostituzione.
- **Semantic search `notion-search`** non indicizza tutte le pagine: per recupero completo di pagine antiche, considera una view temporanea filtrata per data invece del semantic search.

---

## Mapping veloce "frase → azione"

| Utente dice | Cosa fare |
|---|---|
| "sistema le call" | scope = ultime 4 settimane, arricchimento + titoli |
| "fixa tutte le riunioni" | scope = tutto, arricchimento + titoli + conferma mapping |
| "solo le icone" | scope = tutto, solo icon |
| "controlla i tag" | scope = tutto, solo Tag + riferimento a tabella mapping |
| "aggiungi partecipanti" | Step 5–6 solo per campo Partecipanti, con AskUserQuestion aggressiva |

---

## Cambi attesi nel tempo

- Aggiungere nuovi progetti alla tabella "Progetti con ID noto" man mano che li si incontra.
- Aggiornare la mappa utenti quando entrano/escono persone (via `notion-get-users`).
- Evolvere le regole di inferenza Tag se emergono nuovi pattern di titoli (es. nuove serie ricorrenti di meeting).

## Changelog skill

- **0.1 (2026-04-22)**: creazione iniziale dopo prima passata massiva (~100 pagine). Mapping emoji approvato, Simone escluso dai Partecipanti.
