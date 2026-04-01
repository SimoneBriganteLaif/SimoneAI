# Studio Perri - Analisi Completa Repository

## 1. Overview

**Applicazione**: Piattaforma gestionale per Studio Perri, uno studio di Consulenti del Lavoro. Il software gestisce l'intero ciclo operativo dello studio: anagrafica aziende clienti, gestione dipendenti, elaborazione paghe (PayOps), scadenze, processi/adempimenti, fatturazione e control room.

**Cliente**: Studio Perri CdL (Consulenti del Lavoro)
**Settore**: Consulenza del Lavoro / Payroll / HR Administration
**Codice applicazione**: `2025048`

## 2. Versioni

| Componente | Versione |
|---|---|
| App (`version.txt`) | **0.2.79** |
| laif-template (`version.laif-template.txt`) | **5.6.7** |
| laif-ds (frontend) | **0.2.73** |
| values.yaml version | 1.1.0 |
| Node.js richiesto | >= 25.0.0 |
| Python richiesto | >= 3.12, < 3.13 |

## 3. Team (top contributors)

| Contributor | Commits |
|---|---|
| mattiagualandi | 403 |
| mlife | 290 |
| Pinnuz | 269 |
| frabarb | 213 |
| github-actions[bot] | 203 |
| Simone Brigante | 92 |
| bitbucket-pipelines | 86 |
| Marco Pinelli | 85 |
| neghilowio | 75 |
| cavenditti-laif | 54 |

Progetto con team ampio (~44 contributori unici), sviluppo molto attivo (v0.2.79, 136 migrazioni Alembic).

## 4. Stack e dipendenze non-standard

### Backend (Python)

Dipendenze **non-standard** (oltre al template base):

| Dipendenza | Uso |
|---|---|
| `zeep >= 4.3.1` | Client SOAP per integrazione Zucchetti |
| `aiohttp ~= 3.13.3` | HTTP client asincrono |
| `xlsxwriter ~= 3.2.9` | Generazione file Excel (export billing) |
| `pandas ~= 3.0.1` | Analisi dati per export/reporting |
| `openai ~= 2.21.0` | Integrazione AI (gruppo LLM opzionale) |
| `pgvector ~= 0.4.2` | Vettori PostgreSQL per RAG/embedding |
| `python-docx ~= 1.2.0` | Generazione documenti Word |
| `pymupdf ~= 1.27.1` | Gestione PDF |

### Frontend (Next.js / React 19)

Dipendenze **non-standard** (oltre al template base):

| Dipendenza | Uso |
|---|---|
| `@amcharts/amcharts5` | Grafici avanzati (analytics billing) |
| `draft-js` + plugins | Editor rich text (mention, export HTML) |
| `@hello-pangea/dnd` | Drag & Drop (riordino sezioni template) |
| `@microsoft/fetch-event-source` | Server-Sent Events (chat AI) |
| `katex` + `rehype-katex` + `remark-math` | Rendering formule matematiche |
| `react-markdown` + `remark-gfm` | Rendering Markdown |
| `react-syntax-highlighter` | Syntax highlighting codice |
| `canvas-confetti` | Effetti visivi celebrativi |
| `@react-pdf/renderer` | Generazione PDF lato client |
| `framer-motion` | Animazioni UI |

### Docker Compose

Servizi: `db` (PostgreSQL), `backend` (FastAPI). Nessun servizio extra.
Variante `docker-compose.wolico.yaml` per testing con rete condivisa Wolico.

## 5. Modello dati completo

Il modello dati risiede interamente in `/backend/src/app/models.py` (2492 righe, schema `prs`). Conta **~60 tabelle**.

### Tabelle principali per area funzionale

#### Area Anagrafica Aziendale
- **companies** - Anagrafica aziende clienti (cod_company, name, cod_piva, cod_fiscale, legal_address, id_ateco, id_manager, id_supervisor, sicurezza/DVR, DURC, ecc.)
- **employees** - Anagrafica dipendenti (cod_fiscal, name, surname)
- **company_employees** - Relazione M:N azienda-dipendente con dati contrattuali (date assunzione/cessazione, contratto, qualifica, livello)
- **ateco** - Codici ATECO
- **national_collective_labor_agreements** - CCNL (des_ccnl_zucchetti, des_ccnl_perri, cod_ccnl)
- **company_ccnl** - Relazione M:N azienda-CCNL
- **istat_activities** - Attivita ISTAT
- **company_istat_activities** - Relazione M:N azienda-attivita ISTAT

