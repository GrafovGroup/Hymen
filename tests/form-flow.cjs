const fs=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
function setup({fr=false,ok=true,status=200,reject=false,valid=true,deferred=false}={}){
 const listeners={};let calls=0,resets=0,release;
 const button={textContent:'Send',disabled:false};
 const error={hidden:true,focus(){this.focused=true}},success={hidden:true,focus(){this.focused=true}};
 const form={hidden:false,elements:{_gotcha:{value:''}},action:'https://formspree.io/f/myeyblnr',attrs:{},querySelector:()=>button,reportValidity:()=>valid,addEventListener:(e,fn)=>listeners[e]=fn,setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},reset(){resets++}};
 const menu={setAttribute(){},addEventListener(){},focus(){}};
 const nav={hidden:true,querySelectorAll:()=>[]};
 const document={documentElement:{lang:fr?'fr-CA':'en-CA'},querySelector:s=>({'#consultation-form':form,'#submission-error':error,'#submission-success':success,'.menu-button':menu,'#mobile-nav':nav}[s]||null),querySelectorAll:()=>[],addEventListener(){}};
 const context={document,window:{addEventListener(){}},matchMedia:()=>({addEventListener(){}}),FormData:class{constructor(f){assert.equal(f,form)}},AbortController,setTimeout,clearTimeout,fetch:async(url,args)=>{calls++;assert.equal(url,form.action);assert.equal(args.method,'POST');assert.equal(args.credentials,'omit');assert.equal(args.referrerPolicy,'no-referrer');if(deferred)await new Promise(r=>release=r);if(reject)throw Error('offline');return {ok,status};}};
 vm.runInNewContext(fs.readFileSync('dist/assets/app'+(fr?'-fr':'')+'.js','utf8'),context);
 return {form,button,error,success,submit:()=>listeners.submit({preventDefault(){}}),calls:()=>calls,resets:()=>resets,release:()=>release()};
}
(async()=>{
 for(const fr of [false,true]){
  let x=setup({fr});await x.submit();assert.equal(x.calls(),1);assert.equal(x.form.hidden,true);assert.equal(x.success.hidden,false);assert.equal(x.success.focused,true);assert.equal(x.resets(),1);assert.equal(x.button.disabled,false);
  for(const status of [422,429]){x=setup({fr,ok:false,status});await x.submit();assert.equal(x.error.hidden,false);assert.equal(x.error.focused,true);assert.equal(x.form.hidden,false);assert.equal(x.resets(),0);assert.equal(x.button.disabled,false);assert.ok(x.error.textContent.length>10);}
  x=setup({fr,reject:true});await x.submit();assert.equal(x.error.hidden,false);assert.equal(x.resets(),0);assert.equal(x.button.disabled,false);
  x=setup({fr,valid:false});await x.submit();assert.equal(x.calls(),0);
  x=setup({fr});x.form.elements._gotcha.value='spam';await x.submit();assert.equal(x.calls(),0);
  x=setup({fr,deferred:true});const pending=x.submit();assert.equal(x.button.disabled,true);assert.equal(x.form.attrs['aria-busy'],'true');await x.submit();assert.equal(x.calls(),1);x.release();await pending;assert.equal(x.form.attrs['aria-busy'],undefined);
 }
 console.log('PASS: 14 bilingual form scenarios; success, 422, 429, offline, validation, honeypot, duplicate prevention. Mock transport only; no messages sent.');
})().catch(e=>{console.error(e);process.exitCode=1});
