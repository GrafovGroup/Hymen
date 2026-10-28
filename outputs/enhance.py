"""Bilingual UX and metadata pass. Run after localize.py, before prepare_launch.py."""
from pathlib import Path
import re, html, json, hashlib, base64
ROOT=Path(__file__).resolve().parent
SITE=ROOT/'site'
def plain(s): return html.unescape(re.sub('<[^>]+>', '', s)).strip()
def esc(s): return html.escape(s, quote=True)
for p in SITE.rglob('*.html'):
 s=p.read_text(); fr='/fr/' in str(p); prefix='/fr' if fr else ''; lang='fr-CA' if fr else 'en-CA'
 if 'data-enhanced' in s: continue
 s=s.replace('<body>', '<body data-enhanced="2026-10">')
 title=plain(re.search(r'<title>(.*?)</title>',s).group(1))
 desc=html.unescape(re.search(r'<meta name="description" content="(.*?)"',s).group(1))
 url=re.search(r'<link rel="canonical" href="(.*?)"',s).group(1)
 home=p==SITE/'index.html' or p==SITE/'fr/index.html'
 name=plain(re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1))
 if home:
  h='Des réponses claires.<br>Des choix personnels.<br><em>À votre rythme.</em>' if fr else 'Clear answers.<br>Personal choices.<br><em>At your own pace.</em>'
  s=re.sub(r'<h1>.*?</h1>', '<h1>'+h+'</h1>',s,count=1,flags=re.S)
  intro='Comprenez l’hyménoplastie, la labiaplastie et les soins pelviens au Canada. Explorez les guides, comparez vos options et préparez vos questions.' if fr else 'Understand hymenoplasty, labiaplasty and pelvic care in Canada. Explore the guides, compare your options, and prepare your questions.'
  s=re.sub(r'<p class="hero-copy">.*?</p>', '<p class="hero-copy">'+intro+'</p>',s,count=1)
  note='Une ressource indépendante d’information et de demandes, pas une clinique.' if fr else 'An independent information and enquiry resource. Not a medical clinic.'
  s=re.sub(r'<p class="hero-note">.*?</p>', '<p class="hero-note">'+note+'</p>',s,count=1)
  labels=[('hymenoplasty','Comprendre les interventions' if fr else 'Understand procedures','Explorez les guides et les sources.' if fr else 'Explore clear guides and their sources.'),('compare','Comparer mes options' if fr else 'Compare my options','Préparez une décision éclairée.' if fr else 'Make space for an informed decision.'),('cities','Trouver des ressources locales' if fr else 'Find local resources','Consultez les guides de villes au Canada.' if fr else 'Browse city guides across Canada.')]
  cards='<nav class="pathways wrap" aria-label="'+('Par où commencer' if fr else 'Choose your next step')+'">'+''.join(f'<a href="{prefix}/{slug}/"><span class="path-number">0{i+1}</span><strong>{label}</strong><span>{copy}</span><b aria-hidden="true">↗</b></a>' for i,(slug,label,copy) in enumerate(labels))+'</nav>'
  s=re.sub(r'<section class="start-section wrap".*?</section>',cards,s,count=1,flags=re.S)
 # Editorial imagery: local responsive assets; no clinical/testimonial implication.
 if home:
  for slug,asset in [('hymenoplasty','botanical'),('compare','questions'),('cities','canada')]:
   target=f'<a href="{prefix}/{slug}/"><span class="path-number">'
   replacement=f'<a href="{prefix}/{slug}/"><img class="pathway-image" src="/assets/pathway-{asset}.webp" alt="" width="600" height="400" loading="lazy" decoding="async"><span class="path-number">'
   s=s.replace(target,replacement,1)
  s=re.sub(r'<img class="editorial-inline"[^>]+>', '<figure class="reflection-figure"><img src="/assets/personal-reflection.webp" srcset="/assets/personal-reflection-768.webp 768w, /assets/personal-reflection.webp 1536w" sizes="(max-width: 900px) 90vw, 45vw" alt="'+('Une femme lit un carnet près d’une fenêtre' if fr else 'A woman reading a notebook beside a window')+'" width="1536" height="1024" loading="lazy" decoding="async"></figure>',s,count=1)
 if any('/'+slug+'/' in url for slug in ['hymenoplasty','labiaplasty','perineoplasty']):
  s=re.sub(r'<figure class="editorial-banner wrap">.*?</figure>', '<figure class="editorial-banner wrap image-enhanced"><img src="/assets/quiet-space.webp" srcset="/assets/quiet-space-768.webp 768w, /assets/quiet-space.webp 1536w" sizes="90vw" alt="'+('Un fauteuil ivoire, un plaid rose et un carnet dans une pièce lumineuse' if fr else 'An ivory armchair, rose throw and journal in a sunlit room')+'" width="1536" height="1024" loading="lazy" decoding="async"><figcaption>'+('Du temps pour réfléchir, à votre rythme.' if fr else 'Space to reflect, at your own pace.')+'</figcaption></figure>',s,count=1,flags=re.S)
 if '/consultation-guide/' in url or '/about/' in url:
  s=re.sub(r'<img([^>]*?)src="/assets/consultation.jpg"([^>]*)>', lambda m:'<img'+m[1]+'src="/assets/personal-reflection.webp"'+re.sub(r'alt="[^"]*"','alt="'+('Une femme prend le temps de lire près d’une fenêtre' if fr else 'A woman taking time to read beside a window')+'"',m[2])+'>',s)
 # Bring useful guide text before decorative imagery, keeping the original medical wording.
 article=re.search(r'<section id="[^"]+" class="article-section"><h2>(.*?)</h2><p>(.*?)</p>',s,re.S)
 if article:
  summary='<section class="quick-answer wrap" aria-label="'+('En bref' if fr else 'At a glance')+'"><p class="eyebrow">'+('EN BREF' if fr else 'AT A GLANCE')+'</p><h2>'+article.group(1)+'</h2><p>'+article.group(2)+'</p><a href="'+prefix+'/sources/">'+('Sources et approche éditoriale' if fr else 'Sources & editorial approach')+' ↗</a></section>'
  s=s.replace('<figure class="editorial-banner wrap">',summary+'<figure class="editorial-banner wrap">',1) if 'editorial-banner wrap' in s else s.replace('<div class="article-layout wrap">',summary+'<div class="article-layout wrap">',1)
  toc=re.search(r'<aside class="article-nav">(.*?)<div class="aside-note">',s,re.S)
  links=''.join(re.findall(r'<a href="#[^"]+">.*?</a>',toc.group(1))) if toc else ''
  if links:s=s.replace('<article class="article-body">','<article class="article-body"><details class="mobile-guide-nav"><summary>'+('Dans ce guide' if fr else 'In this guide')+'</summary><nav aria-label="'+('Sections du guide' if fr else 'Guide sections')+'">'+links+'</nav></details>',1)
 if '/enquiry/' in url:
  s=re.sub(r'<figure class="editorial-banner wrap">.*?</figure>','',s,count=1,flags=re.S)
  guidance='Choisissez un sujet et vos coordonnées. Les champs obligatoires sont indiqués par *. Aucune histoire médicale ni photo.' if fr else 'Choose a topic and how to reach you. Required fields are marked *. No medical history or photos.'
  s=s.replace('<form id="consultation-form"','<p class="form-intro">'+guidance+'</p><form id="consultation-form"',1)
  s=s.replace('id="main"','id="main" class="enquiry-main"',1)
  heading='Commencez par une conversation.' if fr else 'Start with a conversation.'
  intro='Indiquez un sujet et les coordonnées auxquelles vous souhaitez recevoir une réponse.' if fr else 'Choose a topic and the contact details you are comfortable using for a reply.'
  s=re.sub(r'<h1>.*?</h1>', '<h1>'+heading+'</h1>',s,count=1,flags=re.S)
  s=re.sub(r'<p class="intro-copy">.*?</p>', '<p class="intro-copy">'+intro+'</p>',s,count=1,flags=re.S)
  process_title='Que se passe-t-il après l’envoi?' if fr else 'What happens after I send this?'
  process='Votre demande est transmise par Formspree à l’équipe hymen.ca. L’équipe peut vous contacter avec les coordonnées fournies pour discuter de votre demande. L’envoi ne confirme ni rendez-vous, ni chirurgien, ni traitement.' if fr else 'Your enquiry is sent through Formspree to the hymen.ca team. The team can contact you using the details you provide to discuss your request. Submitting does not confirm an appointment, surgeon or treatment.'
  process_html='<details class="enquiry-process"><summary>'+process_title+'</summary><p>'+process+'</p></details>'
  owner='Demandes traitées par l’équipe hymen.ca.' if fr else 'Enquiries handled by the hymen.ca team.'
  s=s.replace('<p class="form-intro">','<p class="enquiry-owner">'+owner+'</p>'+process_html+'<p class="form-intro">',1)
  s=re.sub(r'<div class="discretion-note"><h3>(.*?)</h3>(.*?)</div>',r'<details class="discretion-note privacy-disclosure"><summary>\1</summary>\2</details>',s,count=1,flags=re.S)
  # Retain required consent disclosures beside the submit action.
  s=re.sub(r'<p class="form-intro">.*?</p>','',s,count=1,flags=re.S)
  s=s.replace('<section id="submission-success"', '<section id="submission-success"',1)
 # Serve a smaller hero asset; native CSS text wrapping avoids JS layout work.
 s=s.replace('src="/assets/rose-anatomy-hero.jpg"', 'src="/assets/rose-hero.webp" srcset="/assets/rose-hero-768.webp 768w, /assets/rose-hero.webp 1536w" sizes="100vw"')

 # Real organization/site/page entities only; never claim clinic status or medical review.
 graph=[{'@type':'Organization','@id':'https://hymen.ca/#organization','name':'Hymen.ca Inc.','url':'https://hymen.ca/','logo':'https://hymen.ca/assets/logo.svg'}, {'@type':'WebSite','@id':'https://hymen.ca/#website','url':'https://hymen.ca/','name':'hymen.ca','inLanguage':['en-CA','fr-CA'],'publisher':{'@id':'https://hymen.ca/#organization'}}, {'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':lang,'isPartOf':{'@id':'https://hymen.ca/#website'}}]
 if not home and p.name!='404.html':graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Accueil' if fr else 'Home','item':'https://hymen.ca'+prefix+'/'},{'@type':'ListItem','position':2,'name':name,'item':url}]})
 data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 digest=base64.b64encode(hashlib.sha256(data.encode()).digest()).decode()
 s=re.sub(r'(<meta http-equiv="Content-Security-Policy" content=")(.*?)(">)', lambda m:m[1]+html.unescape(m[2])+m[3], s)
 s=s.replace("script-src 'self';", "script-src 'self' 'sha256-"+digest+"';")
 meta=''.join(f'<meta property="{key}" content="{esc(value)}">' for key,value in {'og:type':'website','og:site_name':'hymen.ca','og:title':title,'og:description':desc,'og:url':url,'og:locale':'fr_CA' if fr else 'en_CA','og:locale:alternate':'en_CA' if fr else 'fr_CA','og:image':'https://hymen.ca/assets/consultation.jpg','og:image:alt':'Carnet pour préparer vos questions' if fr else 'Notebook for preparing your questions'}.items())
 meta+='<meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">'+data+'</script><link rel="stylesheet" href="/assets/elevate.css">'
 s=s.replace('</head>',meta+'</head>')
 s=s.replace('content="index,follow"','content="index,follow,max-image-preview:large"')
 p.write_text(s)
print('Enhanced bilingual UX and metadata')
