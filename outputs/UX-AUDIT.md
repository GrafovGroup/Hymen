# Mobile and enquiry audit — 28 October 2026

## Implemented

- Enquiry handler identified as the hymen.ca team.
- Bilingual explanation of form processing and the next step, without promising response time, appointments, clinicians or treatment.
- Shorter enquiry introduction and expandable privacy detail; explicit contact consent remains visible and required.
- Larger disclosure, language and submit targets; scrollable mobile menu.
- Responsive WebP hero replaces the original JPG. Removed runtime text measurement and its Pretext module import; native CSS wraps text.

## Validation

All 158 generated HTML pages pass existing links, assets, canonical/language metadata checks and the enhancement verifier. Fourteen English/French form scenarios pass in Node using mocked transport: success, HTTP 422, HTTP 429, network failure, invalid fields, honeypot and concurrent submission prevention. Tests send no messages.

Chrome responsive iframe checks at 320, 390 and 768 nominal pixels covered the homepage, English enquiry, French enquiry and hymenoplasty guide: no document horizontal overflow or completed broken images. Scrollbars reduce content viewport by 15 pixels. Mobile navigation opens and closes with Escape. Process disclosure opens. This is responsive browser QA, not a physical-device test or a Lighthouse/Core Web Vitals score.

First English form field, measured from the top of the page in default disclosure state:

| Frame width | Before | After |
| --- | ---: | ---: |
| 320 px | 1484 px | 890 px |
| 390 px | 1250 px | 782 px |
| 768 px | 1131 px | 835 px |

## Remaining delivery verification

Actual Formspree receipt, recipient routing, spam placement and follow-up delivery are not verified. A narrow connected Gmail lookup for Formspree/Hymen notifications failed with a connector rate-limit error. No real test enquiry was sent. The receiving inbox address was not provided.

Owner follow-up: identify the receiving inbox, check Formspree form `myeyblnr` recipient/activation settings, and arrange one explicitly labelled nonmedical test submission and confirm receipt. Do not infer end-to-end delivery from frontend success handling.
