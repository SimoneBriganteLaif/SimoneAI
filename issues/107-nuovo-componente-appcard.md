# Nuovo componente AppCard

| Campo       | Valore          |
|-------------|-----------------|
| **ID**      | 107             |
| **Stack**   | laif-ds         |
| **Tipo**    | Proposal        |
| **Status**  | In corso        |
| **Effort stimato** | 8h       |

## Descrizione originale

Farei un nuovo componente dev-friendly in modo tale da non dover chiamare tutti i componenti atomici ogni volta - Nuovo Componente AppCard.

## Piano di risoluzione

### 1. Definire l'API con subcomponenti (compound component)

Progettare l'interfaccia usando il pattern compound component:

```typescript
// Uso previsto:
<AppCard variant="elevated">
  <AppCard.Header
    title="Titolo"
    subtitle="Sottotitolo"
    avatar={<Avatar />}
    actions={<IconButton icon="more" />}
  />
  <AppCard.Body>
    {/* contenuto libero */}
  </AppCard.Body>
  <AppCard.Footer>
    <Button>Azione</Button>
  </AppCard.Footer>
</AppCard>
```

Prop principali di `AppCard`:
- `variant?: 'elevated' | 'outlined' | 'flat'`
- `padding?: 'none' | 'sm' | 'md' | 'lg'`
- `clickable?: boolean` (aggiunge hover effect e cursor pointer)
- `onClick?: () => void`
- `className?: string`

### 2. Slot predefiniti per contenuti comuni

`AppCard.Header`:
- `title: string` — titolo principale
- `subtitle?: string` — sottotitolo
- `avatar?: ReactNode` — avatar o icona a sinistra
- `actions?: ReactNode` — azioni a destra (es. menu, pulsanti)
- Layout automatico con flexbox: avatar | title+subtitle | actions

`AppCard.Body`:
- Slot libero per contenuto custom
- Padding configurabile

`AppCard.Footer`:
- Slot per azioni o informazioni aggiuntive
- Layout con allineamento a destra per i pulsanti (convenzione)
- Separatore visuale opzionale rispetto al body

### 3. Supporto varianti

Implementare tre varianti visive:

- **Elevated**: ombra (`box-shadow`), sfondo solido, nessun bordo
- **Outlined**: bordo sottile, nessuna ombra, sfondo trasparente o leggero
- **Flat**: nessun bordo, nessuna ombra, sfondo leggero (utile per card dentro altre card o su sfondo colorato)

Ogni variante deve utilizzare i design token esistenti per colori, ombre e bordi.

### 4. Responsive by default

- La card deve adattarsi alla larghezza del container
- Su viewport piccole: padding ridotto automaticamente
- Le immagini dentro il body devono essere responsive (`max-width: 100%`)
- Il layout dell'header deve gestire testi lunghi con ellipsis o wrap

### 5. Integrazione con i token del tema

Utilizzare i design token esistenti di laif-ds:

- Colori: `--card-bg`, `--card-border`, o token generici se non esistono specifici
- Ombre: `--shadow-sm`, `--shadow-md` per la variante elevated
- Spacing: token di spacing per padding e gap
- Border-radius: token di border-radius del design system
- Transizioni: token per hover/active state

### 6. Documentazione Storybook con esempi reali

Creare stories con casi d'uso concreti:

- **Basic Card**: header con titolo e body con testo
- **Card with Avatar**: header con avatar, titolo, sottotitolo e azioni
- **Card Variants**: elevated, outlined, flat a confronto
- **Clickable Card**: card cliccabile con hover effect
- **Card Grid**: griglia di card responsive (pattern comune nei progetti)
- **Minimal Card**: solo body, senza header e footer
- **Real-world Example**: card che replica un caso d'uso reale dei progetti LAIF (es. card contatto, card progetto)

## Stima effort

| Fase | Ore |
|------|-----|
| Design API + compound component setup | 1.5h |
| Implementazione AppCard + subcomponenti | 2.5h |
| Varianti + stili | 1.5h |
| Responsive + token | 1h |
| Storybook | 1.5h |
| **Totale** | **8h** |
