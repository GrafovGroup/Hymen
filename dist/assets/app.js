import {prepare, layout} from './pretext.js';

// All assets are local. No analytics, persistence, or enquiry network requests.
const menuButton = document.querySelector('.menu-button');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu(){mobileNav.hidden=true;menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label','Open navigation')}
menuButton.addEventListener('click',()=>{const open=mobileNav.hidden;mobileNav.hidden=!open;menuButton.setAttribute('aria-expanded',String(open));menuButton.setAttribute('aria-label',open?'Close navigation':'Open navigation')});
mobileNav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!mobileNav.hidden){closeMenu();menuButton.focus()}});
matchMedia('(min-width:901px)').addEventListener('change',e=>{if(e.matches)closeMenu()});

// Pretext provides resize-aware paragraph measurement; natural CSS remains the fallback.
document.fonts.ready.then(()=>{
  const elements=[...document.querySelectorAll('.hero-copy,.section-heading>p')];
  const handles=new Map();
  function measure(){
    for(const el of elements){
      const style=getComputedStyle(el);
      const key=style.font;
      let cached=handles.get(el);
      if(!cached||cached.key!==key){cached={key,handle:prepare(el.textContent,key)};handles.set(el,cached)}
      const result=layout(cached.handle,el.clientWidth,parseFloat(style.lineHeight));
      el.style.minHeight=`${Math.ceil(result.height)}px`;
    }
  }
  new ResizeObserver(measure).observe(document.body);measure();
}).catch(()=>{/* Readable natural text layout remains available. */});

const filters=[...document.querySelectorAll('[data-filter]')];
const cards=[...document.querySelectorAll('[data-region]')];
function filterProviders(region){
  if(!['all','ontario','quebec','other'].includes(region))region='all';
  filters.forEach(b=>{const active=b.dataset.filter===region;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))});
  let count=0;cards.forEach(card=>{const visible=region==='all'||card.dataset.region===region;card.hidden=!visible;if(visible)count++});
  document.querySelector('#results-count').textContent=`${count} public listing${count===1?'':'s'}`;
  document.querySelector('#no-providers').hidden=count>0;
}
filters.forEach(button=>button.addEventListener('click',()=>filterProviders(button.dataset.filter)));
if(filters.length){
  filterProviders(location.hash.slice(1));
  window.addEventListener('hashchange',()=>filterProviders(location.hash.slice(1)));
}

const checklist=[...document.querySelectorAll('.check-group input')];
function updateChecks(){document.querySelector('#check-progress').textContent=`${checklist.filter(c=>c.checked).length} of ${checklist.length} questions checked`}
checklist.forEach(c=>c.addEventListener('change',updateChecks));
document.querySelector('.reset-checks')?.addEventListener('click',()=>{checklist.forEach(c=>c.checked=false);updateChecks()});
document.querySelector('#print-checklist')?.addEventListener('click',()=>window.print());

// Content selection only: no assessment, storage or requests.
const compareButtons=[...document.querySelectorAll('[data-compare]')];
if(compareButtons.length){
 document.querySelector('.compare-controls').hidden=false;
 const status=document.querySelector('#compare-status');
 compareButtons.forEach(button=>button.addEventListener('click',()=>{
  const selected=compareButtons.filter(b=>b.getAttribute('aria-pressed')==='true');
  const wasSelected=button.getAttribute('aria-pressed')==='true';
  if(wasSelected&&selected.length===1){status.textContent='Keep at least one procedure visible. Select another procedure to compare it.';return}
  button.setAttribute('aria-pressed',String(!wasSelected));
  document.querySelector(`[data-procedure="${button.dataset.compare}"]`).hidden=wasSelected;
  const names=compareButtons.filter(b=>b.getAttribute('aria-pressed')==='true').map(b=>b.textContent);
  status.textContent=`Showing ${names.join(' and ')}.`;
 }));
}

