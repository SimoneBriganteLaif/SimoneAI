---
progetto: "jubatus"
tags:
  - "#progetto:jubatus"
  - "#industria:entertainment"
  - "#fase:dev"
---

# Decisioni Tecniche — Jubatus

> **Formato ADR** (Architecture Decision Record).
> Ogni decisione rilevante viene documentata qui nel momento in cui viene presa.

---

## ADR-001: Deploy su account AWS Jubatus

**Data**: 2026-02-13
**Stato**: Accettata
**Autore**: Team (meeting 2026-02-13)

### Contesto

La piattaforma deve accedere al database MySQL RDS e ai bucket S3 di Jubatus. Questi servizi sono nell'account AWS del cliente. Serviva decidere dove deployare la nostra applicazione.

### Opzioni valutate

**Opzione A: Account AWS LAIF separato**
- Pro: Controllo totale sull'infrastruttura, isolamento
- Contro: Complessità accesso cross-account (VPC peering, IAM roles), costi doppi, latenza

**Opzione B: Account AWS Jubatus**
- Pro: Accesso diretto a MySQL via security group, accesso S3 diretto, infra semplificata
- Contro: Dipendenza dall'account del cliente, meno controllo

### Decisione

Deploy su account AWS Jubatus. L'accesso diretto a MySQL e S3 semplifica enormemente l'architettura e riduce i costi. Il team Jubatus (Jonathan/Marco) gestisce l'account e ha dato disponibilita.

### Conseguenze

**Positive**:
- Connessione MySQL via security group (no VPN, no tunnel SSH)
- Accesso S3 diretto per foto/video
- Infrastruttura semplificata

**Negative / trade-off accettati**:
- LAIF dipende dall'account AWS del cliente
- Necessario coordinare con il team Jubatus per modifiche infra

---

## ADR-002: FastAPI come backend framework

**Data**: 2026-01-28
**Stato**: Accettata
**Autore**: Jonathan / Team Jubatus

### Contesto

Il team Jubatus utilizza gia Python per i servizi interni. Serviva scegliere il framework per il backend della piattaforma CS.

### Opzioni valutate

**Opzione A: FastAPI**
- Pro: Async nativo, validazione automatica (Pydantic), OpenAPI auto-generata, gia usato nel laif-template
- Contro: Nessuno significativo nel contesto

**Opzione B: Django/DRF**
- Pro: Ecosistema maturo, admin panel integrato
- Contro: Non async by default, overhead ORM, non standard laif-template

### Decisione

FastAPI. Allineato con il laif-template, async nativo necessario per email sync, e preferenza esplicita del team Jubatus.

### Conseguenze

**Positive**:
- Coerenza con laif-template
- Performance async per sync email
- OpenAPI spec auto-generata per frontend client

**Azioni richieste**:
- Nessuna — gia standard nel template

---

## ADR-003: Multi-provider email (Gmail + Microsoft + SES)

**Data**: 2026-03 (da codice)
**Stato**: Accettata
**Autore**: Team LAIF

### Contesto

Il sistema deve ricevere e inviare email. Il cliente usa info@ come indirizzo di supporto. Serviva decidere come gestire l'integrazione email.

### Opzioni valutate

**Opzione A: IMAP/SMTP diretto**
- Pro: Universale, semplice
- Contro: Meno affidabile, no push notifications, polling pesante

**Opzione B: API dei provider (Gmail API, Microsoft Graph)**
- Pro: Webhook/push, rate limit gestiti, token refresh automatico, metadata ricchi
- Contro: Implementazione per provider, OAuth complexity

**Opzione C: Servizio terzo (SendGrid, Mailgun)**
- Pro: Astrazione unificata
- Contro: Costo aggiuntivo, dipendenza terza parte

### Decisione

API native dei provider con pattern strategy (base → implementazioni). Gmail API e Microsoft Graph per ricezione/invio, AWS SES come fallback per invio. Pattern: `providers/base.py` + implementazioni specifiche; `senders/base.py` + implementazioni specifiche.

### Conseguenze

**Positive**:
- Supporto multi-provider flessibile
- Facile aggiungere nuovi provider
- SES come fallback economico per invio

**Negative / trade-off accettati**:
- Complessita OAuth per ogni provider
- Token refresh da gestire correttamente
- Necessario mantenere piu implementazioni

---

## ADR-004: Approccio iterativo con dati mock

**Data**: 2026-02-13
**Stato**: Accettata
**Autore**: Team (meeting 2026-02-13)

### Contesto

Il cliente vuole validare l'interfaccia prima di collegare i dati reali. Rischio di costruire qualcosa che non corrisponde alle aspettative.

### Opzioni valutate

**Opzione A: Sviluppo con dati reali da subito**
- Pro: Validazione immediata
- Contro: Rischio rallentamenti per accesso DB, setup complesso

**Opzione B: Mock data → validazione → dati reali**
- Pro: Velocita di sviluppo UI, validazione UX senza dipendenze infra
- Contro: Rischio divergenza mock/reale, doppio lavoro integrazione

### Decisione

Approccio iterativo: sviluppare UI con dati mock realistici, validare con il cliente, poi collegare dati reali. Il frontend usa `src/features/tickets/mock/data.ts` con 20+ ticket finti.

### Conseguenze

**Positive**:
- Demo rapide al cliente
- UX validata prima dell'integrazione
- Sviluppo frontend/backend parallelo

**Negative / trade-off accettati**:
- Frontend attualmente non collegato al backend (debito tecnico #1)
- Dati mock potrebbero non riflettere la complessita reale

---

## ADR-005: Separazione codice template vs. app

**Data**: 2026-01 (da laif-template)
**Stato**: Accettata
**Autore**: Team LAIF (standard template)

### Contesto

Il progetto e basato su laif-template che fornisce funzionalita condivise (user management, chat, file, notifiche). Serviva decidere come organizzare il codice custom.

### Decisione

Separazione netta:
- `backend/src/template/` — codice condiviso (NON modificare)
- `backend/src/app/` — codice specifico Jubatus
- `frontend/template/` — UI condivise
- `frontend/src/` — UI custom Jubatus

Aggiornamenti dal template via merge dal repository upstream.

### Conseguenze

**Positive**:
- Aggiornamenti template senza conflitti
- Chiarezza su cosa e custom e cosa no

**Negative / trade-off accettati**:
- Vincolo: non si puo modificare il template per esigenze specifiche
- Se serve una modifica al template, va proposta upstream

---

## Indice decisioni

| ID | Titolo | Data | Stato |
|----|--------|------|-------|
| ADR-001 | Deploy su account AWS Jubatus | 2026-02-13 | Accettata |
| ADR-002 | FastAPI come backend framework | 2026-01-28 | Accettata |
| ADR-003 | Multi-provider email (Gmail + Microsoft + SES) | 2026-03 | Accettata |
| ADR-004 | Approccio iterativo con dati mock | 2026-02-13 | Accettata |
| ADR-005 | Separazione codice template vs. app | 2026-01 | Accettata |
