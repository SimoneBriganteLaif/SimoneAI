# Dismettere Next.js → TanStack Router + Vite

| Campo | Valore |
|---|---|
| **ID** | 91 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | In corso |
| **Tag** | Breaking |

## Descrizione originale

Il modo in cui usiamo Next.js è troppo overkill, perché lo utilizziamo solo per generare un codice statico da mettere in un bucket. L'unica feature che effettivamente sfruttiamo è l'alberatura dei file che genera i path e il compiler, che è esattamente ciò che fa TanStack Router + Vite (però maggiormente ottimizzato per questo).

## Piano di risoluzione

1. **Già in corso.** Verificare lo stato attuale della migrazione e i branch aperti.
2. **Sostituire Next.js con Vite + TanStack Router** — rimuovere `next`, `next/image`, `next/font` e tutte le dipendenze Next.js dal `package.json`. Aggiungere `vite`, `@tanstack/react-router`, `@tanstack/router-devtools`, `@tanstack/router-vite-plugin`.
3. **Migrare il file-based routing alle convenzioni TanStack Router** — TanStack Router usa una propria convenzione per il file-based routing (cartella `routes/`, file `__root.tsx`, suffisso `.lazy.tsx`). Mappare ogni pagina Next.js (`app/[...]/page.tsx`) alla corrispondente route TanStack.
4. **Sostituire `next/dynamic` con `React.lazy`** — ogni import dinamico Next.js diventa un `React.lazy()` + `Suspense`. Uniformare il pattern di lazy loading su tutte le pagine.
5. **Aggiornare la build pipeline** — configurare `vite.config.ts` per generare output statico (`vite build`). Verificare che l'output sia compatibile con il deploy su S3 bucket (stessa struttura di cartelle, `index.html` con fallback per SPA routing).
6. **Migrare le feature specifiche di Next.js**:
   - `next/image` → componente custom con `<img>` o libreria di ottimizzazione immagini (se necessario).
   - `next/font` → font caricati via CSS standard (`@font-face`) o plugin Vite.
   - `next/head` / metadata → `react-helmet-async` o equivalente.
   - Middleware Next.js (se presente) → route guard TanStack Router.
7. **Aggiornare le pipeline di deploy di tutti i progetti** — modificare gli step di build nei workflow CI/CD (GitHub Actions) e negli script `just` per usare `vite build` al posto di `next build && next export`.
8. **Testing approfondito** — questa è la breaking change più grande del template. Verificare:
   - Routing corretto su tutte le pagine (inclusi path dinamici e nested routes).
   - Lazy loading funzionante.
   - Build statica corretta e deploy su bucket.
   - Nessuna regressione su ogni progetto derivato.
9. **Coordinamento con altre issue correlate**:
   - Issue 147 (font sizes rem) — verificare compatibilità con il nuovo sistema di font.
   - Issue 149 (lazy loading pagine) — il lazy loading sarà nativamente gestito da TanStack Router.
   - Issue 129 (colori Tailwind) — verificare che la configurazione Tailwind funzioni con Vite.

## Stima effort

**Alto** — migrazione strutturale che impatta ogni progetto derivato dal template. La migrazione in sé richiede circa 16-24h di lavoro, ma il testing e l'aggiornamento di tutti i progetti derivati possono richiedere ulteriori 8-16h. Pianificare una finestra di rilascio coordinata.
