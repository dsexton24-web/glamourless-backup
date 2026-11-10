# Builds the GS Start to Rank page: page.html, starttorank.js (HighLevel loader), index.html (preview), hl-block.html
import json, html
esc = html.escape
CSS = open('style.css').read()
FORMJS = open('form.js').read()

FAQ = [
("Do I pay anything before I see the preview?", "No. We build your preview first, from your real Google reviews and photos. You only pay if you want it to go live."),
("Will this get me to number one on Google?", "Nobody can honestly promise that. We build your site the way search engines and customers like: fast, mobile friendly, with your real services, town and reviews. Rankings depend on many things, including your reviews and how long your business has been listed."),
("Who owns the website and the domain?", "You do. The domain is bought in your name, and the site runs on a systeme.io account in your name. We are added as a team member to do the work."),
("Do you need my passwords?", "No. You invite us as a team member on systeme.io and share domain access on Namecheap. We never ask for or keep your passwords."),
("Can I make changes myself?", "Your Care Plan covers updates. Send us what to change, like a new photo, price or seasonal offer, and we handle it."),
("How fast can it go live?", "Usually within a few days of your OK. Connecting a domain can take 24 to 48 hours on the internet's side."),
("What does the CRM actually do?", "It catches every lead from your site in one place, replies right away, follows up until they book, sends booking reminders, asks happy customers for a review and checks in with past customers. All automatic."),
("Can you text back missed calls?", "Yes, as an add-on. Texting needs a business phone line and carrier registration, so we set that up separately through HighLevel."),
("What if I want to leave?", "You keep your domain and your account. If you want the website files to take elsewhere, you can buy them out. Ask us for the buyout price."),
]
faq = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)

