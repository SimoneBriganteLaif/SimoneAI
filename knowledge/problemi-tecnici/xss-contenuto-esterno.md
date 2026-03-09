---
problema: "XSS da contenuto HTML esterno"
categoria: "sicurezza"
frequenza: "alta"
progetti-dove-si-e-presentato: [jubatus]
data-creazione: "2026-03-09"
tags:
  - "#problema:xss"
  - "#problema:sicurezza"
  - "#stack:react"
  - "#stack:nextjs"
---

# Problema Ricorrente: XSS da contenuto HTML esterno

## Descrizione del problema

Quando un'applicazione deve renderizzare HTML proveniente da fonti esterne (email, CMS, API di terze parti), c'è rischio di XSS (Cross-Site Scripting). L'HTML può contenere script malevoli, event handler, o iframe che vengono eseguiti nel browser dell'utente.

**Segnali che stai affrontando questo problema**:
- Devi mostrare body di email in HTML
- Integri contenuti da CMS o API esterne che ritornano HTML
- Usi `dangerouslySetInnerHTML` in React

**Contesto tipico in cui si presenta**:
- Piattaforme di customer care / ticketing (email HTML)
- CMS headless con contenuto ricco
- Applicazioni che aggregano contenuti da fonti multiple

---

## Soluzioni adottate

### Soluzione A: DOMPurify lato client *(raccomandata)*

**Quando usarla**: rendering HTML in React/Next.js

**Come funziona**: DOMPurify sanitizza l'HTML rimuovendo tag e attributi pericolosi (script, onclick, iframe) prima del rendering. Si usa come wrapper attorno a `dangerouslySetInnerHTML`.

**Riferimento al pattern**: [html-sanitization-dompurify](../../patterns/html-sanitization-dompurify.md)

**Risultati ottenuti in LAIF**: zero incidenti XSS su Jubatus con email HTML di varia provenienza

---

## Soluzioni che NON hanno funzionato

- **Stripping di tag con regex**: fragile, non cattura tutti i vettori di attacco (event handler, encoding)
- **Rendering in iframe sandbox**: funziona per isolamento ma complica styling, responsività e interazioni
- **Escape completo dell'HTML**: sicuro ma distrugge la formattazione (le email diventano illeggibili)

---

## Prevenzione

- Mai usare `dangerouslySetInnerHTML` senza sanitizzazione
- Trattare TUTTO l'HTML esterno come non fidato, anche da partner o API "trusted"
- Configurare Content-Security-Policy headers come difesa aggiuntiva

---

## Esperienze nei progetti LAIF

| Progetto | Contesto | Soluzione usata | Risultato |
|---------|---------|----------------|----------|
| Jubatus | Body email HTML in UI ticketing | DOMPurify + wrapper React | Zero XSS, formattazione preservata |
