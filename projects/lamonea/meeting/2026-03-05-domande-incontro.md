---
fonte: notion
url: https://www.notion.so/31a90ad6ee488073a654f759efd27f56
data: 2026-03-05
partecipanti: [Simone Brigante]
tipo: follow-up
tags:
  - "#progetto:lamonea"
---

# Domande incontro 5/3

Domande preparate per l'incontro con Andrea e Matteo del 5 marzo.

## Domande data model

1. Confermare che articoli appartengono a una sola famiglia/sottofamiglia o a un solo gruppo/sottogruppo
2. Gestiremo famiglie e gruppi in app?
3. Come devono funzionare i kit?
4. Come gestiamo i prezzi degli articoli? Possono variare solo nei listini?
   - Prezzo unico su entità articolo?
   - Possono variare solo tramite i listini custom?
   - Quale prezzo va nella sezione public? Varia in base al cliente che si collega?
   - Nei listini si possono alternare prezzi assoluti e scontistiche in percentuale?
5. I listini hanno periodi di durata?
6. Opportunità e gare sono da gestire in maniera separata?
7. Quanti magazzini?

## Data model proposto

Il data model proposto include le seguenti entità principali:

### Prodotti
- **Family** → **Subfamily** (gerarchia classificazione)
- **ProductGroup** → **Subgroup** (seconda gerarchia)
- **Article** (cod_item unique, famiglia, gruppo, brand, classe rischio, prezzo vendita, costo ultimo acquisto, stato, flag catalogo)
- **ArticleBusiness** (multi-società)
- **ArticleDocument**, **ArticleImage** (allegati)
- **ArticleSupplier** (con codice articolo fornitore)
- **SubstituteArticle** (articoli sostitutivi)

### Kit
- **Kit** → **KitArticle** (composizione con quantità)
- **KitBusiness** (multi-società)

### CRM - Clienti
- **Customer** (ragione sociale, P.IVA, tipo, stato, agente, flag B2B)
- **CustomerBusiness**, **CustomerContact**, **CustomerAddress**

### CRM - Fornitori
- **Supplier** (codice TS, ragione sociale, lead time medio, rating)
- **SupplierBusiness**, **SupplierContact**

### Listini
- **PriceList** (nome, validità da/a, stato)
- **PriceListBusiness**, **PriceListItem** (articolo + prezzo), **PriceListCustomer**

### Opportunità e Interazioni
- **Opportunity** (titolo, cliente, business, tipo, stato pipeline, valore, commerciale, date, motivazione chiusura)
- **OpportunityArticle** (righe prodotto con quantità e prezzo)
- **Interaction** (tipo, descrizione, data, cliente, opportunità, autore, follow-up)

### Ordini
- **Order** (cliente, business, numero, data, importo, stato) — read-only da TS

Tutte le entità principali hanno tabella ponte **XxxBusiness** per il supporto multisocietario.