page = f'''<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<div id="gssr">

<section class="hero"><div class="w hg">
 <div>
  <span class="kick">GS Start to Rank</span>
  <h1>Get found. Get called. <span>Get booked.</span></h1>
  <p class="lead">A real website built from your real reviews, plus the follow-up system most local businesses never set up. See your free preview before you pay a dime.</p>
  <div class="cta2"><a class="btn" href="#ask">Get My Free Preview</a><a class="btn ghost" href="#how">See How It Works</a></div>
  <ul class="chips"><li>Free preview first</li><li>You own it</li><li>No passwords needed</li></ul>
 </div>
 <div class="own" style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18)">
  <h3>What you get</h3>
  <ul>
   <li>A mobile-first website built around what your customers already say about you</li>
   <li>Your domain connected and your site live</li>
   <li>A CRM that catches every lead in one place</li>
   <li>Five follow-up automations running from day one</li>
   <li>Updates handled for you every month</li>
  </ul>
 </div>
</div></section>

<section class="s"><div class="w">
 <div class="sh"><h2>Great reviews. No website.</h2><p>Plenty of local businesses do great work and have the reviews to prove it, but when someone searches, there is nothing to click.</p></div>
 <div class="stat"><b>38%</b><p>In our November 2026 check of 230 local businesses around Port Huron, 88 had no website on their Google listing, or only a Facebook or directory page.<small>Source: GS review of Google Business Profile listings in Port Huron, Marysville and Fort Gratiot.</small></p></div>
</div></section>

<section class="s alt" id="how"><div class="w">
 <div class="sh"><h2>How it works</h2><p>You see it before you buy it.</p></div>
 <div class="steps">
  <div class="step"><b>1</b><h3>Free preview</h3><p>We research your business and your top local competitors, then build a preview from your real reviews, photos and services.</p></div>
  <div class="step"><b>2</b><h3>You approve</h3><p>Tell us what to change. Nothing goes live until you say so.</p></div>
  <div class="step"><b>3</b><h3>Quick setup</h3><p>You open a free systeme.io account and buy your domain. We walk you through it and you add us as a team member.</p></div>
  <div class="step"><b>4</b><h3>Go live</h3><p>We connect your domain, add your lead form and turn on your follow-up system.</p></div>
 </div>
</div></section>

<section class="s"><div class="w">
 <div class="sh"><h2>The website</h2><p>Built to turn a search into a phone call.</p></div>
 <div class="gets">
  <div class="get"><h3>Built from your real story</h3><p>Your services, your service area, your photos and the things customers praise in your reviews. Nothing made up.</p></div>
  <div class="get"><h3>Studied against your competition</h3><p>We look at the strongest competitors near you, learn what works, find what they miss, and build yours to stand out. We never copy.</p></div>
  <div class="get"><h3>Made for phones</h3><p>Tap-to-call buttons, fast loading and a simple quote form, because most of your customers find you on their phone.</p></div>
 </div>
</div></section>

<section class="s alt"><div class="w">
 <div class="sh"><h2>The CRM and automations</h2><p>Every business needs these. Almost nobody sets them up.</p></div>
 <div class="auto">
  <div class="get"><h3>Instant reply</h3><p>New leads get a reply right away and you get notified.</p></div>
  <div class="get"><h3>Follow-up</h3><p>A short email follow-up until they book or answer.</p></div>
  <div class="get"><h3>Booking reminders</h3><p>Confirmations and reminders so fewer people forget.</p></div>
  <div class="get"><h3>Review requests</h3><p>Mark a job done and happy customers get asked for a review.</p></div>
  <div class="get"><h3>Win-back</h3><p>Past customers get a friendly check-in down the road.</p></div>
 </div>
</div></section>

<section class="s" id="price"><div class="w">
 <div class="sh"><h2>Pricing</h2><p>Simple and upfront. The preview is free.</p></div>
 <div class="prices">
  <div class="price"><span class="pt">Website and CRM setup</span><div class="amt">$499</div><p>One time. Website, domain connection, lead form, CRM and the five automations.</p></div>
  <div class="price"><span class="pt">Care Plan</span><div class="amt">$99<small style="font-size:20px">/mo</small></div><p>Updates, new photos and offers, and keeping your automations running.</p></div>
 </div>
 <ul class="terms"><li>Your domain is bought in your name and paid to the registrar directly, usually a small yearly fee.</li><li>systeme.io's free plan covers the site and CRM for most small businesses.</li><li>Missed-call text-back is available as an add-on.</li></ul>
</div></section>

<section class="s alt"><div class="w">
 <div class="own">
  <h3>You own everything</h3>
  <ul><li>Your domain is in your name.</li><li>Your systeme.io account is in your name.</li><li>We work as an invited team member. We never ask for your passwords.</li><li>Want to leave? You keep your domain and account, and you can buy the site files.</li></ul>
 </div>
</div></section>

<section class="s" id="ask"><div class="w">
 <div class="sh"><h2>Get your free preview</h2><p>Tell us where to find your business. We will build your preview and reach out to show it to you.</p></div>
 <form class="rf" id="srf" novalidate>
  <div class="fld"><label for="s-biz">Business name</label><input id="s-biz" autocomplete="organization"></div>
  <div class="fld"><label for="s-name">Your name</label><input id="s-name" autocomplete="name"></div>
  <div class="fld full"><label for="s-addr">Business address or city</label><input id="s-addr" autocomplete="street-address"></div>
  <div class="fld"><label for="s-email">Email</label><input id="s-email" type="email" autocomplete="email"></div>
  <div class="fld"><label for="s-phone">Phone</label><input id="s-phone" type="tel" autocomplete="tel"></div>
  <div class="fld full"><label for="s-site">Current website or Facebook page (if any)</label><input id="s-site" placeholder="Leave blank if you don't have one"></div>
  <div class="fld full"><label for="s-offer">Anything we should know?</label><textarea id="s-offer" placeholder="Services you want to highlight, towns you serve, anything else"></textarea></div>
  <div class="fld full"><label>Best way to reach you</label><div class="rad"><label><input type="radio" name="s-pref" value="Phone" checked> Phone</label><label><input type="radio" name="s-pref" value="Email"> Email</label><label><input type="radio" name="s-pref" value="Text"> Text</label></div></div>
  <input type="text" id="s-hp" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
  <div class="fld full"><label class="chk"><input type="checkbox" id="s-ok"><span>Glamourless Systems may contact me about my free preview by phone, email or text. Message and data rates may apply. Reply STOP to opt out of texts.</span></label></div>
  <div class="msg" id="srf-msg" role="status" aria-live="polite"></div>
  <div class="fld full"><button class="btn" type="submit">Get My Free Preview</button></div>
 </form>
</div></section>

<section class="s alt" id="faq"><div class="w nar">
 <div class="sh"><h2>Questions</h2></div>
 {faq}
</div></section>

</div>
'''
open('page.html', 'w').write(page)
js = ('/* GS Start to Rank page loader. Source of truth: Drive folder GS Start to Rank Source Code. */\n(function(){\n'
"var root=document.getElementById('gssr-mount');if(!root){root=document.createElement('div');root.id='gssr-mount';var anchor=[].slice.call(document.querySelectorAll('script')).filter(function(x){return !x.src&&x.textContent.indexOf('starttorank.js')>=0})[0];if(anchor&&anchor.parentNode){anchor.parentNode.insertBefore(root,anchor)}else{document.body.appendChild(root)}}\n"
f"root.innerHTML={json.dumps(page)};\n{FORMJS}\n"
"var g=document.getElementById('gssr');var p=root.parentElement;for(var i=0;i<8&&p&&p!==document.body;i++){if(/c-section|c-row|c-column|inner|custom-code/.test(p.className||'')){p.style.paddingTop='0';p.style.paddingBottom='0';p.style.marginTop='0';p.style.marginBottom='0';p.style.maxWidth='none'}p=p.parentElement}\n"
"try{document.documentElement.style.overflowX='hidden';document.body.style.overflowX='hidden'}catch(e){}\n"
"function fit(){g.style.marginLeft='0';var r=root.getBoundingClientRect();g.style.width=document.documentElement.clientWidth+'px';g.style.marginLeft=(-r.left)+'px'}\n"
"fit();window.addEventListener('resize',fit);window.addEventListener('load',fit);setTimeout(fit,800);\n})();\n")
open('starttorank.js', 'w').write(js)
open('index.html', 'w').write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Start to Rank | Glamourless Systems</title><style>body{margin:0}</style></head><body><script>var s=document.createElement("script");s.src="starttorank.js?v=2";document.body.appendChild(s);</script></body></html>\n')
open('hl-block.html', 'w').write('<script>var s=document.createElement("script");s.src="https://dsexton24-web.github.io/glamourless-backup/starttorank/starttorank.js?v=2";document.body.appendChild(s);</script>\n')
