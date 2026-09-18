// Runs the real config and app with a small DOM adapter; no real advertising requests.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'dist/index.html'),'utf8');
function setup(savedConsent){
 const elements=new Map(),scripts=[];
 const element=()=>({hidden:true,style:{setProperty(){}},listeners:{},addEventListener(n,f){this.listeners[n]=f;},focus(){},close(){},showModal(){}});
 const links=[...html.matchAll(/<a\b[^>]*data-contact="(whatsapp|phone)"[^>]*>/g)].map(m=>({...element(),dataset:{contact:m[1]},closest(){return null;}}));
 const document={head:{appendChild(el){scripts.push(el);}},createElement:element,documentElement:element(),getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id);},querySelector(){return null;},querySelectorAll(selector){return selector==='[data-contact]'?links:[];}};
 let stored=savedConsent;
 const window={};
 const context=vm.createContext({window,document,localStorage:{getItem(){return stored;},setItem(k,v){stored=v;}},Date,encodeURIComponent});
 for(const file of ['config.js','app.js'])vm.runInContext(fs.readFileSync(path.join(root,'dist/assets',file),'utf8'),context);
 return {window,document,links,scripts,click(id){elements.get(id).listeners.click();},conversions(){return window.dataLayer.filter(e=>e[0]==='event'&&e[1]==='conversion');}};
}
const page=setup(null);
assert.equal(page.links.length,9);
assert.equal(page.scripts.length,0,'No Google network before consent');
assert.equal(page.conversions().length,0,'No conversion on page load');
page.links.forEach(l=>l.listeners.click());
assert.equal(page.conversions().length,0,'No conversion before consent');
page.click('accept-cookies');page.click('accept-cookies');
assert.equal(page.scripts.length,1,'Only one Google script after repeated acceptance');
assert.equal(page.scripts[0].src,'https://www.googletagmanager.com/gtag/js?id=AW-979637512');
assert.equal(page.window.dataLayer.filter(e=>e[0]==='config'&&e[1]==='AW-979637512').length,1);
assert.equal(page.conversions().length,0,'Acceptance itself is not a conversion');
for(const link of page.links){
 const before=page.conversions().length;
 let prevented=false;
 link.listeners.click({preventDefault(){prevented=true;}});
 assert.equal(prevented,false,'Native navigation must not be blocked');
 assert.equal(page.conversions().length,before+1,'Exactly one conversion per click');
 const params=page.conversions().at(-1)[2];
 const expected=link.dataset.contact==='whatsapp'?'oAtYCN61l_ocEIiqkNMD':'qXYMCOG1l_ocEIiqkNMD';
 assert.equal(params.send_to,'AW-979637512/'+expected);
 if(link.dataset.contact==='phone')assert.equal(link.href,'tel:+558589414720');
 else{
  const u=new URL(link.href);assert.equal(u.hostname,'wa.me');
  assert.equal(u.searchParams.get('text'),'Olá! Encontrei vocês pelo site e gostaria de tirar uma dúvida sobre o financiamento do meu veículo.');
  assert.equal(link.target,'_blank');
 }
}
page.click('reject-cookies');
const previous=page.conversions().length;
page.links[0].listeners.click();assert.equal(page.conversions().length,previous);
page.click('accept-cookies');assert.equal(page.scripts.length,1);
const returning=setup('accepted');assert.equal(returning.scripts.length,1);assert.equal(returning.conversions().length,0);
const rejected=setup('rejected');assert.equal(rejected.scripts.length,0);
console.log('PASS: all 9 contacts, exact conversion destinations, single tag, consent, no load conversion and no navigation blocking.');
