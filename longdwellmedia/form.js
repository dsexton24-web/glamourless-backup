(function(){
/* Lead form. LDM_WEBHOOK stays empty in staging so nothing is sent. Set it to a HighLevel inbound webhook when Doug approves. */
var LDM_WEBHOOK="";
var f=document.getElementById("ldf"),m=document.getElementById("ldf-msg");if(!f)return;
function show(t,ok){m.textContent=t;m.className="msg show "+(ok?"ok":"err")}
f.addEventListener("submit",function(e){
 e.preventDefault();
 var v=function(id){return document.getElementById(id).value.trim()};
 if(v("l-hp"))return;
 if(!v("l-biz")||!v("l-name"))return show("Please add your business name and your name.");
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("l-email")))return show("Please enter a valid email.");
 if(v("l-phone").replace(/\D/g,"").length<10)return show("Please enter a 10-digit phone number.");
 var role=f.querySelector('input[name="l-role"]:checked').value;
 if(role==="Advertiser"&&!v("l-cat"))return show("Please choose a category.");
 if(!document.getElementById("l-ok").checked)return show("Please check the box so we can contact you.");
 var data={source:"Long Dwell Media page",role:role,business:v("l-biz"),name:v("l-name"),email:v("l-email"),phone:v("l-phone"),city:v("l-city"),category:v("l-cat"),offer:v("l-offer"),preferred_contact:f.querySelector('input[name="l-pref"]:checked').value,consent:"yes",submitted:new Date().toISOString()};
 if(!LDM_WEBHOOK)return show("Staging preview: the form works, but nothing was sent. It connects when this page goes live.",true);
 var b=f.querySelector("button");b.disabled=true;
 fetch(LDM_WEBHOOK,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)}).then(function(r){if(!r.ok)throw 0;f.reset();show("Thanks. We'll contact you with open spots, participating locations and next steps.",true)}).catch(function(){show("Something went wrong and your request was not sent. Please email admin@glamourlesssystems.com.")}).then(function(){b.disabled=false});
});
})();
