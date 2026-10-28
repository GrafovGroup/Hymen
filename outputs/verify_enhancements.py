from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, hashlib, base64, re
ROOT=Path(__file__).resolve().parent.parent/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.ids=[]
 def handle_starttag(self,t,a):
  a=dict(a);self.tags.append((t,a))
  if 'id' in a:self.ids.append(a['id'])
count=0
for p in ROOT.rglob('*.html'):
 s=p.read_text(); parser=Page();parser.feed(s)
 assert len(parser.ids)==len(set(parser.ids)),p
 assert sum(t=='h1' for t,a in parser.tags)==1,p
 data=re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1)
 graph=json.loads(data)['@graph'];assert len(graph)>=3
 digest=base64.b64encode(hashlib.sha256(data.encode()).digest()).decode();assert 'sha256-'+digest in s,p
 assert all(a.get('content') for t,a in parser.tags if a.get('property','').startswith('og:')),p
 for t,a in parser.tags:
  if t!='a':continue
  href=a.get('href','');u=urlsplit(href)
  if u.scheme or u.netloc or not u.fragment:continue
  dest=ROOT/u.path.lstrip('/') if u.path else p
  if dest.is_dir():dest=dest/'index.html'
  target=Page();target.feed(dest.read_text());assert unquote(u.fragment) in target.ids,(p,href)
 count+=1
print(f'PASS: {count} pages; JSON-LD, CSP hashes, single H1, unique IDs, social metadata and internal anchors')
