---
progetto: "sebi-group"
ultimo-aggiornamento: "2026-03-17"
tags:
  - "#progetto:sebi-group"
  - "#fase:presales"
---

# Stato Progetto — Sebi Group

> Punto di ingresso per riprendere il lavoro. Ultimo aggiornamento: 2026-03-17.

---

## Stato complessivo

Fase presales avanzata. Raccolta requisiti completata (kickoff + on-site). Documenti prodotti: requisiti strutturati (17 RF + 5 RNF), allegato tecnico contrattuale, stima modulare (93-142 g/u), brief mockup. In attesa di: punto situazione con cliente (23 marzo), meeting fornitore gestionale, produzione mockup.

---

## Deliverable prodotti

| Documento | Stato | Note |
|-----------|-------|------|
| Note meeting on-site (2026-03-16) | Completato | 2 sessioni documentate |
| `requisiti.md` | Completato v1.0 | 17 RF + 5 RNF, 8 domande aperte |
| `allegato-tecnico.md` | Bozza v1.0 | Max 3 pagine, linguaggio non tecnico |
| `stima-modulare.md` | Completato v1.0 | 6 moduli, 93-142 g/u totali |
| `mockup-brief.md` | Completato v1.0 | 6 schermate, pronto per Windsurf |
| Mockup UI | Da fare | Brief pronto, avviare con Windsurf |
| Repository codice | Da fare | Fork laif-template → sebi-group |

---

## Blocchi critici

### 1. Meeting fornitore gestionale Osma

Il modulo M4 (Integrazione Gestionale) e parti di M3 (Import) dipendono dalla comprensione delle API Osma. Senza questo meeting, la stima M4 ha un range ampio (12-20 g/u) e potrebbe crescere.

**Azione**: Michele Bonicalzi deve organizzare il meeting. Portare le domande dalla sezione "Domande aperte" di `requisiti.md`.

### 2. Verifica API WebCargo

L'integrazione WebCargo (M2 export aereo) è stata messa come fase successiva nell'allegato tecnico, ma il cliente la considera importante. Da verificare scope e costi delle API.

**Azione**: cliente deve contattare WebCargo per documentazione API.

### 3. Esempi email reali

Il tuning del classificatore AI (M1) e del parser preventivi (M2, M3) richiede esempi reali di thread email con screenshot del gestionale. Richiesti al cliente come action item dell'on-site.

**Azione**: Stefano e Gabriella devono preparare esempi (export + import).

---

## Prossimi passi suggeriti

### Priorità 1 — Chiusura presales (settimana 2026-03-17)

1. **Punto situazione con cliente** (2026-03-23)
   - Presentare requisiti estratti per validazione
   - Presentare stima modulare e discutere scope/priorità
   - Raccogliere risposte alle domande aperte
   - Concordare timeline per mockup e proposta commerciale

2. **Produzione mockup**
   - Avviare Windsurf con `mockup-brief.md`
   - Review con il team prima di presentare al cliente

3. **Fork repository**
   - Creare repo `sebi-group` da laif-template

### Priorità 2 — Proposta commerciale (settimane successive)

1. **Meeting fornitore gestionale** — definire API, vincoli, costi
2. **Aggiornare stima** dopo meeting gestionale (ridurre incertezza M4)
3. **Preparare proposta commerciale** con moduli, pricing, timeline
4. **Presentazione al cliente** con mockup + proposta

### Backlog

- Definire architettura tecnica (dopo approvazione proposta)
- Setup ambiente sviluppo
- Raccolta esempi email per training AI

---

## File di riferimento

| Documento | Contenuto |
|-----------|-----------|
| [README.md](README.md) | Overview progetto, team, timeline, moduli, link |
| [requisiti.md](requisiti.md) | 17 requisiti funzionali + 5 non funzionali |
| [allegato-tecnico.md](allegato-tecnico.md) | Allegato contrattuale max 3 pagine |
| [stima-modulare.md](stima-modulare.md) | Stima g/u per modulo (93-142 totale) |
| [mockup-brief.md](mockup-brief.md) | Brief per mockup Windsurf (6 schermate) |
| [meeting/](meeting/) | Note di tutti i meeting |

<!-- **Repository codice**: `/Users/simonebrigante/LAIF/repo/sebi-group/` -->
