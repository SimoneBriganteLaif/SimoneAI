---
tags:
  - "#progetto:laif-issue"
  - "#fase:dev"
aggiornato: "2026-03-18"
---

# Flusso Riunione Settimanale — Stack Interno

Scaletta operativa per la riunione settimanale del team stack interno.
Durata target: **50 minuti**.

> Questa scaletta va anche sulla pagina Notion "Flusso Riunione" come riferimento durante la call.

---

## 1. Review In Corso (10 min)

**Vista Notion**: "In Corso" (Issues DB, filtro Status = In Corso)

**Cosa fare**:
- Scorrere tutte le issue in corso
- Per ciascuna chiedere: *"A che punto siamo? Blocker?"*
- Se bloccata: decidere azione (aiuto, deprioritizzare, escalare)
- Se completata: spostare a "Da Rilasciare"

**Output**: stato aggiornato di tutte le issue in corso, blocker identificati.

---

## 2. PR Ready (10 min)

**Vista Notion**: "PR Template" + "PR laif-ds" (inline DB sulla Dashboard)

**Cosa fare**:
- Scorrere le PR aperte
- Per ciascuna decidere:
  - **Merge**: approvata, mergeare
  - **Richiedi modifiche**: commento con richieste specifiche
  - **Discussione**: dubbi tecnici, servono chiarimenti
- Verificare che ogni PR sia associata a un'issue

**Output**: PR reviewate, decisioni prese.

---

## 3. Prossima Release (5 min)

**Vista Notion**: "Prossime Release" (Issues DB, gruppata per Release)

**Cosa fare**:
- Confermare lo scope della prossima release
- Verificare che tutte le issue assegnate siano "Da Rilasciare" o quasi
- Decidere la data di rilascio (di norma entro la settimana)
- Se serve, spostare issue alla release successiva

**Output**: scope release confermato, data rilascio decisa.

---

## 4. Backlog (10 min)

**Vista Notion**: "Backlog" (Issues DB, filtro Status = Backlog, ordinato per RICE Score DESC)

**Cosa fare**:
- Scorrere il backlog dall'alto (RICE piu' alto)
- Decidere se promuovere issue a "Da Iniziare"
- Considerare capacita' del team nella prossima settimana
- Se un'issue e' obsoleta: spostare a "Cancellata"

**Output**: issue promosse o cancellate, backlog aggiornato.

---

## 5. Da Stimare (10 min)

**Vista Notion**: issue con RICE incompleto (filtro: Effort = vuoto OR Confidence = vuoto)

**Cosa fare**:
- Scorrere le issue senza RICE completo
- Per ciascuna, compilare insieme:
  - **Reach**: quanti progetti/team ne beneficiano?
  - **Impatto**: quanto migliora l'esperienza? (3/2/1/0.5/0.25)
  - **Effort**: quante ore stimate? (incluso test, review, doc)
  - **Confidence**: quanto siamo sicuri? (1/0.8/0.5)
- Se serve spike prima di stimare: segnare "In Analisi"

**Output**: RICE compilato per le issue discusse.

---

## 6. Temi aperti (5 min)

**Nessuna vista specifica** — spazio libero.

**Cosa fare**:
- Nuove proposal da discutere
- Feedback su processo/tool
- Segnalazioni da colleghi esterni
- Prossimi temi da mettere in agenda

**Output**: nuove issue create se necessario, note per la prossima riunione.

---

## Checklist pre-riunione

Da fare **prima** della riunione (idealmente con la skill `gestione-issue`):

- [ ] Verificare che le viste Notion siano aggiornate
- [ ] Controllare issue senza assegnazione che sono "In Corso"
- [ ] Identificare issue bloccate da piu' di 1 settimana
- [ ] Preparare lista issue senza RICE per la sezione "Da Stimare"
- [ ] Controllare PR aperte che necessitano review

---

## Note

- Se un punto si allunga troppo, parcheggiarlo: *"Ne parliamo offline, prossima azione: [chi] [cosa]"*
- Tenere un timer visibile per rispettare i tempi
- Annotare le decisioni prese direttamente sulle issue Notion durante la call