#### Area Struttura Aziendale
- **board_of_directors** - Composizione CDA (ruoli: titolare, amministratore, socio, ecc.)
- **director_delegations** - Deleghe direttori (sicurezza, personale)
- **company_classifications** - Inquadramenti aziendali (artigianato, industria, commercio, ecc.) per livello INPS/INAIL/Company
- **company_inps_identifiers** - Identificatori INPS aziendali (matricola, codice SCS, sede)
- **local_business_units** - Unita locali aziendali con livello informativo
- **subscribed_administrators** - Amministratori iscritti (INPS, INAIL, GS)
- **family_collaborators** - Collaboratori familiari
- **pat** - Posizioni Assicurative Territoriali INAIL
- **employers_association** - Associazioni datoriali
- **rsu** - Rappresentanze Sindacali Unitarie
- **construction_sites** - Cantieri attivi (con flag notifica/edilconnect)
- **not_fireable_employees** - Dipendenti non licenziabili (con motivo: maternita, L104, RSU, ecc.)

#### Area Consulenza Paghe (PayOps)
- **company_pay_ops** - Configurazione operativa paghe per azienda (~60 colonne: presenze, turni, giustificativi, ferie/permessi, trasferte, ecc.)
- **company_pay_ops_documents** - Documenti allegati alle PayOps
- **f24** - Configurazione invio F24
- **ticket_restaurant** - Buoni pasto
- **canteene** - Mensa aziendale
- **health_insurance** - Assicurazioni sanitarie
- **welfare** - Welfare aziendale
- **mandatory_welfare_by_ccnl** - Welfare obbligatorio da CCNL
- **mixed_use_company_car** - Auto aziendali uso promiscuo
- **remuneration** - Retribuzioni (premi netti, mensili, altre pattuizioni)
- **inps_calculations** - Calcoli contributivi INPS
- **irpef_calculations** - Calcoli IRPEF (detrazioni, trattamento integrativo, aliquota maggiorata)
- **bilateral_entities** - Enti bilaterali
- **health_insurance_fund** - Fondi sanitari
- **other_entities** - Altri enti
- **travel_reimbursement** - Rimborsi spese viaggio
- **other_reimbursment** - Altri rimborsi
- **loans_garnishments** - Prestiti e pignoramenti
- **administrators_with_compensation** - Amministratori con compenso
- **on_call_workers_no_more_called** - Lavoratori a chiamata non piu chiamati
- **tfr_complementary_pension** - TFR in previdenza complementare
- **apprentice_type_5** - Apprendisti qualifica previdenziale tipo 5
- **apprentice_type_w** - Apprendisti qualifica previdenziale tipo W

#### Area Assenze Protette
- **illnesses** - Malattie (lunga/corta durata)
- **maternity** - Maternita (obbligatoria/facoltativa)
- **paternity** - Paternita (con calcolo fine periodo)
- **marital_leave** - Congedo matrimoniale
- **l10492** - Legge 104/92 (disabile/caregiver)
- **injuries** - Infortuni

#### Area Regolarita / DURC
- **durc** - Documenti DURC
- **company_irregularities** - Irregolarita aziendali (tipo, ente, priorita, durata)
- **unemployment_benefit** - Ammortizzatori sociali (CIGO, FSBA, FIS)
- **gmo_dismissal** - Licenziamenti GMO

#### Area Scadenze
- **deadlines** - Definizione scadenze (tipo, categoria: PAGHE/COLLOCAMENTO/ANAGRAFICHE)
- **company_deadlines** - Scadenze assegnate ad aziende
- **company_employee_deadlines** - Scadenze assegnate a dipendenti aziendali

#### Area Processi / Adempimenti
- **template_types** - Tipi di template (aziendale, dipendenti, modello annuale, adempimenti)
- **templates** - Template processi (scheduling, soglie giallo/rosso, responsabili)
- **template_sections** - Sezioni del template
- **template_section_items** - Item dentro le sezioni (testo, boolean, date, radio, file, appuntamento, chiamata, ecc.)
- **template_section_item_options** - Opzioni per item a scelta multipla
- **template_conditions** - Condizioni di visibilita sezioni/item
- **template_companies** - Associazione template-aziende
- **processes** - Istanze di processi (con stato BACKLOG/IN_PROGRESS/COMPLETED/EXPIRED/SUSPENDED e super_status calcolato)
- **process_sections** - Sezioni istanziate con durata
- **process_items** - Risposte agli item del template
- **process_item_appointments** - Appuntamenti tracciati
- **process_item_calls** - Chiamate tracciate
- **process_item_back_office_works** - Lavori back-office tracciati
- **process_item_users** - Utenti assegnati ad attivita processo

