"""Original, simplified external anatomy schematics; no surgical outcome depiction.
Landmarks: https://www.acog.org/womens-health/faqs/vulvovaginal-health
Procedure scope: Cleveland Clinic labiaplasty (21953), perineoplasty (23183).
"""
from pathlib import Path
from html import escape
out=Path(__file__).parent/'site/assets'
for procedure in ('labiaplasty','perineoplasty'):
 for fr in (False,True):
  lab=procedure=='labiaplasty'
  title=('Les lèvres de la vulve' if fr else 'The labia of the vulva') if lab else ('Le périnée' if fr else 'The perineum')
  labels=[('Capuchon du clitoris' if fr else 'Clitoral hood',540,176,700,137),('Orifice urétral' if fr else 'Urethral opening',508,270,700,250),('Orifice vaginal' if fr else 'Vaginal opening',529,366,700,367),('Grandes lèvres' if fr else 'Labia majora',372,324,72,240),('Petites lèvres' if fr else 'Labia minora',450,340,72,365),('Périnée' if fr else 'Perineum',539,484,700,485),('Anus',521,565,700,580)]
  color='#ad4d71'; inner=color if lab else '#e8b4c3'; peri=color if not lab else '#f3d9df'
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="700" viewBox="0 0 1000 700" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{('Vue externe simplifiée. La zone concernée est mise en évidence.' if fr else 'Simplified external view. The relevant area is highlighted.')}</desc>
<rect width="1000" height="700" rx="20" fill="#fff6f8"/>
<text x="56" y="66" font-family="Georgia,serif" font-size="35" fill="#502b3b">{title}</text>
<text x="56" y="101" font-family="Arial,sans-serif" font-size="18" fill="#795d69">{('Vue externe · repères anatomiques' if fr else 'External view · anatomical landmarks')}</text>
<g stroke-linejoin="round" stroke-linecap="round">
<path d="M500 137 C420 127 361 190 350 288 C334 398 373 461 449 477 C474 485 489 473 500 454 C511 473 526 485 551 477 C627 461 666 398 650 288 C639 190 580 127 500 137Z" fill="#f3d9df" stroke="#d4a1b2" stroke-width="2"/>
<path d="M498 179 C459 193 435 232 422 290 C409 352 432 406 477 433 C460 390 458 354 464 311 C469 264 478 221 498 179Z" fill="{inner}" stroke="#b56b86" stroke-width="2"/>
<path d="M502 179 C541 193 565 232 578 290 C591 352 568 406 523 433 C540 390 542 354 536 311 C531 264 522 221 502 179Z" fill="{inner}" stroke="#b56b86" stroke-width="2"/>
<path d="M473 199 Q500 150 527 199 Q500 181 473 199Z" fill="#e6acbe" stroke="#b56b86" stroke-width="2"/>
<circle cx="500" cy="213" r="7" fill="#ba758c"/>
<ellipse cx="500" cy="270" rx="8" ry="6" fill="#79505f"/>
<ellipse cx="500" cy="366" rx="28" ry="43" fill="#9c6478" stroke="#c28b9f" stroke-width="5"/>
<path d="M462 455 Q500 469 538 455 L544 513 Q500 535 456 513Z" fill="{peri}" stroke="{'#93415f' if not lab else '#d4a1b2'}" stroke-width="2"/>
<ellipse cx="500" cy="565" rx="22" ry="15" fill="#d5a0b2" stroke="#b57a8e" stroke-width="2"/>
<path d="M488 565 Q500 558 512 565" fill="none" stroke="#79505f" stroke-width="3"/>
</g>
'''
  for label,x,y,tx,ty in labels:
   end=tx-14 if tx>500 else tx+210
   start=x
   # Connect the clitoral hood label to the hood, not the outer labium.
   if y==176: start=510;y=184
   svg+=f'<path d="M{start} {y} L{end} {y} L{end} {ty-8}" fill="none" stroke="#a77c8d" stroke-width="1.5"/><circle cx="{start}" cy="{y}" r="3" fill="#79505f"/><text x="{tx}" y="{ty}" font-family="Arial,sans-serif" font-size="24" fill="#502b3b">{escape(label)}</text>\n'
  svg+=f'<text x="500" y="650" text-anchor="middle" font-family="Arial,sans-serif" font-size="19" fill="#795d69">{("Schéma simplifié. L’anatomie varie d’une personne à l’autre." if fr else "Simplified diagram. Anatomy varies from person to person.")}</text></svg>'
  (out/f'{procedure}-anatomy{"-fr" if fr else ""}.svg').write_text(svg)
print('Created four bilingual anatomy diagrams')
