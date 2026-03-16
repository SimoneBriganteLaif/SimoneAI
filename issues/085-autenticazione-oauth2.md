# Autenticazione con OAuth2

| Campo | Valore |
|---|---|
| **ID** | 85 |
| **Stack** | laif-template |
| **Tipo** | Proposal |
| **Status** | To Review |
| **Effort** | 8h |
| **Tag** | Filone Sicurezza |

## Descrizione originale

Autenticazione con OAuth2.

## Piano di risoluzione

1. **Già in To Review.** Verificare eventuali PR o branch esistenti prima di procedere.
2. **Implementare il flusso di autenticazione OAuth2 nel template** — supportare il flusso Authorization Code con PKCE (consigliato per SPA):
   - Redirect al provider → autorizzazione utente → callback con code → scambio code per token.
3. **Supportare i provider principali**:
   - **Google** — Google OAuth2 / OpenID Connect.
   - **Microsoft** — Azure AD / Microsoft Entra ID.
   - **Custom OIDC** — qualsiasi provider compatibile OpenID Connect (per clienti con IdP aziendale).
4. **Backend: endpoint OAuth2** — implementare:
   - `GET /auth/oauth2/{provider}/authorize` — genera URL di redirect al provider.
   - `GET /auth/oauth2/{provider}/callback` — riceve il code, scambia per token, crea/aggiorna utente locale, emette JWT.
   - Configurazione provider tramite variabili d'ambiente (`OAUTH2_GOOGLE_CLIENT_ID`, ecc.).
   - Mapping attributi: email, nome, ruolo (se disponibile dal provider).
5. **Frontend: flusso di login OAuth2** — implementare:
   - Bottoni OAuth2 nella pagina di login ("Accedi con Google", "Accedi con Microsoft").
   - Redirect al provider e gestione del ritorno (callback page).
   - Gestione errori (utente non autorizzato, provider non disponibile).
6. **Mantenere la compatibilità con l'autenticazione JWT esistente** — OAuth2 è un'opzione aggiuntiva, non sostitutiva. L'autenticazione username/password con JWT deve continuare a funzionare. L'utente può avere entrambi i metodi associati al proprio account.

### Issue correlate

- Issue 54 — HttpOnly cookies per JWT (Filone Sicurezza)
- Issue 70 — Permissions e feature flags

## Stima effort

**8h** — il flusso OAuth2 è standard e ben documentato. Il grosso del lavoro è nella gestione multi-provider e nel mapping degli attributi utente. Librerie consigliate: `authlib` (backend), componenti laif-ds per i bottoni social (frontend).
