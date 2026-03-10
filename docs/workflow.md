# Flussi di Lavoro

← [System.md](../System.md) · [skills.md](skills.md) · [struttura.md](struttura.md)

**Ultimo aggiornamento**: 2026-03-10

---

## Indice

- [Quale flusso usare?](#quale-flusso-usare)
- [Ciclo di vita di un progetto](#ciclo-di-vita-di-un-progetto)
- [Divisione strumenti: Claude Code vs Windsurf](#divisione-strumenti-claude-code-vs-windsurf)
- [Flusso Presales](#flusso-presales)
- [Flusso Development](#flusso-development)
- [Flusso Windsurf (ciclo completo)](#flusso-windsurf-ciclo-completo)
- [Flusso Maintenance](#flusso-maintenance)
- [Flusso Meta / Gestione KB](#flusso-meta--gestione-kb)

---

## Quale flusso usare?

```mermaid
flowchart TD
    Q([Cosa devo fare?]) --> A{Sono in fase...}

    A -->|Presales| B{Fase specifica?}
    A -->|Development| C{Cosa è successo?}
    A -->|Manutenzione KB| D{Tipo operazione?}

    B -->|Nuovo progetto| F1[init-project]
    B -->|Strutturare requisiti| F2[estrazione-requisiti]
    B -->|Generare contratto| F3[genera-allegato-tecnico]
    B -->|Generare brief mockup| F4[genera-mockup-brief]

    C -->|Nuova feature| F5a[feature-workflow\nPlan→Dev→Test→Review]
    C -->|Decisione tecnica rilevante| F5[estrazione-decisioni]
    C -->|Fine sprint| F6[estrazione-pattern]
    C -->|Commit su KB| F7[verifica-pre-commit\nautonoma]

    D -->|Audit KB completo| F8[audit-periodico]
    D -->|Registro modifica struttura/contenuto| F9[gestione-kb\nmod. 1]
    D -->|Nuova idea da registrare| F10[gestione-kb\nmod. 2]
    D -->|Sync documentazione| F11[gestione-kb\nmod. 3]
    D -->|Review idee backlog| F12[gestione-kb\nmod. 4]
```

> Per i dettagli di ogni skill (input, output, flowchart) → [docs/skills.md](skills.md)

---

## Ciclo di vita di un progetto

```mermaid
flowchart LR
    subgraph PRESALES["Presales"]
        P1[init-project] --> P2[estrazione-requisiti]
        P2 --> P3[genera-allegato-tecnico]
        P2 --> P4[genera-mockup-brief]
    end

    subgraph DEV["Development"]
        FW[feature-workflow]
        FP[feature-plan]
        FD[feature-develop]
        FT[feature-test]
        FR[feature-review]
        D2[estrazione-decisioni]
        D3[estrazione-pattern]
        FW --> FP --> FD
        FD --> FT & FR
        FW -.->|decisione tecnica| D2
        FW -.->|fine sprint| D3
    end

    subgraph MAINT["Maintenance"]
        M1[audit-periodico]
    end

    PRESALES -->|contratto firmato| DEV
    DEV -->|go-live| MAINT
    MAINT -.->|nuovo progetto simile| PRESALES
```

---

## Divisione strumenti: Claude Code vs Windsurf

```mermaid
flowchart TD
    subgraph CC["Claude Code"]
        CC1[Gestione Knowledge Base]
        CC2[Pianificazione feature]
        CC3[Generazione brief Windsurf]
        CC4[Review del codice]
        CC5[Esecuzione test]
        CC6[Processamento feedback]
        CC7[KB Enrichment]
        CC8[Gestione meta-file\nchangelog, idee, docs]
    end

    subgraph WS["Windsurf"]
        WS0["Skill: claude-brief\n(~/.codeium/windsurf/skills/)"]
        WS1[Scrittura codice]
        WS2[Implementazione feature]
        WS3[Debug e fix]
        WS4[Refactoring]
        WS5[Compilazione report feedback]
        WS0 -.->|guida| WS1
        WS0 -.->|guida| WS5
    end

    CC2 -->|piano approvato| CC3
    CC3 -->|brief autocontenuto| WS1
    WS1 -->|report feedback| CC6
    CC6 -->|codice pronto| CC4
    CC6 -->|codice pronto| CC5
    CC4 -->|feedback fix| WS3
    CC5 -->|test falliti| WS3
    CC6 -->|pattern, decisioni, problemi| CC7
```

### Quando usare cosa

| Attività | Strumento | Motivo |
|----------|-----------|--------|
| Creare/gestire progetti nella KB | Claude Code | Gestione file .md, skill conversazionali |
| Estrarre requisiti da note meeting | Claude Code | Processo strutturato con loop conversazionale |
| Generare documenti per il cliente | Claude Code | Template e formato specifico |
| Generare brief per Windsurf | Claude Code | Brief autocontenuto con contesto KB |
| Scrivere codice applicativo | Windsurf | Piu token, piu liberta, sviluppo intensivo |
| Compilare report feedback | Windsurf | Documenta difficolta, decisioni, pattern |
| Processare feedback Windsurf | Claude Code | Smista nella KB: pattern, decisioni, problemi |
| Fare code review | Claude Code | Verifica qualita e aderenza a decisioni |
| Eseguire test | Claude Code | Validazione post-sviluppo |
| Documentare decisioni tecniche | Claude Code | ADR nella KB |
| Estrarre pattern a fine sprint | Claude Code | Aggiornamento knowledge base |
| Audit periodico KB | Claude Code | Skill automatizzata |

---

## Flusso Presales

```mermaid
sequenceDiagram
    participant U as Utente
    participant CC as Claude Code
    participant N as Notion
    participant GH as GitHub

    U->>CC: Nuovo progetto
    CC->>CC: skill: init-project
    CC->>U: Nome progetto?
    U->>CC: nome-progetto
    CC->>U: URL GitHub?
    U->>CC: github.com/...
    CC->>U: Link Notion?
    U->>CC: notion.so/...
    CC->>N: Legge note meeting
    CC->>GH: Clona repo, analizza stack
    CC->>CC: Crea struttura in projects/
    CC->>CC: Genera CLAUDE.md nel repo
    CC-->>U: Progetto inizializzato

    Note over U,CC: Dopo il meeting successivo

    U->>CC: Struttura i requisiti
    CC->>CC: skill: estrazione-requisiti
    CC->>U: Domande di chiarimento (una alla volta)
    U->>CC: Risposte
    CC->>CC: Scrive requisiti.md
    CC-->>U: Requisiti strutturati

    Note over U,CC: Quando i requisiti sono validati

    U->>CC: Genera allegato tecnico
    CC->>CC: skill: genera-allegato-tecnico
    CC->>U: Domande su esclusioni, formalità
    U->>CC: Risposte
    CC->>CC: Scrive allegato-tecnico.md
    CC-->>U: Allegato tecnico pronto

    Note over U,CC: Se servono mockup

    U->>CC: Genera brief mockup
    CC->>CC: skill: genera-mockup-brief
    CC->>U: Domande su stile, flussi, brand
    U->>CC: Risposte
    CC->>CC: Scrive mockup-brief.md
    CC-->>U: Brief mockup pronto per Windsurf
```

---

## Flusso Development

### Feature Workflow (ciclo completo)

```mermaid
sequenceDiagram
    participant U as Utente
    participant CC as Claude Code
    participant WS as Windsurf

    Note over U,CC: Nuova feature da sviluppare

    U->>CC: Sviluppa feature RF-XX
    CC->>CC: skill: feature-workflow
    CC->>U: Claude Code o Windsurf?
    U->>CC: Scelta executor

    rect rgb(230, 245, 255)
    Note over CC: Fase 1 — Plan
    CC->>CC: skill: feature-plan
    CC->>U: Domande sul requisito
    U->>CC: Risposte
    CC->>CC: Produce piano tecnico
    CC->>U: Piano proposto — approvi?
    U->>CC: Approvato (GATE 1)
    end

    rect rgb(230, 255, 230)
    Note over CC,WS: Fase 2 — Develop
    CC->>CC: skill: feature-develop
    alt Claude Code diretto
        CC->>CC: Implementa task per task
    else Windsurf (via brief)
        CC->>CC: Genera brief autocontenuto
        CC->>U: Brief salvato in windsurf-briefs/
        U->>WS: Passa brief a Windsurf
        WS->>WS: Implementa + compila report
        U->>CC: Report Windsurf
        CC->>CC: skill: windsurf-feedback
        CC->>CC: Processa feedback → KB
    end
    CC->>U: Sviluppo completo — confermi?
    U->>CC: Confermato (GATE 2)
    end

    rect rgb(255, 245, 230)
    Note over CC: Fase 3 — Test + Review (paralleli)
    par Test
        CC->>CC: skill: feature-test
        CC->>CC: Scrive test + esegue suite
    and Review
        CC->>CC: skill: feature-review
        CC->>CC: Check pattern, duplicazioni, qualita
    end
    end

    alt GATE 3 PASS
        CC->>CC: Aggiorna feature-log.md
        CC->>CC: KB Enrichment (pattern, decisioni, problemi)
        CC-->>U: Feature completata
    else GATE 3 FAIL
        CC->>U: Fix list da test/review
        CC->>CC: Torna a Develop con fix
    end

    Note over U,CC: Fine sprint

    U->>CC: Aggiorna la KB
    CC->>CC: skill: estrazione-pattern
    CC->>U: Pattern riutilizzabili emersi?
    U->>CC: Risposte
    CC->>CC: Estrae pattern → patterns/
    CC-->>U: KB aggiornata
```

### Flusso alternativo (senza orchestratore)

Le sub-skill possono essere invocate singolarmente per task semplici o quando serve solo una fase specifica:

| Skill standalone | Quando usarla da sola |
|-----------------|----------------------|
| `feature-plan` | Voglio solo pianificare, senza sviluppare subito |
| `feature-develop` | Il piano è già stato fatto, devo solo implementare |
| `feature-test` | Il codice è pronto, devo solo testare |
| `feature-review` | Il codice è pronto, voglio solo una review |

### Flusso legacy (senza feature-workflow)

```mermaid
sequenceDiagram
    participant U as Utente
    participant CC as Claude Code
    participant WS as Windsurf

    U->>WS: Implementa feature X
    WS->>WS: Scrive codice
    WS-->>U: Feature implementata
    U->>CC: Rivedi il codice
    CC->>CC: Code review
    CC-->>U: Feedback

    alt Decisione tecnica rilevante
        CC->>CC: skill: estrazione-decisioni
    end
```

---

## Flusso Windsurf (ciclo completo)

Quando l'utente sceglie Windsurf come executor, il ciclo e un loop chiuso:

```mermaid
sequenceDiagram
    participant U as Utente
    participant CC as Claude Code
    participant WS as Windsurf
    participant KB as SimoneAI KB

    CC->>U: Claude Code o Windsurf?
    U->>CC: Windsurf

    rect rgb(230, 245, 255)
    Note over CC: 1. Pianificazione
    CC->>KB: Legge requisiti, pattern, architettura
    CC->>CC: feature-plan
    CC->>U: Piano approvato? (GATE 1)
    end

    rect rgb(230, 255, 230)
    Note over CC,WS: 2. Brief + Sviluppo
    CC->>CC: feature-develop (Windsurf)
    CC->>CC: Genera brief autocontenuto
    Note right of CC: Include: contesto, task,<br/>convenzioni, pattern,<br/>criteri + template report
    CC->>U: Brief salvato in windsurf-briefs/
    U->>WS: Copia brief
    WS->>WS: Implementa feature
    WS->>WS: Compila report feedback
    U->>CC: Passa report a Claude Code
    end

    rect rgb(255, 230, 230)
    Note over CC,KB: 3. Feedback → KB
    CC->>CC: windsurf-feedback
    CC->>KB: Difficolta ricorrenti → problemi-tecnici/
    CC->>KB: Decisioni → decisioni.md
    CC->>KB: Pattern → patterns/
    CC->>U: Sviluppo completo? (GATE 2)
    end

    rect rgb(255, 245, 230)
    Note over CC: 4. Test + Review
    CC->>CC: feature-test + feature-review
    CC->>U: GATE 3
    end

    rect rgb(240, 240, 255)
    Note over CC: 5. Exit
    CC->>KB: feature-log.md
    CC->>U: Feature completata + KB arricchita
    end
```

### Contenuto del brief Windsurf

Il brief e **autocontenuto** (Windsurf non ha accesso alla KB):

| Sezione | Contenuto |
|---------|-----------|
| Metadata | Progetto, requisito, data, repo, stack |
| Obiettivo | Cosa, per chi, perche (2-3 frasi) |
| Contesto tecnico | Architettura + snippet codice dalla codebase |
| Task list | Tabella con ordine, dipendenze, file, tipo |
| Convenzioni LAIF | Copiate integralmente da processi.md |
| Pattern | Copiati integralmente da patterns/ |
| Criteri accettazione | Checklist misurabile |
| Template report | Da compilare a fine sviluppo |

### Contenuto del report feedback

Windsurf compila il report (template incluso nel brief):

| Sezione | Destinazione nella KB |
|---------|----------------------|
| Difficolta ricorrenti | `knowledge/problemi-tecnici/` |
| Decisioni prese | `projects/[nome]/decisioni.md` |
| Pattern individuati | `patterns/` |
| Deviazioni dal piano | `.feature-state.md` |
| Domande aperte | Risolte con l'utente |
| Suggerimenti | `IDEAS.md` |

---

## Flusso Maintenance

```mermaid
sequenceDiagram
    participant CC as Claude Code
    participant KB as Knowledge Base

    Note over CC,KB: Fine mese / fine sprint

    CC->>CC: skill: audit-periodico
    CC->>KB: Legge tutti i progetti
    CC->>CC: Classifica: Aggiorna/Archivia/Recupera/OK
    CC->>KB: Verifica pattern
    CC->>KB: Controlla allineamento tag
    CC->>KB: Cerca domande aperte scadute
    CC->>KB: Aggrega debito tecnico
    CC->>CC: Genera report
    CC-->>CC: Propone azioni
    CC->>KB: Esegue aggiornamenti approvati
```

---

## Flusso Meta / Gestione KB

```mermaid
sequenceDiagram
    participant U as Utente
    participant CC as Claude Code
    participant META as Meta-file

    alt Dopo una modifica alla KB
        U->>CC: Registra questa modifica
        CC->>CC: skill: gestione-kb (modalità 1)
        CC->>U: Framework o contenuto?
        U->>CC: Risposta
        CC->>META: Aggiorna changelog corretto
        CC->>META: Aggiorna docs/ se impattato
    end

    alt Nuova idea
        U->>CC: Ho un'idea per...
        CC->>CC: skill: gestione-kb (modalità 2)
        CC->>U: Categoria? Effort?
        U->>CC: Risposta
        CC->>META: Aggiunge riga a IDEAS.md
    end

    alt Periodicamente
        CC->>CC: skill: gestione-kb (modalità 3 - sync)
        CC->>META: Confronta struttura reale vs docs/
        CC->>META: Aggiorna se necessario

        CC->>CC: skill: gestione-kb (modalità 4 - review idee)
        CC->>U: Idee pendenti — implementare/rimandare/scartare?
        U->>CC: Decisioni
        CC->>META: Aggiorna IDEAS.md
    end
```
