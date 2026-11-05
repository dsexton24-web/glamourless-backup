/* Glamourless Systems backup site glue. Rewrites product links from the assessment results.
   SKU links go to the Payhip page in payhip-links.js when one is set, otherwise to checkout.html. */
(function(){
var MAP=window.GS_PAYHIP||{};
function skuOf(a){var h=a.getAttribute('href')||'';var m=h.match(/GS-\d{4}/i);if(m)return m[0].toUpperCase();
 var card=a.parentElement;for(var i=0;i<6&&card;i++){var c=card.querySelector('a[href*="checkout.html?sku="]');
 if(c){var mm=c.getAttribute('href').match(/GS-\d{4}/i);if(mm)return mm[0].toUpperCase()}card=card.parentElement}return null}
function dest(s){return MAP[s]||('checkout.html?sku='+s)}
function fix(){
 document.querySelectorAll('a[href]').forEach(function(a){if(a.getAttribute('data-gsb'))return;var h=a.getAttribute('href');
  if(/(^|\/)blueprint\/[^\/]+\.html/.test(h)||/checkout\.html\?sku=/.test(h)||/\/blueprint\?sku=GS-\d{4}/i.test(h)){var s=skuOf(a);if(s){a.setAttribute('href',dest(s));a.setAttribute('data-gsb','1')}}});
 var INTERNAL=/Internal review flags|workflow tags \(internal\)|STAGING TEST MODE|Staging checkout\.|Staging only|Flagged for human review/;
 document.querySelectorAll('body *:not(script):not(style):not(template)').forEach(function(e){if(e.children.length===0&&e.style.display!=='none'&&INTERNAL.test(e.textContent)){var b=e.closest('p,div,li,section')||e;b.style.display='none'}});
 document.querySelectorAll('.card').forEach(function(c){var b=c.querySelector('b');if(b&&/^Narrow to three/i.test(b.textContent.trim()))c.remove()});
}
var t=null;new MutationObserver(function(){if(t)return;t=setTimeout(function(){t=null;fix()},200)}).observe(document.documentElement,{childList:true,subtree:true});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fix);else fix();
})();
