const { chromium } = require('playwright');const fs=require('fs');
const SRC='/mnt/user-data/uploads/Glamourless Systems Main/Glamourless Systems Engines/Gs-HTML Tools/';
const names=JSON.parse(fs.readFileSync('tools.json'));
(async()=>{const b=await chromium.launch();const out={};
for(const n of names){const p=await b.newPage();await p.goto('file://'+SRC+n+'.html');await p.waitForTimeout(400);
out[n]=await p.evaluate(()=>{const nav=[...document.querySelectorAll('nav button, nav a, aside button, aside a, [role=tab]')].map(e=>e.innerText.trim()).filter(t=>t&&t.length<45&&!/skip/i.test(t));
const ps=[...document.querySelectorAll('main p, p')].map(e=>e.innerText.trim()).filter(t=>t.length>40).slice(0,3);
const h=[...document.querySelectorAll('main h2, main h3, h2')].map(e=>e.innerText.trim()).filter(Boolean).slice(0,12);
return {nav:[...new Set(nav)].slice(0,16),ps,h}});await p.close()}
fs.writeFileSync('toolinfo.json',JSON.stringify(out,null,1));await b.close()})();
