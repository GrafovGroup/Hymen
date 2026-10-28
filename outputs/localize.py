"""Build French pages from the English HTML and an explicit translation catalogue."""
from pathlib import Path
from html.parser import HTMLParser
import html, json, re
ROOT=Path(__file__).resolve().parent
SITE=ROOT/'site'
CAT=json.loads((ROOT/'fr.json').read_text())
missing=set()
def tr(value):
 key=value.strip()
 if not key:return value
 if key not in CAT:missing.add(key)
 return value[:len(value)-len(value.lstrip())]+CAT.get(key,key)+value[len(value.rstrip()):]
class Translate(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
 def handle_decl(self,d):self.parts.append('<!'+d+'>')
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  for k,v in list(a.items()):
   if v is None:continue
   if k in ('alt','aria-label','placeholder') or (t=='meta' and k=='content' and a.get('name')=='description'):a[k]=tr(v)
   if k=='href' and v.startswith('/') and not v.startswith('/assets/'):a[k]='/fr'+v
   if k in ('href','src') and v=='/assets/hymen-anatomy.svg':a[k]='/assets/hymen-anatomy-fr.svg'
  if t=='input' and a.get('name')=='language':a['value']='fr-CA'
  if t=='html':a['lang']='fr-CA'
  if t=='script' and a.get('src')=='/assets/app.js':a['src']='/assets/app-fr.js'
  self.parts.append('<'+t+''.join(' '+k if v is None else ' '+k+'="'+html.escape(v,quote=True)+'"' for k,v in a.items())+'>')
 def handle_endtag(self,t):self.parts.append('</'+t+'>')
 def handle_data(self,d):self.parts.append(html.escape(tr(d),quote=False))
 def handle_comment(self,d):self.parts.append('<!--'+d+'-->')
def language_bits(content,path,fr):
 en='https://hymen.ca'+path;french='https://hymen.ca/fr'+path
 bits=f'<link rel="canonical" href="{french if fr else en}"><link rel="alternate" hreflang="en-CA" href="{en}"><link rel="alternate" hreflang="fr-CA" href="{french}"><link rel="alternate" hreflang="x-default" href="{en}">'
 content=content.replace('</head>',bits+'</head>')
 switch=f'<a class="language-switch" lang="{"en" if fr else "fr"}" hreflang="{"en-CA" if fr else "fr-CA"}" href="{path if fr else "/fr"+path}">{"English" if fr else "Français"}</a>'
 return content.replace('<button class="menu-button"',switch+'<button class="menu-button"',1)
for p in sorted(SITE.rglob('*.html')):
 if 'fr' in p.relative_to(SITE).parts:continue
 # Strip previously generated locale metadata/switch to keep standalone reruns safe.
 raw=p.read_text()
 raw=re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>','',raw)
 raw=re.sub(r'<a class="language-switch"[^>]*>.*?</a>','',raw)
 path='/'+str(p.relative_to(SITE)).replace('index.html','')
 parser=Translate();parser.feed(raw)
 dest=SITE/'fr'/p.relative_to(SITE);dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(language_bits(''.join(parser.parts),path,True))
 p.write_text(language_bits(raw,path,False))
if missing:raise RuntimeError('Missing translations: '+repr(sorted(missing)))
print('French catalogue complete; reciprocal language links generated.')
js=(SITE/'assets/app.js').read_text()
js_terms={
 'Open navigation':'Ouvrir le menu','Close navigation':'Fermer le menu',
 "`${count} public listing${count===1?'':'s'}`":"`${count} fiche${count===1?'':'s'} publique${count===1?'':'s'}`",
 '`${checklist.filter(c=>c.checked).length} of ${checklist.length} questions checked`':'`${checklist.filter(c=>c.checked).length} question(s) cochée(s) sur ${checklist.length}`',
 'Keep at least one procedure visible. Select another procedure to compare it.':'Gardez au moins une intervention visible. Sélectionnez-en une autre pour la comparer.',
 "`Showing ${names.join(' and ')}.`":"`Interventions affichées : ${names.join(' et ')}.`",
}
for a,b in js_terms.items():
 if a not in js:raise RuntimeError('Missing JS source: '+a)
 js=js.replace(a,b)
(SITE/'assets/app-fr.js').write_text(js)
