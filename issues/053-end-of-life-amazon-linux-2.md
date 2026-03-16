# End of Life Amazon Linux 2

| Campo     | Valore           |
|-----------|------------------|
| ID        | 53               |
| Stack     | laif-infra       |
| Tipo      | Bug              |
| Status    | In pausa         |
| Priorita  | —                |
| Effort    | 8h               |

## Descrizione originale

[Action Recommended] Upcoming End of Life of the Amazon Linux 2 ECS-optimized AMI [AWS Account: 533567530759] [EU-WEST-1]. `machine_image: ecs.EcsOptimizedImage = ecs.EcsOptimizedImage.amazon_linux2023(ecs.AmiHardwareType.ARM)`

## Piano di risoluzione

1. **Il fix e gia identificato** — La riga di codice suggerita nella descrizione indica la sostituzione: passare da `amazon_linux2()` a `amazon_linux2023()` con hardware type ARM.

2. **Aggiornare il codice CDK infra** — Modificare la definizione dell'AMI ECS-optimized:
   ```python
   # Da:
   machine_image = ecs.EcsOptimizedImage.amazon_linux2(...)
   # A:
   machine_image = ecs.EcsOptimizedImage.amazon_linux2023(ecs.AmiHardwareType.ARM)
   ```

3. **Test su ambiente non-produzione** — Deployare prima su DEV per verificare che i container funzionino correttamente su AL2023. Attenzione a:
   - Versione glibc (AL2023 usa glibc 2.34+)
   - Pacchetti di sistema usati nei Dockerfile
   - Compatibilita con le immagini Docker ARM esistenti

4. **Verificare compatibilita container** — Controllare che tutti i Dockerfile dei progetti LAIF non dipendano da pacchetti specifici di Amazon Linux 2. AL2023 usa `dnf` invece di `yum` e ha versioni piu recenti di librerie di sistema.

5. **Rolling deployment per minimizzare downtime** — Usare la strategia di rolling update di ECS:
   - Impostare `minimumHealthyPercent: 50` e `maximumPercent: 200`
   - ECS lancera nuove task con la nuova AMI prima di terminare le vecchie

6. **Aggiornare tutti i progetti** — Verificare che tutte le stack CDK che usano l'infra condivisa ereditino la nuova AMI. Se ogni progetto ha la propria definizione, aggiornarle singolarmente.

## Stima effort

**8 ore** — Il cambio di codice e minimo, ma la verifica di compatibilita e il deploy controllato richiedono tempo:
- Modifica CDK e review (~1h)
- Test compatibilita container su DEV (~3h)
- Deploy progressivo e monitoraggio (~3h)
- Documentazione aggiornamento (~1h)
