---
titolo: "Linkare laif-ds locale nei progetti"
categoria: "sviluppo"
data-creazione: "2026-03-10"
tags:
  - "#knowledge:azienda"
  - "#stack:laif-ds"
  - "#stack:npm"
---

# Linkare laif-ds locale nei progetti

## Quando serve

Quando hai modifiche a laif-ds (repo `ds/`) non ancora pubblicate su npm e vuoi testarle in un progetto consumer (es. umbra-recommend, jubatus). Tipico durante lo sviluppo di nuovi componenti o fix al design system.

## Prerequisiti

- Repository `ds/` clonata in `/Users/simonebrigante/LAIF/repo/ds/`
- Node.js e npm installati
- Il progetto consumer ha `laif-ds` tra le dipendenze npm

## Procedura

### 1. Build locale di laif-ds

```bash
cd /Users/simonebrigante/LAIF/repo/ds/
npm install          # solo la prima volta o dopo cambio dipendenze
npm run build        # produce dist/index.js, dist/index.d.ts, dist/styles.css
```

**Nota**: il build CSS v3 (`postcss.config.v3.js`) potrebbe fallire con `ERR_REQUIRE_ESM` se `tailwindcss@3.x` e in uso. Il build principale (tsc + vite + CSS v4) procede comunque. Il file `dist/styles.v3.css` non verra generato, ma `dist/styles.css` (v4) si.

### 2. Registrare laif-ds come link globale

```bash
cd /Users/simonebrigante/LAIF/repo/ds/
npm link
```

Questo registra il pacchetto `laif-ds` nella directory globale npm. Il nome del pacchetto viene dal `name` in `package.json` (attualmente `laif-ds`).

### 3. Linkare nel progetto consumer

```bash
cd /Users/simonebrigante/LAIF/repo/[progetto]/frontend/
npm link laif-ds
```

Verifica con:
```bash
ls -la node_modules/laif-ds
# Deve mostrare: node_modules/laif-ds -> ../../../ds
```

### 4. Sviluppare e testare

Dopo il link, il progetto consumer usa la versione locale di laif-ds. Se modifichi file in `ds/`:

1. Riesegui `npm run build` nella repo `ds/`
2. Il progetto consumer vedra le modifiche (potrebbe servire restart del dev server)

### 5. Ripristinare la versione npm

Quando hai finito e vuoi tornare alla versione pubblicata:

```bash
cd /Users/simonebrigante/LAIF/repo/[progetto]/frontend/
npm unlink laif-ds
npm install laif-ds    # reinstalla da npm
```

Oppure piu radicale:
```bash
rm -rf node_modules/laif-ds
npm install
```

## Attenzione

- **Non committare** `package-lock.json` con il link attivo — conterrebbe path locali
- **HMR/hot reload** potrebbe non funzionare perfettamente con i symlink. In caso di problemi, riavviare il dev server
- Se il progetto usa `just fe install`, il link viene sovrascritto. Rilinkare dopo ogni `npm install`
- **Turbopack non supporta symlink esterni**: se il symlink punta fuori dalla root del progetto, Turbopack fallisce con `leaves the filesystem root`. Avviare Next.js **senza** `--turbopack` (es. `npx next dev -p 8081` invece di `npm run dev`)
- **Dipendenze peer mancanti**: con il symlink, le dipendenze di laif-ds (es. `react-pdf`) non sono piu nested in `node_modules/laif-ds/node_modules/`. Se il progetto le importa (es. CSS), installarle direttamente: `npm install react-pdf`
- **Copiare asset mancanti**: il build potrebbe non eseguire tutti gli step di copia. Verificare che `dist/css-for-template.css` esista, altrimenti: `cp src/styles/css-for-template.css dist/`

## Progetti dove e stato usato

| Progetto | Data | Motivo |
|---------|------|--------|
| umbra-recommend | 2026-03-10 | Test dimensione WEEK del Gantt (non ancora pubblicata su npm) |
