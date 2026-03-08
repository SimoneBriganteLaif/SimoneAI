# Catalogo Skill

**Ultimo aggiornamento**: 2026-03-08

---

## Riepilogo

| Skill | Fase | Scopo | Input | Output |
|-------|------|-------|-------|--------|
| `init-project` | Presales | Bootstrap completo progetto | Nome, GitHub URL, Notion links | Struttura KB + CLAUDE.md repo |
| `estrazione-requisiti` | Presales | Note grezze → requisiti strutturati | Trascrizioni meeting | `requisiti.md` |
| `genera-documenti` | Presales | Requisiti → documenti cliente | `requisiti.md` validato | Allegato tecnico + brief mockup |
| `estrazione-decisioni` | Development | Documenta scelte architetturali | Descrizione decisione | ADR in `decisioni-tecniche.md` |
| `aggiornamento-kb` | Development | Estrai pattern a fine sprint | Feature log, codice | Pattern in `patterns/` |
| `aggiornamento-periodico` | Maintenance | Audit mensile KB | Nessuno (autonoma) | Report manutenzione |
| `gestione-kb` | Meta | Gestione changelog, idee, docs | Varia per modalità | Aggiornamento meta-file |

---

## Presales

### init-project

**Path**: `skills/presales/init-project/SKILL.md`
**Trigger**: Inizio di un nuovo progetto
**Versione**: 1.0

Crea l'intera struttura di un progetto in una sola operazione: legge le note da Notion, clona il repository, rileva lo stack tecnologico, e genera i file iniziali.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Chiede nome progetto]
    Q1 --> Q2[Chiede URL GitHub]
    Q2 --> Q3[Chiede link Notion]
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
**Versione**: 1.1

Trasforma note grezze di meeting in requisiti strutturati con priorità, criteri di accettazione e domande aperte.

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

### genera-documenti

**Path**: `skills/presales/genera-documenti/SKILL.md`
**Trigger**: Quando `requisiti.md` è validato
**Versione**: 1.1

Produce due documenti: l'allegato tecnico per il contratto (max 3 pagine, linguaggio non tecnico) e il brief per i mockup (schermate, flussi, brand).

```mermaid
flowchart TD
    START([Invocazione]) --> CHECK{requisiti.md\ncompleto?}
    CHECK -->|No| STOP([Prerequisito mancante])
    CHECK -->|Sì| AT[Allegato Tecnico]
    AT --> QA1[Esclusioni abbastanza esplicite?]
    QA1 --> QA2[Chi lo legge? Livello formalità]
    QA2 --> PROP_AT[Propone struttura allegato]
    PROP_AT --> WRITE_AT[Scrive allegato-tecnico.md]
    WRITE_AT --> MB[Brief Mockup]
    MB --> QB1[Top 3-5 schermate prioritarie?]
    QB1 --> QB2[Brand guidelines?]
    QB2 --> QB3[Dispositivi prioritari?]
    QB3 --> WRITE_MB[Scrive requisiti-mockup.md]
    WRITE_MB --> DONE([Output riepilogo])
```

---

## Development

### estrazione-decisioni

**Path**: `skills/development/estrazione-decisioni/SKILL.md`
**Trigger**: Dopo ogni decisione tecnica non banale
**Versione**: 1.1

Documenta decisioni architetturali in formato ADR (Architecture Decision Record). Non per decisioni ovvie, ma per scelte che qualcuno potrebbe mettere in discussione.

```mermaid
flowchart TD
    START([Invocazione]) --> Q1[Cosa è stato deciso?]
    Q1 --> Q2[Perché era necessario decidere?]
    Q2 --> Q3[Alternative valutate?]
    Q3 --> Q4[Perché questa opzione?]
    Q4 --> Q5[Trade-off accettati?]
    Q5 --> Q6{Impatto su\narchitettura?}
    Q6 -->|Sì| Q7[Reversibile?]
    Q6 -->|No| Q7
    Q7 --> WRITE[Scrive ADR in decisioni-tecniche.md]
    Q6 -->|Sì| UPDATE[Aggiorna architettura.md]
    WRITE --> DONE([Output riepilogo])
    UPDATE --> DONE
```

