# Dashboard Issues — Piano di Risoluzione

Generato il: 2026-03-15

---

## Sommario

### Per status

| Status | Conteggio |
|--------|-----------|
| Da rilasciare | 5 |
| To Review | 4 |
| In corso | 10 |
| In analisi | 3 |
| Da iniziare | 6 |
| In pausa | 4 |
| Nuova | 5 |
| Backlog | ~20 |
| **Totale** | **~57** |

### Per stack

| Stack | Issues |
|-------|--------|
| laif-template | ~38 |
| laif-ds | ~15 |
| laif-infra | 4 |
| Generale / Cross-stack | 4 |

---

## Matrice di priorita

### 1. Release immediato

Issue gia pronte, serve solo il deploy.

| ID | Titolo | Stack |
|----|--------|-------|
| 27 | Aggiungere fill-token classi Tailwind | laif-template |
| 149 | Lazy load pagine template | laif-template |
| 147 | Font sizes in rem | laif-template |
| 111 | Refactor Navigazione | laif-template |
| 129 | Ristrutturare colori Tailwind | laif-template |

### 2. Review urgente

Completare la review per sbloccare il rilascio.

| ID | Titolo | Stack |
|----|--------|-------|
| 76 | User Management form | laif-template |
| 80 | Redux serializzare date | laif-template |
| 85 | Autenticazione OAuth2 | laif-template |
| 141 | Config file feature flag | laif-template |

### 3. Bug critici

Impatto diretto su utenti o stabilita del sistema.

| ID | Titolo | Stack | Effort |
|----|--------|-------|--------|
| 103 | Filtro pagina supporto rotto | laif-template | - |
| 110 | Colori Toaster assenti | laif-ds | 1h |
| 169 | Gestione Logging | laif-template | 8h |
| 165 | Config migrazioni Alembic | laif-template | 4h |

### 4. Roadmap items in corso

Iniziative strategiche gia avviate.

| ID | Titolo | Stack | Effort |
|----|--------|-------|--------|
| 166 | Ticketing Refactor | laif-template | 8h |
| 91 | Dismettere Next.js per TanStack Router | laif-template | - |
| 168 | Gestione Date | laif-template | 24h |

### 5. Infra urgente

Ha una deadline AWS — non rimandabile.

| ID | Titolo | Effort |
|----|--------|--------|
| 53 | AMI End of Life (Amazon Linux 2) | 8h |

### 6. Quick wins (effort 4h o meno)

Risolvibili rapidamente, alto rapporto valore/tempo.

| ID | Titolo | Stack | Effort |
|----|--------|-------|--------|
| 110 | Colori Toaster assenti | laif-ds | 1h |
| 160 | Orari WeeklyCalendar | laif-ds | 2h |
| 104 | Focus modale in edit | laif-ds | 2h |
| 114 | Navigation Beta | laif-ds | 4h |
| 151 | Docker Ctrl+C miglioramento | laif-template | 4h |

---

## Issues per stack

### laif-template

| ID | Titolo | Tipo | Status | Effort | File |
|----|--------|------|--------|--------|------|
| 27 | Aggiungere fill-token classi Tailwind | Bug | Da rilasciare | 1h | [027](027-fill-token-classi-tailwind.md) |
| 37 | Notifica Teams nuovo tag | Proposal | Backlog | - | [037](037-notifica-teams-nuovo-tag.md) |
| 51 | n8n per i workflow | Proposal | Backlog | - | [051](051-n8n-workflow.md) |
| 52 | MCP per produttivita | Proposal | In corso | - | [052](052-mcp-produttivita.md) |
| 54 | HttpOnly Cookie per JWT | Bug | Backlog | - | [054](054-httponly-cookie-jwt.md) |
| 56 | Dashboard standard template | Proposal | Backlog | - | [056](056-dashboard-standard-template.md) |
| 65 | Aggiornamento stato ticket | Bug | In pausa | 4h | [065](065-aggiornamento-stato-ticket.md) |
| 70 | Nuova gestione permessi | Proposal | Backlog | - | [070](070-nuova-gestione-permessi.md) |
| 71 | Navigazione stile mobile | Proposal | In pausa | 16h | [071](071-navigazione-stile-mobile.md) |
| 72 | AI Stack di Laif | Proposal | Backlog | - | [072](072-ai-stack-laif.md) |
| 73 | Semplificare upstream | Proposal | Backlog | - | [073](073-semplificare-upstream.md) |
| 74 | Modularizzazione template | Proposal | Backlog | - | [074](074-modularizzazione-template.md) |
| 76 | User Management form | Bug | To Review | 6h | [076](076-user-management-form.md) |
| 80 | Redux serializzare date | Proposal | To Review | 12h | [080](080-redux-serializzare-date.md) |
| 84 | Localhost dal telefono | Proposal | Backlog | 6h | [084](084-localhost-da-telefono.md) |
| 85 | Autenticazione OAuth2 | Proposal | To Review | 8h | [085](085-autenticazione-oauth2.md) |
| 86 | Tipizzare search/CRUD service | Proposal | Da iniziare | 8h | [086](086-tipizzare-search-crud-service.md) |
| 91 | Dismettere Next.js per TanStack Router | Proposal | In corso | - | [091](091-dismettere-nextjs-tanstack-router.md) |
| 92 | Test in pre-commit hook problematici | Bug | In corso | - | [092](092-test-pre-commit-hook-problema.md) |
| 94 | Copier per upstream | Proposal | Backlog | - | [094](094-copier-upstream.md) |
| 103 | Filtro pagina supporto rotto | Bug | Da iniziare | - | [103](103-filtro-pagina-supporto.md) |
| 111 | Refactor Navigazione | Proposal | Da rilasciare | 8h | [111](111-refactor-navigazione.md) |
| 129 | Ristrutturare colori Tailwind | Proposal | Da rilasciare | 2h | [129](129-ristrutturare-colori-tailwind.md) |
| 133 | Miglioramenti Media Service | Proposal | In corso | - | [133](133-miglioramenti-media-service.md) |
| 134 | Backend upload | Proposal | Nuova | - | [134](134-backend-upload.md) |
| 135 | Media service hooks | Proposal | Nuova | - | [135](135-media-service-hooks.md) |
| 141 | Config file feature flag | Proposal | To Review | - | [141](141-config-file-feature-flag.md) |
| 146 | Fork da master non dev | Bug | Backlog | - | [146](146-fork-template-da-master.md) |
| 147 | Font sizes in rem | Proposal | Da rilasciare | 2h | [147](147-font-sizes-rem.md) |
| 149 | Lazy load pagine template | Proposal | Da rilasciare | 1h | [149](149-lazy-load-pagine.md) |
| 150 | KPI fiducia cliente | Proposal | Backlog | - | [150](150-kpi-fiducia-cliente.md) |
| 151 | Docker Ctrl+C miglioramento | Proposal | Backlog | 4h | [151](151-docker-compose-ctrl-c.md) |
| 159 | Metriche utilizzo database | Proposal | In analisi | 8h | [159](159-loggare-metriche-database.md) |
| 163 | Laif Agent | Roadmap | Nuova | - | [163](163-laif-agent.md) |
| 164 | Ripulire template legacy | Bug | Nuova | - | [164](164-ripulire-template-legacy.md) |
| 165 | Config migrazioni Alembic | Bug | In corso | 4h | [165](165-configurazione-migrazioni-alembic.md) |
| 166 | Ticketing Refactor | Roadmap | In corso | 8h | [166](166-ticketing-refactor.md) |
| 168 | Gestione Date | Roadmap | In analisi | 24h | [168](168-gestione-date.md) |
| 169 | Gestione Logging | Bug | In analisi | 8h | [169](169-gestione-logging.md) |

