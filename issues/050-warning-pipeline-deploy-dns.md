# Warning Pipeline Deploy DNS

| Campo     | Valore           |
|-----------|------------------|
| ID        | 50               |
| Stack     | laif-infra       |
| Tipo      | Bug              |
| Status    | In pausa         |
| Priorita  | —                |
| Effort    | 8h               |

## Descrizione originale

Warning: `aws-cdk-lib.aws_route53.RecordSetOptions#deleteExisting` is deprecated. This property is dangerous and can lead to unintended record deletion in case of deployment failure.

## Piano di risoluzione

1. **Review del codice CDK attuale** — Individuare tutti i punti in cui viene usato `deleteExisting=True` su `RecordSetOptions` nelle stack Route53. Cercare in tutte le stack di infrastruttura condivisa e nei progetti che ereditano il pattern.

2. **Comprendere il rischio** — La property e deprecata perche, in caso di fallimento del deploy, CDK potrebbe cancellare i record DNS esistenti prima di riuscire a ricrearli, causando downtime. Il comportamento atteso era "sovrascrivi se esiste", ma l'implementazione reale e "cancella e ricrea", con gap intermedio.

3. **Rimuovere `deleteExisting=True`** — Eliminare il flag da tutti i `RecordSetOptions`. Se il record DNS e gia gestito da CDK (cioe e stato creato dalla stack), CDK lo aggiornera correttamente senza bisogno di `deleteExisting`.

4. **Approccio alternativo per record pre-esistenti** — Se `deleteExisting` era usato per importare record creati fuori da CDK:
   - Usare `cdk import` per importare il record esistente nello state di CloudFormation.
   - Oppure ricreare il record tramite CDK con un nome logico diverso, verificando che non ci siano conflitti.

5. **Test dei record DNS dopo il deploy** — Verificare con `dig` o `nslookup` che tutti i record (A, CNAME, ALIAS) puntino correttamente dopo il deploy senza il flag.

6. **Aggiornare tutte le stack CDK dei progetti** — Il pattern potrebbe essere stato replicato in piu progetti. Verificare e aggiornare ogni stack che usa Route53 record sets.

## Stima effort

**8 ore** — La modifica in se e semplice (rimozione di un flag), ma richiede:
- Audit di tutte le stack CDK (~2h)
- Test su ambiente non-produzione (~3h)
- Deploy e verifica DNS su tutti gli ambienti (~3h)
