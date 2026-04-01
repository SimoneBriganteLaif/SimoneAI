---
tags: ["#progetto:jubatus", "#fase:dev"]
---

# Email post-call Infrastruttura — 20/03/2026

**A**: Team Jubatus
**Oggetto**: Recap call infrastruttura + prossimi passi

---

Ciao ragazzi,

vi faccio un breve recap della call di oggi.

Abbiamo deciso di deployare l'applicazione direttamente sul vostro account AWS, usando la VPC e il load balancer che avete già. Il nostro stack di deploy è pensato per creare le risorse da zero, quindi adattarlo a risorse esistenti potrebbe richiedere qualche aggiustamento in più da parte nostra — niente di bloccante, ma ci potrebbe voler un po' di lavoro extra per far combaciare tutto.

Da parte vostra ci servirebbero queste cose:
- Creare un'utenza tecnica AWS per il deploy, inizialmente con permessi ampi (idealmente AdministratorAccess o simile). Una volta che il setup è stabile andremo a restringere i permessi al minimo necessario
- Creare anche un'utenza personale per me per accesso alla console — per questa valuteremo insieme man mano quali permessi aggiungere in base alle necessità
- Mandarci VPC ID, lista subnet e conferma che ci sia un Internet Gateway
- Per il load balancer avremo bisogno di una mano da parte vostra per capire come è configurato e adattare il nostro deploy di conseguenza

Da parte mia:
- Preparo gli script di setup dell'infrastruttura
- Verifico la compatibilità del nostro stack con le vostre risorse esistenti (VPC, subnet, load balancer)
- Adatto il nostro CDK per lavorare con un load balancer già esistente

Vi propongo di fare una sessione operativa insieme verso fine settimana (giovedì o venerdì), in screen sharing, per procedere con il setup sull'ambiente di test. Avete disponibilità?

A presto,
Simone
