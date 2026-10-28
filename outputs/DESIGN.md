# hymen.ca visual system

## Direction

Soft blush pink, editorial, spacious, and grounded. The design gives sensitive information breathing room and keeps decisions with the reader. It avoids patient photography, sexualised imagery, simulated clinicians, cosmetic before/after comparisons, testimonials, and urgency cues.

## Tokens

| Token | Value | Use |
|---|---|---|
| Ink | `#502b3b` | Main text and headings |
| Deep rose | `#91425f` | Primary buttons and dark section |
| Paper | `#fff9fa` | Main background |
| Cream | `#f7e7ed` | Supporting panels |
| Blush | `#f0d4df` | Soft accents |
| Muted | `#795d69` | Secondary text |
| Line | `#e9cfd9` | Borders and separators |
| Serif | Georgia / Times New Roman | Editorial headings |
| Sans serif | Locally served DM Sans / Arial | Body and controls |

Layout width: 1280px maximum. Page gutters: 5vw, adapting to 23px on phones. Section spacing: 100px desktop, 56px phone. Most containers use square corners and borders. Primary buttons have a 2px radius. Circle arrows and region filter pills are the limited exceptions.

## Patterns

- Large image-backed hero with a layered, anatomy-inspired rose composition.
- One prominent procedure card paired with two editorial procedure rows.
- Full-width fact and Canadian-care sections to organise a long page.
- Long-form guides with a desktop table of contents and compact mobile links.
- Three-step form with progressive disclosure, an explicit local-preview notice, and disabled sample contact fields.
- No automatic animation; reduced-motion preferences suppress transitions and smooth scrolling.

Keep educational copy readable when changing typography. Pretext measures selected homepage paragraphs while CSS retains natural document flow. Branding remains consistent across operating-system colour schemes.

Educational visuals: show crescent-shaped and ring-shaped hymenal tissue as simplified schematics. Never label them by sexual history, virginity, or before/after status. Use a visible explanation and a primary-source link.

Site-wide photography: use contextual rose-toned still lifes and landscape images below interior page introductions. Preserve the homepage header and hero. Homepage editorial images belong only in lower sections. Hide decorative editorial images when printing the checklist.

Logo update: a fine-line double-petal symbol paired with a light lowercase sans-serif wordmark. Assets: `site/assets/logo.svg`, `logo-mark.svg`, and `favicon.svg`. The logo is a botanical brand symbol, not anatomical or clinical certification. Only the brand treatment changed in the homepage header; the hero is preserved.

Guided starting points: native disclosure panels beneath the homepage hero route by informational intent, without collecting symptoms or recommending treatment. Comparison uses consistently labelled cards with optional visibility controls. All content remains available without JavaScript. Mobile stacks cards vertically.

Other services uses a responsive three/two/one-column card grid, with distinct topic labels and dedicated sourced guides. The homepage hero remains unchanged.

French edition: Canadian French across content, controls, metadata and image descriptions; persistent page-matched language switch. French navigation allows extra width and long headings reflow naturally.

National city finder: province-grouped card directory with local search and a province filter; matching English/French pages. Official care resources and medical registration appear in separate panels. City photos are explicitly illustrative Canadian scenery.
