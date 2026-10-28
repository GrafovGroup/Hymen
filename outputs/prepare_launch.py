"""Create a searchable production copy; keep the local preview noindex."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import shutil, json, zipfile, html, re
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parent
SOURCE, DEST = ROOT / 'site', ROOT / 'production'
verification_path = ROOT / 'search-verification.json'
verification = json.loads(verification_path.read_text()) if verification_path.exists() else {}
# Remove only obsolete files inside our generated production directory.
if DEST.exists():
    for p in DEST.rglob('*'):
        if p.is_file() and not (SOURCE / p.relative_to(DEST)).exists():
            p.unlink()
shutil.copytree(SOURCE, DEST, dirs_exist_ok=True)
# Keep full-resolution source artwork in the preview, but deliver only used assets.
references = '\n'.join(p.read_text() for p in DEST.rglob('*') if p.suffix in {'.html', '.css', '.js', '.svg', '.json'})
for p in (DEST / 'assets').glob('*.png'):
    if p.name not in references:
        p.unlink()
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML = 'http://www.w3.org/1999/xhtml'
ET.register_namespace('', NS)
ET.register_namespace('xhtml', XHTML)
root = ET.Element(f'{{{NS}}}urlset')
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links = []; self.canonical = []; self.alternates = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('href', 'src'):
            if a.get(key, '').startswith('/'): self.links.append(a[key])
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a['href'])
        if tag == 'link' and a.get('rel') == 'alternate': self.alternates.append(a)
pages = []
for p in sorted(DEST.rglob('*.html')):
    content = p.read_text()
    if p.name != '404.html':
        assert 'noindex,nofollow' in content, p
        content = content.replace('noindex,nofollow', 'index,follow,max-image-preview:large')
        if p == DEST / 'index.html' and verification.get('google'):
            tag = '<meta name="google-site-verification" content="' + html.escape(verification['google'], quote=True) + '">'
            content = content.replace('</head>', tag + '</head>', 1)
        p.write_text(content)
    parser = Links(); parser.feed(content)
    for link in parser.links:
        target = DEST / unquote(urlsplit(link).path).lstrip('/')
        if target.is_dir(): target = target / 'index.html'
        assert target.is_file(), (p, link)
    assert len(parser.canonical) == 1, p
    if p.name == '404.html': continue
    path = '/' + str(p.relative_to(DEST)).replace('index.html', '')
    assert parser.canonical[0] == 'https://hymen.ca' + path, p
    assert {a['hreflang'] for a in parser.alternates} == {'en-CA', 'fr-CA', 'x-default'}, p
    entry = ET.SubElement(root, f'{{{NS}}}url')
    ET.SubElement(entry, f'{{{NS}}}loc').text = parser.canonical[0]
    for alternate in parser.alternates:
        target = DEST / urlsplit(alternate['href']).path.lstrip('/') / 'index.html'
        assert target.exists(), alternate
        ET.SubElement(entry, f'{{{XHTML}}}link', alternate)
    pages.append(path)
ET.ElementTree(root).write(DEST / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
(DEST / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://hymen.ca/sitemap.xml\n')
if verification.get('indexnow'):
    key = verification['indexnow']
    assert re.fullmatch(r'[a-f0-9]{32}', key), 'Invalid IndexNow key'
    (DEST / (key + '.txt')).write_text(key, encoding='utf-8')
with zipfile.ZipFile(ROOT / 'hymen-ca-production.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(DEST.rglob('*')):
        if p.is_file(): z.write(p, p.relative_to(DEST))
report = {'content_pages': len(pages), 'languages': ['en-CA','fr-CA'], 'local_links_and_assets': 'passed', 'canonical_and_language_targets': 'passed', 'production_indexing': 'enabled', 'preview_indexing': 'disabled', 'deployed': False, 'real_form_delivery': 'not verified'}
(ROOT / 'launch-verification.json').write_text(json.dumps(report, indent=2)+'\n')
# OpenAI Sites serves this conventional static directory.
dist = ROOT.parent / 'dist'
if dist.exists():
    for p in dist.rglob('*'):
        if p.is_file() and not (DEST / p.relative_to(dist)).exists():
            p.unlink()
shutil.copytree(DEST, dist, dirs_exist_ok=True)
print(json.dumps(report, indent=2))
