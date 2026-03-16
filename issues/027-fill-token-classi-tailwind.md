# Classi fill-token e ring-token mancanti in Tailwind

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 27                 |
| Stack     | laif-template      |
| Tipo      | Bug                |
| Status    | Da rilasciare      |
| Priorita  | —                  |
| Effort    | 1h                 |

## Descrizione originale

> Al momento sembrano essere assenti [le classi fill-<token>] assieme a ring-<token> e forse qualche altra utility.

## Piano di risoluzione

1. **Verificare che la fix sia effettivamente presente**
   - Controllare la configurazione Tailwind (`tailwind.config.js` / `tailwind.config.ts`) nel branch corrente
   - Verificare che le utility `fill-<token>` siano generate correttamente (es. `fill-primary`, `fill-secondary`, ecc.)
   - Verificare che le utility `ring-<token>` siano generate correttamente

2. **Testare la generazione delle classi**
   - Buildare il CSS e verificare che le classi siano presenti nell'output
   - Testare in un componente che usa `fill-*` (es. icone SVG) e `ring-*` (es. focus states)

3. **Includere nel prossimo rilascio**
   - La fix e' gia pronta, serve solo includerla nella prossima release del template
   - Verificare che non ci siano altre utility mancanti menzionate nella issue originale

## Stima effort

- Verifica e test: ~0.5h
- Inclusione nel rilascio: ~0.5h
- **Totale: ~1h**
