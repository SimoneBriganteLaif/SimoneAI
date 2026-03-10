---
fonte: notion
url: https://www.notion.so/30290ad6ee4880b9ba57eef0f3b9aed4
data: 2026-02-09
partecipanti: [LAIF team, Adriano Bezzi, Alessandra Olivanti]
tipo: follow-up
tags:
  - "#progetto:umbra"
---

# Promozioni WOW — Requisiti dettagliati

## Struttura promozioni WOW

- 2 nuove WOW a settimana: 1 Studio + 1 Laboratorio
- Ogni WOW dura 15 giorni (si sovrappongono)
- Pianificazione con 15 giorni di anticipo
- Agosto e luglio esclusi (capitolone unico)
- ~40 fornitori totali, di cui 8-9 con target specifici

## Criteri di selezione attuali (processo manuale di Alessandra)

- Priorita di acquisto (indicatore di urgenza)
- Importo previsto (valore economico previsione di vendita)
- Giorni all'out of stock
- Volume di movimentazione
- WOW fatte su classi o sottoclassi, non su singoli articoli

## Vincoli temporali

- Fornitori con target (~8-9): min 2 / max 5 WOW/anno
- Altri fornitori: max 2 WOW/anno
- Non riproporre stessa classe/sottoclasse se fatta di recente

## Obiettivo del sistema AI

- Lista di candidati per WOW del mese corrente e mesi successivi
- ~5 suggerimenti per Studio + ~5 per Laboratorio per ogni settimana target
- Aggiornamento quindicinale, in sincrono con ciclo pianificazione
- Supporto decisionale, non sostitutivo del giudizio di Alessandra

## Dati che Umbra deve passare a LAIF

1. **Storicita WOW**: date inizio/fine, fornitore, linea, classe, sottoclasse, rendimento vs target
2. **Budget per fornitore**: suddiviso per classe e sottoclasse (sell-in)
3. **Listino acquisto**: costo di acquisto per prodotto
4. **Avanzamento fatturato**: per fornitore/classe/sottoclasse (sell-in), aggiornato settimanalmente
5. **Lista fornitori WOW + vincoli temporali**: ~40 fornitori, classi/sottoclassi, intervalli min/max
6. **Distinzione Studio/Laboratorio**: gia in anagrafica prodotti
7. **File settimanali ordini e sconti**: da cartella SFTP `elaborazioni_settimanali`

## Logica di valorizzazione

- L'importo previsto e sell-out (previsione vendita)
- Per decidere WOW: valorizzare al costo di acquisto (sell-in)
- Il sell-in serve per l'avanzamento consultivo sul budget del fornitore

## Stato tecnico SFTP

- IP autorizzati: 18.267.69 e 54.246.152.243
- Cartella `elaborazioni_settimanali` creata nell'SFTP
- Problema: certificato scaduto per SFTP (da risolvere con Paolo sistemista)
- Estrazione ordini funziona, sconti non ancora completata

## Task tecnici LAIF

### Ingestion nuovi dati
- [ ] Leggere file dalla cartella SFTP `elaborazioni_settimanali`
- [ ] Integrare listino acquisto
- [ ] Integrare dati budget normalizzati
- [ ] Importare storicita WOW
- [ ] Importare avanzamento fatturato

### Logica algoritmo
- [ ] Conversione sell-out -> sell-in
- [ ] Aggregazione per fornitore/classe/sottoclasse
- [ ] Implementare vincoli temporali per fornitore
- [ ] Gestire storicita come vincolo di esclusione
- [ ] Distinguere linea Studio vs Laboratorio
- [ ] Escludere agosto
- [ ] Calcolo scostamento budget

### Output
- [ ] ~5 suggerimenti per Studio e ~5 per Laboratorio per settimana
- [ ] Motivazione del suggerimento (gap budget, importo, priorita, OOS, storicita, vincoli)
- [ ] Aggiornamento quindicinale
- [ ] Perimetro pianificazione: 3 settimane avanti con 2 settimane di anticipo

## Action items

- [ ] Alessandra: preparare file fornitori + classi/sottoclassi WOW + vincoli temporali
- [ ] Adriano: completare estrazione settimanale sconti
- [ ] Adriano: passare storicita WOW con tracciato completo
- [ ] Adriano: sviluppare app gestionale per budget normalizzato
- [ ] Adriano: integrare listino acquisto in anagrafica
- [ ] Adriano: implementare estrazione avanzamento fatturato
- [ ] Paolo: risolvere certificato SFTP scaduto
- [ ] LAIF: inviare recap requisiti a Umbra
