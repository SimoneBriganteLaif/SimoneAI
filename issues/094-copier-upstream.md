# Copier come alternativa all'Upstream

| Campo | Valore |
|---|---|
| **ID** | 94 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | Backlog |
| **Tag** | Filone Upstream |

## Descrizione originale

Esiste una libreria Python, Copier, che è un superset di Cookiecutter, nata per fare più agilmente ciò che noi facciamo con gli upstream, permettendo di svincolarci dalla dipendenza git dall'origin del template.

## Piano di risoluzione

1. **PoC con Copier su un progetto di test** — creare un progetto di prova partendo dal template tramite Copier:
   - Installare Copier (`pip install copier`).
   - Definire il template con la sintassi Jinja2 di Copier (`copier.yaml` + file template).
   - Generare un progetto e verificare che la struttura sia corretta.
2. **Definire il template con la sintassi Copier** — mappare la struttura attuale del laif-template in un template Copier:
   - `copier.yaml`: domande interattive (nome progetto, moduli attivi, configurazioni).
   - File con variabili Jinja2 dove necessario.
   - Gestione delle sezioni condizionali (moduli opzionali).
3. **Testare il workflow di aggiornamento (`copier update`)** — questa è la feature killer. Verificare:
   - Che `copier update` applichi le modifiche dal template senza perdere le personalizzazioni del progetto.
   - Come gestisce i conflitti (merge automatico? diff manuale?).
   - Se è possibile aggiornare selettivamente (solo alcuni file o moduli).
4. **Confronto con l'upstream git attuale** — documentare pro e contro:
   - Facilità d'uso per lo sviluppatore.
   - Gestione conflitti.
   - Possibilità di aggiornamento selettivo.
   - Curva di apprendimento.
   - Compatibilità con il nostro workflow CI/CD.
5. **Valutare l'adozione per progetti esistenti** — determinare se Copier può essere adottato anche su progetti già avviati (non solo nuovi fork), e con quale procedura di migrazione.
6. **Decisione architetturale** — questa è una decisione importante che richiede un ADR formale. Se il PoC è positivo, documentare la decisione in `projects/laif-template/decisioni.md`.

### Issue correlate

- Issue 73 — Semplificare processo upstream
- Issue 74 — Modularizzazione template (Copier abilita la modularizzazione)
- Issue 146 — Fork template da master
- Issue 136 — Documentazione upstream

## Stima effort

**PoC: 8h** — sufficiente per generare un template Copier funzionante, testare `copier update` e documentare i risultati. La decisione e l'eventuale migrazione completa richiederebbero ulteriori 16-24h.
