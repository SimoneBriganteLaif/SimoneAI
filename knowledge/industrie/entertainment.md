---
industria: "Entertainment / Eventi"
progetti-laif: [jubatus]
data-creazione: "2026-03-09"
ultimo-aggiornamento: "2026-03-09"
tags:
  - "#industria:entertainment"
---

# Knowledge: Entertainment / Eventi

## Overview del settore

Clienti tipici: aziende che offrono servizi B2C legati a eventi dal vivo (concerti, festival, sport). Spesso startup o PMI in rapida crescita con team tecnico ridotto. Alto volume di utenti concentrato in finestre temporali brevi (giorno dell'evento). Maturità digitale variabile — spesso hanno un prodotto core ma infrastruttura interna frammentata.

---

## Problemi business ricorrenti

- **Gestione customer care frammentata**: richieste via email, social, WhatsApp senza sistema unico. Volume alto post-evento con richieste semplici e ripetitive (90%+ risolvibili automaticamente).
- **Dashboard per partner**: necessità di fornire dati aggregati a partner/sponsor senza esporre dati interni. Grafana spesso usato come soluzione iniziale ma non user-friendly per non-tecnici.
- **Picchi di carico**: traffico concentrato durante/dopo l'evento. Serve scalabilità orizzontale e gestione code.

---

## Aspettative tipiche dei clienti

- **KPI importanti**: velocità di risposta al cliente, tasso di risoluzione automatica, NPS post-evento
- **Timori principali**: downtime durante l'evento, perdita dati (foto/video), costi infrastruttura durante i picchi
- **Terminologia**: "experience", "engagement", "touchpoint", "fan journey", "backstage access"

---

## Vincoli regolatori

- **GDPR / Privacy**: gestione immagini (face recognition) richiede consenso esplicito, data retention policy, diritto all'oblio
- **Diritti d'immagine**: foto e video degli eventi possono avere restrizioni contrattuali con artisti/organizzatori

---

## Integrazioni tipiche richieste

| Sistema | Tipo | Frequenza richiesta | Note |
|---------|------|-------------------|------|
| Email provider (Gmail, custom) | Input ticket | Alta | OAuth, IMAP, multi-provider |
| Database legacy (MySQL, PostgreSQL) | Read-only | Alta | Spesso su AWS RDS, accesso SSH |
| Storage S3 | File media | Alta | Foto, video, documenti |
| WhatsApp Business API | Comunicazione | Media | Bot per notifiche e supporto |
| Sistemi di ticketing eventi | Integrazione | Bassa | Variabile per cliente |

---

## Pattern tecnici più usati in questo settore

- [list-detail-lazy-loading](../../patterns/list-detail-lazy-loading.md) — UI con dati pesanti (foto, allegati)
- [html-sanitization-dompurify](../../patterns/html-sanitization-dompurify.md) — email customer care con HTML non fidato

---

## Esperienze LAIF in questo settore

| Progetto | Anno | Problema risolto | Outcome | Note |
|---------|------|----------------|---------|------|
| Jubatus | 2026 | Customer care frammentato, ticketing email | MVP in corso | Face recognition B2C, eventi musicali |

---

## Note vendita / presales

- **Obiezione comune**: "Il nostro team tecnico può fare questo internamente" → **Risposta**: focus su time-to-market e liberare il team tecnico per il prodotto core
- **Leva efficace**: mostrare demo con dati finti subito (approccio iterativo validato su Jubatus)
- Clienti di questo settore apprezzano velocità e risultati visibili più che documentazione tecnica dettagliata
