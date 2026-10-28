# hymen.ca launch handoff

Prepared 8 September 2026. Operator confirmed by the owner: Hymen.ca Inc.

## Production files

Upload the contents of `hymen-ca-production.zip` to the hosting web root. This archive contains 156 content pages, English and French 404 pages, local assets, robots.txt and sitemap.xml. Its canonical domain is https://hymen.ca. The original `site/` directory remains a noindex local preview.

Rebuild from this directory with `python3 build.py`, followed by `python3 prepare_launch.py`. The second command creates `production/`, the deployment archive and `launch-verification.json`. Do not deploy the preview folder accidentally.

## Domain connection

DNS observed on 8 September 2026: nameservers launch1.spaceship.net and launch2.spaceship.net; apex A records 44.232.173.249 and 52.40.42.113; www CNAME hymen.ca. No DNS records were changed.

Hosting destination is not yet confirmed. Add hymen.ca and www.hymen.ca to the chosen host, then use that host's exact DNS targets in the current DNS dashboard. Preserve email MX and TXT records. Configure HTTPS and permanent redirects from HTTP and www to https://hymen.ca, preserving paths. Configure genuine HTTP 404 responses, with the matching language error page where supported. Provider-specific DNS targets cannot be supplied until the host is selected.

## Enquiry and privacy operations

Form endpoint: https://formspree.io/f/myeyblnr. Confirm the receiving inbox, authorized account access, notification recipients, spam controls and submission retention/deletion process. Supply the privacy contact and identify the team handling requests and arranging surgeon follow-up. The confirmed operator name is already displayed in both languages. No surgeon partnership or follow-up deadline has been invented.

Use one clearly labelled synthetic launch enquiry to check live delivery; verify receipt in the configured inbox and remove the test afterward. Browser form tests have used intercepted requests only. No real test has been sent and inbox delivery remains unverified.

## Content review and search

Arrange review of the English and French clinical content by a qualified clinician and confirm service availability and provider relationships. Review privacy wording against the actual handling process. Existing sourced content is not evidence of independent clinical review.

After domain and HTTPS verification, add the domain to Google Search Console, publish its supplied verification record, submit https://hymen.ca/sitemap.xml and inspect representative English and French URLs. The production package allows indexing; indexing and rankings are not guaranteed. Local link, asset, canonical and language-target validation passed for all 156 content pages.

## Live verification

Check homepage, city hub, a city detail, a procedure, enquiry, privacy, French switching and an unknown path on mobile and desktop. Confirm 404 HTTP status, redirects, HTTPS, form delivery and tap-to-call behavior for (833) 696-9996. Verify the phone reaches the intended team before public launch.

No production deployment or DNS change has been performed by this preparation.
