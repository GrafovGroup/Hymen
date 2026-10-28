# Image and asset provenance

## Pink redesign

Current hero: `site/assets/rose-anatomy-hero.png`, delivered as `rose-anatomy-hero.jpg`. Generated with the built-in image generation tool. Abstract artwork, not a medical diagram.

Prompt: Create a wide 3:2 editorial illustration for a hymenoplasty patient information website. Soft blush pink background, sophisticated dusty rose, pale rose and warm ivory palette. On far right, a sculptural abstract layered paper illustration inspired by vulval folds, with a small crescent-shaped layer surrounding the lower edge of an open oval to allude to hymenal tissue. A botanical, anatomical abstraction, not a literal medical diagram. Matte paper texture, soft studio shadows, refined luxury editorial art. Left 60 percent empty blush pink for a website headline. No text, no people, no photography of genitals, no sexual scene, no before/after, no blood, no instruments. The opening must remain open, never sealed.

Educational graphic: `site/assets/hymen-anatomy.svg`. Original code-based vector schematics of crescent-shaped and ring-shaped tissue. The image generator rejected a separate anatomical diagram request; that rejected output is not used. The vector labels and descriptions follow [Cleveland Clinic's hymen anatomy explanation](https://my.clevelandclinic.org/health/body/22718-hymen). The schematics are simplified, not individual clinical assessments or indicators of sexual history.

## Original magnolia photograph (retained, no longer displayed)

Method: built-in image generation tool, single generation. Original PNG copied into the project. JPEG created for web delivery. No clinical or patient imagery is represented.

Files: `site/assets/magnolia.png` and `site/assets/magnolia.jpg`.

Prompt:

> Use case: photorealistic-natural. Asset type: wide editorial website hero background for an elegant adult women's health information website. Create a quiet, exquisite fine art still-life photograph of a single sculptural pale ivory magnolia branch with a few open magnolia blossoms and deep olive green leaves, placed on the far right side of a warm light oatmeal plaster interior, subtle sheer linen curtain at far right, natural afternoon window light, delicate botanical shadows, a simple limestone ledge along bottom. Wide horizontal 3:2 composition. Left 60 percent mostly clean warm pale ivory plaster with very soft shadow for dark headline overlay. Understated luxury editorial photography, real petal texture, slightly muted colours, organic natural composition. No people, no anatomy, no text, no logos, no medical props. Save image for use as background.

## Other assets

- DM Sans regular, served locally from the public Google Fonts distribution. SIL Open Font License included under `site/assets/licenses/`.
- Pretext 0.0.9, pinned bundled JavaScript obtained from esm.sh. MIT license included under `site/assets/licenses/`.
- Georgia is a system font; no redistributed Georgia font file.
- Favicon and line emblem are original code-based vector graphics. They are decorative, not anatomical diagrams.


## Site-wide editorial photography

Three additional visuals were created with the built-in image generation tool. The final prompts are saved in `site-image-prompts.json`.

- `site/assets/consultation.jpg`: notebook and reading glasses for consultation, enquiry, sources, privacy, and about pages.
- `site/assets/recovery.jpg`: linen robe, towels and water for procedure guides.
- `site/assets/canada.jpg`: illustrative rose-dawn mountain lake for Canadian care research. It does not represent a specific clinic location.

PNG originals are included alongside the optimized JPEG files. These are editorial illustrations, not photographs of the operator, partner clinics, or actual patients. New homepage placements are below the original header and hero, which remain unchanged.

## Soft logo

Original vector identity at `site/assets/logo.svg`, also provided as `logo.svg`. Botanical paths are hand-authored; the light wordmark uses system Helvetica Neue with Arial fallback. `logo-preview.png` provides a visual reference. This logo was created in SVG rather than with image generation.

## Editorial additions — October 2026

Generated with the built-in image generation tool and exported as locally hosted WebP. These are illustrative scenes, not actual patients or facilities.

- `personal-reflection.webp`: Adult woman, fully clothed in an ivory blouse, reading a notebook at an oak table by a window; rose and ivory palette, soft daylight, realistic editorial photography, no text, logo or clinical equipment. A 768-pixel responsive version is included.
- `quiet-space.webp`: Sunlit home corner with an ivory armchair, dusty rose throw, oak side table, journal, water and magnolia; natural editorial interior photography, no people, text or clinical equipment. A 768-pixel responsive version is included.
- `pathway-botanical.webp`, `pathway-questions.webp`, `pathway-canada.webp`: Optimized 600-pixel versions of existing site artwork for homepage navigation cards.

Original generated PNGs are retained in the generating conversation. Published responsive WebP files are under `dist/assets/`; editable project assets are under `outputs/site/assets/`.

## Procedure anatomy diagrams
Original vector schematics in `outputs/site/assets/{labiaplasty,perineoplasty}-anatomy{,-fr}.svg`, generated by `outputs/build_anatomy.py`. English and French external anatomical landmarks checked against ACOG Vulvovaginal Health (https://www.acog.org/womens-health/faqs/vulvovaginal-health), accessed 2026-10-28. These identify regions, not incision plans, before/after outcomes, or an ideal anatomy. No independent clinical review is claimed.

## Coordinated anatomy collection
`outputs/editorial_anatomy.py` creates 16 bilingual SVGs for eight guides, with rose gradients and original vector geometry. Reference URLs are recorded per guide in its GUIDES mapping and linked beside each illustration. New subjects cover hymenal shapes and variations, Bartholin gland location, vaginal opening, vulval/perianal skin landmarks, and a standalone ring pessary. Vaginismus artwork does not claim to show muscle tightening or diagnose symptoms; pessary artwork does not provide placement or sizing instructions. Reviewed against the listed patient-information sources on 2026-10-28; no independent clinical review is claimed.
