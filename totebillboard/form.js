(function(){
/* Lead form. TOTE_WEBHOOK stays empty in staging so nothing is sent. Set it to a HighLevel inbound webhook when Doug approves. */
var TOTE_WEBHOOK="";
var f=document.getElementById("tbf"),m=document.getElementById("tbf-msg");if(!f)return;
function show(t,ok){m.textContent=t;m.className="msg show "+(ok?"ok":"err")}
f.addEventListener("submit",function(e){
 e.preventDefault();
 var v=function(id){return document.getElementById(id).value.trim()};
 if(v("t-hp"))return;
 if(!v("t-biz")||!v("t-name"))return show("Please add your business name and your name.");
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("t-email")))return show("Please enter a valid email.");
 if(v("t-phone").replace(/\D/g,"").length<10)return show("Please enter a 10-digit phone number.");
 if(!v("t-cat"))return show("Please choose a category.");
 if(!document.getElementById("t-ok").checked)return show("Please check the box so we can contact you.");
 var data={source:"Tote Billboard page",business:v("t-biz"),name:v("t-name"),email:v("t-email"),phone:v("t-phone"),city:v("t-city"),category:v("t-cat"),offer:v("t-offer"),preferred_contact:f.querySelector('input[name="t-pref"]:checked').value,consent:"yes",submitted:new Date().toISOString()};
 if(!TOTE_WEBHOOK)return show("Staging preview: the form works, but nothing was sent. It connects when this page goes live.",true);
 var b=f.querySelector("button");b.disabled=true;
 fetch(TOTE_WEBHOOK,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)}).then(function(r){if(!r.ok)throw 0;f.reset();show("Thanks. We'll contact you with available categories, planned distribution details and next steps.",true)}).catch(function(){show("Something went wrong and your request was not sent. Please email admin@glamourlesssystems.com.")}).then(function(){b.disabled=false});
});
})();