### laif-ds

| ID | Titolo | Tipo | Status | Effort | File |
|----|--------|------|--------|--------|------|
| 42 | Async Confirmer | Proposal | Backlog | 4h | [042](042-async-confirmer.md) |
| 88 | Chat refactor UI | Bug | In corso | 12h | [088](088-chat-refactor-ui.md) |
| 89 | AppDialog mobile Drawer | Proposal | Backlog | 6h | [089](089-appdialog-mobile-drawer.md) |
| 97 | Componente recording audio | Proposal | Da iniziare | 8h | [097](097-componente-recording-audio.md) |
| 104 | Focus modale in edit | Proposal | Backlog | 2h | [104](104-focus-modale-edit.md) |
| 107 | Nuovo AppCard | Proposal | In corso | 8h | [107](107-nuovo-componente-appcard.md) |
| 110 | Colori Toaster | Bug | Da iniziare | 1h | [110](110-colori-toaster-assenti.md) |
| 114 | Navigation Beta | Proposal | Da iniziare | 4h | [114](114-navigation-gestione-beta.md) |
| 118 | AppTooltip sidebar mobile | Bug | Backlog | 4h | [118](118-apptooltip-sidebar-open-mobile.md) |
| 119 | Split Button | Proposal | Backlog | 6h | [119](119-split-button.md) |
| 125 | Filtro select/multiselect AppForm | Bug | Da iniziare | 3h | [125](125-filtro-opzioni-select-multiselect-appform.md) |
| 126 | Censimento componenti Firefox | Bug | Backlog | 16h | [126](126-censimento-componenti-firefox.md) |
| 148 | Required e classi DS | Proposal | Backlog | 24h | [148](148-required-allineare-classi-ds.md) |
| 154 | Visual feedback upload | Bug | Backlog | - | [154](154-visual-feedback-file-uploads.md) |
| 160 | Orari WeeklyCalendar | Bug | Backlog | 2h | [160](160-visualizzazione-orari-weekly-calendar.md) |

### laif-infra

| ID | Titolo | Tipo | Status | Effort | File |
|----|--------|------|--------|--------|------|
| 50 | Warning DNS deploy | Bug | In pausa | 8h | [050](050-warning-pipeline-deploy-dns.md) |
| 53 | AMI End of Life | Bug | In pausa | 8h | [053](053-end-of-life-amazon-linux-2.md) |
| 158 | Ambiente TEST | Proposal | Backlog | - | [158](158-ambiente-test-app.md) |
| 167 | Horizontal Scaling | Roadmap | Nuova | - | [167](167-horizontal-scaling.md) |

### Generale / Cross-stack

| ID | Titolo | Tipo | Status | File |
|----|--------|------|--------|------|
| 69 | Servizio antiphishing | Proposal | Backlog | [069](069-servizio-antiphishing.md) |
| 130 | Test improvements | Proposal | In corso | [130](130-test-improvements.md) |
| 136 | Git branches workflow | Proposal | Backlog | [136](136-improve-git-branches-workflow.md) |
| 144 | Transfer data tests | Proposal | Backlog | [144](144-add-transfer-data-tests.md) |
