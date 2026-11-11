const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');
const SRC='/mnt/user-data/uploads/Glamourless Systems Main/Glamourless Systems Engines/Gs-HTML Tools/';
const names=JSON.parse(fs.readFileSync('tools.json'));
(async()=>{
 const b=await chromium.launch();
 for(const n of names){
  const p=await b.newPage({viewport:{width:1000,height:800},deviceScaleFactor:2});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+SRC+n+'.html');await p.waitForTimeout(700);
  await p.screenshot({path:`toolshots/${n} A.png`});
  const h=await p.evaluate(()=>document.documentElement.scrollHeight);
  await p.evaluate(()=>window.scrollTo(0,Math.min(700,document.documentElement.scrollHeight)));await p.waitForTimeout(200);
  await p.screenshot({path:`toolshots/${n} B.png`});
  const txt=await p.evaluate(()=>document.body.innerText.slice(0,600).replace(/\s+/g,' '));
  console.log(JSON.stringify({n,h,errs:errs.length,txt}));
  await p.close();
 }
 await b.close();
})();
