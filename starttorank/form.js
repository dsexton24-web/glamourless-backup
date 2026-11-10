(function(){
/* Lead form. Until SR_WEBHOOK is set to a HighLevel inbound webhook, requests open a filled-in email to admin@glamourlesssystems.com. */
var SR_WEBHOOK="";
function gsMail(subj,d){var L=[];for(var k in d){if(d[k]&&k!=="consent"&&k!=="submitted")L.push(k.replace(/_/g," ")+": "+d[k])}var u="mailto:admin@glamourlesssystems.com?subject="+encodeURIComponent(subj+" - "+(d.business||d.name||""))+"&body="+encodeURIComponent(L.join("\n"));window.location.href=u}
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
 if(!SR_WEBHOOK){gsMail("Start to Rank free preview request",data);f.reset();return show("Your email app should open with your request filled in. Press send and we will contact you. If it did not open, email admin@glamourlesssystems.com.",true)}
 var b=f.querySelector("button");b.disabled=true;
 fetch(SR_WEBHOOK,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)}).then(function(r){if(!r.ok)throw 0;f.reset();show("Thanks. We'll contact you with a time to show you your free preview.",true)}).catch(function(){show("Something went wrong and your request was not sent. Please email admin@glamourlesssystems.com.")}).then(function(){b.disabled=false});
});
})();