// The city finder filters public guide links only; nothing is stored or submitted.
const citySearch=document.querySelector('#city-search');
if(citySearch){
 const isFrench=document.documentElement.lang==='fr-CA';
 const cityProvince=document.querySelector('#city-province');
 const cityCards=[...document.querySelectorAll('[data-city-region]')];
 const cityGroups=[...document.querySelectorAll('[data-city-group]')];
 const normalizeCity=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
 document.querySelector('.city-controls').hidden=false;
 function updateCities(){
  const query=normalizeCity(citySearch.value);let count=0;
  cityCards.forEach(card=>{
   const region=card.dataset.cityRegion;
   const provinceLabel=cityProvince.querySelector(`option[value="${region}"]`).textContent;
   const match=normalizeCity(card.querySelector('h3').textContent+' '+provinceLabel+' '+region);
   const visible=(cityProvince.value==='all'||region===cityProvince.value)&&query.split(' ').every(word=>match.includes(word));
   card.hidden=!visible;if(visible)count++;
  });
  cityGroups.forEach(group=>group.hidden=![...group.querySelectorAll('[data-city-region]')].some(card=>!card.hidden));
  document.querySelector('#city-count').textContent=isFrench?`${count} ${count===1?'guide local':'guides locaux'}`:`${count} city guide${count===1?'':'s'}`;
  document.querySelector('#city-empty').hidden=count>0;
 }
 citySearch.addEventListener('input',updateCities);cityProvince.addEventListener('change',updateCities);
 document.querySelector('#clear-city-filters').addEventListener('click',()=>{citySearch.value='';cityProvince.value='all';updateCities();citySearch.focus()});
 window.addEventListener('pageshow',()=>{citySearch.value='';cityProvince.value='all';updateCities()});
 updateCities();
}

// Native POST is the no-JavaScript fallback; fetch keeps the bilingual result on-page.
const consultation=document.querySelector('#consultation-form');
if(consultation){
 const fr=document.documentElement.lang==='fr-CA';
 const submit=consultation.querySelector('[type=submit]');
 const initialLabel=submit.textContent;
 const error=document.querySelector('#submission-error');
 const success=document.querySelector('#submission-success');
 let sending=false;
 consultation.addEventListener('submit',async event=>{
  event.preventDefault();if(sending||!consultation.reportValidity())return;
  if(consultation.elements._gotcha.value)return;
  sending=true;submit.disabled=true;consultation.setAttribute('aria-busy','true');error.hidden=true;
  submit.textContent=fr?'Envoi en cours…':'Sending…';
  const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),25000);
  try{
   const response=await fetch(consultation.action,{method:'POST',body:new FormData(consultation),headers:{Accept:'application/json'},credentials:'omit',referrerPolicy:'no-referrer',signal:controller.signal});
   if(!response.ok){
    error.textContent=response.status===429?(fr?'Trop de demandes. Veuillez patienter avant de réessayer.':'Too many requests. Please wait before trying again.'):(fr?'Le service n’a pas accepté la demande. Vérifiez vos renseignements et réessayez.':'The service did not accept your request. Check your details and try again.');
    error.hidden=false;error.focus();return;
   }
   consultation.reset();consultation.hidden=true;success.hidden=false;success.focus();
  }catch{
   error.textContent=fr?'Nous n’avons pas pu confirmer l’envoi. Vos renseignements restent dans ce formulaire. Vérifiez votre connexion avant de réessayer; la première demande a peut-être été reçue.':'We could not confirm delivery. Your details remain in this form. Check your connection before trying again; the first request may have been received.';
   error.hidden=false;error.focus();
  }finally{clearTimeout(timer);sending=false;submit.disabled=false;submit.textContent=initialLabel;consultation.removeAttribute('aria-busy')}
 });
 consultation.addEventListener('reset',()=>{error.hidden=true});
 window.addEventListener('pagehide',()=>consultation.reset());
 window.addEventListener('pageshow',event=>{if(event.persisted){consultation.reset();consultation.hidden=false;success.hidden=true}});
}
