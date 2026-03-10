---
fonte: notion
url: https://www.notion.so/31890ad6ee4880d59a6de7551718ba45
data: 2026-03-03
partecipanti: [LAIF team, Adriano Bezzi, Alessandra Olivanti]
tipo: follow-up
tags:
  - "#progetto:umbra"
---

# Pianificazione Sistema Promozioni WOW

## Campagne speciali (oltre alle WOW settimanali)

- **WOW Si Parte**: gennaio, durante convention, durata 3+ settimane
- **Sorprese di Pasqua**: 2-3 settimane prima di Pasqua, 8-9 promozioni
- **Umbra Summer**: tutto luglio e agosto
- **Aspettando il Natale**: 1-24 dicembre

In questi periodi servono slot multipli per gestire piu promozioni contemporaneamente.

## Struttura budget fornitori

- Livello base: fornitore (es. 100.000 EUR per fornitore X)
- Per alcuni fornitori: anche per classe di prodotti
- Per altri: anche per sottoclasse
- Raramente a livello di articolo
- Il budget e sull'**acquistato** (sell-in), non sul venduto (sell-out)
- Rappresenta quanto comprare dal fornitore per raggiungere obiettivo e ottenere premi

## Mockup interfaccia proposta

- Vista Gantt con slot temporali per promozioni future
- Almeno 4 settimane di pianificazione visibile
- Possibilita di selezionare articoli per Studio e Laboratorio
- Score di prioritizzazione: priorita d'acquisto, importo previsto, giorni autostock
- Info ultima WOW per articolo/fornitore
- Avanzamento budget: budget totale vs venduto (valorizzato CELIN)
- Slot configurabili con date modificabili e articoli multipli

## Funzionalita richieste

- Visualizzazione Gantt per pianificazione
- Almeno 4 settimane di pianificazione visibile
- Aggiunta manuale di articoli non suggeriti dall'algoritmo
- Override suggerimenti per accordi specifici con fornitori
- Gestione slot con durate variabili (2 settimane standard, fino a 8 per campagne speciali)

## Tracciamento performance

- Confronto previsione vs vendite effettive
- Calcolo avanzamento budget dopo ogni promozione
- Storico WOW con dati previsti vs effettivi
- Valorizzazione sia sell-out che CELIN

## Dati necessari

- Listino CELIN (acquisto standard) — unico listino
- Budget fornitori: fornitore, classe, sottoclasse, marchio, budget
- Regole numero WOW per fornitore (min/max)
- Storico promozioni WOW (caricamento una tantum)

## Setup tecnico SFTP

- Cartella SFTP disponibile con sottocartelle in/out
- Issue malformazione dati (numeri con punto) risolto
- Caricati dati week 8 e week 9
- Previsioni marzo non ancora generate (problemi tecnici)
- Necessario configurare ponte S400-DMZ per accesso diretto

## Workflow sviluppo concordato

1. Validare prima grafica e interfaccia con dati finti
2. Iterazioni frequenti per definire funzionalita e flusso
3. Solo dopo validazione UI/UX, procedere con integrazione dati reali
4. Evitare rework sviluppando l'interfaccia corretta da subito

## Action items

- [ ] Adriano: controllare situazione magazzino e versioni mancanti
- [ ] Adriano: preparare lista strutture dati necessarie
- [ ] Adriano: coordinare switch da cartella condivisa a cartella SFTP
- [ ] Adriano: configurare accesso S400 alla cartella SFTP in DMZ
- [ ] Team Umbra: fornire storico promozioni WOW
- [ ] Team Umbra: fornire listini CELIN
- [ ] Follow-up: 12 marzo ore 10-11 per validare grafica e flusso
