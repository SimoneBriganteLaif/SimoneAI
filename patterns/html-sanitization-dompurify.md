---
titolo: "HTML Sanitization con DOMPurify"
categoria: "sicurezza"
complessità: "bassa"
usato-in: [jubatus]
data-creazione: "2026-03-09"
ultimo-aggiornamento: "2026-03-09"
tags:
  - "#pattern:sicurezza"
  - "#stack:react"
---

# Pattern: HTML Sanitization con DOMPurify

## Problema

Devi renderizzare HTML proveniente da fonti esterne (email, CMS, user-generated content) in un'app React. Usare `dangerouslySetInnerHTML` senza sanitizzazione espone a XSS.

**Segnali che questo pattern è quello giusto**:
- Hai un campo `body_html` da mostrare in un componente React
- L'HTML arriva da email, API esterne, o input utente
- Vedi `dangerouslySetInnerHTML` nel codice senza protezione

---

## Soluzione

Usare DOMPurify per sanitizzare l'HTML prima del rendering, wrappato in un componente React riutilizzabile con memoizzazione.

### Implementazione

**Passo 1**: Installare DOMPurify

```bash
npm install dompurify
npm install -D @types/dompurify
```

**Passo 2**: Creare componente `SanitizedHtml`

```tsx
import { useMemo } from "react";
import DOMPurify from "dompurify";

interface SanitizedHtmlProps {
  html: string;
  className?: string;
}

export function SanitizedHtml({ html, className }: SanitizedHtmlProps) {
  const clean = useMemo(
    () => DOMPurify.sanitize(html, { USE_PROFILES: { html: true } }),
    [html],
  );

  return (
    <div
      className={className ?? "prose prose-sm max-w-none dark:prose-invert"}
      dangerouslySetInnerHTML={{ __html: clean }}
    />
  );
}
```

**Passo 3**: Usare con fallback su plain text

```tsx
{message.body_html ? (
  <SanitizedHtml html={message.body_html} />
) : message.body_text ? (
  <div className="whitespace-pre-wrap">{message.body_text}</div>
) : (
  <div className="whitespace-pre-wrap">{message.content}</div>
)}
```

### Note

- `useMemo` evita ri-sanitizzazione ad ogni render — importante per email lunghe (30K+ chars)
- `USE_PROFILES: { html: true }` permette tag sicuri (p, div, img, a, table, etc.) e rimuove script, event handlers, iframe
- La classe `prose` di Tailwind Typography formatta bene l'HTML email (headings, link, tabelle)

---

## Trade-off

**Vantaggi**:
- Protezione XSS completa (rimuove script, event handlers, iframe)
- Performance: memoizzazione evita ri-parsing su ogni render
- Compatibilità: funziona con HTML email complesso (tabelle nidificate, CSS inline)

**Svantaggi / costi**:
- Bundle size: DOMPurify aggiunge ~15KB gzipped
- Non è SSR-safe di default (accede a `window`). Per SSR, serve `isomorphic-dompurify`

**Quando NON usare questo pattern**:
- L'HTML è generato internamente e completamente controllato (es. output di un markdown parser)
- Stai mostrando solo testo plain — non serve sanitizzazione
- Il contenuto è già sanitizzato server-side — evita doppia sanitizzazione

---

## Esempi reali in LAIF

| Progetto | Come è stato usato | Note / deviazioni |
|---------|-------------------|------------------|
| Jubatus | Email body HTML nel `ConversationThread` — newsletter con immagini, tabelle, CSS inline | Funziona correttamente con email reali (Serenis, Il Post, Carne Secca Italia) |

---

## Risorse esterne

- [DOMPurify GitHub](https://github.com/cure53/DOMPurify)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html)
