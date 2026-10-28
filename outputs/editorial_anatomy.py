"""Bilingual anatomical artwork. Original vectors; sources listed per guide."""
from pathlib import Path
from html import escape
import runpy
ROOT=Path(__file__).parent
A=ROOT/'site/assets'
GUIDES={
'hymenoplasty':('Hymenal tissue','Le tissu hyménal','https://my.clevelandclinic.org/health/body/22718-hymen','Cleveland Clinic'),
'hymenectomy':('Hymenal variations','Les variations de l’hymen','https://my.clevelandclinic.org/health/treatments/24563-hymenectomy','Cleveland Clinic'),
'bartholin-cyst-treatment':('The Bartholin glands','Les glandes de Bartholin','https://my.clevelandclinic.org/health/treatments/22924-marsupialization','Cleveland Clinic'),
'vaginismus-care':('The vaginal opening','L’orifice vaginal','https://www.nhs.uk/conditions/vaginismus/','NHS'),
'lichen-sclerosus-care':('Vulval skin health','La peau de la vulve','https://www.nhs.uk/conditions/lichen-sclerosus/','NHS'),
'pessary-fitting':('Vaginal support','Le soutien vaginal','https://www.yourpelvicfloor.org/conditions/vaginal-pessary-for-pelvic-organ-prolapse/','IUGA'),
'labiaplasty':('The labia of the vulva','Les lèvres de la vulve','https://www.acog.org/womens-health/faqs/vulvovaginal-health','ACOG'),
'perineoplasty':('The perineum','Le périnée','https://www.acog.org/womens-health/faqs/vulvovaginal-health','ACOG'),
}
DEFS='''<defs>
<linearGradient id="paper" x2="1" y2="1"><stop stop-color="#fffaf7"/><stop offset="1" stop-color="#f7e6ed"/></linearGradient>
<radialGradient id="silk"><stop stop-color="#fffdfa"/><stop offset="1" stop-color="#f4dbe5"/></radialGradient>
<linearGradient id="rose" x2="1" y2="1"><stop stop-color="#e7adbf"/><stop offset=".5" stop-color="#c5809b"/><stop offset="1" stop-color="#a85879"/></linearGradient>
<linearGradient id="petal" x2="1" y2="1"><stop stop-color="#fbebed"/><stop offset=".55" stop-color="#eec8d5"/><stop offset="1" stop-color="#dca5ba"/></linearGradient>
</defs>'''
def text(x,y,value,size=24,anchor='start',serif=False,color='#63404f'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{("Georgia,serif" if serif else "Arial,sans-serif")}" font-size="{size}" fill="{color}">{escape(value)}</text>'
def background():
 return DEFS+'''<rect width="1000" height="700" rx="28" fill="url(#paper)"/>
<path d="M820 -30 C1100 120 745 250 1050 390 M860 -40 C1130 110 790 270 1060 425" stroke="#c69aab" stroke-width="1" opacity=".3" fill="none"/>
<path d="M-80 390 C220 470 -50 620 240 730 M-65 370 C250 470 -15 640 270 730" stroke="#c69aab" stroke-width="1" opacity=".28" fill="none"/>
<rect x="22" y="22" width="956" height="656" rx="18" fill="none" stroke="#fff" opacity=".85"/>
'''
def start(title,sub):
 return '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="700" viewBox="0 0 1000 700" role="img" aria-labelledby="title"><title id="title">'+escape(title)+'</title>'+background()+text(58,76,title,39,serif=True)+text(60,113,sub,18,color='#987384')
def end(note):
 return '<path d="M60 608 H940" stroke="#dcc4ce"/>'+text(500,650,note,18,'middle')+'</svg>'
def label(label,x,y,tx,ty):
 endx=tx-14 if tx>500 else tx+210
 return f'<path d="M{x} {y} H{endx} V{ty-8}" fill="none" stroke="#b990a0" stroke-width="1.5"/><circle cx="{x}" cy="{y}" r="3" fill="#a56c84"/>'+text(tx,ty,label,23)
def make():
 runpy.run_path(str(ROOT/'build_anatomy.py'))
 # Restyle the checked external anatomy while preserving its landmarks.
 for fr in (False,True):
  suffix='-fr' if fr else ''
  for slug in ('labiaplasty','perineoplasty'):
   p=A/f'{slug}-anatomy{suffix}.svg';s=p.read_text().replace('<rect width="1000" height="700" rx="20" fill="#fff6f8"/>',background())
   s=s.replace('fill="#f3d9df"','fill="url(#petal)"').replace('fill="#ad4d71"','fill="url(#rose)"').replace('fill="#e8b4c3"','fill="url(#petal)"')
   p.write_text(s)
  base=(A/f'labiaplasty-anatomy{suffix}.svg').read_text()
  for slug in ('bartholin-cyst-treatment','vaginismus-care','lichen-sclerosus-care'):
   title=GUIDES[slug][1 if fr else 0]
   s=base.replace('Les lèvres de la vulve' if fr else 'The labia of the vulva',title).replace('fill="url(#rose)"','fill="url(#petal)"')
   # Replace label layer with topic-focused landmarks; diagram geometry stays fixed.
   cut=s.index('<path d="M510 184');s=s[:cut]
   if slug=='bartholin-cyst-treatment':
    s+='<g fill="url(#rose)" stroke="#b16e8a" stroke-width="2"><ellipse cx="445" cy="410" rx="13" ry="18"/><ellipse cx="555" cy="410" rx="13" ry="18"/></g><path d="M454 403 Q467 393 476 390 M546 403 Q533 393 524 390" stroke="#b16e8a" fill="none" stroke-width="3"/>'
    s+=label('Glandes de Bartholin' if fr else 'Bartholin glands',445,420,65,440)+label('Orifice vaginal' if fr else 'Vaginal opening',529,366,700,355)
    note='Glandes situées sous la peau, montrées par transparence.' if fr else 'Glands beneath the skin, shown in a transparent view.'
   elif slug=='vaginismus-care':
    s+='<ellipse cx="500" cy="366" rx="37" ry="54" fill="none" stroke="#af6181" stroke-width="3"/>'
    s+=label('Orifice vaginal' if fr else 'Vaginal opening',529,366,700,355)+label('Petites lèvres' if fr else 'Labia minora',450,340,65,300)
    note='Le resserrement musculaire involontaire n’est pas visible sur ce schéma.' if fr else 'Involuntary muscle tightening is not visible in this diagram.'
   else:
    s+='<path d="M380 240 C325 400 390 490 450 490 C418 560 442 606 500 606 C558 606 582 560 550 490 C610 490 675 400 620 240" fill="none" stroke="#ac6b88" stroke-width="2" stroke-dasharray="5 7"/>'
    s+=label('Peau de la vulve' if fr else 'Vulval skin',372,324,65,300)+label('Région périanale' if fr else 'Perianal skin',551,580,700,560)
    note='Repères de la peau à examiner; aucun diagnostic n’est représenté.' if fr else 'Skin landmarks for assessment; no diagnosis is depicted.'
   s+=text(500,650,note,18,'middle')+'</svg>'
   (A/f'{slug}-anatomy{suffix}.svg').write_text(s)
  # Hymenal tissue: educational close-ups, never before/after images.
  for slug in ('hymenoplasty','hymenectomy'):
   title=GUIDES[slug][1 if fr else 0]
   s=start(title,'Vue rapprochée · tissu à l’entrée du vagin' if fr else 'Close-up view · tissue at the vaginal entrance')
   if slug=='hymenoplasty':
    for x,kind in ((290,'crescent'),(710,'ring')):
     s+=f'<ellipse cx="{x}" cy="332" rx="157" ry="172" fill="url(#silk)" stroke="#e2becd"/>'
     if kind=='ring':s+=f'<ellipse cx="{x}" cy="332" rx="124" ry="140" fill="url(#rose)"/><ellipse cx="{x}" cy="332" rx="91" ry="109" fill="#fff9f8"/>'
     else:s+=f'<ellipse cx="{x}" cy="322" rx="120" ry="133" fill="#fff9f8"/><path d="M{x-119} 330 Q{x} 535 {x+119} 330 C{x+136} 472 {x-136} 472 {x-119} 330Z" fill="url(#rose)"/>'
     s+=text(x,325,'Orifice' if fr else 'Vaginal',20,'middle')+text(x,352,'vaginal' if fr else 'opening',20,'middle')
     s+=text(x,548,('En croissant' if fr else 'Crescent-shaped') if kind=='crescent' else ('Annulaire' if fr else 'Ring-shaped'),29,'middle',True)
    s+=end('Deux formes courantes. L’apparence ne révèle pas l’histoire sexuelle.' if fr else 'Two common shapes. Appearance cannot establish sexual history.')
   else:
    for x,kind in ((210,'septate'),(500,'micro'),(790,'imperforate')):
     s+=f'<ellipse cx="{x}" cy="335" rx="118" ry="142" fill="url(#silk)" stroke="#dfb7c7"/><ellipse cx="{x}" cy="335" rx="92" ry="116" fill="url(#rose)"/>'
     if kind=='septate':
      s+=f'<ellipse cx="{x-30}" cy="335" rx="25" ry="83" fill="#fff9f8"/><ellipse cx="{x+30}" cy="335" rx="25" ry="83" fill="#fff9f8"/>'
     elif kind=='micro':s+=f'<circle cx="{x}" cy="358" r="10" fill="#fff9f8"/>'
     names={'septate':('Septate','Cloisonné'),'micro':('Microperforate','Microperforé'),'imperforate':('Imperforate','Imperforé')}
     s+=text(x,535,names[kind][1 if fr else 0],27,'middle',True)
    s+=end('Exemples de variations nécessitant une évaluation selon les symptômes.' if fr else 'Examples of variations that may need assessment based on symptoms.')
   (A/f'{slug}-anatomy{suffix}.svg').write_text(s)
  # Device close-up: a ring pessary, not an insertion or sizing guide.
  s=start(GUIDES['pessary-fitting'][1 if fr else 0],'Un dispositif de soutien · vue du pessaire seul' if fr else 'A support device · pessary shown on its own')
  s+='<ellipse cx="500" cy="490" rx="205" ry="24" fill="#b47c94" opacity=".09"/><ellipse cx="500" cy="335" rx="173" ry="125" fill="none" stroke="#c58aa4" stroke-width="48"/><ellipse cx="500" cy="329" rx="173" ry="125" fill="none" stroke="url(#petal)" stroke-width="38"/><path d="M350 287 C395 210 561 183 637 263" stroke="#fff7f5" stroke-width="7" fill="none" stroke-linecap="round" opacity=".7"/>'
  s+=text(500,540,'Pessaire annulaire' if fr else 'Ring pessary',31,'middle',True)
  s+=end('Placé dans le vagin, cette forme de pessaire soutient les organes pelviens.' if fr else 'Placed in the vagina, this type of pessary supports the pelvic organs.')
  (A/f'pessary-fitting-anatomy{suffix}.svg').write_text(s)
 print('Created 16 coordinated anatomy illustrations')
if __name__=='__main__':make()