#### Area Calendario
- **calendar_reminders** - Promemoria calendario (con ricorrenze)
- **recurrence_patterns** - Pattern di ricorrenza

#### Area Fatturazione (Billing)
- **standard_hourly_price** - Prezzo orario standard
- **company_hourly_price** - Prezzo orario personalizzato per azienda
- **fixed_price** - Prezzi fissi per tipo (processo, DURC, rielaborazione cedolini)
- **billing** - Voci di fatturazione (con tracciamento ore, prezzi, stato Zucchetti)

#### Area ETL / Import
- **lkp_runs** - Registrazione run di import ETL
- **etl_import_errors** - Errori di import ETL

#### Area Monitoraggio
- **company_alerts** - Avvisi aziendali generati automaticamente
- **companies_documents** - Documenti aziendali allegati
- **notes** - Note su aziende/dipendenti
- **time_tracking** - Tracciamento timbrature operatori

### Diagramma ER (Mermaid) - Entita principali

```mermaid
erDiagram
    Companies ||--o{ CompanyEmployees : "ha"
    Companies ||--o{ CompanyCcnl : "ha"
    Companies ||--o{ CompanyIstatActivities : "ha"
    Companies ||--o{ BoardOfDirectors : "ha CDA"
    Companies ||--o{ CompanyClassification : "inquadramento"
    Companies ||--o{ CompanyInpsIdentifier : "INPS"
    Companies ||--o{ LocalBusinessUnits : "unita locali"
    Companies ||--o{ Pat : "PAT INAIL"
    Companies ||--o{ SubscribedAdministrator : "amm. iscritti"
    Companies ||--o{ FamilyCollaborator : "coll. familiari"
    Companies ||--o{ EmployersAssociation : "ass. datoriale"
    Companies ||--o{ RSU : "RSU"
    Companies ||--o{ ConstructionSites : "cantieri"
    Companies ||--o{ NotFireableEmployees : "non licenziabili"
    Companies ||--o{ UnemploymentBenefit : "ammortizzatori"
    Companies ||--o{ GmoDismissal : "licenz. GMO"
    Companies ||--o{ Notes : "note"
    Companies ||--o{ Durc : "DURC"
    Companies ||--o{ CompanyIrregularities : "irregolarita"
    Companies ||--o{ CompanyAlerts : "avvisi"
    Companies ||--o| PayOps : "config paghe"
    Companies ||--o{ CompanyDeadlines : "scadenze"
    Companies ||--o{ Billing : "fatturazione"
    Companies ||--o{ Processes : "processi"

    Employees ||--o{ CompanyEmployees : "impiegato in"
    Employees ||--o{ Remuneration : "retribuzione"
    Employees ||--o{ Illnesses : "malattie"
    Employees ||--o{ Maternity : "maternita"
    Employees ||--o{ Paternity : "paternita"
    Employees ||--o{ MaritalLeave : "congedo matr."
    Employees ||--o{ L10492 : "L104/92"
    Employees ||--o{ Injuries : "infortuni"
    Employees ||--o{ TravelReimbursement : "rimb. viaggio"
    Employees ||--o{ AdministratorsWithCompensation : "amm. compenso"
    Employees ||--o{ TfrComplementaryPension : "TFR prev."
    Employees ||--o{ MixedUseCompanyCar : "auto aziendale"

    NationalCollectiveLaborAgreements ||--o{ CompanyCcnl : "applicato a"
    Ateco ||--o{ Companies : "settore"

    PayOps ||--o{ PayOpsDocuments : "documenti"
    Companies ||--o{ F24 : "F24"
    Companies ||--o{ TicketRestaurant : "buoni pasto"
    Companies ||--o{ Canteen : "mensa"
    Companies ||--o{ HealthInsurance : "assic. sanit."
    Companies ||--o{ Welfare : "welfare"
    Companies ||--o{ MandatoryWelfareByCcnl : "welfare CCNL"
    Companies ||--o{ BilateralEntities : "enti bilat."
    Companies ||--o{ HealthInsuranceFund : "fondi sanit."
    Companies ||--o{ OtherEntities : "altri enti"
    Companies ||--o{ InpsCalculations : "calcoli INPS"
    Companies ||--o{ IrpefCalculations : "calcoli IRPEF"
    Companies ||--o{ ApprenticeType5 : "appr. tipo 5"
    Companies ||--o{ ApprenticeTypeW : "appr. tipo W"
    Companies ||--o{ LoansGarnishments : "prestiti/pign."

    Templates ||--o{ TemplateSections : "sezioni"
    Templates ||--o{ TemplateCompanies : "assegnato a"
    Templates }o--|| TemplateTypes : "tipo"
    TemplateSections ||--o{ TemplateSectionItems : "item"
    TemplateSectionItems ||--o{ TemplateSectionItemOptions : "opzioni"
    TemplateSections ||--o{ TemplateConditions : "condizioni"

    Processes }o--|| Templates : "da template"
    Processes ||--o{ ProcessSections : "sezioni"
    Processes ||--o{ ProcessItems : "risposte"
    ProcessItems ||--o{ ProcessItemAppointment : "appuntamenti"
    ProcessItems ||--o{ ProcessItemCall : "chiamate"
    ProcessItems ||--o{ ProcessItemBackOfficeWork : "lavori BO"

    Deadlines ||--o{ CompanyDeadlines : "assegnata a"
    Deadlines ||--o{ CompanyEmployeeDeadlines : "assegnata a"

    Billing }o--o| Processes : "da processo"
    Billing }o--|| Companies : "per azienda"

    RecurrencePattern ||--o{ CalendarReminders : "ricorrenza"
    Users ||--o{ CalendarReminders : "reminder"
    Users ||--o{ TimeTracking : "timbrature"

    Companies {
        int id PK
        string cod_company
        string name
        string cod_piva
        string cod_fiscale
        string legal_address
        int id_ateco FK
        int id_manager FK
        int id_supervisor FK
        bool flg_valid
    }

    Employees {
        int id PK
        string cod_fiscal UK
        string name
        string surname
    }

    CompanyEmployees {
        int id PK
        int id_company FK
        int id_employee FK
        string cod_employee
        date dat_hiring_date
        date dat_termination_date
        string cod_contract
        string cod_qualification
        string cod_level
    }

    PayOps {
        int id PK
        int id_company FK
        int to_do_before
        int salary_payment_on
        string presence_communication_method
        string working_hours
        date patron_day
        bool flg_portal
        bool flg_ticket_restaurant
        many_more_fields___
    }

    Processes {
        int id PK
        int id_template FK
        int id_company FK
        string status
        date dat_start
        date dat_end
        date dat_completion
        int num_days_yellow
        int num_days_red
    }

    Billing {
        int id PK
        string voice_type
        int id_process FK
        int id_company FK
        float fixed_price
        int total_work_minutes
        float hourly_rate
        float actual_charged_price
        bool flg_recorded_in_zucchetti
    }
```

