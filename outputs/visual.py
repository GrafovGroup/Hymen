"""Presentation pass over localized content; retain all permanent content routes."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent/'site'
for p in ROOT.rglob('*.html'):
 s=p.read_text();fr='fr' in p.relative_to(ROOT).parts;prefix='/fr' if fr else ''
 if '/assets/visual.css' in s:continue
 home=p in (ROOT/'index.html',ROOT/'fr/index.html')
 if home:
  s=s.replace('<main id="main">','<main id="main" class="home-refined">')
  links=[('#procedures','Les interventions' if fr else 'Explore procedures'),('/compare/','Comparer les options' if fr else 'Compare options'),('/cities/','Ressources locales' if fr else 'Find local resources')]
  nav='<nav class="quick-paths wrap" aria-label="'+('Par où commencer' if fr else 'Choose your next step')+'">'+''.join('<a href="'+(href if href.startswith('#') else prefix+href)+'"><span>'+label+'</span><span aria-hidden="true">↗</span></a>' for href,label in links)+'</nav>'
  s=re.sub(r'<nav class="pathways wrap".*?</nav>',nav,s,count=1,flags=re.S)
  data=[('hymenoplasty','Hyménoplastie' if fr else 'Hymenoplasty','pathway-botanical.webp','Comprendre la reconstruction de l’hymen, ses limites et les questions à poser.' if fr else 'Understand hymen reconstruction, its limitations and the questions to ask.'),('labiaplasty','Labiaplastie' if fr else 'Labiaplasty','labiaplasty-magnolia.png','Explorer la chirurgie des lèvres, les variations normales et les autres options.' if fr else 'Explore labial surgery, normal variation and alternatives.'),('perineoplasty','Périnéoplastie' if fr else 'Perineoplasty','perineoplasty-peony.png','Comprendre les préoccupations périnéales et préparer une évaluation individuelle.' if fr else 'Understand perineal concerns and prepare for an individual assessment.')]
  cards='<div class="guide-card-grid">'+''.join(f'<a class="guide-card" href="{prefix}/{slug}/"><div class="guide-card-image"><img src="/assets/{asset}" alt="" width="600" height="400" loading="lazy" decoding="async"></div><div class="guide-card-copy"><span class="guide-card-index">0{i+1} / '+(('Guide principal' if fr else 'Main guide') if i==0 else ('Guide pratique' if fr else 'Procedure guide'))+f'</span><h3>{title}</h3><p>{desc}</p><span class="guide-card-action">'+('Lire le guide' if fr else 'Read the guide')+' <span aria-hidden="true">↗</span></span></div></a>' for i,(slug,title,asset,desc) in enumerate(data))+'</div>'
  # Replace the old asymmetric card group, bounded by its section's closing tag.
  s=re.sub(r'<div class="procedure-grid">.*?</section>',cards+'</section>',s,count=1,flags=re.S)
  # Keep specialist routes discoverable in a compact topic list.
  old=re.search(r'<section id="other-services".*?</section>',s,re.S)
  if old:
   topics=re.findall(r'<a class="other-service-card" href="([^"]+)">.*?<h3>(.*?)</h3>',old.group(),re.S)
   compact='<section id="other-services" class="topic-strip wrap"><div><p class="eyebrow">'+('POUR ALLER PLUS LOIN' if fr else 'MORE TO EXPLORE')+'</p><h2>'+('D’autres questions?' if fr else 'Other questions on your mind?')+'</h2></div><div class="topic-links">'+''.join(f'<a href="{url}">{name}<span aria-hidden="true">↗</span></a>' for url,name in topics)+'</div></section>'
   s=s[:old.start()]+compact+s[old.end():]
  # Detailed anatomy stays in the permanent procedure guides; combine local navigation.
  s=re.sub(r'<section class="anatomy-feature wrap">.*?</section>','',s,count=1,flags=re.S)
  s=re.sub(r'<section class="wrap city-home section">.*?</section>','',s,count=1,flags=re.S)
  # Keep italic emphasis in the hero only; simplify lower-page heading hierarchy.
  hero_end=s.find('</section>',s.find('<section class="hero"'))+10
  tail=s[hero_end:];tail=re.sub(r'<h2>(.*?)</h2>',lambda m:'<h2>'+m[1].replace('<em>','').replace('</em>','').replace('<br>',' ')+'</h2>',tail,flags=re.S)
  s=s[:hero_end]+tail
 # Match the procedure banners to the floral card artwork.
 for slug,asset,en_alt,fr_alt in [
  ('labiaplasty','labiaplasty-magnolia.png','Blush magnolia blossom with gently layered petals','Fleur de magnolia rose aux pétales délicatement superposés'),
  ('perineoplasty','perineoplasty-peony.png','Soft pink peony with rounded layers of petals','Pivoine rose aux pétales arrondis et superposés'),
 ]:
  if p.parent.name==slug:
   flower='<figure class="editorial-banner wrap image-enhanced"><img src="/assets/'+asset+'" alt="'+(fr_alt if fr else en_alt)+'" width="1536" height="1024" loading="lazy" decoding="async"></figure>'
   s=re.sub(r'<figure class="editorial-banner wrap image-enhanced">.*?</figure>',flower,s,count=1,flags=re.S)
 # Style source, question and risk sections without altering their clinical content.
 s=re.sub(r'<section id="(questions|risks|expectations)" class="article-section">',r'<section id="\1" class="article-section guide-highlight">',s)
 s=s.replace('<link rel="stylesheet" href="/assets/elevate.css">','<link rel="stylesheet" href="/assets/elevate.css"><link rel="stylesheet" href="/assets/visual.css">')
 p.write_text(s)
print('Applied bilingual visual system')
