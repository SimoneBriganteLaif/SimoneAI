# Servizio Antiphishing

| Campo     | Valore           |
|-----------|------------------|
| ID        | 69               |
| Stack     | Generale         |
| Tipo      | Proposal         |
| Status    | Backlog          |
| Priorita  | —                |
| Tag       | Filone Sicurezza |

## Descrizione originale

Ricerca e acquisto servizio antiphishing, per filtrare le email automatiche.

## Piano di risoluzione

1. **Ricerca servizi antiphishing** — Valutare le principali soluzioni sul mercato:
   - **Proofpoint** — Leader di mercato, protezione email avanzata, buona integrazione enterprise
   - **Mimecast** — Email security cloud-based, buon rapporto qualita/prezzo
   - **Microsoft Defender for Office 365** — Se si usa gia Microsoft 365, integrazione nativa
   - **Barracuda Email Protection** — Alternativa competitiva, buon supporto PMI
   - **SpamTitan** — Opzione piu economica, adatta a piccole realta

2. **Definire i requisiti** — Funzionalita necessarie:
   - Filtraggio email di phishing (inbound)
   - Scansione URL in tempo reale (link malevoli)
   - Sandboxing allegati (esecuzione in ambiente isolato)
   - Protezione da spoofing (DMARC, DKIM, SPF enforcement)
   - Reportistica e dashboard
   - Integrazione con il provider email attuale
   - API per integrazione con sistemi LAIF (se necessario)

3. **Richiedere preventivi a 2-3 provider** — Per ogni provider:
   - Costo per utente/mese
   - Funzionalita incluse vs add-on
   - SLA e supporto
   - Processo di onboarding
   - Periodo di prova gratuito

4. **PoC con il provider selezionato** — Prima dell'acquisto:
   - Attivare trial (solitamente 14-30 giorni)
   - Configurare su un subset di caselle email
   - Misurare: false positive rate, email di phishing bloccate, impatto su delivery
   - Verificare che le email automatiche LAIF (notifiche, report) non vengano bloccate

5. **Integrazione con infrastruttura email LAIF** — Dopo la selezione:
   - Configurare MX records se necessario
   - Aggiornare SPF, DKIM, DMARC
   - Configurare whitelist per servizi interni
   - Verificare compatibilita con il flusso email delle applicazioni LAIF

6. **Formazione del team** — Dopo l'attivazione:
   - Sessione su come riconoscere phishing
   - Come gestire falsi positivi/negativi
   - Procedura di segnalazione email sospette
   - Dashboard di monitoraggio

7. **Nota** — Questa e principalmente un'attivita di procurement e integrazione, non di sviluppo software. Il coinvolgimento tecnico e limitato alla configurazione DNS e alla verifica di compatibilita.

## Stima effort

**16-24 ore di effort tecnico** (escluso il processo di acquisto):
- Ricerca e comparazione (~4h)
- Richiesta preventivi e valutazione (~4h, distribuito nel tempo)
- PoC e configurazione trial (~4h)
- Integrazione e configurazione DNS (~4h)
- Test e verifica compatibilita (~4h)
- Formazione team (~2h)