## 6. API Routes

L'applicazione espone **~170 endpoint** organizzati in 65+ controller. Raggruppamento per area:

### Anagrafica
- `/companies/` - CRUD aziende + ricerca + statistiche
- `/employees/` - CRUD dipendenti
- `/company-employees/` - Relazione azienda-dipendente
- `/ateco/` - Codici ATECO
- `/national-collective-labor-agreements/` - CCNL
- `/istat-activities/` - Attivita ISTAT

### Struttura Aziendale
- `/board-of-directors/` - Composizione CDA
- `/director-delegations/` - Deleghe
- `/company-classifications/` - Inquadramenti
- `/local-business-units/` - Unita locali
- `/pat/` - Posizioni INAIL
- `/subscribed-administrators/` - Amministratori iscritti
- `/family-collaborators/` - Collaboratori familiari
- `/employers-association/` - Associazioni datoriali
- `/rsu/` - RSU
- `/construction-sites/` - Cantieri
- `/not-fireable-employees/` - Non licenziabili

### Consulenza Paghe
- `/pay-ops/` - Configurazione operativa paghe
- `/pay-ops-documents/` - Documenti PayOps
- `/companies-documents/` - Documenti aziendali
- `/f24/` - Gestione F24
- `/canteen/` - Mensa
- `/ticket-restaurant/` - Buoni pasto
- `/health-insurance/` - Assicurazioni sanitarie
- `/welfare/` - Welfare
- `/mandatory-welfare-by-ccnl/` - Welfare obbligatorio CCNL
- `/mixed-use-company-car/` - Auto aziendali
- `/remuneration/` - Retribuzioni
- `/inps-calculations/` - Calcoli INPS
- `/irpef-calculations/` - Calcoli IRPEF
- `/bilateral-entities/` - Enti bilaterali
- `/health-insurance-fund/` - Fondi sanitari
- `/other-entities/` - Altri enti
- `/travel-reimbursement/` - Rimborsi viaggio
- `/other-reimbursement/` - Altri rimborsi
- `/loans-garnishments/` - Prestiti/pignoramenti
- `/administrators-with-compensation/` - Amministratori con compenso
- `/on-call-workers/` - Lavoratori a chiamata
- `/tfr-complementary-pension/` - TFR previdenza complementare
- `/apprentice-type-5/`, `/apprentice-type-w/` - Apprendisti

