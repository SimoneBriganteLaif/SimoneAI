# Template Drift — Analisi Scostamento dal Template

> Data analisi: 2026-03-21
> Template baseline: **5.7.0**

## Riepilogo Versioni Template

| Repo | Versione Template | Delta da 5.7.0 | Note |
|---|---|---|---|
| sky-agent | 5.7.0 | 0 | Template vanilla, nessun custom |
| far-automation | 5.7.0 | 0 | Aggiornato, progetto attivo |
| wolico | 5.7.0 | 0 | Tool interno, sempre aggiornato |
| sireco | 5.7.0 | 0 | Progetto recente (feb 2026) |
| sebi-group | 5.7.0 | 0 | Solo mockup frontend |
| andriani-sequencing | 5.6.7 | -3 minor | Progetto molto attivo |
| credit-assistant | 5.6.7 | -3 minor | Aggiornato di recente |
| nespak | 5.6.7 | -3 minor | Progetto maturo |
| phoenix-assistant | 5.6.7 | -3 minor | Attivo |
| helia | 5.6.7 | -3 minor | Prodotto complesso |
| studio-perri | 5.6.7 | -3 minor | Molto attivo |
| manfredi | 5.6.4 | -6 minor | Attivo |
| bonfiglioli-riduttori | 5.6.2 | -8 minor | |
| supplynk | 5.6.2 | -8 minor | MVP giovane |
| albini-castelli | 5.6.0 | -10 minor | |
| argo | 5.6.0 | -10 minor | |
| arianna | 5.6.0 | -10 minor | |
| brain | 5.6.0 | -10 minor | |
| competitive-retail | 5.6.0 | -10 minor | |
| fortlan-dibi | 5.6.0 | -10 minor | |
| ids-georadar | 5.6.0 | -10 minor | |
| nessy | 5.6.0 | -10 minor | |
| ref-man | 5.6.0 | -10 minor | |
| searchbridge | 5.6.0 | -10 minor | |
| bandi-platform | 5.6.1 | -9 minor | |
| lamonea | 5.6.1 | -9 minor | |
| sabart-demfor | 5.6.1 | -9 minor | |
| scheduler-roloplast | 5.6.1 | -9 minor | |
| cae-genai | 5.3.5 | -21 minor | Molto indietro |
| formart-marche | 5.3.13 | -17 minor | Indietro |
| coci | 5.4.3 | -14 minor | Indietro |
| experior | 5.4.3 | -14 minor | |
| creama | 5.4.1 | -16 minor | |
| preventivatore | 5.4.0 | -17 minor | FastAPI bloccato a 0.105 |
| umbra-recommend | 5.4.0 | -17 minor | |
| prima-power | 5.6.0 | -10 minor | |
| crif | 5.2.6 | -24 minor | **Piu indietro di tutti** |
| jubatus | standard | N/A | Branch custom, versione non chiara |
| retropricing | N/A | N/A | **NON usa laif-template** (Strapi v3) |

## Repos essenzialmente template vanilla

| Repo | Stato | Raccomandazione |
|---|---|---|
| **sky-agent** | Fork del 2026-03-18, zero codice custom | Archiviare o attendere sviluppo |
| **sebi-group** | Solo mockup frontend, zero backend custom | Fase presales |
| **supplynk** | Solo mockup frontend, zero backend custom | Fase MVP |
| **lamonea** | Solo integrazione TeamSystem passthrough, zero modelli DB | Fase mockup/review |

## Deviazioni strutturali comuni

### Tutti i progetti (standard)
- Schema `prs` per dati applicativi
- Ruolo custom `MANAGER` aggiunto
- `docker-compose.wolico.yaml` per test con rete condivisa
- Changelog controller (boilerplate)

### Deviazioni ricorrenti dal template
1. **FastAPI bloccata a 0.105** in: coci, crif, cae-genai, preventivatore, creama (bug file upload >=0.106)
2. **Schema chat custom** separato da quello template: arianna, bonfiglioli-riduttori (usano schema `prs` invece di `demo`)
3. **ETL come container separato**: andriani-sequencing, far-automation, nespak, prima-power, scheduler-roloplast, sabart-demfor
4. **Modelli DB in un unico models.py** troppo grande (>1000 righe): far-automation (2481), studio-perri (2492), helia (~2400), preventivatore (2180), prima-power (1781), wolico (1600+), bandi-platform (1320), ref-man (1127), formart-marche (1220), searchbridge (1116)

## Repo con stack non-template

| Repo | Stack | Rischio |
|---|---|---|
| **retropricing** | Strapi v3 + React 16 + Node 12 | **CRITICO**: tutte le tecnologie sono EOL |
