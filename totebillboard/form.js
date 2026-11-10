(function(){
/* Lead form. Until TOTE_WEBHOOK is set to a HighLevel inbound webhook, requests open a filled-in email to admin@glamourlesssystems.com. */
var TOTE_WEBHOOK="";
function gsMail(subj,d){var L=[];for(var k in d){if(d[k]&&k!=="consent"&&k!=="submitted")L.push(k.replace(/_/g," ")+": "+d[k])}var u="mailto:admin@glamourlesssystems.com?subject="+encodeURIComponent(subj+" - "+(d.business||d.name||""))+"&body="+encodeURIComponent(L.join("\n"));window.location.href=u}
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
 if(!TOTE_WEBHOOK){gsMail("Tote Billboard request",data);f.reset();return show("Your email app should open with your request filled in. Press send and we will contact you. If it did not open, email admin@glamourlesssystems.com.",true)}
 var b=f.querySelector("button");b.disabled=true;
 fetch(TOTE_WEBHOOK,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)}).then(function(r){if(!r.ok)throw 0;f.reset();show("Thanks. We'll contact you with available categories, planned distribution details and next steps.",true)}).catch(function(){show("Something went wrong and your request was not sent. Please email admin@glamourlesssystems.com.")}).then(function(){b.disabled=false});
});
})();