### Assenze Protette
- `/illnesses/` - Malattie
- `/injuries/` - Infortuni
- `/maternity/` - Maternita
- `/paternity/` - Paternita
- `/marital-leave/` - Congedo matrimoniale
- `/l10492/` - Legge 104/92

### Regolarita
- `/durc/` - DURC
- `/company-irregularities/` - Irregolarita
- `/unemployment-benefit/` - Ammortizzatori sociali
- `/gmo-dismissal/` - Licenziamenti GMO
- `/notification-contacts/` - Contatti notifica

### Scadenze
- `/deadlines/` - Definizione scadenze
- `/company-deadlines/` - Scadenze aziendali
- `/company-employee-deadlines/` - Scadenze dipendenti

### Processi / Adempimenti (~15 controller)
- `/template-types/` - Tipi template
- `/templates/` - Template processi
- `/template-sections/` - Sezioni
- `/template-section-items/` - Item
- `/template-section-item-options/` - Opzioni
- `/template-conditions/` - Condizioni
- `/template-companies/` - Associazione template-aziende
- `/processes/` - Processi istanziati
- `/process-items/` - Risposte processo
- `/process-sections/` - Sezioni processo
- `/process-item-appointments/` - Appuntamenti
- `/process-item-calls/` - Chiamate
- `/process-item-back-office-works/` - Lavori BO
- `/process-item-users/` - Utenti assegnati

### Fatturazione
- `/billing/` - Voci fatturazione + export Excel
- `/standard-hourly-price/` - Prezzi orari standard
- `/company-hourly-price/` - Prezzi personalizzati
- `/fixed-price/` - Prezzi fissi

### Operazioni
- `/control-room/` - Dashboard operativa (aziende gestite, alert, colleghi, irregolarita aperte, stato paghe)
- `/zucchetti/` - Trigger import ETL da Zucchetti
- `/calendar-reminders/` - Promemoria calendario
- `/time-tracking/` - Tracciamento timbrature
- `/notes/` - Note
- `/changelog/` - Changelog

## 7. Business Logic

### ETL Zucchetti (Background Tasks)

La componente piu complessa. Integrazione SOAP con il gestionale Zucchetti per sincronizzazione dati:

- **12 task di import**: CCNL, aziende, dipendenti, attivita ISTAT, prestiti/pignoramenti, contribuzioni INPS agevolate, detrazioni, trattamento integrativo, aliquota maggiorata, TFR, apprendisti tipo 5, apprendisti tipo W
- **Architettura**: client SOAP autenticato (zeep + HTTPBasicAuth), funzione generica `fetch_and_validate_generic` per parsing e validazione Pydantic, logging errori in `etl_import_errors`
- **Schedulazione**: import notturno automatico alle 2:00 AM via `repeat_every` (fastapi-utils), con check orario ogni ora
- **Run tracking**: tabella `lkp_runs` per tracciare inizio/fine/errori di ogni run

### Processi e Adempimenti

Sistema avanzato di workflow management:

