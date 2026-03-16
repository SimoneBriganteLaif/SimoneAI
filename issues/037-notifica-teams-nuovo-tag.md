# Notifica Teams su nuovo tag rilasciato

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 37                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | —                  |

## Descrizione originale

> Quando viene rilasciato un nuovo tag -> Creazione di un post di notifica sul canale Teams

## Piano di risoluzione

1. **Creare una GitHub Action triggerata sulla creazione di un tag**
   - Trigger: `on: push: tags: ['v*']` (solo tag che iniziano con `v`)
   - La action si attiva automaticamente quando viene pushato un nuovo tag
   - Estrarre dal tag: numero versione, commit associato, autore

2. **Configurare l'integrazione con Microsoft Teams via webhook**
   - Creare un Incoming Webhook nel canale Teams di destinazione
   - Salvare l'URL del webhook come GitHub Secret (`TEAMS_WEBHOOK_URL`)
   - Usare l'API webhook di Teams per inviare Adaptive Cards (formato rich)

3. **Formattare il messaggio di notifica**
   - Contenuto: nome progetto, numero versione, data rilascio
   - Includere il riepilogo del changelog (ultime modifiche dalla versione precedente)
   - Estrarre il changelog automaticamente dai commit tra il tag precedente e quello nuovo
   - Link diretto alla release su GitHub
   - Autore del rilascio

4. **Aggiungere il webhook URL come GitHub Secret**
   - Secret name: `TEAMS_WEBHOOK_URL`
   - Documentare la procedura per creare il webhook in Teams
   - Ogni progetto configura il proprio webhook verso il canale Teams corretto
   - Opzionale: webhook diversi per ambienti diversi (staging, produzione)

5. **Creare un template per il messaggio consistente tra progetti**
   - Adaptive Card con sezioni: header (progetto + versione), body (changelog), footer (link + autore)
   - Il template è parte del laif-template, riutilizzabile senza modifiche
   - Colore dell'header configurabile per progetto (brand color)
   - Possibilità di aggiungere mention a persone specifiche nel canale

## Stima effort

- GitHub Action e trigger: ~1h
- Integrazione webhook Teams: ~1h
- Formattazione messaggio e changelog automatico: ~1.5h
- Documentazione e template: ~0.5h
- Test end-to-end: ~0.5h
- **Totale: ~4.5h**
