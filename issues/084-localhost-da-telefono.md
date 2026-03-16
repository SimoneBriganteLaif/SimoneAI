# Accedere al localhost dal telefono

| Campo     | Valore             |
|-----------|--------------------|
| ID        | 84                 |
| Stack     | laif-template      |
| Tipo      | Proposal           |
| Status    | Backlog            |
| Priorita  | —                  |
| Effort    | 6h                 |
| Tag       | Filone Sicurezza   |

## Descrizione originale

> Voglio accedere al localhost dal telefono

## Piano di risoluzione

1. **Configurare il dev server per ascoltare su 0.0.0.0**
   - Frontend (Next.js): aggiungere `--hostname 0.0.0.0` al comando dev
   - Backend (FastAPI/uvicorn): verificare che il bind sia già su `0.0.0.0` nel Docker
   - Aggiornare i comandi `just` per supportare una modalità "network-accessible"
   - Attenzione: non esporre su 0.0.0.0 di default per sicurezza — solo con flag esplicito

2. **Configurare HTTPS con certificati self-signed**
   - Molte API del browser (geolocation, clipboard, service worker) richiedono HTTPS su mobile
   - Generare certificati self-signed con `mkcert` (supporta trust locale)
   - Creare un comando `just certs generate` per generare i certificati
   - Configurare Next.js per usare HTTPS in dev mode con i certificati generati
   - Istruzioni per installare il certificato root CA sul telefono (iOS e Android)

3. **Aggiungere un comando `just` per la modalità mobile**
   - `just run mobile` — avvia frontend e backend accessibili dalla rete locale
   - Stampa in console l'URL da usare sul telefono: `https://192.168.x.x:8080`
   - Mostra QR code in terminale per accesso rapido dal telefono (usando `qrcode` CLI)

4. **Documentare la procedura di connessione da telefono**
   - Come trovare l'IP locale del Mac (`ifconfig en0` o equivalente)
   - Come connettersi dalla stessa rete WiFi
   - Come installare il certificato self-signed su iOS (Impostazioni > Profili)
   - Come installare il certificato self-signed su Android (Impostazioni > Sicurezza)

5. **Gestire CORS per accesso da mobile**
   - Aggiungere l'IP locale alle origini CORS consentite in modalità dev
   - Usare un pattern wildcard per la subnet locale (`192.168.*.*`)
   - Non modificare la configurazione CORS di produzione

6. **Valutare tunneling per test remoti**
   - Considerare ngrok o Cloudflare Tunnel per accesso da reti diverse
   - Utile per test con clienti o da dispositivi non sulla stessa rete
   - Aggiungere come opzione avanzata, non come default

## Stima effort

- Configurazione 0.0.0.0 e comandi just: ~1h
- Setup HTTPS con mkcert: ~1.5h
- Comando just run mobile con QR code: ~1h
- Gestione CORS: ~0.5h
- Documentazione procedura: ~1h
- Valutazione tunneling: ~1h
- **Totale: ~6h**
