# Hymen.ca

Bilingual Canadian intimate-care information and consultation enquiries, operated by Hymen.ca Inc. An information resource, not a medical clinic.

## Build

Requires Python 3; no third-party Python or JavaScript packages are required.

```sh
python3 outputs/build.py
python3 outputs/prepare_launch.py
python3 outputs/verify_enhancements.py
```

Deploy `dist/` as the static document root with real 404 handling. `outputs/site/` is the noindex preview; `dist/` is the indexable production output. Do not deploy the repository root.

## Editing

- English templates: `outputs/build.py`, `outputs/build_cities.py`, `outputs/cities.json`
- French translation catalogue: `outputs/fr.json`; generation: `outputs/localize.py`
- Bilingual presentation and metadata: `outputs/enhance.py`
- Homepage composition and guide styling: `outputs/visual.py`, `outputs/site/assets/visual.css`
- Styling: `outputs/site/assets/style.css` and `elevate.css`
- Behaviour: `outputs/site/assets/app.js` (French counterpart generated)
- Domain and search verification: `outputs/prepare_launch.py`, `outputs/search-verification.json`

The build validates local links, assets, canonical URLs, language alternates, JSON-LD, Content Security Policy hashes and anchor targets. All 156 content pages have an English/French counterpart. Two additional error documents remain noindex.

## October 2026 update

Clearer homepage pathways, sticky navigation, calmer typography, summary blocks and mobile guide navigation, reduced-motion support, and a shorter enquiry-page journey. Page-specific Open Graph metadata and accurate Organization, WebSite, WebPage and BreadcrumbList structured data are rendered in HTML. Canonicals, bilingual sitemap and reciprocal hreflang remain intact. No invented clinical reviewer, clinic status, testimonials or guarantees are added.

SEO and answer-engine visibility depend on indexing, source quality and competition; no ranking or AI citation is guaranteed. Medical content and French translations still need independent clinical/editorial review. Original source-check dates are preserved.

## Enquiries

Forms use the existing public Formspree endpoint. No secrets are required by the static client. Phone and voicemail permission remain optional, and consent is explicit. No new enquiry fields, analytics or browser storage are introduced. Form delivery and receiving inbox settings need verification in the owner's Formspree account; no live test enquiries were sent during this update.

## Hosting

`.openai/hosting.json` preserves the existing Sites project identity. GitHub is a source mirror; pushing here does not automatically deploy to Sites. Run the build before publishing the generated static output. Retain local image/font licenses in `outputs/site/assets/licenses/` and `dist/assets/licenses/`.
