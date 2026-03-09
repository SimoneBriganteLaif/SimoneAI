---
industria: "Healthcare / Medical Devices"
progetti-laif: [lamonea]
data-creazione: "2026-03-09"
ultimo-aggiornamento: "2026-03-09"
tags:
  - "#industria:healthcare"
---

# Knowledge: Healthcare / Medical Devices

## Overview del settore

Clienti tipici: aziende che producono o distribuiscono dispositivi medici. Struttura organizzativa tradizionale con processi regolamentati. Maturità digitale medio-bassa — spesso usano software legacy o fogli Excel per gestione catalogo e CRM. Cicli decisionali lunghi, molteplici stakeholder (commerciale, tecnico, regolatorio).

---

## Problemi business ricorrenti

- **Gestione catalogo prodotti complessa**: dispositivi medici con molte varianti, certificazioni, compatibilità, documentazione tecnica. Catalogo spesso frammentato tra PDF, Excel, e sistemi legacy.
- **CRM specifico per settore**: il ciclo di vendita è lungo e coinvolge demo prodotto, gare d'appalto, referenze cliniche. CRM generici non catturano bene queste peculiarità.
- **Tracciabilità e compliance**: ogni dispositivo deve avere documentazione completa per audit e normative.

---

## Aspettative tipiche dei clienti

- **KPI importanti**: copertura catalogo digitale, tempo di onboarding nuovi prodotti, compliance rate
- **Timori principali**: errori nei dati prodotto (rischio normativo), migrazione da sistemi esistenti, formazione del personale
- **Terminologia**: "scheda tecnica", "codice CND", "classe di rischio", "MDR", "marcatura CE", "UDI", "catalogo ospedaliero"

---

## Vincoli regolatori

- **MDR (Medical Device Regulation EU 2017/745)**: regolamento europeo per dispositivi medici. Impatta classificazione prodotti, documentazione tecnica, sorveglianza post-market.
- **UDI (Unique Device Identification)**: sistema di identificazione unico per ogni dispositivo — influenza struttura dati e codici prodotto.
- **ISO 13485**: standard qualità per dispositivi medici — può richiedere audit trail nel software.
- **GDPR**: se il sistema gestisce dati di pazienti o operatori sanitari.

---

## Integrazioni tipiche richieste

| Sistema | Tipo | Frequenza richiesta | Note |
|---------|------|-------------------|------|
| ERP aziendale | Bidirezionale | Alta | Gestionale per ordini, magazzino, fatturazione |
| Piattaforme gare d'appalto | Consultazione | Media | MePA, Consip, portali regionali |
| Sistemi di certificazione | Read-only | Media | Database CE, MDR, UDI |
| Email / PEC | Comunicazione | Alta | PEC obbligatoria per comunicazioni ufficiali |

---

## Pattern tecnici più usati in questo settore

- Gestione catalogo gerarchico con molte varianti e attributi dinamici
- Import/export dati da Excel (formato predominante nel settore)

---

## Esperienze LAIF in questo settore

| Progetto | Anno | Problema risolto | Outcome | Note |
|---------|------|----------------|---------|------|
| Lamonea | 2026 | Catalogo prodotti + CRM custom | In fase presales | Dispositivi medici, distribuzione |

---

## Note vendita / presales

- **Obiezione comune**: "Abbiamo già il gestionale" → **Risposta**: il gestionale non copre la parte commerciale/catalogo web; integrazione bidirezionale per evitare doppio inserimento
- **Leva efficace**: compliance normativa come driver di adozione (MDR richiede dati strutturati)
- Clienti healthcare richiedono documentazione dettagliata e garanzie sulla sicurezza dei dati prima di procedere
