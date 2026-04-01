---
tags:
  - "#progetto:laif-issue"
  - "#fase:dev"
aggiornato: "2026-03-18"
---

# Decisioni — LAIF Issue

> Registro delle decisioni architetturali e di processo (ADR).
> Formato: contesto, decisione, alternative considerate, conseguenze.

---

## ADR-001: Approccio progressivo al processo

**Data**: 2026-03-18
**Stato**: Accettata

**Contesto**: Il team stack interno e' piccolo e il processo attuale e' informale. Serve struttura ma senza overhead eccessivo.

**Decisione**: Il documento `processo-issue.md` usa un approccio progressivo con sezioni "base" attive subito e sezioni "[Attivare dopo]" da abilitare quando il team cresce (ruoli formali, gate di approvazione, SLA).

**Alternative considerate**:
- Processo completo da subito — troppo overhead per team piccolo
- Nessun processo documentato — non scala, conoscenza tacita

**Conseguenze**: Il team inizia leggero e aggiunge struttura incrementalmente. Le sezioni "[Attivare dopo]" servono come promemoria di cosa attivare quando serve.

---

## ADR-002: Dashboard separata per colleghi

**Data**: 2026-03-18
**Stato**: Accettata

**Contesto**: La Dashboard Issues contiene dettagli operativi (PR, backlog, RICE) che non servono ai colleghi esterni al team stack interno. Servono due livelli di visibilita'.

**Decisione**: Creare una pagina separata "Stack Interno — Overview" con solo viste ad alto livello (release, roadmap, come segnalare). La Dashboard resta operativa per il team.

**Alternative considerate**:
- Unica pagina con sezioni per audience — confusa, troppo lunga
- Solo la Dashboard — i colleghi vedono troppi dettagli operativi

**Conseguenze**: Due pagine da mantenere, ma con scope chiaro. L'Overview e' read-only per i colleghi.

---

## ADR-003: Skill gestione-issue generalista (V1)

**Data**: 2026-03-18
**Stato**: Accettata

**Contesto**: Servono diverse modalita' di interazione con le issue (triage, preparazione riunione, pianificazione release, health check). Non e' chiaro quali saranno le piu' usate.

**Decisione**: La V1 della skill e' generalista — chiede all'utente cosa vuole fare e guida interattivamente. Si specializzera' in modalita' dedicate man mano che emergono pattern d'uso reali.

**Alternative considerate**:
- Skill separate per ogni modalita' — frammentazione, duplicazione contesto
- Skill con modalita' fisse da subito — rischio di over-engineering

**Conseguenze**: La skill evolve organicamente. Quando una modalita' diventa frequente, si estrae in un flow dedicato.
