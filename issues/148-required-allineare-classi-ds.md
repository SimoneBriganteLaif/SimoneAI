# Allineare classi required su tutti i componenti form

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 148             |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | Backlog         |
| **Priorità**| Alta            |
| **Effort stimato** | 24h      |

## Descrizione originale

Tutti gli input, datepicker ecc... dovrebbero predisporre la label e il parametro required.

## Piano di risoluzione

### 1. Audit completo dei componenti form

Esaminare tutti i componenti form presenti in laif-ds e verificare lo stato attuale del supporto alle prop `label` e `required`:

- `Input` / `AppInput`
- `Select` / `AppSelect`
- `DatePicker` / `AppDatePicker`
- `TimePicker` / `AppTimePicker`
- `Textarea` / `AppTextarea`
- `Checkbox` / `AppCheckbox`
- `RadioGroup` / `AppRadioGroup`
- `Switch` / `AppSwitch`
- `FileUpload` / `AppFileUpload`
- Eventuali altri componenti form non elencati

Per ognuno, mappare: presenza della prop `label`, presenza della prop `required`, comportamento visuale attuale, classi CSS applicate.

### 2. Standardizzare le prop `label` e `required`

Per ogni componente form che non le supporta già:

- Aggiungere la prop `label` (tipo `string`, opzionale)
- Aggiungere la prop `required` (tipo `boolean`, default `false`)
- Assicurarsi che la firma delle prop sia coerente tra tutti i componenti (stesso nome, stesso tipo, stessa posizione)

### 3. Indicatore visuale per i campi required

Quando `required={true}` e `label` è presente:

- Mostrare un asterisco (`*`) accanto alla label, con colore coerente con i token del tema (es. `--color-danger` o `--color-text-secondary`)
- Aggiungere la classe CSS `.required` al wrapper del componente
- Aggiungere l'attributo HTML `required` all'elemento nativo sottostante (`<input>`, `<select>`, ecc.)
- Aggiungere `aria-required="true"` per accessibilità

### 4. Standardizzare le classi CSS

Definire un set coerente di classi CSS per tutti i componenti form:

- `.form-field` — wrapper esterno
- `.form-field--required` — modificatore quando required
- `.form-field__label` — label
- `.form-field__label-asterisk` — asterisco required
- `.form-field__input` — area input
- `.form-field__error` — messaggio di errore

Verificare che ogni componente utilizzi le stesse classi e la stessa struttura DOM.

### 5. Aggiornare la documentazione Storybook

Per ogni componente modificato:

- Aggiornare le stories esistenti per mostrare il comportamento con `required`
- Aggiungere una story dedicata "Required Fields" che mostri tutti i componenti form con `required={true}`
- Documentare la nuova API nelle description delle prop

### 6. Coordinamento breaking change

Questa modifica è potenzialmente una **breaking change** per i progetti che usano laif-ds:

- Verificare che le modifiche siano retrocompatibili (le nuove prop devono essere opzionali con default che preservano il comportamento attuale)
- Se ci sono breaking change inevitabili (es. cambiamento di classi CSS), documentarli nel CHANGELOG
- Coordinare con il team template per l'adozione nei progetti esistenti
- Considerare un rilascio major o minor a seconda dell'impatto
- Preparare una guida di migrazione se necessario

## Stima effort

| Fase | Ore |
|------|-----|
| Audit componenti | 3h |
| Standardizzazione prop | 8h |
| Indicatore visuale + CSS | 4h |
| Standardizzazione classi | 4h |
| Storybook | 3h |
| Coordinamento + test | 2h |
| **Totale** | **24h** |
