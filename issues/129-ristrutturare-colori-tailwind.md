# Ristrutturare Colori Tailwind

| Campo | Valore |
|---|---|
| **ID** | 129 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | Da rilasciare |
| **Effort** | 2h |
| **Priorita** | Bassa |

## Descrizione originale

Vista la deprecazione di Figma semplificherei la gestione dei colori su Tailwind.

## Piano di risoluzione

1. **Pronto per il rilascio.** I token colore di Tailwind sono stati ristrutturati.
2. **Lavoro completato**: la gestione dei colori è stata semplificata rimuovendo la dipendenza da Figma. I token colore sono ora definiti direttamente nella configurazione Tailwind con una struttura più chiara e manutenibile.
3. **Verifica pre-rilascio**: controllare che tutti i componenti utilizzino i nuovi token colore e che non ci siano riferimenti residui ai vecchi nomi.

### Issue correlate

- Issue 147 — Font sizes rem (allineamento token design system)

## Stima effort

**2h** — completato, in attesa di rilascio. Effort residuo per testing finale e merge.
