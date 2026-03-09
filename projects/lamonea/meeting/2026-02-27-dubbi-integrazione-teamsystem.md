---
fonte: notion
url: https://www.notion.so/31490ad6ee4880f5aca2f06b8a170b92
data: 2026-02-27
partecipanti: [Simone Brigante, Luca, Daniele]
tipo: follow-up
tags:
  - "#progetto:lamonea"
---

# Dubbi Integrazione TeamSystem

Call interna per discutere strategia di integrazione con TeamSystem e domande per il consulente Alessandro.

## Strategia di integrazione

- **Approccio concordato**: estrarre tutto inizialmente, poi filtrare basandosi su cosa è popolato e necessario
- Razionale: il cliente non è tecnico su TeamSystem, non può fornire elenco completo dei campi
- Disattivare campi sicuramente non necessari per snellire API, ma mantenere flessibilità di riattivarli
- Obiettivo: identificare quali tabelle TS vengono usate da Lamonea (forse 30 su 100)

## Domande per Alessandro (consulente TeamSystem)
1. Come è strutturato il data model
2. Quali "Tabella" vengono usate da Lamonea
3. Come creare un servizio di lettura
4. Come creare un servizio di scrittura
5. Gestione dei documenti (PDF) nel sistema
6. Quanto tempo richiede l'estrazione massiva (intera tabella articoli)

## Test di estrazione
- Test su tabella 5001 (clienti) e 5002 (articoli)
- Estratte oltre 145.000 righe di dati articoli
- Molti campi vuoti, conferma necessità di scremare
- Estrazione più veloce rispetto a test precedenti

## Lavoro completato
- Luca ha analizzato documentazione API TS (83 pagine) con Claude
- Daniele ha creato guida API in parallelo
- Codice pushato su repository
- Mockup creato ma non ancora pushato

## Action Items
- Luca: schedulare meeting con Alessandro per settimana prossima
- Luca: preparare domande per Alessandro su data model e configurazione
- Team: estrarre tutti i dati inizialmente, poi filtrare
- Review analisi Claude della documentazione API TS