- **Template engine**: template configurabili con sezioni, item tipizzati (testo, boolean, date, radio, checkbox, file upload/download, appuntamento, chiamata, lavoro back-office), condizioni di visibilita
- **Scheduling**: processi pianificabili (settimanale, mensile, trimestrale, semestrale, annuale, on demand)
- **Super-status calcolato**: NOT_STARTED -> REGULAR -> WARNING -> CRITICAL -> COMPLETED/EXPIRED/SUSPENDED, calcolato come `column_property` SQL con soglie giallo/rosso configurabili
- **Tracciamento attivita**: ogni processo traccia appuntamenti, chiamate e lavori back-office con durate e partecipanti

### Control Room

Dashboard operativa con query SQL raw dedicate:

- Aziende gestite per operatore con stato paghe mensili
- Alert aziendali (generati/refreshati automaticamente ogni ora)
- Irregolarita aperte
- Gestione colleghi

### Fatturazione (Billing)

- Calcolo automatico basato su ore lavorate (da processi) * tariffa oraria (standard o personalizzata per azienda)
- Prezzi fissi per tipologia (processo, DURC, irregolarita DURC, rielaborazione cedolini)
- Export Excel (xlsxwriter + pandas)
- Analytics su tempi processi
- Flag registrazione in Zucchetti

### Time Tracking

Timbrature operatori per analisi produttivita.

## 8. Integrazioni esterne

| Integrazione | Tecnologia | Scopo |
|---|---|---|
| **Zucchetti HR** | SOAP/WSDL via `zeep` | Import massivo dati: aziende, dipendenti, CCNL, calcoli INPS/IRPEF, TFR, apprendisti, prestiti |
| **Wolico** | Rete Docker condivisa | Testing integrato con piattaforma Wolico (rete `wolico_shared_network`) |
| **OpenAI** | `openai` SDK (opzionale) | Chat AI integrata (template feature) |
| **pgvector** | PostgreSQL extension | Embedding per RAG (template feature) |
| **AWS S3** | `boto3` | Storage file (allegati documenti, PayOps, processi) |
| **AWS Parameter Store** | `boto3` | Gestione credenziali/configurazione |

## 9. Albero pagine frontend

```
/ (login)
/control_room/                    -- Dashboard operativa (home page)
/companies/                       -- Lista aziende
  /companies/detail/
    /general/                     -- Dettaglio azienda - Generale
      - Dati aziendali, CCNL, Ateco, inquadramento
      - CDA, PAT INAIL, INPS, unita locali
      - Amministratori iscritti, collaboratori familiari
      - Associazione datoriale, RSU, note
      - Cantieri, non licenziabili, ammortizzatori, GMO
    /regularity/                  -- Regolarita aziendale
      - DURC, irregolarita
    /safety_at_work/              -- Sicurezza sul lavoro
      - DVR, preposti, documenti
    /payroll_and_accounting/      -- Paghe e contabilita
    /ongoing_proceedings/         -- Procedimenti in corso
/payroll_operating_notes/         -- Note operative paghe
  /pay_ops/                       -- Dettaglio PayOps per azienda
    - Presenze (giustificativi, ratei, turni, trasferte, rimborsi)
    - Retribuzione (premi, amministratori, prestiti, on-call, TFR)
    - Welfare (mensa, buoni pasto, assicurazioni, auto aziendali, welfare CCNL)
    - Enti (bilaterali, fondi sanitari, altri)
    - Calcoli INPS/IRPEF (contribuzioni, detrazioni, apprendisti)
    - Assenze protette (malattie, maternita, paternita, congedo, L104, infortuni)
    - F24
    - Contatti notifica e prospetti
    - Sezione libera
  /deadline_pay_ops/              -- Scadenze paghe
  /status_pay_ops/                -- Status mensile paghe
  /check_list_pay_ops/            -- Checklist paghe
  /pay_ops_templates/             -- Template paghe
    /detail/                      -- Dettaglio template paghe
/procedures/                      -- Processi e adempimenti
  /instructions/                  -- Lista processi
    /detail/                      -- Dettaglio processo
  /mapping/                       -- Mapping template-aziende
    /detail/                      -- Dettaglio template
/billing/                         -- Fatturazione
  /billing_main/                  -- Lista voci fatturazione
  /analytics/                     -- Analytics tempi/costi
  /price_list/                    -- Listino prezzi
/deadline/                        -- Scadenze
  /deadline_main/                 -- Lista scadenze
    /detail/                      -- Dettaglio scadenza
  /calendar/                      -- Calendario promemoria
/time-tracking/                   -- Analisi timbrature
/zucchetti_customization/         -- Personalizzazione Zucchetti
/update_data/                     -- Aggiornamento dati (trigger import)
```

