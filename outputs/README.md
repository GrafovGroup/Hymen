# hymen.ca website

Static, bilingual website with 78 English and 78 Canadian French content pages. Includes procedure guides, specialist topics, 60 city/urban-area guides per language, public provider research, and a consultation request form.

## Build and preview

Serve `site/` as the web root. All images, fonts, styles and scripts are local. Rebuild using:

```sh
python3 build.py
```

Keep `build.py`, `build_cities.py`, `cities.json`, `localize.py` and `fr.json` together. The French catalogue is explicit; missing translations fail the build. Styles live in `site/assets/style.css`; edit `site/assets/app.js` and rebuild to generate its French counterpart.

## Consultation delivery

The English and French forms POST to `https://formspree.io/f/myeyblnr`. Native fetch provides localized in-page feedback, a busy state, duplicate-submit protection and retry messages. Without JavaScript, standard HTML POST sends to the same endpoint and uses Formspree’s hosted response.

Fields: topic, province, city, preferred name, email, optional phone, optional voicemail permission, adult confirmation, contact consent and page language. Email is always required. An absent voicemail_permission field means voicemail is not authorized. There is no medical-history field or upload. Contact consent is separate from voicemail permission and does not include marketing.

The content security policy allows connections and form actions to https://formspree.io. The public form ID is intended to appear in client HTML; no private credential is included. A `_gotcha` honeypot is included. Requests use Accept: application/json; no third-party JavaScript dependency is loaded.

In your Formspree dashboard, verify the receiving email, notification workflow, activation status, spam settings and any domain restrictions. Configure any surgeon/clinic forwarding there only for recipients authorized to handle these requests. The site does not promise a particular surgeon or response time. Formspree account activation, plan limits, retention, recipient configuration and actual email delivery have not been verified from this workspace.

## Verification

`formspree-verification.json` records the current form checks: required fields, English/French payloads, consent, success, 422/429 failures, network failure, duplicate prevention, input clearing and a no-JavaScript POST. Every test POST was intercepted locally; no test enquiry was delivered. `verification.json` records the earlier full 156-page layout and navigation run; its preview-form checks predate this integration.

The local website remains noindex with robots crawling blocked. Canonical and reciprocal language links use the intended hymen.ca domain. Publishing and enabling search indexing are separate from this form connection.

## Content and assets

The website is not a clinic. Provider listings are public research links and do not establish a partnership or availability. City pages distinguish public health navigation from verified procedure listings. Clinical content and the French translation have not received independent clinical review. See `ASSETS.md`, `DESIGN.md` and `CITY-COVERAGE.md` for supporting details.

The standard contact number is (833) 696-9996, linked with `tel:+18336969996` in the top bar, footer and consultation page in both languages.

Privacy-sensitive presentation: the homepage and consultation prompts acknowledge the personal nature of intimate care. A prominent form note explains general-topic selection, optional phone/voicemail and Formspree processing; an email helper asks visitors to use an address suitable for replies. These statements do not promise anonymity or absolute confidentiality.

## Production preparation

Run `python3 prepare_launch.py` after rebuilding. This creates a separate searchable `production/` directory and `hymen-ca-production.zip`, including a bilingual sitemap. The `site/` preview stays noindex. See `LAUNCH.md` for domain setup, outstanding operational details and live checks. Hymen.ca Inc. is the confirmed website operator.
