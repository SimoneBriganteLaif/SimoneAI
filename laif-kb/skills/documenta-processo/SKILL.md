---
nome: "Documenta Processo"
descrizione: >
  Guida la documentazione di un processo aziendale LAIF attraverso domande strutturate.
  Produce un documento .md seguendo il template interno e lo salva in processi/.
fase: meta
versione: "0.1"
stato: beta
legge:
  - processi/README.md (per verificare che il processo non sia gia documentato)
scrive:
  - processi/[nome-processo].md
  - processi/README.md (aggiorna tabella con link al nuovo processo)
aggiornato: "2026-04-05"
---

# Skill: Documenta Processo

## Obiettivo

Documentare un processo aziendale LAIF in modo strutturato e riutilizzabile, attraverso una conversazione guidata.

## Perimetro

**Fa:**
- Raccoglie informazioni sul processo tramite domande
- Genera documento strutturato seguendo il template
- Salva in `processi/`
- Aggiorna la mappa in `processi/README.md`

**Non fa:**
- Non crea skill (per quello serve creare una skill dedicata)
- Non modifica processi esistenti (per aggiornamenti, editare il file direttamente)

## Quando usarla

- Quando si vuole formalizzare un processo che oggi vive solo nelle teste delle persone
- Quando un nuovo processo viene definito e va documentato
- Durante sessioni di knowledge sharing

## Prerequisiti

- Almeno una persona che conosce il processo nel dettaglio

## Loop conversazionale

1. **"Quale processo vuoi documentare?"**
   - Nome breve del processo (es. "deploy in produzione", "onboarding nuovo sviluppatore")

2. **"In una frase, qual e l'obiettivo di questo processo?"**
   - Cosa si ottiene alla fine

3. **"Chi sono gli attori coinvolti?"**
   - Ruoli, non nomi (es. "tech lead", "PM", "sviluppatore")

4. **"Quali sono gli input necessari per iniziare?"**
   - Documenti, decisioni, approvazioni, prerequisiti

5. **"Descrivi gli step del processo, in ordine."**
   - L'utente descrive liberamente, la skill struttura in step numerati

6. **"Qual e l'output finale del processo?"**
   - Cosa viene prodotto, dove viene consegnato

7. **"Ci sono eccezioni o casi particolari da gestire?"**
   - Percorsi alternativi, edge case

8. **"Quali strumenti vengono usati?"**
   - Tool, piattaforme, comandi

9. **"C'e una skill LAIF-KB collegata a questo processo?"**
   - Se si, quale skill supporta o automatizza parte del processo

10. **Riepilogo**: mostra bozza del documento. "Scrivo in `processi/[nome].md`?"

## Processo

1. Raccogli risposte alle domande sopra
2. Genera il documento usando `templates/processo.md`
3. Mostra bozza in chat
4. Con conferma: salva file e aggiorna `processi/README.md`

## Output in chat

```
PROCESSO DOCUMENTATO — [nome-processo]

File creato: processi/[nome-processo].md
Mappa aggiornata: processi/README.md

Riepilogo:
- Attori: [lista]
- Step: [numero]
- Strumenti: [lista]
- Skill collegata: [nome o nessuna]
```

## Checklist qualita

- [ ] Il nome del processo e chiaro e non ambiguo
- [ ] Gli step sono in ordine logico e completi
- [ ] Gli attori sono ruoli, non persone specifiche
- [ ] L'output e concreto e verificabile
- [ ] La mappa in processi/README.md e stata aggiornata
