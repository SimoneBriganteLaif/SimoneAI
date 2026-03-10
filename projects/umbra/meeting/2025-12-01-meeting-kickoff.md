---
fonte: notion
url: https://www.notion.so/2b790ad6ee4880dfa9dccc6639bbbded
data: 2025-12-01
partecipanti: [LAIF team]
tipo: kickoff
tags:
  - "#progetto:umbra"
---

# Meeting Kickoff — Umbra Recommender

## Obiettivo

Primo meeting di allineamento tecnico sul progetto di miglioramento della piattaforma recommender e pianificazione promozioni WOW.

## Punti discussi

### Miglioramento piattaforma recommender

- Passaggio dall'aggiornamento mensile a settimanale dei dati
- Revisione dell'integrazione via FileZilla — attualmente import manuale via SFTP di file di testo
- Necessita di snellire il processo di import dati

### Pianificatore promozioni WOW

- Sviluppo modulo dedicato basato su algoritmo di raccomandazione
- Criteri considerati: obiettivi sell-in per fornitore/classe/sottoclasse, storico WOW, performance passate, stagionalita, lead time fornitori, volumi previsti, sovrapposizioni campagne canvas, fornitori attenzionati, numero WOW da programmare per semestre
- Output: suggerimenti di prodotti da mettere in promozione con motivazione e interpretazione della raccomandazione
- Il cliente poi inserisce la promozione nel gestionale, e il dato viene riletto nello scarico dati successivo
- Non serve tracciare quali predizioni il cliente intende utilizzare

### Scambio dati

- AS400 esporta in cartella, serve fornire un IP statico
- Vale sempre l'ultimo file, si deve ricavare la settimana
- Due opzioni discusse: server (LAIF recupera i file) o email (Umbra li manda)

### Clusterizzazione prodotti

- Gerarchia: classe > sottoclasse > capitolo > modello > prodotto
- Discussa possibilita di usare tabella associazione modello-prodotti di Adriano invece dell'algoritmo semantico attuale
- Necessario verificare coerenza della clusterizzazione automatica con la segmentazione B2B

### Promozioni WOW e Canvas

- Servono dati storici di WOW e Canvas
- Dati gia inclusi nei file di vendita condivisi (incluso tipo WOW/Canvas)
- Regole: non ripetere sullo stesso prodotto entro 4-6 mesi, considerare priorita budget
- Coinvolgere Alessandra per budget e regole marketing

## Action items

- [ ] Comunicare ad Adriano la soluzione piu semplice per automatizzare lo scambio dati
- [ ] Adriano: modificare schedulazione da mensile a settimanale
- [ ] Adriano: condividere tabella associazione modello-prodotti
- [ ] Analizzare algoritmo di clustering per verifica coerenza con segmentazione B2B
- [ ] Coinvolgere Alessandra per budget e regole marketing
