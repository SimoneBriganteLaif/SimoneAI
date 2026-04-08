---
versione: "1.0"
ultima-modifica: "2026-04-05"
tags: [template, skill, analisi-repo, laif-kb]
---

# Analisi Repository: {{nome-repo}}

**Data analisi**: {{data}}
**Path**: {{path}}
**Scope**: {{scope}}

---

## Riepilogo

| Metrica | Valore |
|---------|--------|
| Pagine frontend | {{num_pagine}} |
| Profondita max navigazione | {{profondita_max}} livelli |
| Endpoint API | {{num_endpoint}} |
| Tabelle DB | {{num_tabelle}} |
| Componenti modali | {{num_modali}} |
| File con drift dal template | {{num_drift}} |

---

## Alberatura pagine

```
{{alberatura_pagine}}
```

## Endpoint API

| Metodo | Path | Descrizione |
|--------|------|-------------|
{{tabella_endpoint}}

## Tabelle DB

| Tabella | Colonne | FK | Note |
|---------|---------|----|----- |
{{tabella_db}}

## Componenti modali

{{lista_modali}}

## Drift dal template

| File | Stato | Note |
|------|-------|------|
{{tabella_drift}}

---

## Osservazioni

{{osservazioni}}
