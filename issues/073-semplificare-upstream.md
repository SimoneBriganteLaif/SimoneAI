# Semplificare Processo Upstream

| Campo | Valore |
|---|---|
| **ID** | 73 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | Backlog |
| **Tag** | Filone Upstream |

## Descrizione originale

Semplificare processo aggiornamento delle app (upstream).

## Piano di risoluzione

1. **Documentare i pain point attuali del processo upstream** — raccogliere feedback dal team su cosa non funziona:
   - Conflitti frequenti e difficili da risolvere.
   - Aggiornamenti all-or-nothing (non selettivi).
   - Dipendenza dal remote git del template.
   - Complessità per gli sviluppatori junior.
2. **Valutare le alternative**:
   - **Copier** (issue 94) — PoC dedicato, superset di Cookiecutter con `copier update`.
   - **Git subtree** — merge selettivo di sottocartelle del template.
   - **Cherry-pick manuale** — selezionare commit specifici dal template.
   - **Monorepo con packages** — template come package npm/pip da importare.
3. **Definire i criteri di valutazione**:
   - Facilità d'uso per lo sviluppatore.
   - Qualità della gestione conflitti.
   - Possibilità di aggiornamento selettivo (solo BE, solo FE, solo un modulo).
   - Possibilità di skippare aggiornamenti non voluti.
   - Compatibilità con i progetti esistenti (migrazione).
4. **PoC con l'approccio scelto** — implementare un proof of concept su un progetto reale (o clone di un progetto reale) per validare l'approccio in un caso concreto.
5. **Definire il percorso di migrazione per i progetti esistenti** — non basta che funzioni per i nuovi progetti: deve essere adottabile anche sui 5+ progetti già in produzione.

### Issue correlate

- Issue 94 — Copier come alternativa upstream
- Issue 74 — Modularizzazione template
- Issue 146 — Fork template da master
- Issue 136 — Documentazione upstream

## Stima effort

**Analisi e decisione: 8h.** Implementazione completa: dipende dall'approccio scelto (16-40h). Questa issue è principalmente di analisi — l'implementazione avviene nelle issue collegate.