---

### aggiornamento-kb

**Path**: `skills/development/aggiornamento-kb/SKILL.md`
**Trigger**: Fine sprint o fine progetto
**Versione**: 1.1

Estrae pattern riutilizzabili dall'esperienza del progetto e aggiorna la knowledge base cross-progetto.

```mermaid
flowchart TD
    START([Invocazione]) --> P1[Fase 1: Raccolta]
    P1 --> Q1[Problemi risolti che ricorreranno?]
    Q1 --> Q2[Pattern usati da altri progetti LAIF?]
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

## Maintenance

### aggiornamento-periodico

**Path**: `skills/maintenance/aggiornamento-periodico/SKILL.md`
**Trigger**: Fine mese o fine sprint
**Versione**: 1.1

Sub-agente autonomo che audita l'intera KB: verifica progetti, pattern, tag, domande aperte scadute e debito tecnico.

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

## Meta

### gestione-kb

**Path**: `skills/meta/gestione-kb/SKILL.md`
**Trigger**: Dopo modifiche alla KB, nuove idee, o periodicamente
**Versione**: 1.0

Skill di gestione dei meta-file del sistema (changelog, idee, documentazione). Opera in 4 modalità: registra modifica, aggiungi idea, sync docs, review idee.

```mermaid
flowchart TD
    START([Invocazione]) --> MODE{Modalità?}
    MODE -->|1| REG[Registra modifica]
    MODE -->|2| IDEA[Aggiungi idea]
    MODE -->|3| SYNC[Sync documentazione]
    MODE -->|4| REV[Review idee]

    REG --> RQ1[Cosa è cambiato?]
    RQ1 --> RQ2{Framework\no contenuto?}
    RQ2 -->|Framework| CL_F[Aggiorna CHANGELOG-framework.md]
    RQ2 -->|Contenuto| CL_C[Aggiorna CHANGELOG-contenuti.md]
    CL_F --> RQ3{Impatta\ndocs/?}
    RQ3 -->|Sì| UPD_DOC[Aggiorna docs/ rilevanti]
    RQ3 -->|No| DONE_R([Fatto])
    UPD_DOC --> DONE_R
    CL_C --> DONE_R

    IDEA --> IQ1[Descrivi l'idea]
    IQ1 --> IQ2[Categoria? Effort?]
    IQ2 --> ADD[Aggiunge riga a IDEAS.md]
    ADD --> DONE_I([Fatto])

    SYNC --> READ[Legge struttura attuale]
    READ --> DIFF[Confronta con docs/]
    DIFF --> PROP{Differenze?}
    PROP -->|Sì| SHOW[Mostra differenze]
    SHOW --> FIX[Aggiorna docs/]
    PROP -->|No| OK([Tutto allineato])
    FIX --> OK

    REV --> LIST[Mostra idee pendenti]
    LIST --> EACH{Per ogni idea}
    EACH --> DEC[Implementare / Rimandare / Scartare]
    DEC --> UPD_ID[Aggiorna IDEAS.md]
    UPD_ID --> DONE_V([Fatto])
```

---

## Formato standard SKILL.md

Ogni skill segue questo formato:

```yaml
---
nome: "Nome della skill"
descrizione: >
  Descrizione breve usata per capire quando invocarla.
fase: presales | development | maintenance | meta
versione: "1.0"
output:
  - path/al/file/prodotto.md
aggiornato: "YYYY-MM-DD"
---
```

Sezioni:
1. **Obiettivo** — cosa fa
2. **Quando usarla / Trigger** — quando invocarla
3. **Prerequisiti** — cosa serve prima
4. **Loop conversazionale** — domande da fare (una alla volta)
5. **Processo di produzione** — passi da eseguire
6. **Output in chat** — riepilogo obbligatorio al termine
7. **Checklist qualità** — verifiche finali

**Principio**: mai produrre output senza prima raccogliere le informazioni necessarie.
