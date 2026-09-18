'use strict';
const config=window.SITE_CONFIG;
const google=config.google;
const enabled=Boolean(google.tagManagerId || google.analyticsId || google.adsId);
let choice=null;
try { choice=localStorage.getItem('alcantara-consent-v1'); } catch (_) { /* Navegação sem armazenamento continua funcional. */ }
window.dataLayer=window.dataLayer || [];
function gtag(){ window.dataLayer.push(arguments); }
window.gtag=gtag;
gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
let loaded=false;
function addScript(src){const script=document.createElement('script');script.async=true;script.src=src;document.head.appendChild(script);}
function startGoogle(){
 if(!enabled || choice!=='accepted') return;
 gtag('consent','update',{analytics_storage:'granted',ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});
 if(loaded) return;
 loaded=true;
 if(google.tagManagerId){
  window.dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});
  addScript('https://www.googletagmanager.com/gtm.js?id='+encodeURIComponent(google.tagManagerId));
 }else{
  addScript('https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(google.analyticsId || google.adsId));
  gtag('js',new Date());
  if(google.analyticsId) gtag('config',google.analyticsId);
  if(google.adsId) gtag('config',google.adsId);
 }
}
const panel=document.getElementById('consent-panel');
function choose(value){choice=value;try{localStorage.setItem('alcantara-consent-v1',value);}catch(_){}panel.hidden=true;if(value==='accepted')startGoogle();else{gtag('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});}}
document.getElementById('accept-cookies').addEventListener('click',()=>choose('accepted'));
document.getElementById('reject-cookies').addEventListener('click',()=>choose('rejected'));
if(enabled && !choice) panel.hidden=false;
startGoogle();
document.querySelectorAll('[data-contact]').forEach(link=>{
 const channel=link.dataset.contact;
 link.href=channel==='whatsapp'?'https://wa.me/'+config.whatsapp+'?text='+encodeURIComponent(config.whatsappMessage):'tel:'+config.phone;
 if(channel==='whatsapp'){link.target='_blank';link.rel='noopener noreferrer';}
 link.addEventListener('click',()=>{
  if(choice!=='accepted' || !enabled)return;
  const eventName=channel==='whatsapp'?'click_whatsapp':'click_phone';
  const location=link.closest('.mobile-contact-bar')?'mobile_bar':link.closest('header')?'header':link.closest('footer')?'footer':link.closest('.hero')?'hero':'contact';
  if(google.tagManagerId)window.dataLayer.push({event:eventName,contact_channel:channel,contact_location:location});
  if(!google.tagManagerId){
   gtag('event',eventName,{contact_channel:channel,contact_location:location,transport_type:'beacon'});
   const label=channel==='whatsapp'?google.whatsappConversionLabel:google.phoneConversionLabel;
   if(google.adsId && label)gtag('event','conversion',{send_to:google.adsId+'/'+label,transport_type:'beacon'});
  }
 });
});
const dialog=document.getElementById('legal-dialog');
const copy={
 privacy:{title:'Política de Privacidade',html:'<p>Este site apresenta os serviços de Alcântara Advogados. Ao entrar em contato por telefone, e-mail ou WhatsApp, você escolhe compartilhar as informações necessárias ao atendimento.</p><p>As informações fornecidas são utilizadas para responder ao contato e analisar a solicitação, observando o sigilo profissional. O WhatsApp e outros serviços externos possuem políticas de privacidade próprias.</p><p>Se configuradas, tecnologias do Google para análise de visitas e medição de publicidade são ativadas somente após sua autorização. Você pode aceitar ou recusar essas tecnologias e alterar sua escolha abaixo.</p><p>Para dúvidas sobre seus dados ou pedidos relacionados à privacidade, escreva para <a href="mailto:advogadofortaleza@gmail.com">advogadofortaleza@gmail.com</a>.</p><button class="btn btn-outline-dark" id="manage-consent">Preferências de cookies</button>'},
 terms:{title:'Termos de Uso',html:'<p>O conteúdo deste site é informativo e não substitui a análise individual de um advogado. Nenhuma informação representa promessa ou garantia de resultado.</p><p>O envio de uma mensagem não constitui contratação de serviços nem confirma a aceitação de um caso. As condições de atendimento e eventual contratação são definidas diretamente com o escritório.</p><p>As medidas cabíveis dependem dos documentos, dos fatos e da análise jurídica de cada situação. Para orientação sobre o seu caso, utilize os canais de atendimento.</p>'}
};
document.querySelectorAll('[data-dialog]').forEach(button=>button.addEventListener('click',()=>{
 const content=copy[button.dataset.dialog];document.getElementById('dialog-title').textContent=content.title;document.getElementById('dialog-body').innerHTML=content.html;dialog.showModal();
 const manage=document.getElementById('manage-consent');if(manage)manage.addEventListener('click',()=>{dialog.close();panel.hidden=false;document.getElementById('reject-cookies').focus();});
}));
document.getElementById('close-dialog').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog){const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left || event.clientX>rect.right || event.clientY<rect.top || event.clientY>rect.bottom)dialog.close();}});

// Keep content and consent above the contact bar even with enlarged text.
const contactBar=document.querySelector('.mobile-contact-bar');
if(contactBar && 'ResizeObserver' in window){
 const observer=new ResizeObserver(entries=>{
  const height=entries[0].target.getBoundingClientRect().height;
  document.documentElement.style.setProperty('--contact-bar-height',height+'px');
 });
 observer.observe(contactBar);
}
