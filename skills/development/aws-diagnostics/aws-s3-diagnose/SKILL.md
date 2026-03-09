---
nome: "AWS S3 Diagnose"
descrizione: >
  Diagnosi dei bucket S3 di un progetto LAIF.
  Verifica accessibilita, dimensioni, conteggio oggetti, upload recenti, file grandi.
  Solo lettura — nessuna modifica alle risorse AWS.
fase: development
versione: "1.0"
stato: beta
legge:
  - projects/[nome]/aws-config.yaml
scrive:
  - (nessun file — skill di diagnosi)
aggiornato: "2026-03-09"
---

# Skill: AWS S3 Diagnose

## Obiettivo

Diagnosi dei bucket S3 di un progetto: dimensioni, conteggio oggetti, upload recenti, file di grandi dimensioni.

---

## Perimetro

**Fa**: verifica accessibilita bucket, calcola dimensioni, elenca oggetti recenti e grandi.

**NON fa**: non scarica file, non modifica bucket policy, non cancella oggetti.

**Rimandi**:
- Triage rapido → `aws-triage/`

---

## Quando usarla

- Verificare se un bucket e' pieno o in crescita anomala
- Trovare upload recenti (debug caricamento file)
- Identificare file grandi che occupano spazio
- Verificare accessibilita dopo un cambio di policy

---

## Prerequisiti

- [ ] `projects/[nome]/aws-config.yaml` configurato
- [ ] Profilo AWS con permessi di lettura su S3

---

## Loop conversazionale

### Domanda 1 — Progetto e ambiente

> Quale progetto e ambiente?

### Domanda 2 — Quale bucket

> Quale bucket?
> - `data` — bucket dati privato
> - `frontend` — bucket frontend statico
> - `all` — entrambi

### Domanda 3 — Cosa investigare

> Cosa investigare?
> - `overview` — dimensione totale e conteggio oggetti
> - `recent` — ultimi upload (ultime 24h)
> - `large` — file piu grandi
> - `all` — tutto

---

## Script

```bash
python3 skills/development/aws-diagnostics/aws-s3-diagnose/run.py \
  --project <nome> --env <dev|prod> --bucket <data|frontend|all> --mode <overview|recent|large|all>
```

---

## Vincoli di sicurezza

- Solo comandi read-only: list-objects-v2, head-bucket, s3 ls
- Nessun put-object, delete-object, put-bucket-policy
- Profilo AWS sempre esplicito

---

## Checklist qualita

- [ ] Bucket verificati con output strutturato
- [ ] Dimensioni e conteggi riportati
- [ ] Errori gestiti (bucket non trovato, accesso negato)

#stack:aws #stack:s3 #fase:development
