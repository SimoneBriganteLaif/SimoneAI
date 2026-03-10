---
fonte: notion
url: https://www.notion.so/2f090ad6ee4880cbb1c9e6160b1d8896
data: 2026-01-22
partecipanti: [LAIF team, Adriano Bezzi]
tipo: follow-up
tags:
  - "#progetto:umbra"
---

# Previsioni settimanali e trasferimento dati

## Decisioni prese

### Scambio file via SFTP
- Cartella SFTP condivisa con struttura IN/OUT
- Accesso programmatico, filtrato per IP, senza VPN
- AWS data transfer service per la connessione

### Formato output
- File in formato CSV (non piu Excel)
- Automazione completa del processo di lettura e import

### Frequenza di elaborazione
- Da aggiornamento mensile a settimanale
- La logica dell'algoritmo resta invariata
- La previsione rimane mensile nonostante elaborazione settimanale
- File settimanali piu contenuti, fine mese tutte le variazioni dell'intero portafoglio

### Riconciliazione dati
- Non ci saranno cambiamenti a quantita, logiche di vendita o prezzi nei dati gia elaborati
- Il sistema aggiornera i dati degli ordini esistenti quando corrispondono

### Altro
- Helia (use cases): gestito in tavolo separato
- Marketing e promozioni WOW: servono dati e analisi, necessario coinvolgere responsabile marketing

## Action items

- [ ] Umbra: fornire credenziali SFTP e percorsi file di input
- [ ] Umbra: creare e condividere esempi di file settimanali
- [ ] Umbra: comunicare disponibilita per meeting su promozioni WOW con Alessandra Olivanti
- [ ] LAIF: completare sviluppo recupero dati e riaggregazione settimanale
