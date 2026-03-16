# Config File e Feature Flag centralizzati

| Campo | Valore |
|---|---|
| **ID** | 141 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | To Review |
| **Tag** | Filone Test |

## Descrizione originale

Attualmente abbiamo config sparse fra backend, frontend e infra. È necessario uniformare il punto dove sono queste opzioni, soprattutto perché nel prossimo futuro potranno entrare nuove configurazioni condizionali da attivare in base al progetto.

## Piano di risoluzione

1. **Già in To Review con PR aperta.** Verificare lo stato della PR prima di procedere.
2. **Creare un file di configurazione centrale** (YAML o JSON) per tutti i feature flag e le configurazioni condizionali:
   - Posizione: root del progetto (es. `config.yaml` o `config/features.yaml`).
   - Struttura chiara con sezioni per backend, frontend, e shared.
   - Versionato in git (le configurazioni sono parte del progetto, non segreti).
3. **Backend: lettura della configurazione allo startup** — il backend carica il file di config all'avvio e lo espone internamente tramite un servizio di configurazione. Le variabili d'ambiente possono fare override (per ambienti diversi: dev, staging, prod).
4. **Frontend: ricezione dei feature flag attivi tramite endpoint API** — creare un endpoint `GET /api/config/features` che restituisce i flag attivi per il frontend. Il frontend li carica all'avvio e li rende disponibili tramite un context o nello store Redux.
5. **Definire le categorie di flag**:
   - **Core**: funzionalità sempre attive (auth, user management).
   - **Optional**: funzionalità attivabili per progetto (ticketing, media service, agent AI).
   - **Experimental**: funzionalità in beta, attivabili solo esplicitamente.
6. **Meccanismo di override per progetto** — ogni progetto derivato dal template può fare override dei flag di default nel proprio file di configurazione, senza modificare il template originale.

### Issue correlate

- Issue 70 — Permissions e feature flags (integrazione con il sistema di permessi)

## Stima effort

**6-8h** — la struttura del file di config e l'endpoint API sono rapidi (2h). Il grosso è nel refactoring dei punti dove le config sono attualmente sparse (4h) e nel testing dell'override per progetto (2h).
