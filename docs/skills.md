# Catalogo Skill

← [System.md](../System.md) · [workflow.md](workflow.md) · [struttura.md](struttura.md)

**Ultimo aggiornamento**: 2026-04-01

---

## Indice

- [Mappa globale skill](#mappa-globale-skill)
- [Sistema di stato](#sistema-di-stato-delle-skill)
- [Riepilogo](#riepilogo)
- **Presales**: [init-project](#init-project) · [estrazione-requisiti](#estrazione-requisiti) · [genera-allegato-tecnico](#genera-allegato-tecnico) · [genera-mockup-brief](#genera-mockup-brief)
- **Development**: [feature-workflow](#feature-workflow) · [feature-plan](#feature-plan) · [feature-develop](#feature-develop) · [feature-test](#feature-test) · [feature-review](#feature-review) · [windsurf-feedback](#windsurf-feedback) · [estrazione-decisioni](#estrazione-decisioni) · [estrazione-pattern](#estrazione-pattern) · [setup-progetto-dev](#setup-progetto-dev) · [brainstorming-post-sviluppo](#brainstorming-post-sviluppo) · [crea-task-notion](#crea-task-notion) · [db-transfer](#db-transfer) · [gestione-issue](#gestione-issue) · [AWS Diagnostics](#aws-diagnostics-pacchetto)
- **Maintenance**: [audit-periodico](#audit-periodico) · [sistema-riunioni-notion](#sistema-riunioni-notion)
- **Meta**: [gestione-kb](#gestione-kb) · [verifica-pre-commit](#verifica-pre-commit)
- [Confronto skill manutenzione](#differenze-tra-skill-di-manutenzione)
- [Formato SKILL.md](#formato-standard-skillmd)

---

## Mappa globale skill

```mermaid
flowchart LR
    subgraph PRESALES["Presales"]
        IP[init-project]
        ER[estrazione-requisiti]
        GAT[genera-allegato-tecnico]
        GMB[genera-mockup-brief]
        IP --> ER
        ER --> GAT
        ER --> GMB
    end

    subgraph DEV["Development"]
        FW[feature-workflow]
        FPL[feature-plan]
        FDV[feature-develop]
        FTS[feature-test]
        FRV[feature-review]
        ED[estrazione-decisioni]
        EP[estrazione-pattern]
        SPD[setup-progetto-dev]
        BPS[brainstorming-post-sviluppo]
        AWS[aws-diagnostics]
        SPD -.->|verifica ambiente| FW
        WF[windsurf-feedback]
        FW --> FPL --> FDV
        FDV -->|Windsurf| WF
        FDV --> FTS & FRV
        WF -.->|pattern| EP
        WF -.->|decisioni| ED
        FW -.->|decisioni| ED
        FW -.->|pattern| EP
        FRV -.->|fine sessione| BPS
        CTN[crea-task-notion]
        DBT[db-transfer]
        GI[gestione-issue]
    end

    subgraph MAINT["Maintenance"]
        AP[audit-periodico]
    end

    subgraph META["Meta — autonome"]
        GKB[gestione-kb]
        VPC[verifica-pre-commit]
    end

    PRESALES -->|contratto firmato| DEV
    DEV -->|go-live| MAINT
    MAINT -.->|nuovo progetto simile| PRESALES

    VPC -.->|verifica coerenza KB| PRESALES
    VPC -.->|verifica coerenza KB| DEV
    VPC -.->|verifica coerenza KB| MAINT
    AP -.->|audita| PRESALES
    AP -.->|audita| DEV
    GKB -.->|gestisce meta-file| META
```

> Per i flussi temporali e le sequenze d'uso → [docs/workflow.md](workflow.md)

---

## Ciclo di vita delle skill

Ogni skill ha un campo `stato` nel frontmatter:

| Stato | Significato | Comportamento |
|-------|-------------|---------------|
| `beta` | Skill in fase di rodaggio | All'inizio avvisa che è in beta. Durante l'uso, ad ogni step chiede se il processo ha senso o se va modificato. |
| `stable` | Skill validata e collaudata | Esecuzione normale senza interruzioni extra. |

### Criteri di graduazione beta → stable

Una skill può essere promossa a `stable` quando soddisfa **tutti** i seguenti criteri:

1. **Uso cross-progetto**: usata su almeno 2 progetti diversi **OPPURE** 5+ invocazioni totali sullo stesso
2. **Stabilità processo**: nessuna modifica al processo conversazionale nelle ultime 3 sessioni d'uso
3. **Loop validato**: il loop conversazionale non ha generato feedback negativi nelle ultime esecuzioni

La promozione va registrata nel changelog e il campo `stato` aggiornato nel frontmatter del SKILL.md.

### Skill attualmente stable

- `verifica-pre-commit` — v3.0, usata ad ogni commit
- `estrazione-requisiti` — v1.1, usata su 2 progetti (jubatus, lamonea)
- `estrazione-decisioni` — v1.1, usata su jubatus con 5 ADR
- `estrazione-pattern` — v1.2, usata su jubatus con 5 pattern estratti

---

## Riepilogo

| Skill | Fase | Stato | Nativa | Scopo | Legge | Scrive |
|-------|------|-------|--------|-------|-------|--------|
| `init-project` | Presales | beta | si | Bootstrap completo progetto | Notion, GitHub | projects/[nome]/, INDEX.md |
| `estrazione-requisiti` | Presales | stable | si | Note → requisiti strutturati | Materiale grezzo | requisiti.md, meeting/ |
| `genera-allegato-tecnico` | Presales | beta | si | Requisiti → allegato contrattuale | requisiti.md | allegato-tecnico.md |
| `genera-mockup-brief` | Presales | beta | si | Requisiti → brief mockup per Windsurf | requisiti.md | mockup-brief.md |
| `feature-workflow` | Development | beta | si | Orchestra ciclo completo feature (Plan→Dev→Test→Review) | requisiti.md, .feature-state.md | .feature-state.md, feature-log.md |
| `feature-plan` | Development | beta | — | Requisito → piano implementazione tecnico | requisiti.md, architettura.md, patterns/ | .feature-state.md (Piano) |
| `feature-develop` | Development | beta | — | Piano → implementazione (Claude Code o brief Windsurf) | .feature-state.md (Piano), processi.md | Codebase, .feature-state.md (Sviluppo) |
| `feature-test` | Development | beta | — | Scrive test, esegue suite, verifica criteri e regressioni | .feature-state.md, requisiti.md, codebase | Nuovi test, .feature-state.md (Test) |
| `feature-review` | Development | beta | — | Review codice: pattern LAIF, duplicazioni, qualità, KB | .feature-state.md, processi.md, patterns/ | .feature-state.md (Review) |
| `windsurf-feedback` | Development | beta | si | Processa report feedback Windsurf → KB enrichment | windsurf-briefs/report, .feature-state.md | decisioni.md, patterns/, problemi-tecnici/ |
| `estrazione-decisioni` | Development | stable | si | Documenta decisioni tecniche (ADR) | decisioni.md | decisioni.md, architettura.md |
| `estrazione-pattern` | Development | stable | si | Fine sprint → pattern riutilizzabili | feature-log, decisioni.md | patterns/, knowledge/ |
| `setup-progetto-dev` | Development | beta | si | Verifica ambiente dev locale | architettura.md, MEMORY.md, stack.md | nessuno (solo report) |
| `brainstorming-post-sviluppo` | Development | beta | si | Fine sessione → estrae miglioramenti | Lavoro svolto nella sessione | patterns/, skills/, IDEAS.md |
| `crea-task-notion` | Development | beta | si | KB + Notion → task strutturati su Notion | projects/[nome]/, pagine Notion, Feature DB | Notion Task DB, Notion Feature DB |
| `aws-triage` | Development | beta | si | Health check rapido tutti i servizi AWS | aws-config.yaml | nessuno (diagnosi) |
| `aws-ecs-diagnose` | Development | beta | si | Deep-dive ECS (deployment, task, capacity, config) | aws-config.yaml | nessuno (diagnosi) |
| `aws-logs-diagnose` | Development | beta | si | Query CloudWatch Logs Insights (6 template + custom) | aws-config.yaml | nessuno (diagnosi) |
| `aws-rds-diagnose` | Development | beta | si | Stato RDS, connessioni, log PostgreSQL, parametri | aws-config.yaml | nessuno (diagnosi) |
| `aws-s3-diagnose` | Development | beta | si | Inventario bucket S3, dimensioni, upload recenti | aws-config.yaml | nessuno (diagnosi) |
| `aws-health-report` | Development | beta | si | Report HTML interattivo salute infrastruttura AWS | aws-config.yaml | reports/aws-report-*.html |
| `db-transfer` | Development | beta | si | Trasferimento dati tra DB PostgreSQL con verifica schema | aws-config.yaml, .env | nessuno (opera sui DB) |
| `gestione-issue` | Development | beta | si | Gestione interattiva issue via Notion MCP (triage, riunione, release, health check) | projects/laif-issue/, Notion DB | Notion DB (dopo conferma) |
| `audit-periodico` | Maintenance | beta | si | Audit mensile intera KB | Tutta la KB | Report + aggiornamenti distribuiti |
| `sistema-riunioni-notion` | Maintenance | beta | si | Pulizia tabella Notion "Riunioni Private" (icone, Tag, Progetto, Partecipanti, titoli) | Notion DB Riunioni Private, DB Progetti, utenti workspace | Notion DB Riunioni Private (dopo conferma) |
| `gestione-kb` | Meta | beta | si | Gestione meta-file del sistema | Meta-file, struttura cartelle | changelog, IDEAS.md, docs/ |
| `verifica-pre-commit` | Meta | stable | — | Verifica ibrida coerenza KB pre-commit (script Python + check semantici) | Tutti i meta-file + struttura reale | nessuno (solo report) |

---

## Presales

### init-project

**Path**: `skills/presales/init-project/SKILL.md`
**Trigger**: Inizio di un nuovo progetto
**Stato**: beta

Bootstrap completo: legge Notion, clona repo, rileva stack, popola struttura progetto, genera CLAUDE.md nel repo.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Nome progetto?]
    Q1 --> Q2[URL GitHub?]
    Q2 --> Q3[Link Notion?]
    Q3 --> Q4{Info cliente\nsufficienti da Notion?}
    Q4 -->|No| Q5[Chiede info cliente]
    Q4 -->|Sì| EXEC
    Q5 --> EXEC[Esecuzione]
    EXEC --> E1[Crea struttura cartelle]
    E1 --> E2[Legge Notion via MCP]
    E2 --> E3[Clona repo + analizza stack]
    E3 --> E4[Popola README.md]
    E4 --> E5[Genera CLAUDE.md nel repo]
    E5 --> E6[Aggiorna INDEX.md]
    E6 --> DONE([Output riepilogo])
```

---

### estrazione-requisiti

**Path**: `skills/presales/estrazione-requisiti/SKILL.md`
**Trigger**: Dopo un meeting con il cliente
**Stato**: stable

Note grezze di meeting → requisiti strutturati (RF + RNF) con priorità, criteri di accettazione, domande aperte.

```mermaid
flowchart TD
    START([Invocazione]) --> P1[Fase 1: Orientamento]
    P1 --> Q1[Chi ha partecipato?]
    Q1 --> Q2[Contesto business?]
    Q2 --> Q3[Progetto già esistente?]
    Q3 --> P2[Fase 2: Chiarimento requisiti]
    P2 --> LOOP{Ambiguità\nresidue?}
    LOOP -->|Sì| QN[Domanda specifica]
    QN --> LOOP
    LOOP -->|No| P3[Fase 3: Conferma]
    P3 --> LIST[Mostra RF + RNF + domande aperte]
    LIST --> CONFIRM{Confermato?}
    CONFIRM -->|No| P2
    CONFIRM -->|Sì| WRITE[Scrive requisiti.md]
    WRITE --> DONE([Output riepilogo])
```

---

### genera-allegato-tecnico

**Path**: `skills/presales/genera-allegato-tecnico/SKILL.md`
**Trigger**: Quando `requisiti.md` è validato e serve il documento contrattuale
**Stato**: beta

Produce l'allegato tecnico per il contratto: max 3 pagine, linguaggio non tecnico, comprensibile da un CEO.

```mermaid
flowchart TD
    START([Invocazione]) --> CHECK{requisiti.md\ncompleto?}
    CHECK -->|No| STOP([Prerequisito mancante])
    CHECK -->|Sì| Q1[Esclusioni sufficientemente esplicite?]
    Q1 --> Q2[Chi legge l'allegato? Livello formalità]
    Q2 --> PROP[Propone struttura allegato]
    PROP --> CONFIRM{Approvata?}
    CONFIRM -->|No| PROP
    CONFIRM -->|Sì| WRITE[Scrive allegato-tecnico.md]
    WRITE --> DONE([Output riepilogo])
```

---

### genera-mockup-brief

**Path**: `skills/presales/genera-mockup-brief/SKILL.md`
**Trigger**: Quando `requisiti.md` è validato e servono i mockup
**Stato**: beta

Produce il brief per i mockup destinato a Windsurf: schermate prioritarie, flussi, brand guidelines, vincoli UI.

```mermaid
flowchart TD
    START([Invocazione]) --> CHECK{requisiti.md\ncompleto?}
    CHECK -->|No| STOP([Prerequisito mancante])
    CHECK -->|Sì| Q1[Top 3-5 schermate prioritarie?]
    Q1 --> Q2[Brand guidelines?]
    Q2 --> Q3[Dispositivi prioritari?]
    Q3 --> Q4[Vincoli UI?]
    Q4 --> WRITE[Scrive mockup-brief.md]
    WRITE --> DONE([Output riepilogo])
```

---

## Development

### feature-workflow

**Path**: `skills/development/feature-workflow/SKILL.md`
**Trigger**: Sviluppo feature end-to-end
**Stato**: beta

Orchestra il ciclo completo: Plan → Develop → Test + Review → Exit. Coordina 4 sub-skill con gate di qualità. Può essere ripreso da una fase precedente.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Quale progetto?]
    Q1 --> Q2[Quale requisito RF-XX?]
    Q2 --> Q3{.feature-state.md\nesiste?}
    Q3 -->|Sì| RESUME[Riprendi da fase corrente]
    Q3 -->|No| PLAN

    PLAN[Fase 1: feature-plan] --> G1{GATE 1\nPiano approvato?}
    G1 -->|No| PLAN
    G1 -->|Sì| DEV[Fase 2: feature-develop]
    DEV --> G2{GATE 2\nSviluppo completo?}
    G2 -->|No| DEV
    G2 -->|Sì| PAR

    PAR[Fase 3: Test + Review] --> TEST[feature-test]
    PAR --> REV[feature-review]
    TEST & REV --> G3{GATE 3\nTutti PASS?}
    G3 -->|No| FIX[Fix list → Develop]
    FIX --> DEV
    G3 -->|Sì| EXIT[Exit: feature-log + commit]
    EXIT --> DONE([Output riepilogo])

    RESUME --> G1
```

---

### feature-plan

**Path**: `skills/development/feature-plan/SKILL.md`
**Trigger**: Prima di sviluppare una feature
**Stato**: beta

Analizza un requisito e produce un piano tecnico: task list, file coinvolti, dipendenze, criteri di accettazione, rischi, pattern da applicare.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Qual è il requisito?]
    Q1 --> Q2[Vincoli tecnici noti?]
    Q2 --> Q3[Pattern esistenti da riutilizzare?]
    Q3 --> Q4[Backend / frontend / fullstack?]
    Q4 --> Q5[Complessità percepita?]
    Q5 --> READ[Legge requisiti + architettura + processi + patterns]
    READ --> PLAN[Produce piano tecnico]
    PLAN --> CONFIRM{Approvato?}
    CONFIRM -->|No| PLAN
    CONFIRM -->|Sì| WRITE[Scrive .feature-state.md]
    WRITE --> DONE([Output riepilogo])
```

---

### feature-develop

**Path**: `skills/development/feature-develop/SKILL.md`
**Trigger**: Piano approvato (GATE 1 passato)
**Stato**: beta

Implementa la feature dal piano. Due modalità: sviluppo diretto (Claude Code) o brief autocontenuto per Windsurf.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1{Claude Code\no Windsurf?}
    Q1 -->|Claude Code| CC[Legge piano]
    Q1 -->|Windsurf| WS[Legge piano]

    CC --> LOOP{Per ogni task}
    LOOP --> IMPL[Implementa task]
    IMPL --> CHECK[Verifica compila]
    CHECK --> LOOP
    LOOP -->|Tutti completati| UPDATE[Aggiorna .feature-state.md]

    WS --> BRIEF[Genera brief autocontenuto]
    BRIEF --> SHOW[Mostra brief all'utente]
    SHOW --> UPDATE

    UPDATE --> DONE([Output riepilogo])
```

---

### feature-test

**Path**: `skills/development/feature-test/SKILL.md`
**Trigger**: Sviluppo completato (GATE 2 passato)
**Stato**: beta

Test completo: scrive test mancanti, esegue suite, verifica criteri di accettazione, testa edge case, controlla regressioni.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Edge case specifici?]
    Q1 --> Q2[Test suite esistente?]
    Q2 --> READ[Legge criteri + file modificati]
    READ --> WRITE[Scrive nuovi test]
    WRITE --> RUN[Esegue suite completa]
    RUN --> VERIFY[Verifica criteri di accettazione]
    VERIFY --> REGR[Controlla regressioni]
    REGR --> REPORT{Tutti PASS?}
    REPORT -->|Sì| PASS([PASS])
    REPORT -->|No| FAIL([FAIL + lista problemi])
```

---

### feature-review

**Path**: `skills/development/feature-review/SKILL.md`
**Trigger**: Sviluppo completato (GATE 2 passato)
**Stato**: beta

Review autonoma: check aderenza pattern LAIF, duplicazioni, qualità, sicurezza. Confronta con `patterns/` e suggerisce nuovi pattern estraibili.

```mermaid
flowchart TD
    START([Invocazione autonoma]) --> READ[Legge file modificati]
    READ --> C1[Check 1: Pattern LAIF]
    C1 --> C2[Check 2: Duplicazioni]
    C2 --> C3[Check 3: Qualità + sicurezza]
    C3 --> C4[Check 4: Confronto con KB patterns/]
    C4 --> CLASS{Issue critiche?}
    CLASS -->|Sì| FAIL([FAIL + fix list])
    CLASS -->|No| PASS([PASS + suggerimenti])
```

---

### windsurf-feedback

**Path**: `skills/development/windsurf-feedback/SKILL.md`
**Trigger**: Dopo che Windsurf ha completato lo sviluppo e l'utente fornisce il report
**Stato**: beta

Processa il report strutturato di Windsurf. Estrae difficolta ricorrenti, decisioni, pattern e li smista nella KB.

```mermaid
flowchart TD
    START([Report Windsurf]) --> PARSE[Parse sezioni report]
    PARSE --> DIFF[Difficolta ricorrenti?]
    PARSE --> DEC[Decisioni non banali?]
    PARSE --> PAT[Pattern riutilizzabili?]
    PARSE --> QA[Domande aperte?]

    DIFF -->|Si| D_PROP[Proponi salvataggio\nproblemi-tecnici/]
    DEC -->|Si| DEC_PROP[Proponi ADR\ndecisioni.md]
    PAT -->|Si| PAT_CHECK{Esiste gia\nin patterns/?}
    PAT_CHECK -->|No| PAT_PROP[Proponi estrazione\npatterns/]
    PAT_CHECK -->|Si| PAT_UPD[Aggiorna esempi reali]
    QA -->|Si| QA_USER[Mostra all'utente]

    D_PROP --> UPDATE[Aggiorna .feature-state.md]
    DEC_PROP --> UPDATE
    PAT_PROP --> UPDATE
    PAT_UPD --> UPDATE
    QA_USER --> UPDATE
    UPDATE --> DONE([Output riepilogo KB arricchita])
```

---

### estrazione-decisioni

**Path**: `skills/development/estrazione-decisioni/SKILL.md`
**Trigger**: Dopo ogni decisione tecnica non banale
**Stato**: stable

Cattura decisioni architetturali in formato ADR. Solo per scelte che qualcuno potrebbe mettere in discussione.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Cosa è stato deciso?]
    Q1 --> Q2[Perché era necessario decidere?]
    Q2 --> Q3[Alternative valutate?]
    Q3 --> Q4[Perché questa opzione?]
    Q4 --> Q5[Trade-off accettati?]
    Q5 --> Q6{Impatto su\narchitettura?}
    Q6 --> Q7[Reversibile?]
    Q7 --> WRITE[Scrive ADR in decisioni.md]
    Q6 -->|Sì| UPDATE[Aggiorna architettura.md]
    WRITE --> DONE([Output riepilogo])
    UPDATE --> DONE
```

---

### estrazione-pattern

**Path**: `skills/development/estrazione-pattern/SKILL.md`
**Trigger**: Fine sprint o fine progetto
**Stato**: stable

Analizza UN progetto specifico ed estrae pattern riutilizzabili in `patterns/` e knowledge in `knowledge/`. Non è un audit generale (per quello c'è `audit-periodico`).

```mermaid
flowchart TD
    START([Invocazione]) --> P1[Fase 1: Raccolta]
    P1 --> Q1[Problemi risolti che ricorreranno?]
    Q1 --> Q2[Pattern usati da altri progetti?]
    Q2 --> P2[Fase 2: Valutazione candidati]
    P2 --> EVAL{Per ogni candidato}
    EVAL --> C1{Generico\ncross-progetto?}
    C1 -->|Sì| PAT[→ patterns/]
    C1 -->|No| C2{Specifico\ndi settore?}
    C2 -->|Sì| KNOW[→ knowledge/industrie/]
    C2 -->|No| SKIP[Scarta]
    PAT --> P3
    KNOW --> P3
    SKIP --> P3[Fase 3: Conferma lista]
    P3 --> CONFIRM{Approvato?}
    CONFIRM -->|Sì| EXEC[Crea/aggiorna file]
    CONFIRM -->|No| P2
    EXEC --> DONE([Output riepilogo])
```

---

### setup-progetto-dev

**Path**: `skills/development/setup-progetto-dev/SKILL.md`
**Trigger**: Inizio sessione di sviluppo o dopo onboarding
**Stato**: beta

Verifica che l'ambiente di sviluppo locale sia operativo: Docker, connettività servizi, autenticazione, migrazioni DB.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Quale progetto?]
    Q1 --> Q2[Conferma servizi da verificare]
    Q2 --> S1[Consulta KB progetto]
    S1 --> S2[Verifica Docker]
    S2 --> S3[Verifica connettività servizi]
    S3 --> S4[Verifica autenticazione]
    S4 --> S5[Verifica migrazioni DB]
    S5 --> REPORT([Riepilogo stato ambiente])
```

---

### brainstorming-post-sviluppo

**Path**: `skills/development/brainstorming-post-sviluppo/SKILL.md`
**Trigger**: Fine sessione di sviluppo
**Stato**: beta

Analizza il lavoro svolto nella sessione per estrarre pattern, skill, idee e miglioramenti per SimoneAI. Propone asset concreti da creare o aggiornare.

```mermaid
flowchart TD
    START([Fine sessione]) --> A1[Analizza lavoro svolto]
    A1 --> A2[Identifica pattern tecnici]
    A2 --> A3[Identifica skill/workflow mancanti]
    A3 --> A4[Identifica idee di miglioramento]
    A4 --> PROP[Propone lista asset]
    PROP --> CONFIRM{Approvato?}
    CONFIRM -->|Sì| EXEC[Crea/aggiorna asset]
    CONFIRM -->|Parziale| SELECT[Seleziona quali sviluppare]
    SELECT --> EXEC
    EXEC --> DONE([Output riepilogo])
```

---

### crea-task-notion

**Path**: `skills/development/crea-task-notion/SKILL.md`
**Trigger**: L'utente vuole creare task Notion per un progetto
**Stato**: beta

Genera task Notion strutturati usando KB del progetto e pagine Notion ad-hoc come contesto. Raggruppa i task sotto Feature esistenti o nuove. Tutto interattivo in chat prima di creare qualsiasi cosa su Notion.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Quale progetto?]
    Q1 --> KB[Legge KB: README + requisiti + stato + feature-log]
    KB --> FETCH[Fetch proattivo Notion: Progetti / Note / Riunioni Private]
    FETCH --> Q2[Quali pagine includere come contesto?]
    Q2 --> READ[Legge pagine selezionate via MCP]
    READ --> Q3[Su cosa vuoi concentrarti?]
    Q3 --> FEAT[Legge Feature DB + propone raggruppamento]
    FEAT --> CONFIRM_FEAT{Raggruppamento ok?}
    CONFIRM_FEAT -->|No| FEAT
    CONFIRM_FEAT -->|Sì| PROP[Propone bozza task in chat]
    PROP --> EDIT{Modifiche?}
    EDIT -->|Sì| PROP
    EDIT -->|ok| CONFIRM[Conferma finale: N task + M Feature]
    CONFIRM -->|Sì| CREATE[Crea Feature nuove + Task su Notion]
    CREATE --> DONE([Riepilogo completamento])
    CONFIRM -->|No| PROP
```

---

### db-transfer

**Path**: `skills/development/db-transfer/SKILL.md`
**Trigger**: L'utente vuole copiare/sincronizzare dati tra database PostgreSQL
**Stato**: beta

Trasferimento dati tra database PostgreSQL con verifica schema preventiva, selezione tabelle interattiva e ordinamento automatico per foreign key. Supporta AWS Secrets Manager, URL diretti e file .env. Include script standalone (`transfer_data.py` + `compare_schemas.py`).

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Source e Destination?]
    Q1 --> RESOLVE[Risolvi credenziali: ARN / URL / .env]
    RESOLVE --> COMPARE[compare_schemas.py — confronto schema]
    COMPARE --> DIFF{Discrepanze?}
    DIFF -->|Sì| WARN[Mostra diff, chiedi conferma]
    DIFF -->|No| OK[Schema allineati]
    WARN --> Q2
    OK --> Q2[Mostra tabelle con row count + size]
    Q2 --> SELECT[Selezione tabelle con wildcard]
    SELECT --> PLAN[Mostra piano: ordine FK, truncate, stima]
    PLAN --> CONFIRM{Conferma?}
    CONFIRM -->|No| SELECT
    CONFIRM -->|Sì| EXEC[transfer_data.py — esecuzione]
    EXEC --> VERIFY[Verifica post-trasferimento: row count]
    VERIFY --> DONE([Riepilogo])
```

---

### gestione-issue

**Path**: `skills/development/gestione-issue/SKILL.md`
**Trigger**: Riunione stack interno, triage issue, pianificazione release, health check backlog
**Stato**: beta

Gestione interattiva delle issue dello stack interno LAIF via Notion MCP. Legge DB Issues e Release, guida l'utente in triage, preparazione riunione, pianificazione release e health check backlog. Scrive su Notion solo dopo approvazione esplicita.

```mermaid
flowchart TD
    START([Invocazione]) --> CTX[Carica contesto laif-issue/]
    CTX --> FETCH[Fetch DB Issues + Release da Notion]
    FETCH --> MENU[Cosa vuoi fare?]
    MENU -->|1| MEET[Preparare riunione — genera agenda]
    MENU -->|2| TRIAGE[Triage issue nuove — revisiona una alla volta]
    MENU -->|3| RELEASE[Pianificare release — assegna issue]
    MENU -->|4| HEALTH[Health check — issue stale, RICE mancante]
    MENU -->|5| STATUS[Stato release specifica]
    MENU -->|6| OTHER[Altro]
    MEET --> CONFIRM{Conferma scritture?}
    TRIAGE --> CONFIRM
    RELEASE --> CONFIRM
    HEALTH --> CONFIRM
    CONFIRM -->|Sì| WRITE[Scrivi su Notion]
    CONFIRM -->|No| MENU
    WRITE --> DONE([Riepilogo + Vuoi fare altro?])
    DONE --> MENU
```

---

### AWS Diagnostics (pacchetto)

**Path**: `skills/development/aws-diagnostics/`
**Trigger**: Debug ambienti AWS, troubleshooting servizi
**Stato**: beta (tutte le skill)

Pacchetto di 5 skill diagnostiche read-only per ambienti AWS LAIF. Ogni skill ha un `SKILL.md` + `run.py` eseguibile. Libreria Python condivisa in `_shared/`.

```mermaid
flowchart TD
    START([Problema AWS]) --> Q1{Sai quale\nservizio?}
    Q1 -->|No| TRIAGE[aws-triage]
    Q1 -->|Sì| Q2{Quale?}

    TRIAGE --> R{Risultato}
    R -->|ECS| ECS[aws-ecs-diagnose]
    R -->|Logs| LOGS[aws-logs-diagnose]
    R -->|RDS| RDS[aws-rds-diagnose]
    R -->|S3| S3[aws-s3-diagnose]

    Q2 -->|ECS| ECS
    Q2 -->|Logs| LOGS
    Q2 -->|Database| RDS
    Q2 -->|Storage| S3
```

| Skill | Scopo | Script |
|-------|-------|--------|
| `aws-triage` | Health check rapido (ECS + RDS + Logs + S3) | `run.py --project X --env dev` |
| `aws-ecs-diagnose` | Deployment, task failure, capacity, config | `run.py --project X --env dev --mode all` |
| `aws-logs-diagnose` | Query Logs Insights (6 template + custom) | `run.py --project X --env dev --query-type errors` |
| `aws-rds-diagnose` | Stato, connessioni, log PostgreSQL, parametri | `run.py --project X --env dev --mode status` |
| `aws-s3-diagnose` | Dimensioni, upload recenti, file grandi | `run.py --project X --env dev --bucket all` |

---

## Maintenance

### audit-periodico

**Path**: `skills/maintenance/audit-periodico/SKILL.md`
**Trigger**: Fine mese o fine sprint
**Stato**: beta

Audit autonomo dell'intera KB: verifica progetti, pattern, tag, domande aperte scadute, debito tecnico. Non opera su un singolo progetto (per quello c'è `estrazione-pattern`). Non gestisce meta-file (per quello c'è `gestione-kb`).

```mermaid
flowchart TD
    START([Esecuzione autonoma]) --> S1[Step 1: Inventario progetti]
    S1 --> CLASS[Classifica: Aggiorna/Archivia/Recupera/OK]
    CLASS --> S2[Step 2: Verifica pattern]
    S2 --> S3[Step 3: Allineamento tag]
    S3 --> S4[Step 4: Domande aperte scadute]
    S4 --> S5[Step 5: Debito tecnico aggregato]
    S5 --> REPORT[Genera report manutenzione]
    REPORT --> PROPOSE[Propone azioni]
    PROPOSE --> CONFIRM{Approvato?}
    CONFIRM -->|Sì| EXEC[Esegue aggiornamenti]
    CONFIRM -->|No| ADJUST[Rivedi azioni]
    ADJUST --> CONFIRM
    EXEC --> DONE([Output report finale])
```

---

### sistema-riunioni-notion

**Path**: `skills/maintenance/sistema-riunioni-notion/SKILL.md`
**Trigger**: "sistema le call", "fixa la tabella delle riunioni", o passata mensile di manutenzione
**Stato**: beta

Pulizia della tabella Notion "Riunioni Private": applica icone coerenti al Tag, inferisce Tag/Progetto/Partecipanti dal titolo e dal riassunto, riscrive titoli placeholder ("‣", vuoti, "@date..."). Contiene mapping emoji stabile, mappa utenti Notion, mappa progetti con ID noti e regole di inferenza con errori ricorrenti documentati.

Regole non derogabili:
- **Simone Brigante** non va mai nei Partecipanti Interni (è dato per scontato).
- Mai sovrascrivere valori già popolati.
- Su ogni ambiguità: `AskUserQuestion` con data della riunione + argomenti principali.
- Nessun cambio massivo (>10 pagine) senza approvazione del mapping.

```mermaid
flowchart TD
    START([Richiesta utente]) --> SCOPE[Scope: ultime N settimane / tutto]
    SCOPE --> FETCH[Query DB + fetch utenti]
    FETCH --> DIAG[Diagnostico via subagent]
    DIAG --> INFER[Piano update JSON]
    INFER --> ASK{Ambiguità?}
    ASK -->|Sì| AUQ[AskUserQuestion data+argomenti]
    AUQ --> BATCH
    ASK -->|No| BATCH[Batch update parallelo]
    BATCH --> TITLES{Riscrivo titoli placeholder?}
    TITLES -->|Sì| GENTITLES[Subagent genera titoli da Riassunto]
    GENTITLES --> APPLYTITLES[Applica Name update]
    TITLES -->|No| DONE
    APPLYTITLES --> DONE([Report finale])
```

---

## Meta

### gestione-kb

**Path**: `skills/meta/gestione-kb/SKILL.md`
**Trigger**: Dopo modifiche alla KB, nuove idee, o periodicamente
**Stato**: beta

Gestisce i meta-file del sistema (changelog, idee, documentazione). Non audita progetti o pattern (per quello c'è `audit-periodico`). Opera in 4 modalità.

```mermaid
flowchart TD
    START([Invocazione]) --> MODE{Modalità?}
    MODE -->|1| REG[Registra modifica]
    MODE -->|2| IDEA[Aggiungi idea]
    MODE -->|3| SYNC[Sync documentazione]
    MODE -->|4| REV[Review idee]

    REG --> RQ1[Cosa è cambiato?]
    RQ1 --> RQ2{Struttura\no contenuto?}
    RQ2 -->|Struttura| CL_S[Aggiorna CHANGELOG.md ### Struttura]
    RQ2 -->|Contenuto| CL_C[Aggiorna CHANGELOG.md ### Contenuti]
    CL_S --> RQ3{Impatta docs/?}
    RQ3 -->|Sì| UPD_DOC[Aggiorna docs/]
    RQ3 -->|No| DONE_R([Fatto])
    UPD_DOC --> DONE_R
    CL_C --> DONE_R

    IDEA --> IQ1[Descrivi l'idea]
    IQ1 --> IQ2[Categoria? Effort?]
    IQ2 --> ADD[Aggiunge a IDEAS.md]
    ADD --> DONE_I([Fatto])

    SYNC --> READ[Legge struttura reale]
    READ --> DIFF[Confronta con docs/]
    DIFF --> PROP{Differenze?}
    PROP -->|Sì| FIX[Aggiorna docs/]
    PROP -->|No| OK([Tutto allineato])
    FIX --> OK

    REV --> LIST[Mostra idee pendenti]
    LIST --> DEC[Per ciascuna: implementare/rimandare/scartare]
    DEC --> UPD_ID[Aggiorna IDEAS.md]
    UPD_ID --> DONE_V([Fatto])
```

---

### verifica-pre-commit

**Path**: `skills/meta/verifica-pre-commit/SKILL.md`
**Trigger**: Automatico — dopo ogni modifica a file KB, prima di ogni `git commit`
**Stato**: stable

Verifica ibrida: 4 check automatizzati (script Python) + check semantici (parent agent). Il commit è bloccato finché tutti i check non passano.

```mermaid
flowchart TD
    START([Invocazione pre-commit]) --> SCRIPT[Esegue run_all.py]
    SCRIPT --> PAR{Check paralleli}

    PAR --> C1[Check 1\nCoerenza referenze\ncross-file]
    PAR --> C2[Check 2\nChangelog\naggiornato]
    PAR --> C3[Check 3\nIDEAS.md\nstato]
    PAR --> C4[Check 4\nTag\nfrontmatter]
    PAR --> C5[Check 5\nStruttura\nvs docs]

    C1 & C2 & C3 & C4 & C5 --> MERGE[Aggrega risultati]
    MERGE --> RESULT{Tutti PASS?}
    RESULT -->|Sì| PASS([PASS — commit autorizzato])
    RESULT -->|No| FAIL([FAIL — lista issue al parent agent])
```

---

## Dipendenze tra skill

```mermaid
flowchart TD
    subgraph PRESALES["Presales (sequenziali)"]
        IP[init-project] -->|produce meeting/| ER[estrazione-requisiti]
        ER -->|produce requisiti.md| GAT[genera-allegato-tecnico]
        ER -->|produce requisiti.md| GMB[genera-mockup-brief]
    end

    subgraph DEV["Development"]
        SPD[setup-progetto-dev] -.->|verifica ambiente| FW[feature-workflow]
        FW -->|orchestra| FPL[feature-plan]
        FPL -->|piano| FDV[feature-develop]
        FDV -->|Windsurf report| WFB[windsurf-feedback]
        FDV -->|codice| FTS[feature-test]
        FDV -->|codice| FRV[feature-review]
        WFB -.->|decisioni| ED[estrazione-decisioni]
        WFB -.->|pattern| EP[estrazione-pattern]
        FW -.->|decisioni emerse| ED
        FRV -.->|pattern individuati| EP
        EP -.->|fine sessione| BPS[brainstorming-post-sviluppo]
    end

    subgraph MAINT["Maintenance"]
        AP[audit-periodico]
        AP -.->|analizza| EP
    end

    subgraph META["Meta"]
        GKB[gestione-kb]
        VPC[verifica-pre-commit]
        CTP[contesto-progetto]
        CTP -.->|suggerisce| FW
    end

    PRESALES -->|contratto firmato| DEV
    DEV -->|go-live| MAINT

    style ER fill:#90EE90
    style ED fill:#90EE90
    style EP fill:#90EE90
    style VPC fill:#90EE90
```

> Verde = skill stable. Bianche = skill beta.

---

## Quando NON usare una skill (disambiguazione)

| Vuoi... | NON usare | Usa invece | Motivo |
|---------|-----------|-----------|--------|
| Estrarre pattern a fine sprint da un progetto | `brainstorming-post-sviluppo` | `estrazione-pattern` | brainstorming analizza la sessione corrente, non il progetto intero |
| Analizzare cosa è emerso nella sessione di oggi | `estrazione-pattern` | `brainstorming-post-sviluppo` | estrazione-pattern opera su feature-log/decisioni, non sulla sessione |
| Sviluppare una feature end-to-end | sub-skill singole (plan, develop, test, review) | `feature-workflow` | il workflow orchestra le fasi con gate di qualità |
| Processare il report di Windsurf | skill manuali | `windsurf-feedback` | smista feedback nella KB automaticamente |
| Solo pianificare senza sviluppare | `feature-workflow` | `feature-plan` standalone | il workflow forza il ciclo completo |
| Fare audit di tutta la KB | `estrazione-pattern` | `audit-periodico` | estrazione-pattern opera su UN progetto, non sull'intera KB |
| Registrare una modifica nel changelog | `audit-periodico` | `gestione-kb` (mod. 1) | audit è per review periodiche, non per singole registrazioni |
| Cercare contesto su un progetto prima di lavorarci | skill manuali | `contesto-progetto/match.py` | script deterministico, zero token |

---

## Differenze tra skill di manutenzione

| | `estrazione-pattern` | `audit-periodico` | `gestione-kb` | `verifica-pre-commit` |
|---|---|---|---|---|
| **Scope** | Un singolo progetto | Intera KB | Meta-file del sistema | Coerenza interna KB |
| **Quando** | Fine sprint/progetto | Fine mese | Dopo ogni modifica / periodicamente | Automatico — ad ogni modifica e pre-commit |
| **Legge** | feature-log, decisioni-tecniche di un progetto | Tutti i progetti, pattern, tag | Changelog, IDEAS.md, docs/ | Tutti i meta-file + struttura reale |
| **Scrive** | patterns/, knowledge/ | Report + aggiornamenti distribuiti | Changelog, IDEAS.md, docs/ | Niente — solo report |
| **Conversazione** | Sì | Sì (con conferma) | Sì (4 modalità) | No — autonoma |
| **Focus** | Estrarre knowledge riutilizzabile | Trovare gap, obsolescenze, disallineamenti | Tenere traccia modifiche e idee | Bloccare commit inconsistenti |

---

## Formato standard SKILL.md

Ogni skill segue questo formato nel frontmatter:

```yaml
---
nome: "Nome della skill"
descrizione: >
  Descrizione con scope chiaro: cosa fa, cosa NON fa, e rimandi ad altre skill.
fase: presales | development | maintenance | meta
versione: "1.0"
stato: beta | stable
depends-on: []           # skill che devono essere eseguite prima (opzionale)
enables: []              # skill che questa abilita (opzionale)
legge:
  - file/cartelle che la skill legge come input
scrive:
  - file/cartelle che la skill produce o aggiorna
aggiornato: "YYYY-MM-DD"
---
```

Sezioni nel corpo:
1. **Obiettivo** — cosa fa
2. **Perimetro** — cosa fa / cosa NON fa / rimandi ad altre skill
3. **Quando usarla / Trigger** — quando invocarla
4. **Prerequisiti** — cosa serve prima
5. **Loop conversazionale** — domande da fare (una alla volta)
6. **Processo di produzione** — passi da eseguire
7. **Output in chat** — riepilogo obbligatorio al termine
8. **Checklist qualità** — verifiche finali

**Principio**: mai produrre output senza prima raccogliere le informazioni necessarie.