## 10. Deviazioni dal laif-template

### File/cartelle specifiche del progetto
- `docker-compose.wolico.yaml` - Configurazione per testing integrato con Wolico
- `backend/src/app/background_tasks/` - ETL Zucchetti complesso (12 task, client SOAP)
- `backend/src/app/control_room/queries/` - 4 query SQL raw per dashboard
- `backend/src/app/billing/` - Sistema fatturazione con export Excel
- `backend/src/app/processes/` - Engine processi/adempimenti (service da 1856 righe)
- `backend/src/app/time_tracking/` - Tracciamento timbrature
- `backend/src/app/calendar_reminders/` - Calendario con ricorrenze
- `backend/src/app/config.py` - Configurazione Zucchetti (username, password, env_code, base_endpoint)
- `frontend/src/features/zucchetti-customization/` - UI personalizzazione Zucchetti
- `frontend/src/features/update-data/` - UI trigger import dati
- `frontend/src/features/time_tracking/` - UI analisi timbrature
- `frontend/src/features/billing/` - UI fatturazione con analytics e listino prezzi

### Dipendenze backend non-template
- `zeep` per SOAP
- `aiohttp` per HTTP async
- `xlsxwriter` + `pandas` per export Excel

## 11. Pattern notevoli

1. **ETL Engine strutturato**: architettura pulita con `ZucchettiTaskConfig` dataclass, funzione generica `fetch_and_validate_generic`, error tracking per tabella, run tracking con timestamps. Pattern potenzialmente estraibile.

2. **Modello dati massiccio**: 2492 righe in un singolo `models.py` con ~60 tabelle. Uso estensivo di `column_property` per campi calcolati SQL-side (count scadenze, flag entita attive, super_status processi).

3. **DateIntervalMixin**: mixin riutilizzabile per tutte le entita con intervallo temporale (dat_start/dat_end) con constraint automatico.

4. **Template engine per processi**: sistema flessibile di template con sezioni, item tipizzati, condizioni di visibilita, opzioni. Permette di modellare qualsiasi adempimento/processo senza codice.

5. **Super-status calcolato in SQL**: `column_property` che calcola lo stato evoluto del processo (NOT_STARTED/REGULAR/WARNING/CRITICAL/COMPLETED/EXPIRED/SUSPENDED) direttamente nella query, evitando logica applicativa.

6. **Control Room con raw SQL**: query SQL dedicate in file `.sql` separati per query complesse di dashboard, anziché ORM.

7. **Grace period pattern**: logica `_active_grace_expr` nel modello PayOps che considera un record "attivo" fino al 20 del mese successivo alla data di fine, per gestire i tempi di elaborazione paghe.

8. **RouterBuilder pattern**: uso del `RouterBuilder` del template per generare CRUD standardizzati con una API fluent.

## 12. Note e osservazioni

### Tech Debt
- **models.py monolitico**: 2492 righe in un singolo file. Andrebbe suddiviso per area funzionale.
- **processes/service.py**: 1856 righe, il service piu grande. Candidato per refactoring.
- **CHANGELOG.md vuoto**: nessuna entry dopo la v0.1, nonostante 79 release.
- **Typo nel nome tabella**: `canteene` (con doppia e) anziche `canteen`.
- **Typo nell'enum**: `AZIENDE_SPECIFIHE` anziche `AZIENDE_SPECIFICHE` in `DeadlinesType`.
- **models.py supera la regola dei 500 righe** dichiarata nel README.

### Complessita
- Progetto con dominio molto complesso (diritto del lavoro italiano, contribuzioni INPS/IRPEF, CCNL, sicurezza sul lavoro, DURC).
- 136 migrazioni Alembic indicano evoluzione significativa dello schema.
- 359 file Python nel backend app evidenziano un codebase maturo.
- Integrazione Zucchetti via SOAP e complessa ma ben strutturata.

### Peculiarita
- Integrazione bidirezionale con Zucchetti: import dati + flag `flg_recorded_in_zucchetti` nel billing.
- Supporto Wolico via rete Docker condivisa (variante docker-compose dedicata).
- Dominio 100% italiano (enums, commenti, logica business in italiano).
- Feature LLM/chat del template attiva (openai + pgvector nelle dipendenze default).
