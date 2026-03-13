---
progetto: "albini-castelli"
ultimo-aggiornamento: "2026-03-12"
tags:
  - "#progetto:albini-castelli"
  - "#fase:manutenzione"
---

# Stato Progetto — Albini & Castelli

> Punto di ingresso per riprendere lo sviluppo. Ultimo aggiornamento: 2026-03-12.

---

## Stato complessivo

**Sviluppo concluso.** L'applicazione Schede Cantiere è in produzione su AWS (ECS + RDS + S3, eu-west-1). La fase attuale è di **supporto alla migrazione**: il cliente deve portare la propria gestione storica dei cantieri sull'applicazione. Il lavoro tecnico principale riguarda l'import dei dati storici, la formazione e il supporto operativo.

---

## Mappa requisiti vs. implementazione

> Requisiti da ricostruire formalmente. Le feature principali rilevate dalla codebase sono:

| Area | Modulo backend | Feature frontend | Stato |
|------|---------------|-----------------|-------|
| Anagrafica cantieri | `cantiere`, `cantiere_anno` | `sites-sheets` | Completo |
| Scheda dettaglio cantiere | — | `site-sheet-detail` | Completo |
| Revisioni budget | `revisione`, `revisione_versione`, `revisione_fase` | `site-sheet-detail` | Completo |
| KPI extra revisione | `revisione_extra_kpi`, `revisione_year_summary` | `site-sheet-detail` | Completo |
| Tabellone revisioni | `tabellone_revisione` | — | Completo |
| Consuntivi lavori | `consuntivo` | — | Completo |
| Anagrafica clienti | `cliente` | — | Completo |
| Mappali catastali | `mappale` | — | Completo |
| Dashboard aggregata | `dashboard` | `dashboard` | Completo |
| Import storico | `import_storico` | — | Completo |
| Upload file | `upload` | — | Completo |
| Changelog dati | `changelog` | `changelog` | Completo |

---

## Blocchi critici

### 1. Migrazione dati storici cliente

Il cliente deve migrare la propria gestione (presumibilmente fogli Excel o sistema precedente) sull'applicazione. Il modulo `import_storico` è già disponibile, ma richiede:
- Verifica della compatibilità del formato dati cliente
- Eventuale adattamento degli script di import
- Validazione dei dati importati con il cliente

---

## Prossimi passi suggeriti

### Priorità 1 — Supporto migrazione dati

1. **Raccogliere il formato dati esistente del cliente**
   - Richiedere un campione dei file/fogli Excel attualmente usati
   - Verificare compatibilità con `import_storico`

2. **Pianificare sessioni di import con il cliente**
   - Eseguire import in ambiente dev per validazione
   - Correggere eventuali anomalie prima del caricamento prod

3. **Formazione utenti**
   - Accompagnare i referenti del cliente nell'uso dell'applicazione
   - Documentare eventuali gap UX emersi durante l'uso reale

### Priorità 2 — Stabilizzazione post-migrazione

4. **Monitoraggio AWS post-migrazione**
   - Usare `aws-triage` per health check periodici
   - Attenzionare RDS dopo l'import massivo di dati storici

5. **Documentazione KB**
   - Compilare `requisiti.md` con la skill `estrazione-requisiti`
   - Registrare decisioni tecniche rilevanti in `decisioni.md`

---

## File di riferimento

| Documento | Contenuto |
|-----------|-----------|
| [README.md](README.md) | Overview progetto, team, timeline, link |
| [architettura.md](architettura.md) | Stack, diagrammi, moduli applicativi |
| [decisioni.md](decisioni.md) | Decisioni tecniche (ADR) |
| [requisiti.md](requisiti.md) | Requisiti (da compilare) |
| [feature-log.md](feature-log.md) | Feature implementate con note tecniche |
| [manutenzione.md](manutenzione.md) | Note supporto post go-live e migrazione |
| [meeting/](meeting/) | Note meeting |

**Repository codice**: `/Users/simonebrigante/LAIF/repo/albini-castelli/`
