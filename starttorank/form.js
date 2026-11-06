(function(){
/* Lead form. SR_WEBHOOK stays empty in staging so nothing is sent. Set it to a HighLevel inbound webhook when Doug approves. */
var SR_WEBHOOK="";
var f=document.getElementById("srf"),m=document.getElementById("srf-msg");if(!f)return;
function show(t,ok){m.textContent=t;m.className="msg show "+(ok?"ok":"err")}
f.addEventListener("submit",function(e){
 e.preventDefault();
 var v=function(id){return document.getElementById(id).value.trim()};
 if(v("s-hp"))return;
 if(!v("s-biz")||!v("s-name"))return show("Please add your business name and your name.");
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("s-email")))return show("Please enter a valid email.");
 if(v("s-phone").replace(/\D/g,"").length<10)return show("Please enter a 10-digit phone number.");
 if(!v("s-addr"))return show("Please add your business address or city.");
 if(!document.getElementById("s-ok").checked)return show("Please check the box so we can contact you.");
 var data={source:"Start to Rank page",business:v("s-biz"),name:v("s-name"),email:v("s-email"),phone:v("s-phone"),address:v("s-addr"),current_site:v("s-site"),notes:v("s-offer"),preferred_contact:f.querySelector('input[name="s-pref"]:checked').value,consent:"yes",submitted:new Date().toISOString()};
 if(!SR_WEBHOOK)return show("Staging preview: the form works, but nothing was sent. It connects when this page goes live.",true);
 var b=f.querySelector("button");b.disabled=true;
 fetch(SR_WEBHOOK,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)}).then(function(r){if(!r.ok)throw 0;f.reset();show("Thanks. We'll contact you with a time to show you your free preview.",true)}).catch(function(){show("Something went wrong and your request was not sent. Please email admin@glamourlesssystems.com.")}).then(function(){b.disabled=false});
});
})();
